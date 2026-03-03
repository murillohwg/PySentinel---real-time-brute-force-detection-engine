import time

from core.parser import parse_log_line
from core.detector import BruteForceDetector
from core.correlator import EventCorrelator
from core.alert_manager import AlertManager
import config

LOG_FILE = "data/logs.txt"

detector = BruteForceDetector(threshold=5, time_window_seconds=120)
correlator = EventCorrelator(correlation_window_seconds=300)
alert_manager = AlertManager("data/alerts.log")


def follow(file):
    """
    Fica esperando novas linhas no arquivo.
    """
    file.seek(0, 2)  # vai para o final do arquivo

    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line


def main():
    with open(LOG_FILE, "r") as logfile:
        loglines = follow(logfile)

        for line in loglines:
            event = parse_log_line(line.strip())
            if not event:
                continue

            alert = detector.process_event(event)

            if alert:
                alert_manager.handle(alert)

                correlated = correlator.process_alert(alert)
                if correlated:
                    alert_manager.handle(correlated)


if __name__ == "__main__":
    main()
