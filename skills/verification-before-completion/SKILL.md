---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs — requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

# Verification Before Completion

## The Iron Law

NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying

## In Autonomous Mode

When running without human checkpoints (autonomous loop):

AFTER each implementer subagent completes a task:
1. Run the test command for that task
2. Log the full output
3. If tests pass → log "VERIFIED: tests pass" → proceed to spec review
4. If tests fail → log "FAIL: [reason]" → send back to implementer to fix
5. Do NOT claim "tests pass" without having run and read the output

AFTER each quality review pass:
1. If Critical issues found → log "NEEDS WORK: [issues]" → implementer fixes
2. If no Critical issues → log "APPROVED" → proceed

## What Counts as Verification

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Build succeeds | Build command: exit 0 | Logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Spec compliant | Spec reviewer: COMPLIANT | "looks right" |

## Red Flags — STOP

- "Should work now"
- "I'm confident"
- "Tests pass" without running
- Expressing satisfaction before verification
- About to commit without verification
- "Probably works"
