from flask import Blueprint, render_template

from app.models.item_model import ItemModel

bp = Blueprint("stock", __name__)


@bp.route("/stock")
def stock_page():
    items = ItemModel.query.all()
    return render_template("stock/stock.html", items=items)
