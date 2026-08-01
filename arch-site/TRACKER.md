# Architecture Site — Project Tracker

> **This file is the sole source of truth for this project.** To-dos, decisions,
> open questions and progress live here and nowhere else. If it isn't in this
> file, it isn't tracked. If this file disagrees with something said in chat,
> this file is stale — fix it, don't work around it.
>
> Maintained by the `project-tracker` skill (`/project-tracker`). The section at
> the bottom marked AUTOSNAPSHOT is written by a script — don't hand-edit it.

**Project:** website for Aaron's father's architecture firm, with HubSpot as CRM
**Repo:** `aselkridge/oasplans` (moved from `aarons-portfolio` on 2026-08-01, → Q9)
**Branch:** `claude/portfolio-repo-migration-mp3od6`
**Started:** 2026-08-01

---

## Status at a glance

| | |
|---|---|
| **Phase** | 1 — mockup |
| **Blocked on** | Aaron: feedback on greybox v1 |
| **Next deliverable** | Greybox v2, revised from Aaron's feedback |
| **Nothing is live** | no site scaffold, no domain, no HubSpot portal yet |

---

## Decisions locked

Decisions here are settled. Reopening one is fine, but say so explicitly and
move it back to Open questions — don't just quietly build something else.

| # | Decision | Rationale | Date |
|---|---|---|---|
| D1 | **Static site, not HubSpot CMS.** Astro, deployed to Cloudflare Pages or Netlify. | Architecture firms sell on photography and page speed. HubSpot's CMS costs more and gives less design control. Building *on* HubSpot is the one choice that would be expensive to reverse. | 2026-08-01 |
| D2 | **Aaron's dad must be able to self-edit.** Git-backed CMS (Sveltia, fallback Decap) at `/admin`. | He will want to add projects without calling Aaron. Git-backed keeps content in our repo, so no platform holds it hostage. | 2026-08-01 |
| D3 | **HubSpot starts on the free tier, integration stays thin and swappable.** Tracking script + Forms API v3 + meetings embed only. | Free→Marketing Hub is a billing change, not a migration; contacts and page-view history carry over. Thin integration also means HubSpot itself is replaceable later. | 2026-08-01 |
| D4 | **Form submissions get a second destination** (email or webhook) alongside HubSpot. | So the lead flow — the thing the business actually runs on — never depends on a single vendor. | 2026-08-01 |
| D5 | **Mockups are built as real HTML here, not in a visual design tool.** | The mockup's type scale, grid and image treatment carry straight into the Astro build. A design-tool comp has to be re-implemented, and things get lost in translation. | 2026-08-01 |
| D6 | **Mockup → sign-off → integrate → Aaron merges.** Never deploy to make something live unasked. | House rule, `CLAUDE.md`. | 2026-08-01 |

---

## Open questions — need Aaron

These block real work. Each one says what it blocks, so it's obvious what
shakes loose when it's answered.

| # | Question | Blocks | Status |
|---|---|---|---|
| Q1 | **Reference sites** — veragouthxilema.com + maman-corp.com (2026-08-01). Shared direction: minimal, generous whitespace, restrained sans type, photography-forward, understated heritage confidence. Drove greybox v1. | — | ✅ answered |
| Q2 | **Firm name + city** | copy, page titles, local SEO, domain choice | 📦 boxed |
| Q3 | **What does he build?** residential / commercial / historic reno / institutional | tone and structure differ a lot between these | 📦 boxed |
| Q4 | **Do professional project photos exist?** How many, of what? | Biggest single factor in the design. If only phone snaps and CAD renderings exist, we design around that deliberately instead of pretending. | 📦 boxed |
| Q5 | **Logo / existing brand?** | palette, type pairing | 📦 boxed |
| Q6 | **Domain name** — owned already, or to buy? | deploy config, HubSpot tracking domain | 📦 boxed |
| Q7 | **Who owns the HubSpot account?** Aaron or his dad? Portal ID? | form wiring, and who gets billed if it's ever upgraded | 📦 boxed |
| Q8 | **Any EU/UK traffic expected?** | whether a cookie-consent gate on the HubSpot tracking script is required | 📦 boxed |
| Q9 | **Own repo, or stay inside `aarons-portfolio`?** — own repo: `oasplans`. Tracker + hooks migrated 2026-08-01; nothing else came along, nothing was lost. | ~~was: see R1~~ | ✅ answered |

Legend: ⏳ in flight · 📦 boxed, deliberately deferred · ✅ answered

---

## Work items

