## 概要

指定した、はてなユーザーのブックマークを探索し、自分が興味のあるサイトをレコメンドするプログラムです。
仕組みとしては、

1. 指定したユーザーのブックマーク一覧を取得
1. ブックマークをしているユーザーのブックマークを取得
1. ブックマークが多いURLを通知

という、シンプルな仕組みです。  

[はてなブックマーク記事のレコメンドシステムを作成　PythonによるはてなAPIの活用とRによるモデルベースレコメンド](http://overlap.hatenablog.jp/entry/2013/06/30/232200)を参考にさせていただきました。  

## 使い方

### 環境

以下の環境が必要です。

* Python(2.7 / 3.6)

*Windowsでの動作は確かめていません。*  

### インストール

本リポジトリをクローンするだけです。  
virtualenvを利用している人は適宜、利用してください。  

```bash
git clone https://github.com/pyohei/hatena-bookmark-recommender
cd hatena-bookmark-recommender
pip install -r requirements.txt
```

### 実行

以下のコマンドで実行できます。

```bash
python main.py `はてなユーザー名`
```

実行後にレコメンド結果を実行フォルダの配下に、`recommend.txt`という名前で出力します。  
データはデフォルトでは`sample/hatena.db`に保存されます（sqlite形式）。  


## その他

ブックマーク数が多い場合、結構時間がかかります。  
また、個人用に作成しているため、割と適当に作っていますので、ご了承を。
その他ご希望があれば連絡をください。  

## ライセンス

* MIT
