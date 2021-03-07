from django import forms
from .models import  QuestionModel, AnswerModel, RequestModel


class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        fields = ('title', 'category', 'tags' , 'content',)
        labels = {
            'title': '',
            'category': '',
            'tags': '',
            'content': '',
        }
    
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'Form-Item-Input'
        self.fields['category'].widget.attrs['class'] = 'Form-Item-Select'
        self.fields['tags'].widget.attrs['class'] = 'Form-Item-Input'
        self.fields['content'].widget.attrs['class'] = 'Form-Item-Textarea'

class AnswerForm(forms.ModelForm):
    class Meta:
        model = AnswerModel
        fields = ('answer',)
        labels = {
            'answer': '',
        }

class RequestForm(forms.ModelForm):
    class Meta:
        model = RequestModel
        fields = ('subject', 'message')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs['class'] = 'Form-Item-Input'
        self.fields['message'].widget.attrs['class'] = 'Form-Item-Textarea'

