from django.db import models

class Product(models.Model):
    nume = models.CharField(max_length=100)
    descriere = models.TextField()
    specificatii = models.TextField()
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    stoc = models.PositiveIntegerField()
    furnizor = models.CharField(max_length=100)
    modalitate_de_livrare = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)

    class Meta:
        app_label = 'hello_world'  # Specify the app label