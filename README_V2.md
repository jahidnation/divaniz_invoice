



1st Install
-----------------------------------

```
python -m venv venv

Set-ExecutionPolicy RemoteSigned

.\venv\Scripts\Activate.ps1

pip install jinja2

```



Normal
-----------------------------------
```
python -m venv venv

Set-ExecutionPolicy RemoteSigned

.\venv\Scripts\Activate.ps1

python run.py

```






If Issue
------------------------------------

```
Remove-Item -Recurse -Force .\venv\

python -m venv venv

Set-ExecutionPolicy RemoteSigned

.\venv\Scripts\Activate.ps1

pip install jinja2

```
