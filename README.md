# LC Animation Curve Renderer

Unityのアニメーションカーブをグラフとして描画するツールです。

Lethal Companyのアニメーションカーブを描画することを目的としています。

このツールは、アニメーションカーブのキーフレームデータをTSV形式で入力し、
エルミート曲線として補間したグラフを生成します。

## 環境構築

- Python 3.12
- uv 0.8

```shell
uv sync --all-groups
```

## コードフォーマット

```shell
uv run ruff check --fix
uv run ruff format

uv run mypy .
```

## 実行方法

```shell
uv run python -m lc_animation_curve_renderer --input_file <keyframe_file>
```

`keyframe_file`は、`time`、`value`、`in_tangent`、`out_tangent` の列で構成されるTSVファイルです。
