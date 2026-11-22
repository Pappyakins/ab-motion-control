# AB Motion Control App

A training app for Allen-Bradley motion control: servo drives, VFDs, servo
motors, and starters. It teaches how to use the components — selection,
wiring, configuration, commissioning, tuning, and faults — deep, not surface.

Allen-Bradley only, motion control only. The 20-platform catalog seed it
grew out of lives untouched at `~/workspace/motion-control/` as reference
for later apps in the series.

## Run it locally

Open `www/index.html` in any browser. It works offline from `file://` —
all content is inlined into the single file, no server needed.

```sh
# rebuild after editing data or the template
python3 assemble.py   # merges .research/*.json -> data/ab-motion-control-data.json
python3 build.py      # inlines data into www/index.html
```

Edit `www/index.template.html`, never the built `www/index.html` by hand.

## Contents (v1.0.0)

- 29 families: 9 Kinetix servo drives, 8 PowerFlex VFDs, 6 servo motor
  families, 6 starters/protection families
- 5 learning paths, 34 lessons, 42 quiz questions
- 225 verified configuration steps, 223 verified faults
- 108 TBD items (see SPEC.md for the full list)

## What is TBD

- Fault tables for TL/TLY motors (secondary source only, not a drive manual)
- 750-series stop-mode parameters, 755T TotalFORCE fault events
- Kinetix 5300 tuning beyond the tuningless default
- SMC-50 EtherNet/IP option-module catalog number, E300 full LED blink table
- Several manual URLs to confirm they resolve (70/700/4/40)
- Some manuals were read from mirror hosts because
  literature.rockwellautomation.com blocks direct fetch from this VM;
  re-check those against the vendor site before publishing

## Decisions still needed from Pappy

1. Store name confirmation ("AB Motion Control App" is the working title)
2. Free vs Pro
3. Next content pass: close TBDs / fault tables, or grow coverage first
4. Publishing order (Android first, as with the pricing apps)
