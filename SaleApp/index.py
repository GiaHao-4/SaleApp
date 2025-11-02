from itertools import product

from flask import Flask, render_template, request
import dao
app = Flask(__name__)


@app.route('/')
def index():
    q=request.args.get('q')
    cate_id=request.args.get('cate_id')
    print(q)
    prods=dao.load_products(q=q, cate_id=cate_id)
    cates=dao.load_categories()
    return render_template("index.html", prods=prods)

@app.route('/products/<int:id>')
def detail(id):
    return render_template("products-details.html", prod=dao.get_product_by_id(id))

@app.context_processor
def common_atribute():
    return {
        "cates": dao.load_categories()
    }

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
