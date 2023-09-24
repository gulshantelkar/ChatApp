from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from chatapp.models import User 
from .models import UserProfile
import json

class SuggestedFriendsViewTestCase(TestCase):
    def setUp(self):
   
        self.user = User.objects.create(username='testuser', email='testuser@gmail.com', password='testpassword')
        self.profile = UserProfile.objects.create(
            id=self.user.id,
            name='Test User',
            age=25,
            interests=json.dumps({'music': 5, 'sports': 4, 'movies': 3}),
        )

    def test_get_suggested_friends(self):
        client = APIClient()

       
        response = client.get(f'/api/suggested-friends/{self.user.id}/')

  
        self.assertEqual(response.status_code, status.HTTP_200_OK)

   
        self.assertIn('suggested_friends_previous', response.data)
        self.assertIn('suggested_friends_content_based', response.data)

       
        suggested_friends_previous = response.data['suggested_friends_previous']
        suggested_friends_content_based = response.data['suggested_friends_content_based']
        self.assertEqual(len(suggested_friends_previous), 5)
        self.assertEqual(len(suggested_friends_content_based), 5)

   
        for friend in suggested_friends_previous:
            self.assertIn('id', friend)
            self.assertIn('name', friend)
            self.assertIn('age', friend)
            self.assertIn('interests', friend)
            self.assertIn('score', friend)

        for friend in suggested_friends_content_based:
            self.assertIn('id', friend)
            self.assertIn('name', friend)
            self.assertIn('age', friend)
            self.assertIn('interests', friend)
   

    def tearDown(self):
      
        self.profile.delete()
        self.user.delete()
