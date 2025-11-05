# news/tasks.py
from celery import shared_task
from .models import ScanTask, ScanResult
from django.utils import timezone
import requests


@shared_task
def scan_website(task_id):
    try:
        task = ScanTask.objects.get(id=task_id)
        task.status = 'in_progress'
        task.save()

        response = requests.get(task.url, timeout=10)
        result_data = {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content_length': len(response.text)
        }

        ScanResult.objects.create(task=task, result=result_data)
        task.status = 'done'
        task.completed_at = timezone.now()
        task.save()

        return "Сканирование завершено"

    except Exception as e:
        task.status = 'failed'
        task.completed_at = timezone.now()
        task.save()
        return str(e)
