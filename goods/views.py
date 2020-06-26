from django.core.paginator import Paginator
from django.shortcuts import render

from goods.models import GoodsCategory, GoodsInfo


def index(request):

    gdcategories = GoodsCategory.objects.all()

    for cag in gdcategories:
        cag.goods_list = cag.goodsinfo_set.order_by('-id')[:4]

    cart_goods_list = []
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)

    return render(request, 'index.html', {'dcag': gdcategories,
                                          'cart_goods_list': cart_goods_list,
                                          'cart_goods_count': cart_goods_count})

def detail(request):
    gdcategories = GoodsCategory.objects.all()
    cart_goods_list = []
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)

    goods_id = request.GET.get('id',1)
    goods_data = GoodsInfo.objects.get(id=goods_id)

    return render(request, 'detail.html', {'dcag': gdcategories,
                                           'cart_goods_list' : cart_goods_list,
                                           'cart_goods_count' : cart_goods_count,
                                           'goods_data' : goods_data})

def goods(request):
    cag_id = request.GET.get('cag', 1)
    page_id = request.GET.get('page', 1)

    current_cag = GoodsCategory.objects.get(id=cag_id)
    goods_data = GoodsInfo.objects.filter(goods_cag_id=cag_id)
    paginator = Paginator(goods_data, 4)
    page_data = paginator.page(page_id)

    gdcategories = GoodsCategory.objects.all()

    cart_goods_list = []
    cart_goods_count = 0
    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)

    return render(request, 'goods.html', {'current_cag': current_cag,
                                         'page_data': page_data,
                                         'dcag': gdcategories,
                                         'cart_goods_list': cart_goods_list,
                                         'cart_goods_count': cart_goods_count,
                                         'paginator': paginator,
                                         'cag_id': cag_id})