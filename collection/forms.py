from django.forms import ModelForm
from collection.models import Thing
from django import forms

class ThingForm(ModelForm):
    class Meta:
        model = Thing
        fields = ('name', 'description',)


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)