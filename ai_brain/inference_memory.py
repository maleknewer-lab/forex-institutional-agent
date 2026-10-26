import os

class InferenceMemoryEngine:
    def __init__(self, db_path=None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(base_dir, "..", "data", "inference_memory.db")
        else:
            self.db_path = db_path
            
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        if not os.path.exists(self.db_path):
            open(self.db_path, 'a').close()