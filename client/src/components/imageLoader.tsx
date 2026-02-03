"use client";

import { useRef, ChangeEvent, useState } from 'react';
import Image from 'next/image';
import { BASE_URL, uploadImage } from "@/api";

export default function ImageLoader({ 
  imageUrl = undefined, 
  setImageUrl 
}: {
  imageUrl?: string|undefined;
  setImageUrl: (imageUrl: string|undefined) => void;
}) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [previewUrl, setPreviewUrl] = useState<string|undefined>(imageUrl ? `${BASE_URL}${imageUrl}` : undefined);

  const handleImageChange = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const { url } = await uploadImage(file);
  
      setPreviewUrl(`${BASE_URL}${url}`);
      setImageUrl(url);
    } catch (error) {
      console.error("Error uploading image:", error);
      throw error;
    }
  };

  return (
    <div>
      <input
        type="file"
        ref={fileInputRef}
        accept="image/*"
        onChange={handleImageChange}
        className="hidden"
      />
      <div className='flex flex-row space-x-4'>
        <button
          type='button'
          onClick={() => fileInputRef.current?.click()}
          className="px-4 py-2 bg-blue-500 text-white rounded"
        >
          {previewUrl ? 'Change Image' : 'Upload Image'}
        </button>
        {previewUrl &&  (
          <button
            type='button'
            onClick={() => {
              setPreviewUrl(undefined);
              setImageUrl(undefined);
            }}
            className="px-4 py-2 bg-blue-500 text-white rounded"
          >
            Clear Image
          </button>
        )}
      </div>

      {previewUrl && previewUrl !== undefined && (
        <div className="mt-4 relative h-48 w-full">
          <Image
            src={previewUrl}
            alt="Preview"
            fill
            className="object-contain"
            sizes="(max-width: 768px) 100vw, 50vw"
          />
        </div>
      )}
    </div>
  );
}