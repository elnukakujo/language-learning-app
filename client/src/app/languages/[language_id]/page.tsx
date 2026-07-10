import LessonOverviewCard from "@/components/lesson/lessonOverviewCard";
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
import LanguageHeaderCard from "@/components/language/languageHeaderCard";

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
                <LanguageHeaderCard language={language} />
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
                            <ul className="flex flex-row flex-wrap gap-2 ">
                                {lessons.map((lesson: Lesson) => (
                                    <li key={lesson.id}>
                                        <LessonOverviewCard language_code={language.target_iso639_2t || ""} lesson={lesson} />
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