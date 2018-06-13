from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from django.db.models import Q

from .forms import PostForm
from .models import *

# Create your views here.


def date_parse(date):
    date = date.strftime('%Y-%m-%d')
    return date


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

            tags = request.POST.get('hashtag')
            if tags != '':
                tag_list = []

                post.hashtag = tags

                for x in tags.split(','):
                    tag_list.append(x)
                    try:
                        tag_object = HashTag.objects.get(title=x)
                    except:
                        HashTag.objects.create(title=x, nou=1)
                    else:
                        HashTag.objects.filter(title=x).update(nou=tag_object.nou + 1)

                index = 1

                for x in tag_list:
                    name = 'tag' + str(index)
                    setattr(post, name, x)
                    index += 1

            try:
                category_object = Category.objects.get(id=request.POST.get('category_id'))
            except:
                raise Http404

            post.category = category_object
            Category.objects.filter(id=request.POST.get('category_id')).update(nou=category_object.nou + 1)

            post.save()
        return redirect('blog')


class PostView(View):
    def get(self, request, post_id):
        try:
            post = SummerNote.objects.get(attachment_ptr_id=post_id)
            SummerNote.objects.filter(attachment_ptr_id=post_id).update(hits=post.hits + 1)
            category = Category.objects.get(id=post.category_id)
        except:
            raise Http404

        tag_list = []

        if (post.hashtag == ''):
            post.hashtag = None

        try:
            for x in post.hashtag.split(','):
                tag_list.append(x)

        except AttributeError as e:
            context = {'post': post, 'category': category}

        else:
            context = {'post': post, 'tags': tag_list, 'category': category}

        return render(request, 'blog/post.html', context)


class BlogView(View):
    def get(self, request):
        recent_posts = SummerNote.objects.order_by('-published_date')[:10]
        tags = HashTag.objects.order_by('-nou')[:3]

        for x in recent_posts:
            x.published_date = date_parse(x.published_date)

        context = {'recent_posts': recent_posts, 'tags': tags}
        return render(request, 'blog/blog.html', context)


class SearchView(ListView):
    template_name = 'blog/search.html'
    paginate_by = 10

    def get_queryset(self):
        self.keyword = self.kwargs['keyword']
        keyword = self.keyword

        print(keyword)

        result = SummerNote.objects.filter(title__contains=keyword)

        print(result)

        if (result):
            for x in result:
                x.published_date = date_parse(x.published_date)

        return result

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword

        print(context)

        return context


class TagView(ListView):
    template_name = 'blog/tags.html'
    paginate_by = 2

    def get_queryset(self):
        self.keyword = self.kwargs['keyword']
        keyword = self.keyword

        post = SummerNote.objects.filter(Q(tag1__icontains=keyword) | Q(tag2__icontains=keyword) |
                                         Q(tag3__icontains=keyword)| Q(tag4__icontains=keyword) |
                                         Q(tag5__icontains=keyword)).distinct()
        self.count = 0

        if post:
            self.count = len(post)
            for x in post:
                x.published_date = date_parse(x.published_date)

        return post

    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['count'] = self.count

        return context


class CategoryView(ListView):
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self):
        self.keyword = self.kwargs['keyword']
        keyword = self.keyword

        catgory = Category.objects.get(title=keyword)

        post = SummerNote.objects.filter(category_id=catgory.id)
        self.count = 0

        if post:
            self.count = len(post)
            for x in post:
                x.published_date = date_parse(x.published_date)

        return post

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['count'] = self.count

        return context

