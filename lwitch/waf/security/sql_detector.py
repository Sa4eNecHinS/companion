import re

from lwitch.waf.utils.sqli_patterns import SQLi_PATTERNS


def detect_sql_injection(text):
    for pattern, pattern_name in SQLi_PATTERNS.items():
        if re.search(pattern, text):
            return pattern_name

    return None
