from django.urls import path
from . import views
from .views import load_images
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('', load_images, name='home'),
    path('home/', views.home, name='home'),
    path('products/', views.product_list, name='products'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('create_order/', views.create_order, name='create_order'),
    path('accounts/profile/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.orders_page, name='orders_page'),
    path('orders/fulfill/<int:order_id>/', views.fulfill_order, name='fulfill_order'),
    path('orders/resolve/<int:order_id>/', views.resolve_issue, name='resolve_issue'),
    path('mark_paid/<int:order_id>/', views.mark_paid, name='mark_paid'),
    path('edit-products/', views.edit_products, name='edit_products'),
    path('products/<str:category>/', views.product_page, name='product_page'),
    path('products/<str:category>/', views.get_products_by_category, name='product_list_by_category'), 
    path('manage_address/', views.manage_address, name='manage_address'),   
    path('manage_address/', views.manage_address, name='manage_address'),
    path('search/', views.product_search, name='product_search'),



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
