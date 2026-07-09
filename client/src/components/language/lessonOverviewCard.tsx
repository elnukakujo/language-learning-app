"use client";

import { useParams, useRouter } from 'next/navigation';
import Markdown from "react-markdown";
import remarkGfm from 'remark-gfm';
import type Lesson from "@/interface/containers/Lesson";

export default function LessonOverviewCard({ lesson }: { lesson: Lesson }) {
    const { language_id } = useParams();
    const router = useRouter();
    const handleClick = () => {
        router.push(`/languages/${language_id}/lesson/${lesson.id}`);
    };
    return (
        <button
            className="card flex h-48 w-48 shrink-0 flex-col gap-2 overflow-hidden text-left cursor-pointer transition hover:-translate-y-0.5 hover:bg-accent-soft hover:shadow-md"
            onClick={handleClick}
        >
            <h3 className="font-serif text-lg text-ink line-clamp-1">{lesson.title}</h3>
            <div className="index-divider" />
            <div className="line-clamp-4 flex-1 text-sm text-muted prose-sm">
                <Markdown remarkPlugins={[remarkGfm]}>{lesson.description}</Markdown>
            </div>
            <p className="stat-value text-base">Score: {lesson.score?.toFixed(1)}/100</p>
        </button>
    );
}