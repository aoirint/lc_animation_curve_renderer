import asyncio
import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

from .hermite_curve import HermiteCurve
from .keyframe import load_keyframes_from_tsv

logger = logging.getLogger("animation_curve_renderer")


async def execute_cli(
    input_file: Path,
    output_file: Path,
    title: str,
) -> None:
    # Load keyframes from TSV file
    keyframes = load_keyframes_from_tsv(file=input_file)

    # Build curve
    curve = HermiteCurve(keyframes=keyframes)

    # Sample and plot
    # 右に5%の外挿を含めてサンプリング
    t_min = keyframes[0].time
    t_max = keyframes[-1].time
    t_range = t_max - t_min
    ts = np.linspace(t_min, t_max + t_range * 0.05, 500)
    ys = np.array([curve.evaluate(t) for t in ts])

    plt.figure(
        figsize=(16, 9),
        dpi=300,
        facecolor="white",
        edgecolor="black",
    )
    plt.plot(ts, ys)
    plt.scatter(
        [k.time for k in keyframes],
        [k.value for k in keyframes],
        label="Keyframes",
    )
    plt.xlabel("Input")
    plt.ylabel("Output")
    plt.legend()
    plt.title(title)

    plt.grid(
        visible=True,
        which="both",
        axis="both",
    )
    gca: plt.Axes = plt.gca()  # type: ignore[no-untyped-call]
    gca.xaxis.set_major_locator(MultipleLocator(0.05))
    gca.yaxis.set_major_locator(MultipleLocator(0.1))

    ts_expect = np.linspace(t_min, t_max, 1000)
    ys_expect = np.array([curve.evaluate(t) for t in ts_expect])
    expected_value = ys_expect.mean()
    print(f"Expected value: {expected_value:.4f}")

    # 特別なX値でのY値を取得し、グラフに表示
    special_xs = [0.7865, 1.012]
    for x in special_xs:
        y = curve.evaluate(x)
        plt.plot(x, y, "ro")  # 赤丸でマーク
        plt.text(
            x,
            y,
            f"({x:.4f}, {y:.4f})",
            color="red",
            fontsize=12,
            ha="right",
            va="bottom",
        )

        # 制限値付きの期待値の計算
        ts_expect = np.linspace(t_min, x, 1000)
        ys_expect = np.array([curve.evaluate(t) for t in ts_expect])
        expected_value = ys_expect.mean()
        print(f"Expected value with limit (x <= {x}): {expected_value:.4f}")

    # Y=0となるtを探索し、同様にプロット
    zero_crossings: list[float] = []
    for i in range(len(ts) - 1):
        if ys[i] * ys[i + 1] < 0:
            # 線形補間でゼロ点近似
            t0, t1 = ts[i], ts[i + 1]
            y0, y1 = ys[i], ys[i + 1]
            t_zero = t0 - y0 * (t1 - t0) / (y1 - y0)
            zero_crossings.append(t_zero)

    for x in zero_crossings:
        y = 0.0
        plt.plot(x, y, "ro")
        plt.text(
            x,
            y,
            f"({x:.4f}, 0.0000)",
            color="red",
            fontsize=12,
            ha="right",
            va="bottom",
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(
        fname=output_file,
        bbox_inches="tight",
    )


async def handle_cli(args: Namespace) -> None:
    input_file_string: str = args.input_file
    output_file_string: str = args.output_file
    title: str = args.title

    input_file = Path(input_file_string)
    output_file = Path(output_file_string)

    await execute_cli(
        input_file=input_file,
        output_file=output_file,
        title=title,
    )


async def main() -> None:
    """
    Main function
    """

    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        help="Path to the input TSV file containing keyframes.",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        default="work/curve.webp",
        help="Path to the output WEBP image file.",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Animation Curve",
        help="Title for the plot.",
    )
    parser.set_defaults(func=handle_cli)

    args = parser.parse_args()

    if hasattr(args, "func"):
        if asyncio.iscoroutinefunction(args.func):
            await args.func(args)
        elif callable(args.func):
            args.func(args)
        else:
            raise ValueError("The specified function is not callable or coroutine.")
    else:
        raise ValueError("No function specified in the arguments.")


if __name__ == "__main__":
    asyncio.run(main())
