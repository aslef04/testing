from django import forms
from . models import ProductAdding,RegisterViewModel
import re

class ProductAddingForm(forms.ModelForm):
    class Meta:
        model = ProductAdding
        fields = "__all__"


class RegisterViewForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = RegisterViewModel
        fields = "__all__"


    def clean_full_name(self):
        fullname = self.cleaned_data["full_name"]
        if len(fullname) < 4:
            raise forms.ValidationError("Enter valid Name")
        return fullname

    def clean_email(self):
        email=self.cleaned_data["email"]
        if RegisterViewModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password(self):
        password=self.cleaned_data["password"]
        if len(password) <8:
            raise forms.ValidationError("Password must contain 8 char")
        if not re.search(r'[A-Z]',password):
            raise forms.ValidationError("Password must contain one upper case")
        if not re.search(r'[a-z]',password):
            raise forms.ValidationError("Password must contain one lower case")
        if not re.search(r'[0-9]',password):
            raise forms.ValidationError("Password must contain one number")  
        if not re.search(r'[@!$%^&*()/]',password):
            raise forms.ValidationError("Password must contain one special charcter") 
        return password

    def clean(self):
        data = super().clean()
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if password and confirm_password:
            if password != confirm_password:
                self.add_error("confirm_password","password and confirm_password mismatch")
            return data

    
class UpdateForm(forms.ModelForm):
    class Meta:
        model = RegisterViewModel
        fields = "__all__"