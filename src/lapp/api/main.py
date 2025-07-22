from datetime import date
from pyexpat import model
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import random

from lapp.api.models import RandomRequest, UpdatebyIdRequest, NewElementRequest, UpdateScoreRequest, VocabularyDict, GrammarRuleDict, CalligraphyCharacterDict, ExerciseDict, UnitDict, LanguageDict
from lapp.dbms import find_by_pk, init_db, insert, modify, delete, generate_new_id
from lapp.tables import Language, Unit, Vocabulary, GrammarRule, CalligraphyCharacter, Exercise
from lapp.utils import update_score, orm_to_dict, str_to_modelclass
from sqlalchemy import func

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

    element_type = str_to_modelclass(data.element_id)

    element, _, _ = find_by_pk(session, element_type(id=data.element_id))

    for key, value in data.updates.items():
        setattr(element, key, value)
    
    modify(session, element)
    result = orm_to_dict(element)
    session.close()
    
    return result

@app.post("/new_element")
def new_element(data: NewElementRequest):
    # Initialise la base de données pour la langue spécifiée et crée une session
    _, session = init_db()

    # Récupère l'ID de l'unité au format "ZH_1"
    if data.element_type[0].lower() == "l":
        element = Language(**{k: v for k, v in data.element.model_dump().items() if k not in ("id")}, id=data.element.name[:2].upper())
    elif data.element_type[0].lower() == "u":
        language_id = data.element.language_id.upper()
        same_elements_in_unit = session.query(Unit).filter(Unit.language_id == language_id).all()
        n_elements_same_class = len(same_elements_in_unit)
        id = f"{language_id}_{n_elements_same_class}"
        element = Unit(
            **{k: v for k, v in data.element.model_dump().items() if k not in ("language_id")},
            language_id=language_id,
            id=id
        )
    else:
        unit_id = data.element.unit_id
        id = f"{unit_id}_{data.element_type[0].upper()}"
        model_class = str_to_modelclass(id)

        id += str(generate_new_id(session, unit_id=unit_id, model_class=model_class))

        element = model_class(
            **{k: v for k, v in data.element.model_dump().items() if k not in ("id", "unit_id")},
            id=id,
            unit_id=unit_id
        )

    insert(session, element)
    result = orm_to_dict(element)
    session.close()
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
def language_overview(language_id: str):
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
def unit_details(unit_id: str):
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

    exercise_count = {}
    for e in exercises:
        if e.exercise_type not in exercise_count:
            exercise_count[e.exercise_type] = 0
        exercise_count[e.exercise_type] += 1

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
            "items": [{"type": exercise_type, "count": count} for exercise_type, count in exercise_count.items()],
            "count": len(exercises)
        }
    }

    session.close()

    return result

@app.get("/{unit_id}/exercises_overview")
def exercises_overview(unit_id: str):
    _, session = init_db()

    exercises = session.query(Exercise).filter(Exercise.unit_id == unit_id).all()

    return [orm_to_dict(exercise) for exercise in exercises]

@app.get("/exercise/next/{ex_id}")
def next_exercise(ex_id: str):
    """
    Returns the next exercise for a given unit.
    
    Parameters:
        unit_id (str): The ID of the unit to fetch the next exercise for.
    
    Returns:
        dict: A dictionary representation of the next exercise, or an error message if not found.
    """
    _, session = init_db()
    unit_id = "_".join(ex_id.split("_")[:2])  # Extract the unit_id from the ex_id

    lowest_score = session.query(func.min(Exercise.score)).filter(Exercise.unit_id == unit_id).scalar()
    exercises = session.query(Exercise).filter(Exercise.id != ex_id).filter(Exercise.unit_id == unit_id, Exercise.score == lowest_score).all()

    if not exercises:
        session.close()
        return {"error": f"No exercises found for unit {unit_id}."}
    
    next_exercise = random.choice(exercises)
    
    result = orm_to_dict(next_exercise)
    
    session.close()

    return result["id"]