from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    nume = models.CharField(max_length=100)
    descriere = models.TextField()
    specificatii = models.TextField()
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    stoc = models.PositiveIntegerField()
    furnizor = models.CharField(max_length=100)
    modalitate_de_livrare = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)
    favorited_by = models.ManyToManyField(User, related_name='favorite_products', blank=True)
    carted_by = models.ManyToManyField(User, related_name='cart_products', blank=True)
    carted_byy = models.ManyToManyField(User, related_name='cartt_products', blank=True)
    class Meta:
        app_label = 'hello_world'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"