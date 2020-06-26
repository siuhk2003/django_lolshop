from django.contrib import admin
from .models import OrderInfo, OrderGoods

@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['order_id','order_addr','order_recv',
                    'order_tele','order_fee','order_extra','order_status']

@admin.register(OrderGoods)
class OrderGoodsAdmin(admin.ModelAdmin):
    list_display = ['goods_order','goods_num','goods_info']