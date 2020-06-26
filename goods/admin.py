from django.contrib import admin

from .models import GoodsCategory, GoodsInfo


@admin.register(GoodsCategory)
class GoodsCategoryAdmin(admin.ModelAdmin):
    list_display = ['cag_name','cag_css']

@admin.register(GoodsInfo)
class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['goods_name','goods_price','goods_stock','goods_cag']
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = True
    search_fields = ['id','goods_name']