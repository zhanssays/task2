# Generated by Django 3.1.1 on 2020-09-05 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opponent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.user')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threads', to='chat.user')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.user')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.thread')),
            ],
        ),
    ]