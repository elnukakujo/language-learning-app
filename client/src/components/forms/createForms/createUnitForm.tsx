"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import { createUnit } from "@/api";
import Unit from "@/interface/containers/Unit";

export default function CreateUnitForm({ language_id }: { language_id: string }) {
  const router = useRouter();
  
  const [title, setTitle] = useState<string | undefined>(undefined);
  const [description, setDescription] = useState<string | undefined>(undefined);
  const [level, setLevel] = useState<'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2'>('A1');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const element: Unit = {
      title: title!,
      level: level,
      description: description || undefined,
      language_id: language_id,
    };
    
    try {
      await createUnit(element);
      
      const router_path = `/languages/${language_id}`;
      
      router.push(router_path);
      router.refresh();
      
    } catch (error) {
      console.error("Failed to create unit:", error);
      alert("Failed to create unit. Check console for details.");
    }
  };

  return (
    <form className="flex flex-col space-y-4 items-center" onSubmit={handleSubmit}>
      <AutoWidthInput
        value={title || ""}
        label="Title"
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter unit title"
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
      <NewElementButton>Add Unit</NewElementButton>
    </form>
  );
}