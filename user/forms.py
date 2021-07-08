from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class RegForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        max_length=30,
        min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请输入3-30位用户名"}))
    email = forms.EmailField(
        label="邮箱",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "请输入邮箱"}))
    password = forms.CharField(
        label="密码",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入密码"}))
    password_confirmation = forms.CharField(
        label="密码确认",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请再输入一次密码"}))
    verification_code = forms.CharField(
        label="验证码",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请输入验证码"}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
        verification_code_server = self.request.session.get('register_vc', '')
        verification_code_client = self.cleaned_data.get('verification_code', '')
        if not (verification_code_server != '' and verification_code_server == verification_code_client):
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")
        return email

    def clean_password_confirmation(self):
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']
        if password != password_confirmation:
            raise forms.ValidationError("两次输入的密码不一致")
        return password_confirmation

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError("验证码不能为空")
        return verification_code


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="用户名/邮箱",
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': "请输入用户名/邮箱"}))
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入密码"}))

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
            raise forms.ValidationError("用户名或密码不正确")
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class ChangeDisplayNameForm(forms.Form):
    displayname_new = forms.CharField(
        label='新昵称',
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': "请输入新昵称"}
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
            raise forms.ValidationError("用户尚未登录")
        return self.cleaned_data

    def clean_displayname_new(self):
        displayname_new = self.cleaned_data.get('displayname_new', '').strip()
        if displayname_new == '':
            raise forms.ValidationError("新昵称不能为空")
        return displayname_new


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(
        label="邮箱",
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': "请输入新邮箱"}
        )
    )
    verification_code = forms.CharField(
        label="验证码",
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': "发送验证码到邮箱"}
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
            raise forms.ValidationError("用户尚未登录")
        # 判断验证码
        verification_code_server = self.request.session.get('change_email_vc', '')
        verification_code_client = self.cleaned_data.get('verification_code', '')
        if not (verification_code_server != '' and verification_code_server == verification_code_client):
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被占用')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError("验证码不能为空")
        return verification_code


class ChangePasswordForm(forms.Form):
    password_old = forms.CharField(
        label="原密码",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入原密码"}))
    password_new = forms.CharField(
        label="新密码",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入新密码"}))
    password_confirmation = forms.CharField(
        label="新密码确认",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请再输入一次新密码"}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        password_new = self.cleaned_data.get('password_new')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password_new == '' or password_new != password_confirmation:
            raise forms.ValidationError("两次输入的密码不一致")
        return self.cleaned_data

    def clean_password_old(self):
        password_old = self.cleaned_data.get('password_old', '')
        if not self.request.user.check_password(password_old):
            raise forms.ValidationError("原密码错误")
        return password_old


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        label="邮箱",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "请输入邮箱"}))
    password_new = forms.CharField(
        label="新密码",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入新密码"}))
    password_confirmation = forms.CharField(
        label="新密码确认",
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请再输入一次新密码"}))
    verification_code = forms.CharField(
        label="验证码",
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': "发送验证码到邮箱"}
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
            raise forms.ValidationError("两次输入的密码不一致")

        verification_code_server = self.request.session.get('reset_password_vc', '')
        verification_code_client = self.cleaned_data.get('verification_code', '')
        if not (verification_code_server != '' and verification_code_server == verification_code_client):
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError("验证码不能为空")
        return verification_code
