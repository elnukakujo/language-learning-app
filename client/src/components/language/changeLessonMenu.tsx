"use client";

export default function ChangeLessonMenu({ lessonsId, lessonId, onChange }: { lessonsId: string[]; lessonId: string; onChange: (id: string) => void }) {

    return (
        <select value={lessonId} onChange={(e) => onChange(e.target.value)} className="input w-fit">
            {lessonsId.map((id) => (
                <option key={id} value={id}>
                    {id}
                </option>
            ))}
        </select>
    );
}