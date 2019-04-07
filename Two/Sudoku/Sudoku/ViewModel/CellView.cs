using System.ComponentModel;
using System.Runtime.CompilerServices;
using Sudoku.Annotations;

namespace Sudoku.ViewModel
{
    /// <inheritdoc />
    /// <summary>
    /// Represents a view of a cell on a sudoku board
    /// </summary>
    internal class CellView : INotifyPropertyChanged
    {
        /// <summary>
        /// A number which is stored in a cell
        /// </summary>
        public int? Number
        {
            get => _number;
            set
            {
                if (_number == value) return;
                _number = value;
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs("Number"));
            }
        }

        private int? _number;

        public CellView(int number)
        {
            _number = number;
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