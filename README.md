# meno-lite-0-1-mlx-convert

Convert [bond005/meno-lite-0.1](https://huggingface.co/bond005/meno-lite-0.1) to MLX (mxfp8 8-bit).

## Vendored tools

- `tools/convert_hf_to_gguf.py` — vendored unmodified from
  [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp/blob/465e49b9cea78a68b9c244ffb48d0ee24a82873d/convert_hf_to_gguf.py)
  (pinned commit `465e49b` — the last commit that modified the file), MIT license — see `tools/llama.cpp.LICENSE`.
  Note: it is vendored for reference; running it additionally requires the `gguf`
  package (`gguf-py` from llama.cpp or `pip install gguf`).
- `tools/conversion/` — the `conversion` package used by the script above, vendored
  unmodified from
  [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp/tree/0693dbfb915f33233818373b5f6969396658d02c/conversion)
  (pinned commit `0693dbf` — the last commit that modified the directory), see `tools/conversion/NOTICE.md`.
