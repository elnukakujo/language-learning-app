"use client"
import React, { useState } from "react"
import type DailyStats from "@/interface/dataCollection/DailyStats"
import type CommitmentLog from "@/interface/dataCollection/CommitmentLog"
import DailyStatsCard from "./dailyStatsCard"
import CommitmentLogCard from "./CommitmentLogCard"

export default function LanguageStatsPanel({ dailyStats, commitmentLog }: { dailyStats: DailyStats | null, commitmentLog: CommitmentLog | null }) {
    const [view, setView] = useState<'daily' | 'commitment'>(dailyStats ? 'daily' : 'commitment')

    return (
        <div className="flex flex-col gap-3">
            <div className="flex items-center gap-2">
                <button
                    className={`px-3 py-1 rounded-md text-sm ${view === 'daily' ? 'bg-amber-500 text-black' : 'bg-white/5'}`}
                    onClick={() => setView('daily')}
                >Daily</button>
                <button
                    className={`px-3 py-1 rounded-md text-sm ${view === 'commitment' ? 'bg-amber-500 text-black' : 'bg-white/5'}`}
                    onClick={() => setView('commitment')}
                >Commitment</button>
            </div>

            <div>
                {view === 'daily' ? <DailyStatsCard dailyStats={dailyStats!} /> : <CommitmentLogCard commitmentLog={commitmentLog!} />}
            </div>
        </div>
    )
}
