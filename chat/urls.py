from django.urls import path

from . import views

app_name = 'chat'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('registration/', views.RegistrationView.as_view(),name='registration'),
    path('', views.HomeView.as_view(), name='home'),
    path('settings/', views.SettingsView.as_view(), name = 'settings'),
    path('create_conversation/', views.CreateConversationView.as_view(), name = 'create_conversation'),
    path('<int:conversation_id>/', views.ConversationView.as_view(), name = 'conversation')
]