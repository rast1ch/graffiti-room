from django.http import HttpResponseForbidden


class UserRootsRequired:
    """Миксин для проверки пользователя"""
    def dispatch(self, request, *args, **kwargs):
        if request.user.slug == self.kwargs.get('slug'):
            
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
