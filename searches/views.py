import mygpoclient
from mygpoclient import public, api, feeds
from django.shortcuts import render, render_to_response
from operator import itemgetter
import json
from pprint import pprint
import feedparser

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from mygpoclient import locator
from mygpoclient import feeds

client = public.PublicClient() 
username = "user1117"
password = "password"

user = api.MygPodderClient(username, password)
toplist = client.get_toplist()
top_tags_list = client.get_toptags()
list = []
subscriptions=[]
for i in range(25):
    list.append(toplist[i].__dict__)
    subscriptions.append(toplist[i].url)
device = api.PodcastDevice('top25', 'mydevice', 'desktop', 0)
user.put_subscriptions(device.device_id, subscriptions)
list = list.sort(key=itemgetter('url'),reverse=False)
feedlist = feedparser.parse(toplist[0].url)
print(feedlist['namespaces'])

#print(client.get_episode_data(, toplist[0].website))
#print(list)

@csrf_exempt
def index(request):
    if request.method == 'POST':
        search_term = request.POST.get("search")
        tag_name = request.POST.get("tag")
        search_result = []
        if tag_name != "":
            tag_search = client.get_podcasts_of_a_tag(tag_name)
            if search_term != "":
                for podcast in tag_search:
                    if search_term in podcast.title:
                        search_result.append(podcast)
            else:
                search_result = tag_search
        elif search_term !="":
            search_result = client.search_podcasts(search_term)
        else:
            return render_to_response('podcast/index.html', {"error" : "Please fill one of the fields!"})        
        context = {"search_result": search_result,
                   "search_term":search_term,
                   "tag_name" : tag_name,
                   }
        
        return render_to_response('podcast/index.html', context)        
    else:
        return render_to_response('podcast/index.html', {"toptags": top_tags_list,})


def subscribed(request):
    list  = []
    devices = user.get_devices()
    for dev in devices:
        for podcast in user.get_subscriptions(dev):
            list.append(client.get_podcast_data(podcast))
    return render_to_response('podcast/subscribed.html', {"subscribed": list})

def toptags(request):
    return render_to_response('podcast/toptags.html', {"toptags" : top_tags_list})

def search_result(request):
    tag_name = request.GET['q']
    podcasts_from_tag = client.get_podcasts_of_a_tag(tag_name)
    return render_to_response('podcast/search_result.html', {"podcasts" : podcasts_from_tag, "tag_name" : tag_name,})


def toppodcasts(request):
    podcasts= client.get_toplist()
    return render_to_response('podcast/toppodcasts.html', {"podcasts" : podcasts})

def episodes(request):
    episodes_list = ha.toplist_uri()
    print(episodes_list)
    return render_to_response('podcast/episodes.html' , {"episodes":episodes_list})

def login(request):
    return render_to_response('podcast/login_page.html')


    

    