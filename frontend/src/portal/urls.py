from django.urls import path

from . import views


app_name = "portal"


urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "apps/<slug:app_id>/launch/",
        views.launch_application,
        name="launch_application",
    ),
]