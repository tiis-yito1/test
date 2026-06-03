---
name: sdd-implementer
description: >
  仕様書に基づいた Spec-Driven & Test-Driven Development でコードを実装するスキル。
  ユーザーから実装タスクを依頼されたとき、または tasks/ 配下の plan.md / spec.md を
  作成・実行するときに使用する。
---

# SDD & TDD Implementer

Spec-Driven & Test-Driven Development に基づいてコードを実装するスキル。
Phase 1 で合意した設計に従い、テストファーストでコードを書く。

---

## Coding Standards & Constraints

実装品質を担保するため、以下のルールをコード生成時に即時適用すること。

### Language & Naming

- Code: 変数・関数・クラス名は英語。
- Comments/Docs: コメント・ドキュメント・コミットメッセージは日本語。特に、コード中のコメントは、たとえ数行の簡単なものであっても必ず日本語で記述すること。
- Ubiquitous Language: `docs/01_product/用語集.md` に定義された用語を厳守し、勝手な訳語や略語を作らない。
- Naming Convention: 既存コードベースの命名規則 (PascalCase, camelCase, snake_case 等) を解析し、それに完全準拠する。
- Type Safety: 静的型付け言語の場合、`any` や `unknown` の使用を極力避け、厳格な型定義を行う。

### Code Quality

- 可読性第一: トリッキーな最適化を避け，誰が読んでも理解できるコードを書く
- マジックナンバー排除: 意味のある定数として定義する
- ネスト制限: 深いネスト (3段階以上) を避け，早期リターン (Early Return) や関数分割を行う
- リンター優先: プロジェクトに Linter/Formatter 設定がある場合，その設定を絶対的な正とする

### Security & Integrity

- Fail Fast: データ欠損や異常時は，安易なデフォルト値 (空文字列, 0, null) で埋めて隠蔽せず，即座にエラー/例外として扱う
- Error Handling: まずプロジェクト内の既存のエラー定義（Error クラスや Result 型）を確認し、該当するものがあれば使用する。不足している場合のみ、何が起きたか判別可能なカスタムエラーを新規定義する。
- 機密情報: API キーやパスワードのハードコードは厳禁とし，環境変数やシークレット管理を提案する
- 破壊的操作: 削除，スキーマ変更等の不可逆操作は，実行前に必ずユーザーの明示的な承認を得る
- Dependencies: 標準ライブラリを優先する。新たな外部ライブラリ導入は `Tier 3` での合意を必須とする。

---

## SDD & TDD Workflow

以下の 3 フェーズを厳守すること。Phase 1 をスキップしていきなり Phase 2 に進むことを禁止する。

### Phase 1: Context Checking, Decomposition & Detailed Design

タスクの規模に応じて深さを調整するが、以下の手順は必ず実行する。
成果物は `tasks/{作業内容}/spec.md`（実装仕様）と `tasks/{作業内容}/plan.md`（タスクリスト）に整理する。
テンプレートは本スキルの `references/spec-template.md`, `references/plan-template.md` を参照すること。

1. **Context Checking:**
   - 作業対象の機能に関連するファイルを特定するため、まずは `docs/` のファイルリストや関連しそうなコードのディレクトリ構造を確認する。
   - 必要なファイルのみを特定して読み込み、仕様と現状のギャップを把握する。無関係なファイルをコンテキストに含めないこと。

2. **Decomposition:**
   - 仕様全体を、コミット可能な最小単位（Sub-task）に分割する案を提示する。
   - スモールスタートが望ましい場合は、最終的なゴール含めて提示する。
   - 例: 「1. DBマイグレーション」「2. ドメインモデル実装」「3. Repository実装」

3. **spec.md 作成 → ユーザー承認:**
   - 選択されたタスクについて、`spec-template.md` に従い実装仕様を作成する。
   - spec.md にはスコープ、振る舞い定義、設計（既存資産・根拠・ファイル・依存・インターフェース）、テストケース、受け入れ基準を含める。
   - 設計案が複数ある場合は、1 案に決め打ちせず比較表（メリット・デメリット）を提示してユーザーと合意してから採用すること。
   - **ユーザーの承認を得るまで次のステップに進まないこと。**

4. **plan.md 作成:**
   - spec.md の承認後、`plan-template.md` に従いタスクリストを作成する。
   - plan.md には Sub-task の実行順序と状態管理テーブルを含める。

### Phase 2: TDD Execution

Phase 1 で合意した spec.md に基づき、plan.md のタスク順に TDD サイクルを回す。

1. **Red**: 合意したテストケースをコード化する。テストは失敗する。
   - Constraint: 外部依存（DB, API, 時刻など）は適切にモック化し、単体テストの独立性を保つこと。
   - Test Scope Strategy: テスト種別の選定、モック境界、命名規則は `test-strategy` Skill を参照すること。
2. **Green**: 設計プラン通りの実装を行い、テストを通過させる。過剰な先行実装を行わないように Decomposition しておく。
   - Constraint: 設計プランに含まれていないライブラリやファイルを勝手に追加しない。合意を必ず取る。
3. **Refactor**: Coding Standards および `code-reviewer` Skill のチェックリストを基準に構造を改善する。

### Phase 3: Verification

- spec.md §7 の受け入れ基準 (Acceptance Criteria) をチェックリストとして検証する。
- レビュー観点の詳細チェックリストは `code-reviewer` Skill を参照すること。
- リンターやフォーマッターがあれば適用する。
- plan.md のタスク一覧の状態列を `完了` に更新する。

---

## Directory & File Integrity

- `docs/`: **READ ONLY**。正解となる仕様。AIはここから逸脱してはならない。もし修正が必要な場合はユーザーに提案する。
- `tasks/`: READ / WRITE。Phase 1 で作成した spec.md（実装仕様）と plan.md（タスクリスト）を保存する場所。タスク完了後は plan.md の状態列を `完了` に更新すること。
- `dits-portalapp/`: READ / WRITE。実装コードやテストコード。Phase 1 で定義されたパスにのみ配置する。