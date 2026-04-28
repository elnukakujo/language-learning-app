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
        <button className="border rounded-lg p-4" onClick={handleClick}>
            <h3>{lesson.title}</h3>
            <Markdown remarkPlugins={[remarkGfm]}>{lesson.description}</Markdown>
            <p>Score: {lesson.score?.toFixed(1)}/100</p>
        </button>
    );
}