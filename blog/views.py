from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import DetailView,CreateView,DeleteView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

#to understand basic view
# def home(request):
# 	context = {
# 	'posts': Post.objects.all()
# 	}
# 	return render(request, 'blog/home.html', context)

def about(request):
	return render(request, 'blog/about.html', {'title':'About'})

class PostDetailView(DetailView):
	model = Post
	#context_object_name = ...
	#template_name = ...  <app>/<model>_<viewtype>.html
	#ordering = ...

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content', 'image']
	#template -> <app>/<model>_form.html
	
	#overwrite default form-valid method
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostListView(ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'blog/home.html'
	ordering = ['-date_posted']

class PostDeleteView(DeleteView):
	model = Post
	success_url = '/'

	#checks if it is the right user
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class UserPostListView(ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'blog/user_posts.html'

	#overwritte the queryset
	def get_queryset(self):
		#kwargs = query parameter, user -> takes username from the url
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')




