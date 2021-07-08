from .forms import LoginForm


def modal_login_form(request):
    return {'modal_login_form': LoginForm()}