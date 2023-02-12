# Process
## #1. Created a CSV File with Spring 2023 Classes
Downloaded a pdf of all Spring 2023 classes. The formatting of this data made it unusable. Thus, it was opened and transformed into a usable csv file in Excel with the following VBA script

```
Sub CleanWorksheet()
    
    'Format the output sheet on All Stocks Analysis worksheet
    Worksheets("Cleaned").Activate
    
    Range("A1").Value = "Cleaned Semester Data"
    
    'Create a header row
    Cells(3, 1).Value = "Subject"
    Cells(3, 2).Value = "Catalog Nbr"
    Cells(3, 3).Value = "Section"
    Cells(3, 4).Value = "Class Nbr"
    Cells(3, 5).Value = "Course Title"
    Cells(3, 6).Value = "Component"
    Cells(3, 7).Value = "Units"
    Cells(3, 8).Value = "Bldg"
    Cells(3, 9).Value = "Room"
    Cells(3, 10).Value = "Days"
    Cells(3, 11).Value = "Time"
    Cells(3, 12).Value = "Instructor"
    Cells(3, 13).Value = "Attributes"
    
    'Activate data worksheet
    Worksheets("Test").Activate
    
    'Get the number of rows to loop over
    RowCount = Cells(Rows.Count, "A").End(xlUp).Row
    
    'Initialize array of all subjects and catalong numbers
    Dim subject(87000) As String
    Dim catalog_nbr(87000) As String
    Dim section(87000) As String
    Dim class_nbr(87000) As String
    Dim course_title(87000) As String
    Dim component(87000) As String
    Dim units(87000) As String
    Dim bldg(87000) As String
    Dim room(87000) As String
    Dim days(87000) As String
    Dim time(87000) As String
    Dim instructor(87000) As String
    Dim attributes(87000) As String
    Count = 0
    
    'Loop over all the rows in the spreadsheet.
    For i = 1 To RowCount:
    'Retrieve subject, catalog_nbr, section, class_nbr.
        If ((Len(Cells(i, 1).Value) = 4 Or Cells(i, 1).Value = "HPM" Or Cells(i, 1).Value = "BCS" Or Cells(i, 1).Value = "BCB") And Cells(i, 1).Value <> "INST" And Cells(i, 1).Value <> "DEAN") Then
            subject(Count) = Cells(i, 1).Value
            catalog_nbr(Count) = Cells(i, 2).Value
            section(Count) = Cells(i, 3).Value
            class_nbr(Count) = Cells(i, 4).Value
            'Retrieve units, component, course title.
            TitleText = Cells(i, 5).Value
            If IsEmpty(Cells(i, 7).Value) Then
                units(Count) = Cells(i, 6).Value
                If InStr(1, TitleText, "Lecture") > 0 Then
                    component(Count) = "Lecture"
                    course_title(Count) = Replace(TitleText, "Lecture", "")
                Else
                    If InStr(1, TitleText, "Recitation") > 0 Then
                        component(Count) = "Recitation"
                        course_title(Count) = Replace(TitleText, "Recitation", "")
                    Else
                        If InStr(1, TitleText, "Lab") > 0 Then
                            component(Count) = "Lab"
                            course_title(Count) = Replace(TitleText, "Lab", "")
                        Else
                            If InStr(1, TitleText, "Clinical") > 0 Then
                            component(Count) = "Clinical"
                            course_title(Count) = Replace(TitleText, "Clinical", "")
                            Else
                                If InStr(1, TitleText, "Field Work") > 0 Then
                                component(Count) = "Field Work"
                                course_title(Count) = Replace(TitleText, "Field Work", "")
                                End If
                            End If
                        End If
                    End If
                End If
            Else
                course_title(Count) = TitleText
                component(Count) = Cells(i, 6).Value
                units(Count) = Cells(i, 7).Value
            End If
            'Fix date formatting of units with ranges.
            UnitsText = units(Count)
            If InStr(1, UnitsText, "/") > 0 Then
                UnitsText = Replace(UnitsText, "/", " - ")
                units(Count) = Replace(UnitsText, " - 2023", "")
            End If
            'Retrieve room and building.
            BldgText = Cells(i + 2, 2).Value
            If InStr(1, BldgText, "Bldg:") > 0 Then
                    If InStr(1, BldgText, "Room:") > 0 Then
                        BldgText = Replace(BldgText, "Room: ", "@")
                        RoomText = BldgText
                        room(Count) = Right(RoomText, Len(RoomText) - InStr(RoomText, "@"))
                        BldgText = Left(BldgText, InStr(BldgText, "@") - 1)
                        DaysText = Cells(i + 2, 3).Value
                        TimeText = Cells(i + 2, 4).Value
                    Else
                        RoomText = Cells(i + 2, 3).Value
                        DaysText = Cells(i + 2, 4).Value
                        TimeText = Cells(i + 2, 5).Value
                    End If
                bldg(Count) = Replace(BldgText, "Bldg: ", "")
            End If
            If InStr(1, RoomText, "Room:") > 0 Then
                room(Count) = Replace(RoomText, "Room: ", "")
            End If
            'Retrieve days and times.
            If InStr(1, DaysText, "Days:") > 0 Then
                days(Count) = Replace(DaysText, "Days: ", "")
            End If
            If InStr(1, TimeText, "Time:") > 0 Then
                time(Count) = Replace(TimeText, "Time: ", "")
            End If
            'Retrieve instructor.
            If Cells(i + 3, 4).Value = "INST" Or Cells(i + 3, 4).Value = "GA" Or Cells(i + 3, 4).Value = "TA" Then
                InstructorText = Cells(i + 3, 5).Value
            Else
                InstructorText = Cells(i + 3, 3).Value
                If InstructorText = 100 Then
                    InstructorText = Cells(i + 3, 4).Value
                End If
            End If
            If InStr(1, InstructorText, "Instructor:") > 0 Then
                InstructorText = Replace(InstructorText, "Instructor:", "")
                For j = 0 To 9
                    InstructorText = Replace(InstructorText, j, "")
                Next j
                instructor(Count) = LTrim(Replace(InstructorText, "Class Enrl Cap:", ""))
            End If
            'Retrieve attributes.
            AttributesText = Cells(i + 5, 1).Value
            If InStr(1, AttributesText, "Attributes:") > 0 Then
                attributes(Count) = Replace(AttributesText, "Attributes: ", "")
            Else
                AttributesText = Cells(i + 6, 1).Value
                If InStr(1, AttributesText, "Attributes:") > 0 Then
                    attributes(Count) = Replace(AttributesText, "Attributes: ", "")
                End If
            End If
            'Increase count.
            Count = Count + 1
        End If
    Next i
    
'Loop through your arrays to output the subject.
    Worksheets("Cleaned").Activate
    For i = 0 To Count
        Cells(4 + i, 1).Value = subject(i)
        Cells(4 + i, 2).Value = catalog_nbr(i)
        Cells(4 + i, 3).Value = section(i)
        Cells(4 + i, 4).Value = class_nbr(i)
        Cells(4 + i, 5).Value = course_title(i)
        Cells(4 + i, 6).Value = component(i)
        Cells(4 + i, 7).Value = units(i)
        Cells(4 + i, 8).Value = bldg(i)
        Cells(4 + i, 9).Value = room(i)
        Cells(4 + i, 10).Value = days(i)
        Cells(4 + i, 11).Value = time(i)
        Cells(4 + i, 12).Value = instructor(i)
        Cells(4 + i, 13).Value = attributes(i)
    Next i
    
'Put in TBA dates and times.
    For i = 0 To Count
        If IsEmpty(Cells(4 + i, 10).Value) Then
            Cells(4 + i, 10).Value = "TBA"
        End If
        If IsEmpty(Cells(4 + i, 11).Value) Then
            Cells(4 + i, 11).Value = "TBA"
        End If
    Next i
        
'Formatting
    Worksheets("Cleaned").Activate
    Range("A3:M3").Font.FontStyle = "Bold"
    Range("A3:M3").Borders(xlEdgeBottom).LineStyle = xlContinuous
    Columns("E").AutoFit
    
End Sub
```

## #2. Website Design
Wireframed and developped a protype website for a final submission.

https://xd.adobe.com/view/9c9732e9-0f59-4be7-8945-85cb2d86df11-c9c4/
