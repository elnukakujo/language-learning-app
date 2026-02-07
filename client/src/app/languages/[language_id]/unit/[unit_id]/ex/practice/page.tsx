import Exercise from "@/interface/features/Exercise";
import { getExercisesByUnit } from "@/api";
import ExercisePractice from "@/components/forms/exerciseForms/exercisePractice";

export default async function PracticeExercisePage({ params }: { params: { unit_id: string } }) {
    const { unit_id } = await params;

    const exercises: Exercise[] = await getExercisesByUnit(unit_id);
    exercises.sort(() => Math.random() - 0.5); // Shuffle the array randomly

    return (
        <main>
            <h1>Exercise Practice</h1>
            <ExercisePractice exercise_lists={exercises} />
        </main>
    );
}