#!/usr/bin/env bash
cd "$(dirname "$0")" || exit
source ./runner/src/runner.sh


task_build() {
  nohup docker build -t danobot/rfgateway . &
  echo "Build running in background. Access by tailing nohup.out file. "
}
task_rebuild() {
  docker build -t danobot/rfgateway . && docker-compose up rfgateway
}
task_push() {
  nohup docker push danobot/rfgateway &
}
task_receivelogs() {
  docker logs -f rx-rf-gateway
}
task_sendlogs() {
  docker logs -f tx-rf-gateway
}
task_pushc() {
  nohup docker push danobot/crfgateway &
}
task_buildc() {
  nohup docker build -t danobot/crfgateway -f c-implementation/Dockerfile &
  echo "Build running in background. Access by tailing nohup.out file. "
}

task_runc(){
  cd c-implementation
  docker-compose up
}
task_run(){
  docker-compose up
  echo "Spun up two containers, one for receiving RF traffic and emitting MQTT. The other for receiving MQTT commands to be sent out as RF signals."
}
