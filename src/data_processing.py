import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
import sys


logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file 
        self.output_dir = output_dir
        
        self.rating_df = None
        self.anime_df = None
        self.X_train_array = None
        self.X_test_array = None 
        self.y_train = None
        self.y_test = None
        
        self.user2user_encoded = {}
        self.user2user_decoded = {}
        self.anime2anime_encoded = {}
        self.anime2anime_decoded = {}
        
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"DataProcessing Initialized")
        
    def load_data(self, usecols):
        try:
            self.rating_df = pd.read_csv(self.input_file, low_memory=True, usecols=usecols)
            logger.info(f"Data loaded sucessfully for data processing")
        except Exception as e:
            raise CustomException(f"Failed to load the data {sys}")

    def filter_users(self, min_rating=400):
        try:
            n_ratings=self.rating_df['user_id'].value_counts()
            self.rating_df=self.rating_df[self.rating_df['user_id'].isin(n_ratings[n_ratings>=400].index)].copy()
            logger.info(f"Filtered users sucessfully")
        except Exception as e:
            raise CustomException(f"Failed to filter the data {sys}")
        
    def scale_ratings(self):
        try:
            scaler = MinMaxScaler()
            self.rating_df['rating'] = scaler.fit_transform(self.rating_df[['rating']])
            logger.info(f"Scaling done for Rating column")
        except Exception as e:
            raise CustomException(f"Failed to scale the rating column {sys}")
    
    def encode_data(self):
        try: 
            user_ids = self.rating_df["user_id"].unique().tolist()
            self.user2user_encoded = {user_id: i for i, user_id in enumerate(user_ids)}
            self.user2user_decoded = {i: user_id for i, user_id in enumerate(user_ids)}
            self.rating_df["user"] = self.rating_df["user_id"].map(self.user2user_encoded)
            
            anime_ids = self.rating_df["anime_id"].unique().tolist()
            self.anime2anime_encoded = {anime_id: i for i, anime_id in enumerate(anime_ids)}
            self.anime2anime_decoded = {i: anime_id for i, anime_id in enumerate(anime_ids)}
            self.rating_df["anime"] = self.rating_df["anime_id"].map(self.anime2anime_encoded)
            
            logger.info(f"Encoding done for user and anime ids")    
        except Exception as e:
            raise CustomException(f"Failed to encode the data {sys}")            

    def split_data(self):
        try:
            X = self.rating_df[["user", "anime"]].values
            y = self.rating_df["rating"].values
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.X_train_array = [X_train[:, 0], X_train[:, 1]]
            self.X_test_array = [X_test[:, 0], X_test[:, 1]]
            self.y_train = y_train
            self.y_test = y_test
            logger.info(f"Data Splitt sucessfully")    
        except Exception as e:
            raise CustomException(f"Failed to split the data {sys}")  
        
    def save_artifacts(self):
        try: 
            artifacts = {
                "user2user_encoded" : self.user2user_encoded,
                "user2user_decoded" : self.user2user_decoded,
                "anime2anime_encoded" : self.anime2anime_encoded,
                "anime2anime_decoded" : self.anime2anime_decoded
            }
            for key, value in artifacts.items():
                joblib.dump(value, os.path.join(self.output_dir,f"{key}.pkl"))
                logger.info(f"{key} saved sucessfully in processed directory")
                
            joblib.dump(self.X_train_array, X_TRAIN_ARRAY)
            joblib.dump(self.X_test_array, X_TEST_ARRAY)
            joblib.dump(self.y_train, Y_TRAIN)
            joblib.dump(self.y_test, Y_TEST)

            self.rating_df.to_csv(RATING_DF, index=False) 
            logger.info("all the training, testing data as well as rating_df.csv is saved now")
        except Exception as e:
            raise CustomException(f"Failed to save the artifacts {sys}") 
        
    def process_anime_data(self):
        try:
            df = pd.read_csv(ANIME_CSV)
            cols = ["MAL_ID", "Name", "Genres", "sypnopsis"]
            synopsis_df = pd.read_csv(ANIMESYNOPSIS_CSV, usecols=cols)
             
            df = df.replace("Unknown", np.nan)
            def getAnimeName(anime_id):
                try:
                    name = df[df.anime_id == anime_id].eng_version.values[0]
                    if name is np.nan:
                        name = df[df.anime_id == anime_id].Name.values[0]
                except:
                    print("Error")
                return name 
            df['anime_id'] = df['MAL_ID']
            df['eng_version'] = df['English name']
            df['eng_version'] = df.anime_id.apply(lambda x: getAnimeName(x))
            df.sort_values(by = ["Score"], inplace = True, ascending = False, kind = "quicksort", na_position = "last")
            df = df[["anime_id", "eng_version", "Score", "Genres", "Type", "Episodes", "Premiered", "Members"]]
            df.to_csv(DF, index=False) 
            synopsis_df.to_csv(SYNOPSIS_DF, index=False)
            logger.info("df and synopsis_df saved sucessfully")
        except Exception as e:
            raise CustomException(f"Failed to save df and synopsis_df {sys}")      
        
    def run(self):
        try:
            self.load_data(usecols=["user_id", "anime_id", "rating"])
            self.filter_users()
            self.scale_ratings()
            self.encode_data()
            self.split_data()
            self.save_artifacts()
            self.process_anime_data()
            logger.info("Data processing pipeline run sucessfully")
        except Exception as e:
            raise CustomException(f"Failed to process the pipeline run {sys}") 
        
if __name__=="__main__":
    data_processor = DataProcessor(ANIMELIST_CSV, PROCESSED_DIR)
    data_processor.run()
            
                   





















































































