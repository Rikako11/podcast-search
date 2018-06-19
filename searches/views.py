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
                   "request" : request.method,
                   }
        
        return render_to_response('podcast/index.html', context)        
    else:
        return render_to_response('podcast/index.html', {"toptags": mygpo.top_tags_list,})


def subscribed(request):
    recommended = mygpo.smartSorting(mygpo.subscriptions)
    return render_to_response('podcast/subscribed.html', {"subscribed": mygpo.subscriptions,
                                                          "recommended": recommended[:5]})

def toptags(request):
    return render_to_response('podcast/toptags.html', {"toptags" : mygpo.top_tags_list})

def search_result(request):
    tag_name = request.GET['q']
    podcasts_from_tag = mygpo.client.get_podcasts_of_a_tag(tag_name)
    return render_to_response('podcast/search_result.html', {"podcasts" : podcasts_from_tag, "tag_name" : tag_name,})

def toppodcasts(request):
    podcasts= mygpo.client.get_toplist()
    print(podcasts[0].__dict__)
    return render_to_response('podcast/toppodcasts.html', {"podcasts" : podcasts})

def episodes(request):
    podcast_url = request.GET['q']
    episodes=[]
    links=[]
    feedlist = feedparser.parse(podcast_url)
    for entry in feedlist['entries']:
        for link in entry.links:
            if "audio/mpeg" == link.type:
                try: 
                    details=[]
                    print(link)
                    print(entry.keys())
                    details.append(entry.title)
                    details.append(entry.author)
                    details.append(entry.summary)
                    details.append(link.href)
                    details.append(entry.published)
                    links.append(details)
                    episodes.append(mygpo.client.get_episode_data(podcast_url, link.href))
                except:
                    print()
                    
                #episodes.append(mygpo.client.get_episode_data(podcast_url, link.href))
    return render_to_response('podcast/episodes.html' , {"episodes":episodes,
                                                         "links": links,
                                                         "podcast":podcast_url})

def login(request):
    if request.method=="POST":
        try:
            username = request.POST.get('user')
            password = request.POST.get('pass')
            user = api.MygPodderClient(username, password)
            
        except :
            print("invalid!")
            return render_to_response('podcast/login.html', {"error" : "Invalid Username or Password!"})
    response = render_to_response("template.html", {})
    response['Cache-Control'] = 'no-cache'
    return response

    