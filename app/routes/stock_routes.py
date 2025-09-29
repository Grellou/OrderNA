from flask import Blueprint, render_template, request
from sqlalchemy import asc, desc

from app.models.item_model import ItemModel

bp = Blueprint("stock", __name__)


@bp.route("/stock", methods=["GET"])
def stock_page():
    # List all items
    items = ItemModel.query.order_by(asc(ItemModel.name))
    return render_template("stock/stock.html", items=items)


@bp.route("/stock/search")
def search_page():
    # Search query
    query = request.args.get("query")

    # Get sorting and ordering parameters
    sort_by = request.args.get("sort_by")
    order = request.args.get("order")

    # Temp query variable before calling results at the end
    query_obj = ItemModel.query

    # Show seach results if anything can be found by name, otherwise continue showing all items
    if query:
        query_obj = query_obj.filter(ItemModel.name.ilike(f"%{query}%"))

    # Sort items based on selected column, default sorting by id
    if sort_by == "name":
        sort_field = ItemModel.name
    elif sort_by == "price":
        sort_field = ItemModel.price
    elif sort_by == "quantity":
        sort_field = ItemModel.quantity
    else:
        sort_field = ItemModel.id
        order = "asc"

    # Apply ordering
    if order and order.lower() == "desc":
        query_obj = query_obj.order_by(desc(sort_field))
    else:
        query_obj = query_obj.order_by(asc(sort_field))

    # Apply sorting and search to results
    items = query_obj.all()

    if request.headers.get("HX-Request"):
        return render_template("stock/stock_search.html", items=items)
    else:
        return render_template("stock/stock.html", items=items)
