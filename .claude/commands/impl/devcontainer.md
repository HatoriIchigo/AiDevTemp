あなたは開発環境構築の専門家です。
以下の指示に従って、VS Code DevContainer環境を構築してください。

## 実行前の確認事項

1. `docs/database.md`が存在する場合は確認する
2. `docs/external/`配下のファイルを確認する
3. プロジェクトで使用する技術スタック（言語、フレームワーク）を確認する
4. 不明な点があれば、推測せずにユーザーに質問する

## ディレクトリ構成

以下の構成で`.devcontainer/`ディレクトリを作成してください:

```
.devcontainer/
  |- db/                    # DB用ディレクトリ（必要な場合）
  |   |- Dockerfile
  |   |- init.sql          # 初期データ投入用スクリプト
  |- poc/                   # pocアプリ用ディレクトリ（必要な場合）
  |   |- Dockerfile
  |- backend/               # バックエンド用ディレクトリ
  |   |- Dockerfile
  |- frontend/              # フロントエンド用ディレクトリ（必要な場合）
  |   |- Dockerfile
  |- docker-compose.yml     # devcontainerで起動するdocker-composeファイル
  |- devcontainer.json      # Devcontainer設定用ファイル
```

## 実装手順

### 1. DB用コンテナの作成（必要な場合のみ）

`docs/database.md`を確認し、DB要件がある場合:

- `docs/database.md`を参考にテストデータ（`init.sql`）を作成
- DB用コンテナのDockerfileを作成
- docker-compose.ymlにコンテナを追加:
  - **サービス名**: `db`
  - **docker内部IPアドレス**: `192.168.2.1`
  - **データ永続化**: ボリュームを適切に設定

### 2. 外部接続モック用コンテナの作成（必要な場合のみ）

`docs/external/`配下を確認し、外部接続仕様がある場合:

- 各システムごとに個別のモックコンテナを作成
- **ツール**: [python-openapi-client](https://github.com/openapi-generators/openapi-python-client) を使用
- docker-compose.ymlにコンテナを追加:
  - **サービス名**: `<システム名>_mock`（例: `systemA_mock`）
  - **docker内部IPアドレス**: `192.168.3.xxx`
  - **ポート番号**: `9100`以降を使用（各モックで別々のポート）

### 3. POC用コンテナの作成（必要な場合のみ）

POC開発が必要な場合:

- POC用Dockerfileの作成
- docker-compose.ymlにコンテナを追加:
  - **サービス名**: `poc`
  - **docker内部IPアドレス**: `192.168.10.1`
  - **ポート番号**:
    - バックエンド: `9201`
    - フロントエンド: `9202`
  - **マウント**: プロジェクトルートの`poc/`配下

### 4. Backend用コンテナの作成（必須）

- Backend用Dockerfileの作成
- docker-compose.ymlにコンテナを追加:
  - **サービス名**: `backend`
  - **docker内部IPアドレス**: `192.168.4.1`
  - **ポート番号**: `9001`
  - **マウント**: プロジェクトルートの`backend/`（または`src/`）配下

### 5. Frontend用コンテナの作成（必要な場合のみ）

フロントエンドが必要な場合:

- Frontend用Dockerfileの作成
- docker-compose.ymlにコンテナを追加:
  - **サービス名**: `frontend`
  - **docker内部IPアドレス**: `192.168.4.2`
  - **ポート番号**: `9002`
  - **マウント**: プロジェクトルートの`frontend/`配下

### 6. その他コンテナの作成（必要な場合のみ）

Redis、Message Queue等が必要な場合:

- ユーザーに要件を確認してから作成
- docker-compose.ymlにコンテナを追加
- 適切なIPアドレスとポート番号を割り当て

### 7. devcontainer.json の作成

- VS Code DevContainer設定ファイルを作成
- 必要な拡張機能を定義
- 適切なポートフォワーディング設定

## 必須の確認事項

作成後、以下を必ず確認してください:

### 構成確認
- [ ] `docker-compose.yml`でnetworksを利用し、subnetに`192.168.0.0/24`を設定
- [ ] すべてのコンテナで異なるポート番号を使用
- [ ] マウント設定が正しく、必要なディレクトリがマウントされている
- [ ] 各コンテナのIPアドレスが正しく設定されている
- [ ] devcontainer.jsonの設定が適切

### Docker起動確認
作成したDevContainer環境をテストし、問題があれば修正してください:

1. **コンテナ起動確認**
   ```bash
   cd .devcontainer
   docker-compose up -d
   ```
   - すべてのコンテナが正常に起動するか確認
   - エラーが発生した場合は原因を特定し、Dockerfileまたはdocker-compose.ymlを修正
   - 起動後、以下でコンテナ状態を確認:
     ```bash
     docker-compose ps
     ```
   - すべてのコンテナのStateが`Up`になっているか確認

2. **コンテナログ確認**
   ```bash
   docker-compose logs
   ```
   - エラーメッセージがないか確認
   - 各サービスが正常に起動しているか確認

3. **コンテナ停止・削除**
   ```bash
   docker-compose down
   ```
   - 問題なく停止・削除できるか確認

### 通信確認
すべてのコンテナ間の通信が正常に行えるか確認してください:

1. **IPアドレス確認**
   - 各コンテナに割り当てられたIPアドレスが設定通りか確認:
     ```bash
     docker-compose exec <service-name> ip addr show
     ```

2. **コンテナ間通信確認**
   - Backend → DB への接続確認（DBがある場合）
     ```bash
     docker-compose exec backend ping -c 3 192.168.2.1
     ```
   - Backend → 外部モック への接続確認（外部モックがある場合）
     ```bash
     docker-compose exec backend ping -c 3 192.168.3.xxx
     ```
   - Frontend → Backend への接続確認（Frontendがある場合）
     ```bash
     docker-compose exec frontend ping -c 3 192.168.4.1
     ```

3. **ポート疎通確認**
   - 各サービスのポートが開いているか確認:
     ```bash
     docker-compose exec backend curl -I http://192.168.2.1:5432
     ```
   - ホストからコンテナへのポートフォワード確認:
     ```bash
     curl http://localhost:9001
     ```

4. **DB接続確認**（DBがある場合）
   - 実際にDBに接続できるか確認
   - テストデータ（init.sql）が正しく投入されているか確認

### 修正が必要な場合

以下の問題が発生した場合は、該当箇所を修正してください:

- **コンテナ起動失敗**: Dockerfileの構文エラー、依存関係の不足を確認
- **ポート競合**: docker-compose.ymlのポート番号を変更
- **通信失敗**:
  - docker-compose.ymlのnetworks設定を確認
  - 各サービスのIPアドレス設定を確認
  - ファイアウォール設定を確認
- **マウント失敗**: docker-compose.ymlのvolumes設定を確認

## 注意事項

- **推測禁止**: 不明な技術スタックや要件がある場合は必ずユーザーに質問
- **最小構成**: 明示的に必要と確認できたコンテナのみ作成
- **ファイル名統一**: `docker-compose.yml`を使用（`.yaml`ではなく`.yml`）
- **CLAUDE.mdの遵守**: プロジェクトのディレクトリ構成に従う
- **既存ファイルの確認**: ファイル作成前に既存の設定ファイルを確認し、上書きする場合はユーザーに確認
