from django.forms import ModelForm
from collection.models import Thing, Upload
from django import forms
from django.contrib.auth.models import User


class ThingForm(ModelForm):
    class Meta:
        model = Thing
        fields = ('name', 'description',)


class ContactForm(forms.Form):
    from_email = forms.EmailField(label="Your email ", required=True)
    # first_name = forms.CharField(label="Your name ", max_length=500)
    subject = forms.CharField(label="What's the topic?  ", required=True)
    message = forms.CharField(label="Your message ", widget=forms.Textarea,
                              required=True)

    # def __init__(self, *args, **kwargs):
    #     super(ContactForm, self).__init__(*args, **kwargs)
    #     self.fields['subject'].label = "What's the topic?:"
    #     self.fields['name'].label = "Your name:"
    #     self.fields['from_email'].label = "Your email:"
    #     self.fields['message'].label = "What do you want to say?"


class ThingUploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = ('image',)


class EditEmailForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)