# Lager PDF-ene i testdataene (FR-8, kriterium 5, story 6.1).
#
# Word åpner hver .txt i testdata/case-*/ (cv.txt, annonse.txt og eget-brev.txt) som UTF-8 og
# lagrer den som PDF (format 17) med samme navn ved siden av: cv.txt blir cv.pdf. Da har PDF-en
# samme tekst som .txt-fila, og testen av kriterium 5 i tests/test_testdata.py sjekker at
# begge gir samme testcase og samme nøkkelordtreff.
#
# Trenger Microsoft Word på Windows. Kjøres fra backend/ i PowerShell:
#
#     powershell -ExecutionPolicy Bypass -File scripts\lag_testpdf.ps1
#
# Kjør skriptet på nytt når en .txt-fil i testdataene endres. fasit.md og ki-svar/ røres ikke.

$ErrorActionPreference = "Stop"

$testdata = Join-Path (Split-Path -Parent $PSScriptRoot) "testdata"
$navn = @("cv.txt", "annonse.txt", "eget-brev.txt")

# Konstanter fra Word: åpne som kodet tekst, UTF-8 og lagre som PDF.
$wdOpenFormatEncodedText = 5
$msoEncodingUTF8 = 65001
$wdFormatPDF = 17
$mangler = [Type]::Missing

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    foreach ($case in Get-ChildItem -Path $testdata -Directory -Filter "case-*") {
        foreach ($fil in $navn) {
            $txt = Join-Path $case.FullName $fil
            if (-not (Test-Path $txt)) {
                continue
            }
            $pdf = [System.IO.Path]::ChangeExtension($txt, ".pdf")
            # Open(FileName, ConfirmConversions, ReadOnly, AddToRecentFiles, PasswordDocument,
            # PasswordTemplate, Revert, WritePasswordDocument, WritePasswordTemplate, Format,
            # Encoding, Visible)
            $dokument = $word.Documents.Open(
                $txt, $false, $true, $false, $mangler, $mangler, $mangler, $mangler, $mangler,
                $wdOpenFormatEncodedText, $msoEncodingUTF8, $false
            )
            try {
                $dokument.SaveAs2($pdf, $wdFormatPDF)
            }
            finally {
                $dokument.Close($false)
            }
            Write-Output "Laget $($case.Name)\$([System.IO.Path]::GetFileName($pdf))"
        }
    }
}
finally {
    $word.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($word)
}
