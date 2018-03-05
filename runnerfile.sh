#!/usr/bin/env bash
cd "$(dirname "$0")" || exit
source ./runner/src/runner.sh
source_files=(bin/runner src/*.sh)

task_hello() {
    echo "Hello"
}

task_test() {
    bash test/test.sh >/dev/null
}

task_readme() {
    doctoc README.md
}

task_default() {
    runner_parallel shellcheck test
}
