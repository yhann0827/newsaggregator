import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.core.serializers import serialize
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import NewsStorySerializer
from .models import NewsStory, Author
import json
import requests

# @api_view(['POST'])
@csrf_exempt
def HandleLogin (request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            welcome_message = f"You have successfully logged in. Welcome, {user.username}!"
            return HttpResponse(welcome_message, status=200)
        else:
            return HttpResponse('Invalid login. Invalid Username or Password.', status=401)
    else:
        #If the user does not use POST method 
        return HttpResponse('Invalid Method. The requested method is not allwoed for the requested resource', status=405)

@csrf_exempt
def HandleLogout(request):
    if request.method == 'POST':
        #User can only log out if he has already logged in before logging out
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized. Please log in to access the logout functionality.', status=401)
        else:
            logout(request)
            return HttpResponse('You have been successfully logged out.', status=200)
    else:
        return HttpResponse('Invalid Method. The requested method is not allowed for the requested resource', status=405)

@csrf_exempt
def HandleStory(request):
    # Post a Story
    if request.method == 'POST':
        # Pre-condition: User must be logged in before posting stories
        if not request.user.is_authenticated:
            return HttpResponse('User is not logged in. Please log in to post stories', status=401)
            
        #Check if the data is valid JSON
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse('Invalid JSON data', status=400)

        # Extract the story fields from the JSON data
        headline = data.get('headline')
        story_cat = data.get('category')
        story_region = data.get('region')
        story_details = data.get('details')

        # Check if any of the required fields are missing
        if not all([headline, story_cat, story_region, story_details]):
            return HttpResponse('Missing required fields', status=400)
        # Check if category and region values are valid
        if story_cat not in ["pol", "art", "tech", "trivia"]:
            return HttpResponse('Invalid category provided.', status=400)
        if story_region not in ["uk", "eu", "w"]:
            return HttpResponse('Invalid region provided.', status=400)

        try:
            # Get the corresponding Author instance for the logged-in user
            author = Author.objects.get(user=request.user)
        except Author.DoesNotExist:
            return HttpResponse('Author does not exist', status=404)

        try:
            # Create a new NewsStory object
            news_story = NewsStory.objects.create(
                headline=headline,
                story_cat=story_cat,
                story_region=story_region,
                story_details=story_details,
                story_date=datetime.datetime.now(),
                author=author
            )
            print("Author:", author)
        except Exception as e:
            return HttpResponse(f'Error occurred while creating story: {str(e)}', status=500)

        return HttpResponse('Story created successfully', status=201)

    elif request.method == 'GET':
        stories = NewsStory.objects.all()
        story_cat = request.GET.get('story_cat')
        story_region = request.GET.get('story_region')
        story_date = request.GET.get('story_date')

        # Check if the request is valid and filter the stories according to the request
        if story_cat != '*' and story_cat is not None:
            if story_cat not in ["pol", "art", "tech", "trivia"]:
                 return HttpResponse('Invalid category provided.', status=400)
            else:
                stories = stories.filter(story_cat=story_cat)
    
        # Check if story region is valid
        if story_region != '*' and story_region is not None:
            if story_region not in ["uk", "eu", "w"]:
                return HttpResponse('Invalid region provided.', status=400)
            else:
                stories = stories.filter(story_region=story_region)
        
        # Check if story date is valid
        if story_date != '*' and story_date is not None:
            try:
                datetime.datetime.strptime(story_date, '%d/%m/%Y')
            except ValueError:
                return HttpResponse('Invalid date format. Please use dd/mm/yyyy format.', status=400)
            else:
                story_date = datetime.datetime.strptime(story_date, '%d/%m/%Y').strftime('%Y-%m-%d')
                stories = stories.filter(story_date__gte=story_date)

        serialized_stories = []
        for story in stories:
            author_name = story.author.name if story.author else None
            serialized_story = {
                'key': story.id,
                'headline': story.headline,
                'story_cat': story.story_cat,
                'story_region': story.story_region,
                'author': author_name,
                'story_date': story.story_date.strftime('%Y-%m-%d'), 
                'story_details': story.story_details,
            }
            serialized_stories.append(serialized_story)

        if not stories:
            return HttpResponse('No Stories Found.', status=404)

        # Stories are returned in a JSON payload
        return JsonResponse(serialized_stories, safe=False)

    else:
        return HttpResponse('Invalid Method. The requested method is not allowed for the requested resource', status=405)

@csrf_exempt
def DeleteStory(request, key):
    # Pre-condition: User must be logged in to delete story
    if not request.user.is_authenticated:
        return HttpResponse('User not logged in. Please log in to access this service.', status=401)
    if request.method == 'DELETE':
        try:
            story = NewsStory.objects.get(pk=key)
        except:
            return HttpResponse('Story not found', status=404)

        if request.user != story.author.user:
            return HttpResponse('Unauthorised to delete this story. Only author of this story can delete the story.', status=403)
            
        story.delete()
        return HttpResponse('Story deleted successfully', status=200)

    else:
        return HttpResponse('Fail to delete story.', status=503)