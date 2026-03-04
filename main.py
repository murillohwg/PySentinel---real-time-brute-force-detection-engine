import pyfiglet
from core.parser import parse_log_line
from core.detector import BruteForceDetector
from core.correlator import EventCorrelator
from core.alert_manager import AlertManager
import config


def main():
    detector = BruteForceDetector(
        threshold=config.BRUTE_FORCE_THRESHOLD,
        time_window_seconds=config.BRUTE_FORCE_TIME_WINDOW
    )

    correlator = EventCorrelator(
        correlation_window_seconds=config.CORRELATION_WINDOW
    )

    alert_manager = AlertManager(config.ALERT_LOG_FILE)

    with open(config.LOG_FILE, "r") as f:
        for line in f:
            event = parse_log_line(line.strip())
            if event is None:
                continue

            alert = detector.process_event(event)

            if alert:
                correlated_alert = correlator.process_alert(alert)
                alert_manager.handle(alert)

                if correlated_alert:
                    alert_manager.handle(correlated_alert)


if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("PYSENTINEL")
    print(ascii_banner)
    print("Mini SIEM in Python - Brute Force & Multi-Stage Detection\n")

    while True:
        print("[1] Processar logs")
        print("[2] Sair")

        choice = input("Escolha uma opção: ")
        if choice == "1":
            main()
        elif choice == "2":
            print("\nEncerrando PySentinel...")
            break
        else:
            print("\nOpção inválida.\n")
