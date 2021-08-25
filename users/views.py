from django.http.response import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.views import LoginView, LogoutView
from .models import Artist
from .forms import (
    ArtistCreationForm,
    ArtistChangeForm,
    ArtistLoginForm,
)
from .mixins import UserRootsRequired
from feed.models import Post
from django.utils.text import slugify
from django.urls import reverse_lazy
import redis
from django.conf import settings

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
        form.save()

        return HttpResponseRedirect(reverse_lazy('feed'))


class ArtistLoginView(LoginView):
    form_class = ArtistLoginForm
    template_name = 'users/login.html'


class ArtistLogoutView(LogoutView):
    next_page = reverse_lazy('feed')


class ArtistChangeView(LoginRequiredMixin, UserRootsRequired, UpdateView):
    form_class = ArtistChangeForm
    model = Artist
    template_name = 'users/change.html'


class UserPostsListView(LoginRequiredMixin, DetailView):
    model = Artist
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserPostsListView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author__username=self.get_object())
        posts_amount = r.get(f'{self.request.user}:posts').decode('UTF-8')
        
        try:
            posts_amount = r.get(f'{self.request.user}:posts').decode('UTF-8')
            context['posts_amount'] = posts_amount
        except AttributeError:
            r.append(f'{self.request.user}:posts',
                     Post.objects.filter(author=self.request.user).count())
            context['posts_amount'] = r.get(f'{self.request.user}:posts')
        return context
