from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Item, OutboundRecord
from ..serializers import OutboundRecordSerializer
from .base import _Page, _success, _to_date, _to_int


class OutboundRecordViewSet(viewsets.ModelViewSet):
    queryset = OutboundRecord.objects.all()
    serializer_class = OutboundRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["item", "outbound_date"]
    search_fields = ["item__item_name", "receiver"]
    ordering_fields = ["outbound_date", "created_at"]


@api_view(["GET"])
@permission_classes([AllowAny])
def outbound_list(request):
    paginator = _Page()
    queryset = OutboundRecord.objects.select_related("item").all().order_by("-id")
    search = request.query_params.get("search") or request.query_params.get("q")
    if search:
        queryset = queryset.filter(
            Q(item__item_name__icontains=search) | Q(receiver__icontains=search)
        )
    page = paginator.paginate_queryset(queryset, request)
    rows = []
    for rec in page:
        rows.append({
            "id": rec.id,
            "itemId": rec.item_id,
            "itemName": rec.item.item_name,
            "quantity": rec.quantity,
            "outboundDate": rec.outbound_date,
            "receiver": rec.receiver,
            "reason": rec.reason,
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
def outbound_add(request):
    item_id = request.data.get("itemId") or request.data.get("item")
    item = get_object_or_404(Item, pk=item_id)
    quantity = _to_int(request.data.get("quantity"), 0)
    outbound_date = _to_date(request.data.get("outboundDate") or request.data.get("date"))
    record = OutboundRecord.objects.create(
        item=item,
        quantity=quantity,
        outbound_date=outbound_date,
        receiver=request.data.get("receiver") or "",
        reason=request.data.get("reason") or "",
        operator=None,
    )
    return Response(_success({
        "id": record.id,
        "itemId": item.id,
        "itemName": item.item_name,
        "quantity": record.quantity,
        "outboundDate": record.outbound_date,
        "receiver": record.receiver,
        "reason": record.reason,
    }, "出库成功"))
