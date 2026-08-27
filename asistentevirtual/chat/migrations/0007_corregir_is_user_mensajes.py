from django.db import migrations

def corregir_is_user(apps, schema_editor):
    Message = apps.get_model('chat', 'Message')
    ai_prefixes = ('¡', 'lo siento', 'vaya,', 'gojo está', 'genial:', 'error:', '😓', 'hola! ¿cómo va todo?', 'hola! ¿qué tal?', 'hola! ¡aquí')
    ai_keywords = ('técnica infinita', 'hechicero más fuerte', 'revisa los logs', 'infinito (spoiler', 'mi técnica', 'agendado tu recordatorio', 'recordatorio guardado', 'estoy muy feliz de verte')

    for m in Message.objects.all():
        c_lower = (m.content or "").strip().lower()
        es_ai = any(c_lower.startswith(p) for p in ai_prefixes) or any(k in c_lower for k in ai_keywords)
        deberia_ser_user = not es_ai
        if m.is_user != deberia_ser_user:
            m.is_user = deberia_ser_user
            m.save()

def revertir_corregir_is_user(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_asistenteconfig_personalidad_asistenteconfig_user_and_more'),
    ]

    operations = [
        migrations.RunPython(corregir_is_user, reverse_code=revertir_corregir_is_user),
    ]
