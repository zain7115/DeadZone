# DeadZone — Frontend Handoff

DeadZone is a frontend-only, responsive prototype for the semester project proposal **DeadZone — Intelligent Wi‑Fi Coverage Mapping & Optimization System**. It presents the measurement-driven workflow:

**MEASURE → MAP → ANALYZE → OPTIMIZE → REPORT**

The implementation uses React, TypeScript, Vite, and plain CSS. It intentionally uses realistic mock data and local UI state; it does not scan Wi‑Fi, persist records, authenticate users, or claim guaranteed RF propagation behavior.

## Run locally

```bash
npm install
npm run dev
```

The development server runs on port `3000`. For a production build:

```bash
npm run build
npm run preview
```

## Frontend routes

- `/` — Overview / command center
- `/measure` — Collection session, schema, mock measurement log
- `/map` — Floor plan, point selection, selected-point details
- `/analyze` — Heatmap-style analysis, metric switching, weak-zone and channel insights
- `/optimize` — AP candidate ranking, scoring criteria, DSA/C# handoff cue
- `/compare` — Baseline vs follow-up survey deltas
- `/report` — Report section builder and report preview

## Backend seams

All demo data currently lives near the top of `src/App.tsx`, including `measurements`, `heatCells`, and `candidates`. Replace those arrays with query hooks or API calls when the backend is ready. The UI already exposes these logical contracts:

```ts
type Measurement = {
  id: string
  point: string
  zone: string
  location: string
  rssi: number
  latency: number
  loss: number
  throughput: number
  ssid: string
  bssid: string
  channel: string
  timestamp: string
  status: 'Good' | 'Watch' | 'Weak'
}
```

Suggested integration points:

| UI seam | Suggested backend contract |
| --- | --- |
| Measure session | `GET /surveys/:surveyId`, `POST /surveys/:surveyId/measurements` |
| Measurement log | `GET /surveys/:surveyId/measurements` |
| Floor-plan map | `GET /surveys/:surveyId/map`, `PUT /surveys/:surveyId/map` |
| Analysis heatmap | `GET /surveys/:surveyId/analysis?metric=rssi` |
| AP ranking | `POST /surveys/:surveyId/optimization/run` |
| Survey comparison | `GET /surveys/compare?baseline=:id&followup=:id` |
| Report preview | `POST /reports/preview` |

Use the current mock states as the contract for idle, collecting, completed/demo, selected-point, weak-zone, and report-generated states. Keep the limitation copy: this is measurement-based decision support, not professional RF certification, automatic AP installation, enterprise AP configuration, penetration testing, or guaranteed RF prediction.

## Project structure

- `src/App.tsx` — route-aware screen composition and mock interaction states
- `src/styles.css` — responsive visual system and page layouts
- `src/main.tsx` — React entry point
- `public/manus-routes.json` — page route manifest used by the managed preview
- `app.config.ts` — project logo metadata
- `TODO.md` — approved outcome checklist
