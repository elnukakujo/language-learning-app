"use client";

import { useEffect, useState } from "react";

import AutoWidthInput from "@/components/ui/input/autoWidthInput";

export default function DiscreteInput({ value, setValue, label, is2D=false }: { value: string, setValue: (val: string) => void, label: string, is2D?: boolean }) {
    const [values, setValues] = useState<string[][]>([[""]]);

    const handleUpdate = (rowIndex: number, colIndex: number, value: string) => {
        const newValues = [...values];
        newValues[rowIndex][colIndex] = value;
        setValues(newValues);
        setValue(newValues.map(line => line.join('__')).join('\n'));
    };

    const handleAddRow = () => {
        setValues([...values, [""]]);
    };

    const handleRemoveRow = (rowIndex: number) => {
        const newValues = values.filter((line, i) => i !== rowIndex);
        setValues(newValues);
    };

    const handleAddColumn = (rowIndex: number) => {
        const newValues = values.map((line, i) => i === rowIndex ? [...line, ""] : line);
        setValues(newValues);
    };
    const handleRemoveColumn = (rowIndex: number, colIndex: number) => {
        const newValues = values.map((line, i) => i === rowIndex ? line.filter((_, j) => j !== colIndex) : line);
        setValues(newValues);
    };

    useEffect(() => {
        setValues(value.split("\n").map(line => line.split("__")));
    }, [value]);

    return (
        <span>
            {label && 
                <label 
                htmlFor={label.toLowerCase().replace(/\s+/g, '-')}
                className="text-sm font-medium text-foreground"
                >
                {label}
                </label>
            }
            <article className="max-w-[25rem] flex flex-col items-center space-y-2">
                {values.map((line, rowIndex) => (
                    <span key={rowIndex} className="flex flex-wrap flex-row items-center space-x-2 space-y-2">
                        {values.length > 1 && <button
                            type="button"
                            onClick={() => handleRemoveRow(rowIndex)}
                            className="btn btn-secondary px-2 py-1">
                            x
                        </button>}
                        {line.map((part, colIndex) => (
                            <span key={colIndex} className="flex flex-col space-y-1 items-center">
                                {line.length > 1 && <button
                                    type="button"
                                    onClick={() => handleRemoveColumn(rowIndex, colIndex)}
                                    className="btn btn-secondary px-2 py-1 text-sm size-fit">
                                    x
                                </button>}
                                <AutoWidthInput
                                    value={part}
                                    onChange={(val) => handleUpdate(rowIndex, colIndex, val.target.value)}
                                    minWidth={4}
                                />
                            </span>
                        ))}
                        <button
                            type="button"
                            onClick={() => handleAddColumn(rowIndex)}
                            className="btn btn-secondary px-2 py-1">
                            +
                        </button>
                    </span>
                ))}
                {is2D &&
                    <button type="button" onClick={() => handleAddRow()} className="btn btn-secondary w-full">
                        +
                    </button>
                }
            </article>
        </span>
    );
}
