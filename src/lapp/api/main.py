from datetime import date
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import random
from typing import Type

from lapp.api.models import RandomRequest, UpdatebyIdRequest, NewElementRequest, UpdateScoreRequest
from lapp.dbms import find_by_pk, init_db, insert, modify, delete
from lapp.tables import Language, Unit, Vocabulary, GrammarRule, CalligraphyCharacter, Exercise
from lapp.utils import update_score, orm_to_dict, str_to_modelclass

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Or specify your frontend origin like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Or ["POST"] if you want to restrict
    allow_headers=["*"],
)

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

@app.get("/find_by_id/{element_id}")
def find_by_id(element_id: str):
    """
    Finds an element in the database by its ID.
    
    Parameters:
        element_id (str): The ID of the element to find.
    
    Returns:
        dict: A dictionary representation of the found element, or an error message if not found.
    """
    _, session = init_db()

    element_type = str_to_modelclass(element_id)

    element, _, _ = find_by_pk(session, element_type(id=element_id))
        
    if not element:
        session.close()
        return {"error": "Element not found."}
    
    result = orm_to_dict(element)
    session.close()
    
    return result

@app.get("/delete_by_id/{element_id}")
def delete_by_id(element_id: str):
    """
    Deletes an element in the database by its ID.
    
    Parameters:
        element_id (str): The ID of the element to delete.
    
    Returns:
        dict: A dictionary representation of the deleted element, or an error message if not found.
    """
    _, session = init_db()

    element_type = str_to_modelclass(element_id=element_id)

    element, _, _ = find_by_pk(session, element_type(id=element_id))
    
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
            - id (str): The ID of the element to update.
            - updates (dict): A dictionary of attributes to update and their new values.
    
    Returns:
        dict: A dictionary representation of the updated element, or an error message if not found.
    """
    _, session = init_db()
    print(data)

    element_type = str_to_modelclass(data.element_id)
    print(element_type)

    element, _, _ = find_by_pk(session, element_type(id=data.element_id))
    print(element)

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
    _, session = init_db()

    # Construit l'identifiant de l'unité au format "ZH_1"
    unit_str_id = f"{data.language_id.upper()}_{data.unit_id}"

   # Récupère la classe du modèle SQLAlchemy correspondant à l'alias fourni
    model_class: Type = alias_lookup.get(data.element_type.lower())
    if not model_class:
        return {"error": f"Unknown element type: {data.element_type}"}

    # Cherche les IDs existants pour ce type d'élément dans l'unité donnée
    ids = session.query(model_class.id).filter(model_class.unit_id == unit_str_id).all()
    # Extrait le numéro le plus élevé à la fin de chaque ID pour calculer le prochain
    max_id = max([int(re.search(r"\\d+$", id[0]).group()) for id in ids if re.search(r"\\d+$", id[0])],default=0)
    # Construit le nouvel identifiant pour l'élément, ex: "ZH_1_V1"
    id = f"{unit_str_id}_{data.element_type.upper()}{max_id + 1}"

    # Prépare les données de l'objet à insérer selon le type d'élément
    element_data = {
        Vocabulary: dict(id=id, unit_id=unit_str_id, word=data.word, translation=data.translation,
                         phonetic=data.phonetic, example_sentence=data.example_sentence, type=data.type,
                         score=0, last_seen=date.today()),

        GrammarRule: dict(id=id, unit_id=unit_str_id, title=data.title, explanation=data.explanation,
                          score=0, last_seen=date.today()),

        CalligraphyCharacter: dict(id=id, unit_id=unit_str_id, character=data.character,
                                   translation=data.translation, components=data.components, score=0,
                                   last_seen=date.today()),

        Exercise: dict(id=id, unit_id=unit_str_id, exercise_type=data.exercise_type,
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
    _, session = init_db()

    element_type = str_to_modelclass(element_id=data.element_id)

    element, _, _ = find_by_pk(session, element_type(id=data.element_id))

    if not element:
        session.close()
        return {"error": "Element not found."}

    new_score = update_score(score=element.score, last_seen=element.last_seen, success=data.success)
    print(new_score)

    updated_element = element_type(
        id=element.id,
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
    _, session = init_db()

    languages = session.query(Language).all()
    
    if not languages:
        session.close()
        return {"error": "No languages found in the database."}
    
    dict_languages = []
    for language in languages:
        dict_languages.append(orm_to_dict(language))

    session.close()

    return dict_languages

@app.get("/units/{language_id}")
def units(language_id: str):
    """
    Returns a list of available units for a given language.
    
    Parameters:
        language_id (str): The ID of the language to fetch units for.
    
    Returns:
        list: A list of dictionaries, each containing the unit ID and title.
    """
    _, session = init_db()

    units = session.query(Unit).filter(Unit.language_id == language_id).all()
    
    if not units:
        session.close()
        return {"error": f"No units found for language {language_id}."}
    
    dict_units = [orm_to_dict(unit) for unit in units]
    
    session.close()

    return dict_units

@app.get("/unit/{unit_id}")
def unit(unit_id: str):
    """
    Returns a specific unit for a given language.
    
    Parameters:
        unit_id (str): The ID of the unit to fetch.
    
    Returns:
        dict: A dictionary representation of the unit, or an error message if not found.
    """
    _, session = init_db()

    unit = session.query(Unit).filter(Unit.id == unit_id).first()
    
    if not unit:
        session.close()
        return {"error": f"Unit {unit_id} not found."}

    result = orm_to_dict(unit)

    vocabularies = session.query(Vocabulary).filter(Vocabulary.unit_id == unit.id).all()
    grammar = session.query(GrammarRule).filter(GrammarRule.unit_id == unit.id).all()
    characters = session.query(CalligraphyCharacter).filter(CalligraphyCharacter.unit_id == unit.id).all()
    exercises = session.query(Exercise).filter(Exercise.unit_id == unit.id).all()

    result = {
        **result,
        "vocabulary": {
            "items": [{"id": v.id, "word": v.word, "translation": v.translation} for v in vocabularies],
            "count": len(vocabularies)
        },
        "grammar": {
            "items": [{"id": g.id, "title": g.title} for g in grammar],
            "count": len(grammar)
        },
        "characters": {
            "items": [{"id": c.id, "character": c.character, "meaning": c.meaning} for c in characters],
            "count": len(characters)
        },
        "exercises": {
            "items": [{"type": e.exercise_type} for e in exercises],
            "count": len(exercises)
        }
    }

    session.close()

    return result