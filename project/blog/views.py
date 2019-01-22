import json
import re

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


# 전체글보기
class AllView(ListView):
    template_name = 'blog/all.html'
    paginate_by = 20

    def get_queryset(self):
        result = SummerNote.objects.filter(index__gte=1).order_by('-published_date')

        if (result):
            for x in result:
                x.published_date = date_parse(x.published_date)

        return result

    def get_context_data(self, **kwargs):
        context = super(AllView, self).get_context_data(**kwargs)

        categories = Category.objects.filter(use='Y')
        classify = Classify.objects.all()

        context['categories'] = categories
        context['classify'] = classify

        return context


# 방명록
class GuestBookView(View):
    def get(self, request):
        try:
            post = SummerNote.objects.get(index=0)
            comment = Comment.objects.filter(post=post.id, full_delete='N').order_by('parent', 'depth')
        except:
            raise Http404

        context = {'post': post, 'comment': comment}

        categories = Category.objects.filter(use='Y')
        classify = Classify.objects.all()

        context['categories'] = categories
        context['classify'] = classify

        return render(request, 'blog/guestbook.html', context)


# 글쓰기
class WriteView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'blog/write.html', {'form':form})

    def post(self, request):
        form = PostForm(self.request.POST)
        try:
            index = SummerNote.objects.all().aggregate(max=Max('index'))['max'] + 1
        except:
            index = 1

        if form.is_valid():

            post = form.save()
            post.summer_field = request.POST['post']
            post.published_date = timezone.now()
            post.index = index

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


# 게시글
class PostView(View):
    def get(self, request, post_id):
        ip = get_ip(self.request)
        post = get_object_or_404(SummerNote, attachment_ptr_id=post_id)
        category = get_object_or_404(Category, id=post.category_id)
        comment = Comment.objects.filter(post=post_id, full_delete='N').order_by('parent', 'depth')

        print('ip : ' + str(ip))

        try:
            hits = HitCount.objects.get(ip=ip, post=post)

        except Exception as e:
            print(e)
            hits = HitCount(ip=ip, post=post)
            SummerNote.objects.filter(attachment_ptr_id=post_id).update(hits=post.hits + 1)
            hits.save()

        else:
            if not hits.date == timezone.now().date():
                print(hits.date)
                print(timezone.now().date())
                print('first click')
                SummerNote.objects.filter(attachment_ptr_id=post_id).update(hits=post.hits + 1)
                hits.date = timezone.now()
            else:
                print(str(ip) + ' has already hit this post.\n\n')

        tag_list = []

        if post.hashtag == '':
            post.hashtag = None

        try:
            for x in post.hashtag.split(','):
                tag_list.append(x)

        except AttributeError as e:
            context = {'post': post, 'category': category, 'comment': comment}

        else:
            context = {'post': post, 'tags': tag_list, 'category': category, 'comment': comment}

        categories = Category.objects.filter(use='Y')
        classify = Classify.objects.all()

        context['categories'] = categories
        context['classify'] = classify

        # desc 태그
        cleaner = re.compile('<.*?>')
        desc = re.sub(cleaner, '', post.summer_field)
        desc = desc.replace('&lt;', '<')
        desc = desc.replace('&gt;', '>')
        desc = desc.replace('\r', ' ')
        desc = desc.replace('\n', ' ')

        context['description'] = desc

        return render(request, 'blog/post.html', context)


# 블로그 메인화면
class BlogView(View):
    def get(self, request):
        recent_posts = SummerNote.objects.filter(index__gte=1).order_by('-published_date')[:20]
        tags = HashTag.objects.order_by('-nou')[:3]
        categories = Category.objects.filter(use='Y')
        classify = Classify.objects.all()
        comment = Comment.objects.filter(delete='N', full_delete='N', depth=1, post__index=0).order_by('-published_date')[:5]

        for x in recent_posts:
            x.published_date = date_parse(x.published_date)

        context = {'recent_posts': recent_posts, 'tags': tags, 'categories': categories, 'classify': classify, 'comment': comment}



        return render(request, 'blog/blog.html', context)


# 검색
class SearchView(ListView):
    template_name = 'blog/search.html'
    paginate_by = 20

    def get_queryset(self):
        self.keyword = self.request.GET['keyword']
        keyword = self.keyword

        result = SummerNote.objects.filter(title__contains=keyword, index__gte=1).order_by('-published_date')

        if (result):
            for x in result:
                x.published_date = date_parse(x.published_date)

        return result

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword

        categories = Category.objects.filter(use='Y')
        classify = Classify.objects.all()

        context['categories'] = categories
        context['classify'] = classify
        context['description'] = self.keyword + '검색 결과'

        return context


