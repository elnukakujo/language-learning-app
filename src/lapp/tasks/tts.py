import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask
logger = logging.getLogger(__name__)

from ..core.database import db_manager
from ..services import TTSService, PassageService, WordService, CharacterService
from ..schemas.components import CharacterDict, PassageDict, WordDict
from ..models.components import Passage, Character, Word

passage_service = PassageService()
word_service = WordService()
character_service = CharacterService()

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
                    component_id = component.id

                    updated_component = component.to_dict(include_relations=False)
                    updated_component.pop('id', None)  # Remove ID from dict since it's not updatable
                    updated_component["audio_files"] = [relative_path]  # Ensure audio_files is included in the update data

                    # Update component with audio path
                    if isinstance(component, Character):
                        result = character_service.update(character_id=component_id, data=CharacterDict(**updated_component), session=session)
                    elif isinstance(component, Word):
                        result = word_service.update(word_id=component_id, data=WordDict(**updated_component), session=session)
                    elif isinstance(component, Passage):
                        result = passage_service.update(passage_id=component_id, data=PassageDict(**updated_component), session=session)
                    
                    if not result:
                        logger.warning(f"⚠️  Failed to update component '{text}' (ID: {component.id})")
                        continue

                    if result.audio_files != [relative_path]:
                        logger.warning(f"⚠️  Audio path mismatch for component '{text}' (ID: {component.id}) - expected: {relative_path}, got: {result.audio_files}")
                        continue

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
