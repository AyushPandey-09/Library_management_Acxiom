from django.contrib import admin
from .models import User, Product, Cart, CartItem, Order, OrderItem, RequestItem

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active')
    list_filter = ('user_type', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'price', 'status')
    list_filter = ('status', 'vendor')
    search_fields = ('name', 'description')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('product_name', 'cartuser_username')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'order_date')
    list_filter = ('status', 'payment_method')
    search_fields = ('user__username', 'transaction_id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('product_name', 'orderuser_username')

@admin.register(RequestItem)
class RequestItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'requested_by', 'vendor', 'status', 'created_at')
    list_filter = ('status', 'vendor')
    search_fields = ('name', 'description')