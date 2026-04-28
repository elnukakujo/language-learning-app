import { getCalligraphyByLesson, getElementbyId, getGrammarByLesson, getVocabularyByLesson } from "@/api";
import type Exercise from "@/interface/features/Exercise";
import ExerciseForm from "@/components/forms/entityForms/exerciseForm";
import Calligraphy from "@/interface/features/Calligraphy";
import Grammar from "@/interface/features/Grammar";
import Vocabulary from "@/interface/features/Vocabulary";

type paramsType = {
    language_id: string;
    lesson_id: string;
    ex_id: string;
};

interface LessonElements {
    vocabularies: Vocabulary[];
    grammars: Grammar[];
    calligraphies: Calligraphy[];
}

export default async function UpdateExercisePage({ params }: { params: paramsType }) {
    const { lesson_id, ex_id } = await params;
    const exercise: Exercise = await getElementbyId(ex_id);

    const calligraphies: Calligraphy[] = await getCalligraphyByLesson(lesson_id);
    const grammars: Grammar[] = await getGrammarByLesson(lesson_id);
    const vocabularies: Vocabulary[] = await getVocabularyByLesson(lesson_id);

    const lessonElements: LessonElements = {
        calligraphies,
        grammars,
        vocabularies
    };

    return (
        <main className="p-4">
            <h1 className="text-2xl font-semibold mb-4">Update Exercise Informations</h1>
            <ExerciseForm exercise={exercise} lesson_id={lesson_id} lessonElements={lessonElements} />
        </main>
    );
}