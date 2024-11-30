from django.urls import path

from .src import rest_controller
urlpatterns=[
    path('collections/', rest_controller.collection_main, name='collection_main'),
    path('collections/<int:id>/', rest_controller.collection_main_id, name='collection_main_id'),
    path('collections/<str:id>/recipe/', rest_controller.collection_edit_recipe, name='edit_recipe')
]