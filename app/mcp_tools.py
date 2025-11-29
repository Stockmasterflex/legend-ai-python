"""
MCP tool wrappers for easy integration
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


async def send_telegram_message(
    chat_id: int,
    text: str,
    parse_mode: Optional[str] = None,
    disable_notification: bool = False,
) -> Optional[Dict[str, Any]]:
    """
    Send a message via Telegram MCP

    Args:
        chat_id: Telegram chat ID
        text: Message text
        parse_mode: "Markdown", "MarkdownV2", or "HTML"
        disable_notification: Send silently

    Returns:
        Response dict if successful, None otherwise
    """
    try:
        # This will use the Telegram MCP when available
        # For now, log the message
        logger.info(f"[Telegram] To chat {chat_id}: {text[:100]}...")

        # TODO: Integrate with actual Telegram MCP call
        # result = await mcp_telegram_send_message(
        #     chat_id=chat_id,
        #     text=text,
        #     parse_mode=parse_mode,
        #     disable_notification=disable_notification
        # )

        # Return mock success for now
        return {"ok": True, "result": {"message_id": 1}}

    except Exception as e:
        logger.error(f"Telegram send failed: {e}")
        return None
