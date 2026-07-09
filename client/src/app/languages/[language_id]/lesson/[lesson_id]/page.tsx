import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

import VocabularyList from "@/components/elements/vocabularyList";
import GrammarList from "@/components/elements/grammarList";
import CalligraphyList from "@/components/elements/characterList";
import ExerciseList from "@/components/exercises/exerciseList";

import type Lesson from "@/interface/containers/Lesson";
import type Vocabulary from "@/interface/features/Vocabulary";
import type Grammar from "@/interface/features/Grammar";
import type Calligraphy from "@/interface/features/Calligraphy";
import type Exercise from "@/interface/features/Exercise";

import NavButton from "@/components/layout/navButton";
import DeleteButton from "@/components/ui/buttons/deleteButton";
import ElementPerformanceCard from "@/components/elements/elementPerformanceCard";
import ElementTagsCard from "@/components/elements/elementTagsCard";
import ElementSourcesCard from "@/components/elements/elementSourcesCard";
import { getLessonById } from "@/api/lesson";
import { getVocabularyByLesson } from "@/api/vocabulary";
import { getGrammarByLesson } from "@/api/grammar";
import { getCalligraphyByLesson } from "@/api/calligraphy";
import { getExercisesByLesson } from "@/api/exercise";


export default async function Lesson({ params }: { params: { language_id: string, lesson_id: string } }) {
    const { language_id, lesson_id } = await params;
    const lesson: Lesson = await getLessonById(lesson_id);

    const vocabularies: Vocabulary[] = await getVocabularyByLesson(lesson_id);
    const grammars: Grammar[] = await getGrammarByLesson(lesson_id);
    const calligraphies: Calligraphy[] =  await getCalligraphyByLesson(lesson_id);
    const exercises: Exercise[] = await getExercisesByLesson(lesson_id);

    return (
        <main className="flex flex-col gap-8">
            <header>
                <h1>{lesson.title}</h1>
                <Markdown remarkPlugins={[remarkGfm]}>{lesson.description}</Markdown>
                <ElementPerformanceCard element={lesson} />
                <ElementTagsCard element={lesson} />
                <ElementSourcesCard element={lesson} />
                <nav className="flex flex-row space-x-4">
                    <NavButton path={`/languages/${language_id}/lesson/${lesson_id}/update`}>
                        <p>Update this Lesson Informations</p>
                    </NavButton>
                    <DeleteButton element_id={lesson_id}>
                        <p>Delete this Lesson</p>
                    </DeleteButton>
                </nav>
            </header>
            <article className="flex flex-row gap-8 justify-around">
                <VocabularyList vocProps={vocabularies} />
                <GrammarList gramProps={grammars} />
                <CalligraphyList callProps={calligraphies} />
                <ExerciseList exProps={exercises} />
            </article>
        </main>
    );
}
