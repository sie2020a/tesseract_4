# screens/main_screen.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from file_io import save_profiles, load_nutrition_data

AGE_GROUPS_MEN = [
    {"max_age": 0.5, "label": "男性0-5(月)"},
    {"max_age": 0.9, "label": "男性6-11(月)"},
    {"max_age": 2, "label": "男性1-2(歳)"},
    {"max_age": 5, "label": "男性3-5(歳)"},
    {"max_age": 7, "label": "男性6-7(歳)"},
    {"max_age": 9, "label": "男性8-9(歳)"},
    {"max_age": 11, "label": "男性10-11(歳)"},
    {"max_age": 14, "label": "男性12-14(歳)"},
    {"max_age": 17, "label": "男性15-17(歳)"},
    {"max_age": 29, "label": "男性18-29(歳)"},
    {"max_age": 49, "label": "男性30-49(歳)"},
    {"max_age": 64, "label": "男性50-64(歳)"},
    {"max_age": 74, "label": "男性65-74(歳)"},
    {"max_age": 150, "label": "男性75以上(歳)"}
]

AGE_GROUPS_WOMEN = [
    {"max_age": 0.5, "label": "女性0-5(月)"},
    {"max_age": 0.9, "label": "女性6-11(月)"},
    {"max_age": 2, "label": "女性1-2(歳)"},
    {"max_age": 5, "label": "女性3-5(歳)"},
    {"max_age": 7, "label": "女性6-7(歳)"},
    {"max_age": 9, "label": "女性8-9(歳)"},
    {"max_age": 11, "label": "女性10-11(歳)"},
    {"max_age": 14, "label": "女性12-14(歳)"},
    {"max_age": 17, "label": "女性15-17(歳)"},
    {"max_age": 29, "label": "女性18-29(歳)"},
    {"max_age": 49, "label": "女性30-49(歳)"},
    {"max_age": 64, "label": "女性50-64(歳)"},
    {"max_age": 74, "label": "女性65-74(歳)"},
    {"max_age": 150, "label": "女性75以上(歳)"}
]

PREGNANT_LABELS = {
    "妊婦初期（〜28週）": {"young": "妊婦初期-28週まで18-29歳", "older": "妊婦初期-28週まで30-49歳"},
    "妊婦後期（28週以降）": {"young": "妊婦28週以降18-29歳", "older": "妊婦28週以降30-49歳"}
}

BREASTFEEDING_LABELS = {
    "young": "授乳中 18-29歳",
    "older": "授乳中 30-49歳"
}

def calculate_age(birth_date):
    today = date.today()
    diff = relativedelta(today, birth_date)
    age_years = diff.years + diff.months / 12
    return round(age_years, 2)

def determine_selected_value(gender, age, menstruation, pregnancy, breastfeeding):
    if age < 1:
        age_in_months = age * 12
        if gender == "男性":
            return "男性0-5(月)" if age_in_months <= 5 else "男性6-11(月)"
        else:
            return "女性0-5(月)" if age_in_months <= 5 else "女性6-11(月)"
    if gender == "男性":
        for group in AGE_GROUPS_MEN:
            if age <= group["max_age"]:
                return group["label"]
    elif gender == "女性":
        if pregnancy in PREGNANT_LABELS:
            return PREGNANT_LABELS[pregnancy]["young"] if age <= 29 else PREGNANT_LABELS[pregnancy]["older"]
        elif breastfeeding == "はい":
            return BREASTFEEDING_LABELS["young"] if age <= 29 else BREASTFEEDING_LABELS["older"]
        else:
            for group in AGE_GROUPS_WOMEN:
                if age <= group["max_age"]:
                    is_no_menstruation = menstruation == "ない" and age >= 10
                    return group["label"] + (" N" if is_no_menstruation else "")
    return None

def show(profiles):
    st.title("🩺 健康プロフィール登録・管理")
    nutrition_df = load_nutrition_data()

    if st.session_state.get("updated_user"):
        st.success(f"✅ {st.session_state.updated_user} さんのプロフィールを更新しました。")
        del st.session_state.updated_user

    if st.session_state.get("deleted_user"):
        st.success(f"🗑️ {st.session_state.deleted_user} さんのデータを削除しました。")
        del st.session_state.deleted_user

    mode = st.radio("操作を選んでください", ["📂 既存ユーザー選択", "✏️ ユーザーを編集", "🆕 新規ユーザー登録"])

    if mode == "📂 既存ユーザー選択":
        default_index = 0
        if "selected_user" in st.session_state and st.session_state["selected_user"] in profiles:
            default_index = list(profiles.keys()).index(st.session_state["selected_user"])

        selected_user = st.selectbox("ユーザーを選択", list(profiles.keys()) if profiles else [], index=default_index)

        if selected_user:
            user = profiles[selected_user]
            birth_date = date.fromisoformat(user["birth_date"])
            age = calculate_age(birth_date)

            selected_value = determine_selected_value(
                user["gender"],
                age,
                user.get("menstruation"),
                user.get("pregnancy"),
                user.get("breastfeeding")
            )

            user["age"] = age
            user["selected_value"] = selected_value
            profiles[selected_user] = user
            save_profiles(profiles)

            st.session_state["selected_user"] = selected_user
            st.session_state["profiles"] = profiles

            st.write(f"### {selected_user} さんのプロフィール")
            profile_items = {
                "性別": user.get("gender"),
                "生年月日": user.get("birth_date"),
                "年齢": f"{int(age)} 歳",
                "身長": f"{user.get('height', '未設定')} cm",
                "妊娠状況": user.get("pregnancy", "-"),
                "生理": user.get("menstruation", "-"),
                "授乳中": user.get("breastfeeding", "-"),
                "栄養区分": selected_value
            }

            for key, value in profile_items.items():
                st.markdown(f"**{key}:** {value}")
                
