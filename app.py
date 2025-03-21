from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "123456"

# Ruta principal (Home)
@app.route('/')
def home():
    return render_template('home.html')




# Ruta para registro de restaurantes

@app.route('/registro_restaurantes', methods=['GET', 'POST'])
def registro_restaurantes():
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        telefono = request.form['telefono']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        direccion = request.form['address']
        capacidad = request.form['capacity']

        if password == confirm_password:
            hashed_password = generate_password_hash(password)

            try:
                connection = db.get_connection()
                with connection.cursor() as cursor:
                    sql = "INSERT INTO restaurant (name, email, password, phone_number, address, capacity) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (nombre, email, hashed_password, telefono, direccion, capacidad))
                    connection.commit()
                connection.close()
                return redirect(url_for('login_restaurantes'))
            except Exception as e:
                return f"Ha ocurrido un error en la base de datos: {e}"
        else:
            return "Las contraseñas no coinciden"
    return render_template('registro_restaurantes.html')



# Ruta para login de restaurantes

@app.route('/login_restaurantes', methods=['GET', 'POST'])
def login_restaurantes():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
           connection = db.get_connection()
           cursor = connection.cursor()

           with connection.cursor() as cursor:
                sql = "SELECT * FROM restaurant WHERE email=%s"
                cursor.execute(sql, (email,))
                restaurant = cursor.fetchone()
                connection.close()

                if restaurant and check_password_hash(restaurant['password'], password):
                    session['restaurant_id'] = restaurant['restaurant_id']
                    session['restaurant_name'] = restaurant['name']
                    return redirect(url_for('home_restaurantes'))
                else:
                    return redirect(url_for('login_restaurantes', mensaje="Correo o contraseña inválidos"))
        except Exception as e:
            return f"Ha ocurrido un error en la base de datos: {e}"
    return render_template('login_restaurantes.html')



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
                connection = db.get_connection()
                with connection.cursor() as cursor:
                    sql = "INSERT INTO customer (name, email, password, phone_number) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (nombre, email, hashed_password, telefono))
                    connection.commit()
                connection.close()
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
            connection = db.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM customer WHERE email=%s"
                cursor.execute(sql, (email,))
                customer = cursor.fetchone()
                connection.close()

            if customer and check_password_hash(customer['password'], password):
                session['customer_id'] = customer['customer_id']
                session['customer_name'] = customer['name']
                return redirect(url_for('home_clientes'))
            else:
                return render_template('login_clientes.html', mensaje="Usuario o contraseña inválidos")
        except Exception as e:
            return f"Ha ocurrido un error en la base de datos: {e}"
    return render_template('login_clientes.html')


# Ruta home_restaurantes

@app.route('/home_restaurantes')
def home_restaurantes():
    if 'restaurant_id' not in session:
        return redirect(url_for('login_restaurantes'))  # Redirige al login si no está autenticado
    
    restaurant_id = session['restaurant_id']
    connection = db.get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM restaurant WHERE restaurant_id = %s", (restaurant_id,))
        restaurant = cursor.fetchone()

    connection.close()
    return render_template('home_restaurantes.html', restaurant=restaurant)




# Ruta para ver reservas restaurante

@app.route('/reservas_restaurante')
def reservas_restaurante():
    if 'restaurant_id' not in session:
        return redirect(url_for('login_restaurantes'))  # Redirige al login si no está autenticado

    restaurant_id = session['restaurant_id']
    connection = db.get_connection()
    with connection.cursor() as cursor:
        query = """
        SELECT reserve.reserve_id, customer.name, reserve.number_of_people, reserve.reserve_time, time_slot.start_time, reserve.estatus
        FROM reserve
        JOIN customer ON reserve.customer_id = customer.customer_id
        JOIN time_slot ON reserve.time_slot_id = time_slot.time_slot_id
        WHERE reserve.restaurant_id = %s
        ORDER BY reserve.reserve_id DESC
        """
        cursor.execute(query, (restaurant_id,))
        reservas = cursor.fetchall()

    connection.close()
    
    # Si no hay reservas, pasamos una variable adicional al template para mostrar el mensaje
    
    if not reservas:
        reservas_vacias = True
    else:
        reservas_vacias = False

    return render_template('reservas_restaurante.html', reservas=reservas, reservas_vacias=reservas_vacias)

# Aceptar reservas

