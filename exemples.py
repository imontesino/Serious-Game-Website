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
    con = lite.connect('BD_serious_game.db')
    con.row_factory = lite.Row

    return con

reftotal = 0

     
def selection_commandes(etat_cmd):
	
	conn = connection_bdd()
	cur = conn.cursor()
	
	cur.execute("SELECT ref_commande, Date_commande, Ref_prod, ref_opt, Etat_cmd FROM Commande WHERE Etat_cmd LIKE ?", (etat_cmd,))
	
	lignes = cur.fetchall()
	
	conn.close()
	
	return lignes
	
def selection_commandes_liv(etat_cmd):
	
	conn = connection_bdd()
	cur = conn.cursor()
	
	cur.execute("SELECT ref_commande, Date_commande,Date_OA, Ref_prod, ref_opt, Etat_cmd FROM Commande WHERE Etat_cmd LIKE ? ORDER BY Date_commande ASC", (etat_cmd,))
	
	lignes = cur.fetchall()
	
	conn.close()
	
	return lignes


def selection_commandes_liv_client():
	
	conn = connection_bdd()
	cur = conn.cursor()
	
	cur.execute("SELECT ref_commande, Date_commande, Date_livraison, Ref_prod, ref_opt, Etat_cmd FROM Commande WHERE Etat_cmd LIKE 'En attente de validation client' OR Etat_cmd LIKE 'Validée par le client' ORDER BY Date_commande ASC")
	
	lignes = cur.fetchall()
	
	conn.close()
	
	return lignes


def selection_commandes_production():
	
	conn = connection_bdd()
	cur = conn.cursor()
	
	cur.execute("SELECT ref_commande, Date_commande, Date_OF, Ref_prod, ref_opt, Etat_cmd FROM Commande WHERE Etat_cmd LIKE 'En cours de fabrication' OR Etat_cmd LIKE 'Prête pour lancement OF' ORDER BY Date_commande ASC")
	
	lignes = cur.fetchall()
	
	conn.close()
	
	return lignes

def selection_pb_qualite():
	
	conn = connection_bdd()
	cur = conn.cursor()
	
	cur.execute("SELECT ref_qualite, Ref_commande, Date_detection, Lieu, Description FROM Qualité")
	
	lignes = cur.fetchall()
	
	conn.close()
	
	return lignes
	


##################################  Client  ########################################



def modele_vehicule(x):		
	
	 
	if x == 1:
		return 'CLF'
	elif x == 2:
		return 'CLO'
	elif x == 3:
		return 'CCF'
	elif x == 4 :
		return 'CCO'

def option_vehicule(y):		
	
	 
	if y == 1:
		return 'Sans option'
	elif y == 2:
		return 'Antenne'
	elif y == 3:
		return 'Crochet d''attelage'
	elif y == 4:
		return 'Attache accesoire'
	elif y == 5 :
		return 'Antenne-Crochet d''attelage'
	elif y == 6 :
		return 'Antenne-Attache accesoire'
	elif y == 7 :
		return 'Crochet d''attelage-Attache accesoire'
	elif y == 8 :
		return 'Antenne-Crochet d''attelage-Attache accesoire'
	

# Lancer une nouvelle commande (ajout d'une commande dans la table Commande
def lancer_commande(x, choix, option,etat):
	try:
		conn = connection_bdd()
		cur = conn.cursor()
		
		cur.execute("INSERT INTO Commande('Date_commande', 'Ref_prod', 'ref_opt', 'Etat_cmd') VALUES(?,?,?,?)", (x,modele_vehicule(choix),option_vehicule(option),etat))
		
		conn.commit()
		
		conn.close()
		
		return True
		
	except lite.Error:
		
		return False
 

# Afficher toutes les commandes en cours
def afficher_cmds_en_cours():
    conn = connection_bdd()
    cur = conn.cursor()

    cur.execute("SELECT ref_cmd, date_cmd, etat_cmd, ref_produit FROM Commande WHERE Etat_Cmd=0")

    conn.close()

    return lignes

#Valider une réception de la commande x
def valider_reception(ref_cmd):

    conn = connection_bdd()
    cur = conn.cursor()
    cur.execute("UPDATE Commande SET Etat_cmd = 'Validée par le client' WHERE ref_commande ="+ref_cmd)
    conn.commit()
    conn.close()
    return 1


##################################  AGILEAN  ########Va#############################

