from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import inline_serializer, OpenApiParameter
from rest_framework import serializers

pagination = inline_serializer(
    name="pagination",
    fields={
        "count": serializers.IntegerField(help_text="Количество курсов", default=3),
        "next": serializers.URLField(
            help_text="Следующая страница", default='http://api.example.org/accounts/?page=4'),
        "previous": serializers.URLField(
            help_text="Предыдущая страница", default='http://api.example.org/accounts/?page=2'),
        "next_front": serializers.URLField(
            help_text="Следующая страница", default='http://example.org/accounts/?page=4'),
        "previous_front": serializers.URLField(
            help_text="Предыдущая страница", default='http://example.org/accounts/?page=2'),
    },
    help_text="Пагинация",
)


# Общие функции
def get_2xx(name: str, message: str):
    return inline_serializer(
        name=name,
        fields={"message": serializers.CharField(default=message)},
    )


def get_4xx_many(name: str):
    return inline_serializer(
        name=name,
        fields={"message": serializers.ListField(default=["Сообщение об ошибке."])},
    )


def get_4xx_single(name: str):
    return inline_serializer(
        name=name,
        fields={"message": serializers.CharField(default="Сообщение об ошибке.")},
    )

def get_5xx_many(name:str):
    return inline_serializer(
        name=name,
        fields={'message':serializers.ListField(default=["Сообщение об ошибке"])},
    )


# Ответы специализированные
login_response_200 = inline_serializer(
    name="login_response_200",
    fields={
        "data": inline_serializer(
            name="login_data",
            fields={
                "access": serializers.CharField(default="Токен доступа"),
            },
        ),
        "message": serializers.CharField(default="Токены доступа и обновления"),
    },
)
refresh_response_200 = inline_serializer(
    name="refresh_response_200",
    fields={
        "data": inline_serializer(
            name="refresh_data",
            fields={
                "access": serializers.CharField(default="Токен доступа"),
            },
        ),
        "message": serializers.CharField(default="Токены доступа"),
    },
)

# Параметры
parameter_uidb64 = OpenApiParameter(
    name="uidb64",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.PATH,
    description="Идентификатор пользователя в формате Base64.",
)
parameter_token = OpenApiParameter(
    name="token",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.PATH,
    description="Токен активации.",
)
parameter_authorization = OpenApiParameter(
    name="Authorization",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.HEADER,
    description="Токен авторизации.",
    required=True,
    default="Bearer ENTER_YOUR_TOKEN_HERE",
)

response_delete_course_204 = inline_serializer(
    name="response_delete_course_204",
    fields={
        "message": serializers.CharField(default="Курс успешно удален."),
    },
)

get_subjects_200 = inline_serializer(
    name="get_subjects_200",
    fields={
        "data": serializers.ListSerializer(
            child=inline_serializer(
                name="get_subjects_data",
                fields={
                    "id": serializers.IntegerField(help_text="ID предметной области"),
                    "title": serializers.CharField(
                        max_length=200, help_text="Название предметной области"
                    ),
                    "slug": serializers.CharField(help_text="Слаг предметной области"),
                },
            )
        ),
        "message": serializers.CharField(default="Список предметных областей"),
    },
)

create_subject_201 = inline_serializer(
    name="create_subject_201",
    fields={
        "data": serializers.ListSerializer(
            child=inline_serializer(
                name="create_subject_data",
                fields={
                    "id": serializers.IntegerField(help_text="ID предметной области"),
                    "title": serializers.CharField(
                        max_length=200, help_text="Название предметной области"
                    ),
                    "slug": serializers.CharField(help_text="Слаг предметной области"),
                },
            )
        ),
        "message": serializers.CharField(default="Предметная область создана"),
    },
)

response_create_module_201 = inline_serializer(
    name="response_create_module_201",
    fields={
        "data": inline_serializer(
            name="response_create_module_data",
            fields={
                "id": serializers.IntegerField(help_text="ID модуля"),
                "course_id": serializers.IntegerField(help_text="ID курса"),
                "title": serializers.CharField(
                    max_length=200, help_text="Название модуля"
                ),
                "slug": serializers.CharField(
                    max_length=200, help_text="Слаг модуля"
                ),
                "description": serializers.CharField(
                    help_text="Краткое описание модуля"
                ),
            },
        ),
        "message": serializers.CharField(default="Модуль добавлен."),
    },
)

