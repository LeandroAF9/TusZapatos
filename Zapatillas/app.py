from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import openai
import config
import os

app = Flask(__name__)
app.config.from_object(config)

# Inicialización de MySQL
mysql = MySQL(app)

openai.api_key = 'tu-api-key'  # Reemplaza con tu clave de API de OpenAI

@app.route('/register_admin', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        mysql.connection.commit()
        cursor.close()

        flash('¡Registro exitoso! Por favor, inicia sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')


####################################################
#############  FUNCION LOGIN  ######################
####################################################
                    ########
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', [username])
        user = cursor.fetchone()
        cursor.close()

        if user:
            if check_password_hash(user[2], password):
                session['loggedin'] = True
                session['username'] = user[1]
                session['user_id'] = user[0]
                session['is_admin'] = bool(int(user[3]))  # Asegúrate de que is_admin sea un booleano
                print(f"Session data: {session}")  # Imprime los datos de la sesión para depuración
                return redirect(url_for('dashboard'))
            else:
                flash('Contraseña incorrecta.', 'danger')
        else:
            flash('Usuario no encontrado.', 'danger')

    return render_template('login.html')




@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'loggedin' in session and session.get('is_admin', False):
        # Lógica para mostrar el dashboard
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT ID_Categoria, Nombre FROM categorias')
        categorias = cursor.fetchall()
        cursor.execute('SELECT ID_Marca, Nombre FROM marcas')
        marcas = cursor.fetchall()
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        cursor.close()

        if request.method == 'POST':
            # Lógica para agregar un producto
            nombre = request.form['nombre']
            descripcion = request.form['descripcion']
            precio = request.form['precio']
            stock = request.form['stock']
            id_categoria = request.form['ID_Categoria']
            id_marca = request.form['id_marca']
            imagen = request.form['imagen']

            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO productos (nombre, descripcion, precio, stock, ID_Categoria, id_marca, imagen) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                           (nombre, descripcion, precio, stock, id_categoria, id_marca, imagen))
            mysql.connection.commit()
            cursor.close()

            flash('Producto agregado exitosamente.', 'success')
            return redirect(url_for('dashboard'))

        return render_template('dashboard.html', categorias=categorias, marcas=marcas, productos=productos)
    else:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('login'))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'loggedin' in session:
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            user_id = session['user_id']

            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO Productos (name, description, user_id) VALUES (%s, %s, %s)',
                           (name, description, user_id))
            mysql.connection.commit()
            cursor.close()

            flash('Item creado exitosamente.', 'success')
            return redirect(url_for('dashboard'))

        return render_template('create.html')
    else:
        flash('Por favor, inicia sesión primero.', 'warning')
        return redirect(url_for('login'))

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total_price = sum(item['product_price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product = request.get_json()
    cart = session.get('cart', [])
    
    for item in cart:
        if item['product_id'] == product['product_id']:
            item['quantity'] += product.get('quantity', 1)
            break
    else:
        cart.append({
            'product_id': product['product_id'],
            'product_name': product['product_name'],
            'product_price': product['product_price'],
            'quantity': product.get('quantity', 1)
        })
    
    session['cart'] = cart
    return jsonify({'success': True})

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['input']
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return jsonify({"response": response.choices[0].text.strip()})

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/zapatos/<categoria>')
def zapatos(categoria):
    return render_template(f'zapatos{categoria.capitalize()}.html')

@app.route('/registro')
def rg():
    return render_template('registro.html')

@app.route('/carrito')
def cr():
    return render_template('carrito.html')

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/zapatoshombre')
def zapatos_hombre():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM productos WHERE ID_Categoria = 2')  
    productos = cursor.fetchall()
    cursor.close()
    return render_template('zapatoshombre.html', productos=productos)

@app.route('/zapatosmujer')
def zapatos_mujer():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM productos WHERE ID_Categoria = 1')  
    productos = cursor.fetchall()
    cursor.close()
    return render_template('zapatosmujer.html', productos=productos)

@app.route('/zapatosniño')
def zapatos_niño():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM productos WHERE id_categoria = 3') 
    productos = cursor.fetchall()
    cursor.close()
    return render_template('zapatosniño.html', productos=productos)

@app.route('/zapatosniña')
def zapatos_niña():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM productos WHERE id_categoria = 4')
    productos = cursor.fetchall()
    cursor.close()
    return render_template('zapatosniña.html', productos=productos)

@app.route('/admin_only')
def admin_only():
    if 'is_admin' not in session or not session['is_admin']:
        flash('No tienes permiso para acceder a esta página.')
        return redirect(url_for('login'))
    return render_template('admin_only.html')

if __name__ == '__main__':
    app.run(debug=True)
