# CLAUDE.md — Claude Code 開発ガイドライン

> 本文書の【MUST】【SHOULD】【MAY】は、RFC 2119に準拠します：
> - 【MUST GLOBAL】：MUSTの上位概念。プロジェクトごとのCLAUDE.mdより優先される
> - 【MUST】: 絶対的要求事項。例外なく従う必要がある
> - 【SHOULD】: 強い推奨事項。特別な理由がない限り従う
> - 【MAY】: 任意事項。状況に応じて採用を判断

## 【MUST GLOBAL】基本理念

### 応答原則
- 回答は**すべて日本語**、簡潔・明瞭を徹底
- 不明確な点は「不明」と素直に伝える
- agentが使用できる場合は常にagentを使用する

### 曖昧な要求への対応

- **推測禁止**: 不明な点は必ず質問する
- **確認優先**: 「○○という理解で正しいですか？」と確認
- **最小実行**: 明示的に要求されたことのみ実行

### 禁止行為チェックリスト
- [ ] 要求されていない機能の追加
- [ ] 勝手なリファクタリング  
- [ ] 推測に基づく実装
- [ ] 「ついでに」の作業
- [ ] 親切心からの拡大解釈

### 実行前の自問自答

1. これは明示的に要求されたか？ → NO なら実行しない
2. 解釈に推測が含まれているか？ → YES なら質問する
3. 「ついでに」やろうとしていないか？ → YES なら止める

### 品質哲学
- **読み手に優しいコード** — 次のエンジニアがすぐ理解できる
- **品質最優先** — 妥協を許さず最高水準を追求
- **シンプルさこそ正義（KISS）** — 最も単純で意図が明快な実装
- **ボーイスカウト・ルール** — 触れたモジュールは「来たときよりきれい」に
- **不要な外部依存を追加しない** — 必要最小限の依存関係を維持

### 【悪い例】vs【良い例】

❌ ユーザー: 「ログイン機能を作って」
Claude: セキュリティも重要だから2要素認証も実装しました！

✅ ユーザー: 「ログイン機能を作って」
 Claude: ログイン機能について確認させてください：

- メール/パスワード認証でよろしいですか？
- セッション管理の要件はありますか？
- 既存の認証gemの使用は可能ですか？```

## プロジェクトルートCLAUDE.mdの構成
各プロジェクトルートのCLAUDE.mdは以下構成とする。

1. プロジェクトの概要
2. システム構成図
3. 機能一覧
4. 技術スタック
5. 使用するコマンド
6. ディレクトリ構成
7. メインコード実装方針
8. 単体テストコード実装方針
9. 結合・統合テスト実装方針
10. その他プロジェクトに関する必要事項
11. 注意事項
12. 参照ドキュメント

## ディレクトリ構成
各プロジェクトルートのディレクトリ構成は以下とする。

```
project-root/
  |- .claude/: Claude用ディレクトリ
  |- .devcontainer/: vscodeのdevcontainer専用ディレクトリ
  |   |- docker-compose.yml: devcontainerで使用するdocker-composeファイルはここに配置
  |- .external/: 外部接続（必要な場合）のモックプログラム
  |   |- docs/: モック仕様書のドキュメント
  |   |   |- common.md: 共通で使用するエンドポイント
  |   |- main.py
  |   |- venv/: pythonを動かすvenv環境
  |   |- requirements.txt
  |   ∟ README.md
  |- docs/: ドキュメント関連
  ∟ src/
    |- main
    |- test
```

## 外部接続モックプログラム

### 概要
Python+FastAPIを利用した外部接続をモックするプログラム。

## コード実装上の注意

### Exception関連

指定のない限りExceptionは別途フォルダ及びファイルを作成すること。
実装コードと同一のファイル（Ex. src/main/accounts/Login.pyなど）にExceptionクラスを作成しない。

Ex. src/main/exceptions/ValidationException.py
```python
class ValidationException(Exception):
    pass
```

### Validation関連

指定のない限りValidationは別途フォルダおよびファイルを作成すること。
同一機能のValidationは一つのファイルにまとめる。
また、Validation失敗時にはExceptionとして投げる。

Ex. src/main/validation/UserValidation.py
```python
# Validation定義
class UserValidation:
    def UsernameValidation(username: str, required: str):
        # required
        if (required is False): return 0
        elif (type(username) is not str): raise ValidationException
        elif (username == ""): raise ValidationException
        return 0
```

使用側：
```python
try:
    username = request.getUsername()

    userValidation = UserValidation()
    userValidation.UsernameValidation(username)

    # ビジネスロジック
except:
    # エラー時の挙動
```

### ログ関連
- `print`や`System.out.println`などの標準出力を禁止。`logging`や`log4j`を用いた出力。
