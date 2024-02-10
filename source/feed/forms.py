from django.forms import ModelForm, Textarea
from feed.models import PostModel, CommentModel
from django import forms

class PostForm(ModelForm):
    class Meta:
        model = PostModel
        fields = [
            'image',
            'title',
            'text',
            'category',
            'price'
        ]
        widgets = {
            'text' : forms.Textarea(attrs={'placeholder': 'Описание', 'class': 'input_box text_box'}),
            'title' : forms.TextInput(attrs={'placeholder': 'Название', 'class': 'input_box text_box'}),
            'price' : forms.NumberInput(attrs={'placeholder': 'Цена', 'class': 'input_box text_box'}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = CommentModel
        fields = [
            'text'
        ]
        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Оставьте комментарий',
                'style': "height: 150px"
            })
        }