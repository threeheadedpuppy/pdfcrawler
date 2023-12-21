@echo off
pushd %~dp0\..
pipenv run pyinstaller crawler.py
popd