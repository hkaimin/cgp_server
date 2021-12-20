:start
@echo off
color 0A
::要处理的目录
SET execPath=./table

::前端导出json路径
SET saveClientJsonSrc=./client/config.json

::前端导出ts路径
SET saveClientTsSrc=./client/ConfigInterface.ts

::服务器导出json路径
SET saveServerJsonSrc=./server/res.json

::服务器导出结构体路径
SET saveServerStuctSrc=./server/ConfigStruct.go

::服务器导出结构体的pack名
SET gopack=main

::地图编辑器导出的配置路径
SET mapSrc=./table/map/

::服务器导出多个json开始索引
SET saveServerJsonIndex=1

::服务器导出多个json结束索引
SET saveServerJsonEnd=3

xlsxtool.exe -path=%execPath% -saveClientJsonSrc=%saveClientJsonSrc% -saveClientTsSrc=%saveClientTsSrc% -saveServerJsonSrc=%saveServerJsonSrc% -saveServerStuctSrc=%saveServerStuctSrc% -gopack=%gopack% -mapSrc=%mapSrc% -saveServerJsonIndex=%saveServerJsonIndex% -saveServerJsonEnd=%saveServerJsonEnd%
set choice=
set /p choice=  按任意键退出
