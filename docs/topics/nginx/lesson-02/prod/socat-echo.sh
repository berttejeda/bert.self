#!/bin/bash

handle() {
  echo 'HTTP/1.0 200 OK'
  echo 'Content-Type: text/plain'
  echo "Date: $(date)"
  echo "Server: $SOCAT_SOCKADDR:$SOCAT_SOCKPORT"
  echo "Client: $SOCAT_PEERADDR:$SOCAT_PEERPORT"
  echo 'Connection: close'
  echo
  cat
}

case $1 in
  "bind")
    socat -T0.05 -v tcp-l:10272,reuseaddr,fork,crlf system:". $0 && handle"
    ;;
esac