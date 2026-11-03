# DeadZone — Module 02: Frontend

## 👤 Module Information
- **Module Name:** `02_Frontend`
- **Responsible Member:** Member 2 (Frontend Developer)
- **Git Branch:** `frontend`
- **Technology Stack:** React 18+, TypeScript 5+, Vite 6+, Plain CSS (DM Mono + Manrope fonts)

---

## 🎯 Overview & Responsibilities
The Frontend module is the user-facing interface for the DeadZone Intelligent Wi-Fi Coverage Mapping & Optimization System. It implements a responsive academic prototype dashboard following the core project workflow:

$$\text{MEASURE} \longrightarrow \text{MAP} \longrightarrow \text{ANALYZE} \longrightarrow \text{OPTIMIZE} \longrightarrow \text{REPORT}$$

### Core Features & Views
1. **Overview (`/`):** Command center displaying active survey overview, coverage statistics, stage navigation, and quick metrics.
2. **Measure (`/measure`):** Signal collection console with manual reading entry (RSSI, Latency, Loss, Throughput, Channel), active sampling progress, and live measurement log.
3. **Map (`/map`):** Interactive indoor floor plan with 5 measurement coordinate pins (P-037 to P-041), zone selection, and detailed reading inspection.
4. **Analyze (`/analyze`):** Heatmap visualization (7×12 grid, 84 cells), threshold indicators (-67 dBm boundary), metric toggles, and weak zone callouts.
5. **Optimize (`/optimize`):** Access Point (AP) candidate evaluation ranking (AP-C04, AP-C02, AP-C07) with scores, coverage lift percentages, constraints, and graph traversal paths.
6. **Compare (`/compare`):** Side-by-side comparison between baseline and follow-up surveys showing delta metrics and status improvements.
7. **Report (`/report`):** Report configuration builder and print/PDF ready executive summary with findings, charts, and methodology.

---

## 🚀 Getting Started & Local Development

### Prerequisites
- Node.js (v18.0 or higher)
- npm (v9.0 or higher)

### Installation
Navigate to the `02_Frontend` folder and install dependencies:
```bash
cd 02_Frontend
npm install
```

### Running the Development Server
```bash
npm run dev
```
The application will launch at: **`http://localhost:3000`**

### Building for Production
```bash
npm run build
npm run preview
```

---

## 🔌 Backend Integration & Proxy

The frontend is configured to communicate with the Backend module (`01_Backend`) running on port `5000`.

In `vite.config.ts`, the Vite development server proxies all `/api` requests:
```ts
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      secure: false,
    },
  },
}
```

### Graceful Fallback Mode
If the backend is not running, the frontend automatically falls back to an offline demo state with clear status indicators in the top bar. You can develop and test UI features completely offline!

---

## 📂 File Structure & Modification Guide

### 🟢 Files You Are Expected to Modify
| File / Directory | Purpose & Allowed Work |
| :--- | :--- |
| `src/App.tsx` | Main application routes, page layouts, UI state, and component composition. |
| `src/styles.css` | Styling, theme colors, typography, layout cards, responsive rules. |
| `src/components/` | (Recommended) You can split `App.tsx` into smaller reusable components. |
| `src/assets/` | Floor plans, SVGs, icons, and UI graphics. |
| `public/` | Public static assets and manifests. |

### 🔴 Files That Should NOT Be Independently Modified
*Any changes to these files require coordination with the repository owner and other module leads:*
| File | Reason |
| :--- | :--- |
| `vite.config.ts` | Controls port `3000` and proxy routing to Backend port `5000`. |
| `package.json` | Core build scripts and shared framework versions. |
| API Contract Types in `App.tsx` | Data interfaces (`Measurement`, `Candidate`, `MapPoint`) must match Backend and Data Processing models. |

---

## 🔗 Shared Data Contracts & Types

To ensure seamless integration with `01_Backend`, preserve these data interfaces:

```typescript
export type Measurement = {
  id: string
  point: string
  zone: string
  rssi: number          // in dBm (e.g. -48, -61, -74)
  latency: number       // in ms (e.g. 18, 27)
  loss: number          // in % (e.g. 0.2, 3.4)
  throughput: number    // in Mbps (e.g. 87, 28)
  channel: string       // e.g. '36 / 5 GHz', '11 / 2.4 GHz'
  status: 'Good' | 'Watch' | 'Weak'
}

export type Candidate = {
  rank: string          // e.g. '01', '02'
  label: string         // e.g. 'AP-C04'
  zone: string
  score: number         // 0 - 100
  lift: string          // e.g. '+24%'
  constraints: string
  tone: 'cyan' | 'amber' | 'slate' | 'green' | 'red'
}

export type MapPoint = {
  id: string            // e.g. 'P-039'
  x: number             // percentage (0-100)
  y: number             // percentage (0-100)
  tone: string          // 'good' | 'watch' | 'weak'
  zone: string
}
```

---

## 🤝 Dependencies on Other Modules
1. **Module 01 (Backend):** Consumes `/api/surveys/active`, `/api/surveys/measurements`, `/api/surveys/map-points`, and `/api/optimization/run`.
2. **Module 03 (Data Processing):** Heatmap grid is 7 rows × 12 columns = 84 cells.
3. **Module 04 (Algorithms):** Optimization candidate ranks and scoring weights.
