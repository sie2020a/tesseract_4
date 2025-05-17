# screens/activity_input.py

import streamlit as st
import pandas as pd
from datetime import datetime, date
from file_io import save_profiles

# 最新体重を取得する関数
def get_latest_weight(user):
    weight = None
    if "health_data" in user:
        for day in sorted(user["health_data"].keys(), reverse=True):
            day_data = user["health_data"][day]
            if "weight" in day_data and isinstance(day_data["weight"], (int, float)):
                weight = day_data["weight"]
                break
    return weight

# メイン処理
def show(profiles):
    st.title("\U0001F3C3‍♀️ 運動記録の入力と消費カロリー計算")

    selected_user = st.session_state.get("selected_user")
    if not selected_user or selected_user not in profiles:
        st.warning("まず既存ユーザーを選択してください。")
        return

    user = profiles[selected_user]

    # ページ表示時に最新体重を取得して表示
    latest_weight = get_latest_weight(user)
    if latest_weight and latest_weight > 0:
        st.success(f"🔎 現在の体重: {latest_weight:.1f} kg")
    else:
        st.warning("⚠️「⚖️体重の記録」メニューから、体重を入力してください。")
        latest_weight = None

    activity_df = pd.DataFrame([
        {"カテゴリ": "エクササイズ", "活動": "ストレッチ/ハタヨガ", "METs": 2.5},
        {"カテゴリ": "学校・会社", "活動": "一般的なオフィスワーク（座位）", "METs": 1.5},
        {"カテゴリ": "エクササイズ", "活動": "ランニング:8.0km/時", "METs": 8.0},
    ])

    category = st.selectbox("カテゴリ選択（任意）", ["すべて"] + sorted(activity_df["カテゴリ"].unique()))
    filtered = activity_df if category == "すべて" else activity_df[activity_df["カテゴリ"] == category]
    activity = st.selectbox("活動を検索して選択してください", filtered["活動"].tolist())

    time_min = st.number_input("活動時間（分）", min_value=0.0, format="%.1f")

    if time_min > 0 and latest_weight:
        custom_date = st.date_input("記録日", value=date.today())
        custom_time = st.text_input("記録時刻（例：18:30）", value=datetime.now().strftime("%H:%M"))
        try:
            combined_timestamp = datetime.strptime(f"{custom_date} {custom_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            st.error("⚠️ 記録時刻の形式が正しくありません。例：18:30")
            return

        mets = filtered[filtered["活動"] == activity].iloc[0]["METs"]
        calories = round(latest_weight * 1.05 * mets * time_min / 60, 1)
        st.success(f"\U0001F525 {activity} による消費カロリーは {calories:.1f} kcal（METs: {mets}）")

        if st.button("💾 この記録を保存する"):
            entry = {
                "timestamp": combined_timestamp.strftime("%Y-%m-%d %H:%M"),
                "activity": activity,
                "mets": mets,
                "time_min": time_min,
                "calories": calories
            }
            date_str = custom_date.isoformat()
            if "health_data" not in user:
                user["health_data"] = {}
            if date_str not in user["health_data"]:
                user["health_data"][date_str] = {}
            if "activities" not in user["health_data"][date_str]:
                user["health_data"][date_str]["activities"] = []
            user["health_data"][date_str]["activities"].append(entry)
            save_profiles(profiles)
            st.success("✅ 記録を保存しました。")
            st.rerun()

    if "health_data" in user:
        st.subheader("📅 運動記録履歴")
        for d in sorted(user["health_data"].keys(), reverse=True):
            activities = user["health_data"][d].get("activities")
            if activities:
                st.markdown(f"#### {d}")
                for i, act in enumerate(sorted(activities, key=lambda x: x["timestamp"], reverse=True)):
                    with st.expander(f"{act['timestamp']} - {act['activity']}"):
                        st.write(f"🕒 時間: {act['time_min']} 分")
                        st.write(f"🔥 カロリー: {act['calories']} kcal")
                        st.write(f"💪 METs: {act['mets']}")
                        if st.button("🗑️ 削除", key=f"delete_{d}_{i}"):
                            user["health_data"][d]["activities"].remove(act)
                            save_profiles(profiles)
                            st.success("❌ 記録を削除しました。")
                            st.rerun()
