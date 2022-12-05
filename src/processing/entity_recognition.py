"""
Functions to perform Named Entity Recognition (NER)
"""
import spacy


class EntityRecognition:
    def __init__(self, data, column, scheme='en_core_web_sm'):
        self.texts = data[column]
        self.nlp = spacy.load(scheme)

    def get_gpe(self) -> list:
        """
        Extracts Geopolical Entity information
        """
        locations = []
        for text in self.texts:
            doc = self.nlp(text)
            locations.append(', '.join(list(set([ent.text for ent in doc.ents if ent.label_ in ['GPE']]))).lower())
        return locations
    
    def get_org(self) -> list:
        """
        Extracts Companies, agencies, institutions, etc
        """
        orgs = []
        for text in self.texts:
            doc = self.nlp(text)
            orgs.append(', '.join(list(set([ent.text for ent in doc.ents if ent.label_ in ['ORG']]))).lower())
        return orgs
    
    def get_person(self) -> list:
        """
        Extracts Companies, agencies, institutions, etc
        """
        persons = []
        for text in self.texts:
            doc = self.nlp(text)
            persons.append(', '.join(list(set([ent.text for ent in doc.ents if ent.label_ in ['PERSON']]))).lower())
        return persons
