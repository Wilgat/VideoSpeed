**file**: docs/requirements/requirement-python-json-output.md
**Status**: Active (Version 1.0.3)
**Area**: python
**Key**: `requirement-python-json-output`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite (Caution • Intentional • Anti-fragile • Over-engineered / Over-protect)

## 1. Purpose

This file is the `--json` switch for VideoSpeed. When that switch is set, both the question walk and the one-job path keep their decisions from `requirement-python-interactive-vs-noninteractive`, and the screen stays closed. Standard output is one JSON object and nothing else. Progress text does not share that stream.

The path decision stays on the mode requirement. The screen picture stays on `requirement-python-tui`. Console failure sentences stay on `requirement-python-error-handling`. Durable status lines stay on `requirement-python-cli-logging`. This file owns the object those paths emit.

### 1.1 Human-facing

**In one sentence:** Add `--json` and the program prints one JSON object on standard output, with no text menu and no progress mixed in.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | Person or script that wants data, not a screen | `video-speed --json --file clip.mp4 --start 0 --end 5` |
| The other role | The walk or the one job underneath | Same fields as the mode requirement |
| Not this file | Frame glyphs; which flag selects a job | `requirement-python-tui`, the mode requirement |

| Includes | Excludes |
|----------|----------|
| One pretty-printed JSON object on standard output | A second object, a progress line, or the text menu on that stream |
| The question walk with prompts on the error stream | `--quiet` as a separate flag |
| The same object shape for a job and for a walk | `--help` and `--version` rewritten as JSON |

| Surface | What you open | What for |
|---------|---------------|----------|
| `video-speed --json` | console script on a terminal | questions on the error stream, then one object |
| `video-speed --json --file clip.mp4 --start 0 --end 5` | one job | one object, no questions |
| `src/VideoSpeed/run_output.py` | class `RunOutput` | the only standard-output write for this switch. Shape unchanged. `TP-OOP-04` has landed |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Ask in a terminal and keep the result as data | The menu stays closed. Each question is one line on the error stream. Standard output is one object after the walk ends. End of input ends the walk and does not encode the open question. | `video-speed --json` |
| Run one clip as data | The job flags are unchanged. Progress lines are not printed. The object has at most one job. | `video-speed --json --file clip.mp4 --start 0 --end 5` |
| Pass a flag that cannot run | The program exits non-zero. The object says why, and names a next step when there is one. | `video-speed --json --percent 50` |

## 2. Core Rules (Mandatory)

1. **One switch.** `--json` **MUST** be a boolean flag. It **MUST NOT** select the job by itself and **MUST NOT** be ignored. It **MUST** be named on `requirement-python-cli-interface` and on `requirement-python-interactive-vs-noninteractive`.
2. **No screen.** When `--json` is set, `main` **MUST NOT** open the text menu and **MUST NOT** draw a frame. A terminal with no product verb and no selector, and a terminal running `edit` while a target is still missing, **MUST** ask the fields the mode file still marks as missing, one at a time, on the error stream, folder before the specific file, and **MUST** read the answer from standard input. End of input **MUST** end the walk without encoding the open question. `help` **MUST** stay the human usage text, as `--help` does. `about`, `hello`, and `list-mp4` **MUST NOT** enter the edit walk. A folder question that `list-mp4` still needs is on the error stream. The about page, the hello line, and the MP4 list go to the error stream. Standard output for those three verbs stays this one object, with `jobs` empty.
3. **Quiet standard output.** When `--json` is set, informational progress **MUST NOT** be written to standard output. FFmpeg **MUST NOT** inherit standard output. The only standard-output bytes **MUST** be one JSON object, pretty-printed with two-space indent, then a single newline. No banner before it and no second value after it.
4. **Same shape.** The object **MUST** use the keys below, in this order. `mode` **MUST** be `interactive` only when the question walk was entered. Every other `--json` run **MUST** use `noninteractive`, including a fail-closed stop. `jobs` **MUST** be an array. A job path has at most one element. A walk may have one element per finished encode. `ok` **MUST** be true only when the process exit is 0.
5. **Errors.** A terminal failure **MUST** set `error` to the failure sentence and `ok` to false, and **MUST** exit non-zero. `next` **MUST** be the next-step sentence when the failure has one, otherwise null. The human sentence **MAY** also be written to the error stream. It **MUST NOT** be written to standard output outside the object. A re-ask during the walk **MUST NOT** freeze `error`.
6. **Help and version.** `--help` and `--version` **MUST** still finish inside the parser as human text, even if `--json` is also present. They **MUST** exit 0. They are not this object.
7. **Not a logger.** ChronicleLogger **MUST NOT** encode this object. `quiet(True)` on that logger is not this switch. While `--json` is set, a future console mirror **MUST** stay quiet so status lines do not join standard output.
8. Actor / role / subject / approver: **considered**. No dest machine. No approver. The table stays on `requirement-class-software-dev.md`.
9. Dest fence conditions: **considered — none**. Do not invent one.

