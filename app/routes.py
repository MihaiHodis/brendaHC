from flask import render_template, jsonify, current_app as app, request, redirect

@app.route('/')
def home():
    connection = app.get_db_connection()
    cursor = connection.cursor()

    try:
        # Execută interogarea SQL pentru a obține toate produsele
        cursor.execute('SELECT id, nume, pret, imagine FROM produse')
        produse = cursor.fetchall()

        # Creăm un dicționar pentru a stoca produsele și recenziile asociate
        produse_recenzii = []

        for produs in produse:
            # Pentru fiecare produs, obținem recenziile sale
            cursor.execute('SELECT evaluare, comentariu, utilizator FROM recenzii WHERE produs_id = %s', (produs[0],))
            recenzii = cursor.fetchall()
            print(recenzii)            
            # Adăugăm produsul și recenziile sale într-un dicționar
            produse_recenzii.append({
                'id': produs[0],
                'nume': produs[1],
                'pret': produs[2],
                'imagine': produs[3],
                'recenzii': recenzii
            })

    except Exception as e:
        print(f"Database error: {e}")
        produse_recenzii = []
    finally:
        cursor.close()
        connection.close()

    # Trimite produsele și recenziile către template
    return render_template('index.html', produse=produse_recenzii)


@app.route('/recenzie', methods=['POST'])
def adauga_recenzie():
    produs_id = request.form['produs_id']
    evaluare = int(request.form['evaluare'])
    comentariu = request.form['comentariu']
    utilizator = request.form['utilizator'] if request.form['utilizator'] else 'Anonim'

    connection = app.get_db_connection()
    cursor = connection.cursor()

    # Inserăm recenzia în baza de date
    cursor.execute("""
        INSERT INTO recenzii (produs_id, evaluare, comentariu, utilizator)
        VALUES (%s, %s, %s, %s)
    """, (produs_id, evaluare, comentariu, utilizator))

    connection.commit()
    cursor.close()
    connection.close()

    # Redirecționăm înapoi la pagina principală
    return redirect('/')




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
