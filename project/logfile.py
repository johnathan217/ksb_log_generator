from datetime import datetime


class Logging:
    @staticmethod
    def log_with_timestamp(message: str) -> None:
        timestamp: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        date: str = datetime.now().strftime("%d-%m-%Y")
        log_message: str = f"[{timestamp}] {message}"

        with open(f'../logs/app_{date}.log', 'a') as f:
            f.write(log_message + "\n")
