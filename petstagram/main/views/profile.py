# from django.shortcuts import render, redirect
#
# def show_profile(request):
#     profile = get_profile()
#     pets = Pet.objects.all()
#     pet_photos = PetPhoto.objects.filter(tagged_pets__user=profile).distinct()
#     total_images = len(pet_photos)
#     total_likes = sum(pp.likes for pp in pet_photos)
#
#     context = {
#         'profile': profile,
#         'pets': pets,
#         'total_images': total_images,
#         'total_likes': total_likes,
#     }
#     return render(request, 'main/profile_details.html', context)

#
# def crud_profile(request, form_name, redirect_to, instance, template_name):
#     if request.method == "POST":
#         profile_form = form_name(request.POST, instance=instance)
#         if profile_form.is_valid():
#             profile_form.save()
#             return redirect(redirect_to)
#     else:
#         profile_form = form_name(instance=instance)
#
#     context = {
#         'profile_form': profile_form
#     }
#     return render(request, template_name, context)
#
#
# def create_profile(request):
#     return crud_profile(request, ProfileForm, 'home', Profile(), 'main/profile_create.html')
#
#
# def edit_profile(request):
#     return crud_profile(request, EditProfileForm, 'profile', get_profile(), 'main/profile_edit.html')
#
#
# def delete_profile(request):
#     return crud_profile(request, DeleteProfileForm, 'home', get_profile(), 'main/profile_delete.html')
import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from petstagram.accounts.models import Profile
from petstagram.common.helpers import BootstrapFormMixin
from django import forms

from petstagram.main.models import PetPhoto, Pet


class ProfileForm(BootstrapFormMixin, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.fields['first_name'].label = 'First Name:'
        self.fields['last_name'].label = 'Last Name:'
        self.fields['picture'].label = 'Link to Profile Picture:'

    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
    )
    picture = forms.URLField()
    # date_of_birth = forms.DateField()
    # description = forms.Textarea()
    # email = forms.EmailInput()
    # gender = forms.Select(
    #     choices=Profile.GENDERS,
    # )

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            picture=self.cleaned_data['picture'],
            # date_of_birth=self.cleaned_data['date_of_birth'],
            # last_name=self.cleaned_data['last_name'],
            # last_name=self.cleaned_data['last_name'],
            user=user,
        )

        if commit:
            profile.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2','first_name', 'last_name', 'picture')
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            ),
            'picture': forms.TextInput(
                attrs={
                    'placeholder': 'Enter URL',
                }
            ),
        }


class EditProfileForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.initial['gender'] = Profile.DO_NOT_SHOW
        self.fields['first_name'].label = 'First Name:'
        self.fields['last_name'].label = 'Last Name:'
        self.fields['picture'].label = 'Link to Profile Picture:'
        self.fields['date_of_birth'].label = 'Date of Birth:'
        self.fields['email'].label = 'Email:'
        self.fields['gender'].label = 'Gender:'
        self.fields['description'].label = 'Description:'

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.SelectDateWidget(
                years=range(datetime.datetime.now().year, 1919, -1),
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter email'
                }
            ),
            'gender': forms.Select(
                choices=Profile.GENDERS,
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Enter description',
                },
            )
        }


class DeleteProfileForm(forms.ModelForm):
    # overwrite save() from crud_profile() FBV
    def save(self, commit=True):
        pets = list(self.instance.pet_set.all())
        # Profile.objects.get(user_id=)
        # user_id = self.instance.pk
        PetPhoto.objects.filter(tagged_pets__user_id=pets).delete()
        self.instance.delete()
        return self.instance

    class Meta:
        model = Profile
        fields = ()
