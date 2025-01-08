from django.urls import path
from .views import CollectionView, CollectionIDView, CollectionRecipeView, CollectionTagView

urlpatterns=[
    path('api/v1/collections/', CollectionView.as_view(), name='collection_view'),
    path('api/v1/collections/<int:id>/', CollectionIDView.as_view(), name='collection_id_view'),
    path('api/v2/collections/<int:id>/recipe/', CollectionRecipeView.as_view(), name='collection_recipe_view'),
    path('api/v2/collections/<int:id>/tags/', CollectionTagView.as_view(), name='collection_tag_view')
]