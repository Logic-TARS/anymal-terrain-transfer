#!/usr/bin/env bash
set -euo pipefail

uv run ./scripts/play.py --env anymal_c_navigation_rough --num-envs 64
