from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite
import datetime

# ------------------
# application Flask
# ------------------

app = Flask(__name__)


# ---------------------------------------
# des fonctions utiles à plusieurs pages
# ---------------------------------------

# renvoie un lien HTML pour retourner à la page index
def retour_index():
    return "<a href='" + url_for("index") + "'>retour à l'index</a><br/><br/>"


def render_page(name):
    return render_template(str(name) + ".html")


# renvoie un formulaire vers la page cible demandant un prénom (avec une valeur par défaut)
def formulaire_prenom(cible, prenom="entrez votre prénom"):
    formulaire = ""
    formulaire += "<form method='post' action='" + url_for(cible) + "'>"
    formulaire += "<input type='text' name='prenom' value='" + prenom + "'>"
    formulaire += "<input type='submit' value='Envoyer'>"
    formulaire += "</form><br/>"

    return formulaire


def formulaire_number(cible, number="entrez votre prénom"):
    formulaire = ""
    formulaire += "<form method='post' action='" + url_for(cible) + "'>"
    formulaire += "<input type='text' name='prenom' value='" + number + "'>"
    formulaire += "<input type='submit' value='Envoyer'>"
    formulaire += "</form><br/>"

    return formulaire


# connecte à la BDD, affecte le mode dictionnaire aux résultats de requêtes et renvoie un curseur
def connection_bdd():
    con = lite.connect('BD serious game.db')
    con.row_factory = lite.Row

    return con


# connecte à la BDD et renvoie toutes les lignes de la table personne
def selection_personnes():
    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("SELECT nom, prenom, role FROM personnes")

    lignes = cur.fetchall()

    conn.close()

    return lignes


def lancer_commande(x, y, z):

    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("INSERT INTO Commande('Date_livraison', 'Ref_produit', 'Ref_option') VALUES(" + str(x) + "," + str(y) + "," + str(z) + ")")

    conn.close()

    return lignes






# connecte à la B
# DD et renvoie les lignes de la table personne dont le prénom commence par la lettre donnée
def selection_personnes_lettre(lettre):
    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("SELECT nom, prenom, role FROM personnes WHERE prenom LIKE ?", (lettre + "%",))

    lignes = cur.fetchall()

    conn.close()

    return lignes


# connecte à la BDD et insère une nouvelle ligne avec les valeurs données
def insertion_personne(nom, prenom, role):
    try:
        conn = connection_bdd()
        cur = conn.cursor()

        cur.execute("INSERT INTO personnes('nom', 'prenom', 'role') VALUES (?,?,?)", (nom, prenom, role))

        conn.commit()

        conn.close()

        return True

    except lite.Error:

        return False


# ---------------------------------------
# les différentes pages (fonctions VUES)
# ---------------------------------------


# html
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/agilean')
def agilean():
    return render_template('agilean.html')

@app.route('/prepa_commande')
def prepa_commande():
    return render_template('prepa_commande.html')

@app.route('/passer_une_commande', methods = ['GET'])
def passer_une_commande():
    #if request.method == 'GET':
     #   try:
      #      pass
       #     x=str(datetime.datetime.now()) #'Date_livraison'
        #    y=str(request.form['option1'])+str(request.form['option1']) #'Ref_produit'
         #   z=request.form['type'] #'Ref_option'
          #  lancer_commande(x, y, z)
        #except ValueError:
        #    print("Oops!  That was no valid number.  Try again...")

    return render_template('passer_une_commande.html')


@app.route('/reception_commande')
def reception_commande():
    return render_template('reception_commande.html')


@app.route('/agilog')
def agilog():
    return render_template('agilog.html')


@app.route('/client')
def client():
    return render_template('client.html')


@app.route('/commandes_en_cours')
def commandes_en_cours():
    return render_template('commandes_en_cours.html')


@app.route('/lancer_oa')
def lancer_oa():
    return render_template('lancer_oa.html')


@app.route('/lancer_of')
def lancer_of():
    return render_template('lancer_of.html')


@app.route('/livraison')
def livraison():
    return render_template('livraison.html')


@app.route('/livraison_agilean')
def livraison_agilean():
    return render_template('livraison_agilean.html')


@app.route('/qualite')
def qualite():
    return render_template('qualite.html')


@app.route('/reception_composants')
def reception_composants():
    return render_template('reception_composants.html')





# php

@app.route('/insert')
def insert():
    # if request.method == 'POST':
    #    pass
    return render_template('Insert.html')


@app.route('/ajout_tache')
def ajout_tache():
    return render_template('ajout_tache.html')


@app.route('/tache_php')
def tache():
    return render_template('tache.php')


