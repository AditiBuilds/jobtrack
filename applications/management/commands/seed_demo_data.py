from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from applications.models import JobApplication


class Command(BaseCommand):
    help = 'Seeds realistic demo job application data for testing and demonstration.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding demo user and job applications...'))

        # Create or update demo user
        demo_user, created = User.objects.get_or_create(username='demo')
        if created or not demo_user.check_password('DemoPassword123!'):
            demo_user.set_password('DemoPassword123!')
            demo_user.email = 'demo@jobtrack.app'
            demo_user.first_name = 'Demo'
            demo_user.last_name = 'User'
            demo_user.save()
            self.stdout.write(self.style.SUCCESS('Created demo user: username=demo, password=DemoPassword123!'))
        else:
            self.stdout.write(self.style.SUCCESS('Demo user exists: username=demo'))

        # Clear old applications for demo user to ensure clean state
        demo_user.job_applications.all().delete()

        today = date.today()
        now = timezone.now()

        demo_data = [
            {
                'company': 'Google',
                'position': 'Software Engineer - Backend',
                'location': 'Bengaluru',
                'employment_type': 'Full-time',
                'status': 'Offer',
                'date_applied': today - timedelta(days=45),
                'interview_date': now - timedelta(days=5),
                'salary': 3200000.00,
                'job_url': 'https://careers.google.com/jobs/results/12345678',
                'source': 'LinkedIn',
                'priority': 'High',
                'notes': 'Completed 4 rounds (Coding 1, Coding 2, System Design, Googyness). Received formal offer letter! Negotiating stock units.'
            },
            {
                'company': 'Microsoft',
                'position': 'Software Engineer II',
                'location': 'Hyderabad',
                'employment_type': 'Full-time',
                'status': 'Interview',
                'date_applied': today - timedelta(days=30),
                'interview_date': now + timedelta(days=3),
                'salary': 2800000.00,
                'job_url': 'https://careers.microsoft.com/us/en/job/987654',
                'source': 'Company Website',
                'priority': 'High',
                'notes': 'Passed screening. Technical interview scheduled for upcoming Friday. Focus areas: Distributed systems and trees/graphs.'
            },
            {
                'company': 'Amazon',
                'position': 'SDE-1',
                'location': 'Bengaluru',
                'employment_type': 'Full-time',
                'status': 'Assessment',
                'date_applied': today - timedelta(days=12),
                'interview_date': None,
                'salary': 2500000.00,
                'job_url': 'https://amazon.jobs/en/jobs/234567',
                'source': 'Referral',
                'priority': 'High',
                'notes': 'Completed OA1 and OA2 online assessments on Hackerrank. Waiting for recruiter feedback.'
            },
            {
                'company': 'Razorpay',
                'position': 'Senior Python Developer',
                'location': 'Bengaluru (Hybrid)',
                'employment_type': 'Full-time',
                'status': 'Interview',
                'date_applied': today - timedelta(days=20),
                'interview_date': now + timedelta(days=1),
                'salary': 2400000.00,
                'job_url': 'https://razorpay.com/jobs/py-sr-dev',
                'source': 'Naukri.com',
                'priority': 'High',
                'notes': 'LLD round completed with Principal Engineer. System design round next.'
            },
            {
                'company': 'TCS',
                'position': 'Digital Software Developer',
                'location': 'Hyderabad',
                'employment_type': 'Full-time',
                'status': 'Applied',
                'date_applied': today - timedelta(days=15),
                'interview_date': None,
                'salary': 700000.00,
                'job_url': 'https://nextstep.tcs.com/',
                'source': 'Campus / On-Campus Portal',
                'priority': 'Medium',
                'notes': 'Application submitted via TCS NextStep portal. Awaiting NQT score verification.'
            },
            {
                'company': 'Swiggy',
                'position': 'Backend Engineer - Go/Python',
                'location': 'Remote',
                'employment_type': 'Full-time',
                'status': 'Assessment',
                'date_applied': today - timedelta(days=8),
                'interview_date': None,
                'salary': 2200000.00,
                'job_url': 'https://careers.swiggy.com/job/be-remote',
                'source': 'LinkedIn',
                'priority': 'High',
                'notes': 'Take-home assignment received: Building a rate-limiter service in Python/Go.'
            },
            {
                'company': 'Flipkart',
                'position': 'UI/UX Full Stack Engineer',
                'location': 'Bengaluru',
                'employment_type': 'Full-time',
                'status': 'Applied',
                'date_applied': today - timedelta(days=5),
                'interview_date': None,
                'salary': 2600000.00,
                'job_url': 'https://www.flipkartcareers.com/job-detail/33421',
                'source': 'LinkedIn',
                'priority': 'Medium',
                'notes': 'Applied directly with customized resume emphasizing React and Django skills.'
            },
            {
                'company': 'Zoho',
                'position': 'Product Developer',
                'location': 'Chennai',
                'employment_type': 'Full-time',
                'status': 'Interview',
                'date_applied': today - timedelta(days=25),
                'interview_date': now - timedelta(days=2),
                'salary': 1200000.00,
                'job_url': 'https://www.zoho.com/careers/developer',
                'source': 'Company Website',
                'priority': 'Medium',
                'notes': 'Attended machine coding round in Chennai campus. Solved memory allocation problem.'
            },
            {
                'company': 'Freshworks',
                'position': 'Frontend Engineer (React)',
                'location': 'Chennai',
                'employment_type': 'Full-time',
                'status': 'Applied',
                'date_applied': today - timedelta(days=10),
                'interview_date': None,
                'salary': 1600000.00,
                'job_url': 'https://freshworks.com/careers/fe-eng',
                'source': 'LinkedIn',
                'priority': 'Medium',
                'notes': 'Application submitted.'
            },
            {
                'company': 'Deloitte',
                'position': 'Consultant - Cloud Solutions',
                'location': 'Hyderabad',
                'employment_type': 'Full-time',
                'status': 'Rejected',
                'date_applied': today - timedelta(days=60),
                'interview_date': None,
                'salary': 1500000.00,
                'job_url': 'https://jobs2.deloitte.com/job/4421',
                'source': 'Indeed',
                'priority': 'Low',
                'notes': 'Position on hold due to client budget realignment.'
            },
            {
                'company': 'Infosys',
                'position': 'Specialist Programmer',
                'location': 'Mysuru / Remote',
                'employment_type': 'Full-time',
                'status': 'Applied',
                'date_applied': today - timedelta(days=14),
                'interview_date': None,
                'salary': 950000.00,
                'job_url': 'https://infosys.com/careers',
                'source': 'Infytq Portal',
                'priority': 'Medium',
                'notes': 'HackWithInfy submission done.'
            },
            {
                'company': 'Accenture',
                'position': 'Advanced Application Engineering Analyst',
                'location': 'Pune',
                'employment_type': 'Full-time',
                'status': 'Saved',
                'date_applied': None,
                'interview_date': None,
                'salary': 650000.00,
                'job_url': 'https://accenture.com/jobs/aeea-pune',
                'source': 'Indeed',
                'priority': 'Low',
                'notes': 'Saved to review requirements later.'
            },
            {
                'company': 'Cognizant',
                'position': 'GenC Next Engineer',
                'location': 'Kolkata',
                'employment_type': 'Full-time',
                'status': 'Rejected',
                'date_applied': today - timedelta(days=50),
                'interview_date': None,
                'salary': 675000.00,
                'job_url': 'https://cognizant.com/careers',
                'source': 'Campus',
                'priority': 'Low',
                'notes': 'Did not clear aptitude test section.'
            },
            {
                'company': 'Capgemini',
                'position': 'Software Engineer Intern',
                'location': 'Mumbai',
                'employment_type': 'Internship',
                'status': 'Withdrawn',
                'date_applied': today - timedelta(days=70),
                'interview_date': None,
                'salary': 35000.00,
                'job_url': 'https://capgemini.com/careers/intern-2026',
                'source': 'LinkedIn',
                'priority': 'Low',
                'notes': 'Withdrew application after accepting full-time offer.'
            },
            {
                'company': 'Wipro',
                'position': 'Project Engineer',
                'location': 'Bengaluru',
                'employment_type': 'Full-time',
                'status': 'Saved',
                'date_applied': None,
                'interview_date': None,
                'salary': 550000.00,
                'job_url': 'https://careers.wipro.com/job/pe',
                'source': 'Naukri.com',
                'priority': 'Low',
                'notes': 'Draft saved.'
            },
            {
                'company': 'PhonePe',
                'position': 'Software Engineer - Infrastructure',
                'location': 'Bengaluru',
                'employment_type': 'Full-time',
                'status': 'Applied',
                'date_applied': today - timedelta(days=4),
                'interview_date': None,
                'salary': 2700000.00,
                'job_url': 'https://phonepe.com/careers/infra-sde',
                'source': 'Referral',
                'priority': 'High',
                'notes': 'Referred by senior engineer. Application under recruiter review.'
            },
            {
                'company': 'Intuit',
                'position': 'Software Engineer I',
                'location': 'Bengaluru',
                'employment_type': 'Full-time',
                'status': 'Assessment',
                'date_applied': today - timedelta(days=9),
                'interview_date': None,
                'salary': 2300000.00,
                'job_url': 'https://intuit.com/careers/sde1',
                'source': 'LinkedIn',
                'priority': 'High',
                'notes': 'Karat technical screening scheduled.'
            },
            {
                'company': 'Atlassian',
                'position': 'Associate Developer',
                'location': 'Bengaluru (Remote)',
                'employment_type': 'Full-time',
                'status': 'Interview',
                'date_applied': today - timedelta(days=18),
                'interview_date': now + timedelta(days=4),
                'salary': 3000000.00,
                'job_url': 'https://atlassian.com/careers/assoc-dev',
                'source': 'Company Website',
                'priority': 'High',
                'notes': 'Passed values interview. System design and coding round next.'
            }
        ]

        count = 0
        for data in demo_data:
            JobApplication.objects.create(user=demo_user, **data)
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} job applications for user "demo"!'))
