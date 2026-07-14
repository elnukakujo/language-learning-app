import LessonForm from "@/components/lesson/lessonForm";

export default async function NewLessonPage({ params }: {params: Promise<{ language_id: string }> }) {
    const { language_id } = await params;

    return (
        <main>
            <h1>Create New Lesson for Language ID: {language_id}</h1>
            <LessonForm language_id={language_id} />
        </main>
    );
}