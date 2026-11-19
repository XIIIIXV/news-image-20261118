# WORLD NEWS — Wednesday, 18 November 2026

[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/XIIIIXV/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/XIIIIXV/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

One image that sums up the world news of **Wednesday, 18 November 2026**,
built for the [make.fun bounty](https://make.fun/bounty/news-image-20261118).
A newspaper front page: masthead + date, then the six stories that defined
the day — lead, two secondary, three more — each with a short accurate
headline, a one-line deck, and a hand-drawn pictogram.

## The six stories

1. **Summit in Shenzhen** — Trump lands in Shenzhen; Xi meets Putin.
   First US–China–Russia summit set for Thursday at APEC.
2. **Gulf crisis** — Iran drones target the US base in Kuwait. Kuwait and
   Bahrain intercept drones; the US hits a missile site on Qeshm.
3. **War in Ukraine** — Ukraine strikes the Kerch Bridge again. Day two of
   strikes; Russia claims 1,400 drones downed.
4. **US politics** — Peltola wins Alaska; Democrats take 56–44. Senate now
   56–44; ninth flip, biggest since 2009.
5. **Tech** — Nvidia rejects Huang's return. Record $115.8B quarter amid
   transition.
6. **Disaster** — Cyclone Akvan bears down on Odisha. Odisha evacuates;
   schools shut.

Sources: AP, Reuters, AFP, USA Today, Al Jazeera, The Hindu.

## How it works

`main.py` (Python 3.13, standard library only) copies the repository's
`entry.png` to `/output/entry.png` — or to `$MAKEFUN_OUTPUT_DIR/entry.png`
outside the grader container. No network, fully deterministic: both runs
write the same bytes.

The image itself is drawn by `gen_image.py` (PIL primitives + DejaVu fonts,
no network, no randomness). Run it to regenerate `entry.png`:

```sh
python3 gen_image.py
```

Then run the entry:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT. See [LICENSE](LICENSE).
