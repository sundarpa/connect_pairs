Function OpenOrCloseExcelWorkbook(strWorkbookPath, action)
    On Error Resume Next
    Set objExcel = GetObject(, "Excel.Application")
    If Err.Number <> 0 Then Set objExcel = CreateObject("Excel.Application"): objExcel.Visible = True
    
    Set objWorkbook = objExcel.Workbooks("SearchTool.xlsm")

    Select Case action
        Case "open"
			'If Not objWorkbook Is Nothing Then objExcel.AppActivate objWorkbook.Name
			If objWorkbook Is Nothing Then Set objWorkbook = objExcel.Workbooks.Open(strWorkbookPath)
        Case "close"
			If objWorkbook Is Nothing Then 
			else
				objWorkbook.Close False: objExcel.Quit
			End if
    End Select

    Set objWorkbook = Nothing
    Set objExcel = Nothing
End Function

' To open the workbook if it's not open and bring it to the front:
OpenOrCloseExcelWorkbook "C:\SearchTool\SearchTool.xlsm", "open"
