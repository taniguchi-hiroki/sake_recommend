from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# CSVファイルのパス（サーバーでのファイルの場所に応じて変更してください）
csv_file_path = 'https://raw.githubusercontent.com/taniguchi-hiroki/sake_recommend/main/sake_data.csv'

# CSVファイルを読み込む
sake_data = pd.read_csv(csv_file_path)

# TF-IDFベクトル化
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(sake_data['preprocessed_text'])

# 銘柄名とTF-IDFベクトルのマッピング
sake_names = sake_data['銘柄名'].tolist()
sake_to_tfidf = {name: tfidf_matrix[idx] for idx, name in enumerate(sake_names)}

def find_similar_sakes(sake_name, top_n=5):
    if sake_name not in sake_to_tfidf:
        return f"銘柄 '{sake_name}' はデータに存在しません。"

    sake_vector = sake_to_tfidf[sake_name]
    cosine_similarities = cosine_similarity(sake_vector, tfidf_matrix).flatten()
    similar_indices = np.argsort(-cosine_similarities)[1:top_n+1]  # 自分自身を除く

    similar_sakes = [(sake_names[idx], cosine_similarities[idx]) for idx in similar_indices]
    return similar_sakes

app = FastAPI()

class SakeRecommendation(BaseModel):
    sake_name: str
    recommendations: List[Tuple[str, float]]

@app.get("/recommendations/{sake_name}", response_model=SakeRecommendation)
def get_recommendations(sake_name: str):
    similar_sakes = find_similar_sakes(sake_name)
    if isinstance(similar_sakes, str):
        raise HTTPException(status_code=404, detail=similar_sakes)
    return {"sake_name": sake_name, "recommendations": similar_sakes}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the top page of the sake recommendation system!"}
