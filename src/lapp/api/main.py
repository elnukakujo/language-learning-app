from datetime import date
import json
import re
from fastapi import FastAPI
from pydantic import BaseModel
import random
from typing import Optional, Type

from lapp.dbms import find_by_pk, init_db, insert, modify, delete, find_by_attr
from lapp.tables import Unit, Vocabulary, GrammarRule, CalligraphyCharacter, Exercise
from lapp.utils import update_score, orm_to_dict, str_to_modelclass
from sqlalchemy import Null, table

app = FastAPI()

class RandomRequest(BaseModel):
    language_id: str
    unit_id: int
    type: str

class UpdatebyIdRequest(BaseModel):
    element_id: str
    updates: dict

# Pour element_type = "voc" (vocabulaire) :
#   - word, translation, phonetic, example_sentence, type
#
# Pour element_type = "gram" (règle de grammaire) :
#   - title, explanation
#
# Pour element_type = "char" (caractère calligraphié) :
#   - character, translation, components
#
# Pour element_type = "ex" (exercice) :
#   - exercise_type, question, support, answer
class NewElementRequest(BaseModel):
    language_id: str
    unit_id: int
    element_type: str  # e.g. "voc", "g", "char", "ex"
    word: Optional[str] = None
    translation: Optional[str] = None
    phonetic: Optional[str] = None
    example_sentence: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    explanation: Optional[str] = None
    character: Optional[str] = None
    components: Optional[str] = None
    exercise_type: Optional[str] = None
    question: Optional[str] = None
    support: Optional[str] = None
    answer: Optional[str] = None

class UpdateScoreRequest(BaseModel):
    element_id: str
    success: bool

@app.post("/random")
def get_random(data: RandomRequest):
    """
    Fetches a random element from the database using the specified language and unit filters.
    Parameters:
        data (RandomRequest): An object containing the following attributes:
            - language_id (str): Identifier for the language used to initialize the database.
                - Should be a string that matches the language database name (e.g., "en", "de").
            - type (str): The type of terminology to query. Should be a key in the type_terminology mapping.
                - Valid values are "voc", "gram", "char", or "ex" corresponding to Vocabulary, GrammarRule, CalligraphyCharacter, or Exercise respectively.
            - unit_id (str or int): Identifier for the unit, used alongside language_id to filter elements.
                - Must be an integer from 0 to n, where n is the number of units in the database for the specified language.

    Returns:
        dict: A dictionary representation of the randomly selected element converted via orm_to_dict.
              If no element is found that matches the criteria, returns a dictionary with an 'error' key.
    Notes:
        - The function initializes a database session using init_db() with the provided language_id.
        - It builds a query on the type-specific table (from type_terminology) filtering
          by a compound unit_id formed by concatenating the uppercase language_id with the unit_id.
        - The session is closed after the query is executed.
        - If the query yields no results, an error message is returned.
    """

    _, session = init_db(data.language_id)

    table_class = str_to_modelclass(data.type)
    if table_class is None:
        session.close()
        return {"error": "Invalid type provided."}
    
    unit_id = data.language_id.upper() + "_" + str(data.unit_id)

    elements = session.query(table_class).filter(table_class.unit_id == unit_id).all()
    session.close()

    if not elements:
        return {"error": "No elements found for the specified type and unit."}
    element = random.choice(elements)
    return orm_to_dict(element)

@app.post("/find_by_id")
def find_by_id(element_id: str):
    """
    Finds an element in the database by its ID.
    
    Parameters:
        element_id (str): The ID of the element to find.
    
    Returns:
        dict: A dictionary representation of the found element, or an error message if not found.
    """
    language_id = element_id.split("_")[0].lower()
    suffix = element_id.split("_")[-1].lower()[0]

    _, session = init_db(language_id)

    element_type = str_to_modelclass(suffix)

    element, _, _ = find_by_pk(session, element_type(learn_id=element_id))
        
    if not element:
        session.close()
        return {"error": "Element not found."}
    
    result = orm_to_dict(element)
    session.close()
    
    return result

@app.post("/delete_by_id")
def delete_by_id(element_id: str):
    """
    Deletes an element in the database by its ID.
    
    Parameters:
        element_id (str): The ID of the element to delete.
    
    Returns:
        dict: A dictionary representation of the deleted element, or an error message if not found.
    """

    language_id = element_id.split("_")[0].lower()
    suffix = element_id.split("_")[-1].lower()[0]

    _, session = init_db(language_id)

    element_type = str_to_modelclass(suffix)

    element, _, _ = find_by_pk(session, element_type(learn_id=element_id))
    
    if not element:
        session.close()
        return {"error": "Element not found."}
    
    delete(session, element)
    result = orm_to_dict(element)
    session.close()
    
    return result

