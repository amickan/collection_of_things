from django.forms import ModelForm
from collection.models import Thing
from django import forms

class ThingForm(ModelForm):
    class Meta:
        model = Thing
        fields = ('name', 'description',)


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    # name = forms.CharField(max_length=500)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['subject'].label = "What's the topic?:"
        # self.fields['name'].label = "Your name:"
        self.fields['from_email'].label = "Your email:"
        self.fields['message'].label = "What do you want to say?"