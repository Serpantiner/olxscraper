import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from urllib.parse import quote_plus #adding plus sign in search
from . import models

BASE_URL = 'https://www.olx.ua/list/q-{}'



# Create your views here.
def home(request):
    return render(request,'base.html')
def new_search(request):
    search=request.POST.get('search') #pull data out of search bar # that post request we are fetching
    #search model gives to searches to database
    models.Search.objects.create(search=search) #model creating search object with search argument is search and feeds to search request
    final_url = BASE_URL.format(quote_plus(search)) #плюсуем наш серч из многих слов
    response = requests.get(final_url)
    data= response.text #spit out text
    soup= BeautifulSoup(data, features='html.parser')



    post_listings = soup.find_all('div', {'class': 'rel listHandler'}) # тут ты захватываешь весь контент и парисишь прайс,татйтл и т.д с него


    final_postings= []

    for post in post_listings: #looping through each post and show text
        post_titles = post.find('a',class_= ['marginright5 link linkWithHash detailsLink',
                                         'marginright5 link linkWithHash detailsLink linkWithHashPromoted',
                                        ]).text
        post_url = post.find('a',class_= ['marginright5 link linkWithHash detailsLink',

                                          'marginright5 link linkWithHash detailsLink linkWithHashPromoted']).get('href')


        if post.find('div',class_= 'space inlblk rel'): #if we have a price than show if not NA
            post_price = post.find('div',class_= 'space inlblk rel').text
        else:
            post_price= 'N/A'

        if post.find('img',class_='fleft').get('src'):
            post_image= post.find(class_='fleft').get('src')

        else:
            post_image= 'https://cutt.ly/FnA2cK7'


        final_postings.append((post_titles,post_url,post_price,post_image)) #modifying the list of what we will be returning in new_Serach.html

    stuff_for_frontend = {'search':search, 'final_postings':final_postings,}
    return render(request, 'my_app/new_search.html',stuff_for_frontend)



