from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from library.models import Member, Book, Loan, Author


class LibraryFeatureTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='johndoe', email='johndoe@example.com', password='password')
        self.member = Member.objects.create(user=self.user)
        self.author = Author.objects.create(name='Author A')
        self.book = Book.objects.create(title='Book A', author=self.author, available_copies=3)

    def test_extend_due_date_success(self):
        loan = Loan.objects.create(member=self.member, book=self.book)
        url = f'/api/loans/{loan.id}/extend_due_date/'
        response = self.client.post(url, {'additional_days': 5}, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        loan.refresh_from_db()
        self.assertEqual(loan.due_date, timezone.now().date() + timedelta(days=19))  # 14 default + 5

    def test_extend_due_date_invalid_input(self):
        loan = Loan.objects.create(member=self.member, book=self.book)
        url = f'/api/loans/{loan.id}/extend_due_date/'
        response = self.client.post(url, {'additional_days': -3}, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid number of days', response.json()['error'])

    def test_extend_due_date_overdue(self):
        loan = Loan.objects.create(
            member=self.member,
            book=self.book,
            due_date=timezone.now().date() - timedelta(days=1)
        )
        url = f'/api/loans/{loan.id}/extend_due_date/'
        response = self.client.post(url, {'additional_days': 5}, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Cannot extended overdue loan', response.json()['error'])

    def test_top_active_members_endpoint(self):
        member2_user = User.objects.create_user(username='janedoe', email='janedoe@example.com', password='password')
        member2 = Member.objects.create(user=member2_user)

        for _ in range(3):
            Loan.objects.create(book=self.book, member=self.member)
        for _ in range(2):
            Loan.objects.create(book=self.book, member=member2)

        url = reverse('top-active-members')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['username'], 'johndoe')
        self.assertEqual(response.json()[0]['active_loans'], 3)
