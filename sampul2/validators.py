from django.core.exceptions import ValidationError
import magic


def validate_pdf(value):
    if not magic.from_buffer(value.read(), mime=True) == 'application/pdf':
        raise ValidationError("File harus dalam format PDF.")
