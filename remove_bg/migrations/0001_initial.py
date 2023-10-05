# Generated by Django 4.2.2 on 2023-10-05 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='images')),
                ('rmbg_img', models.ImageField(blank=True, upload_to='images_rmbg')),
                ('is_downloaded', models.BooleanField(default=False)),
            ],
        ),
    ]
