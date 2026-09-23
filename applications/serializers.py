from rest_framework import serializers
from .models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = JobApplication
        fields = [
            'id',
            'user',
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
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
