"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import BackButton from "@/components/buttons/backButton";
import SearchBar from "@/components/searchBar";
import { clearUserCookie } from "@/utils/user_cookie";

const primaryLinks = [
	{ href: "/", label: "Home" },
	{ href: "/sources", label: "Sources" },
	{ href: "/tags", label: "Tags" },
];

export default function NavBar({ currentUserId }: { currentUserId: string | null }) {
	const pathname = usePathname();

	const isActive = (href: string) => {
		if (href === "/") {
			return pathname === "/";
		}

		return pathname === href || pathname.startsWith(`${href}/`);
	};

	return (
		<header className="sticky top-0 z-50 border-b border-black/10 bg-[linear-gradient(135deg,rgba(247,245,238,0.92),rgba(238,244,255,0.88))] backdrop-blur-md">
			<div className="mx-auto flex w-full max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-6 lg:px-8">
				<div className="flex items-center gap-3">
					<div className={pathname === "/" ? "invisible pointer-events-none" : "visible"}>
						<BackButton />
					</div>
					<Link href="/" className="flex flex-col leading-tight">
						<span className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">
							Language Lab
						</span>
						<span className="text-base font-medium text-slate-900">
							Learn with structure
						</span>
					</Link>
				</div>

				<nav className="flex items-center gap-1 overflow-x-auto rounded-full border border-black/10 bg-white/70 p-1 shadow-sm">
					{primaryLinks.map((link) => {
						const active = isActive(link.href);

						return (
							<Link
								key={link.href}
								href={link.href}
								aria-current={active ? "page" : undefined}
								className={`whitespace-nowrap rounded-full px-4 py-2 text-sm font-medium transition-colors ${
									active
										? "bg-slate-900 text-white shadow-sm"
										: "text-slate-600 hover:bg-slate-900/5 hover:text-slate-900"
								}`}
							>
								{link.label}
							</Link>
						);
					})}
				</nav>
				<div className="min-w-0 flex-1">
					<SearchBar currentUserId={currentUserId} />
				</div>
                <div className={`flex items-center gap-2 ${currentUserId ? "visible" : "invisible pointer-events-none"}`}>
                    <button
                        type="button"
                        onClick={() => void clearUserCookie()}
                        className="inline-flex shrink-0 items-center gap-2 rounded-full border border-slate-900/10 bg-white/80 px-4 py-2 text-sm font-semibold text-slate-800 shadow-sm transition-colors hover:bg-white"
                    >
                        Switch User
                    </button>
                    <Link
                        href={`/user/${currentUserId}/update`}
                        className="inline-flex shrink-0 items-center gap-2 rounded-full border border-slate-900/10 bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-sm transition-transform duration-200 hover:-translate-y-0.5"
                    >
                        Settings
                    </Link>
                </div>
			</div>
		</header>
	);
}
