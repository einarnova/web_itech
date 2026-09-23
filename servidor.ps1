param(
    [int]$Port = 8080,
    [switch]$NoBrowser
)

$HostName = "localhost"
$BaseDir = $PSScriptRoot

function Test-PortAvailable([int]$p) {
    try {
        $tcp = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Loopback, $p)
        $tcp.Start()
        $tcp.Stop()
        return $true
    } catch {
        return $false
    }
}

while (-not (Test-PortAvailable $Port)) {
    Write-Host "Puerto $Port ocupado, probando $(($Port + 1))..." -ForegroundColor Yellow
    $Port++
    if ($Port -gt 8100) { break }
}

$Prefix = "http://${HostName}:${Port}/"
$Listener = New-Object System.Net.HttpListener
$Listener.Prefixes.Add($Prefix)

try {
    $Listener.Start()
} catch {
    Write-Error "No se pudo iniciar el servidor en $Prefix : $_"
    exit 1
}

$MimeTypes = @{
    ".html" = "text/html; charset=utf-8"
    ".htm"  = "text/html; charset=utf-8"
    ".css"  = "text/css; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".json" = "application/json; charset=utf-8"
    ".xml"  = "application/xml; charset=utf-8"
    ".txt"  = "text/plain; charset=utf-8"
    ".png"  = "image/png"
    ".jpg"  = "image/jpeg"
    ".jpeg" = "image/jpeg"
    ".webp" = "image/webp"
    ".gif"  = "image/gif"
    ".svg"  = "image/svg+xml"
    ".ico"  = "image/x-icon"
    ".pdf"  = "application/pdf"
    ".woff" = "font/woff"
    ".woff2"= "font/woff2"
    ".ttf"  = "font/ttf"
}

Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  Servidor Web Local - ITECH" -ForegroundColor Green
Write-Host "  URL: $Prefix" -ForegroundColor Yellow
Write-Host "  Directorio: $BaseDir" -ForegroundColor Gray
Write-Host "  Presiona Ctrl+C para detener el servidor" -ForegroundColor Gray
Write-Host "=================================================" -ForegroundColor Cyan

if (-not $NoBrowser) {
    Start-Process $Prefix
}

while ($Listener.IsListening) {
    try {
        $Context = $Listener.GetContext()
        $Request = $Context.Request
        $Response = $Context.Response

        $UrlPath = [System.Uri]::UnescapeDataString($Request.Url.AbsolutePath)
        if ($UrlPath.EndsWith("/")) {
            $UrlPath += "index.html"
        }

        $RelativePath = $UrlPath.TrimStart("/").Replace("/", [System.IO.Path]::DirectorySeparatorChar)
        $FilePath = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($BaseDir, $RelativePath))

        if (-not $FilePath.StartsWith($BaseDir, [System.StringComparison]::OrdinalIgnoreCase)) {
            $Response.StatusCode = 403
            $Buffer = [System.Text.Encoding]::UTF8.GetBytes("403 Forbidden")
            $Response.ContentLength64 = $Buffer.Length
            $Response.OutputStream.Write($Buffer, 0, $Buffer.Length)
            $Response.Close()
            continue
        }

        if (Test-Path $FilePath -PathType Leaf) {
            $Ext = [System.IO.Path]::GetExtension($FilePath).ToLower()
            $ContentType = if ($MimeTypes.ContainsKey($Ext)) { $MimeTypes[$Ext] } else { "application/octet-stream" }
            $Response.ContentType = $ContentType

            $Bytes = [System.IO.File]::ReadAllBytes($FilePath)
            $Response.ContentLength64 = $Bytes.Length
            $Response.StatusCode = 200
            $Response.OutputStream.Write($Bytes, 0, $Bytes.Length)
            Write-Host "200 OK: $UrlPath" -ForegroundColor DarkGreen
        } elseif (Test-Path $FilePath -PathType Container) {
            $Response.Redirect($Request.Url.AbsolutePath + "/")
        } else {
            $Response.StatusCode = 404
            $Buffer = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found: $UrlPath")
            $Response.ContentLength64 = $Buffer.Length
            $Response.OutputStream.Write($Buffer, 0, $Buffer.Length)
            Write-Host "404 Not Found: $UrlPath" -ForegroundColor Red
        }

        $Response.Close()
    } catch {
        if (-not $Listener.IsListening) { break }
    }
}

$Listener.Close()
