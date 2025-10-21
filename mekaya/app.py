from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps
from flask_uploads import UploadSet, configure_uploads, IMAGES
import timeit
import datetime
from flask_mail import Mail, Message
import os
from wtforms.fields.html5 import EmailField

 #-*-coding:utf-8-*-

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/image/product'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# MySQL YAPILANDIRMASI
mysql = MySQL()
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'mekaya'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

 # Bu MySQL sınıfıyla kullanmak için uygulamayı başlat
mysql.init_app(app)


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('index'))
        else:
            return f(*args, *kwargs)

    return wrap


def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('admin_login'))

    return wrap


def not_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return redirect(url_for('admin'))
        else:
            return f(*args, *kwargs)

    return wrap


def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped


def content_based_filtering(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))  # id satırı alındı
    data = cur.fetchone()  # satır bilgisi alındı
    data_cat = data['category']  
    print('Showing result for Product Id: ' + product_id)
    category_matched = cur.execute("SELECT * FROM products WHERE category=%s", (data_cat,))  # tüm  kategoriyi al
    print('Total product matched: ' + str(category_matched))
    cat_product = cur.fetchall()  # tüm satırı al
    cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))  # id seviye bilgisi
    id_level = cur.fetchone()
    recommend_id = []
    cate_level = ['v_shape', 'polo', 'clean_text', 'design', 'leather', 'color', 'formal', 'converse', 'loafer', 'hook',
                  'chain']
    for product_f in cat_product:
        cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_f['id'],))
        f_level = cur.fetchone()
        match_score = 0
        if f_level['product_id'] != int(product_id):
            for cat_level in cate_level:
                if f_level[cat_level] == id_level[cat_level]:
                    match_score += 1
            if match_score == 11:
                recommend_id.append(f_level['product_id'])
    print('Total recommendation found: ' + str(recommend_id))
    if recommend_id:
        cur = mysql.connection.cursor()
        placeholders = ','.join((str(n) for n in recommend_id))
        query = 'SELECT * FROM products WHERE id IN (%s)' % placeholders
        cur.execute(query)
        recommend_list = cur.fetchall()
        return recommend_list, recommend_id, category_matched, product_id
    else:
        return ''


@app.route('/')
def index():
    form = OrderForm(request.form)
    # İmleç oluştur
    cur = mysql.connection.cursor()
    # Mesaj al
    values = 'tshirt'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    tshirt = cur.fetchall()
    values = 'wallet'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    wallet = cur.fetchall()
    values = 'belt'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    belt = cur.fetchall()
    values = 'shoes'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,))
    shoes = cur.fetchall()
    # Bağlantıdan çık
    cur.close()
    return render_template('home.html', tshirt=tshirt, wallet=wallet, belt=belt, shoes=shoes, form=form)


class LoginForm(Form):  # Giriş formu oluştur
    username = StringField('', [validators.length(min=1)],
                           render_kw={'autofocus': True, 'placeholder': 'Kullanıcı Adı'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Şifre'})


# Kullanıcı girişi
@app.route('/login', methods=['GET', 'POST'])
@not_logged_in
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # Kullanıcı Formu al
        username = form.username.data
        # password_candidate = request.form['password']
        password_candidate = form.password.data

        # İmleç oluştur
        cur = mysql.connection.cursor()

        # Kullanıcı adına göre kullanıcı al
        result = cur.execute("SELECT * FROM users WHERE username=%s", [username])

        if result > 0:
            # depolanmış değer al
            data = cur.fetchone()
            password = data['password']
            uid = data['id']
            name = data['name']

            # şifreyi karşılaştır
            if sha256_crypt.verify(password_candidate, password):
                # geçmiş
                session['logged_in'] = True
                session['uid'] = uid
                session['s_name'] = name
                x = '1'
                cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))

                return redirect(url_for('index'))

            else:
                flash('Yanlış şifre girdiniz', 'danger')
                return render_template('login.html', form=form)

        else:
            flash('Kullanıcı adı bulunamadı', 'danger')
            # Bağlantıdan çık
            cur.close()
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/out')
def logout():
    if 'uid' in session:
        # İmleç oluştur
        cur = mysql.connection.cursor()
        uid = session['uid']
        x = '0'
        cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
        session.clear()
        flash('Çıkış yaptınız', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('login'))


