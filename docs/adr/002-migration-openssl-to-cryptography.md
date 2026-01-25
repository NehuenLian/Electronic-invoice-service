## Architecture Decision Record 01/23/2026
Migration from OpenSSL to cryptography python library

### Context
Previously, the cryptographic operation for signing the `loginTicketRequest.xml` was performed using OpenSSL + subprocess. Commands were handled as hardcoded strings, saving the resulting CMS to disk and then retrieving it in base64 format.

### Problem
This led to several issues down the line:
1. The requirement of having OpenSSL installed on the local machine.
2. An additional step was needed to install it within the production container.
3. It was very cumbersome to test, as running tests on any platform required a pre-installed OpenSSL environment.
4. Different commands were required depending on whether the signing process was running on Windows or Linux.

### Solution and Benefits
The solution was to replace OpenSSL with the `cryptography` library, replace subprocess commands with dedicated library functions, and remove the OpenSSL installation from the container. This provided:
1. better portability
2. easier test writing
3. eliminated the need to save the CMS to disk, 
4. reduced the total lines of code.