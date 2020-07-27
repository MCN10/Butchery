from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Count



# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(upload_to='profilePictures/', blank=True, null=True)

    def __str__(self):
        return self.firstname

class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(max_length=2000, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False, null=False, blank=False)
    image1 = models.ImageField(upload_to='main_product/', blank=True, null=False)

    image2 = models.ImageField(upload_to='main_product/', blank=True, null=False)

    image3 = models.ImageField(upload_to='main_product/', blank=True, null=False)

    image4 = models.ImageField(upload_to='main_product/', blank=True, null=False)

    category = models.ForeignKey('Category' , on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.name

    @property
    def imageURL1(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url
    def imageURL2(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url
    def imageURL3(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url
    def imageURL4(self):
        try:
            url = self.image4.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Category(models.Model):
    ## for product category
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)

    def save(self , *args, **kwargs):
        if not self.slug and self.category_name:
            self.slug = slugify(self.category_name)
        super(Category , self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
