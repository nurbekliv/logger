from __future__ import annotations

import os
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from django import forms
from django.views.decorators.http import require_POST

from .models import Code, Device, Screenshot


def get_client_ip(request) -> str:
    # reverse proxy bo'lsa X-Forwarded-For ishlaydi
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "") or ""


class UserLoginView(LoginView):
    template_name = "log/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")


class HomeView(LoginRequiredMixin, ListView):
    template_name = "log/home.html"
    context_object_name = "codes"

    def get_queryset(self):
        return Code.objects.filter(active=True).only("id", "name", "file")


@login_required
def download_code(request, pk: int):
    code = get_object_or_404(Code, pk=pk, active=True)

    if not code.file:
        raise Http404("File not found")

    file_path = code.file.path
    if not os.path.exists(file_path):
        raise Http404("File missing on disk")

    # Brauzerga zip sifatida yuborish
    resp = FileResponse(open(file_path, "rb"), as_attachment=True)
    # original nomni saqlab beramiz:
    filename = os.path.basename(file_path)
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp


class ScreenshotUploadForm(forms.Form):
    image = forms.ImageField()


class ScreenshotUploadView(LoginRequiredMixin, FormView):
    template_name = "log/screenshot_upload.html"
    form_class = ScreenshotUploadForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        ip = get_client_ip(self.request)

        device, _ = Device.objects.get_or_create(ip=ip, defaults={"active": True})
        # device active false bo'lsa ham screenshot saqlashni xohlasang shu yerda tekshir
        screenshot = Screenshot.objects.create(
            image=form.cleaned_data["image"],
            device=device,
            ip=ip,
        )
        return super().form_valid(form)


@require_POST
def api_screenshot_upload(request):
    """
    Device (masalan agent) screenshot yuborishi uchun:
    POST form-data: image=<file>
    """
    if not request.FILES.get("image"):
        return JsonResponse({"ok": False, "error": "image is required"}, status=400)

    ip = get_client_ip(request)

    device, _ = Device.objects.get_or_create(ip=ip, defaults={"active": True})

    # Agar faqat active device qabul qilmoqchi bo'lsang:
    # if not device.active:
    #     return JsonResponse({"ok": False, "error": "device inactive"}, status=403)

    s = Screenshot.objects.create(
        image=request.FILES["image"],
        device=device,
        ip=ip,
    )
    return JsonResponse({"ok": True, "id": s.id})
