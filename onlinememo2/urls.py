from django.conf import settings

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from .urls_api import router as note_router

urlpatterns = [
    path("", TemplateView.as_view(template_name="homepage.html"), name="home"),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("payments/", include("pinax.stripe.urls")),
    path("api/", include(note_router.urls)),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("terms-of-use/", TemplateView.as_view(template_name="terms_of_use.html"), name="terms-of-use"),
    path("privacy-policy/", TemplateView.as_view(template_name="privacy_policy.html"), name="privacy-policy"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
