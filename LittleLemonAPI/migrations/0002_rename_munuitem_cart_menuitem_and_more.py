# Generated by Django 5.0.1 on 2024-02-08 10:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='munuitem',
            new_name='menuitem',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='munuitem',
            new_name='menuitem',
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('menuitem', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together={('order', 'menuitem')},
        ),
    ]
