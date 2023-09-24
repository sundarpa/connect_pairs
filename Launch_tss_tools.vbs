Function OpenOrCloseExcelWorkbook(strWorkbookPath, openOrClose)
    Dim objExcel, objWorkbook

    ' Check if Excel is already running
    On Error Resume Next
    Set objExcel = GetObject(, "Excel.Application")
    If Err.Number <> 0 Then
        ' Excel is not running, create a new instance
        Set objExcel = CreateObject("Excel.Application")
        objExcel.Visible = True
    End If
    On Error GoTo 0

    ' Check if the workbook is already open
    On Error Resume Next
    Set objWorkbook = objExcel.Workbooks(strWorkbookPath)

    If openOrClose = "open" Then
        If Err.Number <> 0 Then
            ' Workbook is not open, open it
            Set objWorkbook = objExcel.Workbooks.Open(strWorkbookPath)
        Else
            ' Workbook is already open, bring it to the front
            objExcel.AppActivate strWorkbookPath
        End If
    ElseIf openOrClose = "close" Then
        If Err.Number = 0 Then
            ' Workbook is open, close it
            objWorkbook.Saved = True
            objWorkbook.Close False
        End If
    End If

    On Error GoTo 0

    ' Clean up
    Set objWorkbook = Nothing
    Set objExcel = Nothing
End Function

' Example usage:

' To open the workbook if it's not open and bring it to the front:
OpenOrCloseExcelWorkbook "C:\SearchTool\SearchTool.xlsm", "open"

' To close the workbook if it's open:
' OpenOrCloseExcelWorkbook "C:\SearchTool\SearchTool.xlsm", "close"

' To do nothing if the workbook is not open:
' OpenOrCloseExcelWorkbook "C:\SearchTool\SearchTool.xlsm", "do nothing"
