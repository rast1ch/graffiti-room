from django.http import HttpResponseForbidden , HttpResponseRedirect
from django.urls import reverse
from .models import Post


class UserRootsRequired:
    """Миксин совмещающий в себе loginReguiredMixin и проверку пользователя"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        else:
            post = Post.objects.get(slug=self.kwargs.get('slug'))
            print(post.author)
            if request.user == post.author:
                return super().dispatch(request,*args, **kwargs)
            else:
                return HttpResponseForbidden()