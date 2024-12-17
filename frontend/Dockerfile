FROM node:18-alpine

WORKDIR /app

# pnpmのインストール
RUN corepack enable && corepack prepare pnpm@latest --activate

# package.jsonのコピー
COPY package.json ./

# クリーンインストール
RUN pnpm install --shamefully-hoist

# ソースコードのコピー
COPY . .

EXPOSE 5173

ENV NODE_ENV=development

# 明示的にviteを実行
CMD ["pnpm", "exec", "vite", "--host", "0.0.0.0"]