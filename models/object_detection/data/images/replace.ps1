Get-Childitem 'C:\Onedrive school\OneDrive - Christelijk College Nassau-Veluwe\school\PWS\code\models\object_detection\data\images\trian colab\dataset\annotations\*.xml' -Recurse | ForEach {
	(Get-Content $_ | ForEach { $_ -replace 'png', 'jpg'}) |
	Set-Content $_
}