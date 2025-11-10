<summary>外部連携モックサーバの作成用コマンド</summary>

<specification>
    外部システムのモックサーバを python+venv+FastAPIで構築するコマンド。
    $ARGUMENTで指定されたIF仕様書を元に、統合モックサーバを作成する。
</specification>

<Usage>
    ```bash
    /aidev-impl:impl-external-mock <IF仕様書のパス>
    ```
</Usage>

<Tasks>
    <task>統合モックサーバ初期化</task>
    <task>共通エンドポイント作成</task>
    <task>IF仕様書読み込み</task>
    <task>外部連携モック実装</task>
    <task>外部連携ドキュメント作成</task>
    <task>起動確認</task>
</Task>

<Phase no=1>
    <summary>
        統合モックサーバ初期化（作成済みの場合は省略）。
        ディレクトリ構築やvenv環境の設定を行う。
    </summary>
    <action no=1>
        <summary>ディレクトリの作成</summary>
        <action>`mkdir .external`を実行し、ディレクトリを作成</action>
    </action>
    <action no=2>
        <summary>venv環境の整備</summary>
        <action>
            1. `cd .external && python3 -m venv venv`を実行し、venv環境を構築
            2. `cd .external && ./venv/bin/python3 -m pip install uvicorn fastapi pydantic`を実行しライブラリのインストール
        </action>
    </action>
    <display>✅ モックサーバの初期化が完了しました</display>
</Phase>

<Phase no=2>
    <summary>
        共通エンドポイントの作成（作成済みの場合は省略）。
        ヘルスチェック、エラー系のエンドポイントを作成。
    </summary>
    <action no=1>
        `.external/src/common`に以下エンドポイントのmodel及びrouterを作成し、main.pyからルーティングする。
        1. /health: `{"status": "ok"}`を返す
        2. /error-403: 403エラーを返す
        3. /error-404: 404エラーを返す
        4. /error-502: 502エラーを返す
        5. /error-503: 503エラーを返す
    </action>
    <action no=2>
        共通エンドポイントのドキュメントを.external/docs配下に作成。
        「エンドポイント仕様書」のサンプルを確認。
    </action>
    <display>✅ 共通エンドポイントの作成が完了しました。</display>
</Phase>

<Phase no=3>
    <summary>
        $ARGUMENT によって指定された、実装を行うモックサーバの対象のIF仕様書を読み込む。
    </summary>
    <action>
        $ARGUMENT によって指定された、実装を行うモックサーバの対象のIF仕様書を読み込む。
    </action>
    <display>✅ IF仕様書の読み込みが完了しました。</display>
</Phase>

<Phase no=4>
    <summary>外部連携モック実装</summary>
    <action>
        読み込んだIF仕様書を元にモックを作成。
        1. src/{SystemName}/model.py を実装
        2. src/{SystemName}/router.py を実装
        3. src/main.py を修正し、ルータを追加
    </action>
    <display>✅ 固有システムのエンドポイントの実装が完了しました。</display>
</Phase>

<Phase no=5>
    <summary>外部連携ドキュメント作成</summary>
    <action>
        実装した外部連携モックのドキュメントを作成し、docs/{SystemName}.mdとして保存する。
        「エンドポイント仕様書」のサンプルを確認。
    </action>
    <display>✅ 固有システムのエンドポイントのドキュメント作成が完了しました。</display>
</Phase>

<Phase no=6>
    <summary>起動確認</summary>
    <action>
        起動コマンドを実行し、起動できるか確認を行う。
        起動できない場合は修正し、起動できるようにする。
        1. `localhost:9100/health`を実行し正常性を確認。
        2. 固有エンドポイントへのcurlを実行し、正常性を確認。
        正常性確認後はtaskをkillすること。
    </action>
    <display>✅ 正常性確認が完了しました。</display>
</Phase>

<Directory>
    <summary>ディレクトリ構成</summary>
    <structure>
        ```
        .external/
          |- requirements.txt
          |- venv/
          |- docs/
          |   |- common.md   # 共通エンドポイント仕様書
          |   |- systemA.md  # システムAのエンドポイント仕様書
          |- src
          |   |- __init__.py
          |   |- main.py     # エントリポイント
          |   |- common      # 共通エンドポイント
          |   |   |- router.py
          |   |   |- model.py
          |   |- systemA    # SystemAのモック
          |       |- router.py
          |       |- model.py
          |- uvicorn.log     # 実行時ログ
        ```
    </structure>
</Directory>

<Command>
    <start-command>`cd .external && ./venv/bin/python3 -m uvicorn src.main:app --host 0.0.0.0 --port 9100 --reload`</start-command>
</Command>

<Docs>
    <specification name="エンドポイント仕様書">
        <summary>docs/配下のドキュメントを定義する</summary>
        <example>

            ```markdown
            # SystemA仕様書

            ## システム概要
            **システム名**: SystemA
            **説明**: User管理を行うSystemAのモックサーバ

            ## APIエンドポイント

            ### 1. ログイン
            **エンドポイント**: `POST /systemA/login`
            **説明**: POST形式で値を渡しログインを行う。

            #### リクエストヘッダ
            | ヘッダ名 | 必須 | 値 |
            | -- | -- | -- |
            | Host | ○ | connect.system.jp |
            | Accept-Charset | ○ | UTF-8 |
            | Connection | ○ | close |
            | Content-Type | ○ | application/x-www.form-urlencoded; charset=UTF-8 |

            #### リクエストボディ
            | パラメータ名 | 必須 | 型 | 説明 | 例 |
            | -- | -- | -- | -- | -- |
            | username | ○ | string | 8～32文字の半角英数小文字 | user1234 |
            | password | ○ | string | 8～32文字の半角英数小文字、記号（_@$#） | P@ssw0rd |

            #### 正常レスポンス（200 OK）
            \`\`\`json
            {
                "status": "success",
                "session_id": "XXXXXXXXXXXXXXXXXXXXXXXXX"
            }
            \`\`\`

            #### 異常系レスポンス（403 Forbidden）
            \`\`\`json
            {
                "status": "failed",
                "errorCode": "E1001",
                "message": "ユーザが見つかりませんでした"
            }
            \`\`\`
            ```
            
        </example>
    </specification>
</Docs>

<Cautions>
    <caution>既存の.externalディレクトリがある場合は、既存システムの上に新しいシステムを追加する</caution>
    <caution>統合モックサーバは開発・テスト用のみに使用する</caution>
    <caution>すべての外部システムがFastAPIアプリケーションで提供される</caution>
</Cautions>