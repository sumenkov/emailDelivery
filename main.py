import logging

from EmailSender import EmailSender

formatted = '%(asctime)s - %(levelname)s - %(message)s'

logging.basicConfig(filename='log.log', level=logging.DEBUG, format=formatted)

stream_formatted = logging.Formatter(formatted)

console_handler = logging.StreamHandler()
console_handler.setFormatter(stream_formatted)

logger = logging.getLogger()
logger.addHandler(console_handler)


def main():
    email_sender = EmailSender("config.ini")
    email_sender.run()


if __name__ == '__main__':
    main()
