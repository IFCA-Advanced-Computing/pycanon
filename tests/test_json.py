import numpy as np

from pycanon import report


class TestMath:
    qi = ['Teacher', 'Gender', 'Ethnic', 'Freeredu', 'wesson']
    sa = ['Score']

    def test_report_math(self):
        dataset = './Data/Processed/StudentsMath_Score.csv'
        expected = (1, 1, 1, 1, np.nan, 71, 5.375278407684164,
                    4.276666119016055, 0.4165919952210274)
        assert expected == report.get_anon_report(dataset, self.qi, self.sa)

    def test_report_math_k5(self):
        dataset = './Data/Processed/StudentsMath_Score_k5.csv'
        expected = (5, 0.5, 4, 3, 1, 29.8, 5.036952602413629,
                    3.4275146899795286, 0.31023287057769827)
        assert expected == report.get_anon_report(dataset, self.qi, self.sa)
