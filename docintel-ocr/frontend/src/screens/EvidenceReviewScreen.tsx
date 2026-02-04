import { useState } from "react";
import api from "../services/api";


export default function EvidenceReviewScreen() {

  const [q, setQ] = useState("");
  const [ans, setAns] = useState("");
  const [loading, setLoading] = useState(false);


  async function handleAsk() {

    if (!q) return;

    setLoading(true);

    const res = await api.post("/ask", {
      question: q
    });

    setAns(res.data.result);

    setLoading(false);
  }


  return (

    <div>

      <h2 className="section-title">
        Evidence Review
      </h2>


      <div className="card">

        <textarea
          rows={3}
          placeholder="Explain Phase II..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />


        <button
          onClick={handleAsk}
          className="btn btn-green"
        >
          Ask AI
        </button>

      </div>


      <div className="card">

        <h3 className="section-title">
          Answer & Citation
        </h3>


        {loading && <p>Processing...</p>}


        <pre className="answer-box">

          {ans || "No answer yet"}

        </pre>

      </div>

    </div>
  );
}
