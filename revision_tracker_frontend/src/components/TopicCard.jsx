import { useState } from "react";

function TopicCard({ topic, onRevise }) {
  const [confidence, setConfidence] = useState(3);

  return (
    <div className="rounded-lg border-2 border-black p-4 bg-white">
      <h4 className="text-lg font-semibold text-black mb-2">{topic.name}</h4>

      <p className="text-sm text-black mb-2">
        {topic.subject}
        {topic.unit && <span className="text-gray-600"> • {topic.unit}</span>}
      </p>

      <p className="text-sm text-black mb-3">
        Difficulty: <strong>{topic.difficulty}</strong> | Importance:{" "}
        <strong>{topic.importance}</strong>
      </p>

      <div className="mt-3 mb-3">
        <label className="text-sm text-black block mb-2">
          Confidence: <strong>{confidence}</strong>
        </label>

        <input
          type="range"
          min="1"
          max="5"
          value={confidence}
          onChange={(e) => setConfidence(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <button
        className="w-full mt-3 px-4 py-2 rounded-lg border-2 border-black text-black font-medium bg-white hover:bg-gray-100 transition-all"
        onClick={() => onRevise(topic.id, confidence)}
      >
        Mark Revised
      </button>
    </div>
  );
}

export default TopicCard;
