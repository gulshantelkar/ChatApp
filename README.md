# ChatApp

## Getting Started
1. Activate the Virtual Environment (Mac Command):
 ```bash
$ source venv/bin activate
```
 ```bash 
pip install -r requirements.txt
```
2. Start the server:
```bash
$ python manage.py runserver
```


## API Endpoints

### User Registration
- **POST** `/api/register/`
![User Registration](https://github.com/gulshantelkar/ChatApp/assets/99161604/a4364490-75bd-4c75-838a-acd9aed73b96)

### User Login
- **POST** `/api/login/`
![User Login](https://github.com/gulshantelkar/ChatApp/assets/99161604/135c6f52-a036-43f7-86d3-d704bd22f606)

### Get Online Users
- **GET** `/api/online-users/`
![Get Online Users](https://github.com/gulshantelkar/ChatApp/assets/99161604/1f49cf10-4b67-430f-9628-47f7528b3f75)
![Online Users](https://github.com/gulshantelkar/ChatApp/assets/99161604/b10526ab-039b-46cc-87b7-84fd40686d05)

### Start a Chat
- **POST** `/api/chat/start/`
![Start a Chat](https://github.com/gulshantelkar/ChatApp/assets/99161604/062c6e48-eddf-4db4-9c60-56219b4cf901)
![Chat](https://github.com/gulshantelkar/ChatApp/assets/99161604/345ca1c1-e24d-4e44-8ae4-f7d227e6573f)

### Send a Message (WebSocket)
- **WebSocket** `/api/chat/send/`
Run this command to start real-time chatting:
```bash
$ wscat -c "ws://127.0.0.1:8000/ws/chat/?token=logged_in_user_token"
```


And also, put JSON in one line when sending the message:
![Send a Message](https://github.com/gulshantelkar/ChatApp/assets/99161604/3bab19f8-2277-4adf-bc49-1f26952936cd)
![Message](https://github.com/gulshantelkar/ChatApp/assets/99161604/494a2a24-0909-4b36-aee3-6dd0b0a88023)

### Recommended Friends
- **GET** `/api/suggested-friends/<user_id>`
Two algorithms are used to get the top 5 suggested friends:

**Algorithm 1: Based on Shared Interests**
- Load user data from a JSON file.
- Find the user's profile within the loaded data using their `user_id`.
- Extract the user's interests and age.
- Calculate common interests and scores for other users.
- Sort users by score and select the top 5.

**Algorithm 2: Content-Based Filtering with Age Similarity as a Secondary Factor**
- Load user data from a JSON file.
- Find the user's profile within the loaded data using their `user_id`.
- Calculate TF-IDF vectors for user interests.
- Compute cosine similarity scores based on interests.
- Identify users with similar ages (within 4 years).
- Sort users by common interests score, considering age similarity.
- Select the top 5 suggested friends.

Example Output:
```json
{
  "suggested_friends_using_first_algo": [     

        {
            "id": 225,
            "name": "User 225",
            "age": 47,
            "interests": {
                "drawing": 40,
                "singing": 31,
                "travelling": 91,
                "cars": 74,
                "music": 10,
                "dancing": 88
            },
            "score": 253
        },...
],
  "suggested_friends_using_second_algo": [

          {
            "id": 856,
            "name": "User 856",
            "age": 52,
            "interests": {
                "movies": 13,
                "cars": 75,
                "music": 11,
                "travelling": 10,
                "dancing": 55,
                "computers": 71
            },
            "interests_text": "movies cars music travelling dancing computers"
          }...
]
```
## Testing

### RESTful API Testing
 ```bash
$ python manage.py test
``` 

I have thoroughly tested the following RESTful APIs:

- **User Registration:** Testing user registration functionality to ensure that new users can create accounts successfully.

- **User Login:** Verifying the user login process to ensure that registered users can log in securely.

- **Get Online Users:** Testing the ability to retrieve a list of users who are currently online.

- **Start a Chat:** Ensuring that users can initiate chat sessions with one another successfully.


### WebSocket Real-Time Chatting

- Testing WebSocket real-time chat in Django, primarily using ChannelsLiveServerTestCase, can be complex due to potential conflicts with database operations.

- Although not covered by tests in this project, it is advisable to manually test WebSocket real-time chat during development using tools like `wscat` for simulating real-time messaging scenarios.



