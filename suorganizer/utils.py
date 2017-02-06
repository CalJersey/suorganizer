from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test

class LoginMixin:

    @method_decorator(login_required)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request, *args, **kwargs)
