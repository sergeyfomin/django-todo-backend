import django.test
import json

from datetime import datetime
from django.core.urlresolvers import reverse
from todo.models.todo import Todo
from todo.models.user import User


class MainTestCase(django.test.TestCase):

    def setUp(self):
        self.client = django.test.Client()

        self.user_1 = User.objects.create(
            username='test',
        )
        self.user_1.set_password('test')
        self.user_1.save()

        self.todo_1 = Todo.objects.create(
            user=self.user_1,
            is_done=False,
            description='descrp',
            created_at=datetime.now()
        )

        self.wrond_id = 987654321

    def login(self, login='test', password='test'):
        response = self.client.post(
            reverse('login'),
            data=json.dumps({
                'login': login,
                'password': password
            }),
            content_type='application/json',
        )

        return response
