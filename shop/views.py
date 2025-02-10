from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def index(request, id=None):
    products = Product.objects.all()
    product = None
    print("----", request.session.get('cart', {}))  # Debugging

    cart = request.session.get('cart', {})
    new_cart = {"total": 0}

    for key, value in cart.items():
        # Vérification que toutes les données sont bien présentes et non vides
        if all(k in value and value[k] for k in ['id', 'size', 'price', 'quantity']):
            new_cart[key] = {
                "id": value['id'],
                "name": value['name'],
                "price": float(value['price']),  # Conversion en float
                "size": value['size'],
                "quantity": int(value['quantity']),
                "total_product_price": float(value['price']) * int(value['quantity'])
            }
            new_cart["total"] += new_cart[key]["total_product_price"]

    if id:
        product = get_object_or_404(Product, id=id)

    return render(request, 'index.html', {
        'products': products,
        'product': product,
        'cart': new_cart,
        'size_choices': Product.SIZE_CHOICES
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
