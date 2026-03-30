from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_room_participants_and_unique_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='read_by',
            field=models.ManyToManyField(blank=True, related_name='read_messages', to='models.user'),
        ),
    ]
