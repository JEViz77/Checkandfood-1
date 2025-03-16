from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "123456"

# Ruta principal (Home)
@app.route('/')
def home():
    return render_template('home.html')


# Ruta para login de restaurantes
@app.route('/restaurantes', methods=['GET'])
def restaurantes():
    return render_template('login_restaurant.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM restaurant WHERE email=%s"
            cursor.execute(sql, (email,))
            restaurant = cursor.fetchone()
            conexion.close()

        if restaurant and check_password_hash(restaurant['password'], password):
            session['restaurant_id'] = restaurant['restaurant_id']
            session['restaurant_name'] = restaurant['name']
            return redirect(url_for('manage_reservations'))
        else:
            return "Credenciales inválidas. Por favor, revisa tu correo y contraseña."
    except Exception as e:
            return f"Ha ocurrido un error en la base de datos: {e}" 
 
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        capacity = int(request.form['capacity'])
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        phone = request.form['phone']
        address = request.form['address']
        
        try:
            conexion = db.get_connection()
            with conexion.cursor() as cursor:
                sql = "INSERT INTO restaurant (name, email, password,address,capacity, phone_number) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, email, hashed_password, address, capacity, phone))
                conexion.commit()
            conexion.close()
            return redirect(url_for('restaurantes'))
        except Exception as e:
            return f"Ha ocurrido un error en la base de datos: {e}"
    return render_template('register_restaurant.html')

    # Ruta para gestionar las reservas y asignar mesas
@app.route('/manage_reservations', methods=['GET', 'POST'])
def manage_reservations():
    if 'restaurant_id' not in session:
        return redirect(url_for('login'))
    
    
    restaurant_id = session['restaurant_id']
    connection = db.get_connection()
    cursor = connection.cursor()

   #accion para cambiar estado a confirmado y rechazado
   
    if request.method == 'POST':
        reserve_id = request.form['reserve_id']
        accion = request.form['action']
        if accion == 'confirm':
            cursor.execute('''UPDATE reserve SET estatus = 'confirmado' WHERE reserve_id = %s;''', (reserve_id,))
            connection.commit()
        elif accion == 'reject':
            cursor.execute('''UPDATE reserve SET estatus = 'rechazado' WHERE reserve_id = %s;''', (reserve_id,))
       
          
            connection.commit()
    # Nombre restaurante
    cursor.execute('''SELECT name FROM restaurant WHERE restaurant_id = %s;''', (restaurant_id,))
    restaurant_name = cursor.fetchone()  
    # Obtener todas las reservas del restaurante
    cursor.execute('''
        SELECT r.reserve_id, r.date, r.dinner, r.estatus, c.name as customer_name,c.phone_number
        FROM reserve r
        JOIN customer c ON r.customer_id = c.customer_id
        WHERE r.restaurant_id = %s ORDER BY r.date;
    ''', (restaurant_id,))
    reservations = cursor.fetchall()
    
    cursor.execute('''
        SELECT capacity FROM restaurant WHERE restaurant_id = %s;
    ''', (restaurant_id,))
    capacity = cursor.fetchone()
    cursor.close()
    connection.close()

    return render_template('manage_reservations.html', reservations=reservations,capacity=capacity,restaurant_name=restaurant_name)

# Ruta para registro de clientes
@app.route('/registro_clientes', methods=['GET', 'POST'])
def registro_clientes():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            hashed_password = generate_password_hash(password)

            try:
                conexion = db.get_connection()
                with conexion.cursor() as cursor:
                    sql = "INSERT INTO customer (name, email, password, phone_number) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (nombre, email, hashed_password, telefono))
                    conexion.commit()
                conexion.close()
                return redirect(url_for('login_clientes'))
            except Exception as e:
                return f"Ha ocurrido un error en la base de datos: {e}"
        else:
            return "Las contraseñas no coinciden"
    return render_template('registro_clientes.html')

# Ruta para login de clientes
@app.route('/login_clientes', methods=['GET', 'POST'])
def login_clientes():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conexion = db.get_connection()
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM customer WHERE email=%s"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()
                conexion.close()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['customer_id']
                session['user_name'] = user['name']
                return redirect(url_for('dashboard'))
            else:
                return render_template('login_clientes.html', mensaje="usuario inválido")
                #return "Credenciales inválidas. Por favor, revisa tu correo y contraseña."
        except Exception as e:
            return f"Ha ocurrido un error en la base de datos: {e}"
    return render_template('login_clientes.html')

    # CLIENTES Ruta para gestionar las reservas 
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
    #if 'restaurant_id' not in session:
        return redirect(url_for('login'))
    
    
    #restaurant_id = session['restaurant_id']
    connection = db.get_connection()
    cursor = connection.cursor()

   #accion para cambiar estado a confirmado y rechazado
   
    if (request.method == 'POST' and ('restaurante' in request.form)):
        id_restaurante = request.form['restaurante'] 
        fecha = request.form['fecha']
        numero_comensales = request.form['comensales']
        cliente = session['user_id']
        #creamos la conexion
        #conexion = db.get_connection()
        try:
            with connection.cursor() as cursor:
                
                #creamos la consulta
                consulta = "INSERT INTO reserve (date, dinner, restaurant_id, customer_id) VALUES (%s, %s, %s, %s)"
                datos = (fecha,numero_comensales,id_restaurante,cliente)
                cursor.execute(consulta,datos)
                resultados = cursor.fetchone()
                connection.commit()

                # Obtener todas las reservas del restaurante
                # cursor.execute('''
                #     SELECT r.reserve_id, r.date, r.dinner, r.estatus, c.name as customer_name,c.phone_number
                #     FROM reserve r
                #     JOIN customer c ON r.customer_id = c.customer_id
                #     WHERE r.restaurant_id = %s;
                # ''', (1,))
                # reservations = cursor.fetchall()
                return redirect(url_for('dashboard'))


                #return render_template('customer_dashboard.html',mensaje="<h1><a href='/'> confirmada </a></h1>")

        except Exception as e:
            print("Ocurrió un error al conectar a la bbdd: ", e)
        finally:    
            connection.close()
            print("Conexión cerrada") 


    if (request.method == 'POST' and request.form['action']):
        reserve_id = request.form['reserve_id']
        accion = request.form['action']
        if accion == 'confirm':
            cursor.execute('''UPDATE reserve SET estatus = 'confirmado' WHERE reserve_id = %s;''', (reserve_id,))
            connection.commit()
        elif accion == 'reject':
            cursor.execute('''UPDATE reserve SET estatus = 'cancelado por cliente' WHERE reserve_id = %s;''', (reserve_id,))
            
            connection.commit()

    # Obtener todas las reservas del restaurante
    ###cursor.execute("SELECT * FROM reserve WHERE customer_id=%s", (session['user_id'],))
    
    # Obtener todas las reservas del restaurante
    #SELECT r.reserve_id, r.date, r.dinner, r.estatus, c.name as restaurant_name FROM reserve r   JOIN restaurant c ON r.restaurant_id = c.restaurant_id        WHERE r.customer_id = 2;
    cursor.execute('''
        SELECT r.reserve_id, r.date, r.dinner, r.estatus, c.name as restaurant_name
        FROM reserve r
        JOIN restaurant c ON r.restaurant_id = c.restaurant_id
        WHERE r.customer_id = %s;
    ''', (session['user_id'],))
    

    reservations = cursor.fetchall()
    
    cursor.execute("SELECT * FROM restaurant")
    restaurantes = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('customer_dashboard.html', restaurantes=restaurantes, reservations=reservations)



 

# Ruta para logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)





