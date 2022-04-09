from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from petstagram.main.forms import CreatePetPhotoForm, EditPetPhotoForm
from petstagram.main.models import PetPhoto


class ShowPhotoDetailsView(DetailView):
    model = PetPhoto
    template_name = 'main/photo_details.html'
    context_object_name = 'pet_photo'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('tagged_pets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['is_owner'] = self.object.user == self.request.user
        context['is_anonymous'] = self.object.user == self.request.user

        return context


class CreatePhotoView(LoginRequiredMixin, CreateView):
    model = PetPhoto
    form_class = CreatePetPhotoForm
    template_name = 'main/photo_create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs


class EditPhotoView(UpdateView):
    model = PetPhoto
    form_class = EditPetPhotoForm
    template_name = 'main/photo_edit.html'

    def get_success_url(self):
        return reverse_lazy('show photo details', kwargs={'pk': self.object.id})


class DeletePhotoView(DeleteView):
    model = PetPhoto
    template_name = 'main/photo_delete.html'
    success_url = reverse_lazy('dashboard')


# def show_photo_details(request, pk):
#     pet_photo = PetPhoto.objects.prefetch_related('tagged_pets').get(pk=pk)
#     context = {
#         'pet_photo': pet_photo,
#         # 'pet': Pet.objects.get(pk=pk),
#     }
#     return render(request, 'main/photo_details.html', context)


def like_pet_photo(request, pk):
    pet_photo = PetPhoto.objects.get(pk=pk)
    pet_photo.likes += 1
    pet_photo.save()

    return redirect('show photo details', pk)

# def crud_pet_photo(request, form_name, redirect_to, instance, template_name):
#     if request.method == "POST":
#         pet_photo_form = form_name(request.POST, request.FILES, instance=instance)
#         if pet_photo_form.is_valid():
#             pet_photo_form.save()
#             return redirect(redirect_to)
#     else:
#         pet_photo_form = form_name(instance=instance)
#
#     context = {
#         'pet_photo_form': pet_photo_form
#     }
#
#     return render(request, template_name, context)


# def add_photo(request):
#     if request.method == "POST":
#         pet_photo_form = CreatePetPhotoForm(request.POST, request.FILES)
#         if pet_photo_form.is_valid():
#             pet_photo_form.save()
#             return redirect('dashboard')
#     else:
#         pet_photo_form = CreatePetPhotoForm()
#
#     context = {
#         'pet_photo_form': pet_photo_form
#     }
#
#     return render(request, 'main/photo_create.html', context)
# return crud_pet_photo(request, CreatePetPhotoForm, 'dashboard', PetPhoto(), 'main/photo_create.html')


# def edit_photo(request, pk):
#     pet_photo = PetPhoto.objects.get(pk=pk)
#     if request.method == "POST":
#         pet_photo_form = EditPetPhotoForm(request.POST, instance=pet_photo)
#         if pet_photo_form.is_valid():
#             pet_photo_form.save()
#             return redirect('show photo details', pet_photo.pk)
#
#     else:
#         pet_photo_form = EditPetPhotoForm(instance=pet_photo)
#
#     context = {
#         'pet_photo_form': pet_photo_form,
#         'pet_photo': pet_photo
#     }
#
#     return render(request, 'main/photo_edit.html', context)


# def delete_photo(request, pk):
#     pet_photo = PetPhoto.objects.get(pk=pk)
#     pet_photo.delete()
#     return redirect('dashboard')
