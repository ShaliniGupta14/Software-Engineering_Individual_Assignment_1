import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


class QuestionModelTests(TestCase):

    def test_question_string_representation(self):
        question = Question(
            question_text="What is your favorite language?",
            pub_date=timezone.now(),
        )
        self.assertEqual(str(question), "What is your favorite language?")

    def test_recently_published_question(self):
        question = Question(
            question_text="Recent question",
            pub_date=timezone.now() - datetime.timedelta(hours=12),
        )
        self.assertTrue(question.was_published_recently())

    def test_old_question(self):
        question = Question(
            question_text="Old question",
            pub_date=timezone.now() - datetime.timedelta(days=2),
        )
        self.assertFalse(question.was_published_recently())

    def test_future_question(self):
        question = Question(
            question_text="Future question",
            pub_date=timezone.now() + datetime.timedelta(days=2),
        )
        self.assertTrue(question.was_published_recently())


class ChoiceModelTests(TestCase):

    def setUp(self):
        self.question = Question.objects.create(
            question_text="Favorite language?",
            pub_date=timezone.now(),
        )

    def test_choice_string_representation(self):
        choice = Choice.objects.create(
            question=self.question,
            choice_text="Python",
        )
        self.assertEqual(str(choice), "Python")

    def test_choice_default_votes(self):
        choice = Choice.objects.create(
            question=self.question,
            choice_text="Python",
        )
        self.assertEqual(choice.votes, 0)

    def test_choice_belongs_to_question(self):
        choice = Choice.objects.create(
            question=self.question,
            choice_text="Java",
        )
        self.assertEqual(choice.question, self.question)


class PollsViewTests(TestCase):

    def setUp(self):
        self.question = Question.objects.create(
            question_text="What is your favorite language?",
            pub_date=timezone.now(),
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Python",
        )

    def test_index_view(self):
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "What is your favorite language?",
        )

    def test_index_displays_latest_five_questions(self):
        for i in range(6):
            Question.objects.create(
                question_text=f"Question {i}",
                pub_date=timezone.now() + datetime.timedelta(minutes=i + 1),
            )

        response = self.client.get(reverse("polls:index"))

        self.assertEqual(
            len(response.context["latest_question_list"]),
            5,
        )

    def test_detail_view(self):
        response = self.client.get(reverse("polls:detail", args=[self.question.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")

    def test_results_view(self):
        response = self.client.get(reverse("polls:results", args=[self.question.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")

    def test_vote_success(self):
        response = self.client.post(
            reverse("polls:vote", args=[self.question.id]),
            {"choice": self.choice.id},
        )

        self.assertRedirects(
            response,
            reverse("polls:results", args=[self.question.id]),
        )

        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)

    def test_vote_without_choice(self):
        response = self.client.post(
            reverse("polls:vote", args=[self.question.id]),
            {},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["error_message"],
            "You didn't select a choice.",
        )

        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 0)

    def test_vote_invalid_choice(self):
        response = self.client.post(
            reverse("polls:vote", args=[self.question.id]),
            {"choice": 99999},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["error_message"],
            "You didn't select a choice.",
        )

        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 0)

    def test_invalid_question_returns_404(self):
        response = self.client.get(reverse("polls:detail", args=[99999]))

        self.assertEqual(response.status_code, 404)

    def test_vote_invalid_question_returns_404(self):
        response = self.client.post(
            reverse("polls:vote", args=[99999]),
            {"choice": self.choice.id},
        )

        self.assertEqual(response.status_code, 404)
