# User Profile

## Profile Type
type: developer
# Options: non-technical | developer | experienced-developer
#
# non-technical   → plain English explanations, lower auto-select threshold,
#                   max 2 options presented, YOLO defaults on
# developer       → standard trade-off explanations, full options presented,
#                   YOLO defaults off
# experienced-developer → same as developer, skip introductory context in summaries

## YOLO Mode
default: off
# Can be overridden at the start of Phase 6 each session.
# YOLO only applies during execution (Phase 6) — architectural gates always hold.
# Exception: when profile type is non-technical, this defaults to on.

## Communication Style
explanation-depth: standard
# Options: minimal | standard | detailed
jargon: some
# Options: none | some | full
