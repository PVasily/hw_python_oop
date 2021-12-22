from dataclasses import dataclass
from typing import Any, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: Any
    duration: float
    distance: float
    speed: float
    calories: float

    TYPE_OF_TRAINING: str = 'Тип тренировки:'
    DURATION_OF_TRAINING: str = 'Длительность:'
    DISTANCE: str = 'Дистанция:'
    MEAN_SPEED: str = 'Ср. скорость:'
    SPENT_CALORIES: str = 'Потрачено ккал:'

    def get_message(self) -> str:
        """Вернуть строку сообщения"""
        return (f'{self.TYPE_OF_TRAINING} {self.training_type}; '
                f'{self.DURATION_OF_TRAINING} {self.duration:.3f} ч.; '
                f'{self.DISTANCE} {self.distance:.3f} км; '
                f'{self.MEAN_SPEED} {self.speed:.3f} км/ч; '
                f'{self.SPENT_CALORIES} {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        if self.__class__.__name__ == 'Swimming':
            return self.action * Swimming.LEN_STEP / self.M_IN_KM
        else:
            return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MULTIPLE_MEAN_SPEED: int = 18
    CALORIES_SHIFT_MEAN_SPEED: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MULTIPLE_MEAN_SPEED * self.get_mean_speed()
                - self.CALORIES_SHIFT_MEAN_SPEED)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MINUTES_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MULTIPLE_WEIGHT_1: float = 0.035
    CALORIES_MULTIPLE_WEIGHT_2: float = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MULTIPLE_WEIGHT_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.CALORIES_MULTIPLE_WEIGHT_2 * self.weight)
                * (self.duration * self.MINUTES_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MEAN_SPEED_INCREASE: float = 1.1
    CALORIES_COEFF_MULTIPLE: float = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_INCREASE)
                * self.CALORIES_COEFF_MULTIPLE * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type not in (training_dict.keys()):
        raise ValueError('Задан не существующий тип тренировки')
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
