from django.utils import timezone
from datetime import timedelta


def get_due_date():
    return timezone.now().date() + timedelta(days=14)