# Generated by Django 3.0.3 on 2020-05-03 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_auto_20200503_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='inspiration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipe_inspiration', to='recipes.Recipe'),
        ),
    ]