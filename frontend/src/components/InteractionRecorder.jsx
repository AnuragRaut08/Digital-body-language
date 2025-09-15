import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import ResultCard from "./ResultCard";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000/v1/interaction";

export default function InteractionRecorder() {
  const [text, setText] = useState("");
  const [events, setEvents] = useState([]);
  const [result, setResult] = useState(null);

  const startTime = useRef(null);
  const lastTypeTime = useRef(null);
  const totalChars = useRef(0);
  const totalPause = useRef(0);
  const pauseCount = useRef(0);
  const backspaceCount = useRef(0);
  const clickCount = useRef(0);
  const scrollMax = useRef(0);

  useEffect(() => {
    const onClick = () => clickCount.current++;
    window.addEventListener("click", onClick);
    const onScroll = () => {
      const doc = document.documentElement;
      const scrollPct = (doc.scrollTop / (doc.scrollHeight - doc.clientHeight)) * 100;
      if (!isNaN(scrollPct)) scrollMax.current = Math.max(scrollMax.current, scrollPct);
    };
    window.addEventListener("scroll", onScroll);
    return () => {
      window.removeEventListener("click", onClick);
      window.removeEventListener("scroll", onScroll);
    };
  }, []);

  function handleChange(e) {
    const now = performance.now();
    if (!startTime.current) startTime.current = now;
    if (lastTypeTime.current) {
      const diff = now - lastTypeTime.current;
      if (diff > 300) { // treat >300ms as pause
        totalPause.current += diff;
        pauseCount.current += 1;
      }
    }
    lastTypeTime.current = now;

    const newText = e.target.value;
    const charsAdded = Math.max(0, newText.length - totalChars.current);
    const charsRemoved = Math.max(0, totalChars.current - newText.length);
    backspaceCount.current += charsRemoved;
    totalChars.current = newText.length;
    setText(newText);
  }

  async function handleSubmit() {
    const durationSec = ((performance.now() - startTime.current) || 1) / 1000;
    const typing_speed = totalChars.current / Math.max(1, durationSec);
    const avg_pause_ms = pauseCount.current ? totalPause.current / pauseCount.current : 0;
    const backspace_rate = totalChars.current ? (backspaceCount.current / totalChars.current) : 0;
    const scroll_depth_pct = scrollMax.current;
    const click_rate_per_min = (clickCount.current / Math.max(0.01, durationSec)) * 60;

    const payload = {
      user_id: "demo_user",
      session_id: "session_demo",
      typing_speed_chars_per_sec: typing_speed,
      avg_pause_ms,
      backspace_rate,
      scroll_depth_pct,
      click_rate_per_min,
      timestamp: Date.now()
    };

    try {
      const { data } = await axios.post(BACKEND_URL, payload, { timeout: 5000 });
      setResult(data);
    } catch (err) {
      setResult({ error: err.message });
    }
  }

  function resetAll() {
    setText("");
    setEvents([]);
    setResult(null);
    startTime.current = null;
    lastTypeTime.current = null;
    totalChars.current = 0;
    totalPause.current = 0;
    pauseCount.current = 0;
    backspaceCount.current = 0;
    clickCount.current = 0;
    scrollMax.current = 0;
  }

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <textarea
        value={text}
        onChange={handleChange}
        rows={6}
        className="w-full p-3 border rounded focus:outline-none"
        placeholder="Write a message to your potential match... try to type naturally, scroll the page, click around."
      />
      <div className="flex gap-3 mt-3">
        <button onClick={handleSubmit} className="px-4 py-2 rounded bg-pink-500 text-white">Send & Analyze</button>
        <button onClick={resetAll} className="px-4 py-2 rounded border">Reset</button>
      </div>

      <div className="mt-4">
        {result ? (
          result.error ? (
            <div className="text-red-500">Error: {result.error}</div>
          ) : (
            <ResultCard result={result} />
          )
        ) : (
          <div className="text-sm text-gray-500">No analysis yet. Interact and press <b>Send & Analyze</b>.</div>
        )}
      </div>
    </div>
  );
}

