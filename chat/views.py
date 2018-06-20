from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views import View, generic

from django.contrib.auth import views, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone

from .models import Conversation, Message
from .forms import ProfileForm, ConversationForm, MessageForm

class HomeView(LoginRequiredMixin, generic.ListView):
    login_url = 'chat:login'
    
    def get(self,request):
        wanted_items = set()
        for conv in Conversation.objects.all():
            if request.user in conv.members.all():
                wanted_items.add(conv.pk)
        conversation_list = Conversation.objects.filter(owner=request.user) | Conversation.objects.filter(pk__in = wanted_items)
        context = {'conversation_list': conversation_list}
        return render(request,'chat/home.html',context)


class LoginView(views.LoginView):
    template_name='chat/login.html'


class LogoutView(views.LogoutView):
    template_name='chat/logout.html'


class RegistrationView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request,'chat/registration.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user.refresh_from_db()
            # user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)
            return redirect('chat:home') 
        return render(request,'chat/registration.html', {'form': form})


class SettingsView(LoginRequiredMixin, View):
    login_url = 'chat:login'

    def get(self, request):
        form = ProfileForm(instance=request.user.profile, initial={'bio': request.user.profile.bio, 'birth_date':request.user.profile.birth_date})
        return render(request,'chat/settings.html', {'form': form})
    
    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('chat:home') 
        return render(request,'chat/settings.html', {'form': form})

class CreateConversationView(LoginRequiredMixin, View):
    login_url = 'chat:login'

    def get(self, request):
        form = ConversationForm(request.user)
        return render(request,'chat/create_conversation.html', {'form': form})
    
    def post(self, request):
        form = ConversationForm(request.user,request.POST)
        if form.is_valid():
            conv = form.save() #commit = False
            conv.owner = request.user
            conv.save()
            return redirect('chat:home') 
        return render(request,'chat/create_conversation.html', {'form': form})

class ConversationView(LoginRequiredMixin, View):
    login_url = 'chat:login'
    def get(self, request, conversation_id):
        conv = get_object_or_404(Conversation, pk=conversation_id)
        members = conv.members.all()
        messages = Message.objects.filter(conversation=conv)[:20][::-1]
        user = request.user
        form = MessageForm()
        return render(request, 'chat/conversation.html', {'conv': conv, 'form': form, 'messages': messages, 'user': user, 'members' : members})
        
    
    def post(self, request, conversation_id):
        form = MessageForm(request.POST)
        conv = get_object_or_404(Conversation, pk=conversation_id)
        if form.is_valid():
            message = form.save(commit = False) 
            message.conversation = conv
            message.sent_date = timezone.now()
            message.sender = request.user
            message.save()
        return redirect('.')