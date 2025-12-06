import time
from Front import Interface
from Streaming.Streaming_to_zarr import main_loop
from Streaming.zarr_to_algorithms import main_to_loop
from Zarr.utils_zarr_corrected import ALGORITMOS_VISIBLES, STORE_PATH, escribir_prediccion
from main import iniciar_streaming_en_thread

iniciar_streaming_en_thread()