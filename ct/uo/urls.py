from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView


from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path("about/", views.about, name="about"),
    path("formation/<int:id>", views.details_formation, name="details_formation"),
    path("ue/<int:id>", views.details_ue, name="details_ue"),
    path("formations/",views.liste_formation, name="formations"),
    path("ues/",views.liste_ue, name="ues"),
    path('ue/ajouter', views.ajouter_ue, name='ajouter_ue'),
    path('ue/modifier/<int:ue_id>/', views.modifier_ue, name='modifier_ue'),
    path('ue/supprimer/<int:ue_id>/', views.supprimer_ue, name='supprimer_ue'),
    path("resume/<int:id>", views.resume_formation, name="resume_formation"),

    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/login', LoginView.as_view(next_page='menu'), name='login'),
    path('accounts/logout', LogoutView.as_view(next_page='menu'), name='logout'),
]