# 태그 검색
class TagView(ListView):
    template_name = 'blog/tags.html'
    paginate_by = 20

    def get_queryset(self):

        self.tags = self.request.GET.get('taglist')

        tag_list = []
        for x in self.tags.split(','):
            tag_list.append(x)

        post = SummerNote.objects

        for x in self.tags.split(','):
            post = post.filter(Q(tag1__icontains=x) | Q(tag2__icontains=x) |
                                             Q(tag3__icontains=x)| Q(tag4__icontains=x) |
                                             Q(tag5__icontains=x), index__gte=1)

        post = post.distinct().order_by('-published_date')
        self.count = 0

        if post:
            self.count = len(post)
            for x in post:
                x.published_date = date_parse(x.published_date)



        return post

    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        context['keyword'] = self.tags
        context['count'] = self.count

        categories = Category.objects.filter(use='Y')
        classify = Classify.objects.all()

        context['categories'] = categories
        context['classify'] = classify

        context['description'] = self.tags + '태그는 ' + str(self.count) + '개의 게시글에 태그되었습니다.'

        return context


# 카테고리 검색
class CategoryView(ListView):
    template_name = 'blog/category.html'
    paginate_by = 20

    def get_queryset(self):
        self.keyword = self.kwargs['keyword']
        keyword = self.keyword

        catgory = Category.objects.get(title=keyword)

        post = SummerNote.objects.filter(category_id=catgory.id, index__gte=1).order_by('-published_date')
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

        categories = Category.objects.filter(use='Y')
        classify = Classify.objects.all()

        context['categories'] = categories
        context['classify'] = classify
        context['description'] = self.keyword + '카테고리에는 게시글이 ' + str(self.count) + '개 있습니다.'

        return context


# 댓글
class CommentView(View):
    def post(self, request):
        type = self.request.POST.get('type')
        ip = get_ip(self.request)
        ip_display = ip.split('.')[0]+ '.' + ip.split('.')[1] + '. * . *'

        if type == 'publish':
            post = SummerNote.objects.get(id=request.POST.get('post_id'))

            cmt = Comment(author=self.request.POST['name'], published_date=timezone.now(),
                          comment=self.request.POST['comment'], email=self.request.POST['email'],
                          post=post, delete='N', full_delete = 'N',
                          password=self.request.POST['passwd'], depth=1, ip=ip, ip_display=ip_display)

            cmt.save()

            cmt.parent = cmt.id

            if self.request.user.is_active:
                cmt.user = self.request.user

            cmt.save()

            SummerNote.objects.filter(id=request.POST.get('post_id')).update(noc=post.noc + 1)

            context = {'writer': self.request.POST['name'], 'comment': self.request.POST['comment'], 'id': cmt.id}
            return HttpResponse(json.dumps(context), content_type="application/json")

        elif type == 'reply':
            post = SummerNote.objects.get(id=request.POST.get('post_id'))
            depth = Comment.objects.filter(parent=self.request.POST.get('parent', 0)).aggregate(max=Max('depth'))['max'] + 1

            cmt = Comment(author=self.request.POST['name'], published_date=timezone.now(),
                          comment=self.request.POST['comment'], email=self.request.POST['email'],
                          post=post, delete='N', full_delete = 'N',
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
            btw = ((timezone.now() - target.published_date).seconds // 60 ) % 60

            if btw <= 10:
                target.full_delete = 'Y'
                Comment.objects.filter(parent=id).update(full_delete='Y')
            else:
                target.delete = 'Y'

            target.save()

            context = {'message': '삭제에 성공했습니다.'}

            post = SummerNote.objects.get(id=request.POST.get('post_id'))
            SummerNote.objects.filter(id=request.POST.get('post_id')).update(noc=post.noc - 1)

            return HttpResponse(json.dumps(context), content_type="application/json")

        elif type == 'check':
            id = self.request.POST.get('id', None)

            target = get_object_or_404(Comment, id=id)

            if self.request.POST.get('password') == target.password:
                context = {'message': 'success'}
            else:
                context = {'message': 'fail'}

            return HttpResponse(json.dumps(context), content_type="application/json")
