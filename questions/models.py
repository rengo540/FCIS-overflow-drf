from django.db import models
from authentication.models import User
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.




class Level(models.Model):
    #first-yaer , second-year , third-year , fourth-year , graduated 
    name = models.CharField(max_length=10)
    #frehsman , sophomore , junior , senior ,postgrad
    nickname = models.CharField(max_length=10)

    def __str__(self) -> str:
        return  self.name






class Course(models.Model):
    level = models.ForeignKey(Level,on_delete=models.PROTECT)
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name



class Question(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='questions')
    course = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True,blank=True,related_name='courses')
    level = models.ForeignKey(Level,on_delete=models.SET_NULL,null=True,blank=True,related_name='levels')
    
    title = models.CharField(max_length=400,null=False)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    #file = models.FileField(null=True,blank=True,upload_to='questions/')
    timestamp = models.DateTimeField(auto_now_add=True)
    voteUp = models.IntegerField(default=0)
    voteDown = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
    
    
    def total_points(self):
        return self.voteUp - self.voteDown

    def get_absolute_url(self):
        return reverse("questions:detail",kwargs={'slug': self.slug})




class UploadedFile(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='files')
    attached_file = models.FileField( upload_to='questions/')

    def save(self, *args, **kwargs):
        if self.attached_file:
            custom_filename = f'{self.question.id}_{self.attached_file.name}'
            self.attached_file.name = custom_filename
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.attached_file)



class Answer(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='answers')
    question = models.ForeignKey(Question,on_delete=models.CASCADE,blank=False,null=False,related_name='answrs')
    
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    voteUp = models.IntegerField(default=0)
    voteDown = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.content)

    def get_total_points(self):
        return self.voteUp - self.voteDown