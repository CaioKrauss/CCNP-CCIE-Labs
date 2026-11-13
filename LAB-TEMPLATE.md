# LAB <number> — <Topic>

## Objective and status

State the exact question, platforms, date and scope. Mark the lab planned, configured, control-plane verified or traffic-tested. Do not describe expected behavior as an observation.

## Topology and addressing

Add a real, reviewed screenshot when available. Label reconstructed diagrams as diagrams. Identify every tested path and any visible but untested nodes.

## Mechanism and hypothesis

Explain the packet/control-message path in plain language. State what should happen and what would disprove the hypothesis. Link authoritative technical references.

## Configuration and purpose

Show platform-specific excerpts and explain what each enables. Identify prerequisites. Distinguish existing configuration from changes actually applied.

## Verification

| Question | Device / command | Expected result | Observed result | Explanation |
|---|---|---|---|---|
| <question> | <command> | <prediction> | <captured output or not tested> | <why> |

## Data-plane test

Specify source, destination, packet count/size and relevant timing. Preserve exact results. Explain the return path and any difference between local reception and transit forwarding.

## Troubleshooting or controlled failure

Record baseline, authorized change, symptom, diagnosis, restoration and recovery evidence. Keep disruptive actions separate from read-only checks.

## Evidence and configuration snapshots

Link actual outputs, collection time, platform/version and reviewed configurations. Document redactions, normalization and hashes where used.

## Conclusions and limits

State what the results establish, what remains unknown and the next useful test. Do not infer whole-network health from one passing ping.
