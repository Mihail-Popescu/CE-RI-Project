"""hello_world URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from hello_world.core import views as core_views
from hello_world.core.views import ProductCreateView, ProductUpdateView, ProductDeleteView, ProductListView,SignUpView, category_products, search_products, all_products

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', core_views.index, name='index'),
    path('admin/products/', ProductListView.as_view(), name='product-list'),
    path('admin/products/add/', ProductCreateView.as_view(), name='product-add'),
    path('admin/products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product-edit'),
    path('admin/products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path("category/<str:category>/", core_views.category_products, name="category_products"),
    path("search/", core_views.search_products, name="search_products"),
    path('all_products/', core_views.all_products, name='all_products'),
    path('add_to_favorites/<str:product_name>/', core_views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<str:product_name>/', core_views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', core_views.favorites, name='favorites'),
    path('cart/', core_views.cart, name='cart'),
    path('make-paypal-payment/', core_views.make_paypal_payment, name='make_paypal_payment'),
    path('payment/', core_views.show_payment_page, name='show_payment_page'),
    path('add_to_cart/<str:product_name>/', core_views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<str:product_name>/', core_views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', core_views.checkout, name='checkout'),
    path('process_order/', core_views.process_order, name='process_order'),
    path('orders/', core_views.orders, name='orders'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
