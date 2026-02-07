import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask

from ..core.database import db_manager
from ..models import Grammar, Vocabulary, Calligraphy
from ..schemas import GrammarDict, CalligraphyDict, VocabularyDict
from ..services import TextGeneratorService, GrammarService, VocabularyService, CalligraphyService

logger = logging.getLogger(__name__)

def register_text_gen_tasks(scheduler: BackgroundScheduler, app: Flask):
    """
    Register Text Generation-related scheduled tasks.
    Uses interval-based scheduling since app doesn't run 24/7.
    
    Args:
        scheduler: APScheduler instance
        app: Flask app instance for accessing config
    """
    # Get Text Generation interval from config (default: 120 minutes = 2 hours)
    text_gen_interval = app.config.get('TEXT_GEN_INTERVAL_MINUTES', 120)
    
    # Run Text Generation immediately on startup
    scheduler.add_job(
        func=generate_missing_texts,
        id='generate_missing_texts_startup',
        name='Generate missing texts (startup)',
        replace_existing=True
    )
    
    # Interval-based Text Generation
    scheduler.add_job(
        func=generate_missing_texts,
        trigger=IntervalTrigger(minutes=text_gen_interval),
        id='generate_missing_texts',
        name=f'Generate missing texts (every {text_gen_interval} min)',
        replace_existing=True
    )

    logger.info(f"✅ Scheduled job: generate_missing_texts (every {text_gen_interval} minutes)")

def generate_missing_texts():
    """
    Background task to generate learnable sentences for Grammars.
    """
    logger.info("🔄 Starting Text Generation task: generate_missing_texts")
    
    try:
        # Initialize services
        text_gen_service = TextGeneratorService()
        grammar_service = GrammarService()
        vocabulary_service = VocabularyService()
        calligraphy_service = CalligraphyService()

        calligraphies_without_words: list[Calligraphy] = db_manager.find_all(
            model_class=Calligraphy,
            filters={"example_word": None}
        )

        vocabularies_without_sentences: list[Vocabulary] = db_manager.find_all(
            model_class=Vocabulary,
            filters = {"example_sentences": None}
        )
        
        grammars_without_sentences: list[Grammar] = db_manager.find_all(
            model_class=Grammar,
            filters={"learnable_sentences": None}
        )

        features_without_texts = calligraphies_without_words + vocabularies_without_sentences + grammars_without_sentences
        
        total_features = len(features_without_texts)
        
        if total_features == 0:
            logger.info("✅ No feature need text generation")
            return
        
        logger.info(f"📋 Found {total_features} features without texts:")
        logger.info(f"   - {len(calligraphies_without_words)} Calligraphies without example words")
        logger.info(f"   - {len(vocabularies_without_sentences)} Vocabularies without example sentences")
        logger.info(f"   - {len(grammars_without_sentences)} Grammars without learnable sentences")
        
        success_count = 0
        error_count = 0
        
        for feature in features_without_texts:
            try:
                # Generate audio using TTS service
                if isinstance(feature, Calligraphy):
                    text = feature.character.character
                    generated_text = text_gen_service.generate_example_word(text)
                elif isinstance(feature, Vocabulary):
                    text = feature.word.word
                    generated_text = text_gen_service.generate_example_sentence(text)
                elif isinstance(feature, Grammar):
                    text = f" #{feature.title}\n\n{feature.explanation}"
                    generated_text = text_gen_service.generate_learnable_sentence(text)
                else:
                    logger.warning(f"⚠️  Unknown feature type for ID {feature.id}, skipping")
                    continue       
                    
                if not generated_text or not generated_text.strip():
                    logger.warning(f"⚠️  Failed to generate text for Feature ID {feature.id} (empty result)")
                    continue
                
                if isinstance(feature, Calligraphy):
                    calligraphy_service.update(
                        calligraphy_id=feature.id,
                        data=CalligraphyDict(
                            unit_id=feature.unit_id,
                            character=feature.character.to_dict(include_relations=False),
                            example_word={"word": generated_text, "translation": "", "type": "noun"}
                        )
                    )
                elif isinstance(feature, Vocabulary):
                    vocabulary_service.update(
                        voc_id=feature.id,
                        data=VocabularyDict(
                            unit_id=feature.unit_id,
                            word={
                                "word": feature.word.word,
                                "translation": feature.word.translation
                            },
                            example_sentences=[
                                {"text": generated_text, "translation": ""}
                            ]
                        )
                    )
                elif isinstance(feature, Grammar):
                    grammar_service.update(
                        grammar_id=feature.id,
                        data=GrammarDict(
                            unit_id=feature.unit_id,
                            title=feature.title,
                            explanation=feature.explanation,
                            learnable_sentences=[
                                {"text":generated_text, "translation":""}
                            ]
                        )
                    )
                
                success_count += 1
                logger.info(f"✅ Generated text for Feature ID {feature.id}: '{generated_text}'")
                
            except Exception as e:
                error_count += 1
                logger.error(f"❌ Failed to generate text for Feature ID {feature.id}: {e}")
                continue
        
        logger.info(f"✅ Text Generation task completed: {success_count} texts generated, {error_count} errors")
    except Exception as e:
        logger.error(f"❌ Text Generation task failed: {e}", exc_info=True)