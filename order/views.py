from django.shortcuts import render, get_object_or_404
from .models import *
from members.models import User as mUser
from cart.cart import Cart
from .forms import OrderCreateForm
#from coupon.forms import SelectCouponForm
from shop.models import *
from django.views.decorators.csrf import csrf_exempt
from coupon.models import *
@csrf_exempt
def order_create(request): # 주문서 입력
    cart = Cart(request)
    user = mUser.objects.get(id=request.user.id)
    coupons = CouponUser.objects.filter(user=user)
    print(request)
    if request.method == 'POST': #place order 버튼 눌렀을 떄
        print(request)
        order_create_form = OrderCreateForm(user)
        if order_create_form.is_valid():
            order = order_create_form.save()
            print("here")
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], option=item['option'], price=item['price'], quantity=item['quantity'])
            '''if 'price_post' in request.POST:
                price = request.POST['price_post']
            order_price = Order.objects.get(order=order)
            order_price.price = price
            order_price.save()'''
    else:
        order_create_form = OrderCreateForm(user)


    '''if coupon_select_form.is_valid():
        order_without_coupon = Order.objects.get(id=order)'''

    return render(request, 'order/create.html', {'cart' : cart, 'order_create_form' : order_create_form,'coupons':coupons})

def order_complete(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)
    print ("*****************test start*******************")
    orderitems = OrderItem.objects.filter(order=order)
    for orderitem in orderitems:
        orderitem.product.count_order+=orderitem.quantity
        orderitem.product.save()
    return render(request, 'order/created.html', {'order': order})

from django.views.generic.base import View
from django.http import JsonResponse

class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        print("-----------------")
        print("start")
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)
        print("finish")
        cart = Cart(request)
        user = mUser.objects.get(id=request.user.id)

        order_create_form = OrderCreateForm(user)

        if order_create_form.is_valid():
            print("valid")
            order = order_create_form.save()
            print("save")
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], option=item['option'], price=item['price'], quantity=item['quantity'])
                print(item)
                print("item")

            cart.clear()
            data = {
                "order_id": order.id
            }

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

# 결제 정보 생성
class OrderCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        amount = request.POST.get('amount')

        try:
            merchant_order_id = OrderTransaction.objects.create_new(
                order=order,
                amount=amount
            )
        except:
            merchant_order_id = None

        if merchant_order_id is not None:
            data = {
                "works": True,
                "merchant_id": merchant_order_id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

# 결제 검증
class OrderImpAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        try:
            trans = OrderTransaction.objects.get(
                order=order,
                merchant_order_id=merchant_id,
                amount=amount
            )
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            trans.success = True
            trans.save()
            order.paid = True
            order.save()

            data = {
                "works" : True
            }

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required # 관리자 권한이 있을때만 호출 가능
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/admin/detail.html', {'order': order})

'''
# pdf 만들기
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('order/admin/pdf.html', {'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATICFILES_DIRS[0]+'/css/pdf.css')])
    return response
'''