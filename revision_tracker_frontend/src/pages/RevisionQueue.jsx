import { useEffect, useState } from "react";
import { getRevisionQueue } from "../api/revision";
import { getToken } from "../api/auth";
import ProgressBar from "../components/ProgressBar";

function RevisionQueue() {
  const [queue, setQueue] = useState([]);

  useEffect(() => {
    async function load() {
      try {
        const data = await getRevisionQueue(getToken());
        // Backend returns array directly, not { revision_queue: [...] }
        setQueue(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Error loading revision queue:", error);
        setQueue([]);
      }
    }
    load();
  }, []);

  return (
    <div className="w-full">
      <h2 className="text-2xl font-bold text-black mb-6">Revision Queue</h2>

      {(!queue || queue.length === 0) && (
        <div className="rounded-lg border-2 border-black p-6 bg-white text-black text-center">
          No items in revision queue
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {queue && queue.map((item, index) => (
          <div 
            key={item.id || index}
            className="rounded-lg border-2 border-black p-4 bg-white"
          >
            <h4 className="text-lg font-semibold text-black mb-2">{item.name || item.topic || "Topic"}</h4>

            <p className="text-sm text-black mb-2">
              Subject: {item.subject || "N/A"}
            </p>

            {item.unit && (
              <p className="text-sm text-black mb-2">
                Unit: {item.unit}
              </p>
            )}

            <div className="mb-2">
              <p className="text-xs text-black mb-1">Priority: {item.priority?.toFixed(2) || "N/A"}</p>
              <ProgressBar score={(item.priority || 0) * 100} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RevisionQueue;
