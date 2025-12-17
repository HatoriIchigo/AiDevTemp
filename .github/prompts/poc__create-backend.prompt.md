---
agent: 'agent'
description: 'バックエンドのPoCコードを生成する。'
---

# POC バックエンド作成

POC（Proof of Concept）用のバックエンドを作成するコマンド。
全てモックデータで動作し、データベースや外部システムとの通信は一切行わない。
正常系1パターンのみを実装する。

## ARGUMENT
ARGUMENTは対象エンドポイントを指定する（任意）。
指定がない場合は全エンドポイントを対象とする。

```
/poc:create-backend                    # 全エンドポイントを作成
/poc:create-backend /api/users         # 特定エンドポイントのみ作成
```

## 前提条件
- `docs/ifspec.yaml` が存在すること（存在しない場合はエラー終了）

## Task
Taskツールを利用し、以下を行う。
1. IF仕様書の存在確認
2. IF仕様書の読み込みと対象エンドポイントの特定
3. 技術スタック確認・プロジェクト初期化
4. モックデータ作成
5. エンドポイント実装
6. 動作確認

---

## Phase 1. IF仕様書の存在確認

1. `docs/ifspec.yaml` の存在を確認
2. 存在しない場合は以下を表示してエラー終了：
    ```
    エラー: docs/ifspec.yaml が見つかりません。
    POCバックエンドを作成するにはIF仕様書が必要です。
    ```

✅ IF仕様書の存在確認が完了しました

---

## Phase 2. IF仕様書の読み込みと対象エンドポイントの特定

1. `docs/ifspec.yaml` を読み込む
2. ARGUMENTでエンドポイントが指定されている場合は該当エンドポイントのみを対象とする
3. 対象エンドポイント一覧を表示し、ユーザに確認：
    ```markdown
    ## 対象エンドポイント一覧
    | メソッド | パス | 概要 |
    | -------- | ---- | ---- |
    | POST | /api/auth/login | ユーザ認証 |
    | GET | /api/users | ユーザ一覧取得 |
    | GET | /api/users/{id} | ユーザ詳細取得 |

    上記のエンドポイントでPOCを作成します。よろしいですか？（y/n）
    ```
    **ユーザの承認が得られた場合にのみ次フェーズへ移行する。**

✅ 対象エンドポイントの特定が完了しました

---

## Phase 3. 技術スタック確認・プロジェクト初期化

### 技術スタックの確認
1. プロジェクトルートの `CLAUDE.md` を確認し、技術スタックを特定
2. 技術スタックが不明な場合はユーザに確認：
    ```markdown
    バックエンドの技術スタックを選択してください：
    1. Python + FastAPI
    2. Node.js + Express
    3. Java + Spring Boot
    4. Go + Gin
    5. その他（指定してください）
    ```

### プロジェクト初期化（poc/backend が存在しない場合）
1. `poc/backend` ディレクトリを作成
2. 選択された技術スタックでプロジェクトを初期化
3. 必要な依存パッケージをインストール

### 初期化例（Python + FastAPI の場合）
```bash
mkdir -p poc/backend/src
cd poc/backend && python3 -m venv venv
cd poc/backend && ./venv/bin/pip install fastapi uvicorn pydantic
```

### 初期化例（Node.js + Express の場合）
```bash
mkdir -p poc/backend/src
cd poc/backend && npm init -y
cd poc/backend && npm install express cors
```

✅ プロジェクト初期化が完了しました

---

## Phase 4. モックデータ作成

1. IF仕様書から必要なデータ構造を分析
2. モックデータディレクトリにモックデータを作成
3. **正常系1パターンのみ**を作成

### Python + FastAPI の場合
```python
# src/mocks/users.py
mock_users = [
    {
        "id": "user-001",
        "name": "テストユーザー1",
        "email": "test1@example.com",
    },
    {
        "id": "user-002",
        "name": "テストユーザー2",
        "email": "test2@example.com",
    },
]

# src/mocks/__init__.py
from .users import mock_users
```

### Node.js + Express の場合
```javascript
// src/mocks/users.js
const mockUsers = [
  {
    id: "user-001",
    name: "テストユーザー1",
    email: "test1@example.com",
  },
];

module.exports = { mockUsers };
```

### モックデータの原則
- IF仕様書のレスポンス形式に準拠
- 正常系1パターンのみ（異常系は実装しない）
- 日本語のダミーデータを使用

✅ モックデータの作成が完了しました

---

## Phase 5. エンドポイント実装

