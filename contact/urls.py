from django.urls import path
from .views import AddContactView, ContactListView, UpdateContactView, DeleteContactView, MarkSpamContactView, DetailContactView

app_name = "contact"

urlpatterns = [
    path("list/", ContactListView.as_view(), name="contact-list"),
    path("add/", AddContactView.as_view(), name="add"),
    path("update/<int:pk>/", UpdateContactView.as_view(), name="update"),
    path("delete/<int:pk>/", DeleteContactView.as_view(), name="delete"),
    path("mark-spam/<int:pk>/", MarkSpamContactView.as_view(), name="mark-spam"),
    path("detail/<int:pk>/", DetailContactView.as_view(), name="detail"),
]
