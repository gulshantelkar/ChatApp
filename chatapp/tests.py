from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User  
from rest_framework.authtoken.models import Token
from channels.layers import get_channel_layer
from channels.testing import ChannelsLiveServerTestCase
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator

class UserRegistrationAPITestCase(APITestCase):
    def test_user_registration_success(self):
        url = reverse('register')  
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_duplicate_username(self):
        User.objects.create_user(username='existinguser', password='password')
        url = reverse('register') 
        data = {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_user_registration_duplicate_email(self):
        User.objects.create_user(username='user1', email='existinguser@example.com', password='password')
        url = reverse('register')  
        data = {
            'username': 'newuser',
            'email': 'existinguser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

class UserLoginAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_login_success(self):
        url = reverse('login')  
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_invalid_credentials(self):
        url = reverse('login') 
        data = {
            'username': 'testuser',
            'password': 'invalidpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid credentials')

class OnlineUsersAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@gmail.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.online_user = User.objects.create_user(username='onlineuser', password='testpassword', is_online=True)

    def test_get_online_users(self):
        url = reverse('get_online_users') 
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 
        self.assertEqual(response.data[0]['username'], 'onlineuser')
        
    def test_start_chat_success(self):
        url = reverse('start_chat')  
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {'recipient_username': 'onlineuser'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Chat started successfully.')

    def test_start_chat_recipient_offline(self):
        url = reverse('start_chat') 
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {'recipient_username': 'nonexistentuser'} 

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Recipient is offline or not available.')
        
        


# User = get_user_model()

# class SendMessageWebSocketTestCase(ChannelsLiveServerTestCase):
#     def setUp(self):
#     
#         self.sender = User(username='sender', password='senderpassword')
#         self.sender_token = Token.objects.create(user=self.sender)

#     async def test_send_message_success(self):
#         channel_layer = get_channel_layer()

#      
#         with patch('django.contrib.auth.models.User.objects.create_user') as mock_create_user:
#             mock_create_user.return_value = self.sender

#             # Connect the sender to the WebSocket
#             communicator = self.get_communicator(
#                 f'/ws/chat/?token={self.sender_token.key}'
#             )
#             connected, _ = await communicator.connect()
#             self.assertTrue(connected)

#   
#             await communicator.send_json_to({
#                 'message': 'Hello, recipient!',
#                 'recipient_username': 'recipient'
#             })

#            
#             response = await communicator.receive_json_from()
#             self.assertIn('message', response)
#             self.assertEqual(response['message'], 'message sent successfully')

#             # Close the WebSocket connection
#             await communicator.disconnect()

#     def get_communicator(self, path):
#         from channels.db import database_sync_to_async

#         async def get_application(scope):
#             return self.application

#         application = database_sync_to_async(get_application)

#         return application(scope={'type': 'websocket', 'path': path})

#     def tearDown(self):
#         self.sender.delete()
