from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from college.models import College  # Adjust import as necessary

class Command(BaseCommand):
    help = 'Populate the database with sample college data'

    def handle(self, *args, **kwargs):
        # Sample user creation
        admin_user_1 = User.objects.create_user(username='IIT_Madras', password='password1')
        admin_user_2 = User.objects.create_user(username='IIT_Bombay', password='password2')
        admin_user_3 = User.objects.create_user(username='IIM_Ahmedabad', password='password3')
        admin_user_4 = User.objects.create_user(username='BITS_Pilani', password='password4')
        admin_user_5 = User.objects.create_user(username='NIT_Trichy', password='password5')
        admin_user_6 = User.objects.create_user(username='IIT_Delhi', password='password6')

        # Sample data for College instances
        colleges = [
            College.objects.create(
                user=admin_user_1,
                established_year=1959,
                type='Public',
                location='Madras, Chennai',
                campus_area=617.00,
                established_by='Government of India',
                nirf_ranking=1,  # Overall NIRF ranking
                total_departments=16,
                admission_criteria='Entrance Based',
                top_courses='B.Tech, M.Tech, Dual Degree',
                official_website='https://www.iitm.ac.in'
            ),
            College.objects.create(
                user=admin_user_2,
                established_year=1958,
                type='Public',
                location='Mumbai, Maharashtra',
                campus_area=550.00,
                established_by='Government of India',
                nirf_ranking=3,  # Overall NIRF ranking
                total_departments=15,
                admission_criteria='Entrance Based',
                top_courses='B.Tech, M.Sc., MBA',
                official_website='https://www.iitb.ac.in'
            ),
            College.objects.create(
                user=admin_user_3,
                established_year=1961,
                type='Public',
                location='Ahmedabad, Gujarat',
                campus_area=102.00,
                established_by='Government of India',
                nirf_ranking=1,  # Management NIRF ranking (considered as overall here)
                total_departments=20,
                admission_criteria='CAT/GRE/GMAT',
                top_courses='MBA, PGP, Executive MBA',
                official_website='https://www.iima.ac.in'
            ),
            College.objects.create(
                user=admin_user_4,
                established_year=1964,
                type='Private',
                location='Pilani, Rajasthan',
                campus_area=328.00,
                established_by='Birla Education Trust',
                nirf_ranking=25,  # Overall NIRF ranking
                total_departments=12,
                admission_criteria='BITSAT',
                top_courses='B.E., M.Sc., PhD',
                official_website='https://www.bits-pilani.ac.in'
            ),
            College.objects.create(
                user=admin_user_5,
                established_year=1964,
                type='Public',
                location='Tiruchirappalli, Tamil Nadu',
                campus_area=800.00,
                established_by='Government of India',
                nirf_ranking=8,  # Overall NIRF ranking
                total_departments=14,
                admission_criteria='JEE Main',
                top_courses='B.Tech, M.Tech, PhD',
                official_website='https://www.nitt.edu'
            ),
            College.objects.create(
                user=admin_user_6,
                established_year=1961,
                type='Public',
                location='New Delhi',
                campus_area=325.00,
                established_by='Government of India',
                nirf_ranking=2,  # Overall NIRF ranking
                total_departments=17,
                admission_criteria='Entrance Based',
                top_courses='B.Tech, M.Tech, MBA',
                official_website='https://www.iitd.ac.in'
            ),
        ]

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with college data.'))
