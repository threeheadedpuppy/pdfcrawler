@echo off
pushd %~dp0\..
pipenv run python crawler.py %*
popd