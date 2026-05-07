# hear-it

A Claude Code plugin that plays a mechanical-keyboard typing sound while
the agent is writing or editing files. macOS only — uses `afplay`.

The duration of the sound scales with how much is being written, so a
one-character edit gives you a short blip and a multi-thousand-character
file write gives you a longer typing run (looped if it exceeds the clip
length).

## Install

```
/plugin marketplace add <owner>/hear-it
/plugin install hear-it@shelden
/reload-plugins
```

Or from a local clone:

```
git clone https://github.com/<owner>/hear-it.git
/plugin marketplace add /absolute/path/to/hear-it
/plugin install hear-it@shelden
/reload-plugins
```

## How it works

- `hooks/hooks.json` registers a `PreToolUse` hook that matches `Write`,
  `Edit`, and `NotebookEdit`.
- `hooks/typing.sh` reads the hook payload from stdin and hands it off to
  `hooks/play.py` in the background, returning immediately so the tool
  call is never blocked.
- `hooks/play.py` derives a duration from the size of the content being
  written (`CHARS_PER_SECOND = 250`, clamped to `[0.4s, 15s]`) and loops
  `hooks/sounds/typing.mp3` until the budget is up.

## Tuning

Edit `hooks/play.py`:

| Constant | What it does |
| --- | --- |
| `CHARS_PER_SECOND` | Lower → longer sound per character. |
| `MIN_SECONDS` | Floor for tiny edits. |
| `MAX_SECONDS` | Ceiling for very large writes. |
| `VOLUME` | Passed to `afplay -v` (0.0–1.0). |

To use a different audio file, drop it in `hooks/sounds/` and update the
`SOUND` path in `hooks/typing.sh`.

## Credits

Audio: `hooks/sounds/typing.mp3` is "Keyboard Typing Sound Effect" by
Dragon Studio, sourced from
[Pixabay](https://pixabay.com/sound-effects/) and used under the Pixabay
Content License.

## License

Code is MIT (see `LICENSE`). The bundled audio file is governed by the
Pixabay Content License referenced above.
