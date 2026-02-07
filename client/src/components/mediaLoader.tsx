"use client";
import { useRef, ChangeEvent, useState } from 'react';
import Image from 'next/image';
import { BASE_URL, uploadImage, uploadAudio } from "@/api";

export default function MediaLoader({ 
  imageUrl = undefined, 
  setImageUrl,
  audioUrl = undefined,
  setAudioUrl
}: {
  imageUrl?: string | undefined;
  setImageUrl: (imageUrl: string | undefined) => void;
  audioUrl?: string | undefined;
  setAudioUrl: (audioUrl: string | undefined) => void;
}) {
  const imageInputRef = useRef<HTMLInputElement>(null);
  const audioInputRef = useRef<HTMLInputElement>(null);
  const audioRef = useRef<HTMLAudioElement>(null);
  
  const [imagePreviewUrl, setImagePreviewUrl] = useState<string | undefined>(
    imageUrl ? `${BASE_URL}${imageUrl}` : undefined
  );
  const [audioPreviewUrl, setAudioPreviewUrl] = useState<string | undefined>(
    audioUrl ? `${BASE_URL}${audioUrl}` : undefined
  );

  const getFileExtension = (filename: string): string => {
    return filename.toLowerCase().split('.').pop() || '';
  };

  const handleImageChange = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const extension = getFileExtension(file.name);
    const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg'];
    
    const isImage = imageExtensions.some(ext => extension.endsWith(ext));
    
    if (!isImage) {
      console.error("Invalid file type. Please upload an image file.");
      return;
    }

    try {
      const { url } = await uploadImage(file);
      const fullUrl = `${BASE_URL}${url}`;
      setImagePreviewUrl(fullUrl);
      setImageUrl(url);
    } catch (error) {
      console.error("Error uploading image:", error);
      throw error;
    }
  };

  const handleAudioChange = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const extension = getFileExtension(file.name);
    const audioExtensions = ['mp3', 'wav', 'ogg', 'aac', 'm4a', 'flac'];
    
    const isAudio = audioExtensions.some(ext => extension.endsWith(ext));
    
    if (!isAudio) {
      console.error("Invalid file type. Please upload an audio file.");
      return;
    }

    try {
      const { url } = await uploadAudio(file);
      const fullUrl = `${BASE_URL}${url}`;
      setAudioPreviewUrl(fullUrl);
      setAudioUrl(url);
    } catch (error) {
      console.error("Error uploading audio:", error);
      throw error;
    }
  };

  const clearImage = () => {
    setImagePreviewUrl(undefined);
    setImageUrl(undefined);
    if (imageInputRef.current) {
      imageInputRef.current.value = '';
    }
  };

  const clearAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setAudioPreviewUrl(undefined);
    setAudioUrl(undefined);
    if (audioInputRef.current) {
      audioInputRef.current.value = '';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-sm font-medium mb-2">Image</h3>
        <input
          type="file"
          ref={imageInputRef}
          accept="image/*"
          onChange={handleImageChange}
          className="hidden"
        />
        <div className='flex flex-row space-x-4'>
          <button
            type='button'
            onClick={() => imageInputRef.current?.click()}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            {imagePreviewUrl ? 'Change Image' : 'Upload Image'}
          </button>
          {imagePreviewUrl && (
            <button
              type='button'
              onClick={clearImage}
              className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
            >
              Clear Image
            </button>
          )}
        </div>
        {imagePreviewUrl && (
          <div className="mt-4 relative h-48 w-full">
            <Image
              src={imagePreviewUrl}
              alt="Preview"
              fill
              className="object-contain"
              sizes="(max-width: 768px) 100vw, 50vw"
            />
          </div>
        )}
      </div>

      {/* Audio Upload Section */}
      <div>
        <h3 className="text-sm font-medium mb-2">Audio</h3>
        <input
          type="file"
          ref={audioInputRef}
          accept="audio/*"
          onChange={handleAudioChange}
          className="hidden"
        />
        <div className='flex flex-row space-x-4'>
          <button
            type='button'
            onClick={() => audioInputRef.current?.click()}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            {audioPreviewUrl ? 'Change Audio' : 'Upload Audio'}
          </button>
          {audioPreviewUrl && (
            <button
              type='button'
              onClick={clearAudio}
              className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
            >
              Clear Audio
            </button>
          )}
        </div>
        {audioPreviewUrl && (
          <div className="mt-4 space-y-3">
            <audio 
              ref={audioRef}
              src={audioPreviewUrl}
              className="w-full"
              controls
            />
          </div>
        )}
      </div>
    </div>
  );
}