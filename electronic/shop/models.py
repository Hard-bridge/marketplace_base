from django.db import models

class User(models.Model):
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    balance = models.IntegerField()

    def __str__(self):
        return self.login

class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=100, decimal_places=2)
    full_text = models.TextField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    products = models.ManyToManyField(Product, related_name='product_order')
    date_order = models.DateTimeField(auto_now=True)
    status = models.CharField(default='Не оплачен', max_length=200)


class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)