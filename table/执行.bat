:start
@echo off
color 0A
::Ҫ�����Ŀ¼
SET execPath=./table

::ǰ�˵���json·��
SET saveClientJsonSrc=./client/config.json

::ǰ�˵���ts·��
SET saveClientTsSrc=./client/ConfigInterface.ts

::����������json·��
SET saveServerJsonSrc=./server/res.json

::�����������ṹ��·��
SET saveServerStuctSrc=./server/ConfigStruct.go

::�����������ṹ���pack��
SET gopack=main

::��ͼ�༭������������·��
SET mapSrc=./table/map/

::�������������json��ʼ����
SET saveServerJsonIndex=1

::�������������json��������
SET saveServerJsonEnd=3

xlsxtool.exe -path=%execPath% -saveClientJsonSrc=%saveClientJsonSrc% -saveClientTsSrc=%saveClientTsSrc% -saveServerJsonSrc=%saveServerJsonSrc% -saveServerStuctSrc=%saveServerStuctSrc% -gopack=%gopack% -mapSrc=%mapSrc% -saveServerJsonIndex=%saveServerJsonIndex% -saveServerJsonEnd=%saveServerJsonEnd%
set choice=
set /p choice=  ��������˳�
