## Architecture Decision Record 12/20/2025
Async use decision explanation

It was decided to use async/await because, even though massive concurrency is probably not expected, it is important to avoid blocking the server while waiting for responses from AFIP services.
These external calls can have variable latencies or take longer than desirable, and using async allows the server to keep processing other tasks instead of sitting idle waiting.
This way resources are used more efficiently, unnecessary blocked threads are avoided, and the system remains more stable and scalable, even when AFIP is not particularly cooperative.