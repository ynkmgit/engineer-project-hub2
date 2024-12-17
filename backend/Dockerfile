FROM python:3.11-slim

WORKDIR /app

# Poetry のインストール
RUN pip install poetry

# Poetry の仮想環境を無効化（Dockerコンテナ内では不要）
RUN poetry config virtualenvs.create false

# pyproject.toml のみをコピー
COPY pyproject.toml ./

# poetry.lock が存在しない場合でも進めるように
RUN poetry install --no-root || poetry install

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]