@app.route('/aceptar_reserva/<int:reserva_id>', methods=['POST'])
def aceptar_reserva(reserva_id):
    if 'restaurant_id' not in session:
        return redirect(url_for('login_restaurantes'))  # Verifica si el restaurante está autenticado

    restaurant_id = session['restaurant_id']
    connection = db.get_connection()
    with connection.cursor() as cursor:
        
        # Actualiza el estado de la reserva a 'aceptada'
        
        query = """
        UPDATE reserve
        SET estatus = 'aceptada'
        WHERE reserve_id = %s AND restaurant_id = %s
        """
        cursor.execute(query, (reserva_id, restaurant_id))
        connection.commit()

    connection.close()
    flash('Reserva aceptada exitosamente.', 'success')
    return redirect(url_for('reservas_restaurante'))

# Rechazar reservas

@app.route('/rechazar_reserva/<int:reserva_id>', methods=['POST'])
def rechazar_reserva(reserva_id):
    if 'restaurant_id' not in session:
        return redirect(url_for('login_restaurantes'))  # Verifica si el restaurante está autenticado

    restaurant_id = session['restaurant_id']
    connection = db.get_connection()
    with connection.cursor() as cursor:
        
        # Actualiza el estado de la reserva a 'rechazada'
        
        query = """
        UPDATE reserve
        SET estatus = 'rechazada'
        WHERE reserve_id = %s AND restaurant_id = %s
        """
        cursor.execute(query, (reserva_id, restaurant_id))
        connection.commit()

    connection.close()
    flash('Reserva rechazada exitosamente.', 'danger')
    return redirect(url_for('reservas_restaurante'))
    
# Ruta para editar restaurante
 
@app.route('/editar_restaurante', methods=['GET', 'POST'])
def editar_restaurante():
    if 'restaurant_id' not in session:
        return redirect(url_for('login_restaurantes'))  # Redirige al login si no está autenticado

    restaurant_id = session['restaurant_id']
    connection = db.get_connection()

    if request.method == 'POST':
        if 'name' in request.form:  # Esto se aplica solo al formulario de editar el restaurante
            name = request.form['name']
            web = request.form['web']
            address = request.form['address']
            capacity = request.form['capacity']
            phone_number = request.form['phone_number']
            type = request.form['type']
            description = request.form['description']
            speciality = request.form['speciality']
            
            # Actualizar los datos del restaurante
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE restaurant 
                    SET name = %s, web= %s, address = %s, capacity = %s, phone_number = %s, type=%s, description=%s, speciality=%s 
                    WHERE restaurant_id = %s
                """, (name, web, address, capacity, phone_number, type, description, speciality, restaurant_id))
            connection.commit()
            flash('Restaurante actualizado exitosamente', 'success')
            
        # Si el formulario de franjas horarias es el que fue enviado
        
        elif 'start_time' in request.form and 'end_time' in request.form:
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO time_slot (restaurant_id, start_time, end_time)
                    VALUES (%s, %s, %s)
                """, (restaurant_id, start_time, end_time))
            
            connection.commit()
            flash('Franja horaria agregada exitosamente', 'success')
        
        
        connection.close()
        
        return redirect(url_for('editar_restaurante'))

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM restaurant WHERE restaurant_id = %s", (restaurant_id,))
        restaurant = cursor.fetchone()

        # Obtener las franjas horarias actuales del restaurante
        
        cursor.execute("SELECT * FROM time_slot WHERE restaurant_id = %s", (restaurant_id,))
        time_slots = cursor.fetchall()

    connection.close()
    return render_template('editar_restaurantes.html', restaurant=restaurant, time_slots=time_slots)

# Ruta para eliminar una franja horaria

@app.route('/eliminar_franja', methods=['POST'])
def eliminar_franja():
    if 'restaurant_id' not in session:
        return redirect(url_for('login_restaurantes'))  # Redirige al login si no está autenticado

    restaurant_id = session['restaurant_id']
    time_slot_id = request.form['time_slot_id']  # Obtén el ID de la franja horaria desde el formulario

    connection = db.get_connection()

    try:
        with connection.cursor() as cursor:
            
            # Eliminar la franja horaria de la base de datos
            
            cursor.execute("DELETE FROM time_slot WHERE time_slot_id = %s AND restaurant_id = %s", (time_slot_id, restaurant_id))
            connection.commit()
            flash('Franja horaria eliminada exitosamente', 'success')
    except Exception as e:
        connection.rollback()  # Si hay un error, hacer rollback
        flash('Error al eliminar la franja horaria', 'danger')
    
    connection.close()

    return redirect(url_for('editar_restaurante'))  # Redirige de nuevo a la página de edición del restaurante

# Ruta para eliminar Restaurante

@app.route('/eliminar_restaurante', methods=['POST'])
def eliminar_restaurante():
    if 'restaurant_id' not in session:
        return redirect(url_for('login_restaurantes'))  # Redirige al login si no está autenticado

    restaurant_id = session['restaurant_id']
    connection = db.get_connection()

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM restaurant WHERE restaurant_id = %s", (restaurant_id,))
        connection.commit()

    connection.close()
    session.pop('restaurant_id', None)  # Elimina la sesión del restaurante
    flash('Restaurante eliminado exitosamente', 'danger')
    return redirect(url_for('login_restaurantes'))  # Redirige a la página de login

