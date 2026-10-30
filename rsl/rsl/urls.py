
from django.contrib import admin
from hello import views
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from authorization import urls
from wagtail.admin import urls as wagtailadmin_urls

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path(
        "news/<int:pk>/", views.news_page, name="news_page"
    ),  # как минимум функция и вью одноименные
    path("auth/", include("authorization.urls")),
    path("news/<int:pk>/delete-comment/", views.delete_comment, name="delete_comment"),
    path("comment/edit/<int:pk>/", views.edit_comment, name="edit_comment"),
    path("profile/", views.profile_view, name="profile"),
    path("news/wagtail/<int:pk>/add-comment/",views.add_wagtail_comment,name="add_wagtail_comment"),
    path("news/", views.news_archive, name="news_archive"),
    path("cms/", include(wagtailadmin_urls)),
    path("", include("wagtail.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
