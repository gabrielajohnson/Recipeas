# Generated by Django 3.0.3 on 2020-05-03 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_recipe_total_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='inspiration',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='recipe_inspiration', to='recipes.Recipe'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=0, upload_to='static/images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
