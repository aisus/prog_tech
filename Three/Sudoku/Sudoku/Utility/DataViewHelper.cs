﻿using System.Data;
using Sudoku.Utility;

public static class DataViewHelper
{
    public static DataView GetBindable2DArray<T>(T[,] array)
    {
        DataTable dataTable = new DataTable();
        for (int i = 0; i < array.GetLength(1); i++)
        {
            dataTable.Columns.Add(i.ToString(), typeof(Ref<T>));
        }

        for (int i = 0; i < array.GetLength(0); i++)
        {
            DataRow dataRow = dataTable.NewRow();
            dataTable.Rows.Add(dataRow);
        }

        DataView dataView = new DataView(dataTable);
        for (int i = 0; i < array.GetLength(0); i++)
        {
            for (int j = 0; j < array.GetLength(1); j++)
            {
                int a = i;
                int b = j;
                Ref<T> refT = new Ref<T>(() => array[a, b], z => { array[a, b] = z; });
                dataView[i][j] = refT;
            }
        }

        return dataView;
    }
}