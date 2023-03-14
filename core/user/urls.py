from django.urls import path


from core.user.views import *


app_name = 'user'

urlpatterns = [
 
    #User
    path('listado/', UserListView.as_view(), name='user_listado'),
    path('add/', UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('password/', UserPasswordView.as_view(), name='user_password'),





    
]