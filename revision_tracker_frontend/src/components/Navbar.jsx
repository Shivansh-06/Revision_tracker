function Navbar({ currentPage, setPage, onLogout }) {
  return (
    <nav className="flex flex-wrap items-center gap-4 px-4 py-3 border-b-2 border-black mb-6 bg-white">
      <button
        className={`px-4 py-2 rounded-lg border-2 border-black text-black font-medium transition-all ${
          currentPage === "queue"
            ? "bg-black text-white"
            : "bg-white hover:bg-gray-100"
        }`}
        onClick={() => setPage("queue")}
      >
        Revision Queue
      </button>

      <button
        className={`px-4 py-2 rounded-lg border-2 border-black text-black font-medium transition-all ${
          currentPage === "topics"
            ? "bg-black text-white"
            : "bg-white hover:bg-gray-100"
        }`}
        onClick={() => setPage("topics")}
      >
        Topics
      </button>

      <button
        className={`px-4 py-2 rounded-lg border-2 border-black text-black font-medium transition-all ${
          currentPage === "syllabus"
            ? "bg-black text-white"
            : "bg-white hover:bg-gray-100"
        }`}
        onClick={() => setPage("syllabus")}
      >
        Syllabus
      </button>

      <div className="flex-1" />

      <button
        className="px-4 py-2 rounded-lg border-2 border-black text-black font-medium bg-white hover:bg-gray-100 transition-all"
        onClick={onLogout}
      >
        Logout
      </button>
    </nav>
  );
}

export default Navbar;
