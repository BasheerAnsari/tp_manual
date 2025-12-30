import os
import functools
import traceback
import logging
from datetime import datetime
from pathlib import Path
from typing import Callable, Any, List, Dict
from tabulate import tabulate


# =========================================================
# Resolve repo root safely
# core_services/app/shared/helper/error_logger.py
# parents[0] -> helper
# parents[1] -> shared
# parents[2] -> app
# parents[3] -> core_services
# parents[4] -> repo root
# =========================================================
BASE_DIR = Path(__file__).resolve().parents[4]


class ErrorLogger:
    """Structured error logger that writes formatted error tables to files."""

    def __init__(self, log_dir: Path = None):
        # Default: <repo_root>/logs/errors
        self.log_dir = log_dir or (BASE_DIR / "logs" / "errors")
        self.errors: List[Dict[str, Any]] = []
        self.logger = logging.getLogger("error_logger")

        # Ensure directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def add_error(
        self,
        stage: str,
        function: str,
        error_type: str,
        error_message: str,
        stack_trace: str = None
    ):
        """Add an error entry to memory."""
        self.errors.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stage": stage,
            "function": function,
            "error_type": error_type,
            "error_message": error_message[:100],
            "stack_trace": stack_trace
        })

    def save_to_file(self, context: str = "errors"):
        """Persist all collected errors into a formatted table file."""
        if not self.errors:
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"error_table_{context}_{timestamp}.txt"
        filepath = self.log_dir / filename

        # Prepare table rows
        table_data = [
            [
                err["timestamp"],
                err["stage"][:20],
                err["function"][:25],
                err["error_type"][:20],
                err["error_message"][:50]
            ]
            for err in self.errors
        ]

        # Create table string
        table_str = tabulate(
            table_data,
            headers=["Timestamp", "Stage", "Function", "Error Type", "Message"],
            tablefmt="grid"
        )

        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=" * 120 + "\n")
            f.write(f"ERROR LOG - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Context: {context}\n")
            f.write(f"Total Errors: {len(self.errors)}\n")
            f.write("=" * 120 + "\n\n")
            f.write(table_str)
            f.write("\n\n")

            # Detailed stack traces
            f.write("=" * 120 + "\n")
            f.write("DETAILED STACK TRACES\n")
            f.write("=" * 120 + "\n\n")

            for err in self.errors:
                f.write(f"Function: {err['function']}\n")
                f.write(f"Error: {err['error_type']}: {err['error_message']}\n")
                f.write("-" * 80 + "\n")

                if err["stack_trace"]:
                    f.write(err["stack_trace"])

                f.write("\n" + "=" * 120 + "\n\n")

        absolute_path = filepath.resolve()
        self.logger.error(f"Error details saved to: file://{absolute_path}")

        # Clear buffer after saving
        self.errors = []

        return str(filepath)


# ✅ Global singleton logger
error_logger = ErrorLogger()


def log_errors(stage: str = "unknown"):
    """
    Decorator to catch, store and persist errors automatically.

    Usage:
        @log_errors(stage="recruiter_signup")
        def my_function():
            pass
    """

    def decorator(func: Callable) -> Callable:

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                error_logger.add_error(
                    stage=stage,
                    function=func.__name__,
                    error_type=type(e).__name__,
                    error_message=str(e),
                    stack_trace=traceback.format_exc()
                )
                error_logger.save_to_file(context=stage)
                raise

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_logger.add_error(
                    stage=stage,
                    function=func.__name__,
                    error_type=type(e).__name__,
                    error_message=str(e),
                    stack_trace=traceback.format_exc()
                )
                error_logger.save_to_file(context=stage)
                raise

        import asyncio
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator
