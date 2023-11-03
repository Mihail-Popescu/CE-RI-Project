from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Product

# Homepage view
def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)

# Product views (admin section)
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'  # Create this template file
    context_object_name = 'products'  # Optional: Set a custom context variable name

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
