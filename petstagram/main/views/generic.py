from django.views.generic import TemplateView, ListView

from petstagram.common.helpers import RedirectToDashboardMixin
from petstagram.main.models import PetPhoto


class HomeView(RedirectToDashboardMixin, TemplateView):
    template_name = 'accounts/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['hide_nav_buttons'] = True
        return context


class DashboardView(ListView):
    model = PetPhoto
    template_name = 'main/dashboard.html'
    context_object_name = 'pet_photos'

#
# def show_dashboard(request):
#     profile = get_profile()
#     pet_photos = set(PetPhoto.objects
#                      .prefetch_related('tagged_pets')
#                      .filter(tagged_pets__pets_owner=profile),
#                      )
#     context = {
#         'pet_photos': pet_photos,
#     }
#     return render(request, 'main/dashboard.html', context)