response_update_module_200 = inline_serializer(
    name="response_update_module_200",
    fields={
        "data": inline_serializer(
            name="response_update_module_data",
            fields={
                "id": serializers.IntegerField(help_text="ID модуля"),
                "course_id": serializers.IntegerField(help_text="ID курса"),
                "title": serializers.CharField(
                    max_length=200, help_text="Название модуля"
                ),
                "slug": serializers.CharField(
                    max_length=200, help_text="Слаг модуля"
                ),
                "description": serializers.CharField(
                    help_text="Краткое описание модуля"
                ),
            },
        ),
        "message": serializers.CharField(default="Модуль обновлен."),
    },
)

response_delete_module_204 = inline_serializer(
    name="response_delete_module_204",
    fields={
        "message": serializers.CharField(default="Модуль успешно удален."),
    },
)

response_create_lesson_201 = inline_serializer(
    name="response_create_lesson_201",
    fields={
        "data": inline_serializer(
            name="response_create_lesson_data",
            fields={
                "id": serializers.IntegerField(help_text="ID урока"),
                "module_id": serializers.IntegerField(help_text="ID модуля"),
                "title": serializers.CharField(max_length=200, help_text="Название урока"),
                "slug": serializers.CharField(max_length=200, help_text="Слаг урока"),
            },
        ),
        "message": serializers.CharField(default="Урок добавлен."),
    },
)

response_update_lesson_200 = inline_serializer(
    name="response_update_lesson_200",
    fields={
        "data": inline_serializer(
            name="response_update_lesson_data",
            fields={
                "id": serializers.IntegerField(help_text="ID урока"),
                "module_id": serializers.IntegerField(help_text="ID модуля"),
                "title": serializers.CharField(max_length=200, help_text="Название урока"),
                "slug": serializers.CharField(max_length=200, help_text="Слаг урока"),
            },
        ),
        "message": serializers.CharField(default="Урок обновлен."),
    },
)

response_delete_lesson_204 = inline_serializer(
    name="response_delete_lesson_204",
    fields={
        "message": serializers.CharField(default="Урок успешно удален."),
    },
)

teacher_courses_response_200 = inline_serializer(
    name="teacher_courses_response_200",
    fields={
        "data": serializers.ListSerializer(
            child=inline_serializer(
                name="teacher_courses_data",
                fields={
                    "id": serializers.CharField(help_text="ID курса"),
                    "title": serializers.CharField(max_length=200, help_text="Название курса"),
                    "overview": serializers.CharField(help_text="Описание курса"),
                    "is_fixed": serializers.CharField(help_text="Закреплён"),
                    "is_published": serializers.CharField(help_text="Опубликован"),
                    "count_modules": serializers.IntegerField(help_text="Количество модулей в курсе"),
                    "count_lessons": serializers.IntegerField(help_text="Количество уроков"),
                    "count_students": serializers.IntegerField(help_text="Количество студентов записанных на курс"),
                },
            )
        ),
        "pagination": pagination,
        "message": serializers.CharField(default="Курсы учителя"),
    },
)

get_lesson_response_200 = inline_serializer(
    name="get_lesson_response_200",
    fields={
        "data": serializers.ListSerializer(
            child=inline_serializer(
                name="get_lesson_data",
                fields={
                    "id": serializers.CharField(help_text="ID шага"),
                    "content": serializers.CharField(help_text="Контент шага"),
                    "solution_comments": serializers.ListSerializer(
                        child=inline_serializer(
                            name="get_solution_data",
                            fields={
                                "solution_link": serializers.URLField(
                                    help_text="Ссылки на решение задачи контента шага", ),
                                "comment": serializers.URLField(help_text="Ссылки на решение задачи контента шага", ),
                            }
                        )
                    ),
                    "solve_required": serializers.BooleanField(help_text="Наличие задачи", required=False),
                    "attempts": serializers.IntegerField(help_text="Попытки", required=False),
                    "status": serializers.ChoiceField(choices=[
                        ('success', 'success'),
                        ('error', 'error'),
                        ('review', 'review'),
                    ], help_text="статус шага", required=False),
                },
            )
        ),
        "pagination": pagination,
        "message": serializers.CharField(default="Данные урока для шагов"),
    },
)

