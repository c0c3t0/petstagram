from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from petstagram.accounts.forms import ProfileForm, EditProfileForm, DeleteProfileForm
from petstagram.accounts.models import Profile
from petstagram.common.helpers import RedirectToDashboardMixin
from petstagram.main.models import Pet, PetPhoto


class UserRegisterView(RedirectToDashboardMixin, CreateView):
    form_class = ProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('home')


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login_page.html'

    def get_success_url(self):
        return reverse_lazy('home')


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pets = list(Pet.objects.filter(user_id=self.object.user_id))
        pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets).distinct()

        total_images = len(pet_photos)
        total_likes = sum(pp.likes for pp in pet_photos)

        context.update({
            'pets': pets,
            'total_images': total_images,
            'total_likes': total_likes,
            'is_owner': self.object.user_id == self.request.user.id
        })
        return context


class EditProfileView(UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'accounts/profile_edit.html'

    def get_success_url(self):
        profile_id = self.kwargs['pk']
        return reverse_lazy('profile details', kwargs={'pk': profile_id})


class DeleteProfileView(DeleteView):
    model = Profile
    form_class = DeleteProfileForm
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('home')


# def edit_profile(request):
#     return crud_profile(request, EditProfileForm, 'profile', get_profile(), 'main/profile_edit.html')

class ChangeUserPasswordView:
    pass
