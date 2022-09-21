from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm


# Create your views here.
def index(request):
  # if the method is POST
    if request.method == 'POST':
      form = PostForm(request.POST,request.FILES)
  # if the form is valid
      if form.is_valid():
  # Yes, save
       form.save()

  # redirect to home
       return HttpResponseRedirect('/')

      # get all posts, limit = 20
    posts = Post.objects.all().order_by('-created_at')[:20]

      # show
    return render(request, 'posts.html', {'posts': posts})


def delete(request, post_id):
  # find post
  post = Post.objects.get(id = post_id)
  post.delete()
  return HttpResponseRedirect('/')

def like(request,post_id):
  newlikecount = Post.objects.get(id=post_id)
  newlikecount.likecount +=1
  newlikecount.save()
  return HttpResponseRedirect('/')

def edit(request,post_id):
  post = Post.objects.get(id=post_id)
  if request.method =='POST':
    form = PostForm(request.POST,request.FILES,instance=post)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/')
    else:
      return HttpResponseRedirect(form.errors.as_json())
  return render(request,"edit.html",{"post":post})