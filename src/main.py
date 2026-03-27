import os
import yaml
import traceback
from LopmConnector import LopmConnector

config_file_path = os.path.dirname(os.path.abspath(__file__)) + "/config.yml"

config = (
    yaml.load(open(config_file_path), Loader=yaml.FullLoader)
    if os.path.isfile(config_file_path)
    else {}
)


if __name__ == "__main__":
    try:
        connector = LopmConnector(config=config)
        connector.run()
    except Exception as e:
        print(f"Произошла ошибка: {type(e).__name__} — {e}")
        traceback.print_exc()



