@echo off

cd dependencies
git clone https://github.com/pybind/pybind11.git

cd ..

:: Create build directory if it doesn't exist
if not exist build (
    mkdir build
)

:: Navigate to build directory
cd build

:: Run cmake in the parent directory
cmake ..

:: Replace with your MSBuild.exe path!
call "C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe" pyDEM.sln /p:Configuration=Release

:: Python install
cd ..\py

:: Check if virtual environment directory exists
if not exist venv (
    :: Create a virtual environment
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate

:: Upgrade pip
pip install --upgrade pip

:: Install dependencies
pip install -r requirements.txt

:: copy the DEM module to the virtual environment
if not exist .\venv\Lib\site-packages\pyDEM (
    mkdir .\venv\Lib\site-packages\pyDEM
)
xcopy /Y ..\build\Release\*.pyd .\venv\Lib\site-packages

echo Setup complete.
pause