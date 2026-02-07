type NewElementButtonProps = {
  children?: React.ReactNode;
};

export default function NewElementButton({ children }: NewElementButtonProps) {
  return (
    <button 
      type="submit" 
      className="bg-blue-500 text-white rounded-md p-2"
    >
      {children || "Add new element"}
    </button>
  );
}