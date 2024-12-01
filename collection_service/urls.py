from django.urls import path

from .src import views_controller
urlpatterns=[
    path('collections/', views_controller.collection_main, name='collection_main'),
    path('collections/<int:id>/', views_controller.collection_main_id, name='collection_main_id'),
    path('collections/<str:id>/recipe/', views_controller.collection_edit_recipe, name='edit_recipe')
]