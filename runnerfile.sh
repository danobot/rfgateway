#!/usr/bin/env bash
cd "$(dirname "$0")" || exit
source ./runner/src/runner.sh


task_build() {
  nohup docker build -t danobot/rfgateway . &
  echo "Build running in background. Access by tailing nohup.out file. "
}
task_push() {
  docker push danobot/rfgateway
}
task_receivelogs() {
  docker logs -f gateway-rx
}
task_sendlogs() {
  docker logs -f gateway-tx
}
task_pushc() {
  docker push danobot/crfgateway
}
task_buildc() {
  nohup docker build -t danobot/crfgateway c\ implementation/. &
  echo "Build running in background. Access by tailing nohup.out file. "
}

task_runc(){
  cd c\ implementation
  docker-compose up
}
task_run(){
  docker-compose up
  echo "Spun up two containers, one for receiving RF traffic and emitting MQTT. The other for receiving MQTT commands to be sent out as RF signals."
}
