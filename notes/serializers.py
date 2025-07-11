from rest_framework import serializers

from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('uuid', 'content', 'created_at', 'updated_at')
        read_only_fields = ('uuid', 'created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NoteSerializer, self).__init__(*args, **kwargs)


    def create(self, validated_data):
        note = Note.objects.create(user=self.user, **validated_data)

        return note