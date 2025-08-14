from dataclasses import dataclass
from pathlib import Path


@dataclass
class Keyframe:
    """
    Unity-style keyframe data structure.
    """

    time: float
    value: float
    inTangent: float
    outTangent: float


def load_keyframes_from_tsv(file: Path) -> list[Keyframe]:
    """
    Load keyframes from a TSV file.
    """
    keyframes: list[Keyframe] = []

    with file.open(mode="r", encoding="utf-8") as fp:
        for index, line in enumerate(fp):
            if not line.strip():
                continue

            parts = line.strip().split("\t")
            if len(parts) != 4:
                raise ValueError(f"Invalid line {index + 1}: {line.strip()}")

            time, value, in_tangent, out_tangent = map(float, parts)
            keyframes.append(Keyframe(time, value, in_tangent, out_tangent))

    return keyframes