# =====栄養目標データの表示======
            # if selected_value:
            #     normalized_value = selected_value.replace("(歳)", "").replace(" ", "").replace("女性", "f").replace("男性", "m")
            #     found = False
            #     for idx in nutrition_df.index:
            #         if normalized_value in idx.replace(" ", "").replace("女性", "f").replace("男性", "m"):
            #             st.subheader("📝 栄養目標データ")
            #             nutrition_data = nutrition_df.loc[idx].to_dict()
            #             readable_data = {k: ("" if str(v).strip().upper() == "NA" else v) for k, v in nutrition_data.items()}
            #             st.dataframe(pd.DataFrame(readable_data.items(), columns=["項目", "目標値"]))
            #             found = True
            #             break
            #     if not found:
            #         st.warning(f"⚠️ {selected_value} に該当する栄養データが見つかりません。")
            # else:
            #     st.warning("⚠️ 栄養区分情報が見つかりません。")

                
                
    elif mode == "✏️ ユーザーを編集":
        selected_user = st.selectbox("編集したいユーザーを選択", list(profiles.keys()) if profiles else [], key="edit_select")
        if selected_user:
            user = profiles[selected_user]
            with st.form("edit_user_form"):
                st.subheader(f"✏️ {selected_user} さんの情報を編集")
                gender = st.radio("性別", ["男性", "女性"], index=0 if user["gender"] == "男性" else 1)
                # 生年月日の年範囲を拡張
                birth_date = st.date_input(
                    "生年月日",
                    value=date.fromisoformat(user["birth_date"]),
                    min_value=date(1900, 1, 1),
                    max_value=date.today()
                )

                menstruation = pregnancy = breastfeeding = None
                if gender == "女性":
                    pregnancy = st.selectbox("妊娠状況", ["なし", "妊婦初期（〜28週）", "妊婦後期（28週以降）"], index=["なし", "妊婦初期（〜28週）", "妊婦後期（28週以降）"].index(user.get("pregnancy", "なし")))

                    if pregnancy != "なし":
                        st.markdown("**妊娠中のため生理は自動的に 'ない' と設定されます。**")
                        menstruation = "ない"
                    else:
                        menstruation = st.radio("生理", ["ある", "ない"], index=0 if user.get("menstruation") == "ある" else 1)

                    breastfeeding = st.radio("授乳中", ["はい", "いいえ"], index=0 if user.get("breastfeeding") == "はい" else 1)

                height = st.number_input("身長（cm）", min_value=0.0, value=user.get("height") or 0.0, format="%.1f")
                save_clicked = st.form_submit_button("保存する")


            if save_clicked:
                age = calculate_age(birth_date)
                selected_value = determine_selected_value(gender, age, menstruation, pregnancy, breastfeeding)
                updated_profile = {
                    "gender": gender,
                    "birth_date": birth_date.isoformat(),
                    "age": age,
                    "height": height,
                    "selected_value": selected_value,
                    "timestamp": datetime.now().isoformat()
                }

                if gender == "女性":
                    updated_profile.update({
                        "menstruation": menstruation,
                        "pregnancy": pregnancy,
                        "breastfeeding": breastfeeding
                    })

                profiles[selected_user] = updated_profile
                save_profiles(profiles)
                st.session_state.updated_user = selected_user
                st.rerun()
    

    elif mode == "🆕 新規ユーザー登録":
        st.subheader("新規ユーザー登録")
        with st.form("new_user_form"):
            name = st.text_input("👤 ユーザー名（ニックネーム可）")
            gender = st.radio("性別", ["男性", "女性"])
            birth_date = st.date_input("生年月日", min_value=date(1900, 1, 1), max_value=date.today())
            height = st.number_input("身長（cm）", min_value=0.0, format="%.1f")

            menstruation = pregnancy = breastfeeding = None
            if gender == "女性":
                menstruation = st.radio("生理", ["ある", "ない"])
                pregnancy = st.selectbox("妊娠状況", ["なし", "妊婦初期（〜28週）", "妊婦後期（28週以降）"])
                breastfeeding = st.radio("授乳中", ["はい", "いいえ"], index=1)

            submitted = st.form_submit_button("登録")

        if submitted and name:
            age = calculate_age(birth_date)
            selected_value = determine_selected_value(gender, age, menstruation, pregnancy, breastfeeding)
            new_profile = {
                "gender": gender,
                "birth_date": birth_date.isoformat(),
                "age": age,
                "height": height,
                "selected_value": selected_value,
                "timestamp": datetime.now().isoformat()
            }

            if gender == "女性":
                new_profile.update({
                    "menstruation": menstruation,
                    "pregnancy": pregnancy,
                    "breastfeeding": breastfeeding
                })

            profiles[name] = new_profile
            save_profiles(profiles)
            st.success(f"💾 {name} さんのプロフィールを保存しました。")