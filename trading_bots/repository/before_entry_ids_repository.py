import logging
import sys
import json


class BeforeEntryIdsRepository:

    def __init__(self, before_entry_ids_json_path: str):
        self.before_entry_ids_json_path = before_entry_ids_json_path

    def load(self) -> list:
        try:
            logging.debug("Start loading before entry ids list")
            with open(self.before_entry_ids_json_path) as f:
                content = f.read()
                if content:
                    return json.loads(content)
                logging.debug(f"Loaded before entry ids list: {content}")
        except Exception as e:
            logging.error(f"Failed to load before entry ids list: {str(e)}")
            sys.exit(-1)

    def save(self, before_entry_ids: list) -> None:
        try:
            logging.debug("Start saving before entry ids list")
            with open(self.before_entry_ids_json_path, 'w') as f:
                json.dump(before_entry_ids, f, indent=4)
        except Exception as e:
            logging.error(f"Failed to save before entry ids list: {str(e)}")
            sys.exit(-1)
