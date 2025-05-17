import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib import rcParams
from file_io import save_profiles

# フォント設定（日本語環境で利用可能なら）
try:
    rcParams['font.family'] = 'IPAexGothic'  # 環境に応じて変更可
except:
    pass

# メイン処理
def show(profiles):
    st.title("⚖️ 体重記録・推移グラフ")

    selected_user = st.session_state.get("selected_user")
    if not selected_user or selected_user not in profiles:
        st.warning("まず既存ユーザーを選択してください。")
        return

    user = profiles[selected_user]

    # 期間選択
    st.subheader("📅 表示期間")
    option = st.radio("期間を選んでください", ["1年", "1ヶ月", "1週間", "カスタム"])

    end_date = datetime.today().date()

    if option == "1年":
        start_date = end_date - timedelta(days=365)
    elif option == "1ヶ月":
        start_date = end_date - timedelta(days=30)
    elif option == "1週間":
        start_date = end_date - timedelta(days=7)
    else:
        start_date = st.date_input("開始日", value=end_date - timedelta(days=30), key="custom_start")
        end_date = st.date_input("終了日", value=end_date, key="custom_end")

    # 目標体重入力
    st.subheader("🎯 目標体重ライン")
    target_weight = st.number_input("目標体重 (kg)", min_value=0.0, format="%.1f")

    # データ取得
    weight_records = []
    dates = []
    fat_percent_records = []

    for d in sorted(user.get("health_data", {}).keys()):
        date_obj = datetime.strptime(d, "%Y-%m-%d").date()
        if start_date <= date_obj <= end_date:
            day_data = user["health_data"][d]
            w = day_data.get("weight")
            fat = day_data.get("fat_percent")  # 将来追加用
            if w:
                dates.append(date_obj)
                weight_records.append(w)
                fat_percent_records.append(fat if fat else None)

    if dates:
        fig, ax1 = plt.subplots()
        ax1.plot(dates, weight_records, marker='o', label='Weight (kg)')
        ax1.set_ylabel('Weight (kg)')
        ax1.tick_params(axis='x', rotation=45)

        if target_weight > 0:
            ax1.axhline(y=target_weight, color='red', linestyle='--', label=f'Target {target_weight:.1f}kg')

        # 将来的な体脂肪率の追加枠
        if any(fat_percent_records):
            ax2 = ax1.twinx()
            ax2.plot(dates, fat_percent_records, marker='x', color='orange', label='Body Fat (%)')
            ax2.set_ylabel('Body Fat (%)')

        fig.tight_layout()
        plt.legend()
        st.pyplot(fig)
    else:
        st.info("指定された期間内に体重記録がありません。")
