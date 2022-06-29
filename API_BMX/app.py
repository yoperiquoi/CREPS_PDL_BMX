from mysql.connector import connect, Error
import os
from flask import request, Flask, make_response, jsonify
from flask_cors import CORS

import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'records'
# Define max content higher in order to import csv file of records
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Activate CORS
CORS(app)

# Extensions allowed for file upload
ALLOWED_EXTENSIONS = {'csv'}

# Databases parameters, change according to the configuration
db = connect(
    host="localhost",
    user="user",
    password="password",
    database="bmx"
)


# Confirm the validity of uploaded file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Add several row at once
def add_many_row(tables_query, param):
    connection = db
    cursor = connection.cursor(buffered=True)
    cursor.executemany(tables_query, param)
    connection.commit()
    return str(cursor.lastrowid)


# Read a csv file and at it according to enregistrement schema
def add_enregistre_fichier(filename):
    df = pd.read_csv(app.config['UPLOAD_FOLDER']+ "/" + filename, sep=',')

    fill = list(df.itertuples(index=False, name=None))

    tables_query = "INSERT INTO T_ENREGISTREMENT (K_CAPTEUR,F_LAT, F_LONG, F_GYRX, F_GYRY, F_GYRZ, " \
                   "F_ACCX, F_ACCY,F_ACCZ, F_MAGX, F_MAGY, F_MAGZ, F_TIME, K_COURSE) " \
                   "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    i = add_many_row(tables_query, fill)
    return i


# Route for adding several enregistrements at once
@app.route('/file-upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        try:
            i = add_enregistre_fichier(filename)
        except Error as e:
            return make_response(jsonify('Error in DB :' + e.msg), 200)
        resp = jsonify({'message': 'File successfully uploaded and added records : ' + i})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are csv'})
        resp.status_code = 400
        return resp


@app.route('/')
def index():
    return "Nothing here"


# Show pistes
@app.route('/piste', methods=['GET'])
def get_pistes():
    try:
        return get_full_table("T_PISTE", convert_to_json_piste)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


# Show enregistrements
@app.route('/enregistrement', methods=['GET'])
def get_enregistrements():
    try:
        return get_full_table("T_ENREGISTREMENT", convert_to_json_enregistrement)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


# Show courses
@app.route('/course', methods=['GET'])
def get_courses():
    try:
        return get_full_table("T_COURSE", convert_to_json_course)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


# Show capteurs
@app.route('/capteur', methods=['GET'])
def get_capteurs():
    try:
        return get_full_table("T_CAPTEUR", convert_to_json_capteur)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


# Generic method to show a full table
def get_full_table(table_name, convert_json):
    connection = db
    table_query = "SELECT * FROM " + table_name + ";"
    data = {}
    data["res"] = []
    cursor = connection.cursor(buffered=True)
    cursor.execute(table_query)

    for row in cursor:
        data["res"].append(convert_json(row))

    return make_response(jsonify(data), 200)


# Show a piste by id
@app.route('/piste/<id>', methods=['GET'])
def get_piste(id):
    try:
        return get_from_id("T_PISTE", id, convert_to_json_piste)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


# Show a course by id
@app.route('/course/<id>', methods=['GET'])
def get_course(id):
    try:
        get_from_id("T_COURSE", id, convert_to_json_piste)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


# Show a capteur by id
@app.route('/capteur/<id>', methods=['GET'])
def get_capteur(id):
    try:
        return get_from_id("T_CAPTEUR", id, convert_to_json_capteur)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


# Show a enregistrement by id
@app.route('/enregistrement/<id>', methods=['GET'])
def get_enregistrement(id):
    try:
        return get_from_id("T_ENREGISTREMENT", id, convert_to_json_enregistrement)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


# Generic method to get a row from an id
def get_from_id(table_name, id, convert_to_json):
    connection = db
    fill = (id,)
    table_query = "SELECT * FROM " + table_name + " WHERE K_ID = %s;"
    data = {}
    data["res"] = []
    cursor = connection.cursor(buffered=True)
    cursor.execute(table_query, fill)

    for row in cursor:
        data["res"].append(convert_to_json(row))

    return make_response(jsonify(data), 200)


# Add a piste
@app.route('/piste', methods=['POST'])
def add_piste():
    data = request.get_json()
    arrivee1_lat, arrivee1_lon, arrivee2_lat, arrivee2_lon, depart1_lat, depart1_lon, depart2_lat, depart2_lon, nom \
        = get_data_from_json_piste(data)
    fill = (nom, depart1_lat, depart1_lon, depart2_lat, depart2_lon,
            arrivee1_lat, arrivee1_lon, arrivee2_lat, arrivee2_lon)
    tables_query = "INSERT INTO T_PISTE (K_NOM, F_DEPART1_LATITUDE, F_DEPART1_LONGITUDE, F_DEPART2_LATITUDE, " \
                   "F_DEPART2_LONGITUDE, F_ARRIVEE1_LATITUDE, F_ARRIVEE1_LONGITUDE, " \
                   "F_ARRIVEE2_LATITUDE, F_ARRIVEE2_LONGITUDE) " \
                   "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    try:
        return add_row(tables_query, fill)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


def get_data_from_json_capteur(data):
    nom = data.get('F_NOM', 'DEFAUT')
    type = data.get('F_TYPE', '0')
    return nom, type


# Add a capteur
@app.route('/capteur', methods=['POST'])
def add_capteur():
    data = request.get_json()
    nom, type = get_data_from_json_capteur(data)
    fill = (nom, type)
    tables_query = "INSERT INTO T_CAPTEUR (F_NOM, F_TYPE) " \
                   "VALUES(%s, %s);"
    try:
        return add_row(tables_query, fill)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


def get_data_from_json_course(data):
    debut = data.get('F_DEBUT', '0')
    fin = data.get('F_FIN', '0')
    course = data.get('K_PISTE', '0')
    return debut, fin, course


#Add a course
@app.route('/course', methods=['POST'])
def add_course():
    data = request.get_json()
    debut, fin, piste = get_data_from_json_course(data)
    fill = (debut, fin, piste)
    tables_query = "INSERT INTO T_COURSE (F_DEBUT, F_FIN, K_PISTE) " \
                   "VALUES(%s, %s, %s);"
    try:
        return add_row(tables_query, fill)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


def get_data_from_json_enregistrement(data):
    return pd.DataFrame(data)


# Add a enregistrement
@app.route('/enregistrement', methods=['POST'])
def add_enregistrement():
    data = request.get_json()
    fill = get_data_from_json_enregistrement(data)
    tables_query = "INSERT INTO T_ENREGISTREMENT (K_COURSE, K_CAPTEUR,F_LAT, F_LONG, F_GYRX, F_GYRY, F_GYRZ, " \
                   "F_ACCX, F_ACCY,F_ACCZ, F_MAGX, F_MAGY,F_MAGZ) " \
                   "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    try:
        for index, row in fill.iterrows():
            i = add_row(tables_query, tuple(row))
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)

    return i


