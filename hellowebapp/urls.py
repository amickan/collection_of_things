from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
)
from collection import views
from collection.backends import MyRegistrationView
from collection.views import AboutView, IndexView, DetailView, BrowseName
from django.contrib.sitemaps.views import sitemap
from collection.sitemap import (
 ThingSitemap,
 StaticSitemap,
 HomepageSitemap,
)
sitemaps = {
 'things': ThingSitemap,
 'static': StaticSitemap,
 'homepage': HomepageSitemap,
}
from django.conf import settings
from django.views.static import serve
from django.urls import re_path


urlpatterns = (
    # path('', views.index, name='home'),
    path('', IndexView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    # path('contact/', ContactView.as_view(), name='contact'),
    path('contact/', views.emailView, name='contact'),
    #      name='email'),
    # path('about/',
    #      TemplateView.as_view(template_name='about.html'),
    #      name='about'),
    # path('contact/',
    #      TemplateView.as_view(template_name='contact.html'),
    #      name='contact'),
    path('things/', RedirectView.as_view(
        pattern_name='browse', permanent=True)),
    path('things/<slug:slug>/', DetailView.as_view(), name='thing_detail'),
    # path('things/<slug:slug>/', DetailViewSocial.as_view(), name='thing_detail'),
    # path('things/<slug>/', views.thing_detail, name='thing_detail'),
    path('things/<slug>/edit/', views.edit_thing, name='edit_thing'),
    path('browse/', RedirectView.as_view(
        pattern_name='browse', permanent=True)),
    path('browse/name/',
         BrowseName.as_view(), name='browse'),
    # path('browse/name/<initial>/',
    #      views.browse_by_name, name='browse_by_name'),
    path('browse/name/<initial>/', BrowseName.as_view(), name='browse_by_name'),
    path('accounts/password/reset/', PasswordResetView.as_view(),
         name="password_reset"),
    path('accounts/password/reset/done/', PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path('accounts/password/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('accounts/password/done', PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path('accounts/password/change/', PasswordChangeView.as_view(),
          name='password_change'),
    path('accounts/register/', MyRegistrationView.as_view(),
         name='registration_register'),
    path('accounts/create_thing/', views.create_thing,
         name='registration_create_thing'),
    path('things/<slug>/edit/images/', views.edit_thing_uploads,
         name='edit_thing_uploads'),
    path('things/edit/email/', views.edit_email,
         name='edit_email'),
    # path('email/', views.emailView,
    #      name='email'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('delete/<id>/', views.delete_upload, name='delete_upload'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    path('', include('collection.urls')),
    path('admin/', admin.site.urls),
    path('api/things/', views.api_thing_list,
        name="api_thing_list"),
    path('api/things/<id>/', views.api_thing_detail,
         name="api_thing_detail"),
)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
    urlpatterns = (
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
                  ) + urlpatterns