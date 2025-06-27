from django.test import TestCase, Client
from django.urls import reverse
from .models import Answer, Tag, AnswerTag

# Create your tests here.


class ModelTests(TestCase):
    def setUp(self):
        self.answer = Answer.objects.create(
            value="TEST", language="pl", type="definicja", content="Test content"
        )

    def test_answer_creation(self):
        self.assertEqual(Answer.objects.count(), 1)

    def test_tag_uniqueness(self):
        tag1 = Tag.objects.create(
            name="tag1", value="TEST", language="pl", type="definicja")
        with self.assertRaises(Exception):
            Tag.objects.create(name="tag1", value="TEST",
                               language="pl", type="definicja")

    def test_answer_tag_uniqueness(self):
        tag = Tag.objects.create(
            name="tag2", value="TEST", language="pl", type="definicja")
        at1 = AnswerTag.objects.create(answer=self.answer, tag=tag)
        with self.assertRaises(Exception):
            AnswerTag.objects.create(answer=self.answer, tag=tag)


class AnswerDetailViewTests(TestCase):
    def setUp(self):
        self.answer = Answer.objects.create(
            value="TEST", language="pl", type="definicja", content="Test content"
        )
        self.url = reverse("answer_detail", args=[self.answer.pk])
        self.client = Client()

    def test_get_answer_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.answer.content)

    def test_post_add_tag_valid(self):
        response = self.client.post(
            self.url, {"add_new_tag": "1", "tag_name": "nowy", "category": "test"})
        self.assertEqual(response.status_code, 302)  # Redirect
        tag_exists = Tag.objects.filter(name="nowy").exists()
        self.assertTrue(tag_exists)

    def test_post_add_tag_empty_name(self):
        response = self.client.post(
            self.url, {"add_new_tag": "1", "tag_name": "", "category": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nazwa tagu nie może być pusta.")