create_comment_teacher_task_201 = inline_serializer(
    name="create_comment_teacher_task_201",
    fields={
        "data": serializers.ListSerializer(
            child=inline_serializer(
                name="create_comment_teacher_task_data",
                fields={
                    "id": serializers.IntegerField(
                        help_text="ID коментария"
                    ),
                    "text": serializers.CharField(
                        help_text="Текст комментария"
                    ),
                    "teacher": serializers.IntegerField(
                        help_text="учитель комментатор"
                    ),
                    "task_text": serializers.IntegerField(
                        help_text="текст комментария"
                    ),
                    "is_passed": serializers.BooleanField(
                        help_text="пройдено"
                    ),
                },
            )
        ),
        "message": serializers.CharField(
            default="Комментарий учителя к заданию с оценкой добавлен"
        ),
    },
)

response_update_comment_teacher_task_200 = inline_serializer(
    name="update_comment_teacher_task_201",
    fields={
        "data": serializers.ListSerializer(
            child=inline_serializer(
                name="update_comment_teacher_task_data",
                fields={
                    "id": serializers.IntegerField(
                        help_text="ID коментария"
                    ),
                    "text": serializers.CharField(
                        help_text="Текст комментария"
                    ),
                    "teacher": serializers.IntegerField(
                        help_text="учитель комментатор"
                    ),
                    "task_text": serializers.IntegerField(
                        help_text="текст комментария"
                    ),
                    "is_passed": serializers.BooleanField(
                        help_text="пройдено"
                    ),
                },
            )
        ),
        "message": serializers.CharField(
            default="Комментарий учителя к заданию с оценкой обновлён"
        ),
    },
)

response_delete_comment_teacher_task_204 = inline_serializer(
    name="response_delete_comment_teacher_task_204",
    fields={
        "message": serializers.CharField(
            default="Комментарий учителя к заданию с оценкой успешно удален."
        ),
    },
)

send_solution_task_lesson_201 = inline_serializer(
    name="send_solution_task_204",
    fields={
        "message": serializers.CharField(default="Решение отправлено на проверку."),
    },
)

response_delete_text_step_teacher_task_204 = inline_serializer(
    name="response_delete_text_step_teacher_task_204",
    fields={
        "message": serializers.CharField(
            default="Шаг успешно удалён."
        ),
    },
)

steps_lesson_response_200 = inline_serializer(
    name="steps_lesson_message_200",
    fields={
        "message": serializers.CharField(default="Шаг пройден."),
    },
)

subscription_course_response_201 = inline_serializer(
    name="subscription_course_message_201",
    fields={
        "message": serializers.CharField(default="Пользователь подписан на курс."),
    },
)

progress_course_module_response_200 = inline_serializer(
    name="progress_course_module_response_200",
    fields={
        "data": serializers.ListSerializer(
            child=inline_serializer(
                name="progress_course_module_200",
                fields={
                    "course": inline_serializer(
                        name="progress_course",
                        fields={
                            "id": serializers.IntegerField(help_text="ID курса"),
                            "title": serializers.CharField(help_text="Название курса"),
                            "is_completed": serializers.BooleanField(help_text="Состояние курса")
                        },
                    ),
                    "modules": inline_serializer(
                        name="progress_module",
                        fields={
                            "id": serializers.IntegerField(help_text="ID модуля"),
                            "title": serializers.CharField(help_text="Название название"),
                            "is_completed": serializers.BooleanField(help_text="Состояние модуля")
                        },
                    ),
                },
            )
        ),
        "pagination": pagination,
        "message": serializers.CharField(default="Прогресс курса"),
    },
)
