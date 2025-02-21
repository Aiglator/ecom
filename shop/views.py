# attention ce code a été réalisé dans le cadre d'un devoir python
# toute fois il est fonctionnel ceci est un Message du développeur Rayan Chattaoui
from django.shortcuts import render, get_object_or_404, redirect
import re   # importation de cette bibliothéque pour le regex de la carte bancaire vue quelle n'est pas stocker je l'utilise au ca ou
from django.db.models import Q
from django.http import HttpResponse,HttpResponseBadRequest
from .models import Product

# Page d'accueil avec liste des produits et filtres
def index(request):
    query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    size_filter = request.GET.get('size', '')
    product_id = request.GET.get('id')

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if min_price.isdigit():
        products = products.filter(price__gte=int(min_price))

    if max_price.isdigit():
        products = products.filter(price__lte=int(max_price))

    if size_filter:
        products = products.filter(size=size_filter)

    product = get_object_or_404(Product, id=product_id) if product_id else None

    cart = request.session.get('cart', {})
    updated_cart = {"total": 0}

    for key, item in cart.items():
        if 'id' in item and 'size' in item and 'price' in item and 'quantity' in item:
            updated_cart[key] = {
                "id": item['id'],
                "name": item['name'],
                "price": float(item['price']),
                "size": item['size'],
                "quantity": int(item['quantity']),
                "total_product_price": float(item['price']) * int(item['quantity'])
            }
            updated_cart["total"] += updated_cart[key]["total_product_price"]

    return render(request, 'index.html', {
        'products': products,
        'product': product,
        'cart': updated_cart,
        'size_choices': Product.SIZE_CHOICES,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'size_filter': size_filter
    })

# Ajout d'un produit au panier
def addtocart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        size = request.POST.get('size')
        quantity = int(request.POST.get('quantity', 1))
        cart_key = f"{product.id}_{size}"

        if cart_key in cart:
            cart[cart_key]['quantity'] += quantity
        else:
            cart[cart_key] = {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'size': size,
                'quantity': quantity
            }

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('index')

# Affichage des produits filtrés
def search_product(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)) if query else Product.objects.none()

    return render(request, 'search_results.html', {
        'products': products,
        'query': query,
        'cart': request.session.get('cart', {}),
        'size_choices': Product.SIZE_CHOICES
    })

# Affichage du panier
def cart_view(request):
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * int(item['quantity']) for item in cart.values())
    products = Product.objects.all()

    return render(request, 'index.html', {
        'products': products,
        'cart': cart,
        'total': total,
        'product': None,
        'size_choices': Product.SIZE_CHOICES
    })

# Suppression d'un produit du panier
def remove_from_cart(request, product_id, size):
    cart = request.session.get('cart', {})
    cart_key = f"{product_id}_{size}"

    if cart_key in cart:
        del cart[cart_key]
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('index')

# Page de commande
def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        mail = request.POST.get('mail')
        address = request.POST.get('address')
        card_number = request.POST.get('card_number')
        # attention : ne jamais stocker les numéros de carte bancaire en clair dans une base de données ceci est pour un devoir python

        # if not re.match(r"^\d{13,19}$", card_number):
        #     return HttpResponseBadRequest("Numéro de carte invalide.")
        # ceci est un exemple de regex pour la carte bancaire mais c'est surtout utilissée dans le cadre de la vérification de maim
        
        cart = request.session.get('cart', {})
        if not cart:
            return HttpResponse("Votre panier est vide ! <a href='/'>Retour</a>")

        request.session['cart'] = {}
        request.session.modified = True

        return HttpResponse(f"""
            <h2>Commande validée</h2>
            <p>Merci {name} {surname} pour votre achat.</p>
            <p> Cette commande est enregistrer sous le mail : {mail}</p>
            <p>Votre commande sera envoyée à : {address}.</p>
            <a href="/">Retour à l'accueil</a>
        """)

    return render(request, 'checkout.html')