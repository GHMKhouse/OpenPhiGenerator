python -m PyInstaller main.py -n OpenPhiGenerator -i OpenPhiGenerator.ico
copy SmileySans-Oblique.ttf .\dist\OpenPhiGenerator
xcopy .\resources .\dist\OpenPhiGenerator\resources\ /e
copy OpenPhiGenerator.ico .\dist\OpenPhiGenerator
rem "C:\Program Files\7-Zip\7z.exe" a -tzip OpenPhiGenerator-win64.zip .\dist\OpenPhiGenerator
