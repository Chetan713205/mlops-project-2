from utils.helpers import *
from config.paths_config import *
from pipeline.prediction_pipeline import hybrid_recommendation

print(getAnimeFrame(40028, DF))
print(find_similar_users(11880, USER_WEIGHTS_PATH, USER2USER_ENCODED, USER2USER_DECODED))
print(get_user_preferences(11880, RATING_DF, DF))
print(hybrid_recommendation(11880))