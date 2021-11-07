#!/usr/bin/env bash
#source $HOME/.bashrc
source env.source

gofmt -w src

echo $GOPATH, $GOROOT
go install main

echo 'finished'
