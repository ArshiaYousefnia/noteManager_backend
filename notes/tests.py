import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from notes.models import Note
from notes.serializers import NoteSerializer
from notes.views import NoteListView, NoteDetailView

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

    def test_serializer_partial_update(self):
        self.note = Note.objects.create(user=self.user, content="test md\n### title")
        data = {
            "content": "new md"
        }

        serializer = NoteSerializer(user=self.user, instance=self.note, data=data, partial=True)

        serializer.is_valid()
        serializer.save()

        self.assertEqual(self.note.content, data['content'])

class NoteListViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.location = "/api/notes/"
        self.user = User.objects.create_user(username="abcd123", email="email@email.com", password="djksldksld")
        self.note_1 = Note.objects.create(user=self.user, content="test md\n### title 1")
        self.note_2 = Note.objects.create(user=self.user, content="test md2\n### title 2")

    def test_list_get(self):
        request = self.factory.get(self.location)
        force_authenticate(request, self.user)

        response = NoteListView.as_view()(request)
        response.render()
        data = json.loads(response.content)

        serializer = NoteSerializer(Note.objects.filter(user=self.user), user=self.user, many=True)

        self.assertEqual(serializer.data, data, msg=serializer.data)

    def test_note_create(self):
        data = {
            "content": "test_note_create_md"
        }

        request = self.factory.post(self.location, data, content_type="application/json")
        force_authenticate(request, self.user)

        NoteListView.as_view()(request)

        self.assertTrue(Note.objects.filter(content=data['content'], user=self.user).exists())


class NoteDetailViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.location = "/api/notes/{uuid}"
        self.user = User.objects.create_user(username="abcd123", email="email@email.com", password="djksldksld")
        self.note_1 = Note.objects.create(user=self.user, content="test md\n### title 1")

    def test_detail_get(self):
        request = self.factory.get(self.location.format(uuid=self.note_1.uuid))
        force_authenticate(request, self.user)

        response = NoteDetailView.as_view()(request, uuid=self.note_1.uuid)
        response.render()
        response_data = json.loads(response.content)
        serializer_data = NoteSerializer(Note.objects.get(user=self.user), user=self.user).data

        self.assertEqual(response_data, serializer_data, msg=response_data)

    def test_detail_update(self):
        data = {"content": "new md"}
        request = self.factory.patch(self.location.format(uuid=self.note_1.uuid), data=data)
        force_authenticate(request, self.user)

        response = NoteDetailView.as_view()(request, uuid=self.note_1.uuid)
        response.render()
        response_data = json.loads(response.content)

        instance = Note.objects.get(uuid=self.note_1.uuid, user=self.user)
        serializer_data = NoteSerializer(user=self.user, instance=instance).data

        self.assertEqual(response_data, serializer_data, msg=response_data)

    def test_detail_delete(self):
        request = self.factory.delete(self.location.format(uuid=self.note_1.uuid))
        force_authenticate(request, self.user)

        NoteDetailView.as_view()(request, uuid=self.note_1.uuid)

        self.assertFalse(Note.objects.filter(uuid=self.note_1.uuid, user=self.user).exists())
