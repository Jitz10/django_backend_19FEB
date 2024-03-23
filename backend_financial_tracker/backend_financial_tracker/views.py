from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
import json
from service.models import Transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
import random
from django.conf import settings
import base64
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import matplotlib.pyplot as plt
import os
from django.db import models

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

        # Generate pie chart based on transaction categories for weekly transactions
        weekly_transactions = Transaction.objects.filter(term='weekly')
        weekly_categories = weekly_transactions.values('category').annotate(total=models.Count('category'))
        weekly_labels = [item['category'] for item in weekly_categories]
        weekly_totals = [item['total'] for item in weekly_categories]

        plt.figure(figsize=(2,2))
        plt.pie(weekly_totals, labels=weekly_labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Weekly Transaction Categories')
        weekly_pie_chart_path = os.path.join(os.getcwd(), 'weekly_pie_chart.png')
        plt.savefig(weekly_pie_chart_path)  # Save the pie chart as an image
        plt.close()

        # Generate bar chart based on transaction amounts for weekly transactions
        weekly_amounts = weekly_transactions.values('category').annotate(total_amount=models.Sum('amount'))
        weekly_categories = [item['category'] for item in weekly_amounts]
        weekly_totals = [item['total_amount'] for item in weekly_amounts]

        plt.figure(figsize=(2,2), facecolor="#333333")
        plt.bar(weekly_categories, weekly_totals)
        plt.xlabel('Weekly Transaction Categories')
        plt.ylabel('Total Amount')
        plt.title('Weekly Transaction Amounts')
        weekly_bar_chart_path = os.path.join(os.getcwd(), 'weekly_bar_chart.png')
        plt.savefig(weekly_bar_chart_path)  # Save the bar chart as an image
        plt.close()

        # Generate pie chart based on transaction categories for monthly transactions
        monthly_transactions = Transaction.objects.filter(term='monthly')
        monthly_categories = monthly_transactions.values('category').annotate(total=models.Count('category'))
        monthly_labels = [item['category'] for item in monthly_categories]
        monthly_totals = [item['total'] for item in monthly_categories]

        plt.figure(figsize=(5,2), facecolor="#333333")
        plt.pie(monthly_totals, labels=monthly_labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Monthly Transaction Categories')
        monthly_pie_chart_path = os.path.join(os.getcwd(), 'monthly_pie_chart.png')
        plt.savefig(monthly_pie_chart_path)  # Save the pie chart as an image
        plt.close()

        # Generate bar chart based on transaction amounts for monthly transactions
        monthly_amounts = monthly_transactions.values('category').annotate(total_amount=models.Sum('amount'))
        monthly_categories = [item['category'] for item in monthly_amounts]
        monthly_totals = [item['total_amount'] for item in monthly_amounts]

        plt.figure(figsize=(2,2), facecolor="#333333")
        plt.bar(monthly_categories, monthly_totals)
        plt.xlabel('Monthly Transaction Categories')
        plt.ylabel('Total Amount')
        plt.title('Monthly Transaction Amounts')
        monthly_bar_chart_path = os.path.join(os.getcwd(), 'monthly_bar_chart.png')
        plt.savefig(monthly_bar_chart_path)  # Save the bar chart as an image
        plt.close()

        # Generate pie chart based on transaction categories for yearly transactions
        yearly_transactions = Transaction.objects.filter(term='yearly')
        yearly_categories = yearly_transactions.values('category').annotate(total=models.Count('category'))
        yearly_labels = [item['category'] for item in yearly_categories]
        yearly_totals = [item['total'] for item in yearly_categories]

        plt.figure(figsize=(3, 3), facecolor="#333333")
        plt.pie(yearly_totals, labels=yearly_labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Yearly Transaction Categories')
        yearly_pie_chart_path = os.path.join(os.getcwd(), 'yearly_pie_chart.png')
        plt.savefig(yearly_pie_chart_path)  # Save the pie chart as an image
        plt.close()

        # Generate bar chart based on transaction amounts for yearly transactions
        yearly_amounts = yearly_transactions.values('category').annotate(total_amount=models.Sum('amount'))
        yearly_categories = [item['category'] for item in yearly_amounts]
        yearly_totals = [item['total_amount'] for item in yearly_amounts]

        plt.figure(figsize=(8, 6), facecolor="#333333")
        plt.bar(yearly_categories, yearly_totals)
        plt.xlabel('Yearly Transaction Categories')
        plt.ylabel('Total Amount')
        plt.title('Yearly Transaction Amounts')
        yearly_bar_chart_path = os.path.join(os.getcwd(), 'yearly_bar_chart.png')
        plt.savefig(yearly_bar_chart_path)  # Save the bar chart as an image
        plt.close()

        return HttpResponse('Data saved successfully')
    else:
        return HttpResponseNotAllowed(['POST'])

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

        # Read the monthly pie chart image file and encode it in base64
        monthly_pie_chart_path = os.path.join(os.getcwd(), 'monthly_pie_chart.png')
        with open(monthly_pie_chart_path, 'rb') as image_file:
            image_url_base64 = f"data:image/png;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"

        # Send the response with income, expense, balance, and base64-encoded image URL
        return JsonResponse({'income': income, 'expense': expense, 'balance': balance, 'imageUrlBase64': image_url_base64})

    except Exception as e:
        pass