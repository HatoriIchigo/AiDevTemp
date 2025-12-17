# 単体テストの自動生成

単体テストコードの自動生成を行う。
カバレッジ率100%を目標とする。

## ARGUMENT
ARGUMENTは「実装コード」もしくは「単体テストコード」を引数に取る
```
/aidev-impl:impl-unit-test @src/main/accounts/Login.py
/aidev-impl:impl-unit-test @src/test/accounts/LoginTest.py
```
引数がない場合はエラーを出力して終了。

## Task
Taskツールを利用し、以下を行う。
1. 実装コードに対応する単体テストコードを探索
2. 実装されている、実装するべきテスト項目を表示
3. 単体テストコード実装
4. カバレッジ率測定

## Phase 1. 実装コードに対応するテストコードを探索
1. $ARGUMENT がメインコードかテストコード化を把握
2. それに対応するメインコード及びテストコードを探索
    - メインコードが`Login.py`なら、`LoginTest`のように、`ファイル名Test` 及び `Testファイル名`でファイル検索
    - テストコードがない場合は新規で作成を行う。
3. それぞれをペアとして表示する。
    ```markdown
    main: `src/main/accounts/Login.py`
    test: `src/test/accounts/LoginTest.py`

    ファイルに問題が無ければ承認してください。（y/n）
    ```
    **問題が無いかユーザに確認を行い、承認が得られた場合にのみ次フェーズへ移行する。**

## Phase 2. 実装されている・実装するべきテスト項目を表示

1. メインのソースコードの分析
    - テストするべき箇所を確認
2. 追加実装するべきテストなどの項目を表示
    - 追加するべきテスト項目
        - given/when/then形式で表示
    - 実装されているテスト項目
        - テスト項目名のみでOK

    ```markdown
    ## ➕ 追加するべきテスト項目
    1. `username`のバリデーションエラー
        - given: username=0000, password=Passw0rd
        - when: `register(username, password)`関数を実行
        - then: エラーメッセージ・usernameの文字数が足りません。
    2. `password`のバリデーションエラー
        - given: username=user0000, password=1234
        - when: `register(username, password)`関数を実行
        - then: エラーメッセージ・passwordの文字数が足りません。
    
    ## ✔️ 実装されているテスト項目
    1. 正常系
    2. 異常系、DB登録失敗

    問題が無ければ承認してください。（y/n）
    ```

    **問題が無いかユーザに確認を行い、承認が得られた場合にのみ次フェーズへ移行する。**

## Phase 3. 実装を行う

テストコードの実装を行う。

サブエージェントが使用できる場合は、適切なサブエージェントを選択し、テストコードの実装を行う。

### 実装上の注意
- given/when/thenを意識したコード
- 適切なコメントを付与する
- **文字数を定義して実装する場合、`"a".repeat(100)`や`"a" * 100`のように実装する。ハードコード禁止。**

### 実装例
```python
"""
異常系・ユーザ名バリデーションエラー
"""
def UsernameValidationErrorTest():
    # given
    username = "0000"
    password = "Passw0rd"

    # when
    result = accounts.register(username, password)

    # then
    assert.contain(result["message"], "ユーザ名の文字数が足りません")


"""
異常系・文字列境界テスト
"""
def PasswordBoundaryTest():
    # given
    username = "0000"
    # ❌ password = "Passw0rdaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"   # 30文字
    password = "P" * 30     # ⭕ 正しい例

    # when
    result = accounts.register(username, password)

    # then
    assert.contain(result["message"], "パスワードの文字数が多すぎます")

```


## Phase 4. カバレッジの測定

カバレッジの測定を行う。

カバレッジ率が100%に満たない場合は Phase2から再度実行し、カバレッジ率100%を目標にする。

何かしらの問題で100%にできない場合は明示して終了。

成功例：
```markdown
テストコードの作成が完了しました：　カバレッジ率100%で終了します。
```

失敗例：
```markdown
テストコードの作成が完了しました：　カバレッジ率70%で終了します。

❌ 以下の理由でカバレッジ率100%が未達です。
1. `os.Copy`にて失敗時の挙動が実行不可能
2. `client.execute`で実際の通信が発生し、モック化ができないため
```

## 注意事項
- **NEVER**: mainコードは変更しない
- **MUST**: 適切なコメントを付与する


