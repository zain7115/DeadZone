# DeadZone Frontend — Outcome Checklist

## Frontend-only prototype architecture
- Create a responsive academic prototype dashboard for DeadZone — Wi‑Fi Coverage Intelligence.
- Express the approved measurement-based workflow as MEASURE → MAP → ANALYZE → OPTIMIZE → REPORT.
- Use realistic mock data and integration-ready UI states so a later backend can replace the frontend data contracts.
- Do not implement backend services, authentication, real Wi‑Fi scanning, database persistence, or guaranteed RF propagation modeling.

## Overview and workflow navigation
- Provide an overview dashboard with survey progress, workflow stages, key coverage metrics, recent surveys, alerts, and recommended next actions.
- Keep the five workflow stages discoverable and make the current active stage clear.

## Measurement collection
- Provide measurement collection controls and mock records for RSSI, latency, packet loss, throughput, SSID/BSSID, channel, timestamp, and indoor location.
- Represent idle, collecting, completed, error/demo states in the UI without performing real Wi‑Fi scanning.

## Floor-plan mapping
- Provide a floor-plan mapping screen with measurement points, access points, rooms/zones, legends, filters, and selected-point details.
- Support frontend-only mock interactions for selecting points and switching visible layers.

## Coverage analysis
- Provide heatmap-style signal visualization with metric switching, thresholds, weak-zone identification, channel/interference insights, and explanatory confidence/limitation cues.
- Clearly frame results as measurement-based decision support, not certified RF prediction.

## AP optimization
- Provide proposed AP locations, comparative scoring, ranked alternatives, expected improvement estimates, constraints, and transparent decision criteria.
- Avoid claiming guaranteed RF propagation or automatic AP installation/configuration.

## Survey comparison and reporting
- Provide a survey comparison view for baseline and follow-up surveys across locations, metrics, heatmaps, weak zones, and before/after changes.
- Provide report configuration, preview, findings, methodology, recommendations, charts, limitations, and simulated export/print actions.

## Academic scope communication
- Connect the interface to Computer Networks, Data Science, DSA/C#, and Software Engineering.
- Explicitly exclude professional RF certification, automatic physical AP installation, enterprise AP configuration, unauthorized penetration testing, and guaranteed propagation prediction.

## Validation and delivery
- Ensure the app serves `/manus-routes.json` with the complete page route set.
- Verify the frontend builds cleanly and the preview responds on the configured port.
- Save the intended frontend source as the handoff deliverable for backend integration.
