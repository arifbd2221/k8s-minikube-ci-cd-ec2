#!/usr/bin/env bash
# Use this script to wait for a service to be ready

TIMEOUT=15
QUIET=0
WAITFORIT_host=
WAITFORIT_port=

echoerr() {
  if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi
}

usage() {
  echo "Usage: $0 host:port [-t timeout] [-- command args]"
  echo "  -h HOST | --host=HOST       Host or IP under test"
  echo "  -p PORT | --port=PORT       TCP port under test"
  echo "  -t TIMEOUT | --timeout=TIMEOUT"
  echo "                              Timeout in seconds, zero for no timeout"
  echo "  -q | --quiet                Don't output any status messages"
  echo "  -- COMMAND ARGS             Execute command with args after the test finishes"
  exit 1
}

wait_for() {
  for i in `seq $TIMEOUT` ; do
    nc -z "$WAITFORIT_host" "$WAITFORIT_port" > /dev/null 2>&1

    if [[ $? -eq 0 ]] ; then
      if [[ $QUIET -ne 1 ]] ; then echo "wait-for-it: $WAITFORIT_host:$WAITFORIT_port is available after $i seconds"; fi
      return 0
    fi

    sleep 1
  done
  echo "wait-for-it: timeout occurred after waiting $TIMEOUT seconds for $WAITFORIT_host:$WAITFORIT_port"
  return 1
}

wait_for_wrapper() {
  # In order to support SIGINT during timeout: http://unix.stackexchange.com/a/57692
  if [[ $QUIET -eq 1 ]]; then
    timeout $TIMEOUT bash -c "wait_for" > /dev/null 2>&1 &
  else
    timeout $TIMEOUT bash -c "wait_for" &
  fi
  PID=$!
  trap "kill -INT -$PID" INT
  wait $PID
  return $?
}

while [[ $# -gt 0 ]]
do
  case "$1" in
    *:* )
    WAITFORIT_host=$(printf "%s\n" "$1"| cut -d : -f 1)
    WAITFORIT_port=$(printf "%s\n" "$1"| cut -d : -f 2)
    shift 1
    ;;
    -q | --quiet)
    QUIET=1
    shift 1
    ;;
    -t)
    TIMEOUT="$2"
    shift 2
    ;;
    --timeout=*)
    TIMEOUT="${1#*=}"
    shift 1
    ;;
    -h)
    WAITFORIT_host="$2"
    shift 2
    ;;
    --host=*)
    WAITFORIT_host="${1#*=}"
    shift 1
    ;;
    -p)
    WAITFORIT_port="$2"
    shift 2
    ;;
    --port=*)
    WAITFORIT_port="${1#*=}"
    shift 1
    ;;
    --)
    shift
    exec "$@"
    ;;
    *)
    usage
    ;;
  esac
done

if [[ "$WAITFORIT_host" == "" || "$WAITFORIT_port" == "" ]]; then
  echo "Error: you need to provide a host and port to test."
  usage
fi

wait_for_wrapper

