import json

from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from django.db.models import Q, Max
from ipware.ip import get_ip

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
            comment = Comment.objects.filter(post=post_id).order_by('parent', 'depth')
        except:
            raise Http404

        tag_list = []

        if (post.hashtag == ''):
            post.hashtag = None

        try:
            for x in post.hashtag.split(','):
                tag_list.append(x)

        except AttributeError as e:
            context = {'post': post, 'category': category, 'comment': comment}

        else:
            context = {'post': post, 'tags': tag_list, 'category': category, 'comment': comment}

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
    paginate_by = 10

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


class CommentView(View):
    def post(self, request):
        type = self.request.POST.get('type')
        ip = get_ip(self.request)
        ip_display = ip.replace(ip.split('.')[2], ' * ')
        ip_display = ip_display.replace(ip_display.split('.')[3], ' *')

        if type == 'publish':
            post = SummerNote.objects.get(id=request.POST.get('post_id'))

            cmt = Comment(author=self.request.POST['name'], published_date=timezone.now(),
                          comment=self.request.POST['comment'],
                          post=post, delete='N',
                          password=self.request.POST['passwd'], depth=1, ip=ip, ip_display=ip_display)

            cmt.save()

            cmt.parent = cmt.id
            cmt.save()

            SummerNote.objects.filter(id=request.POST.get('post_id')).update(noc=post.noc + 1)

            context = {'writer': self.request.POST['name'], 'comment': self.request.POST['comment'], 'id': cmt.id}
            return HttpResponse(json.dumps(context), content_type="application/json")

        elif type == 'reply':
            post = SummerNote.objects.get(id=request.POST.get('post_id'))
            depth = Comment.objects.filter(parent=self.request.POST.get('parent', 0)).aggregate(max=Max('depth'))['max'] + 1


            cmt = Comment(author=self.request.POST['name'], published_date=timezone.now(),
                          comment=self.request.POST['comment'],
                          post=post, delete='N',
                          password=self.request.POST['passwd'], depth=depth, ip=ip, ip_display=ip_display)

            cmt.save()

            cmt.parent = self.request.POST.get('parent', cmt.id)
            cmt.save()

            SummerNote.objects.filter(id=request.POST.get('post_id')).update(noc=post.noc + 1)


            context = {'writer': self.request.POST['name'], 'comment': self.request.POST['comment'], 'id': cmt.id}
            return HttpResponse(json.dumps(context), content_type="application/json")

        elif type == 'delete':
            id = self.request.POST.get('id', None)

            target = get_object_or_404(Comment, id=id)
            target.delete = 'Y'
            target.save()

            context = {'message': '삭제에 성공했습니다.'}

            return HttpResponse(json.dumps(context), content_type="application/json")

        elif type == 'check':
            id = self.request.POST.get('id', None)

            target = get_object_or_404(Comment, id=id)

            if self.request.POST.get('password') == target.password:
                context = {'message': 'success'}
            else:
                context = {'message': 'fail'}

            return HttpResponse(json.dumps(context), content_type="application/json")

