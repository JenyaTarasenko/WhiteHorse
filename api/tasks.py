# news/tasks.py
from celery import shared_task
from django.utils import timezone
import requests
from .url_scanner import quick_scan


@shared_task
def run_scan_task(url):
    result = quick_scan(url)
    return result
