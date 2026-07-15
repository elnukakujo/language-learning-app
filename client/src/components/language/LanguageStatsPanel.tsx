"use client"
import React, { useState } from "react"
import type DailyStats from "@/interface/dataCollection/DailyStats"
import type CommitmentLog from "@/interface/dataCollection/CommitmentLog"
import DailyStatsCard from "./dailyStatsCard"
import CommitmentLogCard from "./CommitmentLogCard"
import PracticeHeatmap from "./practiceHeatmap"

export default function LanguageStatsPanel({ dailyStats, commitmentLog, history }: { dailyStats: DailyStats | null, commitmentLog: CommitmentLog | null, history: DailyStats[] }) {
    const [view, setView] = useState<'daily' | 'commitment' | 'history'>(dailyStats ? 'daily' : 'commitment')

    return (
        <div className="flex flex-col gap-3">
            <div className="btn-row border-b border-dashed border-[var(--border)] pb-2">
                <button
                    className={`btn ${view === 'daily' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setView('daily')}
                >Daily</button>
                <button
                    className={`btn ${view === 'commitment' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setView('commitment')}
                >Commitment</button>
                <button
                    className={`btn ${view === 'history' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setView('history')}
                >History</button>
            </div>

            <div>
                {view === 'daily' && <DailyStatsCard dailyStats={dailyStats!} />}
                {view === 'commitment' && <CommitmentLogCard commitmentLog={commitmentLog!} />}
                {view === 'history' && <PracticeHeatmap history={history} />}
            </div>
        </div>
    )
}
