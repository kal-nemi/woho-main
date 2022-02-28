"""Podacity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
import project_app.views
import accounts.views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('preferences', project_app.views.preferences, name='preferences'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('signup', accounts.views.register, name='signup'),
    # path('', project_app.views.podacity, name='podacity'),
    path('podacity', project_app.views.homepage, name='podacity'),
    path('network_map', project_app.views.network_map, name='network_map'),
    # path('preferences', project_app.views.preferences, name='preferences_2'),
    path('testgame/', TemplateView.as_view(template_name="nx.html"), name='testgame'),
    path('search_professors', project_app.views.search_professors, name='search_professors'),
    path('search_expertise', project_app.views.search_expertise, name='search_expertise'),
    path('tender_search', project_app.views.tender_search, name='tender_search'),
    path('add_new_tender', project_app.views.add_new_tender, name='add_new_tender'),
    path('search', project_app.views.search_new, name='search_new'),
    path('expertise_map', project_app.views.expertise_map, name='expertise_map'),
    path('expertise_map_new', project_app.views.expertise_map_new, name='expertise_map_new'),
    path('expertise_graph', project_app.views.expertise_graph),
    path('graphs/<int:index>/', project_app.views.ok_to_load),
    path('graph/<int:index>/', project_app.views.graph_frame),
    path('home', project_app.views.home, name='home'),
    # path('', project_app.views.woho_home, name='woho_home'),
    path('', project_app.views.woho_home, name='woho_home'),
    path('addspace', project_app.views.woho_addspace, name='woho_addspace'),
    path('partner_search', project_app.views.partner_search, name='partner_search'),
    path('directory', project_app.views.directory, name='directory'),
    path('projects', project_app.views.projects, name='projects'),
    path('clusters', project_app.views.clusters, name='clusters'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
