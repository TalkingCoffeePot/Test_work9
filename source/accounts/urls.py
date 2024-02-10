from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import UserRegisterView, UserProfile, logout_view, subscribe_view, UserProfileEdit
from feed.views import PostCreateView, PostDetailedView

app_name='accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/sign_in.html'), name='log_in'),
    path('create/', UserRegisterView.as_view(), name='register_user'),
    path('profile/<int:profile_pk>', UserProfile.as_view(), name='profile'),
    path('profile/<int:profile_pk>/edit', UserProfileEdit.as_view(), name='edit_profile'),
    path('profile/<int:profile_pk>/subscribe/', subscribe_view, name='profile_sub'),
    path('logout/', logout_view, name='log_out'),
    path('<int:profile_pk>/new_post/', PostCreateView.as_view(), name='new_post'),
    path('profile/<int:profile_pk>/post/<int:post_pk>/', PostDetailedView.as_view(), name='detailed_post')
]