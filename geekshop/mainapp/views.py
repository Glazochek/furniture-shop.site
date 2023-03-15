import json, os
from django.shortcuts import render
from .management.commands.fill_db import JSON_PATH
from .models import ProductCategory, Product
from django.shortcuts import get_object_or_404
import random
from basketapp.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.views.decorators.cache import never_cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.all()
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True).order_by('price')


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', errors='ignore') as infile:
        return json.load(infile)


def main(request):
    title = 'главная'
    products = Product.objects.all()
    content = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', content)


def contact(request):
    title = 'контакты'
    info = {1: ['Москва', '+7-888-888-8888', 'info@geekshop.ru', 'В пределах МКАД'],
            2: ['Питер', '+7-888-888-8888', 'info@geekshop.ru', 'Не в пределах МКАД'],
            3: ['Мухосранск', '+7-888-888-8888', 'info@geekshop.ru', 'Не в пределах МКАД']

            }
    content = {'title': title, 'info': info}
    return render(request, 'mainapp/contact.html', content)


@never_cache
@cache_page(3600)
def products(request, pk=None, page=1):
    title = 'продукты'
    links_menu = get_links_menu()
    basket = get_basket(request.user)
    if pk:
        if pk == 0:
            category = {
                'pk': 0,
                'name': 'все'
            }
            products = get_products_orederd_by_price()
        else:
            category = get_category(pk)
            products = get_products_in_category_orederd_by_price(pk)

        paginator = Paginator(products, 6)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
            # 'basket': basket,
        }

        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    product = Product.objects.filter(category__pk=pk).order_by('price').select_related()

    content = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'product': product,
        # 'basket': basket,
    }

    return render(request, 'mainapp/products.html', content)


@never_cache
def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        # 'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/product.html', content)


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = get_products()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products

#
# def products_ajax(request, pk=None, page=1):
#     if request.is_ajax():
#         links_menu = get_links_menu()
#         if pk:
#             if pk == '0':
#                 category = {
#                     'pk': 0,
#                     'name': 'все'
#                 }
#                 products = get_products_orederd_by_price()
#             else:
#                 category = get_category(pk)
#                 products = get_products_in_category_orederd_by_price(pk)
#
#         paginator = Paginator(products, 2)
#         try:
#             products_paginator = paginator.page(page)
#         except PageNotAnInteger:
#             products_paginator = paginator.page(1)
#         except EmptyPage:
#             products_paginator = paginator.page(paginator.num_pages)
#
#         content = {
#             'links_menu': links_menu,
#             'category': category,
#             'products': products_paginator,
#         }
#
#         result = render_to_string(
#             'mainapp/includes/inc_products_list_content.html',
#             context=content,
#             request=request)
#         return JsonResponse({'result': result})
