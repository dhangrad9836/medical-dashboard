from django.core.management.base import BaseCommand #this is to create custom management commands like python manage.py generate_data
from metrics.models import PatientVisit #import the PatientVisit model/database that we will populate with fake data
from faker import Faker #faker library to generate fake data
import random
from datetime import timedelta, datetime 
from django.utils import timezone

# instance of Faker data using the Faker library
# store an instance of the Faker class inside a variable called fake
fake = Faker()

# Every django management command must be a class named Command that inherits from BaseCommand
class Command(BaseCommand):
    help = 'Generate sample patient visit data for the dashboard'   # what will be shown when running python manage.py help generate_data
    
    def add_arguments(self, parser): # add custom arguments to the command line
        parser.add_argument(    # allow user to specify number of patient visits to generate
            '--count',          # flag to specify number of records to create (visits)
            type=int,
            default=200,        # ie: python manage.py generate_data --count 500 would generate 500 records
            help='Number of patient visits to generte'
        )
        
    # when the command is run, this handle method is called
    def handle(self, *args, **options):
        count = options['count']    # gets the number you passed with --count (or default 200 which we specified above)
        
        
        #Clear exisitng data
        PatientVisit.objects.all().delete()
        self.stdout.write('Cleared exisitng patient visit data')
        
        #Exam type probabilities (based on a normal radiology workflow)
        # Exam type is MRI_BRAIN, Modality is MRI, Weight is 20...how common this exam type is
        exam_types = [
            # SCAN, MODALITY, TIME
            ('MRI_BRAIN', 'MRI', 20),
            ('MRI_SPINE', 'MRI', 18),
            ('MRI_KNEE', 'MRI', 15),
            ('MRI_SHOULDER', 'MRI', 10),
            ('MRI_ABDOMEN', 'MRI', 10),
            ('CT_HEAD', 'CT', 8),
            ('CT_CHEST', 'CT', 7),
            ('CT_ABDOMEN', 'CT', 5),
            ('XRAY_CHEST', 'XRAY', 4),
            ('XRAY_SPINE', 'XRAY', 3)
        ]
        
        #Create weighted list for random selection
        exam_pool = []  # extend to this list based on weights above
        for exam, modality, weight in exam_types:
            exam_pool.extend([(exam, modality)] * weight)
            
            
        # Generate sample physicians
        physicians = [
            'Dr. Smith',
            'Dr. Williams',
            'Dr. Johnson',
            'Dr. Brown',
            'Dr. Miller',
            'Dr. Wilson',
            'Dr. Davis',
            'Dr. Moore',
        ]
        
        # visits list to store visits objects before bulk creating
        visits = []
        start_date = timezone.now() - timedelta(days=90) # represents 90 days ago from today
        
        for i in range(count):  # loop to create 'count' number of patient visits the 200 visits by default
            #Random date within the last 90 days
            #weight towards weekdays (less active on weekends)
            days_ago = random.randint(0, 90) # this number represents the number of days to add to the start_date below
            visit_date = start_date + timedelta(days=days_ago)
            
            # if we randomly picked a weekend day, there's a 60% chance we'll re-roll and pick a different day. Most visits are on weekdays
            if visit_date.weekday() >= 5 and random.random() < 0.6: # .weekday() is a builtin method from datetime that returns 5 for saturday and 6 for sunday and we skip 60% of weekends
                days_ago = random.randint(0, 90)
                visit_date = start_date + timedelta(days=days_ago)
                
                
            #add time of day (business hrs 7a - 7p)
            hour = random.randint(7,19) # pick a random hour btw 7a and 7p
            minute = random.choice([0, 15, 30, 45])  # pick a random minute
            visit_date = visit_date.replace(hour=hour, minute=minute, second=0)
            
            
            # select exam type and modality
            # might return exam_type = 'MRI_BRAIN', modality = 'MRI'
            exam_type, modality = random.choice(exam_pool)
                
            
            # Generate wait time
            # most wait times are 10-45 minutes, sometimes longer (if hospital emergencies, stats etc...)
            if random.random() < 0.8:   # generates a time btw 0.0 and 1.0, 80% of the time wait time is 10-45 minutes
                wait_time = random.randint(10,45)
            else:
                wait_time = random.randint(45, 120) # 20% of the wait times are longer ie: emergencies. delays...45-120 minutes long
                
            # scan duration varies my modality
            if modality == 'MRI':
                scan_duration = random.randint(20,60)
            elif modality =='CT':
                scan_duration = random.randint(5, 15)
            else: #xray
                scan_duration = random.randint(2, 8)
                
            #satisfaction score (positive/negative)
            satisfaction_weights = [2, 5, 10, 35, 48] #1-5 stars...1 star is 2% chance, 2 stars is 5% chance, 3 stars is 10% chance, 4 stars is 35% chance, 5 stars is 48% chance
            satisfaction_score = random.choices(range(1,6), weights=satisfaction_weights)[0] # weights parameter allows us to specify the prbablility of each choice. Returns a list, so we take the first element with [0]
            # random.choices returns a list even if we only want one choice
                
                
            # Emergency cases (5% of visits)
            is_emergency = random.random() < 0.05
            if is_emergency:
                wait_time = random.randint(2, 15)   #if emergency is not too long 2-15 minutes
            
            # create PatientVisit object with all the data we generated above stored in vist variable    
            visit = PatientVisit(
                patient_id=f'PT{1000 + i}', # unique patient id like PT1001, PT1002, etc
                visit_date=visit_date,
                exam_type=exam_type,
                modality=modality,
                wait_time=wait_time,
                scan_duration=scan_duration,
                satisfaction_score=satisfaction_score,
                is_emergency=is_emergency,
                referring_physician=random.choice(physicians)
            )
            
            visits.append(visit) # add the visit object to the visits list
            
        # Bulk create for efficiency..saves all visits to the database at once
        PatientVisit.objects.bulk_create(visits)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated {count} patient visits'
            )
        )
        
        # Print some statistics
        self.stdout.write('\n--- Statistics ---')
        self.stdout.write(f'Total visits: {PatientVisit.objects.count()}')
        self.stdout.write(f'MRI visits: {PatientVisit.objects.filter(modality="MRI").count()}')
        self.stdout.write(f'CT visits: {PatientVisit.objects.filter(modality="CT").count()}')
        self.stdout.write(f'X-Ray visits: {PatientVisit.objects.filter(modality="XRAY").count()}')
        self.stdout.write(f'Emergency visits: {PatientVisit.objects.filter(is_emergency=True).count()}')
        
        avg_wait = PatientVisit.objects.aggregate(models.Avg('wait_time'))
        self.stdout.write(f'Average wait time: {avg_wait["wait_time__avg"]:.1f} minutes')
        
        avg_satisfaction = PatientVisit.objects.aggregate(models.Avg('satisfaction_score'))
        self.stdout.write(f'Average satisfaction: {avg_satisfaction["satisfaction_score__avg"]:.2f}/5.0')


# Import at the end to avoid circular import
from django.db import models