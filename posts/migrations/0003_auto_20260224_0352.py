from django.db import migrations

def populate_status(apps, schemaeditor):
    entries = {
        "published": "A post available for all to view",
        "draft": "A post only visible to the author",
        "archived": "An older post visible only to the logged user"
    }
    Status = apps.get_model("posts", "Status")
    for key, value in entries.items():
        status_obj = Status(name=key, description=value)
        status_obj.save()

class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0002_status_alter_post_author'),
    ]
    operations = [
        migrations.RunPython(populate_status)
    ]
