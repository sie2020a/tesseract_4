# screens/diet_support.py (# BMI計算によるダイエット支援)

import streamlit as st
import pandas as pd
from datetime import datetime, date
# from file_io import save_profiles

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
    st.title("🔥 ダイエット支援")

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
        return

    height = user.get("height")

    st.write(f"### {selected_user} さん")

    # BMIの計算と表示
    if height and latest_weight:
        bmi = latest_weight / ((height / 100) ** 2)
        st.write(f"体重: {latest_weight:.2f} kg")
        st.write(f"BMI: {bmi:.2f}")
    else:
        st.warning("メイン画面のユーザー編集から、身長を入力してください。")

    # 基礎代謝（BMR）の計算
    gender = user.get("gender")
    age = user.get("age")

    bmr = None
    if all(isinstance(val, (int, float)) and val > 0 for val in [latest_weight, height, age]):
        if gender == "男性":
            bmr = 13.397 * latest_weight + 4.799 * height - 5.677 * age + 88.362
        elif gender == "女性":
            bmr = 9.247 * latest_weight + 3.098 * height - 4.33 * age + 447.593

        if bmr:
            st.write(f"基礎代謝量: {bmr:.2f} kcal/日")
        else:
            st.warning("性別が未設定または無効です。")

    # 目標体重減少の設定
    target_weight_loss = st.number_input("1ヶ月で痩せたい体重 (kg)", min_value=0.0, step=0.1)
    if target_weight_loss > 0:
        daily_calorie_deficit = target_weight_loss * 7200 / 30 * -1
        st.success(f"1日あたりのカロリー抑制量: {daily_calorie_deficit:.2f} kcal")

    if latest_weight:
        max_target_weight_loss = latest_weight * 0.05
        st.warning(f"急激な減量はリバウンドの原因になります。目標体重減少の上限は {max_target_weight_loss:.2f} kg です。")

    # 運動消費カロリー計算
    if "health_data" in user:
        st.subheader("📅 日別消費カロリー")
        selected_summary_date = st.date_input("消費カロリー集計対象日", value=datetime.now().date(), key="summary_date")
        date_str = selected_summary_date.isoformat()

        total_activity_calories = 0
        if date_str in user["health_data"]:
            activities = user["health_data"][date_str].get("activities", [])
            total_activity_calories = sum(act.get("calories", 0) for act in activities)

        st.info(f"📊 合計運動消費カロリー: {total_activity_calories:.1f} kcal")

        # 基礎代謝 + 運動消費量
        if bmr is not None:
            total_calories = bmr + total_activity_calories
            st.success(f"基礎代謝 + 運動消費量: {total_calories:.2f} kcal")
