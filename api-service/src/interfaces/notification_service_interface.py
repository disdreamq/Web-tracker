from abc import ABC, abstractmethod


class INotificationService(ABC):
    """Notification service interface.

    Defines the contract for sending notifications to users via WebSocket.
    Implemented by NotificationService and used in test mocks.
    """

    @abstractmethod
    def send_to_user(self, user_id: int) -> None:
        """Send notification to a user.

        Args:
            user_id: User identifier to send the notification to.

        Raises:
            ValueError: If user_id is invalid.
            ConnectionError: If user is not connected via WebSocket.
        """
        pass
