from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db


# Model for shopping cart
class CartModel(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    state = db.Column(db.String, default="active", nullable=False)

    # cart.user -> user who owns this cart
    user = relationship("UserModel", back_populates="carts")

    # cart.cart_items -> list of items added to the cart
    cart_items = relationship(
        "CartItemModel", back_populates="cart", cascade="all, delete-orphan"
    )

    # One active cart per user constrain
    __table_args__ = (
        db.UniqueConstraint("user_id", "state", name="uix_user_active_cart"),
    )


# Model for items to be stored in cart
class CartItemModel(db.Model):
    __tablename__ = "cart_item"
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(
        db.Integer, ForeignKey("cart.id", ondelete="CASCADE"), nullable=False
    )
    item_id = db.Column(
        db.Integer, ForeignKey("item.id", ondelete="CASCADE"), nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float)
    total_price = db.Column(db.Float)

    # cart_item.cart -> cart that this item belongs to
    cart = relationship("CartModel", back_populates="cart_items")

    # cart_item.item -> item this entry refers to
    item = relationship("ItemModel", back_populates="cart_items")


# Model for literature and other stock
class ItemModel(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, index=True)
    category = db.Column(db.String(128), nullable=False)
    language = db.Column(db.String(24), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float)

    # item.cart_items -> list of CartItem entries where this item appears
    cart_items = relationship("CartItemModel", back_populates="item")
