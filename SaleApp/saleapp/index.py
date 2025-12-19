import sqlalchemy
print("PHIEN BAN SQLALCHEMY HIEN TAI:", sqlalchemy.__version__)
from saleapp import app
from flask import render_template, request, redirect, session, jsonify
from saleapp import dao, login, admin, db
import math
from flask_login import login_user, current_user, logout_user, login_required
import cloudinary.uploader
from decorators import anonymous_required

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

@app.route("/register", methods=["GET", "POST"])
def register():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm= request.form.get('confirm')

        if password.__eq__(confirm):
            name = request.form.get('name')
            username = request.form.get('username')
            file=request.files.get('avatar')
            file_path=None
            if file:
                res=cloudinary.uploader.upload(file)
                file_path = res["secure_url"]
            try:
                dao.add_user(name=name, username=username, password=password, avatar=file_path)
            except Exception as e:
                db.session.rollback()
                print("LỖI ĐĂNG KÝ:", str(e))
                err_msg="Hệ thống đang bị lỗi, vui lòng quay lại sau"
        else:
            err_msg = "Mật khẩu không khớp"
    return render_template('register.html', err_msg=err_msg)

@app.route('/login', methods=['GET', 'POST'])
@anonymous_required
def login_my_user():
    err_msg = None

    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user=dao.auth_user(username, password)
        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg="Tài khoản hoặc mật khẩu không đúng"
    return render_template("login.html", err_msg=err_msg)

@app.route('/admin-login', methods=['POST'])
def admin_login_process():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username, password)
    if user:
        login_user(user)
        return redirect('/admin')
    else:
        err_msg = "Tài khoản hoặc mật khẩu không đúng"
@app.route('/logout')
def logout_by_user():
    logout_user()
    return redirect('/login')
@login.user_loader
def get_user(id):
    return dao.get_user_by_id(id)
@app.route('/cart')
def cart():
    # session['cart'] = {
    #     "1": {
    #         "id": "1",
    #         "name": "Iphone 15",
    #         "price": 100,
    #         "quantity": 3
    #     },
    #     "2": {
    #         "id": "2",
    #         "name": "SamSung Galaxy",
    #         "price": 150,
    #         "quantity": 1
    #     }
    # }
    return render_template('cart.html')

@app.route('/api/carts', methods=['POST'])
def add_to_cart():
    cart=session.get('cart')
    if not cart:
        cart={}
    id=str(request.json.get('id'))
    if id in cart:
        cart[id]["quantity"]=cart[id]["quantity"]+1
    else:
        cart[id]={
            "id": id,
            "name": request.json.get('name'),
            "price": request.json.get('price'),
            "quantity": 1
        }
    session['cart'] = cart
    print(session['cart'])
    return jsonify({
        "total_quantity": 3
    })
if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
