from django.db import models
from django.utils import timezone

# Create your models here.

class PatientVisit(models.Model):
    """
    Model representing a patient visit to the imaging dept.
    Based on real radiology workflow patterns.
    """
    
    EXAM_TYPE_CHOICES = [
        ('MRI_BRAIN', 'MRI Brain'),
        ('MRI_SPINE', 'MRI Spine'),
        ('MRI_KNEE', 'MRI Knee'),
        ('MRI_SHOULDER', 'MRI Shoulder'),
        ('MRI_ABDOMEN', 'MRI Abdomen'),
        ('CT_HEAD', 'CT Head'),
        ('CT_ABDOMEN', 'CT Abdomen'),
        ('CT_CHEST', 'CT Chest'),
        ('XRAY_CHEST', 'X-Ray Chest'),
        ('XRAY_SPINE', 'X-Ray Spine'),        
    ]

    MODALITY_CHOICES = [
        ('MRI', 'MRI'),
        ('CT', 'CT'),
        ('XRAY', 'X-Ray'),
    ]
    
    # Patient identification
    patient_id = models.CharField(max_length=20)
    
    
    # visit details
    visit_date = models.DateTimeField(default=timezone.now)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    modality = models.CharField(max_length=10, choices=MODALITY_CHOICES)
    
    
    # Operational metrics
    wait_time = models.IntegerField(help_text="Wait time in minutes")
    scan_duration = models.IntegerField(help_text="Actual scan time in minutes")
    
    
    # Quality metrics
    satisfaction_score = models.IntegerField(
        help_text="Patient satisfaction score (1-5)",
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    
    
    # additional fields
    is_emergency = models.BooleanField(default=False)
    referring_physician = models.CharField(max_length=100)
    
    
    class Meta: 
        ordering = ['-visit_date']
        verbose_name = "Patient Visit"
        verbose_name_plural = "Patients Visits"
        
        
    def __str__(self):
        return f"{self.patient_id} - {self.get_exam_type_display()} on {self.visit_date.date()}"
    
    @property
    def total_time(self):
        """Total time patient speng (wait + scan)"""
        return self.wait_time + self.scan_duration