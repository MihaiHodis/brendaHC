from flask import render_template, jsonify, current_app as app, request, redirect

@app.route('/')
def home():
    connection = app.get_db_connection()
    cursor = connection.cursor()

    try:
        # Execută interogarea SQL pentru a obține toate categoriile de produsele
        cursor.execute('SELECT id, nume, imagine FROM categorii')
        categorii = cursor.fetchall()

        # Cream o lista de dictionare pentru a stoca categoriile
        categorii_list = [{'id': categorie[0], 'nume': categorie[1], 'imagine': categorie[2]} for categorie in categorii]        

    except Exception as e:
        print(f"Database error: {e}")
        categorii_list = []
    finally:
        cursor.close()
        connection.close()

    # Trimite categoriile către template
    return render_template('index.html', categorii=categorii_list)


@app.route('/categorii/<int:categorie_id>')
def afisare_produse(categorie_id):
    connection = app.get_db_connection()
    cursor = connection.cursor()

    try:
        # Fetch all categories for dropdown
        cursor.execute('SELECT id, nume FROM categorii')
        categorii = cursor.fetchall()
        categorii_list = [{'id': cat[0], 'nume': cat[1]} for cat in categorii]

        # Fetch products for the given category
        cursor.execute('SELECT id, nume, imagine FROM produse WHERE categorie_id = %s', (categorie_id,))
        produse = cursor.fetchall()
        produse_list = [{'id': produs[0], 'nume': produs[1], 'imagine': produs[2]} for produs in produse]

        # Find the name of the current category
        categorie_nume = next((cat['nume'] for cat in categorii_list if cat['id'] == categorie_id), "Categorie")

    except Exception as e:
        print(f"Database error: {e}")
        produse_list = []
        categorii_list = []
        categorie_nume = "Categorie"
    finally:
        cursor.close()
        connection.close()

    # Render a new template for the products in a specific category
    return render_template('categorie.html', produse=produse_list, categorii=categorii_list, categorie=categorie_nume)


@app.route('/produse/<int:produs_id>')
def afisare_pagina_produs(produs_id):
    connection = app.get_db_connection()
    cursor = connection.cursor()

    try:
        # Selecteaza produsul de interes din baza de date
        cursor.execute('SELECT id, nume, imagine, pret, descriere FROM produse WHERE id = %s', (produs_id,))
        produs = cursor.fetchone()
        if produs:
            produs_data = {'id': produs[0], 'nume': produs[1], 'imagine': produs[2], 'pret': produs[3], 'descriere': produs[4]}
        else:
            produs_data = None

        if not produs_data:
            return "Produsul nu a fost găsit", 404

    except Exception as e:
        print(f"Database error: {e}")
        return "A intervenit o eroare la baza de date", 500

    finally:
        cursor.close()
        connection.close()

    return render_template('produs.html', produs=produs_data)



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

"""
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
            }) """


