from deep_translator import GoogleTranslator
from lingua import LanguageDetectorBuilder
def translateazen(tgstr):
    # translate a spanish text to english text (by default)
    detector=LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()
    lang=detector.detect_language_of(tgstr).iso_code_639_1.name.lower()
    translation = GoogleTranslator(source=lang, target='en').translate(tgstr)
    return translation,lang

def translateenaz(tgstr,lang):
    # translate a spanish text to english text (by default)
    translation = GoogleTranslator(source='en', target=lang).translate(tgstr)
    return translation

def translate(tgstr):
    translation = GoogleTranslator(source='en', target='az').translate(tgstr)
    return translation