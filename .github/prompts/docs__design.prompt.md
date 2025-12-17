---
agent: 'agent'
description: '設計ドキュメントを生成'
---

# 設計書（design.md）の作成

## 目的

要件定義書から設計情報を抽出し、以下の成果物を作成する：
- **docs/design.md**: システム設計書（アーキテクチャ、コンポーネント設計、データフロー等）

---

## 前提条件

以下のいずれかが存在すること：
- `docs/requirements.md`（要件定義書）
- `CLAUDE.md`（プロジェクト概要・技術スタック情報）
- ユーザから提供される設計要件

---

## Task

1. 入力資料の読み込み（note-explorer agentによる補足情報収集を含む）
2. 設計方針の確認（ユーザ承認）
3. システムアーキテクチャの作成
4. コンポーネント設計の作成
5. データフロー・シーケンス設計の作成
6. 非機能要件への対応方針の作成

---

## Step 1: 入力資料の読み込み

### 実行内容

1. 以下のファイルを順に確認し、存在するものを読み込む：
   - `docs/requirements.md`
   - `CLAUDE.md`
   - `docs/database.md`（存在すれば参照）
   - `docs/ifspec.yaml`（存在すれば参照）

2. **【MUST】note-explorer agentを使用して`docs/note`配下から設計に関連する情報を検索する**
   - 検索キーワード例：「設計」「アーキテクチャ」「技術選定」「方針」「検討」
   - 過去の設計議論、技術選定の経緯、アーキテクチャ検討メモなどを収集
   - note-explorerが返す情報を設計の参考資料として活用する

3. 読み込んだ内容から以下を抽出：
   - システムの目的・スコープ
   - 技術スタック
   - 主要機能
   - 外部システム連携
   - **`docs/note`から得られた設計関連の知見・制約事項**

### note-explorer agent の呼び出し方

```
Task tool を使用:
- subagent_type: "note-explorer"
- prompt: "設計書作成のため、docs/note配下から以下の情報を検索してください：
  1. アーキテクチャに関する検討メモ
  2. 技術選定の経緯や理由
  3. 設計方針や制約事項
  4. 過去の設計レビュー記録
  該当する情報があれば要約して報告してください。"
```

### 出力

抽出した情報（note-explorerからの情報を含む）をユーザに報告し、Step 2へ進む。

---

## Step 2: 設計方針の確認

### 実行内容

1. 採用するアーキテクチャパターンを提案
2. **ユーザに確認を求める**（必須）
3. 承認後、Step 3へ進む

### 確認項目

- アーキテクチャパターン（クリーンアーキテクチャ、MVC、レイヤード等）
- 認証・認可方式
- エラーハンドリング方針
- ログ・監視方針

---

## Step 3: システムアーキテクチャの作成

### 実行内容

システム全体のアーキテクチャを`docs/design.md`に記載する。

### 出力フォーマット

```markdown
# 設計書

## 1. システムアーキテクチャ

### 1.1 全体構成図

\```mermaid
graph TB
    subgraph Frontend
        FE[フロントエンド<br/>React/Vue/etc]
    end

    subgraph Backend
        API[APIサーバ<br/>Spring Boot/Express/etc]
        BL[ビジネスロジック層]
        DA[データアクセス層]
    end

    subgraph Infrastructure
        DB[(データベース<br/>PostgreSQL/MySQL)]
        CACHE[(キャッシュ<br/>Redis)]
    end

    subgraph External
        EXT[外部システム]
    end

    FE -->|REST API| API
    API --> BL
    BL --> DA
    DA --> DB
    DA --> CACHE
    BL -->|API連携| EXT
\```

### 1.2 採用アーキテクチャ

| 項目 | 採用パターン | 理由 |
|------|--------------|------|
| 全体構成 | クリーンアーキテクチャ | 依存関係の制御、テスト容易性 |
| API設計 | RESTful API | シンプルさ、標準的なHTTPメソッド活用 |
| データアクセス | リポジトリパターン | DB抽象化、テスト容易性 |

### 1.3 レイヤー構成

| レイヤー | 責務 | 主要コンポーネント |
|----------|------|-------------------|
| プレゼンテーション層 | リクエスト受付、レスポンス整形 | Controller, DTO |
| アプリケーション層 | ユースケース実行 | Service, UseCase |
| ドメイン層 | ビジネスロジック | Entity, DomainService |
| インフラストラクチャ層 | 外部リソースアクセス | Repository, Gateway |
```

---

## Step 4: コンポーネント設計の作成

### 実行内容

主要コンポーネントの設計を記載する。

### 出力フォーマット

