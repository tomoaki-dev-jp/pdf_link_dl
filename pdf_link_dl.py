import os
import fitz
import requests

pdf_path = "pdf"
save_dir = "downloaded_files"
os.makedirs(save_dir, exist_ok=True)

# ブラウザを模倣するUser-Agentヘッダー
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

doc = fitz.open(pdf_path)

# 重複ダウンロード防止用のセット
downloaded_urls = set()

for page_num in range(len(doc)):
    page = doc[page_num]
    links = page.get_links()

    for link in links:
        if link["kind"] == fitz.LINK_URI:
            url = link["uri"]
            if url in downloaded_urls:
                continue

            # 拡張子の判定（小文字化して判定）
            url_clean = url.split("?")[0]
            if any(url_clean.lower().endswith(ext) for ext in [".pdf", ".zip", ".xlsx", ".png"]):
                filename = os.path.basename(url_clean)
                save_path = os.path.join(save_dir, filename)
                print(f"ダウンロード試行: {url}")

                try:
                    # User-Agent を指定してリクエストを送信
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        with open(save_path, "wb") as f:
                            f.write(response.content)
                        print(f"  -> ダウンロード成功: {filename}")
                        downloaded_urls.add(url)
                    else:
                        print(f"  -> ダウンロード失敗 (HTTP status: {response.status_code}): {url}")
                except Exception as e:
                    print(f"  -> エラー発生: {url}, {e}")