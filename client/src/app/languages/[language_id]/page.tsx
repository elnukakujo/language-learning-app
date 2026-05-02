import { getLanguageData } from "@/api";

import LessonOverviewCard from "@/components/cards/lessonOverviewCard";
import type Lesson from "@/interface/containers/Lesson";
import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";

export default async function Language({ params }: { params: { language_id: string } }) {
    const { language_id } = await params;
    const { language, lessons } = await getLanguageData(language_id);
    const hasLessons = lessons && lessons.length > 0;

    return (
        <main className="flex flex-col space-y-4">
            <header className="flex flex-col">
                <h1>{language.flag} {language.name} ({language.native_name})</h1>
                {language.level && <p>Language Level: {language.level}</p>}
                <p>Language Score: {language.score.toFixed(1)}/100</p>
                <p>Status: {language.status}</p>
                <p>Created at: {new Date(language.created_at || 0).toLocaleDateString('en-US')}</p>
                <p>Last Seen: {new Date(language.last_seen_at || 0).toLocaleDateString('en-US')}</p>
                {language.current_lesson_id && <p>Current Lesson ID: {language.current_lesson_id}</p>}
                <nav className="flex flex-row space-x-4">
                    {language.current_lesson_id && <NavButton path={`/languages/${language_id}/lesson/${language.current_lesson_id}`}>
                        <p>Go to Current Lesson</p>
                    </NavButton>}
                    <NavButton path={`/languages/${language_id}/update`}>
                        <p>Update Language</p>
                    </NavButton>
                    <DeleteButton element_id={language_id}/>
                </nav>
            </header>
            <article className="flex flex-col space-y-4">
                {
                    hasLessons && 
                    (
                        <section>
                            <h2>Lessons</h2>
                            <ul className="flex flex-col space-y-2">
                                {lessons.map((lesson: Lesson) => (
                                    <li key={lesson.id}>
                                        <LessonOverviewCard lesson={lesson} />
                                    </li>
                                ))}
                            </ul>
                        </section>
                    )
                }
                
                <NavButton path={`/languages/${language_id}/lesson/new`}>
                    <p>Create New Lesson</p>
                </NavButton>
            </article>
        </main>
    );
}