type UpdateButtonProps = {
    children?: React.ReactNode;
};

export default function UpdateButton({ children }: UpdateButtonProps) {

    return (
        <button type="submit" className="bg-blue-500 text-white rounded-md p-2">
            {children||"Update the element"}
        </button>
    );
}