# Ruta para home_clientes

@app.route('/home_clientes')
def home_clientes():
    if 'customer_id' not in session:
        return redirect(url_for('login_clientes'))  # Redirige al login si no está autenticado
    
    customer_id = session['customer_id']
    connection = db.get_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()

    connection.close()
    return render_template('home_clientes.html', customer=customer)

# Ruta para editar perfil
 
@app.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'customer_id' not in session:
        flash("Debes iniciar sesión para editar tu perfil.", "warning")
        return redirect('/login_clientes')

    customer_id = session['customer_id']
    connection = db.get_connection()
    cursor=connection.cursor()
    

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']

        try:
            # Verificar si se ingresó una nueva contraseña
            if password:
                hashed_password = generate_password_hash(password)
                cursor.execute(
                    "UPDATE customer SET name=%s, email=%s, phone_number=%s, password=%s WHERE customer_id=%s",
                    (name, email, phone_number, hashed_password, customer_id)
                )
            else:
                cursor.execute(
                    "UPDATE customer SET name=%s, email=%s, phone_number=%s WHERE customer_id=%s",
                    (name, email, phone_number, customer_id)
                )

            connection.commit()
            flash("Perfil actualizado con éxito.", "success")
            return redirect('/home_clientes')

        except pymysql.MySQLError as e:
            db.get_connection.rollback()
            flash(f"Error al actualizar el perfil: {str(e)}", "danger")

    # Obtener datos actuales del usuario
    cursor.execute("SELECT name, email, phone_number FROM customer WHERE customer_id=%s", (customer_id,))
    customer = cursor.fetchone()
    
    return render_template('editar_perfil.html', customer=customer)

# Ruta para mis reservas

@app.route('/mis_reservas')
def mis_reservas():
    if 'customer_id' not in session:
        flash("Debes iniciar sesión para ver tus reservas.", "warning")
        return redirect('/login_clientes')

    customer_id = session['customer_id']
    
    try:
        connection = db.get_connection()
        cursor = connection.cursor()

        # Consultar las reservas del usuario
        cursor.execute("""
            SELECT r.reserve_id, r.reserve_time, r.number_of_people, r.estatus, 
                   res.name AS restaurant_name, t.start_time, t.end_time
            FROM reserve r
            JOIN restaurant res ON r.restaurant_id = res.restaurant_id
            JOIN time_slot t ON r.time_slot_id = t.time_slot_id
            WHERE r.customer_id = %s
            ORDER BY r.reserve_id DESC
        """, (customer_id,))
        
        reservas = cursor.fetchall()

    except Exception as e:
        flash(f"Error al obtener reservas: {str(e)}", "danger")
        reservas = []
    
    finally:
        cursor.close()
        connection.close()

    return render_template('mis_reservas.html', reservas=reservas)

# Ruta para cancelar una reserva

@app.route('/cancelar_reserva/<int:reserve_id>', methods=['POST'])
def cancelar_reserva(reserve_id):
    if 'customer_id' not in session:
        return redirect(url_for('login_clientes'))  # Solo redirige si no hay sesión

    try:
        connection = db.get_connection()
        with connection.cursor() as cursor:
            # Cambiar el estado en lugar de eliminar
            sql = "UPDATE reserve SET estatus = 'cancelada' WHERE reserve_id = %s AND customer_id = %s"
            cursor.execute(sql, (reserve_id, session['customer_id']))
        connection.commit()
        flash("Reserva cancelada con éxito.", "success")
    except Exception as e:
        flash(f"Error al cancelar la reserva: {e}", "danger")
    finally:
        connection.close()

    return redirect(url_for('mis_reservas'))  # Asegúrate de que 'mis_reservas' está definida


# Ruta para eliminar Perfil

@app.route('/eliminar_perfil', methods=['POST'])
def eliminar_perfil():
    if 'customer_id' not in session:
        return redirect(url_for('login_clientes'))  # Redirige al login si no está autenticado

    customer_id = session['customer_id']
    connection = db.get_connection()

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM customer WHERE customer_id = %s", (customer_id,))
        connection.commit()

    connection.close()
    session.pop('customer_id', None)  # Elimina la sesión del restaurante
    flash('Perfil eliminado exitosamente', 'danger')
    return redirect(url_for('login_clientes'))  # Redirige a la página de login

# Ruta para logout
@app.route('/logout')
def logout():
    session.clear()
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)





