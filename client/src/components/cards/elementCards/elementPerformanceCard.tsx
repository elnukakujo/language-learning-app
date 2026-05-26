'use client';

import { useState, useEffect } from "react";
import { useParams } from 'next/navigation';
import { BaseElement } from "@/interface/base";
import { getLanguageById } from "@/api/language";
import { languageProficiencySystems } from "@/utils/language_iso639";

export default function ElementPerformanceCard({ element }: { element: BaseElement }) {
  const params = useParams();
  const language_id = params?.language_id as string;
  const [language_iso639_1, setLanguageIso639_1] = useState<string>("");

  useEffect(() => {
    if (!('level' in element)) return;

    getLanguageById(language_id).then(lang => {
        setLanguageIso639_1(lang.target_iso639_2t as string);
    });
  }, []);

  return (
    <section className="flex flex-col space-y-2 p-4 border rounded-md">
      <h3>Performance Information</h3>
      {'level' in element && (
        <p>Level: {languageProficiencySystems[language_iso639_1]?.levels[element.level as number].code}</p>
      )}
      {'score' in element && (element as any).score != null && (
        <p>Score: {(element as any).score.toFixed(2)}/100</p>
      )}
      {'difficulty' in element && (element as any).difficulty != null && (
        <p>Difficulty: {(element as any).difficulty.toFixed(2)}</p>
      )}
      {'status' in element && (element as any).status != null && (
        <p>Status: {(element as any).status}</p>
      )}
      {'created_at' in element && (element as any).created_at != null && (
        <p>Created at: {new Date((element as any).created_at).toLocaleDateString()}</p>
      )}
      {'last_seen_at' in element && (element as any).last_seen_at != null && (
        <p>Last seen at: {new Date((element as any).last_seen_at).toLocaleDateString()}</p>
      )}
    </section>
  );
}