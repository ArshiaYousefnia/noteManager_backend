from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from notes.models import Note
from notes.serializers import NoteSerializer


class NoteListView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [AllowAny()]

    def get(self, request):
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, user=request.user, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NoteSerializer(user=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)

        note = serializer.save()

        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)

class NoteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        note = Note.objects.get(user=request.user, uuid=uuid)

        serializer = NoteSerializer(note, user=request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, uuid):
        note = Note.objects.get(user=request.user, uuid=uuid)

        serializer = NoteSerializer(note, user=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, uuid):
        note = Note.objects.get(user=request.user, uuid=uuid)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)