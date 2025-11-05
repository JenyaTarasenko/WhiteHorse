---------------url_scanner.py--------------

файл в котором находится скрипт сканера

--------------tasks.py---------------------Celery
нужно установить локально brew install redis

pip install celery redis

в терминале 
redis-server

backend   ->  __init__.py и фал celery.py


Когда пользователь вызывает /start_scan?url=https://example.com:

Django создаёт новую запись ScanTask

Celery автоматически подхватывает задачу и выполняет её в фоне

Redis хранит состояние

Когда всё готово — ScanResult создаётся, а статус задачи обновляется на done
-----------------------------------Анимация
