from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user doesnot exists")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is not active")
            return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput)
    email2 = forms.EmailField(label="Confirm Email", widget=forms.EmailInput)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'email2', 'password']

    def clean_email2(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email != email2:
            raise forms.ValidationError("Email did not match")
        email_qs = User.objects.filter(email=email)
        print(email_qs, email_qs.exists())
        if email_qs.exists():
            raise forms.ValidationError(
                "This email has been already registered")
        return email
