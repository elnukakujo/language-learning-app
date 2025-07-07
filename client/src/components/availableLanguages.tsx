import { getAvailableLanguages } from "@/api";
import LanguageOverviewCard from "./cards/languageOverviewCard";
import Language from "@/interface/Language";

type LanguagesObject = {
    [key: string]: Language;
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