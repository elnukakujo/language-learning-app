"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import { createLanguage } from "@/api";

export default function CreateLanguageForm() {
  const router = useRouter();
  
  const [name, setName] = useState<string | undefined>(undefined);
  const [nativeName, setNativeName] = useState<string | undefined>(undefined);
  const [description, setDescription] = useState<string | undefined>(undefined);
  const [level, setLevel] = useState<'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2'>("A1");
  const [flag, setFlag] = useState<string | undefined>(undefined);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const element = {
      name: name,
      native_name: nativeName,
      description: description || undefined,
      level: level,
      flag: flag || undefined
    };
    
    try {
      await createLanguage(element);
      
      router.push('/');
      router.refresh();
      
    } catch (error) {
      console.error("Failed to create language:", error);
      alert("Failed to create language. Check console for details.");
    }
  };

  return (
    <form className="flex flex-col space-y-4 items-center" onSubmit={handleSubmit}>
      <AutoWidthInput
        value={name || ""}
        label="Name"
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter language name"
        className="border border-gray-300"
        required={true}
      />
      <AutoWidthInput
        value={nativeName || ""}
        label="Native Name"
        onChange={(e) => setNativeName(e.target.value)}
        placeholder="Enter native name"
        className="border border-gray-300"
        required={true}
      />
      <AutoSizeTextArea
        value={description || ""}
        onChange={(e) => setDescription(e.target.value)}
        className="border border-gray-300"
        label="Description"
      />
      <ClassicSelectMenu
        label="Level"
        options={['A1', 'A2', 'B1', 'B2', 'C1', 'C2']}
        selectedOption={level}
        onChange={(value) => setLevel(value as typeof level)}
        required={true}
      />
      <AutoWidthInput
        value={flag || ""}
        label="Flag"
        onChange={(e) => setFlag(e.target.value)}
        placeholder="Enter flag"
        className="border border-gray-300"
      />
      <NewElementButton>Add Language</NewElementButton>
    </form>
  );
}