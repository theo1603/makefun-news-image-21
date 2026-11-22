# makefun-news-image-21

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/theo1603/makefun-news-image-21/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/theo1603/makefun-news-image-21/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image summing up the world news of Saturday 21 November 2026: a
newspaper-style poster with the day's six biggest stories — Russian missiles
landing in Poland, the tech-stock crash, COP31 running into overtime, the
Trump–Xi–Putin summit in Shenzhen, the 6.9 quake in the Peruvian Andes, and
the Hormuz tanker attacks at a wartime high — plus a ticker of the rest in
brief. `draw_poster.py` (Pillow, run at build time) drew the poster from
stories reported that day; `main.ts` copies the finished `entry.png` to the
output directory. Deterministic, no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
