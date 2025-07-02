from time import sleep
from django.core.mail import send_mail
from django import forms

from feedback.tasks import send_feedback_email_task

class FeedbackForm(forms.Form):
    email = forms.CharField(label="Email Address comma seperated abs@mail.com, bbc@mail.com")
    message = forms.CharField(
        label="Message", widget=forms.Textarea(attrs={"rows": 5})
    )