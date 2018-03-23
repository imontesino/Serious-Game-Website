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

#afficher un e template html
def render_page(name):
    return render_template(str(name) + ".html")


# connecte à la BDD, affecte le mode dictionnaire aux résultats de requêtes et renvoie un curseur
def connection_bdd():
    con = lite.connect('BD serious game.db')
    con.row_factory = lite.Row

    return con

reftotal = 0


##################################  Client  ########################################


# Afficher toutes les commandes en cours
def lancer_commande(x, y, z):
    global reftotal

    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("INSERT INTO Commande(Date_livraison, Ref_produit, Ref_option) VALUES(" + str(datetime.datetime.now()) + "," + str(y) + "," + str(z) + ")")
    cur.execute("INSERT INTO commande_contient_option VALUES ref_commande=x, ref_option=y")
    lignes = cur.fetchall()

    conn.close()

    return lignes


# Lancer une nouvelle commande (ajout d'une commande dans la table Commande
def afficher_cmds_en_cours():
    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("SELECT ref_cmd, date_cmd, etat_cmd, ref_produit FROM Commande WHERE Etat_Cmd=0")

    conn.close()

    return lignes

#Valider une réception de la commande x
def valider_reception(ref):

    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("UPDATE commande SET etat_cmd = 1 WHERE ref_commande = " + str(ref))
    lignes = cur.fetchall()

    conn.close()

    return




##################################  AGILEAN  #####################################

#Lancer ordre de fabrication
def lancer_ordref(ref):

    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("UPDATE commande SET Date_OF = " + str(datetime.datetime.now()) + " WHERE ref_commande = " + str(ref))

    conn.close()

    return

#Lancer OA
def lancer_ordrea(ref):

    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("UPDATE commande SET Date_OA = " + str(datetime.datetime.now()) + " WHERE ref_commande = " + str(ref))

    conn.close()

    return

#Ajouter une demande de kit correspondant à l'OA lancé
def demande_kit(ref, id, quant):

    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("INSERT INTO Demander_kits(ref_cmd, id_kit, quantite) VALUES (?,?,?)", (ref, id, quant))

    conn.close()

    return

#Accuser réception des kits pour la commande y
def ajputer_demande_kit(ref):

    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("UPDATE commande SET Date_recpKit = " + str(datetime.datetime.now()) + " WHERE ref_commande = " + str(ref))
    conn.close()

    return

#Ajouter un problème de qualité (avec date de détection, lieu, et description et réf de commande associée)
def probleme_qualite(id, lieu, description, ref):

    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("INSERT INTO Qualité(ref_qualite, date_detection, lieu, description, ref_commande) VALUES(?,?,?,?,?)", (id,str(datetime.datetime.now()),lieu,description,ref))

    conn.close()

    return

#Ajouter dans la table commande la date du contrôle qualité x à la commande de référence y
def ajouter_date_qualite(ref):

    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("UPDATE Commande SET Date_ctrl_quali= " + str(datetime.datetime.now()) + "WHERE ref_commande = " + str(ref))

    conn.close()

    return

#Livrer la commande x au client (date automatique)
def livrer_commande(ref):

    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("UPDATE Commande SET Date_livraison VALUES(" + str(datetime.datetime.now()) + ")")

    conn.close()

    return




##################################  AGILOG  ######################################

#Livrer les kits de la commande de référence x à Agilean (la commande va entrer l'instant de livraison automatiquement à la colonne date_liv_agilog)
def livrer_kit():
    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("UPDATE Commande SET Date_liv_Agilog VALUES(" + str(datetime.datetime.now()) + ")")

    conn.close()

    return

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


@app.route('/agilog')
def agilog():
    return render_template('agilog.html')


@app.route('/ajout_tache')
def ajout_tache():
    return render_template('ajout_tache.html')


@app.route('/client')
def client():
    return render_template('client.html')


@app.route('/commandes_en_cours')
def commandes_en_cours():
    return render_template('commandes_en_cours.html')


@app.route('/cmd_urgente')
def cmd_urgente():
    return render_template('cmd_urgente.html')


@app.route('/insert')
def insert():
    # if request.method == 'POST':
    #    pass
    return render_template('Insert.html')


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


@app.route('/prepa_commande')
def prepa_commande():
    return render_template('prepa_commande.html')


@app.route('/passer_une_commande', methods=['GET'])
def passer_une_commande():
    # if request.method == 'GET':
    #   try:
    #      pass
    #     x=str(datetime.datetime.now()) #'Date_livraison'
    #    y=str(request.form['option1'])+str(request.form['option1']) #'Ref_produit'
    #   z=request.form['type'] #'Ref_option'
    #  lancer_commande(x, y, z)
    # except ValueError:
    #    print("Oops!  That was no valid number.  Try again...")

    return render_template('passer_une_commande.html')


@app.route('/qualite')
def qualite():
    return render_template('qualite.html')


@app.route('/reception_commande')
def reception_commande():
    return render_template('reception_commande.html')


@app.route('/reception_composants')
def reception_composants():
    return render_template('reception_composants.html')


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
