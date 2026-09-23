import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import Http404

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import JobApplication
from .forms import JobApplicationForm, UserRegisterForm
from .serializers import JobApplicationSerializer


# --- Template Views ---

def landing_page(request):
    """Public landing page; redirects authenticated users directly to dashboard."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to JobTrack, {user.username}! Your account has been created.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below to register.")
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard_view(request):
    """User analytics and summary dashboard."""
    user_apps = JobApplication.objects.filter(user=request.user)

    total_apps = user_apps.count()
    applied_count = user_apps.filter(status='Applied').count()
    assessment_count = user_apps.filter(status='Assessment').count()
    interview_count = user_apps.filter(status='Interview').count()
    offer_count = user_apps.filter(status='Offer').count()
    rejected_count = user_apps.filter(status='Rejected').count()
    saved_count = user_apps.filter(status='Saved').count()
    withdrawn_count = user_apps.filter(status='Withdrawn').count()

    # Status Breakdown for Chart.js
    status_counts = user_apps.values('status').annotate(count=Count('id'))
    status_dict = {s[0]: 0 for s in JobApplication.STATUS_CHOICES}
    for item in status_counts:
        status_dict[item['status']] = item['count']

    status_labels = list(status_dict.keys())
    status_data = list(status_dict.values())

    # Priority Breakdown for Chart.js
    priority_counts = user_apps.values('priority').annotate(count=Count('id'))
    priority_dict = {p[0]: 0 for p in JobApplication.PRIORITY_CHOICES}
    for item in priority_counts:
        priority_dict[item['priority']] = item['count']

    recent_applications = user_apps[:5]

    context = {
        'total_apps': total_apps,
        'applied_count': applied_count,
        'assessment_count': assessment_count,
        'interview_count': interview_count,
        'offer_count': offer_count,
        'rejected_count': rejected_count,
        'saved_count': saved_count,
        'withdrawn_count': withdrawn_count,
        'status_labels_json': json.dumps(status_labels),
        'status_data_json': json.dumps(status_data),
        'priority_labels_json': json.dumps(list(priority_dict.keys())),
        'priority_data_json': json.dumps(list(priority_dict.values())),
        'recent_applications': recent_applications,
    }
    return render(request, 'dashboard.html', context)


@login_required
def application_list_view(request):
    """Application list page with Search, Multi-field Filtering, Sorting, and Pagination."""
    queryset = JobApplication.objects.filter(user=request.user)

    # Search Query
    search_query = request.GET.get('q', '').strip()
    if search_query:
        queryset = queryset.filter(
            Q(company__icontains=search_query) |
            Q(position__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(source__icontains=search_query)
        )

    # Filtering
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    emp_type_filter = request.GET.get('employment_type', '').strip()
    if emp_type_filter:
        queryset = queryset.filter(employment_type=emp_type_filter)

    priority_filter = request.GET.get('priority', '').strip()
    if priority_filter:
        queryset = queryset.filter(priority=priority_filter)

    # Sorting
    sort_by = request.GET.get('sort', '-updated_at').strip()
    valid_sort_fields = [
        'company', '-company',
        'position', '-position',
        'date_applied', '-date_applied',
        'status', '-status',
        'priority', '-priority',
        'updated_at', '-updated_at',
        'created_at', '-created_at',
    ]
    if sort_by in valid_sort_fields:
        queryset = queryset.order_by(sort_by)
    else:
        queryset = queryset.order_by('-updated_at')

    # Pagination
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'emp_type_filter': emp_type_filter,
        'priority_filter': priority_filter,
        'sort_by': sort_by,
        'status_choices': JobApplication.STATUS_CHOICES,
        'emp_type_choices': JobApplication.EMPLOYMENT_TYPE_CHOICES,
        'priority_choices': JobApplication.PRIORITY_CHOICES,
        'total_count': paginator.count,
    }
    return render(request, 'applications/list.html', context)


@login_required
def application_detail_view(request, pk):
    """View details of a single job application."""
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    return render(request, 'applications/detail.html', {'application': application})


@login_required
def application_create_view(request):
    """Add new job application."""
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, f"Application for '{application.position}' at '{application.company}' added successfully.")
            return redirect('application_detail', pk=application.pk)
        else:
            messages.error(request, "Please fix the errors in the form below.")
    else:
        form = JobApplicationForm()

    return render(request, 'applications/form.html', {'form': form, 'title': 'Add New Job Application', 'is_edit': False})


@login_required
def application_update_view(request, pk):
    """Edit existing job application."""
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, f"Application for '{application.company}' updated successfully.")
            return redirect('application_detail', pk=application.pk)
        else:
            messages.error(request, "Please fix the errors in the form below.")
    else:
        form = JobApplicationForm(instance=application)

    return render(request, 'applications/form.html', {'form': form, 'title': f'Edit Application - {application.company}', 'application': application, 'is_edit': True})


@login_required
def application_delete_view(request, pk):
    """Delete job application with confirmation."""
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)

    if request.method == 'POST':
        company_name = application.company
        application.delete()
        messages.success(request, f"Application for '{company_name}' deleted successfully.")
        return redirect('application_list')

    return render(request, 'applications/confirm_delete.html', {'application': application})


# --- REST API Views ---

class JobApplicationListCreateAPIView(generics.ListCreateAPIView):
    """
    GET /api/applications/ - List logged-in user's applications
    POST /api/applications/ - Create new application for logged-in user
    """
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobApplicationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/applications/<id>/ - Retrieve user's application
    PUT /api/applications/<id>/ - Update user's application
    PATCH /api/applications/<id>/ - Partial update
    DELETE /api/applications/<id>/ - Delete application
    """
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)
