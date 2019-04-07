using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using Sudoku.Annotations;
using Sudoku.Controller;
using Sudoku.Model;

namespace Sudoku.ViewModel
{
    /// <inheritdoc />
    /// <summary>
    /// Represents a view of the sudoku board with cells
    /// </summary>
    internal class SudokuBoardView : INotifyPropertyChanged
    {
        /// <summary>
        /// Sudoku board cells with numbers
        /// </summary>
        public ObservableCollection<ObservableCollection<CellView>> Cells { get; }

        /// <summary>
        /// Game controller callback
        /// </summary>
        private SudokuController _controller;

        public SudokuBoardView(SudokuBoardEntity entity, SudokuController controller)
        {
            _controller = controller;

            Cells = new ObservableCollection<ObservableCollection<CellView>>();

            // Populating the board with values from SudokuBoardEntity
            var grid = entity.Grid;
            for (int i = 0; i < grid.GetLength(0); i++)
            {
                var row = new ObservableCollection<CellView>();
                for (int j = 0; j < grid.GetLength(1); j++)
                {
                    var cell = new CellView(grid[i, j]);
                    // Whenever the cell value is modified, we handle it
                    cell.PropertyChanged += CellChangedHandler;
                    row.Add(cell);
                }
                Cells.Add(row);
            }
        }

        private void CellChangedHandler(object sender, PropertyChangedEventArgs args)
        {
            if (args.PropertyName.Equals("Number"))
            {
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs("Number"));
            }
        }

        #region Implementation of INotifyPropertyChanged

        public event PropertyChangedEventHandler PropertyChanged;

        [NotifyPropertyChangedInvocator]
        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

        #endregion
    }
}