```markdown
## 2. コンポーネント設計

### 2.1 コンポーネント一覧

| コンポーネント名 | 責務 | 依存先 |
|-----------------|------|--------|
| AuthController | 認証APIエンドポイント | AuthService |
| AuthService | 認証ビジネスロジック | UserRepository, TokenService |
| UserRepository | ユーザデータアクセス | Database |

### 2.2 コンポーネント詳細

#### AuthController

**責務**: 認証関連のHTTPリクエストを受け付け、適切なサービスに処理を委譲する

**公開インターフェース**:

| メソッド | パス | 説明 |
|----------|------|------|
| POST | /api/auth/login | ログイン処理 |
| POST | /api/auth/logout | ログアウト処理 |
| POST | /api/auth/refresh | トークンリフレッシュ |

**依存関係**:
- AuthService（認証処理）
- TokenService（トークン管理）

---

### 2.3 クラス図

\```mermaid
classDiagram
    class AuthController {
        -authService: AuthService
        +login(request: LoginRequest): LoginResponse
        +logout(token: String): void
        +refresh(token: String): TokenResponse
    }

    class AuthService {
        -userRepository: UserRepository
        -tokenService: TokenService
        +authenticate(email: String, password: String): User
        +validateToken(token: String): boolean
    }

    class UserRepository {
        +findByEmail(email: String): User
        +save(user: User): User
    }

    AuthController --> AuthService
    AuthService --> UserRepository
    AuthService --> TokenService
\```
```

---

## Step 5: データフロー・シーケンス設計の作成

### 実行内容

主要ユースケースのデータフローとシーケンスを記載する。

### 出力フォーマット

```markdown
## 3. シーケンス設計

### 3.1 ログイン処理

\```mermaid
sequenceDiagram
    actor User
    participant FE as Frontend
    participant API as AuthController
    participant SVC as AuthService
    participant REPO as UserRepository
    participant DB as Database

    User->>FE: ログイン情報入力
    FE->>API: POST /api/auth/login
    API->>SVC: authenticate(email, password)
    SVC->>REPO: findByEmail(email)
    REPO->>DB: SELECT * FROM users
    DB-->>REPO: User data
    REPO-->>SVC: User entity
    SVC->>SVC: パスワード検証
    SVC->>SVC: トークン生成
    SVC-->>API: AuthResult
    API-->>FE: 200 OK + Token
    FE-->>User: ログイン成功
\```

### 3.2 データフロー概要

\```mermaid
flowchart LR
    subgraph Input
        A[ユーザ入力]
        B[外部API]
    end

    subgraph Processing
        C[バリデーション]
        D[ビジネスロジック]
        E[データ変換]
    end

    subgraph Output
        F[(データベース)]
        G[APIレスポンス]
    end

    A --> C
    B --> C
    C --> D
    D --> E
    E --> F
    E --> G
\```
```

---

## Step 6: 非機能要件への対応方針の作成

### 実行内容

セキュリティ、パフォーマンス、エラーハンドリング等の方針を記載する。

### 出力フォーマット

```markdown
## 4. セキュリティ設計

### 4.1 認証・認可

| 項目 | 方式 | 説明 |
|------|------|------|
| 認証方式 | JWT | ステートレスなトークンベース認証 |
| トークン有効期限 | アクセス: 15分, リフレッシュ: 7日 | セキュリティとUXのバランス |
| パスワード保存 | bcrypt | ソルト付きハッシュ化 |

### 4.2 入力検証

- 全ての入力値をサーバサイドで検証
- SQLインジェクション対策（パラメータバインディング）
- XSS対策（出力エスケープ）

---

## 5. エラーハンドリング

### 5.1 エラーレスポンス形式

```json
{
  "error": {
    "code": "ERR_INVALID_CREDENTIALS",
    "message": "認証に失敗しました",
    "details": []
  }
}
```

### 5.2 エラーコード体系

| コード | HTTPステータス | 説明 |
|--------|---------------|------|
| ERR_INVALID_CREDENTIALS | 401 | 認証失敗 |
| ERR_UNAUTHORIZED | 403 | 権限不足 |
| ERR_NOT_FOUND | 404 | リソース未発見 |
| ERR_VALIDATION | 400 | バリデーションエラー |
| ERR_INTERNAL | 500 | 内部エラー |

---

## 6. パフォーマンス設計

### 6.1 キャッシュ戦略

| 対象 | キャッシュ方式 | TTL |
|------|---------------|-----|
| セッション情報 | Redis | 15分 |
| マスタデータ | アプリケーションキャッシュ | 1時間 |
| APIレスポンス | HTTP Cache-Control | 5分 |

### 6.2 データベース最適化

- インデックス設計（検索頻度の高いカラム）
- N+1問題の回避（JOIN/Eager Loading）
- コネクションプーリング
```

---

## 成果物チェックリスト

実行完了時に以下を確認：

- [ ] note-explorer agentを使用して`docs/note`配下の関連情報を検索した
- [ ] `docs/design.md`にシステムアーキテクチャ図が含まれている
- [ ] `docs/design.md`にレイヤー構成が定義されている
- [ ] `docs/design.md`にコンポーネント設計が記載されている
- [ ] `docs/design.md`に主要シーケンス図が含まれている
- [ ] `docs/design.md`にセキュリティ設計が記載されている
- [ ] `docs/design.md`にエラーハンドリング方針が記載されている
- [ ] `docs/note`から得られた知見が設計に反映されている（該当情報がある場合）
- [ ] mermaid図が正しい構文で記述されている
- [ ] 要件定義書との整合性が取れている

---

## 他ドキュメントとの関係

| ドキュメント | 関係 |
|-------------|------|
| requirements.md | 入力：要件から設計を導出 |
| docs/note/* | 入力：過去の検討メモ・技術選定経緯を参照（note-explorer経由） |
| database.md | 出力：設計に基づきDB設計を詳細化 |
| screen.md | 出力：画面設計の基盤となる |
| ifspec.yaml | 出力：API設計を詳細化 |
