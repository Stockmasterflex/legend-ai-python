using System;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Microsoft.VisualBasic.Devices;
using Microsoft.Win32;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class Mainform : Form
{
	private const string KEYMF = "MainForm";

	private const string KEYCF = "ChartForm";

	private const string KEYFFF = "FileFormatForm";

	private const string KEYPF = "PatternForm";

	private const string KEYLF = "LicenseForm";

	private const string KEYLISF = "ListForm";

	private const string KEYLCF = "ListChartForm";

	private const string KEYCANF = "CandleForm";

	private const string KEYIF = "IndicatorsForm";

	private const string KEYSF = "SetupForm";

	private const string KEYSDF = "SplitDivForm";

	private const string KEYSCORF = "ScoreForm";

	private const string KEYMANSCORF = "ManScoreForm";

	private const string KEYNEWS = "NewsForm";

	private const string KEYFIXSPLIT = "FixSplitForm";

	private const string KEYSEAF = "SeasonalityForm";

	private bool lsChartVolume;

	private bool lsShowAllPatterns;

	private bool lsStrictPatterns;

	private bool MainFormSizeChanged;

	private bool LockFlag;

	private bool FirstTime;

	private long lsLFDateLookBack;

	private bool lsLFPatterns;

	private bool lsLFCandles;

	private long lsUFDateLookBack;

	private int lsUpdatePeriod;

	private int lsUpdateSource;

	private string lsIndexSymbol;

	private readonly long lsCPIDateLookBack;

	private bool lsShowPortfolio;

	private bool lsWatchList;

	private int lsChartPeriodShown;

	private int lsMALength;

	private int lsMAType;

	private bool lsMAUsed;

	private int lsRadButton;

	private string SearchString;

	private int lsChartType;

	private int lsSDFUpdateSource;

	private bool lsSplits;

	private bool lsDividends;

	private int lsSDFDateLookBack;

	private int lsSFDateLookBack;

	private bool lsSFStrict;

	private int lsSFDWM;

	private int lsMSFCombo;

	private bool lsAutoRetry;

	private bool lsEntireFile;

	private Color lsUpCandleColor;

	private Color lsDownCandleColor;

	private Color lsChartBGColor;

	private Color lsVolumeBGColor;

	private Color lsPriceBarColor;

	private double lsGapSize;

	private bool lsPatternTargets;

	private bool lsLCFPatternTargets;

	private bool lsShowConfirmation;

	private bool lsShowStopLoss;

	private bool lsShowTargetprice;

	private bool lsShowUltHighLow;

	private bool lsShowUnHit;

	private bool lsShowUpTarget;

	private int lsShowUpPercentage;

	private bool lsShowDownTarget;

	private int lsShowDownPercentage;

	private bool lsffDateTimeFormat;

	private bool lsShowBARRLines;

	private int lsDayOfWeek;

	private int lsMonthLB;

	private int lsRBSelected;

	private bool lsAnnotations;

	private bool lsIncludePhrase;

	private int lsSkipType;

	private int lsVendor;

	private int lsTLUpLength;

	private int lsTLDNLength;

	private int lsUserDecimals;

	private int lsDecimalsOption;

	private int lsNewsDateRB;

	private int lsArticleNumber;

	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("ExitMenuItem")]
	private ToolStripMenuItem _ExitMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("FileFormatMenuItem")]
	private ToolStripMenuItem _FileFormatMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("PatternsMenuItem")]
	private ToolStripMenuItem _PatternsMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("ListBox1")]
	private ListBox _ListBox1;

	[CompilerGenerated]
	[AccessedThroughProperty("AllButton")]
	private Button _AllButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ChartButton")]
	private Button _ChartButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ListButton")]
	private Button _ListButton;

	[CompilerGenerated]
	[AccessedThroughProperty("BrowseButton")]
	private Button _BrowseButton;

	[CompilerGenerated]
	[AccessedThroughProperty("AboutToolStripMenuItem")]
	private ToolStripMenuItem _AboutToolStripMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("RemovePatternzMenuItem")]
	private ToolStripMenuItem _RemovePatternzMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("LicenseToolStripMenuItem")]
	private ToolStripMenuItem _LicenseToolStripMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("CandlesToolStripMenuItem")]
	private ToolStripMenuItem _CandlesToolStripMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("UpdateButton")]
	private Button _UpdateButton;

	[CompilerGenerated]
	[AccessedThroughProperty("IndicatorsButton")]
	private Button _IndicatorsButton;

	[CompilerGenerated]
	[AccessedThroughProperty("MainFormHelpToolStripMenuItem")]
	private ToolStripMenuItem _MainFormHelpToolStripMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("PortfolioTextBox")]
	private TextBox _PortfolioTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("DeleteButton")]
	private Button _DeleteButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ChangeButton")]
	private Button _ChangeButton;

	[CompilerGenerated]
	[AccessedThroughProperty("AddButton")]
	private Button _AddButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ShowPortfolioCheckBox")]
	private CheckBox _ShowPortfolioCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("HelpButton1")]
	private Button _HelpButton1;

	[CompilerGenerated]
	[AccessedThroughProperty("PortfolioDataGridView")]
	private DataGridView _PortfolioDataGridView;

	[CompilerGenerated]
	[AccessedThroughProperty("SplitsDivsToolStripMenuItem")]
	private ToolStripMenuItem _SplitsDivsToolStripMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("ScoreButton")]
	private Button _ScoreButton;

	[CompilerGenerated]
	[AccessedThroughProperty("RelStrengthToolStripMenuItem")]
	private ToolStripMenuItem _RelStrengthToolStripMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("ManualScoreToolStripMenuItem")]
	private ToolStripMenuItem _ManualScoreToolStripMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("FixSplitMI")]
	private ToolStripMenuItem _FixSplitMI;

	[CompilerGenerated]
	[AccessedThroughProperty("Fib")]
	private ToolStripMenuItem _Fib;

	[CompilerGenerated]
	[AccessedThroughProperty("NewsMenuItem")]
	private ToolStripMenuItem _NewsMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("SimulatorButton")]
	private Button _SimulatorButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PredictionMI")]
	private ToolStripMenuItem _PredictionMI;

	[CompilerGenerated]
	[AccessedThroughProperty("RestoreLayoutToolStripMenuItem")]
	private ToolStripMenuItem _RestoreLayoutToolStripMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("SeasonalityToolStripMenuItem")]
	private ToolStripMenuItem _SeasonalityToolStripMenuItem;

	[CompilerGenerated]
	[AccessedThroughProperty("MyBuyingsellingToolStripMenuItem")]
	private ToolStripMenuItem _MyBuyingsellingToolStripMenuItem;

	[field: AccessedThroughProperty("MenuStrip1")]
	internal virtual MenuStrip MenuStrip1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual ToolStripMenuItem ExitMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _ExitMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ExitMenuItem_Click;
			ToolStripMenuItem val = _ExitMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_ExitMenuItem = value;
			val = _ExitMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem FileFormatMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _FileFormatMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = FileFormatToolStripMenuItem_Click;
			ToolStripMenuItem val = _FileFormatMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_FileFormatMenuItem = value;
			val = _FileFormatMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PatternsMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _PatternsMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PatternsMenuItem_Click;
			ToolStripMenuItem val = _PatternsMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_PatternsMenuItem = value;
			val = _PatternsMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("HelpMenuItem")]
	internal virtual ToolStripMenuItem HelpMenuItem
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
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
			//IL_0014: Unknown result type (might be due to invalid IL or missing references)
			//IL_001a: Expected O, but got Unknown
			//IL_0021: Unknown result type (might be due to invalid IL or missing references)
			//IL_0027: Expected O, but got Unknown
			//IL_002e: Unknown result type (might be due to invalid IL or missing references)
			//IL_0034: Expected O, but got Unknown
			EventHandler eventHandler = ListBox1_DoubleClick;
			KeyPressEventHandler val = new KeyPressEventHandler(ListBox1_KeyPress);
			KeyEventHandler val2 = new KeyEventHandler(ListBox1_KeyUp);
			MouseEventHandler val3 = new MouseEventHandler(ListBox1_MouseClick);
			EventHandler eventHandler2 = ListBox1_SelectedIndexChanged;
			ListBox val4 = _ListBox1;
			if (val4 != null)
			{
				((Control)val4).DoubleClick -= eventHandler;
				((Control)val4).KeyPress -= val;
				((Control)val4).KeyUp -= val2;
				val4.MouseClick -= val3;
				val4.SelectedIndexChanged -= eventHandler2;
			}
			_ListBox1 = value;
			val4 = _ListBox1;
			if (val4 != null)
			{
				((Control)val4).DoubleClick += eventHandler;
				((Control)val4).KeyPress += val;
				((Control)val4).KeyUp += val2;
				val4.MouseClick += val3;
				val4.SelectedIndexChanged += eventHandler2;
			}
		}
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

	internal virtual Button ChartButton
	{
		[CompilerGenerated]
		get
		{
			return _ChartButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ChartButton_Click;
			Button val = _ChartButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ChartButton = value;
			val = _ChartButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button ListButton
	{
		[CompilerGenerated]
		get
		{
			return _ListButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ListButton_Click;
			Button val = _ListButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ListButton = value;
			val = _ListButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("FileSystemWatcher1")]
	internal virtual FileSystemWatcher FileSystemWatcher1
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

	internal virtual ToolStripMenuItem AboutToolStripMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _AboutToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = AboutToolStripMenuItem_Click;
			ToolStripMenuItem val = _AboutToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_AboutToolStripMenuItem = value;
			val = _AboutToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem RemovePatternzMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _RemovePatternzMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = RemovePatternzMenuItem_Click;
			ToolStripMenuItem val = _RemovePatternzMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_RemovePatternzMenuItem = value;
			val = _RemovePatternzMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem LicenseToolStripMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _LicenseToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = LicenseToolStripMenuItem_Click;
			ToolStripMenuItem val = _LicenseToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_LicenseToolStripMenuItem = value;
			val = _LicenseToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem CandlesToolStripMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _CandlesToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CandlesToolStripMenuItem_Click;
			ToolStripMenuItem val = _CandlesToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_CandlesToolStripMenuItem = value;
			val = _CandlesToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button UpdateButton
	{
		[CompilerGenerated]
		get
		{
			return _UpdateButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = UpdateButton_Click;
			Button val = _UpdateButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_UpdateButton = value;
			val = _UpdateButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("FileLocationLabel")]
	internal virtual Label FileLocationLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button IndicatorsButton
	{
		[CompilerGenerated]
		get
		{
			return _IndicatorsButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = IndicatorsButton_Click;
			Button val = _IndicatorsButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_IndicatorsButton = value;
			val = _IndicatorsButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem MainFormHelpToolStripMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _MainFormHelpToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = MainFormHelpToolStripMenuItem_Click;
			ToolStripMenuItem val = _MainFormHelpToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_MainFormHelpToolStripMenuItem = value;
			val = _MainFormHelpToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("PortfolioPanel")]
	internal virtual Panel PortfolioPanel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual TextBox PortfolioTextBox
	{
		[CompilerGenerated]
		get
		{
			return _PortfolioTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PortfolioTextBox_TextChanged;
			TextBox val = _PortfolioTextBox;
			if (val != null)
			{
				((Control)val).TextChanged -= eventHandler;
			}
			_PortfolioTextBox = value;
			val = _PortfolioTextBox;
			if (val != null)
			{
				((Control)val).TextChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label1")]
	internal virtual Label Label1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button DeleteButton
	{
		[CompilerGenerated]
		get
		{
			return _DeleteButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DeleteButton_Click;
			Button val = _DeleteButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_DeleteButton = value;
			val = _DeleteButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button ChangeButton
	{
		[CompilerGenerated]
		get
		{
			return _ChangeButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ChangeButton_Click;
			Button val = _ChangeButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ChangeButton = value;
			val = _ChangeButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button AddButton
	{
		[CompilerGenerated]
		get
		{
			return _AddButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = AddButton_Click;
			Button val = _AddButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_AddButton = value;
			val = _AddButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual CheckBox ShowPortfolioCheckBox
	{
		[CompilerGenerated]
		get
		{
			return _ShowPortfolioCheckBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CheckBox1_CheckedChanged;
			CheckBox val = _ShowPortfolioCheckBox;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_ShowPortfolioCheckBox = value;
			val = _ShowPortfolioCheckBox;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
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
			EventHandler eventHandler = HelpButton1_Click_1;
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

	[field: AccessedThroughProperty("Label3")]
	internal virtual Label Label3
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("LabelPanel")]
	internal virtual Panel LabelPanel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual DataGridView PortfolioDataGridView
	{
		[CompilerGenerated]
		get
		{
			return _PortfolioDataGridView;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DataGridView1_SelectionChanged;
			EventHandler eventHandler2 = PortfolioDataGridView_GotFocus;
			DataGridView val = _PortfolioDataGridView;
			if (val != null)
			{
				val.SelectionChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_PortfolioDataGridView = value;
			val = _PortfolioDataGridView;
			if (val != null)
			{
				val.SelectionChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	[field: AccessedThroughProperty("PortfolioColumn")]
	internal virtual DataGridViewTextBoxColumn PortfolioColumn
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("PathColumn")]
	internal virtual DataGridViewTextBoxColumn PathColumn
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual ToolStripMenuItem SplitsDivsToolStripMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _SplitsDivsToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SplitsDivsToolStripMenuItem_Click;
			ToolStripMenuItem val = _SplitsDivsToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_SplitsDivsToolStripMenuItem = value;
			val = _SplitsDivsToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button ScoreButton
	{
		[CompilerGenerated]
		get
		{
			return _ScoreButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ScoreButton_Click;
			Button val = _ScoreButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ScoreButton = value;
			val = _ScoreButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label2")]
	internal virtual Label Label2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual ToolStripMenuItem RelStrengthToolStripMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _RelStrengthToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = RelStrengthToolStripMenuItem_Click;
			ToolStripMenuItem val = _RelStrengthToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_RelStrengthToolStripMenuItem = value;
			val = _RelStrengthToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label4")]
	internal virtual Label Label4
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual ToolStripMenuItem ManualScoreToolStripMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _ManualScoreToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ManualScoreToolStripMenuItem_Click;
			ToolStripMenuItem val = _ManualScoreToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_ManualScoreToolStripMenuItem = value;
			val = _ManualScoreToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem FixSplitMI
	{
		[CompilerGenerated]
		get
		{
			return _FixSplitMI;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ToolStripMenuItem1_Click;
			ToolStripMenuItem val = _FixSplitMI;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_FixSplitMI = value;
			val = _FixSplitMI;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem Fib
	{
		[CompilerGenerated]
		get
		{
			return _Fib;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ToolStripMenuItem1_Click_1;
			ToolStripMenuItem val = _Fib;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_Fib = value;
			val = _Fib;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("SeasonalityMI")]
	internal virtual ToolStripMenuItem SeasonalityMI
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual ToolStripMenuItem NewsMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _NewsMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = NewsMenuItem_Click;
			ToolStripMenuItem val = _NewsMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_NewsMenuItem = value;
			val = _NewsMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button SimulatorButton
	{
		[CompilerGenerated]
		get
		{
			return _SimulatorButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SimulatorButton_Click;
			Button val = _SimulatorButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_SimulatorButton = value;
			val = _SimulatorButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem PredictionMI
	{
		[CompilerGenerated]
		get
		{
			return _PredictionMI;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PredictionToolStripMenuItem_Click;
			ToolStripMenuItem val = _PredictionMI;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_PredictionMI = value;
			val = _PredictionMI;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem RestoreLayoutToolStripMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _RestoreLayoutToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = RestoreLayoutToolStripMenuItem_Click;
			ToolStripMenuItem val = _RestoreLayoutToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_RestoreLayoutToolStripMenuItem = value;
			val = _RestoreLayoutToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem SeasonalityToolStripMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _SeasonalityToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SeasonalityToolStripMenuItem_Click;
			ToolStripMenuItem val = _SeasonalityToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_SeasonalityToolStripMenuItem = value;
			val = _SeasonalityToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	internal virtual ToolStripMenuItem MyBuyingsellingToolStripMenuItem
	{
		[CompilerGenerated]
		get
		{
			return _MyBuyingsellingToolStripMenuItem;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = MyBuyingsellingToolStripMenuItem_Click;
			ToolStripMenuItem val = _MyBuyingsellingToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click -= eventHandler;
			}
			_MyBuyingsellingToolStripMenuItem = value;
			val = _MyBuyingsellingToolStripMenuItem;
			if (val != null)
			{
				((ToolStripItem)val).Click += eventHandler;
			}
		}
	}

	public Mainform()
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		//IL_0044: Unknown result type (might be due to invalid IL or missing references)
		//IL_004e: Expected O, but got Unknown
		((Form)this).FormClosing += new FormClosingEventHandler(Mainform_FormClosing);
		((Form)this).Load += Mainform_Load;
		((Form)this).Activated += Mainform_Activated;
		((Control)this).KeyDown += new KeyEventHandler(Mainform_KeyDown);
		((Control)this).SizeChanged += Mainform_SizeChanged;
		FirstTime = true;
		lsLFDateLookBack = 400L;
		lsLFPatterns = true;
		lsLFCandles = false;
		lsUFDateLookBack = 400L;
		lsCPIDateLookBack = 262L;
		lsMALength = 50;
		lsMAType = 1;
		lsMAUsed = false;
		SearchString = "";
		lsDayOfWeek = 1;
		lsMonthLB = 0;
		lsRBSelected = GlobalForm.SFDaily;
		InitializeComponent();
	}

	private void Mainform_FormClosing(object sender, FormClosingEventArgs e)
	{
		//IL_0060: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			if (LockFlag | !GlobalForm.RemovePatternzFlag)
			{
				if (GlobalForm.PathChanged)
				{
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "FilePath", (object)GlobalForm.OpenPath);
						GlobalForm.PathChanged = false;
					}
					catch (Exception ex)
					{
						ProjectData.SetProjectError(ex);
						Exception ex2 = ex;
						MessageBox.Show("I tried to save the file path to the registry but was unsuccessful. Error: " + ex2.Message, "MainForm: Mainform_FormClosing", (MessageBoxButtons)0, (MessageBoxIcon)16);
						ProjectData.ClearProjectError();
					}
				}
				try
				{
					if (MainFormSizeChanged | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "Width", (object)Conversions.ToString(((Control)this).Width));
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "Height", (object)Conversions.ToString(((Control)this).Height));
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
					if ((lsShowPortfolio != ShowPortfolioCheckBox.Checked) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "ShowPortfolio", (object)ShowPortfolioCheckBox.Checked);
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
					if (lsWatchList | FirstTime)
					{
						string[] array = null;
						if (PortfolioDataGridView.RowCount > 0)
						{
							int num = 2 * PortfolioDataGridView.RowCount - 1;
							for (int i = 0; i <= num; i += 2)
							{
								array = (string[])Utils.CopyArray((Array)array, (Array)new string[i + 1 + 1]);
								array[i] = PortfolioDataGridView.Rows[(int)Math.Round((double)i / 2.0)].Cells[0].Value.ToString();
								array[i + 1] = PortfolioDataGridView.Rows[(int)Math.Round((double)i / 2.0)].Cells[1].Value.ToString();
							}
							((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "PortfolioList", (object)array);
						}
						else
						{
							array = new string[2];
							array = new string[2] { "", "" };
							((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "PortfolioList", (object)array);
						}
					}
				}
				catch (Exception ex7)
				{
					ProjectData.SetProjectError(ex7);
					Exception ex8 = ex7;
					ProjectData.ClearProjectError();
				}
				int num2 = 0;
				try
				{
					num2 = ListBox1.SelectedIndices.Count;
					((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "SelectedCount", (object)num2);
					if (num2 > 0)
					{
						string[] array2 = new string[num2 - 1 + 1];
						int num3 = num2 - 1;
						for (int j = 0; j <= num3; j++)
						{
							array2[j] = ListBox1.SelectedIndices[j].ToString();
						}
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "SelectedList", (object)array2);
					}
				}
				catch (Exception ex9)
				{
					ProjectData.SetProjectError(ex9);
					Exception ex10 = ex9;
					ProjectData.ClearProjectError();
				}
				if (GlobalForm.FileFormatChanged | FirstTime)
				{
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ffDate", (object)Conversions.ToString(GlobalForm.FileFormat[0]));
					}
					catch (Exception ex11)
					{
						ProjectData.SetProjectError(ex11);
						Exception ex12 = ex11;
						ProjectData.ClearProjectError();
					}
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ffTime", (object)Conversions.ToString(GlobalForm.FileFormat[1]));
					}
					catch (Exception ex13)
					{
						ProjectData.SetProjectError(ex13);
						Exception ex14 = ex13;
						ProjectData.ClearProjectError();
					}
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "Open", (object)Conversions.ToString(GlobalForm.FileFormat[2]));
					}
					catch (Exception ex15)
					{
						ProjectData.SetProjectError(ex15);
						Exception ex16 = ex15;
						ProjectData.ClearProjectError();
					}
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "High", (object)Conversions.ToString(GlobalForm.FileFormat[3]));
					}
					catch (Exception ex17)
					{
						ProjectData.SetProjectError(ex17);
						Exception ex18 = ex17;
						ProjectData.ClearProjectError();
					}
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "Low", (object)Conversions.ToString(GlobalForm.FileFormat[4]));
					}
					catch (Exception ex19)
					{
						ProjectData.SetProjectError(ex19);
						Exception ex20 = ex19;
						ProjectData.ClearProjectError();
					}
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "Close", (object)Conversions.ToString(GlobalForm.FileFormat[5]));
					}
					catch (Exception ex21)
					{
						ProjectData.SetProjectError(ex21);
						Exception ex22 = ex21;
						ProjectData.ClearProjectError();
					}
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "Volume", (object)Conversions.ToString(GlobalForm.FileFormat[6]));
					}
					catch (Exception ex23)
					{
						ProjectData.SetProjectError(ex23);
						Exception ex24 = ex23;
						ProjectData.ClearProjectError();
					}
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "AdjClose", (object)Conversions.ToString(GlobalForm.FileFormat[7]));
					}
					catch (Exception ex25)
					{
						ProjectData.SetProjectError(ex25);
						Exception ex26 = ex25;
						ProjectData.ClearProjectError();
					}
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "sDateFormat", (object)GlobalForm.UserDate);
					}
					catch (Exception ex27)
					{
						ProjectData.SetProjectError(ex27);
						Exception ex28 = ex27;
						ProjectData.ClearProjectError();
					}
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ckTime", (object)Conversions.ToString(GlobalForm.ckFileFormat[1]));
					}
					catch (Exception ex29)
					{
						ProjectData.SetProjectError(ex29);
						Exception ex30 = ex29;
						ProjectData.ClearProjectError();
					}
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ckOpen", (object)Conversions.ToString(GlobalForm.ckFileFormat[2]));
					}
					catch (Exception ex31)
					{
						ProjectData.SetProjectError(ex31);
						Exception ex32 = ex31;
						ProjectData.ClearProjectError();
					}
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ckVolume", (object)Conversions.ToString(GlobalForm.ckFileFormat[6]));
					}
					catch (Exception ex33)
					{
						ProjectData.SetProjectError(ex33);
						Exception ex34 = ex33;
						ProjectData.ClearProjectError();
					}
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ckAdjClose", (object)Conversions.ToString(GlobalForm.ckFileFormat[7]));
					}
					catch (Exception ex35)
					{
						ProjectData.SetProjectError(ex35);
						Exception ex36 = ex35;
						ProjectData.ClearProjectError();
					}
					try
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ffDateTimeFormat", (object)GlobalForm.ffDateTimeFormat);
					}
					catch (Exception ex37)
					{
						ProjectData.SetProjectError(ex37);
						Exception ex38 = ex37;
						ProjectData.ClearProjectError();
					}
				}
				try
				{
					if ((lsChartVolume != GlobalForm.ChartVolume) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ChartForm", "Volume", (object)GlobalForm.ChartVolume);
					}
				}
				catch (Exception ex39)
				{
					ProjectData.SetProjectError(ex39);
					Exception ex40 = ex39;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsShowAllPatterns != GlobalForm.ShowAllPatterns) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ChartForm", "ShowAllPatterns", (object)GlobalForm.ShowAllPatterns);
					}
				}
				catch (Exception ex41)
				{
					ProjectData.SetProjectError(ex41);
					Exception ex42 = ex41;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((FindCandles.lsShowCandles != GlobalForm.ShowCandles) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ChartForm", "ShowCandles", (object)GlobalForm.ShowCandles);
					}
				}
				catch (Exception ex43)
				{
					ProjectData.SetProjectError(ex43);
					Exception ex44 = ex43;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsStrictPatterns != GlobalForm.StrictPatterns) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ChartForm", "Strict", (object)GlobalForm.StrictPatterns);
					}
				}
				catch (Exception ex45)
				{
					ProjectData.SetProjectError(ex45);
					Exception ex46 = ex45;
					ProjectData.ClearProjectError();
				}
				try
				{
					if (GlobalForm.DLBChanged | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ChartForm", "DateLookback", (object)GlobalForm.DateLookback);
					}
				}
				catch (Exception ex47)
				{
					ProjectData.SetProjectError(ex47);
					Exception ex48 = ex47;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsChartPeriodShown != GlobalForm.ChartPeriodShown) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ChartForm", "ChartPeriodshown", (object)GlobalForm.ChartPeriodShown);
					}
				}
				catch (Exception ex49)
				{
					ProjectData.SetProjectError(ex49);
					Exception ex50 = ex49;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsIncludePhrase != GlobalForm.IncludePhrase) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "IncludePhrase", (object)GlobalForm.IncludePhrase);
					}
				}
				catch (Exception ex51)
				{
					ProjectData.SetProjectError(ex51);
					Exception ex52 = ex51;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsAnnotations != GlobalForm.Annotations) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "Annotations", (object)GlobalForm.Annotations);
					}
				}
				catch (Exception ex53)
				{
					ProjectData.SetProjectError(ex53);
					Exception ex54 = ex53;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsMALength != GlobalForm.MALength) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "MALength", (object)GlobalForm.MALength);
					}
				}
				catch (Exception ex55)
				{
					ProjectData.SetProjectError(ex55);
					Exception ex56 = ex55;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsMAType != GlobalForm.MAType) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "MAType", (object)GlobalForm.MAType);
					}
				}
				catch (Exception ex57)
				{
					ProjectData.SetProjectError(ex57);
					Exception ex58 = ex57;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsMAUsed != GlobalForm.MAUsed) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "MAUsed", (object)GlobalForm.MAUsed);
					}
				}
				catch (Exception ex59)
				{
					ProjectData.SetProjectError(ex59);
					Exception ex60 = ex59;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsChartType != GlobalForm.ChartType) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ChartType", (object)GlobalForm.ChartType);
					}
				}
				catch (Exception ex61)
				{
					ProjectData.SetProjectError(ex61);
					Exception ex62 = ex61;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsUserDecimals != GlobalForm.UserDecimals) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "Decimals", (object)GlobalForm.UserDecimals);
					}
				}
				catch (Exception ex63)
				{
					ProjectData.SetProjectError(ex63);
					Exception ex64 = ex63;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsDecimalsOption != GlobalForm.DecimalsOption) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "DecimalOpt", (object)GlobalForm.DecimalsOption);
					}
				}
				catch (Exception ex65)
				{
					ProjectData.SetProjectError(ex65);
					Exception ex66 = ex65;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.lsDiscardQuote != GlobalForm.DiscardQuote) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "DiscardQuote", (object)GlobalForm.DiscardQuote);
					}
				}
				catch (Exception ex67)
				{
					ProjectData.SetProjectError(ex67);
					Exception ex68 = ex67;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsUpCandleColor != GlobalForm.UpCandleColor) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "UpCandleColor", (object)GlobalForm.UpCandleColor.ToArgb());
					}
				}
				catch (Exception ex69)
				{
					ProjectData.SetProjectError(ex69);
					Exception ex70 = ex69;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsDownCandleColor != GlobalForm.DownCandleColor) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "DownCandleColor", (object)GlobalForm.DownCandleColor.ToArgb());
					}
				}
				catch (Exception ex71)
				{
					ProjectData.SetProjectError(ex71);
					Exception ex72 = ex71;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsChartBGColor != GlobalForm.ChartBGColor) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ChartBGColor", (object)GlobalForm.ChartBGColor.ToArgb());
					}
				}
				catch (Exception ex73)
				{
					ProjectData.SetProjectError(ex73);
					Exception ex74 = ex73;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsVolumeBGColor != GlobalForm.VolumeBGColor) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "VolumeBGColor", (object)GlobalForm.VolumeBGColor.ToArgb());
					}
				}
				catch (Exception ex75)
				{
					ProjectData.SetProjectError(ex75);
					Exception ex76 = ex75;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsPriceBarColor != GlobalForm.PriceBarColor) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "PriceBarColor", (object)GlobalForm.PriceBarColor.ToArgb());
					}
				}
				catch (Exception ex77)
				{
					ProjectData.SetProjectError(ex77);
					Exception ex78 = ex77;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsPatternTargets != GlobalForm.PatternTargets) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "PatternTargets", (object)GlobalForm.PatternTargets);
					}
				}
				catch (Exception ex79)
				{
					ProjectData.SetProjectError(ex79);
					Exception ex80 = ex79;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsShowConfirmation != GlobalForm.ShowConfirmation) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "Confirmation", (object)GlobalForm.ShowConfirmation);
					}
				}
				catch (Exception ex81)
				{
					ProjectData.SetProjectError(ex81);
					Exception ex82 = ex81;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsShowStopLoss != GlobalForm.ShowStopLoss) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "StopLoss", (object)GlobalForm.ShowStopLoss);
					}
				}
				catch (Exception ex83)
				{
					ProjectData.SetProjectError(ex83);
					Exception ex84 = ex83;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsShowTargetprice != GlobalForm.ShowTargetprice) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "TargetPrice", (object)GlobalForm.ShowTargetprice);
					}
				}
				catch (Exception ex85)
				{
					ProjectData.SetProjectError(ex85);
					Exception ex86 = ex85;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsShowUltHighLow != GlobalForm.ShowUltHighLow) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "UltHighLow", (object)GlobalForm.ShowUltHighLow);
					}
				}
				catch (Exception ex87)
				{
					ProjectData.SetProjectError(ex87);
					Exception ex88 = ex87;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsShowUnHit != GlobalForm.ShowUnHit) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ShowUnhit", (object)GlobalForm.ShowUnHit);
					}
				}
				catch (Exception ex89)
				{
					ProjectData.SetProjectError(ex89);
					Exception ex90 = ex89;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsShowUpTarget != GlobalForm.ShowUpTarget) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ShowUpTarget", (object)GlobalForm.ShowUpTarget);
					}
				}
				catch (Exception ex91)
				{
					ProjectData.SetProjectError(ex91);
					Exception ex92 = ex91;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsShowUpPercentage != GlobalForm.ShowUpPercentage) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ShowUpPercentage", (object)GlobalForm.ShowUpPercentage);
					}
				}
				catch (Exception ex93)
				{
					ProjectData.SetProjectError(ex93);
					Exception ex94 = ex93;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsShowDownTarget != GlobalForm.ShowDownTarget) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ShowDownTarget", (object)GlobalForm.ShowDownTarget);
					}
				}
				catch (Exception ex95)
				{
					ProjectData.SetProjectError(ex95);
					Exception ex96 = ex95;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsShowDownPercentage != GlobalForm.ShowDownPercentage) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ShowDownPercentage", (object)GlobalForm.ShowDownPercentage);
					}
				}
				catch (Exception ex97)
				{
					ProjectData.SetProjectError(ex97);
					Exception ex98 = ex97;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsSkipType != GlobalForm.SkipType) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "SkipType", (object)GlobalForm.SkipType);
					}
				}
				catch (Exception ex99)
				{
					ProjectData.SetProjectError(ex99);
					Exception ex100 = ex99;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsShowBARRLines != GlobalForm.ShowBARRLines) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "BARR", (object)GlobalForm.ShowBARRLines);
					}
				}
				catch (Exception ex101)
				{
					ProjectData.SetProjectError(ex101);
					Exception ex102 = ex101;
					ProjectData.ClearProjectError();
				}
				try
				{
					if (FindCandles.CLChanged | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\CandleForm", "CandleList", (object)FindCandles.CandleList, RegistryValueKind.Binary);
					}
				}
				catch (Exception ex103)
				{
					ProjectData.SetProjectError(ex103);
					Exception ex104 = ex103;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((Operators.CompareString(GlobalForm.IndexSymbol, lsIndexSymbol, false) != 0) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\IndicatorsForm", "IndexSymbol", (object)GlobalForm.IndexSymbol);
					}
				}
				catch (Exception ex105)
				{
					ProjectData.SetProjectError(ex105);
					Exception ex106 = ex105;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.CPIDateLookback != lsCPIDateLookBack) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\IndicatorsForm", "CPIDateLookback", (object)GlobalForm.CPIDateLookback);
					}
				}
				catch (Exception ex107)
				{
					ProjectData.SetProjectError(ex107);
					Exception ex108 = ex107;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.RadButton != lsRadButton) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\IndicatorsForm", "RadButton", (object)GlobalForm.RadButton);
					}
				}
				catch (Exception ex109)
				{
					ProjectData.SetProjectError(ex109);
					Exception ex110 = ex109;
					ProjectData.ClearProjectError();
				}
				try
				{
					((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\LicenseForm", "License", (object)GlobalForm.SignedLicense);
				}
				catch (Exception ex111)
				{
					ProjectData.SetProjectError(ex111);
					Exception ex112 = ex111;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.LFDateLookBack != lsLFDateLookBack) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ListForm", "LFDateLookback", (object)GlobalForm.LFDateLookBack);
					}
				}
				catch (Exception ex113)
				{
					ProjectData.SetProjectError(ex113);
					Exception ex114 = ex113;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.LFPatterns != lsLFPatterns) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ListForm", "LFPatterns", (object)GlobalForm.LFPatterns);
					}
				}
				catch (Exception ex115)
				{
					ProjectData.SetProjectError(ex115);
					Exception ex116 = ex115;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.LFCandles != lsLFCandles) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ListForm", "LFCandles", (object)GlobalForm.LFCandles);
					}
				}
				catch (Exception ex117)
				{
					ProjectData.SetProjectError(ex117);
					Exception ex118 = ex117;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsLCFPatternTargets != GlobalForm.LCFPatternTargets) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ListChartForm", "LCFPatternTargets", (object)GlobalForm.LCFPatternTargets);
					}
				}
				catch (Exception ex119)
				{
					ProjectData.SetProjectError(ex119);
					Exception ex120 = ex119;
					ProjectData.ClearProjectError();
				}
				try
				{
					if (GlobalForm.NewsOptionsChanged | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\NewsForm", "NewsOptions", (object)GlobalForm.NewsOptions);
					}
				}
				catch (Exception ex121)
				{
					ProjectData.SetProjectError(ex121);
					Exception ex122 = ex121;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsArticleNumber != GlobalForm.ArticleNumber) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\NewsForm", "ArticleNumber", (object)GlobalForm.ArticleNumber);
					}
				}
				catch (Exception ex123)
				{
					ProjectData.SetProjectError(ex123);
					Exception ex124 = ex123;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsNewsDateRB != GlobalForm.NewsDateRB) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\NewsForm", "DateRB", (object)GlobalForm.NewsDateRB);
					}
				}
				catch (Exception ex125)
				{
					ProjectData.SetProjectError(ex125);
					Exception ex126 = ex125;
					ProjectData.ClearProjectError();
				}
				try
				{
					if (GlobalForm.pfPRChanged | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PatternForm", "PctRise", (object)GlobalForm.pfPctRise);
					}
				}
				catch (Exception ex127)
				{
					ProjectData.SetProjectError(ex127);
					Exception ex128 = ex127;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((Convert.ToDouble(GlobalForm.GapSize) != lsGapSize) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PatternForm", "GapSize", (object)GlobalForm.GapSize);
					}
				}
				catch (Exception ex129)
				{
					ProjectData.SetProjectError(ex129);
					Exception ex130 = ex129;
					ProjectData.ClearProjectError();
				}
				try
				{
					if (GlobalForm.PLChanged | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PatternForm", "PatternList", (object)GlobalForm.PatternList, RegistryValueKind.Binary);
					}
				}
				catch (Exception ex131)
				{
					ProjectData.SetProjectError(ex131);
					Exception ex132 = ex131;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.TLUpLength != lsTLUpLength) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PatternForm", "TLUpLength", (object)GlobalForm.TLUpLength);
					}
				}
				catch (Exception ex133)
				{
					ProjectData.SetProjectError(ex133);
					Exception ex134 = ex133;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.TLDNLength != lsTLDNLength) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PatternForm", "TLDnLength", (object)GlobalForm.TLDNLength);
					}
				}
				catch (Exception ex135)
				{
					ProjectData.SetProjectError(ex135);
					Exception ex136 = ex135;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.SFDayOfWeek != lsDayOfWeek) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SeasonalityForm", "DayOfWeek", (object)GlobalForm.SFDayOfWeek);
					}
				}
				catch (Exception ex137)
				{
					ProjectData.SetProjectError(ex137);
					Exception ex138 = ex137;
					ProjectData.ClearProjectError();
				}
				try
				{
					if (GlobalForm.SFMonthLB != lsMonthLB)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SeasonalityForm", "Month", (object)GlobalForm.SFMonthLB);
					}
				}
				catch (Exception ex139)
				{
					ProjectData.SetProjectError(ex139);
					Exception ex140 = ex139;
					ProjectData.ClearProjectError();
				}
				try
				{
					if (GlobalForm.SFRBSelected != lsRBSelected)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SeasonalityForm", "Radio", (object)GlobalForm.SFRBSelected);
					}
				}
				catch (Exception ex141)
				{
					ProjectData.SetProjectError(ex141);
					Exception ex142 = ex141;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.UFDateLookBack != lsUFDateLookBack) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "UFDateLookback", (object)GlobalForm.UFDateLookBack);
					}
				}
				catch (Exception ex143)
				{
					ProjectData.SetProjectError(ex143);
					Exception ex144 = ex143;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.UpdatePeriod != lsUpdatePeriod) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "UFUpdatePeriod", (object)GlobalForm.UpdatePeriod);
					}
				}
				catch (Exception ex145)
				{
					ProjectData.SetProjectError(ex145);
					Exception ex146 = ex145;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.UpdateSource != lsUpdateSource) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "UFUpdateSource", (object)GlobalForm.UpdateSource);
					}
				}
				catch (Exception ex147)
				{
					ProjectData.SetProjectError(ex147);
					Exception ex148 = ex147;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((Operators.CompareString(GlobalForm.DBName, GlobalForm.lsDBName, false) != 0) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "DBNameChange", (object)GlobalForm.DBName);
					}
				}
				catch (Exception ex149)
				{
					ProjectData.SetProjectError(ex149);
					Exception ex150 = ex149;
					ProjectData.ClearProjectError();
				}
				try
				{
					if (GlobalForm.lsDBList | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "DBList", (object)GlobalForm.DBList);
					}
				}
				catch (Exception ex151)
				{
					ProjectData.SetProjectError(ex151);
					Exception ex152 = ex151;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsAutoRetry != GlobalForm.AutoRetry) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "AutoRetry", (object)GlobalForm.AutoRetry);
					}
				}
				catch (Exception ex153)
				{
					ProjectData.SetProjectError(ex153);
					Exception ex154 = ex153;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.SDFUpdateSource != lsSDFUpdateSource) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SplitDivForm", "UpdateSource", (object)GlobalForm.SDFUpdateSource);
					}
				}
				catch (Exception ex155)
				{
					ProjectData.SetProjectError(ex155);
					Exception ex156 = ex155;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.Splits != lsSplits) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SplitDivForm", "Splits", (object)GlobalForm.Splits);
					}
				}
				catch (Exception ex157)
				{
					ProjectData.SetProjectError(ex157);
					Exception ex158 = ex157;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.Dividends != lsDividends) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SplitDivForm", "Dividends", (object)GlobalForm.Dividends);
					}
				}
				catch (Exception ex159)
				{
					ProjectData.SetProjectError(ex159);
					Exception ex160 = ex159;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.SDFDateLookBack != lsSDFDateLookBack) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SplitDivForm", "Lookback", (object)GlobalForm.SDFDateLookBack);
					}
				}
				catch (Exception ex161)
				{
					ProjectData.SetProjectError(ex161);
					Exception ex162 = ex161;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((lsEntireFile != GlobalForm.EntireFile) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FixSplitForm", "EntireFile", (object)GlobalForm.EntireFile);
					}
				}
				catch (Exception ex163)
				{
					ProjectData.SetProjectError(ex163);
					Exception ex164 = ex163;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.SFDateLookBack != lsSFDateLookBack) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ScoreForm", "Lookback", (object)GlobalForm.SFDateLookBack);
					}
				}
				catch (Exception ex165)
				{
					ProjectData.SetProjectError(ex165);
					Exception ex166 = ex165;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.SFStrict != lsSFStrict) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ScoreForm", "Strict", (object)GlobalForm.SFStrict);
					}
				}
				catch (Exception ex167)
				{
					ProjectData.SetProjectError(ex167);
					Exception ex168 = ex167;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.SFDWM != lsSFDWM) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ScoreForm", "TimePeriod", (object)GlobalForm.SFDWM);
					}
				}
				catch (Exception ex169)
				{
					ProjectData.SetProjectError(ex169);
					Exception ex170 = ex169;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.Vendor != lsVendor) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ScoreForm", "Vendor", (object)GlobalForm.Vendor);
					}
				}
				catch (Exception ex171)
				{
					ProjectData.SetProjectError(ex171);
					Exception ex172 = ex171;
					ProjectData.ClearProjectError();
				}
				try
				{
					if ((GlobalForm.MSFCombo != lsMSFCombo) | FirstTime)
					{
						((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ManScoreForm", "Combo", (object)GlobalForm.MSFCombo);
					}
				}
				catch (Exception ex173)
				{
					ProjectData.SetProjectError(ex173);
					Exception ex174 = ex173;
					ProjectData.ClearProjectError();
				}
			}
			MySettingsProperty.Settings.MainFormLocation = ((Form)this).Location;
			MySettingsProperty.Settings.MainFormSize = ((Form)this).Size;
			((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
		}
	}

	private void Mainform_Load(object sender, EventArgs e)
	{
		//IL_003d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0042: Unknown result type (might be due to invalid IL or missing references)
		//IL_004d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0058: Unknown result type (might be due to invalid IL or missing references)
		//IL_0063: Unknown result type (might be due to invalid IL or missing references)
		//IL_006a: Unknown result type (might be due to invalid IL or missing references)
		//IL_007b: Unknown result type (might be due to invalid IL or missing references)
		//IL_008c: Unknown result type (might be due to invalid IL or missing references)
		//IL_009d: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ae: Unknown result type (might be due to invalid IL or missing references)
		//IL_00bf: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f2: Unknown result type (might be due to invalid IL or missing references)
		//IL_0103: Unknown result type (might be due to invalid IL or missing references)
		//IL_0114: Unknown result type (might be due to invalid IL or missing references)
		//IL_0125: Unknown result type (might be due to invalid IL or missing references)
		//IL_020b: Unknown result type (might be due to invalid IL or missing references)
		//IL_22ea: Unknown result type (might be due to invalid IL or missing references)
		//IL_019c: Unknown result type (might be due to invalid IL or missing references)
		//IL_2221: Unknown result type (might be due to invalid IL or missing references)
		//IL_01eb: Unknown result type (might be due to invalid IL or missing references)
		//IL_1836: Unknown result type (might be due to invalid IL or missing references)
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.MainFormLocation, MySettingsProperty.Settings.MainFormSize);
		Application.CurrentCulture = new CultureInfo("EN-US");
		LockFlag = true;
		lsWatchList = false;
		GlobalForm.NewsOptionsChanged = false;
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)AddButton, "Browse To the location of files you wish To add, enter a portfolio na then click Add.");
		val.SetToolTip((Control)(object)AllButton, "Select all of the symbols listed.");
		val.SetToolTip((Control)(object)ChangeButton, "Replace the portfolio name with a new one.");
		val.SetToolTip((Control)(object)ChartButton, "Load the form which displays chart patterns.");
		val.SetToolTip((Control)(object)PortfolioDataGridView, "Portfolio names appear here.");
		val.SetToolTip((Control)(object)DeleteButton, "Remove a portfolio from the list.");
		val.SetToolTip((Control)(object)HelpButton1, "Get help on portfolio controls.");
		val.SetToolTip((Control)(object)BrowseButton, "Locate files containing stock quotes for use by Patternz.");
		val.SetToolTip((Control)(object)ListButton, "Find chart patterns for copying into another program.");
		val.SetToolTip((Control)(object)PortfolioTextBox, "The name of the portfolio goes here.");
		val.SetToolTip((Control)(object)ShowPortfolioCheckBox, "Show or hide the portfolio watch list.");
		val.SetToolTip((Control)(object)SimulatorButton, "Practice trading.");
		val.SetToolTip((Control)(object)UpdateButton, "Update quote information.");
		((Form)this).Text = "ThePatternSite.com's Patternz Main Form Version: " + ((ApplicationBase)MyProject.Application).Info.Version.ToString();
		GlobalForm.FillDetails();
		try
		{
			if (((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\LicenseForm", "License", (object)null) == null)
			{
				FirstTime = true;
				((Form)MyProject.Forms.LicenseForm).ShowDialog();
			}
			else
			{
				FirstTime = false;
				GlobalForm.SignedLicense = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\LicenseForm", "License", (object)"0"));
				if (!GlobalForm.SignedLicense)
				{
					FirstTime = true;
					((Form)MyProject.Forms.LicenseForm).ShowDialog();
				}
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			FirstTime = true;
			((Form)MyProject.Forms.LicenseForm).ShowDialog();
			ProjectData.ClearProjectError();
		}
		if (!GlobalForm.SignedLicense)
		{
			((Form)this).Close();
		}
		LockFlag = false;
		GlobalForm.PathChanged = false;
		MainFormSizeChanged = false;
		GlobalForm.RemovePatternzFlag = false;
		lsShowPortfolio = false;
		ShowPortfolioCheckBox.Checked = false;
		GlobalForm.UserDate = "yyyy-MM-dd";
		FindCandles.CandleList = new byte[105]
		{
			1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
			1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
			1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
			1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
			1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
			1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
			1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
			1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
			1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
			1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
			1, 1, 1, 1, 1
		};
		GlobalForm.DateLookback = 400L;
		GlobalForm.ChartVolume = false;
		lsChartVolume = GlobalForm.ChartVolume;
		GlobalForm.ShowAllPatterns = true;
		lsShowAllPatterns = GlobalForm.ShowAllPatterns;
		GlobalForm.ShowCandles = true;
		FindCandles.lsShowCandles = GlobalForm.ShowCandles;
		lsChartPeriodShown = 0;
		GlobalForm.ChartPeriodShown = 0;
		GlobalForm.IncludePhrase = true;
		GlobalForm.Annotations = false;
		GlobalForm.MALength = 50;
		lsMALength = GlobalForm.MALength;
		GlobalForm.MAType = 1;
		lsMAType = GlobalForm.MAType;
		GlobalForm.MAUsed = false;
		lsMAUsed = GlobalForm.MAUsed;
		GlobalForm.ChartType = 0;
		lsChartType = GlobalForm.ChartType;
		GlobalForm.DecimalsUsed = GlobalForm.TWODECIMALS;
		lsUserDecimals = GlobalForm.TWODECIMALS;
		lsDecimalsOption = GlobalForm.DECIMALSFILE;
		GlobalForm.DiscardQuote = 1;
		GlobalForm.lsDiscardQuote = 1;
		GlobalForm.UpCandleColor = Color.FromArgb(255, 255, 255, 255);
		lsUpCandleColor = GlobalForm.UpCandleColor;
		GlobalForm.DownCandleColor = Color.FromArgb(255, 0, 0, 0);
		lsDownCandleColor = GlobalForm.DownCandleColor;
		GlobalForm.ChartBGColor = Color.FromArgb(255, 255, 255, 255);
		lsChartBGColor = GlobalForm.ChartBGColor;
		GlobalForm.VolumeBGColor = Color.FromArgb(255, 255, 128, 0);
		lsVolumeBGColor = GlobalForm.VolumeBGColor;
		GlobalForm.PriceBarColor = Color.FromArgb(255, 0, 0, 0);
		lsPriceBarColor = GlobalForm.PriceBarColor;
		GlobalForm.PatternTargets = true;
		GlobalForm.ShowConfirmation = true;
		GlobalForm.ShowStopLoss = true;
		GlobalForm.ShowTargetprice = true;
		GlobalForm.ShowUltHighLow = true;
		GlobalForm.ShowUnHit = false;
		GlobalForm.ShowUpTarget = false;
		GlobalForm.ShowUpPercentage = 20;
		GlobalForm.ShowDownTarget = false;
		GlobalForm.ShowBARRLines = false;
		GlobalForm.ShowDownPercentage = 8;
		GlobalForm.SkipType = 1;
		lsIndexSymbol = "";
		GlobalForm.IndexSymbol = lsIndexSymbol;
		GlobalForm.CPIDateLookback = 262L;
		GlobalForm.RadButton = 0;
		lsRadButton = GlobalForm.RadButton;
		lsEntireFile = false;
		GlobalForm.EntireFile = false;
		GlobalForm.LFDateLookBack = 400L;
		lsLFDateLookBack = GlobalForm.LFDateLookBack;
		GlobalForm.LFPatterns = true;
		lsLFPatterns = GlobalForm.LFPatterns;
		GlobalForm.LFCandles = false;
		lsLFCandles = GlobalForm.LFCandles;
		GlobalForm.LCFPatternTargets = true;
		GlobalForm.MSFCombo = 0;
		lsMSFCombo = GlobalForm.MSFCombo;
		Array.Copy(GlobalForm.NewsDEFAULTS, GlobalForm.NewsOptions, GlobalForm.NewsDEFAULTS.Length);
		GlobalForm.ArticleNumber = 10;
		GlobalForm.NewsDateRB = 2;
		GlobalForm.pfPctRise = GlobalForm.iDCBPERCENTRISE;
		GlobalForm.pfPRChanged = false;
		GlobalForm.GapSize = 0.2m;
		lsGapSize = 0.2;
		Array.Copy(GlobalForm.DEFAULTPATTERNLIST, GlobalForm.PatternList, GlobalForm.DEFAULTPATTERNLIST.Length);
		lsTLUpLength = 252;
		GlobalForm.TLUpLength = 252;
		lsTLDNLength = 252;
		GlobalForm.TLDNLength = 252;
		GlobalForm.SFDateLookBack = 100;
		lsSFDateLookBack = GlobalForm.SFDateLookBack;
		GlobalForm.SFStrict = false;
		lsSFStrict = GlobalForm.SFStrict;
		GlobalForm.SFDWM = 0;
		lsSFDWM = GlobalForm.SFDWM;
		GlobalForm.SFDayOfWeek = 1;
		GlobalForm.SFMonthLB = DateAndTime.Month(DateAndTime.Now);
		GlobalForm.SFRBSelected = GlobalForm.SFDaily;
		GlobalForm.SDFDateLookBack = 365;
		lsSDFDateLookBack = GlobalForm.SDFDateLookBack;
		GlobalForm.Splits = true;
		lsSplits = GlobalForm.Splits;
		GlobalForm.Dividends = true;
		lsDividends = GlobalForm.Dividends;
		GlobalForm.AutoRetry = false;
		lsAutoRetry = GlobalForm.AutoRetry;
		GlobalForm.UFDateLookBack = 400L;
		lsUFDateLookBack = GlobalForm.UFDateLookBack;
		GlobalForm.UpdatePeriod = 2;
		lsUpdatePeriod = GlobalForm.UpdatePeriod;
		GlobalForm.UpdateSource = 1;
		lsUpdateSource = GlobalForm.UpdateSource;
		GlobalForm.DBName = "WIKI (US EOD stock prices)";
		GlobalForm.lsDBName = GlobalForm.DBName;
		GlobalForm.DBList = new string[7] { "BSE (Bombay Stock Exchange)", "FSE (Frankfurt Stock Exchange)", "HKEX (Hong Kong Exchange)", "LSE (London Stock Exchange)", "NSE (National Stock Exchange of India)", "TSE (Tokyo Stock Exchange)", "WIKI (US EOD stock prices)" };
		GlobalForm.lsDBList = false;
		checked
		{
			try
			{
				if (((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "FilePath", (object)null) == null)
				{
					GlobalForm.FileFormat[0] = 1;
					GlobalForm.FileFormat[1] = 0;
					GlobalForm.FileFormat[2] = 2;
					GlobalForm.FileFormat[3] = 3;
					GlobalForm.FileFormat[4] = 4;
					GlobalForm.FileFormat[5] = 5;
					GlobalForm.FileFormat[6] = 6;
					GlobalForm.FileFormat[7] = 0;
					GlobalForm.ckFileFormat[1] = false;
					GlobalForm.ckFileFormat[2] = true;
					GlobalForm.ckFileFormat[6] = true;
					GlobalForm.ckFileFormat[7] = false;
					GlobalForm.ffDateTimeFormat = false;
					GlobalForm.FileFormatChanged = true;
					FindCandles.CandleList = new byte[105]
					{
						1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
						1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
						1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
						1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
						1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
						1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
						1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
						1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
						1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
						1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
						1, 1, 1, 1, 1
					};
				}
				else
				{
					try
					{
						((Control)this).Width = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "Width", (object)"649"));
					}
					catch (Exception ex3)
					{
						ProjectData.SetProjectError(ex3);
						Exception ex4 = ex3;
						ProjectData.ClearProjectError();
					}
					if (((Control)this).Width == 0)
					{
						((Control)this).Width = 649;
					}
					try
					{
						((Control)this).Height = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "Height", (object)"403"));
					}
					catch (Exception ex5)
					{
						ProjectData.SetProjectError(ex5);
						Exception ex6 = ex5;
						ProjectData.ClearProjectError();
					}
					if (((Control)this).Height == 0)
					{
						((Control)this).Height = 403;
					}
					try
					{
						lsShowPortfolio = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "ShowPortfolio", (object)false));
					}
					catch (Exception ex7)
					{
						ProjectData.SetProjectError(ex7);
						Exception ex8 = ex7;
						ProjectData.ClearProjectError();
					}
					ShowPortfolioCheckBox.Checked = lsShowPortfolio;
					try
					{
						string[] array = (string[])((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "PortfolioList", (object)"");
						if (Operators.CompareString(array[0], "", false) != 0)
						{
							LockFlag = true;
							int num = Information.UBound((Array)array, 1);
							for (int i = 0; i <= num; i += 2)
							{
								PortfolioDataGridView.Rows.Add();
								PortfolioDataGridView.Rows[PortfolioDataGridView.RowCount - 1].Cells[0].Value = array[i];
								PortfolioDataGridView.Rows[PortfolioDataGridView.RowCount - 1].Cells[1].Value = array[i + 1];
							}
							LockFlag = false;
						}
					}
					catch (Exception ex9)
					{
						ProjectData.SetProjectError(ex9);
						Exception ex10 = ex9;
						Debugger.Break();
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.FileFormat[0] = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ffDate", (object)"1"));
					}
					catch (Exception ex11)
					{
						ProjectData.SetProjectError(ex11);
						Exception ex12 = ex11;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.FileFormat[1] = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ffTime", (object)"0"));
					}
					catch (Exception ex13)
					{
						ProjectData.SetProjectError(ex13);
						Exception ex14 = ex13;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.FileFormat[2] = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "Open", (object)"2"));
					}
					catch (Exception ex15)
					{
						ProjectData.SetProjectError(ex15);
						Exception ex16 = ex15;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.FileFormat[3] = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "High", (object)"3"));
					}
					catch (Exception ex17)
					{
						ProjectData.SetProjectError(ex17);
						Exception ex18 = ex17;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.FileFormat[4] = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "Low", (object)"4"));
					}
					catch (Exception ex19)
					{
						ProjectData.SetProjectError(ex19);
						Exception ex20 = ex19;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.FileFormat[5] = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "Close", (object)"5"));
					}
					catch (Exception ex21)
					{
						ProjectData.SetProjectError(ex21);
						Exception ex22 = ex21;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.FileFormat[6] = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "Volume", (object)"6"));
					}
					catch (Exception ex23)
					{
						ProjectData.SetProjectError(ex23);
						Exception ex24 = ex23;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.FileFormat[7] = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "AdjClose", (object)"0"));
					}
					catch (Exception ex25)
					{
						ProjectData.SetProjectError(ex25);
						Exception ex26 = ex25;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.ckFileFormat[1] = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ckTime", (object)"0"));
					}
					catch (Exception ex27)
					{
						ProjectData.SetProjectError(ex27);
						Exception ex28 = ex27;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.ckFileFormat[2] = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ckOpen", (object)"-1"));
					}
					catch (Exception ex29)
					{
						ProjectData.SetProjectError(ex29);
						Exception ex30 = ex29;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.ckFileFormat[6] = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ckVolume", (object)"-1"));
					}
					catch (Exception ex31)
					{
						ProjectData.SetProjectError(ex31);
						Exception ex32 = ex31;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.ckFileFormat[7] = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ckAdjClose", (object)"0"));
					}
					catch (Exception ex33)
					{
						ProjectData.SetProjectError(ex33);
						Exception ex34 = ex33;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.UserDate = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "sDateFormat", (object)GlobalForm.UserDate));
					}
					catch (Exception ex35)
					{
						ProjectData.SetProjectError(ex35);
						Exception ex36 = ex35;
						ProjectData.ClearProjectError();
					}
					if (Operators.CompareString(GlobalForm.UserDate, (string)null, false) == 0)
					{
						GlobalForm.UserDate = "yyyy-MM-dd";
					}
					try
					{
						GlobalForm.ffDateTimeFormat = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FileFormatForm", "ffDateTimeFormat", (object)false));
					}
					catch (Exception ex37)
					{
						ProjectData.SetProjectError(ex37);
						Exception ex38 = ex37;
						ProjectData.ClearProjectError();
					}
					lsffDateTimeFormat = GlobalForm.ffDateTimeFormat;
					try
					{
						GlobalForm.DateLookback = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ChartForm", "DateLookback", (object)"400"));
					}
					catch (Exception ex39)
					{
						ProjectData.SetProjectError(ex39);
						Exception ex40 = ex39;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.DateLookback == 0L)
					{
						GlobalForm.DateLookback = 400L;
					}
					try
					{
						GlobalForm.ChartVolume = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ChartForm", "Volume", (object)false));
					}
					catch (Exception ex41)
					{
						ProjectData.SetProjectError(ex41);
						Exception ex42 = ex41;
						ProjectData.ClearProjectError();
					}
					lsChartVolume = GlobalForm.ChartVolume;
					try
					{
						GlobalForm.ShowAllPatterns = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ChartForm", "ShowAllPatterns", (object)true));
					}
					catch (Exception ex43)
					{
						ProjectData.SetProjectError(ex43);
						Exception ex44 = ex43;
						ProjectData.ClearProjectError();
					}
					lsShowAllPatterns = GlobalForm.ShowAllPatterns;
					try
					{
						GlobalForm.StrictPatterns = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ChartForm", "Strict", (object)true));
					}
					catch (Exception ex45)
					{
						ProjectData.SetProjectError(ex45);
						Exception ex46 = ex45;
						ProjectData.ClearProjectError();
					}
					lsStrictPatterns = GlobalForm.StrictPatterns;
					try
					{
						GlobalForm.ShowCandles = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ChartForm", "ShowCandles", (object)true));
					}
					catch (Exception ex47)
					{
						ProjectData.SetProjectError(ex47);
						Exception ex48 = ex47;
						ProjectData.ClearProjectError();
					}
					FindCandles.lsShowCandles = GlobalForm.ShowCandles;
					try
					{
						GlobalForm.ChartPeriodShown = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ChartForm", "ChartPeriodShown", (object)0));
					}
					catch (Exception ex49)
					{
						ProjectData.SetProjectError(ex49);
						Exception ex50 = ex49;
						ProjectData.ClearProjectError();
					}
					lsChartPeriodShown = GlobalForm.ChartPeriodShown;
					try
					{
						GlobalForm.IncludePhrase = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "IncludePhrase", (object)true));
					}
					catch (Exception ex51)
					{
						ProjectData.SetProjectError(ex51);
						Exception ex52 = ex51;
						ProjectData.ClearProjectError();
					}
					lsIncludePhrase = GlobalForm.IncludePhrase;
					try
					{
						GlobalForm.Annotations = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "Annotations", (object)false));
					}
					catch (Exception ex53)
					{
						ProjectData.SetProjectError(ex53);
						Exception ex54 = ex53;
						ProjectData.ClearProjectError();
					}
					lsAnnotations = GlobalForm.Annotations;
					try
					{
						GlobalForm.MALength = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "MALength", (object)50));
					}
					catch (Exception ex55)
					{
						ProjectData.SetProjectError(ex55);
						Exception ex56 = ex55;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.MALength == 0)
					{
						GlobalForm.MALength = 50;
					}
					lsMALength = GlobalForm.MALength;
					try
					{
						GlobalForm.MAType = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "MAType", (object)1));
					}
					catch (Exception ex57)
					{
						ProjectData.SetProjectError(ex57);
						Exception ex58 = ex57;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.MAType == 0)
					{
						GlobalForm.MAType = 1;
					}
					lsMAType = GlobalForm.MAType;
					try
					{
						GlobalForm.MAUsed = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "MAUsed", (object)false));
					}
					catch (Exception ex59)
					{
						ProjectData.SetProjectError(ex59);
						Exception ex60 = ex59;
						ProjectData.ClearProjectError();
					}
					lsMAUsed = GlobalForm.MAUsed;
					try
					{
						GlobalForm.ChartType = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ChartType", (object)0));
					}
					catch (Exception ex61)
					{
						ProjectData.SetProjectError(ex61);
						Exception ex62 = ex61;
						ProjectData.ClearProjectError();
					}
					lsChartType = GlobalForm.ChartType;
					try
					{
						GlobalForm.UserDecimals = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "Decimals", (object)GlobalForm.TWODECIMALS));
					}
					catch (Exception ex63)
					{
						ProjectData.SetProjectError(ex63);
						Exception ex64 = ex63;
						ProjectData.ClearProjectError();
					}
					lsUserDecimals = GlobalForm.UserDecimals;
					GlobalForm.DecimalsUsed = GlobalForm.UserDecimals;
					try
					{
						GlobalForm.DecimalsOption = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "DecimalOpt", (object)GlobalForm.DECIMALSFILE));
					}
					catch (Exception ex65)
					{
						ProjectData.SetProjectError(ex65);
						Exception ex66 = ex65;
						ProjectData.ClearProjectError();
					}
					lsDecimalsOption = GlobalForm.DecimalsOption;
					try
					{
						GlobalForm.DiscardQuote = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "DiscardQuote", (object)1));
					}
					catch (Exception ex67)
					{
						ProjectData.SetProjectError(ex67);
						Exception ex68 = ex67;
						ProjectData.ClearProjectError();
					}
					GlobalForm.lsDiscardQuote = GlobalForm.DiscardQuote;
					try
					{
						GlobalForm.PriceBarColor = Color.FromArgb(Convert.ToInt32(RuntimeHelpers.GetObjectValue(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "PriceBarColor ", (object)Color.FromArgb(255, 0, 0, 0).ToArgb()))));
					}
					catch (Exception ex69)
					{
						ProjectData.SetProjectError(ex69);
						Exception ex70 = ex69;
						ProjectData.ClearProjectError();
					}
					lsPriceBarColor = GlobalForm.PriceBarColor;
					try
					{
						GlobalForm.VolumeBGColor = Color.FromArgb(Convert.ToInt32(RuntimeHelpers.GetObjectValue(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "VolumeBGColor", (object)Color.FromArgb(255, 255, 128, 0).ToArgb()))));
					}
					catch (Exception ex71)
					{
						ProjectData.SetProjectError(ex71);
						Exception ex72 = ex71;
						ProjectData.ClearProjectError();
					}
					lsVolumeBGColor = GlobalForm.VolumeBGColor;
					try
					{
						GlobalForm.UpCandleColor = Color.FromArgb(Convert.ToInt32(RuntimeHelpers.GetObjectValue(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "UpCandleColor", (object)Color.FromArgb(255, 255, 255, 255).ToArgb()))));
					}
					catch (Exception ex73)
					{
						ProjectData.SetProjectError(ex73);
						Exception ex74 = ex73;
						ProjectData.ClearProjectError();
					}
					lsUpCandleColor = GlobalForm.UpCandleColor;
					try
					{
						GlobalForm.DownCandleColor = Color.FromArgb(Convert.ToInt32(RuntimeHelpers.GetObjectValue(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "DownCandleColor", (object)Color.FromArgb(255, 0, 0, 0).ToArgb()))));
					}
					catch (Exception ex75)
					{
						ProjectData.SetProjectError(ex75);
						Exception ex76 = ex75;
						ProjectData.ClearProjectError();
					}
					lsDownCandleColor = GlobalForm.DownCandleColor;
					try
					{
						GlobalForm.ChartBGColor = Color.FromArgb(Convert.ToInt32(RuntimeHelpers.GetObjectValue(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ChartBGColor", (object)Color.FromArgb(255, 255, 255, 255).ToArgb()))));
					}
					catch (Exception ex77)
					{
						ProjectData.SetProjectError(ex77);
						Exception ex78 = ex77;
						ProjectData.ClearProjectError();
					}
					lsChartBGColor = GlobalForm.ChartBGColor;
					try
					{
						GlobalForm.PatternTargets = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "PatternTargets", (object)true));
					}
					catch (Exception ex79)
					{
						ProjectData.SetProjectError(ex79);
						Exception ex80 = ex79;
						ProjectData.ClearProjectError();
					}
					lsPatternTargets = GlobalForm.PatternTargets;
					try
					{
						GlobalForm.ShowConfirmation = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "Confirmation", (object)true));
					}
					catch (Exception ex81)
					{
						ProjectData.SetProjectError(ex81);
						Exception ex82 = ex81;
						ProjectData.ClearProjectError();
					}
					lsShowConfirmation = GlobalForm.ShowConfirmation;
					try
					{
						GlobalForm.ShowStopLoss = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "StopLoss", (object)true));
					}
					catch (Exception ex83)
					{
						ProjectData.SetProjectError(ex83);
						Exception ex84 = ex83;
						ProjectData.ClearProjectError();
					}
					lsShowStopLoss = GlobalForm.ShowStopLoss;
					try
					{
						GlobalForm.ShowTargetprice = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "TargetPrice", (object)true));
					}
					catch (Exception ex85)
					{
						ProjectData.SetProjectError(ex85);
						Exception ex86 = ex85;
						ProjectData.ClearProjectError();
					}
					lsShowTargetprice = GlobalForm.ShowTargetprice;
					try
					{
						GlobalForm.ShowUltHighLow = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "UltHighLow", (object)true));
					}
					catch (Exception ex87)
					{
						ProjectData.SetProjectError(ex87);
						Exception ex88 = ex87;
						ProjectData.ClearProjectError();
					}
					lsShowUltHighLow = GlobalForm.ShowUltHighLow;
					try
					{
						GlobalForm.ShowUnHit = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ShowUnhit", (object)false));
					}
					catch (Exception ex89)
					{
						ProjectData.SetProjectError(ex89);
						Exception ex90 = ex89;
						ProjectData.ClearProjectError();
					}
					lsShowUnHit = GlobalForm.ShowUnHit;
					try
					{
						GlobalForm.ShowUpTarget = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ShowUpTarget", (object)false));
					}
					catch (Exception ex91)
					{
						ProjectData.SetProjectError(ex91);
						Exception ex92 = ex91;
						ProjectData.ClearProjectError();
					}
					lsShowUpTarget = GlobalForm.ShowUpTarget;
					try
					{
						GlobalForm.ShowUpPercentage = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ShowUpPercentage", (object)20));
					}
					catch (Exception ex93)
					{
						ProjectData.SetProjectError(ex93);
						Exception ex94 = ex93;
						ProjectData.ClearProjectError();
					}
					lsShowUpPercentage = GlobalForm.ShowUpPercentage;
					try
					{
						GlobalForm.ShowDownTarget = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ShowDownTarget", (object)false));
					}
					catch (Exception ex95)
					{
						ProjectData.SetProjectError(ex95);
						Exception ex96 = ex95;
						ProjectData.ClearProjectError();
					}
					lsShowDownTarget = GlobalForm.ShowDownTarget;
					try
					{
						GlobalForm.ShowDownPercentage = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "ShowDownPercentage", (object)8));
					}
					catch (Exception ex97)
					{
						ProjectData.SetProjectError(ex97);
						Exception ex98 = ex97;
						ProjectData.ClearProjectError();
					}
					lsShowDownPercentage = GlobalForm.ShowDownPercentage;
					try
					{
						GlobalForm.SkipType = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "SkipType", (object)1));
					}
					catch (Exception ex99)
					{
						ProjectData.SetProjectError(ex99);
						Exception ex100 = ex99;
						ProjectData.ClearProjectError();
					}
					lsSkipType = GlobalForm.SkipType;
					try
					{
						GlobalForm.ShowBARRLines = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SetupForm", "BARR", (object)false));
					}
					catch (Exception ex101)
					{
						ProjectData.SetProjectError(ex101);
						Exception ex102 = ex101;
						ProjectData.ClearProjectError();
					}
					lsShowBARRLines = GlobalForm.ShowBARRLines;
					try
					{
						GlobalForm.NewsOptions = (byte[])((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\NewsForm", "NewsOptions", (object)GlobalForm.NewsDEFAULTS);
					}
					catch (Exception ex103)
					{
						ProjectData.SetProjectError(ex103);
						Exception ex104 = ex103;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.ArticleNumber = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\NewsForm", "ArticleNumber", (object)10));
					}
					catch (Exception ex105)
					{
						ProjectData.SetProjectError(ex105);
						Exception ex106 = ex105;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.ArticleNumber == 0)
					{
						GlobalForm.ArticleNumber = 10;
					}
					lsArticleNumber = GlobalForm.ArticleNumber;
					try
					{
						GlobalForm.NewsDateRB = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\NewsForm", "DateRB", (object)1));
					}
					catch (Exception ex107)
					{
						ProjectData.SetProjectError(ex107);
						Exception ex108 = ex107;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.NewsDateRB == 0)
					{
						GlobalForm.NewsDateRB = 2;
					}
					lsNewsDateRB = GlobalForm.NewsDateRB;
					try
					{
						GlobalForm.pfPctRise = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PatternForm", "PctRise", (object)GlobalForm.iDCBPERCENTRISE));
					}
					catch (Exception ex109)
					{
						ProjectData.SetProjectError(ex109);
						Exception ex110 = ex109;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.pfPctRise == 0)
					{
						GlobalForm.pfPctRise = GlobalForm.iDCBPERCENTRISE;
					}
					try
					{
						GlobalForm.GapSize = Conversions.ToDecimal(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PatternForm", "GapSize", (object)0.2m));
					}
					catch (Exception ex111)
					{
						ProjectData.SetProjectError(ex111);
						Exception ex112 = ex111;
						ProjectData.ClearProjectError();
					}
					if (decimal.Compare(GlobalForm.GapSize, 0m) == 0)
					{
						GlobalForm.GapSize = 0.2m;
					}
					try
					{
						GlobalForm.PatternList = (byte[])((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PatternForm", "PatternList", (object)GlobalForm.DEFAULTPATTERNLIST);
					}
					catch (Exception ex113)
					{
						ProjectData.SetProjectError(ex113);
						Exception ex114 = ex113;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.PatternList == null)
					{
						Array.Copy(GlobalForm.DEFAULTPATTERNLIST, GlobalForm.PatternList, GlobalForm.DEFAULTPATTERNLIST.Length);
						GlobalForm.PLChanged = true;
					}
					else if (GlobalForm.PatternList.Length != GlobalForm.DEFAULTPATTERNLIST.Length)
					{
						GlobalForm.PatternList = null;
						GlobalForm.PatternList = GlobalForm.DEFAULTPATTERNLIST;
						Array.Copy(GlobalForm.DEFAULTPATTERNLIST, GlobalForm.PatternList, GlobalForm.DEFAULTPATTERNLIST.Length);
						GlobalForm.PLChanged = true;
						MessageBox.Show("I changed the patterns form, so you'll have to pick new chart patterns from the list. See the Main Menu, Patterns menu item.", "MainForm: Mainform_Load", (MessageBoxButtons)0, (MessageBoxIcon)64);
					}
					try
					{
						GlobalForm.TLUpLength = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PatternForm", "TLUpLength", (object)252));
					}
					catch (Exception ex115)
					{
						ProjectData.SetProjectError(ex115);
						Exception ex116 = ex115;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.TLUpLength == 0)
					{
						GlobalForm.TLUpLength = 252;
					}
					lsTLUpLength = GlobalForm.TLUpLength;
					try
					{
						GlobalForm.TLDNLength = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PatternForm", "TLDnLength", (object)252));
					}
					catch (Exception ex117)
					{
						ProjectData.SetProjectError(ex117);
						Exception ex118 = ex117;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.TLDNLength == 0)
					{
						GlobalForm.TLDNLength = 252;
					}
					lsTLDNLength = GlobalForm.TLDNLength;
					try
					{
						FindCandles.CandleList = (byte[])((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\CandleForm", "CandleList", (object)0);
					}
					catch (Exception ex119)
					{
						ProjectData.SetProjectError(ex119);
						Exception ex120 = ex119;
						ProjectData.ClearProjectError();
					}
					if (FindCandles.CandleList == null)
					{
						FindCandles.CandleList = new byte[105]
						{
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
							1, 1, 1, 1, 1
						};
					}
					try
					{
						GlobalForm.IndexSymbol = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\IndicatorsForm", "IndexSymbol", (object)""));
					}
					catch (Exception ex121)
					{
						ProjectData.SetProjectError(ex121);
						Exception ex122 = ex121;
						ProjectData.ClearProjectError();
					}
					lsIndexSymbol = GlobalForm.IndexSymbol;
					try
					{
						GlobalForm.CPIDateLookback = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\IndicatorsForm", "CPIDateLookback", (object)"262"));
					}
					catch (Exception ex123)
					{
						ProjectData.SetProjectError(ex123);
						Exception ex124 = ex123;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.CPIDateLookback == 0L)
					{
						GlobalForm.CPIDateLookback = 262L;
					}
					try
					{
						GlobalForm.RadButton = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\IndicatorsForm", "RadButton", (object)"0"));
					}
					catch (Exception ex125)
					{
						ProjectData.SetProjectError(ex125);
						Exception ex126 = ex125;
						ProjectData.ClearProjectError();
					}
					lsRadButton = GlobalForm.RadButton;
					try
					{
						GlobalForm.LFDateLookBack = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ListForm", "LFDateLookback", (object)"400"));
					}
					catch (Exception ex127)
					{
						ProjectData.SetProjectError(ex127);
						Exception ex128 = ex127;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.LFDateLookBack == 0L)
					{
						GlobalForm.LFDateLookBack = 400L;
					}
					lsLFDateLookBack = GlobalForm.LFDateLookBack;
					try
					{
						GlobalForm.LFPatterns = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ListForm", "LFPatterns", (object)true));
					}
					catch (Exception ex129)
					{
						ProjectData.SetProjectError(ex129);
						Exception ex130 = ex129;
						ProjectData.ClearProjectError();
					}
					lsLFPatterns = GlobalForm.LFPatterns;
					try
					{
						GlobalForm.LFCandles = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ListForm", "LFCandles", (object)false));
					}
					catch (Exception ex131)
					{
						ProjectData.SetProjectError(ex131);
						Exception ex132 = ex131;
						ProjectData.ClearProjectError();
					}
					lsLFCandles = GlobalForm.LFCandles;
					try
					{
						GlobalForm.LCFPatternTargets = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ListChartForm", "LCFPatternTargets", (object)true));
					}
					catch (Exception ex133)
					{
						ProjectData.SetProjectError(ex133);
						Exception ex134 = ex133;
						ProjectData.ClearProjectError();
					}
					lsLCFPatternTargets = GlobalForm.LCFPatternTargets;
					try
					{
						GlobalForm.AutoRetry = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "AutoRetry", (object)false));
					}
					catch (Exception ex135)
					{
						ProjectData.SetProjectError(ex135);
						Exception ex136 = ex135;
						ProjectData.ClearProjectError();
					}
					lsAutoRetry = GlobalForm.AutoRetry;
					try
					{
						GlobalForm.UFDateLookBack = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "UFDateLookback", (object)"400"));
					}
					catch (Exception ex137)
					{
						ProjectData.SetProjectError(ex137);
						Exception ex138 = ex137;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.UFDateLookBack == 0L)
					{
						GlobalForm.UFDateLookBack = 400L;
					}
					lsUFDateLookBack = GlobalForm.UFDateLookBack;
					try
					{
						GlobalForm.UpdatePeriod = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "UFUpdatePeriod", (object)"2"));
					}
					catch (Exception ex139)
					{
						ProjectData.SetProjectError(ex139);
						Exception ex140 = ex139;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.UpdatePeriod == 0)
					{
						GlobalForm.UpdatePeriod = 2;
					}
					lsUpdatePeriod = GlobalForm.UpdatePeriod;
					try
					{
						GlobalForm.UpdateSource = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "UFUpdateSource", (object)"1"));
					}
					catch (Exception ex141)
					{
						ProjectData.SetProjectError(ex141);
						Exception ex142 = ex141;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.UpdateSource == 0)
					{
						GlobalForm.UpdateSource = 1;
					}
					lsUpdateSource = GlobalForm.UpdateSource;
					try
					{
						GlobalForm.DBName = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "DBNameChange", (object)"WIKI (US EOD stock prices)"));
					}
					catch (Exception ex143)
					{
						ProjectData.SetProjectError(ex143);
						Exception ex144 = ex143;
						ProjectData.ClearProjectError();
					}
					try
					{
						if (GlobalForm.DBName == null)
						{
							GlobalForm.DBName = "WIKI (US EOD stock prices)";
						}
						GlobalForm.lsDBName = GlobalForm.DBName;
						GlobalForm.DBList = (string[])((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "DBList", (object)new string[7] { "BSE (Bombay Stock Exchange)", "FSE (Frankfurt Stock Exchange)", "HKEX (Hong Kong Exchange)", "LSE (London Stock Exchange)", "NSE (National Stock Exchange of India)", "TSE (Tokyo Stock Exchange)", "WIKI (US EOD stock prices)" });
					}
					catch (Exception ex145)
					{
						ProjectData.SetProjectError(ex145);
						Exception ex146 = ex145;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.DBList == null)
					{
						GlobalForm.DBList = new string[7] { "BSE (Bombay Stock Exchange)", "FSE (Frankfurt Stock Exchange)", "HKEX (Hong Kong Exchange)", "LSE (London Stock Exchange)", "NSE (National Stock Exchange of India)", "TSE (Tokyo Stock Exchange)", "WIKI (US EOD stock prices)" };
					}
					GlobalForm.lsDBList = false;
					try
					{
						GlobalForm.SFDayOfWeek = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SeasonalityForm", "DayOfWeek", (object)1));
					}
					catch (Exception ex147)
					{
						ProjectData.SetProjectError(ex147);
						Exception ex148 = ex147;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.SFDayOfWeek == 0)
					{
						GlobalForm.SFDayOfWeek = 1;
					}
					lsDayOfWeek = GlobalForm.SFDayOfWeek;
					try
					{
						GlobalForm.SFMonthLB = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SeasonalityForm", "Month", (object)DateAndTime.Month(DateAndTime.Now)));
					}
					catch (Exception ex149)
					{
						ProjectData.SetProjectError(ex149);
						Exception ex150 = ex149;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.SFMonthLB == 0)
					{
						GlobalForm.SFMonthLB = DateAndTime.Month(DateAndTime.Now);
					}
					lsMonthLB = GlobalForm.SFMonthLB;
					try
					{
						GlobalForm.SFRBSelected = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SeasonalityForm", "Radio", (object)GlobalForm.SFDaily));
					}
					catch (Exception ex151)
					{
						ProjectData.SetProjectError(ex151);
						Exception ex152 = ex151;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.SFRBSelected == 0)
					{
						GlobalForm.SFRBSelected = GlobalForm.SFDaily;
					}
					lsRBSelected = GlobalForm.SFRBSelected;
					try
					{
						GlobalForm.SDFUpdateSource = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SplitDivForm", "UpdateSource", (object)"4"));
					}
					catch (Exception ex153)
					{
						ProjectData.SetProjectError(ex153);
						Exception ex154 = ex153;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.SDFUpdateSource == 0)
					{
						GlobalForm.SDFUpdateSource = 4;
					}
					lsSDFUpdateSource = GlobalForm.SDFUpdateSource;
					try
					{
						lsSplits = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SplitDivForm", "Splits", (object)true));
					}
					catch (Exception ex155)
					{
						ProjectData.SetProjectError(ex155);
						Exception ex156 = ex155;
						ProjectData.ClearProjectError();
					}
					GlobalForm.Splits = lsSplits;
					try
					{
						lsDividends = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SplitDivForm", "Dividends", (object)true));
					}
					catch (Exception ex157)
					{
						ProjectData.SetProjectError(ex157);
						Exception ex158 = ex157;
						ProjectData.ClearProjectError();
					}
					GlobalForm.Dividends = lsDividends;
					try
					{
						GlobalForm.SDFDateLookBack = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SplitDivForm", "Lookback", (object)"365"));
					}
					catch (Exception ex159)
					{
						ProjectData.SetProjectError(ex159);
						Exception ex160 = ex159;
						ProjectData.ClearProjectError();
					}
					if (lsSDFDateLookBack == 0)
					{
						GlobalForm.SDFDateLookBack = 365;
					}
					try
					{
						lsEntireFile = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FixSplitForm", "EntireFile", (object)false));
						GlobalForm.EntireFile = lsEntireFile;
					}
					catch (Exception ex161)
					{
						ProjectData.SetProjectError(ex161);
						Exception ex162 = ex161;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.SFDateLookBack = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ScoreForm", "Lookback", (object)"100"));
					}
					catch (Exception ex163)
					{
						ProjectData.SetProjectError(ex163);
						Exception ex164 = ex163;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.SFDateLookBack == 0)
					{
						GlobalForm.SFDateLookBack = 100;
					}
					lsSFDateLookBack = GlobalForm.SFDateLookBack;
					try
					{
						GlobalForm.SFStrict = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ScoreForm", "Strict", (object)false));
					}
					catch (Exception ex165)
					{
						ProjectData.SetProjectError(ex165);
						Exception ex166 = ex165;
						ProjectData.ClearProjectError();
					}
					lsSFStrict = GlobalForm.SFStrict;
					try
					{
						GlobalForm.SFDWM = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ScoreForm", "TimePeriod", (object)0.ToString()));
					}
					catch (Exception ex167)
					{
						ProjectData.SetProjectError(ex167);
						Exception ex168 = ex167;
						ProjectData.ClearProjectError();
					}
					try
					{
						GlobalForm.Vendor = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ScoreForm", "Vendor", (object)GlobalForm.FINNHUB));
					}
					catch (Exception ex169)
					{
						ProjectData.SetProjectError(ex169);
						Exception ex170 = ex169;
						ProjectData.ClearProjectError();
					}
					if (GlobalForm.Vendor == 0)
					{
						GlobalForm.Vendor = GlobalForm.FINNHUB;
					}
					lsVendor = GlobalForm.Vendor;
					try
					{
						GlobalForm.MSFCombo = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\ManScoreForm", "Combo", (object)"1"));
					}
					catch (Exception ex171)
					{
						ProjectData.SetProjectError(ex171);
						Exception ex172 = ex171;
						ProjectData.ClearProjectError();
					}
					lsMSFCombo = GlobalForm.MSFCombo;
				}
			}
			catch (Exception ex173)
			{
				ProjectData.SetProjectError(ex173);
				Exception ex174 = ex173;
				ProjectData.ClearProjectError();
			}
			GlobalForm.ckFileFormat[0] = true;
			GlobalForm.ckFileFormat[3] = true;
			GlobalForm.ckFileFormat[4] = true;
			GlobalForm.ckFileFormat[5] = true;
			try
			{
				GlobalForm.OpenPath = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "FilePath", (object)""));
			}
			catch (Exception ex175)
			{
				ProjectData.SetProjectError(ex175);
				Exception ex176 = ex175;
				GlobalForm.OpenPath = "";
				ProjectData.ClearProjectError();
			}
			if (Operators.CompareString(GlobalForm.OpenPath, "", false) == 0)
			{
				MessageBox.Show("Select a path to where the stock data files are Or WILL BE (you can do this later, too, by clicking the 'Browse Portfolio Location' button when the main form loads).", "MainForm: Mainform_Load", (MessageBoxButtons)0, (MessageBoxIcon)64);
				BrowseButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			}
			else
			{
				MFDisplayFiles(BrowseFlag: false);
			}
			GlobalForm.ConfigLocation = "";
			try
			{
				GlobalForm.ConfigLocation = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "ConfigPath", (object)(GlobalForm.OpenPath + "\\Configs")));
			}
			catch (Exception ex177)
			{
				ProjectData.SetProjectError(ex177);
				Exception ex178 = ex177;
				ProjectData.ClearProjectError();
			}
			if (!Directory.Exists(GlobalForm.ConfigLocation))
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "ConfigPath", (object)(GlobalForm.OpenPath + "\\Configs"));
				try
				{
					Directory.CreateDirectory(GlobalForm.ConfigLocation);
				}
				catch (Exception ex179)
				{
					ProjectData.SetProjectError(ex179);
					Exception ex180 = ex179;
					MessageBox.Show("Can't create Configs folder to store the config files at: " + GlobalForm.ConfigLocation, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
					ProjectData.ClearProjectError();
				}
			}
			int num2 = 0;
			try
			{
				num2 = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "SelectedCount", (object)0));
			}
			catch (Exception ex181)
			{
				ProjectData.SetProjectError(ex181);
				Exception ex182 = ex181;
				ProjectData.ClearProjectError();
			}
			if ((num2 > 0) & (num2 <= ListBox1.Items.Count))
			{
				try
				{
					string[] array2 = new string[num2 - 1 + 1];
					array2 = (string[])((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\MainForm", "SelectedList", (object)"");
					int num3 = num2 - 1;
					for (int j = 0; j <= num3; j++)
					{
						if (Conversions.ToInteger(array2[j]) < ListBox1.Items.Count)
						{
							ListBox1.SetSelected(Conversions.ToInteger(array2[j]), true);
						}
					}
				}
				catch (Exception ex183)
				{
					ProjectData.SetProjectError(ex183);
					Exception ex184 = ex183;
					ProjectData.ClearProjectError();
				}
			}
			PortWatchButtons(Conversions.ToBoolean(Interaction.IIf(PortfolioDataGridView.RowCount == 0, (object)false, (object)true)));
			FileLocationLabel.Text = "File location: " + GlobalForm.OpenPath;
			SynchPortfolio();
			ListBox1_SelectedIndexChanged(RuntimeHelpers.GetObjectValue(sender), e);
			GlobalForm.ReadWriteBearFile();
		}
	}

	private void Mainform_Activated(object sender, EventArgs e)
	{
		FileLocationLabel.Text = "File location: " + GlobalForm.OpenPath;
		SynchPortfolio();
	}

	private void AboutToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.AboutForm).ShowDialog();
	}

	private void AddButton_Click(object sender, EventArgs e)
	{
		//IL_0181: Unknown result type (might be due to invalid IL or missing references)
		//IL_006b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0161: Unknown result type (might be due to invalid IL or missing references)
		string text = Strings.Trim(PortfolioTextBox.Text);
		checked
		{
			if (text.Length > 0)
			{
				int num = PortfolioDataGridView.RowCount - 1;
				for (int i = 0; i <= num; i++)
				{
					if (Operators.CompareString(Conversions.ToString(PortfolioDataGridView.Rows[i].Cells[0].Value), text, false) == 0)
					{
						MessageBox.Show("The portfolio is already in the list.", "MainForm: AddButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)64);
						return;
					}
				}
				LockFlag = true;
				PortfolioDataGridView.Rows.Add();
				PortfolioDataGridView.Rows[PortfolioDataGridView.RowCount - 1].Cells[0].Value = text;
				PortfolioDataGridView.Rows[PortfolioDataGridView.RowCount - 1].Cells[1].Value = GlobalForm.OpenPath;
				PortWatchButtons(Conversions.ToBoolean(Interaction.IIf(PortfolioDataGridView.RowCount == 0, (object)false, (object)true)));
				lsWatchList = true;
				PortfolioDataGridView.Rows[PortfolioDataGridView.RowCount - 1].Selected = true;
				LockFlag = false;
				if (!GlobalForm.Quiet)
				{
					MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				}
			}
			else
			{
				((Control)PortfolioTextBox).Focus();
				MessageBox.Show("Please add a unique portfolio name to the text box.", "MainForm: AddButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
		}
	}

	public void AllButton_Click(object sender, EventArgs e)
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
			FileLocationLabel.Text = ListBox1.Items.Count + " Selected";
		}
	}

	private void AnalyzeMenuItem_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.AnalyzeForm).ShowDialog();
		CheckIntraday();
		if (GlobalForm.PathChanged)
		{
			MFDisplayFiles(BrowseFlag: false);
		}
	}

	private void BrowseButton_Click(object sender, EventArgs e)
	{
		//IL_0010: Unknown result type (might be due to invalid IL or missing references)
		//IL_0015: Unknown result type (might be due to invalid IL or missing references)
		//IL_0025: Expected O, but got Unknown
		//IL_002b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0031: Invalid comparison between Unknown and I4
		if (!LockFlag)
		{
			LockFlag = true;
			FolderBrowserDialog1 = new FolderBrowserDialog
			{
				Description = "Select the path to the portfolio (folder) you'd like to open."
			};
			if ((int)((CommonDialog)FolderBrowserDialog1).ShowDialog() == 1)
			{
				GlobalForm.PathChanged = true;
				GlobalForm.OpenPath = FolderBrowserDialog1.SelectedPath;
				MFDisplayFiles(BrowseFlag: false);
			}
			LockFlag = false;
		}
	}

	private void CandlesToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.CandlesForm).ShowDialog();
	}

	private void ChangeButton_Click(object sender, EventArgs e)
	{
		//IL_012e: Unknown result type (might be due to invalid IL or missing references)
		//IL_011a: Unknown result type (might be due to invalid IL or missing references)
		//IL_00bf: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			if (((BaseCollection)PortfolioDataGridView.SelectedRows).Count > 0)
			{
				if (((TextBoxBase)PortfolioTextBox).TextLength > 0)
				{
					int num = PortfolioDataGridView.RowCount - 1;
					for (int i = 0; i <= num; i++)
					{
						if ((Operators.CompareString(PortfolioDataGridView.Rows[i].Cells[0].Value.ToString(), Strings.Trim(PortfolioTextBox.Text), false) == 0) & (Operators.CompareString(GlobalForm.OpenPath, PortfolioDataGridView.Rows[i].Cells[1].Value.ToString(), false) == 0))
						{
							MessageBox.Show("The portfolio is already in the list.", "MainForm: AddButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)64);
							return;
						}
					}
					LockFlag = true;
					GlobalForm.Quiet = true;
					DeleteButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
					GlobalForm.Quiet = false;
					LockFlag = false;
					AddButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
					lsWatchList = true;
				}
				else
				{
					MessageBox.Show("Please add a new portfolio name in the text box.", "MainForm: ChangeButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)64);
				}
			}
			else
			{
				MessageBox.Show("Please select a portfolio name from the list to change.", "MainForm: ChangeButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
		}
	}

	private void ChartButton_Click(object sender, EventArgs e)
	{
		//IL_000c: Unknown result type (might be due to invalid IL or missing references)
		ChartForm chartForm = new ChartForm();
		((Form)chartForm).StartPosition = (FormStartPosition)0;
		((Form)chartForm).ShowDialog();
		CheckIntraday();
	}

	public void CheckIntraday()
	{
		if (GlobalForm.IntradayData)
		{
			SeasonalityMI.Enabled = false;
			PredictionMI.Enabled = false;
		}
		else
		{
			SeasonalityMI.Enabled = true;
			PredictionMI.Enabled = true;
		}
	}

	private void CheckBox1_CheckedChanged(object sender, EventArgs e)
	{
		((Control)PortfolioPanel).Visible = !((Control)PortfolioPanel).Visible;
		((Control)LabelPanel).Visible = !((Control)PortfolioPanel).Visible;
	}

	private void DataGridView1_SelectionChanged(object sender, EventArgs e)
	{
		if (!LockFlag && ((PortfolioDataGridView.RowCount > 0) & (PortfolioDataGridView.GetCellCount((DataGridViewElementStates)32) > 0)))
		{
			if (Operators.CompareString(GlobalForm.OpenPath, PortfolioDataGridView.Rows[PortfolioDataGridView.SelectedCells[0].RowIndex].Cells[1].Value.ToString(), false) != 0)
			{
				GlobalForm.OpenPath = PortfolioDataGridView.Rows[PortfolioDataGridView.SelectedCells[0].RowIndex].Cells[1].Value.ToString();
				MFDisplayFiles(BrowseFlag: false);
				GlobalForm.PathChanged = true;
				ListBox1_SelectedIndexChanged(RuntimeHelpers.GetObjectValue(sender), e);
			}
			PortfolioTextBox.Text = PortfolioDataGridView.Rows[PortfolioDataGridView.SelectedCells[0].RowIndex].Cells[0].Value.ToString();
		}
	}

	private void DeleteButton_Click(object sender, EventArgs e)
	{
		//IL_011b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0107: Unknown result type (might be due to invalid IL or missing references)
		//IL_0078: Unknown result type (might be due to invalid IL or missing references)
		//IL_006f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0074: Unknown result type (might be due to invalid IL or missing references)
		//IL_0079: Unknown result type (might be due to invalid IL or missing references)
		//IL_007b: Invalid comparison between Unknown and I4
		//IL_00e6: Unknown result type (might be due to invalid IL or missing references)
		if (((BaseCollection)PortfolioDataGridView.SelectedRows).Count > 0)
		{
			DialogResult val = (GlobalForm.Quiet ? ((DialogResult)6) : MessageBox.Show("Are you sure you want to delete " + PortfolioDataGridView.Rows[PortfolioDataGridView.SelectedCells[0].RowIndex].Cells[0].Value.ToString() + "?\r\n\r\nPlease note: the delete button only removes the portfolio name, not the associated folder or files.", "MainForm: DeleteButton_Click", (MessageBoxButtons)4, (MessageBoxIcon)32));
			if ((int)val == 6)
			{
				PortfolioDataGridView.Rows.Remove(PortfolioDataGridView.SelectedRows[0]);
				PortWatchButtons(Conversions.ToBoolean(Interaction.IIf(PortfolioDataGridView.RowCount == 0, (object)false, (object)true)));
				lsWatchList = true;
				if (!GlobalForm.Quiet)
				{
					MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				}
			}
		}
		else if (PortfolioDataGridView.RowCount == 0)
		{
			MessageBox.Show("There are no portfolio names to delete.", "MainForm: DeleteButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
		else
		{
			MessageBox.Show("Please select a portfolio name from the list to delete.", "MainForm: DeleteButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)64);
			((Control)PortfolioDataGridView).Focus();
		}
	}

	private void EnableDisable()
	{
		if (ListBox1.SelectedItems.Count > 0)
		{
			((Control)IndicatorsButton).Enabled = true;
			((Control)SimulatorButton).Enabled = true;
			FixSplitMI.Enabled = true;
			CheckIntraday();
			Fib.Enabled = true;
		}
		else
		{
			((Control)IndicatorsButton).Enabled = false;
			PredictionMI.Enabled = false;
			((Control)SimulatorButton).Enabled = false;
			FixSplitMI.Enabled = false;
			SeasonalityMI.Enabled = false;
			Fib.Enabled = false;
		}
	}

	private void ExitMenuItem_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void FileFormatToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.FileFormatForm).ShowDialog();
		if (GlobalForm.PathChanged)
		{
			MFDisplayFiles(BrowseFlag: false);
		}
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.MainFormHelp).ShowDialog();
	}

	private void HelpButton1_Click_1(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.HelpMainFormPortfolio).ShowDialog();
	}

	private void IndicatorsButton_Click(object sender, EventArgs e)
	{
		//IL_006f: Unknown result type (might be due to invalid IL or missing references)
		//IL_001b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0021: Invalid comparison between Unknown and I4
		if (ListBox1.SelectedIndex == -1)
		{
			if ((int)MessageBox.Show("No stocks were selected. Did you want me to select all of them?", "MainForm: IndicatorsButton_Click", (MessageBoxButtons)4, (MessageBoxIcon)64) != 6)
			{
				return;
			}
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
		((Form)MyProject.Forms.CPIForm).ShowDialog();
		CheckIntraday();
	}

	private void LicenseToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.LicenseForm).ShowDialog();
		if (!GlobalForm.SignedLicense)
		{
			((Form)this).Close();
		}
	}

	private void ListBox1_DoubleClick(object sender, EventArgs e)
	{
		ChartButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
	}

	private void ListBox1_KeyPress(object sender, KeyPressEventArgs e)
	{
		SearchString += Conversions.ToString(e.KeyChar);
	}

	private void ListBox1_KeyUp(object sender, KeyEventArgs e)
	{
		if (Operators.CompareString(SearchString, string.Empty, false) != 0)
		{
			int num = ListBox1.FindString(SearchString);
			if (num != -1)
			{
				ListBox1.SelectedIndex = -1;
				ListBox1.SetSelected(num, true);
			}
			else
			{
				SearchString = "";
			}
		}
		else
		{
			e.Handled = GlobalForm.ListBoxHandler(e, ListBox1, ColonChange: false);
		}
	}

	private void ListBox1_MouseClick(object sender, MouseEventArgs e)
	{
		SearchString = "";
	}

	private void ListBox1_SelectedIndexChanged(object sender, EventArgs e)
	{
		EnableDisable();
		FileLocationLabel.Text = ListBox1.SelectedItems.Count + " Selected";
	}

	private void ListButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.ListForm).ShowDialog();
		CheckIntraday();
	}

	private void MainFormHelpToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.MainFormHelp).ShowDialog();
	}

	private void Mainform_KeyDown(object sender, KeyEventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_0008: Invalid comparison between Unknown and I4
		if ((int)e.KeyCode == 112)
		{
			HelpButton1_Click(RuntimeHelpers.GetObjectValue(sender), (EventArgs)(object)e);
		}
	}

	private void Mainform_SizeChanged(object sender, EventArgs e)
	{
		MainFormSizeChanged = true;
	}

	public void MFDisplayFiles(bool BrowseFlag)
	{
		//IL_00e8: Unknown result type (might be due to invalid IL or missing references)
		if ((Operators.CompareString(GlobalForm.OpenPath, "", false) != 0) & Directory.Exists(GlobalForm.OpenPath))
		{
			ListBox1.Items.Clear();
			string[] files = Directory.GetFiles(GlobalForm.OpenPath, "*.txt");
			foreach (string path in files)
			{
				ListBox1.Items.Add((object)Path.GetFileName(path));
			}
			string[] files2 = Directory.GetFiles(GlobalForm.OpenPath, "*.csv");
			foreach (string path2 in files2)
			{
				ListBox1.Items.Add((object)Path.GetFileName(path2));
			}
		}
		else if ((Operators.CompareString(GlobalForm.OpenPath, "", false) != 0) & !Directory.Exists(GlobalForm.OpenPath))
		{
			MessageBox.Show("The path, " + GlobalForm.OpenPath + " does not exist. Click the 'Browse Portfolio Location' button and pick a new folder.");
			((Control)BrowseButton).Focus();
		}
		else if (BrowseFlag)
		{
			BrowseButton.PerformClick();
			if (Operators.CompareString(GlobalForm.OpenPath, "", false) != 0)
			{
				MFDisplayFiles(BrowseFlag);
			}
		}
		EnableDisable();
		bool enabled = Conversions.ToBoolean(Interaction.IIf(ListBox1.Items.Count == 0, (object)false, (object)true));
		((Control)AllButton).Enabled = enabled;
		((Control)ChartButton).Enabled = enabled;
		((Control)ListButton).Enabled = enabled;
		FileLocationLabel.Text = "File location: " + GlobalForm.OpenPath;
	}

	private void PatternsMenuItem_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.PatternsForm).ShowDialog();
	}

	private void PortfolioDataGridView_GotFocus(object sender, EventArgs e)
	{
		if (PortfolioDataGridView.RowCount > 0 && ((TextBoxBase)PortfolioTextBox).TextLength == 0 && PortfolioDataGridView.GetCellCount((DataGridViewElementStates)32) > 0)
		{
			PortfolioTextBox.Text = PortfolioDataGridView.Rows[PortfolioDataGridView.SelectedCells[0].RowIndex].Cells[0].Value.ToString();
		}
	}

	private void PortfolioTextBox_TextChanged(object sender, EventArgs e)
	{
		if (PortfolioTextBox.Text.Length == 0)
		{
			((Control)ChangeButton).Enabled = false;
			((Control)AddButton).Enabled = false;
			return;
		}
		if (!((Control)ChangeButton).Enabled & (PortfolioDataGridView.RowCount > 0))
		{
			((Control)ChangeButton).Enabled = true;
		}
		if (!((Control)AddButton).Enabled)
		{
			((Control)AddButton).Enabled = true;
		}
	}

	public void PortWatchButtons(bool Flag)
	{
		((Control)DeleteButton).Enabled = Flag;
		((Control)ChangeButton).Enabled = Flag;
	}

	private void RelStrengthToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.RelStrengthForm).ShowDialog();
		CheckIntraday();
		if (GlobalForm.PathChanged)
		{
			MFDisplayFiles(BrowseFlag: false);
		}
	}

	private void RemovePatternzMenuItem_Click(object sender, EventArgs e)
	{
		//IL_0005: Unknown result type (might be due to invalid IL or missing references)
		((Form)new RemovePatternz()).ShowDialog();
	}

	private void ScoreButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.ScoreForm).ShowDialog();
	}

	private void SynchPortfolio()
	{
		if (LockFlag || PortfolioDataGridView.RowCount <= 0)
		{
			return;
		}
		checked
		{
			try
			{
				int num = PortfolioDataGridView.RowCount - 1;
				for (int i = 0; i <= num; i++)
				{
					if (Operators.CompareString(PortfolioDataGridView.Rows[i].Cells[1].Value.ToString(), GlobalForm.OpenPath, false) == 0)
					{
						LockFlag = true;
						PortfolioDataGridView.Rows[i].Cells[0].Selected = true;
						PortfolioTextBox.Text = PortfolioDataGridView.Rows[PortfolioDataGridView.SelectedCells[0].RowIndex].Cells[0].Value.ToString();
						LockFlag = false;
						return;
					}
				}
				if (PortfolioDataGridView.GetCellCount((DataGridViewElementStates)32) > 0)
				{
					PortfolioDataGridView.Rows[PortfolioDataGridView.SelectedCells[0].RowIndex].Cells[0].Selected = false;
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				if (PortfolioDataGridView.GetCellCount((DataGridViewElementStates)32) > 0)
				{
					PortfolioDataGridView.Rows[PortfolioDataGridView.SelectedCells[0].RowIndex].Cells[0].Selected = false;
				}
				ProjectData.ClearProjectError();
			}
		}
	}

	private void ManualScoreToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.ManualScoreForm).ShowDialog();
		CheckIntraday();
	}

	private void NewsMenuItem_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.NewsForm).ShowDialog();
	}

	private void PredictionToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_0011: Unknown result type (might be due to invalid IL or missing references)
		//IL_0049: Unknown result type (might be due to invalid IL or missing references)
		if (!GlobalForm.IntradayData)
		{
			((Form)MyProject.Forms.ForecastForm).ShowDialog();
		}
		CheckIntraday();
		if (GlobalForm.IntradayData)
		{
			SeasonalityMI.Enabled = false;
			PredictionMI.Enabled = false;
			MessageBox.Show("The Forecast Form does not work well with intraday data (price doesn't vary enough intraday).", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
	}

	private void SimulatorButton_Click(object sender, EventArgs e)
	{
		//IL_006f: Unknown result type (might be due to invalid IL or missing references)
		//IL_001b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0021: Invalid comparison between Unknown and I4
		if (ListBox1.SelectedIndex == -1)
		{
			if ((int)MessageBox.Show("No stocks were selected. Did you want me to select all of them?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)64) != 6)
			{
				return;
			}
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
		((Form)MyProject.Forms.SimulatorForm).ShowDialog();
	}

	private void SplitsDivsToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.SplitsDivsForm).ShowDialog();
		CheckIntraday();
		if (GlobalForm.PathChanged)
		{
			MFDisplayFiles(BrowseFlag: false);
		}
	}

	private void ToolStripMenuItem1_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.FixSplitForm).ShowDialog();
		CheckIntraday();
	}

	private void ToolStripMenuItem1_Click_1(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.FibFinderForm).ShowDialog();
		CheckIntraday();
	}

	private void UpdateButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.UpdateForm).ShowDialog();
		MFDisplayFiles(BrowseFlag: false);
	}

	private void RestoreLayoutToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0013: Invalid comparison between Unknown and I4
		if ((int)MessageBox.Show("Did you want to restore the size and location of all forms to their factory settings?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32) == 6)
		{
			Point point = new Point(-1, -1);
			Size size = new Size(-1, -1);
			MySettingsProperty.Settings.MainFormLocation = point;
			MySettingsProperty.Settings.MainFormSize = size;
			MySettingsProperty.Settings.ListFormLocation = point;
			MySettingsProperty.Settings.ListFormSize = size;
			MySettingsProperty.Settings.CandlesFormLocation = point;
			MySettingsProperty.Settings.CandlesFormSize = size;
			MySettingsProperty.Settings.ChartFormLocation = point;
			MySettingsProperty.Settings.ChartFormSize = size;
			MySettingsProperty.Settings.CPIFormLocation = point;
			MySettingsProperty.Settings.CPIFormSize = size;
			MySettingsProperty.Settings.FibFinderLocation = point;
			MySettingsProperty.Settings.FibFinderSize = size;
			MySettingsProperty.Settings.FixedSplitLocation = point;
			MySettingsProperty.Settings.FixedSplitSize = size;
			MySettingsProperty.Settings.ForecastLocation = point;
			MySettingsProperty.Settings.ForecastSize = size;
			MySettingsProperty.Settings.ListChartLocation = point;
			MySettingsProperty.Settings.ListChartSize = size;
			MySettingsProperty.Settings.ManualScoreLocation = point;
			MySettingsProperty.Settings.ManualScoreSize = size;
			MySettingsProperty.Settings.BestTradingTimeLocation = point;
			MySettingsProperty.Settings.BestTradingTimeSize = size;
			MySettingsProperty.Settings.NewsFormLocation = point;
			MySettingsProperty.Settings.NewsFormSize = size;
			MySettingsProperty.Settings.PatternsLocation = point;
			MySettingsProperty.Settings.PatternsSize = size;
			MySettingsProperty.Settings.RelStrengthLocation = point;
			MySettingsProperty.Settings.RelStrengthSize = size;
			MySettingsProperty.Settings.ScoreLocation = point;
			MySettingsProperty.Settings.ScoreSize = size;
			MySettingsProperty.Settings.SeasonLocation = point;
			MySettingsProperty.Settings.SeasonSize = size;
			MySettingsProperty.Settings.SimLocation = point;
			MySettingsProperty.Settings.SimSize = size;
			MySettingsProperty.Settings.SplitsLocation = point;
			MySettingsProperty.Settings.SplitsSize = size;
			MySettingsProperty.Settings.UpdateLocation = point;
			MySettingsProperty.Settings.UpdateSize = size;
			((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
		}
	}

	private void SeasonalityToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_0011: Unknown result type (might be due to invalid IL or missing references)
		if (!GlobalForm.IntradayData)
		{
			((Form)MyProject.Forms.Seasonality).ShowDialog();
		}
		CheckIntraday();
	}

	private void MyBuyingsellingToolStripMenuItem_Click(object sender, EventArgs e)
	{
		//IL_0011: Unknown result type (might be due to invalid IL or missing references)
		if (!GlobalForm.IntradayData)
		{
			((Form)MyProject.Forms.BestTradingTime).ShowDialog();
		}
		CheckIntraday();
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
		//IL_0011: Unknown result type (might be due to invalid IL or missing references)
		//IL_001b: Expected O, but got Unknown
		//IL_001c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0026: Expected O, but got Unknown
		//IL_0027: Unknown result type (might be due to invalid IL or missing references)
		//IL_0031: Expected O, but got Unknown
		//IL_0032: Unknown result type (might be due to invalid IL or missing references)
		//IL_003c: Expected O, but got Unknown
		//IL_003d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0047: Expected O, but got Unknown
		//IL_0048: Unknown result type (might be due to invalid IL or missing references)
		//IL_0052: Expected O, but got Unknown
		//IL_0053: Unknown result type (might be due to invalid IL or missing references)
		//IL_005d: Expected O, but got Unknown
		//IL_005e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0068: Expected O, but got Unknown
		//IL_0069: Unknown result type (might be due to invalid IL or missing references)
		//IL_0073: Expected O, but got Unknown
		//IL_0074: Unknown result type (might be due to invalid IL or missing references)
		//IL_007e: Expected O, but got Unknown
		//IL_007f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0089: Expected O, but got Unknown
		//IL_008a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0094: Expected O, but got Unknown
		//IL_0095: Unknown result type (might be due to invalid IL or missing references)
		//IL_009f: Expected O, but got Unknown
		//IL_00a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00aa: Expected O, but got Unknown
		//IL_00ab: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b5: Expected O, but got Unknown
		//IL_00b6: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c0: Expected O, but got Unknown
		//IL_00c1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00cb: Expected O, but got Unknown
		//IL_00cc: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d6: Expected O, but got Unknown
		//IL_00d7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e1: Expected O, but got Unknown
		//IL_00e2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ec: Expected O, but got Unknown
		//IL_00ed: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f7: Expected O, but got Unknown
		//IL_00f8: Unknown result type (might be due to invalid IL or missing references)
		//IL_0102: Expected O, but got Unknown
		//IL_0103: Unknown result type (might be due to invalid IL or missing references)
		//IL_010d: Expected O, but got Unknown
		//IL_010e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0118: Expected O, but got Unknown
		//IL_0119: Unknown result type (might be due to invalid IL or missing references)
		//IL_0123: Expected O, but got Unknown
		//IL_012f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0139: Expected O, but got Unknown
		//IL_013a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0144: Expected O, but got Unknown
		//IL_0145: Unknown result type (might be due to invalid IL or missing references)
		//IL_014f: Expected O, but got Unknown
		//IL_0150: Unknown result type (might be due to invalid IL or missing references)
		//IL_015a: Expected O, but got Unknown
		//IL_015b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0165: Expected O, but got Unknown
		//IL_0166: Unknown result type (might be due to invalid IL or missing references)
		//IL_0170: Expected O, but got Unknown
		//IL_0171: Unknown result type (might be due to invalid IL or missing references)
		//IL_017b: Expected O, but got Unknown
		//IL_017c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0186: Expected O, but got Unknown
		//IL_0187: Unknown result type (might be due to invalid IL or missing references)
		//IL_0191: Expected O, but got Unknown
		//IL_0192: Unknown result type (might be due to invalid IL or missing references)
		//IL_019c: Expected O, but got Unknown
		//IL_019d: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a7: Expected O, but got Unknown
		//IL_01a8: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b2: Expected O, but got Unknown
		//IL_01b3: Unknown result type (might be due to invalid IL or missing references)
		//IL_01bd: Expected O, but got Unknown
		//IL_01be: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c8: Expected O, but got Unknown
		//IL_01c9: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d3: Expected O, but got Unknown
		//IL_01d4: Unknown result type (might be due to invalid IL or missing references)
		//IL_01de: Expected O, but got Unknown
		//IL_01df: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e9: Expected O, but got Unknown
		//IL_01ea: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f4: Expected O, but got Unknown
		//IL_01f5: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ff: Expected O, but got Unknown
		//IL_0200: Unknown result type (might be due to invalid IL or missing references)
		//IL_020a: Expected O, but got Unknown
		//IL_020b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0215: Expected O, but got Unknown
		//IL_0216: Unknown result type (might be due to invalid IL or missing references)
		//IL_0220: Expected O, but got Unknown
		//IL_160b: Unknown result type (might be due to invalid IL or missing references)
		//IL_1615: Expected O, but got Unknown
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(Mainform));
		MenuStrip1 = new MenuStrip();
		ExitMenuItem = new ToolStripMenuItem();
		CandlesToolStripMenuItem = new ToolStripMenuItem();
		Fib = new ToolStripMenuItem();
		FileFormatMenuItem = new ToolStripMenuItem();
		PredictionMI = new ToolStripMenuItem();
		ManualScoreToolStripMenuItem = new ToolStripMenuItem();
		NewsMenuItem = new ToolStripMenuItem();
		PatternsMenuItem = new ToolStripMenuItem();
		RelStrengthToolStripMenuItem = new ToolStripMenuItem();
		SeasonalityMI = new ToolStripMenuItem();
		SeasonalityToolStripMenuItem = new ToolStripMenuItem();
		MyBuyingsellingToolStripMenuItem = new ToolStripMenuItem();
		SplitsDivsToolStripMenuItem = new ToolStripMenuItem();
		FixSplitMI = new ToolStripMenuItem();
		HelpMenuItem = new ToolStripMenuItem();
		AboutToolStripMenuItem = new ToolStripMenuItem();
		LicenseToolStripMenuItem = new ToolStripMenuItem();
		MainFormHelpToolStripMenuItem = new ToolStripMenuItem();
		RemovePatternzMenuItem = new ToolStripMenuItem();
		RestoreLayoutToolStripMenuItem = new ToolStripMenuItem();
		ListBox1 = new ListBox();
		AllButton = new Button();
		ChartButton = new Button();
		ListButton = new Button();
		FileSystemWatcher1 = new FileSystemWatcher();
		BrowseButton = new Button();
		FolderBrowserDialog1 = new FolderBrowserDialog();
		UpdateButton = new Button();
		FileLocationLabel = new Label();
		IndicatorsButton = new Button();
		PortfolioPanel = new Panel();
		PortfolioDataGridView = new DataGridView();
		PortfolioColumn = new DataGridViewTextBoxColumn();
		PathColumn = new DataGridViewTextBoxColumn();
		HelpButton1 = new Button();
		PortfolioTextBox = new TextBox();
		Label1 = new Label();
		DeleteButton = new Button();
		ChangeButton = new Button();
		AddButton = new Button();
		ShowPortfolioCheckBox = new CheckBox();
		Label3 = new Label();
		LabelPanel = new Panel();
		Label4 = new Label();
		Label2 = new Label();
		ScoreButton = new Button();
		SimulatorButton = new Button();
		((Control)MenuStrip1).SuspendLayout();
		((ISupportInitialize)FileSystemWatcher1).BeginInit();
		((Control)PortfolioPanel).SuspendLayout();
		((ISupportInitialize)PortfolioDataGridView).BeginInit();
		((Control)LabelPanel).SuspendLayout();
		((Control)this).SuspendLayout();
		((ToolStrip)MenuStrip1).Items.AddRange((ToolStripItem[])(object)new ToolStripItem[13]
		{
			(ToolStripItem)ExitMenuItem,
			(ToolStripItem)CandlesToolStripMenuItem,
			(ToolStripItem)Fib,
			(ToolStripItem)FileFormatMenuItem,
			(ToolStripItem)PredictionMI,
			(ToolStripItem)ManualScoreToolStripMenuItem,
			(ToolStripItem)NewsMenuItem,
			(ToolStripItem)PatternsMenuItem,
			(ToolStripItem)RelStrengthToolStripMenuItem,
			(ToolStripItem)SeasonalityMI,
			(ToolStripItem)SplitsDivsToolStripMenuItem,
			(ToolStripItem)FixSplitMI,
			(ToolStripItem)HelpMenuItem
		});
		((Control)MenuStrip1).Location = new Point(0, 0);
		((Control)MenuStrip1).Name = "MenuStrip1";
		((Control)MenuStrip1).Size = new Size(847, 24);
		((Control)MenuStrip1).TabIndex = 3;
		((Control)MenuStrip1).Text = "MenuStrip1";
		((ToolStripItem)ExitMenuItem).Name = "ExitMenuItem";
		((ToolStripItem)ExitMenuItem).Size = new Size(38, 20);
		((ToolStripItem)ExitMenuItem).Tag = "0";
		((ToolStripItem)ExitMenuItem).Text = "&Exit";
		((ToolStripItem)ExitMenuItem).ToolTipText = "End the program";
		((ToolStripItem)CandlesToolStripMenuItem).Name = "CandlesToolStripMenuItem";
		((ToolStripItem)CandlesToolStripMenuItem).Size = new Size(61, 20);
		((ToolStripItem)CandlesToolStripMenuItem).Text = "&Candles";
		((ToolStripItem)CandlesToolStripMenuItem).ToolTipText = "Select candlestick patterns to search for";
		Fib.Enabled = false;
		((ToolStripItem)Fib).Name = "Fib";
		((ToolStripItem)Fib).Size = new Size(35, 20);
		((ToolStripItem)Fib).Text = "Fib";
		((ToolStripItem)FileFormatMenuItem).Name = "FileFormatMenuItem";
		((ToolStripItem)FileFormatMenuItem).Size = new Size(78, 20);
		((ToolStripItem)FileFormatMenuItem).Tag = "10";
		((ToolStripItem)FileFormatMenuItem).Text = "&File Format";
		((ToolStripItem)FileFormatMenuItem).ToolTipText = "Configures the program to accept data from files";
		((ToolStripItem)PredictionMI).Name = "PredictionMI";
		((ToolStripItem)PredictionMI).Size = new Size(63, 20);
		((ToolStripItem)PredictionMI).Text = "F&orecast";
		((ToolStripItem)ManualScoreToolStripMenuItem).Name = "ManualScoreToolStripMenuItem";
		((ToolStripItem)ManualScoreToolStripMenuItem).Size = new Size(91, 20);
		((ToolStripItem)ManualScoreToolStripMenuItem).Text = "&Manual Score";
		((ToolStripItem)NewsMenuItem).AutoToolTip = true;
		((ToolStripItem)NewsMenuItem).Name = "NewsMenuItem";
		((ToolStripItem)NewsMenuItem).Size = new Size(48, 20);
		((ToolStripItem)NewsMenuItem).Text = "&News";
		((ToolStripItem)NewsMenuItem).ToolTipText = "Get news from Tiingo";
		((ToolStripItem)PatternsMenuItem).Name = "PatternsMenuItem";
		((ToolStripItem)PatternsMenuItem).Size = new Size(62, 20);
		((ToolStripItem)PatternsMenuItem).Tag = "20";
		((ToolStripItem)PatternsMenuItem).Text = "&Patterns";
		((ToolStripItem)PatternsMenuItem).ToolTipText = "Select which chart patterns you wish to look for";
		((ToolStripItem)RelStrengthToolStripMenuItem).Name = "RelStrengthToolStripMenuItem";
		((ToolStripItem)RelStrengthToolStripMenuItem).Size = new Size(83, 20);
		((ToolStripItem)RelStrengthToolStripMenuItem).Text = "&Rel Strength";
		((ToolStripDropDownItem)SeasonalityMI).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[2]
		{
			(ToolStripItem)SeasonalityToolStripMenuItem,
			(ToolStripItem)MyBuyingsellingToolStripMenuItem
		});
		((ToolStripItem)SeasonalityMI).Name = "SeasonalityMI";
		((ToolStripItem)SeasonalityMI).Size = new Size(78, 20);
		((ToolStripItem)SeasonalityMI).Text = "Seaso&nality";
		((ToolStripItem)SeasonalityToolStripMenuItem).Name = "SeasonalityToolStripMenuItem";
		((ToolStripItem)SeasonalityToolStripMenuItem).Size = new Size(167, 22);
		((ToolStripItem)SeasonalityToolStripMenuItem).Text = "&Seasonality";
		((ToolStripItem)MyBuyingsellingToolStripMenuItem).Name = "MyBuyingsellingToolStripMenuItem";
		((ToolStripItem)MyBuyingsellingToolStripMenuItem).Size = new Size(167, 22);
		((ToolStripItem)MyBuyingsellingToolStripMenuItem).Text = "&Best Trading Time";
		((ToolStripItem)SplitsDivsToolStripMenuItem).Name = "SplitsDivsToolStripMenuItem";
		((ToolStripItem)SplitsDivsToolStripMenuItem).Size = new Size(74, 20);
		((ToolStripItem)SplitsDivsToolStripMenuItem).Text = "S&plits/Divs";
		FixSplitMI.Enabled = false;
		((ToolStripItem)FixSplitMI).Name = "FixSplitMI";
		((ToolStripItem)FixSplitMI).Size = new Size(60, 20);
		((ToolStripItem)FixSplitMI).Text = "Fix Split";
		((ToolStripDropDownItem)HelpMenuItem).DropDownItems.AddRange((ToolStripItem[])(object)new ToolStripItem[5]
		{
			(ToolStripItem)AboutToolStripMenuItem,
			(ToolStripItem)LicenseToolStripMenuItem,
			(ToolStripItem)MainFormHelpToolStripMenuItem,
			(ToolStripItem)RemovePatternzMenuItem,
			(ToolStripItem)RestoreLayoutToolStripMenuItem
		});
		((ToolStripItem)HelpMenuItem).Name = "HelpMenuItem";
		((ToolStripItem)HelpMenuItem).Size = new Size(44, 20);
		((ToolStripItem)HelpMenuItem).Tag = "30";
		((ToolStripItem)HelpMenuItem).Text = "&Help";
		((ToolStripItem)HelpMenuItem).ToolTipText = "Ask for help with the program";
		((ToolStripItem)AboutToolStripMenuItem).Name = "AboutToolStripMenuItem";
		((ToolStripItem)AboutToolStripMenuItem).Size = new Size(163, 22);
		((ToolStripItem)AboutToolStripMenuItem).Text = "&About";
		((ToolStripItem)LicenseToolStripMenuItem).Name = "LicenseToolStripMenuItem";
		((ToolStripItem)LicenseToolStripMenuItem).Size = new Size(163, 22);
		((ToolStripItem)LicenseToolStripMenuItem).Text = "&License";
		((ToolStripItem)MainFormHelpToolStripMenuItem).Name = "MainFormHelpToolStripMenuItem";
		((ToolStripItem)MainFormHelpToolStripMenuItem).Size = new Size(163, 22);
		((ToolStripItem)MainFormHelpToolStripMenuItem).Text = "&MainForm Help";
		((ToolStripItem)RemovePatternzMenuItem).Name = "RemovePatternzMenuItem";
		((ToolStripItem)RemovePatternzMenuItem).Size = new Size(163, 22);
		((ToolStripItem)RemovePatternzMenuItem).Text = "&Remove Patternz";
		((ToolStripItem)RemovePatternzMenuItem).ToolTipText = "How to remove Patternz from your computer";
		((ToolStripItem)RestoreLayoutToolStripMenuItem).Name = "RestoreLayoutToolStripMenuItem";
		((ToolStripItem)RestoreLayoutToolStripMenuItem).Size = new Size(163, 22);
		((ToolStripItem)RestoreLayoutToolStripMenuItem).Text = "R&estore layout";
		((Control)ListBox1).Anchor = (AnchorStyles)15;
		ListBox1.HorizontalScrollbar = true;
		((Control)ListBox1).Location = new Point(12, 62);
		ListBox1.MultiColumn = true;
		((Control)ListBox1).Name = "ListBox1";
		ListBox1.SelectionMode = (SelectionMode)3;
		((Control)ListBox1).Size = new Size(531, 290);
		ListBox1.Sorted = true;
		((Control)ListBox1).TabIndex = 5;
		((Control)AllButton).Anchor = (AnchorStyles)10;
		((Control)AllButton).Location = new Point(745, 297);
		((Control)AllButton).Name = "AllButton";
		((Control)AllButton).Size = new Size(59, 23);
		((Control)AllButton).TabIndex = 13;
		((ButtonBase)AllButton).Text = "&Select All";
		((ButtonBase)AllButton).UseVisualStyleBackColor = true;
		((Control)ChartButton).Anchor = (AnchorStyles)10;
		((Control)ChartButton).Location = new Point(597, 324);
		((Control)ChartButton).Name = "ChartButton";
		((Control)ChartButton).Size = new Size(59, 23);
		((Control)ChartButton).TabIndex = 0;
		((ButtonBase)ChartButton).Text = "Ch&art";
		((ButtonBase)ChartButton).UseVisualStyleBackColor = true;
		((Control)ListButton).Anchor = (AnchorStyles)10;
		((Control)ListButton).Location = new Point(671, 324);
		((Control)ListButton).Name = "ListButton";
		((Control)ListButton).Size = new Size(59, 23);
		((Control)ListButton).TabIndex = 1;
		((ButtonBase)ListButton).Text = "&List";
		((ButtonBase)ListButton).UseVisualStyleBackColor = true;
		FileSystemWatcher1.EnableRaisingEvents = true;
		FileSystemWatcher1.SynchronizingObject = (ISynchronizeInvoke?)this;
		((Control)BrowseButton).Anchor = (AnchorStyles)10;
		((Control)BrowseButton).Location = new Point(597, 270);
		((Control)BrowseButton).Name = "BrowseButton";
		((Control)BrowseButton).Size = new Size(143, 23);
		((Control)BrowseButton).TabIndex = 10;
		((ButtonBase)BrowseButton).Text = "&Browse Portfolio Location";
		((ButtonBase)BrowseButton).UseVisualStyleBackColor = true;
		((Control)UpdateButton).Anchor = (AnchorStyles)10;
		((Control)UpdateButton).Location = new Point(745, 324);
		((Control)UpdateButton).Name = "UpdateButton";
		((Control)UpdateButton).Size = new Size(59, 23);
		((Control)UpdateButton).TabIndex = 2;
		((ButtonBase)UpdateButton).Text = "&Update";
		((ButtonBase)UpdateButton).UseVisualStyleBackColor = true;
		((Control)FileLocationLabel).Anchor = (AnchorStyles)13;
		FileLocationLabel.BorderStyle = (BorderStyle)2;
		((Control)FileLocationLabel).CausesValidation = false;
		((Control)FileLocationLabel).Location = new Point(12, 24);
		((Control)FileLocationLabel).Name = "FileLocationLabel";
		((Control)FileLocationLabel).Size = new Size(823, 23);
		((Control)FileLocationLabel).TabIndex = 4;
		FileLocationLabel.TextAlign = (ContentAlignment)16;
		((Control)IndicatorsButton).Anchor = (AnchorStyles)10;
		((Control)IndicatorsButton).Location = new Point(597, 297);
		((Control)IndicatorsButton).Name = "IndicatorsButton";
		((Control)IndicatorsButton).Size = new Size(59, 23);
		((Control)IndicatorsButton).TabIndex = 11;
		((ButtonBase)IndicatorsButton).Text = "Indicato&r";
		((ButtonBase)IndicatorsButton).UseVisualStyleBackColor = true;
		((Control)PortfolioPanel).Anchor = (AnchorStyles)11;
		PortfolioPanel.BorderStyle = (BorderStyle)2;
		((Control)PortfolioPanel).Controls.Add((Control)(object)PortfolioDataGridView);
		((Control)PortfolioPanel).Controls.Add((Control)(object)HelpButton1);
		((Control)PortfolioPanel).Controls.Add((Control)(object)PortfolioTextBox);
		((Control)PortfolioPanel).Controls.Add((Control)(object)Label1);
		((Control)PortfolioPanel).Controls.Add((Control)(object)DeleteButton);
		((Control)PortfolioPanel).Controls.Add((Control)(object)ChangeButton);
		((Control)PortfolioPanel).Controls.Add((Control)(object)AddButton);
		((Control)PortfolioPanel).Location = new Point(556, 62);
		((Control)PortfolioPanel).Name = "PortfolioPanel";
		((Control)PortfolioPanel).Size = new Size(279, 175);
		((Control)PortfolioPanel).TabIndex = 7;
		((Control)PortfolioPanel).Visible = false;
		PortfolioDataGridView.AllowUserToAddRows = false;
		PortfolioDataGridView.AllowUserToDeleteRows = false;
		((Control)PortfolioDataGridView).Anchor = (AnchorStyles)15;
		((Control)PortfolioDataGridView).CausesValidation = false;
		PortfolioDataGridView.ColumnHeadersHeightSizeMode = (DataGridViewColumnHeadersHeightSizeMode)2;
		PortfolioDataGridView.Columns.AddRange((DataGridViewColumn[])(object)new DataGridViewColumn[2]
		{
			(DataGridViewColumn)PortfolioColumn,
			(DataGridViewColumn)PathColumn
		});
		PortfolioDataGridView.EditMode = (DataGridViewEditMode)4;
		((Control)PortfolioDataGridView).Location = new Point(10, 3);
		PortfolioDataGridView.MultiSelect = false;
		((Control)PortfolioDataGridView).Name = "PortfolioDataGridView";
		PortfolioDataGridView.ReadOnly = true;
		PortfolioDataGridView.RowHeadersWidth = 4;
		PortfolioDataGridView.RowHeadersWidthSizeMode = (DataGridViewRowHeadersWidthSizeMode)1;
		PortfolioDataGridView.SelectionMode = (DataGridViewSelectionMode)1;
		PortfolioDataGridView.ShowCellErrors = false;
		PortfolioDataGridView.ShowEditingIcon = false;
		PortfolioDataGridView.ShowRowErrors = false;
		((Control)PortfolioDataGridView).Size = new Size(255, 110);
		((Control)PortfolioDataGridView).TabIndex = 0;
		((DataGridViewColumn)PortfolioColumn).AutoSizeMode = (DataGridViewAutoSizeColumnMode)16;
		((DataGridViewColumn)PortfolioColumn).HeaderText = "                                  Portfolio";
		((DataGridViewColumn)PortfolioColumn).Name = "PortfolioColumn";
		((DataGridViewColumn)PortfolioColumn).ReadOnly = true;
		((DataGridViewColumn)PathColumn).HeaderText = "Path";
		((DataGridViewColumn)PathColumn).Name = "PathColumn";
		((DataGridViewColumn)PathColumn).ReadOnly = true;
		((DataGridViewColumn)PathColumn).Visible = false;
		((Control)HelpButton1).Anchor = (AnchorStyles)10;
		((Control)HelpButton1).Location = new Point(206, 148);
		((Control)HelpButton1).Name = "HelpButton1";
		((Control)HelpButton1).Size = new Size(59, 23);
		((Control)HelpButton1).TabIndex = 6;
		((ButtonBase)HelpButton1).Text = "&Help";
		((ButtonBase)HelpButton1).UseVisualStyleBackColor = true;
		((Control)PortfolioTextBox).Anchor = (AnchorStyles)10;
		((Control)PortfolioTextBox).Location = new Point(100, 122);
		((Control)PortfolioTextBox).Name = "PortfolioTextBox";
		((Control)PortfolioTextBox).Size = new Size(165, 20);
		((Control)PortfolioTextBox).TabIndex = 2;
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(15, 125);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(79, 13);
		((Control)Label1).TabIndex = 1;
		Label1.Text = "Portfolio Na&me:";
		((Control)DeleteButton).Anchor = (AnchorStyles)10;
		((Control)DeleteButton).Enabled = false;
		((Control)DeleteButton).Location = new Point(141, 148);
		((Control)DeleteButton).Name = "DeleteButton";
		((Control)DeleteButton).Size = new Size(59, 23);
		((Control)DeleteButton).TabIndex = 5;
		((ButtonBase)DeleteButton).Text = "Dele&te";
		((ButtonBase)DeleteButton).UseVisualStyleBackColor = true;
		((Control)ChangeButton).Anchor = (AnchorStyles)10;
		((Control)ChangeButton).Enabled = false;
		((Control)ChangeButton).Location = new Point(76, 148);
		((Control)ChangeButton).Name = "ChangeButton";
		((Control)ChangeButton).Size = new Size(59, 23);
		((Control)ChangeButton).TabIndex = 4;
		((ButtonBase)ChangeButton).Text = "Chan&ge";
		((ButtonBase)ChangeButton).UseVisualStyleBackColor = true;
		((Control)AddButton).Anchor = (AnchorStyles)10;
		((Control)AddButton).Enabled = false;
		((Control)AddButton).Location = new Point(10, 148);
		((Control)AddButton).Name = "AddButton";
		((Control)AddButton).Size = new Size(59, 23);
		((Control)AddButton).TabIndex = 3;
		((ButtonBase)AddButton).Text = "Ad&d";
		((ButtonBase)AddButton).UseVisualStyleBackColor = true;
		((Control)ShowPortfolioCheckBox).Anchor = (AnchorStyles)10;
		((ButtonBase)ShowPortfolioCheckBox).AutoSize = true;
		((Control)ShowPortfolioCheckBox).Location = new Point(661, 247);
		((Control)ShowPortfolioCheckBox).Name = "ShowPortfolioCheckBox";
		((Control)ShowPortfolioCheckBox).Size = new Size(69, 17);
		((Control)ShowPortfolioCheckBox).TabIndex = 8;
		((ButtonBase)ShowPortfolioCheckBox).Text = "Port&folios";
		((ButtonBase)ShowPortfolioCheckBox).UseVisualStyleBackColor = true;
		((Control)Label3).Location = new Point(12, 0);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(265, 31);
		((Control)Label3).TabIndex = 2;
		Label3.Text = "Use \"Browse Portfolio Location\" (below) to assign where you want to store your stock files.";
		((Control)LabelPanel).Anchor = (AnchorStyles)9;
		((Control)LabelPanel).Controls.Add((Control)(object)Label4);
		((Control)LabelPanel).Controls.Add((Control)(object)Label2);
		((Control)LabelPanel).Controls.Add((Control)(object)Label3);
		((Control)LabelPanel).Location = new Point(549, 62);
		((Control)LabelPanel).Name = "LabelPanel";
		((Control)LabelPanel).Size = new Size(286, 174);
		((Control)LabelPanel).TabIndex = 6;
		((Control)Label4).Location = new Point(12, 97);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(271, 80);
		((Control)Label4).TabIndex = 1;
		Label4.Text = componentResourceManager.GetString("Label4.Text");
		((Control)Label2).Location = new Point(12, 45);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(265, 52);
		((Control)Label2).TabIndex = 0;
		Label2.Text = "Click \"Update\" (below) to add symbols to the list box (left) and retrieve quote information. Quotes become available a few hours after the US market's close.";
		((Control)ScoreButton).Anchor = (AnchorStyles)10;
		((Control)ScoreButton).Location = new Point(746, 270);
		((Control)ScoreButton).Name = "ScoreButton";
		((Control)ScoreButton).Size = new Size(59, 23);
		((Control)ScoreButton).TabIndex = 9;
		((ButtonBase)ScoreButton).Text = "Sco&re";
		((ButtonBase)ScoreButton).UseVisualStyleBackColor = true;
		((Control)SimulatorButton).Anchor = (AnchorStyles)10;
		((Control)SimulatorButton).Location = new Point(671, 297);
		((Control)SimulatorButton).Name = "SimulatorButton";
		((Control)SimulatorButton).Size = new Size(59, 23);
		((Control)SimulatorButton).TabIndex = 12;
		((ButtonBase)SimulatorButton).Text = "Si&mulator";
		((ButtonBase)SimulatorButton).UseVisualStyleBackColor = true;
		((Form)this).AcceptButton = (IButtonControl)(object)ChartButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).ClientSize = new Size(847, 360);
		((Control)this).Controls.Add((Control)(object)SimulatorButton);
		((Control)this).Controls.Add((Control)(object)ScoreButton);
		((Control)this).Controls.Add((Control)(object)PortfolioPanel);
		((Control)this).Controls.Add((Control)(object)ShowPortfolioCheckBox);
		((Control)this).Controls.Add((Control)(object)IndicatorsButton);
		((Control)this).Controls.Add((Control)(object)FileLocationLabel);
		((Control)this).Controls.Add((Control)(object)UpdateButton);
		((Control)this).Controls.Add((Control)(object)BrowseButton);
		((Control)this).Controls.Add((Control)(object)ListButton);
		((Control)this).Controls.Add((Control)(object)ChartButton);
		((Control)this).Controls.Add((Control)(object)AllButton);
		((Control)this).Controls.Add((Control)(object)ListBox1);
		((Control)this).Controls.Add((Control)(object)MenuStrip1);
		((Control)this).Controls.Add((Control)(object)LabelPanel);
		((Control)this).DataBindings.Add(new Binding("Location", (object)MySettings.Default, "MainFormLocation", true, (DataSourceUpdateMode)1));
		((Form)this).KeyPreview = true;
		((Form)this).Location = MySettings.Default.MainFormLocation;
		((Form)this).MainMenuStrip = MenuStrip1;
		((Control)this).Name = "Mainform";
		((Form)this).ShowIcon = false;
		((Form)this).StartPosition = (FormStartPosition)1;
		((Form)this).Text = "Patternz Main Form";
		((Control)MenuStrip1).ResumeLayout(false);
		((Control)MenuStrip1).PerformLayout();
		((ISupportInitialize)FileSystemWatcher1).EndInit();
		((Control)PortfolioPanel).ResumeLayout(false);
		((Control)PortfolioPanel).PerformLayout();
		((ISupportInitialize)PortfolioDataGridView).EndInit();
		((Control)LabelPanel).ResumeLayout(false);
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}
}
