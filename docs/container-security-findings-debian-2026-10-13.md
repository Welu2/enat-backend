# Container security findings

Scan: 2026-10-13T18:12:53.585369+00:00.
Image: `sha256:b29d201ee1f8e4aedbed8e78a81a9a7f79ec31b10d4c357540749f96b91ec51f`.
Scanner: `aquasec/trivy:0.75.0@sha256:af6acf9a6b85dfe389a1941505c0ce9efef52a4719635e1a962f022a3d855daa`.

Gate: FAIL. 213 high/critical package findings; 47 distinct finding IDs.
These are scanner classifications, not independently established application exploit paths.
No exceptions are accepted. No reported fixed version does not mean that no upstream patch exists.

| Severity | Finding | Affected packages | Fixed versions reported |
|---|---|---|---|
| CRITICAL | CVE-2026-6653 | libxml2 | None for this release |
| HIGH | CVE-2025-69720 | libncursesw6, libtinfo6, ncurses-base, ncurses-bin | None for this release |
| HIGH | CVE-2026-16554 | libcjson1 | None for this release |
| HIGH | CVE-2026-16742 | libsystemd0, libudev1 | None for this release |
| HIGH | CVE-2026-29036 | libcjson1 | None for this release |
| HIGH | CVE-2026-36849 | libtiff6 | None for this release |
| HIGH | CVE-2026-37555 | libsndfile1 | None for this release |
| HIGH | CVE-2026-52490 | libtiff6 | None for this release |
| HIGH | CVE-2026-54369 | libacl1 | None for this release |
| HIGH | CVE-2026-58049 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-64830 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-64832 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-64833 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-64834 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-64835 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-66036 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-66039 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-66040 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-66041 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-66046 | libexpat1 | None for this release |
| HIGH | CVE-2026-67215 | libcjson1 | None for this release |
| HIGH | CVE-2026-67216 | libcjson1 | None for this release |
| HIGH | CVE-2026-70628 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-70632 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-74860 | libxml2 | None for this release |
| HIGH | CVE-2026-75142 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-75143 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-75144 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-75146 | ffmpeg, libavcodec61, libavdevice61, libavfilter10, libavformat61, libavutil59, libpostproc58, libswresample5, libswscale8 | None for this release |
| HIGH | CVE-2026-76642 | bsdutils, libblkid1, liblastlog2-2, libmount1, libsmartcols1, libuuid1, login, mount, util-linux | None for this release |
| HIGH | CVE-2026-76956 | libexpat1 | None for this release |
| HIGH | CVE-2026-76957 | libexpat1 | None for this release |
| HIGH | CVE-2026-77214 | libexpat1 | None for this release |
| HIGH | CVE-2026-78408 | bsdutils, libblkid1, liblastlog2-2, libmount1, libsmartcols1, libuuid1, login, mount, util-linux | None for this release |
| HIGH | CVE-2026-78409 | bsdutils, libblkid1, liblastlog2-2, libmount1, libsmartcols1, libuuid1, login, mount, util-linux | None for this release |
| HIGH | CVE-2026-78410 | bsdutils, libblkid1, liblastlog2-2, libmount1, libsmartcols1, libuuid1, login, mount, util-linux | None for this release |
| HIGH | CVE-2026-86138 | libxml2 | None for this release |
| HIGH | CVE-2026-86139 | libxml2 | None for this release |
| HIGH | CVE-2026-86140 | libxml2 | None for this release |
| HIGH | CVE-2026-86142 | libxml2 | None for this release |
| HIGH | CVE-2026-86143 | libxml2 | None for this release |
| HIGH | CVE-2026-86144 | libxml2 | None for this release |
| HIGH | CVE-2026-87933 | libcjson1 | None for this release |
| HIGH | CVE-2026-88806 | libx11-6, libx11-data, libx11-xcb1 | None for this release |
| HIGH | CVE-2026-88807 | libxrender1 | None for this release |
| HIGH | CVE-2026-93990 | libexpat1 | None for this release |
| HIGH | CVE-2026-9538 | perl-base | None for this release |
