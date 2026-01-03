# Code Reviewer Command

## 概要
コードの総合的なレビューを行うカスタムスラッシュコマンド。複数の専門エージェントを使用してコードを多角的に分析し、優先順位付きの改善提案を提供します。

## 実行内容

### 1. 多角的レビューの実行
以下の専門エージェントを並列で実行してコードレビューを行います：

- **code-design-reviewer**: コードの品質、美しさ、設計の一貫性をレビュー
- **performance-reviewer**: 性能要件とパフォーマンスの最適化をレビュー
- **security-reviewer**: セキュリティ脆弱性と安全性をレビュー

### 2. 結果の統合と優先順位付け
各エージェントの結果を統合し、以下の基準で優先順位を決定：

1. **Critical**: セキュリティ脆弱性、重大なパフォーマンス問題
2. **High**: 設計の不整合、保守性に関わる問題
3. **Medium**: コード品質の改善、軽微な最適化
4. **Low**: スタイル調整、推奨事項

### 3. ユーザー承認と提案
優先順位付きの改善提案をユーザーに提示し、実装の承認を得ます。

### 4. コンテキストファイル生成
承認された修正内容を構造化してコンテキストファイル（`.context/YYYYMMDDhhmmss.md`）に出力し、実行を促します。

## 使用方法

```
/code-reviewer [対象ファイル/ディレクトリ]
```

### 例
```
/code-reviewer src/
/code-reviewer src/components/UserAuth.tsx
/code-reviewer
```

## 出力形式

### レビュー結果サマリー
```
## コードレビュー結果

### Critical Issues (即座に修正が必要)
- [セキュリティ] パスワードのハードコーディング detected in auth.js:23
- [パフォーマンス] N+1クエリ問題 in UserService.ts:45

### High Priority Issues
- [設計] 単一責任原則違反 in PaymentProcessor.ts
- [パフォーマンス] 不適切なレンダリング最適化 in ProductList.tsx

### Medium Priority Issues
- [コード品質] 複雑すぎる条件分岐 in validateInput.ts:67
- [保守性] マジックナンバーの使用 in config.ts

### Low Priority Issues
- [スタイル] 命名規則の不整合
- [推奨] TypeScriptの型定義改善
```

### コンテキストファイル出力
修正が承認された項目について、実装可能な形でコンテキストファイルに記録します。

## 注意事項
- レビュー対象を明示的に指定しない場合、コードディレクトリ（src/）全体を対象とします
- 各エージェントは独立して動作し、結果を総合的に評価します
- Critical/Highレベルの問題については、修正の緊急性を強調します
