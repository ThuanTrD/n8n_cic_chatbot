# Integration Report

Production recovery chain was verified after the draft import:

`offline publish old version -> n8n start -> healthy -> GET/POST registration -> edge -> Facebook verification challenge`

The final public challenge returned HTTP 200 with an exact match. The optimized Hermes branch was not published because its upstream endpoint still returns HTTP 502.
