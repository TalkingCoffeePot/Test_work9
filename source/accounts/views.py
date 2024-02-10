from django.contrib.auth import login, logout
from django.views.generic import CreateView, DetailView, UpdateView
from accounts.models import Profile
from accounts.forms import NewUserForm, UserEditForm
from typing import Any
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

def logout_view(request):
    logout(request)
    return redirect('feed')

class UserRegisterView(CreateView):
    model = Profile
    template_name = 'accounts/sign_up.html'
    form_class = NewUserForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse('feed'))
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('feed')
        return next_url
    
class UserProfile(DetailView):
    template_name = 'accounts/profile_page.html'
    model = Profile
    context_object_name = 'profile_obj'
    pk_url_kwarg = 'profile_pk'


class UserProfileEdit(LoginRequiredMixin, UpdateView):
    login_url = 'accounts:log_in'
    model = Profile
    form_class = UserEditForm
    template_name = 'accounts/edit_profile.html'
    pk_url_kwarg = 'profile_pk'
    context_object_name = 'profile_obj'

    def get_success_url(self, **kwargs):
        return reverse('accounts:profile', kwargs={'profile_pk': self.request.user.pk})
    
    def get_context_data(self, **kwargs):
        kwargs['profile_obj'] = self.get_object()
        kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)
    