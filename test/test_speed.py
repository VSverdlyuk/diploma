# test_speed.py
import requests
import time

# Flask
start_time = time.time()
requests.post('http://127.0.0.1:5000/write')
flask_time = time.time() - start_time

# FastAPI
start_time = time.time()
requests.post('http://127.0.0.1:8000/write')
fastapi_time = time.time() - start_time

# Django
start_time = time.time()
requests.post('http://127.0.0.1:8001/write/')
django_time = time.time() - start_time

print(f"Flask: {flask_time} seconds")
print(f"FastAPI: {fastapi_time} seconds")
print(f"Django: {django_time} seconds")
