import { useEffect, useState } from "react";
import { getTopics, addRevision } from "../api/revision";
import { getToken } from "../api/auth";
import TopicCard from "../components/TopicCard";

function Topics() {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadTopics() {
      try {
        const data = await getTopics(getToken());
        // Backend returns array directly, not { topics: [...] }
        setTopics(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Error loading topics:", error);
        setTopics([]);
      } finally {
        setLoading(false);
      }
    }
    loadTopics();
  }, []);

  async function handleRevise(topicId, confidence) {
    try {
      const result = await addRevision(getToken(), topicId, confidence);
      if (result.detail) {
        alert(`Error: ${result.detail}`);
        return;
      }
      alert("Revision saved");
      // Optionally reload topics to show updated data
      window.location.reload();
    } catch (error) {
      console.error("Error saving revision:", error);
      alert("Failed to save revision");
    }
  }

  if (loading) {
    return (
      <div className="rounded-lg border-2 border-black p-6 bg-white text-black text-center">
        Loading topics...
      </div>
    );
  }

  return (
    <div className="w-full">
      <h2 className="text-2xl font-bold text-black mb-6">Your Topics</h2>

      {(!topics || topics.length === 0) && (
        <div className="rounded-lg border-2 border-black p-6 bg-white text-black text-center">
          No topics yet.
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {topics && topics.map((topic) => (
          <TopicCard
            key={topic.id}
            topic={topic}
            onRevise={handleRevise}
          />
        ))}
      </div>
    </div>
  );
}

export default Topics;
