from django import forms
from django.core import validators
from website.models import Ticket
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput)
    class Meta:
        model = Ticket
        fields = ["name","email",'ticket_type','phone_number',"body"]
    
    def clean_botcatcher(self):
            botcatcher = self.cleaned_data['botcatcher']
            if len(botcatcher) > 0:
                raise forms.ValidationError("Gotcha BOT")
            return botcatcher



