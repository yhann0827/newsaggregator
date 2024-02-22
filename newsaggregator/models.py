from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class NewsStory(models.Model):
    headline = models.CharField(max_length=64)
    CATEGORY_CHOICES = [
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivia'),
    ]
    story_cat = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    REGION_CHOICES = [
        ('uk', 'UK'),
        ('eu', 'EU'),
        ('w', 'World'),
    ]
    story_region = models.CharField(max_length=10, choices=REGION_CHOICES)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    story_date = models.DateField()
    story_details = models.CharField(max_length=128)

    def __str__(self):
        return self.headline

#References
#Django Field Choices: https://www.geeksforgeeks.org/how-to-use-django-field-choices/
