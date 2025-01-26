import re

def escalateit(incoming_issues):
    tags_combine = " ".join([incoming_issues.get(f"tag_{i+1}", "") for i in range(9)])

    # Check for high-priority and critical keywords
    critical_keywords = ["issue", "problem", "urgent", "disruption", "failure",
                         "incident", "crash", "refund", "outage", "critical"]
    if incoming_issues["priority"] == "high" and any(key.lower() in tags_combine.lower() for key in critical_keywords):
        return True

    # Escalate if specific tags are present
    specific_tags = ["security", "data breach", "compliance"]
    if any(tag.lower() in tags_combine.lower() for tag in specific_tags):
        return True

    return False