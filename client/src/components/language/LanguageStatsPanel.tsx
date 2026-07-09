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
            <div className="flex items-center gap-2 border-b border-dashed border-[var(--border)] pb-2">
                <button
                    className={`btn ${view === 'daily' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setView('daily')}
                >Daily</button>
                <button
                    className={`btn ${view === 'commitment' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setView('commitment')}
                >Commitment</button>
            </div>

            <div>
                {view === 'daily' ? <DailyStatsCard dailyStats={dailyStats!} /> : <CommitmentLogCard commitmentLog={commitmentLog!} />}
            </div>
        </div>
    )
}
