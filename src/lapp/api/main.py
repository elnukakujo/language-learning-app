from datetime import date
from hmac import new
import re
from fastapi import FastAPI
from pydantic import BaseModel
import random

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

class NewVocabularyRequest(BaseModel):
    language_id: str
    unit_id: int
    word: str
    translation: str
    phonetic: str = Null
    example_sentence: str = Null
    type: str = Null

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

@app.post("/new_vocabulary")
def new_vocabulary(data: NewVocabularyRequest):
    """
    Adds a new vocabulary entry to the database.
    
    Parameters:
        data (NewVocabularyRequest): An object containing:
            - language_id (str): Identifier for the language used to initialize the database.
            - unit_id (int): Identifier for the unit, used alongside language_id to filter elements.
            - word (str): The vocabulary word to add.
            - translation (str): The translation of the vocabulary word.
            - phonetic (str, optional): Phonetic representation of the word. Defaults to None.
            - example_sentence (str, optional): Example sentence using the word. Defaults to None.
            - type (str, optional): Type of vocabulary. Defaults to None.
    
    Returns:
        dict: A dictionary representation of the newly added vocabulary entry.
    """
    _, session = init_db(data.language_id)

    unit_id = data.language_id.upper() + "_" + str(data.unit_id)

    unit_learn_ids = session.query(Vocabulary.learn_id).filter(Vocabulary.unit_id == unit_id).all()

    max_id = max(
        int(re.search(r'\d+$', learn_id[0]).group()) for learn_id in unit_learn_ids if re.search(r'\d+$', learn_id[0])
    )

    new_voc = Vocabulary(
        unit_id=unit_id,
        learn_id=f"{data.language_id.upper()}_{data.unit_id}_V{max_id + 1}",
        word=data.word,
        translation=data.translation,
        phonetic=data.phonetic,
        example_sentence=data.example_sentence,
        type=data.type,
        score=0.0,
        last_seen=date.today()
    )

    insert(session, new_voc)
    
    result = orm_to_dict(new_voc)
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