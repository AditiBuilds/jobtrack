from django.db import models
from django.contrib.auth.models import User


class JobApplication(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract'),
    ]

    STATUS_CHOICES = [
        ('Saved', 'Saved'),
        ('Applied', 'Applied'),
        ('Assessment', 'Assessment'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected'),
        ('Withdrawn', 'Withdrawn'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )
    company = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True, default='')
    employment_type = models.CharField(
        max_length=50,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='Full-time'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Applied'
    )
    date_applied = models.DateField(null=True, blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    job_url = models.URLField(max_length=500, blank=True, default='')
    source = models.CharField(max_length=100, blank=True, default='')
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.company} - {self.position}"

    @property
    def status_badge_class(self):
        badge_map = {
            'Saved': 'bg-secondary',
            'Applied': 'bg-primary',
            'Assessment': 'bg-info text-dark',
            'Interview': 'bg-warning text-dark',
            'Offer': 'bg-success',
            'Rejected': 'bg-danger',
            'Withdrawn': 'bg-dark',
        }
        return badge_map.get(self.status, 'bg-secondary')

    @property
    def priority_badge_class(self):
        badge_map = {
            'Low': 'bg-secondary',
            'Medium': 'bg-info text-dark',
            'High': 'bg-danger',
        }
        return badge_map.get(self.priority, 'bg-secondary')
