from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_view
from .forms import LoginForm, UserPasswordChangeForm, UserPassworResetForm, UserSetPasswordConfirm


urlpatterns = [

    path('', views.ProductHomeView.as_view(), name='home'),

    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    
    path('cart/', views.show_cart, name='showcart'),

    # Quantity plus, minus, remove
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),


    path('buy/', views.buy_now, name='buy-now'),


    path('profile/', views.ProfileViewCustomer.as_view(), name='profile'),

    path('address/', views.AddressView.as_view(), name='address'),



    path('orders/', views.orders, name='orders'),


    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),


    path('accounts/login/', auth_view.LoginView.as_view(template_name = 'app/login.html', authentication_form=LoginForm), name='login'),

    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    path('changepassword/', auth_view.PasswordChangeView.as_view(template_name = 'app/changepassword.html', form_class = UserPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name = 'app/passwordchangedone.html'), name='changepassworddone'),


    path('password-reset/', auth_view.PasswordResetView.as_view(template_name = 'app/password_reset.html', form_class=UserPassworResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name = 'app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name = 'app/password_reset_confirm.html', form_class=UserSetPasswordConfirm, success_url='/password-reset-complete/'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name = 'app/password_reset_complete.html'), name='password_reset_conmplete'),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    


    path('checkout/',  views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),


]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
