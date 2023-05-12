Set-Location .\kivy_pigrapp
py -m pip install --upgrade pip setuptools virtualenv

py -m virtualenv kivy_venv
kivy_venv\Scripts\activate
py -m pip install "kivy[base]" kivy_examples
pip install requests