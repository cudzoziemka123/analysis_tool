from django.urls import path
from . import views

urlpatterns = [
    path("answers/", views.answer_list, name="answer_list"),
    path("answers/<int:pk>/", views.answer_detail, name="answer_detail"),
    path("answers/<str:value>/<str:language>/<str:type>/",
         views.answer_list_for_category, name="answer_list_for_category"),

]