class RegisterForm(Form):
    name = StringField('', [validators.length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Ad Soyad'})
    username = StringField('', [validators.length(min=3, max=25)], render_kw={'placeholder': 'Kullanıcı Adı'})
    email = EmailField('', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'E-posta'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Şifre'})
    mobile = StringField('', [validators.length(min=11, max=15)], render_kw={'placeholder': 'Mobil'})


@app.route('/register', methods=['GET', 'POST'])
@not_logged_in
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        mobile = form.mobile.data

        # İmleç oluştur
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password, mobile) VALUES(%s, %s, %s, %s, %s)",
                    (name, email, username, password, mobile))

        # İmleci kaydet
        mysql.connection.commit()

        # Bağlantıdan çık
        cur.close()

        flash('Şimdi kayıt oldunuz ve giriş yapabilirsiniz', 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)


class MessageForm(Form):  # Mesaj formu oluştur
    body = StringField('', [validators.length(min=1)], render_kw={'autofocus': True})



class OrderForm(Form):  # Sipariş formu yarat
    name = StringField('', [validators.length(min=1), validators.DataRequired()],
                       render_kw={'autofocus': True, 'placeholder': 'Ürün İsmi'})
    mobile_num = StringField('', [validators.length(min=1), validators.DataRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'Mobil'})
    quantity = SelectField('', [validators.DataRequired()],
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    order_place = StringField('', [validators.length(min=1), validators.DataRequired()],
                              render_kw={'placeholder': 'Sipariş Yeri'})


@app.route('/tshirt', methods=['GET', 'POST'])
def tshirt():
    form = OrderForm(request.form)
    
    cur = mysql.connection.cursor()
    
    values = 'tshirt'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    
    cur.close()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # İmleç oluştur
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))
        # İmleci kaydet
        mysql.connection.commit()

        # Bağlantıdan çık
        cur.close()

        flash('Sipariş Verildi', 'success')
        return render_template('tshirt.html', tshirt=products, form=form)
    if 'view' in request.args:
        product_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        wrappered = wrappers(content_based_filtering, product_id)
        execution_time = timeit.timeit(wrappered, number=0)
        # print('Execution time: ' + str(execution_time) + ' usec')
        if 'uid' in session:
            uid = session['uid']
            # İmleç oluştur
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM product_view WHERE user_id=%s AND product_id=%s", (uid, product_id))
            result = cur.fetchall()
            if result:
                now = datetime.datetime.now()
                now_time = now.strftime("%y-%m-%d %H:%M:%S")
                cur.execute("UPDATE product_view SET date=%s WHERE user_id=%s AND product_id=%s",
                            (now_time, uid, product_id))
            else:
                cur.execute("INSERT INTO product_view(user_id, product_id) VALUES(%s, %s)", (uid, product_id))
                mysql.connection.commit()
        return render_template('view_product.html', x=x, tshirts=product)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, tshirts=product, form=form)
    return render_template('tshirt.html', tshirt=products, form=form)


@app.route('/wallet', methods=['GET', 'POST'])
def wallet():
    form = OrderForm(request.form)
    # İmleç oluştur
    cur = mysql.connection.cursor()
    # Mesaj al
    values = 'wallet'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Bağlantıdan çık
    cur.close()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']

        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # İmleç oluştur
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))
        # İmleci kaydet
        mysql.connection.commit()
        # Bağlantıdan çık
        cur.close()

        flash('Sipariş Verildi', 'success')
        return render_template('wallet.html', wallet=products, form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        products = curso.fetchall()
        return render_template('view_product.html', x=x, tshirts=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, tshirts=product, form=form)
    return render_template('wallet.html', wallet=products, form=form)


@app.route('/belt', methods=['GET', 'POST'])
def belt():
    form = OrderForm(request.form)
    # İmleç oluştur
    cur = mysql.connection.cursor()
    # Mesaj al
    values = 'belt'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Bağlantıdan çık
    cur.close()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # İmleç oluştur
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))

        # İmleci kaydet
        mysql.connection.commit()

        # Bağlantıdan çık
        cur.close()

        flash('Sipariş Verildi', 'success')
        return render_template('belt.html', belt=products, form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        products = curso.fetchall()
        return render_template('view_product.html', x=x, tshirts=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, tshirts=product, form=form)
    return render_template('belt.html', belt=products, form=form)


@app.route('/shoes', methods=['GET', 'POST'])
def shoes():
    form = OrderForm(request.form)
    # İmleç oluştur
    cur = mysql.connection.cursor()
    # Mesaj al
    values = 'shoes'
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Bağlantıdan çık
    cur.close()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args['order']
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # İmleç oluştur
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))
        # İmleci kaydet
        mysql.connection.commit()
        # Bağlantıdan çık
        cur.close()

        flash('Sipariş Verildi', 'success')
        return render_template('shoes.html', shoes=products, form=form)
    if 'view' in request.args:
        q = request.args['view']
        product_id = q
        x = content_based_filtering(product_id)
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        products = curso.fetchall()
        return render_template('view_product.html', x=x, tshirts=products)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        x = content_based_filtering(product_id)
        return render_template('order_product.html', x=x, tshirts=product, form=form)
    return render_template('shoes.html', shoes=products, form=form)


