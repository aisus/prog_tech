using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;

namespace Sudoku
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            int[,] array = {
                {0,0,0,0},
                {0,0,0,0},
                {0,0,0,0},
                {0,0,0,0}
            };

            InitializeComponent();

            CDataGrid.ItemsSource = DataViewHelper.GetBindable2DArray(array);
            CDataGrid.CellEditEnding += delegate { MessageBox.Show("Pydor");};
        }

        private void c_dataGrid_AutoGeneratingColumn(object sender, DataGridAutoGeneratingColumnEventArgs e)
        {
            DataGridTextColumn column = e.Column as DataGridTextColumn;
            if (column?.Binding is Binding binding) binding.Path = new PropertyPath(binding.Path.Path + ".Value");
        }
    }
}
