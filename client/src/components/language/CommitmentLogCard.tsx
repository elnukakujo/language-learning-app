"use client"
import type CommitmentLog from "@/interface/dataCollection/CommitmentLog"

export default function CommitmentLogCard({ commitmentLog }: { commitmentLog: CommitmentLog | null }) {
    function formatMs(ms: number) {
        const totalMinutes = Math.floor(ms / 60000)
        const hours = Math.floor(totalMinutes / 60)
        const minutes = totalMinutes % 60
        return `${hours}h ${minutes}m`
    }

    if (!commitmentLog) {
        return (
            <section className="flex flex-col gap-2 text-sm">
                <div className="flex items-center justify-between gap-4">
                    <h4 className="font-serif text-base text-ink">Commitment</h4>
                </div>
                <div className="text-xs text-muted">No commitment data</div>
            </section>
        )
    }

    return (
        <section className="flex flex-col gap-3 text-sm">
            <div className="flex items-center justify-between gap-4">
                <h4 className="font-serif text-base text-ink">Commitment</h4>
                <span className="text-xs text-muted">Last updated {new Date(commitmentLog.updated_at ?? commitmentLog.created_at).toLocaleString()}</span>
            </div>

            <div className="flex flex-row gap-3 overflow-x-auto">
                <div className="card flex flex-1 min-w-[7rem] flex-col gap-2">
                    <p className="text-xs uppercase tracking-wide text-muted">Days Active</p>
                    <div className="index-divider" />
                    <p className="stat-value">{commitmentLog.days_active}</p>
                </div>
                <div className="card flex flex-1 min-w-[7rem] flex-col gap-2">
                    <p className="text-xs uppercase tracking-wide text-muted">Total Items Reviewed</p>
                    <div className="index-divider" />
                    <p className="stat-value">{commitmentLog.total_items_reviewed}</p>
                </div>
                <div className="card flex flex-1 min-w-[7rem] flex-col gap-2">
                    <p className="text-xs uppercase tracking-wide text-muted">Total Time Studied</p>
                    <div className="index-divider" />
                    <p className="stat-value">{formatMs(commitmentLog.total_time_ms)}</p>
                </div>
                <div className="card flex flex-1 min-w-[7rem] flex-col gap-2">
                    <p className="text-xs uppercase tracking-wide text-muted">Longest Streak</p>
                    <div className="index-divider" />
                    <p className="stat-value">{commitmentLog.longest_streak_ever}</p>
                </div>
                <div className="card flex flex-1 min-w-[7rem] flex-col gap-2">
                    <p className="text-xs uppercase tracking-wide text-muted">Last Updated</p>
                    <div className="index-divider" />
                    <p className="text-sm font-medium">{new Date(commitmentLog.updated_at ?? commitmentLog.created_at).toLocaleString()}</p>
                </div>
            </div>
        </section>
    )
}
