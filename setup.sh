#!/bin/bash

# 環境変数を設定してライセンスに自動同意
export ACCEPT_EULA=Y

# パッケージリストを更新
apt-get update 

# Microsoft ODBC Driver 18 をインストール
apt-get install -y msodbcsql18 unixodbc unixodbc-dev
