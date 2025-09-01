from django.urls import path
from . import views

app_name = "tickets"

urlpatterns = [
    path("welcome/", views.WelcomeView.as_view()),
    path("menu/", views.menu_view),
    path("get_ticket/<str:service_name>", views.line_view, name="line"),
    path("processing", views.processing_view, name="processing"),
    path("next", views.next_view, name="next")
]