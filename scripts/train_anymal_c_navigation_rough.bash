#!/usr/bin/env bash
set -euo pipefail

uv run scripts/train.py --env anymal_c_navigation_rough --num-envs 4096
