from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_financial_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='name',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
    ]
