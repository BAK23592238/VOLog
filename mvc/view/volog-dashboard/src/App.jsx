import { useState, useEffect } from "react"
import axios from "axios"

function App() {
  const [entries, setEntries] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchEntries = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/api/entries")
      setEntries(response.data)
    } catch (error) {
      console.error("Failed to fetch entries:", error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchEntries()
    const interval = setInterval(fetchEntries, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: "2rem", maxWidth: "900px", margin: "0 auto" }}>
      <h1>VOLog — Gate Entry Dashboard</h1>
      <p style={{ color: "#666" }}>Refreshes every 5 seconds</p>

      {loading ? (
        <p>Loading...</p>
      ) : entries.length === 0 ? (
        <p>No entries logged yet.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ backgroundColor: "#f0f0f0" }}>
              <th style={th}>Entry ID</th>
              <th style={th}>Number Plate</th>
              <th style={th}>Headcount</th>
              <th style={th}>Gate</th>
              <th style={th}>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {entries.map((entry) => (
              <tr key={entry.entry_ID} style={{ borderBottom: "1px solid #ddd" }}>
                <td style={td}>{entry.entry_ID}</td>
                <td style={td}>{entry.number_plate}</td>
                <td style={td}>{entry.headcount}</td>
                <td style={td}>{entry.gate_id}</td>
                <td style={td}>{entry.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

const th = {
  padding: "10px 14px",
  textAlign: "left",
  borderBottom: "2px solid #ccc",
  fontWeight: "bold"
}

const td = {
  padding: "10px 14px",
  textAlign: "left"
}

export default App