using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Threading;
using System.Threading.Tasks;
//using System.Windows.Forms;
//using System.Windows.Controls;


namespace GraphicFilesInfo
{
    /// <summary>
    /// Логика взаимодействия для MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private static readonly HashSet<string> ImageExtensions = new HashSet<string>
        {
            ".jpg", ".tiff", ".gif", ".bmp", ".png" ,".pcx"
        };

        private static readonly Dictionary<long, string> CompressionTypes = new Dictionary<long, string>()
        {
            {1, "Uncompressed"},
            {2, "CCITT modified Huffman RLE"},
            {32773, "PackBits"},
            {3, "CCITT3"},
            {4, "CCITT4"},
            {5, "LZW"},
            {6, "JPEG_old"},
            {7, "JPEG_new"},
            {32946, "DeflatePKZIP"},
            {8, "DeflateAdobe"},
            {9, "JBIG_85"},
            {10, "JBIG_43"},
            {11, "JPEG"},
            {12, "JPEG"},
            {32766, "RLE_NeXT"},
            {32809, "RLE_ThunderScan"},
            {32895, "RasterPadding"},
            {32896, "RLE_LW"},
            {32897, "RLE_HC"},
            {32947, "RLE_BL"},
            {34661, "JBIG"},
            {34713, "Nikon_NEF"},
            {34712, "JPEG2000"}
        };

        public MainWindow()
        {
            InitializeComponent();

            string[] col = { "Name", "Size", "Resolution", "ColorDepth", "Compression" };
            for (int i = 0; i < col.Length; i++)
            {
                var column = new DataGridTextColumn();
                column.Header = col[i];
                column.Binding = new Binding(col[i]);
                dataImages.Columns.Add(column);
            }
        }

        private async void btnOpenFile_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Multiselect = true;
            openFileDialog.Filter = "Image files (*.jpg;*.jpeg;*.gif;*.tif;*.bmp;*.png;*.pcx)|*.jpg;*.jpeg;*.gif;*.tif;*.bmp;*.png;*.pcx|All files (*.*)|*.*";

            if (openFileDialog.ShowDialog() == true)
            {
                dataImages.Items.Clear();
                await Task.Run(() => { 
                    foreach (string filename in openFileDialog.FileNames)
                    {
                        FileInfo file = new FileInfo(filename);
                        if (file.Extension == ".pcx")
                        {
                            SetPcxInfo(file.FullName);
                        }
                        else
                        {
                            SetInfo(filename);
                        }
                    }
                });
            }
        }

        private void btnOpenFolder_Click(object sender, RoutedEventArgs e)
        {
            var dialog = new System.Windows.Forms.FolderBrowserDialog();
            dialog.ShowNewFolderButton = false;

            if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                DirectoryInfo directory = new DirectoryInfo(dialog.SelectedPath);
                FileInfo[] files = directory.GetFiles("*.*")
                    .Where(file => ImageExtensions.Contains(file.Extension.ToLower()))
                    .ToArray();

                dataImages.Items.Clear();
                foreach (var file in files)
                {
                    if (file.Extension == ".pcx")
                    {
                        SetPcxInfo(file.FullName);
                    }
                    else
                    {
                        SetInfo(file.FullName);
                    }
                }
            }
        }

        private void SetInfo(string filename)
        {
            Bitmap bitmap = new Bitmap(filename);
            int id;
            string compression = "undefined";

            try
            {
                id = BitConverter.ToInt16(bitmap.GetPropertyItem(0x0103).Value, 0);
                CompressionTypes.TryGetValue(id, out compression);
            }
            catch { }

            Dispatcher.Invoke(() =>
            {
                dataImages.Items.Add(new DataItem
                {
                    Name = filename,
                    Size = bitmap.Width + "x" + bitmap.Height,
                    Resolution = Math.Round(bitmap.HorizontalResolution) + "x" + Math.Round(bitmap.VerticalResolution),
                    ColorDepth = GetColorDepth(bitmap.PixelFormat).ToString(),
                    Compression = compression
                });
            });

            bitmap.Dispose();
        }

        public void SetPcxInfo(string filename)
        {
            BinaryReader myFile;
            myFile = new BinaryReader(File.Open(filename, FileMode.Open));

            byte mark = myFile.ReadByte();
            if (mark != 10)
                return;

            myFile.BaseStream.Seek(2, SeekOrigin.Begin);
            mark = myFile.ReadByte();
            byte bitsPerPlane = myFile.ReadByte();

            short xMin = myFile.ReadInt16();
            short yMin = myFile.ReadInt16();
            short xMax = myFile.ReadInt16();
            short yMax = myFile.ReadInt16();

            short resolutionX = myFile.ReadInt16();
            short resolutionY = myFile.ReadInt16();

            myFile.BaseStream.Seek(65, SeekOrigin.Begin);
            byte colorPlanes = myFile.ReadByte();

            Dispatcher.Invoke(() =>
            {
                dataImages.Items.Add(new DataItem
                {
                    Name = filename,
                    Size = (xMax - xMin + 1) + "x" + (yMax - yMin + 1),
                    Resolution = resolutionX + "x" + resolutionY,
                    ColorDepth = (colorPlanes * bitsPerPlane).ToString(),
                    Compression = mark == 1 ? "RLE" : "No compression"
                });
            });

            myFile.Close();
        }

        public static int GetColorDepth(PixelFormat pixelFormat)
        {
            switch (pixelFormat)
            {
                case PixelFormat.Format1bppIndexed:
                    return 1;
                case PixelFormat.Format4bppIndexed:
                    return 4;
                case PixelFormat.Format8bppIndexed:
                    return 8;
                case PixelFormat.Format16bppGrayScale:
                case PixelFormat.Format16bppRgb555:
                case PixelFormat.Format16bppRgb565:
                case PixelFormat.Format16bppArgb1555:
                    return 16;
                case PixelFormat.Format24bppRgb:
                    return 24;
                case PixelFormat.Format32bppRgb:
                case PixelFormat.Format32bppArgb:
                case PixelFormat.Format32bppPArgb:
                    return 32;
                case PixelFormat.Format48bppRgb:
                    return 48;
                case PixelFormat.Format64bppArgb:
                case PixelFormat.Format64bppPArgb:
                    return 64;
                default:
                    throw new ArgumentOutOfRangeException();
            }

        }

        
    }
}
