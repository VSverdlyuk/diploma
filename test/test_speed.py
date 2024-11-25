import requests
import time


def measure_request_time(url, method="POST"):
    """
    Measures the time taken to send a request to the specified URL.

    Args:
        url (str): The URL to send the request to.
        method (str): The HTTP method to use (default is "POST").

    Returns:
        float: The time taken to complete the request in seconds.
    """
    start_time = time.time()
    if method.upper() == "POST":
        requests.post(url)
    elif method.upper() == "GET":
        requests.get(url)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    return time.time() - start_time


# URLs for the respective servers
flask_url = "http://127.0.0.1:5000/write"
fastapi_url = "http://127.0.0.1:8000/write"
django_url = "http://127.0.0.1:8001/write/"

# Measure request times
flask_time = measure_request_time(flask_url)
fastapi_time = measure_request_time(fastapi_url)
django_time = measure_request_time(django_url)

# Print results
print(f"Flask: {flask_time:.2f} seconds")
print(f"FastAPI: {fastapi_time:.2f} seconds")
print(f"Django: {django_time:.2f} seconds")
