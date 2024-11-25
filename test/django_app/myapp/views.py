from django.http import JsonResponse
import time
from django.views.decorators.csrf import csrf_exempt
from .models import Record  # Importing the Record model


@csrf_exempt
def write(request):
    """
    Adds 10,000 records to the database and measures the time taken.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the time taken to write the records.
    """
    start_time = time.time()  # Start timing the operation

    # Add 10,000 records to the database
    records = [Record(name=f"Record {i + 1}") for i in range(10000)]
    Record.objects.bulk_create(records)  # Use bulk_create for better performance

    end_time = time.time()  # End timing the operation

    # Return the time taken as a JSON response
    return JsonResponse({"message": f"Django write of 10,000 records took {end_time - start_time:.2f} seconds"})
