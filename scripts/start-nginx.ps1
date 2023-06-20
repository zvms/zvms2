echo "making dirs"
Function GenerateFolder($path) {
    $global:foldPath = $null
    foreach($foldername in $path.split("")) {
        $global:foldPath += ($foldername+"")
        if (!(Test-Path $global:foldPath)){
            New-Item -ItemType Directory -Path $global:foldPath
            # Write-Host"$global:foldPath Folder Created Successfully"
        }
    }
}
GenerateFolder nginx\80\logs
GenerateFolder nginx\80\temp
GenerateFolder nginx\4000\logs
GenerateFolder nginx\4000\temp
mkdir ../web/deploy
mkdir ../web/deploy/assets
./copy-dist.ps1
echo "starting 80"
start nginx "-c conf/nginx.conf -p nginx/80"
echo "starting 4000"
start nginx "-c conf/nginx.conf -p nginx/4000"
echo "OK"