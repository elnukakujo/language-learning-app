import { getLanguageData } from "@/api";
import Language from "@/interface/containers/Language";
import UpdateLanguageForm from "@/components/forms/updateForms/updateLanguageForm";

export default async function UpdateLanguagePage({params }: {params: {language_id: string}}) {
    const { language_id } = await params;
    // Fetch the language data based on the language_id
    const languageData = await getLanguageData(language_id);
    const language: Language = await languageData.language;

    return (
        <main>
            <h1>Update Language</h1>
            <UpdateLanguageForm language={language} />
        </main>
    );

}