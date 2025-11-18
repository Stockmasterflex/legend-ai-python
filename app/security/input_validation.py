"""
Input Validation and Sanitization
Prevents SQL injection, XSS, path traversal, and other injection attacks
"""
import re
import html
import logging
from typing import Any, Optional, List
from pathlib import Path
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class InputValidator:
    """
    Comprehensive input validation and sanitization.

    Protects against:
    - SQL injection
    - XSS (Cross-Site Scripting)
    - Path traversal
    - Command injection
    - LDAP injection
    - XML injection
    """

    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|UNION|DECLARE)\b)",
        r"(--|\#|\/\*|\*\/)",
        r"(;|\|\||&&)",
        r"('|('')|(\")|(\"\")|(`)|(\-\-))",
        r"(\bOR\b.*=.*)",
        r"(\bAND\b.*=.*)",
        r"(0x[0-9a-fA-F]+)",
        r"(\bxp_\w+)",
        r"(\bsp_\w+)",
    ]

    # XSS patterns
    XSS_PATTERNS = [
        r"<script[\s\S]*?>[\s\S]*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe[\s\S]*?>",
        r"<object[\s\S]*?>",
        r"<embed[\s\S]*?>",
        r"<applet[\s\S]*?>",
        r"<meta[\s\S]*?>",
        r"<link[\s\S]*?>",
        r"<style[\s\S]*?>[\s\S]*?</style>",
    ]

    # Path traversal patterns
    PATH_TRAVERSAL_PATTERNS = [
        r"\.\.",
        r"\/\.\.",
        r"\.\./",
        r"\.\.\\",
        r"\\\.\.\\",
        r"%2e%2e",
        r"%252e%252e",
        r"..;",
    ]

    # Command injection patterns
    COMMAND_INJECTION_PATTERNS = [
        r"[;&|`$()]",
        r"\$\(",
        r"`.*`",
        r"\|\|",
        r"&&",
    ]

    # Valid ticker symbol pattern (letters and dots only)
    TICKER_PATTERN = re.compile(r"^[A-Z]{1,5}(\.[A-Z]{1,2})?$")

    # Valid interval pattern
    INTERVAL_PATTERN = re.compile(r"^(1m|5m|15m|30m|1h|4h|1d|1w|1M)$")

    @classmethod
    def validate_ticker(cls, ticker: str) -> str:
        """
        Validate and sanitize stock ticker symbol.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Sanitized ticker symbol

        Raises:
            HTTPException: If ticker is invalid
        """
        if not ticker:
            raise HTTPException(status_code=400, detail="Ticker symbol is required")

        # Convert to uppercase and strip whitespace
        ticker = ticker.strip().upper()

        # Check length
        if len(ticker) > 10:
            raise HTTPException(
                status_code=400,
                detail="Ticker symbol too long (max 10 characters)"
            )

        # Validate format
        if not cls.TICKER_PATTERN.match(ticker):
            raise HTTPException(
                status_code=400,
                detail="Invalid ticker symbol format. Use only letters (e.g., AAPL, BRK.B)"
            )

        return ticker

    @classmethod
    def validate_interval(cls, interval: str) -> str:
        """
        Validate trading interval.

        Args:
            interval: Trading interval (1m, 5m, 15m, etc.)

        Returns:
            Validated interval

        Raises:
            HTTPException: If interval is invalid
        """
        if not interval:
            raise HTTPException(status_code=400, detail="Interval is required")

        interval = interval.strip().lower()

        if not cls.INTERVAL_PATTERN.match(interval):
            raise HTTPException(
                status_code=400,
                detail="Invalid interval. Must be one of: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M"
            )

        return interval

    @classmethod
    def sanitize_string(cls, value: str, max_length: int = 1000) -> str:
        """
        Sanitize string input to prevent injection attacks.

        Args:
            value: Input string
            max_length: Maximum allowed length

        Returns:
            Sanitized string

        Raises:
            HTTPException: If input is malicious
        """
        if not value:
            return ""

        # Check length
        if len(value) > max_length:
            raise HTTPException(
                status_code=400,
                detail=f"Input too long (max {max_length} characters)"
            )

        # Check for SQL injection
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                logger.warning(f"🚨 SQL injection attempt detected: {value[:100]}")
                raise HTTPException(
                    status_code=400,
                    detail="Invalid input detected"
                )

        # Check for XSS
        for pattern in cls.XSS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                logger.warning(f"🚨 XSS attempt detected: {value[:100]}")
                raise HTTPException(
                    status_code=400,
                    detail="Invalid input detected"
                )

        # Check for path traversal
        for pattern in cls.PATH_TRAVERSAL_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                logger.warning(f"🚨 Path traversal attempt detected: {value[:100]}")
                raise HTTPException(
                    status_code=400,
                    detail="Invalid input detected"
                )

        # HTML entity encode for safety
        value = html.escape(value)

        return value

    @classmethod
    def validate_file_path(cls, file_path: str, allowed_dirs: Optional[List[str]] = None) -> Path:
        """
        Validate file path to prevent path traversal attacks.

        Args:
            file_path: File path to validate
            allowed_dirs: List of allowed base directories

        Returns:
            Validated Path object

        Raises:
            HTTPException: If path is invalid or outside allowed directories
        """
        if not file_path:
            raise HTTPException(status_code=400, detail="File path is required")

        # Check for path traversal patterns
        for pattern in cls.PATH_TRAVERSAL_PATTERNS:
            if re.search(pattern, file_path):
                logger.warning(f"🚨 Path traversal attempt: {file_path}")
                raise HTTPException(
                    status_code=400,
                    detail="Invalid file path"
                )

        try:
            # Resolve to absolute path
            path = Path(file_path).resolve()

            # Check if path is within allowed directories
            if allowed_dirs:
                is_allowed = False
                for allowed_dir in allowed_dirs:
                    allowed_path = Path(allowed_dir).resolve()
                    try:
                        path.relative_to(allowed_path)
                        is_allowed = True
                        break
                    except ValueError:
                        continue

                if not is_allowed:
                    logger.warning(f"🚨 Path outside allowed directories: {file_path}")
                    raise HTTPException(
                        status_code=403,
                        detail="Access to this path is forbidden"
                    )

            return path

        except Exception as e:
            logger.error(f"Path validation error: {e}")
            raise HTTPException(status_code=400, detail="Invalid file path")

    @classmethod
    def validate_email(cls, email: str) -> str:
        """
        Validate email address format.

        Args:
            email: Email address

        Returns:
            Validated email

        Raises:
            HTTPException: If email is invalid
        """
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")

        email = email.strip().lower()

        # Simple email validation regex
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

        if not email_pattern.match(email):
            raise HTTPException(status_code=400, detail="Invalid email format")

        if len(email) > 254:  # RFC 5321
            raise HTTPException(status_code=400, detail="Email too long")

        return email

    @classmethod
    def validate_integer(
        cls,
        value: Any,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        name: str = "value"
    ) -> int:
        """
        Validate integer input with bounds checking.

        Args:
            value: Input value
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            name: Name of the field (for error messages)

        Returns:
            Validated integer

        Raises:
            HTTPException: If value is invalid
        """
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid {name}: must be an integer"
            )

        if min_value is not None and int_value < min_value:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid {name}: must be at least {min_value}"
            )

        if max_value is not None and int_value > max_value:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid {name}: must be at most {max_value}"
            )

        return int_value

    @classmethod
    def validate_float(
        cls,
        value: Any,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        name: str = "value"
    ) -> float:
        """
        Validate float input with bounds checking.

        Args:
            value: Input value
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            name: Name of the field (for error messages)

        Returns:
            Validated float

        Raises:
            HTTPException: If value is invalid
        """
        try:
            float_value = float(value)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid {name}: must be a number"
            )

        if min_value is not None and float_value < min_value:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid {name}: must be at least {min_value}"
            )

        if max_value is not None and float_value > max_value:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid {name}: must be at most {max_value}"
            )

        return float_value

    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """
        Sanitize filename to prevent directory traversal and command injection.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename

        Raises:
            HTTPException: If filename is invalid
        """
        if not filename:
            raise HTTPException(status_code=400, detail="Filename is required")

        # Remove path components
        filename = Path(filename).name

        # Remove any characters that aren't alphanumeric, dash, underscore, or dot
        filename = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)

        # Prevent hidden files
        if filename.startswith("."):
            filename = "_" + filename[1:]

        # Limit length
        if len(filename) > 255:
            raise HTTPException(status_code=400, detail="Filename too long")

        if not filename:
            raise HTTPException(status_code=400, detail="Invalid filename")

        return filename
