from django.urls import path
import authapp.views as authapp


app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('edit/', authapp.edit, name='edit'),

    # path('login/', authapp.Login.as_view(), name='login'),
    # path('logout/', authapp.Logout.as_view(), name='logout'),
    # path('register/', authapp.Register.as_view(), name='register'),
    # path('edit/', authapp.Edit.as_view(), name='edit'),

    # path('verify/<str:email>/<str:activate_key>/', authapp.Register.verify, name='verify')
]