def add_row(tables_query, data):
    connection = db
    cursor = connection.cursor(buffered=True)
    cursor.execute(tables_query, data)
    connection.commit()
    return str(cursor.lastrowid)


# Delete a piste by id
@app.route('/piste/<id>', methods=['DELETE'])
def delete_piste(id):
    try:
        return delete_row("T_PISTE", id)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


# Delete a capteur by id
@app.route('/capteur/<id>', methods=['DELETE'])
def delete_capteur(id):
    try:
        return delete_row("T_CAPTEUR", id)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


# Delete a course by id
@app.route('/course/<id>', methods=['DELETE'])
def delete_course(id):
    try:
        return delete_row("T_COURSE", id)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


# Delete a enregistrement by id
@app.route('/enregistrement/<id>', methods=['DELETE'])
def delete_enregistrement(id):
    try:
        return delete_row("T_ENREGISTREMENT", id)
    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)


# Generic method to remove a row from a table
def delete_row(table_name, id):
    connection = db
    fill = (str(id),)
    tables_query = "DELETE FROM " + table_name + " WHERE K_ID = %s;"

    cursor = connection.cursor(prepared=True)
    cursor.execute(tables_query, fill)
    connection.commit()

    return "1"


# Update a piste by id
@app.route('/piste/<id>', methods=['PUT'])
def update_piste(id):
    data = request.get_json()
    try:
        delete_row("T_PISTE", id)

        arrivee1_lat, arrivee1_lon, arrivee2_lat, arrivee2_lon, depart1_lat, depart1_lon, depart2_lat, depart2_lon, nom \
            = get_data_from_json_piste(data)

        fill = (id, nom, depart1_lat, depart1_lon, depart2_lat, depart2_lon,
                arrivee1_lat, arrivee1_lon, arrivee2_lat, arrivee2_lon)

        tables_insert = "INSERT INTO T_PISTE VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        add_row(tables_insert, fill)

    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)

    return "1"


