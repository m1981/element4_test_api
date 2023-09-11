$owner="m1981" 
$repo="element4_test_api"
$githubAPI="https://api.github.com/repos/$owner/$repo/actions/artifacts"
$token = "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"

$header = @{
    Authorization = "Bearer $token"
    accept = 'application/vnd.github+json'
    }

    try {
        # Parse the JSON response from GitHub's API for listing the latest artifacts.
        $artifacts = Invoke-RestMethod -Uri $githubAPI -Headers $header -ErrorAction Stop
        $latestArtifact = $artifacts.artifacts[0]

        # Extract the download URL
        $downloadUrl = $latestArtifact.archive_download_url


        # Parse the JSON response from GitHub's API for listing the latest artifacts.
        $artifacts = Invoke-RestMethod -Uri $githubAPI -Headers $header
        $latestArtifact = $artifacts.artifacts[0]

        # Extract the download URL
        $downloadUrl = $latestArtifact.archive_download_url

        if (!(Test-Path -Path ".\latest-downloaded.txt")) {
            # If the file doesn't exist yet, create it.
            New-Item .\latest-downloaded.txt -ItemType File -Force
        }

        # Load latest downloaded version
        $lastDownloaded = Get-Content .\latest-downloaded.txt

        # If the latest artifact is different from what was last downloaded, download it.
        if ($latestArtifact.id -ne $lastDownloaded)  {

            # Download the latest artifact
            $zipFile = "$($latestArtifact.name).zip"
            Invoke-WebRequest -Uri $downloadUrl -Headers @{accept='application/vnd.github.v3+json'} -OutFile $zipFile
            Invoke-WebRequest -Uri $downloadUrl -Headers $header -OutFile $zipFile

            # Extract zip content in the current directory
            Expand-Archive -Path $zipFile -DestinationPath "." -Force

            # Remove the zipped file if not required
            Remove-Item -Path $zipFile

            #Update latest downloaded version
            Set-Content -Path .\latest-downloaded.txt -Value $latestArtifact.id
        }
    }
    catch {
        $errorDetails = $_.Exception.Response.Headers["x-accepted-github-permissions"]
        Write-Output "Error: $($_.Exception.Message)"
        Write-Output "Missing Permissions: $errorDetails"
    }
