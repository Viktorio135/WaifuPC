from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login, logout, authenticate

from .models import CustomUser, Works, Builds, Repair, TradeIn, Contacts
from .forms import LoginForm, RegistrationForm, TradeInForm


class IndexPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["works"] = Works.objects.all()
        context["builds"] = Builds.objects.first()
        context["repair"] = Repair.objects.first()
        context["tradein"] = TradeIn.objects.first()
        context["contacts"] = Contacts.objects.first()
        context['form'] = TradeInForm()
        return context

    def post(self, request, *args, **kwargs):
        # Получаем данные из формы
        form = TradeInForm(request.POST)
        if form.is_valid():

            # Отправляем письмо
            subject = 'Новая заявка на Trade-In'
            message = f"Email: {form.cleaned_data['email']}\n" \
                      f"Сообщение: {form.cleaned_data['text']}"
            from_email = 'spakovskijviktor0@gmail.com'  # Укажите ваш email
            recipient_list = ['spakovskijviktor0@gmail.com']  # Укажите email получателя

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            # Устанавливаем флаг успешной отправки в сессии
            request.session['success_message'] = 'Спасибо! Ваша заявка отправлена.'

            # Перенаправляем пользователя на ту же страницу
            return redirect('main:index')  # 'index' — это имя URL для вашей страницы

        # Если форма не валидна, возвращаем её с ошибками
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        # Проверяем, есть ли сообщение об успешной отправке в сессии
        success_message = request.session.pop('success_message', None)
        context = self.get_context_data(**kwargs)
        if success_message:
            context['success_message'] = success_message
        return self.render_to_response(context)

    


class RegisterPage(View):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = 'main:profile'  # URL для перенаправления после успешной регистрации

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main:profile')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(request, email=user.email, password=form.cleaned_data['password1'])
            backend = 'main.backends.CustomAuthBackend'  # Укажите путь к вашему бэкенду
            if user is not None:
                login(request, user, backend=backend)
                return redirect(self.success_url) 
            else:
                form.add_error(None, "Не удалось выполнить вход после регистрации.")

        return render(request, self.template_name, {'form': form})
        

class CustomLoginView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main:profile')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.user  # Пользователь, который был найден в методе clean формы
            # Указываем бэкенд аутентификации
            backend = 'main.backends.CustomAuthBackend'  # Укажите путь к вашему бэкенду
            login(request, user, backend=backend)  # Выполняем вход с указанием бэкенда
            return redirect('main:profile')  # Перенаправляем на страницу профиля
        return render(request, self.template_name, {'form': form})


class Logout(LogoutView):
    next_page = reverse_lazy('main:index')

class ProfilePage(TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # Используем свойство, а не метод
            return redirect('main:login')  # Возвращаем результат вызова redirect
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_data'] = {
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'city': user.city, 
        }
        return context
