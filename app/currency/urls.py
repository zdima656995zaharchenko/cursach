from django.urls import path, include, reverse_lazy
from django.contrib import admin
from django.contrib.auth import views as auth_views
from currency.views import (
    SourceListView,
    SourceCreateView,
    SourceUpdateView,
    SourceDeleteView,
    contact_view,
    contact_us_list,
    source_details,
    ContactUsCreateView,
    IndexView,
    RateListView,
    RateCreateView,
    RateUpdateView,
    RateDeleteView,
    RateDetailView,
    TemplateView,
)

urlpatterns = [
    path('rate_list/', RateListView.as_view(), name='rate_list'),
    path('rates/create/', RateCreateView.as_view(), name='rate_create'),
    path('rates/update/<int:pk>/', RateUpdateView.as_view(), name='rate_update'),
    path('rates/delete/<int:pk>/', RateDeleteView.as_view(), name='rate_delete'),
    path('rates/details/<int:pk>/', RateDetailView.as_view(), name='rate_details'),
    path('contact/', contact_view, name='contact'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path("__debug__/", include("debug_toolbar.urls")),
    path('contact-us/', contact_us_list, name='contact_us_list'),
    path('sources/', SourceListView.as_view(), name='source_list'),
    path('sources/details/<int:pk>/', source_details, name='source_details'),
    path('sources/create/', SourceCreateView.as_view(), name='source_create'),
    path('sources/update/<int:pk>/', SourceUpdateView.as_view(), name='source_update'),
    path('sources/delete/<int:pk>/', SourceDeleteView.as_view(), name='source_delete'),
    path('contactus/create/', ContactUsCreateView.as_view(), name='contactus_create'),
]
