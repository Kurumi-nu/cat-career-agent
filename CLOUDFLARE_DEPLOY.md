# Cloudflare Deploy

このプロジェクトは Cloudflare Pages + Functions + D1 でデプロイします。

## 1. Wrangler を使える環境でログイン

```bash
npm install -g wrangler
wrangler login
```

## 2. D1 データベースを作成

```bash
wrangler d1 create miranoa-db
```

表示された `database_id` を `wrangler.toml` の `REPLACE_WITH_D1_DATABASE_ID` に貼り付けます。

## 3. SQLite互換DBへ初期データを投入

```bash
wrangler d1 execute miranoa-db --file=./schema.sql
```

## 4. Pagesへデプロイ

```bash
wrangler pages deploy public --project-name=miranoa-archive
```

Cloudflare DashboardでPagesプロジェクトにD1 bindingを追加する場合は、binding名を `DB`、databaseを `miranoa-db` にしてください。

## GitHub経由で自動デプロイする場合

このリポジトリには GitHub Actions の自動デプロイ設定があります。

```text
.github/workflows/cloudflare-pages.yml
```

GitHubのリポジトリ設定で、以下のActions Secretsを登録してください。

```text
CLOUDFLARE_API_TOKEN
CLOUDFLARE_ACCOUNT_ID
```

`CLOUDFLARE_API_TOKEN` は Cloudflare Pages の編集とデプロイができる権限を持つAPI tokenを使います。

Secrets登録後、`main` ブランチにpushすると自動で以下が実行されます。

```bash
wrangler pages deploy public --project-name=miranoa-archive
```

D1は自動デプロイ前に一度だけ作成・初期投入してください。

```bash
wrangler d1 create miranoa-db
wrangler d1 execute miranoa-db --file=./schema.sql
```

Cloudflare Pages側のD1 bindingは次の値にします。

```text
Variable name: DB
D1 database: miranoa-db
```

## 公開される主なURL

- `/`
- `/places/1`
- `/api/places`
- `/api/places/1`
- `/api/events`
- `/api/stats`
