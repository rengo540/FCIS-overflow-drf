from django.db import models
from django.utils.text import slugify
from authentication.models import User
# Create your models here.

class Group(models.Model):
    """Model definition for Group."""
    name = models.CharField(max_length=225,null=False,blank=False)
    slug= models.SlugField(primary_key=True,max_length=225)
    
    member= models.ManyToManyField(User,blank=True)
    
    
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for Group."""

        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        """Unicode representation of Group."""
        pass
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Group, self).save(*args, **kwargs)
    
    

class Membership(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('person', 'group')
        
        
