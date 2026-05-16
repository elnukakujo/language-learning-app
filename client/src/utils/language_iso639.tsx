export const LANGUAGE_to_ISO639_2T: Record<string, string> = {
    "Catalan": "cat",
    "Chinese": "zho",
    "Croatian": "hrv",
    "Danish": "dan",
    "Dutch": "nld",
    "English": "eng",
    "Finnish": "fin",
    "French": "fra",
    "German": "deu",
    "Greek": "ell",
    "Italian": "ita",
    "Japanese": "jpn",
    "Korean": "kor",
    "Lithuanian": "lit",
    "Macedonian": "mkd",
    "Norwegian Bokmål": "nob",
    "Norwegian": "nor",
    "Polish": "pol",
    "Portuguese": "por",
    "Romanian": "ron",
    "Russian": "rus",
    "Slovenian": "slv",
    "Spanish": "spa",
    "Swedish": "swe",
    "Ukrainian": "ukr",
    "Custom": "",
    // Add more languages as needed
};

export const ISO639_2T_to_LANGUAGE: Record<string, string> = Object.fromEntries(
    Object.entries(LANGUAGE_to_ISO639_2T).map(([language, iso]) => [iso, language])
);