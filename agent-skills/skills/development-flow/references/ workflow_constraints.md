# Workflow Constraints & Rules

このドキュメントは `development-flow` スキルが実行されるプロセス全体において、AIが遵守しなければならない絶対的なルールと制約を定義します。

## 1. Directory & Architecture
プロジェクトはモノレポ構成（`try1-dits-portalapp/`）および Clean Architecture を採用しています。ファイルの読み書きにおいて以下の権限と配置ルールを遵守してください。

- **`docs/` (仕様書)**: 
  - **Absolute Rule**: このディレクトリは原則として **READ ONLY** です。AIが自律的に仕様を書き換えることは固く禁じます。仕様変更（Case D）の際は、変更案を提示して必ずユーザーの承認を得てください。
- **Frontend (`dits-portalapp/frontend/`)**: 
  - プレゼンテーション層に徹し、ビジネスロジックを持たせないでください。
- **Backend (`dits-portalapp/backend/`)**:
  - `src/Core/`: Domain (ドメインモデル) と Application (ユースケース) を配置します。ここのプロジェクトは `src/Infrastructure` や外部ライブラリ（NuGet パッケージ等）に依存してはいけません。
  - `src/Infrastructure/`: DB (EF Core) や外部連携 (Slack, S3) の実装を配置してください。

## 2. Checkpoints (関所ルール)
他のスキル（`sdd-implementer` 等）を呼び出して進行する際、以下の関所で必ず停止し、ユーザーの承認（Goサイン）を得てください。

- **[Checkpoint 1] Phase 1 (詳細設計) 完了時**:
  - `tasks/{作業内容}/spec.md` と `plan.md` を作成後、共通仕様 (`DateTime.UtcNow` の使用等) に反していないか監査してください。
  - **Absolute Rule**: ユーザーから「設計OK」の明示的な合意を得るまで、絶対に Phase 2 (コード実装) に進んではなりません。

- **[Checkpoint 2] Phase 2 (TDD Execution) 実行中**:
  - TDDサイクル（Red -> Green -> Refactor）を回す際、一度の応答でテストコードと本体コードを同時に出力しないでください。
  - **Absolute Rule**: テストを実行する際、AIがコマンド実行ツールを持っている場合は自律的に実行し、持っていない場合はユーザーに実行とエラーログの提示を依頼して、対話のターンを分割してください。

## 3. Communication & Git Operations
- **Stop & Confirm**: ユーザーが詳細設計を飛ばして「コードを書いて」と指示した場合、推測で進めず、即座に実装を停止して Phase 1 (設計) へ誘導してください。
- **Git 操作の禁止**: 
  - **Absolute Rule**: AIが自発的に `git commit` や `git push` 等の操作を実行することを固く禁じます。必要な場合は `git-operations` スキルに従い、ユーザーの明示的な指示を待ってください。