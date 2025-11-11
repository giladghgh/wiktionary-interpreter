import requests
from TranslationExceptions import *

from bs4 import BeautifulSoup





class Arabiciser:
    ISO = {
        "ar" : "Modern Standard Arabic",
        # "ara" : "Arabic",
        # "arb" : "Standard Arabic",
        "arz" : "Egyptian Arabic",
        "afb" : "Gulf Arabic",
        "acw" : "Hijazi Arabic",
        "ars" : "Najdi Arabic",
        "ajp" : "South Levantine Arabic",
        "apc" : "North Levantine Arabic",
        "ary" : "Moroccan Arabic",
        "acm" : "Iraqi Arabic",
        "arq" : "Algerian Arabic",
        "acx" : "Omani Arabic",
        "aeb" : "Tunisian Arabic",
        "ayl" : "Libyan Arabic",
        "shu" : "Chadian Arabic",
        "apd" : "Sudanese Arabic",
        "auz" : "Uzbeki Arabic",
    }

    PRIORITIES = [
        "ajp",          ### South Levantine
        # "apc",          ### North Levantine
    ]


    def __init__(self):
        self.urlb = "https://en.wiktionary.org"
        self.head = {"User-Agent":"WiktionaryTranslatorBot/0.1 (https://github.com/giladghgh;giladgurharush@gmail.com)"}

        self.lang_code = "ar"
        self.lang_name = "Arabic"


    def fetch(self , link):
        """Fetch valid page from Wiktionary."""

        reply = requests.get(
            url=link,
            headers=self.head
        )

        if reply.status_code != 200:
            raise NoWordException()

        return BeautifulSoup(reply.text,"html.parser")


    def trace(self , html):
        """Trace valid translation elements from page."""

        frame_navigations = []
        frame_suggestions = []
        for frame in html.find_all(
            name="div",
            attrs={"class":"pseudo NavFrame"}
        ):
            (frame_navigations,frame_suggestions)[frame.has_attr("id")].append(frame)

        frame_translations = {}
        for frame in html.find_all(
            name="table",
            attrs={"class":"translations"}
        ):
            for item in frame.find_all("li"):
                if item.find(lang=self.lang_code):
                    frame_translations[frame["data-gloss"]] = item
                    break

        return frame_translations , frame_navigations , frame_suggestions


    def parse(self , frame_elements):
        """Parse valid translations from their elements."""

        table = {}
        for sense,elem in frame_elements.items():
            table[sense] = {}

            for tag in elem.find_all("span", class_="Arab"):
                for code in self.ISO.keys():
                    if tag["lang"] == code:
                        table[sense].setdefault(code,[]).append((
                            tag.find("a").string,                   ### txl with ḥarakāt
                            self.urlb + tag.find("a")["href"],      ### hyperlink
                        ))
                        break

        return table


    def vouch(self , fusha):
        """Vouch priority dialect translation exists in their Fuṣḥā page."""

        translations_priority = {}
        for prior in self.PRIORITIES:
            for sense,gloss in fusha.items():
                for code,trans in gloss.items():
                    for tran,link in trans:
                        html = self.fetch(link)
                        if anchor := html.find("h2",string=self.ISO[prior]):
                            translations_priority.setdefault(sense,{})
                            translations_priority[sense].setdefault(prior,[]).append((
                                tran,                                                       ### txl with ḥarakāt
                                link.split("#")[0] + "#" + anchor.string.replace(" ","_")   ### re-anchored hyperlink
                            ))

        return translations_priority


    def translate(self , word):
        """Main method."""

        html = self.fetch(self.urlb + "/wiki/" + word)

        frame_txl , frame_nav , frame_sug = self.trace(html)

        # Find translations if on standalone page
        if not frame_txl:
            if not frame_nav:
                raise NoTranslationException()
            else:
                for nav in frame_nav:
                    html = self.fetch(self.urlb + nav.find("a")["href"].split("#")[0])

                    f_t , _ , f_s = self.trace(html)
                    frame_txl.update(f_t)
                    frame_sug.extend(f_s)

        translations = self.parse(frame_txl)

        # Impute priority translations if not found already
        fusha = {}
        for sense,gloss in translations.items():
            if set(gloss.keys()) - {"ar"}:          ### don't bother if only Fuṣḥā displayed, too costly
                for code,trans in gloss.items():
                    if code in self.PRIORITIES:
                        break
                    elif code == "ar":
                        # if
                        fusha[sense] = {code:trans}
                else:
                    continue
                break
            else:
                break
        else:
            for sense,gloss in self.vouch(fusha).items():
                for code,trans in gloss.items():
                    translations[sense][code] = trans

        suggestions = {}
        if frame_sug:
            for frame in frame_sug:
                suggestions[frame.find("a").string] = self.urlb + frame.find("a")["href"].split("#")[0]

        return translations , suggestions
