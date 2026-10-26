import os

BASE_DIR = "/content/drive/MyDrive/forex_institutional_agent"
DATA_DIR = os.path.join(BASE_DIR, "logs_and_backtest", "history_db")

# إعدادات نموذج Ollama المحلي مع اعتماد نموذج علام (Allam)
OLLAMA_HOST = "http://localhost:11434"
# يمكنك استبدال اسم النموذج بالاسم الدقيق المحمل لديك في Ollama (مثل "allam" أو "ibm/allam")
OLLAMA_MODEL = "allam"  

ASSETS_CONFIG_PATH = os.path.join(BASE_DIR, "config", "assets.json")
