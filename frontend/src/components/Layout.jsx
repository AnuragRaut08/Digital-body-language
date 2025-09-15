import React from "react";

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-pink-50 to-white">
      <header className="py-6 bg-white shadow-sm">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">LoveOS — Digital Body Language</h2>
            <div className="text-sm text-gray-500">Build to Bond — HackBees</div>
          </div>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}

