from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from telebot.base.models import UserLink
from telebot.logger.models import MessageLogRecord


class LoggerView(LoginRequiredMixin, ListView):
    template_name = 'telebot/logger.html'
    paginate_by = 100

    def get_queryset(self):
        chat_id = self.request.GET.get('chat_id')
        qs = MessageLogRecord.objects.order_by('-date')
        if chat_id:
            qs = qs.filter(link__chat_id=chat_id)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        chat_id = self.request.GET.get('chat_id')
        if chat_id:
            context['UserLink'] = UserLink.objects.filter(chat_id=chat_id).first()
        return context

