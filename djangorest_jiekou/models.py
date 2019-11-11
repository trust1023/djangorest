from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50,verbose_name='商品名称')
    category = models.CharField(max_length=50,verbose_name='商品分类')
    is_hot = models.BooleanField(default=False,verbose_name='是否热卖')
    price = models.FloatField(default=0,verbose_name='商品价格')

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

