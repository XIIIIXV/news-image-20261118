# ONE DAY ON EARTH — Wednesday, 18 November 2026

[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/XIIIIXV/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/XIIIIXV/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

One image that sums up the world news of **Wednesday, 18 November 2026**,
built for the [make.fun bounty](https://make.fun/bounty/news-image-20261118).
A map-first broadsheet — **42 stories, one planet, one day** — deliberately
unlike a traditional front page: a NEW name, a deep ink/teal + amber
identity, a LARGE dotted world map as the hero (top ~36% of the page) with
amber pins for the 11 biggest stories, a "BY THE NUMBERS" data strip,
stories grouped by THEME (not region), 11 lead cards in three rows
(3 hero + 4 + 4 text cards), a compact bullet index of 31 more stories
("THE REST OF THE DAY"), and a one-line footer.

The news is mostly new as well: 38 of the 42 stories are fresh. Only 4
stories carry over from the earlier draft, and only as one-line index
briefs, never as leads: the Shenzhen summit, Voyager 1, GTA VI, and
Cyclone Akvan.

Every story on the page happened, or was first reported, on Wednesday
18 November 2026. Items first reported on Tuesday 17 November — Nvidia's
results, the Alaska Senate call, the US strike on Qeshm, the Knesset
speaker vote, the Kerch Bridge collapse, the US measles ruling, the
Russian airspace violation, Colombia's Q3 GDP — are deliberately left
out, so the page never misdates anything. All words are real typeset
text (PIL + DejaVu); every picture is a clearly illustrative, stylised
panel (no photorealistic images of real people, no real attack
photography).

## The 11 leads

1. **Missiles over Riyadh as Houthis strike the capital** (WAR · RIYADH) —
   Two cruise missiles bound for Riyadh are intercepted; explosions
   rattle homes across the city. Reuters.
2. **China's humanoid robots are coming home** (TECH · SHENZHEN) — A
   robot already serves ice cream at a Shenzhen park stand; Beijing
   wants them in homes next. Standard Topic.
3. **Glastonbury 2027: Styles, Fender, Eilish — and Cher** (LIFE ·
   SOMERSET) — Harry Styles, Sam Fender and Billie Eilish top the bill;
   Cher takes the legends slot. BBC.
4. **Gaza truce 'on the brink', peace board warns** (WAR · GAZA) — The
   Board of Peace tells the UN the ceasefire nears collapse.
   Board of Peace.
5. **EU 'sugarcoated' Egypt's figures to free loans** (MONEY · CAIRO) —
   Leaked papers say poverty rolls shrank as MEPs were told they grew;
   €3.5bn released. The Guardian.
6. **OpenAI's models now design better chips** (TECH · SAN FRAN) —
   AI-tuned circuits beat AMD GPU blocks by up to 14% — verified on
   real silicon. OpenAI.
7. **India slaps 162.5% levy on Scotch whisky** (MONEY · NEW DELHI) —
   Bulk Scotch faces a duty above the pre-deal 150% rate, sources say.
   Reuters.
8. **Harry: 'I'd rejoin the Army to fight Russia'** (LIFE · LONDON) —
   After a trip to Ukraine, the duke says Britain should be nervous. BBC.
9. **EU approves Indonesia trade and investment deals** (MONEY ·
   BRUSSELS) — The Council signs off the CEPA and investment pacts.
   EU Council.
10. **TJX jumps 10% as shoppers lift retail; Dow falls** (MONEY ·
    NEW YORK) — Target rises 5.6% on strong results; UnitedHealth
    slides 7%. Motley Fool.
11. **Cassava seeks $1bn for Nvidia chips in Africa** (TECH ·
    JOHANNESBURG) — The group talks to US and Gulf investors to build
    AI data centres. TechCabal.

Plus 31 one-line briefs spanning Nigeria, Telkom/Amazon Leo, the APEC
sidelines, the South China Sea, India's climate toll, the ECB race,
Trump's records, the ATP Finals, the ODI series, the Nations League,
FIFA rankings, Gaza, Hormuz, Hizballah, Turkey–Qatar, Iraq, Google's
Genie 4 and Gemini 4 Neon, OpenAI's GPT-6.2, the Tube strike and TfL
hack, the West Bank, Australia's pay gap, Yemen, COP31, and Britain's
EU-rejoin debate — plus the four carried-over briefs (Shenzhen summit,
Voyager 1, GTA VI, Cyclone Akvan).

Themes: WAR 2 · TECH 3 · MONEY 4 · LIFE 2 = 11 leads; 42 stories total.

## How it works

`main.py` (Python 3.13, standard library only) copies the repository's
`entry.png` to `/output/entry.png` — or to `$MAKEFUN_OUTPUT_DIR/entry.png`
outside the grader container. No network, fully deterministic: both runs
write the same bytes (sha256
`02ca90645766f7a15c3dc4aa9778a3d046a357f994e65db0cc2c3a9051bd2540`).

The image is composited by `gen_image.py`: it crops the illustration
panels in `assets/` (generated artwork, fixed files — 4 new AI panels
for Riyadh, the Shenzhen robot, Glastonbury and Gaza, plus 3 drawn by
PIL itself: the balance scale + €3.5bn, the chip + 14%, and the bottle
+ 162.5%), lays them out with PIL, draws the dotted world map from a
Natural Earth land outline (2,231 dots, re-rasterised at 940×371), and
draws all text as real text (DejaVu Serif Bold for headlines and the
masthead, DejaVu Sans for labels, decks and briefs). No network, no
randomness. Run it to regenerate `entry.png`:

```sh
python3 gen_image.py
```

Then run the entry:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Design follows the Impeccable typesetting method (two font families,
a strict size ladder, proximity + hairline rules for grouping, a 4px
spacing scale, body contrast ≥ 4.5:1). Readability was verified by
pixel measurement (every headline, deck, tag, brief and the footer
measured against its container; zero ink in the gaps between cards
and columns) and by zoomed crops of the pin clusters and card edges.

Sources: Reuters · BBC · The Guardian · TechCabal · Motley Fool ·
OpenAI · EU Council · Board of Peace · and wire reports.

## License

MIT. See [LICENSE](LICENSE).
