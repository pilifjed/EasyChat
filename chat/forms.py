from django import forms

from .models import Profile, Conversation, Message

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio','birth_date',)


class ConversationForm(forms.ModelForm):

    class Meta:
        model = Conversation
        fields = ('members','name','description',)
        widgets = {
            'members' : forms.CheckboxSelectMultiple
        }

    def __init__(self, user, *args, **kwargs):
        super(ConversationForm, self).__init__(*args, **kwargs)
        q = self.fields['members'].queryset
        self.fields['members'].queryset = q.exclude(id=user.id)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('message_content',)