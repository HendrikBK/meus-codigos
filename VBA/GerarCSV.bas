Attribute VB_Name = "GerarCSV"
Sub GerarCSV()

    If Dir(Range("G3").Value, vbDirectory) <> Empty Then
    
        Open Range("G3").Value & "\livro-caixa.csv" For Output As 1
        
        Dim dia As String
        Dim mes As String
        Dim ano As String
               
        If Len(Range("F2").Value) = 1 Then
            mes = "0" & Range("F2").Value
        Else
            mes = Range("F2")
        End If
            
        If Len(Range("F3").Value) = 1 Then
            ano = "0" & Range("F3").Value
        Else
            ano = Range("F3").Value
        End If
        
        
        Dim date_concat As String
        
        date_concat = "/" & mes & "/" & ano
    
        Range("A6").Select
        
        Do While ActiveCell.Value <> ""
            If Len(ActiveCell.Value) = 1 Then
                dia = "0" & ActiveCell.Value
            Else
                dia = ActiveCell.Value
            End If
            Print #1, dia & date_concat & ";" & Cells(ActiveCell.Row, 2).Value & ";" & Cells(ActiveCell.Row, 3).Value & ";" & Cells(ActiveCell.Row, 4).Value
            Cells(ActiveCell.Row + 1, ActiveCell.Column).Select
        Loop
        
        MsgBox "Arquivo gerado com sucesso!", vbInformation, "Sucesso"
    
        Close 1
    Else
        MsgBox "Diretório " & Range("G3").Value & " da célula K9 não existe ou é inválido!"
        End
    End If

End Sub
