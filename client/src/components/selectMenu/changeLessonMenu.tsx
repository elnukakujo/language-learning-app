"use client";

export default function ChangeLessonMenu({ lessonsId, lessonId, onChange }: { lessonsId: string[]; lessonId: string; onChange: (id: string) => void }) {

    return (
        <select value={lessonId} onChange={(e) => onChange(e.target.value)} className="flex w-fit overflow-hidden border border-gray-300 rounded-md p-2">
            {lessonsId.map((id) => (
                <option key={id} value={id}>
                    {id}
                </option>
            ))}
        </select>
    );
}