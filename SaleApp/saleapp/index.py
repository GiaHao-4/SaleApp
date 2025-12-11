from saleapp import app

from flask import render_template, request
from saleapp import dao
import math


@app.route('/')
def index():
    q=request.args.get('q')
    cate_id=request.args.get('cate_id')
    page=request.args.get('page')
    print(q)
    prods= dao.load_products(q=q, cate_id=cate_id, page=page)
    pages = math.ceil(dao.count_products()/app.config["PAGE_SIZE"])
    cates= dao.load_categories()
    return render_template("index.html", prods=prods, pages=pages)

@app.route('/products/<int:id>')
def detail(id):
    return render_template("products-details.html", prod=dao.get_product_by_id(id))

@app.context_processor
def common_atribute():
    return {
        "cates": dao.load_categories()
    }

@app.route('/login')
def login_my_user():
    return render_template("login.html")

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
