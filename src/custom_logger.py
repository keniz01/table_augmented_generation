import logging
import structlog

class LoggerConfigurator:
    """
    Configures and returns a structured logger using structlog
    that outputs to the console only.
    """

    def __init__(
        self,
        name: str,
        log_level: int = logging.INFO,
    ):
        """
        Initialize the logger configuration.

        Args:
            name (str): Name of the logger instance.
            log_level (int): Logging level (e.g., logging.DEBUG, logging.INFO).
        """
        self.name = name
        self.log_level = log_level

        self._configure_logging()
        self.logger = structlog.get_logger(name)

    def _configure_logging(self):
        """
        Configure the standard logging and structlog processors.
        Logs are sent to the console using pretty formatting.
        """

        # Set up basic standard logging (structlog uses this under the hood)
        logging.basicConfig(
            level=self.log_level,
            format="%(message)s",  # structlog formats the final output
            handlers=[logging.StreamHandler()]  # Console output only
        )

        # Configure structlog with processors for formatting and context
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,          # Include context vars
                structlog.processors.TimeStamper(fmt="iso"),      # Add timestamp
                structlog.stdlib.add_log_level,                   # Include log level
                structlog.stdlib.add_logger_name,                 # Include logger name
                structlog.processors.StackInfoRenderer(),         # Stack info if available
                structlog.processors.format_exc_info,             # Exception formatting
                structlog.dev.ConsoleRenderer()                   # Pretty console output
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.make_filtering_bound_logger(self.log_level),
            cache_logger_on_first_use=True,
        )

    def get_logger(self):
        """
        Return the configured structlog logger instance.

        Returns:
            structlog.BoundLogger: A structured logger instance.
        """
        return self.logger