### 2.1 Object

| Key | JSON type | Meaning |
|-----|-----------|---------|
| `ok` | boolean | True only when the process exits 0 |
| `mode` | string | `interactive` if the question walk was entered; otherwise `noninteractive` |
| `app` | string | `VideoSpeed` |
| `version` | string | Package version from `requirement-python-version` |
| `error` | string or null | First terminal failure, without a second stdout copy |
| `next` | string or null | Next step, when the failure names one |
| `jobs` | array | Finished encodes. Empty when nothing was encoded |

Each job object, in this order:

| Key | JSON type | Meaning |
|-----|-----------|---------|
| `file` | string | Source MP4 path |
| `start` | number | Cut start seconds |
| `end` | number | Cut end seconds |
| `percent` | number | Length percent. 100 when omitted on the job path |
| `boomerang` | boolean | Reverse pass. False when omitted |
| `output` | string | Final file path |

There is no `--quiet` flag. `--json` is the quiet switch for standard output.

### 2.2 Samples

Failure, modifier alone:

```json
{
  "ok": false,
  "mode": "noninteractive",
  "app": "VideoSpeed",
  "version": "1.0.7",
  "error": "--percent and --boomerang need --file, --start, and --end.",
  "next": "video-speed --file clip.mp4 --start 0 --end 5",
  "jobs": []
}
```

Success, one job (paths are the paths the run used):

```json
{
  "ok": true,
  "mode": "noninteractive",
  "app": "VideoSpeed",
  "version": "1.0.7",
  "error": null,
  "next": null,
  "jobs": [
    {
      "file": "clip.mp4",
      "start": 0.0,
      "end": 5.0,
      "percent": 100.0,
      "boomerang": false,
      "output": "clip_cut0.0-5.0s_100pct.mp4"
    }
  ]
}
```

Walk entered, then end of input before a folder:

```json
{
  "ok": true,
  "mode": "interactive",
  "app": "VideoSpeed",
  "version": "1.0.7",
  "error": null,
  "next": null,
  "jobs": []
}
```

The version string in these samples is the package version at the time of writing. A later package version **MUST** appear in `version` instead.

Invocations:

```text
video-speed --json
video-speed --json --file clip.mp4 --start 0 --end 5
video-speed --json --percent 50
```

### 2.3 Walk prompts (stderr only)

The labels match the mode file. They are written to the error stream. Empty answers use the same defaults. An invalid value re-asks and does not encode.

| Field | Prompt label | On failure under `--json` |
|-------|--------------|----------------------------|
| Folder | `Folder (Enter = current):` | Not a directory: re-ask. No MP4: say so and re-ask the folder. There is no menu to return to |
| Video | `Choose video (1–N):` | Bad index or unreadable duration: re-ask the video |
| Start | `Start seconds (default 0.0):` | Invalid range: re-ask start. Do not encode |
| End | `End seconds [{duration:.3f}]:` | Same as start |
| Percent | `New length % [100%]:` | Outside 20–200: re-ask start. Do not encode |
| Boomerang | `Make it go forward + backward (y/n) [n]:` | Anything other than y/yes/n/no: re-ask |
| Again | `Again? (y/n):` | Empty means no. No ends the walk. Yes repeats the cut on this video |

End of input at any row ends the walk. A missing `ffmpeg` before the first question ends the walk with `ok` false. The job path still does not ask again.

### 2.4 Implementation Notes (this project)

| Item | Value |
|------|--------|
| **Flag** | `--json` on `Cli.build_parser` in `src/VideoSpeed/cli.py`. `def main` stays in that file |
| **Quiet channel** | `RunOutput.out_info` writes nothing while the switch is set |
| **Result writer** | Class `RunOutput` in `src/VideoSpeed/run_output.py`. The emit runs after dispatch returns. Shape in this file is unchanged. `TP-OOP-04` has landed |
| **Walk** | Class `EditWalk` in `src/VideoSpeed/edit_walk.py` when the switch is set, no selector is set, and stdin is a terminal |
| **Job** | `Encoder.batch_session`, then one job object |
| **Indent** | two spaces, `ensure_ascii` false, one trailing newline |
| **FFmpeg** | standard output and standard error are captured while the switch is set |
| **Privilege** | normal user privilege |

### 2.5 Why This Requirement Exists (Direct CIAO Alignment)

