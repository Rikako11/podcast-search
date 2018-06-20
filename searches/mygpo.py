import mygpoclient
from mygpoclient import public, api, simple
from django.shortcuts import render, render_to_response
import feedparser

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.template.defaulttags import register
...

client = public.PublicClient() 
username = "user1117"
password = "password"

user = api.MygPodderClient(username, password)
toplist = client.get_toplist()
top_tags_list = client.get_toptags()
list = []
subscriptions=[]
subscriptions_url=[]
device = api.PodcastDevice('top25', 'mydevice', 'desktop', 0)

for i in range(25):
    list.append(toplist[i].__dict__)
    subscriptions.append(toplist[i].__dict__)
    subscriptions_url.append(toplist[i].url)

user.put_subscriptions(device.device_id, subscriptions_url)



