import pandas as pd
import numpy as np
import joblib
from config.paths_config import *
from utils.helpers import * 



def hybrid_recommendation(user_id, user_weight=0.5, content_weight=0.5):
    # User Recommendation
    similar_user = find_similar_users(user_id, USER_WEIGHTS_PATH, USER2USER_ENCODED, USER2USER_DECODED)
    user_pref = get_user_preferences(user_id, RATING_DF, DF)
    user_recommended_animes = get_user_recommendations(similar_user, user_pref, DF, SYNOPSIS_DF, RATING_DF)
    user_recommended_anime_list = user_recommended_animes["anime_name"].tolist()
    
    # Content Recommendation
    content_recommended_animes = []  
    for anime in user_recommended_anime_list:
        similar_animes = find_similar_animes(anime, ANIME_WEIGHTS_PATH, ANIME2ANIME_ENCODED, ANIME2ANIME_DECODED, DF)
        if similar_animes is not None and not similar_animes.empty:
            content_recommended_animes.extend(similar_animes["name"].tolist())
        else:
            print("No Similar Anime found wrt, ", anime)
    
    combines_score = {}
    for anime in  user_recommended_anime_list:
        combines_score[anime] = combines_score.get(anime, 0) + user_weight
    for anime in content_recommended_animes:
        combines_score[anime] = combines_score.get(anime, 0) + content_weight
        
    sorted_animes = sorted(combines_score.items(), key = lambda x:x[1], reverse=True)
    return [anime for anime, score in sorted_animes[:10]]
             