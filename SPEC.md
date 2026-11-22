# AB Motion Control App — Spec v1.0.0

## App name
**AB Motion Control App** (working title; Pappy to confirm the store name).

## Purpose
A **training app** that teaches how to use Allen-Bradley motion control
components — deep, not surface. The learner finishes a path able to select,
wire, configure, commission, tune, and fault-find the component on a real
machine. This is the first app in the industrial component library series;
the 20-platform catalog seed lives untouched at
`~/workspace/motion-control/` as reference for later apps in the series.

## Scope — Allen-Bradley motion only
| Category | Families covered (29 total) |
|---|---|
| Servo drives (9) | Kinetix 5100, 5300, 5500, 5700, 6500, 6200, 6000, 350, 300 |
| VFDs (8) | PowerFlex 523, 525, 753, 755, 755T, 70, 700, 4/40 |
| Servo motors (6) | MP-Series MPL, MPM; Kinetix VP VPL, VPF; TL-Series TLY, TL |
| Starters & protection (6) | SMC-3, SMC Flex, SMC-50; Bulletin 140M; Bulletin 100-C; E300 |
| Supporting context (1 module) | Studio 5000 motion: I/O tree, AXIS_CIP_DRIVE, motion groups, motion instructions, autotune |

Keyence is out of this app (sensors, not motion). Other vendors belong to
later apps in the series.

## Learning structure
Five learning paths (modules), one per area, each with lessons and a quiz:

| Module | Lessons | Quiz questions |
|---|---|---|
| Kinetix 5700: from selection to running axis | 7 | 8 |
| PowerFlex 525: from selection to running motor | 7 | 8 |
| Servo motors: pick the right motor for the axis | 6 | 8 |
| Starters: soft start, protect, and stop the motor | 6 | 8 |
| Studio 5000 motion: from drive to running axis | 8 | 10 |
| **Total** | **34** | **42** |

Every component also has a standalone detail page (Library tab) with the
same training fields, so the app works as a reference as well as a course.

## Data model
### Component (one per family)
`id, category, subcategory?, family, catalogNumbers[], name, whatItIs,
whenToUse, selection, wiring{power, feedback, safety, network},
configuration[{step, screen, parameter, value, source}], commissioning[],
tuning, faults[{code, meaning, fix}], manualUrl, sources[], tbd[]`

- `configuration` steps name the exact screen and parameter as printed in
  the manual, with the publication in `source`.
- `faults` carry verified codes only; unverified codes are not listed.
- `tbd` lists every unverified point with the source needed; the field
  itself reads "TBD" in the app.

### Module
`id, title, family, lessons[{id, title, body, componentIds[]}],
quiz[{q, options[4], answer, explain}], tbd[]?, sources[]?`

### Lesson
`body` is multi-paragraph teaching text in plain language. `componentIds`
link the lesson to the Library detail pages.

## Verification rules (hard)
1. Every procedure, parameter number, and spec must come from a Rockwell
   manual, user manual, or technote actually read. Never invent a parameter
   number, wiring detail, or step.
2. Anything unverified is marked TBD with the source needed. The app shows
   TBD items in a dashed warning box, never as fact.
3. `manualUrl` is the canonical Rockwell literature URL where known;
   `sources[]` lists only URLs actually read (some were mirror hosts —
   see "Access limitation" below).
4. Discontinued families are taught as documented but flagged with their
   replacement (140M → 140MT, PowerFlex 4/40 → 523/525).

## Verified totals (v1.0.0)
- 29 families, 225 verified configuration steps, 223 verified faults,
  34 lessons, 42 quiz questions.
- All 9 Allen-Bradley seed catalog numbers from the 20-platform build are
  present in the deepened family records (assemble.py cross-checks this).

## Known gaps / TBD (108 items)
- **Kinetix (30):** 5300 tuning beyond the tuningless default (→ MOTION-AT005);
  ERS4 safe-monitor detail (→ 2198-RM001 full text); full RD003/RD005/RD006
  fault spreadsheets; 6000 lifecycle status; 5100 24V control-power spec.
- **PowerFlex (27):** 750-series stop-mode parameter numbers (P370/P371);
  exact encoder-feedback terminals on 70/700; 755T user-manual number
  (expected 750-UM003) and TotalFORCE fault events; 70/700/4/40 manual URLs
  to confirm they resolve.
- **Servo motors (25):** TL/TLY fault codes came from a secondary summary,
  not a drive manual; VPL/VPF rated-speed discrepancy (KNX-TD001A says
  4000 rpm, current Rockwell listings say 4500–6600 rpm); TL feedback
  discrepancy (absolute-only vs incremental in the catalog chart); TLY/TL
  catalog numbers verified on distributor pages, not Rockwell pages.
- **Starters (18):** SMC-3 network capability; SMC Flex full fault table
  beyond the Quick Start; SMC-50 EtherNet/IP option-module catalog number;
  140MT tables; 100-C terminal torques; E300 DeviceNet module numbers and
  full LED blink table.
- **Studio 5000 (8):** exact New Module click path in v36/37; SERCOS
  creation steps (MOTION-AT006); MAB confirmation; 5700 DC-bus supply
  I/O-tree add order; full CIP Motion fault-code list (MOTION-RM003);
  whether PowerFlex 525 can be an Integrated Motion axis; tuning-less /
  Load Observer numeric defaults; current-version fault-clear click path.

## Corrections baked in (do not regress)
- The modern axis type is **AXIS_CIP_DRIVE**; AXIS_SERVO_DRIVE is the legacy
  SERCOS type. The Studio 5000 module teaches the CIP path.
- **MAB is not a native Logix motion instruction** (no entry in
  MOTION-RM002L). MAM/MAJ Merge is the verified blending mechanism; quiz Q7
  in the Studio 5000 module tests this.
- The commonly quoted "80:1 inertia mismatch" for Kinetix 5500 was left out
  — it was not found in a Rockwell manual read in this pass.
- P036 is **not** "Start Source" on the 520 series; the correct numbering is
  pinned to Quick Start 520-QS001A.

## Access limitation
`literature.rockwellautomation.com` could not be fetched directly from this
VM (Akamai "Access Denied"). Identical manual revisions were read from
mirror hosts (ManualsLib, manuals.plus, NHP, archive.org OCR, distributor
copies). Each family's `sources[]` lists only URLs actually read. Before
publishing, re-check the flagged mirror-sourced items against the vendor
site: Lenze-style mirror risk applies here to KNX-TD001A (distributor copy),
2198-UM001 fault tables (ManualsLib), and the 6000/300/350 manuals
(archive.org OCR).

## Lifecycle notes
- Bulletin 140M discontinued **31 March 2025**; replacement is 140MT.
- PowerFlex 4/40 discontinued **30 June 2025**; replaced by 523/525.
- Kinetix 6000/6200 and 300/350 are legacy; taught as legacy, not current.

## Open decisions for Pappy
1. Store name confirmation ("AB Motion Control App" is the working title).
2. Free vs Pro (suggestion, not decided: free paths for Kinetix 5700 and
   PowerFlex 525; one-time Pro unlock for the rest — his call).
3. Next content pass: pull the remaining fault tables and close TBDs, or
   grow component coverage first (e.g. more catalog numbers per family).
4. iOS / Play publishing order (Android first, as with the pricing apps).

## Build
- `assemble.py` merges `.research/*.json` into `data/ab-motion-control-data.json`.
- `build.py` inlines the data into `www/index.html` (single file, offline
  from file://). `www/index.template.html` is the source; never edit the
  built `index.html` by hand.
- Nothing published, no repo created, no vendor contacted, nothing spent.
