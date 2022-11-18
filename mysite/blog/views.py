from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, ListView, 
                                    DetailView, CreateView, 
                                    UpdateView, DeleteView)

from django.http import HttpResponseRedirect
                                    


# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        # This allows us to use django's ORM when dealing with just generic views
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        # __lte stands for less than or equal to
        # The - in front of published_date states order by published date in a decending order; so the most recent comes up first or at the top of the list view


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class CreatePostView(LoginRequiredMixin,CreateView):
    # while we were working with function based views, we used decorators but now we are working with class based views we are using mixins.
    # We are going to inherit from both classes.
    login_url = '/login/'
    redirect_field_name = 'post_detail'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')




#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('blog:post_detail',pk=post.pk)
    # return render(request=request, template_name="login.html", context={"login_form":form})


@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method =='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('blog:post_detail',pk=post.pk)
    else:
        form=CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail',pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail', pk=post_pk)
