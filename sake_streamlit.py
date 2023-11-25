import streamlit as st
import requests

# Streamlitアプリの設定
st.title("日本酒銘柄おすすめアプリ")
st.header("類似する日本酒銘柄を見つけましょう")

# ユーザー入力
sake_name = st.text_input("日本酒の銘柄名を入力してください:", "")

# FastAPIエンドポイント（このURLをデプロイされたFastAPIのURLに置き換える）
FASTAPI_ENDPOINT = "http://localhost:8000/recommendations"

if sake_name:
    # FastAPIサーバーにリクエストを送信
    response = requests.get(f"{FASTAPI_ENDPOINT}/{sake_name}")

    if response.status_code == 200:
        recommendations = response.json()['recommendations']
        st.subheader("おすすめの日本酒銘柄:")
        for rec in recommendations:
            st.write(f"{rec[0]}（類似度スコア: {rec[1]:.2f}）")
    else:
        st.error("指定された銘柄は見つかりませんでした。別の銘柄名を試してください。")
