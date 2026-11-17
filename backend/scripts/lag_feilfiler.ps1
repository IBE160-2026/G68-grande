# Lager feilfilene i testdata/feil/ (FR-10, FR-11, story 6.2).
#
# - skannet.pdf: CV-teksten fra case 1 tegnet som et bilde (System.Drawing), satt inn i Word og
#   lagret som PDF (format 17). PDF-en har bare bildet og ingen tekst, som en skannet CV, så
#   nettsiden gir «Vi klarer ikke å lese teksten i PDF-en».
# - feil-type.docx: Word åpner case-1-utvikler/cv.txt som UTF-8 og lagrer den som Word-fil
#   (format 16), så nettsiden gir «Feil filtype, prøv PDF».
#
# Bildet lagres som en midlertidig PNG og slettes til slutt. Testene i
# tests/adaptere/test_pdf_inn.py sjekker at skannet.pdf har under 50 bokstaver (MIN_BOKSTAVER_PDF),
# og tests/test_testdata.py at begge filene finnes.
#
# Trenger Microsoft Word på Windows. Kjøres fra backend/ i PowerShell:
#
#     powershell -ExecutionPolicy Bypass -File scripts\lag_feilfiler.ps1

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

$testdata = Join-Path (Split-Path -Parent $PSScriptRoot) "testdata"
$cv = Join-Path $testdata "case-1-utvikler\cv.txt"
$feil = Join-Path $testdata "feil"
# [string]: Word henger i SaveAs2 når stien er en PowerShell-streng fra Join-Path (prøvd
# 16. november 2026), men ikke med en vanlig .NET-streng.
[string]$skannet = Join-Path $feil "skannet.pdf"
[string]$docx = Join-Path $feil "feil-type.docx"
$png = Join-Path ([System.IO.Path]::GetTempPath()) "skannet-cv-$([guid]::NewGuid()).png"

# Konstanter fra Word: åpne som kodet tekst, UTF-8, lagre som PDF og som Word-fil (.docx).
$wdOpenFormatEncodedText = 5
$msoEncodingUTF8 = 65001
$wdFormatPDF = 17
$wdFormatDocumentDefault = 16
$mangler = [Type]::Missing

New-Item -ItemType Directory -Force -Path $feil | Out-Null

# CV-teksten tegnet på et hvitt A4-ark i 150 dpi (1240 x 1754 punkter), med 100 punkter marg.
$tekst = [System.IO.File]::ReadAllText($cv, [System.Text.Encoding]::UTF8)
$bilde = New-Object System.Drawing.Bitmap 1240, 1754
$bilde.SetResolution(150, 150)
$tegner = [System.Drawing.Graphics]::FromImage($bilde)
$skrift = New-Object System.Drawing.Font "Arial", 10
try {
    $tegner.Clear([System.Drawing.Color]::White)
    $tegner.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAlias
    $flate = New-Object System.Drawing.RectangleF 100, 100, 1040, 1554
    $tegner.DrawString($tekst, $skrift, [System.Drawing.Brushes]::Black, $flate)
    $bilde.Save($png, [System.Drawing.Imaging.ImageFormat]::Png)
}
finally {
    $skrift.Dispose()
    $tegner.Dispose()
    $bilde.Dispose()
}

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    # skannet.pdf: et tomt dokument med bare bildet, like bredt som teksten på siden.
    $dokument = $word.Documents.Add()
    try {
        $bildet = $dokument.InlineShapes.AddPicture($png)
        $bildet.LockAspectRatio = -1
        $oppsett = $dokument.PageSetup
        $bildet.Width = $oppsett.PageWidth - $oppsett.LeftMargin - $oppsett.RightMargin
        $dokument.SaveAs2($skannet, $wdFormatPDF)
    }
    finally {
        $dokument.Close($false)
    }
    Write-Output "Laget feil\skannet.pdf"

    # feil-type.docx: cv.txt lagret som Word-fil.
    # Open(FileName, ConfirmConversions, ReadOnly, AddToRecentFiles, PasswordDocument,
    # PasswordTemplate, Revert, WritePasswordDocument, WritePasswordTemplate, Format,
    # Encoding, Visible)
    $dokument = $word.Documents.Open(
        $cv, $false, $true, $false, $mangler, $mangler, $mangler, $mangler, $mangler,
        $wdOpenFormatEncodedText, $msoEncodingUTF8, $false
    )
    try {
        $dokument.SaveAs2($docx, $wdFormatDocumentDefault)
    }
    finally {
        $dokument.Close($false)
    }
    Write-Output "Laget feil\feil-type.docx"
}
finally {
    $word.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($word)
    Remove-Item -Path $png -Force -ErrorAction SilentlyContinue
}
