from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from basketapp.models import Basket
from django.views.generic import UpdateView, FormView
from adminapp.mixin import BaseClassContextMixin, UserDispatchMixin
from authapp.models import User
from geekshop import settings
from django.db import transaction
from django.contrib.auth.views import LogoutView, LoginView
from authapp.forms import UserLoginForm, UserRegisterForm, UserEditForm, UserProfileEditForm


def login(request):
    title = 'вход'
    login_form = UserLoginForm(data=request.POST or None)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))
    content = {
        'title': title,
        'login_form': login_form,
        'next': next
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


@login_required
@transaction.atomic
def edit(request):
    title = 'редактирование'
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = UserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)

    content = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form
    }
    return render(request, 'authapp/edit.html', content)


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#
#             form.save()
#         else:
#             print(form.errors)
#     user_select = request.user
#     context = {
#         'title': 'Geekshop | Профайл',
#         'form': UserProfileForm(instance=user_select),
#         'basket': Basket.objects.filter(user=user_select)
#     }
#
#     return render(request, 'authapp/profile.html', context)


def register(request):
    title = 'регистрация'
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))

    else:
        register_form = UserRegisterForm()
    content = {'title': title, 'register_form': register_form}
    return render(request, 'authapp/register.html', content)


# --------------------------------------------------------------------------------


class Logout(LogoutView):
    template_name = 'mainapp/index.html'


class Login(LoginView, BaseClassContextMixin):
    title = 'Вход'
    from_class = UserLoginForm
    template_name = 'authapp/login.html'


class Edit(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    model = User
    template_name = 'authapp/edit.html'
    form_class = UserEditForm
    success_url = reverse_lazy('authapp:edit')
    title = 'Geekshop | Профайл'

    def from_valid(self, form):
        messages.set_level(self.request, messages.SUCCESS)
        messages.success(self.request, 'Вы успешно сохранили профиль !!!')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(Edit, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context


class Register(FormView, BaseClassContextMixin):
    title = 'Регистрация'
    model = User
    from_class = UserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')

    def post(self, request, *args, **kwargs):
        register_form = self.form_class(data=request.POST)
        if register_form.is_valid():
            user = UserRegisterForm.save()
            if self.send_verify_link(user):
                messages.set_level(request, messages.SUCCESS)
                messages.success(self.request, 'Вы успешно зарегались !!!')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                messages.set_level(request, messages.ERROR)
                messages.error(self.request, register_form.errors)
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(self.request, register_form.errors)
        return render(request, self.template_name, {'form': register_form})

    def send_verify_link(self, user):
        verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
        title = f"Для активации учетной записи {user.username} пройдите по ссылке"
        message = f"Для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}"
        return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activate_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activate_key and not user.is_activation_key_expires():
                user.activation_key = ''
                user.activation_kry_expires = None
                user.is_active = True
                user.save()

                auth.login(self, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(self, 'authapp/verification.html')

        except Exception as e:
            print(f'error activation user : {e.args}')
            return HttpResponseRedirect(reverse('index'))
