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
            <section className="flex flex-col gap-2 rounded-lg border border-white/10 bg-white/5 p-4 text-sm shadow-sm">
                <div className="flex items-center justify-between gap-4">
                    <h4 className="text-sm font-medium uppercase tracking-wide opacity-80">Commitment</h4>
                </div>
                <div className="text-xs opacity-60">No commitment data</div>
            </section>
        )
    }

    return (
        <section className="flex flex-col gap-2 rounded-lg border border-white/10 bg-white/5 p-4 text-sm shadow-sm">
            <div className="flex items-center justify-between gap-4">
                <h4 className="text-sm font-medium uppercase tracking-wide opacity-80">Commitment</h4>
                <span className="text-xs opacity-60">Last updated {new Date(commitmentLog.streak_last_computed_at).toLocaleString()}</span>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                <div>
                    <p className="text-xs uppercase opacity-50">Days Active</p>
                    <p className="text-base font-semibold">{commitmentLog.days_active}</p>
                </div>
                <div>
                    <p className="text-xs uppercase opacity-50">Total Items Reviewed</p>
                    <p className="text-base font-semibold">{commitmentLog.total_items_reviewed}</p>
                </div>
                <div>
                    <p className="text-xs uppercase opacity-50">Total Time Studied</p>
                    <p className="text-base font-semibold">{formatMs(commitmentLog.total_time_ms)}</p>
                </div>
                <div>
                    <p className="text-xs uppercase opacity-50">Longest Streak</p>
                    <p className="text-base font-semibold">{commitmentLog.longest_streak_ever}</p>
                </div>
                <div>
                    <p className="text-xs uppercase opacity-50">Last Updated</p>
                    <p className="text-base font-semibold">{new Date(commitmentLog.streak_last_computed_at).toLocaleString()}</p>
                </div>
            </div>
        </section>
    )
}
