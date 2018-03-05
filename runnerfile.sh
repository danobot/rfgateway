#!/usr/bin/env bash
cd "$(dirname "$0")" || exit
source ./runner/src/runner.sh


task_build_receive() {
  docker build -t danobot/rfgateway .
}
