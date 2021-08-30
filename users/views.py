from django.http.response import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    TemplateView,
    FormView,
)
from django.contrib.auth.views import LoginView, LogoutView
from .models import Artist
from .forms import (
    ArtistCreationForm,
    ArtistChangeForm,
    ArtistLoginForm,
    EmailForm,
)
from .mixins import UserRootsRequired
from feed.models import Post
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
import redis
import uuid
from .tasks import send_mail_celery
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
# Подключение к Redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class ArtistCreateView(CreateView):
    """View для регистрации новых пользователей"""
    form_class = ArtistCreationForm
    model = Artist
    template_name = 'users/registration.html'
    success_url = reverse_lazy('feed')
        

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        form = form.save(commit=False)
        form.slug = slugify(str(username))
        form.uuid = uuid.uuid4()
        form.is_active = False
        subject,link = ["Подтверждение адресса электронной почты",
                                f'http://localhost:8000/account/verify/{uuid}']
        message = f"Для подтвержения адресса электронной почты, нужно перейти по ссылке {link}"
        send_mail_celery(subject, message, form.email)
        form.save()
        

        return HttpResponseRedirect(reverse_lazy('feed'))


class ArtistLoginView(LoginView):
    """View отвечающее за логин пользователей"""
    form_class = ArtistLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('feed')

class ArtistLogoutView(LogoutView):
    """View отвечающее за выход пользователей"""
    next_page = reverse_lazy('feed')


class ArtistChangeView(LoginRequiredMixin, UserRootsRequired, UpdateView):
    """View отвечающее за смену данных о пользователе"""
    form_class = ArtistChangeForm
    model = Artist
    template_name = 'users/change.html'


class UserPostsListView(LoginRequiredMixin, DetailView):
    """Посты сгрупированые по одно пользователю + информация по пользователю"""
    model = Artist
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserPostsListView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author__username=self.get_object())
        # posts_amount = r.get(f'{self.request.user}:posts').decode('UTF-8')
        
        try:
            posts_amount = r.get(f'{self.request.user}:posts').decode('UTF-8')
            context['posts_amount'] = posts_amount
            
        except AttributeError:
            r.append(f'{self.request.user}:posts',
                     Post.objects.filter(author=self.request.user).count())
            context['posts_amount'] = r.get(f'{self.request.user}:posts').decode('UTF-8')
        return context


class ArtistChangePasswordWithEmail(FormView):
    form_class = EmailForm
    template_name = 'users/forgot_password.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            email = Artist.objects.get(email=email)
            temp_uuid = uuid.uuid4()
            subject,link = ["Смена пароля",
                            f'http://localhost:8000/account/reset_password/{temp_uuid}']
            message = f"Для смены пароля, нужно перейти по ссылке {link}"
            r.append(f'{temp_uuid}', email.email)
            r.expire(f'{temp_uuid}', 600)

            send_mail_celery(subject,message,email)
        except Artist.DoesNotExist:
            return HttpResponseNotFound()
        
        return super().form_valid(form)


class ArtistResetPassword(TemplateView):
    template_name = 'users/reset.html'

    def get(self, request, *args, **kwargs):
        temp_uuid = uuid.uuid4()
        r.append(f'{temp_uuid}', request.user.username)
        r.expire(f'{temp_uuid}', 600)

        email = Artist.objects.get(username=request.user.username).email
        subject,link = ["Смена пароля",
                        f'http://localhost:8000/account/change_password/{temp_uuid}']
        message = f"Для смены пароля, нужно перейти по ссылке {link}"
        send_mail_celery(subject,message,email)
        return super(ArtistResetPassword,self).get(request,*args, **kwargs)



class ArtistChangePassword(FormView):
    form_class = SetPasswordForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('logout')

    @property
    def user(self):
        temp_uuid = self.kwargs.get('uuid')
        try:
            username_r = r.get(f'{temp_uuid}').decode('UTF-8')
            print(type(Artist.objects.get(username__exact=username_r)))
            return Artist.objects.get(username__exact=username_r)
        except AttributeError:
            return HttpResponseForbidden()
    
    def form_valid(self, form):
        temp_uuid = self.kwargs.get('uuid')
        try:
            r.delete(str(temp_uuid))
        except AttributeError:
            print('0')
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs =  super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs
    
    def get(self,request,*args, **kwargs):
        return super(ArtistChangePassword, self).get(request, *args, **kwargs)

class ArtistChangeForgottenPassword(ArtistChangePassword):
    success_url = reverse_lazy('feed')
    
    @property
    def user(self):
        temp_uuid = self.kwargs.get('uuid')
        try:
            email = r.get(f'{temp_uuid}').decode('UTF-8')
            return Artist.objects.get(email__exact=email)
        except AttributeError:
            return HttpResponseForbidden()

class ArtistConfirmView(TemplateView):
    """View для подтверждения электронной почты"""
    template_name = 'users/confirm.html'

    def get(self,request,*args, **kwargs):
        user_uuid = self.kwargs.get('uuid')
        try:
            user = Artist.objects.get(uuid=user_uuid)
            if user.is_active:
                return HttpResponseForbidden()
            else:
                user.is_active = True
                user.save()
                return super(ArtistConfirmView,self).get(request,*args, **kwargs)
        except Artist.DoesNotExist:
            return Http404()
    
