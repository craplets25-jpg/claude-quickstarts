<!-- Source: debater-early-access-program-sdk-Deepwiki.md -->
<!-- Section: Authentication and Setup -->
<!-- Lines: 1878-1894 -->

## Authentication and Setup

The admin client requires both a standard API key and an admin password for elevated operations.

### Initialization

| Parameter | Type | Description |
|-----------|------|-------------|
| `admin_password` | `str` | Administrative password for elevated operations |
| `apikey` | `str` | Standard API authentication key |
| `host` | `Optional[str]` | Service host URL (optional) |
| `verify_certificate` | `bool` | SSL certificate verification flag |

The admin client uses the `get_admin_password_header()` method to include admin credentials in requests through the `admin-password` header.

**Sources:** [debater_python_api/api/clients/keypoints_admin_client.py:10-16]()

