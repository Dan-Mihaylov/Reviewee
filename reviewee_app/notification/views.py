from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic as views
from .models import Notification


class NotificationListView(LoginRequiredMixin, views.ListView):
    template_name = 'notification/notification-list.html'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-pk')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.request.user
        context['filter'] = self.request.GET.get('filter', '')
        # context['object_list'] = []
        return context
