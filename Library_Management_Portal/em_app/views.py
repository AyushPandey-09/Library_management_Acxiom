# em_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import *
from .forms import *

# Utility functions
def is_admin(user):
    return user.is_admin

def is_vendor(user):
    return user.is_vendor

def is_regular_user(user):
    return user.is_regular_user

# Auth Views
def user_login(request):
    if request.user.is_authenticated:
        return redirect('products')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('products')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('user_login')

def user_signup(request):
    if request.user.is_authenticated:
        return redirect('products')
    
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = User.UserTypes.REGULAR
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('products')
    else:
        form = UserSignupForm()
    return render(request, 'auth/user_signup.html', {'form': form})

def vendor_signup(request):
    if request.user.is_authenticated:
        return redirect('products')
    
    if request.method == 'POST':
        form = VendorSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = User.UserTypes.VENDOR
            user.save()
            login(request, user)
            messages.success(request, 'Vendor account created successfully!')
            return redirect('vendor_portal')
    else:
        form = VendorSignupForm()
    return render(request, 'auth/vendor_signup.html', {'form': form})

# Product Views
@login_required
def products(request):
    products = Product.objects.filter(status='approved')
    return render(request, 'products/list.html', {'products': products})

@login_required
@user_passes_test(is_vendor)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('vendor_portal')
    else:
        form = ProductForm()
    return render(request, 'products/add.html', {'form': form})

# Cart Views
@login_required
@user_passes_test(is_regular_user)
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/view.html', {'cart': cart})

@login_required
@user_passes_test(is_regular_user)
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, 'Product added to cart!')
    return redirect('products')

@login_required
@user_passes_test(is_regular_user)
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('view_cart')

# Order Views
@login_required
@user_passes_test(is_regular_user)
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('products')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                shipping_address=form.cleaned_data['shipping_address'],
                payment_method=form.cleaned_data['payment_method'],
                total_amount=cart.total_price
            )
            
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            cart.items.all().delete()
            messages.success(request, 'Order placed successfully!')
            return redirect('order_status', order_id=order.id)
    else:
        form = CheckoutForm()
    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})

@login_required
def order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/status.html', {'order': order})

# Vendor Portal
@login_required
@user_passes_test(is_vendor)
def vendor_portal(request):
    products = Product.objects.filter(vendor=request.user)
    requests = RequestItem.objects.filter(vendor=request.user)
    return render(request, 'vendor/portal.html', {
        'products': products,
        'requests': requests
    })

# Admin Views
@login_required
@user_passes_test(is_admin)
def admin_portal(request):
    pending_products = Product.objects.filter(status='pending')
    return render(request, 'admin/portal.html', {'pending_products': pending_products})

@login_required
@user_passes_test(is_admin)
def approve_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.status = 'approved'
    product.save()
    messages.success(request, 'Product approved!')
    return redirect('admin_portal')

@login_required
@user_passes_test(is_admin)
def reject_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.status = 'rejected'
    product.save()
    messages.success(request, 'Product rejected!')
    return redirect('admin_portal')

@login_required
@user_passes_test(is_admin)
def maintain_users(request):
    users = User.objects.filter(user_type=User.UserTypes.REGULAR)
    return render(request, 'admin/maintain_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def maintain_vendors(request):
    vendors = User.objects.filter(user_type=User.UserTypes.VENDOR)
    return render(request, 'admin/maintain_vendors.html', {'vendors': vendors})

# Request Item
@login_required
@user_passes_test(is_regular_user)
def request_item(request):
    if request.method == 'POST':
        form = RequestItemForm(request.POST)
        if form.is_valid():
            req_item = form.save(commit=False)
            req_item.requested_by = request.user
            req_item.save()
            messages.success(request, 'Item request submitted!')
            return redirect('products')
    else:
        form = RequestItemForm()
    return render(request, 'requests/create.html', {'form': form})

@login_required
@user_passes_test(is_vendor)
def update_request_status(request, request_id, status):
    req_item = get_object_or_404(RequestItem, pk=request_id, vendor=request.user)
    req_item.status = status
    req_item.save()
    messages.success(request, 'Request status updated!')
    return redirect('vendor_portal')