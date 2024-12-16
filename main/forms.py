from django import forms
from django.contrib.auth import authenticate
from django.conf import settings
from django.db.models import Q
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
import re

from .models import CustomUser


class LoginForm(forms.Form):
    login = forms.CharField(
        label="Номер телефона или почта",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'login-form',
            'id': 'login',
            'required': True,
            'placeholder': 'Введите номер телефона или email'
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'login-form',
            'id': 'password',
            'required': True,
            'placeholder': 'Введите пароль'
        })
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY,
        label='ReCAPTCHA'
    )

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')

        if not login or not password:
            raise forms.ValidationError("Пожалуйста, заполните все поля.")

        # Ищем пользователя по email или phone
        try:
            user = CustomUser.objects.get(Q(email=login) | Q(phone=login))
            if not user.check_password(password):
                raise forms.ValidationError("Неверный email/номер телефона или пароль.")
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("Неверный email/номер телефона или пароль.")

        self.user = user  # Сохраняем пользователя для дальнейшего использования
        return cleaned_data


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'registration-form',
            'id': 'password1',
            'required': True,
            'placeholder': 'Введите пароль'
        }),
        required=True
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'registration-form',
            'id': 'password2',
            'required': True,
            'placeholder': 'Подтвердите пароль'
        }),
        required=True
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
        label='ReCAPTCHA'
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone', 'city']
        labels = {
            'name': 'Ваше имя',  
            'email': 'Ваш email',  
            'phone': 'Ваш номер телефона',  
            'city': 'Ваш город',  
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'registration-form',
                'id': 'name',
                'required': True,
                'placeholder': 'Введите ваше имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'registration-form',
                'id': 'email',
                'required': True,
                'placeholder': 'Введите ваш email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'registration-form',
                'id': 'phone',
                'required': True,
                'placeholder': 'Введите ваш номер телефона'
            }),
            'city': forms.TextInput(attrs={
                'class': 'registration-form',
                'id': 'city',
                'required': True,
                'placeholder': 'Введите ваш город'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        phone = cleaned_data.get('phone')

        # Проверка уникальности email
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")

        # Проверка совпадения паролей
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        # Проверка номера телефона
        if phone:
            # Проверка формата телефона (например, +71234567890 или 1234567890)
            if not re.match(r'^\+?\d{10,15}$', phone):
                raise forms.ValidationError('Неправильный формат номера телефона.')
            if CustomUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError("Этот номер телефона уже зарегистрирован.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

class TradeInForm(forms.Form):
    email = forms.EmailField(
                label='Ваша почта', 
                widget=forms.EmailInput(attrs={
                'placeholder': 'Введите ваше почту'
            }),)
    text = forms.CharField(
        label='Описание компьютера',
        widget=forms.Textarea(attrs={
            'placeholder': 'Опишите ваш компьютер'
        }),
    )





# class ProfileEditForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['name', 'email', 'phone', 'city']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'profile-info', 'placeholder': 'Введите ваше имя'}),
#             'email': forms.EmailInput(attrs={'class': 'profile-info', 'placeholder': 'Введите ваш email'}),
#             'phone': forms.TextInput(attrs={'class': 'profile-info', 'placeholder': 'Введите ваш номер телефона'}),
#             'city': forms.TextInput(attrs={'class': 'profile-info', 'placeholder': 'Введите ваш город'}),
#         }