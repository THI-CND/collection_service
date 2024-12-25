from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from ..src.models import Collection, Recipe, User
import json

# Create your tests here.

class CollectionServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.recipe1 = Recipe.objects.create(name='Test Recipe1')
        self.recipe2 = Recipe.objects.create(name='Test Recipe2')
        self.collection = Collection.objects.create(name='Test Collection', author=self.user, description='Test Description')
        self.collection.recipes.set([])
        
    def test_get_collections(self):
        response = self.client.get(reverse('collection_view'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_get_collection(self):
        response = self.client.get(reverse('collection_id_view', args=[self.collection.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], "Test Collection")

    @patch('collection_service.src.rabbitmq.rabbitmq_config.connect', MagicMock())
    @patch('collection_service.src.rabbitmq.rabbitmq_sender.publish_event')
    def test_create_collection(self, mock_publish_event):
        data = {
            'name': 'New Collection',
            'author': self.user.username,
            'description': 'New Description',
            'recipes': [self.recipe1.id, self.recipe2.id]
        }
        response = self.client.post(reverse('collection_view'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Collection.objects.count(), 2)
        mock_publish_event.assert_called_once_with('collection.created', {
            "user": self.user.username,
            "title": "Collection created",
            "message": f'Hello {self.user.username}, your new collection "New Collection" was created.'
        })

    @patch('collection_service.src.rabbitmq.rabbitmq_config.connect', MagicMock())
    @patch('collection_service.src.rabbitmq.rabbitmq_sender.publish_event')
    def test_update_collection(self, mock_publish_event):
        data = {
            'name': 'Updated Collection',
            'author': self.user.username,
            'description': 'Updated Description',
            'recipes': [self.recipe2.id]
        }
        response = self.client.put(reverse('collection_id_view', args=[self.collection.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.collection.refresh_from_db()
        self.assertEqual(self.collection.name, 'Updated Collection')
        mock_publish_event.assert_called_once_with('collection.updated', {
            "user": self.user.username,
            "title": "Collection updated",
            "message": f'Hello {self.user.username}, your collection "Updated Collection" was updated.'
        })
        
    def test_update_collection_by_other_user(self):
        other_user = User.objects.create(username='other_user')
        data = {
            'name': 'Updated Collection',
            'author': other_user.username,
            'description': 'Updated Description',
            'recipes': [self.recipe2.id]
        }
        response = self.client.put(reverse('collection_id_view', args=[self.collection.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.collection.refresh_from_db()
        self.assertNotEqual(self.collection.name, 'Updated Collection')

    @patch('collection_service.src.rabbitmq.rabbitmq_config.connect', MagicMock())
    @patch('collection_service.src.rabbitmq.rabbitmq_sender.publish_event')
    def test_delete_collection(self, mock_publish_event):
        data = {
            'author': self.user.username
        }
        response = self.client.delete(reverse('collection_id_view', args=[self.collection.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Collection.objects.count(), 0)
        mock_publish_event.assert_called_once_with('collection.deleted', {
            "user": self.user.username,
            "title": "Collection deleted",
            "message": f'Hello {self.user.username}, your collection "Test Collection" was deleted.'
        })
    
    def test_delete_collection_by_other_user(self):
        other_user = User.objects.create(username='other_user')
        data = {
            'author': other_user.username
        }
        response = self.client.delete(reverse('collection_id_view', args=[self.collection.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Collection.objects.count(), 1)

    def test_add_recipe(self):
        data = {
            'recipe_id': self.recipe1.id
        }
        response = self.client.post(reverse('collection_recipe_view', args=[self.collection.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.collection.recipes.count(), 1)

    def test_remove_recipe(self):
        self.collection.recipes.add(self.recipe1)
        data = {
            'recipe_id': self.recipe1.id
        }
        response = self.client.delete(reverse('collection_recipe_view', args=[self.collection.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.collection.recipes.count(), 0)

    def test_get_collections_empty(self):
        # Lösche alle vorhandenen Collections
        Collection.objects.all().delete()
        response = self.client.get(reverse('collection_view'))
        self.assertEqual(response.status_code, 204)