from flask import Blueprint, render_template, request

from app.models.item_model import ItemModel

bp = Blueprint("stock", __name__)


@bp.route("/stock")
def stock_page():
    # List all items
    items = ItemModel.query.all()
    return render_template("stock/stock.html", items=items)


@bp.route("/stock/search")
def search_page():
    query = request.args.get("query")
    # Show seach results if anything can be found by name, otherwise continue showing all items
    if query:
        results = ItemModel.query.filter(ItemModel.name.ilike(f"%{query}%")).all()
    else:
        results = ItemModel.query.all()

    return render_template("stock/stock_search.html", results=results)
