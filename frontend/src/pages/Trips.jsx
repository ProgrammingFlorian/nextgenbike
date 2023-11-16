import { useState } from "react";

export default function Homepage() {
  const [keyword, setKeyword] = useState("");

  return (
    <div className="p-9 mt-4">
      {/* Welcome Message */}
      <div className="flex flex-col gap-0.5">
        <h1 className="text-2xl font-bold">Your Recent Trips</h1>
      </div>

      {/* Search Bar */}
      <input
        className="text-sm py-2 px-4 mt-8 border border-gray w-full rounded-lg"
        type="text"
        value={keyword}
        placeholder="Search Trip ..."
        onChange={(e) => setKeyword(e.target.value)}
      />

      {/* Render Small Items */}
    </div>
  );
}
