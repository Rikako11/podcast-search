import mygpoclient
from mygpoclient import public, api, feeds
from django.shortcuts import render, render_to_response
from operator import itemgetter
import feedparser
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from mygpoclient import locator
from mygpoclient import feeds
from . import mygpo

@csrf_exempt
def index(request):
    if request.method == 'POST':
        search_term = request.POST.get("search")
        tag_name = request.POST.get("tag")
        search_result = []
        if tag_name != "":
            tag_search = mygpo.client.get_podcasts_of_a_tag(tag_name)
            if search_term != "":
                for podcast in tag_search:
                    if search_term in podcast.title:
                        search_result.append(podcast)
            else:
                search_result = tag_search
        elif search_term !="":
            search_result = mygpo.client.search_podcasts(search_term)
        else:
            return render_to_response('podcast/index.html', {"error" : "Please fill one of the fields!"})        
        context = {"search_result": search_result,
                   "search_term":search_term,
                   "tag_name" : tag_name,
                   }
        
        return render_to_response('podcast/index.html', context)        
    else:
        return render_to_response('podcast/index.html', {"toptags": mygpo.top_tags_list,})


def subscribed(request):
    return render_to_response('podcast/subscribed.html', {"subscribed": mygpo.subscriptions})

def toptags(request):
    return render_to_response('podcast/toptags.html', {"toptags" : mygpo.top_tags_list})

def search_result(request):
    tag_name = request.GET['q']
    podcasts_from_tag = mygpo.client.get_podcasts_of_a_tag(tag_name)
    return render_to_response('podcast/search_result.html', {"podcasts" : podcasts_from_tag, "tag_name" : tag_name,})


def toppodcasts(request):
    podcasts= mygpo.client.get_toplist()
    return render_to_response('podcast/toppodcasts.html', {"podcasts" : podcasts})

def episodes(request):
    podcast_url = request.GET['q']
    episodes=[]
    feedlist = feedparser.parse(podcast_url)
    for entry in feedlist['entries']:
        for link in entry.links:
            if "audio/mpeg" == link.type:
                try: 
                    episode= mygpo.client.get_episode_data(podcast_url, link.href)
                    episodes.append(episode)
                except:
                    print("EPISODE DOES NOT EXIST:" + link.href)
                #episodes.append(mygpo.client.get_episode_data(podcast_url, link.href))
    return render_to_response('podcast/episodes.html' , {"episodes":episodes})

def login(request):
    return render_to_response('podcast/login_page.html')


    

    