from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from .models import CustomUser
from django import forms


class UserAddForm(UserCreationForm):
    class Meta:
        model = CustomUser 
        # fields = "__all__"
        fields = ["username","phone","pro_pic","email","first_name","last_name","password1","password2"]


        widgets = {
            "username":forms.TextInput(attrs={"class":"form-control", "placeholder":"Username"}),
            "phone":forms.NumberInput(attrs={"class":"form-control","placeholder":"Phone Number"}),
            "pro_pic":forms.FileInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control","placeholder":"Email"}),
            "first_name":forms.TextInput(attrs={"class":"form-control", "placeholder":"First Name"}),
            "last_name":forms.TextInput(attrs={"class":"form-control", "placeholder":"Last Name"}),
        
        }

    def __init__(self, *args, **kwargs):
        super(UserAddForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control  py-3', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control  py-3', 'placeholder': 'Password confirmation'})


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser 
        # fields = "__all__"
        fields = ["username","phone","pro_pic","email","first_name","last_name","password"]


        widgets = {
            "username":forms.TextInput(attrs={"class":"form-control", "placeholder":"Username"}),
            "phone":forms.NumberInput(attrs={"class":"form-control","placeholder":"Phone Number"}),
            "pro_pic":forms.ClearableFileInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control","placeholder":"Email"}),
            "first_name":forms.TextInput(attrs={"class":"form-control", "placeholder":"First Name"}),
            "last_name":forms.TextInput(attrs={"class":"form-control", "placeholder":"Last Name"}),
        
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control  py-3', 'placeholder': 'Password'})
       
