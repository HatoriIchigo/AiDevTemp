# TDD REFACTOR カスタムコマンド

## 目的
TDD GREENフェーズで作成したコードをリファクタリングし、その計画をコンテキストファイルに保存する。

## 実行手順

### Step 1: 対象ファイルの特定
ユーザーに以下を確認する：
- リファクタリング対象のソースファイルパス
- 関連するテストファイルパス（存在する場合）

### Step 2: コード分析
対象ファイルを読み込み、以下の観点で分析する：
1. 責務の分離が必要な箇所
2. 設定値・固定値のハードコーディング
3. Exception定義の場所
4. Validation処理の場所
5. ログ出力の実装状況

### Step 3: リファクタリング計画の作成
以下のルールに従って計画を立てる。

---

## リファクタリングルール

### ルール1: メインコードの構造
メインコードは以下の構造に統一する：

```python
def login(username: str, password: str):
    # 1. 開始ログの出力
    logger(LogTemplate["I-1001"])

    try:
        # 2. バリデーション
        validateUsername(username)
        validatePassword(password)

        # 3. ビジネスロジック
        registerUser(username, password)

    except Exception as ValidationError:
        # 異常時のログを表示
        logger(LogTemplate["E-1002"])

    except Exception as DBConnectionError:
        logger(LogTemplate["E-1003"])

    except Exception as e:
        logger(LogTemplate["E-1004"])

    finally:
        # 終了ログを表示
        logger(LogTemplate["I-1005"])
```

### ルール2: 責務の分離
- メインコードからは少ないコード量で呼び出す
- 分離したロジックは別フォルダ・別ファイルとして実装

```python
# ✅ 正しい例
registerUser(username, password)      # 本体はdb/User.pyに実装

# ❌ 悪い例（User/Login.pyに直接実装されている）
dbname = ('test.db')
conn = sqlite3.connect(dbname, isolation_level=None)
cursor = conn.cursor()
sql = "INSERT INTO users VALUES(?, ?)"
data = ((username, password))
cursor.execute(sql, data)
conn.commit()
```

### ルール3: 設定値の分離
- **MUST**: 外部システム（外部接続、DB、Redisなど）に依存しているパラメータは設定ファイルに記述
- **MUST**: 環境変数からも読み込めるようにする

```yaml
redis:
    host: ${REDIS_HOST:redis-host}
    port: ${REDIS_PORT:5366}

external:
    systemA:
        host: ${SYSTEMA_HOST:api.systemA.co.jp}
        port: ${SYSTEMA_PORT:443}
        path: ${SYSTEMA_PATH:/register}
```

### ルール4: 固定値の分離
- **MUST**: システムで利用する固定値をファイルを分けて分離する
- 共通と各機能で使用するもので分ける

```python
# constants/common.py
class CommonConstants:
    CHARSET_WINDOWS_31J = "Windows-31J"
    CHARSET_UTF8 = "utf-8"

# constants/account.py
class AccountConstants:
    LOGIN_NAME = "AAA"
```

### ルール5: Exceptionの分離
- **MUST**: `Exception class`は別途フォルダおよびファイルを分けて作成
- 実装コードと同一ファイルにExceptionクラスを作成しない

```python
# src/main/exceptions/ValidationException.py
class ValidationException(Exception):
    pass
```

### ルール6: Validationの分離
- **MUST**: Validationは別途フォルダおよびファイルを作成する
- 同一機能のValidationは一つのファイルにまとめる
- Validation失敗時にはExceptionとして投げる

```python
# src/main/validation/UserValidation.py
class UserValidation:
    def UsernameValidation(username: str, required: bool):
        if (required is False): return 0
        elif (type(username) is not str): raise ValidationException
        elif (username == ""): raise ValidationException
        return 0

    def PasswordValidation(password: str, required: bool):
        pass
```

### ルール7: ログの分離
- **MUST**: ログメッセージおよびログ初期化処理を分離
- **MUST**: `print`や`System.out.println`などの標準出力を禁止。`logging`や`log4j`を使用
- ログメッセージを別途定義

