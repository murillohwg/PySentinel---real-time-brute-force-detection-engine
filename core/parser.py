import re
from datetime import datetime

LOG_PATTERN = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\w+)\s+([\d\.]+)\s+(SUCCESS|FAILED)"
)

def parse_log_line(line):
    """
    Recebe uma linha de log -> retorna um dicionário estruturado.
    """

    match = LOG_PATTERN.match(line)

    if not match:
        return None

    timestamp_str = match.group(1)
    username = match.group(2)
    ip_address = match.group(3)
    status = match.group(4)

    try:
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

    return {
        "timestamp": timestamp,
        "username": username,
        "ip": ip_address,
        "status": status
    }
