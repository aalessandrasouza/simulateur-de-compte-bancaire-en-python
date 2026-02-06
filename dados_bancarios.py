import re

# Listes pour stocker les utilisateurs et les comptes
utilisateurs = []
comptes = []

# Fonction pour enregistrer un utilisateur
def enregistrer_utilisateur():
    nom = input("Nom : ")
    date_naissance = input("Date de naissance (JJ/MM/AAAA) : ")
    cpf = input("CPF (uniquement des chiffres) : ").strip()
    
    # Valider CPF : uniquement des chiffres et unique
    if not cpf.isdigit() or len(cpf) != 11:
        print("CPF invalide. Doit contenir exactement 11 chiffres.")
        return
    if any(u['cpf'] == cpf for u in utilisateurs):
        print("CPF déjà enregistré. Impossible d'enregistrer deux utilisateurs avec le même CPF.")
        return
    
    adresse = input("Adresse (logradouro, numero - bairro - cidade/sigla estado) : ")
    
    utilisateur = {
        'nom': nom,
        'date_naissance': date_naissance,
        'cpf': cpf,
        'adresse': adresse
    }
    utilisateurs.append(utilisateur)
    print("Utilisateur enregistré avec succès !")

# Fonction pour enregistrer un compte bancaire
def enregistrer_compte():
    cpf = input("CPF de l'utilisateur : ").strip()
    
    # Filtrer l'utilisateur par CPF
    utilisateur = next((u for u in utilisateurs if u['cpf'] == cpf), None)
    if not utilisateur:
        print("Utilisateur non trouvé. Enregistrez l'utilisateur d'abord.")
        return
    
    # Créer le compte
    agence = "0001"
    numero_compte = len(comptes) + 1
    compte = {
        'agence': agence,
        'numero_compte': numero_compte,
        'utilisateur': cpf,
        'solde': 0,
        'releve': "",
        'nombre_retraits': 0
    }
    comptes.append(compte)
    print(f"Compte enregistré avec succès ! Agence : {agence}, Compte : {numero_compte}")

# Fonction pour dépôt (positional only)
def deposer(solde, valeur, releve):
    if valeur > 0:
        solde += valeur
        releve += f"Dépôt : € {valeur:.2f}\n"
        print(f"Dépôt de € {valeur:.2f} effectué avec succès !")
    else:
        print("Valeur invalide pour le dépôt.")
    return solde, releve

# Fonction pour retrait (keyword only)
def retirer(*, solde, valeur, releve, limite, nombre_retraits, limite_retrait):
    if valeur <= 0:
        print("Valeur invalide pour le retrait.")
        return solde, releve
    if valeur > solde:
        print("Solde insuffisant.")
        return solde, releve
    if valeur > limite:
        print("Valeur dépasse la limite de retrait.")
        return solde, releve
    if nombre_retraits >= limite_retrait:
        print("Nombre maximum de retraits atteint.")
        return solde, releve
    
    solde -= valeur
    releve += f"Retrait : € {valeur:.2f}\n"
    nombre_retraits += 1
    print(f"Retrait de € {valeur:.2f} effectué avec succès !")
    return solde, releve

# Fonction pour afficher le relevé (positional : solde ; keyword : releve)
def afficher_releve(solde, *, releve):
    print("\n================ RELEVÉ DE COMPTE ================")
    print("Aucune opération effectuée." if not releve else releve)
    print(f"\nSolde : € {solde:.2f}")
    print("==================================================")

# Fonction pour lister les comptes
def lister_comptes():
    if not comptes:
        print("Aucun compte enregistré.")
        return
    for compte in comptes:
        utilisateur = next((u for u in utilisateurs if u['cpf'] == compte['utilisateur']), None)
        nom_utilisateur = utilisateur['nom'] if utilisateur else "Utilisateur non trouvé"
        print(f"Agence : {compte['agence']}, Compte : {compte['numero_compte']}, Utilisateur : {nom_utilisateur} (CPF : {compte['utilisateur']})")

# Menu principal
menu = """
[1] Déposer
[2] Retirer
[3] Relevé de compte
[4] Enregistrer un utilisateur
[5] Enregistrer un compte
[6] Lister les comptes
[0] Quitter

=> """

# Variables pour un compte actif (pour les opérations bancaires ; dans un système réel, il serait sélectionné)
compte_actif = None
LIMITE_RETRAIT = 500
LIMITE_RETRAITS = 3

while True:
    option = input(menu).strip()
    
    if option == "1":  # Déposer
        if not compte_actif:
            print("Aucun compte actif. Enregistrez et sélectionnez un compte.")
            continue
        try:
            valeur = float(input("Montant du dépôt : "))
            compte_actif['solde'], compte_actif['releve'] = deposer(
                compte_actif['solde'], valeur, compte_actif['releve']
            )
        except ValueError:
            print("Montant invalide.")
    
    elif option == "2":  # Retirer
        if not compte_actif:
            print("Aucun compte actif. Enregistrez et sélectionnez un compte.")
            continue
        try:
            valeur = float(input("Montant du retrait : "))
            compte_actif['solde'], compte_actif['releve'] = retirer(
                solde=compte_actif['solde'],
                valeur=valeur,
                releve=compte_actif['releve'],
                limite=LIMITE_RETRAIT,
                nombre_retraits=compte_actif['nombre_retraits'],
                limite_retrait=LIMITE_RETRAITS
            )
        except ValueError:
            print("Montant invalide.")
    
    elif option == "3":  # Relevé de compte
        if not compte_actif:
            print("Aucun compte actif. Enregistrez et sélectionnez un compte.")
            continue
        afficher_releve(compte_actif['solde'], releve=compte_actif['releve'])
    
    elif option == "4":  # Enregistrer un utilisateur
        enregistrer_utilisateur()
    
    elif option == "5":  # Enregistrer un compte
        enregistrer_compte()
        # Après enregistrement, définir le dernier compte comme actif pour les opérations (simplification)
        if comptes:
            compte_actif = comptes[-1]
            print("Compte actif défini pour les opérations.")
    
    elif option == "6":  # Lister les comptes
        lister_comptes()
    
    elif option == "0":  # Quitter
        print("Merci d'avoir utilisé notre système bancaire !")
        break
    
    else:
        print("Option invalide. Veuillez réessayer.")