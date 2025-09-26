# utils/custom_metrics.py
from prometheus_client import Gauge

# Service-specific custom metrics
users_total_gauge = Gauge(
    "paig_users_total",
    "Total number of users in the system"
)

groups_total_gauge = Gauge(
    "paig_groups_total",
    "Total number of groups in the system"
)
ai_apps_total_gauge = Gauge(
    "paig_ai_applications_total",
    "Total number of AI applications in the system"
)
# utils/custom_metrics.py
ai_app_policies_total_gauge = Gauge(
    "paig_ai_application_policies_total",
    "Total number of AI application policies in the system"
)
