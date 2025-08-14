import bisect

from .keyframe import Keyframe


class HermiteCurve:
    """
    Non-weighted Hermite curve evaluator.

    Out of range data is clamped to the nearest keyframe value.
    This behavior is similar to Unity's AnimationCurve with
    `pre_wrap_mode` and `post_wrap_mode` set to `ClampForever`.
    """

    def __init__(self, keyframes: list[Keyframe]):
        self.keyframes = sorted(keyframes, key=lambda k: k.time)

    def evaluate(self, t: float) -> float:
        keyframes = self.keyframes

        if not keyframes:
            return 0.0
        if len(keyframes) == 1:
            return keyframes[0].value

        times = [k.time for k in keyframes]

        # ClampForever: 範囲外は端の値を返す
        if t <= keyframes[0].time:
            return keyframes[0].value
        if t >= keyframes[-1].time:
            return keyframes[-1].value

        i = bisect.bisect_right(times, t) - 1
        k0 = keyframes[i]
        k1 = keyframes[i + 1]

        t0, t1 = k0.time, k1.time
        y0, y1 = k0.value, k1.value
        dx = t1 - t0
        if dx == 0.0:
            return y1

        u = (t - t0) / dx
        m0 = k0.outTangent
        m1 = k1.inTangent

        h00 = 2 * u**3 - 3 * u**2 + 1
        h10 = u**3 - 2 * u**2 + u
        h01 = -2 * u**3 + 3 * u**2
        h11 = u**3 - u**2

        return h00 * y0 + h10 * (dx * m0) + h01 * y1 + h11 * (dx * m1)
