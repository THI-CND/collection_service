from django.urls import path
from .views import CollectionView, CollectionIDView, CollectionRecipeView, CollectionTagView

urlpatterns=[
    path('collections/', CollectionView.as_view(), name='collection_view'),
    path('collections/<int:id>/', CollectionIDView.as_view(), name='collection_id_view'),
    path('collections/<int:id>/recipe/', CollectionRecipeView.as_view(), name='collection_recipe_view'),
    path('collections/<int:id>/tags/', CollectionTagView.as_view(), name='collection_tag_view')
]