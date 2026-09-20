from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models


def home_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(
        request,
        'home.html'
    )


def register_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Registration successful! Welcome to SmartWaste.'
            )

            return redirect('dashboard')

    else:

        form = UserCreationForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            messages.success(
                request,
                'Login successful!'
            )

            return redirect('dashboard')

    else:

        form = AuthenticationForm()

    return render(
        request,
        'login.html',
        {'form': form}
    )


def logout_view(request):

    if request.method == 'POST':
        logout(request)

        messages.success(
            request,
            'You have been logged out successfully.'
        )

        return redirect('login_view')

    return redirect('dashboard')


@login_required
def dashboard_view(request):

    if not request.user.is_authenticated:
        return redirect('login_view')

    from detection.models import WasteDetection

    user_detections = WasteDetection.objects.filter(
        user=request.user
    )

    # Total detections
    total_detections = user_detections.count()

    # Recyclable waste
    recyclable_count = user_detections.filter(
        predicted_category__is_recyclable=True
    ).count()

    # Non-recyclable waste
    non_recyclable_count = user_detections.filter(
        predicted_category__is_recyclable=False
    ).count()

    # Category-wise detection count
    category_summary = (
        user_detections
        .filter(predicted_category__isnull=False)
        .values('predicted_category__name')
        .annotate(count=models.Count('id'))
        .order_by('-count')
    )

    # Prepare chart data
    category_labels = []
    category_counts = []

    for item in category_summary:
        category_labels.append(
            item['predicted_category__name'].title()
        )

        category_counts.append(
            item['count']
        )

    context = {
        'total_detections': total_detections,
        'recyclable_count': recyclable_count,
        'non_recyclable_count': non_recyclable_count,
        'category_summary': category_summary,
        'category_labels': category_labels,
        'category_counts': category_counts,
    }

    return render(
        request,
        'dashboard.html',
        context
    )

@login_required
def admin_dashboard_view(request):

    if not request.user.is_staff:
        return redirect('dashboard')

    from django.contrib.auth.models import User
    from detection.models import WasteDetection

    # Total Users
    total_users = User.objects.count()

    # Total Detections
    total_detections = WasteDetection.objects.count()

    # Recyclable Waste
    recyclable_count = WasteDetection.objects.filter(
        predicted_category__is_recyclable=True
    ).count()

    # Non-Recyclable Waste
    non_recyclable_count = WasteDetection.objects.filter(
        predicted_category__is_recyclable=False
    ).count()

    # Category-wise Waste Summary
    category_summary = (
        WasteDetection.objects
        .filter(predicted_category__isnull=False)
        .values('predicted_category__name')
        .annotate(count=models.Count('id'))
        .order_by('-count')
    )

    # Recent 10 Detections
    recent_detections = (
        WasteDetection.objects
        .select_related('user', 'predicted_category')
        .order_by('-created_at')[:10]
    )

    # Data for Chart
    category_labels = []
    category_counts = []

    for item in category_summary:
        category_labels.append(
            item['predicted_category__name'].title()
        )
        category_counts.append(
            item['count']
        )

    # Data sent to Template
    context = {
        'total_users': total_users,
        'total_detections': total_detections,
        'recyclable_count': recyclable_count,
        'non_recyclable_count': non_recyclable_count,
        'category_summary': category_summary,
        'recent_detections': recent_detections,
        'category_labels': category_labels,
        'category_counts': category_counts,
    }

    return render(
        request,
        'admin_dashboard.html',
        context
    )
@login_required
def profile_view(request):
    from detection.models import WasteDetection

    user_detections = WasteDetection.objects.filter(user=request.user)

    total_detections = user_detections.count()

    recyclable_count = user_detections.filter(
        predicted_category__is_recyclable=True
    ).count()

    non_recyclable_count = user_detections.filter(
        predicted_category__is_recyclable=False
    ).count()

    context = {
        'total_detections': total_detections,
        'recyclable_count': recyclable_count,
        'non_recyclable_count': non_recyclable_count,
    }

    return render(request, 'profile.html', context)