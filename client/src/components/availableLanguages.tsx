import { getAvailableLanguages } from "@/api";
import LanguageOverviewCard from "./cards/languageOverviewCard";

type LanguagesObject = {
    [key: string]: Language;
};

type Language = {
    id: string;
    name: string;
    native_name: string;
    flag: string;
    level: string;
    current_unit_id: string;
    description?: string;
    score: number;
    last_seen: Date;
};

export default async function AvailableLanguages() {
  const languages: LanguagesObject = await getAvailableLanguages();

  return (
    <section>
        <p>Which language do you want to learn?</p>
        <ul>
            {Object.values(languages).map((lang) => (
                <li key={lang.id}>
                    <LanguageOverviewCard language={lang} />
                </li>
            ))}
        </ul>
    </section>
  );
}