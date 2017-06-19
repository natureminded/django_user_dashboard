"""dashboard application URL Configuration"""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), # load homepage
    url(r'^signin$', views.login), # login a user
    url(r'^register$', views.register), # register a user
    url(r'^dashboard$', views.dashboard), # load normal user dashboard
    url(r'^dashboard/admin$', views.dashboard), # load admin dashboard
    url(r'^users/new$', views.new_user), # load new user form or create new user
    url(r'^users/show/(?P<id>\d*)$', views.show_or_message_user), # Show user / Create Message on User Show page
    url(r'^users/show/(?P<id>\d*)/comment$', views.comment), # Comment
    url(r'^users/edit/(?P<id>\d*)$', views.admin_update_user), # Admin Edit / update a user
    url(r'^users/edit/(?P<id>\d*)/password$', views.admin_update_password), # Admin update user password
    url(r'^users/edit$', views.update_profile), # Edit / update
    url(r'^users/edit/password$', views.update_password), # Update user password
    url(r'^users/edit/description$', views.update_profile_description), # Update user description
    url(r'^users/edit/(?P<id>\d*)/delete$', views.delete_user), # Delete a user
    url(r'^logout$', views.logout), # Logout user
]
