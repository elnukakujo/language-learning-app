from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / 'instance'
MEDIA_DIR = BASE_DIR / 'media'
BACKUP_DIR = BASE_DIR / 'backups'

class Config:
    """Base configuration for personal use"""
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Paths
    MEDIA_ROOT = str(BASE_DIR / 'media')
    BACKUP_ROOT = str(BASE_DIR / 'backups')
    
    # Media settings
    MAX_AUDIO_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_IMAGE_SIZE = 5 * 1024 * 1024   # 5MB
    ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav'}
    ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    
    # Backup settings
    BACKUP_INTERVAL_MINUTES = 20  # Every 20 minutes
    MAX_BACKUPS = 10  # Keep last 10 backups

    # TTS settings
    TTS_INTERVAL_MINUTES = 20  # Generate TTS every 20 minuters while app is running

    # Text Generation settings
    TEXT_GEN_INTERVAL_MINUTES = 20 # Generate text examples every 20 minutes while app is running

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{INSTANCE_DIR}/dev_languages.db'
    ENV = 'development'
    MEDIA_ROOT = str(BASE_DIR / 'dev' / 'media')
    BACKUP_ROOT = str(BASE_DIR / 'dev' / 'backups')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{INSTANCE_DIR}/test_languages.db'
    ENV = 'testing'
    MEDIA_ROOT = str(BASE_DIR / 'test' / 'media')
    BACKUP_ROOT = str(BASE_DIR / 'test' / 'backups')

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{INSTANCE_DIR}/languages.db')
    ENV = 'production'

# Default to development
config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}