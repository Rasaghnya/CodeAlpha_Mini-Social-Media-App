from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, CommentForm
@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/create_post.html', {'form': PostForm(), 'posts': posts, 'comment_form': CommentForm()})

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.author == request.user:
        post.delete()
    return redirect('home')

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('home')


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('home')

# @login_required
# def total_likes(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     return post.likes.count()