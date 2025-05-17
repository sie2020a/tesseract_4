# Tesseract_4 健康管理アプリ
# 2025/05/10　時点

## 📁 プロジェクト構成

📁 Tesseract_4/
├── input_user_info.py          # メインアプリ本体
├── config.py                   # 設定
├── file_io.py                  # JSON入出力
├── README.md                   # 説明ドキュメント
├── .gitignore                  # Git管理外にしたいファイルを記載
│
├──📁 screens/                  # 各画面モジュール
│	├── activity_input.py      # 運動入力とカロリー計算画面
│	├── diet_support.py        # BMI計算によるダイエット支援
│	├── main_screen.py         # ユーザー登録と選択（メイン画面）
│	├── weight_input.py        # 体重記録
│	├── weight_log.py          # 体重グラフ表示
│	└── nutrition_view.py      # 栄養素の一覧表示
│
└──📁 data/                     # 保存データ
 	├── health_profiles.json
  └── nutrition_targets.csv


## ✅ 使用技術
- Python / Streamlit
- Google Sheets API
- JSONローカル保存

## 📝 今後の拡張予定
- METsデータの外部ファイル化
- CSVエクスポート機能
- UIのスタイル統一
