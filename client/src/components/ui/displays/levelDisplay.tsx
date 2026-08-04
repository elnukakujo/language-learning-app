import {languageProficiencySystems} from '@/utils/language_iso639';

interface LevelDisplayProps {
  levelIdx: number; // 0-5
  language_iso639_1: string;
}

export default function LevelDisplay({ levelIdx, language_iso639_1 }: LevelDisplayProps) {
    const level_code = languageProficiencySystems[language_iso639_1]?.levels[levelIdx].code

    return (
        <div className="inline-flex items-center gap-2">
            <span className="text-sm text-muted">Level</span>

            <span className={`text-xs font-medium level-${levelIdx}`}>
                {level_code}
            </span>
        </div>
    );
}