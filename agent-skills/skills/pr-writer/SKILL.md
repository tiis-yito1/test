---
name: pr-writer
description: >
  PR (Pull Request) の記述を作成するスキル。
  ユーザーから PR の下書き作成を依頼されたときに使用する。
  作業成果物 (tasks/ の spec.md / plan.md) やコード差分から、
  PR テンプレートに沿った記述を生成する。
---

# PR Writer

PR テンプレート (`.github/pull_request_template.md`) に沿った PR 記述の下書きを生成するスキル。
AI はコミットやプッシュ操作を実行せず、テキスト生成のみを行う。

---

## 生成手順

1. **入力情報の収集**:
   - `tasks/{作業内容}/spec.md` から変更の目的とスコープを確認する。
   - `tasks/{作業内容}/plan.md` から設計の根拠と変更ファイル一覧を確認する。
   - `git diff` または変更ファイル一覧からコード差分を把握する。
   - 関連する GitHub Issue 番号があれば特定する。

2. **テンプレートに沿って記述を組み立てる**:
   - `.github/pull_request_template.md` の各セクションに対応する内容を生成する。

3. **出力**:
   - Markdown 形式で PR 記述の下書きを提示する。
   - ユーザーが内容を確認・修正した上で PR に貼り付ける想定。

---

## 各セクションの記述ガイド

### 概要

- 変更の目的を 1〜3 文で簡潔に書く。
- Tier 2 仕様書 (`docs/03_features/{FeatureName}/仕様.md`) への参照を含める。
- 影響範囲（Backend / Frontend / Slack / DB マイグレーション等）を明記する。

**良い例**:
```markdown
イベントカレンダーのキーワード検索機能を実装する。
`docs/03_features/イベントカレンダー/仕様.md` §2.2「検索・フィルタリング」に基づく。
Backend (API エンドポイント追加) と Frontend (検索 UI) の両方を変更。
```

**悪い例**:
```markdown
検索機能を追加しました。
```

### 細かな変更点

- ファイルまたはモジュール単位の変更サマリを箇条書きで記述する。
- レビュアーが「なぜ概要に書かれていないこれが変更されたのか」と疑問に思わないようにする。

**良い例**:
```markdown
- `backend/src/EventCalendar/EventQueryParameterHelper.cs`: 検索パラメータのパース処理を追加
- `backend/src/Api/EventsController.cs`: `GET /api/events` にクエリパラメータ `keyword` を追加
- `frontend/src/components/events/SearchBar.tsx`: 検索バーコンポーネントを新規作成
- `frontend/src/tests/components/events/SearchBar.test.tsx`: SearchBar のテストを追加
```

### 変更理由

- 「なぜこの変更が必要か」を記述する。
- Tier 2 仕様への参照、または GitHub Issue へのリンクで根拠を示す。

**良い例**:
```markdown
`docs/03_features/イベントカレンダー/仕様.md` §2.2 に定義されたキーワード検索機能の実装。
イベント数の増加に伴い、タイトル・概要からの検索による絞り込みが必要になった。
```

### 関連タスク

- `tasks/` 配下の spec.md / plan.md へのリンク。
- GitHub Issue がある場合は `#123` の形式でリンクする。
- Issue をクローズする場合は `Closes #123` と記述する。

### その他

- レビュアーへの注意事項を記述する。
- 例: 破壊的な API 変更がある場合、DB マイグレーションの確認が必要な場合、特定の順序でレビューすべき場合。
- 特になければ省略可。

---

## 参考情報: Git 規約

以下はユーザーが手動でブランチ作成やコミットを行う際の参考情報。AI はこれらの操作を実行しない。

### ブランチ命名

`feature/{add|update|fix|remove}-英語の機能名`

### コミットメッセージ

プレフィックス + 日本語の説明:
- `[add]` : 新規機能追加
- `[update]` : 機能修正（バグではない）
- `[fix]` : バグ修正
- `[remove]` : 削除