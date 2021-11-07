set OLD=%GOPATH%
set GOPATH=%~dp0;%GOPATH%
echo GOPATH=%GOPATH%

gofmt -w src

SET GOOS=
SET GOARCH=
go install main

SET GOOS=linux
SET GOARCH=amd64
go install main

SET GOOS=
SET GOARCH=

echo 'finished'

set GOPATH=%OLD%
