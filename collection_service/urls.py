from django.urls import path

from .src import views
urlpatterns=[
    path('collections/', views.collection_main, name='collection_main'),
    path('collections/<int:id>/', views.collection_main_id, name='collection_main_id'),
    path('collections/<str:id>/recipe/', views.collection_edit_recipe, name='edit_recipe')
]