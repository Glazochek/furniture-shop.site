from authapp.models import User
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from authapp.forms import UserRegisterForm
from adminapp.forms import UserAdminEditForm, ProductEditForm, ProductCategoryEditForm
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from django.db.models import F


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)
        db_profile_by_type(sender, 'UPDATE', connection.queries)


class UsersListView(ListView):
    model = User
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'


class ProductCategoryUpdateView(UpdateView):
    # model = ProductCategory
    # template_name = 'adminapp/category_update.html'
    # success_url = reverse_lazy('admin:categories')
    # fields = '__all__'
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'категории/редактирование'
    #     return context

    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        return super().form_valid(form)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'
    users_list = User.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    content = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', content)


def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    self.object.is_active = False
    self.object.save()
    return HttpResponseRedirect(self.get_success_url())


def user_create(request):
    title = 'пользователи/создание'
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = UserRegisterForm()
    content = {'title': title, 'update_form': user_form}
    return render(request, 'adminapp/user_update.html', content)


def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        edit_form = UserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
    else:

        edit_form = UserAdminEditForm(instance=edit_user)
    content = {'title': title, 'update_form': edit_form}
    return render(request, 'adminapp/user_update.html', content)


def user_delete(request, pk):
    title = 'пользователи/удаление'
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        # вместо удаления лучше сделаем неактивным
        # user.is_active = False
        # user.save()
        return HttpResponseRedirect(reverse('admin:users'))
    content = {'title': title, 'user_to_delete': user}
    return render(request, 'adminapp/user_delete.html', content)


def categories(request):
    title = 'админка/категории'
    categories_list = ProductCategory.objects.all()
    content = {
        'title': title,
        'objects': categories_list
    }
    return render(request, 'adminapp/categories.html', content)


def category_create(request, pk):
    pass
    # title = 'продукт/создание'
    # category = get_object_or_404(ProductCategory, pk=pk)
    # if request.method == 'POST':
    #     product_form = ProductCategoryEditForm(request.POST, request.FILES)
    #     if product_form.is_valid():
    #         product_form.save()
    #         return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    # else:
    #     product_form = ProductEditForm(initial={'category': category})
    #
    # content = {
    #     'title': title,
    #     'update_form': product_form,
    #     'category': category,
    # }
    # return render(request, 'adminapp/product_update.html', content)


def category_update(request, pk):
    title = 'категория/редактирование'
    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES,
                                    instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:category_update',
                                                args=[edit_category.pk]))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)
    content = {'title': title,
               'update_edit_category_form': edit_form,
               'category': edit_category,
               }
    return render(request, 'adminapp/category_update.html', content)


def category_delete(request, pk):
    title = 'продукт/удаление'
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        # category.is_active = False
        # category.save()
        return HttpResponseRedirect(reverse('admin:categories'))
    content = {'title': title, 'category_to_delete': category}
    return render(request, 'adminapp/category_delete.html', content)


def products(request, pk):
    title = 'админка/продукт'
    category = get_object_or_404(ProductCategory, pk=pk)
    categories = ProductCategory.objects.all()
    products_list = Product.objects.filter(category__pk=pk).order_by('name')
    content = {
        'title': title,
        'category': category,
        'categories': categories,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', content)


def product_create(request, pk):
    title = 'продукт/создание'
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    content = {
        'title': title,
        'update_form': product_form,
        'category': category,
    }
    return render(request, 'adminapp/product_update.html', content)


def product_read(request, pk):
    title = 'продукт/подробнее'
    product = get_object_or_404(Product, pk=pk)
    content = {'title': title, 'object': get_object_or_404(Product, pk=pk), }
    return render(request, 'adminapp/product_read.html', content)


def product_update(request, pk):
    title = 'продукт/редактирование'
    edit_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES,
                                    instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update',
                                                args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)
    content = {'title': title,
               'update_form': edit_form,
               'category': edit_product.category,
               }
    return render(request, 'adminapp/product_update.html', content)


def product_delete(request, pk):
    title = 'продукт/удаление'
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        # product.is_active = False
        # product.save()
        return HttpResponseRedirect(reverse('admin:products',
                                            args=[product.category.pk]))
    content = {'title': title, 'product_to_delete': product}
    return render(request, 'adminapp/product_delete.html', content)
