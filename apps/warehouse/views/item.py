import csv
import io

from django.db import models, transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Item
from ..serializers import ItemSerializer
from .base import _Page, _error, _read_upload_rows, _success, _to_date, _to_int


def _normalize_item_payload(data):
    return {
        "item_code": data.get("itemCode") or data.get("item_code"),
        "item_name": data.get("itemName") or data.get("item_name"),
        "category": data.get("category") or "其他",
        "specification": data.get("specification") or "",
        "unit": data.get("unit") or "个",
        "initial_stock": _to_int(data.get("initialStock") or data.get("initial_stock"), 0),
        "current_stock": _to_int(data.get("currentStock") or data.get("current_stock"), 0),
        "min_stock": _to_int(data.get("minStock") or data.get("min_stock"), 10),
        "location": data.get("location") or "",
        "remark": data.get("remark") or "",
    }


def _item_to_front(obj: Item):
    return {
        "id": obj.id,
        "itemCode": obj.item_code,
        "itemName": obj.item_name,
        "category": obj.category,
        "specification": obj.specification,
        "unit": obj.unit,
        "initialStock": obj.initial_stock,
        "currentStock": obj.current_stock,
        "minStock": obj.min_stock,
        "location": obj.location,
        "remark": obj.remark,
        "createdAt": obj.created_at,
        "updatedAt": obj.updated_at,
    }


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "unit"]
    search_fields = ["item_code", "item_name"]
    ordering_fields = ["created_at", "current_stock"]

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        items = self.queryset.filter(current_stock__lte=models.F("min_stock"))
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def statistics(self, request):
        total_items = self.queryset.count()
        total_stock = sum(item.current_stock for item in self.queryset)
        low_stock_count = self.queryset.filter(current_stock__lte=models.F("min_stock")).count()
        return Response({
            "total_items": total_items,
            "total_stock": total_stock,
            "low_stock_count": low_stock_count,
            "normal_stock_count": total_items - low_stock_count,
        })


@api_view(["GET"])
@permission_classes([AllowAny])
def stock_list(request):
    paginator = _Page()
    queryset = Item.objects.all().order_by("-id")
    search = request.query_params.get("search") or request.query_params.get("q")
    if search:
        queryset = queryset.filter(Q(item_code__icontains=search) | Q(item_name__icontains=search))
    page = paginator.paginate_queryset(queryset, request)
    items = [_item_to_front(obj) for obj in page]
    payload = {
        "list": items,
        "total": paginator.page.paginator.count if paginator.page else queryset.count(),
        "page": paginator.page.number if paginator.page else 1,
        "size": paginator.get_page_size(request),
    }
    return Response(_success(payload))


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([AllowAny])
def stock_detail(request, pk: int):
    item = get_object_or_404(Item, pk=pk)

    if request.method in ["PUT", "PATCH"]:
        payload = _normalize_item_payload(request.data)
        serializer = ItemSerializer(item, data=payload, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_success(None, "更新成功"))

    if request.method == "DELETE":
        item.delete()
        return Response(_success(None, "删除成功"))

    return Response(_success(_item_to_front(item)))


@api_view(["POST"])
@permission_classes([AllowAny])
def stock_add(request):
    payload = _normalize_item_payload(request.data)
    if payload["current_stock"] == 0:
        payload["current_stock"] = payload["initial_stock"]
    serializer = ItemSerializer(data=payload)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    item = Item.objects.get(pk=serializer.instance.pk)
    return Response(_success(_item_to_front(item), "添加成功"))


@api_view(["POST"])
@permission_classes([AllowAny])
def stock_import(request):
    upload = request.FILES.get("file")
    if not upload:
        return Response(_error("缺少文件"), status=400)

    rows, err = _read_upload_rows(upload)
    if err:
        return Response(_error(err), status=400)

    created, updated, errors = 0, 0, []
    with transaction.atomic():
        for idx, row in enumerate(rows, start=1):
            code = (row.get("item_code") or "").strip()
            name = (row.get("item_name") or "").strip()
            if not code or not name:
                errors.append(f"第{idx}行缺少 item_code 或 item_name")
                continue

            # 名称重复校验：数据库已存在同名则拒绝导入该行
            if Item.objects.filter(item_name=name).exists():
                errors.append(f"第{idx}行物品名称已存在: {name}")
                continue

            defaults = {
                "item_name": name,
                "category": (row.get("category") or "其他").strip(),
                "specification": (row.get("specification") or "").strip(),
                "unit": (row.get("unit") or "个").strip(),
                "initial_stock": _to_int(row.get("initial_stock") or row.get("current_stock"), 0),
                "current_stock": _to_int(row.get("current_stock"), 0),
                "min_stock": _to_int(row.get("min_stock"), 10),
                "location": (row.get("location") or "").strip(),
                "remark": (row.get("remark") or "").strip(),
            }

            obj, created_flag = Item.objects.update_or_create(
                item_code=code,
                defaults=defaults,
            )
            if created_flag:
                created += 1
            else:
                updated += 1

    result = {"created": created, "updated": updated, "errors": errors}
    return Response(_success(result, "导入完成"))


@api_view(["GET"])
@permission_classes([AllowAny])
def stock_export(request):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "item_code",
        "item_name",
        "category",
        "specification",
        "unit",
        "initial_stock",
        "current_stock",
        "min_stock",
        "location",
        "remark",
        "created_at",
        "updated_at",
    ])
    for item in Item.objects.all().order_by("-id"):
        writer.writerow([
            item.item_code,
            item.item_name,
            item.category,
            item.specification,
            item.unit,
            item.initial_stock,
            item.current_stock,
            item.min_stock,
            item.location,
            item.remark,
            item.created_at.isoformat(),
            item.updated_at.isoformat(),
        ])
    response = HttpResponse(output.getvalue(), content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="stock.csv"'
    return response