# Update a capteur by id
@app.route('/capteur/<id>', methods=['PUT'])
def update_capteur(id):
    data = request.get_json()
    try:
        delete_row("T_CAPTEUR", id)

        nom, type = get_data_from_json_capteur(data)

        fill = (id, nom, type)

        tables_insert = "INSERT INTO T_CAPTEUR VALUES(%s, %s, %s);"

        add_row(tables_insert, fill)

    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)

    return "1"


# Update a course by id
@app.route('/course/<id>', methods=['PUT'])
def update_course(id):
    data = request.get_json()
    try:
        delete_row("T_COURSE", id)

        debut, fin, piste = get_data_from_json_course(data)

        fill = (id, debut, fin, piste)

        tables_insert = "INSERT INTO T_COURSE VALUES(%s,%s, %s, %s);"

        add_row(tables_insert, fill)

    except Error as e:
        return 'Error in DB :' + e.msg

    return "1"


# Update a enregistrement by id
@app.route('/enregistrement/<id>', methods=['PUT'])
def update_enregistrement(id):
    data = request.get_json()

    try:
        delete_row("T_ENREGISTREMENT", id)

        table = get_data_from_json_enregistrement(data)

        tables_insert = "INSERT INTO T_ENREGISTREMENT (K_ID, K_COURSE, K_CAPTEUR,F_LAT, F_LONG, F_GYRX, F_GYRY, F_GYRZ, " \
                        "F_ACCX, F_ACCY,F_ACCZ, F_MAGX, F_MAGY,F_MAGZ) " \
                        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        for index, row in table.iterrows():
            if row['K_ID'] == id:
                add_row(tables_insert, tuple(row))

    except Error as e:
        return make_response(jsonify('Error in DB :' + e.msg), 200)

    return "1"


def get_data_from_json_piste(data):
    nom = data.get('K_NOM', 'DEFAUT')
    depart1_lat = data.get('F_DEPART1_LATITUDE', '0')
    depart1_lon = data.get('F_DEPART1_LONGITUDE', '0')
    depart2_lat = data.get('F_DEPART2_LATITUDE', '0')
    depart2_lon = data.get('F_DEPART2_LONGITUDE', '0')
    arrivee1_lat = data.get('F_ARRIVEE1_LATITUDE', '0')
    arrivee1_lon = data.get('F_ARRIVEE1_LONGITUDE', '0')
    arrivee2_lat = data.get('F_ARRIVEE2_LATITUDE', '0')
    arrivee2_lon = data.get('F_ARRIVEE2_LONGITUDE', '0')
    return arrivee1_lat, arrivee1_lon, arrivee2_lat, arrivee2_lon, depart1_lat, depart1_lon \
        , depart2_lat, depart2_lon, nom


def convert_to_json_piste(piste):
    row = {'K_ID': piste[0], 'K_NOM': piste[1], 'F_DEPART1_LATITUDE': piste[2], 'F_DEPART1_LONGITUDE': piste[3],
           'F_DEPART2_LATITUDE': piste[4], 'F_DEPART2_LONGITUDE': piste[5], 'F_ARRIVEE1_LATITUDE': piste[6],
           'F_ARRIVEE1_LONGITUDE': piste[7], 'F_ARRIVEE2_LATITUDE': piste[8], 'F_ARRIVEE2_LONGITUDE': piste[9]}
    return row


def convert_to_json_capteur(capteur):
    row = {'K_ID': capteur[0], 'F_NOM': capteur[1], 'F_TYPE': capteur[2]}
    return row


def convert_to_json_course(course):
    row = {'K_ID': course[0], 'F_NOM': course[1], 'F_TYPE': course[2]}
    return row


def convert_to_json_enregistrement(enregistrement):
    row = {'K_ID': enregistrement[0], 'K_COURSE': enregistrement[1], 'K_CAPTEUR': enregistrement[2],
           'F_LAT': enregistrement[3], 'F_LONG': enregistrement[4], 'F_GYRX': enregistrement[5],
           'F_GYRY': enregistrement[6], 'F_GYRZ': enregistrement[7], 'F_ACCX': enregistrement[8],
           'F_ACCY': enregistrement[9], 'F_ACCZ': enregistrement[10], 'F_MAGX': enregistrement[11],
           'F_MAGY': enregistrement[12], 'F_MAGZ': enregistrement[13]}
    return row


# Define IP the app will run on (0.0.0.0 is localhost and public IP)
if __name__ == '__main__':
    app.run(host="0.0.0.0")
