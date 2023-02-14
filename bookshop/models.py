from django.db import models
from django.utils import timezone
from django.urls import  reverse
# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'CATEGORY'
        verbose_name_plural = 'CATEGORY'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail',args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    image2 = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    image3 = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)

    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail',args=[str(self.slug)])

class Review(models.Model):
    
    product = models.ForeignKey(Product,related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=20)
    rating = models.IntegerField( default=1)
    review_comment = models.TextField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return self.product.name
    
class Contact(models.Model):
    name = models.CharField('Ismi',max_length=80)
    email = models.EmailField('Emaili',max_length=70)
    message = models.CharField('Xabari',max_length=250)

    verbose_name = 'CONTACT'
    verbose_name_plural = 'CONTACTS'

    def __str__(self):
        return f"{self.name}"
class Post(models.Model):
    title = models.CharField('Maqola nomi',max_length=300)
    date = models.DateField("Qo'shilgan vaqti", auto_now_add=True)
    body = models.CharField('Maydon',max_length=300)
    image = models.ImageField('Maqola rasmi', upload_to='Maqolalar_rasmi/')

    class Meta:
        verbose_name = 'NEWS'
        verbose_name_plural = 'NEWS'

    def __str__(self):
        return f'{self.title}'