function ProgressBar({ score }) {
  const percent = Math.min(score, 100);

  return (
    <div className="w-full bg-white border-2 border-black rounded-lg h-4 overflow-hidden">
      <div
        className="h-full bg-black rounded transition-all"
        style={{ width: `${percent}%` }}
      />
    </div>
  );
}

export default ProgressBar;