from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.db.models import Q
from django.http import HttpResponse

def index(request):
    query = request.GET.get('q', '').strip()  # Recherche
    min_price = request.GET.get('min_price', '')  # Prix minimum
    max_price = request.GET.get('max_price', '')  # Prix maximum
    size_filter = request.GET.get('size', '')  # Taille du produit
    product_id = request.GET.get('id')  # ID d'un produit spécifique

    # 🔥 Commencer avec tous les produits
    products = Product.objects.all()

    # 🔎 Appliquer les filtres dynamiquement
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if min_price.isdigit():
        products = products.filter(price__gte=int(min_price))

    if max_price.isdigit():
        products = products.filter(price__lte=int(max_price))

    if size_filter:
        products = products.filter(size=size_filter)

    # 🔥 Récupérer un produit spécifique si un ID est fourni
    product = get_object_or_404(Product, id=product_id) if product_id else None

    # 🛒 Gestion du panier
    cart = request.session.get('cart', {})
    new_cart = {"total": 0}

    for key, value in cart.items():
        if all(k in value and value[k] for k in ['id', 'size', 'price', 'quantity']):
            new_cart[key] = {
                "id": value['id'],
                "name": value['name'],
                "price": float(value['price']),
                "size": value['size'],
                "quantity": int(value['quantity']),
                "total_product_price": float(value['price']) * int(value['quantity'])
            }
            new_cart["total"] += new_cart[key]["total_product_price"]

    return render(request, 'index.html', {
        'products': products,
        'product': product,
        'cart': new_cart,
        'size_choices': Product.SIZE_CHOICES,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'size_filter': size_filter
    })


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
                'price': float(product.price),  # Conversion en float
                'size': size,
                'quantity': quantity
            }

        request.session['cart'] = cart
        request.session.modified = True

        print("Cart content:", request.session['cart'])  # Debugging

    return redirect('index')

def cart_view(request):
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * int(item['quantity']) for item in cart.values())  # Vérification du total
    products = Product.objects.all()
    
    return render(request, 'index.html', {
        'products': products,
        'cart': cart,
        'total': total,
        'product': None,
        'size_choices': Product.SIZE_CHOICES
    })

def remove_from_cart(request, product_id, size):
    cart = request.session.get('cart', {})
    cart_key = f"{product_id}_{size}"

    if cart_key in cart:
        del cart[cart_key]
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('index')

def search_product(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query) if query else Product.objects.none()

    return render(request, 'search_results.html', {
        'products': products,
        'query': query,
        'cart': request.session.get('cart', {}),
        'size_choices': Product.SIZE_CHOICES
    })
def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        address = request.POST.get('address')
        card_number = request.POST.get('card_number')
        
        # 🛒 Récupération du panier
        cart = request.session.get('cart', {})

        if not cart:
            return HttpResponse("Votre panier est vide ! <a href='/'>Retour</a>")

        # 📌 Ici, on pourrait enregistrer la commande dans la base de données

        # 🗑️ On vide le panier après la commande
        request.session['cart'] = {}
        request.session.modified = True

        return HttpResponse(f"""
            <h2>✅ Commande validée</h2>
            <p>Merci {name} {surname} pour votre achat.</p>
            <p>Votre commande sera envoyée à : {address}.</p>
            <a href="/">Retour à l'accueil</a>
        """)

    return render(request, 'checkout.html')