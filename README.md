# AI駆動開発テンプレート（AiDevTemplate）

Claude Code、GitHub Copilot、Google Geminiを使用したAI駆動開発のテンプレートプロジェクトです。

`.ai/`ディレクトリで統一管理されたカスタムコマンド・エージェント・開発ガイドラインを、`python .ai/copy.py`を実行することで各AIツール用のフォーマットに自動展開できます。

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

- **統一管理システム**: `.ai/`ディレクトリで全AIツール用の設定を一元管理
- **自動展開機能**: `python .ai/copy.py`で各AIツール用フォーマットに自動配布
  - `.claude/` - Claude Code用（エージェント・カスタムコマンド）
  - `.github/` - GitHub Copilot用（エージェント・プロンプト）
  - `.gemini/` - Google Gemini用（コマンド）
- **CLAUDE.md/GEMINI.md**: AI駆動開発のガイドライン・規約・ベストプラクティス
- **カスタムコマンド**: TDD実装、単体テスト生成、コンテキスト作成など
- **専門エージェント**: Python/Java専門家、コード探索、ドキュメント探索など
- **ディレクトリ構成規約**: backend/frontend/docs/pocなどの標準構成
- **Gitブランチ戦略**: release/fix/delete/refactorの命名規則

---

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <このリポジトリURL> ~/AiDevTemplate
cd ~/AiDevTemplate
```

### 2. 設定の展開

```bash
# Python実行で各AIツール用のディレクトリに自動展開
python .ai/copy.py
```

これにより以下が生成されます：
- `.claude/` - Claude Code用の設定
- `.github/` - GitHub Copilot用のエージェント
- `.gemini/` - Google Gemini用のコマンド
- `CLAUDE.md` - Claude用開発ガイドライン
- `GEMINI.md` - Gemini用開発ガイドライン

---

## カスタムコマンド一覧

カスタムコマンドは以下のカテゴリに分類されます。

### 📝 コンテキスト（context/）

| コマンド | Claude | Copilot | Gemini | 説明 |
|---------|:------:|:-------:|:------:|------|
| `context:action` | ✅ | ✅ | - | コンテキストファイルを実行 |
| `context:create-code` | ✅ | ✅ | - | コンテキストファイルを作成 |
| `context:review` | ✅ | ✅ | ✅ | コンテキストファイルをレビュー |

### 📖 ドキュメント生成（docs/）

| コマンド | Claude | Copilot | Gemini | 説明 |
|---------|:------:|:-------:|:------:|------|
| `docs:design` | ✅ | ✅ | - | 設計書生成 |
| `docs:screen` | ✅ | ✅ | - | 画面仕様書生成 |

### 🔀 Git操作（git/）

| コマンド | Claude | Copilot | Gemini | 説明 |
|---------|:------:|:-------:|:------:|------|
| `git:commit-push-pr` | ✅ | ✅ | - | コミット・プッシュ・PR作成 |

### 🛠️ 実装支援（impl/）

| コマンド | Claude | Copilot | Gemini | 説明 |
|---------|:------:|:-------:|:------:|------|
| `impl:bugfix` | ✅ | ✅ | - | バグ修正用ブランチ作成とコンテキスト生成 |
| `impl:build-and-test` | ✅ | ✅ | - | ビルド＆テスト実行、失敗時は修正案提示 |
| `impl:devcontainer` | ✅ | - | - | DevContainer環境構築 |
| `impl:impl-external-mock` | ✅ | ✅ | - | 外部APIモック実装生成 |
| `impl:tdd-red-green` | ✅ | ✅ | - | TDD RED/GREENフェーズ実装 |
| `impl:tdd-refactor` | ✅ | ✅ | - | TDD REFACTORフェーズ実装 |
| `impl:unit-test` | ✅ | ✅ | ✅ | 単体テストの自動生成（カバレッジ100%目標） |

### 🧪 PoC（poc/）

| コマンド | Claude | Copilot | Gemini | 説明 |
|---------|:------:|:-------:|:------:|------|
| `poc:create-backend` | ✅ | ✅ | ✅ | バックエンドPoC作成 |
| `poc:create-frontend` | ✅ | ✅ | ✅ | フロントエンドPoC作成 |

### ⚙️ ユーティリティ（util/）

| コマンド | Claude | Copilot | Gemini | 説明 |
|---------|:------:|:-------:|:------:|------|
| `util:custom-command-refiner` | ✅ | - | - | カスタムコマンド改善 |
| `util:resolve-issue-plan` | ✅ | ✅ | - | イシュー解決プラン作成 |

---

## エージェント一覧

専門エージェントを使用することで、より高品質な実装が可能になります。

> **Note**: Claude Codeでは`@エージェント名`、GitHub Copilotでは`@workspace /agent エージェント名`で呼び出します。

### 👨‍💻 言語専門家

| エージェント | Claude | Copilot | 説明 |
|------------|:------:|:-------:|------|
| `python-expert` | ✅ | ✅ | Python開発の専門家（pytest、venv、ベストプラクティス） |
| `java-expert` | ✅ | ✅ | Java開発の専門家（Spring、Maven、JUnit） |

### 🔍 探索・分析

| エージェント | Claude | Copilot | 説明 |
|------------|:------:|:-------:|------|
| `code-explorer` | ✅ | ✅ | ソースコード探索・要約・分析 |
| `document-explorer` | ✅ | ✅ | ドキュメント探索・要約 |
| `note-explorer` | ✅ | - | `docs/note/`配下の情報検索・要約 |

### 🎯 特殊用途

| エージェント | Claude | Copilot | 説明 |
|------------|:------:|:-------:|------|
| `task-analyzer-decomposer` | ✅ | ✅ | タスク・ファイル・アクション・テスト項目の推論分析 |
| `context-review` | ✅ | ✅ | コンテキストファイルのレビュー |
| `slash-command-creator` | ✅ | - | カスタムスラッシュコマンド作成・修正 |
| `git-expert` | ✅ | ✅ | Git操作の専門家 |

### 使用例

**Claude Code:**
```
# Pythonの専門家エージェントを呼び出す
@python-expert ログイン機能を実装してください

