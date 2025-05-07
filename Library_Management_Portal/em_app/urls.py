from django.urls import path
from . import views

urlpatterns = [
    # Auth URLs
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='user_signup'),
    path('vendor/signup/', views.vendor_signup, name='vendor_signup'),
    
    # Product URLs
    path('products/', views.products, name='products'),
    
    # Cart URLs
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Order URLs
    path('checkout/', views.checkout, name='checkout'),
    path('orders/<int:order_id>/', views.order_status, name='order_status'),
    
    # Vendor URLs
    path('vendor/portal/', views.vendor_portal, name='vendor_portal'),
    path('vendor/add-product/', views.add_product, name='add_product'),
    path('vendor/request/<int:request_id>/<str:status>/', views.update_request_status, name='update_request_status'),
    
    # Admin URLs
    path('admin/portal/', views.admin_portal, name='admin_portal'),
    path('admin/approve-product/<int:product_id>/', views.approve_product, name='approve_product'),
    path('admin/reject-product/<int:product_id>/', views.reject_product, name='reject_product'),
    path('admin/users/', views.maintain_users, name='maintain_users'),
    path('admin/vendors/', views.maintain_vendors, name='maintain_vendors'),
    
    # Request URLs
    path('request-item/', views.request_item, name='request_item'),
]