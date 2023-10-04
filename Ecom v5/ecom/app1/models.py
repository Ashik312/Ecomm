from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class product(models.Model):
    product_name = models.CharField(max_length=50)
    product_desc = models.CharField(max_length=200)
    product_img = models.ImageField(upload_to='image/proimg')
    product_price = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return self.product_name
class cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.user.username
    
class CartItem(models.Model):
    crt = models.ForeignKey(cart,on_delete=models.CASCADE)
    pro = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

