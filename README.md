<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [ETFデータ変換およびAPI](#etf%E3%83%87%E3%83%BC%E3%82%BF%E5%A4%89%E6%8F%9B%E3%81%8A%E3%82%88%E3%81%B3api)
  - [機能](#%E6%A9%9F%E8%83%BD)
  - [非ルートユーザーでの実行](#%E9%9D%9E%E3%83%AB%E3%83%BC%E3%83%88%E3%83%A6%E3%83%BC%E3%82%B6%E3%83%BC%E3%81%A7%E3%81%AE%E5%AE%9F%E8%A1%8C)
  - [はじめに](#%E3%81%AF%E3%81%98%E3%82%81%E3%81%AB)
    - [前提条件](#%E5%89%8D%E6%8F%90%E6%9D%A1%E4%BB%B6)
    - [1. 設定](#1-%E8%A8%AD%E5%AE%9A)
      - [URLとUser-Agent](#url%E3%81%A8user-agent)
      - [データ取得頻度の設定](#%E3%83%87%E3%83%BC%E3%82%BF%E5%8F%96%E5%BE%97%E9%A0%BB%E5%BA%A6%E3%81%AE%E8%A8%AD%E5%AE%9A)
    - [2. アプリケーションの実行](#2-%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AE%E5%AE%9F%E8%A1%8C)
  - [API利用](#api%E5%88%A9%E7%94%A8)
    - [エンドポイント: `GET /{coin_type}`](#%E3%82%A8%E3%83%B3%E3%83%89%E3%83%9D%E3%82%A4%E3%83%B3%E3%83%88-get-coin_type)
      - [クエリパラメータ](#%E3%82%AF%E3%82%A8%E3%83%AA%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF)
      - [リクエスト例](#%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%E4%BE%8B)
      - [レスポンス例 (`btc`)](#%E3%83%AC%E3%82%B9%E3%83%9D%E3%83%B3%E3%82%B9%E4%BE%8B-btc)
    - [エンドポイント: `GET /{coin_type}/latest`](#%E3%82%A8%E3%83%B3%E3%83%89%E3%83%9D%E3%82%A4%E3%83%B3%E3%83%88-get-coin_typelatest)
      - [リクエスト例](#%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88%E4%BE%8B-1)
      - [レスポンス例 (`btc`)](#%E3%83%AC%E3%82%B9%E3%83%9D%E3%83%B3%E3%82%B9%E4%BE%8B-btc-1)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# cec(crypto etf converter) - ETFデータ変換およびAPI

このプロジェクトは、様々な暗号通貨のETF（上場投資信託）フローデータを自動的に取得し、CSV形式に変換し、RESTful APIを介して提供するための一連のサービスを提供します。

## 機能

## それぞれのコンテナ
-   `fetcher-service`: 指定されたURLからETFフローデータを定期的に取得し、HTML形式で保存します。
  - Denoを使用して実装されています。
    - このwasmライブラリを仕様しています: [GitHub - b-fuze/deno-dom: Browser DOM & HTML parser in Deno](https://github.com/b-fuze/deno-dom)  
  - コンテナ間(`converter-service`)でのみ機能する内部APIとして機能してます。  
-   `converter-service`: 取得したHTMLデータを解析し、CSV形式に変換します。
    - Pythonを使用して実装されています。
    - このコンテナ自体は、`fetcher-service`のAPIを介してHTMLデータを取得します。  
-   `api-service`: 変換されたCSVデータを読み込み、RESTful APIを介してクライアントに提供します。
  - Python(FastAPI)を使用して実装されています。
  - `converter-service`が最初のCSVデータセットを生成した後に利用可能になります。

## APIサーバが不要な場合
`api-service` コンテナを起動しないことで、APIサーバーを無効にできます。`docker-compose.yml` ファイルから `api-service` セクションを削除するか、`docker-compose up` コマンドで特定のサービスのみを指定して起動してください。  

```bash
docker-compose up --build -d fetcher converter
```

## 非ルートユーザーでの実行

デフォルトでは、Dockerコンテナはrootユーザーとして実行されます。セキュリティを向上させるために、`userns-remap`機能を使用して、コンテナを非rootユーザーとして実行するようにDockerデーモンを設定することが推奨されます。

コンテナ内のrootユーザーがホスト上の非特権ユーザーにマッピングされ、潜在的な脆弱性のリスクが軽減されます。  

設定方法の詳細については、以下のドキュメントを参照してください。
[Dockerのuserns-remap機能でコンテナをroot以外のユーザで実行する](https://makiuchi-d.github.io/2024/06/08/klabtechbook11-docker-userns-remap.ja.html)

## はじめに

### 前提条件

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 1. 設定

#### URLとUser-Agent

アプリケーションを実行する前に、プロジェクトルート (`cec/`) にある `.env` ファイルを編集して、取得URLとUser-Agentを設定できます。このファイルが存在しない場合は、`.env.example` をコピーして作成してください。

```bash
cp .env.example .env
```

```env
# すべてのフェッチリクエストで使用するUser-Agent
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"

# ETFデータ用のURL
ETF_BTC_URL="https://farside.co.uk/bitcoin-etf-flow-all-data/"
ETF_ETH_URL="https://farside.co.uk/ethereum-etf-flow-all-data/"
ETF_SOL_URL="https://farside.co.uk/sol/"
```

#### データ取得頻度の設定

`converter-service`（HTMLからCSVへの変換）は、デフォルトで30分（1800秒）ごとに実行されます。この間隔を変更するには、`docker-compose.yml` ファイルの `converter` サービスに `command` を追加して、実行時の引数を指定します。

例えば、間隔を1時間（3600秒）に変更するには、以下のように `command` を追加します。

```yaml
# docker-compose.yml の converter サービスを編集

  converter:
    build: ./converter-service
    container_name: converter-service
    command: ["python", "main.py", "--interval", "3600"] # この行を追加
    volumes:
      - csv_data:/app/csv_output
    depends_on:
      fetcher:
        condition: service_healthy
    environment:
      - DENO_API_URL=http://fetcher:8000
    env_file:
      - ./.env
```

変更後は、`docker-compose up --build -d` を実行してサービスを再ビルド・再起動してください。

### 2. アプリケーションの実行

すべてのサービスを開始するには、`cec` ディレクトリに移動し、次のコマンドを実行します。

```bash
# すべてのサービスをビルドし、デタッチモードで開始
docker-compose up --build -d
```

`converter-service` が開始され、データを取得し、初期CSVファイルを作成します。その後、30分ごとにこのプロセスを繰り返します。`api-service` は、最初のCSVセットが生成されると利用可能になります。

サービスを停止するには、以下を実行します。
```bash
docker-compose down
```

## API利用

APIサーバーは `http://localhost:8080` で動作します。`curl` のようなHTTPクライアントを使用して操作できます。APIは、構造化されたJSON形式でETFフローデータを提供します。

**公開デプロイに関する注意点:**
本アプリケーションを公開環境で運用する場合、エンドポイントのパスをより適切に管理するために、リバースプロキシ（Nginxなど）を導入し、`/api/etf/[coin]` のようなプレフィックスでエンドポイントをルーティングすることを強く推奨します。または、アプリケーションコードを改変し、内部的に`/api/etf`のプレフィックスを使用するように設定することも検討してください。

### エンドポイント: `GET /{coin_type}`

特定のコインの日次ETFフローデータリストを取得します。フィルタリングとページネーションに対応しています。

-   **`coin_type`** (パスパラメータ): クエリ対象のコイン。サポートされている値は `btc`、`eth`、`sol` です。

#### クエリパラメータ

-   **`limit`**: `integer` (オプション、デフォルト: `30`) - 返されるレコードの最大数。
-   **`offset`**: `integer` (オプション、デフォルト: `0`) - ページネーションの開始オフセット。
-   **`from`**: `string` (オプション、形式: `YYYY-MM-DD`) - フィルタリングの開始日。
-   **`to`**: `string` (オプション、形式: `YYYY-MM-DD`) - フィルタリングの終了日。

#### リクエスト例

ビットコインの直近2件のレコードを取得します。

```bash
curl "http://localhost:8080/btc?limit=2" | jq
```

#### レスポンス例 (`btc`)

```json
[
  {
    "date": "2024-01-19",
    "total": 625.7,
    "flows": {
      "IBIT": 396.3,
      "FBTC": 235.1,
      "BITB": 86.3,
      "ARKB": 105.7,
      "BTCO": 11.9,
      "EZBC": 31.5,
      "BRRR": 20.9,
      "HODL": 10.1,
      "BTCW": 3.9,
      "GBTC": -598.9
    }
  },
  {
    "date": "2024-01-18",
    "total": 440.0,
    "flows": {
        "IBIT": 358.4,
        "FBTC": 178.2,
        "BITB": 69.5,
        "ARKB": 87.5,
        "BTCO": 8.9,
        "EZBC": 25.4,
        "BRRR": 12.1,
        "HODL": 9.2,
        "BTCW": 2.1,
        "GBTC": -582.3
    }
  }
]
```

---

### エンドポイント: `GET /{coin_type}/latest`

特定のコインの最新の日次ETFフローデータのみを取得します。

-   **`coin_type`** (パスパラメータ): クエリ対象のコイン。サポートされている値は `btc`、`eth`、`sol` です。

#### リクエスト例

```bash
curl http://localhost:8080/btc/latest | jq
```

#### レスポンス例 (`btc`)

```json
{
  "date": "2024-01-19",
  "total": 625.7,
  "flows": {
    "IBIT": 396.3,
    "FBTC": 235.1,
    "BITB": 86.3,
    "ARKB": 105.7,
    "BTCO": 11.9,
    "EZBC": 31.5,
    "BRRR": 20.9,
    "HODL": 10.1,
    "BTCW": 3.9,
    "GBTC": -598.9
  }
}
```
