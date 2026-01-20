from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import InboundRecord, Item
from ..serializers import InboundRecordSerializer
from .base import _Page, _success, _to_date, _to_int


class InboundRecordViewSet(viewsets.ModelViewSet):
    queryset = InboundRecord.objects.all()
    serializer_class = InboundRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["item", "inbound_date"]
    search_fields = ["item__item_name", "supplier"]
    ordering_fields = ["inbound_date", "created_at"]


@api_view(["GET"])
@permission_classes([AllowAny])
def inbound_list(request):
    paginator = _Page()
    queryset = InboundRecord.objects.select_related("item", "operator").all().order_by("-id")
    search = request.query_params.get("search") or request.query_params.get("q")
    if search:
        queryset = queryset.filter(
            Q(item__item_name__icontains=search)
            | Q(supplier__icontains=search)
            | Q(operator__username__icontains=search)
        )
    page = paginator.paginate_queryset(queryset, request)
    rows = []
    for rec in page:
        rows.append({
            "id": rec.id,
            "itemId": rec.item_id,
            "itemName": rec.item.item_name,
            "quantity": rec.quantity,
            "inboundDate": rec.inbound_date,
            "supplier": rec.supplier,
            "operatorName": rec.operator.username if rec.operator else "",
            "remark": rec.remark,
        })
    payload = {
        "list": rows,
        "total": paginator.page.paginator.count if paginator.page else queryset.count(),
        "page": paginator.page.number if paginator.page else 1,
        "size": paginator.get_page_size(request),
    }
    return Response(_success(payload))


@api_view(["POST"])
@permission_classes([AllowAny])
def inbound_add(request):
    item_id = request.data.get("itemId") or request.data.get("item")
    item = get_object_or_404(Item, pk=item_id)
    quantity = _to_int(request.data.get("quantity"), 0)
    inbound_date = _to_date(request.data.get("inboundDate") or request.data.get("date"))
    record = InboundRecord.objects.create(
        item=item,
        quantity=quantity,
        supplier=request.data.get("supplier") or "",
        inbound_date=inbound_date,
        operator=request.user if getattr(request, "user", None) and request.user.is_authenticated else None,
        remark=request.data.get("remark") or "",
    )
    return Response(_success({
        "id": record.id,
        "itemId": item.id,
        "itemName": item.item_name,
        "quantity": record.quantity,
        "inboundDate": record.inbound_date,
        "supplier": record.supplier,
        "operatorName": record.operator.username if record.operator else "",
        "remark": record.remark,
    }, "入库成功"))
