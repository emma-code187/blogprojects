from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post, Comment
from users.models import Profile
from .forms import CommentForm, AuthorComment
from django.contrib.auth.decorators import login_required




def home(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html', context) 


class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted'] 
	paginate_by = 2

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts' 
	paginate_by = 2

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'post_image', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'post_image', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False
	

def about(request):
	return render(request, 'blog/about.html', {'title': 'About'}) 
	
@login_required
def create_post(request):
	user = request.user
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = user
			post.save()
			return redirect('blog-home')
			#return redirect('post-detail', pk=post.pk)
			#return render(request, 'blog/post_detail.html', {'form': form})
	else:
		form = PostForm()
		return render(request, 'blog/post_form.html', {'form': form})





@login_required
def add_comment_to_post(request, pk):
	user = request.user
	#user = get_object_or_404(User, username=self.kwargs.get('username'))
	post = get_object_or_404(Post, pk=pk)
	#profile = get_object_or_404(Profile, user=user)
	#user = get_object_or_404(User, username=self.kwargs.get('username'))
	#email = user.email
	#image = profile.image.url
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.name = user
			#comment.image = image
			#comment.email = email
			comment.save()
			return redirect('post-detail', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form': form})
# Create your views here.
@login_required
def comment_block(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.active is True:
    	comment.active = False
    	comment.save()
    	return redirect('post-detail', pk=comment.post.pk)
    else:
    	comment.active = True
    	comment.save()
    	return redirect('post-detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', pk=comment.post.pk)

