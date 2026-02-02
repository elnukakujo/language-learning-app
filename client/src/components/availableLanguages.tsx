import { getAvailableLanguages } from "@/api";
import LanguageOverviewCard from "./cards/languageOverviewCard";
import Language from "@/interface/containers/Language";
import NavButton from "@/components/buttons/navButton";

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
                <li key={"l"+lang.id}>
                    <LanguageOverviewCard language={lang} />
                </li>
            ))}
        </ul>
        <NavButton path="/languages/new">
            <p>Create New Language</p>
        </NavButton>
    </section>
  );
}