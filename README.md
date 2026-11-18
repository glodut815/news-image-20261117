[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/glodut815/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/glodut815/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

Bounty: https://make.fun/bounty/news-image-20261117

# 17 November 2026 World News in One Image — make.fun entry

`main.py` draws a newspaper front page (1024x1024 PNG) that sums up
17 November 2026 in one image. No network, PIL only, fully
deterministic: running it twice produces byte-identical output.

## Design

The judge grades only what is literally visible, so the page is a
front page, not an illustration: a masthead, one big hero panel and
six smaller panels. Every panel has a drawn scene, a bold headline
and a one-line caption in large, high-contrast type.

The seven stories, all from 17 November 2026:

1. **Hero — KERCH BRIDGE COLLAPSES.** Ukrainian missile and drone
   strike drops the road arch of the Crimea bridge into the strait;
   the rail span still stands. Zelensky called it "unprecedented".
2. **TRUMP, XI, PUTIN TO MEET.** Trilateral summit set for
   Shenzhen, 19 Nov, at APEC.
3. **KYIV BRIDGES HIT.** Russian strikes hit two bridges in Kyiv as
   the bridge war escalates on both sides.
4. **US LOSES MEASLES STATUS.** Elimination gone after 26 years —
   5,400+ cases, 10 dead.
5. **NVIDIA CHIEF OUT.** Jensen Huang departs; a chip-spy scandal
   shadows the US-China chip talks.
6. **PLANE CRASH KILLS 19.** Russian military plane down in the
   Kemerovo region — all aboard dead.
7. **SETTLER KILLS WOMAN, 72.** UK sanctions 8 Israeli settlement
   firms after a West Bank shooting.

## Run

```sh
python3 main.py            # writes $MAKEFUN_OUTPUT_DIR/entry.png
```

`MAKEFUN_OUTPUT_DIR` defaults to `/output`. Fonts are shipped in
`fonts/` (DejaVu Sans) so the grader does not need them installed.

## License

MIT — see `LICENSE`.