```python
# LogMessageTemplate.py
logMessage = {
    "I-1001": "ログイン処理を開始します",
    "E-1002": "DB接続に失敗しました",
    "I-1005": "ログイン処理を終了します",
}
```

### ルール8: 抽象クラスの活用
- **MAY**: 同フォルダを確認し、抽象クラスがあるか、抽象クラスに置き換えられるか確認
- **MAY**: 抽象クラスへと置換し、処理を簡略化する

---

## 注意事項

### 実装時の注意
- **テストを壊さない**: リファクタリング後も既存のテストが全てパスすることを確認

### 分離時の注意
- **循環参照を避ける**: モジュール間の依存関係に注意
- **命名規則の統一**: プロジェクトの命名規則に従う
- **過度な分離を避ける**: 必要以上にファイルを分割しない

### 禁止事項
- リファクタリングと同時に機能追加を行わない
- テストなしでリファクタリングを進めない
- 既存の動作を変更しない（振る舞いを保つ）

## Step 4: コンテキストファイルの作成

分析結果をもとに、`.context/context_YYYYMMDDHHMMSS.md` 形式でコンテキストファイルを作成する。

### コンテキストファイルのテンプレート

```markdown
# Login.pyのリファクタリング

## 概要
Login.pyのリファクタを行います。
- **ソース**: `src/main/accounts/Login.py`

## 修正後メインコードの構成

リファクタリング後、メインコードは以下構成とします。

\```python
def login(username: str, password: str):
    # 1. 開始ログの出力
    logger(LogTemplate["I-1001"])

    try:
        # 2. バリデーション
        validateUsername(username)
        validatePassword(password)

        # 3. ビジネスロジック
        registerUser(username, password)

    except Exception as ValidationError:
        # 異常時のログを表示
        logger(LogTemplate["E-1002"])
    
    except Exception as DBConnectionError:
        logger(LogTemplate["E-1003"])

    except Exception as e:
        logger(LogTemplate["E-1004"])

    finally:
        # 終了ログを表示
        logger(LogTemplate["I-1005"])
\```

## 責務の分離

1. 外部接続処理の委譲
    - 天気取得APIで取得する処理の委譲
    - `src/main/external/GetWeather.py`に実装
2. ユーザ登録処理の委譲
    - DB・ユーザ管理テーブルにユーザ情報を登録する処理を委譲
    - `src/main/db/Accounts.py`に実装

## 設定値の分離

1. 天気取得APIで使用する設定値を`src/main/settings.yml`に実装
    \```yaml
    external:
      weather:
        host: ${WEATHER_HOST:weather.yahoo.co.jp}
        port: ${WEATHER_PORT:443}
    \```
2. DBで使用する設定値を`src/main/settings.yml`に実装
    \```yaml
    mysql:
      host: ${MYSQL_HOST:}
      port: ${MYSQL_PORT:}
      dbname: ${MYSQL_DBNAME:}
      password: ${MYSQL_PASSWORD:}
    \```

## 固有値の分離

1. `"http://"`の分離
    - `src/main/constants/CommonConstants.py`に実装
2. `charset`の分離
    - `src/main/constants/User.py`に実装

## Exceptionの分離
<分離対象と分離先を記載>

## Validationの分離
<分離対象と分離先を記載>

## ログの分離

1. ログメッセージ：`"バリデーション処理に失敗しました。"`の分離
    - `src/main/log/LogMessage.py`に分離
    - `E-1001`に割り当てる
2. ログメッセージ：`"DB処理に失敗しました。"`の分離
    - `src/main/log/LogMessage.py`に分離
    - `E-1002`に割り当てる

## 実装時の注意事項
- 既存テストが全てパスすることを確認
- ビルドを通す
- 段階的にリファクタリングを実施
```

---

## Step 6: コンテキストファイルを批判的レビュー

- `context-review-agent`を使用し、コンテキストファイルの目的に対して、このコンテキストファイルのみで実装が可能か批判的にレビュー
- 上記レビューに対し、コンテキストファイルの修正を行う
