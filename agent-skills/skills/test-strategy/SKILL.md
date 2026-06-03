---
name: test-strategy
description: >
  テストコードを実装するときに使用するスキル。
  テスト種別の選定、モック境界、命名規則、各スタックのテストパターンを定義する。
  sdd-implementer の Phase 2 (TDD Execution) から参照される。
---

# Test Strategy

テスト方針・パターンを定義するスキル。
「どの粒度のテストをいつ書くか」「各スタックでどういうパターンで書くか」を統一する。

---

## テストピラミッドと判断基準

### Unit Test

- **目的**: ビジネスロジック単体の正しさを検証する。
- **特徴**: 高速、メモリ内完結、外部依存なし。
- **対象**: ドメインモデルのメソッド、Application 層のマッパー・バリデーション、ユーティリティ関数、フロントエンドのフック・ヘルパー。

### Integration Test

- **目的**: コンポーネント間の結合（DB クエリ、API エンドポイント）の正しさを検証する。
- **特徴**: 実際の DB（TestContainers）やエミュレータに接続。安易なモック化をしない。
- **対象**: Repository の CRUD 操作、API エンドポイント（`CustomWebApplicationFactory` 経由）、フィルタリング・ソートクエリ。

### Component Test (Frontend)

- **目的**: UI コンポーネントの描画と操作を検証する。
- **特徴**: Testing Library + Jest。DOM レベルの検証。
- **対象**: ボタンの状態変化、フォームの入力・送信、条件付きレンダリング。

### E2E Test

- **目的**: ユーザーシナリオ全体の動作を検証する。
- **特徴**: Playwright。原則モックなし（認証のみバイパス可）。
- **対象**: `docs/03_features/*/E2Eテストケース.md` に定義されたシナリオ。テストケース ID (`E2E-EC-XXX` 等) を参照する。

---

## モック境界の定義

| テスト種別 | DB | 外部 API (Slack 等) | 時刻 | ファイルシステム (S3) |
| :--- | :--- | :--- | :--- | :--- |
| **Unit** | モック化 | モック化 | モック化 (`FakeTimers` / 固定値) | モック化 |
| **Integration** | 実物 (TestContainers) | モックサーバー or スタブ | 実時刻 or 固定値 | モック化 or LocalStack |
| **E2E** | 実物 | 実物 (可能な場合) | 実時刻 | 実物 |

---

## 各スタックのテストパターン

### .NET (NUnit + Moq)

**Unit Test 例**:
```csharp
[TestFixture]
public class EventMapperTests
{
    private Mock<IS3Service> _s3ServiceMock;

    [SetUp]
    public void SetUp()
    {
        _s3ServiceMock = new Mock<IS3Service>();
    }

    [Test]
    public void ToDetailDto_正常なEventを渡した場合_DTOに変換されること()
    {
        // Arrange / Act / Assert
    }
}
```

**Integration Test 例**:
```csharp
[TestFixture]
public class EventCalendarApiTests
{
    private CustomWebApplicationFactory _factory;
    private HttpClient _client;

    [SetUp]
    public void SetUp()
    {
        _factory = new CustomWebApplicationFactory();
        _client = _factory.CreateClient();
    }

    [Test]
    public async Task GetEvents_イベントが存在する場合_200とリストを返すこと()
    {
        // HttpClient で API をコールし、レスポンスを検証
    }
}
```

### Next.js (Jest + Testing Library)

```tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "@/components/ui/Button";

describe("Button", () => {
  test("クリック時にonClickが呼ばれること", () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>テスト</Button>);
    fireEvent.click(screen.getByRole("button"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test("disabled時にクリックできないこと", () => {
    render(<Button disabled>テスト</Button>);
    expect(screen.getByRole("button")).toBeDisabled();
  });
});
```

### Slack (Jest + ts-jest)

```typescript
describe("eventParser", () => {
  beforeEach(() => {
    // 時刻依存のテストではタイマーを固定
    jest.useFakeTimers();
    jest.setSystemTime(new Date("2026-04-01T09:00:00+09:00"));
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it("正しいフォーマットの投稿を解析できること", () => {
    // Arrange / Act / Assert
  });
});
```

### E2E (Playwright)

```typescript
import { test, expect } from "@playwright/test";

test.describe("イベント表示・検索 (E2E-EC-007〜)", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/events");
  });

  // E2E-EC-007: ビューの切り替え
  test("カレンダーとリスト表示を切り替えられること", async ({ page }) => {
    await expect(page.getByTestId("calendar-view")).toBeVisible();
    await page.getByRole("button", { name: "リスト" }).click();
    await expect(page.getByTestId("list-view")).toBeVisible();
  });
});
```

---

## 命名規則

### ファイル名

| スタック | パターン | 例 |
| :--- | :--- | :--- |
| .NET (Unit) | `*Tests.cs` | `EventMapperTests.cs` |
| .NET (Integration) | `*ApiTests.cs` / `*Tests.cs` | `EventCalendarApiTests.cs` |
| Next.js (Component/Unit) | `*.test.tsx` / `*.test.ts` | `Button.test.tsx` |
| Slack | `*.test.ts` | `eventParser.test.ts` |
| E2E (Playwright) | `*.spec.ts` | `event-display-search.spec.ts` |

### テスト名

- 日本語で「〜の場合、〜であること」形式を推奨する。
- 例: `GetEvents_イベントが存在する場合_200とリストを返すこと`
- 例: `disabled時にクリックできないこと`

### ファイル配置

| スタック | ディレクトリ |
| :--- | :--- |
| .NET Unit | `dits-portalapp/backend/tests/Unit/` |
| .NET Integration | `dits-portalapp/backend/tests/Integration/` |
| Next.js | `dits-portalapp/frontend/src/tests/` |
| Slack | `dits-portalapp/slack/test/` |
| E2E | `dits-portalapp/frontend/e2e/` |

---

## カバレッジ目標

- 全体目標: **85%+** (`docs/02_architecture/アーキテクチャ.md` 準拠)
- CI でカバレッジレポートを artifact としてアップロードする（`.github/workflows/test.yml` 参照）。