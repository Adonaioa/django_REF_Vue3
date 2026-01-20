from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    """物品模型"""
    # 分类、单位仅在前端做限制，后端不再限制 choices
    CATEGORY_CHOICES = []
    UNIT_CHOICES = []

    item_code = models.CharField(max_length=50, unique=True, verbose_name='物品编号')
    item_name = models.CharField(max_length=100, verbose_name='物品名称')
    category = models.CharField(max_length=20, verbose_name='分类')
    specification = models.CharField(max_length=200, blank=True, verbose_name='规格型号')
    unit = models.CharField(max_length=10, default='个', verbose_name='单位')
    initial_stock = models.IntegerField(default=0, verbose_name='初始库存')
    current_stock = models.IntegerField(default=0, verbose_name='当前库存')
    min_stock = models.IntegerField(default=10, verbose_name='最低库存预警')
    location = models.CharField(max_length=100, blank=True, verbose_name='存放位置')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'warehouse_item'
        verbose_name = '物品'
        verbose_name_plural = '物品列表'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.item_code} - {self.item_name}"


class InboundRecord(models.Model):
    """入库记录模型"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='物品')
    quantity = models.IntegerField(verbose_name='数量')
    supplier = models.CharField(max_length=100, verbose_name='供应商')
    inbound_date = models.DateField(verbose_name='入库日期')
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='操作员')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'warehouse_inbound'
        verbose_name = '入库记录'
        verbose_name_plural = '入库记录列表'
        ordering = ['-inbound_date', '-created_at']
    
    def __str__(self):
        return f"{self.item.item_name} - 入库{self.quantity}{self.item.unit}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 更新库存
        self.item.current_stock += self.quantity
        self.item.save()


class OutboundRecord(models.Model):
    """出库记录模型"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='物品')
    quantity = models.IntegerField(verbose_name='数量')
    receiver = models.CharField(max_length=100, verbose_name='领用人')
    outbound_date = models.DateField(verbose_name='出库日期')
    reason = models.TextField(verbose_name='出库原因')
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='操作员')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        db_table = 'warehouse_outbound'
        verbose_name = '出库记录'
        verbose_name_plural = '出库记录列表'
        ordering = ['-outbound_date', '-created_at']
    
    def __str__(self):
        return f"{self.item.item_name} - 出库{self.quantity}{self.item.unit}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 更新库存
        self.item.current_stock -= self.quantity
        self.item.save()
