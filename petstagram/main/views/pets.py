from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from petstagram.main.forms import CreatePetForm, EditPetForm, DeletePetForm
from petstagram.main.models import Pet


class CreatePetView(CreateView):
    form_class = CreatePetForm
    template_name = 'main/pet_create.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditPetView(UpdateView):
    model = Pet
    form_class = EditPetForm
    template_name = 'main/pet_edit.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})


class DeletePetView(CreateView, DeleteView):
    model = Pet
    form_class = DeletePetForm
    template_name = 'main/pet_delete.html'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})

# def crud_pet(request, form_name, redirect_to, instance, template_name):
#     if request.method == "POST":
#         pet_form = form_name(request.POST, instance=instance)
#         if pet_form.is_valid():
#             pet_form.save()
#             return redirect(redirect_to)
#     else:
#         pet_form = form_name(instance=instance)
#
#     context = {
#         'pet_form': pet_form,
#         'pet': instance,
#     }
#     return render(request, template_name, context)


# def add_pet(request):
#     return crud_pet(request, CreatePetForm, 'profile', Pet(pets_owner=get_profile()), 'main/pet_create.html')
#
#
# def edit_pet(request, pk):
#     return crud_pet(request, EditPetForm, 'profile', Pet.objects.get(pk=pk), 'main/pet_edit.html')


# def delete_pet(request, pk):
#     return crud_pet(request, DeletePetForm, 'profile', Pet.objects.get(pk=pk), 'main/pet_delete.html')
