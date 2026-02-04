import { useState } from "react";
import api from "../services/api";


export default function TrialOverviewScreen() {

  const [file, setFile] = useState<File | null>(null);


  async function upload() {

    if (!file) return;

    const form = new FormData();
    form.append("file", file);

    await api.post("/upload", form);

    alert("Document Uploaded");
  }


  return (

    <div>

      <h2 className="section-title">
        Trial Documents
      </h2>


      <div className="card">

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />


        <button
          onClick={upload}
          className="btn"
        >
          Upload Protocol
        </button>

      </div>

    </div>
  );
}
