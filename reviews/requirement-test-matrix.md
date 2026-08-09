# Requirement ↔ test matrix — VideoSpeed

**Updated:** 2026-08-09  
**Suite:** not present yet — map is the design SSOT until `tests/` lands

| Requirement key | Area | TP families | Coverage notes |
|-----------------|------|-------------|----------------|
| requirement-class-software-dev | class | TP-PKG-04 · TP-STRUCT-01 | Python residual; stack honesty |
| requirement-domain-videospeed | domain | TP-DOMAIN-* · TP-FFMPEG-01..05 · TP-CLI-03 | Four pillars; workflow |
| requirement-video-ffmpeg-pipeline | video | TP-FFMPEG-* · TP-FS-* · TP-ERR-03 | Ops SSOT; **shutil.move**; temps |
| requirement-python-cli-interface | python | TP-CLI-* | Type N interactive; help/version |
| requirement-python-coding-style | python | TP-FS-01..02 · TP-PKG-01 | Move/temp coding rules |
| requirement-python-packaging | python | TP-PKG-* | Manifest + version dual SSOT |
| requirement-python-project-structure | python | TP-STRUCT-01 | src layout; ship SSOT |
| requirement-python-error-handling | python | TP-ERR-* · TP-CLI-04..05 | Fail closed; source safe |
| requirement-runtime-prerequisites | runtime | TP-PRE-* | FFmpeg + OpenCV honesty |

**Absent by design (no TP Core):** online-install, remote self-management, automatic channel checksum, Type 1 sudoers elevation.
