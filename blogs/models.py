from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    '''Single post on the blog.'''
    #slug = models.SlugField(max_length=200 , unique=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        '''Return a string representation of the model.'''
        return f'{self.title} {self.owner} {self.text}'

class Comment(models.Model):
    '''Comment section for posts.'''
    post = models.ForeignKey(BlogPost, related_name="comments", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering= ['-date_added']

    def __str__(self):
        return f"{self.title} {self.owner} {self.text}"
