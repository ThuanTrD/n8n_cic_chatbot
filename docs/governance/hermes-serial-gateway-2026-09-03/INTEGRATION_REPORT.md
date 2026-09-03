# Integration Report

Local real-network integration used five concurrent client threads through the gateway to a multithreaded mock upstream. All five returned 200, elapsed time was approximately 1.05 seconds, and observed upstream max concurrency was exactly 1.

Production upstream integration is blocked because the existing Cloudflare endpoint returns 502. The gateway correctly propagates that status without publishing the Hermes branch.
