from django.shortcuts import render
from django.template import Context, loader 
from django.http import HttpResponse 
import models
from models import UserLink
from django.contrib.auth.models import User

def user_list(request): 
  user_list = User.objects.all()
  t = loader.get_template('rubbish_social_network/user_list.html') 
  c = Context({ 'user_list': user_list, }) 
  return HttpResponse(t.render(c)) 
 
def user_detail(request, id): 
  user = User.objects.get(pk=id) 
  t = loader.get_template('rubbish_social_network/user_detail.html') 
  c = Context({ 'user': user, }) 
  return HttpResponse(t.render(c))

def user_followers(request, username):
  link_list = UserLink.objects.all()
  user_list = User.objects.all()
  for i in user_list:
    if username == i.username:
      user = i
  user_followers = []
  for userlink in link_list:
    if userlink.to_user.username == user.username:
      user_followers.append(userlink.from_user)
  t = loader.get_template('rubbish_social_network/user_followers.html')
  c = Context ({ 'user_followers' : user_followers, })
  return HttpResponse(t.render(c))

def user_following(request, username):
  link_list = UserLink.objects.all()
  user_list = User.objects.all()
  for i in user_list:
    if username == i.username:
      user = i
  user_following = []
  for userlink in link_list:
    if userlink.from_user.username == user.username:
      user_following.append(userlink.to_user)
  t = loader.get_template('rubbish_social_network/user_following.html')
  c = Context ({ 'user_following' : user_following, })
  return HttpResponse(t.render(c))

# Create your views here.
