from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from .forms import LoginForm, ProfileForm, RegistrationForm


class StoreLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Welcome back! You're signed in.")
        return super().form_valid(form)


class StoreLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        messages.success(request, "You've been signed out.")
        return super().post(request, *args, **kwargs)


def register(request):
    if request.user.is_authenticated:
        return redirect("store:home")
    form = RegistrationForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account is ready. Make yourself at home!")
        return redirect("accounts:profile")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    form = ProfileForm(request.POST if request.method == "POST" else None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your profile has been updated.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"form": form})
