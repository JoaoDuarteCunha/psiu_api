# Generated by Django 5.1.3 on 2024-11-30 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psiuApiApp', '0004_conhecerpessoas_estudos_extracurriculares_liga_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='criador_id',
            field=models.TextField(db_column='criador_id'),
        ),
    ]
