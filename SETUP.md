# How this profile works

Four generated pieces, all built from `scripts/`:

| File | Built by | Refreshed |
|---|---|---|
| `portrait.svg` | `prep_photo.py` → `make_ascii_svg.py` | manually, when you change your photo |
| `info-card.svg` | `make_info_card.py` | on every workflow run |
| `contrib-heatmap.svg` | `fetch_contributions.py` → `make_heatmap.py` | daily via GitHub Action |
| `README.md` | hand-written | whenever you want |

---

## One-time setup

### 1. Push this repo

Copy everything here into your clone of `yuvaraj-dudukuru/yuvaraj-dudukuru`, then:

```bash
git add .
git commit -m "feat: animated profile README"
git push
```

### 2. Turn on the daily refresh

Repo → **Settings** → **Actions** → **General** → *Workflow permissions* →
**"Read and write permissions"** → **Save**.

Then repo → **Actions** tab → **"Update profile art"** → **Run workflow**.

That's it. The heatmap already contains your real data as of the day this was
built, and the Action keeps it current from here on.

---

## Adding your portrait

This is the only step that needs your photo, so it can't be pre-done.

1. Put your photo in the repo root as `source-photo.jpg`
   (front-facing, plain background, decent lighting works best)
2. Install the local-only deps:

```bash
pip install -r scripts/requirements-local.txt
```

3. Generate:

```bash
python scripts/prep_photo.py
python scripts/make_ascii_svg.py
```

4. Open `portrait.svg` in a browser. Don't like it? Tune and re-run:
   - `CHARS` in `make_ascii_svg.py` — the character ramp, dark to light.
     Try `" .:-=+*#%@"` (default), `" ░▒▓█"`, or `" .oO@"`
   - `COLS` — more columns = finer detail, bigger file
   - `CHAR_ASPECT` — raise it if the face looks squashed, lower if stretched
   - In `prep_photo.py`, the `enhance()` values control contrast and brightness

5. Commit `portrait.svg` and push.

**Background removal** is optional. If your photo has a busy background,
`pip install rembg` and re-run `prep_photo.py` — it'll detect it and use it.
It's a large ML download, which is why it isn't required.

---

## Editing your info card

Open `scripts/make_info_card.py`, edit the `ROWS` list, run:

```bash
python scripts/make_info_card.py
```

The Action also regenerates this on every run, so once it's pushed you can
edit `ROWS` on GitHub directly and the SVG rebuilds itself.

---

## Changing the colours

Every script has its palette constants at the top. The accent is `#14b8a6`
(teal). Search and replace across `scripts/` to change the whole thing at once.

---

## Troubleshooting

**Heatmap is empty or the workflow fails**
GitHub occasionally changes the calendar markup. `fetch_contributions.py` exits
loudly if it finds no cells — that's the signal the selectors need updating
(`td.ContributionCalendar-day` and the `tool-tip` elements).

**Workflow fails with a permissions error**
Workflow permissions weren't set to read-write. See step 2 above.

**Portrait shows the placeholder box**
`data/prepped.png` doesn't exist — run `prep_photo.py` first. Note that
`data/prepped.png` is gitignored, so `make_ascii_svg.py` on CI would also hit
this; that's why the portrait is generated locally and committed, not built by
the Action.

**SVGs don't animate on GitHub**
GitHub allows SMIL animation in SVGs but strips JavaScript. Everything here uses
`<animate>` elements, which work. If animation stops, check you haven't
introduced a `<script>` tag.
