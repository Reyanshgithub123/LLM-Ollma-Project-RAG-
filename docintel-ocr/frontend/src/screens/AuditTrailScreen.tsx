import { useEffect, useState } from "react";
import { getAuditLogs, getStats } from "../services/api";
import "../audit.css";

export default function AuditTrailScreen() {

  const [logs, setLogs] = useState<any[]>([]);
  const [filter, setFilter] = useState("all");

  const [stats, setStats] = useState<any>({
    total: 0,
    documents: 0,
    ai: 0,
    alerts: 0
  });


  /* ================= LOAD DATA ================= */

  async function load() {

    try {

      const l = await getAuditLogs();
      const s = await getStats();

      setLogs(l.data);
      setStats(s.data);

    } catch (err) {

      console.error("Failed to load audit data");

    }
  }


  useEffect(() => {

    load();

    const t = setInterval(load, 3000);

    return () => clearInterval(t);

  }, []);


  /* ================= FILTER LOGIC ================= */

  const filteredLogs = logs.filter((l) => {

    if (filter === "all") return true;

    const now = new Date().getTime();
    const logTime = new Date(l.time).getTime();

    const diff = now - logTime;

    if (filter === "1h") return diff <= 60 * 60 * 1000;
    if (filter === "24h") return diff <= 24 * 60 * 60 * 1000;
    if (filter === "7d") return diff <= 7 * 24 * 60 * 60 * 1000;

    return true;
  });


  return (

    <div>

      {/* ================= STATS ================= */}

      <div className="stats-grid mb-6">

        <StatBox
          title="Total Events"
          value={stats.total}
          change="+12.5%"
          positive
        />

        <StatBox
          title="Documents"
          value={stats.documents}
          change="+8.2%"
          positive
        />

        <StatBox
          title="AI Ops"
          value={stats.ai}
          change="-3.1%"
        />

        <StatBox
          title="Alerts"
          value={stats.alerts}
          change="+4.9%"
          positive
        />

      </div>


      {/* ================= FILTER ================= */}

      <div className="filter-bar mb-4">

        <button
          onClick={() => setFilter("all")}
          className={filter === "all" ? "filter-btn active" : "filter-btn"}
        >
          🌍 All
        </button>

        <button
          onClick={() => setFilter("1h")}
          className={filter === "1h" ? "filter-btn active" : "filter-btn"}
        >
          ⏱ 1 Hour
        </button>

        <button
          onClick={() => setFilter("24h")}
          className={filter === "24h" ? "filter-btn active" : "filter-btn"}
        >
          📅 24 Hours
        </button>

        <button
          onClick={() => setFilter("7d")}
          className={filter === "7d" ? "filter-btn active" : "filter-btn"}
        >
          📆 7 Days
        </button>

      </div>


      {/* ================= LOGS ================= */}

      <div className="card">

        <h2 className="section-title">
          Activity Log
        </h2>


        {filteredLogs.length === 0 && (
          <div className="text-gray-500 text-sm text-center py-6">
            No logs found for this filter
          </div>
        )}


        {filteredLogs.map((l, i) => (

          <div key={i} className="log-row">

            <div className="log-main">
              <b>{l.event?.toUpperCase()}</b> — {l.message}
            </div>

            <div className="log-meta">

              <span>👤 {l.user}</span>
              <span>🌐 {l.ip}</span>
              <span>🕒 {new Date(l.time).toLocaleString()}</span>

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}


/* ================= STAT BOX ================= */

function StatBox({ title, value, change, positive }: any) {

  return (

    <div className="stat-box">

      <div className="stat-header">
        {title}
      </div>

      <div className="stat-main">

        <div className="stat-number">
          {value}
        </div>

        <div
          className={
            positive
              ? "stat-change positive"
              : "stat-change negative"
          }
        >

          {positive ? "▲" : "▼"} {change}

        </div>

      </div>

    </div>

  );
}
