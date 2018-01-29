from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'main/index.html')

class WriteView(View):
    def get(self, request):
        return render(request, 'blog/write.html')

class BlogView(View):
    def get(self, request):
        return render(request, 'blog/blog.html')