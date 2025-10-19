from os import getenv
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product
from fastapi import Request
from models import Purchase
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import status
from models import Base
from database import engine
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app-002-gen10-step3-1-node-oshima22.azurewebsites.net/"],  # Next.jsのURL http://localhost:3002
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "FastAPI 起動成功！"}

# DBセッション取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DB_USER= os.getenv("DB_USER")
DB_PASSWORD= os.getenv("DB_PASSWORD")
DB_HOST= os.getenv("DB_HOST")
DB_PORT= os.getenv("DB_PORT")
DB_NAME= os.getenv("DB_NAME")


@app.get("/api/product")
def read_product(code: str, db: Session = Depends(get_db)):
    try:
        product = db.query(Product).filter(Product.code == code.strip()).first()
        if product:
            return {
                "code": product.code,
                "name": product.name,
                "price": product.price
            }
        else:
            return {
                "code": code,
                "name": "商品がマスタ未登録です",
                "price": 0
            }
    except Exception as e:
        print(f"エラー発生: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "サーバーエラー", "detail": str(e)}
        )

@app.get("/api/products")
def get_products(db: Session = Depends(get_db)):
    try:
        products = db.query(Product).all()
        return [
            {
                "code": p.code,
                "name": p.name,
                "price": p.price
            }
            for p in products
        ]
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "商品一覧取得エラー", "detail": str(e)}
        )

@app.post("/api/purchase")
async def register_purchase(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    for item in data:
        purchase = Purchase(
            code=item["code"],
            name=item["name"],
            price=int(item["price"] * 1.1),  # 税込価格（10%）
            # price=item["price"],
            purchased_at=datetime.now().isoformat()
        )
        db.add(purchase)
    db.commit()
    return {"message": "購入履歴を保存しました(税込)"}

@app.get("/api/history")
def get_history(db: Session = Depends(get_db)):
    purchases = db.query(Purchase).order_by(Purchase.purchased_at.desc()).all()
    return [
        {
            "code": p.code,
            "name": p.name,
            "price": p.price,
            "purchased_at": p.purchased_at
        }
        for p in purchases
    ]
