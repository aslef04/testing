from django.db import models

# Create your models here.

class RegisterModel(models.Model):
    profile=models.ImageField(upload_to="profile_image/")
    full_name=models.CharField(max_length=20)
    user_name=models.CharField(max_length=20)
    phone_number=models.IntegerField()
    choose=[
        ("Male","Male"),
        ("Female","Female")
    ]
    gender=models.CharField(max_length=15)
    dob=models.DateField()
    email=models.EmailField()
    address=models.TextField(max_length=100)
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.full_name 

class ProductAdding(models.Model):
    image = models.ImageField(upload_to="product_image/")
    name = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField(max_length=500)

class RegisterViewModel(models.Model):
    full_name=models.CharField(max_length=50)
    user_name=models.CharField(max_length=30)
    email=models.EmailField()
    password=models.CharField(max_length=20)


class Student(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    age = models.IntegerField()
    departement = models.CharField(max_length=50)
