import streamlit as st
from datetime import datetime, date
from file_io import save_profiles

def show(profiles):
    st.title("⚖️ 体重の記録と履歴表示")
    selected_user = st.session_state.get("selected_user")

    if not selected_user or selected_user not in profiles:
        st.warning("まず既存ユーザーを選択してください。")
        return

    user = profiles[selected_user]
    selected_user = st.session_state.get("selected_user")
    st.write(f"### {selected_user} さん")


    # 記録日と時刻を選択（未来日不可）
    today = date.today()
    input_date = st.date_input("記録日を選択", value=today, max_value=today)
    input_time = st.text_input("記録時刻（例：18:30）", value=datetime.now().strftime("%H:%M"))
    date_str = input_date.isoformat()

    # 入力欄
    weight = st.number_input("体重（kg）", min_value=0.0, format="%.1f")
    submit = st.button("保存する")

    if submit:
        try:
            combined_timestamp = datetime.strptime(f"{date_str} {input_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            st.error("⚠️ 時刻形式が不正です（例：18:30）")
            return

        if "health_data" not in user:
            user["health_data"] = {}
        if date_str not in user["health_data"]:
            user["health_data"][date_str] = {}

        if "weight_log" not in user["health_data"][date_str]:
            user["health_data"][date_str]["weight_log"] = []

        log_entry = {
            "timestamp": combined_timestamp.strftime("%Y-%m-%d %H:%M"),
            "weight": weight
        }
        user["health_data"][date_str]["weight_log"].append(log_entry)

        user["health_data"][date_str]["weight"] = weight

        height = user.get("height")
        if height:
            bmi = weight / ((height / 100) ** 2)
            user["health_data"][date_str]["bmi"] = round(bmi, 2)
            st.success(f"✅ BMI: {bmi:.2f}")
        else:
            st.warning("※ 身長が未登録のため、BMIは計算できません。")

        save_profiles(profiles)
        st.success(f"{date_str} の体重を保存しました。")

    if "health_data" in user:
        st.subheader("📊 体重の履歴")
        records = user["health_data"]
        for d in sorted(records.keys(), reverse=True):
            entries = records[d].get("weight_log")
            if entries:
                st.markdown(f"#### {d}")
                for i, entry in enumerate(sorted(entries, key=lambda x: x["timestamp"], reverse=True)):
                    ts = entry["timestamp"]
                    w = entry["weight"]
                    bmi = records[d].get("bmi")
                    col1, col2 = st.columns([5,1])
                    with col1:
                        st.write(f"🕒 {ts} - 体重: {w:.1f}kg / BMI: {bmi if bmi else 'N/A'}")
                    with col2:
                        if st.button("🗑️ 削除", key=f"delete_{d}_{i}"):
                            user["health_data"][d]["weight_log"].remove(entry)
                            save_profiles(profiles)
                            st.success("❌ 削除しました。")
                            st.rerun()
