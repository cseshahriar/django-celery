import requests
from time import sleep
from django.core.mail import send_mail
from celery import shared_task, states
from celery.exceptions import Ignore
from celery.utils.log import get_task_logger

@shared_task(bind=True, max_retries=3, default_retry_delay=60)  # Retry up to 3 times, with a delay of 60 seconds between retries
def send_feedback_email_task(self, email_address, message):  # self is celery
    """Sends an email when the feedback form has been submitted."""
    try:
        print("================= send_feedback_email_task called")
        logger.info("Task send_feedback_email_task")
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


@shared_task
def send_daily_summary():
    """
    In Admin Panel:
    Go to Periodic Tasks
    Add a new task: your_app.tasks.send_daily_summary
    Choose interval or crontab (e.g., every day at 10.30 AM
    """
    print("Sending daily summary... caleld")
    logger.info("send_daily_summary task called")
    send_feedback_email_task.delay("cse.shahriar.hosen@gmail.com", "send_daily_summary test")