from django.shortcuts import render
from django.views import View

# Create your views here.


class WriteView(View):
    def get(self, request):
        return render(request, 'blog/write.html')

class BlogView(View):
    def get(self, request):
        return render(request, 'blog/blog.html')