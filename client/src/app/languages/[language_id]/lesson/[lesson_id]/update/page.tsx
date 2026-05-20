import Lesson from "@/interface/containers/Lesson";
import { getLessonById } from "@/api/lesson";
import LessonForm from "@/components/forms/entityForms/lessonForm";

export default async function UpdateLessonPage({ params }: { params: { language_id: string, lesson_id: string } }) {
    const { language_id, lesson_id } = await params;

    const lesson: Lesson = await getLessonById(lesson_id);

    return (
        <main>
            <h1>Update Lesson</h1>
            <LessonForm language_id={language_id} lesson={lesson} />
        </main>
    );
}