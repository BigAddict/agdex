from django.urls import path
from .views import BlogTemplateView, BlogDetailsTemplateView, ContactTemplateView

urlpatterns = [
    path("", BlogTemplateView.as_view(), name='blogs'),
    path("blog_detail/<int:blog_id>/", BlogDetailsTemplateView.as_view(), name='blog_details'),
    path("contacts", ContactTemplateView.as_view(), name="contacts")
]
