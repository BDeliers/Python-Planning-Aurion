# Python-Planning-Aurion

Classe Python pour télécharger le planning Aurion sous forme d'une chaîne JSON
BDeliers, août 2018
Sous License APACHE 2.0

---

Pour utiliser cette classe, il vous faudra installer Python 3 et Pip3 ainsi que Firefox
Sous linux :

```
    sudo apt-get install python3 python3-dev python3-pip
```

Ensuite, les modules selenium, lxml et requests sont indispensables

```
    sudo pip3 install selenium
    sudo pip3 install lxml
    sudo pip3 install requests
```

Enfin, il vous faudra télécharger [geckodriver](https://github.com/mozilla/geckodriver/releases) et le désarchiver

---

Exemple d'utilisation pour récupérer le planning du mois prochain :

```
    # La classe
    from aurion import *
    # Modules nécessaires pour l'exemple
    from datetime import datetime, timedelta
    from time import mktime, sleep

    # Date actuelle, le mois prochain, dans 2 mois
    maintenant = datetime.now()
    moisPro = datetime.now() + timedelta(days=31)
    moisProPo = moisPro + timedelta(days=31)

    # Début et fin : le mois prochain et dans 2 mois
    debut = int(mktime(moisPro.timetuple()))
    tend = int(mktime(moisProPro.timetuple()))

    # On initialise l'objet en supposant que geckodriver est dans le répertoire courant
    aurion = Aurion("monLogin", "monMDP", getcwd() + "/geckodriver")
    # On récupère les informations de login
    aurion.queryInformations()

    # On descend le planning en JSON
    print(aurion.queryPlanningOnPeriod(debut, fin))
```
