from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import requests
import random
from datetime import datetime

url = "https://jsonplaceholder.typicode.com/photos"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    print(f"エラーが発生しました：{response.status_code}")


def get_random_stock() -> int:
    return random.randint(10, 200)


class Photo(BaseModel):
    id: int = Field(gt=0)
    title: str | None = None
    url: str
    thumbnailUrl: str

    stock: int = Field(default_factory=get_random_stock)
    price: int = 0


@field_validator("title", mode="before")
def validate_title(cls, v: str) -> str:
    return v.capitalize().strip()


@field_validator("thumbnailUrl", mode="before")
def default_if_none(cls, v: str | None) -> str:
    if v is None:
        return "デフォルト値"
    else:
        return v


@field_validator("price", mode="after")
def adjust_price(self) -> "Photo":
    self.price = (self.stock * self.price) * 1.1
    return self


box = Photo.model_validate(data)

with open("products_fianl_json", "w", encoding="utf-8") as f:
    json_stirng = box.model_dump_json(indent=2)
    f.write(json_stirng)

print("ファイルを保存しました")
