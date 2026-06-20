# Radio Astronomy on Mastodon

After the upheaval on Twitter/X, a large slice of the astronomy community moved to
**Mastodon** and the wider **Fediverse**. It's an excellent place to follow real research as it
happens, ask questions, and meet working radio astronomers.

This is a small, **hand-verified** list — every account in the tables below was confirmed to
resolve to a real profile with an on-topic bio and genuine post history (checked 2026-06-19).
We deliberately kept it short and trustworthy rather than padding it with unverified handles:
several plausible-looking institutional handles turned out to belong to *unrelated people*, so
when in doubt, we left it out. The instances and hashtags at the bottom are the most reliable way
to discover more.

!!! tip "Finding people"
    Astronomers cluster on community instances like **astrodon.social** and **fediscience.org**.
    The fastest way to find more radio astronomers is to follow the hashtags below and the
    institutional accounts, then see who they boost and reply to.

## Observatories, instruments & institutions

| Account | Handle | What | Link |
|---|---|---|---|
| ASTRON | `@astron@mastodon.nl` | Netherlands Institute for Radio Astronomy — LOFAR, WSRT & SKA | [profile](https://mastodon.nl/@astron) |
| ESO | `@esoastronomy@mastodon.social` | European Southern Observatory (operates ALMA & APEX, among others) | [profile](https://mastodon.social/@esoastronomy) |
| Event Horizon Telescope | `@ehtelescope@mastodon.social` | Global VLBI network that imaged a black hole | [profile](https://mastodon.social/@ehtelescope) |
| Dwingeloo Radiotelescoop (CAMRAS) | `@radiotelescoop@mastodon.nl` | Historic 1956 Dwingeloo radio telescope, operated by Stichting CAMRAS | [profile](https://mastodon.nl/@radiotelescoop) |
| NRAO #HamRadio Project | `@nrao_hamradio@mastodon.hams.social` | NRAO outreach — "Exploring the EM Spectrum with Ham Radio" | [profile](https://mastodon.hams.social/@nrao_hamradio) |

## Astronomers & science communicators

| Account | Handle | What | Link |
|---|---|---|---|
| Tessa Vernstrom | `@tvern@mastodon.social` | Radio astronomer, ICRAR (Perth); EMU Survey Project Scientist | [profile](https://mastodon.social/@tvern) |
| Heino Falcke | `@hfalcke@mastodon.social` | Professor of Astrophysics, Radboud University; Event Horizon Telescope | [profile](https://mastodon.social/@hfalcke) |
| Robert Minchin | `@Robminchin@mastodon.online` | Astronomer at NRAO; formerly Arecibo & SOFIA | [profile](https://mastodon.online/@Robminchin) |
| Juan Carlos Muñoz | `@astro_jcm@mastodon.online` | Astronomer & science communicator; Media Officer at ESO | [profile](https://mastodon.online/@astro_jcm) |
| Benjamin Winkel | `@HIprocessor@mastodon.social` | Radio astronomer, MPIfR/Effelsberg; HI4PI / EBHIS surveys; CRAF chair | [profile](https://mastodon.social/@HIprocessor) |
| Andreas Brunthaler | `@brunthal@mastodon.social` | Astronomer, MPIfR; Milky Way & Sgr A* VLBI (Reid & Brunthaler 2004) | [profile](https://mastodon.social/@brunthal) |
| Rami Mandow (CosmicRami) | `@CosmicRami@aus.social` | Pulsar astronomer (Parkes "Murriyang") & science communicator | [profile](https://aus.social/@CosmicRami) |

## Instances, groups & hashtags

**Astronomy-focused instances** — good places to find (and host) astronomers:

- **[fediscience.org](https://fediscience.org)** — an active social network for working scientists; a common home for astronomy researchers.
- **astrodon.social** — the long-standing astronomy/astrophysics community instance ("The Astro Community") and the source of the widely-used `#astrodon` tag. *Note: its availability has been intermittent and some users are migrating off it, so its long-term status is uncertain.*
- **[mastodon.social](https://mastodon.social)** and **[mastodon.online](https://mastodon.online)** — large general instances where many astronomers also post.

**Useful hashtags for discovery:**

`#radioastronomy` · `#astronomy` · `#astrophysics` · `#astrodon` (the astronomy-community
cross-instance tag) · topic tags like `#pulsars`, `#FRB`, `#VLBI`, `#SKA`.

## Read the feed in your terminal

The course ships a small reader that pulls these accounts' recent **public** posts straight from
Mastodon's API — no login or token needed — and shows them as text or in a terminal UI with
inline images:

```bash
# plain text (works anywhere, no extra dependencies)
uv run python -m jansky.mastodon_reader --no-tui --limit 3

# the terminal UI with image viewing (needs the optional extra)
uv sync --extra tui
uv run python -m jansky.mastodon_reader        # or: make mastodon
```

It reads the handles directly from this page, so the feed stays in sync with the list above.
Images render inline in terminals that speak the **kitty**, **iTerm2**, or **sixel** graphics
protocols (kitty, WezTerm, iTerm2, Konsole, foot, …); elsewhere they fall back to Unicode blocks.
In the UI: arrow keys to browse, `o` to open a post in your browser, `r` to refresh, `q` to quit.

---

!!! note "This list is a snapshot"
    Handles and instance availability change over time, and this is only a small sample of
    *public, professional* accounts. If you'd like to be **added or removed**, please open an
    issue on the repository. For more of the radio-astronomy community — forums, societies, and
    YouTube channels — see [Field Notes](field-notes.md#communities-worth-your-time) and
    [Resources](resources.md).
