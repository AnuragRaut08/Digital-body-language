import React from "react";
import Layout from "./components/Layout";
import InteractionRecorder from "./components/InteractionRecorder";

export default function App() {
  return (
    <Layout>
      <div className="max-w-3xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-4">Digital Body Language — Demo</h1>
        <p className="mb-6 text-gray-600">Type into the box below and scroll. This demo collects typing & scroll signals and returns an engagement score.</p>
        <InteractionRecorder />
      </div>
    </Layout>
  );
}

