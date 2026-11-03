// ─────────────────────────────────────────────────────────────
//  DeadZone · Backend MVP  (20 % integration skeleton)
//  Express server — serves measurement, map, and optimization
//  endpoints that the React frontend consumes via Vite proxy.
// ─────────────────────────────────────────────────────────────

import express from 'express'
import cors from 'cors'

const app = express()
const PORT = 5000

// ── Middleware ───────────────────────────────────────────────
app.use(cors({ origin: 'http://localhost:3000' }))
app.use(express.json())

// ── In-memory data stores ───────────────────────────────────
// Seeded with the same demo data the frontend previously hard-coded.

const measurements = [
  { id: 'M-041', point: 'P-041', zone: 'Lab corridor',    rssi: -48, latency: 18, loss: 0.2, throughput: 87, channel: '36 / 5 GHz',   status: 'Good'  },
  { id: 'M-040', point: 'P-040', zone: 'Data lab',        rssi: -61, latency: 27, loss: 0.8, throughput: 61, channel: '36 / 5 GHz',   status: 'Watch' },
  { id: 'M-039', point: 'P-039', zone: 'Stairwell B',     rssi: -74, latency: 46, loss: 3.4, throughput: 28, channel: '11 / 2.4 GHz', status: 'Weak'  },
  { id: 'M-038', point: 'P-038', zone: 'Seminar room',    rssi: -56, latency: 21, loss: 0.5, throughput: 72, channel: '44 / 5 GHz',   status: 'Good'  },
  { id: 'M-037', point: 'P-037', zone: 'Faculty office',  rssi: -67, latency: 34, loss: 1.9, throughput: 42, channel: '11 / 2.4 GHz', status: 'Watch' },
]

const mapPoints = [
  { id: 'P-041', x: 23, y: 25, tone: 'good',  zone: 'Lab corridor'   },
  { id: 'P-040', x: 47, y: 33, tone: 'watch', zone: 'Data lab'       },
  { id: 'P-039', x: 74, y: 59, tone: 'weak',  zone: 'Stairwell B'    },
  { id: 'P-038', x: 33, y: 68, tone: 'good',  zone: 'Seminar room'   },
  { id: 'P-037', x: 58, y: 78, tone: 'watch', zone: 'Faculty office' },
]

const heatCells = [
  82,88,91,86,79,69,60,44,38,45,57,71,
  89,94,96,92,83,74,67,52,42,47,62,78,
  86,90,93,87,81,70,64,48,34,41,58,76,
  78,84,87,82,75,66,54,39,28,36,51,69,
  72,79,81,77,69,59,47,34,24,31,46,63,
  66,72,76,71,63,52,43,31,22,27,41,58,
  59,65,68,64,57,47,37,29,21,25,38,54,
  53,59,62,57,50,41,33,26,19,24,34,48,
]

// ─────────────────────────────────────────────────────────────
//  1.  MEASURE endpoints
// ─────────────────────────────────────────────────────────────

/** GET /api/surveys/active
 *  Return the current survey state — measurements + heat cells.
 */
app.get('/api/surveys/active', (_req, res) => {
  res.json({
    surveyId: 'DZ-2026-10-14',
    building: 'North Block',
    floor: '2nd floor',
    measurements,
    heatCells,
    pointsTotal: 48,
    pointsSampled: measurements.length,
  })
})

/** POST /api/surveys/measurements
 *  Append a new JSON reading to the in-memory array.
 *  Expects: { point, zone, rssi, latency, loss, throughput, channel }
 */
app.post('/api/surveys/measurements', (req, res) => {
  const { point, zone, rssi, latency, loss, throughput, channel } = req.body

  if (!point || rssi === undefined) {
    return res.status(400).json({ error: 'point and rssi are required fields.' })
  }

  // Derive status from RSSI value
  const status = rssi >= -55 ? 'Good' : rssi >= -67 ? 'Watch' : 'Weak'

  const newMeasurement = {
    id: `M-${String(measurements.length + 37).padStart(3, '0')}`,
    point,
    zone: zone || 'Unknown zone',
    rssi,
    latency: latency ?? 0,
    loss: loss ?? 0,
    throughput: throughput ?? 0,
    channel: channel || 'auto',
    status,
  }

  // Prepend so newest appears first
  measurements.unshift(newMeasurement)

  console.log(`  ✓ New measurement recorded: ${newMeasurement.id} at ${point} (${rssi} dBm → ${status})`)

  res.status(201).json({
    measurement: newMeasurement,
    totalCount: measurements.length,
  })
})

