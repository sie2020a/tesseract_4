# input_user_info.py（本体）
# streamlit run input_user_info.py

import streamlit as st
from file_io import load_profiles
from screens import nutrition_view, diet_support, activity_input, main_screen, weight_input, weight_log

# if "screen" not in st.session_state:
#     st.session_state.screen = "main"

profiles = load_profiles()
st.session_state["profiles"] = profiles

menu = st.sidebar.radio("📌 機能メニュー", [
    "🩺 メイン画面",
    "🔥 ダイエット支援",
    "🏃‍♀️ 運動記録の入力",
    "⚖️ 体重の記録", 
    "📈 グラフ", 
    "🥦 あなたの理想 各種栄養素 一覧"
])

screen_map = {
    "🩺 メイン画面": "main",
    "🔥 ダイエット支援": "diet_support",
    "🏃‍♀️ 運動記録の入力": "activity_input",
    "⚖️ 体重の記録": "weight_input", 
    "📈 グラフ": "weight_log", 
    "🥦 あなたの理想 各種栄養素 一覧": "nutrition_view"
}

st.session_state.screen = screen_map[menu]

if st.session_state.screen == "main":
    main_screen.show(profiles)
elif st.session_state.screen == "diet_support":
    diet_support.show(profiles)
elif st.session_state.screen == "activity_input":
    activity_input.show(profiles)
elif st.session_state.screen == "weight_input":
    weight_input.show(profiles)
elif st.session_state.screen == "weight_log":
    weight_log.show(profiles)
elif st.session_state.screen == "nutrition_view":
    nutrition_view.show()