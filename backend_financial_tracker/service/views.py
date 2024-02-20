# views.py
import json
import random
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import SuspiciousOperation
from django.conf import settings

@csrf_exempt
@require_POST
def form_handler(request):
    try:
        # Check if request body exists
        if not request.body:
            raise SuspiciousOperation('Missing JSON data in the request body')

        # Extract JSON data from the request body
        details = json.loads(request.body.decode('utf-8'))

        # Process the details or perform any desired operations
        print('Received data:', details)

        # Respond with a success message
        return JsonResponse({'status': 'success', 'message': 'Data received and processed successfully'})

    except Exception as e:
        # Handle errors and respond with an error message
        print('Error processing data:', e)
        return JsonResponse({'status': 'error', 'message': 'Internal Server Error'}, status=500)

from django.http import JsonResponse
from django.views.decorators.http import require_GET
import random

@require_GET
def dashboard(request, term):
    try:
        # Generate random values for income and expense
        get_random_value = lambda: random.randint(1, 1000)

        income = get_random_value()
        expense = get_random_value()

        if term == 'daily':
            # Daily calculations
            income *= 1.5
            expense *= 1.2
        elif term == 'weekly':
            # Weekly calculations
            income *= 7
            expense *= 6
        elif term == 'monthly':
            # Monthly calculations
            income *= 30
            expense *= 28
        elif term == 'yearly':
            # Yearly calculations
            income *= 365
            expense *= 360
        else:
            # Handle unknown terms or provide default values
            pass

        # Calculate balance
        balance = income - expense

        # Read the image file and encode it in base64
        image_path = settings.BASE_DIR / 'rickroll.jpg'  # Replace with the actual path to your image
        with open(image_path, 'rb') as image_file:
            image_url_base64 = f"data:image/png;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"

        # Send the response with income, expense, balance, and base64-encoded image URL
        return JsonResponse({'income': income, 'expense': expense, 'balance': balance, 'imageUrlBase64': image_url_base64})

    except Exception as e:
        print('Error handling request:', e)
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
