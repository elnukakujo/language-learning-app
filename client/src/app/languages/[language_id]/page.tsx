export default async function Language({ params }: { params: { language_id: string } }) {
    const { language_id } = await params;

    return (
        <div>
            <h1>Language Details</h1>
            <p>Language ID: {language_id}</p>
        </div>
    );
}