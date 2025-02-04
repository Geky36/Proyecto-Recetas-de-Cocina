from flask import Blueprint, render_template, request, redirect, url_for
from config.database import get_db_connection

router = Blueprint('pacientes', __name__)

# Ruta para listar los pacientes
@router.route('/')
def index():    
    return render_template('index.html')


@router.route('/mostrarPacientes')
def mostrar_pacientes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Paciente')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('listaPacientes.html', Pacientes=data)

# Ruta para agregar un nuevo paciente
@router.route('/agregar', methods=['GET', 'POST'])
def agregar_paciente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion_casa = request.form['direccionCasa']
        direccion_calle = request.form['direccionCalle']
        direccion_ciudad = request.form['direccionCiudad']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Paciente (nombre, apellido, direccionCasa, direccionCalle, direccionCiudad) 
            VALUES (%s, %s, %s, %s, %s)
        ''', (nombre, apellido, direccion_casa, direccion_calle, direccion_ciudad))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('pacientes.index'))
    
    return render_template('agregar_paciente.html')

@router.route('/listaTelefono')
def mostrarTelefonos():
    base = get_db_connection()
    cursor = base.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Telefono')
    data = cursor.fetchall()
    base.close()
    return render_template('listaTelefono.html',Telefono = data)

@router.route('/agregarTelefono', methods=['GET','POST'])
def agregar_telefono():
    if request.method == 'POST':
        numero = request.form['numero']
        idPaciente = int (request.form ['idPaciente'])
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Telefono (numero, idPaciente)
            VALUES (%s,%s)
        ''',(numero,idPaciente))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('pacientes.index'))
    return render_template('registrarTelefono.html')


# Ruta para editar un paciente
@router.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion_casa = request.form['direccionCasa']
        direccion_calle = request.form['direccionCalle']
        direccion_ciudad = request.form['direccionCiudad']
        
        cursor.execute('''
            UPDATE Paciente 
            SET nombre = %s, apellido = %s, direccionCasa = %s, direccionCalle = %s, direccionCiudad = %s
            WHERE idPaciente = %s
        ''', (nombre, apellido, direccion_casa, direccion_calle, direccion_ciudad, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('pacientes.index'))

    cursor.execute('SELECT * FROM Paciente WHERE idPaciente = %s', (id,))
    paciente = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('editarPaciente.html', paciente=paciente)

# Ruta para eliminar un paciente
@router.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_paciente(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Paciente WHERE idPaciente = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('pacientes.index'))


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