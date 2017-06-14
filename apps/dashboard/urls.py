"""dashboard application URL Configuration"""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), # load homepage
    url(r'^signin$', views.login), # login a user
    url(r'^register$', views.register), # register a user
    url(r'^dashboard$', views.user_dashboard), # load normal user dashboard
    url(r'^dashboard/admin$', views.admin_dashboard), # load admin dashboard
    url(r'^users/show/(?P<id>\d*)$', views.show_user), # Show user / Create Message on User Show page
    url(r'^users/show/(?P<id>\d*)/comment$', views.comment), # Comment
    url(r'^users/edit/(?P<id>\d*)/$', views.edit_user), # Edit a user
    url(r'^users/edit/(?P<id>\d*)/delete/$', views.delete_user), # Delete a user
    url(r'^logout$', views.logout), # Logout user
]
