from datetime import date
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
import random
from fastapi import UploadFile, File, HTTPException

from lapp.api.models import UpdatebyIdRequest, NewElementRequest, UpdateScoreRequest
from lapp.dbms import find_by_pk, init_db, insert, modify, delete, generate_new_id
from lapp.tables import Language, Unit, Vocabulary, GrammarRule, CalligraphyCharacter, Exercise
from lapp.utils import update_score, orm_to_dict, str_to_modelclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Or specify your frontend origin like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Or ["POST"] if you want to restrict
    allow_headers=["*"],
)


REPO_ROOT = Path(__file__).parent.parent.parent.parent
app.mount("/assets", StaticFiles(directory=REPO_ROOT / "assets"), name="assets")

IMAGE_DIR = REPO_ROOT / "assets" / "images"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/next/{element_id}")
def get_random(element_id: str):
    _, session = init_db()
    unit_id = "_".join(element_id.split("_")[:2])  # Extract the unit_id from the element_id

    element_type = str_to_modelclass(element_id)

    lowest_score = session.query(func.min(element_type.score)).filter(element_type.unit_id == unit_id).scalar()
    threshold = 2  # adjust threshold as needed
    elements = session.query(element_type).filter(
        element_type.id != element_id,
        element_type.unit_id == unit_id,
        element_type.score >= lowest_score,
        element_type.score <= lowest_score + threshold
    ).all()

    if not elements:
        elements = session.query(element_type).filter(element_type.unit_id == unit_id).filter(element_type.id != element_id).all()

    next_element = random.choice(elements)
    logger.info(f"Found next element for element_id: {element_id} in unit_id: {unit_id}: {next_element.id}")

    result = orm_to_dict(next_element)

    session.close()

    return result["id"]

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

    if "unit_id" in data.updates and data.updates["unit_id"] != element.unit_id:
        data.updates["id"] = f'{data.updates["unit_id"]}_{element_type.__name__[0].upper()}'+str(generate_new_id(session, unit_id=data.updates["unit_id"], model_class=element_type))

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
    Updates the score of an element, its unit as well as the language in the database based on its success or failure.
    
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
    logger.info(f"Updating score for element {data.element_id} of type {element_type.__name__}: new score is {new_score}")

    if element_type == Exercise:
        associated_voc = session.query(Vocabulary).filter(Vocabulary.id.in_(element.associated_to.get("vocabulary", []))).all()
        associated_char = session.query(CalligraphyCharacter).filter(CalligraphyCharacter.id.in_(element.associated_to.get("characters", []))).all()
        associated_gram = session.query(GrammarRule).filter(GrammarRule.id.in_(element.associated_to.get("grammar", []))).all()

        for associated_element in associated_voc + associated_char + associated_gram:
            associated_element.score = update_score(score=associated_element.score, last_seen=associated_element.last_seen, success=data.success)
            modify(session, associated_element)

        # In case an associated element has been deleted, we need to update the associated_to field
        if len(associated_voc) < len(element.associated_to.get("vocabulary", [])) or len(associated_char) < len(element.associated_to.get("characters", [])) or len(associated_gram) < len(element.associated_to.get("grammar", [])):
            updated_element = element_type(
                id=element.id,
                score=new_score,
                last_seen=date.today(),
                associated_to= {
                    "vocabulary": [v.id for v in associated_voc],
                    "characters": [c.id for c in associated_char],
                    "grammar": [g.id for g in associated_gram]
                }
            )
        else:
            updated_element = element_type(
                id=element.id,
                score=new_score,
                last_seen=date.today()
            )
    else:
        updated_element = element_type(
            id=element.id,
            score=new_score,
            last_seen=date.today()
        )

    updated_element = modify(session, updated_element)

    average_vocab_score = session.query(func.avg(Vocabulary.score)).filter(Vocabulary.unit_id == updated_element.unit_id).scalar()
    average_char_score = session.query(func.avg(CalligraphyCharacter.score)).filter(CalligraphyCharacter.unit_id == updated_element.unit_id).scalar()
    average_exercise_score = session.query(func.avg(Exercise.score)).filter(Exercise.unit_id == updated_element.unit_id).scalar()

    scores = [s for s in (average_vocab_score, average_char_score, average_exercise_score) if s is not None]
    average_score = sum(scores) / len(scores) if scores else None

    if average_score is None:
        result = orm_to_dict(updated_element)
        session.close()
        return result
    
    updated_unit = Unit(
        id = updated_element.unit_id,
        score = average_score,
        last_seen = date.today()
    )
    updated_unit = modify(session, updated_unit)

    average_unit_score = session.query(func.avg(Unit.score)).filter(Unit.language_id == updated_unit.language_id).scalar()

    if average_unit_score is None:
        result = orm_to_dict(updated_element)
        session.close()
        return result
    
    updated_language = Language(
        id = updated_unit.language_id,
        score = average_unit_score,
        last_seen = date.today()
    )

    updated_language = modify(session, updated_language)

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

    exercise_types = {}
    for e in exercises:
        if e.exercise_type not in exercise_types:
            exercise_types[e.exercise_type] = {"count": 0, "score": 0}
        exercise_types[e.exercise_type]["count"] += 1
        exercise_types[e.exercise_type]["score"] += e.score

    for _, data in exercise_types.items():
        data["score"] /= data["count"]

    result = {
        **result,
        "vocabulary": {
            "items": [{"id": v.id, "word": v.word, "translation": v.translation, "score": v.score} for v in vocabularies],
            "count": len(vocabularies)
        },
        "grammar": {
            "items": [{"id": g.id, "title": g.title, "score": g.score} for g in grammar],
            "count": len(grammar)
        },
        "characters": {
            "items": [{"id": c.id, "character": c.character, "meaning": c.meaning, "score": c.score} for c in characters],
            "count": len(characters)
        },
        "exercises": {
            "items": [{"type": exercise_type, "count": data["count"], "score": data["score"]} for exercise_type, data in exercise_types.items()],
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

@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Generate unique filename with original extension
        file_ext = file.filename.split('.')[-1]
        file_name = f"{file.filename.split('.')[0]}.{file_ext}"
        file_path = IMAGE_DIR / file_name
        
        # Save the file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {
            "file_url": f"/assets/images/{file_name}",  # URL path
            "file_path": str(file_path),  # Physical path (for reference)
            "message": "Image uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))