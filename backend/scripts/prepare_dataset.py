import requests
import pandas as pd
from tqdm import tqdm
import os

os.makedirs("data", exist_ok=True)

def fetch_surah(surah_id):
    ayahs = []
    for ayah_id in range(1, 300):  # Try up to 299 ayahs
        url = f"https://quranenc.com/api/v1/translation/aya/english_saheeh/{surah_id}/{ayah_id}"
        response = requests.get(url)
        if response.status_code != 200:
            break  # No more ayahs in this surah

        json_data = response.json()
        if "result" not in json_data:
            break  # Unexpected response

        result = json_data["result"]
        ayahs.append({
            "surah": surah_id,
            "ayah": result.get("verse_id", ayah_id),
            "arabic_text": result.get("arabic_text", ""),
            "english_text": result.get("translation", "")
        })

    return ayahs

def build_dataset():
    all_ayahs = []
    for surah_id in tqdm(range(1, 115)):  # Surah 1 to 114
        ayahs = fetch_surah(surah_id)
        all_ayahs.extend(ayahs)

    df = pd.DataFrame(all_ayahs)
    df.to_csv("data/ayah_dataset.csv", index=False)
    print("✅ Saved dataset to data/ayah_dataset.csv")

if __name__ == "__main__":
    build_dataset()
