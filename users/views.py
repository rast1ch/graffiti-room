from django.http.response import HttpResponseRedirect
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView
)
from .models import Artist
from .forms import (
    ArtistCreationForm,
    ArtistChangeForm,
)
from django.shortcuts import get_object_or_404
from feed.models import Post
from django.utils.text import slugify
from django.urls import reverse_lazy


class ArtistCreateView(CreateView):
    form_class = ArtistCreationForm
    model = Artist
    template_name = 'users/registration.html'
    success_url = reverse_lazy('feed')
    
    def form_valid(self,form):
        username = form.cleaned_data.get('username')
        form = form.save(commit=False)
        form.slug = slugify(str(username))
        form.save()
        return HttpResponseRedirect(reverse_lazy('feed'))

class ArtistChangeView(UpdateView):
    form_class = ArtistChangeForm
    model = Artist
    template_name = 'users/change.html'



class UserPostsListView(DetailView):
    model = Artist
    template_name = 'users/profile.html'
    
    
    def get_context_data(self, **kwargs):
        context =  super(UserPostsListView,self).get_context_data(**kwargs)
        context['posts']= Post.objects.filter(user__username=self.get_object())
        return context


