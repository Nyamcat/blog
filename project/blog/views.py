from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from .forms import PostForm
from .models import SummerNote

# Create your views here.


class WriteView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/write.html', {'form':form})

    def post(self, request):
        form = PostForm(self.request.POST)
        if form.is_valid():
            post = form.save()
            post.summer_field = request.POST['post']
            post.published_date = timezone.now()

            print(post.published_date)

            post.save()
        print(form)
        return redirect('blog')


class PostView(View):
    def get(self, request, post_id):
        try:
            post = SummerNote.objects.get(attachment_ptr_id=post_id)
        except:
            print('no post')
        return render(request, 'blog/post.html', {'post': post})


class BlogView(View):
    def get(self, request):
        recent_posts = SummerNote.objects.order_by('-published_date')[:5]

        for x in recent_posts:
            print(x)

        context = {'recent_posts': recent_posts}
        return render(request, 'blog/blog.html', context)