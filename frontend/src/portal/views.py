from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .models import Application, SecurityGroup
from .node_bff import BFF

# Page title and blurb per group. Add an entry when you add a group.
LANDING = {
    "admin": {"title": "Administrator", "blurb": "Full platform access."},
    "manager": {"title": "Manager", "blurb": "Team and reporting tools."},
    "developer": {"title": "Developer", "blurb": "Build and deploy tools."},
    "test": {"title": "Test", "blurb": "Test environments."},
}


@login_required
def home(request):
    groups = list(request.user.security_groups.order_by("name"))

    if not groups:
        return render(request, "portal/no_access.html", status=403)

    if len(groups) == 1:
        return redirect("portal:landing", group=groups[0].name)

    return render(request, "portal/pick_group.html", {"groups": groups})


@login_required
def landing(request, group):
    sg = get_object_or_404(SecurityGroup, name=group)

    if not sg.users.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden("You are not in this group.")

    applications = sg.applications.filter(enabled=True).order_by("name")
    info = LANDING.get(sg.name, {"title": sg.name.title(), "blurb": ""})

    return render(
        request,
        "portal/landing.html",
        {"group": sg, "info": info, "applications": applications},
    )


@login_required
def launch_application(request, app_id):
    if request.method != "POST":
        return HttpResponseForbidden()

    application = get_object_or_404(
        Application,
        id=app_id,
        enabled=True,
        groups__users=request.user,   # was groups__user
    )

    result = BFF().start(application.service)
    return redirect(result["url"])