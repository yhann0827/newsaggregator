from django.contrib import admin
from .models import NewsStory, Author

admin.site.register(NewsStory)
admin.site.register(Author)