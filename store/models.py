from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Color(models.Model):
    color = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.color


class Category(models.Model):
    category = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category


class Product(models.Model):
    title = models.CharField(max_length=200)
    detail_preview = models.CharField(max_length=1000)
    detail = RichTextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(
        Color, on_delete=models.SET_NULL, null=True)
    availiability = models.IntegerField()
    price = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        ordering = ['-created']

    # Generate random slugs
    def save(self, *args, **kwargs):
        global str
        if self.slug == None:
            slug = slugify(self.title)

            has_slug = Product.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.slug) + '-' + str(count)
                has_slug = Product.objects.filter(slug=slug).exists()
            self.slug = slug
        super().save(self, *args, **kwargs)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f'Images for {self.product.title}'
