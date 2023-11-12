from django.contrib.auth.views import LoginView
from django.views.generic import FormView


class AccountLoginView(LoginView):
    pass


class AccountSignUpView(FormView):
    pass