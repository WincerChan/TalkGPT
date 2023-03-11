import unittest

from tg.chatgpt.utils import CircularConversation


class TestCircularQueue(unittest.TestCase):
    def __init__(self, *args):
        self.cq = CircularConversation(3)
        super().__init__(*args)

    def check(self, i):
        ans = list(filter(lambda x: x >= 0, range(i - 2, i + 1)))
        print(self.cq.queue, ans)
        self.assertEqual(self.cq.queue, ans)

    def test_push(self):
        for i in range(10):
            self.cq.push(i)
            self.check(i)


if __name__ == "__main__":
    unittest.main()
