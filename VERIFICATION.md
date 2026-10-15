# Verification and limits

Revision date: 15 October 2026.

## Reproducible local checks

Run `python3 -m unittest discover -s tests -v` from the repository root.
The suite checks the four stored samples, documented field names, localization
parameters, error payloads, HTTP failures, unfinished responses, pagination bounds,
and README structure. Network responses in unit tests are mocked.

All four engine commands are also checked in offline mode. An offline success is
not a successful live request. This revision did not use an API key or run live
SerpApi calls. CI results are available under the repository Actions tab after push.

## What this does not establish

The tests do not establish live service availability, comprehensive API coverage,
ranking accuracy, adoption, revenue, or independent coding authorship. Code and
writing were developed with AI assistance. A candidate walkthrough should explain
the request, response fields, error cases and personal contribution in detail.

## Optional live verification

With an authorized account, make one request for one engine. Record the date,
engine, query, status and redacted result shape. Check the account usage. Do not
publish the API key, credential-bearing request URL or private customer data.
Only update this record to say live tested after that request actually succeeds.
