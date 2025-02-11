from flask import Blueprint, render_template, request, redirect, url_for
from config.database import get_db_connection

router = Blueprint('Recetario', __name__)

@router.route('/')
def index():    
    return render_template('index.html')


@router.route('/mostrarRestaurantes')
def mostrar_restaurantes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Restaurante')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('listaRestaurantes.html', restaurantes=data)

# Ruta para agregar un nuevo paciente
@router.route('/agregar', methods=['GET', 'POST'])
def agregar_restaurante():
    if request.method == 'POST':
        horario = request.form['horario']
        nombre = request.form['nombre']
        correo = request.form['correo']
        direccion_calle = request.form['calles']
        direccion_ciudad = request.form['ciudad']
        categoria = request.form['categoria']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Restaurante (horario, nombre, correo, direccion_calle, direccion_ciudad, categoria) 
            VALUES (%s, %s, %s, %s, %s,%s)
        ''', (horario,nombre, correo,direccion_calle, direccion_ciudad,categoria))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('Recetario.mostrar_restaurantes'))
    
    return render_template('agregar_restaurante.html')

@router.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_restaurante(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        horario = request.form['horario']
        nombre = request.form['nombre']
        correo = request.form['correo']
        direccion_calle = request.form['calles']
        direccion_ciudad = request.form['ciudad']
        categoria = request.form['categoria']

        cursor.execute('''
            UPDATE Restaurante 
            SET horario = %s, nombre = %s, correo = %s, direccion_calle = %s, direccion_ciudad = %s, categoria = %s
            WHERE id = %s
        ''', (horario,nombre, correo, direccion_calle, direccion_ciudad, categoria, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('Recetario.mostrar_restaurantes'))

    cursor.execute('SELECT * FROM Restaurante WHERE id = %s', (id,))
    rest = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('editar_restaurante.html', restaurante=rest)

# Ruta para eliminar un paciente
@router.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_restaurante(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Restaurante WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('Recetario.mostrar_restaurantes'))


@router.route('/listaTelefono/<int:id>')
def mostrar_telefonos(id):
    base = get_db_connection()
    cursor = base.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Telefono_Restaurante where id_restaurante =%s',(id,))
    data = cursor.fetchall()
    base.close()
    return render_template('listaTelefono.html',telefonos = data)

@router.route('/agregarTelefono', methods=['GET','POST'])
def agregar_telefono():
    if request.method == 'POST':
        telefono = request.form['telefono']
        id = int (request.form ['id_restaurante'])
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Telefono_Restaurante (telefono, id_restaurante)
            VALUES (%s,%s)
        ''',(telefono,id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('Recetario.mostrar_restaurantes'))
    return render_template('registrarTelefono.html')

@router.route('/historialMedico')
def mostrar_historial():
    base = get_db_connection()
    cursor = base.cursor(dictionary=True)
    cursor.execute('SELECT * FROM HistorialMedico')
    data = cursor.fetchall()
    base.close()
    return render_template('listaHistorial.html',Historial = data)


@router.route('/agregarHitorial', methods=['GET', 'POST'])
def agregar_historial():
    if request.method == 'POST':
        fecha = request.form['fecha']
        diagnostico = request.form['diagnostico']
        observaciones = request.form['observaciones']
        idPaciente = int (request.form['idPaciente'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO HistorialMedico (fecha, diagnostico, observaciones, idPaciente) 
            VALUES (%s, %s, %s, %s)
        ''', (fecha, diagnostico, observaciones, idPaciente))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('pacientes.index'))
    
    return render_template('agregarHistorial.html')