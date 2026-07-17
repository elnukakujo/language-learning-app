import { Ring } from "ldrs/react";
import "ldrs/react/Ring.css";

type SubmitButtonProps = {
  children?: React.ReactNode;
  isLoading?: boolean;
};

export default function SubmitButton({ children, isLoading }: SubmitButtonProps) {
  return (
    <button type="submit" className="btn btn-primary" disabled={isLoading}>
      {isLoading ? <Ring size={16} color="#fff" /> : children || "Save"}
    </button>
  );
}
