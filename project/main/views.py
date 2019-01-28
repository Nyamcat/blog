from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View, FormView, UpdateView
from statis.models import Visitor

# Create your views here.
from .forms import SignUpForm, ProfileForm


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


class SignupView(FormView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = '/accounts/login/'

    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()  # load the profile instance created by the signal

        user.save()

        return super(SignupView, self).form_valid(form)


class ProfileView(FormView):
    form_class = ProfileForm
    template_name = 'registration/profile.html'
    success_url = '/accounts/profile/'

    def form_valid(self, form):
        self.request.user.email = self.request.POST.get('email')
        self.request.user.first_name = self.request.POST.get('first_name')

        if self.request.POST.get('subscribe', None):
            self.request.user.profile.subscribe = True
        else:
            self.request.user.profile.subscribe = False

        self.request.user.save()
        self.request.user.profile.save()

        return super(ProfileView, self).form_valid(form)

    def form_invalid(self, form):
        return super(ProfileView, self).form_invalid(form)
