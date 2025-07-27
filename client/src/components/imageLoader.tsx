"use client";

import { useState, useRef, ChangeEvent } from 'react';
import Image from 'next/image';
import { uploadImage } from "@/api";

interface ImageLoaderProps {
  previewUrl: string | null;
  setPreviewUrl: (imageUrl: string|null) => void;
}

export default function ImageLoader({ previewUrl, setPreviewUrl }: ImageLoaderProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageChange = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const { file_url } = await uploadImage(file);
      setPreviewUrl("http://localhost:8000"+file_url);
    } catch (error) {
      setPreviewUrl(null);
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
              setPreviewUrl(null);
            }}
            className="px-4 py-2 bg-blue-500 text-white rounded"
          >
            Clear Image
          </button>
        )}
      </div>
      
      {previewUrl && (
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