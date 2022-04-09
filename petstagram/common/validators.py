from django.core.exceptions import ValidationError


def contain_only_letters_validator(value):
    for char in value:
        if not char.isalpha():
            raise ValidationError('Name must contain only letters!')


def validate_image(value, PHOTO_MAX_SIZE=5):
    filesize = value.file.size
    if filesize > PHOTO_MAX_SIZE * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(PHOTO_MAX_SIZE))
