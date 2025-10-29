from django.contrib import admin
from .models import PatientVisit

# Register your models here.
@admin.register(PatientVisit)
class PatientVisitAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'visit_date', 'exam_type', 'modality', 'wait_time', 'satisfaction_score']
    list_filter = ['modality', 'exam_type', 'is_emergency']
    search_fields = ['patient_id', 'referring_physician']
    date_hierarchy = 'visit_date'