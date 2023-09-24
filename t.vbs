Dim objExcel, objWorkbook
Dim strWorkbookPath, strFunctionName, strSearchKeyword, strCategory, strResult

' Set the workbook path
strWorkbookPath = "C:\SearchTool\SearchTool.xlsm"  ' Replace with the actual file path and name

' Set the function name and category
strFunctionName = "SearchRun"
strCategory = "Documents"

' Get the command line arguments
Set objArgs = WScript.Arguments
If objArgs.Count > 0 Then
    ' Use the first argument as the search keyword
    strSearchKeyword = objArgs(0)
    
    ' Check if Excel is already running
    On Error Resume Next
    Set objExcel = GetObject(, "Excel.Application")
    If Err.Number <> 0 Then
        ' Excel is not running, create a new instance
        Set objExcel = CreateObject("Excel.Application")
        objExcel.Visible = True
		msgbox "test here"
    End If
    On Error GoTo 0
    
    ' Check if the workbook is already open
    On Error Resume Next
    Set objWorkbook = objExcel.Workbooks(strWorkbookPath)
	msgbox "test here 2"
    ' Activate the workbook
    objWorkbook.Activate
    If Err.Number <> 0 Then
        ' Workbook is not open, open it
        Set objWorkbook = objExcel.Workbooks.Open(strWorkbookPath)
    End If
    On Error GoTo 0
    
    ' Display the result in the Excel worksheet (in cell A1 of the active sheet)
    objWorkbook.ActiveSheet.Cells(5,1).Value = strSearchKeyword

    strResult = objExcel.Run("'" & objWorkbook.Name & "'!" & strFunctionName)
	
	objWorkbook.Activate
	
	' Call the function and capture the returned value
    'strResult = objExcel.Run("'" & objWorkbook.Name & "'!" & strFunctionName, CStr(strSearchKeyword), CStr(strCategory))
    
    ' Display the result in the Excel worksheet (in cell A1 of the active sheet)
    'objWorkbook.ActiveSheet.Cells(5,1).Value = strSearchKeyword
    
    ' Save the workbook
    'objWorkbook.Save
    
    ' Clean up
    Set objWorkbook = Nothing
    Set objExcel = Nothing
End If