#Lancer OA
def commander_composants(ref_cmd):

    conn = connection_bdd()
    cur = conn.cursor()
    x=datetime.datetime.now()
    y=str(x)
    cur.execute("UPDATE Commande  SET Date_OA=? WHERE ref_commande =?", (y[11:19], ref_cmd))
    cur.execute("UPDATE Commande SET Etat_cmd = 'En attente de composants' WHERE ref_commande ="+ref_cmd)
    conn.commit()
    conn.close()
    return 1

#Validation des composants reçus par AgiLog
def valider_reception_comp(ref_cmd):

    conn = connection_bdd()
    cur = conn.cursor()
    x=datetime.datetime.now()
    y=str(x)
    cur.execute("UPDATE Commande SET Etat_cmd = 'Prête pour lancement OF', Date_recpKit=? WHERE ref_commande =?",(y[11:19],ref_cmd))
    conn.commit()
    conn.close()
    return 1

#Lancer ordre de fabrication
def lancement_of(ref_cmd):

    conn = connection_bdd()
    cur = conn.cursor()
    x=datetime.datetime.now()
    y=str(x)
    cur.execute("UPDATE Commande SET Etat_cmd = 'En cours de fabrication', Date_OF=? WHERE ref_commande =?",(y[11:19],ref_cmd))
    conn.commit()
    conn.close()
    return 1

#Ajouter un produit fini au stock
def ajouter_PF(ref_cmd):

    conn = connection_bdd()
    cur = conn.cursor()
    cur.execute("UPDATE Commande SET Etat_cmd = 'En stock' WHERE ref_commande ="+ref_cmd)
    conn.commit()
    conn.close()
    return 1
    
#Fonction pour livrer le client
def livraison_client(ref_cmd):

    conn = connection_bdd()
    cur = conn.cursor()
    x=datetime.datetime.now()
    y=str(x)
    cur.execute("UPDATE Commande SET Etat_cmd = 'En attente de validation client', Date_livraison=? WHERE ref_commande =?",(y[11:19],ref_cmd))
    conn.commit()
    conn.close()
    return 1



#Déclarer un problème qualité
def declarer_pb_qualite(ref, lieu, description):
	try:
		conn = connection_bdd()
		cur = conn.cursor()
		x=datetime.datetime.now()
		y=str(x)
	
		cur.execute("INSERT INTO Qualité(Date_detection, Lieu, Description, Ref_commande) VALUES(?,?,?,?)", (y[11:19],lieu,description,ref))
		cur.execute("UPDATE Commande SET Etat_cmd = 'Problème qualité' WHERE ref_commande ="+ref)
		conn.commit()
		
		conn.close()
		
		return True
		
	except lite.Error:
		
		return False

def remettre_stock_pf(ref_cmd):

    conn = connection_bdd()
    cur = conn.cursor()
    cur.execute("UPDATE Commande SET Etat_cmd = 'En stock' WHERE ref_commande ="+ref_cmd)
    conn.commit()
    conn.close()
    return 1


 


##################################  AGILOG  ######################################

#Fonction pour lancer la préparation des commandes
def lancer_prepa(ref_cmd):

    conn = connection_bdd()
    cur = conn.cursor()
    cur.execute("UPDATE Commande SET Etat_cmd = 'En cours de préparation de kits' WHERE ref_commande ="+ref_cmd)
    conn.commit()
    conn.close()
    return 1

#Fonction pour enregistrer les kits réalisés 
def finaliser_prepa(ref_cmd):

    conn = connection_bdd()
    cur = conn.cursor()
    cur.execute("UPDATE Commande SET Etat_cmd = 'Kits prêts' WHERE ref_commande ="+ref_cmd)
    conn.commit()
    conn.close()
    return 1
    
#Fonction pour livrer AgiLean   
def livrer_kits(ref_cmd):

    conn = connection_bdd()
    cur = conn.cursor()
    x=datetime.datetime.now()
    y=str(x)
    cur.execute("UPDATE Commande SET Etat_cmd = 'Kits livrés à AgiLean', Date_liv_AgiLog=? WHERE ref_commande =?",(y[11:19],ref_cmd))
    conn.commit()
    conn.close()
    return 1
    


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



@app.route('/client')
def client():
    return render_template('client.html')



@app.route('/cmd_urgente')
def cmd_urgente():
    return render_template('cmd_urgente.html')

	
@app.route('/commandes_en_cours_client', methods=['GET'])
def commandes_en_cours_client():
	
	lignes = selection_commandes("%")
	
	return render_template('commandes_en_cours_client.html', commandes = lignes)

