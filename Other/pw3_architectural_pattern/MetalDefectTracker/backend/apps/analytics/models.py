"""
analytics.models
----------------
FRQ-8  History & filtering
FRQ-9  Statistics and analytics

This app has NO own database tables - all analytics are computed by
querying existing records from receiver, detection, and verification modules
through their public Python APIs (services).  The only responsibility of
this module is to expose aggregated read-only views over the shared
PostgreSQL database.

See analytics.services for the aggregation logic stubs.
"""

# No models - analytics is a purely read/query module.
