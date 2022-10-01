from django.db import models
from django.urls import reverse

# Create your models here.
class Animals(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL Slug")
    content = models.TextField(blank=True, verbose_name="Text article")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Picture")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time_created")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Time_updated")
    is_published = models.BooleanField(default=True, verbose_name="Is_published")
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name="Category", null=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})
    
    class Meta:
        verbose_name = "Popular animal"
        verbose_name_plural = "Popular animals"
        ordering = ['id']
    
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='CATEGORY')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
            return self.name
    
    def get_absolute_url(self):
        return reverse("category", kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['id']