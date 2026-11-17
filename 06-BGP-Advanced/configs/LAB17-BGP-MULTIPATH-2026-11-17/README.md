# LAB 17 — Final configuration collection pending

No current running-config was available in the retrieved chat or workspace. No CFG file in this directory is claimed as the final LAB 17 state.

The existing [historical XR snapshot](../../../03-Segment-Routing/configs/LABS12-16-2026-11-17/README.md) is from 20261117-022341.zip, collected at 2026-11-17 02:23:43 -03:00 (05:23:43 UTC). LAB 17's output is from 05:34:22 UTC. Preserve the older files as historical evidence; do not use them as current configurations for LABs 13–17 or as independent restore points.

## Requested backup

- Generate a new XR1/XR2 export with the existing local XR collector, `backup_sr_mpls.py`, after checking its console mapping locally.
- Also supply R1/R2 `show running-config` from this BGP topology. The repository's IOS collector requires the correct local device mapping and is not an IOS XR collector.
- Include capture timestamps/timezone, device names, software versions, manifest and hashes. Review secrets before public upload.
- Preserve historical LAB 13–15 outputs and LAB 16 AS-PATH/MED before/after logs if available; a current backup cannot recreate removed intermediate states.
- For LAB 17, supply the before/failure/restored CLI and traffic results. CEF, negotiated ADD-PATH capabilities and advertised-path output are needed for any stronger forwarding/advertisement claim.

This publication did not access EVE-NG/SecureCRT, collect from devices, change configuration or rerun a failure.