// ─────────────────────────────────────────────────────────────
//  2.  MAP endpoint
// ─────────────────────────────────────────────────────────────

/** GET /api/surveys/map-points
 *  Return the 5 core coordinate points (P-037 → P-041).
 */
app.get('/api/surveys/map-points', (_req, res) => {
  res.json({ points: mapPoints })
})

// ─────────────────────────────────────────────────────────────
//  3.  OPTIMIZE / DSA C# SEAM endpoint
// ─────────────────────────────────────────────────────────────

/** POST /api/optimization/run
 *  Accept current coordinates, mock a graph traversal trigger,
 *  and return the ranked AP candidate array with scores.
 *  This simulates the C# handoff logic from the proposal.
 */
app.post('/api/optimization/run', (req, res) => {
  const { coordinates } = req.body  // array of { id, x, y } from the map

  console.log(`  ✣ Optimization requested with ${coordinates?.length ?? 0} coordinate(s)`)
  console.log(`    └─ Simulating DSA graph traversal (C# service seam)…`)

  // ── Mock graph traversal logic ──
  // In production this would call the C# DSA service.
  // Here we simulate the ranked output described in the proposal.

  const candidates = [
    {
      rank: '01',
      label: 'AP-C04',
      zone: 'Stairwell B / north landing',
      score: 91,
      lift: '+24%',
      constraints: 'Power nearby · clear sightline',
      tone: 'cyan',
      graphPath: ['P-039', 'P-040', 'P-041'],         // simulated traversal path
      algorithm: 'weighted-shortest-path',
    },
    {
      rank: '02',
      label: 'AP-C02',
      zone: 'Seminar room / east wall',
      score: 84,
      lift: '+18%',
      constraints: 'Needs ceiling drop · low overlap',
      tone: 'amber',
      graphPath: ['P-038', 'P-040'],
      algorithm: 'weighted-shortest-path',
    },
    {
      rank: '03',
      label: 'AP-C07',
      zone: 'Data lab / south aisle',
      score: 76,
      lift: '+12%',
      constraints: 'High channel overlap',
      tone: 'slate',
      graphPath: ['P-037', 'P-040'],
      algorithm: 'weighted-shortest-path',
    },
  ]

  res.json({
    status: 'completed',
    engine: 'mock-dsa-graph-traversal',
    inputPoints: coordinates?.length ?? 0,
    candidates,
    meta: {
      note: 'This is a simulated response. Replace with real C# DSA service call.',
      weights: { coverageGap: 0.4, measuredRSSI: 0.3, channelOverlap: 0.2, installConstraints: 0.1 },
    },
  })
})

// ── Health check ────────────────────────────────────────────
app.get('/api/health', (_req, res) => {
  res.json({ status: 'ok', server: 'deadzone-backend', version: '0.1.0' })
})

// ── Start ───────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log()
  console.log('  ╔═══════════════════════════════════════════════╗')
  console.log('  ║   DeadZone Backend · MVP (20 % skeleton)     ║')
  console.log(`  ║   Running on http://localhost:${PORT}            ║`)
  console.log('  ╠═══════════════════════════════════════════════╣')
  console.log('  ║  GET  /api/surveys/active                    ║')
  console.log('  ║  POST /api/surveys/measurements              ║')
  console.log('  ║  GET  /api/surveys/map-points                ║')
  console.log('  ║  POST /api/optimization/run                  ║')
  console.log('  ║  GET  /api/health                            ║')
  console.log('  ╚═══════════════════════════════════════════════╝')
  console.log()
})
