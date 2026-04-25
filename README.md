# Props Lab — 公式サイト

別府の宿泊施設に特化した IT・Web 運用支援サービス「Props Lab」の公式サイト。

## 構成

純粋な静的 HTML サイト。ビルドツール・フレームワーク不要。

```
/
├── index.html       — トップ
├── about.html       — わたしたちのこと
├── service.html     — サービス
├── pricing.html     — 料金
├── contact.html     — お問い合わせ
└── assets/
    ├── favicon.svg / favicon-32.png / apple-touch-icon.png
    ├── ogp.png
    └── hero-japanese-room.png
```

- CSS は各 HTML の `<style>` ブロックにインライン
- 外部依存は Google Fonts のみ（ランタイム読み込み）

## ローカルプレビュー

```sh
python -m http.server 8000
```

ブラウザで `http://localhost:8000/` を開く。

## お問い合わせフォーム

`contact.html` のフォームは `mailto:` 送信方式。送信ボタン押下で入力内容を整形した本文付きでメールクライアントが起動する。デプロイ先が決まったタイミングで Formspree / Netlify Forms 等への差し替えを想定。
