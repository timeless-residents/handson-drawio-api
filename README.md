# Draw.io API Hands-on

プログラムからDraw.ioダイアグラムを作成、変更、エクスポートするための実践的なプロジェクト。

## 概要

このプロジェクトは、Draw.io APIを使用して以下のことを行う方法を示しています：
- プログラムでダイアグラムを作成する
- 既存のダイアグラムを変更する
- ダイアグラムをXML形式でエクスポートする
- ダイアグラムをWebブラウザで表示する

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/timeless-residents/handson-drawio-api.git
cd handson-drawio-api

# 仮想環境を作成して有効化
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt
```

## 使い方

このプロジェクトの基本的な使い方は以下の通りです：

### 1. ダイアグラムの作成

```python
from src.drawio_api.client import DrawioAPIClient

# クライアントを初期化
client = DrawioAPIClient()

# 新しいダイアグラムを作成
diagram = client.create_diagram(title="My Diagram")

# ノードを追加（x, y座標を指定）
diagram = client.add_node(diagram, "Start", 100, 40, 120, 60)
diagram = client.add_node(diagram, "Process", 100, 160, 120, 60)
diagram = client.add_node(diagram, "End", 100, 280, 120, 60)

# ノードIDを取得
start_id = diagram["cells"][0]["id"]
process_id = diagram["cells"][1]["id"]
end_id = diagram["cells"][2]["id"]

# エッジ（接続線）を追加
diagram = client.add_edge(diagram, start_id, process_id)
diagram = client.add_edge(diagram, process_id, end_id)
```

### 2. XMLへの変換とWeb表示

```python
# ダイアグラムをXML形式にエクスポート
xml_data = client.export_diagram(diagram, format="xml")

# プレビューURLを生成
preview_url = client.get_preview_url(xml_data, title=diagram["title"])

# ブラウザでURLを開く
import webbrowser
webbrowser.open(preview_url)
```

## サンプルの実行

`examples`ディレクトリには、様々な例が含まれています：

```bash
# 簡単なフローチャートを作成してJSONとして保存
python examples/create_simple_diagram.py

# 組織図を作成してDraw.ioで開く
python examples/generate_xml_and_preview.py

# ネットワーク図を作成して独自のHTMLビューアで表示
python examples/generate_html_viewer.py
```

## 主な機能

1. **ダイアグラム作成**: `create_diagram()`を使用して新しいダイアグラムを作成
2. **ノード追加**: `add_node()`でダイアグラムにノードを追加
3. **エッジ追加**: `add_edge()`でノード間に接続線を追加
4. **エクスポート**: `export_diagram()`でJSONまたはXML形式に変換
5. **Web表示**: `get_preview_url()`で表示用URLを生成

## ディレクトリ構造

```
handson-drawio-api/
├── examples/          # サンプルスクリプト
│   ├── create_simple_diagram.py        # 基本的な使用例
│   ├── generate_xml_and_preview.py     # XML生成とWebプレビュー
│   └── generate_html_viewer.py         # HTMLビューア作成
├── src/               # ソースコード
│   └── drawio_api/    # メインパッケージ
│       ├── __init__.py
│       └── client.py  # DrawioAPIClientの実装
├── tests/             # テストスイート
├── README.md
└── requirements.txt
```

## ライセンス

MIT

## 貢献

貢献は歓迎します！プルリクエストをお気軽にお送りください。