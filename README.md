# pdf_link_dl

PDF 内のハイパーリンクから、指定拡張子のファイルを一括ダウンロードするスクリプトです。

各ページの URI リンクを走査し、`.pdf` / `.zip` / `.xlsx` / `.png` で終わる URL だけを取得します。同じ URL は 1 回だけダウンロードします。

## 必要環境

- Python 3
- [PyMuPDF](https://pymupdf.readthedocs.io/)（`fitz`）
- [requests](https://requests.readthedocs.io/)

## セットアップ

```bash
pip install -r requirements.txt
```

## 使い方

1. 対象 PDF を、スクリプトと同じディレクトリに `pdf` というファイル名で置きます（拡張子なし）。
2. スクリプトを実行します。

```bash
python pdf_link_dl.py
```

ダウンロードしたファイルは `downloaded_files/` に保存されます。ディレクトリが無い場合は自動で作成します。

```
.
├── pdf                 # 入力 PDF（ファイル名は固定）
├── pdf_link_dl.py
├── requirements.txt
└── downloaded_files/   # 出力先（実行時に作成）
    ├── example.pdf
    └── data.xlsx
```

## 動作

1. `pdf` を開き、全ページのリンクを取得する
2. URI リンクだけを対象にする（ページ内ジャンプなどは無視）
3. クエリ文字列（`?` 以降）を除いた URL が、次のいずれかの拡張子で終わるものだけ処理する
   - `.pdf`
   - `.zip`
   - `.xlsx`
   - `.png`
4. ファイル名は URL の末尾（`os.path.basename`）を使う
5. ブラウザ相当の `User-Agent` を付けて GET し、HTTP 200 なら保存する
6. 成功した URL は記録し、以降はスキップする

進捗・成功・失敗は標準出力に出ます。

```
ダウンロード試行: https://example.com/files/report.pdf
  -> ダウンロード成功: report.pdf
  -> ダウンロード失敗 (HTTP status: 404): ...
  -> エラー発生: ..., ConnectionError(...)
```

## 設定

スクリプト先頭の定数を書き換えて使います。

| 変数 | 初期値 | 意味 |
| --- | --- | --- |
| `pdf_path` | `"pdf"` | 入力 PDF のパス |
| `save_dir` | `"downloaded_files"` | 保存先ディレクトリ |

対象拡張子はコード内のリストで指定しています。

```python
[".pdf", ".zip", ".xlsx", ".png"]
```

リクエストはタイムアウト 10 秒、Chrome を模倣した `User-Agent` 付きです。

## 注意

- 入力ファイル名は `pdf` 固定です。別名の PDF を使う場合は `pdf_path` を変更してください。
- 拡張子の判定は URL パスだけです。クエリや `Content-Disposition` は見ません。
- 保存名が同じだと、後から来たファイルで上書きされます。
- リダイレクト先の実体が別拡張子でも、元 URL の拡張子で判定します。
- 認証が必要な URL や、ボット対策の強いサイトでは失敗することがあります。
