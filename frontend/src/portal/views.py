from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .models import Application
from .node_bff import BFF


@login_required
def home(request):
    applications = (
        Application.objects
        .filter(
            enabled=True,
            groups__user=request.user,
        )
        .distinct()
        .order_by("name")
    )

    return render(
        request,
        "portal/home.html",
        {
            "applications": applications,
        },
    )


@login_required
def launch_application(request, app_id):
    if request.method != "POST":
        return HttpResponseForbidden()

    application = get_object_or_404(
        Application,
        id=app_id,
        enabled=True,
        groups__user=request.user,
    )

    manager = BFF()

    result = manager.start(
        application.service,
    )

    return redirect(
        result["url"],
    )