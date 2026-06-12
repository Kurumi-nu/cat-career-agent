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

Cloudflare Pages の画面から GitHub リポジトリを接続します。

```text
Repository: Kurumi-nu/cat-career-agent
Production branch: main
Build command: 空欄
Build output directory: public
```

接続後、`main` ブランチにpushするとCloudflare Pagesが自動でデプロイします。

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
