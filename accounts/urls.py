from django.urls import path
from .views import  like, save_history, CreateUser, LoginView, MypageView, LogoutView, Resign, ResConduct, ResComplete, guest_login

urlpatterns = [
    path('post/<int:pk>', save_history, name='save_history'),
    path('post/<int:pk>/like', like, name='like'),
    path('create/', CreateUser.as_view(), name='create'),
    path('login/', LoginView.as_view(), name='login'),
    path('mypage/<int:pk>/', MypageView.as_view(), name='mypage'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('resign/', Resign.as_view(), name='resign'),
    path('resign/<int:pk>/conduct', ResConduct.as_view(), name='resign_conduct'),
    path('resign/complete/', ResComplete.as_view(), name='resign_complete'),
    path('guest_login/', guest_login, name = 'guest_login'),
]