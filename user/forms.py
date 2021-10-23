from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class RegForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=30,
        min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username"}))
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Email"}))
    password = forms.CharField(
        label="Password",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    password_confirmation = forms.CharField(
        label="Confirm password",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Confirm password"}))
    verification_code = forms.CharField(
        label="Verification code",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Verification code"}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
        verification_code_server = self.request.session.get('register_vc', '')
        verification_code_client = self.cleaned_data.get('verification_code', '')
        if not (verification_code_server != '' and verification_code_server == verification_code_client):
            raise forms.ValidationError("Verification code is incorrect")
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password_confirmation(self):
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']
        if password != password_confirmation:
            raise forms.ValidationError("Passwords are not the same")
        return password_confirmation

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError("Verification code is blank")
        return verification_code


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username/Email",
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': "Username/Email"}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        #try login by username
        user = auth.authenticate(username=username_or_email, password=password)

        if user is None:
            # try login by email
            if User.objects.filter(email=username_or_email):
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            # both failed
            raise forms.ValidationError("Username or email is incorrect")
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class ChangeDisplayNameForm(forms.Form):
    displayname_new = forms.CharField(
        label='New nickname',
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': "New nickname"}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeDisplayNameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError("Not logged in")
        return self.cleaned_data

    def clean_displayname_new(self):
        displayname_new = self.cleaned_data.get('displayname_new', '').strip()
        if displayname_new == '':
            raise forms.ValidationError("New nickname cannot be blank")
        return displayname_new


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': "New Email"}
        )
    )
    verification_code = forms.CharField(
        label="Verification code",
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': "Send verification code to email"}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ChangeEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断登录状态
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError("Not logged in")
        # 判断Verification code
        verification_code_server = self.request.session.get('change_email_vc', '')
        verification_code_client = self.cleaned_data.get('verification_code', '')
        if not (verification_code_server != '' and verification_code_server == verification_code_client):
            raise forms.ValidationError("Verification code is incorrect")
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError("Verification code cannot be blank")
        return verification_code


class ChangePasswordForm(forms.Form):
    password_old = forms.CharField(
        label="Current password",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Current password"}))
    password_new = forms.CharField(
        label="New password",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "New password"}))
    password_confirmation = forms.CharField(
        label="Confirm new password",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Confirm new password"}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        password_new = self.cleaned_data.get('password_new')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password_new == '' or password_new != password_confirmation:
            raise forms.ValidationError("Passwords are not the same")
        return self.cleaned_data

    def clean_password_old(self):
        password_old = self.cleaned_data.get('password_old', '')
        if not self.request.user.check_password(password_old):
            raise forms.ValidationError("Current password is incorrect")
        return password_old


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Email"}))
    password_new = forms.CharField(
        label="New password",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "New password"}))
    password_confirmation = forms.CharField(
        label="Confirm new password",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Confirm new password"}))
    verification_code = forms.CharField(
        label="Verification code",
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': "Send verification code to email"}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        password_new = self.cleaned_data.get('password_new')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password_new == '' or password_new != password_confirmation:
            raise forms.ValidationError("Passwords are not the same")

        verification_code_server = self.request.session.get('reset_password_vc', '')
        verification_code_client = self.cleaned_data.get('verification_code', '')
        if not (verification_code_server != '' and verification_code_server == verification_code_client):
            raise forms.ValidationError("Verification code is incorrect")
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email not exist')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError("Verification code is blank")
        return verification_code
