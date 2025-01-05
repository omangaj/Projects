import datetime
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from tinymce.models import HTMLField




# Create your models here.

class Contact_info(models.Model):
    address=models.TextField()
    mobile=models.CharField(max_length=10)
    email=models.EmailField()


    def __str__(self):
        return self.address
    class Meta:
        verbose_name_plural="1. Contact_info"

class Links(models.Model):
    name=models.CharField(max_length=100)
    link=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="2. Links"

class Categories(models.Model):
    name=models.CharField(max_length=150)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="4. Categories"

class Sub_categories(models.Model):
    name=models.CharField(max_length=150)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="5. Sub_categories"

class Brand(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="6. Brand"


class Product(models.Model):
    availability=(('In stock','In stock'),('Out of stock','out of stock'))
    condition=(('New','New'),('Used','Used'),('refurbished','refurbished'))
    category=models.ForeignKey(Categories,on_delete=models.CASCADE,default="")
    sub_category=models.ForeignKey(Sub_categories,on_delete=models.CASCADE,default="")
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,default="",null=True)
    image=models.ImageField(upload_to="ecommerce/pro_img")
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    condition=models.CharField(max_length=100,choices=condition,null=True)
    availability=models.CharField(max_length=100,choices=availability,null=True)
    description=HTMLField(null=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="7. Product"


class UserCreateForm(UserCreationForm):
    email=forms.EmailField(required=True,label="Email",error_messages={'exists':'This Already exists'})

    class Meta:
        model=User
        fields=('username','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def save(self,commit=True):
        user=super(UserCreateForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']


class Contact_us(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=150)
    subject=models.CharField(max_length=100)
    message=models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="8. Contact_us"

class Order(models.Model):
    image=models.ImageField(upload_to="ecommerce/order_img")
    product=models.CharField(max_length=100)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.IntegerField()
    total=models.IntegerField()
    address=models.TextField()
    mobile=models.CharField(max_length=10)
    pincode=models.CharField(max_length=10)
    date=models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.product
    class Meta:
        verbose_name_plural="9. Order"