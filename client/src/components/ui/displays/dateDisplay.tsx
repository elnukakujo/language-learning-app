type DateDisplayProps = {
	date?: string | Date | null;
	locale?: string;
	options?: Intl.DateTimeFormatOptions;
	fallback?: string;
    message?: string;
};

const defaultOptions: Intl.DateTimeFormatOptions = {
	year: "numeric",
	month: "short",
	day: "2-digit",
};

function formatDate(
	date: string | Date | null | undefined,
	locale?: string,
	options?: Intl.DateTimeFormatOptions,
): string | null {
	if (!date) return null;

	const parsed = date instanceof Date ? date : new Date(date);
	if (Number.isNaN(parsed.getTime())) return null;

	return new Intl.DateTimeFormat(locale, options ?? defaultOptions).format(parsed);
}

export default function DateDisplay({
	date,
	locale,
	options,
	fallback = "-",
    message
}: DateDisplayProps) {
	const formattedDate = formatDate(date, locale, options);

	return (
		<div className="inline-flex items-center gap-2">
			{message && <span className="text-sm text-muted">{message}</span>}
			<span className="text-sm">{formattedDate ?? fallback}</span>
		</div>
	);
}
