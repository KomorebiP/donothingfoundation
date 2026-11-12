# Session notes

Author: Komorebi P.
Date: 2026-11-12

## Migration scope

Created a separate GitHub project for Do Nothing Foundation, leaving the research repositories untouched. Baseline is BiB Desktop 116.1.0 plus Signal Studio 2.1 source. Added a hash-locked baseline importer, static Pages builder, CI configuration and Codex handoff.

## Transfer limitation

The chat-mounted 158,375,826-byte ZIP could not be uploaded through the connected release action: that action requires a remote FileUploadable reference, not a chat-local path. The remote tool workspace did not contain the mounted archive. No successful source/media transfer should be inferred from repository creation alone.

The prepared draft release accepts the existing ZIP through GitHub's upload interface. Publishing it starts the import workflow. This is a one-time step. Consult BASELINE_IMPORT.json and Actions for actual import/deployment state.

## Next verification

Check real website navigation and origin storage after deployment. Rerun Python and Go suites. Verify full narrative and native Windows behavior separately. Preserve historical reports without upgrading their claims.
