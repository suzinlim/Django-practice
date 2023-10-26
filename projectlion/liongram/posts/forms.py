from django import forms
from .models import Post

# class PostBaseForm(forms.Form): form -> model과 비슷
#     CATEGORY_CHOICES = [
#         ('1', '일반'),
#         ('2', '계정'),
#     ]
#     image = forms.ImageField(label='이미지')
#     content = forms.CharField(label='내용', widget=forms.Textarea, required = True)
#     category = forms.ChoiceField(choices=CATEGORY_CHOICES) 
# django에서 폼을 정의해서 view에서 context로 html을 렌더링하면 동적으로 html 폼 태그를 자유롭게 다룰 수 있음

class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"

from django.core.exceptions import ValidationError
class PostCreateForm(PostBaseForm):
    class Meta(PostBaseForm.Meta):
        fields = ['image', 'content']
    
    def clean_content(self):
        data = self.cleaned_data['content']
        if "비속어" == data:
            raise ValidationError("'비속어'는 사용하실 수 없습니다.")
        
        return data

class PostUpdateForm(PostBaseForm):
    class Meta(PostBaseForm.Meta):
        fields = ['image', 'content']

class PostDetailForm(PostBaseForm):
    def __init__(self, *args, **kwargs):
        super(PostDetailForm, self).__init__(self, *args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['disabled'] = True