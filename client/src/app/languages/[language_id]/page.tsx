import LessonOverviewCard from "@/components/language/lessonOverviewCard";
import type Lesson from "@/interface/containers/Lesson";
import NavButton from "@/components/layout/navButton";
import DeleteButton from "@/components/ui/buttons/deleteButton";
import ElementPerformanceCard from "@/components/elements/elementPerformanceCard";
import ElementTagsCard from "@/components/elements/elementTagsCard";
import ElementSourcesCard from "@/components/elements/elementSourcesCard";
import DailyStatsCard from "@/components/language/dailyStatsCard";
import LanguageStatsPanel from "@/components/language/LanguageStatsPanel";
import { ISO639_2T_to_LANGUAGE } from "@/utils/language_iso639";
import { getLanguageData } from "@/api/language";
import { getTodayDailyStats } from "@/api/dailyStats";

export default async function Language({ params }: { params: { language_id: string } }) {
    const { language_id } = await params;
    const { language, lessons } = await getLanguageData(language_id);
    const dailyStats = language.user_id ? await getTodayDailyStats(language.user_id, language_id) : null;
    const commitmentLog = language.user_id ? await (await import("@/api/commitmentLog")).getCommitmentLogForUserLanguage(language.user_id, language_id) : null;
    const hasLessons = lessons && lessons.length > 0;
    console.log(language);

    return (
        <main className="flex flex-col space-y-4">
            <header className="flex flex-col gap-4">
                <h1>{language.flag} {language.name} ({language.alias})</h1>
                <span>
                    {language.source_iso639_2t && <p>From: {ISO639_2T_to_LANGUAGE[language.source_iso639_2t]}</p>}
                    {language.target_iso639_2t && <p>To: {ISO639_2T_to_LANGUAGE[language.target_iso639_2t]}</p>}
                </span>
                {language.description && <p>{language.description}</p>}
                <ElementPerformanceCard element={language} />
                <ElementTagsCard element={language} />
                <ElementSourcesCard element={language} />
                <LanguageStatsPanel dailyStats={dailyStats} commitmentLog={commitmentLog} />
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