from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("libros/", views.book_list, name="books"),
]