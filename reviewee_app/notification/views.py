from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic as views
from django.db.models import Q
from .models import Notification


class NotificationListView(LoginRequiredMixin, views.ListView):
    template_name = 'notification/notification-list.html'

    def get_queryset(self):
        query = self.create_filter_query()
        return Notification.objects.filter(query).order_by('-pk')

    def create_filter_query(self):
        filter_info = self.request.GET.get('filter', '')
        if filter_info in ['', 'All']:
            return Q(user=self.request.user)
        return Q(user=self.request.user) & Q(type=filter_info)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.request.user
        context['filter'] = self.request.GET.get('filter', '')
        # context['object_list'] = []
        return context