@app.route('/admin_login', methods=['GET', 'POST'])
@not_admin_logged_in
def admin_login():
    if request.method == 'POST':
        # Kullanıcı formu al
        username = request.form['email']
        password_candidate = request.form['password']

        # İmleç Oluştur
        cur = mysql.connection.cursor()

        # Kullanıcı adına göre kullanıcı al
        result = cur.execute("SELECT * FROM admin WHERE email=%s", [username])

        if result > 0:
            # Depolanmış değer al
            data = cur.fetchone()
            password = data['password']
            uid = data['id']
            name = data['firstName']

            # Şifreyi karşılaştır
            if sha256_crypt.verify(password_candidate, password ):
                # geçti
                session['admin_logged_in'] = True
                session['admin_uid'] = uid
                session['admin_name'] = name

                return redirect(url_for('admin'))

            else:
                flash('Şifre yanlış', 'danger')
                return render_template('pages/login.html')

        else:
            flash('Kullanıcı ismi bulunamadı', 'danger')
            # Bağlantıdan Çık
            cur.close()
            return render_template('pages/login.html')
    return render_template('pages/login.html')


@app.route('/admin_out')
def admin_logout():
    if 'admin_logged_in' in session:
        session.clear()
        return redirect(url_for('admin_login'))
    return redirect(url_for('admin'))


@app.route('/admin')
@is_admin_logged_in
def admin():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    result = curso.fetchall()
    order_rows = curso.execute("SELECT * FROM orders")
    users_rows = curso.execute("SELECT * FROM users")
    return render_template('pages/index.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/orders')
@is_admin_logged_in
def orders():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    order_rows = curso.execute("SELECT * FROM orders")
    result = curso.fetchall()
    users_rows = curso.execute("SELECT * FROM users")
    return render_template('pages/all_orders.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/users')
@is_admin_logged_in
def users():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    order_rows = curso.execute("SELECT * FROM orders")
    users_rows = curso.execute("SELECT * FROM users")
    result = curso.fetchall()
    return render_template('pages/all_users.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/admin_add_product', methods=['POST', 'GET'])
@is_admin_logged_in
def admin_add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form['price']
        description = request.form['description']
        available = request.form['available']
        category = request.form['category']
        item = request.form['item']
        code = request.form['code']
        file = request.files['picture']
        if name and price and description and available and category and item and code and file:
            pic = file.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "_")
            if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                save_photo = photos.save(file, folder=category)
                if save_photo:
                    # İmleç Oluştur
                    curs = mysql.connection.cursor()
                    curs.execute("INSERT INTO products(pName,price,description,available,category,item,pCode,picture)"
                                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                                 (name, price, description, available, category, item, code, picture))
                    mysql.connection.commit()
                    product_id = curs.lastrowid
                    curs.execute("INSERT INTO product_level(product_id)" "VALUES(%s)", [product_id])
                    if category == 'tshirt':
                        level = request.form.getlist('tshirt')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # İmleci Kaydet
                            mysql.connection.commit()
                    elif category == 'wallet':
                        level = request.form.getlist('wallet')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # İmleci Kaydet
                            mysql.connection.commit()
                    elif category == 'belt':
                        level = request.form.getlist('belt')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # İmleci Kaydet
                            mysql.connection.commit()
                    elif category == 'shoes':
                        level = request.form.getlist('shoes')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # İmleci Kaydet
                            mysql.connection.commit()
                    else:
                        flash('Product level not fund', 'danger')
                        return redirect(url_for('admin_add_product'))
                    # Bağlantıdan çık
                    curs.close()

                    flash('Product added successful', 'success')
                    return redirect(url_for('admin_add_product'))
                else:
                    flash('Picture not save', 'danger')
                    return redirect(url_for('admin_add_product'))
            else:
                flash('File not supported', 'danger')
                return redirect(url_for('admin_add_product'))
        else:
            flash('Please fill up all form', 'danger')
            return redirect(url_for('admin_add_product'))
    else:
        return render_template('pages/add_product.html')


