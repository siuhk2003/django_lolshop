from django.shortcuts import render
from django.shortcuts import redirect
from goods.models import GoodsInfo
from goods.models import GoodsCategory
from .models import OrderInfo
from .models import OrderGoods
import time


def add_cart(request):
    goods_id = request.GET.get('id', '')
    if goods_id:
        prev_url = request.META['HTTP_REFERER']
        response = redirect(prev_url)
        goods_count = request.COOKIES.get(goods_id, '')
        if goods_count:
            goods_count = int(goods_count) + 1
        else:
            goods_count = 1

        response.set_cookie(goods_id, goods_count)

    return response


def show_cart(request):
    cart_goods_list = []
    cart_goods_count = 0
    cart_goods_money = 0
    out = 0
    for goods_id, goods_num in request.COOKIES.items():

        if not goods_id.isdigit():
            continue

        cart_goods = GoodsInfo.objects.get(id=goods_id)

        if cart_goods.goods_stock < int(goods_num):
            out = 1
            cart_goods.outstock = "存貨不夠"

        cart_goods.goods_num = goods_num
        cart_goods.total_money = int(goods_num) * cart_goods.goods_price
        cart_goods_list.append(cart_goods)
        cart_goods_count += int(goods_num)
        cart_goods_money += int(goods_num) * cart_goods.goods_price

    return render(request, 'cart.html', {'cart_goods_list': cart_goods_list,
                                         'cart_goods_count': cart_goods_count,
                                         'cart_goods_money': cart_goods_money})


def remove_cart(request):

    goods_id = request.GET.get('id', '')
    if goods_id:
        prev_url = request.META['HTTP_REFERER']
        response = redirect(prev_url)
        goods_count = request.COOKIES.get(goods_id, '')
        if goods_count:
            response.delete_cookie(goods_id)

    return response


def place_order(request):
    cart_goods_list = []
    cart_goods_count = 0
    cart_goods_money = 0
    prev_url = request.META['HTTP_REFERER']
    response = redirect(prev_url)
    out = 0
    for goods_id, goods_num in request.COOKIES.items():

        if not goods_id.isdigit():
            continue

        cart_goods = GoodsInfo.objects.get(id=goods_id)

        if cart_goods.goods_stock < int(goods_num):
            out = 1

        cart_goods.goods_num = goods_num
        cart_goods.total_money = int(goods_num) * cart_goods.goods_price
        cart_goods_list.append(cart_goods)
        cart_goods_count = cart_goods_count + int(goods_num)
        cart_goods_money += int(goods_num) * cart_goods.goods_price

    if out == 1:
        return response
    else:
        return render(request, 'place_order.html', {'cart_goods_list': cart_goods_list,
                                                    'cart_goods_count': cart_goods_count,
                                                    'cart_goods_money': cart_goods_money})


def submit_order(request):
    addr = request.POST.get('addr', '')
    recv = request.POST.get('recv', '')
    tele = request.POST.get('tele', '')
    extra = request.POST.get('extra', '')

    order_info = OrderInfo()
    order_info.order_addr = addr
    order_info.order_tele = tele
    order_info.order_recv = recv
    order_info.order_extra = extra
    order_info.order_id = str(int(time.time() * 1000)) + str(int(time.process_time() * 1000000))
    order_info.save()

    response = redirect('/cart/submit_success/?id=%s' % order_info.order_id)

    for goods_id, goods_num in request.COOKIES.items():
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        order_goods = OrderGoods()
        order_goods.goods_info = cart_goods
        order_goods.goods_order = order_info
        order_goods.goods_num = goods_num
        order_goods.save()
        response.delete_cookie(goods_id)

    return response


def submit_success(request):
    order_id = request.GET.get('id')

    order_info = OrderInfo.objects.get(order_id=order_id)
    order_goods_list = OrderGoods.objects.filter(goods_order=order_info)

    total_money = 0
    total_num = 0
    for goods in order_goods_list:
        goods.total_money = goods.goods_num * goods.goods_info.goods_price
        total_money += goods.total_money
        total_num += goods.goods_num

    return render(request, 'success.html', {'order_info': order_info,
                                            'order_goods_list': order_goods_list,
                                            'total_money': total_money,
                                            'total_num': total_num})
