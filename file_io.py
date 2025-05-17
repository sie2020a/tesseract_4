# file_io.py (json入出力 + CSV読み込み)
import json
import os
import pandas as pd
from config import SAVE_FILE, NUTRITION_CSV_FILE

def load_profiles():
    return json.load(open(SAVE_FILE, encoding="utf-8")) if os.path.exists(SAVE_FILE) else {}

def save_profiles(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_nutrition_data():
    """
    栄養データCSVを読み込む関数
    """
    if not os.path.exists(NUTRITION_CSV_FILE):
        raise FileNotFoundError(f"{NUTRITION_CSV_FILE} が見つかりません。")

    df = pd.read_csv(NUTRITION_CSV_FILE)
    df = df.fillna("NA")  # 欠損値があるときに 'NA' に置き換え
    return df.set_index("年齢区分")
