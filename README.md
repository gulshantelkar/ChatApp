# ChatApp
Activate the Virtual Environment : source myenv/bin/activate (mac command)
Start the server : python manage.py runserver


User registration: POST /api/register/ ::
     ![image](https://github.com/gulshantelkar/ChatApp/assets/99161604/a4364490-75bd-4c75-838a-acd9aed73b96)

User login: POST /api/login/ ::
     ![image](https://github.com/gulshantelkar/ChatApp/assets/99161604/135c6f52-a036-43f7-86d3-d704bd22f606)

Get online users: GET /api/online-users/ ::
      ![image](https://github.com/gulshantelkar/ChatApp/assets/99161604/1f49cf10-4b67-430f-9628-47f7528b3f75)
      ![image](https://github.com/gulshantelkar/ChatApp/assets/99161604/b10526ab-039b-46cc-87b7-84fd40686d05)


Start a chat: POST /api/chat/start/ ::
     ![image](https://github.com/gulshantelkar/ChatApp/assets/99161604/062c6e48-eddf-4db4-9c60-56219b4cf901)
     ![image](https://github.com/gulshantelkar/ChatApp/assets/99161604/345ca1c1-e24d-4e44-8ae4-f7d227e6573f)

Send a message: WEBSOCKET /api/chat/send/::
    run this command to start real time chatting : wscat -c "ws://127.0.0.1:8000/ws/chat/?token=logged_in_user_token"
    and also put json in one line when sending the message
    ![image](https://github.com/gulshantelkar/ChatApp/assets/99161604/3bab19f8-2277-4adf-bc49-1f26952936cd)
    ![image](https://github.com/gulshantelkar/ChatApp/assets/99161604/494a2a24-0909-4b36-aee3-6dd0b0a88023)

Recommended friends: GET /api/suggested–friends/<user_id> ::
 I have used 2 algorithms to get top 5 suggested friends


**Algorithm 1:  Based on Shared Interests**
1. Load user data from a JSON file.
2. Find the user's profile within the loaded data using their `user_id`.
3. Extract the user's interests and age.
4. Iterate through all users in the data except the current user:
   - Calculate common interests between the current user and other users.
   - Calculate a "score" for each user based on the sum of their interests' values that match the current user's interests.
   - Create a list of users with their scores.
5. Sort the list of users by their scores in descending order.
6. Select the top 5 users as suggested friends (`suggested_friends_previous`).

**Algorithm 2: Content-Based Filtering with Age Similarity as a Secondary Factor**
1. Load user data from a JSON file.
2. Find the user's profile within the loaded data using their `user_id`.
3. Extract the user's age.
4. Calculate TF-IDF (Term Frequency-Inverse Document Frequency) vectors for users' interests.
5. Compute cosine similarity scores between users based on their interests.
6. Find the user's index in the similarity scores.
7. Identify users with similar ages (within 4 years) to the current user.
8. If no users with similar ages are found, use all users.
9. Sort users by common interests score among those with similar ages (or all users if no similar age users).
10. Select the top 5 users as suggested friends (`suggested_friends_content_based`).

In both algorithms, the goal is to recommend friends to a user based on their interests. The first algorithm prioritizes users with common interests, while the second algorithm uses content-based filtering with an additional consideration for age similarity. The resulting suggested friends are returned in the response.

Output : http://127.0.0.1:8000/api/suggested-friends/145/
         {
    "suggested_friends_previous": [
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
        },
        {
            "id": 421,
            "name": "User 421",
            "age": 45,
            "interests": {
                "cars": 78,
                "computers": 93,
                "dancing": 88,
                "travelling": 79,
                "music": 99
            },
            "score": 245
        },
        {
            "id": 461,
            "name": "User 461",
            "age": 84,
            "interests": {
                "dancing": 75,
                "movies": 62,
                "photography": 72,
                "travelling": 74,
                "cars": 96,
                "drawing": 16
            },
            "score": 245
        },
        {
            "id": 650,
            "name": "User 650",
            "age": 12,
            "interests": {
                "cars": 97,
                "music": 37,
                "cooking": 59,
                "travelling": 94,
                "movies": 65,
                "dancing": 53
            },
            "score": 244
        },
        {
            "id": 716,
            "name": "User 716",
            "age": 91,
            "interests": {
                "computers": 88,
                "cooking": 14,
                "travelling": 100,
                "cars": 40,
                "dancing": 93
            },
            "score": 233
        }
    ],
    "suggested_friends_content_based": [
        {
            "id": 184,
            "name": "User 184",
            "age": 58,
            "interests": {
                "cooking": 94,
                "dancing": 56,
                "photography": 96,
                "cars": 33,
                "travelling": 85,
                "drawing": 44
            },
            "interests_text": "cooking dancing photography cars travelling drawing"
        },
        {
            "id": 367,
            "name": "User 367",
            "age": 59,
            "interests": {
                "dancing": 63,
                "cars": 84,
                "computers": 94
            },
            "interests_text": "dancing cars computers"
        },
        {
            "id": 443,
            "name": "User 443",
            "age": 54,
            "interests": {
                "cars": 10,
                "dancing": 57,
                "music": 58,
                "computers": 26,
                "travelling": 40,
                "singing": 93
            },
            "interests_text": "cars dancing music computers travelling singing"
        },
        {
            "id": 708,
            "name": "User 708",
            "age": 52,
            "interests": {
                "cars": 48,
                "dancing": 24,
                "travelling": 48,
                "music": 21,
                "photography": 89,
                "cooking": 53
            },
            "interests_text": "cars dancing travelling music photography cooking"
        },
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
        }
    ]
}
    




     


     
