import { useState } from "react";
import { parseSyllabus, bulkCreateTopics } from "../api/syllabus";
import { getToken } from "../api/auth";

function Syllabus() {
  const [text, setText] = useState("");
  const [preview, setPreview] = useState([]);
  const [loading, setLoading] = useState(false);

  async function handleParse() {
    setLoading(true);
    try {
      const data = await parseSyllabus(getToken(), text);
      if (data.detail) {
        alert(`Error: ${data.detail}`);
        setPreview([]);
      } else {
        setPreview(data?.topics || []);
      }
    } catch (error) {
      console.error("Error parsing syllabus:", error);
      alert("Failed to parse syllabus. Please try again.");
      setPreview([]);
    } finally {
      setLoading(false);
    }
  }

  async function handleConfirm() {
    try {
      const result = await bulkCreateTopics(getToken(), preview);
      if (result.detail) {
        alert(`Error: ${result.detail}`);
        return;
      }
      alert("Topics saved successfully");
      setText("");
      setPreview([]);
    } catch (error) {
      console.error("Error saving topics:", error);
      alert("Failed to save topics. Please try again.");
    }
  }

  return (
    <div className="w-full max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold text-black mb-6">Syllabus Input</h2>

      <div className="rounded-lg border-2 border-black p-6 bg-white mb-4">
        <textarea
          rows={8}
          className="w-full px-4 py-2 rounded-lg border-2 border-black text-black placeholder-gray-500 bg-white focus:outline-none focus:ring-2 focus:ring-black resize-none"
          placeholder="Paste your syllabus here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      </div>

      <button 
        onClick={handleParse} 
        disabled={loading || !text}
        className="px-4 py-2 rounded-lg border-2 border-black text-black font-medium bg-white hover:bg-gray-100 transition-all disabled:opacity-50 disabled:cursor-not-allowed mb-6"
      >
        {loading ? "Parsing..." : "Parse Syllabus"}
      </button>

      {preview && preview.length > 0 && (
        <div className="mt-6">
          <h3 className="text-xl font-bold text-black mb-4">Preview Topics</h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            {preview.map((topic, idx) => (
              <div 
                key={idx}
                className="rounded-lg border-2 border-black p-4 bg-white"
              >
                <p className="text-black">
                  <strong>{topic.subject}</strong> — {topic.name}
                </p>
                {topic.unit && (
                  <p className="text-sm text-gray-600">
                    {topic.unit}
                  </p>
                )}
                <p className="text-sm text-black mt-1">
                  (difficulty: {topic.difficulty}, importance: {topic.importance})
                </p>
              </div>
            ))}
          </div>

          <button 
            onClick={handleConfirm}
            className="px-4 py-2 rounded-lg border-2 border-black text-black font-medium bg-white hover:bg-gray-100 transition-all"
          >
            Confirm & Save Topics
          </button>
        </div>
      )}
    </div>
  );
}

export default Syllabus;
