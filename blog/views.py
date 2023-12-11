from typing import Any
from django import http
from django.http import HttpRequest
from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Department, Blog
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class BlogTemplateView(TemplateView):
    template_name = 'blog/blog.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.all()
        context['departments'] = Department.objects.all()
        return context
    
class BlogDetailsTemplateView(TemplateView):
    template_name = "blog/blog_detail.html"

    def get(self, request: HttpRequest, blog_id ,*args: Any, **kwargs: Any) -> HttpResponse:
        self.blog = get_object_or_404(Blog, pk=blog_id)
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['blog'] = self.blog
        context['departments'] = Department.objects.all()
        return context
    
class ContactTemplateView(TemplateView):
    template_name = 'blog/contacts.html'