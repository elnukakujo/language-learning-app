import { getAvailableLanguages } from "@/api/language";
import { getCurrentUserId } from "@/utils/user_cookie";
import LanguageOverviewCard from "./cards/languageOverviewCard";
import Language from "@/interface/containers/Language";

export default async function AvailableLanguages() {
    const userId: string | null = await getCurrentUserId();
    const languages: Language[] = await getAvailableLanguages(userId!);

    return (
        <article className="flex flex-row gap-4 items-center">
            {languages.length === 0 && (
                <p className="text-sm opacity-50">No available languages found. Please add some.</p>
            )}
            {languages.map((lang, idx) => (
                <section key={idx}>
                    <LanguageOverviewCard language={lang} />
                </section>
            ))}
        </article>
    );
}