各エンドポイントを順次実装する。

### 実装方針
1. **正常系のみ**: 全エンドポイントは正常レスポンスのみ返す
2. **モックデータ使用**: DB接続なし、モックデータから返却
3. **バリデーションなし**: リクエストバリデーションは最小限
4. **認証なし**: 認証・認可処理は実装しない

### Python + FastAPI 実装例
```python
# src/routers/users.py
from fastapi import APIRouter
from ..mocks import mock_users

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("")
async def get_users():
    return {"users": mock_users}

@router.get("/{user_id}")
async def get_user(user_id: str):
    return mock_users[0]  # 常に最初のユーザを返す
```

### Node.js + Express 実装例
```javascript
// src/routes/users.js
const express = require("express");
const { mockUsers } = require("../mocks/users");
const router = express.Router();

router.get("/", (req, res) => {
  res.json({ users: mockUsers });
});

router.get("/:id", (req, res) => {
  res.json(mockUsers[0]); // 常に最初のユーザを返す
});

module.exports = router;
```

### エンドポイントごとの実装
```markdown
### POST /api/auth/login 実装中...
- [ ] ルーター作成
- [ ] モックレスポンス定義
- [ ] メインアプリへの登録

✅ POST /api/auth/login の実装が完了しました
```

### 注意事項
- **通信禁止**: 外部API・DB への通信は一切行わない
- **正常系のみ**: エラーハンドリングは実装しない
- **固定レスポンス**: 入力に関わらず固定のモックデータを返す

✅ 全エンドポイントの実装が完了しました

---

## Phase 6. 動作確認

1. 開発サーバーを起動
    ```bash
    # Python + FastAPI
    cd poc/backend && ./venv/bin/uvicorn src.main:app --reload --port 8080

    # Node.js + Express
    cd poc/backend && node src/index.js
    ```
2. 各エンドポイントの動作確認（curl）
3. エラーがある場合は修正

### 確認項目
- [ ] サーバーが正常に起動する
- [ ] 全エンドポイントが正常にレスポンスを返す
- [ ] レスポンス形式がIF仕様書と一致する

### 確認コマンド例
```bash
# ヘルスチェック
curl http://localhost:8080/health

# ユーザ一覧
curl http://localhost:8080/api/users

# ユーザ詳細
curl http://localhost:8080/api/users/user-001
```

✅ 動作確認が完了しました

---

## ディレクトリ構成

### Python + FastAPI
```
poc/backend/
  |- venv/
  |- src/
  |   |- __init__.py
  |   |- main.py           # エントリポイント
  |   |- mocks/            # モックデータ
  |   |   |- __init__.py
  |   |   |- users.py
  |   |- routers/          # ルーター
  |   |   |- __init__.py
  |   |   |- users.py
  |   |   |- auth.py
  |   |- models/           # Pydanticモデル
  |       |- __init__.py
  |       |- user.py
  |- requirements.txt
```

### Node.js + Express
```
poc/backend/
  |- node_modules/
  |- src/
  |   |- index.js          # エントリポイント
  |   |- mocks/            # モックデータ
  |   |   |- users.js
  |   |- routes/           # ルーター
  |       |- users.js
  |       |- auth.js
  |- package.json
```

---

## 注意事項

- **NEVER**: データベースへの接続コードを書かない
- **NEVER**: 外部APIへの通信コードを書かない
- **NEVER**: 認証・認可の実装を行わない
- **NEVER**: エラーハンドリング・異常系を実装しない
- **MUST**: 全データはモックを使用する
- **MUST**: IF仕様書に記載されたレスポンス形式に準拠する
- **MUST**: 正常系1パターンのみ実装する
- **SHOULD**: CORSは全許可で設定（POCのため）

---

## 完了メッセージ

```markdown
POCバックエンドの作成が完了しました。

## 作成したエンドポイント
| メソッド | パス | 概要 |
| -------- | ---- | ---- |
| POST | /api/auth/login | ユーザ認証 |
| GET | /api/users | ユーザ一覧取得 |
| GET | /api/users/{id} | ユーザ詳細取得 |

## 起動方法
\`\`\`bash
# Python + FastAPI
cd poc/backend && ./venv/bin/uvicorn src.main:app --reload --port 8080

# Node.js + Express
cd poc/backend && node src/index.js
\`\`\`

## 確認URL
http://localhost:8080

## 注意
- 全エンドポイントは正常系のみ実装
- 認証・バリデーションは未実装
- モックデータを固定で返却
```
