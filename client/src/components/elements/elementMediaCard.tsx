import { BaseMediaFiles } from "@/interface/base";
import { BASE_URL } from "@/api";
import Image from "next/image";

export default function ElementMediaCard({element}: { element: BaseMediaFiles }) {
    const hasImages = !!element.image_files?.length;
    const hasAudio = !!element.audio_files?.length;
    if (!hasImages && !hasAudio) return null;

    return (
        <section className="card flex flex-col space-y-4">
            {element.image_files && element.image_files.map((url, idx) => (
                <Image
                    key={idx}
                    src={BASE_URL + url}
                    alt=""
                    width={200}
                    height={200}
                />
            ))}
            {element.audio_files && element.audio_files.map((url, idx) => (
                <audio key={idx} src={BASE_URL + url} controls />
            ))}
        </section>
    );
}