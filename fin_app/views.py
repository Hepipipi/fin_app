from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .forms import SignUpForm, RecordForm
from .models import Category, Record
from django.db import models
from .models import User





def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} был успешно создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'fin/register.html', {'form': form})

def fin_main_page(request):
    return render(request, 'fin/index.html')


def expence(request):
    all_expences = Category.objects.filter(type='expense')
    context = {
        'all_expences': all_expences
    }
    return render(request, 'fin/expences.html', context)


def r_cat(request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        records = Record.objects.filter(category=category)

        context = {
            'category': category,
            'records': records
        }
        return render(request, 'fin/d_cat.html', context)

from django.shortcuts import render, redirect
from .forms import RecordForm
from .models import Record

@login_required()
def add_record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('records_of_category', category_slug=record.category.slug)
    else:
        form = RecordForm()

    records = Record.objects.filter(user=request.user)  # Получаем записи пользователя
    return render(request, 'fin/add_record.html', {'form': form})


def income(request):
    all_incomes = Category.objects.filter(type='income')
    context = {
        'all_incomes': all_incomes
    }
    return render(request, 'fin/incomes.html', context)

def analis():
    today = timezone.now().date()

    income_categories = Category.objects.filter(type='income')
    expense_categories = Category.objects.filter(type='expense')

    daily_income = Record.objects.filter(
        category__in=income_categories,
        date__date=today
    ).aggregate(total=models.Sum('price'))['total'] or 0

    daily_expense = Record.objects.filter(
        category__in=expense_categories,
        date__date=today
    ).aggregate(total=models.Sum('price'))['total'] or 0

    total_income = Record.objects.filter(
        category__in=income_categories
    ).aggregate(total=models.Sum('price'))['total'] or 0

    total_expense = Record.objects.filter(
        category__in=expense_categories
    ).aggregate(total=models.Sum('price'))['total'] or 0

    analysis = {
        'daily_income': daily_income,
        'daily_expense': daily_expense,
        'total_income': total_income,
        'total_expense': total_expense,
        
    }

    return analysis

def analysis_view(request):
    analysis_data = analis()
    return render(request, 'fin/analysis.html', {'analysis': analysis_data})

# @login_required()
# def edit_record(request, record_id):
#     record = get_object_or_404(Record, id=record_id)
#
#     form = RecordForm(instance=record)
#
#
#     if request.method == 'POST':
#         form = RecordForm(request.POST, instance=record)
#         if form.is_valid():
#             form.save()
#         user.record.save(commit=False)
#         user.record.author = request.user
#         user.record.save()
#         return redirect('records_of_category', record_id=record.id)
#
#     return render(request, 'fin/edit_record.html', {'form': form})

@login_required
def edit_record(request, record_id):

    record = get_object_or_404(Record, id=record_id)


    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('records_of_category', record_id=record.category.id)


    else:
        form = RecordForm(instance=record)


    return render(request, 'fin/d_cat.html', {'form': form})


