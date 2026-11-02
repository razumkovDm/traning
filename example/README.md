# Example

Простейшее использование тестовой выборки:

```python
from pathlib import Path

queries = Path("data/queries_300.txt").read_text(encoding="utf-8").splitlines()
assert len(queries) == 300
for query in queries[:10]:
    print(query)
```

`Processing/` — входящие данные/очередь обработки, `Processed/` — уже обработанные наборы, `Ready/` — прошедшие проверки готовые наборы. Сейчас они пустые; основная проверенная подборка расположена в `data/`.
