from sqlalchemy.orm import Session

from app.products.models import Product
from app.products.schemas import ProductCreate, ProductUpdate


def create_product(db: Session, product_data: ProductCreate) -> Product:
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    source_website: str | None = None,
) -> list[Product]:
    query = db.query(Product).filter(Product.is_active == True)
    if source_website is not None:
        query = query.filter(Product.source_website == source_website)
    return query.offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()


def update_product(
    db: Session, product_id: int, product_data: ProductUpdate
) -> Product | None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        return None
    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> Product | None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        return None
    product.is_active = False
    db.commit()
    db.refresh(product)
    return product
