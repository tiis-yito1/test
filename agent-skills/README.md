# 社内で利用する skill をまとめた repository

## skill install 方法

### npx skills を使ったパターン
npx skills でインストールができます。

> **注意**  
> すでにログイン(gh auth login)をしている前提です。  

以下のように叩くことでローカル環境（Gemini CLI等）へ追加・インストールができます。

#### 通常インストール

```sh
npx skills add https://github.com/project-gena/agent-skills.git
```

#### ブランチを指定してインストールする場合

```sh
npx skills add https://github.com/project-gena/agent-skills.git#create_readme
```

#### （参考）環境が対応している場合はSSHでも実行可能です

```sh
npx skills add git@github.com:project-gena/agent-skills.git
```

---

### github cli を使ったパターン

github cli でインストールができます。

> **注意**  
> すでにログイン(gh auth login)をしている前提です。

```sh
gh skill install project-gena/agent-skills
```

ブランチで実施する場合は以下のように `#` を後ろにつける

```sh
gh skill install git@github.com:project-gena/agent-skills.git#develop/function-list-md
```

---
