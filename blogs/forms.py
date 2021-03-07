from django import forms


# 12/27斉藤コメント　コンタクトフォーム 
class ContactForm(forms.Form):
    contact_email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'メールアドレス'}),
    )
    contact_subject = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '件名'}),
    )
    contact_message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'メッセージ'}),
    )

# CSSのためのクラス
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_email'].widget.attrs['class'] = 'Form-Item-Input'
        self.fields['contact_subject'].widget.attrs['class'] = 'Form-Item-Input'
        self.fields['contact_message'].widget.attrs['class'] = 'Form-Item-Textarea'