- **CIAO Principle 5 – SSOT** (https://github.com/cloudgen/ciao): Standard output has one writer when `--json` is set.
- **CIAO Principle 1 – Caution** (https://github.com/cloudgen/ciao): A failure is inside the object and the process exits non-zero. Progress cannot be mistaken for the object.
- **CIAO Principle 2 – Intentional** (https://github.com/cloudgen/ciao): The walk and the job share one shape. The switch does not invent a second job language.
- **CIAO Principle 16 – Interactive** (https://github.com/cloudgen/ciao): A person can still answer, on the error stream, without a screen.

## Under command line for normal user only

On Termux, Git Bash, Windows cmd, or the same class, **admin privilege** and **dedicated system user privilege** stay unused. **This requirement:** `--json` **MUST NOT** call `sudo`, wrap `apt` / `dnf`, create a dedicated account, or recommend `sudo pip` or `sudo curl \| sh`. Git Bash and Windows cmd **MUST NOT** invoke Termux `pkg`. The object is data. It does not escalate.

## 3. Design Principles (CIAO / CIAO-Lite)

- **Caution:** One object, then stop. Do not encode on a bad range.
- **Intentional:** The key order and the two modes are named.
- **Anti-fragile:** Pipes and a missing terminal still return one object and a non-zero exit.
- **Over-protect (Principle 20):** Do not add a second JSON shape, and do not let the text menu open behind this switch.

## 4. Protection Rule (Sacred)

**Future AI assistants or maintainers MUST NOT:**

- Open the text menu when `--json` is set.
- Write progress, a banner, or a second JSON value to standard output while the switch is set.
- Let FFmpeg inherit standard output while the switch is set.
- Treat `--json` as a job selector or as `--quiet`.
- Encode this object with ChronicleLogger.
- Drop `error` or `jobs` from the object.
- Put the question labels on standard output.

## 5. Design-time verification

| ID | Suite | Status |
|----|-------|--------|
| TP-JSON-01 | `tests/test_json.py` | have |
| TP-JSON-02 | `tests/test_json.py` | have |
| TP-JSON-03 | `tests/test_json.py` | have |
| TP-JSON-04 | `tests/test_json.py` | have |
| TP-JSON-05 | `tests/test_json.py` | have |

TP-JSON-01 asserts `--json --percent 80` exits 1, does not open the menu, and writes one object with `ok` false. TP-JSON-02 asserts `--json --file` without start and end is one object and does not encode. TP-JSON-03 asserts `--json` with no terminal is one object and names the missing terminal. TP-JSON-04 asserts a terminal plus `--json` asks the folder line on the error stream, does not call `open_text_menu`, and writes one `interactive` object. TP-JSON-05 asserts `--json --version` stays human text and exits 0.

**Matrix:** `reviews/requirement-test-matrix.md`
**Map:** `reviews/test-plan.md`.

## 6. Related artifacts

| Artifact | Role |
|----------|------|
| `docs/requirements/index.md` | Registry |
| `docs/requirements/requirement-python-cli-interface.md` | Names `--json`; help and version stay human |
| `docs/requirements/requirement-python-interactive-vs-noninteractive.md` | Which path runs; the screen stays closed under this switch |
| `docs/requirements/requirement-python-error-handling.md` | Failure sentences that `error` repeats |
| `docs/requirements/requirement-python-cli-logging.md` | Durable status; not this encoder |
| `docs/requirements/requirement-python-version.md` | String stored in `version` |
| `docs/requirements/requirement-class-software-dev.md` | Approver none; no dest fence |
| `src/VideoSpeed/cli.py` | Class `Cli`. The `--json` flag. `def main` stays here |
| `src/VideoSpeed/run_output.py` | Class `RunOutput`. The one writer. `TP-OOP-04` has landed |
| `src/VideoSpeed/edit_walk.py` | Class `EditWalk`. The stderr questions. `TP-OOP-04` has landed |
| `docs/requirements/requirement-python-oop.md` | Class homes. This file keeps the object shape |

## 7. Status history

| Date | Status | Note |
|------|--------|------|
| 2026-10-01 | Active 1.0.0 | `--json` quiets stdout to one object and skips the text menu |
| 2026-10-01 | Active 1.0.1 | `edit` under `--json` asks missing targets on the error stream, folder then file. `about`, `hello`, and `list-mp4` do not enter that walk |
| 2026-10-01 | Active 1.0.2 | The writer is class `RunOutput`. The walk is class `EditWalk`. The object shape is unchanged. `TP-OOP-04` is todo |
| 2026-10-01 | Active 1.0.3 | `RunOutput` and `EditWalk` are on disk. `TP-OOP-04` has landed. The object shape is unchanged |

**Last Updated**: 2026-10-01
**Owner**: VideoSpeed project maintainers
**Alignment**: Registry `docs/requirements/index.md`; CIAO (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
