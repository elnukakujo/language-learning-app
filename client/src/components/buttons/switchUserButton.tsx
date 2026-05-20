"use client";

import { clearUserCookie } from "@/utils/user_cookie";

export default function SwitchUserButton() {
    return (
        <button 
            className="border-2 rounded px-4 py-2"
            onClick={() => clearUserCookie()}
        >
            Switch User
        </button>
    );
}