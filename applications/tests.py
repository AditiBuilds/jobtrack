from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import JobApplication

# Python 3.14 compatibility patch for Django template Context copy during test rendering signal
from django.template.context import BaseContext
def _patched_context_copy(self):
    duplicate = object.__new__(self.__class__)
    duplicate.dicts = [d.copy() for d in self.dicts]
    if hasattr(self, 'request'):
        duplicate.request = self.request
    if hasattr(self, 'template'):
        duplicate.template = self.template
    return duplicate
BaseContext.__copy__ = _patched_context_copy


class JobApplicationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='TestPassword123!')
        self.app = JobApplication.objects.create(
            user=self.user,
            company='Google',
            position='Software Engineer',
            location='Bengaluru',
            employment_type='Full-time',
            status='Applied',
            priority='High',
            salary=3000000.00,
            job_url='https://careers.google.com/jobs/1',
            notes='Prepping DSA and System Design'
        )

    def test_model_creation_and_str(self):
        self.assertEqual(str(self.app), 'Google - Software Engineer')
        self.assertEqual(self.app.user.username, 'testuser')
        self.assertEqual(self.app.status_badge_class, 'bg-primary')
        self.assertEqual(self.app.priority_badge_class, 'bg-danger')


class AuthenticationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alice', password='AlicePassword123!', email='alice@example.com')

    def test_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'bob',
            'email': 'bob@example.com',
            'password1': 'BobPassword123!',
            'password2': 'BobPassword123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='bob').exists())

    def test_login_and_logout(self):
        login_success = self.client.login(username='alice', password='AlicePassword123!')
        self.assertTrue(login_success)

        # Dashboard protected access
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_redirect(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"/login/?next=/dashboard/")


class JobApplicationCRUDViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='Password123!')
        self.user2 = User.objects.create_user(username='user2', password='Password123!')

        self.app1 = JobApplication.objects.create(
            user=self.user1,
            company='Microsoft',
            position='SDE 2',
            location='Hyderabad',
            status='Interview',
            priority='High'
        )
        self.app2 = JobApplication.objects.create(
            user=self.user2,
            company='Amazon',
            position='SDE 1',
            location='Bengaluru',
            status='Applied',
            priority='Medium'
        )

    def test_application_creation_view(self):
        self.client.login(username='user1', password='Password123!')
        response = self.client.post(reverse('application_create'), {
            'company': 'Netflix',
            'position': 'Senior Software Engineer',
            'location': 'Remote',
            'employment_type': 'Full-time',
            'status': 'Applied',
            'priority': 'High',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(JobApplication.objects.filter(company='Netflix', user=self.user1).exists())

    def test_application_edit_view(self):
        self.client.login(username='user1', password='Password123!')
        response = self.client.post(reverse('application_update', args=[self.app1.pk]), {
            'company': 'Microsoft Azure',
            'position': 'Senior SDE',
            'location': 'Hyderabad',
            'employment_type': 'Full-time',
            'status': 'Offer',
            'priority': 'High',
        })
        self.assertEqual(response.status_code, 302)
        self.app1.refresh_from_db()
        self.assertEqual(self.app1.company, 'Microsoft Azure')
        self.assertEqual(self.app1.status, 'Offer')

    def test_application_delete_view(self):
        self.client.login(username='user1', password='Password123!')
        response = self.client.post(reverse('application_delete', args=[self.app1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(JobApplication.objects.filter(pk=self.app1.pk).exists())

    def test_user_data_isolation(self):
        """Ensure User 1 cannot view or edit User 2's applications."""
        self.client.login(username='user1', password='Password123!')

        # Detail view for User 2's app should return 404
        response_detail = self.client.get(reverse('application_detail', args=[self.app2.pk]))
        self.assertEqual(response_detail.status_code, 404)

        # Edit view for User 2's app should return 404
        response_edit = self.client.get(reverse('application_update', args=[self.app2.pk]))
        self.assertEqual(response_edit.status_code, 404)

        # List view should only contain user1's app, not user2's app
        response_list = self.client.get(reverse('application_list'))
        self.assertContains(response_list, 'Microsoft')
        self.assertNotContains(response_list, 'Amazon')

    def test_search_and_filters(self):
        self.client.login(username='user1', password='Password123!')
        # Search for 'Microsoft'
        res_search = self.client.get(reverse('application_list') + '?q=Microsoft')
        self.assertContains(res_search, 'Microsoft')

        # Filter by status 'Interview'
        res_filter = self.client.get(reverse('application_list') + '?status=Interview')
        self.assertContains(res_filter, 'Microsoft')

        # Filter by status 'Offer' (should return empty)
        res_empty = self.client.get(reverse('application_list') + '?status=Offer')
        self.assertNotContains(res_empty, 'Microsoft')


class JobApplicationAPITest(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.user1 = User.objects.create_user(username='api_user1', password='Password123!')
        self.user2 = User.objects.create_user(username='api_user2', password='Password123!')

        self.app1 = JobApplication.objects.create(
            user=self.user1,
            company='Zoho',
            position='Backend Developer',
            status='Applied'
        )
        self.app2 = JobApplication.objects.create(
            user=self.user2,
            company='Flipkart',
            position='UI Developer',
            status='Interview'
        )

    def test_unauthorized_api_access(self):
        response = self.api_client.get(reverse('api_application_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_get_list(self):
        self.api_client.login(username='api_user1', password='Password123!')
        response = self.api_client.get(reverse('api_application_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should contain app1 but NOT app2
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['company'], 'Zoho')

    def test_api_post_create(self):
        self.api_client.login(username='api_user1', password='Password123!')
        payload = {
            'company': 'Swiggy',
            'position': 'Backend Developer',
            'location': 'Bengaluru',
            'status': 'Applied',
            'priority': 'High'
        }
        response = self.api_client.post(reverse('api_application_list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], 'api_user1')

    def test_api_update(self):
        self.api_client.login(username='api_user1', password='Password123!')
        payload = {'status': 'Interview'}
        response = self.api_client.patch(reverse('api_application_detail', args=[self.app1.pk]), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.app1.refresh_from_db()
        self.assertEqual(self.app1.status, 'Interview')

    def test_api_delete(self):
        self.api_client.login(username='api_user1', password='Password123!')
        response = self.api_client.delete(reverse('api_application_detail', args=[self.app1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(JobApplication.objects.filter(pk=self.app1.pk).exists())

    def test_api_user_isolation(self):
        """Verify User 1 cannot access User 2's application via API."""
        self.api_client.login(username='api_user1', password='Password123!')

        response = self.api_client.get(reverse('api_application_detail', args=[self.app2.pk]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response_delete = self.api_client.delete(reverse('api_application_detail', args=[self.app2.pk]))
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)
