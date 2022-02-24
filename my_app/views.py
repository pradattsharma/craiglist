# import requests
from django.shortcuts import render
from .models import Search
from django.utils import timezone
import requests
import urllib
from bs4 import BeautifulSoup


# Create your views here.

BASE_CRAIGSLIST_URL = 'https://indore.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search=search, created=timezone.now())
    final_url = BASE_CRAIGSLIST_URL.format(urllib.parse.quote(search, safe=''))
    print(final_url)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_lists = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_lists:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    context = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'my_app/new_search.html', context)
