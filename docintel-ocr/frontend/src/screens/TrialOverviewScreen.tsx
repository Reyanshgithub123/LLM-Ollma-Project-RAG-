import { useEffect, useState } from "react";
import api, { getRecentUploads } from "../services/api";
import "../audit.css";

export default function TrialOverviewScreen() {

  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState("");

  const [recentFiles, setRecentFiles] = useState<any[]>([]);


  /* ================= LOAD RECENT UPLOADS ================= */

  async function loadRecent() {

    try {

      const res = await getRecentUploads();
      setRecentFiles(res.data);

    } catch (e) {

      console.error("Failed to load recent uploads", e);

    }
  }


  useEffect(() => {

    loadRecent();

    const t = setInterval(loadRecent, 5000);

    return () => clearInterval(t);

  }, []);


  /* ================= UPLOAD ================= */

  async function upload() {

    if (!file || loading) return;

    setLoading(true);
    setSuccessMsg("");

    try {

      const form = new FormData();
      form.append("file", file);

      await api.post("/upload", form);

      setSuccessMsg(`✅ ${file.name} successfully added`);

      setFile(null);

      // Refresh list after upload
      loadRecent();

    } catch (err) {

      alert("Upload failed. Try again.");

    } finally {

      setLoading(false);
    }
  }


  /* ================= TIME AGO ================= */

  function timeAgo(time: string) {

    const now = Date.now();
    const t = Date.parse(time);

    if (isNaN(t)) return "Just now";

    const diff = Math.floor((now - t) / 1000);

    if (diff < 60) return "Just now";

    if (diff < 3600)
      return `${Math.floor(diff / 60)} min ago`;

    if (diff < 86400)
      return `${Math.floor(diff / 3600)} hours ago`;

    return `${Math.floor(diff / 86400)} days ago`;
  }


  return (

    <div>

      <h2 className="section-title">
        Trial Documents
      </h2>


      {/* ================= UPLOAD CARD ================= */}

      <div className="card space-y-4 mb-6">

        {/* File Input */}
        <input
          type="file"
          accept=".pdf"
          disabled={loading}
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />


        {/* Upload Button */}
        <button
          onClick={upload}
          disabled={loading || !file}
          className="btn"
        >
          {loading ? "Uploading..." : "Upload Protocol"}
        </button>


        {/* Loader */}
        {loading && (
          <div className="upload-loader">
            ⏳ Uploading document, please wait...
          </div>
        )}


        {/* Success Message */}
        {successMsg && (
          <div className="upload-success">
            {successMsg}
          </div>
        )}

      </div>


      {/* ================= RECENT UPLOADS ================= */}

      <div className="card">

        <h3 className="section-title">
          Recent Uploads
        </h3>


        {recentFiles.length === 0 && (
          <div className="text-gray-500 text-sm text-center py-4">
            No uploads yet
          </div>
        )}


        {recentFiles.map((f, i) => (

          <div key={i} className="recent-row">

  <div className="recent-left">

    <div className="file-icon">📄</div>

    <div className="recent-info">

      <div className="recent-name">
        {f.name}
      </div>

      <div className="recent-time">
        {timeAgo(f.time)}
      </div>

    </div>

  </div>

</div>


        ))}

      </div>

    </div>
  );
}