### Now
- [x] Decide platform + HubSpot approach (→ D1–D4)
- [x] Stand up this tracker + the skill and hooks that maintain it
- [x] Greybox v1: homepage + case-study page (`arch-site/mockups/greybox-v1.html`,
      published as private Artifact) — placeholders labeled with the tracker
      question they wait on (†Q2/Q3/Q4)
- [ ] **Wait on Aaron** — greybox v1 feedback, then iterate

### Next
- [ ] Greybox v2 from feedback; repeat until the feel is right
- [ ] Answering Q2–Q4 replaces the † placeholders (name, work mix, photos)

### Later
- [ ] Scaffold Astro project + content collections for projects
- [ ] Wire Sveltia CMS at `/admin`, test that a non-technical user can publish
- [ ] HubSpot: tracking script, Forms API v3 submit, meetings embed
- [ ] Second destination for form submissions (D4)
- [ ] Cookie consent gate, if Q8 says yes
- [ ] Image pipeline — responsive sizes, lazy loading, sensible LCP
- [ ] SEO: per-page metadata, sitemap, structured data, Google Business Profile
- [ ] Deploy config + custom domain + HTTPS
- [ ] Handoff doc written for Aaron's dad, in plain language

### Done
- 2026-08-01 — Platform recommendation delivered and accepted (D1–D5)
- 2026-08-01 — Tracker, `project-tracker` skill, and PreCompact/SessionStart/Stop hooks built
- 2026-08-01 — Project moved to its own repo, `oasplans` (Q9 ✅, R1 retired)
- 2026-08-01 — Q1 answered (2 reference sites); greybox v1 built and published
  as a private Artifact for review

---

## Risks / watch-list

- ~~**R1 — wrong repo.**~~ Resolved 2026-08-01: project migrated to its own repo,
  `oasplans`, before any scaffolding landed. (→ Q9)
- **R2 — photography is the product.** A beautiful shell around weak imagery
  reads as a weak firm. If good photos don't exist, that's the first spend,
  before any code. (→ Q4)
- **R3 — local SEO outweighs design** for inquiry volume. "Architect in
  \[city\]" plus a Google Business Profile will out-earn any clever interaction.
- **R4 — HubSpot free tier puts HubSpot branding on embedded forms.** Using the
  Forms API instead of the embed avoids this, and keeps the form a design
  surface we control. Already the plan (D3), noted so nobody "simplifies" it
  back to the embed.

---

## Glossary — for Aaron's dad, and for future sessions

- **Astro** — the tool that turns our content files into a plain, fast website.
- **Static site** — pages are pre-built, so they load instantly and can't break
  the way a database-backed site can.
- **Git-backed CMS** — an admin screen for editing the site. It saves changes
  into the project's own files rather than a company's private database.
- **HubSpot Forms API** — lets us build our own contact form and hand the
  submission to HubSpot, instead of embedding HubSpot's pre-styled form.
- **Portal ID** — the number identifying a HubSpot account.

---

<!-- AUTOSNAPSHOT:BEGIN -->

### Auto-snapshot — written by the PreCompact hook, do not hand-edit

_Captured 2026-08-01 20:17 UTC (trigger: compaction). Mechanical git state only._

**Branch:** `claude/architecture-website-hubspot-gnkmg0`  
**HEAD:** 318b2e5 docs: R2 art sourcing kit — ready-to-paste prompts for all 5 scenes (both themes, 3 layers each) + shelf objects

**Uncommitted (2):**

- `?? .claude/`
- `?? arch-site/`

> Uncommitted work at compaction time — verify it wasn't lost.

**Recent commits:**

- `318b2e5` docs: R2 art sourcing kit — ready-to-paste prompts for all 5 scenes (both themes, 3 layers each) + shelf objects
- `1a0de54` docs: R3a content inventory — full REAL vs PLACEHOLDER walk of every surface
- `6f6ca60` docs: Keyboard Pong v2 (feedback round) + v3 (tap mode for touch devices) logged in R4b spec
- `5f0d2eb` Merge in Keyboard Pong docs (session) with parallel live-branch work
- `b7a62c0` docs: #12a closed (20k stays), R4b specced as Keyboard Pong with prototype out for review
- `441ba9c` Merge branch 'claude/website-build-addition-05kyz5' into claude/website-build-nevi30
- `0418a0c` fix: toasts stay up long enough to read, tap to dismiss
- `8ce74a6` Merge in feedback door + dash fixes (parallel session) with R2e hangar art

<!-- AUTOSNAPSHOT:END -->
