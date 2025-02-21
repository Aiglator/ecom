from django.db import models

#  Catégories des produits
class Category(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.name

#  Produits
class Product(models.Model):
    SIZE_CHOICES = [
        ('xs', 'Extra Small'),
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),
        ('xl', 'Extra Large'),
    ]
    
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    # Stocke les tailles disponibles sous forme de texte séparé par des virgules
    available_sizes = models.CharField(max_length=50, default='xs,s,m,l,xl')

    def get_available_sizes(self):
        """Retourne une liste de tuples (code, label) des tailles disponibles."""
        size_codes = self.available_sizes.split(',')  # Ex: ['xs', 's', 'm']
        return [(code, dict(self.SIZE_CHOICES).get(code, code)) for code in size_codes]

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.name

#  Commande principale (Client + Infos de livraison)
class Order(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande de {self.name} {self.surname} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"

#  Produits associés à une commande
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    size = models.CharField(max_length=50, choices=Product.SIZE_CHOICES)  # Utilisation des choix prédéfinis
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.quantity} x {self.product_name} ({self.size})"
