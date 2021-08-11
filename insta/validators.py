from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > 10 * 1024 * 1024:  # 10MB
        raise ValidationError("The maximum file size is 10MB")
    else:
        return value
