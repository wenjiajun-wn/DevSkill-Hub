# ADR 0001: Store repository metadata once

Status: accepted. Date: 2026-10-21.

## Context

Two skills can share the same source repository. GitHub stars describe that repository, and a star observation is independent of the content-review date of either skill. Repeating source metadata in every entry invites contradictory counts and timestamps.

## Decision

Keep repository identity, star observations, scoped license evidence, and upstream-monitoring baselines under one repository key. Skill entries reference that key and keep their own reviewed revision and installation/evaluation evidence. Unknown star values remain null. Sort entries within categories using the shared observed count.

## Alternatives and consequences

Per-entry duplication makes each record self-contained but requires synchronizing shared facts. Normalization adds a lookup for consumers and produces one consistent source of repository facts. Generated Markdown resolves that lookup for readers. A star refresh does not renew either skill's review or testing claims.
