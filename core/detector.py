from collections import defaultdict
from datetime import timedelta

class BruteForceDetector:
    def __init__(self, threshold=5, time_window_seconds=120):
        self.threshold = threshold
        self.time_window = timedelta(seconds=time_window_seconds)
        self.failed_attempts = defaultdict(list)

    def process_event(self, event):
        
        if event["status"] != "FAILED":
            return None

        ip = event["ip"]
        timestamp = event["timestamp"]

        # Armazenando a tentativa
        self.failed_attempts[ip].append(timestamp)

        # Removendo tentativas fora da janela de tempo
        self.failed_attempts[ip] = [
            t for t in self.failed_attempts[ip]
            if timestamp - t <= self.time_window
        ]

        # Verificando se o limite de tentivas foi ultrapassado
        if len(self.failed_attempts[ip]) >= self.threshold:
            return {
                "type": "BRUTE_FORCE_SUSPECTED",
                "ip": ip,
                "count": len(self.failed_attempts[ip]),
                "time_window_seconds": self.time_window.total_seconds()
            }

        return None
