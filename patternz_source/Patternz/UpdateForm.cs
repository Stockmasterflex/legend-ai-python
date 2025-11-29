using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Microsoft.VisualBasic.Devices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class UpdateForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StartButton")]
	private Button _StartButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StopButton")]
	private Button _StopButton;

	[CompilerGenerated]
	[AccessedThroughProperty("SymbolTextBox")]
	private TextBox _SymbolTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("AllButton")]
	private Button _AllButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ListBox1")]
	private ListBox _ListBox1;

	[CompilerGenerated]
	[AccessedThroughProperty("HelpButton1")]
	private Button _HelpButton1;

	[CompilerGenerated]
	[AccessedThroughProperty("BrowseButton")]
	private Button _BrowseButton;

	[CompilerGenerated]
	[AccessedThroughProperty("HistoricalRadioButton")]
	private RadioButton _HistoricalRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("UpdateRadioButton")]
	private RadioButton _UpdateRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("AllPortsButton")]
	private Button _AllPortsButton;

	[CompilerGenerated]
	[AccessedThroughProperty("APIKeyTextBox")]
	private TextBox _APIKeyTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("TiingoRadioButton")]
	private RadioButton _TiingoRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("TiingoHelpButton")]
	private Button _TiingoHelpButton;

	[CompilerGenerated]
	[AccessedThroughProperty("RetryButton")]
	private Button _RetryButton;

	[CompilerGenerated]
	[AccessedThroughProperty("Timer1")]
	private Timer _Timer1;

	[CompilerGenerated]
	[AccessedThroughProperty("FinnhubRB")]
	private RadioButton _FinnhubRB;

	[CompilerGenerated]
	[AccessedThroughProperty("BarchartRB")]
	private RadioButton _BarchartRB;

	[CompilerGenerated]
	[AccessedThroughProperty("IEXRadioButton")]
	private RadioButton _IEXRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("IEXButton")]
	private Button _IEXButton;

	[CompilerGenerated]
	[AccessedThroughProperty("BarChartButton")]
	private Button _BarChartButton;

	[CompilerGenerated]
	[AccessedThroughProperty("FinnhubButton")]
	private Button _FinnhubButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ReplaceQuoteButton")]
	private Button _ReplaceQuoteButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StockDataHelpButton")]
	private Button _StockDataHelpButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StockDataRB")]
	private RadioButton _StockDataRB;

	[CompilerGenerated]
	[AccessedThroughProperty("EODHDButton")]
	private Button _EODHDButton;

	[CompilerGenerated]
	[AccessedThroughProperty("UnibitButton")]
	private Button _UnibitButton;

	[CompilerGenerated]
	[AccessedThroughProperty("UnibitRB")]
	private RadioButton _UnibitRB;

	[CompilerGenerated]
	[AccessedThroughProperty("EodhdRB")]
	private RadioButton _EodhdRB;

	private readonly string IEXWarning;

	private const int SYMBOLONLY = 0;

	private const int FULLSYMBOL = 1;

	private const int SYMBOLOPATH = 2;

	private const int SYMBOLMAX = 2;

	private string[,] SymbolArray;

	private const string KEYUT = "FrmLngth";

	private const string KEYQT = "Capton";

	private const int ASCEND = 1;

	private const int DESCEND = 2;

	private bool StopPressed;

	private string RecentLine;

	private string FileDelimiter;

	private bool Quiet;

	private bool UpdateAllPorts;

	private bool RetryChecked;

	private int AutoStart;

	private int RetryEngagedCounter;

	private bool StopAsking;

	private bool TimerRunFlag;

	private string LocalBuffer;

	internal virtual Button DoneButton
	{
		[CompilerGenerated]
		get
		{
			return _DoneButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DoneButton_Click;
			Button val = _DoneButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_DoneButton = value;
			val = _DoneButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button StartButton
	{
		[CompilerGenerated]
		get
		{
			return _StartButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = StartButton_Click;
			Button val = _StartButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_StartButton = value;
			val = _StartButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button StopButton
	{
		[CompilerGenerated]
		get
		{
			return _StopButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = StopButton_Click;
			Button val = _StopButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_StopButton = value;
			val = _StopButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("SymbolLabel")]
	internal virtual Label SymbolLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual TextBox SymbolTextBox
	{
		[CompilerGenerated]
		get
		{
			return _SymbolTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SymbolTextBox_TextChanged;
			TextBox val = _SymbolTextBox;
			if (val != null)
			{
				((Control)val).TextChanged -= eventHandler;
			}
			_SymbolTextBox = value;
			val = _SymbolTextBox;
			if (val != null)
			{
				((Control)val).TextChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label3")]
	internal virtual Label Label3
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label2")]
	internal virtual Label Label2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button AllButton
	{
		[CompilerGenerated]
		get
		{
			return _AllButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = AllButton_Click;
			Button val = _AllButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_AllButton = value;
			val = _AllButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual ListBox ListBox1
	{
		[CompilerGenerated]
		get
		{
			return _ListBox1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0007: Unknown result type (might be due to invalid IL or missing references)
			//IL_000d: Expected O, but got Unknown
			KeyEventHandler val = new KeyEventHandler(ListBox1_KeyUp);
			ListBox val2 = _ListBox1;
			if (val2 != null)
			{
				((Control)val2).KeyUp -= val;
			}
			_ListBox1 = value;
			val2 = _ListBox1;
			if (val2 != null)
			{
				((Control)val2).KeyUp += val;
			}
		}
	}

	[field: AccessedThroughProperty("Label4")]
	internal virtual Label Label4
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button HelpButton1
	{
		[CompilerGenerated]
		get
		{
			return _HelpButton1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = HelpButton1_Click;
			Button val = _HelpButton1;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_HelpButton1 = value;
			val = _HelpButton1;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("ProgressBar1")]
	internal virtual ProgressBar ProgressBar1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button BrowseButton
	{
		[CompilerGenerated]
		get
		{
			return _BrowseButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BrowseButton_Click;
			Button val = _BrowseButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_BrowseButton = value;
			val = _BrowseButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("FolderBrowserDialog1")]
	internal virtual FolderBrowserDialog FolderBrowserDialog1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton HistoricalRadioButton
	{
		[CompilerGenerated]
		get
		{
			return _HistoricalRadioButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = HistoricalRadioButton_CheckedChanged;
			RadioButton val = _HistoricalRadioButton;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_HistoricalRadioButton = value;
			val = _HistoricalRadioButton;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual RadioButton UpdateRadioButton
	{
		[CompilerGenerated]
		get
		{
			return _UpdateRadioButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = UpdateRadioButton_CheckedChanged;
			RadioButton val = _UpdateRadioButton;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_UpdateRadioButton = value;
			val = _UpdateRadioButton;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("ErrorListBox")]
	internal virtual ListBox ErrorListBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("GoogleRadioButton")]
	internal virtual RadioButton GoogleRadioButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("GroupBox1")]
	internal virtual GroupBox GroupBox1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button AllPortsButton
	{
		[CompilerGenerated]
		get
		{
			return _AllPortsButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = AllPortsButton_Click;
			Button val = _AllPortsButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_AllPortsButton = value;
			val = _AllPortsButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("QuandlRadioButton")]
	internal virtual RadioButton QuandlRadioButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label5")]
	internal virtual Label Label5
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label1")]
	internal virtual Label Label1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual TextBox APIKeyTextBox
	{
		[CompilerGenerated]
		get
		{
			return _APIKeyTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = APIKeyTextBox_LostFocus;
			EventHandler eventHandler2 = APIKeyTextBox_TextChanged;
			TextBox val = _APIKeyTextBox;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
				((Control)val).TextChanged -= eventHandler2;
			}
			_APIKeyTextBox = value;
			val = _APIKeyTextBox;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
				((Control)val).TextChanged += eventHandler2;
			}
		}
	}

	[field: AccessedThroughProperty("QuandlComboBox")]
	internal virtual ComboBox QuandlComboBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("QuandlHelpButton")]
	internal virtual Button QuandlHelpButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("FromDatePicker")]
	internal virtual DateTimePicker FromDatePicker
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("ToDatePicker")]
	internal virtual DateTimePicker ToDatePicker
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton TiingoRadioButton
	{
		[CompilerGenerated]
		get
		{
			return _TiingoRadioButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = TiingoRadioButton_CheckedChanged;
			RadioButton val = _TiingoRadioButton;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_TiingoRadioButton = value;
			val = _TiingoRadioButton;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual Button TiingoHelpButton
	{
		[CompilerGenerated]
		get
		{
			return _TiingoHelpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = TiingoHelpButton_Click;
			Button val = _TiingoHelpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_TiingoHelpButton = value;
			val = _TiingoHelpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("RetryListBox")]
	internal virtual ListBox RetryListBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button RetryButton
	{
		[CompilerGenerated]
		get
		{
			return _RetryButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = RetryButton_Click;
			Button val = _RetryButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_RetryButton = value;
			val = _RetryButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label6")]
	internal virtual Label Label6
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label7")]
	internal virtual Label Label7
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("YahooRadioButton")]
	internal virtual RadioButton YahooRadioButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("AlphaVantageRadioButton")]
	internal virtual RadioButton AlphaVantageRadioButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Panel1")]
	internal virtual Panel Panel1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("AlphaVHelpButton")]
	internal virtual Button AlphaVHelpButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("AutoRetryCheckBox")]
	internal virtual CheckBox AutoRetryCheckBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Timer Timer1
	{
		[CompilerGenerated]
		get
		{
			return _Timer1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = Timer1_Tick;
			Timer val = _Timer1;
			if (val != null)
			{
				val.Tick -= eventHandler;
			}
			_Timer1 = value;
			val = _Timer1;
			if (val != null)
			{
				val.Tick += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label8")]
	internal virtual Label Label8
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("NumericUpDown1")]
	internal virtual NumericUpDown NumericUpDown1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("TimeSeriesPanel")]
	internal virtual Panel TimeSeriesPanel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RB60")]
	internal virtual RadioButton RB60
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RB30")]
	internal virtual RadioButton RB30
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RB15")]
	internal virtual RadioButton RB15
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RB5")]
	internal virtual RadioButton RB5
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RB1")]
	internal virtual RadioButton RB1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBDaily")]
	internal virtual RadioButton RBDaily
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton FinnhubRB
	{
		[CompilerGenerated]
		get
		{
			return _FinnhubRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = FinnhubRB_CheckedChanged;
			RadioButton val = _FinnhubRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_FinnhubRB = value;
			val = _FinnhubRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual RadioButton BarchartRB
	{
		[CompilerGenerated]
		get
		{
			return _BarchartRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BarchartRB_CheckedChanged;
			RadioButton val = _BarchartRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_BarchartRB = value;
			val = _BarchartRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual RadioButton IEXRadioButton
	{
		[CompilerGenerated]
		get
		{
			return _IEXRadioButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = IEXRadioButton_CheckedChanged;
			RadioButton val = _IEXRadioButton;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_IEXRadioButton = value;
			val = _IEXRadioButton;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label9")]
	internal virtual Label Label9
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("LinkLabel")]
	internal virtual LinkLabel LinkLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button IEXButton
	{
		[CompilerGenerated]
		get
		{
			return _IEXButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = IEXButton_Click;
			Button val = _IEXButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_IEXButton = value;
			val = _IEXButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button BarChartButton
	{
		[CompilerGenerated]
		get
		{
			return _BarChartButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BarChartButton_Click;
			Button val = _BarChartButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_BarChartButton = value;
			val = _BarChartButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button FinnhubButton
	{
		[CompilerGenerated]
		get
		{
			return _FinnhubButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = FinnhubButton_Click;
			Button val = _FinnhubButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_FinnhubButton = value;
			val = _FinnhubButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("ReplaceQuoteCB")]
	internal virtual CheckBox ReplaceQuoteCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button ReplaceQuoteButton
	{
		[CompilerGenerated]
		get
		{
			return _ReplaceQuoteButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ReplaceQuoteButton_Click;
			Button val = _ReplaceQuoteButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ReplaceQuoteButton = value;
			val = _ReplaceQuoteButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button StockDataHelpButton
	{
		[CompilerGenerated]
		get
		{
			return _StockDataHelpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = StockDataHelpButton_Click;
			Button val = _StockDataHelpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_StockDataHelpButton = value;
			val = _StockDataHelpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual RadioButton StockDataRB
	{
		[CompilerGenerated]
		get
		{
			return _StockDataRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = StockDataRB_CheckedChanged;
			RadioButton val = _StockDataRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_StockDataRB = value;
			val = _StockDataRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual Button EODHDButton
	{
		[CompilerGenerated]
		get
		{
			return _EODHDButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = EODHDButton_Click;
			Button val = _EODHDButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_EODHDButton = value;
			val = _EODHDButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button UnibitButton
	{
		[CompilerGenerated]
		get
		{
			return _UnibitButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = UnibitButton_Click;
			Button val = _UnibitButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_UnibitButton = value;
			val = _UnibitButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual RadioButton UnibitRB
	{
		[CompilerGenerated]
		get
		{
			return _UnibitRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = UnibitRB_CheckedChanged;
			RadioButton val = _UnibitRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_UnibitRB = value;
			val = _UnibitRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual RadioButton EodhdRB
	{
		[CompilerGenerated]
		get
		{
			return _EodhdRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = EodhdRB_CheckedChanged;
			RadioButton val = _EodhdRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_EodhdRB = value;
			val = _EodhdRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	public UpdateForm()
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		((Form)this).FormClosing += new FormClosingEventHandler(UpdateForm_FormClosing);
		((Form)this).Load += UpdateForm_Load;
		IEXWarning = "Warning: For IEX, I use the current date, not the To date.";
		SymbolArray = new string[3, 1];
		StopPressed = false;
		RetryChecked = false;
		AutoStart = -1;
		RetryEngagedCounter = 0;
		StopAsking = false;
		TimerRunFlag = false;
		InitializeComponent();
	}

	[DebuggerNonUserCode]
	protected override void Dispose(bool disposing)
	{
		try
		{
			if (disposing && components != null)
			{
				components.Dispose();
			}
		}
		finally
		{
			((Form)this).Dispose(disposing);
		}
	}

	[DebuggerStepThrough]
	private void InitializeComponent()
	{
		//IL_000c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0016: Expected O, but got Unknown
		//IL_0017: Unknown result type (might be due to invalid IL or missing references)
		//IL_0021: Expected O, but got Unknown
		//IL_0022: Unknown result type (might be due to invalid IL or missing references)
		//IL_002c: Expected O, but got Unknown
		//IL_002d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0037: Expected O, but got Unknown
		//IL_0038: Unknown result type (might be due to invalid IL or missing references)
		//IL_0042: Expected O, but got Unknown
		//IL_0043: Unknown result type (might be due to invalid IL or missing references)
		//IL_004d: Expected O, but got Unknown
		//IL_004e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0058: Expected O, but got Unknown
		//IL_0059: Unknown result type (might be due to invalid IL or missing references)
		//IL_0063: Expected O, but got Unknown
		//IL_0064: Unknown result type (might be due to invalid IL or missing references)
		//IL_006e: Expected O, but got Unknown
		//IL_006f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0079: Expected O, but got Unknown
		//IL_007a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0084: Expected O, but got Unknown
		//IL_0085: Unknown result type (might be due to invalid IL or missing references)
		//IL_008f: Expected O, but got Unknown
		//IL_0090: Unknown result type (might be due to invalid IL or missing references)
		//IL_009a: Expected O, but got Unknown
		//IL_009b: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a5: Expected O, but got Unknown
		//IL_00a6: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b0: Expected O, but got Unknown
		//IL_00b1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00bb: Expected O, but got Unknown
		//IL_00bc: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c6: Expected O, but got Unknown
		//IL_00c7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d1: Expected O, but got Unknown
		//IL_00d2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00dc: Expected O, but got Unknown
		//IL_00dd: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e7: Expected O, but got Unknown
		//IL_00e8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f2: Expected O, but got Unknown
		//IL_00f3: Unknown result type (might be due to invalid IL or missing references)
		//IL_00fd: Expected O, but got Unknown
		//IL_00fe: Unknown result type (might be due to invalid IL or missing references)
		//IL_0108: Expected O, but got Unknown
		//IL_0109: Unknown result type (might be due to invalid IL or missing references)
		//IL_0113: Expected O, but got Unknown
		//IL_0114: Unknown result type (might be due to invalid IL or missing references)
		//IL_011e: Expected O, but got Unknown
		//IL_011f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0129: Expected O, but got Unknown
		//IL_012a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0134: Expected O, but got Unknown
		//IL_0135: Unknown result type (might be due to invalid IL or missing references)
		//IL_013f: Expected O, but got Unknown
		//IL_0140: Unknown result type (might be due to invalid IL or missing references)
		//IL_014a: Expected O, but got Unknown
		//IL_014b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0155: Expected O, but got Unknown
		//IL_0156: Unknown result type (might be due to invalid IL or missing references)
		//IL_0160: Expected O, but got Unknown
		//IL_0161: Unknown result type (might be due to invalid IL or missing references)
		//IL_016b: Expected O, but got Unknown
		//IL_016c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0176: Expected O, but got Unknown
		//IL_0177: Unknown result type (might be due to invalid IL or missing references)
		//IL_0181: Expected O, but got Unknown
		//IL_0182: Unknown result type (might be due to invalid IL or missing references)
		//IL_018c: Expected O, but got Unknown
		//IL_018d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0197: Expected O, but got Unknown
		//IL_0198: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a2: Expected O, but got Unknown
		//IL_01a3: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ad: Expected O, but got Unknown
		//IL_01ae: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b8: Expected O, but got Unknown
		//IL_01b9: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c3: Expected O, but got Unknown
		//IL_01c4: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ce: Expected O, but got Unknown
		//IL_01cf: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d9: Expected O, but got Unknown
		//IL_01da: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e4: Expected O, but got Unknown
		//IL_01e5: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ef: Expected O, but got Unknown
		//IL_01f0: Unknown result type (might be due to invalid IL or missing references)
		//IL_01fa: Expected O, but got Unknown
		//IL_01fb: Unknown result type (might be due to invalid IL or missing references)
		//IL_0205: Expected O, but got Unknown
		//IL_0206: Unknown result type (might be due to invalid IL or missing references)
		//IL_0210: Expected O, but got Unknown
		//IL_0211: Unknown result type (might be due to invalid IL or missing references)
		//IL_021b: Expected O, but got Unknown
		//IL_021c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0226: Expected O, but got Unknown
		//IL_0227: Unknown result type (might be due to invalid IL or missing references)
		//IL_0231: Expected O, but got Unknown
		//IL_0232: Unknown result type (might be due to invalid IL or missing references)
		//IL_023c: Expected O, but got Unknown
		//IL_023d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0247: Expected O, but got Unknown
		//IL_0248: Unknown result type (might be due to invalid IL or missing references)
		//IL_0252: Expected O, but got Unknown
		//IL_0253: Unknown result type (might be due to invalid IL or missing references)
		//IL_025d: Expected O, but got Unknown
		//IL_025e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0268: Expected O, but got Unknown
		//IL_0269: Unknown result type (might be due to invalid IL or missing references)
		//IL_0273: Expected O, but got Unknown
		//IL_0274: Unknown result type (might be due to invalid IL or missing references)
		//IL_027e: Expected O, but got Unknown
		//IL_027f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0289: Expected O, but got Unknown
		//IL_028a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0294: Expected O, but got Unknown
		//IL_0295: Unknown result type (might be due to invalid IL or missing references)
		//IL_029f: Expected O, but got Unknown
		//IL_02a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_02aa: Expected O, but got Unknown
		//IL_02b1: Unknown result type (might be due to invalid IL or missing references)
		//IL_02bb: Expected O, but got Unknown
		//IL_02bc: Unknown result type (might be due to invalid IL or missing references)
		//IL_02c6: Expected O, but got Unknown
		//IL_02c7: Unknown result type (might be due to invalid IL or missing references)
		//IL_02d1: Expected O, but got Unknown
		//IL_02d2: Unknown result type (might be due to invalid IL or missing references)
		//IL_02dc: Expected O, but got Unknown
		//IL_0ad4: Unknown result type (might be due to invalid IL or missing references)
		//IL_0ade: Expected O, but got Unknown
		//IL_0d62: Unknown result type (might be due to invalid IL or missing references)
		//IL_0d6c: Expected O, but got Unknown
		//IL_0df0: Unknown result type (might be due to invalid IL or missing references)
		//IL_0dfa: Expected O, but got Unknown
		//IL_0f72: Unknown result type (might be due to invalid IL or missing references)
		//IL_0f7c: Expected O, but got Unknown
		//IL_107b: Unknown result type (might be due to invalid IL or missing references)
		//IL_1085: Expected O, but got Unknown
		//IL_1105: Unknown result type (might be due to invalid IL or missing references)
		//IL_110f: Expected O, but got Unknown
		//IL_118f: Unknown result type (might be due to invalid IL or missing references)
		//IL_1199: Expected O, but got Unknown
		//IL_1503: Unknown result type (might be due to invalid IL or missing references)
		//IL_150d: Expected O, but got Unknown
		//IL_16c2: Unknown result type (might be due to invalid IL or missing references)
		//IL_16cc: Expected O, but got Unknown
		//IL_1f52: Unknown result type (might be due to invalid IL or missing references)
		//IL_1f5c: Expected O, but got Unknown
		//IL_2586: Unknown result type (might be due to invalid IL or missing references)
		//IL_2590: Expected O, but got Unknown
		components = new Container();
		DoneButton = new Button();
		StartButton = new Button();
		StopButton = new Button();
		SymbolLabel = new Label();
		SymbolTextBox = new TextBox();
		Label3 = new Label();
		Label2 = new Label();
		AllButton = new Button();
		ListBox1 = new ListBox();
		Label4 = new Label();
		HelpButton1 = new Button();
		ProgressBar1 = new ProgressBar();
		BrowseButton = new Button();
		FolderBrowserDialog1 = new FolderBrowserDialog();
		HistoricalRadioButton = new RadioButton();
		UpdateRadioButton = new RadioButton();
		ErrorListBox = new ListBox();
		GoogleRadioButton = new RadioButton();
		GroupBox1 = new GroupBox();
		EODHDButton = new Button();
		UnibitButton = new Button();
		UnibitRB = new RadioButton();
		EodhdRB = new RadioButton();
		StockDataHelpButton = new Button();
		StockDataRB = new RadioButton();
		FinnhubButton = new Button();
		BarChartButton = new Button();
		IEXButton = new Button();
		BarchartRB = new RadioButton();
		IEXRadioButton = new RadioButton();
		FinnhubRB = new RadioButton();
		AutoRetryCheckBox = new CheckBox();
		Panel1 = new Panel();
		RetryButton = new Button();
		TiingoHelpButton = new Button();
		TiingoRadioButton = new RadioButton();
		YahooRadioButton = new RadioButton();
		QuandlHelpButton = new Button();
		QuandlRadioButton = new RadioButton();
		TimeSeriesPanel = new Panel();
		Label9 = new Label();
		RBDaily = new RadioButton();
		RB60 = new RadioButton();
		RB30 = new RadioButton();
		NumericUpDown1 = new NumericUpDown();
		Label8 = new Label();
		RB15 = new RadioButton();
		QuandlComboBox = new ComboBox();
		Label5 = new Label();
		RB5 = new RadioButton();
		RB1 = new RadioButton();
		AlphaVHelpButton = new Button();
		AlphaVantageRadioButton = new RadioButton();
		AllPortsButton = new Button();
		Label1 = new Label();
		APIKeyTextBox = new TextBox();
		FromDatePicker = new DateTimePicker();
		ToDatePicker = new DateTimePicker();
		RetryListBox = new ListBox();
		Label6 = new Label();
		Label7 = new Label();
		Timer1 = new Timer(components);
		LinkLabel = new LinkLabel();
		ReplaceQuoteCB = new CheckBox();
		ReplaceQuoteButton = new Button();
		((Control)GroupBox1).SuspendLayout();
		((Control)Panel1).SuspendLayout();
		((Control)TimeSeriesPanel).SuspendLayout();
		((ISupportInitialize)NumericUpDown1).BeginInit();
		((Control)this).SuspendLayout();
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(611, 524);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(60, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)StartButton).Anchor = (AnchorStyles)10;
		((Control)StartButton).Location = new Point(545, 524);
		((Control)StartButton).Name = "StartButton";
		((Control)StartButton).Size = new Size(60, 23);
		((Control)StartButton).TabIndex = 21;
		((ButtonBase)StartButton).Text = "St&art";
		((ButtonBase)StartButton).UseVisualStyleBackColor = true;
		((Control)StopButton).Anchor = (AnchorStyles)10;
		((Control)StopButton).Enabled = false;
		((Control)StopButton).Location = new Point(545, 495);
		((Control)StopButton).Name = "StopButton";
		((Control)StopButton).Size = new Size(60, 23);
		((Control)StopButton).TabIndex = 20;
		((ButtonBase)StopButton).Text = "St&op";
		((ButtonBase)StopButton).UseVisualStyleBackColor = true;
		((Control)SymbolLabel).Anchor = (AnchorStyles)10;
		((Control)SymbolLabel).Location = new Point(338, 460);
		((Control)SymbolLabel).Name = "SymbolLabel";
		((Control)SymbolLabel).Size = new Size(91, 29);
		((Control)SymbolLabel).TabIndex = 11;
		SymbolLabel.Text = "&New symbol(s), space separated:";
		((Control)SymbolTextBox).Anchor = (AnchorStyles)10;
		((Control)SymbolTextBox).Enabled = false;
		((Control)SymbolTextBox).Location = new Point(435, 466);
		SymbolTextBox.Multiline = true;
		((Control)SymbolTextBox).Name = "SymbolTextBox";
		((Control)SymbolTextBox).Size = new Size(103, 20);
		((Control)SymbolTextBox).TabIndex = 12;
		((TextBoxBase)SymbolTextBox).WordWrap = false;
		((Control)Label3).Anchor = (AnchorStyles)10;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(406, 526);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(23, 13);
		((Control)Label3).TabIndex = 16;
		Label3.Text = "&To:";
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(396, 503);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(33, 13);
		((Control)Label2).TabIndex = 14;
		Label2.Text = "&From:";
		((Control)AllButton).Anchor = (AnchorStyles)10;
		((Control)AllButton).Location = new Point(611, 466);
		((Control)AllButton).Name = "AllButton";
		((Control)AllButton).Size = new Size(60, 23);
		((Control)AllButton).TabIndex = 22;
		((ButtonBase)AllButton).Text = "&Select All";
		((ButtonBase)AllButton).UseVisualStyleBackColor = true;
		((Control)ListBox1).Anchor = (AnchorStyles)15;
		ListBox1.HorizontalScrollbar = true;
		((Control)ListBox1).Location = new Point(12, 12);
		ListBox1.MultiColumn = true;
		((Control)ListBox1).Name = "ListBox1";
		ListBox1.SelectionMode = (SelectionMode)3;
		((Control)ListBox1).Size = new Size(661, 212);
		ListBox1.Sorted = true;
		((Control)ListBox1).TabIndex = 1;
		((Control)Label4).Anchor = (AnchorStyles)10;
		Label4.BorderStyle = (BorderStyle)2;
		Label4.FlatStyle = (FlatStyle)0;
		((Control)Label4).Location = new Point(225, 391);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(446, 21);
		((Control)Label4).TabIndex = 6;
		Label4.TextAlign = (ContentAlignment)16;
		((Control)HelpButton1).Anchor = (AnchorStyles)10;
		((Control)HelpButton1).Location = new Point(611, 495);
		((Control)HelpButton1).Name = "HelpButton1";
		((Control)HelpButton1).Size = new Size(60, 23);
		((Control)HelpButton1).TabIndex = 23;
		((ButtonBase)HelpButton1).Text = "&Help";
		((ButtonBase)HelpButton1).UseVisualStyleBackColor = true;
		((Control)ProgressBar1).Anchor = (AnchorStyles)14;
		((Control)ProgressBar1).ForeColor = Color.Green;
		((Control)ProgressBar1).Location = new Point(12, 580);
		((Control)ProgressBar1).Name = "ProgressBar1";
		((Control)ProgressBar1).Size = new Size(661, 23);
		((Control)ProgressBar1).TabIndex = 24;
		((Control)BrowseButton).Anchor = (AnchorStyles)10;
		((Control)BrowseButton).Location = new Point(545, 466);
		((Control)BrowseButton).Name = "BrowseButton";
		((Control)BrowseButton).Size = new Size(60, 23);
		((Control)BrowseButton).TabIndex = 19;
		((ButtonBase)BrowseButton).Text = "&Browse";
		((ButtonBase)BrowseButton).UseVisualStyleBackColor = true;
		((Control)HistoricalRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)HistoricalRadioButton).AutoSize = true;
		HistoricalRadioButton.Checked = true;
		((Control)HistoricalRadioButton).Location = new Point(16, 25);
		((Control)HistoricalRadioButton).Name = "HistoricalRadioButton";
		((Control)HistoricalRadioButton).Size = new Size(121, 17);
		((Control)HistoricalRadioButton).TabIndex = 1;
		HistoricalRadioButton.TabStop = true;
		((ButtonBase)HistoricalRadioButton).Text = "Get historical &quotes";
		((ButtonBase)HistoricalRadioButton).UseVisualStyleBackColor = true;
		((Control)UpdateRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)UpdateRadioButton).AutoSize = true;
		((Control)UpdateRadioButton).Location = new Point(16, 3);
		((Control)UpdateRadioButton).Name = "UpdateRadioButton";
		((Control)UpdateRadioButton).Size = new Size(125, 17);
		((Control)UpdateRadioButton).TabIndex = 0;
		((ButtonBase)UpdateRadioButton).Text = "Start f&rom last update";
		((ButtonBase)UpdateRadioButton).UseVisualStyleBackColor = true;
		((Control)ErrorListBox).Anchor = (AnchorStyles)14;
		((Control)ErrorListBox).CausesValidation = false;
		ErrorListBox.HorizontalScrollbar = true;
		((Control)ErrorListBox).Location = new Point(12, 609);
		((Control)ErrorListBox).Name = "ErrorListBox";
		((Control)ErrorListBox).Size = new Size(661, 108);
		ErrorListBox.Sorted = true;
		((Control)ErrorListBox).TabIndex = 25;
		((Control)GoogleRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)GoogleRadioButton).AutoSize = true;
		((Control)GoogleRadioButton).Enabled = false;
		((Control)GoogleRadioButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)GoogleRadioButton).Location = new Point(28, 15);
		((Control)GoogleRadioButton).Name = "GoogleRadioButton";
		((Control)GoogleRadioButton).Size = new Size(59, 17);
		((Control)GoogleRadioButton).TabIndex = 5;
		((ButtonBase)GoogleRadioButton).Text = "&Google";
		((ButtonBase)GoogleRadioButton).UseVisualStyleBackColor = true;
		((Control)GoogleRadioButton).Visible = false;
		((Control)GroupBox1).Anchor = (AnchorStyles)10;
		((Control)GroupBox1).CausesValidation = false;
		((Control)GroupBox1).Controls.Add((Control)(object)EODHDButton);
		((Control)GroupBox1).Controls.Add((Control)(object)UnibitButton);
		((Control)GroupBox1).Controls.Add((Control)(object)UnibitRB);
		((Control)GroupBox1).Controls.Add((Control)(object)EodhdRB);
		((Control)GroupBox1).Controls.Add((Control)(object)StockDataHelpButton);
		((Control)GroupBox1).Controls.Add((Control)(object)StockDataRB);
		((Control)GroupBox1).Controls.Add((Control)(object)FinnhubButton);
		((Control)GroupBox1).Controls.Add((Control)(object)BarChartButton);
		((Control)GroupBox1).Controls.Add((Control)(object)IEXButton);
		((Control)GroupBox1).Controls.Add((Control)(object)BarchartRB);
		((Control)GroupBox1).Controls.Add((Control)(object)IEXRadioButton);
		((Control)GroupBox1).Controls.Add((Control)(object)FinnhubRB);
		((Control)GroupBox1).Controls.Add((Control)(object)AutoRetryCheckBox);
		((Control)GroupBox1).Controls.Add((Control)(object)Panel1);
		((Control)GroupBox1).Controls.Add((Control)(object)RetryButton);
		((Control)GroupBox1).Controls.Add((Control)(object)TiingoHelpButton);
		((Control)GroupBox1).Controls.Add((Control)(object)TiingoRadioButton);
		((Control)GroupBox1).Location = new Point(12, 380);
		((Control)GroupBox1).Name = "GroupBox1";
		((Control)GroupBox1).Size = new Size(207, 194);
		((Control)GroupBox1).TabIndex = 5;
		GroupBox1.TabStop = false;
		GroupBox1.Text = "Quote Providers";
		((Control)EODHDButton).Anchor = (AnchorStyles)10;
		((Control)EODHDButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)EODHDButton).Location = new Point(166, 96);
		((Control)EODHDButton).Name = "EODHDButton";
		((Control)EODHDButton).Size = new Size(20, 20);
		((Control)EODHDButton).TabIndex = 16;
		((ButtonBase)EODHDButton).Text = "?";
		((ButtonBase)EODHDButton).UseVisualStyleBackColor = true;
		((Control)UnibitButton).Anchor = (AnchorStyles)10;
		((Control)UnibitButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)UnibitButton).Location = new Point(166, 72);
		((Control)UnibitButton).Name = "UnibitButton";
		((Control)UnibitButton).Size = new Size(20, 20);
		((Control)UnibitButton).TabIndex = 15;
		((ButtonBase)UnibitButton).Text = "?";
		((ButtonBase)UnibitButton).UseVisualStyleBackColor = true;
		((Control)UnibitRB).Anchor = (AnchorStyles)10;
		((ButtonBase)UnibitRB).AutoSize = true;
		((Control)UnibitRB).Location = new Point(103, 75);
		((Control)UnibitRB).Name = "UnibitRB";
		((Control)UnibitRB).Size = new Size(53, 17);
		((Control)UnibitRB).TabIndex = 10;
		((ButtonBase)UnibitRB).Text = "&UniBit";
		((ButtonBase)UnibitRB).UseVisualStyleBackColor = true;
		((Control)EodhdRB).Anchor = (AnchorStyles)10;
		((ButtonBase)EodhdRB).AutoSize = true;
		((Control)EodhdRB).Location = new Point(103, 98);
		((Control)EodhdRB).Name = "EodhdRB";
		((Control)EodhdRB).Size = new Size(64, 17);
		((Control)EodhdRB).TabIndex = 11;
		((ButtonBase)EodhdRB).Text = "&EODHD";
		((ButtonBase)EodhdRB).UseVisualStyleBackColor = true;
		((Control)StockDataHelpButton).Anchor = (AnchorStyles)10;
		((Control)StockDataHelpButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)StockDataHelpButton).Location = new Point(104, 168);
		((Control)StockDataHelpButton).Name = "StockDataHelpButton";
		((Control)StockDataHelpButton).Size = new Size(20, 20);
		((Control)StockDataHelpButton).TabIndex = 14;
		((ButtonBase)StockDataHelpButton).Text = "?";
		((ButtonBase)StockDataHelpButton).UseVisualStyleBackColor = true;
		((Control)StockDataRB).Anchor = (AnchorStyles)10;
		((ButtonBase)StockDataRB).AutoSize = true;
		((Control)StockDataRB).Location = new Point(7, 167);
		((Control)StockDataRB).Name = "StockDataRB";
		((Control)StockDataRB).Size = new Size(92, 17);
		((Control)StockDataRB).TabIndex = 5;
		((ButtonBase)StockDataRB).Text = "&Stockdata.org";
		((ButtonBase)StockDataRB).UseVisualStyleBackColor = true;
		((Control)FinnhubButton).Anchor = (AnchorStyles)10;
		((Control)FinnhubButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)FinnhubButton).Location = new Point(69, 96);
		((Control)FinnhubButton).Name = "FinnhubButton";
		((Control)FinnhubButton).Size = new Size(20, 20);
		((Control)FinnhubButton).TabIndex = 7;
		((ButtonBase)FinnhubButton).Text = "?";
		((ButtonBase)FinnhubButton).UseVisualStyleBackColor = true;
		((Control)BarChartButton).Anchor = (AnchorStyles)10;
		((Control)BarChartButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)BarChartButton).Location = new Point(69, 72);
		((Control)BarChartButton).Name = "BarChartButton";
		((Control)BarChartButton).Size = new Size(20, 20);
		((Control)BarChartButton).TabIndex = 6;
		((ButtonBase)BarChartButton).Text = "?";
		((ButtonBase)BarChartButton).UseVisualStyleBackColor = true;
		((Control)IEXButton).Anchor = (AnchorStyles)10;
		((Control)IEXButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)IEXButton).Location = new Point(69, 120);
		((Control)IEXButton).Name = "IEXButton";
		((Control)IEXButton).Size = new Size(20, 20);
		((Control)IEXButton).TabIndex = 8;
		((ButtonBase)IEXButton).Text = "?";
		((ButtonBase)IEXButton).UseVisualStyleBackColor = true;
		((Control)BarchartRB).Anchor = (AnchorStyles)10;
		((ButtonBase)BarchartRB).AutoSize = true;
		((Control)BarchartRB).Location = new Point(7, 75);
		((Control)BarchartRB).Name = "BarchartRB";
		((Control)BarchartRB).Size = new Size(65, 17);
		((Control)BarchartRB).TabIndex = 1;
		((ButtonBase)BarchartRB).Text = "&Barchart";
		((ButtonBase)BarchartRB).UseVisualStyleBackColor = true;
		((Control)IEXRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)IEXRadioButton).AutoSize = true;
		((Control)IEXRadioButton).Location = new Point(7, 121);
		((Control)IEXRadioButton).Name = "IEXRadioButton";
		((Control)IEXRadioButton).Size = new Size(42, 17);
		((Control)IEXRadioButton).TabIndex = 3;
		((ButtonBase)IEXRadioButton).Text = "&IEX";
		((ButtonBase)IEXRadioButton).UseVisualStyleBackColor = true;
		((Control)FinnhubRB).Anchor = (AnchorStyles)10;
		((ButtonBase)FinnhubRB).AutoSize = true;
		((Control)FinnhubRB).Enabled = false;
		((Control)FinnhubRB).Location = new Point(7, 98);
		((Control)FinnhubRB).Name = "FinnhubRB";
		((Control)FinnhubRB).Size = new Size(63, 17);
		((Control)FinnhubRB).TabIndex = 2;
		((ButtonBase)FinnhubRB).Text = "&Finnhub";
		((ButtonBase)FinnhubRB).UseVisualStyleBackColor = true;
		((Control)AutoRetryCheckBox).Anchor = (AnchorStyles)10;
		((ButtonBase)AutoRetryCheckBox).AutoSize = true;
		((Control)AutoRetryCheckBox).Location = new Point(104, 124);
		((Control)AutoRetryCheckBox).Name = "AutoRetryCheckBox";
		((Control)AutoRetryCheckBox).Size = new Size(71, 17);
		((Control)AutoRetryCheckBox).TabIndex = 12;
		((ButtonBase)AutoRetryCheckBox).Text = "Auto retry";
		((ButtonBase)AutoRetryCheckBox).UseVisualStyleBackColor = true;
		((Control)Panel1).Anchor = (AnchorStyles)10;
		Panel1.BorderStyle = (BorderStyle)1;
		((Control)Panel1).Controls.Add((Control)(object)HistoricalRadioButton);
		((Control)Panel1).Controls.Add((Control)(object)UpdateRadioButton);
		((Control)Panel1).Location = new Point(3, 18);
		((Control)Panel1).Name = "Panel1";
		((Control)Panel1).Size = new Size(154, 51);
		((Control)Panel1).TabIndex = 0;
		((Control)RetryButton).Anchor = (AnchorStyles)10;
		((Control)RetryButton).Location = new Point(104, 144);
		((Control)RetryButton).Name = "RetryButton";
		((Control)RetryButton).Size = new Size(53, 20);
		((Control)RetryButton).TabIndex = 13;
		((ButtonBase)RetryButton).Text = "&Retry";
		((ButtonBase)RetryButton).UseVisualStyleBackColor = true;
		((Control)TiingoHelpButton).Anchor = (AnchorStyles)10;
		((Control)TiingoHelpButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)TiingoHelpButton).Location = new Point(69, 144);
		((Control)TiingoHelpButton).Name = "TiingoHelpButton";
		((Control)TiingoHelpButton).Size = new Size(20, 20);
		((Control)TiingoHelpButton).TabIndex = 9;
		((ButtonBase)TiingoHelpButton).Text = "?";
		((ButtonBase)TiingoHelpButton).UseVisualStyleBackColor = true;
		((Control)TiingoRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)TiingoRadioButton).AutoSize = true;
		((Control)TiingoRadioButton).Location = new Point(7, 144);
		((Control)TiingoRadioButton).Name = "TiingoRadioButton";
		((Control)TiingoRadioButton).Size = new Size(54, 17);
		((Control)TiingoRadioButton).TabIndex = 4;
		((ButtonBase)TiingoRadioButton).Text = "&Tiingo";
		((ButtonBase)TiingoRadioButton).UseVisualStyleBackColor = true;
		((Control)YahooRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)YahooRadioButton).AutoSize = true;
		YahooRadioButton.Checked = true;
		((Control)YahooRadioButton).Enabled = false;
		((Control)YahooRadioButton).Location = new Point(10, 79);
		((Control)YahooRadioButton).Name = "YahooRadioButton";
		((Control)YahooRadioButton).Size = new Size(56, 17);
		((Control)YahooRadioButton).TabIndex = 9;
		YahooRadioButton.TabStop = true;
		((ButtonBase)YahooRadioButton).Text = "&Yahoo";
		((ButtonBase)YahooRadioButton).UseVisualStyleBackColor = true;
		((Control)YahooRadioButton).Visible = false;
		((Control)QuandlHelpButton).Anchor = (AnchorStyles)10;
		((Control)QuandlHelpButton).Enabled = false;
		((Control)QuandlHelpButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)QuandlHelpButton).Location = new Point(91, 119);
		((Control)QuandlHelpButton).Name = "QuandlHelpButton";
		((Control)QuandlHelpButton).Size = new Size(20, 20);
		((Control)QuandlHelpButton).TabIndex = 8;
		((ButtonBase)QuandlHelpButton).Text = "?";
		((ButtonBase)QuandlHelpButton).UseVisualStyleBackColor = true;
		((Control)QuandlHelpButton).Visible = false;
		((Control)QuandlRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)QuandlRadioButton).AutoSize = true;
		((Control)QuandlRadioButton).Enabled = false;
		((Control)QuandlRadioButton).Location = new Point(29, 119);
		((Control)QuandlRadioButton).Name = "QuandlRadioButton";
		((Control)QuandlRadioButton).Size = new Size(59, 17);
		((Control)QuandlRadioButton).TabIndex = 7;
		((ButtonBase)QuandlRadioButton).Text = "&Quandl";
		((ButtonBase)QuandlRadioButton).UseVisualStyleBackColor = true;
		((Control)QuandlRadioButton).Visible = false;
		((Control)TimeSeriesPanel).Anchor = (AnchorStyles)10;
		TimeSeriesPanel.BorderStyle = (BorderStyle)1;
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)Label9);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)RBDaily);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)RB60);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)RB30);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)NumericUpDown1);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)Label8);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)RB15);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)QuandlComboBox);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)YahooRadioButton);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)Label5);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)RB5);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)RB1);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)GoogleRadioButton);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)QuandlHelpButton);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)AlphaVHelpButton);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)QuandlRadioButton);
		((Control)TimeSeriesPanel).Controls.Add((Control)(object)AlphaVantageRadioButton);
		((Control)TimeSeriesPanel).Location = new Point(444, 609);
		((Control)TimeSeriesPanel).Name = "TimeSeriesPanel";
		((Control)TimeSeriesPanel).Size = new Size(229, 148);
		((Control)TimeSeriesPanel).TabIndex = 13;
		((Control)TimeSeriesPanel).Visible = false;
		((Control)Label9).Anchor = (AnchorStyles)14;
		Label9.AutoSize = true;
		((Control)Label9).ForeColor = Color.Red;
		((Control)Label9).Location = new Point(16, 103);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(134, 13);
		((Control)Label9).TabIndex = 17;
		Label9.Text = "These are unused vendors";
		Label9.TextAlign = (ContentAlignment)32;
		((Control)RBDaily).Anchor = (AnchorStyles)10;
		((ButtonBase)RBDaily).AutoSize = true;
		RBDaily.Checked = true;
		((Control)RBDaily).Location = new Point(142, 120);
		((Control)RBDaily).Name = "RBDaily";
		((Control)RBDaily).Size = new Size(48, 17);
		((Control)RBDaily).TabIndex = 16;
		RBDaily.TabStop = true;
		((ButtonBase)RBDaily).Text = "&Daily";
		((ButtonBase)RBDaily).UseVisualStyleBackColor = true;
		((Control)RB60).Anchor = (AnchorStyles)10;
		((ButtonBase)RB60).AutoSize = true;
		((Control)RB60).Location = new Point(142, 99);
		((Control)RB60).Name = "RB60";
		((Control)RB60).Size = new Size(71, 17);
		((Control)RB60).TabIndex = 4;
		((ButtonBase)RB60).Text = "&60 minute";
		((ButtonBase)RB60).UseVisualStyleBackColor = true;
		((Control)RB30).Anchor = (AnchorStyles)10;
		((ButtonBase)RB30).AutoSize = true;
		((Control)RB30).Location = new Point(142, 78);
		((Control)RB30).Name = "RB30";
		((Control)RB30).Size = new Size(71, 17);
		((Control)RB30).TabIndex = 3;
		((ButtonBase)RB30).Text = "&30 minute";
		((ButtonBase)RB30).UseVisualStyleBackColor = true;
		((Control)NumericUpDown1).Anchor = (AnchorStyles)10;
		((Control)NumericUpDown1).Location = new Point(67, 73);
		((Control)NumericUpDown1).Name = "NumericUpDown1";
		((Control)NumericUpDown1).Size = new Size(40, 20);
		((Control)NumericUpDown1).TabIndex = 4;
		NumericUpDown1.Value = new decimal(new int[4] { 5, 0, 0, 0 });
		((Control)NumericUpDown1).Visible = false;
		((Control)Label8).Anchor = (AnchorStyles)10;
		Label8.AutoSize = true;
		((Control)Label8).Location = new Point(61, 57);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(62, 13);
		((Control)Label8).TabIndex = 3;
		Label8.Text = "Quotes/min";
		((Control)Label8).Visible = false;
		((Control)RB15).Anchor = (AnchorStyles)10;
		((ButtonBase)RB15).AutoSize = true;
		((Control)RB15).Location = new Point(142, 57);
		((Control)RB15).Name = "RB15";
		((Control)RB15).Size = new Size(71, 17);
		((Control)RB15).TabIndex = 2;
		((ButtonBase)RB15).Text = "15 &minute";
		((ButtonBase)RB15).UseVisualStyleBackColor = true;
		((Control)QuandlComboBox).Anchor = (AnchorStyles)10;
		((Control)QuandlComboBox).Enabled = false;
		((ListControl)QuandlComboBox).FormattingEnabled = true;
		((Control)QuandlComboBox).Location = new Point(84, 3);
		((Control)QuandlComboBox).Name = "QuandlComboBox";
		((Control)QuandlComboBox).Size = new Size(239, 21);
		QuandlComboBox.Sorted = true;
		((Control)QuandlComboBox).TabIndex = 12;
		((Control)QuandlComboBox).Visible = false;
		((Control)Label5).Anchor = (AnchorStyles)10;
		Label5.AutoSize = true;
		((Control)Label5).Location = new Point(16, 6);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(62, 13);
		((Control)Label5).TabIndex = 11;
		Label5.Text = "&Quandl DB:";
		Label5.TextAlign = (ContentAlignment)32;
		((Control)RB5).Anchor = (AnchorStyles)10;
		((ButtonBase)RB5).AutoSize = true;
		((Control)RB5).Location = new Point(142, 36);
		((Control)RB5).Name = "RB5";
		((Control)RB5).Size = new Size(65, 17);
		((Control)RB5).TabIndex = 1;
		((ButtonBase)RB5).Text = "&5 minute";
		((ButtonBase)RB5).UseVisualStyleBackColor = true;
		((Control)RB1).Anchor = (AnchorStyles)10;
		((ButtonBase)RB1).AutoSize = true;
		((Control)RB1).Location = new Point(142, 15);
		((Control)RB1).Name = "RB1";
		((Control)RB1).Size = new Size(65, 17);
		((Control)RB1).TabIndex = 0;
		((ButtonBase)RB1).Text = "&1 minute";
		((ButtonBase)RB1).UseVisualStyleBackColor = true;
		((Control)AlphaVHelpButton).Anchor = (AnchorStyles)10;
		((Control)AlphaVHelpButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)AlphaVHelpButton).Location = new Point(28, 53);
		((Control)AlphaVHelpButton).Name = "AlphaVHelpButton";
		((Control)AlphaVHelpButton).Size = new Size(20, 20);
		((Control)AlphaVHelpButton).TabIndex = 2;
		((ButtonBase)AlphaVHelpButton).Text = "?";
		((ButtonBase)AlphaVHelpButton).UseVisualStyleBackColor = true;
		((Control)AlphaVHelpButton).Visible = false;
		((Control)AlphaVantageRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)AlphaVantageRadioButton).AutoSize = true;
		((Control)AlphaVantageRadioButton).Enabled = false;
		((Control)AlphaVantageRadioButton).Location = new Point(28, 36);
		((Control)AlphaVantageRadioButton).Name = "AlphaVantageRadioButton";
		((Control)AlphaVantageRadioButton).Size = new Size(95, 17);
		((Control)AlphaVantageRadioButton).TabIndex = 1;
		((ButtonBase)AlphaVantageRadioButton).Text = "Alpha Vantage";
		((ButtonBase)AlphaVantageRadioButton).UseVisualStyleBackColor = true;
		((Control)AlphaVantageRadioButton).Visible = false;
		((Control)AllPortsButton).Anchor = (AnchorStyles)10;
		((Control)AllPortsButton).Location = new Point(545, 435);
		((Control)AllPortsButton).Name = "AllPortsButton";
		((Control)AllPortsButton).Size = new Size(126, 23);
		((Control)AllPortsButton).TabIndex = 18;
		((ButtonBase)AllPortsButton).Text = "&Update All Portfolios";
		((ButtonBase)AllPortsButton).UseVisualStyleBackColor = true;
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(345, 435);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(84, 13);
		((Control)Label1).TabIndex = 9;
		Label1.Text = "&API Key/Token:";
		((Control)APIKeyTextBox).Anchor = (AnchorStyles)10;
		((Control)APIKeyTextBox).Location = new Point(435, 435);
		((TextBoxBase)APIKeyTextBox).MaxLength = 100;
		((Control)APIKeyTextBox).Name = "APIKeyTextBox";
		((Control)APIKeyTextBox).Size = new Size(103, 20);
		((Control)APIKeyTextBox).TabIndex = 10;
		((TextBoxBase)APIKeyTextBox).WordWrap = false;
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(435, 499);
		((Control)FromDatePicker).Name = "FromDatePicker";
		FromDatePicker.ShowUpDown = true;
		((Control)FromDatePicker).Size = new Size(100, 20);
		((Control)FromDatePicker).TabIndex = 15;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(435, 525);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(100, 20);
		((Control)ToDatePicker).TabIndex = 17;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)RetryListBox).Anchor = (AnchorStyles)14;
		RetryListBox.HorizontalScrollbar = true;
		((Control)RetryListBox).Location = new Point(11, 244);
		((Control)RetryListBox).Name = "RetryListBox";
		RetryListBox.SelectionMode = (SelectionMode)3;
		((Control)RetryListBox).Size = new Size(661, 108);
		((Control)RetryListBox).TabIndex = 3;
		((Control)Label6).Anchor = (AnchorStyles)14;
		Label6.AutoSize = true;
		((Control)Label6).Location = new Point(90, 355);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(421, 13);
		((Control)Label6).TabIndex = 4;
		Label6.Text = "(Retry list box above. Highlight symbols to retry, switch quote providers, and click 'Retry')";
		Label6.TextAlign = (ContentAlignment)32;
		((Control)Label7).Anchor = (AnchorStyles)14;
		Label7.AutoSize = true;
		((Control)Label7).Location = new Point(197, 228);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(219, 13);
		((Control)Label7).TabIndex = 2;
		Label7.Text = "(Above: Delete key to remove, F2 to rename)";
		Label7.TextAlign = (ContentAlignment)32;
		((Label)LinkLabel).AutoSize = true;
		LinkLabel.LinkColor = Color.Black;
		((Control)LinkLabel).Location = new Point(246, 546);
		((Control)LinkLabel).Name = "LinkLabel";
		((Control)LinkLabel).Size = new Size(138, 13);
		((Control)LinkLabel).TabIndex = 8;
		LinkLabel.TabStop = true;
		LinkLabel.Text = "Data provided by IEX Cloud";
		((Control)ReplaceQuoteCB).Anchor = (AnchorStyles)10;
		((ButtonBase)ReplaceQuoteCB).AutoSize = true;
		((Control)ReplaceQuoteCB).Location = new Point(225, 502);
		((Control)ReplaceQuoteCB).Name = "ReplaceQuoteCB";
		((Control)ReplaceQuoteCB).Size = new Size(115, 17);
		((Control)ReplaceQuoteCB).TabIndex = 7;
		((ButtonBase)ReplaceQuoteCB).Text = "Replace last quote";
		((ButtonBase)ReplaceQuoteCB).UseVisualStyleBackColor = true;
		((Control)ReplaceQuoteButton).Anchor = (AnchorStyles)10;
		((Control)ReplaceQuoteButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)ReplaceQuoteButton).Location = new Point(346, 501);
		((Control)ReplaceQuoteButton).Name = "ReplaceQuoteButton";
		((Control)ReplaceQuoteButton).Size = new Size(20, 20);
		((Control)ReplaceQuoteButton).TabIndex = 13;
		((ButtonBase)ReplaceQuoteButton).Text = "?";
		((ButtonBase)ReplaceQuoteButton).UseVisualStyleBackColor = true;
		((Form)this).AcceptButton = (IButtonControl)(object)StartButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Control)this).CausesValidation = false;
		((Form)this).ClientSize = new Size(685, 729);
		((Control)this).Controls.Add((Control)(object)ReplaceQuoteButton);
		((Control)this).Controls.Add((Control)(object)ReplaceQuoteCB);
		((Control)this).Controls.Add((Control)(object)LinkLabel);
		((Control)this).Controls.Add((Control)(object)Label7);
		((Control)this).Controls.Add((Control)(object)Label6);
		((Control)this).Controls.Add((Control)(object)RetryListBox);
		((Control)this).Controls.Add((Control)(object)TimeSeriesPanel);
		((Control)this).Controls.Add((Control)(object)ToDatePicker);
		((Control)this).Controls.Add((Control)(object)FromDatePicker);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)APIKeyTextBox);
		((Control)this).Controls.Add((Control)(object)AllPortsButton);
		((Control)this).Controls.Add((Control)(object)GroupBox1);
		((Control)this).Controls.Add((Control)(object)ErrorListBox);
		((Control)this).Controls.Add((Control)(object)ProgressBar1);
		((Control)this).Controls.Add((Control)(object)BrowseButton);
		((Control)this).Controls.Add((Control)(object)HelpButton1);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)ListBox1);
		((Control)this).Controls.Add((Control)(object)AllButton);
		((Control)this).Controls.Add((Control)(object)SymbolLabel);
		((Control)this).Controls.Add((Control)(object)SymbolTextBox);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)StartButton);
		((Control)this).Controls.Add((Control)(object)StopButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Name = "UpdateForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Update Form";
		((Control)GroupBox1).ResumeLayout(false);
		((Control)GroupBox1).PerformLayout();
		((Control)Panel1).ResumeLayout(false);
		((Control)Panel1).PerformLayout();
		((Control)TimeSeriesPanel).ResumeLayout(false);
		((Control)TimeSeriesPanel).PerformLayout();
		((ISupportInitialize)NumericUpDown1).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void UpdateForm_FormClosing(object sender, FormClosingEventArgs e)
	{
		//IL_001a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0020: Invalid comparison between Unknown and I4
		if (((Control)StopButton).Enabled)
		{
			if ((int)MessageBox.Show("Did you want to stop the update and exit the form?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32) != 6)
			{
				((CancelEventArgs)(object)e).Cancel = true;
				return;
			}
			StopPressed = true;
			((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
		}
		GlobalForm.AutoRetry = AutoRetryCheckBox.Checked;
		TimerRunFlag = false;
		Timer1.Enabled = false;
		GlobalForm.UFDateLookBack = Math.Abs(DateAndTime.DateDiff((DateInterval)4, FromDatePicker.Value, ToDatePicker.Value, (FirstDayOfWeek)1, (FirstWeekOfYear)1));
		if (UpdateRadioButton.Checked)
		{
			GlobalForm.UpdatePeriod = 2;
		}
		else if (HistoricalRadioButton.Checked)
		{
			GlobalForm.UpdatePeriod = 3;
		}
		bool flag = true;
		if (flag == BarchartRB.Checked)
		{
			GlobalForm.UpdateSource = 8;
		}
		else if (flag == IEXRadioButton.Checked)
		{
			GlobalForm.UpdateSource = 7;
		}
		else if (flag == FinnhubRB.Checked)
		{
			GlobalForm.UpdateSource = 6;
		}
		else if (flag == StockDataRB.Checked)
		{
			GlobalForm.UpdateSource = 9;
		}
		else if (flag == TiingoRadioButton.Checked)
		{
			GlobalForm.UpdateSource = 4;
		}
		else if (flag == UnibitRB.Checked)
		{
			GlobalForm.UpdateSource = 10;
		}
		else if (flag == EodhdRB.Checked)
		{
			GlobalForm.UpdateSource = 11;
		}
		if (Operators.CompareString(GlobalForm.lsTiingoKey, GlobalForm.TiingoKey, false) != 0)
		{
			string text = new GlobalForm.Simple3Des("da9ba2681").EncryptData(GlobalForm.TiingoKey);
			try
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "Captoff", (object)text);
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				ProjectData.ClearProjectError();
			}
		}
		if (Operators.CompareString(GlobalForm.lsBarchartKey, GlobalForm.BarchartKey, false) != 0)
		{
			string text2 = new GlobalForm.Simple3Des("FF341EB231C7\u0019").EncryptData(GlobalForm.BarchartKey);
			try
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap1", (object)text2);
			}
			catch (Exception ex3)
			{
				ProjectData.SetProjectError(ex3);
				Exception ex4 = ex3;
				ProjectData.ClearProjectError();
			}
		}
		if (Operators.CompareString(GlobalForm.lsFinnhubKey, GlobalForm.FinnhubKey, false) != 0)
		{
			string text3 = new GlobalForm.Simple3Des("F712DC14acD5\u0019").EncryptData(GlobalForm.FinnhubKey);
			try
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap2", (object)text3);
			}
			catch (Exception ex5)
			{
				ProjectData.SetProjectError(ex5);
				Exception ex6 = ex5;
				ProjectData.ClearProjectError();
			}
		}
		if (Operators.CompareString(GlobalForm.lsIEXKey, GlobalForm.IEXKey, false) != 0)
		{
			string text4 = new GlobalForm.Simple3Des("45EDC2319CBc5\u0019").EncryptData(GlobalForm.IEXKey);
			try
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap3", (object)text4);
			}
			catch (Exception ex7)
			{
				ProjectData.SetProjectError(ex7);
				Exception ex8 = ex7;
				ProjectData.ClearProjectError();
			}
		}
		if (Operators.CompareString(GlobalForm.lsSDKey, GlobalForm.SDKey, false) != 0)
		{
			string text5 = new GlobalForm.Simple3Des("97FAC936qr{=48").EncryptData(GlobalForm.SDKey);
			try
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap4", (object)text5);
			}
			catch (Exception ex9)
			{
				ProjectData.SetProjectError(ex9);
				Exception ex10 = ex9;
				ProjectData.ClearProjectError();
			}
		}
		if (Operators.CompareString(GlobalForm.lsUnibitKey, GlobalForm.UnibitKey, false) != 0)
		{
			string text6 = new GlobalForm.Simple3Des("10D0A983EB430C").EncryptData(GlobalForm.UnibitKey);
			try
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap5", (object)text6);
			}
			catch (Exception ex11)
			{
				ProjectData.SetProjectError(ex11);
				Exception ex12 = ex11;
				ProjectData.ClearProjectError();
			}
		}
		if (Operators.CompareString(GlobalForm.lsEODHDKey, GlobalForm.EODHDKey, false) != 0)
		{
			string text7 = new GlobalForm.Simple3Des("04CEA3718DBC40").EncryptData(GlobalForm.EODHDKey);
			try
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap6", (object)text7);
			}
			catch (Exception ex13)
			{
				ProjectData.SetProjectError(ex13);
				Exception ex14 = ex13;
				ProjectData.ClearProjectError();
			}
		}
		MySettingsProperty.Settings.UpdateLocation = ((Form)this).Location;
		MySettingsProperty.Settings.UpdateSize = ((Form)this).Size;
		MySettingsProperty.Settings.ReplaceQuoteCB = ReplaceQuoteCB.Checked;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
	}

	private void UpdateForm_Load(object sender, EventArgs e)
	{
		//IL_0036: Unknown result type (might be due to invalid IL or missing references)
		//IL_003b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0046: Unknown result type (might be due to invalid IL or missing references)
		//IL_0051: Unknown result type (might be due to invalid IL or missing references)
		//IL_005c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0063: Unknown result type (might be due to invalid IL or missing references)
		//IL_0074: Unknown result type (might be due to invalid IL or missing references)
		//IL_0085: Unknown result type (might be due to invalid IL or missing references)
		//IL_0096: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c9: Unknown result type (might be due to invalid IL or missing references)
		//IL_00da: Unknown result type (might be due to invalid IL or missing references)
		//IL_00eb: Unknown result type (might be due to invalid IL or missing references)
		//IL_00fc: Unknown result type (might be due to invalid IL or missing references)
		//IL_010d: Unknown result type (might be due to invalid IL or missing references)
		//IL_011e: Unknown result type (might be due to invalid IL or missing references)
		//IL_012f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0140: Unknown result type (might be due to invalid IL or missing references)
		//IL_0151: Unknown result type (might be due to invalid IL or missing references)
		//IL_0162: Unknown result type (might be due to invalid IL or missing references)
		//IL_0173: Unknown result type (might be due to invalid IL or missing references)
		//IL_0184: Unknown result type (might be due to invalid IL or missing references)
		//IL_0195: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a6: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b7: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c8: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d9: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ea: Unknown result type (might be due to invalid IL or missing references)
		//IL_01fb: Unknown result type (might be due to invalid IL or missing references)
		//IL_020c: Unknown result type (might be due to invalid IL or missing references)
		//IL_021d: Unknown result type (might be due to invalid IL or missing references)
		//IL_022e: Unknown result type (might be due to invalid IL or missing references)
		//IL_023f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0250: Unknown result type (might be due to invalid IL or missing references)
		//IL_0261: Unknown result type (might be due to invalid IL or missing references)
		//IL_0272: Unknown result type (might be due to invalid IL or missing references)
		//IL_0283: Unknown result type (might be due to invalid IL or missing references)
		//IL_0294: Unknown result type (might be due to invalid IL or missing references)
		//IL_02a5: Unknown result type (might be due to invalid IL or missing references)
		//IL_02b6: Unknown result type (might be due to invalid IL or missing references)
		//IL_02c7: Unknown result type (might be due to invalid IL or missing references)
		//IL_02d8: Unknown result type (might be due to invalid IL or missing references)
		//IL_08dc: Unknown result type (might be due to invalid IL or missing references)
		//IL_0964: Unknown result type (might be due to invalid IL or missing references)
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.UpdateLocation, MySettingsProperty.Settings.UpdateSize);
		ReplaceQuoteCB.Checked = MySettingsProperty.Settings.ReplaceQuoteCB;
		Quiet = false;
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)AllButton, "Select all of the symbols listed.");
		val.SetToolTip((Control)(object)AllPortsButton, "Update quote files In all portfolios.");
		val.SetToolTip((Control)(object)AlphaVantageRadioButton, "Use https://www.alphavantage.co/ as the source for quote data.");
		val.SetToolTip((Control)(object)AlphaVHelpButton, "Click for an explanation of Alpha Vantage services.");
		val.SetToolTip((Control)(object)APIKeyTextBox, "Provide the API code (everyone except yahoo) assigned you when you registered with their service.");
		val.SetToolTip((Control)(object)AutoRetryCheckBox, "Automatically retry other quote services after receiving a bad quote.");
		val.SetToolTip((Control)(object)BarChartButton, "Get information about Barchart.");
		val.SetToolTip((Control)(object)BarchartRB, "Get quote information from Barchart.");
		val.SetToolTip((Control)(object)BrowseButton, "Locate files containing stock quotes for use by Patternz.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)EODHDButton, "Help for EOD.");
		val.SetToolTip((Control)(object)EodhdRB, "Information about EOD.");
		val.SetToolTip((Control)(object)ErrorListBox, "Errors encountered during update are displayed here.");
		val.SetToolTip((Control)(object)FinnhubButton, "Informaton about Finnhub.io.");
		val.SetToolTip((Control)(object)FinnhubRB, "Get quote informaton from Finnhub.io.");
		val.SetToolTip((Control)(object)FromDatePicker, "Enter the starting date For getting historical quotes.");
		val.SetToolTip((Control)(object)GoogleRadioButton, "Use Google as the source for quote data.");
		val.SetToolTip((Control)(object)HelpButton1, "Get help.");
		val.SetToolTip((Control)(object)HistoricalRadioButton, "Add new quote files, replace existing ones, or speed load times (keep short: 2 years long). WARNING: Erases manually entered splits (see Fix Split Form).");
		val.SetToolTip((Control)(object)IEXButton, "Explains how to use IEX.");
		val.SetToolTip((Control)(object)IEXRadioButton, "Get quote informaton from IEX.");
		val.SetToolTip((Control)(object)LinkLabel, "Legal stuff for IEX.");
		val.SetToolTip((Control)(object)ListBox1, "Quote files appear here, if any.");
		val.SetToolTip((Control)(object)NumericUpDown1, "Alpha Vantage users: Enter maxiumum requests per minute allowed by them. Click Help for more info.");
		val.SetToolTip((Control)(object)RetryButton, "When an error occurs, change quote providers and click retry to get the information from another source.");
		val.SetToolTip((Control)(object)RetryListBox, "When an error occurs, files needing an update are placed here. Click the Retry button to update these files.");
		val.SetToolTip((Control)(object)StartButton, "Begin updating quote files.");
		val.SetToolTip((Control)(object)StockDataHelpButton, "Info about StockData.org.");
		val.SetToolTip((Control)(object)StockDataRB, "Use StockData.org as a data source for quotes.");
		val.SetToolTip((Control)(object)StopButton, "Halt the updating process.");
		val.SetToolTip((Control)(object)SymbolTextBox, "Enter new symbol(s) to add to the list then click Start.");
		val.SetToolTip((Control)(object)TiingoHelpButton, "Provides more information about the Tiingo.com quote service.");
		val.SetToolTip((Control)(object)TiingoRadioButton, "Use https://www.tiingo.com/welcome as the source for quote data.");
		val.SetToolTip((Control)(object)ToDatePicker, "Enter the ending date for getting historical quotes.");
		val.SetToolTip((Control)(object)UnibitRB, "Information about Unibit.");
		val.SetToolTip((Control)(object)UnibitButton, "Help for Unibit.");
		val.SetToolTip((Control)(object)UpdateRadioButton, "Bring quote files up to date. Best if used well after the close.");
		val.SetToolTip((Control)(object)ReplaceQuoteCB, "If updating your quote files before the close, check this box.");
		val.SetToolTip((Control)(object)ReplaceQuoteButton, "Help for the check box.");
		TimerRunFlag = false;
		Timer1.Enabled = false;
		ProgressBar1.Value = 0;
		SymbolTextBox.Text = "";
		StopAsking = false;
		StopPressed = false;
		FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)checked(-1 * GlobalForm.UFDateLookBack), DateAndTime.Now);
		ToDatePicker.Value = DateAndTime.Now;
		((Form)this).Text = "Update Form: " + GlobalForm.OpenPath;
		ListBox ListBox = ListBox1;
		GlobalForm.DisplayFiles(ref ListBox);
		ListBox1 = ListBox;
		SymbolNameCheck();
		if (ListBox1.Items.Count > 0)
		{
			AllButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		}
		else
		{
			((Control)AllButton).Enabled = false;
		}
		try
		{
			string text = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "Captoff", (object)""));
			if (Operators.CompareString(text, "", false) != 0)
			{
				GlobalForm.TiingoKey = new GlobalForm.Simple3Des("da9ba2681").DecryptData(text);
			}
			else
			{
				GlobalForm.TiingoKey = "";
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		try
		{
			string text = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap1", (object)""));
			if (Operators.CompareString(text, "", false) != 0)
			{
				GlobalForm.BarchartKey = new GlobalForm.Simple3Des("FF341EB231C7\u0019").DecryptData(text);
			}
			else
			{
				GlobalForm.BarchartKey = "";
			}
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			ProjectData.ClearProjectError();
		}
		try
		{
			string text = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap2", (object)""));
			if (Operators.CompareString(text, "", false) != 0)
			{
				GlobalForm.FinnhubKey = new GlobalForm.Simple3Des("F712DC14acD5\u0019").DecryptData(text);
			}
			else
			{
				GlobalForm.FinnhubKey = "";
			}
		}
		catch (Exception ex5)
		{
			ProjectData.SetProjectError(ex5);
			Exception ex6 = ex5;
			ProjectData.ClearProjectError();
		}
		try
		{
			string text = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap3", (object)""));
			if (Operators.CompareString(text, "", false) != 0)
			{
				GlobalForm.IEXKey = new GlobalForm.Simple3Des("45EDC2319CBc5\u0019").DecryptData(text);
			}
			else
			{
				GlobalForm.IEXKey = "";
			}
		}
		catch (Exception ex7)
		{
			ProjectData.SetProjectError(ex7);
			Exception ex8 = ex7;
			ProjectData.ClearProjectError();
		}
		try
		{
			string text = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap4", (object)""));
			if (Operators.CompareString(text, "", false) != 0)
			{
				GlobalForm.SDKey = new GlobalForm.Simple3Des("97FAC936qr{=48").DecryptData(text);
			}
			else
			{
				GlobalForm.SDKey = "";
			}
		}
		catch (Exception ex9)
		{
			ProjectData.SetProjectError(ex9);
			Exception ex10 = ex9;
			ProjectData.ClearProjectError();
		}
		try
		{
			string text = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap5", (object)""));
			if (Operators.CompareString(text, "", false) != 0)
			{
				GlobalForm.UnibitKey = new GlobalForm.Simple3Des("10D0A983EB430C").DecryptData(text);
			}
			else
			{
				GlobalForm.UnibitKey = "";
			}
		}
		catch (Exception ex11)
		{
			ProjectData.SetProjectError(ex11);
			Exception ex12 = ex11;
			ProjectData.ClearProjectError();
		}
		try
		{
			string text = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap6", (object)""));
			if (Operators.CompareString(text, "", false) != 0)
			{
				GlobalForm.EODHDKey = new GlobalForm.Simple3Des("04CEA3718DBC40").DecryptData(text);
			}
			else
			{
				GlobalForm.EODHDKey = "";
			}
		}
		catch (Exception ex13)
		{
			ProjectData.SetProjectError(ex13);
			Exception ex14 = ex13;
			ProjectData.ClearProjectError();
		}
		GlobalForm.lsBarchartKey = GlobalForm.BarchartKey;
		GlobalForm.lsFinnhubKey = GlobalForm.FinnhubKey;
		GlobalForm.lsIEXKey = GlobalForm.IEXKey;
		GlobalForm.lsTiingoKey = GlobalForm.TiingoKey;
		GlobalForm.lsSDKey = GlobalForm.SDKey;
		GlobalForm.lsUnibitKey = GlobalForm.UnibitKey;
		GlobalForm.lsEODHDKey = GlobalForm.EODHDKey;
		if (TiingoRadioButton.Checked)
		{
			APIKeyTextBox.Text = GlobalForm.TiingoKey;
		}
		else if (BarchartRB.Checked)
		{
			APIKeyTextBox.Text = GlobalForm.BarchartKey;
		}
		else if (FinnhubRB.Checked)
		{
			APIKeyTextBox.Text = GlobalForm.FinnhubKey;
		}
		else if (IEXRadioButton.Checked)
		{
			APIKeyTextBox.Text = GlobalForm.IEXKey;
		}
		else if (StockDataRB.Checked)
		{
			APIKeyTextBox.Text = GlobalForm.SDKey;
		}
		else if (UnibitRB.Checked)
		{
			APIKeyTextBox.Text = GlobalForm.UnibitKey;
		}
		else if (EodhdRB.Checked)
		{
			APIKeyTextBox.Text = GlobalForm.EODHDKey;
		}
		else
		{
			APIKeyTextBox.Text = "";
		}
		AutoRetryCheckBox.Checked = GlobalForm.AutoRetry;
		AutoStart = -1;
		switch (GlobalForm.UpdatePeriod)
		{
		case 2:
			UpdateRadioButton.Checked = true;
			break;
		case 3:
			HistoricalRadioButton.Checked = true;
			break;
		}
		UpdateRadioButton_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
		HistoricalRadioButton_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
		((Control)ReplaceQuoteCB).Enabled = UpdateRadioButton.Checked;
		switch (GlobalForm.UpdateSource)
		{
		case 8:
			BarchartRB.Checked = true;
			break;
		case 7:
			IEXRadioButton.Checked = true;
			break;
		case 4:
			TiingoRadioButton.Checked = true;
			break;
		case 9:
			StockDataRB.Checked = true;
			if (HistoricalRadioButton.Checked)
			{
				((Control)FromDatePicker).Enabled = false;
			}
			break;
		case 10:
			UnibitRB.Checked = true;
			break;
		case 11:
			EodhdRB.Checked = true;
			break;
		default:
			MessageBox.Show("Note: Alpha Vantage, Finnhub, Quandl, Yahoo, and Google are no longer supported. Pick another quote provider.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			TiingoRadioButton.Checked = true;
			break;
		}
		AllButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		RetryListBox.Items.Clear();
		if ((Operators.CompareString(GlobalForm.UserDate, "yyyy-MM-dd", false) != 0) & (Operators.CompareString(GlobalForm.UserDate, "yyyy/MM/dd", false) != 0) & (Operators.CompareString(GlobalForm.UserDate, "yyyy.MM.dd", false) != 0))
		{
			MessageBox.Show("WARNING: The date format you are using (" + GlobalForm.UserDate + ") does not match the format this (Update) Form uses (yyyy-MM-dd).\r\n\r\nUnless you intend to replace ALL of your files using this form (by selecting 'Get historical quotes'),Patternz will likely crash later (such as when using Chart, List, and so on).\r\n\r\nThis situation can happen when you provide your own data (such as using Metastock to provide .csv files).\r\n\r\nIF YOU ARE PROVIDING YOUR OWN DATA, DO NOT USE THIS (Update) FORM.\r\n\r\nIf you wish Patternz to provide the data (by using this Update Form), then ignore this warning.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)48);
		}
	}

	private void AllButton_Click(object sender, EventArgs e)
	{
		ListBox1.BeginUpdate();
		checked
		{
			int num = ListBox1.Items.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				ListBox1.SetSelected(i, true);
			}
			ListBox1.EndUpdate();
		}
	}

	private void AllPortsButton_Click(object sender, EventArgs e)
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_017f: Unknown result type (might be due to invalid IL or missing references)
		//IL_016a: Unknown result type (might be due to invalid IL or missing references)
		UpdateAllPorts = true;
		GlobalForm.CustomCheckbox = false;
		GlobalForm.CustomResult = (DialogResult)0;
		StopAsking = false;
		Quiet = true;
		StartButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		checked
		{
			if (MyProject.Forms.Mainform.PortfolioDataGridView.RowCount > 0)
			{
				string openPath = GlobalForm.OpenPath;
				int num = MyProject.Forms.Mainform.PortfolioDataGridView.RowCount - 1;
				ListBox ListBox;
				for (int i = 0; i <= num; i++)
				{
					GlobalForm.OpenPath = MyProject.Forms.Mainform.PortfolioDataGridView.Rows[i].Cells[1].Value.ToString();
					MyProject.Forms.Mainform.MFDisplayFiles(BrowseFlag: false);
					ListBox = ListBox1;
					GlobalForm.DisplayFiles(ref ListBox);
					ListBox1 = ListBox;
					SymbolNameCheck();
					if (ListBox1.Items.Count > 0)
					{
						AllButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
						StartButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
					}
					if (StopPressed)
					{
						break;
					}
				}
				GlobalForm.OpenPath = openPath;
				MyProject.Forms.Mainform.MFDisplayFiles(BrowseFlag: false);
				ListBox = ListBox1;
				GlobalForm.DisplayFiles(ref ListBox);
				ListBox1 = ListBox;
				SymbolNameCheck();
				if ((RetryListBox.Items.Count > 0) & AutoRetryCheckBox.Checked)
				{
					MessageBox.Show("I could not update quote files listed in the retry list box.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				}
				else
				{
					MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				}
			}
			Quiet = false;
			UpdateAllPorts = false;
		}
	}

	private void APIKeyTextBox_LostFocus(object sender, EventArgs e)
	{
		//IL_0024: Unknown result type (might be due to invalid IL or missing references)
		if (FinnhubRB.Checked)
		{
			GlobalForm.FinnhubKey = APIKeyTextBox.Text;
			Interaction.MsgBox((object)"Please note that Finnhub is no longer supported. Pick another quote provider.", (MsgBoxStyle)0, (object)null);
		}
		else if (IEXRadioButton.Checked)
		{
			GlobalForm.IEXKey = APIKeyTextBox.Text;
		}
		else if (BarchartRB.Checked)
		{
			GlobalForm.BarchartKey = APIKeyTextBox.Text;
		}
		else if (TiingoRadioButton.Checked)
		{
			GlobalForm.TiingoKey = APIKeyTextBox.Text;
		}
		else if (StockDataRB.Checked)
		{
			GlobalForm.SDKey = APIKeyTextBox.Text;
		}
		else if (UnibitRB.Checked)
		{
			GlobalForm.UnibitKey = APIKeyTextBox.Text;
		}
		else if (EodhdRB.Checked)
		{
			GlobalForm.EODHDKey = APIKeyTextBox.Text;
		}
	}

	private void APIKeyTextBox_TextChanged(object sender, EventArgs e)
	{
		bool flag = true;
		if (flag == FinnhubRB.Checked)
		{
			GlobalForm.FinnhubKey = APIKeyTextBox.Text;
		}
		else if (flag == IEXRadioButton.Checked)
		{
			GlobalForm.IEXKey = APIKeyTextBox.Text;
		}
		else if (flag == BarchartRB.Checked)
		{
			GlobalForm.BarchartKey = APIKeyTextBox.Text;
		}
		else if (flag == TiingoRadioButton.Checked)
		{
			GlobalForm.TiingoKey = APIKeyTextBox.Text;
		}
		else if (flag == StockDataRB.Checked)
		{
			GlobalForm.SDKey = APIKeyTextBox.Text;
		}
		else if (flag == UnibitRB.Checked)
		{
			GlobalForm.UnibitKey = APIKeyTextBox.Text;
		}
		else if (flag == EodhdRB.Checked)
		{
			GlobalForm.EODHDKey = APIKeyTextBox.Text;
		}
	}

	private void BarchartRB_CheckedChanged(object sender, EventArgs e)
	{
		Timer1.Enabled = false;
		if (BarchartRB.Checked)
		{
			((Control)APIKeyTextBox).Enabled = true;
			APIKeyTextBox.Text = GlobalForm.BarchartKey;
			((Control)LinkLabel).Visible = false;
		}
	}

	private void BarChartButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("As of May 5, 2022, barchart (https://www.barchart.com/ondemand) appears to be a subscription-only service.\r\n\r\nYou'll need a API key to use this service.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void BrowseButton_Click(object sender, EventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_0006: Unknown result type (might be due to invalid IL or missing references)
		//IL_0016: Expected O, but got Unknown
		//IL_001c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0022: Invalid comparison between Unknown and I4
		FolderBrowserDialog1 = new FolderBrowserDialog
		{
			Description = "Select the path to the stock quote files."
		};
		if ((int)((CommonDialog)FolderBrowserDialog1).ShowDialog() == 1)
		{
			GlobalForm.PathChanged = true;
			GlobalForm.OpenPath = FolderBrowserDialog1.SelectedPath;
			ListBox ListBox = ListBox1;
			GlobalForm.DisplayFiles(ref ListBox);
			ListBox1 = ListBox;
			SymbolNameCheck();
			((Control)AllButton).Enabled = Conversions.ToBoolean(Interaction.IIf(ListBox1.Items.Count > 0, (object)true, (object)false));
		}
		((Form)this).Text = "Update Form: " + GlobalForm.OpenPath;
	}

	private bool CheckUpdated(string Buffer, string Symbol)
	{
		//IL_003d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0043: Invalid comparison between Unknown and I4
		if (!StopAsking && Strings.InStr(Buffer, Strings.Format((object)DateAndTime.Now, GlobalForm.UserDate), (CompareMethod)0) == 0)
		{
			if ((int)MessageBox.Show("Today's quote information is not available (yet) for " + Symbol + ". Do you want to continue?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32) == 7)
			{
				StopPressed = true;
				return true;
			}
			StopAsking = true;
		}
		return false;
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void ErrorBump()
	{
		checked
		{
			GlobalForm.ErrorCount++;
			Label4.Text = "Error count: " + Strings.Format((object)GlobalForm.ErrorCount, "") + ". Symbols updated properly: " + GlobalForm.GoodCount;
			if (ErrorListBox.Items.Count != 0)
			{
				ErrorListBox.TopIndex = ErrorListBox.Items.Count - 1;
			}
		}
	}

	private void FinnhubButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("As of August 15, 2024, Finnhub.io is no longer suported because they changed their format.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void FinnhubRB_CheckedChanged(object sender, EventArgs e)
	{
		Timer1.Enabled = false;
		if (FinnhubRB.Checked)
		{
			((Control)APIKeyTextBox).Enabled = true;
			APIKeyTextBox.Text = GlobalForm.FinnhubKey;
			((Control)LinkLabel).Visible = false;
		}
	}

	private string GetEOLCode(string Buffer, string Symbol)
	{
		string text = "\r\n";
		while (true)
		{
			if (Strings.InStr(Buffer, text, (CompareMethod)0) != 0)
			{
				return text;
			}
			if (Operators.CompareString(text, "\r\n", false) == 0)
			{
				text = "\n";
				continue;
			}
			if (Operators.CompareString(text, "\n", false) != 0)
			{
				break;
			}
			text = "\r";
		}
		ErrorListBox.Items.Add((object)("Can't find EOL character for: " + Symbol + ". Bad symbol, download limit exceeded, or data not available yet. "));
		ErrorBump();
		return null;
	}

	private string GetExtension(string Symbol)
	{
		int num = Strings.InStrRev(Symbol, ".", -1, (CompareMethod)0);
		if (num == 0)
		{
			return ".csv";
		}
		return Strings.Right(Symbol, checked(Symbol.Length - (num - 1)));
	}

	public void GetHistoricalQuotes(int lbcount)
	{
		//IL_01da: Unknown result type (might be due to invalid IL or missing references)
		//IL_026e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0274: Invalid comparison between Unknown and I4
		//IL_027e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0284: Invalid comparison between Unknown and I4
		//IL_029e: Unknown result type (might be due to invalid IL or missing references)
		//IL_02a4: Unknown result type (might be due to invalid IL or missing references)
		//IL_02aa: Invalid comparison between Unknown and I4
		//IL_00b7: Unknown result type (might be due to invalid IL or missing references)
		string text = "";
		WebRequest webRequest = null;
		GlobalForm.Recursive = false;
		int num = 0;
		DateTime date = FromDatePicker.Value.Date;
		DateTime value = ToDatePicker.Value;
		checked
		{
			if (YahooRadioButton.Checked)
			{
				int num2 = 0;
				while ((Operators.CompareString(Token.Cookie, "", false) == 0) & (Operators.CompareString(Token.Crumb, "", false) == 0))
				{
					Token.Refresh();
					num2++;
					if (num2 >= 3)
					{
						break;
					}
					if ((Operators.CompareString(Token.Cookie, "-1", false) == 0) & (Operators.CompareString(Token.Crumb, "-1", false) == 0))
					{
						Token.Cookie = "";
						Token.Crumb = "";
						if (!Quiet)
						{
							MessageBox.Show("The internet (or yahoo only) may be down. Try another quote provider.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
						}
						return;
					}
				}
			}
			else if (TiingoRadioButton.Checked)
			{
				try
				{
					text = "&startDate=" + Strings.Format((object)date, "yyyy") + "-" + Strings.Format((object)date, "MM") + "-" + Strings.Format((object)date, "dd");
					text = text + "&endDate=" + Strings.Format((object)value, "yyyy") + "-" + Strings.Format((object)value, "MM") + "-" + Strings.Format((object)value, "dd");
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					MessageBox.Show("Check the format of the 'from' and 'to' fields.", "GetHistoricalQuotes", (MessageBoxButtons)0, (MessageBoxIcon)16);
					ProjectData.ClearProjectError();
					return;
				}
			}
			else
			{
				_ = FinnhubRB.Checked;
			}
			do
			{
				GlobalForm.CurrentSymbol = SymbolArray[0, num];
				string extension = GetExtension(SymbolArray[1, num]);
				string text2 = SymbolArray[2, num] + GlobalForm.Swap(":", "_", SymbolArray[1, num]);
				unchecked
				{
					if (!(!RetryChecked & ((ServerComputer)MyProject.Computer).FileSystem.FileExists(text2)) || (((int)GlobalForm.CustomResult == 6) & GlobalForm.CustomCheckbox))
					{
						goto IL_02af;
					}
					if (((int)GlobalForm.CustomResult == 0) | !GlobalForm.CustomCheckbox)
					{
						((Form)MyProject.Forms.CustomDialogBox).ShowDialog();
						if ((int)GlobalForm.CustomResult == 6)
						{
							goto IL_02af;
						}
					}
					goto IL_0901;
				}
				IL_0901:
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				ProgressBar1.Value = (int)Math.Round((double)(100 * num) / (double)lbcount);
				num++;
				continue;
				IL_02af:
				GlobalForm.CurrentSymbol = GlobalForm.Swap("_", ":", GlobalForm.CurrentSymbol);
				Label4.Text = "Processing: " + GlobalForm.CurrentSymbol;
				string Buffer = null;
				StreamReader streamReader = null;
				Stream stream = null;
				WebResponse webResponse = null;
				ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
				try
				{
					if (BarchartRB.Checked)
					{
						webRequest = WebRequest.CreateHttp(GlobalForm.BARCHARTURL + GlobalForm.BarchartKey + "&symbol=" + GlobalForm.CurrentSymbol + "&type=daily&startDate=" + Strings.Format((object)date, "yyyyMMdd"));
					}
					else if (FinnhubRB.Checked)
					{
						DateTime dateTime = FromDatePicker.Value.Date.AddHours(10.0);
						dateTime = DateAndTime.DateAdd((DateInterval)4, -1.0, dateTime);
						string text3 = Conversions.ToString(Historical.DateTimeToUnixTimestamp(dateTime));
						dateTime = ToDatePicker.Value.Date.AddHours(10.0);
						string text4 = Conversions.ToString(Historical.DateTimeToUnixTimestamp(dateTime));
						webRequest = WebRequest.CreateHttp(GlobalForm.FINNURL + "stock/candle?symbol=" + GlobalForm.CurrentSymbol + "&resolution=D&from=" + text3 + "&to=" + text4 + "&format=csv&adjusted=true&token=" + GlobalForm.FinnhubKey);
					}
					else if (IEXRadioButton.Checked)
					{
						long num3 = GetWorkingDates(FromDatePicker.Value.Date, DateAndTime.Now) - 1;
						webRequest = WebRequest.CreateHttp(GlobalForm.IEXURL + GlobalForm.CurrentSymbol + "/chart/max?chartByDay=true&chartLast=" + num3 + "&token=" + GlobalForm.IEXKey + "&format=csv");
					}
					else if (YahooRadioButton.Checked)
					{
						Buffer = Historical.GetRaw(GlobalForm.CurrentSymbol, FromDatePicker.Value, ToDatePicker.Value);
					}
					else if (StockDataRB.Checked)
					{
						webRequest = WebRequest.CreateHttp(GlobalForm.SDURL + GlobalForm.CurrentSymbol + "&sort=asc&date_to=" + Strings.Format((object)value, "yyyy-MM-dd") + "&format=csv&api_token=" + GlobalForm.SDKey);
					}
					else if (UnibitRB.Checked)
					{
						webRequest = WebRequest.CreateHttp(GlobalForm.UNIBITURL + "?tickers=" + GlobalForm.CurrentSymbol + "&startDate=" + Strings.Format((object)date, "yyyy-MM-dd") + "&endDate=" + Strings.Format((object)DateAndTime.Now, "yyyy-MM-dd") + "&dataType=csv&accessKey=" + GlobalForm.UnibitKey);
					}
					else if (EodhdRB.Checked)
					{
						webRequest = WebRequest.CreateHttp(GlobalForm.EODHDURL + GlobalForm.CurrentSymbol + "?from=" + Strings.Format((object)date, "yyyy-MM-dd") + "&to=" + Strings.Format((object)value, "yyyy-MM-dd") + "&period=d&order=a&fmt=csv&api_token=" + GlobalForm.EODHDKey);
					}
					else if (TiingoRadioButton.Checked)
					{
						webRequest = WebRequest.CreateHttp(GlobalForm.TIINGOURL + GlobalForm.CurrentSymbol + "/prices?token=" + APIKeyTextBox.Text + "&format=csv" + text);
					}
					if (!YahooRadioButton.Checked)
					{
						webResponse = webRequest.GetResponse();
						stream = webResponse.GetResponseStream();
						streamReader = new StreamReader(stream);
						Buffer = streamReader.ReadToEnd();
						streamReader.Close();
						streamReader = null;
						stream.Close();
						stream = null;
						webResponse.Close();
						webResponse = null;
					}
					if (Buffer == null)
					{
						HandleRetryLB(GlobalForm.CurrentSymbol);
						ErrorListBox.Items.Add((object)("Bad/changed symbol, bad API key/token, or download limit exceeded? " + GlobalForm.CurrentSymbol));
					}
					else
					{
						Buffer = ProcessData(ref Buffer, GlobalForm.CurrentSymbol, IncludeHeader: true, date, value);
						if (Buffer.Length == 0)
						{
							HandleRetryLB(GlobalForm.CurrentSymbol);
						}
						else
						{
							if (DateTime.Compare(ToDatePicker.Value.Date, DateAndTime.Now.Date) == 0 && CheckUpdated(Buffer, GlobalForm.CurrentSymbol))
							{
								StopPressed = true;
							}
							text2 = GlobalForm.OpenPath + "\\" + GlobalForm.Swap(":", "_", GlobalForm.CurrentSymbol) + extension;
							File.WriteAllText(text2, Buffer);
							GlobalForm.GoodCount++;
							if (!(ListBox1.Items.Contains((object)(Strings.LCase(GlobalForm.CurrentSymbol) + Strings.UCase(extension))) | ListBox1.Items.Contains((object)(Strings.UCase(GlobalForm.CurrentSymbol) + Strings.LCase(extension))) | ListBox1.Items.Contains((object)Strings.UCase(GlobalForm.CurrentSymbol + extension)) | ListBox1.Items.Contains((object)Strings.LCase(GlobalForm.CurrentSymbol + extension))))
							{
								ListBox1.Items.Add((object)(GlobalForm.CurrentSymbol + extension));
							}
							if (RetryChecked)
							{
								int num4 = RetryListBox.FindString(text2);
								if (num4 != -1)
								{
									RetryListBox.Items.RemoveAt(num4);
								}
								if (RetryListBox.Items.Count == 0)
								{
									RetryChecked = false;
								}
							}
						}
					}
				}
				catch (Exception ex3)
				{
					ProjectData.SetProjectError(ex3);
					Exception ex4 = ex3;
					HandleInternetException(ex4, GlobalForm.CurrentSymbol, ref Buffer);
					HandleRetryLB(GlobalForm.CurrentSymbol);
					streamReader?.Close();
					stream?.Close();
					webResponse?.Close();
					ProjectData.ClearProjectError();
				}
				goto IL_0901;
			}
			while (!((num == lbcount) | StopPressed));
		}
	}

	private void GetUpdatedQuotes(int lbCount)
	{
		//IL_00f5: Unknown result type (might be due to invalid IL or missing references)
		//IL_00fb: Invalid comparison between Unknown and I4
		string Buffer = "";
		string HeaderString = "";
		bool UpToDate = false;
		bool flag = false;
		checked
		{
			int num = lbCount - 1;
			DateTime FirstDate = default(DateTime);
			DateTime LastDate = default(DateTime);
			int HeaderPosition = default(int);
			for (int i = 0; i <= num; i++)
			{
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				if (StopPressed)
				{
					break;
				}
				ProgressBar1.Value = (int)Math.Round((double)(100 * i) / (double)lbCount);
				string symbol = SymbolArray[0, i];
				string original = SymbolArray[1, i];
				original = GlobalForm.Swap(":", "_", original);
				bool flag2 = ReadFileGetDates(ref Buffer, original, ref FirstDate, ref LastDate, ref HeaderString, ref HeaderPosition);
				string InternetBuffer;
				unchecked
				{
					if (BarchartRB.Checked && !flag && DateTime.Compare(Conversions.ToDate(Interaction.IIf(DateTime.Compare(LastDate, FirstDate) > 0, (object)LastDate, (object)FirstDate)), DateAndTime.DateAdd((DateInterval)2, -6.0, DateAndTime.Now)) < 0)
					{
						flag = true;
						if ((int)MessageBox.Show("As of August 2020, barchart only provides 6 months of data, so if I continue, it'll leave a data hole in the file(s). Continue anyway?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32, (MessageBoxDefaultButton)256) == 7)
						{
							break;
						}
					}
					if (flag2)
					{
						continue;
					}
					InternetBuffer = "";
				}
				if (!UQuotes(ref InternetBuffer, symbol, GlobalForm.MyCDate(RuntimeHelpers.GetObjectValue(Interaction.IIf(DateTime.Compare(LastDate, FirstDate) > 0, (object)LastDate, (object)FirstDate))), ref UpToDate))
				{
					DateTime fromDate = Conversions.ToDate(Interaction.IIf(DateTime.Compare(LastDate, FirstDate) > 0, (object)LastDate, (object)FirstDate));
					string NewQuote = ProcessData(ref InternetBuffer, symbol, IncludeHeader: false, fromDate, DateAndTime.Now);
					if (NewQuote.Length > 0)
					{
						Buffer = VerifyQuotes(Buffer, ref NewQuote, LastDate);
						File.WriteAllText(SymbolArray[2, i] + original, Buffer);
						GlobalForm.GoodCount++;
					}
					else
					{
						HandleRetryLB(symbol);
					}
					if (CheckUpdated(Buffer, symbol))
					{
						StopPressed = true;
					}
					if (RetryChecked)
					{
						int num2 = RetryListBox.FindString(SymbolArray[2, i] + original);
						if (num2 != -1)
						{
							RetryListBox.Items.RemoveAt(num2);
						}
						if (RetryListBox.Items.Count == 0)
						{
							RetryChecked = false;
						}
					}
				}
				else if (!UpToDate)
				{
					HandleRetryLB(symbol);
				}
			}
		}
	}

	private int GetWorkingDates(DateTime startDate, DateTime endDate)
	{
		List<DateTime> list = new List<DateTime>();
		list = GlobalForm.GetHolidayList(DateAndTime.Year(startDate));
		List<DateTime> list2 = (from n in Enumerable.Range(0, checked(1 + (int)Math.Round((endDate - startDate).TotalDays)))
			select startDate.AddDays(n)).ToList();
		if (list != null)
		{
			list2.RemoveAll([SpecialName] (DateTime d) => list.Contains(d));
		}
		DayOfWeek[] source = new DayOfWeek[2]
		{
			DayOfWeek.Saturday,
			DayOfWeek.Sunday
		};
		list2.RemoveAll([SpecialName] (DateTime d) => source.Contains(d.DayOfWeek));
		return list2.Count;
	}

	private void HandleInternetException(Exception ex, string Symbol, ref string Buffer)
	{
		if (StockDataRB.Checked)
		{
			if (Strings.InStr(ex.Message, "400", (CompareMethod)0) != 0)
			{
				ErrorListBox.Items.Add((object)(ex.Message + " Validation of parameters failed."));
			}
			else if (Strings.InStr(ex.Message, "401", (CompareMethod)0) != 0)
			{
				ErrorListBox.Items.Add((object)(ex.Message + " Bad API key/token."));
			}
			else if (Strings.InStr(ex.Message, "402", (CompareMethod)0) != 0)
			{
				ErrorListBox.Items.Add((object)(ex.Message + " Usage limit of your plan has been reached."));
			}
			else if (Strings.InStr(ex.Message, "403", (CompareMethod)0) != 0)
			{
				ErrorListBox.Items.Add((object)(ex.Message + " Access isn't allowed on your subscription."));
			}
			else if (Strings.InStr(ex.Message, "404", (CompareMethod)0) != 0)
			{
				ErrorListBox.Items.Add((object)(ex.Message + " Resource not found or API route doesn't exist."));
			}
			else if (Strings.InStr(ex.Message, "429", (CompareMethod)0) != 0)
			{
				ErrorListBox.Items.Add((object)(ex.Message + " Too many requests in the past 60 seconds."));
			}
			else if (Strings.InStr(ex.Message, "500", (CompareMethod)0) != 0)
			{
				ErrorListBox.Items.Add((object)(ex.Message + " A server error occured. Visit StockData.org"));
			}
			else if (Strings.InStr(ex.Message, "503", (CompareMethod)0) != 0)
			{
				ErrorListBox.Items.Add((object)(ex.Message + " Service under maintenance. Visit StockData.org"));
			}
		}
		else if (UnibitRB.Checked)
		{
			if (Strings.InStr(ex.Message, "400", (CompareMethod)0) != 0)
			{
				ErrorListBox.Items.Add((object)(ex.Message + " Bad request."));
			}
			else if (Strings.InStr(ex.Message, "403", (CompareMethod)0) != 0)
			{
				ErrorListBox.Items.Add((object)(ex.Message + " Forbidden: too many requests or plan expired."));
			}
			else if (Strings.InStr(ex.Message, "404", (CompareMethod)0) != 0)
			{
				ErrorListBox.Items.Add((object)(ex.Message + " Data not found. Bad ticker symbol?"));
			}
		}
		else if (EodhdRB.Checked)
		{
			ErrorListBox.Items.Add((object)(ex.Message + ". Remember: Add exchange to symbol as in AAPL.US. See https://eodhistoricaldata.com/financial-apis/list-supported-exchanges/. " + Symbol));
		}
		else if (Strings.InStr(ex.Message, "404", (CompareMethod)0) != 0)
		{
			ErrorListBox.Items.Add((object)("Quotes unavailable from website yet (likely) or unknown/changed symbol: " + Symbol));
		}
		else if (Strings.InStr(ex.Message, "400", (CompareMethod)0) != 0)
		{
			ErrorListBox.Items.Add((object)("Bad/changed symbol or bad API key/token? " + Symbol));
		}
		else if (Strings.InStr(ex.Message, "401", (CompareMethod)0) != 0)
		{
			if (TiingoRadioButton.Checked)
			{
				ErrorListBox.Items.Add((object)"Bad API key/token?");
			}
			else
			{
				ErrorListBox.Items.Add((object)(ex.Message + ": " + Symbol));
			}
		}
		else if (Strings.InStr(ex.Message, "402", (CompareMethod)0) != 0)
		{
			if (IEXRadioButton.Checked)
			{
				ErrorListBox.Items.Add((object)"You have exceeded your allotted message quota.");
			}
		}
		else if (TiingoRadioButton.Checked)
		{
			if (Buffer == null)
			{
				ErrorListBox.Items.Add((object)Strings.Left(Symbol + ": " + ex.Message, 120));
			}
			else
			{
				ErrorListBox.Items.Add((object)Strings.Left(Symbol + ": " + Buffer, 120));
			}
		}
		else if (Strings.InStr(ex.Message, "429", (CompareMethod)0) != 0)
		{
			if (FinnhubRB.Checked)
			{
				Label4.Text = "Pausing 1 minute because of FinnHub rate limit.";
				Timer1.Interval = 60000;
				TimerRunFlag = false;
				Timer1.Enabled = true;
				do
				{
					if (StopPressed)
					{
						Interaction.Beep();
						Timer1.Enabled = false;
						break;
					}
					((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				}
				while (!TimerRunFlag);
				Label4.Text = "Continuing... You may need to download " + Symbol + " again.";
			}
			ErrorListBox.Items.Add((object)("Error 429: FinnHub rate limit exceeded. Symbol: " + Symbol));
		}
		else
		{
			ErrorListBox.Items.Add((object)("Internet unavailable (anti-virus software blocking access?) or bad key/token? " + Symbol));
			ErrorListBox.Items.Add((object)(Symbol + ": " + ex.Message));
		}
		ErrorBump();
	}

	private void HandleRetryLB(string Symbol)
	{
		int num = ListBox1.FindString(Symbol + ".");
		if (num != -1)
		{
			string text = GlobalForm.OpenPath + "\\" + ListBox1.Items[num].ToString();
			if (RetryListBox.FindStringExact(text) == -1)
			{
				RetryListBox.Items.Add((object)text);
			}
		}
		else if (RetryListBox.FindStringExact(GlobalForm.OpenPath + "\\" + Symbol + ".csv") == -1)
		{
			RetryListBox.Items.Add((object)(GlobalForm.OpenPath + "\\" + Symbol + ".csv"));
		}
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.UpdateHelpForm).ShowDialog();
	}

	private void HistoricalRadioButton_CheckedChanged(object sender, EventArgs e)
	{
		bool flag = HistoricalRadioButton.Checked;
		((Control)FromDatePicker).Enabled = flag;
		((Control)ToDatePicker).Enabled = flag;
		((Control)SymbolTextBox).Enabled = flag;
		if (HistoricalRadioButton.Checked & IEXRadioButton.Checked)
		{
			Label4.Text = IEXWarning;
		}
		else
		{
			Label4.Text = "";
		}
		if (HistoricalRadioButton.Checked & StockDataRB.Checked)
		{
			((Control)FromDatePicker).Enabled = false;
		}
		((Control)ReplaceQuoteCB).Enabled = !flag;
	}

	private void IEXButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("The free plan can access only 50 days of price data on the top 500 U.S. stocks as of May 5, 2022, and making a lot of calls chews up the allowed monthly 50,000 credits fast.\r\n\r\nFor historical quotes, this provider is not a good choice.\r\n\r\nFor 'start from last update', it might work for a few symbols providing the last quote is not older than 50 days.\r\n\r\nYou'll need a API key to use this service.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void IEXRadioButton_CheckedChanged(object sender, EventArgs e)
	{
		Timer1.Enabled = false;
		if (IEXRadioButton.Checked)
		{
			if (HistoricalRadioButton.Checked)
			{
				Label4.Text = IEXWarning;
			}
			else
			{
				Label4.Text = "";
			}
			((Control)LinkLabel).Visible = true;
			((Control)APIKeyTextBox).Enabled = true;
			APIKeyTextBox.Text = GlobalForm.IEXKey;
		}
		else
		{
			Label4.Text = "";
			((Control)LinkLabel).Visible = false;
		}
	}

	private void LinkLabel_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
	{
		LinkLabel.LinkVisited = true;
		Process.Start("https://iexcloud.io");
	}

	private void ListBox1_KeyUp(object sender, KeyEventArgs e)
	{
		e.Handled = GlobalForm.ListBoxHandler(e, ListBox1, ColonChange: true);
	}

	private string ProcessData(ref string Buffer, string Symbol, bool IncludeHeader, DateTime FromDate, DateTime ToDate)
	{
		string text = "";
		int[] array = new int[10];
		string text2 = "";
		DateTime t = DateTime.MinValue;
		DateTime dateTime = DateTime.MinValue;
		bool flag = true;
		int num = ((flag == BarchartRB.Checked) ? 8 : ((flag == FinnhubRB.Checked) ? 6 : ((flag == IEXRadioButton.Checked) ? 7 : ((flag == TiingoRadioButton.Checked) ? 4 : ((flag == StockDataRB.Checked) ? 9 : ((flag == UnibitRB.Checked) ? 10 : ((flag != EodhdRB.Checked) ? 4 : 11)))))));
		if (Buffer != null)
		{
			Buffer = Buffer.Replace("\n", "\r\n");
			if (BarchartRB.Checked)
			{
				Buffer = Buffer.Replace("\r\r\n", "\r\n");
				Buffer = Buffer.Replace("\"", "");
			}
		}
		string eOLCode = GetEOLCode(Buffer, Symbol);
		checked
		{
			if (Operators.CompareString(eOLCode, (string)null, false) != 0)
			{
				int num2 = Strings.InStr(Buffer, eOLCode, (CompareMethod)0);
				string text3 = Strings.Left(Buffer, num2 - (eOLCode.Length - 1));
				string text4 = GlobalForm.ClosestDelimiter(text3);
				if (Operators.CompareString(text4, "-1", false) == 0)
				{
					ErrorListBox.Items.Add((object)("Can't find column delimiter in: " + Symbol + ". "));
					ErrorBump();
					return "";
				}
				if ((Strings.InStr(Strings.UCase(text3), "DATE", (CompareMethod)0) != 0) | FinnhubRB.Checked | (BarchartRB.Checked & (Strings.InStr(Strings.UCase(text3), "TIMESTAMP", (CompareMethod)0) != 0)))
				{
					text = Strings.Right(Buffer, Strings.Len(Buffer) - (num2 + 1));
					if (text.Length == 0)
					{
						return text;
					}
					string[] array2 = Regex.Split(text3, text4);
					int num3 = 0;
					string[] array3 = array2;
					for (int i = 0; i < array3.Length; i++)
					{
						switch (Strings.UCase(array3[i]))
						{
						case "DATE":
						case "T":
						case "TRADINGDAY":
							array[0] = num3;
							break;
						case "OPEN":
						case "O":
							array[2] = num3;
							break;
						case "HIGH":
						case "H":
							array[3] = num3;
							break;
						case "LOW":
						case "L":
							array[4] = num3;
							break;
						case "CLOSE":
						case "C":
							array[5] = num3;
							break;
						case "VOLUME":
						case "TOTAL TRADE QUANTITY":
						case "V":
							array[6] = num3;
							break;
						case "DIVCASH":
						case "EX-DIVIDEND":
							array[8] = num3;
							break;
						case "SPLITFACTOR":
						case "SPLIT RATIO":
							array[9] = num3;
							break;
						case "ADJCLOSE":
						case "ADJ. CLOSE":
							if (num != 1)
							{
								array[5] = num3;
							}
							break;
						case "ADJOPEN":
						case "ADJ. OPEN":
							array[2] = num3;
							break;
						case "ADJHIGH":
						case "ADJ. HIGH":
							array[3] = num3;
							break;
						case "ADJLOW":
						case "ADJ. LOW":
							array[4] = num3;
							break;
						case "ADJVOLUME":
						case "ADJ. VOLUME":
							array[6] = num3;
							break;
						}
						num3++;
					}
					num2 = Strings.InStr(Buffer, "\r\n", (CompareMethod)0) + "\r\n".Length;
					int num4 = num2;
					text = ((!IncludeHeader) ? "" : "Date,Open,High,Low,Close,Volume\r\n");
					while (true)
					{
						try
						{
							if (num4 >= Buffer.Length)
							{
								break;
							}
							text2 = Strings.Right(Buffer, Buffer.Length - (num4 - 1));
							if (text2.Length != 0)
							{
								num2 = Strings.InStr(text2, "\r\n", (CompareMethod)0) + "\r\n".Length;
								if (num2 > "\r\n".Length)
								{
									goto IL_0802;
								}
								if (text2.Length > "\r\n".Length)
								{
									text2 += "\r\n";
									num2 = Strings.InStr(text2, "\r\n", (CompareMethod)0) + "\r\n".Length;
									goto IL_0802;
								}
							}
							goto end_IL_0768;
							IL_0a86:
							num4 += num2 - 1;
							continue;
							IL_0802:
							text2 = Strings.Mid(text2, 1, num2 - "\r\n".Length - 1);
							if (num == 9)
							{
								text2 = text2.Replace("T", " ");
								text2 = text2.Replace("Z", "");
							}
							string[] array4;
							if (Strings.InStr(text2, "null", (CompareMethod)0) == 0)
							{
								array4 = Regex.Split(text2, text4);
								array4[array[0]] = array4[array[0]].Replace("T", " ");
								string text5 = text;
								decimal d = new decimal(Conversion.Val(array4[array[6]]));
								if ((decimal.Compare(d, 0m) != 0) | ((decimal.Compare(d, 0m) == 0) & (Conversion.Val(array4[array[3]]) != 0.0) & (Conversion.Val(array4[array[4]]) != 0.0)))
								{
									DateTime dateTime2;
									if (FinnhubRB.Checked)
									{
										dateTime2 = Historical.UnixTimestampToDateTime(Conversions.ToDouble(array4[array[0]]));
										text = text + Strings.Format((object)dateTime2, "yyyy-MM-dd") + ",";
										if (DateTime.Compare(t, DateTime.MinValue) == 0)
										{
											t = dateTime2;
										}
										else if (DateTime.Compare(dateTime, DateTime.MinValue) == 0)
										{
											dateTime = dateTime2;
										}
									}
									else
									{
										text = text + Strings.Format((object)GlobalForm.MyCDate(array4[array[0]]), "yyyy-MM-dd") + ",";
										dateTime2 = GlobalForm.MyCDate(array4[array[0]]);
										if (DateTime.Compare(t, DateTime.MinValue) == 0)
										{
											t = GlobalForm.MyCDate(array4[array[0]]);
										}
										else if (DateTime.Compare(dateTime, DateTime.MinValue) == 0)
										{
											dateTime = GlobalForm.MyCDate(array4[array[0]]);
										}
									}
									if (FinnhubRB.Checked)
									{
										if (!((DateTime.Compare(dateTime2.Date, FromDate.Date) < 0) | (DateTime.Compare(dateTime2.Date, ToDate.Date) > 0)))
										{
											goto IL_0a27;
										}
										text = text5;
									}
									else
									{
										if (!((DateTime.Compare(dateTime2, FromDate) < 0) | (DateTime.Compare(dateTime2, ToDate) > 0)))
										{
											goto IL_0a27;
										}
										text = text5;
									}
								}
							}
							goto IL_0a86;
							IL_0a27:
							text = text + array4[array[2]] + ",";
							text = text + array4[array[3]] + ",";
							text = text + array4[array[4]] + ",";
							text = text + array4[array[5]] + ",";
							text = text + array4[array[6]] + "\r\n";
							goto IL_0a86;
							end_IL_0768:;
						}
						catch (Exception ex)
						{
							ProjectData.SetProjectError(ex);
							Exception ex2 = ex;
							num4 += num2 - 1;
							ProjectData.ClearProjectError();
							continue;
						}
						break;
					}
					if ((DateTime.Compare(t, dateTime) > 0) & (DateTime.Compare(dateTime, DateTime.MinValue) != 0))
					{
						string text6 = "";
						int num5 = text.Length;
						try
						{
							while (true)
							{
								num2 = Strings.InStrRev(text, "\r\n", num5 - "\r\n".Length, (CompareMethod)0);
								if (num2 == 0)
								{
									if (Strings.InStr(Strings.Left(text, Strings.InStr(text, "\r\n", (CompareMethod)0) + "\r\n".Length - 1).ToUpper(), "DATE", (CompareMethod)0) == 0)
									{
										text6 += Strings.Left(text, Strings.InStr(text, "\r\n", (CompareMethod)0) + "\r\n".Length - 1);
									}
									break;
								}
								if (num5 - num2 > 0)
								{
									text2 = Strings.Mid(text, num2 + "\r\n".Length, num5 - num2);
									text6 += text2;
									num5 = num2;
									continue;
								}
								break;
							}
						}
						catch (Exception ex3)
						{
							ProjectData.SetProjectError(ex3);
							Exception ex4 = ex3;
							ProjectData.ClearProjectError();
						}
						text = ((!IncludeHeader) ? text6 : ("Date,Open,High,Low,Close,Volume\r\n" + text6));
					}
					return text;
				}
				ErrorListBox.Items.Add((object)("Can't find header in: " + Symbol + ". "));
				ErrorBump();
				return "";
			}
			return "";
		}
	}

	private bool ReadFileGetDates(ref string Buffer, string FileName, ref DateTime FirstDate, ref DateTime LastDate, ref string HeaderString, ref int HeaderPosition)
	{
		string text = GlobalForm.OpenPath + "\\" + FileName;
		if ((Strings.InStrRev(text.ToLower(), ".csv", -1, (CompareMethod)0) == 0) & (Strings.InStrRev(text.ToLower(), ".txt", -1, (CompareMethod)0) == 0))
		{
			text += GetExtension(FileName);
		}
		bool result;
		checked
		{
			try
			{
				if (FileSystem.FileLen(text) == 0L)
				{
					FirstDate = DateAndTime.DateAdd((DateInterval)0, -2.0, DateAndTime.Now);
					LastDate = FirstDate;
					result = false;
					goto IL_0577;
				}
				Buffer = ((ServerComputer)MyProject.Computer).FileSystem.ReadAllText(text);
				string eOLCode = GetEOLCode(Buffer, FileName);
				if (Operators.CompareString(eOLCode, (string)null, false) != 0)
				{
					int num = Strings.InStr(Buffer, eOLCode, (CompareMethod)0) + eOLCode.Length;
					string text2 = (HeaderString = (RecentLine = Strings.Left(Buffer, num - 1)));
					HeaderPosition = num;
					string text3 = GlobalForm.ClosestDelimiter(text2);
					if (Operators.CompareString(text3, "-1", false) == 0)
					{
						ErrorListBox.Items.Add((object)("Can't find column delimiter in: " + FileName + ". "));
						ErrorBump();
					}
					else
					{
						FileDelimiter = text3;
						string[] array = Regex.Split(text2, text3);
						if (Strings.InStr(Strings.UCase(text2), "DATE", (CompareMethod)0) != 0)
						{
							int num2 = 0;
							bool flag = false;
							string[] array2 = array;
							for (int i = 0; i < array2.Length; i++)
							{
								string text4 = array2[i];
								text4 = Strings.UCase(text4);
								if (Strings.Trim(text4).Length != 0)
								{
									if ((Operators.CompareString(text4, "DATE", false) == 0) | (Operators.CompareString(text4, "DATE" + eOLCode, false) == 0))
									{
										flag = true;
										break;
									}
									num2++;
								}
							}
							if (!flag)
							{
								ErrorListBox.Items.Add((object)("Date column not found in: " + FileName + ". "));
								ErrorBump();
								result = true;
								goto IL_0577;
							}
							int num3 = Strings.InStr(num, Buffer, eOLCode, (CompareMethod)0);
							array = Regex.Split(RecentLine = Strings.Mid(Buffer, num, num3 - num + eOLCode.Length), text3);
							if (ReturnDate(array, ref FirstDate, 0, num2))
							{
								ErrorListBox.Items.Add((object)("Ending date not found in: " + FileName + ". "));
								ErrorBump();
								result = true;
								goto IL_0577;
							}
							int num4 = 0;
							int num5 = Buffer.Length - 1;
							if ((Operators.CompareString(Conversions.ToString(Buffer[num5]), "\n", false) == 0) | (Operators.CompareString(Conversions.ToString(Buffer[num5]), "\r", false) == 0))
							{
								num4 = 1;
							}
							if ((Operators.CompareString(Conversions.ToString(Buffer[num5 - 1]), "\n", false) == 0) | (Operators.CompareString(Conversions.ToString(Buffer[num5 - 1]), "\r", false) == 0))
							{
								num4++;
							}
							num3 = Strings.InStrRev(Buffer, eOLCode, Buffer.Length - num4, (CompareMethod)0);
							text2 = Strings.Right(Buffer, Buffer.Length - (num3 + eOLCode.Length - 1));
							array = Regex.Split(text2, text3);
							if (ReturnDate(array, ref LastDate, 0, num2))
							{
								ErrorListBox.Items.Add((object)("Ending Date not found in: " + FileName + ". "));
								ErrorBump();
								result = true;
								goto IL_0577;
							}
							if (DateTime.Compare(FirstDate, LastDate) < 0)
							{
								RecentLine = text2;
							}
						}
						else
						{
							HeaderString = null;
							HeaderPosition = 0;
							if (ReturnDate(array, ref FirstDate, 1, GlobalForm.FileFormat[0]))
							{
								ErrorListBox.Items.Add((object)("Beginning date not found in: " + FileName + ". "));
								ErrorBump();
								result = true;
								goto IL_0577;
							}
							int num4 = 0;
							int num5 = Buffer.Length - 1;
							if ((Operators.CompareString(Conversions.ToString(Buffer[num5]), "\n", false) == 0) | (Operators.CompareString(Conversions.ToString(Buffer[num5]), "\r", false) == 0))
							{
								num4 = 1;
							}
							if ((Operators.CompareString(Conversions.ToString(Buffer[num5 - 1]), "\n", false) == 0) | (Operators.CompareString(Conversions.ToString(Buffer[num5 - 1]), "\r", false) == 0))
							{
								num4++;
							}
							int num3 = Strings.InStrRev(Buffer, eOLCode, Buffer.Length - num4, (CompareMethod)0);
							text2 = Strings.Right(Buffer, Buffer.Length - (num3 + eOLCode.Length - 1));
							array = Regex.Split(text2, text3);
							if (ReturnDate(array, ref LastDate, 1, GlobalForm.FileFormat[0]))
							{
								ErrorListBox.Items.Add((object)("Last date not found in: " + FileName + ". "));
								ErrorBump();
								result = true;
								goto IL_0577;
							}
							if (DateTime.Compare(FirstDate, LastDate) < 0)
							{
								RecentLine = text2;
							}
						}
					}
				}
			}
			catch (OutOfMemoryException ex)
			{
				ProjectData.SetProjectError((Exception)ex);
				OutOfMemoryException ex2 = ex;
				ErrorListBox.Items.Add((object)("Error with: " + FileName + ". "));
				ErrorBump();
				result = true;
				ProjectData.ClearProjectError();
				goto IL_0577;
			}
			catch (Exception ex3)
			{
				ProjectData.SetProjectError(ex3);
				Exception ex4 = ex3;
				ErrorListBox.Items.Add((object)("Error with: " + FileName + ". " + ex4.Message));
				ErrorBump();
				result = true;
				ProjectData.ClearProjectError();
				goto IL_0577;
			}
			result = false;
			goto IL_0577;
		}
		IL_0577:
		return result;
	}

	private void RetryButton_Click(object sender, EventArgs e)
	{
		//IL_0007: Unknown result type (might be due to invalid IL or missing references)
		GlobalForm.CustomCheckbox = false;
		GlobalForm.CustomResult = (DialogResult)0;
		RetryChecked = true;
		StartButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		RetryChecked = false;
	}

	private bool ReturnDate(string[] SubStrings, ref DateTime FoundDate, int Init, int Column)
	{
		int num = Init;
		foreach (string phrase in SubStrings)
		{
			if (num == Column)
			{
				if (!GlobalForm.IsDate(phrase))
				{
					break;
				}
				FoundDate = GlobalForm.MyCDate(phrase);
				return false;
			}
			num = checked(num + 1);
		}
		return true;
	}

	private void StartButton_Click(object sender, EventArgs e)
	{
		//IL_008b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0090: Unknown result type (might be due to invalid IL or missing references)
		//IL_0091: Unknown result type (might be due to invalid IL or missing references)
		//IL_0093: Invalid comparison between Unknown and I4
		//IL_00c1: Unknown result type (might be due to invalid IL or missing references)
		//IL_0447: Unknown result type (might be due to invalid IL or missing references)
		//IL_0129: Unknown result type (might be due to invalid IL or missing references)
		//IL_047f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0484: Unknown result type (might be due to invalid IL or missing references)
		//IL_046f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0190: Unknown result type (might be due to invalid IL or missing references)
		//IL_0187: Unknown result type (might be due to invalid IL or missing references)
		//IL_018c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0485: Unknown result type (might be due to invalid IL or missing references)
		//IL_0487: Invalid comparison between Unknown and I4
		//IL_0191: Unknown result type (might be due to invalid IL or missing references)
		//IL_0193: Invalid comparison between Unknown and I4
		//IL_0e29: Unknown result type (might be due to invalid IL or missing references)
		//IL_0e14: Unknown result type (might be due to invalid IL or missing references)
		//IL_0dff: Unknown result type (might be due to invalid IL or missing references)
		if (!Quiet)
		{
			StopAsking = false;
		}
		GlobalForm.Recursive = false;
		if ((TiingoRadioButton.Checked | FinnhubRB.Checked | IEXRadioButton.Checked | BarchartRB.Checked | StockDataRB.Checked | UnibitRB.Checked | EodhdRB.Checked) & (APIKeyTextBox.Text.Length == 0))
		{
			DialogResult val = MessageBox.Show("Most quote providers require an API token/key. Did you want to continue anyway?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32);
			if ((int)val == 7)
			{
				((Control)APIKeyTextBox).Focus();
				return;
			}
		}
		ErrorListBox.Items.Clear();
		if (!UpdateAllPorts)
		{
			GlobalForm.CustomCheckbox = false;
			GlobalForm.CustomResult = (DialogResult)0;
		}
		checked
		{
			int num;
			if (!RetryChecked)
			{
				if ((ListBox1.Items.Count == 0) & (Operators.CompareString(Strings.Trim(SymbolTextBox.Text), "", false) == 0))
				{
					HistoricalRadioButton.Checked = true;
					if (!Quiet)
					{
						MessageBox.Show("Please enter one or more symbols into the text box (each of them separated by a space) then click Start.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
						((Control)SymbolTextBox).Focus();
					}
					return;
				}
				num = ListBox1.SelectedIndices.Count;
				unchecked
				{
					if (Operators.CompareString(Strings.Trim(SymbolTextBox.Text), "", false) == 0 && num == 0)
					{
						DialogResult val = (Quiet ? ((DialogResult)6) : MessageBox.Show("No symbols have been selected in the listbox. Did you want me to select them all?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32));
						if ((int)val != 6)
						{
							return;
						}
						AllButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
						num = ListBox1.SelectedIndices.Count;
					}
				}
				if (Operators.CompareString(SymbolTextBox.Text, "", false) != 0)
				{
					string[] array = Strings.Split(Strings.Trim(SymbolTextBox.Text), " ", -1, (CompareMethod)0);
					num = 0;
					int num2 = array.Length - 1;
					for (int i = 0; i <= num2; i++)
					{
						if (Operators.CompareString(array[i], "", false) != 0)
						{
							ref string[,] symbolArray = ref SymbolArray;
							symbolArray = (string[,])Utils.CopyArray((Array)symbolArray, (Array)new string[3, num + 1]);
							SymbolArray[0, num] = array[i];
							SymbolArray[1, num] = array[i] + ".csv";
							SymbolArray[2, num] = GlobalForm.OpenPath + "\\";
							num++;
						}
					}
					if (HistoricalRadioButton.Checked)
					{
						if (ListBox1.SelectedIndices.Count > 0)
						{
							ref string[,] symbolArray2 = ref SymbolArray;
							symbolArray2 = (string[,])Utils.CopyArray((Array)symbolArray2, (Array)new string[3, num - 1 + ListBox1.SelectedIndices.Count + 1]);
							int num3 = num;
							int num4 = Information.UBound((Array)SymbolArray, 2);
							for (int i = num3; i <= num4; i++)
							{
								string text = ListBox1.SelectedItems[i - num].ToString();
								SymbolArray[0, i] = Strings.Left(text, Strings.InStrRev(text, ".", -1, (CompareMethod)0) - 1);
								SymbolArray[1, i] = text;
								SymbolArray[2, i] = GlobalForm.OpenPath + "\\";
							}
						}
						num = Information.UBound((Array)SymbolArray, 2) + 1;
					}
					else
					{
						ref string[,] symbolArray3 = ref SymbolArray;
						symbolArray3 = (string[,])Utils.CopyArray((Array)symbolArray3, (Array)new string[3, num - 1 + 1]);
					}
				}
				else
				{
					SymbolArray = new string[3, num - 1 + 1];
					int num5 = num - 1;
					for (int i = 0; i <= num5; i++)
					{
						string text = ListBox1.SelectedItems[i].ToString();
						SymbolArray[0, i] = Strings.Left(text, Strings.InStrRev(text, ".", -1, (CompareMethod)0) - 1);
						SymbolArray[1, i] = text;
						SymbolArray[2, i] = GlobalForm.OpenPath + "\\";
					}
				}
			}
			else
			{
				if (RetryListBox.Items.Count == 0)
				{
					MessageBox.Show("No symbols are in the retry list box, so there's nothing to retry.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
					return;
				}
				num = RetryListBox.SelectedIndices.Count;
				if (num == 0)
				{
					DialogResult val = ((AutoStart == -1) ? MessageBox.Show("Did you want me to process all symbols in the retry list box?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32) : ((DialogResult)6));
					if (unchecked((int)val) != 6)
					{
						return;
					}
					RetryListBox.BeginUpdate();
					int num6 = RetryListBox.Items.Count - 1;
					for (int j = 0; j <= num6; j++)
					{
						RetryListBox.SetSelected(j, true);
					}
					RetryListBox.EndUpdate();
					num = RetryListBox.SelectedIndices.Count;
				}
				SymbolArray = new string[3, num - 1 + 1];
				int num7 = num - 1;
				for (int i = 0; i <= num7; i++)
				{
					string text = RetryListBox.SelectedItems[i].ToString();
					string text2 = Strings.Right(text, text.Length - Strings.InStrRev(text, "\\", -1, (CompareMethod)0));
					SymbolArray[0, i] = Strings.Left(text2, Strings.InStrRev(text2, ".", -1, (CompareMethod)0) - 1);
					SymbolArray[1, i] = text2;
					SymbolArray[2, i] = Strings.Left(text, text.Length - text2.Length);
				}
			}
			GlobalForm.FileFormat[0] = 1;
			GlobalForm.FileFormat[1] = 0;
			GlobalForm.FileFormat[2] = 2;
			GlobalForm.FileFormat[3] = 3;
			GlobalForm.FileFormat[4] = 4;
			GlobalForm.FileFormat[5] = 5;
			GlobalForm.FileFormat[6] = 6;
			GlobalForm.FileFormat[7] = 0;
			GlobalForm.UserDate = "yyyy-MM-dd";
			GlobalForm.ckFileFormat[0] = true;
			GlobalForm.ckFileFormat[1] = false;
			GlobalForm.ckFileFormat[2] = true;
			GlobalForm.ckFileFormat[3] = true;
			GlobalForm.ckFileFormat[4] = true;
			GlobalForm.ckFileFormat[5] = true;
			GlobalForm.ckFileFormat[6] = true;
			GlobalForm.ckFileFormat[7] = false;
			StopPressed = false;
			((Control)AllButton).Enabled = false;
			((Control)AllPortsButton).Enabled = false;
			((Control)APIKeyTextBox).Enabled = false;
			((Control)AutoRetryCheckBox).Enabled = false;
			((Control)BarchartRB).Enabled = false;
			((Control)BarChartButton).Enabled = false;
			((Control)BrowseButton).Enabled = false;
			((Control)DoneButton).Enabled = false;
			((Control)ErrorListBox).Enabled = false;
			((Control)EodhdRB).Enabled = false;
			((Control)EODHDButton).Enabled = false;
			((Control)FinnhubRB).Enabled = false;
			((Control)FinnhubButton).Enabled = false;
			((Control)FromDatePicker).Enabled = false;
			((Control)HelpButton1).Enabled = false;
			((Control)HistoricalRadioButton).Enabled = false;
			((Control)IEXRadioButton).Enabled = false;
			((Control)IEXButton).Enabled = false;
			((Control)ListBox1).Enabled = false;
			((Control)NumericUpDown1).Enabled = false;
			((Control)ReplaceQuoteButton).Enabled = false;
			((Control)RetryButton).Enabled = false;
			((Control)RetryListBox).Enabled = false;
			((Control)StartButton).Enabled = false;
			((Control)StockDataRB).Enabled = false;
			((Control)StockDataHelpButton).Enabled = false;
			((Control)StopButton).Enabled = true;
			((Control)SymbolTextBox).Enabled = false;
			((Control)TiingoHelpButton).Enabled = false;
			((Control)TiingoRadioButton).Enabled = false;
			((Control)ToDatePicker).Enabled = false;
			((Control)UnibitRB).Enabled = false;
			((Control)UnibitButton).Enabled = false;
			((Control)UpdateRadioButton).Enabled = false;
			ProgressBar1.Value = 0;
			Label4.Text = "";
			GlobalForm.ErrorCount = 0;
			GlobalForm.GoodCount = 0;
			if (HistoricalRadioButton.Checked)
			{
				DateTimePicker fromDatePicker = FromDatePicker;
				DateTime FromDate = fromDatePicker.Value;
				DateTimePicker toDatePicker;
				DateTime ToDate = (toDatePicker = ToDatePicker).Value;
				GlobalForm.SwapDates(ref FromDate, ref ToDate);
				toDatePicker.Value = ToDate;
				fromDatePicker.Value = FromDate;
				GetHistoricalQuotes(num);
			}
			else if (UpdateRadioButton.Checked)
			{
				GetUpdatedQuotes(num);
			}
			((Control)UpdateRadioButton).Enabled = true;
			((Control)UnibitButton).Enabled = true;
			((Control)UnibitRB).Enabled = true;
			((Control)TiingoRadioButton).Enabled = true;
			((Control)TiingoHelpButton).Enabled = true;
			((Control)StopButton).Enabled = false;
			((Control)StockDataHelpButton).Enabled = true;
			((Control)StockDataRB).Enabled = true;
			((Control)StartButton).Enabled = true;
			((Control)RetryListBox).Enabled = true;
			((Control)RetryButton).Enabled = true;
			((Control)ReplaceQuoteButton).Enabled = true;
			((Control)NumericUpDown1).Enabled = true;
			((Control)ListBox1).Enabled = true;
			((Control)IEXRadioButton).Enabled = true;
			((Control)IEXButton).Enabled = true;
			((Control)HistoricalRadioButton).Enabled = true;
			((Control)HelpButton1).Enabled = true;
			((Control)FinnhubButton).Enabled = true;
			((Control)ErrorListBox).Enabled = true;
			((Control)EodhdRB).Enabled = true;
			((Control)EODHDButton).Enabled = true;
			((Control)DoneButton).Enabled = true;
			((Control)BrowseButton).Enabled = true;
			((Control)BarChartButton).Enabled = true;
			((Control)BarchartRB).Enabled = true;
			((Control)AutoRetryCheckBox).Enabled = true;
			((Control)AllPortsButton).Enabled = true;
			((Control)AllButton).Enabled = true;
			if (!YahooRadioButton.Checked)
			{
				((Control)APIKeyTextBox).Enabled = true;
			}
			if (HistoricalRadioButton.Checked)
			{
				((Control)FromDatePicker).Enabled = true;
				((Control)ToDatePicker).Enabled = true;
				((Control)SymbolTextBox).Enabled = true;
			}
			ProgressBar1.Value = 100;
			if (RetryListBox.Items.Count > 0)
			{
				if (AutoRetryCheckBox.Checked)
				{
					if (AutoStart == -1)
					{
						bool flag = true;
						if (flag == BarchartRB.Checked)
						{
							AutoStart = 8;
						}
						else if (flag == FinnhubRB.Checked)
						{
							AutoStart = 6;
						}
						else if (flag == IEXRadioButton.Checked)
						{
							AutoStart = 7;
						}
						else if (flag == TiingoRadioButton.Checked)
						{
							AutoStart = 4;
						}
						else if (flag == StockDataRB.Checked)
						{
							AutoStart = 9;
						}
						else if (flag == UnibitRB.Checked)
						{
							AutoStart = 10;
						}
						else if (flag == EodhdRB.Checked)
						{
							AutoStart = 11;
						}
						else
						{
							AutoStart = 4;
						}
						RetryChecked = true;
					}
					bool flag2 = true;
					if (flag2 == BarchartRB.Checked)
					{
						FinnhubRB.Checked = true;
						if (AutoStart == 6)
						{
							AutoStart = -1;
							RetryChecked = false;
						}
						else if (Operators.CompareString(APIKeyTextBox.Text, "", false) != 0)
						{
						}
					}
					else if (flag2 == FinnhubRB.Checked)
					{
						IEXRadioButton.Checked = true;
						if (AutoStart == 7)
						{
							AutoStart = -1;
							RetryChecked = false;
						}
						else if (Operators.CompareString(APIKeyTextBox.Text, "", false) != 0)
						{
						}
					}
					else if (flag2 == IEXRadioButton.Checked)
					{
						TiingoRadioButton.Checked = true;
						if (AutoStart == 4)
						{
							AutoStart = -1;
							RetryChecked = false;
						}
						else if (Operators.CompareString(APIKeyTextBox.Text, "", false) != 0)
						{
						}
					}
					else if (flag2 == TiingoRadioButton.Checked)
					{
						StockDataRB.Checked = true;
						if (AutoStart == 9)
						{
							AutoStart = -1;
							RetryChecked = false;
						}
						else if (Operators.CompareString(APIKeyTextBox.Text, "", false) != 0)
						{
						}
					}
					else if (flag2 == StockDataRB.Checked)
					{
						BarchartRB.Checked = true;
						if (AutoStart == 8)
						{
							AutoStart = -1;
							RetryChecked = false;
						}
						else if (Operators.CompareString(APIKeyTextBox.Text, "", false) != 0)
						{
						}
					}
					else if (flag2 != UnibitRB.Checked)
					{
						_ = EodhdRB.Checked;
					}
					if ((AutoStart != -1) & RetryChecked & (RetryListBox.Items.Count > 0))
					{
						RetryEngagedCounter++;
						StartButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
					}
				}
			}
			else if (RetryChecked)
			{
				switch (AutoStart)
				{
				case 8:
					BarchartRB.Checked = true;
					break;
				case 6:
					FinnhubRB.Checked = true;
					break;
				case 7:
					IEXRadioButton.Checked = true;
					break;
				case 4:
					TiingoRadioButton.Checked = true;
					break;
				case 9:
					StockDataRB.Checked = true;
					break;
				case 10:
					UnibitRB.Checked = true;
					break;
				case 11:
					EodhdRB.Checked = true;
					break;
				default:
					TiingoRadioButton.Checked = true;
					break;
				}
				AutoStart = -1;
				RetryChecked = false;
			}
			if (!Quiet & (RetryEngagedCounter == 0))
			{
				if (RetryListBox.Items.Count > 0)
				{
					if (AutoRetryCheckBox.Checked)
					{
						MessageBox.Show("I could not update quote files listed in the retry list box.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
					}
					else
					{
						MessageBox.Show("Done! Symbols not updated are listed in the retry list box. Change quote providers and click Retry to update them.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
					}
				}
				else
				{
					MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				}
			}
			ProgressBar1.Value = 0;
			Timer1.Enabled = false;
			if (RetryEngagedCounter > 0)
			{
				RetryEngagedCounter--;
			}
			Label4.Text = "Error count: " + Strings.Format((object)GlobalForm.ErrorCount, "") + ". Symbols updated properly: " + GlobalForm.GoodCount;
		}
	}

	private void StockDataHelpButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("As of March 23, 2023, Stockdata.org (https://www.stockdata.org/) provides 100 requests, each day, for up to 1-year of data, for free.\r\n\r\nWhen getting historical quotes, I ask for all data before the 'To' date (which is why 'From' is grayed), so if you have a subcription, your files could be long (slowing Patternz). You can cut their size using Excel or another program for faster Patternz performance.\r\n\r\nYou'll need an API key to use this service.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void StockDataRB_CheckedChanged(object sender, EventArgs e)
	{
		Timer1.Enabled = false;
		if (StockDataRB.Checked)
		{
			((Control)APIKeyTextBox).Enabled = true;
			APIKeyTextBox.Text = GlobalForm.SDKey;
			((Control)LinkLabel).Visible = false;
			if (HistoricalRadioButton.Checked)
			{
				((Control)FromDatePicker).Enabled = false;
			}
		}
		else if (HistoricalRadioButton.Checked)
		{
			((Control)FromDatePicker).Enabled = true;
		}
	}

	private void StopButton_Click(object sender, EventArgs e)
	{
		StopPressed = true;
		Interaction.Beep();
	}

	private void SymbolNameCheck()
	{
		bool flag = false;
		int count = ListBox1.Items.Count;
		if (count <= 0)
		{
			return;
		}
		checked
		{
			string[] array = new string[count + 1];
			int num = count - 1;
			for (int i = 0; i <= num; i++)
			{
				array[i] = ListBox1.Items[i].ToString();
				if (Strings.InStr(array[i], "_", (CompareMethod)0) != 0)
				{
					array[i] = array[i].Replace("_", ":");
					SymbolTextBox.Text = SymbolTextBox.Text.Replace("_", ":");
					flag = true;
				}
			}
			SymbolTextBox.Text = SymbolTextBox.Text.Replace("_", ":");
			if (flag)
			{
				ListBox1.BeginUpdate();
				ListBox1.Items.Clear();
				int num2 = Information.UBound((Array)array, 1) - 1;
				for (int i = 0; i <= num2; i++)
				{
					ListBox1.Items.Add((object)array[i]);
				}
				ListBox1.EndUpdate();
			}
		}
	}

	private void SymbolTextBox_TextChanged(object sender, EventArgs e)
	{
		if ((Strings.InStr(SymbolTextBox.Text, "\r\n", (CompareMethod)0) != 0) | (Strings.InStr(SymbolTextBox.Text, "\n", (CompareMethod)0) != 0))
		{
			string text = SymbolTextBox.Text;
			text = text.Replace("\r\n", " ");
			text = text.Replace("\n", " ");
			SymbolTextBox.Text = text;
		}
	}

	private void TiingoHelpButton_Click(object sender, EventArgs e)
	{
		//IL_0027: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			Clipboard.SetText("https://www.tiingo.com/welcome");
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		MessageBox.Show(GlobalForm.TiingoMsg, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void TiingoRadioButton_CheckedChanged(object sender, EventArgs e)
	{
		Timer1.Enabled = false;
		if (TiingoRadioButton.Checked)
		{
			((Control)APIKeyTextBox).Enabled = true;
			APIKeyTextBox.Text = GlobalForm.TiingoKey;
			((Control)LinkLabel).Visible = false;
		}
	}

	private void Timer1_Tick(object sender, EventArgs e)
	{
		TimerRunFlag = true;
	}

	private void UpdateRadioButton_CheckedChanged(object sender, EventArgs e)
	{
		if (UpdateRadioButton.Checked)
		{
			SymbolTextBox.Text = "";
		}
	}

	private bool UQuotes(ref string InternetBuffer, string Symbol, DateTime LastUpdated, ref bool UpToDate)
	{
		//IL_0191: Unknown result type (might be due to invalid IL or missing references)
		string text = "";
		WebRequest webRequest = null;
		WebResponse webResponse = null;
		Stream stream = null;
		StreamReader streamReader = null;
		if (!ReplaceQuoteCB.Checked)
		{
			LastUpdated = DateAndTime.DateAdd((DateInterval)4, 1.0, LastUpdated);
		}
		if (DateTime.Compare(LastUpdated, DateAndTime.Now) > 0)
		{
			LastUpdated = DateAndTime.Now;
		}
		InternetBuffer = null;
		bool result;
		checked
		{
			if (YahooRadioButton.Checked)
			{
				int num = 0;
				while ((Operators.CompareString(Token.Cookie, "", false) == 0) & (Operators.CompareString(Token.Crumb, "", false) == 0))
				{
					Token.Refresh();
					num++;
					if (num >= 3)
					{
						break;
					}
				}
			}
			else if (TiingoRadioButton.Checked)
			{
				try
				{
					text = "&startDate=" + Strings.Format((object)LastUpdated, "yyyy") + "-" + Strings.Format((object)LastUpdated, "MM") + "-" + Strings.Format((object)LastUpdated, "dd");
					text = text + "&endDate=" + Strings.Format((object)DateAndTime.Now, "yyyy") + "-" + Strings.Format((object)DateAndTime.Now, "MM") + "-" + Strings.Format((object)DateAndTime.Now, "dd");
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					MessageBox.Show("Check the format Of the 'from' and 'to' fields.", "GetHistoricalQuotes", (MessageBoxButtons)0, (MessageBoxIcon)16);
					result = true;
					ProjectData.ClearProjectError();
					goto IL_0587;
				}
			}
			if (Strings.InStr(Symbol, ":", (CompareMethod)0) > 0)
			{
				Symbol = Strings.Right(Symbol, Symbol.Length - Strings.InStr(Symbol, ":", (CompareMethod)0));
			}
			ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
			try
			{
				if (FinnhubRB.Checked)
				{
					DateTime dateTime = LastUpdated;
					dateTime = DateAndTime.DateAdd((DateInterval)4, -1.0, dateTime);
					string text2 = Conversions.ToString(Historical.DateTimeToUnixTimestamp(dateTime));
					string text3 = Conversions.ToString(Math.Round(Historical.DateTimeToUnixTimestamp(DateAndTime.Now)));
					webRequest = WebRequest.CreateHttp(GlobalForm.FINNURL + "stock/candle?symbol=" + Symbol + "&resolution=D&from=" + text2 + "&to=" + text3 + "&format=csv&adjusted=true&token=" + GlobalForm.FinnhubKey);
				}
				else if (IEXRadioButton.Checked)
				{
					long num2 = GetWorkingDates(LastUpdated, DateAndTime.Now) - 1;
					webRequest = WebRequest.CreateHttp(GlobalForm.IEXURL + Symbol + "/chart/max?chartByDay=true&chartLast=" + num2 + "&token=" + GlobalForm.IEXKey + "&format=csv");
				}
				else if (BarchartRB.Checked)
				{
					webRequest = WebRequest.CreateHttp(GlobalForm.BARCHARTURL + GlobalForm.BarchartKey + "&symbol=" + Symbol + "&type=daily&startDate=" + Strings.Format((object)LastUpdated, "yyyyMMdd"));
				}
				else if (StockDataRB.Checked)
				{
					webRequest = WebRequest.CreateHttp(GlobalForm.SDURL + Symbol + "&sort=asc&date_from=" + Strings.Format((object)LastUpdated, "yyyy-MM-dd") + "&format=csv&api_token=" + GlobalForm.SDKey);
				}
				else if (UnibitRB.Checked)
				{
					webRequest = WebRequest.CreateHttp(GlobalForm.UNIBITURL + "?tickers=" + Symbol + "&startDate=" + Strings.Format((object)LastUpdated, "yyyy-MM-dd") + "&endDate=" + Strings.Format((object)DateAndTime.Now, "yyyy-MM-dd") + "&dataType=csv&accessKey=" + GlobalForm.UnibitKey);
				}
				else if (EodhdRB.Checked)
				{
					webRequest = WebRequest.CreateHttp(GlobalForm.EODHDURL + Symbol + "?from=" + Strings.Format((object)LastUpdated, "yyyy-MM-dd") + "&to=" + Strings.Format((object)DateAndTime.Now, "yyyy-MM-dd") + "&period=d&order=a&fmt=csv&api_token=" + GlobalForm.EODHDKey);
				}
				else if (YahooRadioButton.Checked)
				{
					InternetBuffer = Historical.GetRaw(Symbol, LastUpdated, DateAndTime.Now);
				}
				else if (TiingoRadioButton.Checked)
				{
					webRequest = WebRequest.CreateHttp(GlobalForm.TIINGOURL + Symbol + "/prices?token=" + APIKeyTextBox.Text + "&format=csv" + text);
				}
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				if (!YahooRadioButton.Checked)
				{
					webResponse = webRequest.GetResponse();
					stream = webResponse.GetResponseStream();
					streamReader = new StreamReader(stream);
					InternetBuffer = streamReader.ReadToEnd();
					streamReader.Close();
					streamReader = null;
					stream.Close();
					stream = null;
					webResponse.Close();
					webResponse = null;
				}
			}
			catch (Exception ex3)
			{
				ProjectData.SetProjectError(ex3);
				Exception ex4 = ex3;
				HandleInternetException(ex4, Symbol, ref InternetBuffer);
				streamReader?.Close();
				stream?.Close();
				webResponse?.Close();
				result = true;
				ProjectData.ClearProjectError();
				goto IL_0587;
			}
			result = false;
			goto IL_0587;
		}
		IL_0587:
		return result;
	}

	private string VerifyQuotes(string ExistingBuffer, ref string NewQuote, DateTime LastDate)
	{
		int num = Strings.InStr(NewQuote, ",", (CompareMethod)0);
		checked
		{
			if (num - 1 > 0)
			{
				if (DateTime.Compare(GlobalForm.MyCDate(Strings.Left(NewQuote, num - 1)), LastDate) != 0)
				{
					return ExistingBuffer + NewQuote;
				}
				num = Strings.InStrRev(ExistingBuffer, "\r\n", -1, (CompareMethod)0);
				if (num - "\r\n".Length > 0)
				{
					LocalBuffer = Strings.Left(ExistingBuffer, num - "\r\n".Length);
					num = Strings.InStrRev(LocalBuffer, "\r\n", -1, (CompareMethod)0);
					if (num - "\r\n".Length > 0)
					{
						LocalBuffer = Strings.Left(LocalBuffer, num + "\r\n".Length - 1);
						return LocalBuffer + NewQuote;
					}
				}
				return ExistingBuffer;
			}
			return ExistingBuffer;
		}
	}

	private void ReplaceQuoteButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("If you update your quote files before the market closes, you may have incomplete data. If you check this box, Patternz will replace the last day shown in the quote file with a new quote.\r\n\r\nIf you ALWAYS update your files after the close, then leave this unchecked (you'll get faster processing). This checkbox only applies to 'Start from last update' (and not getting historical quotes).", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void UnibitRB_CheckedChanged(object sender, EventArgs e)
	{
		Timer1.Enabled = false;
		if (UnibitRB.Checked)
		{
			((Control)APIKeyTextBox).Enabled = true;
			APIKeyTextBox.Text = GlobalForm.UnibitKey;
			((Control)LinkLabel).Visible = false;
		}
	}

	private void EodhdRB_CheckedChanged(object sender, EventArgs e)
	{
		Timer1.Enabled = false;
		if (EodhdRB.Checked)
		{
			((Control)APIKeyTextBox).Enabled = true;
			APIKeyTextBox.Text = GlobalForm.EODHDKey;
			((Control)LinkLabel).Visible = false;
		}
	}

	private void UnibitButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("As of March 27, 2023, Unibit (https://unibit.ai/) provides 50,000 credits per month for free, where one historical quote costs 10 credits.\r\n\r\nYou'll need an API key to use this service.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void EODHDButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("As of March 27, 2023, EODHD (https://eodhistoricaldata.com) provides 20 requests, each day, for free. NOTE: symbol should include exchange: .US should be appended to apple's symbol as in AAPL.US for data from a United States exchange. For a list of exchanges, see https://eodhistoricaldata.com/financial-apis/list-supported-exchanges/.\r\n\r\nYou'll need an API key to use this service.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}
}
