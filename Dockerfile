FROM python:3.10

WORKDIR /app

# コピー
COPY . /app

# 依存関係
RUN pip install -r requirements.txt

# Render の PORT を渡す（ダミーWebサーバーに必要）
ENV PORT=3000

# Bot 起動
CMD ["python", "bot.py"]