# コード探索エージェントを使用
@code-explorer Login.pyの実装内容を要約してください
```

**GitHub Copilot:**
```
# Pythonの専門家エージェントを呼び出す
@workspace /agent python-expert ログイン機能を実装してください

# コード探索エージェントを使用
@workspace /agent code-explorer Login.pyの実装内容を要約してください
```

---

## ディレクトリ構成

プロジェクトは以下の標準構成に従います：

```
project-root/
  |- .ai/                       # AIツール設定統一管理ディレクトリ
  |   |- agents/                # エージェント定義（共通）
  |   |- commands/              # カスタムコマンド定義（共通）
  |   |- copy.py                # 自動展開スクリプト
  |   |- copy-info.json         # 展開設定ファイル
  |   |- AGENTS.md              # 開発ガイドライン（元データ）
  |- .claude/                   # Claude Code用ディレクトリ（自動生成）
  |   |- commands/              # カスタムコマンド
  |   |- agents/                # 専門エージェント
  |- .github/                   # GitHub Copilot用ディレクトリ（自動生成）
  |   |- agents/                # 専門エージェント
  |   |- prompts/               # プロンプト定義
  |- .gemini/                   # Google Gemini用ディレクトリ（自動生成）
  |   |- commands/              # コマンド定義
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
  |- CLAUDE.md                  # Claude用開発ガイドライン（自動生成）
  |- GEMINI.md                  # Gemini用開発ガイドライン（自動生成）
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

#### 概要

コンテキスト駆動開発は、AIアシスタントに対して**プロジェクトの背景・要件・設計・制約などを構造化して提供**することで、より正確で一貫性のある開発を実現する手法です。

