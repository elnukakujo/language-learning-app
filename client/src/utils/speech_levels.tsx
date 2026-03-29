export const SPEECH_LEVELS: { label: string; threshold: number; description: string; stars: string }[] = [
    { label: "Lost in Translation", threshold: 0, description: "Your pronunciation is still finding its way—keep practicing!", stars: "☆☆☆☆☆" },
    { label: "Tourist Mode", threshold: 0.50, description: "You're getting there, but locals might need to guess a bit.", stars: "★☆☆☆☆" },
    { label: "Confident Speaker", threshold: 0.70, description: "You're understood, and that's a big win!", stars: "★★★☆☆" },
    { label: "Almost Native", threshold: 0.85, description: "Impressive! Just a few tweaks and you'll fool everyone.", stars: "★★★★☆" },
    { label: "Native-like", threshold: 0.95, description: "Flawless! Even locals would think you grew up here.", stars: "★★★★★" },
];

export function getLevelForScore(score: number) {
    return (
        [...SPEECH_LEVELS].sort((a, b) => b.threshold - a.threshold).find((l) => score >= l.threshold)
        ?? { label: "Unknown", description: "No feedback available.", stars: "☆☆☆☆☆" }
    );
}