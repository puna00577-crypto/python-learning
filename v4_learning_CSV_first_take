import requests  # 1. APIからデータを取得
import random  # 2. 在庫数をランダム生成（課題で使う場合）
import pandas as pd  # 3. データ加工・CSV/Excel出力

from pydantic import BaseModel, Field, field_validator, ConfigDict  # 4. データ検証
from typing import Optional


class CryptoCoin(BaseModel):
    id: str
    symbol: str
    name: str
    image: Optional[str] = None
    current_price: float
    market_cap: Optional[float] = None
    market_cap_rank: Optional[int] = None
    price_change_percentage_24h: Optional[float] = None
    last_updated: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

    # 後で追加するフィールド
    price_jpy: float = Field(default=0.0)
    market_cap_jpy: float = Field(default=0.0)
    status: str = Field(default="不明")


def main():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {"vs_currency": "usd", "per_page": 50, "page": 1, "sparkline": False}
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()  # エラー対策

        raw_data = response.json()

        box_1 = []
        for item in raw_data:
            be_object = CryptoCoin.model_validate(item)

            be_object.price_jpy = float(be_object.current_price * 150)
            be_object.market_cap_jpy = float(be_object.market_cap * 150)

            change = be_object.price_change_percentage_24h or 0

            if change >= 5.0:
                be_object.status = "非常に良好"
            elif change >= 2.0:
                be_object.status = "良好"
            elif change >= -2.0:
                be_object.status = "横ばい"
            elif change >= -5.0:
                be_object.status = "要注意"
            else:
                be_object.status = "危険"

            box_1.append(be_object)

        box_2 = []
        for i in box_1:
            original = i.model_dump()
            box_2.append(original)

        df = pd.DataFrame(box_2)  # ここでpandasが利用しやすいようにデータを整える

        column_order = [
            "id",
            "symbol",
            "name",
            "current_price",
            "price_jpy",
            "price_change_percentage_24h",
            "status",
            "market_cap",
            "market_cap_jpy",
            "market_cap_rank",
            "last_updated",
        ]

        df = df[column_order]

        df = df.rename(
            columns={
                "id": "コインID",
                "symbol": "シンボル",
                "name": "コイン名",
                "current_price": "価格(USD)",
                "price_jpy": "価格(円)",
                "price_change_percentage_24h": "24h変動率(%)",
                "status": "評価",
                "market_cap": "時価総額(USD)",
                "market_cap_jpy": "時価総額(円)",
                "market_cap_rank": "ランキング",
                "last_updated": "最終更新",
            }
        )

        df.to_csv("crypto_prices.csv", index=False, encoding="utf-8")
        print("✅ crypto_prices.csv を保存しました")

        print("\n=== 仮想通貨価格監視結果 ===")
        print(f"取得コイン数: {len(df)}件")
        print(
            f"最高価格コイン: {df.loc[df['価格(円)'].idxmax(), 'コイン名']} "
            f"({df['価格(円)'].max():,}円)"
        )
        print(
            f"最低価格コイン: {df.loc[df['価格(円)'].idxmin(), 'コイン名']} "
            f"({df['価格(円)'].min():,}円)"
        )
        print(f"平均24h変動率: {df['24h変動率(%)'].mean():.2f}%")

        danger = df[df["評価"] == "危険"]

        if not danger.empty:
            print(f"\n⚠️ 注意: 危険評価のコインが {len(danger)}件あります")

    except requests.exceptions.RequestException as e:
        print(f"❌ APIリクエストエラー: {e}")
    except Exception as e:
        print(f"❌ 予期せぬエラー: {e}")


if __name__ == "__main__":
    main()
