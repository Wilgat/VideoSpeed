# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.12 (current) | Yes |
| 1.0.11 | Yes |
| 1.0.10 | Yes |
| 1.0.9 | Yes |
| Older releases | Best-effort; prefer upgrading to current |

## Reporting a Vulnerability

Please **do not** open a public issue for security-sensitive reports when a private channel is available.

**Maintainer contact (email):** `wilgat.wong@gmail.com`

- Source of contact: product **author-email** SSOT in [`LICENSE.md`](./LICENSE.md) (Copyright line).
- Prefer email for vulnerability details, reproduction steps, and impact.
- You should receive an acknowledgment when the report is received and actionable.
- Do not include exploit weaponization guides in public channels.

## Security Design Principles (CIAO)

This project follows **[CIAO](https://github.com/cloudgen/ciao)** / **CIAO-Lite** defensive design. Security-relevant intent:

| Letter | Principle | Security application |
|--------|-----------|----------------------|
| **C** | **Caution** | Assume missing tools and unexpected media. Fail closed when FFmpeg is missing from `PATH`. Re-prompt or refuse invalid cut ranges and length percents outside 20–200%. Do not claim success on a failed encode. |
| **I** | **Intentional** | FFmpeg is invoked with argument lists (not a shell-interpolated free-form filter graph). Intermediate files are staged next to the output when writable. Source media is never the final output path. |
| **A** | **Anti-fragile** | Multi-mount publish (USB vs system temp) uses same-filesystem staging plus `shutil.move`. Unique temp names avoid fixed cwd races. |
| **O** | **Over-protect** | Protection Zones on staging/publish helpers; least privilege day-to-day (user-level CLI; no root elevation product surface). |

Full principles: [CIAO Defensive Programming](https://github.com/cloudgen/ciao) · agent contract: [CIAO-Lite](https://github.com/cloudgen/ciao-lite).

This section describes **design posture**. It is **not** a claim of third-party certification.

## Scope notes

- VideoSpeed is a **local** interactive CLI. It does **not** implement online install channels or companion `.sha256` download integrity.
- Prefer keeping untrusted media and scripts offline unless you trust their origin.
- Related product docs: [`README.md`](./README.md), [`LICENSE.md`](./LICENSE.md).
