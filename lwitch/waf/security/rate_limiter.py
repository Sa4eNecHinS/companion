from collections import defaultdict, deque
from time import monotonic


class RateLimiter:
    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        self.max_requests = max_requests  # in minutes
        self.window_seconds = window_seconds
        # defaultdict(factory) - создает ключ автоматическси (при его отсутствии)
        # и создает значение вызовом factory
        # в данном случае для каждого пользователя создается новая deque
        self._requests = defaultdict(deque)

    def _cleanup(self, user_id: str):
        # monotonic аналог time.time
        # главное отличие в том, что не сдвигает время при изменении времени в системе
        now = monotonic()
        queue = self._requests[user_id]

        # queue[0] - monotonic (лежат числа)
        while queue and (now - queue[0]) > self.window_seconds:
            # время самого последнего визита пользователя удаляется
            queue.popleft()

    def allow(self, user_id: str = "default_user") -> bool:
        self._cleanup(user_id)
        queue = self._requests[user_id]

        if len(queue) >= self.max_requests:
            return False

        # добавление времени последнего запроса
        queue.append(monotonic())
        return True

    def get_status(self, user_id: str = "default_user") -> tuple[int, int]:
        self._cleanup(user_id)
        return len(self._requests[user_id]), self.max_requests
