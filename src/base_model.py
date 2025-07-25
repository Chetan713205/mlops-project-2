from tensorflow.keras import layers 
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Activation, BatchNormalization, Input, Dot, Dense, Embedding, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
from utils.common_functions import read_yaml
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class BaseModel:
    def __init__(self, config_path):
        try:
            self.config = read_yaml(config_path)
            logger.info("Loaded configuration from config.yaml file")
        except Exception as e:
            raise CustomException("Error loading configuration", e)
        
    def RecommenderNet(self, n_user, n_anime):
        try: 
            embedding_size = self.config["model"]["embedding_size"]
            user = Input(name = "user", shape = [1])
            user_embedding = Embedding(name = "user_embedding", input_dim = n_user, output_dim = embedding_size)(user)
            anime = Input(name = "anime", shape = [1])
            anime_embedding = Embedding(name = "anime_embedding", input_dim = n_anime, output_dim = embedding_size)(anime)
            x = Dot(name = "dot_product", normalize = True, axes = 2)([user_embedding, anime_embedding])     
            x = Flatten()(x)     
            x = Dense(1, kernel_initializer = "he_normal")(x)
            x = BatchNormalization()(x)  # Normalizing the output
            x = Activation("sigmoid")(x)
            
            model = Model(inputs = [user, anime], outputs = x)
            model.compile(
                loss=self.config["model"]["loss"],
                optimizer=self.config["model"]["optimizer"],
                metrics=self.config["model"]["metrics"] 
            )
            logger.info("Model created sucessfully")
            return model
        except Exception as e:
            logger.error("Error occured model creation")
    