# Python-Planning-Aurion

Classe Python pour télécharger le planning Aurion sous forme d'une chaîne JSON  
Aurion est un "ERP de Scolarité" créé par Auriga. Il permet de gérer entr-autres le planning des étudiants dans des grandes écoles  
**BDeliers, août 2018**  
Sous License APACHE 2.0  

---

Pour fonctionner, ce module se connecte à Aurion dans Firefox (de manière invisible) puis récupère les infos indispensables.
Par la suite, il envoie une requête HTTP à une page d'Aurion pour récupérer les données de planning, que le script convertit ensuite
en JSON.

---

Pour utiliser cette classe, il vous faudra installer Python 3 et Pip3 ainsi que Firefox  
Sous linux :

```shell
    sudo apt-get install python3 python3-dev python3-pip
```

Ensuite, les modules selenium, lxml et requests sont indispensables

```shell
    sudo pip3 install selenium
    sudo pip3 install lxml
    sudo pip3 install requests
```

Enfin, il vous faudra télécharger [geckodriver](https://github.com/mozilla/geckodriver/releases) et le désarchiver dans le répertoire qui contient votre script python (ou bien l'ajouter au PATH)

---

Exemple d'utilisation pour récupérer le planning du mois prochain :

```python
    # La classe
    from aurion import *

    # Modules de temps
    from datetime import datetime, timedelta
    from time import mktime, sleep

    # Current directory
    from os import getcwd

    # Date actuelle, le mois prochain, dans 2 mois
    maintenant = datetime.now()
    moisPro = datetime.now() + timedelta(days=31)
    moisProPro = moisPro + timedelta(days=31)

    # Début et fin : le mois prochain et dans 2 mois
    debut = int(mktime(moisPro.timetuple()))
    fin = int(mktime(moisProPro.timetuple()))

    # On initialise l'objet en supposant que geckodriver est dans le répertoire courant
    aurion = Aurion("monLogin", "monMDP", getcwd() + "./geckodriver")

    # On récupère les informations de login
    aurion.queryInformations()

    # On descend le planning en JSON
    print(aurion.queryPlanningOnPeriod(debut, fin))
```
