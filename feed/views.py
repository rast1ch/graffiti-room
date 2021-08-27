from django.urls.base import reverse_lazy
from django.views.generic.edit import DeleteView
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    RedirectView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .mixins import UserRootsRequired
import random
import string
from .forms import PostModelForm, ImageFormSet,PostUpdateForm
from django.shortcuts import redirect
from .models import Image, Post
import redis
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


def rand_slug(model):
    """Формирования случайного url"""
    random_slug = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
    for i in model.objects.all():  # Перебор и рекурсия на случай совпадения,
        if random_slug == i.slug:  # хоть там 1,340,095,640,625 вариантов, но мало ли
            rand_slug(model)
    else:
        return random_slug


class PostListView(LoginRequiredMixin, ListView):
    """View для просмотра списка постов"""
    model = Post
    context_object_name = 'posts'
    template_name = 'feed/feed.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data()
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        return Post.objects.filter(active=True)


class PostDetailView(LoginRequiredMixin, DetailView):
    """View для просмотра конкретного поста"""
    template_name = 'feed/post_detail.html'
    model = Post
    context_object_name = 'object'

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect(reverse('feed'))


class PostCreateView(LoginRequiredMixin, TemplateView):
    """View для создания постов с поддержкой нескольких картинок"""

    def get(self, request, *args, **kwargs):
        postForm = PostModelForm()
        formset = ImageFormSet(queryset=Image.objects.none())
        return render(request, 'feed/post_create.html',
                      {'postForm': postForm, 'formset': formset})

    def post(self, request, *args, **kwargs):
        postForm = PostModelForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Image.objects.none())

        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.author = request.user
            post_form.slug = rand_slug(Post)
            post_form.active = True
            post_form.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Image(post=post_form, img=image)
                    photo.save()
            post_amount = Post.objects.filter(author=self.request.user).count()
            try:
                r.get(f'{self.request.user}:posts').decode('UTF-8')
                r.incr(f'{self.request.user}:posts')
            except AttributeError:
                r.append(f'{self.request.user}:posts', post_amount)
            return HttpResponseRedirect("/feed/")
        else:
            print(postForm.errors, formset.errors)


class PostUpdateView(UserRootsRequired, UpdateView):
    """View для изменения описания постов"""
    template_name = 'feed/post_update.html'
    model = Post
    form_class = PostUpdateForm
    

class PostDeleteView(UserRootsRequired, DeleteView):
    """View для удаления постов"""
    model = Post
    success_url = reverse_lazy('feed')
    template_name = 'feed/post_delete.html'


class FeedRedirectView(RedirectView):
    """Реализация авто-редиректа с неправильной ссылки"""
    url = reverse_lazy('feed')
