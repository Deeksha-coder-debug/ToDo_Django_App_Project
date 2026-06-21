from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task


class TaskSecurityTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user('alice', 'a@test.com', 'ComplexPass123!')
        self.bob = User.objects.create_user('bob', 'b@test.com', 'ComplexPass123!')
        self.alice_task = Task.objects.create(
            user=self.alice,
            title="Alice's Secret Task",
            priority='H'
        )
        self.client = Client()

    def test_unauthenticated_user_redirected(self):
        response = self.client.get(reverse('application:index'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_user_sees_only_own_tasks(self):
        self.client.login(username='alice', password='ComplexPass123!')
        Task.objects.create(user=self.bob, title="Bob's Task", priority='M')
        response = self.client.get(reverse('application:index'))
        self.assertContains(response, "Alice's Secret Task")
        self.assertNotContains(response, "Bob's Task")

    def test_user_cannot_edit_others_task(self):
        self.client.login(username='bob', password='ComplexPass123!')
        response = self.client.get(reverse('application:edit_task', args=[self.alice_task.id]))
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_delete_others_task(self):
        self.client.login(username='bob', password='ComplexPass123!')
        response = self.client.get(reverse('application:delete_task', args=[self.alice_task.id]))
        self.assertEqual(response.status_code, 403)

    def test_task_creation_assigns_user(self):
        self.client.login(username='alice', password='ComplexPass123!')
        self.client.post(reverse('application:add_task'), {
            'title': 'New Task',
            'priority': 'M',
            'category': 'Work'
        })
        task = Task.objects.latest('id')
        self.assertEqual(task.user, self.alice)

    def test_past_due_date_rejected(self):
        self.client.login(username='alice', password='ComplexPass123!')
        response = self.client.post(reverse('application:add_task'), {
            'title': 'Bad Task',
            'due_date': '2020-01-01',
            'priority': 'M',
            'category': 'Work'
        })
        self.assertEqual(response.status_code, 200)  # Re-renders form with error
        self.assertFalse(Task.objects.filter(title='Bad Task').exists())


# from django.test import TestCase

# Create your tests here.
