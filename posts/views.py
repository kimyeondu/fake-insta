from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm, ImageForm, CommentForm
from django.db.models import Q
from itertools import chain
from .models import Post, Image, Comment
# Create your views here.

def list(request):
    #1
    followings = user__in=request.user.followings.all()
    posts = Post.objects.filter(
        Q(user__in=followings) | Q(user=request.user.id)).order_by('-pk')
    
    #2
    # followings = request.user.followings.all()
    # chain_followings = chain(followings, [request.user])    # iterable끼리만 합칠 수 있음
    # posts = Post.objects.filter(user_in=followings).order_by('-pk')
    
    # posts = Post.objects.filter(user__in=request.user.followings.all()).order_by('-pk')
    # posts = get_list_or_404(Post.objects.order_by('-pk'))
    comment_form = CommentForm()
    context = {
        'posts':posts,
        'comment_form':comment_form,
    }
    return render(request, 'posts/list.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False) # 게시글 내용 처리 끝
            post.user = request.user
            post.save()
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect('posts:list')
    else:
        post_form = PostForm()
        image_form = ImageForm()
        context = {
            'post_form':post_form,
            'image_form':image_form,
        }
    return render(request, 'posts/form.html', context)

@login_required  
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.user != request.user:
        return redirect('posts:list')
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    else:
        post_form = PostForm(instance=post)
        context = {
            'post_form':post_form
        }
    return render(request, 'posts/form.html', context)

@login_required
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.user != request.user:
        return redirect('posts:list')
    if request.method == 'POST':
        post.delete()
    return redirect('posts:list')
    
    
@login_required
def create_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post_id = post_pk
            comment.user = request.user
            comment.save()
    return redirect('posts:list')

@login_required   
def delete_comment(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user != request.user:
        return redirect('posts:list')
    if request.method == 'POST':
        comment.delete()
    return redirect('posts:list')
    
@login_required
def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # 1
    # 이미 해당 유저가 like_users 에 존재하면 해당 유저를 삭제
    # 이미 해당 유저가 like를 누른 상태면 좋아요 취소
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    # 없으면 좋아요 추가
    else:
        post.like_users.add(request.user)
    return redirect('posts:list')
    
    # 2
    # user = request.user
    # if post.like_users.filter(pk=user.pk).exists():
    #     post.like_users.remove()
    # else:
    #     post.like_users.add(user)
    # return redirect('posts:list')

@login_required
def explore(request):
    posts = Post.objects.order_by('-pk')
    # posts = Post.objects.exclude(user=request.user).order_by('-pk')
    comment_form = CommentForm()
    context = {
        'posts':posts,
        'comment_form':comment_form,
    }
    return render(request, 'posts/explore.html', context)