from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q, Count
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from accounts.models import Profile

from .models import Comment, Post
from .forms import PostForm

# Create your views here.

def home(request, *args, **kwargs):
    posts = Post.objects.all()
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    posts = Post.objects.filter(
        Q(title__icontains=q)|
        Q(content__icontains=q)
    )

    if request.GET.get('tag'):
        tag = request.GET.get('tag')
        posts = Post.objects.filter(tags__name=tag)

    
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    



    context = {'posts':posts}
    return render(request, 'myapp/home.html', context)


def detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    try:
        post = get_object_or_404(Post, slug=slug)
    except Post.DoesNotExist:
        raise Http404
    except Post.MultipleObjectsReturned:
        post = Post.objects.filter(slug=slug).first()
    likes = post.likes.all()
    post_comments = post.comment_set.all()

    hit_count = get_hitcount_model().objects.get_for_object(post)
    hits = hit_count.hits
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits += 1
        

    tag = post.tags
    tags = tag.names()

    if request.method == 'POST':
        comment = Comment.objects.create(
            user = request.user,
            post = post,
            content = request.POST.get('comment')
        )
        
        return redirect('detail', slug=post.slug)
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    posts = Post.objects.filter(tags__in=post_tags_ids).exclude(slug=post.slug)
    posts = posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:3]
    

    context = {
        'post':post, 
        'post_comments':post_comments, 
        'likes':likes, 
        'tags':tags,
        'posts':posts,
        'hits':hits
        }
    return render(request, 'myapp/detail.html', context)

@login_required
def myPost(request, pk):
    user = User.objects.get(id=pk)
    print(user)
    posts = Post.objects.all().filter(author=user)

    return render(request, 'myapp/myPost.html', {'posts':posts})


@login_required(login_url='login')
def likeView(request, post):
    post = get_object_or_404(Post, id=request.POST.get('comment_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('detail', args=[str(post.slug)]))

@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'myapp/create.html', {'form':form})

@login_required(login_url='login')
def updatePost(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(instance=post)
    
    
    if request.user != post.author:
        return HttpResponse("Sizga ruxsat yo'q!")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post tahrirlandi!")
            return redirect('detail', slug=post.slug)

    return render(request, 'myapp/update.html', {'form':form})

@login_required(login_url='login')
def deletePost(request, slug=None):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        return HttpResponse("Sizga ruxsat yo'q!")

    if request.method == 'POST':
        post.delete()
        messages.error(request, "Post o'chirildi!")
        return redirect('home')
    context = {"obj":post}
    return render(request, 'myapp/delete.html', context)


@login_required
def deleteComment(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    if request.user != comment.user:
        return HttpResponse("Sizga ruxsat yo'q!")

    if request.method == 'POST':
        comment.delete()
        return redirect('home')

    context = {'obj':comment}

    return render(request, 'myapp/delete.html', context)


@login_required
def updateComment(request, slug=None):
    page = 'update-comment'
    comment = Comment.objects.get(id=slug)

    post = comment.post
    likes = post.likes.all()
    post_comments = post.comment_set.all()
    editComment = post.comment_set.get(id=slug)
    if request.method == 'POST':
        comment = Comment.objects.filter(id=slug).update(
            user = request.user,
            post = post,
            content = request.POST.get('comment'),
            updated=timezone.now()
        )
        return redirect('detail', slug=post.slug)
    
    context = {'post':post, 'post_comments':post_comments, 'likes':likes, 'page':page,'edit_comment':editComment}

    return render(request, 'myapp/detail.html', context)
