import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { getLessonById, getVocabularyByLesson, getGrammarByLesson, getCalligraphyByLesson, getExercisesByLesson } from "@/api";
import VocabularyList from "@/components/lists/vocabularyList";
import GrammarList from "@/components/lists/grammarList";
import CalligraphyList from "@/components/lists/characterList";
import ExerciseList from "@/components/lists/exerciseList";

import type Lesson from "@/interface/containers/Lesson";
import type Vocabulary from "@/interface/features/Vocabulary";
import type Grammar from "@/interface/features/Grammar";
import type Calligraphy from "@/interface/features/Calligraphy";
import type Exercise from "@/interface/features/Exercise";

import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";


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
                <p>Score: {lesson.score?.toFixed(1) || "N/A"}/100</p>
                <p>Status: {lesson.status || "N/A"}</p>
                <p>Created at: {new Date(lesson.created_at || 0).toLocaleDateString('en-US')}</p>
                <p>Last Seen: {new Date(lesson.last_seen_at || 0).toLocaleDateString('en-US')}</p>
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
