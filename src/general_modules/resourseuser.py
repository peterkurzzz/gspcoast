"""
    Модуль логины и пароли пользователей БД:
        AdminUser - логины и пароли администраторов
"""

import enum


class AdminUser(enum.Enum):
    """Логины и пароли администраторов"""
    MAIN_AKK = 'postgres', '007'

