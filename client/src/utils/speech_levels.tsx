export const EXERCISE_LEVELS: Record<string, { label: string; threshold: number; description: string; stars: string }[]> = {
    speaking: [
        { label: "Lost in Translation", threshold: 0,    description: "Your repetition is still finding its way—keep practicing!", stars: "☆☆☆☆☆" },
        { label: "Tourist Mode",        threshold: 0.50, description: "You're getting there, but a few words slipped!", stars: "★☆☆☆☆" },
        { label: "Confident Speaker",   threshold: 0.70, description: "You're repeating well, and that's a big win!", stars: "★★★☆☆" },
        { label: "Almost Native",       threshold: 0.85, description: "Impressive! Just a few tweaks and you'll nail it.", stars: "★★★★☆" },
        { label: "Native-like",         threshold: 0.95, description: "Flawless! Spot-on repetition every time.", stars: "★★★★★" },
    ],
    type_in_the_blank: [
        { label: "Lost in Translation", threshold: 0,    description: "The blanks are still a mystery—keep at it!", stars: "☆☆☆☆☆" },
        { label: "Tourist Mode",        threshold: 0.50, description: "Some blanks filled, but a few gaps remain.", stars: "★☆☆☆☆" },
        { label: "Confident Speaker",   threshold: 0.70, description: "You're filling in the blanks with confidence!", stars: "★★★☆☆" },
        { label: "Almost Native",       threshold: 0.85, description: "Almost perfect—just a couple of blanks to go.", stars: "★★★★☆" },
        { label: "Native-like",         threshold: 0.95, description: "Flawless! Every blank filled perfectly.", stars: "★★★★★" },
    ],
    organize: [
        { label: "Lost in Translation", threshold: 0,    description: "The sentence order is still a puzzle—keep practicing!", stars: "☆☆☆☆☆" },
        { label: "Tourist Mode",        threshold: 0.45, description: "Some words in place, but the order needs work.", stars: "★☆☆☆☆" },
        { label: "Confident Speaker",   threshold: 0.65, description: "Your sentence structure is coming together!", stars: "★★★☆☆" },
        { label: "Almost Native",       threshold: 0.80, description: "Nearly perfect order—just a little reshuffling needed.", stars: "★★★★☆" },
        { label: "Native-like",         threshold: 0.92, description: "Flawless! Every word exactly where it should be.", stars: "★★★★★" },
    ],
    translate: [
        { label: "Lost in Translation", threshold: 0,    description: "The meaning is still getting lost—keep practicing!", stars: "☆☆☆☆☆" },
        { label: "Tourist Mode",        threshold: 0.40, description: "You're conveying some meaning, but locals might need to guess.", stars: "★☆☆☆☆" },
        { label: "Confident Speaker",   threshold: 0.60, description: "Your translation gets the message across!", stars: "★★★☆☆" },
        { label: "Almost Native",       threshold: 0.78, description: "Impressive! Just a few word choices to refine.", stars: "★★★★☆" },
        { label: "Native-like",         threshold: 0.90, description: "Flawless! A translator would be proud.", stars: "★★★★★" },
    ],
    answering: [
        { label: "Lost in Translation", threshold: 0,    description: "Your answer is still finding its footing—keep going!", stars: "☆☆☆☆☆" },
        { label: "Tourist Mode",        threshold: 0.35, description: "You're on the right track, but the answer needs more.", stars: "★☆☆☆☆" },
        { label: "Confident Speaker",   threshold: 0.55, description: "Your answer makes sense—good job!", stars: "★★★☆☆" },
        { label: "Almost Native",       threshold: 0.72, description: "Great answer! Just a little more detail or accuracy.", stars: "★★★★☆" },
        { label: "Native-like",         threshold: 0.88, description: "Flawless! A model answer through and through.", stars: "★★★★★" },
    ],
    conversation: [
        { label: "Lost in Translation", threshold: 0,    description: "The conversation is still a challenge—keep practicing!", stars: "☆☆☆☆☆" },
        { label: "Tourist Mode",        threshold: 0.30, description: "You're joining the conversation, but it's a bit bumpy.", stars: "★☆☆☆☆" },
        { label: "Confident Speaker",   threshold: 0.50, description: "You're holding your own in the conversation!", stars: "★★★☆☆" },
        { label: "Almost Native",       threshold: 0.68, description: "Natural and fluent—almost indistinguishable!", stars: "★★★★☆" },
        { label: "Native-like",         threshold: 0.85, description: "Flawless! You'd fit right into any conversation.", stars: "★★★★★" },
    ],
    essay: [
        { label: "Lost in Translation", threshold: 0,    description: "Your essay is still taking shape—keep writing!", stars: "☆☆☆☆☆" },
        { label: "Tourist Mode",        threshold: 0.25, description: "You're expressing ideas, but clarity needs work.", stars: "★☆☆☆☆" },
        { label: "Confident Speaker",   threshold: 0.45, description: "Your essay communicates well—nice work!", stars: "★★★☆☆" },
        { label: "Almost Native",       threshold: 0.65, description: "Impressive writing! A few refinements and it'll shine.", stars: "★★★★☆" },
        { label: "Native-like",         threshold: 0.82, description: "Flawless! A beautifully written, compelling essay.", stars: "★★★★★" },
    ],
};

export function getLevelForScore(score: number, exerciseType: string) {
    const levels = EXERCISE_LEVELS[exerciseType] ?? EXERCISE_LEVELS["translate"];
    return (
        [...levels]
            .sort((a, b) => b.threshold - a.threshold)
            .find((l) => score >= l.threshold)
        ?? { label: "Unknown", description: "No feedback available.", stars: "☆☆☆☆☆" }
    );
}