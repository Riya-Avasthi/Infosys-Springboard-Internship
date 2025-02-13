

def escalateit(title, description):
    # Combine the title and description into one string and make it case-insensitive
    combined_text = f"{title} {description}".lower()

    # List of critical keywords that should trigger escalation
    critical_keywords = [
        "issue", "problem", "urgent", "disruption", "failure",
        "incident", "crash", "refund", "outage", "critical"
    ]
    
    # Check if any critical keywords are present in the title or description
    if any(key in combined_text for key in critical_keywords):
        return True

    # List of specific keywords like security, data breach, compliance, etc., for additional escalation
    specific_keywords = ["security", "data breach", "compliance"]

    # Check if any specific keywords are present in the title or description
    if any(keyword in combined_text for keyword in specific_keywords):
        return True

    # If none of the conditions for escalation are met, return False
    return False

# Example usage of the function

# Example 1: Issue with urgent system failure
title1 = "Urgent: System failure on the server"
description1 = "There has been a critical failure in the server that needs immediate attention. The system is down, and users are unable to access critical services."

# Call the function to check if the issue should be escalated
is_escalated1 = escalateit(title1, description1)
print(f"Is the issue escalated? {is_escalated1}")

# Example 2: Issue with security concern
title2 = "Security Alert: Data breach detected"
description2 = "A data breach has occurred, exposing sensitive information of customers. Immediate action is required."

# Call the function to check if the issue should be escalated
is_escalated2 = escalateit(title2, description2)
print(f"Is the issue escalated? {is_escalated2}")

# Example 3: Non-urgent issue
title3 = "User feedback on new feature"
description3 = "The new feature was well-received, but there are some suggestions for improvements."

# Call the function to check if the issue should be escalated
is_escalated3 = escalateit(title3, description3)
print(f"Is the issue escalated? {is_escalated3}")
