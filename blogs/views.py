from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm


# Posts

def index(request):
    '''Home page'''
    return render(request, 'blogs/index.html')

def posts(request):
    '''Show all admin posts'''
    admin_posts = BlogPost.objects.filter(owner=1).filter(delete_flag=False).order_by('-date_added')
    context = {'posts': admin_posts}
    return render(request, 'blogs/posts.html', context)

def post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    #post = BlogPost.objects.get(id=post_id)
    context = {'post' : post}
    return render(request, 'blogs/post.html', context)

@login_required
def new_post(request):
    '''Add a new post'''
    if request.method != 'POST':
        # create blank form
        form = BlogPostForm()
    else:
        # post data submitted; process data
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()

            if request.user.is_superuser:
                return redirect('blogs:posts')
            else:
                return redirect('blogs:user_posts')
    # Display blank form
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    #post = BlogPost.objects.get(id=post_id)
    if post.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = BlogPostForm(instance=post)
    else:
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:post', post_id=post.id)
    context = {'post':post, 'form':form}
    return render(request, 'blogs/edit_post.html', context)

@login_required
def delete_post(request, post_id):
    post_to_delete = get_object_or_404(BlogPost, id=post_id)
    #post_to_delete = BlogPost.objects.get(id=post_id)
    if post_to_delete.owner != request.user:
        raise Http404
    else:
        if request.method == 'POST':
            post_to_delete.delete_flag = True
            post_to_delete.save()

            if request.user.is_superuser:
                return redirect('blogs:posts')
            else:
                return redirect('blogs:user_posts')
    context = {'post':post_to_delete}
    return render(request, 'blogs/delete_post.html', context)

# Comments

@login_required
def comment_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    #post = BlogPost.objects.get(id=post_id)
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.owner = request.user
            comment.save()
            return redirect('blogs:post', post_id=post_id)
    context = {'post':post, 'form': form}
    return render(request, 'blogs/comment_post.html', context)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    #comment = Comment.objects.get(id=comment_id)
    post = comment.post
    if comment.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            comment.owner = request.user
            form.save()
            return redirect('blogs:post', post_id=post.id)
    context = {'comment':comment, 'post':post, 'form':form}
    return render(request, 'blogs/edit_comment.html', context)

@login_required
def delete_comment(request, comment_id):
    comment_to_delete = get_object_or_404(Comment, id=comment_id)
    #comment_to_delete = Comment.objects.get(id=comment_id)
    post = comment_to_delete.post
    if comment_to_delete.owner != request.user:
        raise Http404
    else:
        if request.method == 'POST':
            comment_to_delete.delete()
            return redirect('blogs:post', post_id=post.id)
    context = {'comment':comment_to_delete, 'post':post}
    return render(request, 'blogs/delete_comment.html', context)


# User

@login_required
def user_posts(request):
    user_posts = BlogPost.objects.filter(delete_flag=False).exclude(owner=1).order_by('-date_added')
    context = {'user_posts': user_posts}
    return render(request, 'blogs/user_posts.html', context)
