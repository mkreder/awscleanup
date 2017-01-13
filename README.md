This scripts does the following:

1. Cleanup instances that doesn't have termination protection and are older than 1 week
2. Cleanup volumes that are available and not used
3. Cleanup elastic IPs that are allocated but not assigned

This script is perfect for lab environments where you use instances for a certain number of days and then you want to get rid of them automatically.
Please don't use it in a production environment or your instances will be deleted.
