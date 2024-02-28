import unittest
import numpy as np


def calc_vels(m1: float,
              m2: float,
              v1: np.array,
              v2: np.array,
              a1: np.array,
              a2: np.array
              ) -> tuple[list, list]:

    w1 = v1 - 2 * m2 / (m1 + m2) * ((v1 - v2).T @ (a1 - a2)) / ((a1 - a2).T @ (a1 - a2)) * (a1 - a2)
    w2 = v2 - 2 * m1 / (m1 + m2) * ((v2 - v1).T @ (a2 - a1)) / ((a2 - a1).T @ (a2 - a1)) * (a2 - a1)
    return w1.tolist(), w2.tolist()


def flatten_list(list_of_lists: list[list]) -> list:
    return [round(item, 10) for sublist in list_of_lists for item in sublist]


class TestMathFunctions(unittest.TestCase):

    def test_1(self):
        m1, m2 = 1.0, 1.0
        v1 = np.array([10.0, 0.0])
        v2 = np.array([-10.0, 0.0])
        a1 = np.array([-1.0, 0.0])
        a2 = np.array([1.0, 0.0])

        result = calc_vels(m1, m2, v1, v2, a1, a2)
        expected_result = [-10.0, 0.0], [10.0, 0.0]

        self.assertEqual(result, expected_result)

    def test_2(self):
        m1, m2 = 99.0, 1.0
        v1 = np.array([10.0, 0.0])
        v2 = np.array([-10.0, 0.0])
        a1 = np.array([-9.0, 0.0])
        a2 = np.array([1.0, 0.0])

        result = flatten_list(calc_vels(m1, m2, v1, v2, a1, a2))
        expected_result = flatten_list([[9.6, 0.0], [29.6, 0.0]])

        self.assertEqual(result, expected_result)

    def test_3(self):
        m1, m2 = 100.0, 100.0
        v1 = np.array([-5.944050560528412, -8.564544641233914])
        v2 = np.array([-3.126256984519088, 7.602630729293933])
        a1 = np.array([0.6381731882506756, 9.98254824345279])
        a2 = np.array([-0.6381731882506472, -9.982548243452786])

        result = flatten_list(calc_vels(m1, m2, v1, v2, a1, a2))
        expected_result = flatten_list([[-4.903238699022251, 7.716231190674263], [-4.167068846025249, -8.678145102614243]])

        self.assertEqual(result, expected_result)

    def test_4(self):
        m1, m2 = 900.0, 100.0
        v1 = np.array([6.275207281781148, 1.8525669980804769])
        v2 = np.array([-2.4707106152583087, 12.334611148103816])
        a1 = np.array([-15.828382139122077, 25.495324853000263])
        a2 = np.array([5.276127379707354, -8.49844161766675])

        result = flatten_list(calc_vels(m1, m2, v1, v2, a1, a2))
        expected_result = flatten_list([[4.849142448095183, 4.149579154894633], [10.36387288791537, -8.338498263223586]])

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
