Dim objExcel, objWorkbook
Dim strWorkbookPath

' Set the workbook path
strWorkbookPath = "C:\SearchTool\SearchTool.xlsm"  ' Replace with the actual file path and name


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
    ' Activate the workbook
    objWorkbook.Activate
    If Err.Number <> 0 Then
        ' Workbook is not open, open it
        Set objWorkbook = objExcel.Workbooks.Open(strWorkbookPath)
    End If
    On Error GoTo 0
	
	objWorkbook.Activate
	
	'objWorkbook.Saved = False
	'objWorkbook.Close False
	
    ' Clean up
    Set objWorkbook = Nothing
    Set objExcel = Nothing
