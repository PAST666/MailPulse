# Generated by Django 5.1.7 on 2025-03-26 05:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_first_send', models.DateTimeField(verbose_name='Дата и время первой отправки')),
                ('time_of_last_send', models.DateTimeField(verbose_name='Дата и время последней отправки')),
                ('status', models.CharField(max_length=150, verbose_name='Статус')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mailings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='MailAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_attempt', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')),
                ('status', models.CharField(max_length=150, verbose_name='Статус')),
                ('answer', models.CharField(max_length=255, verbose_name='Ответ')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailings.mailing')),
            ],
            options={
                'verbose_name': 'Попытка рассылки',
                'verbose_name_plural': 'Попытки рассылки',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('message_text', models.CharField(max_length=255, verbose_name='Текст сообщения')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.AddField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailings.message'),
        ),
        migrations.CreateModel(
            name='MessageRecipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=150, unique=True, verbose_name='Почта')),
                ('name', models.CharField(max_length=150, verbose_name='ФИО')),
                ('middle_name', models.CharField(max_length=150, verbose_name='ФИО')),
                ('surname', models.CharField(max_length=150, verbose_name='ФИО')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipients', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Получатель',
                'verbose_name_plural': 'Получатели',
            },
        ),
        migrations.AddField(
            model_name='mailing',
            name='recipients',
            field=models.ManyToManyField(to='mailings.messagerecipient'),
        ),
    ]
