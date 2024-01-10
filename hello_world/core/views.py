from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from hello_world.core.models import Product, Order
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.shortcuts import redirect

def index(request):
    categories = Product.objects.values_list('categorie', flat=True).distinct()
    context = {
        "title": "Company A",
        "categories": categories,
    }
    return render(request, "index.html", context)

# favorite
def favorites(request):
    if request.user.is_authenticated:
        user_favorites = Product.objects.filter(favorited_by=request.user)
        return render(request, 'favorites.html', {'user_favorites': user_favorites})
    else:
        return render(request, 'login.html')
    
@login_required
def add_to_favorites(request, product_name):
    product = Product.objects.get(nume=product_name)
    user = request.user
    product.favorited_by.add(user)
    return JsonResponse({'message': 'Product added to favorites'})

@login_required
def remove_from_favorites(request, product_name):
    product = Product.objects.get(nume=product_name)
    user = request.user
    product.favorited_by.remove(user)
    return JsonResponse({'message': 'Product removed from favorites'})

#cart
def cart(request):
    if request.user.is_authenticated:
        user_cart = Product.objects.filter(carted_byy=request.user)
        total_price = Decimal('0') 
        for product in user_cart:
            total_price += product.pret
        return render(request, 'cart.html', {'user_cart': user_cart, 'total_price': total_price})
    else:
        return render(request, 'login.html')

#checkout
    
def checkout(request):
    if request.user.is_authenticated:
        user_cart = Product.objects.filter(carted_byy=request.user)
        total_price = Decimal('0') 
        for product in user_cart:
            total_price += product.pret    
    return render(request, 'checkout.html', {'user_cart': user_cart, 'total_price': total_price})   

def process_order(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        
        if request.user.is_authenticated:
            user_cart = Product.objects.filter(carted_byy=request.user)
            total_price = Decimal('0') 
            products = list(user_cart)
            for product in user_cart:
                total_price += product.pret
            
            new_order = Order.objects.create(
                user=request.user,
                address=address,
                total_price=total_price,
            )
            new_order.products.add(*products)

            return redirect('orders')
        else:
            return render(request, 'login.html')

def orders(request):
    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'user_orders': user_orders})

@login_required
def add_to_cart(request, product_name):
    product = Product.objects.get(nume=product_name)
    user = request.user
    product.carted_byy.add(user)
    return JsonResponse({'message': 'Product added to cart'})

@login_required
def remove_from_cart(request, product_name):
    product = Product.objects.get(nume=product_name)
    user = request.user
    product.carted_byy.remove(user)
    return JsonResponse({'message': 'Product removed from cart'})

# search/categorii
def category_products(request, category):
    products = Product.objects.filter(categorie=category)
    return render(request, "category_products.html", {'products': products})
    
def search_products(request):
    query = request.GET.get('search_query')
    products = Product.objects.filter(nume__icontains=query)
    return render(request, "search_products.html", {'products': products})

def all_products(request):
    products = Product.objects.all()
    return render(request, "search_products.html", {'products': products})

# admin
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    template_name = 'product_form.html'
    success_url = '/admin/products/'

class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'product_form.html'
    success_url = '/admin/products/'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = '/admin/products/'

# sign up
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


#paypal

from django.http import JsonResponse
import paypalrestsdk
from django.conf import settings

def show_payment_page(request):
    return render(request, 'payment.html')


def make_paypal_payment(request):
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET,
    })

    # Cererea pentru paypal
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/execute/",
            "cancel_url": "http://localhost:8000/payment/cancel/"
        },
        "transactions": [{
    "item_list": {
        "items": [
            {
                "name": "Item Name 1",
                "sku": "Item1",
                "price": "10.00",
                "currency": "USD",
                "quantity": 1
            },
            {
                "name": "Item Name 2",
                "sku": "Item2",
                "price": "15.00",
                "currency": "USD",
                "quantity": 2
            },
            {
                "name": "Item Name 3",
                "sku": "Item3",
                "price": "20.00",
                "currency": "USD",
                "quantity": 1
            }
        ]
    },
    "amount": {
        "total": "60.00",
        "currency": "USD"
    },
    "description": "Payment description for multiple items"
    }]
    })

    if payment.create():
        success_url = payment.links[1].href
        return JsonResponse({"success": True, "success_url": success_url})
    else:
        return JsonResponse({"success": False, "error": payment.error})