@app.route('/passer_une_commande', methods=['GET','POST'])
def passer_une_commande():
	erreur = ""
	if request.method == 'POST':
		
		if (request.form.get('choix', type=int) > 0 and request.form.get('choix', type=int) < 5 and request.form.get('choix_opt', type=int) > 0 and request.form.get('choix_opt', type=int) < 8):
			x=datetime.datetime.now()
			y=str(x)
			res = lancer_commande(y[11:19],request.form.get('choix', type=int),request.form.get('choix_opt', type=int),"Envoyée à AgiLean")
			
			if (res):
			
				return redirect(url_for('commandes_en_cours_client'))
				
			else:
				erreur = "Une erreur a été détectée lors de l'insertion dans la base de données. Veuillez réessayer ou contacter l'administrateur du site."
		else:
			erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	return render_template('passer_une_commande.html', msg = erreur, choix = request.form.get('role', 0, type=int))
	

@app.route('/reception_commande', methods=['GET','POST'])
def reception_commande():
	
	lignes = selection_commandes_liv_client()
	erreur = ""
	if request.method == 'POST':
		
		if (request.form['ref_cmd'] != ""):
			
			res=valider_reception(request.form['ref_cmd'])
			
			if (res):
			
				return redirect(url_for('reception_commande'))
				
			else:
				erreur = "Une erreur a été détectée lors de la modification de la base de données. Veuillez réessayer ou contacter l'administrateur du site."
		else:
			erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	return render_template('reception_commande.html',commandes = lignes, msg = erreur, ref_cmd = request.form.get('ref_cmd', ''))

@app.route('/lancer_oa', methods=['GET','POST'])
def lancer_oa():
	
	lignes = selection_commandes_liv("Envoyée à AgiLean")
	erreur = ""
	if request.method == 'POST':
		
		if (request.form['ref_cmd'] != ""):
			
			res=commander_composants(request.form['ref_cmd'])
			
			if (res):
			
				return redirect(url_for('lancer_oa'))
				
			else:
				erreur = "Une erreur a été détectée lors de la modification de la base de données. Veuillez réessayer ou contacter l'administrateur du site."
		else:
			erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	return render_template('lancer_oa.html',commandes = lignes, msg = erreur, ref_cmd = request.form.get('ref_cmd', ''))
	
@app.route('/prepa_commande', methods=['GET','POST'])
def prepa_commande():
	
	lignes = selection_commandes_liv("En attente de composants")
	erreur = ""
	if request.method == 'POST':
		
		if (request.form['ref_cmd'] != ""):
			
			res=lancer_prepa(request.form['ref_cmd'])
			
			if (res):
			
				return redirect(url_for('prepa_commande'))
				
			else:
				erreur = "Une erreur a été détectée lors de la modification de la base de données. Veuillez réessayer ou contacter l'administrateur du site."
		else:
			erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	return render_template('prepa_commande.html',commandes = lignes, msg = erreur, ref_cmd = request.form.get('ref_cmd', ''))

@app.route('/commandes_en_cours', methods=['GET','POST'])
def commandes_en_cours():
	
	lignes = selection_commandes("En cours de préparation de kits")
	erreur = ""
	if request.method == 'POST':
		
		if (request.form['ref_cmd'] != ""):
			
			res=finaliser_prepa(request.form['ref_cmd'])
			
			if (res):
			
				return redirect(url_for('commandes_en_cours'))
				
			else:
				erreur = "Une erreur a été détectée lors de la modification de la base de données. Veuillez réessayer ou contacter l'administrateur du site."
		else:
			erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	return render_template('commandes_en_cours.html',commandes = lignes, msg = erreur, ref_cmd = request.form.get('ref_cmd', ''))
	

@app.route('/livraison_agilean', methods=['GET','POST'])
def livraison_agilean():
	lignes = selection_commandes_liv("Kits prêts")
	erreur = ""
	if request.method == 'POST':
		
		if (request.form['ref_cmd'] != ""):
			
			res=livrer_kits(request.form['ref_cmd'])
			
			if (res):
			
				return redirect(url_for('livraison_agilean'))
				
			else:
				erreur = "Une erreur a été détectée lors de la modification de la base de données. Veuillez réessayer ou contacter l'administrateur du site."
		else:
			erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	return render_template('livraison_agilean.html',commandes = lignes, msg = erreur, ref_cmd = request.form.get('ref_cmd', ''))

