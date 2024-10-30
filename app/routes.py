from flask import render_template, jsonify, current_app as app, request, redirect, flash

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

        # Daca produsul nu a fost gasit, afiseaza o eroare
        if not produs:
            return "Produsul cautat nu a fost gasit", 404
        
        # Selecteaza review-ul pentru produsul corespunzator conform id-ului
        cursor.execute('SELECT evaluare, comentariu, utilizator, data FROM recenzii WHERE produs_id = %s', (produs_id,))
        recenzii = cursor.fetchall()

        # Se pregateste un dictionare care va trimite datele cerute catre template
    
        produs_data = {
            'id': produs[0],
            'nume': produs[1],
            'imagine': produs[2],
            'pret': produs[3],
            'descriere': produs[4],
            'recenzii': [{'evaluare': rec[0], 'comentariu': rec[1], 'utilizator': rec[2], 'data': rec[3]} for rec in recenzii]
        }

        # Se face media rating-urile oferite produselor
        if recenzii:
            total_evaluare = sum([rec[0] for rec in recenzii])
            produs_data['rating_mediu'] = round(total_evaluare / len(recenzii), 1)
        else:
            produs_data['rating_mediu'] = None

    except Exception as e:
        print(f"Database error: {e}")
        produs_data = None

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
    return redirect(f'/produse/{produs_id}')


# Ruta backend pentru procesarea cererii de comanda
@app.route('/contact', methods=['POST'])
def contacteaza_admin():
    produs_id = request.form['produs_id']
    nume_utilizator = request.form['nume_utilizator']
    email = request.form['email']
    detalii = request.form['detalii']

    # Conexiunea cu baza de date pentru a salva cererea
    connection = app.get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO cereri_contact (produs_id, nume_utilizator, email, detalii)
            VALUES (%s, %s, %s, %s)
        """, (produs_id, nume_utilizator, email, detalii))
        connection.commit()
    except Exception as e:
        print(f"Eroare la salvarea cererii: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
    
    # Redirectionam utilizatorul inapoi cu un mesaj de confirmare
    flash('Cererea ta a fost trimisa cu succes!')
    return redirect(f'/produse/{produs_id}')