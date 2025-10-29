from django.shortcuts import render
from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncDate, ExtractWeekDay
from django.utils import timezone
from datetime import timedelta
from .models import PatientVisit

def dashboard_home(request):
    """
    Main dashboard view with key metrics.
    Demonstrates SQL aggregation and date filtering.
    """
    
    # Current month start
    today = timezone.now()
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Last 30 days
    thirty_days_ago = today - timedelta(days=30)
    
    # Key Metrics (SQL aggregations)
    
    # Total visits this month
    visits_this_month = PatientVisit.objects.filter(
        visit_date__gte=month_start
    ).count()
    
    # Average wait time (last 30 days)
    avg_wait = PatientVisit.objects.filter(
        visit_date__gte=thirty_days_ago
    ).aggregate(Avg('wait_time'))['wait_time__avg'] or 0
    
    # Patient satisfaction average
    avg_satisfaction = PatientVisit.objects.aggregate(
        Avg('satisfaction_score')
    )['satisfaction_score__avg'] or 0
    
    # Most common exam type
    top_exam = PatientVisit.objects.values('exam_type').annotate(
        count=Count('id')
    ).order_by('-count').first()
    
    # Modality utilization
    modality_stats = PatientVisit.objects.values('modality').annotate(
        count=Count('id'),
        avg_wait=Avg('wait_time')
    ).order_by('modality')
    
    # Recent visits (last 10)
    recent_visits = PatientVisit.objects.all()[:10]
    
    context = {
        'visits_this_month': visits_this_month,
        'avg_wait_time': round(avg_wait, 1),
        'avg_satisfaction': round(avg_satisfaction, 2),
        'top_exam': top_exam,
        'modality_stats': modality_stats,
        'recent_visits': recent_visits,
        'total_visits': PatientVisit.objects.count(),
    }
    
    return render(request, 'metrics/dashboard.html', context)


def data_view(request):
    """
    Data table view with filtering.
    Shows all patient visits with optional filters.
    """
    
    visits = PatientVisit.objects.all()
    
    # Optional filtering
    modality = request.GET.get('modality')
    exam_type = request.GET.get('exam_type')
    
    if modality:
        visits = visits.filter(modality=modality)
    
    if exam_type:
        visits = visits.filter(exam_type=exam_type)
    
    # Get unique values for filters
    modalities = PatientVisit.objects.values_list('modality', flat=True).distinct()
    exam_types = PatientVisit.objects.values_list('exam_type', flat=True).distinct()
    
    context = {
        'visits': visits[:100],  # Limit to 100 for performance
        'modalities': modalities,
        'exam_types': exam_types,
        'selected_modality': modality,
        'selected_exam_type': exam_type,
    }
    
    return render(request, 'metrics/data.html', context)


def reports_view(request):
    """
    Reports view with data for charts.
    Provides aggregated data for Chart.js visualizations.
    """
    
    # Visits by day of week
    visits_by_weekday = PatientVisit.objects.annotate(
        weekday=ExtractWeekDay('visit_date')
    ).values('weekday').annotate(
        count=Count('id')
    ).order_by('weekday')
    
    # Convert weekday numbers to names
    weekday_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    weekday_data = {day: 0 for day in weekday_names}
    
    for item in visits_by_weekday:
        # Django's ExtractWeekDay: 1=Sunday, 2=Monday, etc.
        day_name = weekday_names[item['weekday'] - 1]
        weekday_data[day_name] = item['count']
    
    # Exam type breakdown
    exam_breakdown = PatientVisit.objects.values('exam_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Daily visit trends (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    daily_trends = PatientVisit.objects.filter(
        visit_date__gte=thirty_days_ago
    ).annotate(
        date=TruncDate('visit_date')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    # Average wait time by exam type
    wait_by_exam = PatientVisit.objects.values('exam_type').annotate(
        avg_wait=Avg('wait_time')
    ).order_by('-avg_wait')
    
    context = {
        'weekday_data': weekday_data,
        'exam_breakdown': exam_breakdown,
        'daily_trends': list(daily_trends),
        'wait_by_exam': wait_by_exam,
    }
    
    return render(request, 'metrics/reports.html', context)


def technical_notes(request):
    """
    Technical documentation page.
    Shows SQL queries and explains the implementation.
    """
    
    sql_examples = [
        {
            'title': 'Total Visits This Month',
            'query': '''
SELECT COUNT(*) as total_visits
FROM metrics_patientvisit
WHERE visit_date >= DATE('now', 'start of month');
            ''',
            'django_orm': "PatientVisit.objects.filter(visit_date__gte=month_start).count()"
        },
        {
            'title': 'Average Wait Time by Exam Type',
            'query': '''
SELECT exam_type, AVG(wait_time) as avg_wait
FROM metrics_patientvisit
GROUP BY exam_type
ORDER BY avg_wait DESC;
            ''',
            'django_orm': "PatientVisit.objects.values('exam_type').annotate(avg_wait=Avg('wait_time')).order_by('-avg_wait')"
        },
        {
            'title': 'Busiest Days of Week',
            'query': '''
SELECT strftime('%w', visit_date) as day_of_week, 
       COUNT(*) as visit_count
FROM metrics_patientvisit
GROUP BY day_of_week
ORDER BY visit_count DESC;
            ''',
            'django_orm': "PatientVisit.objects.annotate(weekday=ExtractWeekDay('visit_date')).values('weekday').annotate(count=Count('id'))"
        },
        {
            'title': 'Patient Satisfaction Breakdown',
            'query': '''
SELECT satisfaction_score, COUNT(*) as count
FROM metrics_patientvisit
GROUP BY satisfaction_score
ORDER BY satisfaction_score DESC;
            ''',
            'django_orm': "PatientVisit.objects.values('satisfaction_score').annotate(count=Count('id'))"
        }
    ]
    
    context = {
        'sql_examples': sql_examples
    }
    
    return render(request, 'metrics/technical.html', context)