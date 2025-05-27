menu = """

[1] Déposer
[2] Retirer
[3] Relevé de compte
[0] Quitter

=> """

solde = 0
limite = 500
releve = ""
nombre_retraits = 0
LIMITE_RETRAITS = 3

while True:
    option = input(menu)

    if option == "1":
        # Demander le montant du dépôt
        try:
            montant = float(input("Indiquez le montant du dépôt : "))
        except ValueError:
            print("Entrée invalide : veuillez saisir un nombre.")
            continue

        if montant > 0:
            solde += montant
            releve += f"Dépôt : € {montant:.2f}\n"
        else:
            print("Opération échouée ! Le montant indiqué est invalide.")

    elif option == "2":
        # Demander le montant du retrait
        try:
            montant = float(input("Indiquez le montant du retrait : "))
        except ValueError:
            print("Entrée invalide : veuillez saisir un nombre.")
            continue

        depasse_solde = montant > solde
        depasse_limite = montant > limite
        depasse_retraits = nombre_retraits >= LIMITE_RETRAITS

        if depasse_solde:
            print("Opération échouée ! Vous n'avez pas assez de solde.")
        elif depasse_limite:
            print("Opération échouée ! Le montant du retrait dépasse la limite.")
        elif depasse_retraits:
            print("Opération échouée ! Nombre maximum de retraits atteint.")
        elif montant > 0:
            solde -= montant
            releve += f"Retrait : € {montant:.2f}\n"
            nombre_retraits += 1
        else:
            print("Opération échouée ! Le montant indiqué est invalide.")

    elif option == "3":
        print("\n================ RELEVÉ DE COMPTE ================")
        print("Aucune opération effectuée." if not releve else releve)
        print(f"\nSolde : € {solde:.2f}")
        print("==================================================")

    elif option == "0":
        print("Merci d'avoir utilisé notre service. À bientôt !")
        break

    else:
        print("Opération invalide, veuillez sélectionner une option valide.")
