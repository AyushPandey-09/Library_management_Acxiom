# em_app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class UserTypes(models.IntegerChoices):
        ADMIN = 1, 'Admin'
        VENDOR = 2, 'Vendor'
        REGULAR = 3, 'Regular User'

    user_type = models.PositiveSmallIntegerField(
        choices=UserTypes.choices,
        default=UserTypes.REGULAR
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name="custom_user_groups",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name="custom_user_permissions",
        related_query_name="custom_user",
    )

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def _str_(self):
        return self.username

    @property
    def is_admin(self):
        return self.user_type == self.UserTypes.ADMIN

    @property
    def is_vendor(self):
        return self.user_type == self.UserTypes.VENDOR

    @property
    def is_regular_user(self):
        return self.user_type == self.UserTypes.REGULAR

class Product(models.Model):
    class ProductStatus(models.TextChoices):
        PENDING = 'pending', _('Pending Approval')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejected')

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': User.UserTypes.VENDOR}
    )
    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def _str_(self):
        return f"{self.name} - {self.get_status_display()}"

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': User.UserTypes.REGULAR}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"Cart for {self.user.username}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def _str_(self):
        return f"{self.quantity}x {self.product.name} in {self.cart}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PROCESSING = 'processing', _('Processing')
        SHIPPED = 'shipped', _('Shipped')
        DELIVERED = 'delivered', _('Delivered')
        CANCELLED = 'cancelled', _('Cancelled')

    class PaymentMethods(models.TextChoices):
        CASH = 'cash', _('Cash')
        UPI = 'upi', _('UPI')
        CARD = 'card', _('Credit/Debit Card')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': User.UserTypes.REGULAR}
    )
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PaymentMethods.choices
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-order_date']

    def _str_(self):
        return f"Order #{self.id} - {self.user.username}"

    @property
    def item_count(self):
        return self.items.count()

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order.id}"

    @property
    def subtotal(self):
        return self.price * self.quantity

class RequestItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='requested_items',
        limit_choices_to={'user_type': User.UserTypes.REGULAR}
    )
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendor_requests',
        limit_choices_to={'user_type': User.UserTypes.VENDOR}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ('open', _('Open')),
            ('in_progress', _('In Progress')),
            ('completed', _('Completed')),
            ('rejected', _('Rejected')),
        ),
        default='open'
    )

    class Meta:
        ordering = ['-created_at']

    def _str_(self):
        return f"Request for {self.name} by {self.requested_by.username}"