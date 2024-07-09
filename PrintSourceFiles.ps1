# PrintSourceFiles.ps1
# This script prints the filename and subsequently the content of each file relevant to the development of the project source code.
# The purpose of this script is to easily send the project source code to an AI Programming Assistant LLM like ChatGPT, or Gemini, etc.

<#
.SYNOPSIS
Prints the filename and content of each relevant project source file.

.DESCRIPTION
This script iterates over a predefined list of relevant project source files, prints the filename, and then prints the content of each file.
It is useful for sharing the project source code with AI Programming Assistants.

.NOTES
File Name  : PrintSourceFiles.ps1
Author     : Daniel Hamelberg
Date       : 2024-07-09

#>

# Define the list of relevant files
$files = @(
    "src\**\*.*",
    "tests\**\*.*",
    "README.md"
)

# Iterate over each file and print its name and content
foreach ($file in $files) {
    if (Test-Path $file) {
        $filename = $file -replace '\\', '\\\\'  # Escape backslashes in the filename
        $content = Get-Content $file | ForEach-Object { $_ -replace '"', '\"' }  # Escape double quotes in the content
        $json = @{
            Filename = $filename
            Content = $content
        } | ConvertTo-Json
        Write-Output $json
    } else {
        Write-Output "File not found: $file"
    }
}
