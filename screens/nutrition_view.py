# screens/nutrition_view.py
import streamlit as st
import pandas as pd

def get_user_age_group(user):
    return user.get("selected_value")

def show():
    st.title("🥦 あなたの理想 各種栄養素 一覧")

    selected_user = st.session_state.get("selected_user")
    profiles = st.session_state.get("profiles")

    if not selected_user or not profiles or selected_user not in profiles:
        st.warning("まず既存ユーザーを選択してください。")
        return

    user = profiles[selected_user]
    age_group = get_user_age_group(user)

    st.write(f"### 👤 ユーザー: {selected_user}")
    st.write(f"🗂️ 区分: {age_group}")

    try:
        df = pd.read_csv("data/nutrition_targets.csv")

        target_row = df[df["年齢区分"] == age_group]
        if target_row.empty:
            st.warning("⚠️ 対応するデータが見つかりませんでした。")
            return

        # データ整形
        data = target_row.drop(columns=["id", "年齢区分"]).T.reset_index()
        data.columns = ["項目", "値"]

        # 栄養素ごとにまとめる
        nutrients = {}
        for _, row in data.iterrows():
            nutrient = row["項目"].replace("目標", "").replace("最大", "").strip()
            value = row["値"]
            if "目標" in row["項目"]:
                nutrients.setdefault(nutrient, {})["目標値"] = value
            elif "最大" in row["項目"]:
                nutrients.setdefault(nutrient, {})["上限値"] = value

        # 表示用データフレーム作成
        final_df = pd.DataFrame([{
            "栄養素": k,
            "目標値": v.get("目標値", ""),
            "上限値": v.get("上限値", "")
        } for k, v in nutrients.items()]).sort_values(by="栄養素")

        st.subheader(f"🌱 栄養素目標と上限（{age_group}）")

        # 表を見やすく表示
        st.dataframe(
            final_df.set_index("栄養素"),
            use_container_width=True,
            height=500
        )

    except FileNotFoundError:
        st.error("❌ CSVファイルが見つかりません。`data/nutrition_targets.csv` を配置してください。")
    except Exception as e:
        st.error(f"⚠️ エラーが発生しました: {e}")
