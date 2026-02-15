from datetime import datetime
from typing import List


def send_notification(user_id: str, message: str) -> None:
    """
    Отправляет уведомление пользователю.
    
    Args:
        user_id: Идентификатор пользователя
        message: Текст сообщения
    """
    if not user_id or not isinstance(user_id, str):
        raise ValueError("user_id должен быть непустой строкой")
    if not message or not isinstance(message, str):
        raise ValueError("message должен быть непустой строкой")

    print(f"INFO: Sending notification to user_id={user_id}: '{message}'")

class Notification:

    '''
    Класс для хранения данных уведомления.
    
    Attributes:
        user_id: Идентификатор пользователя
        message: Текст сообщения
        scheduled_time: Время отправки
        created_at: Время создания (автоматически)
        status: Статус уведомления
    '''

    def __init__(self, user_id: str, message: str, scheduled_time: str, priority: str = 'normal'):
        self.user_id = user_id
        self.message = message
        self.scheduled_time = self.parse_datetime(scheduled_time)
        self.created_at = datetime.now()
        self.status = 'pending'
        self.priority = self.validate_priority(priority)
        self.validate()


    def validate_priority(self, priority: str) -> str:

        '''Валидация приоритета.'''

        valid_priorities = ['high', 'normal', 'low']
        priority_lower = priority.lower()
        
        if priority_lower not in valid_priorities:
            raise ValueError(f"Приоритет должен быть одним из: {valid_priorities}")
        
        return priority_lower

    
    def parse_datetime(self, datetime_str: str) -> datetime:

        '''Парсит строку с датой в разных форматах.'''
        
        datetime_str = datetime_str.strip()
        
        formats = [
            "%Y-%m-%d %H:%M:%S",      # 2025-10-26 10:00:00
            "%Y-%m-%d %H:%M",         # 2025-10-26 10:00
            "%Y-%m-%dT%H:%M:%S",      # 2025-10-26T10:00:00
            "%Y-%m-%dT%H:%M",         # 2025-10-26T10:00
            "%d.%m.%Y %H:%M",         # 26.10.2025 10:00
            "%d/%m/%Y %H:%M",         # 26/10/2025 10:00
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(datetime_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Неподдерживаемый формат даты: {datetime_str}")


    def validate(self) -> None:

        '''Валидация данных уведомления.'''

        if not self.user_id or not  isinstance(self.user_id, str):
            raise ValueError('user_id должен быть непустой строкой')
        if not self.message or not  isinstance(self.message, str):
            raise ValueError('message должен быть непустой строкой')
        if not isinstance(self.scheduled_time, datetime):
            raise TypeError('scheduled_time должен быть объектом типа datetime')

    def to_dict(self) -> dict:

        '''Конвертируем уведомления в словарь.'''

        return {
            'user_id': self.user_id,
            'message_preview': self.message[:30] + '...' if len(self.message) > 30 else self.message,
            'scheduled_time': self.scheduled_time.isoformat(),
            'created_at': self.created_at.isoformat(),
            'status': self.status
        }


class Scheduler:

    '''
    Планировщик уведомлений.
    
    Отвечает за хранение запланированных уведомлений
    и отправку тех, у которых наступило время.
    '''
    
    def __init__(self):
        self.notifications: List[Notification] = []
        self.sent_notifications: List[Notification] = []

    def schedule(self, notification: Notification) -> None:

        '''Добавляет уведомление в планировщик.'''

        if not isinstance(notification, Notification):
            raise TypeError('notification должен быть типа Notification')
        
        self.notifications.append(notification)

    def run_pending(self) -> int:

        '''Проверяет и отправляет все просроченные уведомления.'''

        now = datetime.now()
        sent_count = 0

        for notification in self.notifications[:]:
            if notification.scheduled_time <= now:
                send_notification(notification.user_id, notification.message)
                notification.status = "sent"
                self.notifications.remove(notification)
                self.sent_notifications.append(notification)
                sent_count += 1

        return sent_count


    def send_notification(self, notification: dict) -> None:
        pass


if __name__ == '__main__':
    scheduler = Scheduler()

    scheduler.schedule(Notification('a1b2-c3d4', 'Напоминание о встрече', '2025-10-26T10:00:00'))
    scheduler.schedule(Notification('e5f6-g7h8', 'Проверь почту', '2026-02-09T12:00:00'))

    scheduler.run_pending()
