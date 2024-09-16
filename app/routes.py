from flask import render_template, jsonify, current_app as app

@app.route('/')
def home():
    connection = app.get_db_connection()
    cursor = connection.cursor()

    # Execută interogarea SQL pentru a obține produsele
    try:
        cursor.execute('SELECT nume, pret, imagine FROM produse')
        produse = cursor.fetchall()

        # Convertim fiecare tuple într-un dicționar pentru a facilita accesul în template
        produse_list = [{'nume': row[0], 'pret': row[1], 'imagine': row[2]} for row in produse]

    except Exception as e:
        print(f"Database error: {e}")
        produse_list = []
    finally:
        cursor.close()
        connection.close()

    # Trimite lista de produse către template
    return render_template('index.html', produse=produse_list)



@app.route('/api/produse', methods=['GET'])
def get_produse():
    connection = app.get_db_connection()  # Accesăm funcția prin `current_app`
    cursor = connection.cursor()

    cursor.execute('SELECT id, nume FROM produse')
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    produse = [{'id': row[0], 'nume': row[1]} for row in rows]
    return jsonify(produse)
