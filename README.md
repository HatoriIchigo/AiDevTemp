# AI駆動開発テンプレート（AiDevTemplate）

Claude Codeを使用したAI駆動開発のテンプレートプロジェクトです。
`~/.claude/`に配置することで、全プロジェクトで共通のカスタムコマンド・エージェント・開発ガイドラインを使用できます。

## 目次

- [概要](#概要)
- [セットアップ](#セットアップ)
- [主要ファイル](#主要ファイル)
- [カスタムコマンド一覧](#カスタムコマンド一覧)
- [エージェント一覧](#エージェント一覧)
- [ディレクトリ構成](#ディレクトリ構成)
- [開発ガイドライン](#開発ガイドライン)

---

## 概要

このテンプレートは、以下を提供します：

- **CLAUDE.md**: AI駆動開発のガイドライン・規約・ベストプラクティス
- **カスタムコマンド**: TDD実装、単体テスト生成、コンテキスト作成など
- **専門エージェント**: Python/Java専門家、コード探索、ドキュメント探索など
- **ディレクトリ構成規約**: backend/frontend/docs/pocなどの標準構成
- **Gitブランチ戦略**: release/fix/delete/refactorの命名規則

---

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <このリポジトリURL> ~/.claude
```

### 2. 既存プロジェクトへの適用

```bash
# プロジェクトルートで実行
cp ~/.claude/CLAUDE.md ./CLAUDE.md
```

### 3. プロジェクト固有設定の追加

[CLAUDE.md](CLAUDE.md) の「プロジェクトルートCLAUDE.mdの構成」に従って、プロジェクト固有の情報を追記してください。

---

## 主要ファイル

| ファイル | 説明 |
|---------|------|
| [CLAUDE.md](CLAUDE.md) | AI駆動開発ガイドライン（全プロジェクト共通） |
| `.claude/commands/` | カスタムコマンド定義 |
| `.claude/agents/` | 専門エージェント定義 |
| `.context/` | コンテキストエンジニアリング用ファイル保存先 |

---

## カスタムコマンド一覧

カスタムコマンドは以下のカテゴリに分類されます。

### 📝 コンテキスト作成（context/）

| コマンド | 説明 |
|---------|------|
| `/context:create` | コンテキストファイル作成（コンテキストエンジニアリング） |

### 🛠️ 実装支援（impl/）

| コマンド | 説明 |
|---------|------|
| `/impl:unit-test` | 単体テストの自動生成（カバレッジ100%目標） |
| `/impl:tdd-red-green` | TDD RED/GREENフェーズ実装コンテキスト作成 |
| `/impl:tdd-refactor` | TDD REFACTORフェーズ実装 |
| `/impl:build-and-test` | ビルド＆テスト実行 |
| `/impl:impl-external-mock` | 外部接続モックプログラム実装 |
| `/impl:devcontainer` | DevContainer環境構築 |

### 🧪 PoC（poc/）

| コマンド | 説明 |
|---------|------|
| `/poc:create-backend` | バックエンドPoC作成 |
| `/poc:create-frontend` | フロントエンドPoC作成 |

### 📖 ドキュメント生成（docs/）

| コマンド | 説明 |
|---------|------|
| `/docs:design` | 設計書生成 |
| `/docs:screen` | 画面仕様書生成 |

### ⚙️ ユーティリティ（util/）

| コマンド | 説明 |
|---------|------|
| `/util:resolve-issue-plan` | イシュー解決プラン作成 |
| `/util:custom-command-refiner` | カスタムコマンド改善 |

---

## エージェント一覧

専門エージェントを使用することで、より高品質な実装が可能になります。

### 👨‍💻 言語専門家

| エージェント | 説明 |
|------------|------|
| `python-expert` | Python開発の専門家（pytest、venv、ベストプラクティス） |
| `java-expert` | Java開発の専門家（Spring、Maven、JUnit） |

### 🔍 探索・分析

| エージェント | 説明 |
|------------|------|
| `code-explorer` | ソースコード探索・要約・分析 |
| `document-explorer` | ドキュメント探索・要約 |
| `note-explorer` | `docs/note/`配下の情報検索・要約 |

### 🎯 特殊用途

| エージェント | 説明 |
|------------|------|
| `task-reasoning-analyzer` | タスク・ファイル・アクション・テスト項目の推論分析 |
| `context-review` | コンテキストファイルのレビュー |
| `slash-command-creator` | カスタムスラッシュコマンド作成・修正 |
| `git-expert` | Git操作の専門家 |

### 使用例

```
# Pythonの専門家エージェントを呼び出す
@python-expert ログイン機能を実装してください

# コード探索エージェントを使用
@code-explorer Login.pyの実装内容を要約してください
```

---

## ディレクトリ構成

プロジェクトは以下の標準構成に従います：

```
project-root/
  |- .claude/                   # Claude用ディレクトリ
  |   |- commands/              # カスタムコマンド
  |   |- agents/                # 専門エージェント
  |- .devcontainer/             # DevContainer設定
  |- .external/                 # 外部接続モックプログラム
  |   |- docs/                  # モック仕様書
  |   |- main.py
  |   |- venv/
  |- docs/                      # ドキュメント
  |   |- requirements.md        # 要件定義書
  |   |- design.md              # 設計書
  |   |- database.md            # DB仕様書
  |   |- screen.md              # 画面仕様書
  |   |- external/              # 外部接続IF仕様書
  |   |- ifspec.yaml            # backend用IF仕様書
  |   |- note/                  # その他ドキュメント
  |- backend/                   # バックエンドアプリケーション
  |   |- src/
  |   |- test/
  |- frontend/                  # フロントエンドアプリケーション
  |   |- src/
  |   |- test/
  |- poc/                       # 試作
  |   |- backend/
  |   |- frontend/
  |- .tmp/                      # 一時ディレクトリ
  |- .context/                  # コンテキストエンジニアリング用
  |- CLAUDE.md                  # プロジェクト固有のガイドライン
```

---

## 開発ガイドライン

### 基本理念

- **推測禁止**: 不明な点は必ず質問する
- **確認優先**: 曖昧な要求は確認してから実行
- **最小実行**: 明示的に要求されたことのみ実行
- **品質最優先**: 妥協を許さず最高水準を追求
- **シンプルさこそ正義（KISS）**: 最も単純で明快な実装

詳細は [CLAUDE.md](CLAUDE.md) を参照してください。

### Gitブランチ戦略

#### ブランチ

- `main`: メインブランチ
- `stg`: 検証用ブランチ
- `dev`: 開発用ブランチ

#### 命名規則

- 新規機能: `release/XXX`
- バグ修正: `fix/XXX`
- 削除: `delete/XXX`
- リファクタ: `refactor/XXX`

#### コミットメッセージ形式

```
[RELEASE/FIX/DELETE/REFACTOR]: <修正内容>

- 変更内容の詳細1
- 変更内容の詳細2
- 関連ファイルやモジュール
```

詳細な例は [CLAUDE.md#コミットメッセージ書き方](CLAUDE.md#コミットメッセージ書き方) を参照してください。

### コンテキスト駆動開発

AIアシスタントに対して、プロジェクトの背景・要件・設計・制約などを構造化して提供することで、より正確で一貫性のある開発を実現します。

#### コンテキストファイル作成

```bash
# コンテキスト作成コマンド実行
/context:create

# 作成されたコンテキストファイルを確認
# .context/20251127143000.md

# コンテキストに基づいて実装
/context:action 20251127143000.md
```

詳細は [CLAUDE.md#コンテキスト駆動開発について](CLAUDE.md#コンテキスト駆動開発について) を参照してください。

---

## 外部接続モックプログラム

Python + FastAPIを利用した外部接続モックプログラムが`.external/`に配置されています。

### 起動方法

```bash
cd .external && ./venv/bin/python3 -m uvicorn src.main:app --host 0.0.0.0 --port 9100 --reload
```

---

## ライセンス

MIT License

---

## 貢献

プルリクエスト・イシュー報告を歓迎します。

---

## 参考資料

- [Claude Code公式ドキュメント](https://code.claude.com/docs)
- [CLAUDE.md 開発ガイドライン](CLAUDE.md)
