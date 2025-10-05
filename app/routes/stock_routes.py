from flask import Blueprint, render_template, request
from sqlalchemy import asc, desc

from app.models.item_model import ItemModel

bp = Blueprint("stock", __name__)


@bp.route("/stock", methods=["GET"])
def stock_page():
    # List all items
    items = ItemModel.query.order_by(asc(ItemModel.name))
    return render_template("stock/stock.html", items=items)
