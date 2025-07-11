import pandas as pd
import numpy as np
import joblib
from config.paths_config import *

# 1. Get anime frame function
def getAnimeFrame(anime, path_df):
    df = pd.read_csv(path_df)
    if isinstance(anime, int):
        return df[df.anime_id == anime]
    elif isinstance(anime, str):
        return df[df.eng_version == anime]
    else:
        print("Incorrect name or id emtered")
        
# 2. Get Synopsis function
def getSynopsis(anime, path_synopsis_df):
    synopsis_df = pd.read_csv(path_synopsis_df)
    if isinstance(anime, int):
        return synopsis_df[synopsis_df.MAL_ID == anime].sypnopsis.values[0]
    elif isinstance(anime, str):
        return synopsis_df[synopsis_df.Name == anime].sypnopsis.values[0]
    else:
        print("Incorrect name or id emtered")
        
# 3. Content Recommendation
def find_similar_animes(name, path_anime_weights, path_anime2anime_encoded, path_anime2anime_decoded, 
                        path_anime_df, n=10, return_dist=False, neg=False):
    
    anime_weights = joblib.load(path_anime_weights)
    anime2anime_encoded = joblib.load(path_anime2anime_encoded)
    anime2anime_decoded = joblib.load(path_anime2anime_decoded)
    
    try:
        # Fetching the original index from df
        index = getAnimeFrame(name, path_anime_df).anime_id.values[0]
        
        # Fetching the encoded index from the trained model df
        encoded_index = anime2anime_encoded.get(index) 
        
        # Calculation of the weight of all the anime w.r.t the particular anime and sort from least similar to most similar
        weights = anime_weights
        dists = np.dot(weights, weights[encoded_index]) 
        sorted_dists = np.argsort(dists)
        
        # Want the target anime to be included in the list
        n = n+1 
        
        # If neg=True will get least similar anime || neg=False most similar anime
        if neg:
            closest = sorted_dists[:n]
        else:
            closest = sorted_dists[-n:]
        
        # If user sets return_dist=true it will return, but here it is false   
        if return_dist:
            return dists, closest
        
        # Sreating an emmpty list then append the similar ones in it
        SimilarityArr = []
        for close in closest:
            decoded_id = anime2anime_decoded.get(close)
            anime_frame = getAnimeFrame(decoded_id, path_anime_df)
            anime_name = anime_frame.eng_version.values[0]
            genres = anime_frame.Genres.values[0]
            similarity = dists[close]
            
            SimilarityArr.append({
                "anime_id" : decoded_id,
                "name" : anime_name,
                "similarity" : similarity,
                "genre" : genres
            })
        
        # Converting the nested list dict to pandas df and sorting them in descending order
        Frame = pd.DataFrame(SimilarityArr).sort_values(by="similarity", ascending=False)
        
        # Dropping the target anime name because it is of no use
        return Frame[Frame.anime_id != index].drop(['anime_id'], axis = 1)    
    
    except Exception as e:
        print("Error Occure...", e)
        
# 4. Find Similar users
def find_similar_users(item_input, path_user_weights, path_user2user_encoded, path_user2user_decoded, n=10, return_dist=False, neg=False):
    user_weights = joblib.load(path_user_weights)
    user2user_encoded = joblib.load(path_user2user_encoded)
    user2user_decoded = joblib.load(path_user2user_decoded)    
    try:
        index=item_input
        encoded_index=user2user_encoded.get(index)
        weights = user_weights
        
        # Compute cosine-style similarities (dot products)
        dists = np.dot(weights, weights[encoded_index]) 
        sorted_dists = np.argsort(dists)
        
        # Want the target anime to be included in the list
        n=n+1 
        
        # If neg=True will get least similar anime || neg=False most similar anime
        if neg:
            closest = sorted_dists[:n]
        else:
            closest = sorted_dists[-n:]
        
        # If user sets return_dist=true it will return, but here it is false   
        if return_dist:
            return dists, closest
        
        # Sreating an emmpty list then append the similar ones in it
        rows = []
        for close in closest:
            sim = dists[close]
            decoded_id = user2user_decoded.get(close)
            rows.append({
                "similar_user": decoded_id,
                "similarity": sim,
            })

        df = pd.DataFrame(rows)
        # Exclude the target user by filtering on the correct column name
        df = df[df.similar_user != item_input]
        # Sort descending by similarity
        df = df.sort_values("similarity", ascending=False).reset_index(drop=True)

        return df   
    
    except Exception as e:
        print("Error Occure...", e)
        
# 5. Get User preferences
def get_user_preferences(user_id, path_rating_df, path_anime_df, plot=False):
    
    rating_df = pd.read_csv(path_rating_df)
    df = pd.read_csv(path_anime_df)
    
    animes_watched_by_user = rating_df[rating_df.user_id == user_id]
    user_rating_percentile = np.percentile(animes_watched_by_user.rating, 75)
    animes_watched_by_user = animes_watched_by_user[animes_watched_by_user.rating >= user_rating_percentile]
    top_animes_user = (animes_watched_by_user.sort_values(by='rating', ascending=False).anime_id.values)
    anime_df_rows = df[df["anime_id"].isin(top_animes_user)]
    anime_df_rows = anime_df_rows[["eng_version", "Genres"]]
    return anime_df_rows

# 6. Get user recommendation
def get_user_recommendations(similar_user, user_pref, path_anime_df, path_synopsis_df, path_rating_df, n=10):
    
 
    
    recommended_animes = []
    anime_list = []
    
    for user_id in similar_user.similar_user.values:
        pref_list = get_user_preferences(int(user_id), path_rating_df, path_anime_df)
        
        pref_list = pref_list[~pref_list.eng_version.isin(user_pref.eng_version.values)]
        
        if not pref_list.empty:
            anime_list.append(pref_list.eng_version.values)
            
    if anime_list:
        anime_list = pd.DataFrame(anime_list)
        sorted_list = pd.DataFrame(pd.Series(anime_list.values.ravel()).value_counts().head(n))
                
        for i, anime_name in enumerate(sorted_list.index):
            n_user_pref = sorted_list[sorted_list.index == anime_name].values[0][0]
                    
            if isinstance(anime_name, str):
                frame = getAnimeFrame(anime_name, path_anime_df)
                anime_id = frame.anime_id.values[0]
                genre = frame.Genres.values[0]
                synopsis = getSynopsis(int(anime_id), path_synopsis_df)
                        
                recommended_animes.append({
                    "n" : n_user_pref,
                    "anime_name" : anime_name,
                    "genre" : genre,
                    "synopsis" : synopsis
                })
                        
    return pd.DataFrame(recommended_animes).head(n)