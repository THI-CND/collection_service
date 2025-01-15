from django.test import TestCase
from django.urls import reverse
from ..src.models import Collection
import json


class CollectionServiceTests(TestCase):
    def setUp(self):
        self.user = 'testuser'
        self.recipe1 = "1"
        self.recipe2 = "2"
        self.collection = Collection.objects.create(
            name='Test Collection',
            author=self.user,
            description='Test Description'
        )
        self.collection.recipes = []
        self.collection.save()

    def test_get_collections(self):
        response = self.client.get(reverse('collection_view'))
        self.assertEqual(response.status_code, 200)
        collections = response.json()
        self.assertEqual(len(collections), 1)
        self.assertEqual(collections[0]['name'], 'Test Collection')

    def test_get_collection_by_id(self):
        response = self.client.get(reverse('collection_id_view', args=[self.collection.id]))
        self.assertEqual(response.status_code, 200)
        collection = response.json()
        self.assertEqual(collection['name'], "Test Collection")

    def test_create_collection(self):
        data = {
            'name': 'New Collection',
            'author': self.user,
            'description': 'New Description',
            'recipes': [self.recipe1, self.recipe2]
        }
        response = self.client.post(
            reverse('collection_view'), 
            data=json.dumps(data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Collection.objects.count(), 2)
        created_collection = Collection.objects.get(name='New Collection')
        self.assertEqual(created_collection.author, self.user)
        self.assertEqual(len(created_collection.recipes), 2)

    def test_update_collection(self):
        data = {
            'name': 'Updated Collection',
            'author': self.user,
            'description': 'Updated Description',
            'recipes': [self.recipe2]
        }
        response = self.client.put(
            reverse('collection_id_view', args=[self.collection.id]), 
            data=json.dumps(data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.collection.refresh_from_db()
        self.assertEqual(self.collection.name, 'Updated Collection')
        self.assertEqual(self.collection.description, 'Updated Description')
        self.assertEqual(len(self.collection.recipes), 1)
        
    def test_update_collection_by_other_user(self):
        other_user = 'other_user'
        data = {
            'name': 'Updated Collection',
            'author': other_user,
            'description': 'Updated Description',
            'recipes': [self.recipe2]
        }
        response = self.client.put(
            reverse('collection_id_view', args=[self.collection.id]), 
            data=json.dumps(data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
        self.collection.refresh_from_db()
        self.assertNotEqual(self.collection.name, 'Updated Collection')

    def test_delete_collection(self):
        data = {'author': self.user}
        response = self.client.delete(
            reverse('collection_id_view', args=[self.collection.id]), 
            data=json.dumps(data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Collection.objects.count(), 0)
       
    def test_delete_collection_by_other_user(self):
        other_user = 'other_user'
        data = {'author': other_user}
        response = self.client.delete(
            reverse('collection_id_view', args=[self.collection.id]), 
            data=json.dumps(data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Collection.objects.count(), 1)

    def test_add_recipe_to_collection(self):
        data = {'recipe_id': self.recipe1}
        response = self.client.post(
            reverse('collection_recipe_view', args=[self.collection.id]), 
            data=json.dumps(data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.collection.refresh_from_db()
        self.assertIn(self.recipe1, self.collection.recipes)

    def test_remove_recipe_from_collection(self):
        self.collection.recipes.append(self.recipe1)
        self.collection.save()
        data = {'recipe_id': self.recipe1}
        response = self.client.delete(
            reverse('collection_recipe_view', args=[self.collection.id]), 
            data=json.dumps(data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.collection.refresh_from_db()
        self.assertNotIn(self.recipe1, self.collection.recipes)

    def test_get_collections_empty(self):
        Collection.objects.all().delete()
        response = self.client.get(reverse('collection_view'))
        self.assertEqual(response.status_code, 200)