#### なぜコンテキストが重要なのか

AIアシスタントは会話履歴から情報を得ますが、以下の課題があります：

- **情報の散在**: 要件や設計が複数の会話に分散
- **文脈の欠落**: 過去の意思決定理由が不明確
- **一貫性の欠如**: 実装方針がブレる
- **引き継ぎ困難**: 新しい会話で同じ説明を繰り返す

コンテキストファイルを使うことで、これらの課題を解決できます。

#### コンテキストファイルに含まれる情報

コンテキストファイル（`.context/`配下）には以下を記載します：

1. **背景・目的**
   - なぜこの機能が必要なのか
   - ビジネス上の価値

2. **要件定義**
   - 機能要件・非機能要件
   - 制約事項

3. **設計方針**
   - アーキテクチャ
   - 使用技術・ライブラリ
   - 設計パターン

4. **実装指針**
   - ディレクトリ構成
   - 命名規則
   - コーディング規約

5. **テスト方針**
   - テスト戦略
   - カバレッジ目標

6. **関連ファイル**
   - 参照すべきドキュメント
   - 既存コードの場所

#### 使い方

##### 1. コンテキストファイル作成

**Claude Code:**
```bash
# コンテキスト作成コマンド実行
/context:create-code

# AIが対話形式で質問し、コンテキストファイルを作成
# → .context/20251211143000.md が生成される
```

**GitHub Copilot:**
```bash
# コンテキスト作成コマンド実行
#context:create-code
```

##### 2. コンテキストファイルの確認・編集

```bash
# 生成されたファイルを確認
cat .context/20251211143000.md

# 必要に応じて手動で編集・補足
vim .context/20251211143000.md
```

##### 3. コンテキストに基づいて実装

**Claude Code:**
```bash
# コンテキストファイルを指定して実装を依頼
/context:action 20251211143000.md
```

**GitHub Copilot:**
```bash
# コンテキストファイルを指定して実装を依頼
#context:action 20251211143000.md
```

##### 4. コンテキストのレビュー（オプション）

実装前にコンテキストの妥当性を確認：

```bash
# Claude Code
/context:review 20251211143000.md

# GitHub Copilot
#context:review 20251211143000.md

# Gemini
.context:review 20251211143000.md
```

#### ワークフロー例

```mermaid
graph TD
    A[新機能の要求] --> B[/context:create-code]
    B --> C[コンテキストファイル生成<br>.context/YYYYMMDDHHMMSS.md]
    C --> D{レビューが必要?}
    D -->|Yes| E[/context:review]
    E --> F{修正が必要?}
    F -->|Yes| G[手動編集]
    G --> C
    F -->|No| H[/context:action]
    D -->|No| H
    H --> I[実装完了]
    I --> J[コンテキスト保存<br>今後の参照用]
```

#### メリット

✅ **再現性**: 同じコンテキストで何度でも同じ品質の実装
✅ **一貫性**: プロジェクト全体で統一された設計・実装
✅ **効率性**: 何度も同じ説明をする必要がない
✅ **引き継ぎ**: 新しいメンバーや会話でも即座に状況把握
✅ **トレーサビリティ**: 意思決定の経緯が記録として残る

#### 実践例

```markdown
# .context/20251211143000.md

## 背景・目的
ユーザーからログイン機能のセキュリティ強化要求があった。
現在はパスワードのみの認証だが、2要素認証(2FA)を導入する。

## 要件
- TOTPベースの2FA実装
- QRコード表示機能
- バックアップコード生成（10個）
- 既存ユーザーは段階的移行（強制しない）

## 設計方針
- ライブラリ: pyotp
- 秘密鍵はDB暗号化保存
- フロントエンド: QRコード表示にqrcode.js使用

## 実装指針
- backend/src/auth/two_factor.py に実装
- 既存のauth.pyは修正最小限
- テストカバレッジ100%必須
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
