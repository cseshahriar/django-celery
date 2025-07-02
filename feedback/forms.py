from time import sleep
from django.core.mail import send_mail
from django import forms

from feedback.tasks import send_feedback_email_task

class FeedbackForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(
        label="Message", widget=forms.Textarea(attrs={"rows": 5})
    )

    def send_email(self):
        """Sends an email when the feedback form has been submitted."""
        print("================================= FeedbackForm send_email called")
        sleep(20)  # Simulate expensive operation(s) that freeze Django
        send_feedback_email_task.delay(
            self.cleaned_data["email"], self.cleaned_data["message"]
        )