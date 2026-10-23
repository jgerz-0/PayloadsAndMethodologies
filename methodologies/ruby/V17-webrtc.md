# V17 – WebRTC (Rails)

> **ASVS 5.0 · Chapter V17** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V17-WebRTC.md`](../_asvs-base/V17-WebRTC.md).

## Applicability

**Not applicable to a typical Rails web application.** V17 covers the
WebRTC **media/signaling infrastructure** — TURN servers (coturn), DTLS/SRTP
media servers, and signaling servers — not the Rails HTTP app itself.

A Rails app usually only participates as the **signaling broker** (exchanging
SDP offers/answers and ICE candidates over its own channel, often ActionCable
WebSockets) and does not terminate media. In that case:

- If signaling rides **ActionCable**, its transport/origin/auth requirements are
  covered in [V4.4 WebSocket](V04-api-and-web-service.md) (WSS, `Origin`
  allowlist, authenticated connections).
- Mark **17.1.x (TURN)**, **17.2.x (DTLS/SRTP media)**, and **17.3.x
  (signaling-server flood/malformed handling)** as **N/A — no WebRTC media/TURN
  infrastructure in scope**, unless the engagement includes a TURN/media server
  (e.g. coturn, Janus, mediasoup, LiveKit), in which case test those components
  directly against the base requirements.

### If TURN/media IS in scope

- **17.1.1 (L2):** confirm the TURN server refuses relaying to reserved ranges
  (internal/loopback/link-local) — a TURN SSRF/relay-abuse test
  (`169.254.169.254`, `127.0.0.1`, RFC1918) via TURN allocations.
- **17.2.x / 17.3.x:** DTLS cipher/profile hardening, SRTP auth, and
  resilience to malformed/flood SRTP and signaling — media-server tests,
  outside the Rails codebase.

---
*Covers ASVS V17.1–V17.3 (applicability-scoped). Signaling over ActionCable:
[V4.4](V04-api-and-web-service.md).*
