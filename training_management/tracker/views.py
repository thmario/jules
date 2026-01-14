from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import CourseAssignment

def index(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        else:
            return redirect('employee_dashboard')
    else:
        return redirect('login')

@login_required
def employee_dashboard(request):
    assignments = CourseAssignment.objects.filter(employee=request.user)
    total_courses = assignments.count()
    completed_courses = assignments.filter(status='COMPLETED').count()

    if total_courses > 0:
        progress_percentage = (completed_courses / total_courses) * 100
    else:
        progress_percentage = 0

    context = {
        'assignments': assignments,
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'progress_percentage': progress_percentage,
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    employees = User.objects.filter(is_staff=False)
    employee_progress = []

    for employee in employees:
        assignments = CourseAssignment.objects.filter(employee=employee)
        total_courses = assignments.count()
        completed_courses = assignments.filter(status='COMPLETED').count()

        if total_courses > 0:
            progress_percentage = (completed_courses / total_courses) * 100
        else:
            progress_percentage = 0

        employee_progress.append({
            'employee': employee,
            'progress_percentage': progress_percentage,
            'completed_courses': completed_courses,
            'total_courses': total_courses,
        })

    context = {
        'employee_progress': employee_progress,
    }
    return render(request, 'tracker/admin_dashboard.html', context)
