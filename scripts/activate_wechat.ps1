Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")]
    public static extern bool IsIconic(IntPtr hWnd);
    public const int SW_RESTORE = 9;
}
"@

$wechat = Get-Process WeChatAppEx -ErrorAction SilentlyContinue | Select-Object -First 1
if ($wechat) {
    $hwnd = $wechat.MainWindowHandle
    if ($hwnd -ne 0) {
        Write-Host "Found window handle: $hwnd"
        if ([Win32]::IsIconic($hwnd)) {
            [Win32]::ShowWindow($hwnd, 9) | Out-Null
        }
        [Win32]::SetForegroundWindow($hwnd) | Out-Null
        Write-Host "Window activated"
    } else {
        Write-Host "No window handle"
    }
}
