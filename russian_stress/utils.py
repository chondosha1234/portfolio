import requests
from bs4 import BeautifulSoup
import re

def add_stress(text):

    # seperate out words and punctuation
    word_list = re.findall(r'\w+|[^\w\s]+', text)
    punctuation_list = [p for p in word_list if not p.isalnum()]
    result = []

    for word in word_list:
        if not re.match(r'\W', word):   # if it is a word
            found_word = find_word_on_wiktionary(word)
            result.append(found_word)
        else:
            result.append(word) #just punctuation

    # this retains spacing, but does not put a space before punctuation marks
    return ''.join(
        f'{w} ' if i < len(result)-1 and re.match(r'\w+', result[i+1]) else w for i, w in enumerate(result)
    )


def find_word_on_wiktionary(word):
    url = "https://wiktionary.org/wiki/" + word
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    russian_section = soup.find("span", {"id": "Russian"})
    if russian_section:
        # if the word has multiple spellings / meanings/ stress patterns -- return without stress
        if len(russian_section.find_all_next("strong", {"class": "Cyrl headword", "lang": "ru"})) > 1:
            return word

        rus_word = russian_section.find_next("strong", {"class": "Cyrl headword", "lang": "ru"})
        if rus_word:
            return rus_word.text
        else:
            return word # russian word not found, use original
    else:
        # if a normal word is capitalized, such as at beginning of sentence, it won't return proper result
        if word[0].isalpha() and word[0].isupper():
            word = word.lower()
            found = find_word_on_wiktionary(word)
            return found.capitalize()
        else:
            return word
