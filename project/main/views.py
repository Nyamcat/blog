from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View
from statis.models import Visitor

# Create your views here.


class IndexView(View):
    def get(self, request):
        total_visit = len(Visitor.objects.all())
        today_visit = len(Visitor.objects.filter(date=timezone.now().date()))
        yesterday_visit = len(Visitor.objects.filter(date=timezone.now().date() + timezone.timedelta(days=-1)))
        context = {'total_visit': total_visit, 'today_visit': today_visit, 'yesterday_visit': yesterday_visit}
        return render(request, 'main/index.html', context)


class AboutView(View):
    def get(self, request):
        return render(request, 'main/about.html')