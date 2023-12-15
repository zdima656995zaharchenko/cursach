from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Rate, ContactUs, Source
from .forms import SourceForm, ContactUsForm, RateForm
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseServerError
from django.views.generic.edit import FormView
from .forms import SupportForm, RateForm
from .forms import CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from .filters import RateFilter, SourceFilter
from django.db.models import QuerySet

class RateListView(FilterView):
    model = Rate
    template_name = 'rate_list.html'
    context_object_name = 'rates'
    paginate_by = 10
    filterset_class = RateFilter

    def get_queryset(self):
        return Rate.objects.all().order_by('buy', 'sell', 'currency')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['filter_params'] = "&".join(
            f"{key}={value}" for key, value in self.request.GET.items() if key != "page"
        )

        return context

    def my_view(request):
        rates = Rate.objects.all()
        return render(request, 'rate_list.html', {'rates': rates})

class RateCreateView(CreateView):
    model = Rate
    form_class = RateForm
    template_name = 'rate_create.html'
    success_url = reverse_lazy('rate_list')

class RateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Rate
    form_class = RateForm
    template_name = 'rate_update.html'
    success_url = reverse_lazy('rate_list')

    def test_func(self):
        return self.request.user.is_superuser

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Rate, pk=pk)

class RateDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Rate
    template_name = 'rate_delete.html'
    success_url = reverse_lazy('rate_list')

    def test_func(self):
        return self.request.user.is_superuser

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Rate, pk=pk)

class RateDetailView(LoginRequiredMixin, DetailView):
    model = Rate
    template_name = 'rate_details.html'
    success_url = reverse_lazy('rate_list')

class SourceListView(ListView):
    model = Source
    template_name = 'source_list.html'
    context_object_name = 'sources'
    paginate_by = 10
    filterset_class = SourceFilter

    def get_queryset(self):
        queryset = Source.objects.all().order_by('name', 'source_url', 'exchange_address', 'phone_number')
        return queryset
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['filter_params'] = "&".join(
            f"{key}={value}" for key, value in self.request.GET.items() if key != "page"
        )

        return context

class SourceCreateView(CreateView):
    model = Source
    form_class = SourceForm
    template_name = 'source_create.html'
    success_url = reverse_lazy('source_list')

class SourceUpdateView(UpdateView):
    model = Source
    form_class = SourceForm
    template_name = 'source_update.html'
    success_url = reverse_lazy('source_list')

class SourceDeleteView(DeleteView):
    model = Source
    form_class = SourceForm
    template_name = 'source_delete.html'
    success_url = reverse_lazy('source_list')

def contact_view(request):
    return render(request, 'contact.html')

def contact_us_list(request):
    contacts = ContactUs.objects.all()
    return render(request, 'currency/contact_us_list.html', {'contacts': contacts})

def source_details(request, pk):
    source = Source.objects.get(pk=pk)
    return render(request, 'source_details.html', {'source': source})

class IndexView(TemplateView):
    template_name = 'index.html'

class ContactUsCreateView(CreateView):
    model = ContactUs
    template_name = 'contactus_create.html'
    success_url = reverse_lazy('index')
    form_class = ContactUsForm

    def form_valid(self, form):
        recipient = settings.DEFAULT_FROM_EMAIL
        subject = 'User Contact Us'
        body = f'''
           Request from: {form.cleaned_data['name']}.
           Email to reply: {form.cleaned_data['reply_to']}.
           Subject Subject: {form.cleaned_data['subject']}.
           Body: {form.cleaned_data['body']}.
           '''
        send_mail(
            subject,
            body,
            recipient,
            [recipient],
            fail_silently=False
        )
        return super().form_valid(form)


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('password_change_done')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})