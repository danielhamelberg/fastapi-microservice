# This script prints the filename and subsequently the content of each file relevant to the development of the project source code.

# Define the list of relevant files
$files = @(
    "main.py"
    # Add other relevant files here
)

# Iterate over each file and print its name and content
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Output "Filename: $file"
        Write-Output "Content:"
        Get-Content $file | ForEach-Object { Write-Output $_ }
        Write-Output "`n"  # Add a newline for better readability
    } else {
        Write-Output "File not found: $file"
    }
}
