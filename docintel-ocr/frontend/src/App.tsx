import "./App.css";

import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

import TrialOverviewScreen from "./screens/TrialOverviewScreen";
import ProtocolChangesScreen from "./screens/ProtocolChangesScreen";
import EvidenceReviewScreen from "./screens/EvidenceReviewScreen";
import AuditTrailScreen from "./screens/AuditTrailScreen";


export default function App() {

  return (

    <BrowserRouter>

      <div className="app-container">

        {/* NAV */}
        <div className="navbar">

          <h1>Clinical Trial Intelligence</h1>

          <div className="nav-links">

            <Link to="/">Trial</Link>
            <Link to="/changes">Changes</Link>
            <Link to="/evidence">Evidence</Link>
            <Link to="/audit">Audit</Link>

          </div>

        </div>


        {/* CONTENT */}
        <div className="page">

          <Routes>

            <Route path="/" element={<TrialOverviewScreen />} />
            <Route path="/changes" element={<ProtocolChangesScreen />} />
            <Route path="/evidence" element={<EvidenceReviewScreen />} />
            <Route path="/audit" element={<AuditTrailScreen />} />

          </Routes>

        </div>


        {/* FOOTER */}
        <div className="footer">

          Regulatory AI System · Internal Demo · 2026

        </div>

      </div>

    </BrowserRouter>
  );
}
