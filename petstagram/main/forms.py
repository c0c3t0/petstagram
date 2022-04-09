import datetime

from django import forms

from petstagram.common.helpers import BootstrapFormMixin, DisabledFieldsFormMixin
from petstagram.main.models import Pet, PetPhoto


class CreatePetForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()
        self.fields['name'].label = 'Pet Name:'
        self.fields['pet_type'].label = 'Type:'
        self.fields['date_of_birth'].label = 'Day of Birth:'

    def save(self, commit=True):
        pet = super().save(commit=False)

        pet.user = self.user
        if commit:
            pet.save()

        return pet

    class Meta:
        model = Pet
        fields = ('name', 'pet_type', 'date_of_birth')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'label': 'Pet name',
                    'placeholder': 'Enter pet name',
                }
            ),
            'pet_type': forms.Select(
                choices=Pet.ANIMAL_TYPES,
            ),
            'date_of_birth': forms.SelectDateWidget(
                years=range(datetime.datetime.now().year, 1919, -1)
            ),
        }


class EditPetForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Pet
        fields = ('name', 'pet_type', 'date_of_birth')
        widgets = {
            'date_of_birth': forms.SelectDateWidget(
                years=range(datetime.datetime.now().year, 1919, -1),
            ),
        }


class DeletePetForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()
        self.fields['name'].label = 'Pet Name'
        self.fields['pet_type'].label = 'Type'
        self.fields['date_of_birth'].label = 'Date of Birth'

    def save(self, commit=True):
        Pet.objects.get(pk=self.instance.pk).delete()
        return self.instance

    class Meta:
        model = Pet
        fields = ('name', 'pet_type', 'date_of_birth')
        widgets = {
            'date_of_birth': forms.SelectDateWidget(
                years=range(datetime.datetime.now().year, 1919, -1),
            ),
        }


class CreatePetPhotoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._init_bootstrap_form_controls()
        self.fields['photo'].label = 'Pet Image:'
        self.fields['description'].label = 'Description:'
        self.fields['tagged_pets'].label = 'Tag Pets:'

    #
    # def save(self, commit=True):
    #     pet_photo = super().save(commit=False)
    #
    #     pet_photo.user = self.user
    #     if commit:
    #         pet_photo.save()
    #
    #     return pet_photo

    class Meta:
        model = PetPhoto
        fields = ('photo', 'description', 'tagged_pets')
        widgets = {
            'photo': forms.FileInput(
                attrs={
                    'class': 'form-control-file'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter description',
                    'rows': 3,
                },
            ),
            'tagged_pets': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            )
        }


class EditPetPhotoForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.fields['tagged_pets'].label = 'Tag Pets'

    class Meta:
        model = PetPhoto
        fields = ('description', 'tagged_pets')
        # widgets = {
        #     # 'description'
        # }