@app.route('/contact_php')
def contact():
    return render_template('contact.php')


# une page avec du texte statique


@app.route('/hello')
def hello():
    contenu = ""
    contenu += retour_index()
    contenu += "Hello, World !"

    return contenu


# une page avec du texte dynamique déterminé par l'URL
@app.route('/hello_url/<prenom>')
def hello_url_prenom(prenom):
    contenu = ""
    contenu += retour_index()
    contenu += "Hello, " + prenom + " !"

    return contenu


# une page avec un entier dynamique déterminé par l'URL
@app.route('/hello_url_entier/<int:valeur>')
def hello_url_entier(valeur):
    contenu = ""
    contenu += retour_index()
    contenu += "Hello, n * 2 = " + str(valeur * 2) + " !"

    return contenu


# une page avec du texte dynamique envoyé par HTTP/GET
@app.route('/hello_get', methods=['GET'])
def hello_get_prenom():
    contenu = ""
    contenu += retour_index()
    contenu += "Hello, " + request.args.get('prenom', 'une valeur par défaut') + " !"

    return contenu

    return contenu


@app.route('/fichier_statique')
def fichier_statique():
    contenu = ""
    contenu += retour_index()
    contenu += "Hello, World !<br/>"
    contenu += "<img src='" + url_for('static', filename='globe.png') + "'/>"

    return contenu


# une page avec du texte dynamique envoyé par HTTP/POST
@app.route('/hello_post', methods=['POST'])
def hello_post_prenom():
    contenu = ""
    contenu += retour_index()
    contenu += "Hello, " + request.form['prenom'] + " !"

    return contenu


# un page qui combine affichage du formulaire et traitement
@app.route('/formulaire_combine', methods=['GET', 'POST'])
def formulaire_combine():
    contenu = ""
    contenu += retour_index()

    erreur = ""
    if request.method == 'POST':

        if (request.form['prenom'][0].lower() == "a"):
            contenu += "Hello, " + request.form['prenom'] + " !"
            return contenu

        else:
            erreur = 'le prénom doit commencer par un "A"'

    # on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué

    if (erreur != ""):
        contenu += "<strong>Erreur : " + erreur + "</strong>"

    contenu += formulaire_prenom("formulaire_combine", prenom="prénom en A")

    return contenu


@app.route('/template_html', methods=['GET'])
def template_html():
    return render_template('index.html')


@app.route('/afficher_personnes', methods=['GET'])
def affichage_bdd_personnes():
    lignes = selection_personnes()

    return render_template('affichage_personnes.html', personnes=lignes)


@app.route('/afficher_personnes_a')
def affichage_bdd_personnes_a():
    lignes = selection_personnes_lettre("A")

    return render_template('affichage_personnes_lettre.html', lettre="A", personnes=lignes)


@app.route('/ajouter_personne', methods=['GET', 'POST'])
def insertion_bdd_personne():
    erreur = ""
    if request.method == 'POST':

        if (request.form['nom'] != "" and request.form['prenom'] != "" and request.form.get('role',
                                                                                            type=int) > 0 and request.form.get(
                'role', type=int) < 4):

            res = insertion_personne(request.form['nom'], request.form['prenom'], request.form.get('role', type=int))

            if (res):

                return redirect(url_for('affichage_bdd_personnes'))

            else:
                erreur = "Une erreur a été détectée lors de l'insertion dans la base de données. Veuillez réessayer ou contacter l'administrateur du site."
        else:
            erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."

    # on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué

    return render_template('formulaire_personne.html', msg=erreur, nom=request.form.get('nom', ''),
                           prenom=request.form.get('prenom', ''), role=request.form.get('role', 0, type=int))


# Test tutoriel

@app.route('/exo1', methods=['GET'])
def exo1():
    contenu = ""
    contenu += retour_index()
    contenu += "premier parametre: " + request.args.get('p1', 'une valeur par défaut') + "<br/><br/>"
    contenu += "deuxieme parametre: " + request.args.get('p2', 'une valeur par défaut')


@app.route('/formulaire_number', methods=['GET', 'POST'])
def formulaire_number():
    contenu = ""
    contenu += retour_index()

    erreur = ""
    if request.method == 'POST':

        try:
            int(request.form['prenom'])
            contenu += "The number is " + request.form['prenom'] + " !"
            return contenu

        except:
            erreur = 'The input should be a number'

    # on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué

    if (erreur != ""):
        contenu += "<strong>Erreur : " + erreur + "</strong>"

    contenu += formulaire_prenom("formulaire_number", prenom="the input should be a number")
    return contenu


# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
