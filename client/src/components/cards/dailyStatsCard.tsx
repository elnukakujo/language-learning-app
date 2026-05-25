"use client";

import type DailyStats from "@/interface/dataCollection/DailyStats";

export default function DailyStatsCard({ dailyStats }: { dailyStats: DailyStats }) {
    const studiedMinutes = Math.round(dailyStats.time_studied_ms / 60000);
    const accuracy = dailyStats.items_reviewed > 0
        ? Math.round((dailyStats.items_correct / dailyStats.items_reviewed) * 100)
        : 0;

    return (
        <section className="flex flex-col gap-2 rounded-lg border border-white/10 bg-white/5 p-4 text-sm shadow-sm">
            <div className="flex items-center justify-between gap-4">
                <h4 className="text-sm font-medium uppercase tracking-wide opacity-80">Daily Stats</h4>
                <span className="text-xs opacity-60">{dailyStats.streak_day ? "Streak day" : "Building streak"}</span>
            </div>

            <div className="grid grid-cols-2 gap-3">
                <div>
                    <p className="text-xs uppercase opacity-50">Reviewed</p>
                    <p className="text-base font-semibold">{dailyStats.items_reviewed}</p>
                </div>
                <div>
                    <p className="text-xs uppercase opacity-50">Correct</p>
                    <p className="text-base font-semibold">{dailyStats.items_correct}</p>
                </div>
                <div>
                    <p className="text-xs uppercase opacity-50">Accuracy</p>
                    <p className="text-base font-semibold">{accuracy}%</p>
                </div>
                <div>
                    <p className="text-xs uppercase opacity-50">Study time</p>
                    <p className="text-base font-semibold">{studiedMinutes} min</p>
                </div>
            </div>

            <div className="flex items-center justify-between text-xs opacity-70">
                <span>Current streak</span>
                <span>{dailyStats.current_streak_length}</span>
            </div>
        </section>
    );
}