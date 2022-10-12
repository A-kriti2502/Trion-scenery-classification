from django.apps import AppConfig
import html
import pathlib
import os
from tensorflow.keras.models import model_from_json
from django.conf import settings


class MlConfig(AppConfig):
    name = 'ml'
    # path = os.path.join(settings.MODELS, "Terrain_model.h5")
    # path1 = os.path.join(settings.MODELS, "Terrain_model/variables")

    # json_file = open(path1, 'r')
    # loaded_model_json = json_file.read()
    # json_file.close()
    # loaded_model = model_from_json(loaded_model_json)
    # loaded_model.load_weights(path)