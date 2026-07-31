# クイックスタート

[English](QUICKSTART.md)

この文書は，AI Development Standardをローカルで試すための最小手順です．プロジェクト全体では英語文書を正本とし，この日本語版は利便性のための翻訳として提供します．内容に差異がある場合は，英語版を優先します．

## 前提環境

- Git
- Python 3.12を推奨
- このリポジトリのローカルclone
- 空または破棄可能な導入先ディレクトリ

現在のスクリプトはPython標準ライブラリのみを使用します．

## 1．標準をcloneして検証する

```bash
git clone https://github.com/Eruhitsuji/ai-development-standard.git
cd ai-development-standard
python scripts/validate-standard.py
python scripts/run-standard-evals.py
python scripts/check-public-release.py
```

まとめて確認する場合は，次を実行します．

```bash
./scripts/check.sh
```

PowerShellでは次を実行します．

```powershell
.\scripts\check.ps1
```

## 2．標準のcommitを固定する

現在の初期化スクリプトは，ローカルcheckoutの内容を導入先へコピーします．導入したいReleaseまたはcommitを先にcheckoutし，同じcommit SHAをlockファイルへ記録してください．

Bash：

```bash
STANDARD_COMMIT="$(git rev-parse HEAD)"
```

PowerShell：

```powershell
$StandardCommit = git rev-parse HEAD
```

## 3．破棄可能なプロジェクトへ導入する

Bash：

```bash
mkdir -p ../ai-standard-example
python scripts/init-project.py \
  --project-dir ../ai-standard-example \
  --mode new \
  --commit "$STANDARD_COMMIT" \
  --profiles core python \
  --install-github-templates
```

PowerShell：

```powershell
New-Item -ItemType Directory -Force ..\ai-standard-example | Out-Null
python scripts/init-project.py `
  --project-dir ..\ai-standard-example `
  --mode new `
  --commit $StandardCommit `
  --profiles core python `
  --install-github-templates
```

## 4．生成結果を確認する

導入先には，少なくとも次が生成されます．

```text
.ai/
+-- standard.lock.yml
+-- managed/
+-- project/
AGENTS.md
CLAUDE.md
.kiro/steering/
.github/
```

主な所有範囲は次のとおりです．

- `.ai/managed/**`は共通標準から生成される領域であり，通常の機能開発では編集しません．
- `.ai/project/**`には，プロジェクト固有の規則，コマンド，役割，保証レベル，トレーサビリティ，Capability，権限，ライフサイクル設定を置きます．
- 実行可能なタスクの正本はGitHub Issuesです．

## 5．AIアシスタントから開始する

生成したプロジェクトをCodex，Claude Code，Kiro，または互換AIで開き，例えば次のように依頼します．

```text
今は何をすべきですか？
この初期化結果を確認し，不足している基盤タスクを示してください．
この要件を小さなGitHub Issuesへ分割してください．
この機能案が既存Capabilityと重複していないか確認してください．
人間の判断が必要な項目だけを教えてください．
```

AIは入口ファイルを読み，`.ai/project/CONTEXT_INDEX.yml`を通して関係する標準だけを読み込み，利用可能なリポジトリ状態を確認した上で，簡潔な推奨または判断依頼を提示します．

## 6．既存プロジェクトへの導入計画を確認する

既存リポジトリを変更する前に，保守的な導入計画を生成します．

```bash
python scripts/plan-adoption.py \
  --project-dir ../existing-project \
  --profiles core python
```

その後，専用の導入Issue，branch，Pull Requestを使用します．既存のAI指示，CI，所有者設定，GitHubテンプレートは原則として保持され，置き換える場合は明示的なレビューを必要とします．

## 現在の制限

このPreviewでは，次はまだ実装されていません．

- 評価シナリオを実際のAIモデルへ入力する実行評価
- GitHub Projects，Labels，Rulesets，Teams，Merge Queueの自動設定
- Release artifactの自動取得と検証
- `--commit`と現在のローカルcheckoutが一致することの検証
- 下流プロジェクト向け標準更新Pull Requestの完全自動生成

現在の対象範囲と安定性については，[Project Status](PROJECT_STATUS.md)を参照してください．
