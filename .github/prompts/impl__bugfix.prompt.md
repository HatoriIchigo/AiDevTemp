---
agent: 'agent'
description: 'バグ修正用のブランチを作成し、バグ修正のコンテキストを生成する'
---

# バグ修正（Bugfix）

## 概要

バグ修正用のブランチを作成し、修正を行うためのコンテキストファイルを作成するカスタムコマンドです。

---

## 使用例

```bash
/impl:bugfix ログイン機能でログが表示されないバグを修正してください
```

---

## Tasks

1. ユーザからバグ情報をヒアリング
2. code-explorerエージェントで既存コードを調査
3. 複数の修正方針を提示してユーザに選択してもらう
4. 修正用ブランチ名の決定
5. 選択された方針に基づいてバグ修正用コンテキストファイルを作成（`.context/YYYYMMDDhhmmss.md`）


---

## Phase 1. バグ情報のヒアリング

ユーザから以下の情報を収集：

```markdown
## 🐛 バグ情報の確認

バグ修正を開始します。以下の情報を教えてください：

1. **バグの概要**: どのような不具合ですか？
   例: 削除フラグが更新されない

2. **発生箇所**: どのファイル・関数で発生していますか？
   例: src/services/UserRepository.delete()

3. **期待する動作**: 本来どうあるべきですか？
   例: delete()実行時にis_deleted=1に更新されるべき

4. **現在の動作**: 実際にはどうなっていますか？
   例: is_deletedが0のまま変更されない

5. **再現手順**: どうすれば再現できますか？
   例: UserRepository.delete(user_id=1)を実行

回答をお願いします。
```

## Phase 2. 既存コードの調査

**code-explorer エージェント** を使用して、バグ発生箇所のコードを調査：

```markdown
## 🔍 既存コードの調査

code-explorer エージェントを使用して、バグ発生箇所を調査します...

【調査対象】
- src/services/UserRepository.py
- src/test/test_user_repository.py

【調査結果】
- delete()メソッドの実装状況
- 関連するテストケース
- 依存関係
- 影響範囲
...
```

## Phase 3. 修正方針の複数案提示

既存コード調査の結果を踏まえ、複数の修正方針を提案してユーザに選択してもらう：

```markdown
## 🔧 修正方針の提案

既存コードを調査した結果、以下の修正方針を提案します。
どの方針で進めますか？

### 案1: 最小限の修正（推奨）

**概要**: delete()メソッドにis_deletedフラグ更新処理を追加

**メリット**:
- 影響範囲が最小限
- 既存の処理フローを変更しない
- リスクが低い

**デメリット**:
- 根本的な設計改善にはならない

**修正内容**:
- `UserRepository.delete()` にフラグ更新処理を追加
- 対応するテストケースを追加

**影響ファイル**:
- src/services/UserRepository.py (修正)
- src/test/test_user_repository.py (修正)

---

### 案2: BaseRepositoryでの共通処理化

**概要**: 論理削除処理をBaseRepositoryに共通化

**メリット**:
- 他のRepositoryでも同様の問題を防げる
- 保守性が向上
- DRY原則に従う

**デメリット**:
- 影響範囲が広い
- テスト工数が増加
- リスクが高い

**修正内容**:
- BaseRepositoryにlogical_delete()メソッドを追加
- 各Repositoryでlogical_delete()を使用
- 全Repositoryのテストケースを追加・修正

**影響ファイル**:
- src/services/BaseRepository.py (修正)
- src/services/UserRepository.py (修正)
- src/services/OrderRepository.py (修正)
- src/test/test_base_repository.py (新規)
- src/test/test_user_repository.py (修正)
- src/test/test_order_repository.py (修正)

---

### 案3: Decoratorパターンで削除処理を統一

**概要**: @logical_deleteデコレータを作成して削除処理を統一

**メリット**:
- 柔軟性が高い
- 各Repositoryで個別カスタマイズ可能
- 拡張性が高い

**デメリット**:
- 実装が複雑
- デコレータの理解が必要
- オーバーエンジニアリングの可能性

**修正内容**:
- decorators.pyにlogical_deleteデコレータを作成
- 各Repositoryの削除メソッドにデコレータを適用
- デコレータのテストケースを追加

**影響ファイル**:
- src/decorators.py (新規)
- src/services/UserRepository.py (修正)
- src/services/OrderRepository.py (修正)
- src/test/test_decorators.py (新規)
- src/test/test_user_repository.py (修正)
- src/test/test_order_repository.py (修正)

---

**選択してください**:
1. 案1: 最小限の修正（推奨）
2. 案2: BaseRepositoryでの共通処理化
3. 案3: Decoratorパターンで削除処理を統一
4. その他（具体的に教えてください）

選択した案の番号を入力してください:
```

## Phase 4. ブランチ名の決定

`.claude\docs\git-branch-strategy.md`のブランチ戦略に従い、選択された修正方針に基づいてブランチ名を提案：

```markdown
## 🌿 ブランチ名の決定

選択された修正方針: 案1（最小限の修正）

【提案するブランチ名】
fix/delete-flag-update

この名前でよろしいですか？ (y/n)
変更する場合は、希望するブランチ名を入力してください。
```

## Phase 5. コンテキストファイルの作成

収集した情報に基づいて、バグ修正用コンテキストファイルを作成：

