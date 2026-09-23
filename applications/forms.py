from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'company',
            'position',
            'location',
            'employment_type',
            'status',
            'date_applied',
            'interview_date',
            'salary',
            'job_url',
            'source',
            'priority',
            'notes',
        ]
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. TCS, Google, Amazon'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Software Engineer, Data Analyst'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Hyderabad, Remote, Bengaluru'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'date_applied': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'interview_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 600000', 'step': '1000'}),
            'job_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/jobs/...'}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. LinkedIn, Indeed, Referral'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Add notes about interview prep, tech stack, contacts...'}),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}))
    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
