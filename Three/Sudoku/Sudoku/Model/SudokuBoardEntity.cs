using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Sudoku.Model
{
    internal class SudokuBoardEntity
    {
        public int[,] Grid { get; }

        public SudokuBoardEntity()
        {
            Grid = new[,]
            {
                {0, 0, 0, 0},
                {0, 0, 0, 0},
                {0, 0, 0, 0},
                {0, 0, 0, 0}
            };
        }
    }
}