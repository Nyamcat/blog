from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    subscribe = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ('first_name', 'username', 'password1', 'password2', 'email', 'subscribe')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True
        self.fields['subscribe'].required = False


class ProfileForm(forms.ModelForm):
    subscribe = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ('first_name', 'email', 'subscribe')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True
        self.fields['subscribe'].required = False
