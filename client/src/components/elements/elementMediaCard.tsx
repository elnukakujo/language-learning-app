import { BaseMediaFiles } from "@/interface/base";
import { PUBLIC_BASE_URL as BASE_URL } from "@/api";
import AudioPlayer from "../media/audioPlayer";
import ImageViewer from "../media/imageViewer";

export default function ElementMediaCard({element}: { element: BaseMediaFiles }) {
    const hasImages = !!element.image_files?.length;
    const hasAudio = !!element.audio_files?.length;
    if (!hasImages && !hasAudio) return null;

    return (
        <section 
            className="card flex flex-col space-y-4"
        >
            {element.image_files && element.image_files.map((url, idx) => (
                <ImageViewer
                    key={idx}
                    src={BASE_URL + url}
                    alt=""
                    className="max-w-[16rem] max-h-[16rem] object-contain"
                />
            ))}
            {element.audio_files && element.audio_files.map((url, idx) => (
                <AudioPlayer key={idx} src={BASE_URL + url} />
            ))}
        </section>
    );
}