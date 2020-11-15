from messaging.handlers.pv_data_generation_handler import PvDataGenerationHandler
SIMULATOR_QUEUE = "meter_load"


HANDLER_MAPPING = {
    "meter_data": [PvDataGenerationHandler]
}
