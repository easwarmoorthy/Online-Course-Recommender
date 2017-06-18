from django import forms
from .models import *
from django.contrib.auth import(
        authenticate,
        get_user_model,
        login,
        logout,
        )

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length = 16)
    password = forms.CharField(widget = forms.PasswordInput)
    def clean(self , *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError("User Name or Password is Incorrect")
        return super(UserLoginForm,self).clean(*args,**kwargs)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password']:
            self.fields[fieldname].help_text = None

class SearchForm(forms.Form):
    keyword = forms.CharField(widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['keyword'].label = ""


"""class QuoteForm(forms.ModelForm):
    class Meta:
        model = QuoteModel
        fields =[
            'quote',
            'qname'
        ]
        labels = {
            'quote': ('Your Quote'),
            'qname': ('Your Name')
        }
"""
