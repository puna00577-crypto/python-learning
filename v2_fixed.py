import requests
import random
import json
from pydantic import BaseModel, Field, field_validator


def get_random_stock() -> int:
    return random.randint(10, 200)


class Photo(BaseModel):
    id: int = Field(gt=0)
    title: str
    url: str
    thumbnailUrl: str | None = None

    stock: int = Field(default_factory=get_random_stock)
    price: int = 0  # 後で計算するので初期値は0でOK

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str | None) -> str:  # 正常終了時はstrを返す
        if not v or v.strip() == "":
            raise ValueError("タイトルは必須です")
        return v.strip().capitalize()



def main():
    try:
        url = "https://jsonplaceholder.typicode.com/photos"

        print("🌐 APIからデータを取得中...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        raw_data = response.json()

        photos = []
        for item in raw_data[:50]:
            photo = Photo.model_validate(item)

            # ここで価格を計算
            photo.price = int(photo.stock * 100 * 1.1)
            photos.append(photo)

        # JSON保存
        data = []
        for p in photos:
            photo_dic = p.model_dump()
            data.append(photo_dic)

        with open("products_final.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 集計表示
        total_price = 0
        for p in photos:
            total_price += p.price

        if photos:
            avg_price = total_price / len(photos)
        else:
            avg_price = 0

        print(f"✅ 処理完了！ {len(photos)}件のデータを保存しました")
        print(f"   合計価格: {total_price:,}円")
        print(f"   平均価格: {avg_price:,.0f}円")

    except requests.exceptions.RequestException as e:
        print(f"❌ APIリクエストエラー: {e}")
    except Exception as e:
        print(f"❌ 予期せぬエラー: {e}")


if __name__ == "__main__":
    main()
