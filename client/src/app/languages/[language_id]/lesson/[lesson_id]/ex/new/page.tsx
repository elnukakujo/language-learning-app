import { getCalligraphyByLesson } from "@/api/calligraphy";
import { getGrammarByLesson } from "@/api/grammar";
import { getVocabularyByLesson } from "@/api/vocabulary";
import ExerciseForm from "@/components/forms/entityForms/exerciseForm";
import Calligraphy from "@/interface/features/Calligraphy";
import Grammar from "@/interface/features/Grammar";
import Vocabulary from "@/interface/features/Vocabulary";

interface LessonElements {
    vocabularies: Vocabulary[];
    grammars: Grammar[];
    calligraphies: Calligraphy[];
}

export default async function createExercisePage({ params }: { params: { lesson_id: string } }) {
    const { lesson_id } = await params;

    const calligraphies: Calligraphy[] = await getCalligraphyByLesson(lesson_id);
    const grammars: Grammar[] = await getGrammarByLesson(lesson_id);
    const vocabularies: Vocabulary[] = await getVocabularyByLesson(lesson_id);

    const lessonElements: LessonElements = {
        vocabularies,
        grammars,
        calligraphies
    };

    return (
        <div className="flex flex-col items-center justify-center h-full">
            <h1 className="text-2xl font-bold mb-4">Create New Exercise</h1>
            <ExerciseForm lesson_id={lesson_id} lessonElements={lessonElements} />
        </div>
    );
}