from time import sleep
from feedback.forms import FeedbackForm
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import HttpResponse

from feedback.tasks import send_feedback_email_task


class FeedbackFormView(FormView):
    template_name = "feedback/feedback.html"
    form_class = FeedbackForm
    success_url = "/feedback/success/"

    def form_valid(self, form):
        print(f"{'*' * 5} form valid called {form.cleaned_data}")
        cleaned_email = form.cleaned_data['email']
        email_list = []
        message = form.cleaned_data['message']

        if ',' in cleaned_email:
            for email in cleaned_email.split(','):
                email_list.append(email)
        else:
            email_list.append(cleaned_email)
        
        for reever_email in email_list:
            sleep(10)  # Simulate expensive operation(s) that freeze Django
            send_feedback_email_task.delay(
                reever_email, message
            )

        return super().form_valid(form)

class SuccessView(TemplateView):
    template_name = "feedback/success.html"