from django.contrib.auth import get_user_model
from django.db import models
from petstagram.common.validators import validate_image

UserModel = get_user_model()


class Pet(models.Model):
    NAME_MAX_LENGTH = 30

    CAT = 'Cat'
    DOG = 'Dog'
    BUNNY = 'Bunny'
    PARROT = 'Parrot'
    FISH = 'Fish'
    OTHER = 'Other'

    ANIMAL_TYPES = [(x, x) for x in (CAT, DOG, BUNNY, FISH, PARROT, OTHER)]

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
    )

    pet_type = models.CharField(
        max_length=max(len(x) for x, _ in ANIMAL_TYPES),
        choices=ANIMAL_TYPES,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ('user', 'name')


class PetPhoto(models.Model):
    PHOTO_MAX_SIZE = 5
    photo = models.ImageField(
        upload_to='images/',
        validators=[validate_image]
    )

    tagged_pets = models.ManyToManyField(
        Pet,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )

    likes = models.IntegerField(
        default=0,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
