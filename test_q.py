import unittest

from question_lists import QuestionList

class Test_Continuum(unittest.TestCase):
    """
    Test class for QOTD
    """

    q = QuestionList()
    
    def test_init(self):
        print("Testing initialized state of QContinuum.")
        self.assertEqual(self.q.past, dict())
        self.assertEqual(self.q.future, dict())
        self.assertEqual(self.q.current_id, 0)
        print("Test passed")


if __name__ == '__main__':
    unittest.main()
