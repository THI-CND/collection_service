from django.test import TestCase
from django.urls import reverse
from .src.models import Collection, Recipe, User
import json

# Create your tests here.

class CollectionServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.recipe = Recipe.objects.create(name='Test Recipe')
        self.collection = Collection.objects.create(name='Test Collection', author=self.user, description='Test Description')
        self.collection.recipes.set([])
        
    def test_get_collections(self):
        response = self.client.get(reverse('collection_main'))
        self.assertEqual(response.status_code, 200)

    def test_get_collection(self):
        response = self.client.get(reverse('collection_main', args=[self.collection.id]))
        self.assertEqual(response.status_code, 200)

    def test_create_collection(self):
        data = {
            'name': 'New Collection',
            'author': self.user.username,
            'description': 'New Description',
            'recipes': [self.recipe.id]
        }
        response = self.client.post(reverse('collection_main'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Collection.objects.count(), 2)

    def test_update_collection(self):
        data = {
            'name': 'Updated Collection',
            'author': self.user.username,
            'description': 'Updated Description',
            'recipes': [self.recipe.id]
        }
        response = self.client.put(reverse('collection_main', args=[self.collection.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.collection.refresh_from_db()
        self.assertEqual(self.collection.name, 'Updated Collection')
        
    def test_update_collection_by_other_user(self):
        other_user = User.objects.create(username='other_user')
        data = {
            'name': 'Updated Collection',
            'author': other_user.username,
            'description': 'Updated Description',
            'recipes': [self.recipe.id]
        }
        response = self.client.put(reverse('collection_main', args=[self.collection.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.collection.refresh_from_db()
        self.assertNotEqual(self.collection.name, 'Updated Collection')

    def test_delete_collection(self):
        data = {
            'author': self.user.username
        }
        response = self.client.delete(reverse('collection_main', args=[self.collection.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Collection.objects.count(), 0)
    
    def test_delete_collection_by_other_user(self):
        other_user = User.objects.create(username='other_user')
        data = {
            'author': other_user.username
        }
        response = self.client.delete(reverse('collection_main', args=[self.collection.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Collection.objects.count(), 1)

    def test_add_recipe(self):
        data = {
            'recipe_id': self.recipe.id
        }
        response = self.client.post(reverse('edit_recipe', args=[self.collection.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.collection.recipes.count(), 1)

    def test_remove_recipe(self):
        self.collection.recipes.add(self.recipe)
        data = {
            'recipe_id': self.recipe.id
        }
        response = self.client.delete(reverse('edit_recipe', args=[self.collection.id]), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.collection.recipes.count(), 0)

    def test_get_collections_empty(self):
        # Lösche alle vorhandenen Collections
        Collection.objects.all().delete()
        response = self.client.get(reverse('collection_main'))
        self.assertEqual(response.status_code, 204)