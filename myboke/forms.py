from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='用户名或邮箱', 
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入用户名或邮箱',
                }),
        error_messages={
            'required':'请输入用户名或邮箱'
            })

    password = forms.CharField(
        label='密码',
        label_suffix='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入密码',
                }),
        error_messages={
            'required':'请输入密码'
            })


    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                user = auth.authenticate(username=User.objects.get(email=username_or_email),
                        password=password)
                if user is None:
                    raise forms.ValidationError('用户名或密码不正确，请重新输入')
                else:
                    self.cleaned_data['user'] = user         
            else:
                raise forms.ValidationError('用户名或密码不正确，请重新输入')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegisterForm(forms.Form):
    error_css_class = 'text-danger'
    username = forms.CharField(
        label='用户名',
        label_suffix='',
        max_length=10,
        min_length=3,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入用户名',
            }),
        error_messages={
            'required': '请输入用户名',
            'min_length': '用户名长度要大于3',
            'max_length': '用户名长度要小于10',
        },)
    email = forms.EmailField(
        label='邮箱',
        label_suffix='',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入邮箱',
            }),
        error_messages={
            'required': '请输入邮箱',
            'invalid': '请输入一个邮箱地址'
        },)
    verify_code = forms.CharField(
            label='验证码',
            max_length=4,
            required = False,
            widget=forms.TextInput(attrs={
                    'placeholder': "点击发送验证码发送至您的邮箱",
                    'class': 'form-control',
                })
        )
    password = forms.CharField(
        label='密码',
        label_suffix='',
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入密码',
            }),
        error_messages={
            'required': '请输入密码',
            'min_length': '密码长度要大于6',
        },)
    password_again = forms.CharField(
        label='重复密码',
        label_suffix='',
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请再次输入密码',
            }),
        error_messages={
            'required': '请输入密码',
        },)
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

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

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError("两次密码不一致")
        return password_again

    def clean_verify_code(self):
        verify_code = self.cleaned_data['verify_code'].strip()
        if verify_code == '':
            raise forms.ValidationError('验证码不能为空')
        if verify_code != self.request.session.get('register',''):
            raise forms.ValidationError('验证码输入有误')
        return verify_code


class ChangeNickNameForm(forms.Form):
    nick_name = forms.CharField(
            max_length=20,
            label='昵称',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入昵称',
                })
        )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNickNameForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.user.is_authenticated:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data

    def clean_nick_name(self):
        nick_name = self.cleaned_data['nick_name']
        if nick_name.strip() == '' :
            raise forms.ValidationError('昵称不能为空')
        return nick_name


class BindEmailForm(forms.Form):
    email = forms.EmailField(
            label='邮箱',
            widget=forms.EmailInput(attrs={
                    'placeholder': '请输入邮箱',
                    'class': 'form-control',
                })
        )
    verify_code = forms.CharField(
            label='验证码',
            max_length=4,
            required = False,
            widget=forms.TextInput(attrs={
                    'placeholder': "点击发送验证码发送至您的邮箱",
                    'class': 'form-control',
                })
        )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.request.user.is_authenticated:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data

    def clean_verify_code(self):
        verify_code = self.cleaned_data['verify_code'].strip()
        if verify_code == '':
            raise forms.ValidationError('验证码不能为空')
        if verify_code != self.request.session.get('bind_email',''):
            raise forms.ValidationError('验证码输入有误')
        return verify_code


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已绑定")
        return email


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='旧密码',
        label_suffix='',
        widget=forms.PasswordInput(attrs={
            'placeholder': '请输入旧密码',
            'class': 'form-control',
        }))
    new_password = forms.CharField(
        label='新密码',
        label_suffix='',
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'placeholder': '请输入新密码',
            'class': 'form-control',
        }))
    new_password_again = forms.CharField(
        label='重复密码',
        label_suffix='',
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'placeholder': '请输入重复密码',
            'class': 'form-control',
        }))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.user.is_authenticated:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码输入错误')
        return old_password

    def clean_new_password_again(self):
        new_password = self.cleaned_data['new_password']
        new_password_again = self.cleaned_data['new_password_again']
        if new_password_again != new_password:
            raise forms.ValidationError('两次密码不一致')
        return new_password


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(
        label='邮箱',
        label_suffix='',
        widget=forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入邮箱',
            }))
    verify_code = forms.CharField(
            label='验证码',
            max_length=4,
            required = False,
            widget=forms.TextInput(attrs={
                    'placeholder': "点击发送验证码发送至您的邮箱",
                    'class': 'form-control',
                })
        )
    password = forms.CharField(
        label='密码',
        label_suffix='',
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'placeholder': '请输入密码',
            'class': 'form-control',
        }))
 
    password_again = forms.CharField(
        label='重复密码',
        label_suffix='',
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'placeholder': '请重复输入密码',
            'class': 'form-control',
        }))


    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱未绑定用户')
        return email

    def clean_verify_code(self):
        verify_code = self.cleaned_data['verify_code'].strip()
        if verify_code == '':
            raise forms.ValidationError('验证码不能为空')
        elif verify_code != self.request.session['forgot_password']:
            raise forms.ValidationError('验证码输入错误')
        return verify_code

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password_again != password:
            raise forms.ValidationError('两次密码不一致')
        return password
