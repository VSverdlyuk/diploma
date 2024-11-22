# django_app/myapp/views.py
from django.http import JsonResponse
import time
from django.views.decorators.csrf import csrf_exempt
from .models import Record  # Импортируем модель

@csrf_exempt
def write(request):
    start_time = time.time()

    # Добавление 100 записей в базу данных
    for i in range(10000):
        record = Record(name=f"Record {i + 1}")
        record.save()  # Сохраняем запись в базу данных
    
    end_time = time.time()
    
    return JsonResponse({"message": f"Django write of 100 records took {end_time - start_time} seconds"})
