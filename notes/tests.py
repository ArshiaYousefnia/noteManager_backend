from django.contrib.auth import get_user_model
from django.test import TestCase

from notes.models import Note
from notes.serializers import NoteSerializer

User = get_user_model()

class NoteSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="abcd123", email="email@email.com", password="djksldksld")

    def test_data_serializer(self):
        data = {
            "content": "test md\n### title"
        }
        serilaizer = NoteSerializer(user=self.user, data=data)

        self.assertEqual(serilaizer.is_valid(), True)

    def test_serializer_save(self):
        data = {
            "content": "test md\n### title"
        }

        serializer = NoteSerializer(user=self.user, data=data)
        serializer.is_valid()
        serializer.save()

        data = serializer.data

        self.assertTrue(Note.objects.filter(uuid=data['uuid'], user=self.user).exists())


