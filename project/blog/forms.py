from django_summernote import fields as summer_fields
from .models import *
from django import forms


class PostForm(forms.ModelForm):

    post = summer_fields.SummernoteTextFormField(error_messages={'required': (u'데이터를 입력해주세요'),})
    category_id = forms.CharField(label='')

    class Meta:
        model = SummerNote
        fields = ('title', 'post', 'category_id', )

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        qs = Category.objects.all()
        categoryList = [(category.id, category.label) for category in qs]

        self.fields['category_id'] = forms.CharField(label='', widget=forms.Select(choices=categoryList, attrs={
            'class': 'form-control'}))