@app.post("/update_by_id")
def update_by_id(data: UpdatebyIdRequest):
    """
    Updates an element in the database by its ID with the provided updates.
    
    Parameters:
        data (UpdatebyIdRequest): An object containing:
            - element_id (str): The ID of the element to update.
            - updates (dict): A dictionary of attributes to update and their new values.
    
    Returns:
        dict: A dictionary representation of the updated element, or an error message if not found.
    """
    language_id = data.element_id.split("_")[0].lower()
    suffix = data.element_id.split("_")[-1].lower()[0]

    _, session = init_db(language_id)

    element_type = str_to_modelclass(suffix)

    element, _, _ = find_by_pk(session, element_type(learn_id=data.element_id))

    for key, value in data.updates.items():
        setattr(element, key, value)
    
    modify(session, element)
    result = orm_to_dict(element)
    session.close()
    
    return result

# Dictionnaire d'alias qui associe chaque type d'élément à ses abréviations textuelles
alias_map = {
    Vocabulary: ["voc", "v"],
    GrammarRule: ["gram", "g"],
    CalligraphyCharacter: ["char", "c"],
    Exercise: ["ex", "e"]
}
# Inverse le dictionnaire pour passer d'une abréviation à un type d'élément directement
alias_lookup = {alias: model for model, aliases in alias_map.items() for alias in aliases}

@app.post("/new_element")
def new_element(data: NewElementRequest):
    """ 
    Create a new learning element (vocabulary, grammar rule, calligraphy character, or exercise).

    Required fields depend on the 'element_type' value:

    - "voc" (Vocabulary): word, translation, phonetic, example_sentence, type
    - "gram" (Grammar Rule): title, explanation
    - "char" (Calligraphy Character): character, translation, components
    - "ex" (Exercise): exercise_type, question, support, answer
    """

    # Initialise la base de données pour la langue spécifiée et crée une session
    _, session = init_db(data.language_id)

    # Construit l'identifiant de l'unité au format "ZH_1"
    unit_str_id = f"{data.language_id.upper()}_{data.unit_id}"

   # Récupère la classe du modèle SQLAlchemy correspondant à l'alias fourni
    model_class: Type = alias_lookup.get(data.element_type.lower())
    if not model_class:
        return {"error": f"Unknown element type: {data.element_type}"}

    # Cherche les IDs existants pour ce type d'élément dans l'unité donnée
    learn_ids = session.query(model_class.learn_id).filter(model_class.unit_id == unit_str_id).all()
    # Extrait le numéro le plus élevé à la fin de chaque ID pour calculer le prochain
    max_id = max([int(re.search(r"\\d+$", learn_id[0]).group()) for learn_id in learn_ids if re.search(r"\\d+$", learn_id[0])],default=0)
    # Construit le nouvel identifiant pour l'élément, ex: "ZH_1_V1"
    learn_id = f"{unit_str_id}_{data.element_type.upper()}{max_id + 1}"

    # Prépare les données de l'objet à insérer selon le type d'élément
    element_data = {
        Vocabulary: dict(learn_id=learn_id, unit_id=unit_str_id, word=data.word, translation=data.translation,
                         phonetic=data.phonetic, example_sentence=data.example_sentence, type=data.type,
                         score=0, last_seen=date.today()),

        GrammarRule: dict(learn_id=learn_id, unit_id=unit_str_id, title=data.title, explanation=data.explanation,
                          score=0, last_seen=date.today()),

        CalligraphyCharacter: dict(learn_id=learn_id, unit_id=unit_str_id, character=data.character,
                                   translation=data.translation, components=data.components, score=0,
                                   last_seen=date.today()),

        Exercise: dict(learn_id=learn_id, unit_id=unit_str_id, exercise_type=data.exercise_type,
                       question=data.question, support=data.support, answer=data.answer, score=0,
                       last_seen=date.today())
    }

    # Crée une instance de l'objet basé sur le modèle et les données
    new_object = model_class(**element_data[model_class])
    # Insère l'objet dans la base de données
    insert(session, new_object)
    # Convertit l'objet en dictionnaire pour l'API
    result = orm_to_dict(new_object)
    # Ferme la session SQL
    session.close()
    # Retourne le résultat au client
    return result


@app.post("/update_score")
def score_update(data: UpdateScoreRequest):
    """
    Updates the score of an element in the database based on its success or failure.
    
    Parameters:
        data (UpdateScoreRequest): An object containing:
            - element_id (str): The ID of the element to update.
            - success (bool): Whether the update is a success or failure.
    
    Returns:
        dict: A dictionary representation of the updated element, or an error message if not found.
    """
    language_id = data.element_id.split("_")[0].lower()
    suffix = data.element_id.split("_")[-1].lower()[0]

    _, session = init_db(language_id)

    element_type = str_to_modelclass(suffix)

    element, _, _ = find_by_pk(session, element_type(learn_id=data.element_id))

    if not element:
        session.close()
        return {"error": "Element not found."}

    new_score = update_score(score=element.score, last_seen=element.last_seen, success=data.success)
    print(new_score)

    updated_element = element_type(
        learn_id=element.learn_id,
        score=new_score,
        last_seen=date.today()
    )

    updated_element = modify(session, updated_element)
    
    result = orm_to_dict(updated_element)
    session.close()
    
    return result

@app.get("/available_languages")
def available_languages():
    """
    Returns a list of available languages in the database.
    
    Returns:
        list: A list of dictionaries, each containing the language ID and name.
    """
    with open("db/languages.json", "r", encoding="utf-8") as f:
        languages = json.load(f)
    return languages