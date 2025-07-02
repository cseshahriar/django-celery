from time import sleep
from django.core.mail import send_mail
from celery import shared_task, states
from celery.exceptions import Ignore


@shared_task(bind=True, max_retries=3, default_retry_delay=60)  # Retry up to 3 times, with a delay of 60 seconds between retries
def send_feedback_email_task(self, email_address, message):
    """Sends an email when the feedback form has been submitted."""
    try:
        print("------------------------------------- send_feedback_email_task called")
        sleep(10)  # Simulate expensive operation(s)
        send_mail(
            "Your Feedback",
            f"\t{message}\n\nThank you!",
            "support@example.com",
            [email_address],
            fail_silently=False,
        )
    except Exception as exc:
        print(f"Task failed: {exc}")
        raise self.retry(exc=exc)  # Retry on failure