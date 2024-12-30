from django.urls import path
from .views import CollectionView, CollectionIDView, CollectionRecipeView

urlpatterns=[
    path('collections/', CollectionView.as_view(), name='collection_view'),
    path('collections/<int:id>/', CollectionIDView.as_view(), name='collection_id_view'),
    path('collections/<str:id>/recipe/', CollectionRecipeView.as_view(), name='collection_recipe_view')
]