**ファイル名**: `.context/YYYYMMDDhhmmss.md`

**コンテキスト内容（テンプレート）**:

```markdown
# コンテキスト: [バグの概要]

## 1. 背景・目的

【バグの詳細】
- 発生箇所: [ファイル名:行数]
- 期待する動作: [期待値]
- 現在の動作: [実際の動作]
- 再現手順: [再現方法]

【選択された修正方針】
- 案1: 最小限の修正（推奨）
- メリット: 影響範囲が最小限、リスクが低い
- デメリット: 根本的な設計改善にはならない

## 2. 修正方針

### 2-1. Git操作
1. 開発用ブランチ（`dev`）へ移動
2. 修正用ブランチ（`fix/XXX`）を作成・移動

### 2-2. 修正手順
1. TDD REDフェーズ: 失敗するテストケースを追加
2. TDD GREENフェーズ: バグを修正し、テストをパス
3. TDD REFACTORフェーズ: リファクタリング
4. 全テスト実行: すべてのテストがパスすることを確認

## 3. 実装の詳細

### Phase 1: 開発用ブランチへ移動

\```bash
git checkout dev
\```

### Phase 2: 修正用ブランチの作成・移動

- **ブランチ名**: `fix/delete-flag-update`

\```bash
git checkout -b fix/delete-flag-update
\```

### Phase 3: TDD REDフェーズ - 失敗するテストケースを追加

**対象ファイル**: `src/test/test_user_repository.py`

失敗するテストケースを追加：

\```python
def test_delete_updates_delete_flag():
    """削除時にis_deletedフラグが1に更新されることを確認"""
    # given
    user = User(id=1, name="test", is_deleted=0)
    repository.save(user)

    # when
    repository.delete(user.id)

    # then
    deleted_user = repository.find_by_id(user.id)
    assert deleted_user.is_deleted == 1  # このテストが失敗する
\```

テストを実行して失敗を確認：

\```bash
pytest src/test/test_user_repository.py::test_delete_updates_delete_flag -v
\```

### Phase 4: TDD GREENフェーズ - バグ修正

**対象ファイル**: `src/services/UserRepository.py`

修正内容：

\```python
def delete(self, user_id: int) -> None:
    """ユーザーを削除（論理削除）"""
    user = self.find_by_id(user_id)
    if user:
        user.is_deleted = 1  # この行を追加
        user.deleted_at = datetime.now()  # タイムスタンプも記録
        self.db.commit()
\```

テストを実行してパスを確認：

\```bash
pytest src/test/test_user_repository.py::test_delete_updates_delete_flag -v
\```

### Phase 5: TDD REFACTORフェーズ - リファクタリング

必要に応じてコードをリファクタリング（今回は不要と判断）

### Phase 6: 全テスト実行

すべてのテストが通ることを確認：

\```bash
pytest src/test/ -v
\```

## 4. 終了条件

- [x] 開発用ブランチからfix/XXXブランチを作成
- [x] 失敗するテストケースを追加（RED）
- [x] バグを修正してテストがパス（GREEN）
- [x] リファクタリング完了（REFACTOR）
- [x] 全テストがパス
- [x] コーディング規約に準拠

## 5. 使用するエージェント

- **code-explorer**: バグ発生箇所の調査
- **python-expert** または **java-expert**: 修正実装

## 6. 参照ドキュメント

- CLAUDE.md: Gitブランチ戦略、TDD方針
- 関連する設計書・仕様書
```

### Phase 6. コンテキストファイル保存と案内

```markdown
✅ バグ修正用コンテキストファイルを作成しました

📄 ファイル: `.context/20251127153000.md`

【選択された修正方針】
案1: 最小限の修正

次のステップ：

1. コンテキストファイルの内容を確認してください
2. 以下のコマンドで修正を実行できます：

\```bash
/context:action 20251127153000.md
\```

または、手動でGit操作と修正を行うこともできます。
```

---

## コンテキストファイル作成例

### 例1: 削除フラグが更新されない不具合

**ユーザ入力**:
- バグ概要: 削除フラグが更新されない
- 発生箇所: `src/services/UserRepository.py:42`
- 期待動作: delete()実行時にis_deleted=1に更新
- 現在動作: is_deletedが0のまま
- 再現手順: `UserRepository.delete(1)` 実行

**作成されるコンテキストファイル**: `.context/20251127153000.md`（上記テンプレートに基づく）

---

## 注意事項

- **MUST**: ユーザからバグ情報を収集してからコンテキスト作成
- **MUST**: 既存コード調査後、必ず複数の修正方針を提示してユーザに選択してもらう
- **MUST**: 各修正方針のメリット・デメリット・影響範囲を明示
- **MUST**: ブランチ名は `fix/XXX` 形式を厳守
- **MUST**: TDD（RED → GREEN → REFACTOR）を徹底
- **SHOULD**: code-explorerエージェントで既存コード調査
- **SHOULD**: 最低2案、推奨は3案提示する
- **NEVER**: 推測でコンテキストを作成しない
- **NEVER**: 修正方針を1つだけ提示して勝手に決定しない

---

## 参考

- コンテキスト実行: `/context:action`
- CLAUDE.md: Gitブランチ戦略、TDD方針
- git-expertエージェント: Git操作支援