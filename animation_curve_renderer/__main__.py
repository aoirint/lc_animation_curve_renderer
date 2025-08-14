import asyncio
import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path

logger = logging.getLogger("animation_curve_renderer")


async def execute_cli(
    input_file: Path,
    output_file: Path,
    title: str,
) -> None:
    logger.info("Hello from animation_curve_renderer!")


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
