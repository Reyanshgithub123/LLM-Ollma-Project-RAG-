import { useEffect, useState } from "react";
import { getAuditLogs, getStats } from "../services/api";


export default function AuditTrailScreen() {

  const [logs, setLogs] = useState<any[]>([]);
  const [stats, setStats] = useState<any>({
    total: 0,
    documents: 0,
    ai: 0,
    alerts: 0
  });


  async function load() {

    const l = await getAuditLogs();
    const s = await getStats();

    setLogs(l.data);
    setStats(s.data);
  }


  useEffect(() => {

    load();

    const t = setInterval(load, 3000);

    return () => clearInterval(t);

  }, []);


  return (

    <div>

      {/* STATS */}
      <div className="grid grid-cols-4 gap-4 mb-6">

        <Stat title="Total Events" value={stats.total} />
        <Stat title="Documents" value={stats.documents} />
        <Stat title="AI Ops" value={stats.ai} />
        <Stat title="Alerts" value={stats.alerts} />

      </div>


      {/* LOGS */}
      <div className="card">

        <h2 className="section-title">
          Activity Log
        </h2>


        {logs.map((l, i) => (

          <div
            key={i}
            className="border-b py-3 text-sm"
          >

            <b>{l.event.toUpperCase()}</b> — {l.message}

            <div className="text-gray-500 text-xs">

              {l.user} · {l.ip} · {new Date(l.time).toLocaleString()}

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}


function Stat({ title, value }: any) {

  return (

    <div className="card text-center">

      <div className="text-2xl font-bold text-blue-800">
        {value}
      </div>

      <div className="text-gray-600 text-sm">
        {title}
      </div>

    </div>
  );
}