@app.route('/edit_product', methods=['POST', 'GET'])
@is_admin_logged_in
def edit_product():
    if 'id' in request.args:
        product_id = request.args['id']
        curso = mysql.connection.cursor()
        res = curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        curso.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))
        product_level = curso.fetchall()
        if res:
            if request.method == 'POST':
                name = request.form.get('name')
                price = request.form['price']
                description = request.form['description']
                available = request.form['available']
                category = request.form['category']
                item = request.form['item']
                code = request.form['code']
                file = request.files['picture']
                # İmleç oluştur
                if name and price and description and available and category and item and code and file:
                    pic = file.filename
                    photo = pic.replace("'", "")
                    picture = photo.replace(" ", "")
                    if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file.filename = picture
                        save_photo = photos.save(file, folder=category)
                        if save_photo:
                            # İmleç oluştur
                            cur = mysql.connection.cursor()
                            exe = curso.execute(
                                "UPDATE products SET pName=%s, price=%s, description=%s, available=%s, category=%s, item=%s, pCode=%s, picture=%s WHERE id=%s",
                                (name, price, description, available, category, item, code, picture, product_id))
                            if exe:
                                if category == 'tshirt':
                                    level = request.form.getlist('tshirt')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # İmleci kaydet
                                        mysql.connection.commit()
                                elif category == 'wallet':
                                    level = request.form.getlist('wallet')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # İmleci kaydet
                                        mysql.connection.commit()
                                elif category == 'belt':
                                    level = request.form.getlist('belt')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # İmleci kaydet
                                        mysql.connection.commit()
                                elif category == 'shoes':
                                    level = request.form.getlist('shoes')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # İmleci kaydet
                                        mysql.connection.commit()
                                else:
                                    flash('Product level not fund', 'danger')
                                    return redirect(url_for('admin_add_product'))
                                flash('Product updated', 'success')
                                return redirect(url_for('edit_product'))
                            else:
                                flash('Data updated', 'success')
                                return redirect(url_for('edit_product'))
                        else:
                            flash('Pic not upload', 'danger')
                            return render_template('pages/edit_product.html', product=product,
                                                   product_level=product_level)
                    else:
                        flash('File not support', 'danger')
                        return render_template('pages/edit_product.html', product=product,
                                               product_level=product_level)
                else:
                    flash('Fill all field', 'danger')
                    return render_template('pages/edit_product.html', product=product,
                                           product_level=product_level)
            else:
                return render_template('pages/edit_product.html', product=product, product_level=product_level)
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    form = OrderForm(request.form)
    if 'q' in request.args:
        q = request.args['q']
        # İmleç oluştur
        cur = mysql.connection.cursor()
        # Mesaj al
        query_string = "SELECT * FROM products WHERE pName LIKE %s ORDER BY id ASC"
        cur.execute(query_string, ('%' + q + '%',))
        products = cur.fetchall()
        # Bağlantıdan çık
        cur.close()
        flash('İçin sonuç gösteriliyor: ' + q, 'success')
        return render_template('search.html', products=products, form=form)
    else:
        flash('Tekrar arayın', 'danger')
        return render_template('search.html')


@app.route('/profile')
@is_logged_in
def profile():
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                curso.execute("SELECT * FROM orders WHERE uid=%s ORDER BY id ASC", (session['uid'],))
                res = curso.fetchall()
                return render_template('profile.html', result=res)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


class UpdateRegisterForm(Form):
    name = StringField('Ad Soyad', [validators.length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Ad Soyad'})
    email = EmailField('E-posta', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)],
                       render_kw={'placeholder': 'E-posta'})
    password = PasswordField('Şifre', [validators.length(min=3)],
                             render_kw={'placeholder': 'Şifre'})
    mobile = StringField('Mobil', [validators.length(min=11, max=15)], render_kw={'placeholder': 'Mobil'})


@app.route('/settings', methods=['POST', 'GET'])
@is_logged_in
def settings():
    form = UpdateRegisterForm(request.form)
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                if request.method == 'POST' and form.validate():
                    name = form.name.data
                    email = form.email.data
                    password = sha256_crypt.encrypt(str(form.password.data))
                    mobile = form.mobile.data

                    # İmleç oluştur
                    cur = mysql.connection.cursor()
                    exe = cur.execute("UPDATE users SET name=%s, email=%s, password=%s, mobile=%s WHERE id=%s",
                                      (name, email, password, mobile, q))
                    if exe:
                        flash('Profil güncellendi', 'success')
                        return render_template('user_settings.html', result=result, form=form)
                    else:
                        flash('Profil güncellenemedi', 'danger')
                return render_template('user_settings.html', result=result, form=form)
            else:
                flash('Yetkisiz!', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Yetkisiz! Lütfen giriş yapın', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
