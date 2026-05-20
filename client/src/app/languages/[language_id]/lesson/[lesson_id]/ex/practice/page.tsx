import Exercise from "@/interface/features/Exercise";
import { getExercisesByLesson } from "@/api/exercise";
import ExercisePractice from "@/components/forms/exerciseForms/exercisePractice";

export default async function PracticeExercisePage({ params }: { params: { lesson_id: string } }) {
    const { lesson_id } = await params;

    const exercises: Exercise[] = await getExercisesByLesson(lesson_id);
    exercises.sort(() => Math.random() - 0.5); // Shuffle the array randomly

    return (
        <main>
            <h1>Exercise Practice</h1>
            <ExercisePractice exercise_lists={exercises} />
        </main>
    );
}