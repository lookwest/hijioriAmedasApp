#!/bin/bash
# スクリプトがあるディレクトリに移動
cd "$(dirname "$0")"

# 気象データを更新
python3 update_weather_data.py

# geminiをフルパスで実行し、更新されたデータを読み込む
/Users/ryu1hysk/.npm-global/bin/gemini @hijioriAmedas_data_utf8.csv
