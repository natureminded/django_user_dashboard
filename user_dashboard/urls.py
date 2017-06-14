"""user_dashboard project URL Configuration"""

from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include("apps.dashboard.urls")), # grabs urls.py for `dashboard` application
]
