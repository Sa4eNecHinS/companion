SQLi_PATTERNS = {
    r"(?i)\bunion\s+select\b": "UNION SELECT",
    r"(?i)\bdrop\s+table\b": "DROP TABLE",
    r"(?i)\bdelete\s+from\b": "DELETE FROM",
    r"(?i)\bor\s+1=1\b": "OR 1=1",
    r"(?i)--": "SQL Comment Injection",
    r"(?i)\btruncate\s+table\b": "TRUNCATE TABLE",
    r"(?i)\binsert\s+into\b": "INSERT INTO",
    r"(?i)\bupdate\s+\w+\s+set\b": "UPDATE SET",
    r"(?i)\bexec\s+xp_": "EXEC xp_cmdshell",
    r"(?i)\bpg_sleep\s*\(": "PostgreSQL Sleep Injection",
}
