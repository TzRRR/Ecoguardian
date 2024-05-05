from django.test import TestCase
from django import forms
from ecoguardian.models import User, IncidentCategory
from ecoguardian.forms import IncidentReportForm
from ecoguardian.views import MainView, IncidentReportView

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(username="testuser", password="password", is_admin=False)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password, "password")
        self.assertFalse(user.is_admin)

class IncidentCategoryModelTest(TestCase):
    def test_incident_category_creation(self):
        category = IncidentCategory.objects.create(name=IncidentCategory.AIR_POLLUTION)
        self.assertEqual(category.name, IncidentCategory.AIR_POLLUTION)

class IncidentReportFormTest(TestCase):
    def test_form_fields(self):
        form = IncidentReportForm()
        self.assertIn('description', form.fields)
        self.assertIn('location', form.fields)
        self.assertIn('date', form.fields)
        self.assertIn('incident_categories', form.fields)
        self.assertIn('evidence', form.fields)
        self.assertTrue(isinstance(form.fields['date'].widget, forms.SelectDateWidget))

    def test_incident_report_form_valid(self):
        form_data = {
            'description': 'Test description',
            'location': 'Test location',
            'date': '2023-01-01',
            'incident_categories': [IncidentCategory.AIR_POLLUTION],
            'evidence': None
        }
        form = IncidentReportForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_incident_report_form_invalid(self):
        form_data = {
            'description': '',
            'location': 'Test location',
            'date': '2023-01-01',
            'incident_categories': [IncidentCategory.AIR_POLLUTION],
            'evidence': None
        }
        form = IncidentReportForm(data=form_data)
        self.assertFalse(form.is_valid())

class MainViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/ecoguardian/main/')
        self.assertEqual(response.status_code, 200)

class IncidentReportViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/ecoguardian/incident_report/')
        self.assertEqual(response.status_code, 200)