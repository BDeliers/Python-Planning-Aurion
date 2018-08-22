#!/usr/bin/python3
# -*-coding:Utf-8 -*

# HTTP requests
import requests

# Selenium for Firefox control
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

# XML parser
from xml.etree import ElementTree as etree

# JSON parser
import json

# Sleep
from time import sleep


class Aurion:
    """
        By BDeliers, Août 2018
        SOUS LICENSE APACHE

        Classe qui récupère les données de planning entre deux timestamps sous forme de chaîne JSON
        Pour instancier la classe : Aurion(username, password, geckodriver)

        username = votre login
        password = votre mdp
        geckodriver = le chemin du geckodriver

        Pour descendre les informations nécessaires : queryInformations()
        Pour télécharger le planning : queryPlanningOnPeriod(timestamp départ, timestamp fin) et retourne les évènements

        Dépendances nécessaires : requests, lxml, selenium (installées par PIP)
        Programmes nécessaires : Firefox
        Autres : mettre geckodriver dans /usr/bin (ou dans le $PATH)

    """

    def __init__(self, username, password, geckodriver):
        self._url = "https://aurion-lille.yncrea.fr"
        self._username = username
        self._password = password
        self._geckodriver = geckodriver

    def queryPlanningOnPeriod(self, start, end):
        """
            Télécharge les données du planning entre un timestamp start et un timestamp end
        """

        # x1000 nénécessaire
        start = start * 1000
        end = end * 1000

        # Cookie à envoyer
        cookies = {
            "JSESSIONID": self._sessionId,
        }

        # Headers
        headers = {
            "Host": "aurion-lille.yncrea.fr",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Accept-Language": "fr-FR,fr;q=0.5",
            "Referer": "https://aurion-lille.yncrea.fr/faces/Planning.xhtml",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Faces-Request": "partial/ajax",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
        }

        # Données
        data = [
          ("javax.faces.partial.ajax", "true"),
          ("javax.faces.source", self._formId),
          ("javax.faces.partial.execute", self._formId),
          ("javax.faces.partial.render", self._formId),
          (self._formId, self._formId),
          (self._formId + "_start", start),
          (self._formId + "_end", end),
          ("form", "form"),
          ("form:largeurDivCenter", "1606"),
          ("form:j_idt133_view", "week"),
          ("form:offsetFuseauNavigateur", "-7200000"),
          ("form:onglets_activeIndex", "0"),
          ("form:onglets_scrollState", "0"),
          ("javax.faces.ViewState", self._viewState),
        ]

        # La requête
        r = requests.post(self._url + "/faces/Planning.xhtml", headers=headers, cookies=cookies, data=data)

        # Retour en XML
        xml = etree.fromstring(r.text)
        # On parse la parti intéressante en JSON
        events = json.loads(xml.findall(".//update")[1].text)["events"]

        eventsFormatted = []

        # On formatte un peu tout ça
        for i in range(0, len(events)):
            tmp = events[i]["title"]
            tmp = tmp.split("-")
            for j in range(0, len(tmp)):
                # Espaces en début/fin
                tmp[j] = tmp[j].strip()
            # Les noms de profs
            # Remplacer les slashes par des virgules
            tmp[4] = tmp[4].replace('/', ',')
            # En minuscule
            tmp[4] = tmp[4].lower()
            # Première lettre en majuscule
            tmp[4] = tmp[4].title()
            # Un bel évèneent formatté
            tmp = {"debut":events[i]["start"], "fin":events[i]["end"], "type":tmp[2], "cours":tmp[3], "prof":tmp[4], "salle":tmp[5], "titre":tmp[6]}
            # On l'ajoute à la liste
            eventsFormatted.append(tmp)

        return eventsFormatted

    def queryInformations(self):
        """
            Récupère les informations vitales au programme : le cookie de session et le ViewState, ne retourne rien
        """

        # Options firefox sans interface
        options = Options()
        options.add_argument("--headless")

        # On initialise le driver
        driver = webdriver.Firefox(options=options, executable_path=self._geckodriver)

        # On se connecte au faux formulaire de login
        driver.get(self._url + "/faces/Login.xhtml")

        # On attend le chargement de la page de login d'Aurion
        while True:
            try:
                driver.find_element_by_id("username")
                break
            except:
                sleep(1)
                continue

        # On le remplit avec les infos de l'utilisateur et on le valide
        driver.find_element_by_id("username").send_keys(self._username)
        driver.find_element_by_id("password").send_keys(self._password)
        driver.find_element_by_xpath("//button[@type='submit']").click()

        # On attend le chargement de la page d'accueil d'Aurion
        while True:
            try:
                # On clicke sur l'onglet Planning
                driver.find_element_by_link_text("Mon Planning").click()
                break
            except:
                sleep(1)
                continue


        # Quand le planning est chargé
        while True:
            try:
                driver.find_element_by_xpath("//button[text()='Mois']")
                break
            except:
                sleep(1)
                continue

        # On récupère la valeur du ViewState
        self._viewState = driver.find_element_by_xpath("//input[@name='javax.faces.ViewState']").get_attribute("value")

        # On récupère l'id du form (form:j_idtxxx)
        self._formId = driver.find_element_by_class_name("schedule").get_attribute("id")

        # On récupère le cookie
        cookies = driver.get_cookies()
        self._sessionId = ""

        # On garde l'ID de session
        for c in cookies:
            if c["name"] == "JSESSIONID":
                self._sessionId = c["value"]

        # On ferme le navigateur
        driver.close()

        return True
