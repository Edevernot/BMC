# 姿态分类结果平滑
class EMADictSmoothing(object):
    """平滑姿势分类。"""

    def __init__(self, window_size=10, alpha=0.2):
        self._window_size = window_size
        self._alpha = alpha
        self._data_in_window = []

    def __call__(self, data):
        """平滑给定的姿势分类。

        平滑是通过计算在给定时间窗口中观察到的每个姿势类别的指数移动平均值来完成的。错过的姿势类将替换为 0。

        Args:
          data: Dictionary with pose classification. Sample:
              {
                'pushups_down': 8,
                'pushups_up': 2,
              }

        Result:
          Dictionary in the same format but with smoothed and float instead of
          integer values. Sample:
            {
              'pushups_down': 8.3,
              'pushups_up': 1.7,
            }
        """
        # 将新数据添加到窗口的开头以获得更简单的代码.
        self._data_in_window.insert(0, data)
        self._data_in_window = self._data_in_window[:self._window_size]

        #搜集所有数据点的关键点
        keys = set([key for data in self._data_in_window for key, _ in data.items()])

        # 计算平滑之值.
        smoothed_data = dict()
        for key in keys:
            ema_factor = 1.0    # 初始化EMA
            weighted_sum = 0.0   # 初始化加权
            normalization_factor = 0.0    # 初始化归一
            for data in self._data_in_window:
                value = data[key] if key in data else 0.0

                weighted_sum += ema_factor * value
                normalization_factor += ema_factor

                # Update factor.
                ema_factor *= (1.0 - self._alpha)

            smoothed_data[key] = weighted_sum / normalization_factor

        return smoothed_data

