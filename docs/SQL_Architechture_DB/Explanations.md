# Description de l'architechture de la database SQL 

![Diagramme UML de la base de données](./docs/SQL_Architechture_DB/GeneralDatabase.png)

Le diagrame UML modélise la structure relationnelle de la base de données pour un système d’apprentissage potentiellement multilingue.

---

## Tables et attributs principaux

- **Language**  
  - `language_id` (PK) : Identifiant unique et code de la langue (ex : "CH" pour chinois).  
  - `name` : Nom complet de la langue.

- **Unit**  
  - `unit_id` (PK) : Identifiant du module d’apprentissage (ex : "CH_1").  
  - `language_id` (FK) : Référence à la langue correspondante.  
  - `title` : Titre du module.  
  - `description` : Description détaillée du module.  
  - `level` : Niveau (ex : A1, A2…).

- **Vocabulary**  
  - `vocab_id` (PK) : Identifiant unique du mot (ex : "CH_4_V_1").  
  - `unit_id` (FK) : Module auquel appartient le mot.  
  - `word` : Mot ou caractère dans la langue cible.  
  - `translation` : Traduction du mot.  
  - `phonetic` : Prononciation (ex : pinyin pour le chinois).  
  - `word_type` : Type grammatical (nom, adjectif, verbe…).

- **GrammarLesson**  
  - `grammar_id` (PK) : Identifiant unique de la leçon (ex : "CH_1_G_1").  
  - `unit_id` (FK) : Module auquel appartient la leçon.  
  - `title` : Titre de la leçon de grammaire.  
  - `explanation` : Contenu explicatif de la règle.

- **CalligraphyCharacter**  
  - `char_id` (PK) : Identifiant du caractère calligraphique (ex : "CH_1_C_1").  
  - `unit_id` (FK) : Module associé.  
  - `character` : Caractère à apprendre.  
  - `components` : Composants ou radicaux formant le caractère.  
  - `translation` : Signification ou traduction.

---

## Relations et multiplicité

- Un **Language** peut contenir plusieurs **Unit** (`1 .. *`).  
- Une **Unit** regroupe plusieurs éléments dans :  
  - **Vocabulary** (`1 .. *`)  
  - **GrammarLesson** (`1 .. *`)  
  - **CalligraphyCharacter** (`1 .. *`)  

Les relations sont modélisées via des clés étrangères (`FK`) dans les tables enfants pointant vers leurs parents.

---