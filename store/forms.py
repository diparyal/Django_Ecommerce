from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _

class UserForm(UserCreationForm):
    #Edit label
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        # fields = '__all__'
        
        fields = ['username','email','password1','password2']
        widgets = {
        'username': forms.fields.TextInput(attrs={'placeholder': 'Your Name'}),
        'email': forms.fields.TextInput(attrs={'placeholder': 'Email Address'})
        # 'password1': forms.fields.CharField(attrs={'placeholder': 'Password'}),
        # 'password2': forms.fields.CharField(attrs={'placeholder': 'Password confirmation'})
        }


        # def __init__(self, *args, **kwargs):  
        #     super(SignUpForm, self).__init__(*args, **kwargs)
        #     self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password from numbers and letters of the Latin alphabet'})
        #     self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'})


        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['username'].widget.attrs.update({'placeholder':_('Username')})
        #     self.fields['email'].widget.attrs.update({'placeholder':_('Email')})
        #     self.fields['password1'].widget.attrs.update({'placeholder':_('Password')})        
        #     self.fields['password2'].widget.attrs.update({'placeholder':_('Repeat password')})
        
        

        # def __init__(self,*args,**kwargs):
        #     super().__init__(*args,**kwargs)
        #     self.fields['username'].label = 'Your Name'
        #     self.fields['email'].label = 'Email Address'
        #     self.fields['password1'].label = 'Password'
        #     self.fields['password2'].label = 'Password confirmation'
      

class loginForm(forms.Form):
    username =  forms.CharField(label='Your Name', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
  