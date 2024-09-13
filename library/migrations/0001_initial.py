# Generated by Django 4.2.16 on 2024-09-13 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('author', models.CharField(max_length=30)),
                ('publisher', models.CharField(max_length=50)),
                ('price', models.CharField(max_length=50)),
                ('category', models.CharField(blank=True, choices=[('Kids & Teens', 'Kids'), ('Science Fiction', 'Sci-Fi'), ('History', 'HS'), ('Religion', 'RG'), ('Health & Fitness', 'HF')], max_length=20)),
                ('is_available', models.BooleanField(default=True)),
                ('borrow_date', models.DateField(blank=True, null=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('book_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('borrowed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Borrowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(auto_now_add=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('fee', models.DecimalField(blank=True, decimal_places=4, max_digits=7, null=True)),
                ('is_returned', models.BooleanField(default=False)),
                ('is_late', models.BooleanField(default=False)),
                ('is_damaged', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
        ),
    ]
