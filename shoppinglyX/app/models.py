import datetime

from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from PIL import Image
# Create your models here.

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email", error_messages={'exists': 'This Already exists'})

    class mete:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class User_info(models.Model):
    name=models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    mobile = models.BigIntegerField()
    address=models.CharField(max_length=200)
    village = models.CharField(max_length=20,default="")
    city = models.CharField(max_length=20,default="")
    sub_district = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    state = models.CharField(max_length=30)
    pincode=models.IntegerField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="1. User_info"

class Brand(models.Model):
    brand=models.CharField(max_length=100)

    def __str__(self):
        return self.brand
    class Meta:
        verbose_name_plural="2. Brand"

class Categories(models.Model):
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    category= models.CharField(max_length=100)

    def __str__(self):
        return self.category
    class Meta:
        verbose_name_plural="3. Category"

def validate_image_dimensions(image):
    img = Image.open(image)
    if img.width != 920 or img.height != 1080:
        raise ValidationError("Image must be exactly 920x1080 pixels.")

class Product(models.Model):
    title=models.CharField(max_length=100)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    price=models.FloatField()
    discount=models.FloatField(default=0)
    delivery_charge = models.FloatField(default=0, null=True)
    prod_image=models.ImageField(upload_to='images/prod_images',validators=[validate_image_dimensions])
    offer_price = models.FloatField(default=0)
    delivery = models.FloatField( default=0,null=True)
    field = models.CharField(max_length=20,default="product", null=True, editable=False)

    def save(self, *args, **kwrgs):
        self.op = self.price * (self.discount / 100)
        self.offer_price = self.price - self.op
        self.delivery = self.offer_price * (self.delivery_charge / 100)
        super(Product,self).save(*args, **kwrgs)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="4. Product"

class One_day_deal(models.Model):
    title=models.ForeignKey(Product,on_delete=models.CASCADE)
    product=models.CharField(max_length=100,null=True,editable=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,editable=False,null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE,editable=False,null=True)
    price = models.FloatField(default=0,editable=False,null=True)
    discount = models.FloatField()
    delivery_charge = models.FloatField(default=0, null=True)
    prod_image = models.ImageField(upload_to='images/one_day', null=True,validators=[validate_image_dimensions],editable=False)
    offer_price=models.FloatField(default=0,editable=False,null=True)
    delivery = models.FloatField(default=0, null=True,editable=False)
    field=models.CharField(max_length=20,default="one_day",null=True,editable=False)



    def save(self, *args, **kwrgs):
        self.product=self.title
        self.brand=self.title.brand
        self.category=self.title.category
        self.price = self.title.price
        self.op = self.price * (self.discount / 100)
        self.offer_price = self.price - self.op
        self.delivery = self.offer_price * (self.delivery_charge / 100)
        self.prod_image=self.title.prod_image
        super(One_day_deal,self).save(*args, **kwrgs)

    def __str__(self):
        return str(self.title)
    class Meta:
        verbose_name_plural="5. One_day_deal"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user.username if self.user else 'Anonymous'}"
    class Meta:
        verbose_name_plural="6. Cart"

# Cart Item (Stores Items in Cart)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    one_day=models.ForeignKey(One_day_deal,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.product:
            return f"{self.quantity} x {self.product.title}"
        elif self.one_day:
            return f"{self.quantity} x {self.one_day.title}"
        return f"{self.quantity} x Unknown"
    class Meta:
        verbose_name_plural="7. CartItem"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_info = models.ForeignKey(User_info, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=150)
    image=models.ImageField(upload_to="images/order_img")
    product=models.CharField(max_length=100)
    quantity=models.IntegerField()
    price=models.FloatField()
    delivery=models.FloatField(null=True)
    pro_total=models.FloatField()
    payment=models.CharField(max_length=10,null=True,default="Unpaid")
    date=models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.product
    class Meta:
        verbose_name_plural="8. Order"