@app.route('/reception_composants', methods=['GET','POST'])
def reception_composants():
	lignes = selection_commandes_liv("Kits livrés à AgiLean")
	erreur = ""
	if request.method == 'POST':
		
		if (request.form['ref_cmd'] != ""):
			
			res=valider_reception_comp(request.form['ref_cmd'])
			
			if (res):
			
				return redirect(url_for('reception_composants'))
				
			else:
				erreur = "Une erreur a été détectée lors de la modification de la base de données. Veuillez réessayer ou contacter l'administrateur du site."
		else:
			erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	return render_template('reception_composants.html',commandes = lignes, msg = erreur, ref_cmd = request.form.get('ref_cmd', ''))  
    
@app.route('/lancer_of', methods=['GET','POST'])
def lancer_of():
	lignes = selection_commandes_production()
	erreur = ""
	if request.method == 'POST':
		
		if (request.form['ref_cmd_of'] != ""):
			
			res=lancement_of(request.form['ref_cmd_of'])
			
			if (res):
			
				return redirect(url_for('lancer_of'))
				
			else:
				erreur = "Une erreur a été détectée lors de la modification de la base de données. Veuillez réessayer ou contacter l'administrateur du site."
		else:
			erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	return render_template('lancer_of.html',commandes = lignes, msg = erreur, ref_cmd = request.form.get('ref_cmd_of', '')) 
    
@app.route('/ajouter_pf', methods=['GET','POST'])
def ajouter_pf():
	lignes = selection_commandes_production()
	erreur = ""
	if request.method == 'POST':
		
		if (request.form['ref_cmd'] != ""):
			
			res=ajouter_PF(request.form['ref_cmd'])
			
			if (res):
			
				return redirect(url_for('ajouter_pf'))
				
			else:
				erreur = "Une erreur a été détectée lors de la modification de la base de données. Veuillez réessayer ou contacter l'administrateur du site."
		else:
			erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	return render_template('lancer_of.html',commandes = lignes, msg = erreur, ref_cmd = request.form.get('ref_cmd', '')) 
    
@app.route('/livrer_client', methods=['GET','POST'])
def livrer_client():
	lignes = selection_commandes("En stock")
	erreur = ""
	if request.method == 'POST':
		
		if (request.form['ref_cmd'] != ""):
			
			res=livraison_client(request.form['ref_cmd'])
			
			if (res):
			
				return redirect(url_for('livrer_client'))
				
			else:
				erreur = "Une erreur a été détectée lors de la modification de la base de données. Veuillez réessayer ou contacter l'administrateur du site."
		else:
			erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	return render_template('livrer_client.html',commandes = lignes, msg = erreur, ref_cmd = request.form.get('ref_cmd', '')) 
    
    
@app.route('/qualite', methods=['GET', 'POST'])
def qualite():
	lignes=selection_pb_qualite()
	erreur = ""
	if request.method == 'POST':
		
		if (request.form['ref_cmd'] != "" and request.form['lieu'] != "" and request.form['description'] != "" ):
			
			res = declarer_pb_qualite(request.form['ref_cmd'],request.form['lieu'],request.form['description'])
			
			if (res):
			
				return redirect(url_for('livrer_client'))
				
			else:
				erreur = "Une erreur a été détectée lors de l'insertion dans la base de données. Veuillez réessayer ou contacter l'administrateur du site."
		else:
			erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	return render_template('qualite.html', msg = erreur,commandes = lignes, ref_cmd = request.form.get('ref_cmd', ''), lieu = request.form.get('lieu', ''), description = request.form.get('description', ''))

#Route pour réinjecter les commandes dont les problèmes qualité ont été réglés
@app.route('/injecter_stock', methods=['GET', 'POST'])
def injecter_stock():
	erreur = ""
	if request.method == 'POST':
		
		if (request.form['ref'] != ""):
			
			res = remettre_stock_pf(request.form['ref'])
			
			if (res):
			
				return redirect(url_for('livrer_client'))
				
			else:
				erreur = "Une erreur a été détectée lors de l'insertion dans la base de données. Veuillez réessayer ou contacter l'administrateur du site."
		else:
			erreur = "Une erreur a été détectée dans le formulaire, merci de remplir tous les champs correctement."
	
	# on arrive ici si rien n'a été envoyé par POST, ou si la validation des données a échoué
	
	return render_template('qualite.html', msg = erreur, ref = request.form.get('ref', ''))




# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0')
	
	
	
	
	
	
	
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
