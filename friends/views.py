
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import F, Sum
import json 
from .models import UserProfile
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class SuggestedFriendsView(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']

    
        with open('/Users/gulshantelkar/Desktop/App/mydrfproject/friends/friend.json', 'r') as json_file:
            user_data = json.load(json_file)

    
        users = user_data.get('users', [])


        user_profile = None
        for user in users:
            if user.get('id') == user_id:
                user_profile = user
                break

        if not user_profile:
            return Response({'error': 'User not found'}, status=404)

        user_interests = user_profile.get('interests', {}).keys()
        user_age = user_profile.get('age', 0)

        users_with_scores = []
        for user in users:
            if user.get('id') != user_id:
                common_interests = set(user.get('interests', {}).keys()) & set(user_interests)
                score = sum(user['interests'].get(interest, 0) for interest in common_interests)
                users_with_scores.append({
                    'id': user.get('id'),
                    'name': user.get('name'),
                    'age': user.get('age'),
                    'interests': user.get('interests'),
                    'score': score,
                })

     
        users_with_scores.sort(key=lambda x: x['score'], reverse=True)

   
        suggested_friends_previous = users_with_scores[:5]


        users_df = pd.DataFrame(users)
        users_df['interests_text'] = users_df['interests'].apply(lambda x: ' '.join(x.keys()))
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(users_df['interests_text'])
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        user_index = users_df[users_df['id'] == user_id].index[0]
        sim_scores = list(enumerate(cosine_sim[user_index]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)


        user_age = users_df.iloc[user_index]['age']
        close_age_users = []
        for user in sim_scores[1:]:
            other_user_age = users_df.iloc[user[0]]['age']
            if abs(user_age - other_user_age) <= 4:
                close_age_users.append(user)

  
        if not close_age_users:
            close_age_users = sim_scores

       
        close_age_users = sorted(close_age_users, key=lambda x: x[1], reverse=True)

     
        recommended_user_ids = [users_df.iloc[user[0]]['id'] for user in close_age_users[:5]]
        recommended_friends_content_based = users_df[users_df['id'].isin(recommended_user_ids)]

        top5_recommended_friends_content_based = recommended_friends_content_based.head(5).to_dict('records')


        return Response({'suggested_friends_previous': suggested_friends_previous, 'suggested_friends_content_based': top5_recommended_friends_content_based})
