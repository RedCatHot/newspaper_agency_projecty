from django.test import Client, TestCase
from django.urls import reverse
from agency.forms import (RedactorCreationForm,
                          NewspaperForm,
                          RedactorSearchForm,
                          NewspaperSearchForm,
                          TopicSearchForm)
from agency.models import Topic, Redactor, Newspaper
from django.contrib.auth import get_user_model


class ModelTestCase(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            email="test@example.com"
        )
        self.redactor = Redactor.objects.create(
            username="redactor",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            years_of_experience=5
        )
        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            content="Some content",
            topic=self.topic
        )
        self.newspaper.publishers.add(self.user)

    def test_topic_model(self):
        self.assertEqual(str(self.topic), "Test Topic")

    def test_redactor_model(self):
        self.assertEqual(str(self.redactor), "redactor (John Doe)")

    def test_newspaper_model(self):
        self.assertEqual(str(self.newspaper), "Test Newspaper")


class FormTestCase(TestCase):
    def test_redactor_creation_form(self):
        form_data = {
            "username": "new_user",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
            "email": "new_user@example.com",
            "years_of_experience": 3,
            "first_name": "New",
            "last_name": "User"
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_newspaper_form(self):
        topic = Topic.objects.create(name="Test Topic")
        form_data = {
            "title": "Test Newspaper",
            "content": "Some content",
            "topic": topic.id,
        }
        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_redactor_search_form(self):
        form_data = {
            "last_name": "Doe"
        }
        form = RedactorSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_newspaper_search_form(self):
        form_data = {
            "title": "Test"
        }
        form = NewspaperSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_topic_search_form(self):
        form_data = {
            "name": "Test"
        }
        form = TopicSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.topic = Topic.objects.create(name="Test Topic")
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            email="test@example.com"
        )
        self.redactor = Redactor.objects.create(
            username="redactor",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            years_of_experience=5
        )
        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            content="Some content",
            topic=self.topic
        )
        self.newspaper.publishers.add(self.user)

    def test_index_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(reverse("newspaper:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Newspaper Agency")
        self.assertEqual(response.context["num_topics"], 1)
        self.assertEqual(response.context["num_newspapers"], 1)
        self.assertEqual(response.context["num_redactors"], 2)
        self.assertEqual(self.client.session["num_visits"], 1)

    def test_topic_list_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(reverse("newspaper:topic-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Topic")

    def test_topic_create_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(reverse("newspaper:topic-create"))
        self.assertEqual(response.status_code, 200)

    def test_topic_update_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(
            reverse("newspaper:topic-update", kwargs={"pk": self.topic.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_topic_delete_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(
            reverse("newspaper:topic-delete", kwargs={"pk": self.topic.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_newspaper_list_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(reverse("newspaper:newspaper-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Newspaper")

    def test_newspaper_detail_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(
            reverse("newspaper:newspaper-detail", kwargs={"pk": self.newspaper.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Newspaper")

    def test_newspaper_create_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(reverse("newspaper:newspaper-create"))
        self.assertEqual(response.status_code, 200)

    def test_newspaper_update_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(
            reverse("newspaper:newspaper-update", kwargs={"pk": self.newspaper.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_redactor_list_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(reverse("newspaper:redactor-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John")

    def test_redactor_detail_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(
            reverse("newspaper:redactor-detail", kwargs={"pk": self.redactor.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")

    def test_redactor_create_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(reverse("newspaper:redactor-create"))
        self.assertEqual(response.status_code, 200)

    def test_redactor_update_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(
            reverse("newspaper:redactor-update", kwargs={"pk": self.redactor.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_redactor_delete_view(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(
            reverse("newspaper:redactor-delete", kwargs={"pk": self.redactor.pk})
        )
        self.assertEqual(response.status_code, 200)
