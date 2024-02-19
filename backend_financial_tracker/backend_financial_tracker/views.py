from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
import json
from service.models import Transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
@csrf_exempt
def da(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        print(form_data)
        json_data = json.loads(form_data['jsonString'])
        print(json_data)
        print(json_data.get('category'))
        transaction = Transaction(
            type=json_data.get('type'),
            name=json_data.get('name',' '),
            category=json_data.get('category'),
            description=json_data.get('description'),
            amount=json_data.get('amount'),
            recurring=json_data.get('recurring'),
            term=json_data.get('term'),
            end_date=json_data.get('endDate')
        )
        transaction.save()
        return HttpResponse('Data saved successfully')
    else:
        return HttpResponseNotAllowed(['POST'])
