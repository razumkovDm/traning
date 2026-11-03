# TRANSACTIONAL: аудит 900 запросов

Дата: 2026-11-03. Переводы не выполнялись.

## Сводка

- Исходная выборка: 900 реальных RU-запросов из выгрузки Букварикса.
- Выгрузка: **139,839** исходных строк.
- Сохранено оригиналов: **379**. Заменено: **521**; полный журнал в `review_log.csv`.
- Итог: **900 уникальных RU-запросов**. Назначение языков: **RU 300 / UK 300 / EN 300**.
- Россия-специфичных формулировок, закреплённых за RU: **106**.
- Источник и точная/общая частотность подтверждены для всех **900** запросов.
- Точных дублей и пересечений с остальными пятью классами (включая исправленные INFORMATIONAL и COMMERCIAL): **0**.
- Запросы не переводились и не генерировались.

## Принципы

- Убираются информационные вопросы («как скачать», «сколько стоит»), сравнения, навигационные формулировки («официальный сайт»), неоднозначное «доставка отследить», слишком расплывчатые фразы, очевидные спам-кластеры и слабые запросы.
- Контролируется однотипность: многократные варианты Roblox, Minecraft, Steam, авиабилетов и региональных услуг не должны занимать весь датасет.
- Набор распределён по разным действиям (купить, заказать, снять, забронировать, записаться, скачать, оплатить, оформить, зарегистрироваться и др.) и по предметным группам.
- Российские сервисы, бюрократические названия и геозависимые фразы оставлены преимущественно в RU, чтобы UK/EN были естественнее.
- `collected_at` пусто, потому что исходная дата сбора неизвестна.

## Темы

- `software_download`: 100 (RU 33 / UK 34 / EN 33)
- `game_download`: 50 (RU 16 / UK 17 / EN 17)
- `media_download`: 25 (RU 8 / UK 8 / EN 9)
- `electronics_purchase`: 93 (RU 31 / UK 31 / EN 31)
- `home_tools_purchase`: 64 (RU 21 / UK 22 / EN 21)
- `clothes_beauty_purchase`: 40 (RU 13 / UK 14 / EN 13)
- `vehicle_purchase`: 35 (RU 11 / UK 12 / EN 12)
- `property_purchase`: 35 (RU 11 / UK 12 / EN 12)
- `kids_pets_purchase`: 29 (RU 10 / UK 9 / EN 10)
- `other_purchase`: 36 (RU 12 / UK 12 / EN 12)
- `tickets_booking`: 70 (RU 23 / UK 24 / EN 23)
- `food_goods_delivery`: 63 (RU 21 / UK 21 / EN 21)
- `taxi_courier`: 11 (RU 4 / UK 3 / EN 4)
- `rental`: 50 (RU 16 / UK 17 / EN 17)
- `payments_topups`: 60 (RU 20 / UK 20 / EN 20)
- `subscriptions`: 30 (RU 10 / UK 10 / EN 10)
- `appointments`: 40 (RU 16 / UK 12 / EN 12)
- `account_registration`: 16 (RU 6 / UK 5 / EN 5)
- `forms_finance`: 45 (RU 15 / UK 15 / EN 15)
- `services_order`: 8 (RU 3 / UK 2 / EN 3)

## Замены: распределение причин

- `known_bad_context`: 8
- `near_duplicate_or_topic_balance`: 399
- `time_bound_or_outdated`: 6
- `navigation_contamination`: 5
- `navigation_cabinet`: 2
- `game_mod_or_hack`: 11
- `unsafe_or_weak_query`: 4
- `bad_entity_or_obsolete_version`: 4
- `time_bound_media`: 1
- `local_electronics_repeat`: 1
- `too_generic`: 2
- `narrow_regional_dup`: 2
- `nontransactional_or_unrecognized_action`: 46
- `ambiguous_or_wrong_topic`: 1
- `ticket_false_positive`: 2
- `mixed_or_nontransactional_intent`: 9
- `weak_media_query`: 1
- `unsuitable_software_query`: 1
- `info_about_document`: 2
- `unbalanced_regional_density`: 11
- `subscription_not_checkout`: 2
- `not_rental`: 1

## Ограничения

Разметка является предварительной (эвристики, тематические правила и выборочная смысловая проверка). **Она не подтверждена независимой ручной проверкой каждой строки** и не основана на просмотре SERP по каждому запросу. Часть поисковых намерений остаётся пограничной, особенно подписки, загрузки и локальные запросы. Частотности взяты из пользовательского CSV и не перепроверялись на актуальность.