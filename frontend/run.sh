#!/usr/bin/env bash

echo fs.inotify.max_user_watches=524288 | tee -a /etc/sysctl.conf && sysctl -p

case $1 in
  start)
    # The '| cat' is to trick Node that this is an non-TTY terminal
    # then react-scripts won't clear the console.
    npm start | cat
    ;;
  build)
    npm build
    ;;
  test)
    npm test $@
    ;;
  *)
    npm "$@"
    ;;
esac