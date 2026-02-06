import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask
from lapp.models.components.character import Character
from lapp.models.components.passage import Passage

from ..core.database import db_manager
from ..models.components.word import Word
from ..services import TTSService

logger = logging.getLogger(__name__)


def register_tts_tasks(scheduler: BackgroundScheduler, app: Flask):
    """
    Register TTS-related scheduled tasks.
    Uses interval-based scheduling since app doesn't run 24/7.
    
    Args:
        scheduler: APScheduler instance
        app: Flask app instance for accessing config
    """
    # Get TTS interval from config (default: 120 minutes = 2 hours)
    tts_interval = app.config.get('TTS_INTERVAL_MINUTES', 120)
    
    # Run TTS generation immediately on startup
    scheduler.add_job(
        func=generate_missing_component_audio,
        id='generate_missing_component_audio_startup',
        name='Generate missing audio for Components (startup)',
        replace_existing=True,
        args=[app]  # Pass app context to the task function
    )
    
    # Interval-based TTS generation
    scheduler.add_job(
        func=generate_missing_component_audio,
        trigger=IntervalTrigger(minutes=tts_interval),
        id='generate_missing_component_audio',
        name=f'Generate missing audio for Components (every {tts_interval} min)',
        replace_existing=True,
        args=[app]  # Pass app context to the task function
    )

    
    logger.info(f"✅ Scheduled job: generate_missing_component_audio (every {tts_interval} minutes)")

def generate_missing_component_audio(app: Flask):
    """
    Background task to generate audio for Components (Characters/Words/Passages) without audio files.
    """
    logger.info("🎵 Starting TTS generation task for Components...")
    
    with app.app_context():
        try:
            # Get config values from app
            media_root = app.config['MEDIA_ROOT']

            # Initialize TTS service with media_root (avoids app context issue)
            tts_service = TTSService(media_root=media_root)

            session = db_manager.get_session()
            
            # Query Characters without audio_files or with empty audio_files list
            characters_without_audio = session.query(Character).filter(
                (Character.audio_files == None) | (Character.audio_files == [])
            ).all()
            words_without_audio = session.query(Word).filter(
                (Word.audio_files == None) | (Word.audio_files == [])
            ).all()
            passages_without_audio = session.query(Passage).filter(
                (Passage.audio_files == None) | (Passage.audio_files == [])
            ).all()

            components_without_audio = characters_without_audio + words_without_audio + passages_without_audio
            
            total_components = len(components_without_audio)
            
            if total_components == 0:
                logger.info("✅ No components need audio generation")
                return
            
            logger.info(f"📋 Found {total_components} components without audio:")
            logger.info(f"   - Characters: {sum(1 for c in components_without_audio if isinstance(c, Character))}")
            logger.info(f"   - Words: {sum(1 for c in components_without_audio if isinstance(c, Word))}")
            logger.info(f"   - Passages: {sum(1 for c in components_without_audio if isinstance(c, Passage))}")
            
            success_count = 0
            error_count = 0
            
            for component in components_without_audio:
                try:
                    # Generate audio using TTS service

                    if isinstance(component, Character):
                        text = getattr(component, 'character', None)
                    elif isinstance(component, Word):
                        text = getattr(component, 'word', None)
                    elif isinstance(component, Passage):
                        text = getattr(component, 'text', None)

                    if not text:
                        logger.warning(f"⚠️  Component ID {component.id} has no text to generate audio from")
                        continue

                    relative_path = tts_service.generate_audio(text=text)
                        
                    # Update component with audio path
                    component.audio_files = [relative_path]
                    db_manager.modify(component, session=session)
                    session.commit()
                    
                    success_count += 1
                    logger.info(f"✅ Generated audio for component '{text}' (ID: {component.id})")
                    
                except Exception as e:
                    error_count += 1
                    session.rollback()
                    logger.error(f"❌ Failed to generate audio for component '{text}' (ID: {component.id}): {e}")
                    continue
            
            logger.info(f"🎵 TTS generation task completed: {success_count} succeeded, {error_count} failed")
        except Exception as e:
            logger.error(f"❌ TTS generation task failed: {e}", exc_info=True)
            if session:
                session.rollback()
        finally:
            if session:
                session.close()


def generate_audio_for_character_id(character_id: str) -> bool:
    """
    Generate audio for a specific character by ID.
    
    Args:
        character_id: The ID of the character
        
    Returns:
        True if successful, False otherwise
    """
    tts_service = TTSService()
    session = None
    
    try:
        session = db_manager.get_session()
        
        character = db_manager.get_by_id(Character, character_id, session=session)
        
        if not character:
            logger.error(f"Character with ID {character_id} not found")
            return False
        
        # Generate audio
        relative_path = tts_service.generate_audio(text=character.character)
        
        # Update character
        character.audio_files = [relative_path]
        session.commit()
        
        logger.info(f"✅ Generated audio for character '{character.character}' (ID: {character_id})")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to generate audio for character ID {character_id}: {e}")
        if session:
            session.rollback()
        return False
    finally:
        if session:
            session.close()


def generate_audio_for_word_id(word_id: str) -> bool:
    """
    Generate audio for a specific word by ID.
    
    Args:
        word_id: The ID of the word
        
    Returns:
        True if successful, False otherwise
    """
    tts_service = TTSService()
    session = None
    
    try:
        session = db_manager.get_session()
        
        word = db_manager.get_by_id(Word, word_id, session=session)
        
        if not word:
            logger.error(f"Word with ID {word_id} not found")
            return False
        
        # Generate audio
        relative_path = tts_service.generate_audio(text=word.word)
        
        # Update word
        word.audio_files = [relative_path]
        session.commit()
        
        logger.info(f"✅ Generated audio for word '{word.word}' (ID: {word_id})")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to generate audio for word ID {word_id}: {e}")
        if session:
            session.rollback()
        return False
    finally:
        if session:
            session.close()


def generate_audio_for_passage_id(passage_id: str) -> bool:
    """
    Generate audio for a specific passage by ID.
    
    Args:
        passage_id: The ID of the passage
        
    Returns:
        True if successful, False otherwise
    """
    tts_service = TTSService()
    session = None
    
    try:
        session = db_manager.get_session()
        
        passage = db_manager.get_by_id(Passage, passage_id, session=session)
        
        if not passage:
            logger.error(f"Passage with ID {passage_id} not found")
            return False
        
        # Generate audio
        relative_path = tts_service.generate_audio(text=passage.passage)
        
        # Update passage
        passage.audio_files = [relative_path]
        session.commit()
        
        logger.info(f"✅ Generated audio for passage '{passage.passage}' (ID: {passage_id})")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to generate audio for passage ID {passage_id}: {e}")
        if session:
            session.rollback()
        return False
    finally:
        if session:
            session.close()