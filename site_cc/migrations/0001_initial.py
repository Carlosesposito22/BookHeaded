# Generated by Django 5.1 on 2024-09-19 19:42

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
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=3, unique=True)),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Clube',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=255)),
                ('modalidade', models.CharField(choices=[('N', '-'), ('P', 'Presencial'), ('O', 'Online'), ('H', 'Híbrido')], default='N', max_length=1)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('avaliacoes', models.IntegerField(blank=True, default=0, null=True)),
                ('livroAtual', models.CharField(blank=True, default='Sem livro definido', max_length=255, null=True)),
                ('numeroMembros', models.IntegerField(blank=True, default=1, null=True)),
                ('privado', models.BooleanField(default=False)),
                ('favoritado', models.BooleanField(default=False)),
                ('dataDeCriacao', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='site_cc.categoria')),
                ('moderador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
