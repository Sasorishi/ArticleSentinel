import ScraperController
import sys
from datetime import datetime

def main():
    print('[Init] Article Sentinel')
    # url = 'https://www.ilo.org/dyn/normlex/en/f?p=NORMLEXPUB:13100:0::NO::P13100_COMMENT_ID,P13100_COUNTRY_ID:4322614,103004'
    url = input("Veuillez entrer l'URL du site que vous souhaitez scraper : ")
    keywords = input("Veuillez entrer les mots-clés que vous souhaitez rechercher (séparés par des virgules) : ").split(",")

    specific_keywords_input = input("Veuillez entrer les mots-clés spécifiques dans les URIs (séparés par des virgules) : ")
    specific_keywords = specific_keywords_input.split(",") if specific_keywords_input else None

    # Saisie de la condition pour specific_keywords
    specific_condition_choice = input("Veuillez choisir 'any' ou 'all' pour la condition des mots-clés spécifiques : ")
    
    excluded_keywords_input = input("Veuillez entrer les mots-clés à exclure dans les URIs (séparés par des virgules) : ")
    excluded_keywords = excluded_keywords_input.split(",") if excluded_keywords_input else None

    # Saisie de la condition pour excluded_keywords
    excluded_condition_choice = input("Veuillez choisir 'any' ou 'all' pour la condition des mots-clés exclus : ")
    
    visited_urls = set()  # Pour garder une trace des URLs visitées

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    condition_suffix_specific = f"_{specific_condition_choice}" if specific_condition_choice else ""
    condition_suffix_excluded = f"_{excluded_condition_choice}" if excluded_condition_choice else ""

    result_file = f"{current_datetime}_results{condition_suffix_specific}{condition_suffix_excluded}.txt"

    ScraperController.scrape_page(url, visited_urls, keywords, specific_keywords=specific_keywords, excluded_keywords=excluded_keywords, result_file=result_file, specific_condition_choice=specific_condition_choice, excluded_condition_choice=excluded_condition_choice)

if __name__ == "__main__":
    main()
