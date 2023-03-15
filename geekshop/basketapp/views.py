from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse

# @login_required
# def basket_add(request, pk):
#     if 'login' in request.META.get('HTTP_REFERER'):
#         return HttpResponseRedirect(reverse('products:product', args=[pk]))
#
#     product = get_object_or_404(Product, pk=pk)
#     basket = Basket.objects.filter(user=request.user, product=product).first()
#
#     if not basket:
#         basket = Basket(user=request.user, product=product)
#
#     basket.quantity += 1
#     basket.save()
#
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
# def is_ajax(request):
#     return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
def basket_add(request, pk):
    user_select = request.user
    product = Product.objects.get(pk=pk)
    baskets = Basket.objects.filter(user=user_select, product=product)
    # old_basket_item = Basket.get_product(user=request.user, product=product)
    # if old_basket_item:
    #     old_basket_item[0].quantity += 1
    #     old_basket_item[0].save()
    if baskets:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    else:
        Basket.objects.create(user=user_select, product=product, quantity=1)

    products = Product.objects.all()
    content = {'products': products}

    result = render_to_string('mainapp/includes/products_list.html', content)
    return JsonResponse({'result': result})


@login_required
def basket(request):
    title = 'корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category').select_related()

    content = {
        'title': title,
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/basket.html', content)


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))
        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()
        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {
            'basket_items': basket_items,
        }
        result = render_to_string('basketapp/includes/inc_basket_list.html', content)
        return JsonResponse({'result': result})


