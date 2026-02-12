## Architecture Decision Record 05/02/2025
Decision to remove controllers

### Context
Previously, each endpoint had its own controller where its flow was orchestrated. This allowed for the decoupling of the internal logic of the endpoint and its entry point.

### Problem
As more endpoints were added, it was not viable to have a controller for each endpoint if the number of endpoints grew significantly. For example, the WSFE has 22 endpoints, so if controllers had not been removed, there would be 22 controllers, which unnecessarily increases complexity and complicates maintenance due to more code and more files.

### Solution
Therefore, it was decided to remove the controllers from the web services except for some specific ones such as the Access Ticket (TA) request and the readiness health check. The logic that each WSFE controller had was simplified and moved to the endpoint functions, and this pattern will be maintained for other web services that are added.