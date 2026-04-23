import { useState, useEffect } from "react"
import axios from "axios"

const API = "http://127.0.0.1:5000"

export default function App() {
  const [entries, setEntries] = useState([])
  const [loading, setLoading] = useState(true)
  const [gateFilter, setGateFilter] = useState("all")
  const [image, setImage] = useState(null)
  const [imageName, setImageName] = useState(null)
  const [gateId, setGateId] = useState(1)
  const [submitting, setSubmitting] = useState(false)
  const [feedback, setFeedback] = useState(null)
  const [feedbackType, setFeedbackType] = useState("success")

  const fetchEntries = async () => {
    try {
      const res = await axios.get(`${API}/api/entries`)
      setEntries(res.data)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchEntries()
    const interval = setInterval(fetchEntries, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleFile = (e) => {
    const file = e.target.files[0]
    setImage(file)
    setImageName(file?.name || null)
  }

  const handleSubmit = async () => {
    if (!image) return
    setSubmitting(true)
    setFeedback(null)
    const formData = new FormData()
    formData.append("image", image)
    formData.append("gate_id", gateId)
    try {
      const res = await axios.post(`${API}/api/entry`, formData)
      setFeedback(`LOGGED — ${res.data.number_plate} · ${res.data.headcount} occupant(s) · Gate ${gateId}`)
      setFeedbackType("success")
      setImage(null)
      setImageName(null)
      fetchEntries()
    } catch {
      setFeedback("Submission failed. Check server connection.")
      setFeedbackType("error")
    } finally {
      setSubmitting(false)
    }
  }

  const gates = ["all", ...new Set(entries.map(e => String(e.gate_id)))]
  const filtered = gateFilter === "all" ? entries : entries.filter(e => String(e.gate_id) === gateFilter)

  return (
    <div style={styles.page}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;700&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #f5f3ee; }
        input[type=file] { display: none; }
        tr:hover td { background: #f0ede6; }
        select:focus, button:focus { outline: 2px solid #1a1a2e; outline-offset: 2px; }
      `}</style>

      {/* Header */}
      <header style={styles.header}>
        <div style={styles.headerInner}>
          <div>
            <div style={styles.badge}>LIVE</div>
            <h1 style={styles.title}>VOLog</h1>
            <p style={styles.subtitle}>Vehicle Occupancy & Licence Plate Logger</p>
          </div>
          <div style={styles.stats}>
            <div style={styles.statBox}>
              <span style={styles.statNum}>{entries.length}</span>
              <span style={styles.statLabel}>Total Entries</span>
            </div>
            <div style={styles.statBox}>
              <span style={styles.statNum}>
                {entries.filter(e => e.timestamp.startsWith(new Date().toISOString().slice(0, 10))).length}
              </span>
              <span style={styles.statLabel}>Entries Today</span>
            </div>
            <div style={styles.statBox}>
              <span style={styles.statNum}>
                {new Set(entries.map(e => e.gate_id)).size}
              </span>
              <span style={styles.statLabel}>Active Gates</span>
            </div>
          </div>
        </div>
      </header>

      <main style={styles.main}>
        {/* Submit Panel */}
        <section style={styles.card}>
          <h2 style={styles.cardTitle}>Submit Entry</h2>
          <div style={styles.formRow}>
            <label style={styles.fileLabel}>
              <input type="file" accept="image/*" onChange={handleFile} />
              <span style={styles.fileBtn}>
                {imageName ? `📎 ${imageName}` : "Choose Image"}
              </span>
            </label>

            <select
              value={gateId}
              onChange={e => setGateId(e.target.value)}
              style={styles.select}
            >
              {[1, 2, 3, 4, 5].map(g => (
                <option key={g} value={g}>Gate {g}</option>
              ))}
            </select>

            <button
              onClick={handleSubmit}
              disabled={submitting || !image}
              style={{ ...styles.submitBtn, opacity: (!image || submitting) ? 0.45 : 1 }}
            >
              {submitting ? "Processing…" : "Submit"}
            </button>
          </div>

          {feedback && (
            <div style={{ ...styles.feedback, background: feedbackType === "success" ? "#dcfce7" : "#fee2e2", color: feedbackType === "success" ? "#166534" : "#991b1b" }}>
              {feedback}
            </div>
          )}
        </section>

        {/* Log Table */}
        <section style={styles.card}>
          <div style={styles.tableHeader}>
            <h2 style={styles.cardTitle}>Entry Log</h2>
            <div style={styles.filterRow}>
              <label style={styles.filterLabel}>Gate</label>
              <select
                value={gateFilter}
                onChange={e => setGateFilter(e.target.value)}
                style={styles.select}
              >
                {gates.map(g => (
                  <option key={g} value={g}>{g === "all" ? "All Gates" : `Gate ${g}`}</option>
                ))}
              </select>
              <span style={styles.refreshNote}>↻ every 5s</span>
            </div>
          </div>

          {loading ? (
            <p style={styles.empty}>Loading…</p>
          ) : filtered.length === 0 ? (
            <p style={styles.empty}>No entries logged yet.</p>
          ) : (
            <div style={styles.tableWrap}>
              <table style={styles.table}>
                <thead>
                  <tr>
                    {["Entry ID", "Number Plate", "Headcount", "Gate", "Timestamp"].map(h => (
                      <th key={h} style={styles.th}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {filtered.map(entry => (
                    <tr key={entry.entry_ID}>
                      <td style={styles.tdMono}>{entry.entry_ID}</td>
                      <td style={{ ...styles.tdMono, fontWeight: 600, letterSpacing: "0.05em" }}>{entry.number_plate}</td>
                      <td style={styles.td}>
                        <span style={styles.badge2}>{entry.headcount}</span>
                      </td>
                      <td style={styles.td}>Gate {entry.gate_id}</td>
                      <td style={styles.tdMono}>{entry.timestamp}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

const styles = {
  page: { fontFamily: "'DM Sans', sans-serif", minHeight: "100vh", background: "#f5f3ee" },
  header: { background: "#1a1a2e", color: "#fff", padding: "2rem 2.5rem", borderBottom: "4px solid #e8c547" },
  headerInner: { maxWidth: "1000px", margin: "0 auto", display: "flex", justifyContent: "space-between", alignItems: "flex-end", flexWrap: "wrap", gap: "1.5rem" },
  badge: { display: "inline-block", background: "#e8c547", color: "#1a1a2e", fontSize: "0.7rem", fontWeight: 700, letterSpacing: "0.15em", padding: "2px 8px", borderRadius: "2px", marginBottom: "0.5rem" },
  title: { fontSize: "2.5rem", fontWeight: 700, letterSpacing: "-0.02em", lineHeight: 1 },
  subtitle: { fontSize: "0.9rem", color: "#9ca3af", marginTop: "0.4rem" },
  stats: { display: "flex", gap: "2rem" },
  statBox: { display: "flex", flexDirection: "column", alignItems: "flex-end" },
  statNum: { fontSize: "2rem", fontWeight: 700, color: "#e8c547", lineHeight: 1 },
  statLabel: { fontSize: "0.75rem", color: "#9ca3af", marginTop: "2px" },
  main: { maxWidth: "1000px", margin: "2rem auto", padding: "0 1.5rem", display: "flex", flexDirection: "column", gap: "1.5rem" },
  card: { background: "#fff", borderRadius: "8px", padding: "1.75rem", boxShadow: "0 1px 4px rgba(0,0,0,0.08)", border: "1px solid #e5e1d8" },
  cardTitle: { fontSize: "1rem", fontWeight: 700, color: "#1a1a2e", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: "1.25rem" },
  formRow: { display: "flex", gap: "0.75rem", alignItems: "center", flexWrap: "wrap" },
  fileLabel: { cursor: "pointer" },
  fileBtn: { display: "inline-block", padding: "8px 16px", background: "#f5f3ee", border: "1.5px solid #d1cdc4", borderRadius: "6px", fontSize: "0.9rem", color: "#1a1a2e", fontWeight: 500, whiteSpace: "nowrap" },
  select: { padding: "8px 12px", borderRadius: "6px", border: "1.5px solid #d1cdc4", background: "#fff", color: "#1a1a2e", fontSize: "0.9rem", fontFamily: "'DM Sans', sans-serif" },
  submitBtn: { padding: "8px 24px", borderRadius: "6px", background: "#1a1a2e", color: "#e8c547", border: "none", fontWeight: 700, fontSize: "0.9rem", cursor: "pointer", fontFamily: "'DM Sans', sans-serif", letterSpacing: "0.05em" },
  feedback: { marginTop: "1rem", padding: "10px 16px", borderRadius: "6px", fontSize: "0.875rem", fontWeight: 500 },
  tableHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "1rem", marginBottom: "1.25rem" },
  filterRow: { display: "flex", alignItems: "center", gap: "0.75rem" },
  filterLabel: { fontSize: "0.85rem", color: "#6b7280", fontWeight: 500 },
  refreshNote: { fontSize: "0.8rem", color: "#9ca3af" },
  tableWrap: { overflowX: "auto" },
  table: { width: "100%", borderCollapse: "collapse" },
  th: { padding: "10px 16px", textAlign: "left", fontSize: "0.75rem", fontWeight: 700, color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.08em", borderBottom: "2px solid #e5e1d8", background: "#faf9f6" },
  td: { padding: "12px 16px", fontSize: "0.9rem", color: "#1a1a2e", borderBottom: "1px solid #f0ede6" },
  tdMono: { padding: "12px 16px", fontSize: "0.875rem", color: "#1a1a2e", borderBottom: "1px solid #f0ede6", fontFamily: "'DM Mono', monospace" },
  badge2: { display: "inline-block", background: "#1a1a2e", color: "#e8c547", fontWeight: 700, fontSize: "0.8rem", padding: "2px 10px", borderRadius: "20px" },
  empty: { color: "#9ca3af", padding: "2rem 0", textAlign: "center" },
}