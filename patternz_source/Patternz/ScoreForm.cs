using System;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.IO;
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
public class ScoreForm : Form
{
	private struct ScoreInfo
	{
		public bool qTrendStart;

		public bool qFlatBase;

		public bool qHCR;

		public bool qYrlyRange;

		public bool qHeight;

		public bool qVolume;

		public bool qBkoutVol;

		public bool qThrowPull;

		public bool qBkoutGap;

		public bool qMarketCap;

		public string TrendStart;

		public int iTs;

		public int iFlatBaseStart;

		public int iFlatBaseEnd;

		public bool HCR;

		public int iHCRStart;

		public int iHCREnd;

		public string YrlyRange;

		public bool Tall;

		public int Volume;

		public string BkoutVol;

		public bool ThrowPull;

		public bool BkoutGap;

		public string MarketCap;

		public int sTrendStart;

		public int sFlatBase;

		public int sHCR;

		public int sYrlyRange;

		public int sHeight;

		public int sVolume;

		public int sBkoutVol;

		public int sThrowPull;

		public int sBkoutGap;

		public int sMarketCap;
	}

	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("HelpButton1")]
	private Button _HelpButton1;

	[CompilerGenerated]
	[AccessedThroughProperty("StrictCheckBox")]
	private CheckBox _StrictCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("PatternsButton")]
	private Button _PatternsButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ClipboardButton")]
	private Button _ClipboardButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StartButton")]
	private Button _StartButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StopButton")]
	private Button _StopButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("TestButton")]
	private Button _TestButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ScoreAllPortfoliosButton")]
	private Button _ScoreAllPortfoliosButton;

	[CompilerGenerated]
	[AccessedThroughProperty("APIKeyTextBox")]
	private TextBox _APIKeyTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("IEXRadioButton")]
	private RadioButton _IEXRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("FinnhubRB")]
	private RadioButton _FinnhubRB;

	[CompilerGenerated]
	[AccessedThroughProperty("LinkLabel1")]
	private LinkLabel _LinkLabel1;

	private bool StopPressed;

	private int iRow;

	private bool lsStrict;

	private const int deSTART = 0;

	private const int deCLIPBOARD = 1;

	private const int gSTOCKNAME = 0;

	private const int gLASTCLOSE = 1;

	private const int gSCORE = 2;

	private const int gGAIN = 3;

	private const int gPATTERN = 4;

	private const int gSTART = 5;

	private const int gEND = 6;

	private const int gTRENDSTART = 7;

	private const int gFLATBASE = 8;

	private const int gHCR = 9;

	private const int gYEARLYHL = 10;

	private const int gHEIGHT = 11;

	private const int gVOLTREND = 12;

	private const int gBKOUTVOLUME = 13;

	private const int gTHROWPULL = 14;

	private const int gBKOUTGAP = 15;

	private const int gMARKETCAP = 16;

	private const int gBKOUTDIR = 17;

	private const int gBKOUTDATE = 18;

	private const int gBKOUTPRICE = 19;

	private const int gULTHILOW = 20;

	private const int gULTHLDATE = 21;

	private ScoreInfo Scores;

	[field: AccessedThroughProperty("ToDatePicker")]
	internal virtual DateTimePicker ToDatePicker
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

	[field: AccessedThroughProperty("FilenameLabel")]
	internal virtual Label FilenameLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("ErrorLabel")]
	internal virtual Label ErrorLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("MonthlyRadioButton")]
	internal virtual RadioButton MonthlyRadioButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("WeeklyRadioButton")]
	internal virtual RadioButton WeeklyRadioButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("DailyRadioButton")]
	internal virtual RadioButton DailyRadioButton
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

	internal virtual CheckBox StrictCheckBox
	{
		[CompilerGenerated]
		get
		{
			return _StrictCheckBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = StrictCheckBox_CheckedChanged;
			CheckBox val = _StrictCheckBox;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_StrictCheckBox = value;
			val = _StrictCheckBox;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label1")]
	internal virtual Label Label1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("SymbolTextBox")]
	internal virtual TextBox SymbolTextBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button PatternsButton
	{
		[CompilerGenerated]
		get
		{
			return _PatternsButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PatternsButton_Click;
			Button val = _PatternsButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_PatternsButton = value;
			val = _PatternsButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button ClipboardButton
	{
		[CompilerGenerated]
		get
		{
			return _ClipboardButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ClipboardButton_Click;
			Button val = _ClipboardButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ClipboardButton = value;
			val = _ClipboardButton;
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

	[field: AccessedThroughProperty("DataGridView1")]
	internal virtual DataGridView DataGridView1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button TestButton
	{
		[CompilerGenerated]
		get
		{
			return _TestButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = TestButton_Click;
			Button val = _TestButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_TestButton = value;
			val = _TestButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button ScoreAllPortfoliosButton
	{
		[CompilerGenerated]
		get
		{
			return _ScoreAllPortfoliosButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ScoreAllPortfoliosButton_Click_1;
			Button val = _ScoreAllPortfoliosButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ScoreAllPortfoliosButton = value;
			val = _ScoreAllPortfoliosButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label4")]
	internal virtual Label Label4
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
			EventHandler eventHandler = APIKeyTextBox_TextChanged;
			TextBox val = _APIKeyTextBox;
			if (val != null)
			{
				((Control)val).TextChanged -= eventHandler;
			}
			_APIKeyTextBox = value;
			val = _APIKeyTextBox;
			if (val != null)
			{
				((Control)val).TextChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("GroupBox1")]
	internal virtual GroupBox GroupBox1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
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

	internal virtual LinkLabel LinkLabel1
	{
		[CompilerGenerated]
		get
		{
			return _LinkLabel1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0007: Unknown result type (might be due to invalid IL or missing references)
			//IL_000d: Expected O, but got Unknown
			LinkLabelLinkClickedEventHandler val = new LinkLabelLinkClickedEventHandler(LinkLabel1_LinkClicked);
			LinkLabel val2 = _LinkLabel1;
			if (val2 != null)
			{
				val2.LinkClicked -= val;
			}
			_LinkLabel1 = value;
			val2 = _LinkLabel1;
			if (val2 != null)
			{
				val2.LinkClicked += val;
			}
		}
	}

	public ScoreForm()
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		((Form)this).FormClosing += new FormClosingEventHandler(ScoreForm_FormClosing);
		((Form)this).Load += ScoreForm_Load;
		StopPressed = false;
		iRow = 0;
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
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_000b: Expected O, but got Unknown
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
		ToDatePicker = new DateTimePicker();
		FromDatePicker = new DateTimePicker();
		FilenameLabel = new Label();
		ErrorLabel = new Label();
		MonthlyRadioButton = new RadioButton();
		WeeklyRadioButton = new RadioButton();
		DailyRadioButton = new RadioButton();
		HelpButton1 = new Button();
		ProgressBar1 = new ProgressBar();
		StrictCheckBox = new CheckBox();
		Label1 = new Label();
		SymbolTextBox = new TextBox();
		PatternsButton = new Button();
		ClipboardButton = new Button();
		StartButton = new Button();
		StopButton = new Button();
		DoneButton = new Button();
		Label3 = new Label();
		Label2 = new Label();
		DataGridView1 = new DataGridView();
		TestButton = new Button();
		ScoreAllPortfoliosButton = new Button();
		Label4 = new Label();
		APIKeyTextBox = new TextBox();
		GroupBox1 = new GroupBox();
		IEXRadioButton = new RadioButton();
		FinnhubRB = new RadioButton();
		LinkLabel1 = new LinkLabel();
		((ISupportInitialize)DataGridView1).BeginInit();
		((Control)GroupBox1).SuspendLayout();
		((Control)this).SuspendLayout();
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(577, 491);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(100, 20);
		((Control)ToDatePicker).TabIndex = 18;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(577, 465);
		((Control)FromDatePicker).Name = "FromDatePicker";
		FromDatePicker.ShowUpDown = true;
		((Control)FromDatePicker).Size = new Size(100, 20);
		((Control)FromDatePicker).TabIndex = 16;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FilenameLabel).Anchor = (AnchorStyles)14;
		FilenameLabel.BorderStyle = (BorderStyle)2;
		((Control)FilenameLabel).Location = new Point(12, 460);
		((Control)FilenameLabel).Name = "FilenameLabel";
		((Control)FilenameLabel).Size = new Size(265, 22);
		((Control)FilenameLabel).TabIndex = 6;
		((Control)ErrorLabel).Anchor = (AnchorStyles)14;
		ErrorLabel.BorderStyle = (BorderStyle)2;
		((Control)ErrorLabel).ForeColor = Color.Red;
		((Control)ErrorLabel).Location = new Point(12, 488);
		((Control)ErrorLabel).Name = "ErrorLabel";
		((Control)ErrorLabel).Size = new Size(265, 22);
		((Control)ErrorLabel).TabIndex = 7;
		((Control)MonthlyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)MonthlyRadioButton).AutoSize = true;
		((Control)MonthlyRadioButton).Location = new Point(283, 492);
		((Control)MonthlyRadioButton).Name = "MonthlyRadioButton";
		((Control)MonthlyRadioButton).Size = new Size(62, 17);
		((Control)MonthlyRadioButton).TabIndex = 10;
		((Control)MonthlyRadioButton).Tag = "Monthly";
		((ButtonBase)MonthlyRadioButton).Text = "&Monthly";
		((ButtonBase)MonthlyRadioButton).UseVisualStyleBackColor = true;
		((Control)WeeklyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)WeeklyRadioButton).AutoSize = true;
		((Control)WeeklyRadioButton).Location = new Point(283, 477);
		((Control)WeeklyRadioButton).Name = "WeeklyRadioButton";
		((Control)WeeklyRadioButton).Size = new Size(61, 17);
		((Control)WeeklyRadioButton).TabIndex = 9;
		((Control)WeeklyRadioButton).Tag = "Weekly";
		((ButtonBase)WeeklyRadioButton).Text = "&Weekly";
		((ButtonBase)WeeklyRadioButton).UseVisualStyleBackColor = true;
		((Control)DailyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)DailyRadioButton).AutoSize = true;
		DailyRadioButton.Checked = true;
		((Control)DailyRadioButton).Location = new Point(283, 462);
		((Control)DailyRadioButton).Name = "DailyRadioButton";
		((Control)DailyRadioButton).Size = new Size(48, 17);
		((Control)DailyRadioButton).TabIndex = 8;
		DailyRadioButton.TabStop = true;
		((Control)DailyRadioButton).Tag = "Daily";
		((ButtonBase)DailyRadioButton).Text = "Dail&y";
		((ButtonBase)DailyRadioButton).UseVisualStyleBackColor = true;
		((Control)HelpButton1).Anchor = (AnchorStyles)10;
		((Control)HelpButton1).Location = new Point(936, 463);
		((Control)HelpButton1).Name = "HelpButton1";
		((Control)HelpButton1).Size = new Size(60, 23);
		((Control)HelpButton1).TabIndex = 22;
		((ButtonBase)HelpButton1).Text = "&Help";
		((ButtonBase)HelpButton1).UseVisualStyleBackColor = true;
		((Control)ProgressBar1).Anchor = (AnchorStyles)10;
		((Control)ProgressBar1).ForeColor = Color.Green;
		((Control)ProgressBar1).Location = new Point(410, 463);
		((Control)ProgressBar1).Name = "ProgressBar1";
		((Control)ProgressBar1).Size = new Size(122, 23);
		((Control)ProgressBar1).TabIndex = 12;
		((Control)StrictCheckBox).Anchor = (AnchorStyles)10;
		((ButtonBase)StrictCheckBox).AutoSize = true;
		((Control)StrictCheckBox).Location = new Point(351, 492);
		((Control)StrictCheckBox).Name = "StrictCheckBox";
		((Control)StrictCheckBox).Size = new Size(50, 17);
		((Control)StrictCheckBox).TabIndex = 11;
		((ButtonBase)StrictCheckBox).Text = "St&rict";
		((ButtonBase)StrictCheckBox).UseVisualStyleBackColor = true;
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(407, 494);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(44, 13);
		((Control)Label1).TabIndex = 13;
		Label1.Text = "S&ymbol:";
		((Control)SymbolTextBox).Anchor = (AnchorStyles)10;
		((Control)SymbolTextBox).Location = new Point(457, 491);
		((Control)SymbolTextBox).Name = "SymbolTextBox";
		((Control)SymbolTextBox).Size = new Size(75, 20);
		((Control)SymbolTextBox).TabIndex = 14;
		((Control)PatternsButton).Anchor = (AnchorStyles)10;
		((Control)PatternsButton).Location = new Point(804, 492);
		((Control)PatternsButton).Name = "PatternsButton";
		((Control)PatternsButton).Size = new Size(60, 23);
		((Control)PatternsButton).TabIndex = 24;
		((ButtonBase)PatternsButton).Text = "&Patterns";
		((ButtonBase)PatternsButton).UseVisualStyleBackColor = true;
		((Control)ClipboardButton).Anchor = (AnchorStyles)10;
		((Control)ClipboardButton).Enabled = false;
		((Control)ClipboardButton).Location = new Point(738, 464);
		((Control)ClipboardButton).Name = "ClipboardButton";
		((Control)ClipboardButton).Size = new Size(60, 23);
		((Control)ClipboardButton).TabIndex = 19;
		((ButtonBase)ClipboardButton).Text = "Clip&board";
		((ButtonBase)ClipboardButton).UseVisualStyleBackColor = true;
		((Control)StartButton).Anchor = (AnchorStyles)10;
		((Control)StartButton).Location = new Point(870, 492);
		((Control)StartButton).Name = "StartButton";
		((Control)StartButton).Size = new Size(60, 23);
		((Control)StartButton).TabIndex = 0;
		((ButtonBase)StartButton).Text = "St&art";
		((ButtonBase)StartButton).UseVisualStyleBackColor = true;
		((Control)StopButton).Anchor = (AnchorStyles)10;
		((Control)StopButton).Enabled = false;
		((Control)StopButton).Location = new Point(870, 463);
		((Control)StopButton).Name = "StopButton";
		((Control)StopButton).Size = new Size(60, 23);
		((Control)StopButton).TabIndex = 21;
		((ButtonBase)StopButton).Text = "St&op";
		((ButtonBase)StopButton).UseVisualStyleBackColor = true;
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(936, 492);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(60, 23);
		((Control)DoneButton).TabIndex = 1;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)Label3).Anchor = (AnchorStyles)10;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(548, 494);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(23, 13);
		((Control)Label3).TabIndex = 17;
		Label3.Text = "&To:";
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(538, 469);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(33, 13);
		((Control)Label2).TabIndex = 15;
		Label2.Text = "&From:";
		DataGridView1.AllowUserToAddRows = false;
		DataGridView1.AllowUserToDeleteRows = false;
		DataGridView1.AllowUserToResizeColumns = false;
		DataGridView1.AllowUserToResizeRows = false;
		((Control)DataGridView1).Anchor = (AnchorStyles)15;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)10;
		DataGridView1.AutoSizeRowsMode = (DataGridViewAutoSizeRowsMode)11;
		((Control)DataGridView1).CausesValidation = false;
		DataGridView1.ColumnHeadersHeightSizeMode = (DataGridViewColumnHeadersHeightSizeMode)2;
		DataGridView1.EditMode = (DataGridViewEditMode)4;
		((Control)DataGridView1).Location = new Point(12, 12);
		((Control)DataGridView1).Name = "DataGridView1";
		DataGridView1.ReadOnly = true;
		DataGridView1.RowTemplate.ReadOnly = true;
		DataGridView1.RowTemplate.Resizable = (DataGridViewTriState)1;
		DataGridView1.SelectionMode = (DataGridViewSelectionMode)1;
		DataGridView1.ShowCellErrors = false;
		DataGridView1.ShowCellToolTips = false;
		DataGridView1.ShowEditingIcon = false;
		DataGridView1.ShowRowErrors = false;
		((Control)DataGridView1).Size = new Size(984, 396);
		((Control)DataGridView1).TabIndex = 2;
		((Control)TestButton).Anchor = (AnchorStyles)10;
		((Control)TestButton).Enabled = false;
		((Control)TestButton).Location = new Point(804, 464);
		((Control)TestButton).Name = "TestButton";
		((Control)TestButton).Size = new Size(60, 23);
		((Control)TestButton).TabIndex = 20;
		((ButtonBase)TestButton).Text = "&Test";
		((ButtonBase)TestButton).UseVisualStyleBackColor = true;
		((Control)ScoreAllPortfoliosButton).Anchor = (AnchorStyles)10;
		((Control)ScoreAllPortfoliosButton).Enabled = false;
		((Control)ScoreAllPortfoliosButton).Location = new Point(686, 491);
		((Control)ScoreAllPortfoliosButton).Name = "ScoreAllPortfoliosButton";
		((Control)ScoreAllPortfoliosButton).Size = new Size(112, 23);
		((Control)ScoreAllPortfoliosButton).TabIndex = 23;
		((ButtonBase)ScoreAllPortfoliosButton).Text = "&Score All Portfolios";
		((ButtonBase)ScoreAllPortfoliosButton).UseVisualStyleBackColor = true;
		((Control)Label4).Anchor = (AnchorStyles)10;
		Label4.AutoSize = true;
		((Control)Label4).Location = new Point(12, 436);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(84, 13);
		((Control)Label4).TabIndex = 3;
		Label4.Text = "&API Key/Token:";
		((Control)APIKeyTextBox).Anchor = (AnchorStyles)10;
		((Control)APIKeyTextBox).Location = new Point(102, 433);
		((TextBoxBase)APIKeyTextBox).MaxLength = 100;
		((Control)APIKeyTextBox).Name = "APIKeyTextBox";
		((Control)APIKeyTextBox).Size = new Size(103, 20);
		((Control)APIKeyTextBox).TabIndex = 4;
		((TextBoxBase)APIKeyTextBox).WordWrap = false;
		((Control)GroupBox1).Anchor = (AnchorStyles)10;
		((Control)GroupBox1).Controls.Add((Control)(object)IEXRadioButton);
		((Control)GroupBox1).Controls.Add((Control)(object)FinnhubRB);
		((Control)GroupBox1).Location = new Point(226, 414);
		((Control)GroupBox1).Name = "GroupBox1";
		((Control)GroupBox1).Size = new Size(138, 43);
		((Control)GroupBox1).TabIndex = 5;
		GroupBox1.TabStop = false;
		GroupBox1.Text = "Quote Vendor";
		((Control)IEXRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)IEXRadioButton).AutoSize = true;
		((Control)IEXRadioButton).Location = new Point(89, 18);
		((Control)IEXRadioButton).Name = "IEXRadioButton";
		((Control)IEXRadioButton).Size = new Size(42, 17);
		((Control)IEXRadioButton).TabIndex = 1;
		((Control)IEXRadioButton).Tag = "Daily";
		((ButtonBase)IEXRadioButton).Text = "&IEX";
		((ButtonBase)IEXRadioButton).UseVisualStyleBackColor = true;
		((Control)FinnhubRB).Anchor = (AnchorStyles)10;
		((ButtonBase)FinnhubRB).AutoSize = true;
		FinnhubRB.Checked = true;
		((Control)FinnhubRB).Location = new Point(9, 18);
		((Control)FinnhubRB).Name = "FinnhubRB";
		((Control)FinnhubRB).Size = new Size(74, 17);
		((Control)FinnhubRB).TabIndex = 0;
		FinnhubRB.TabStop = true;
		((Control)FinnhubRB).Tag = "Daily";
		((ButtonBase)FinnhubRB).Text = "&Finnhub.io";
		((ButtonBase)FinnhubRB).UseVisualStyleBackColor = true;
		((Control)LinkLabel1).Anchor = (AnchorStyles)10;
		((Label)LinkLabel1).AutoSize = true;
		LinkLabel1.LinkColor = Color.Black;
		((Control)LinkLabel1).Location = new Point(370, 432);
		((Control)LinkLabel1).Name = "LinkLabel1";
		((Control)LinkLabel1).Size = new Size(233, 13);
		((Control)LinkLabel1).TabIndex = 25;
		LinkLabel1.TabStop = true;
		LinkLabel1.Text = "Data provided by IEX Cloud:  https://iexcloud.io";
		((Control)LinkLabel1).Visible = false;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(1008, 521);
		((Control)this).Controls.Add((Control)(object)LinkLabel1);
		((Control)this).Controls.Add((Control)(object)GroupBox1);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)APIKeyTextBox);
		((Control)this).Controls.Add((Control)(object)ScoreAllPortfoliosButton);
		((Control)this).Controls.Add((Control)(object)TestButton);
		((Control)this).Controls.Add((Control)(object)ToDatePicker);
		((Control)this).Controls.Add((Control)(object)FromDatePicker);
		((Control)this).Controls.Add((Control)(object)FilenameLabel);
		((Control)this).Controls.Add((Control)(object)ErrorLabel);
		((Control)this).Controls.Add((Control)(object)MonthlyRadioButton);
		((Control)this).Controls.Add((Control)(object)WeeklyRadioButton);
		((Control)this).Controls.Add((Control)(object)DailyRadioButton);
		((Control)this).Controls.Add((Control)(object)HelpButton1);
		((Control)this).Controls.Add((Control)(object)ProgressBar1);
		((Control)this).Controls.Add((Control)(object)StrictCheckBox);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)SymbolTextBox);
		((Control)this).Controls.Add((Control)(object)PatternsButton);
		((Control)this).Controls.Add((Control)(object)ClipboardButton);
		((Control)this).Controls.Add((Control)(object)StartButton);
		((Control)this).Controls.Add((Control)(object)StopButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)DataGridView1);
		((Control)this).Name = "ScoreForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Score Form";
		((ISupportInitialize)DataGridView1).EndInit();
		((Control)GroupBox1).ResumeLayout(false);
		((Control)GroupBox1).PerformLayout();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void ScoreForm_FormClosing(object sender, FormClosingEventArgs e)
	{
		GlobalForm.SFDateLookBack = checked((int)Math.Abs(DateAndTime.DateDiff((DateInterval)4, FromDatePicker.Value, ToDatePicker.Value, (FirstDayOfWeek)1, (FirstWeekOfYear)1)));
		GlobalForm.StrictPatterns = lsStrict;
		GlobalForm.SFStrict = StrictCheckBox.Checked;
		bool flag = true;
		if (flag == DailyRadioButton.Checked)
		{
			GlobalForm.SFDWM = 0;
		}
		else if (flag == WeeklyRadioButton.Checked)
		{
			GlobalForm.SFDWM = 1;
		}
		else if (flag == MonthlyRadioButton.Checked)
		{
			GlobalForm.SFDWM = 2;
		}
		bool flag2 = true;
		if (flag2 == FinnhubRB.Checked)
		{
			GlobalForm.Vendor = GlobalForm.FINNHUB;
		}
		else if (flag2 == IEXRadioButton.Checked)
		{
			GlobalForm.Vendor = GlobalForm.IEX;
		}
		if (Operators.CompareString(GlobalForm.lsFinnhubKey, GlobalForm.FinnhubKey, false) != 0)
		{
			string text = new GlobalForm.Simple3Des("F712DC14acD5\u0019").EncryptData(GlobalForm.FinnhubKey);
			try
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap2", (object)text);
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				ProjectData.ClearProjectError();
			}
		}
		if (Operators.CompareString(GlobalForm.lsIEXKey, GlobalForm.IEXKey, false) != 0)
		{
			string text2 = new GlobalForm.Simple3Des("45EDC2319CBc5\u0019").EncryptData(GlobalForm.IEXKey);
			try
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "MarketCap3", (object)text2);
			}
			catch (Exception ex3)
			{
				ProjectData.SetProjectError(ex3);
				Exception ex4 = ex3;
				ProjectData.ClearProjectError();
			}
		}
		MySettingsProperty.Settings.ScoreLocation = ((Form)this).Location;
		MySettingsProperty.Settings.ScoreSize = ((Form)this).Size;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
	}

	private void ScoreForm_Load(object sender, EventArgs e)
	{
		//IL_001a: Unknown result type (might be due to invalid IL or missing references)
		//IL_001f: Unknown result type (might be due to invalid IL or missing references)
		//IL_002a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0035: Unknown result type (might be due to invalid IL or missing references)
		//IL_0040: Unknown result type (might be due to invalid IL or missing references)
		//IL_0047: Unknown result type (might be due to invalid IL or missing references)
		//IL_0058: Unknown result type (might be due to invalid IL or missing references)
		//IL_0069: Unknown result type (might be due to invalid IL or missing references)
		//IL_007a: Unknown result type (might be due to invalid IL or missing references)
		//IL_008b: Unknown result type (might be due to invalid IL or missing references)
		//IL_009c: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_00be: Unknown result type (might be due to invalid IL or missing references)
		//IL_00cf: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f1: Unknown result type (might be due to invalid IL or missing references)
		//IL_0102: Unknown result type (might be due to invalid IL or missing references)
		//IL_0113: Unknown result type (might be due to invalid IL or missing references)
		//IL_0124: Unknown result type (might be due to invalid IL or missing references)
		//IL_0135: Unknown result type (might be due to invalid IL or missing references)
		//IL_0146: Unknown result type (might be due to invalid IL or missing references)
		//IL_0157: Unknown result type (might be due to invalid IL or missing references)
		//IL_0168: Unknown result type (might be due to invalid IL or missing references)
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.ScoreLocation, MySettingsProperty.Settings.ScoreSize);
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)APIKeyTextBox, "Enter token or API key for the associated Quote Vendor.");
		val.SetToolTip((Control)(object)ClipboardButton, "Copy highlighted rows to the clipboard.");
		val.SetToolTip((Control)(object)DailyRadioButton, "Find patterns using the daily scale.");
		val.SetToolTip((Control)(object)DataGridView1, "Highlight rows to copy to the clipboard.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)FinnhubRB, "Get informaton from Finnhub.io.");
		val.SetToolTip((Control)(object)FromDatePicker, "Enter the starting date to search for patterns.");
		val.SetToolTip((Control)(object)HelpButton1, "Get help for this form.");
		val.SetToolTip((Control)(object)IEXRadioButton, "Get informaton from IEX.");
		val.SetToolTip((Control)(object)MonthlyRadioButton, "Find patterns using the monthly scale.");
		val.SetToolTip((Control)(object)PatternsButton, "Load the Chart Patterns Form.");
		val.SetToolTip((Control)(object)ScoreAllPortfoliosButton, "Open all portfolios and score each symbol file.");
		val.SetToolTip((Control)(object)StartButton, "Start scoring patterns.");
		val.SetToolTip((Control)(object)StopButton, "Halt the scoring process.");
		val.SetToolTip((Control)(object)StrictCheckBox, "Use strict or loose rules when finding chart patterns.");
		val.SetToolTip((Control)(object)SymbolTextBox, "Enter a symbol, if desired, to score.");
		val.SetToolTip((Control)(object)TestButton, "After scoring patterns, rank how well the scores performed.");
		val.SetToolTip((Control)(object)ToDatePicker, "Enter the ending date to search for pattern.");
		val.SetToolTip((Control)(object)WeeklyRadioButton, "Find patterns using the weekly scale.");
		ProgressBar1.Value = 0;
		SymbolTextBox.Text = "";
		StopPressed = false;
		switch (GlobalForm.SFDWM)
		{
		case 0:
			DailyRadioButton.Checked = true;
			break;
		case 1:
			WeeklyRadioButton.Checked = true;
			break;
		case 2:
			MonthlyRadioButton.Checked = true;
			break;
		default:
			DailyRadioButton.Checked = true;
			break;
		}
		DisableEnable(EnableFlag: true);
		((Control)DailyRadioButton).Tag = 0;
		((Control)WeeklyRadioButton).Tag = 1;
		((Control)MonthlyRadioButton).Tag = 2;
		FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)checked(-1 * GlobalForm.SFDateLookBack), DateAndTime.Now);
		ToDatePicker.Value = DateAndTime.Now;
		lsStrict = GlobalForm.StrictPatterns;
		StrictCheckBox.Checked = GlobalForm.SFStrict;
		GlobalForm.StrictPatterns = GlobalForm.SFStrict;
		GlobalForm.ShowAllPatterns = true;
		DataGridView1.ClipboardCopyMode = (DataGridViewClipboardCopyMode)2;
		BuildGridHeader();
		if (GlobalForm.Vendor == GlobalForm.FINNHUB)
		{
			FinnhubRB.Checked = true;
		}
		else if (GlobalForm.Vendor == GlobalForm.IEX)
		{
			IEXRadioButton.Checked = true;
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
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		GlobalForm.lsFinnhubKey = GlobalForm.FinnhubKey;
		if (FinnhubRB.Checked)
		{
			APIKeyTextBox.Text = GlobalForm.FinnhubKey;
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
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			ProjectData.ClearProjectError();
		}
		GlobalForm.lsIEXKey = GlobalForm.IEXKey;
		if (IEXRadioButton.Checked)
		{
			APIKeyTextBox.Text = GlobalForm.IEXKey;
		}
	}

	private void APIKeyTextBox_TextChanged(object sender, EventArgs e)
	{
		if (FinnhubRB.Checked)
		{
			GlobalForm.FinnhubKey = APIKeyTextBox.Text;
		}
		else
		{
			GlobalForm.IEXKey = APIKeyTextBox.Text;
		}
	}

	private void BuildGrid(string Filename)
	{
		DataGridView1.RowHeadersVisible = false;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)1;
		GetMarketCapScore(Filename);
		checked
		{
			int num = GlobalForm.PatternCount - 1;
			for (int i = 0; i <= num; i++)
			{
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				if (StopPressed)
				{
					break;
				}
				GlobalForm.UseOriginalDate = false;
				string marketCap = Scores.MarketCap;
				bool qMarketCap = Scores.qMarketCap;
				int sMarketCap = Scores.sMarketCap;
				Scores = default(ScoreInfo);
				Scores.MarketCap = marketCap;
				Scores.qMarketCap = qMarketCap;
				Scores.sMarketCap = sMarketCap;
				GlobalForm.GetCPInformation(i);
				if (GetScore(i, Filename))
				{
					continue;
				}
				DataGridView1.Rows.Add();
				DataGridView1.Rows[iRow].Cells[0].Value = Filename;
				DataGridView1.Rows[iRow].Cells[1].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]);
				int num2 = 0;
				num2 += Scores.sTrendStart;
				num2 += Scores.sFlatBase;
				num2 += Scores.sHCR;
				num2 += Scores.sYrlyRange;
				num2 += Scores.sHeight;
				num2 += Scores.sVolume;
				num2 += Scores.sBkoutVol;
				num2 += Scores.sThrowPull;
				num2 += Scores.sBkoutGap;
				num2 += Scores.sMarketCap;
				DataGridView1.Rows[iRow].Cells[2].Value = num2;
				try
				{
					if ((Conversion.Val(GlobalForm.CPInfo.BkoutPrice) != 0.0) & (Operators.CompareString(GlobalForm.CPInfo.UltHLPrice, "", false) != 0))
					{
						DataGridView1.Rows[iRow].Cells[3].Value = Strings.Format((object)((Conversion.Val(GlobalForm.CPInfo.UltHLPrice) - Conversion.Val(GlobalForm.CPInfo.BkoutPrice)) / Conversion.Val(GlobalForm.CPInfo.BkoutPrice)), "0.0%");
					}
					else
					{
						DataGridView1.Rows[iRow].Cells[3].Value = "?";
						DataGridView1.Rows[iRow].Cells[3].Style.BackColor = Color.Red;
					}
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					ProjectData.ClearProjectError();
				}
				DataGridView1.Rows[iRow].Cells[4].Value = GlobalForm.GetPatternPhrase(i);
				int num3 = ((GlobalForm.ChartPatterns[i].iStart2Date == 0) ? GlobalForm.ChartPatterns[i].iStartDate : Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iStartDate < GlobalForm.ChartPatterns[i].iStart2Date, (object)GlobalForm.ChartPatterns[i].iStartDate, (object)GlobalForm.ChartPatterns[i].iStart2Date)));
				int num4 = ((!GlobalForm.UseOriginalDate) ? Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iEndDate > GlobalForm.ChartPatterns[i].iEnd2Date, (object)GlobalForm.ChartPatterns[i].iEndDate, (object)GlobalForm.ChartPatterns[i].iEnd2Date)) : GlobalForm.ChartPatterns[i].iEndDate);
				DataGridView1.Rows[iRow].Cells[5].Value = Strings.Format((object)GlobalForm.nDT[0, num3], GlobalForm.UserDate);
				DataGridView1.Rows[iRow].Cells[6].Value = Strings.Format((object)GlobalForm.nDT[0, num4], GlobalForm.UserDate);
				if (Scores.qTrendStart)
				{
					if (Scores.iTs == -1)
					{
						DataGridView1.Rows[iRow].Cells[7].Value = "? " + Scores.TrendStart + " " + Conversions.ToString(Scores.sTrendStart);
						DataGridView1.Rows[iRow].Cells[7].Style.BackColor = Color.Red;
					}
					else
					{
						DataGridView1.Rows[iRow].Cells[7].Value = Strings.Format((object)GlobalForm.nDT[0, Scores.iTs], "yyyy/MM/dd") + " " + Scores.TrendStart + " " + Conversions.ToString(Scores.sTrendStart);
					}
				}
				else
				{
					DataGridView1.Rows[iRow].Cells[7].Value = "? 0";
					DataGridView1.Rows[iRow].Cells[7].Style.BackColor = Color.Red;
				}
				if (Scores.qFlatBase)
				{
					DataGridView1.Rows[iRow].Cells[8].Value = Strings.Format((object)GlobalForm.nDT[0, Scores.iFlatBaseStart], "yyyy/MM/dd") + " to " + Strings.Format((object)GlobalForm.nDT[0, Scores.iFlatBaseEnd], "yyyy/MM/dd") + " " + Conversions.ToString(Scores.sFlatBase);
				}
				else
				{
					DataGridView1.Rows[iRow].Cells[8].Value = Scores.sFlatBase;
				}
				if (Scores.HCR)
				{
					DataGridView1.Rows[iRow].Cells[9].Value = Strings.Format((object)GlobalForm.nDT[0, Scores.iHCRStart], "yyyy/MM/dd") + " to " + Strings.Format((object)GlobalForm.nDT[0, Scores.iHCREnd], "yyyy/MM/dd") + " " + Conversions.ToString(Scores.sHCR);
				}
				else
				{
					DataGridView1.Rows[iRow].Cells[9].Value = Scores.sHCR;
				}
				if (Scores.qYrlyRange)
				{
					DataGridView1.Rows[iRow].Cells[10].Value = Scores.YrlyRange + " " + Conversions.ToString(Scores.sYrlyRange);
				}
				else
				{
					DataGridView1.Rows[iRow].Cells[10].Value = "None. 0";
					DataGridView1.Rows[iRow].Cells[10].Style.BackColor = Color.Red;
				}
				if (Scores.qHeight)
				{
					DataGridView1.Rows[iRow].Cells[11].Value = Conversions.ToString(Interaction.IIf(Scores.Tall, (object)"Tall ", (object)"Short ")) + Scores.sHeight;
				}
				else
				{
					DataGridView1.Rows[iRow].Cells[11].Value = "? 0";
					DataGridView1.Rows[iRow].Cells[11].Style.BackColor = Color.Red;
				}
				if (Scores.qVolume)
				{
					DataGridView1.Rows[iRow].Cells[12].Value = Conversions.ToString(Interaction.IIf(Scores.Volume == -1, (object)"Down ", (object)"Up ")) + Conversions.ToString(Scores.sVolume);
				}
				else
				{
					DataGridView1.Rows[iRow].Cells[12].Value = "? 0";
					DataGridView1.Rows[iRow].Cells[12].Style.BackColor = Color.Red;
				}
				if (Scores.qBkoutVol)
				{
					DataGridView1.Rows[iRow].Cells[13].Value = Scores.BkoutVol + " " + Conversions.ToString(Scores.sBkoutVol);
				}
				else
				{
					DataGridView1.Rows[iRow].Cells[13].Value = "? 0";
					DataGridView1.Rows[iRow].Cells[13].Style.BackColor = Color.Red;
				}
				if (Scores.qThrowPull)
				{
					DataGridView1.Rows[iRow].Cells[14].Value = Conversions.ToString(Scores.ThrowPull) + " " + Conversions.ToString(Scores.sThrowPull);
				}
				else
				{
					DataGridView1.Rows[iRow].Cells[14].Value = "? " + Conversions.ToString(Scores.sThrowPull);
					DataGridView1.Rows[iRow].Cells[14].Style.BackColor = Color.Red;
				}
				DataGridView1.Rows[iRow].Cells[15].Value = Conversions.ToString(Scores.BkoutGap) + " " + Conversions.ToString(Scores.sBkoutGap);
				if (Scores.qMarketCap)
				{
					DataGridView1.Rows[iRow].Cells[16].Value = Scores.MarketCap + " " + Conversions.ToString(Scores.sMarketCap);
				}
				else
				{
					DataGridView1.Rows[iRow].Cells[16].Value = "? 0";
					DataGridView1.Rows[iRow].Cells[16].Style.BackColor = Color.Red;
				}
				DataGridView1.Rows[iRow].Cells[17].Value = RuntimeHelpers.GetObjectValue(Interaction.IIf(Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, (string)null, false) == 0, (object)"None yet", (object)GlobalForm.CPInfo.BkoutDirection));
				DataGridView1.Rows[iRow].Cells[18].Value = GlobalForm.CPInfo.BkoutDate;
				DataGridView1.Rows[iRow].Cells[19].Value = GlobalForm.CPInfo.BkoutPrice;
				DataGridView1.Rows[iRow].Cells[20].Value = GlobalForm.CPInfo.UltHLPrice;
				DataGridView1.Rows[iRow].Cells[21].Value = GlobalForm.CPInfo.UltHLDate;
				iRow++;
			}
			DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)6;
			DataGridView1.RowHeadersVisible = true;
		}
	}

	private void BuildGridHeader()
	{
		DataGridView1.RowCount = 0;
		DataGridView1.ColumnCount = 22;
		DataGridView1.Columns[0].Name = "Stock";
		DataGridView1.Columns[1].Name = "Last Close";
		DataGridView1.Columns[2].Name = "Score";
		DataGridView1.Columns[3].Name = "Gain";
		DataGridView1.Columns[4].Name = "Pattern";
		DataGridView1.Columns[5].Name = "Start";
		DataGridView1.Columns[6].Name = "End";
		DataGridView1.Columns[7].Name = "Trend Start";
		DataGridView1.Columns[8].Name = "Flat Base";
		DataGridView1.Columns[9].Name = "HCR";
		DataGridView1.Columns[10].Name = "Yr Hi/Lo Position";
		DataGridView1.Columns[11].Name = "Height";
		DataGridView1.Columns[12].Name = "Volume Trend";
		DataGridView1.Columns[13].Name = "Bkout Day Volume";
		DataGridView1.Columns[14].Name = "Throw/Pullback";
		DataGridView1.Columns[15].Name = "Bkout Day Gaps";
		DataGridView1.Columns[16].Name = "Market Cap";
		DataGridView1.Columns[17].Name = "Breakout";
		DataGridView1.Columns[18].Name = "Bkout Date";
		DataGridView1.Columns[19].Name = "Bkout Price";
		DataGridView1.Columns[20].Name = "Ultimate High/Low";
		DataGridView1.Columns[21].Name = "Ultimate H/L Date";
	}

	private void BuildList()
	{
		//IL_00b0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ac: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b3: Invalid comparison between Unknown and I4
		GlobalForm.ChartStart = FromDatePicker.Value.Date;
		GlobalForm.ChartEnd = ToDatePicker.Value.Date;
		ProgressBar1.Value = 0;
		if (!GlobalForm.Quiet)
		{
			DataGridView1.RowCount = 0;
			iRow = 0;
		}
		else
		{
			iRow = DataGridView1.RowCount;
		}
		checked
		{
			if (MyProject.Forms.Mainform.ListBox1.SelectedIndex == -1)
			{
				if (((TextBoxBase)SymbolTextBox).TextLength != 0)
				{
					ProcessSymbol();
					ProgressBar1.Value = 100;
					return;
				}
				DialogResult val = (GlobalForm.Quiet ? ((DialogResult)6) : MessageBox.Show("No stocks were selected on the prior form. Did you want me to select all of them?", "Patternz: ThePatternSite.com", (MessageBoxButtons)4, (MessageBoxIcon)64));
				if (unchecked((int)val) != 6)
				{
					return;
				}
				MyProject.Forms.Mainform.ListBox1.BeginUpdate();
				int num = MyProject.Forms.Mainform.ListBox1.Items.Count - 1;
				for (int i = 0; i <= num; i++)
				{
					MyProject.Forms.Mainform.ListBox1.SetSelected(i, true);
				}
				MyProject.Forms.Mainform.ListBox1.EndUpdate();
			}
			else if (((TextBoxBase)SymbolTextBox).TextLength != 0)
			{
				ProcessSymbol();
			}
			int num2 = MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count - 1;
			for (int j = 0; j <= num2; j++)
			{
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				if (StopPressed)
				{
					break;
				}
				string text = MyProject.Forms.Mainform.ListBox1.SelectedItems[j].ToString();
				FilenameLabel.Text = text;
				((Control)FilenameLabel).Refresh();
				ProgressBar ProgBar = null;
				Label ErrorLabel = null;
				if (GlobalForm.LoadFile(text, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this)))
				{
					continue;
				}
				if (GlobalForm.IntradayData)
				{
					(ErrorLabel = this.ErrorLabel).Text = ErrorLabel.Text + "\r\n" + text + ": Intraday data files not supported.";
				}
				else
				{
					GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
					if (GlobalForm.ErrorMessage != null)
					{
						(ErrorLabel = this.ErrorLabel).Text = ErrorLabel.Text + "\r\n" + GlobalForm.ErrorMessage;
					}
					bool showCandles = GlobalForm.ShowCandles;
					GlobalForm.ShowCandles = false;
					FindPatterns.EnterFindPatterns(GlobalForm.ChartStart, GlobalForm.ChartEnd, null, ref StopPressed, 3);
					GlobalForm.ShowCandles = showCandles;
					if (GlobalForm.PatternCount > 0)
					{
						BuildGrid(text);
					}
				}
				ProgressBar1.Value = (int)Math.Round((double)(100 * j) / (double)MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count);
			}
			ProgressBar1.Value = 100;
			if (GlobalForm.Quiet)
			{
				return;
			}
			if (this.ErrorLabel.Text.Length > 0)
			{
				this.ErrorLabel.Text = "Numerous errors could mean the quote file received a bad update. Go to the Update Form and update the file using 'Get historical quotes' option to make sure the file has good information.\r\n\r\n" + this.ErrorLabel.Text;
				try
				{
					Clipboard.SetText(this.ErrorLabel.Text);
					this.ErrorLabel.Text = "Error messages are on the clipboard.";
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					ProjectData.ClearProjectError();
				}
			}
			FilenameLabel.Text = "We're done, boss!";
		}
	}

	private void ClipboardButton_Click(object sender, EventArgs e)
	{
		//IL_01de: Unknown result type (might be due to invalid IL or missing references)
		//IL_0213: Unknown result type (might be due to invalid IL or missing references)
		//IL_014d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0153: Expected O, but got Unknown
		if (((BaseCollection)DataGridView1.SelectedRows).Count == 0)
		{
			DataGridView1.SelectAll();
		}
		DisableEnable(EnableFlag: false);
		StopPressed = false;
		((Control)StopButton).Focus();
		ErrorLabel.Text = "This could take a while. If needed, click Stop to cancel.";
		FilenameLabel.Text = "";
		((Control)this).Cursor = Cursors.WaitCursor;
		string text = "DISCLAIMER: The scoring system is a tool to help you select better performing chart patterns, but there is no guarantee. Some patterns will work better than others, regardless of the score. How you trade will determine success or failure. The gains shown on the Scoring Form represent PERFECT TRADES, so your actual trading results will vary. Past performance doesn't guarantee future results. YOU ALONE ARE RESPONSIBLE FOR YOUR INVESTMENT DECISIONS. Please understand that the Score Form does NOT make recommendations as to which security you should trade.";
		text += "\r\n\r\nOn average, patterns with scores above 0 tend to perform better than do those with scores below 0. Generally, the lower the number (10 is best, -10 is worst), the worse the performance.";
		text += "\r\n\r\nSCORE: A number from +10 to -10, based on ten performance factors. Those appear in the list with a 1, 0, or -1 value appended to them and the score may vary from chart pattern to pattern. A question mark means a score could not be determined. CHECK ALL RESULTS FOR ACCURACY.";
		text += "\r\nGAIN: measures from the breakout price to the ultimate high or ultimate low, if available. The ult hi is the highest price before price drops at least 20%. Ult low is the lowest price before price rises at least 20%.";
		text += "\r\nTREND START: Before the chart pattern start, it's the highest high or lowest low before which price drops/rises, respectively, at least 20%.";
		text += "\r\nFLAT BASE: When price moves horizontally, often for months. Very rare, but precedes a good performing chart pattern. Hard to find automatically, accurately so check the weekly chart (3 months of horizontal price movement in a narrow range).";
		text += "\r\nHCR: Horizontal consolidation region. Hard to find automatically, accurately, so check the chart. HCRs are regions of congestion likely to hinder future price movement. Located between the trend start and pattern start and always in the path of future price movement (above the pattern for upward breakouts, for example). HCRs are bad news for performance.";
		text += "\r\nYEARLY HI/LO POSITION: Location of the breakout price in the yearly price range (split into thirds). Generally, patterns near the yearly low outperform.";
		text += "\r\nHEIGHT: height of the chart pattern as a percentage of the breakout price. On average, tall patterns outperform short ones.";
		text += "\r\nVOLUME TREND: Linear regression volume trend from the start to end of the chart pattern.";
		text += "\r\nBKOUT DAY VOLUME: Volume on day of breakout versus 3-month average. Heavy is 25% or more above the average.";
		text += "\r\nTHROW/PULLBACK: A throwback or pullback almost always hurts performance.";
		text += "\r\nBKOUT DAY GAPS: A gap that occurs on the day of breakout. Can help or hurt performance, depending on chart pattern type.";
		text += "\r\nMARKET CAP: Small (below 1 billion), mid (1-5 billion), large (over 5 billion) cap. A function of the stock's price and shares outstanding.";
		text += "\r\n";
		text += "\r\nFor more information on the scoring system, buy a copy of my book(s) 'Trading Classic Chart Patterns' or 'Fundamental Analysis and Position Trading'.";
		text += "\r\nFor more information on terms, read the glossary on ThePatternSite.com. Copyright (c) 2016-2024 by Thomas Bulkowski and ThePatternSite.com. All rights reserved.";
		text += "\r\n\r\n";
		foreach (DataGridViewColumn item in (BaseCollection)DataGridView1.Columns)
		{
			DataGridViewColumn val = item;
			text = text + val.Name + "\t";
		}
		text += "\r\n";
		try
		{
			Clipboard.SetDataObject((object)DataGridView1.GetClipboardContent());
			text += Clipboard.GetText();
			((Control)StopButton).Enabled = false;
			Clipboard.SetText(text);
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			MessageBox.Show("Clipboard is busy with another user. Error: " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			ProjectData.ClearProjectError();
		}
		((Control)this).Cursor = Cursors.Default;
		ErrorLabel.Text = "";
		MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		DisableEnable(EnableFlag: true);
	}

	private void DisableEnable(bool EnableFlag)
	{
		if (EnableFlag)
		{
			((Control)WeeklyRadioButton).Enabled = true;
			((Control)ToDatePicker).Enabled = true;
			((Control)SymbolTextBox).Enabled = true;
			((Control)StrictCheckBox).Enabled = true;
			((Control)StopButton).Enabled = false;
			((Control)StartButton).Enabled = true;
			((Control)ScoreAllPortfoliosButton).Enabled = true;
			((Control)PatternsButton).Enabled = true;
			((Control)MonthlyRadioButton).Enabled = true;
			((Control)HelpButton1).Enabled = true;
			((Control)FromDatePicker).Enabled = true;
			((Control)DoneButton).Enabled = true;
			((Control)DailyRadioButton).Enabled = true;
			if (DataGridView1.RowCount > 0)
			{
				((Control)ClipboardButton).Enabled = true;
				((Control)TestButton).Enabled = true;
			}
			else
			{
				((Control)ClipboardButton).Enabled = false;
				((Control)TestButton).Enabled = false;
			}
		}
		else
		{
			((Control)ClipboardButton).Enabled = false;
			((Control)DailyRadioButton).Enabled = false;
			((Control)DoneButton).Enabled = false;
			((Control)FromDatePicker).Enabled = false;
			((Control)HelpButton1).Enabled = false;
			((Control)MonthlyRadioButton).Enabled = false;
			((Control)PatternsButton).Enabled = false;
			((Control)ScoreAllPortfoliosButton).Enabled = false;
			((Control)StartButton).Enabled = false;
			((Control)StopButton).Enabled = true;
			((Control)StrictCheckBox).Enabled = false;
			((Control)SymbolTextBox).Enabled = false;
			((Control)TestButton).Enabled = false;
			((Control)ToDatePicker).Enabled = false;
			((Control)WeeklyRadioButton).Enabled = false;
		}
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void FindFlatBase(int StartIndex)
	{
		int chartStartIndex = GlobalForm.ChartStartIndex;
		int chartEndIndex = GlobalForm.ChartEndIndex;
		int patternCount = GlobalForm.PatternCount;
		GlobalForm.DisplayFmtns[] array;
		int num2;
		checked
		{
			array = new GlobalForm.DisplayFmtns[GlobalForm.PatternCount + 1];
			Array.Copy(GlobalForm.ChartPatterns, array, GlobalForm.PatternCount);
			GlobalForm.ChartStartIndex = Conversions.ToInteger(Interaction.IIf(StartIndex - 105 > 0, (object)(StartIndex - 105), (object)0));
			GlobalForm.ChartEndIndex = StartIndex;
			GlobalForm.PatternCount = 0;
			GlobalForm.ChartPatterns = null;
			FindPatterns.FindRectangles(102);
			if (GlobalForm.PatternCount > 0)
			{
				int num = GlobalForm.PatternCount - 1;
				num2 = 0;
				while (num2 <= num)
				{
					if (GlobalForm.ChartPatterns[num2].iEndDate - GlobalForm.ChartPatterns[num2].iStartDate < 63)
					{
						num2++;
						continue;
					}
					goto IL_00ad;
				}
			}
			GlobalForm.PatternCount = 0;
			GlobalForm.ChartPatterns = null;
			FindPatterns.FindRectangles(101);
			if (GlobalForm.PatternCount > 0)
			{
				int num3 = GlobalForm.PatternCount - 1;
				for (int i = 0; i <= num3; i++)
				{
					if (GlobalForm.ChartPatterns[i].iEndDate - GlobalForm.ChartPatterns[i].iStartDate >= 63)
					{
						Scores.qFlatBase = true;
						Scores.iFlatBaseStart = GlobalForm.ChartPatterns[i].iStartDate;
						Scores.iFlatBaseEnd = GlobalForm.ChartPatterns[i].iEndDate;
						break;
					}
				}
			}
			goto IL_01a7;
		}
		IL_01a7:
		GlobalForm.ChartStartIndex = chartStartIndex;
		GlobalForm.ChartEndIndex = chartEndIndex;
		GlobalForm.PatternCount = patternCount;
		GlobalForm.ChartPatterns = new GlobalForm.DisplayFmtns[checked(GlobalForm.PatternCount - 1 + 1)];
		Array.Copy(array, GlobalForm.ChartPatterns, GlobalForm.PatternCount);
		return;
		IL_00ad:
		Scores.qFlatBase = true;
		Scores.iFlatBaseStart = GlobalForm.ChartPatterns[num2].iStartDate;
		Scores.iFlatBaseEnd = GlobalForm.ChartPatterns[num2].iEndDate;
		goto IL_01a7;
	}

	private void FindHCR(int TsIndex, decimal BkoutPrice, int iPatternStart, int BkoutDirection)
	{
		bool flag = false;
		checked
		{
			if (BkoutDirection == 1)
			{
				int num = iPatternStart - 1;
				for (int i = TsIndex; i <= num; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[1, i], BkoutPrice) > 0)
					{
						flag = true;
						break;
					}
				}
				if (!flag)
				{
					Scores.qHCR = true;
					Scores.HCR = false;
					return;
				}
			}
			else
			{
				int num2 = iPatternStart - 1;
				for (int i = TsIndex; i <= num2; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[2, i], BkoutPrice) < 0)
					{
						flag = true;
						break;
					}
				}
				if (!flag)
				{
					Scores.qHCR = true;
					Scores.HCR = false;
					return;
				}
			}
			int num3 = iPatternStart - 1;
			decimal d3 = default(decimal);
			for (int i = TsIndex; i <= num3; i++)
			{
				int num4 = Conversions.ToInteger(Interaction.IIf(i + 10 < GlobalForm.HLCRange, (object)(i + 10), (object)(GlobalForm.HLCRange - 1)));
				int num5 = 0;
				int num6 = i;
				int num7 = num4;
				for (int j = num6; j <= num7; j++)
				{
					decimal d = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, j + 1]) > 0, (object)GlobalForm.nHLC[1, j], (object)GlobalForm.nHLC[1, j + 1]));
					decimal d2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, j + 1]) < 0, (object)GlobalForm.nHLC[2, j], (object)GlobalForm.nHLC[2, j + 1]));
					decimal num8 = decimal.Subtract(d, d2);
					if (decimal.Compare(num8, 0m) > 0)
					{
						d3 = default(decimal);
						if ((decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, j + 1]) <= 0) & (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, j + 1]) <= 0) & (decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[2, j + 1]) >= 0))
						{
							d3 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, j], GlobalForm.nHLC[2, j + 1]), num8);
						}
						else if ((decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, j + 1]) >= 0) & (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, j + 1]) >= 0) & (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[1, j + 1]) <= 0))
						{
							d3 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, j + 1], GlobalForm.nHLC[2, j]), num8);
						}
						else if ((decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, j + 1]) >= 0) & (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, j + 1]) <= 0))
						{
							d3 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, j + 1], GlobalForm.nHLC[2, j + 1]), num8);
						}
						else if ((decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, j + 1]) <= 0) & (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, j + 1]) >= 0))
						{
							d3 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, j], GlobalForm.nHLC[2, j]), num8);
						}
					}
					if (decimal.Compare(d3, 0.55m) >= 0)
					{
						num5++;
					}
					if (num5 >= 4)
					{
						break;
					}
				}
				if (num5 < 4)
				{
					continue;
				}
				decimal num9 = decimal.Divide(decimal.Add(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 2m);
				decimal num10 = decimal.Divide(decimal.Add(GlobalForm.nHLC[1, num4], GlobalForm.nHLC[2, num4]), 2m);
				decimal d4 = default(decimal);
				if (num4 - i != 0)
				{
					d4 = decimal.Divide(Math.Abs(decimal.Subtract(num10, num9)), new decimal(num4 - i));
				}
				if (decimal.Compare(d4, 0.03m) > 0)
				{
					continue;
				}
				if (BkoutDirection == 1)
				{
					if (decimal.Compare(decimal.Divide(decimal.Add(num9, num10), 2m), BkoutPrice) > 0)
					{
						Scores.qHCR = true;
						Scores.HCR = true;
						Scores.iHCRStart = i;
						Scores.iHCREnd = num4;
						return;
					}
				}
				else if (decimal.Compare(decimal.Divide(decimal.Add(num9, num10), 2m), BkoutPrice) < 0)
				{
					Scores.qHCR = true;
					Scores.HCR = true;
					Scores.iHCRStart = i;
					Scores.iHCREnd = num4;
					return;
				}
			}
			Scores.qHCR = true;
			Scores.HCR = false;
		}
	}

	private void FinnhubRB_CheckedChanged(object sender, EventArgs e)
	{
		if (FinnhubRB.Checked)
		{
			APIKeyTextBox.Text = GlobalForm.FinnhubKey;
		}
	}

	public void GetMarketCapScore(string Symbol)
	{
		WebRequest webRequest = null;
		string text = "marketCapitalization\":";
		checked
		{
			Symbol = Strings.Left(Symbol, Strings.InStrRev(Symbol, ".", -1, (CompareMethod)0) - 1);
			string text2 = null;
			StreamReader streamReader = null;
			Stream stream = null;
			WebResponse webResponse = null;
			ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
			try
			{
				if (FinnhubRB.Checked)
				{
					webRequest = WebRequest.CreateHttp(GlobalForm.FINNURL + "stock/profile2?symbol=" + Symbol + "&token=" + APIKeyTextBox.Text);
				}
				else if (IEXRadioButton.Checked)
				{
					webRequest = WebRequest.CreateHttp(GlobalForm.IEXURL + Symbol + "/stats/marketcap?token=" + GlobalForm.IEXKey);
				}
				webResponse = webRequest.GetResponse();
				stream = webResponse.GetResponseStream();
				streamReader = new StreamReader(stream);
				text2 = streamReader.ReadToEnd();
				streamReader.Close();
				stream.Close();
				webResponse.Close();
				double num2 = default(double);
				if (FinnhubRB.Checked)
				{
					int num = Strings.InStr(text2, text, (CompareMethod)0);
					num += text.Length - 1;
					text2 = Strings.Right(text2, text2.Length - num);
					num2 = Conversion.Val(Strings.Mid(text2, 1, Strings.InStr(text2, ",", (CompareMethod)0))) * 1000000.0;
				}
				else if (IEXRadioButton.Checked)
				{
					num2 = Conversion.Val(text2);
				}
				double num3 = num2;
				if (num3 < 1000000000.0)
				{
					Scores.MarketCap = "Small";
					Scores.sMarketCap = 1;
				}
				else if (num3 > 5000000000.0)
				{
					Scores.MarketCap = "Large";
					Scores.sMarketCap = -1;
				}
				else
				{
					Scores.MarketCap = "Mid";
					Scores.sMarketCap = 0;
				}
				Scores.qMarketCap = true;
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				if (Strings.InStr(ex2.Message, "401", (CompareMethod)0) != 0)
				{
					ErrorLabel.Text = "Error 401: Token is invalid.";
				}
				Scores.qMarketCap = false;
				streamReader?.Close();
				stream?.Close();
				webResponse?.Close();
				ProjectData.ClearProjectError();
			}
		}
	}

	private bool GetScore(int index, string Symbol)
	{
		int num = -1;
		string text = "";
		int num2 = -1;
		int num3 = -1;
		bool flag = false;
		int num4 = 1;
		float num5 = 0f;
		float num6 = 0f;
		long num7 = 0L;
		float num8 = 0f;
		long num9 = 0L;
		int num10 = 0;
		decimal d = default(decimal);
		decimal d2 = default(decimal);
		switch (GlobalForm.ChartPatterns[index].Type)
		{
		case 116:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0)
			{
				return true;
			}
			d = 0.1163m;
			text = "Down";
			break;
		case 115:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Down", false) == 0)
			{
				return true;
			}
			d2 = 0.115m;
			text = "Up";
			break;
		case 98:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Down", false) == 0)
			{
				return true;
			}
			d2 = 0.1414m;
			text = "Up";
			break;
		case 97:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0)
			{
				return true;
			}
			d = 0.1285m;
			text = "Down";
			break;
		case 94:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Down", false) == 0)
			{
				return true;
			}
			d2 = 0.142m;
			text = "Up";
			break;
		case 93:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Down", false) == 0)
			{
				return true;
			}
			d2 = 0.177m;
			text = "Up";
			break;
		case 108:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0)
			{
				return true;
			}
			d = 0.1603m;
			text = "Down";
			break;
		case 107:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0)
			{
				return true;
			}
			d = 0.1325m;
			text = "Down";
			break;
		case 102:
			d = 0.105m;
			d2 = 0.0906m;
			text = "Up";
			break;
		case 101:
			d = 0.0875m;
			d2 = 0.0914m;
			text = "Up";
			break;
		case 89:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Down", false) == 0)
			{
				return true;
			}
			d2 = 0.0978m;
			text = "Up";
			break;
		case 88:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0)
			{
				return true;
			}
			d = 0.1176m;
			text = "Down";
			break;
		case 86:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Down", false) == 0)
			{
				return true;
			}
			d2 = 0.1237m;
			text = "Up";
			break;
		case 85:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0)
			{
				return true;
			}
			d = 0.1293m;
			text = "Down";
			break;
		default:
			return true;
		}
		int iStartDate = GlobalForm.ChartPatterns[index].iStartDate;
		int iEndDate = GlobalForm.ChartPatterns[index].iEndDate;
		decimal num12;
		decimal num19 = default(decimal);
		bool flag3;
		DateTime dateTime;
		int num24;
		int hLCRange2;
		checked
		{
			int num11;
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDate, (string)null, false) == 0)
			{
				num11 = GlobalForm.HLCRange;
				num12 = GlobalForm.nHLC[3, GlobalForm.HLCRange];
				num = GlobalForm.HLCRange;
			}
			else
			{
				num12 = Conversions.ToDecimal(GlobalForm.CPInfo.BkoutPrice);
				num11 = -1;
				if (DateTime.Compare(GlobalForm.MyCDate(GlobalForm.CPInfo.BkoutDate).Date, GlobalForm.nDT[0, iEndDate].Date) < 0)
				{
					int num13 = iStartDate;
					for (int i = iEndDate; i >= num13; i += -1)
					{
						if (DateTime.Compare(GlobalForm.nDT[0, i].Date, GlobalForm.MyCDate(GlobalForm.CPInfo.BkoutDate).Date) <= 0)
						{
							num11 = i;
							num = i;
							break;
						}
					}
					if (num11 == -1)
					{
						num11 = iEndDate;
						num = num11;
					}
				}
				else
				{
					int hLCRange = GlobalForm.HLCRange;
					for (int i = iEndDate; i <= hLCRange; i++)
					{
						if (DateTime.Compare(GlobalForm.nDT[0, i].Date, GlobalForm.MyCDate(GlobalForm.CPInfo.BkoutDate).Date) >= 0)
						{
							num11 = i;
							num = i;
							break;
						}
					}
					if (num11 == -1)
					{
						num11 = iEndDate;
						num = num11;
					}
				}
			}
			bool flag2 = false;
			int num14 = 0;
			int num15 = default(int);
			int num16 = default(int);
			int num17 = default(int);
			int num18 = default(int);
			for (int i = num11; i >= 1; i += -1)
			{
				if (i == num11)
				{
					num15 = i - 1;
					num16 = i - 1;
					if (num11 == num)
					{
						Scores.qBkoutGap = true;
						if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0)
						{
							if (decimal.Compare(GlobalForm.nHLC[2, num11], GlobalForm.nHLC[1, num11 - 1]) > 0)
							{
								Scores.BkoutGap = true;
							}
						}
						else if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Down", false) == 0 && decimal.Compare(GlobalForm.nHLC[2, num11 - 1], GlobalForm.nHLC[1, num11]) > 0)
						{
							Scores.BkoutGap = true;
						}
					}
				}
				if (i >= iEndDate)
				{
					num17 = i;
					num18 = i;
					num19 = decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]);
					num14 = 1;
				}
				else if (unchecked(i >= iStartDate && i < iEndDate))
				{
					float num20 = Convert.ToSingle(GlobalForm.nHLC[4, i]);
					num7 += num4;
					num8 += num20;
					num5 += (float)(num4 * num4);
					num6 += (float)num4 * num20;
					num4++;
					if (i == iStartDate)
					{
						int num21 = num4 - 1;
						if ((float)num21 * num5 - (float)(num7 * num7) != 0f)
						{
							if (((float)num21 * num6 - (float)num7 * num8) / ((float)num21 * num5 - (float)(num7 * num7)) > 0f)
							{
								Scores.Volume = -1;
							}
							else
							{
								Scores.Volume = 1;
							}
							Scores.qVolume = true;
						}
					}
					num19 = decimal.Add(num19, decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]));
					num14++;
					if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num17]) > 0)
					{
						num17 = i;
					}
					if ((decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num18]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i], 0m) != 0))
					{
						num18 = i;
					}
					if (i != iStartDate)
					{
						continue;
					}
					if ((Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0) | ((Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, (string)null, false) == 0) & (Operators.CompareString(text, "Up", false) == 0)))
					{
						if (decimal.Compare(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num17], GlobalForm.nHLC[2, num18]), num12), d2) > 0)
						{
							Scores.Tall = true;
							Scores.qHeight = true;
						}
						else
						{
							Scores.qHeight = true;
						}
					}
					else if ((Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Down", false) == 0) | ((Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, (string)null, false) == 0) & (Operators.CompareString(text, "Down", false) == 0)))
					{
						if (decimal.Compare(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num17], GlobalForm.nHLC[2, num18]), num12), d) > 0)
						{
							Scores.Tall = true;
							Scores.qHeight = true;
						}
						else
						{
							Scores.qHeight = true;
						}
					}
				}
				else
				{
					if (i >= iStartDate)
					{
						continue;
					}
					if (!flag2 && i < iStartDate - 10)
					{
						if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[2, num18]) < 0)
						{
							num2 = iStartDate - 1;
							for (int j = iStartDate - 1; j >= 0; j += -1)
							{
								if (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num2]) < 0)
								{
									num2 = j;
								}
								if (unchecked(Convert.ToDouble(GlobalForm.nHLC[3, j]) >= Convert.ToDouble(GlobalForm.nHLC[2, num2]) * 1.2 && j != num2) | ((double)DateAndTime.DateDiff((DateInterval)4, GlobalForm.nDT[0, j], GlobalForm.nDT[0, iStartDate], (FirstDayOfWeek)1, (FirstWeekOfYear)1) > 182.5))
								{
									long num22 = DateAndTime.DateDiff((DateInterval)4, GlobalForm.nDT[0, num2], GlobalForm.nDT[0, iStartDate], (FirstDayOfWeek)1, (FirstWeekOfYear)1);
									if ((double)num22 < 91.25)
									{
										Scores.qTrendStart = true;
										Scores.TrendStart = "Short";
										Scores.iTs = num2;
									}
									else if ((double)num22 >= 182.5)
									{
										Scores.qTrendStart = true;
										Scores.TrendStart = "Long";
										Scores.iTs = num2;
									}
									else
									{
										Scores.qTrendStart = true;
										Scores.TrendStart = "Intermediate";
										Scores.iTs = num2;
									}
									FindHCR(num2, num12, iStartDate, Conversions.ToInteger(Interaction.IIf(Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0, (object)1, (object)(-1))));
									flag2 = true;
									break;
								}
							}
						}
						else if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[1, num17]) > 0)
						{
							num3 = iStartDate - 1;
							for (int j = iStartDate - 1; j >= 0; j += -1)
							{
								if (decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, num3]) > 0)
								{
									num3 = j;
								}
								if (unchecked(Convert.ToDouble(GlobalForm.nHLC[3, j]) <= Convert.ToDouble(GlobalForm.nHLC[1, num3]) * 0.8 && j != num3) | ((double)DateAndTime.DateDiff((DateInterval)4, GlobalForm.nDT[0, j], GlobalForm.nDT[0, iStartDate], (FirstDayOfWeek)1, (FirstWeekOfYear)1) > 182.5))
								{
									long num23 = DateAndTime.DateDiff((DateInterval)4, GlobalForm.nDT[0, num3], GlobalForm.nDT[0, iStartDate], (FirstDayOfWeek)1, (FirstWeekOfYear)1);
									if ((double)num23 < 91.25)
									{
										Scores.qTrendStart = true;
										Scores.TrendStart = "Short";
										Scores.iTs = num3;
									}
									else if ((double)num23 >= 182.5)
									{
										Scores.qTrendStart = true;
										Scores.TrendStart = "Long";
										Scores.iTs = num3;
									}
									else
									{
										Scores.qTrendStart = true;
										Scores.TrendStart = "Intermediate";
										Scores.iTs = num3;
									}
									FindHCR(num3, num12, iStartDate, Conversions.ToInteger(Interaction.IIf(Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0, (object)1, (object)(-1))));
									flag2 = true;
									break;
								}
							}
						}
					}
					if (!flag2 && (double)DateAndTime.DateDiff((DateInterval)4, GlobalForm.nDT[0, i], GlobalForm.nDT[0, iStartDate], (FirstDayOfWeek)1, (FirstWeekOfYear)1) > 182.5)
					{
						Scores.qTrendStart = true;
						Scores.iTs = -1;
						Scores.TrendStart = "Long";
						FindHCR(i, num12, iStartDate, Conversions.ToInteger(Interaction.IIf(Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0, (object)1, (object)(-1))));
						flag2 = true;
					}
					if (!flag)
					{
						if ((double)DateAndTime.DateDiff((DateInterval)4, GlobalForm.nDT[0, i], GlobalForm.nDT[0, num - 1], (FirstDayOfWeek)1, (FirstWeekOfYear)1) > 91.25)
						{
							if (num10 > 0)
							{
								if (Convert.ToDouble(GlobalForm.nHLC[4, num]) > 1.25 * (double)num9 / (double)num10)
								{
									Scores.BkoutVol = "Heavy";
								}
								else
								{
									Scores.BkoutVol = "Light";
								}
								Scores.qBkoutVol = true;
							}
							flag = true;
						}
						else
						{
							num9 += Convert.ToInt64(GlobalForm.nHLC[4, i]);
							num10++;
						}
					}
					if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num15]) > 0)
					{
						num15 = i;
					}
					if (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num16]) < 0)
					{
						num16 = i;
					}
					if (DateAndTime.DateDiff((DateInterval)4, GlobalForm.nDT[0, i], GlobalForm.nDT[0, num], (FirstDayOfWeek)1, (FirstWeekOfYear)1) >= 365)
					{
						if (decimal.Compare(num12, decimal.Subtract(GlobalForm.nHLC[1, num15], decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num15], GlobalForm.nHLC[2, num16]), 3m))) >= 0)
						{
							Scores.YrlyRange = "High";
							Scores.qYrlyRange = true;
						}
						else if (decimal.Compare(num12, decimal.Add(GlobalForm.nHLC[2, num16], decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num15], GlobalForm.nHLC[2, num16]), 3m))) <= 0)
						{
							Scores.YrlyRange = "Low";
							Scores.qYrlyRange = true;
						}
						else
						{
							Scores.YrlyRange = "Middle";
							Scores.qYrlyRange = true;
						}
						break;
					}
				}
			}
			if (num14 != 0)
			{
				num19 = decimal.Divide(num19, new decimal(num14));
				num19 = decimal.Divide(num19, 2m);
			}
			flag3 = false;
			dateTime = DateAndTime.DateAdd((DateInterval)4, 32.0, GlobalForm.nDT[0, num]);
			num24 = num11;
			hLCRange2 = GlobalForm.HLCRange;
		}
		int num25 = default(int);
		for (int i = num24; i <= hLCRange2; i = checked(i + 1))
		{
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0)
			{
				if (!flag3 & (decimal.Compare(GlobalForm.nHLC[2, i], decimal.Add(num12, num19)) > 0))
				{
					num25 = i;
					flag3 = true;
				}
				if (flag3 && i != num25)
				{
					Scores.qThrowPull = true;
					if (decimal.Compare(GlobalForm.nHLC[2, i], decimal.Add(num12, num19)) <= 0)
					{
						Scores.ThrowPull = true;
						break;
					}
				}
			}
			else
			{
				if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Down", false) != 0)
				{
					break;
				}
				if (!flag3 & (decimal.Compare(GlobalForm.nHLC[1, i], decimal.Subtract(num12, num19)) < 0))
				{
					num25 = i;
					flag3 = true;
				}
				if (flag3 && i != num25)
				{
					Scores.qThrowPull = true;
					if (decimal.Compare(GlobalForm.nHLC[1, i], decimal.Subtract(num12, num19)) >= 0)
					{
						Scores.ThrowPull = true;
						break;
					}
				}
			}
			if (DateTime.Compare(GlobalForm.nDT[0, i].Date, dateTime.Date) >= 0)
			{
				break;
			}
		}
		FindFlatBase(iStartDate);
		TabulateScores(index, Symbol);
		return false;
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.HelpScoreForm).ShowDialog();
	}

	private void IEXRadioButton_CheckedChanged(object sender, EventArgs e)
	{
		if (IEXRadioButton.Checked)
		{
			APIKeyTextBox.Text = GlobalForm.IEXKey;
			((Control)LinkLabel1).Visible = true;
		}
		else
		{
			((Control)LinkLabel1).Visible = false;
		}
	}

	private void ScoreAllPortfoliosButton_Click_1(object sender, EventArgs e)
	{
		//IL_0140: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			if (MyProject.Forms.Mainform.PortfolioDataGridView.RowCount > 0)
			{
				GlobalForm.Quiet = true;
				string openPath = GlobalForm.OpenPath;
				DataGridView1.RowCount = 0;
				int num = MyProject.Forms.Mainform.PortfolioDataGridView.RowCount - 1;
				for (int i = 0; i <= num; i++)
				{
					GlobalForm.OpenPath = MyProject.Forms.Mainform.PortfolioDataGridView.Rows[i].Cells[1].Value.ToString();
					MyProject.Forms.Mainform.MFDisplayFiles(BrowseFlag: false);
					MyProject.Forms.Mainform.AllButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
					StartButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
					if (StopPressed)
					{
						break;
					}
				}
				GlobalForm.OpenPath = openPath;
				MyProject.Forms.Mainform.MFDisplayFiles(BrowseFlag: false);
				GlobalForm.Quiet = false;
				try
				{
					if (ErrorLabel.Text.Length > 0)
					{
						Clipboard.SetText(ErrorLabel.Text);
						ErrorLabel.Text = "Error messages are on the clipboard.";
					}
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					ProjectData.ClearProjectError();
				}
				FilenameLabel.Text = "We're done, boss!";
				MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				ProgressBar1.Value = 0;
			}
			else
			{
				StartButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			}
		}
	}

	private void PatternsButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.PatternsForm).ShowDialog();
	}

	private void ProcessSymbol()
	{
		//IL_002c: Unknown result type (might be due to invalid IL or missing references)
		if (Regex.Split(Strings.Trim(SymbolTextBox.Text), " ").Length > 1)
		{
			MessageBox.Show("Only one symbol is allowed in the Symbol text box.", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)64);
			((Control)SymbolTextBox).Focus();
			return;
		}
		string text = Strings.Trim(SymbolTextBox.Text);
		if (Strings.InStr(text, ".", (CompareMethod)0) == 0)
		{
			string text2 = text + ".csv";
			if (!File.Exists(GlobalForm.OpenPath + "\\" + text2))
			{
				text2 = text + ".txt";
			}
			text = text2;
		}
		string fileName = text;
		ProgressBar ProgBar = null;
		Label ErrorLabel = this.ErrorLabel;
		bool num = GlobalForm.LoadFile(fileName, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
		this.ErrorLabel = ErrorLabel;
		if (!num)
		{
			GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
			bool showCandles = GlobalForm.ShowCandles;
			GlobalForm.ShowCandles = false;
			FindPatterns.EnterFindPatterns(GlobalForm.ChartStart, GlobalForm.ChartEnd, null, ref StopPressed, 3);
			GlobalForm.ShowCandles = showCandles;
			if (GlobalForm.PatternCount > 0)
			{
				BuildGrid(text);
			}
		}
	}

	private void StartButton_Click(object sender, EventArgs e)
	{
		//IL_003b: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d9: Unknown result type (might be due to invalid IL or missing references)
		if (!GlobalForm.Quiet && Strings.Trim(APIKeyTextBox.Text).Length == 0)
		{
			ErrorLabel.Text = "API key/token missing.";
			MessageBox.Show("To use this form, you need a quote vendor token!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			((Control)APIKeyTextBox).Focus();
			return;
		}
		DateTimePicker fromDatePicker = FromDatePicker;
		DateTime FromDate = fromDatePicker.Value;
		DateTimePicker toDatePicker;
		DateTime ToDate = (toDatePicker = ToDatePicker).Value;
		GlobalForm.SwapDates(ref FromDate, ref ToDate);
		toDatePicker.Value = ToDate;
		fromDatePicker.Value = FromDate;
		if (!GlobalForm.Quiet)
		{
			StopPressed = false;
		}
		DisableEnable(EnableFlag: false);
		GlobalForm.HideMessages = true;
		if (!GlobalForm.Quiet)
		{
			ErrorLabel.Text = "";
		}
		BuildList();
		GlobalForm.HideMessages = false;
		DisableEnable(EnableFlag: true);
		if (!GlobalForm.Quiet)
		{
			MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			ProgressBar1.Value = 0;
		}
	}

	private void StopButton_Click(object sender, EventArgs e)
	{
		StopPressed = true;
		Interaction.Beep();
	}

	private void StrictCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		GlobalForm.StrictPatterns = StrictCheckBox.Checked;
	}

	private void TabulateScores(int index, string Symbol)
	{
		Scores.sFlatBase = Conversions.ToInteger(Interaction.IIf(Scores.qFlatBase, (object)1, (object)(-1)));
		Scores.sHCR = Conversions.ToInteger(Interaction.IIf(Scores.HCR, (object)(-1), (object)1));
		switch (GlobalForm.ChartPatterns[index].Type)
		{
		case 116:
			if (Operators.CompareString(Scores.TrendStart, "Long", false) == 0)
			{
				Scores.sTrendStart = -1;
			}
			else
			{
				Scores.sTrendStart = 1;
			}
			switch (Scores.YrlyRange)
			{
			case "Low":
				Scores.sYrlyRange = 1;
				break;
			case "Middle":
				Scores.sYrlyRange = 1;
				break;
			case "High":
				Scores.sYrlyRange = -1;
				break;
			}
			Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
			Scores.sVolume = 0;
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)(-1), (object)0));
			if (Scores.qThrowPull)
			{
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
			}
			else
			{
				Scores.sThrowPull = -1;
			}
			if (Scores.qBkoutGap)
			{
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.BkoutGap, (object)1, (object)0));
			}
			else
			{
				Scores.sBkoutGap = 0;
			}
			break;
		case 115:
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf((Operators.CompareString(Scores.TrendStart, "Short", false) == 0) | (Operators.CompareString(Scores.TrendStart, "Long", false) == 0), (object)1, (object)(-1)));
			switch (Scores.YrlyRange)
			{
			case "Low":
				Scores.sYrlyRange = 1;
				break;
			case "Middle":
				Scores.sYrlyRange = -1;
				break;
			case "High":
				Scores.sYrlyRange = -1;
				break;
			}
			Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
			Scores.sVolume = Conversions.ToInteger(Interaction.IIf(Scores.Volume == 1, (object)(-1), (object)1));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)(-1), (object)1));
			if (Scores.qThrowPull)
			{
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
			}
			else
			{
				Scores.sThrowPull = -1;
			}
			if (Scores.qBkoutGap)
			{
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.BkoutGap, (object)(-1), (object)0));
			}
			else
			{
				Scores.sBkoutGap = 0;
			}
			break;
		case 98:
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.TrendStart, "Short", false) == 0, (object)1, (object)(-1)));
			switch (Scores.YrlyRange)
			{
			case "Low":
				Scores.sYrlyRange = 1;
				break;
			case "Middle":
				Scores.sYrlyRange = 0;
				break;
			case "High":
				Scores.sYrlyRange = -1;
				break;
			}
			Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
			Scores.sVolume = Conversions.ToInteger(Interaction.IIf(Scores.Volume == 1, (object)(-1), (object)0));
			Scores.sBkoutVol = 0;
			if (Scores.qThrowPull)
			{
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
			}
			else
			{
				Scores.sThrowPull = -1;
			}
			if (Scores.qBkoutGap)
			{
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.BkoutGap, (object)1, (object)(-1)));
			}
			else
			{
				Scores.sBkoutGap = -1;
			}
			break;
		case 97:
			if (Operators.CompareString(Scores.TrendStart, "Short", false) == 0)
			{
				Scores.sTrendStart = 1;
			}
			else if (Operators.CompareString(Scores.TrendStart, "Long", false) == 0)
			{
				Scores.sTrendStart = -1;
			}
			else
			{
				Scores.sTrendStart = 0;
			}
			switch (Scores.YrlyRange)
			{
			case "Low":
				Scores.sYrlyRange = 0;
				break;
			case "Middle":
				Scores.sYrlyRange = 0;
				break;
			case "High":
				Scores.sYrlyRange = -1;
				break;
			}
			Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
			Scores.sVolume = Conversions.ToInteger(Interaction.IIf(Scores.Volume == 1, (object)0, (object)(-1)));
			Scores.sBkoutVol = 0;
			if (Scores.qThrowPull)
			{
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
			}
			else
			{
				Scores.sThrowPull = -1;
			}
			Scores.sBkoutGap = 0;
			break;
		case 94:
			if (Operators.CompareString(Scores.TrendStart, "Short", false) == 0)
			{
				Scores.sTrendStart = 1;
			}
			else if (Operators.CompareString(Scores.TrendStart, "Long", false) == 0)
			{
				Scores.sTrendStart = -1;
			}
			else
			{
				Scores.sTrendStart = 0;
			}
			switch (Scores.YrlyRange)
			{
			case "Low":
				Scores.sYrlyRange = 1;
				break;
			case "Middle":
				Scores.sYrlyRange = -1;
				break;
			case "High":
				Scores.sYrlyRange = -1;
				break;
			}
			Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
			Scores.sVolume = 0;
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)(-1), (object)1));
			if (Scores.qThrowPull)
			{
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
			}
			else
			{
				Scores.sThrowPull = -1;
			}
			Scores.sBkoutGap = 0;
			break;
		case 93:
			if (Operators.CompareString(Scores.TrendStart, "Short", false) == 0)
			{
				Scores.sTrendStart = 0;
			}
			else if (Operators.CompareString(Scores.TrendStart, "Long", false) == 0)
			{
				Scores.sTrendStart = -1;
			}
			else
			{
				Scores.sTrendStart = 1;
			}
			switch (Scores.YrlyRange)
			{
			case "Low":
				Scores.sYrlyRange = -1;
				break;
			case "Middle":
				Scores.sYrlyRange = 1;
				break;
			case "High":
				Scores.sYrlyRange = -1;
				break;
			}
			Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)0));
			Scores.sVolume = Conversions.ToInteger(Interaction.IIf(Scores.Volume == 1, (object)1, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)(-1), (object)1));
			if (Scores.qThrowPull)
			{
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
			}
			else
			{
				Scores.sThrowPull = -1;
			}
			Scores.sBkoutGap = 0;
			break;
		case 108:
			if (Operators.CompareString(Scores.TrendStart, "Short", false) == 0)
			{
				Scores.sTrendStart = 1;
			}
			else
			{
				Scores.sTrendStart = -1;
			}
			switch (Scores.YrlyRange)
			{
			case "Low":
				Scores.sYrlyRange = 1;
				break;
			case "Middle":
				Scores.sYrlyRange = 0;
				break;
			case "High":
				Scores.sYrlyRange = 0;
				break;
			}
			Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
			Scores.sVolume = Conversions.ToInteger(Interaction.IIf(Scores.Volume == 1, (object)1, (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)0, (object)1));
			if (Scores.qThrowPull)
			{
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
			}
			else
			{
				Scores.sThrowPull = -1;
			}
			if (Scores.qBkoutGap)
			{
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.BkoutGap, (object)1, (object)0));
			}
			else
			{
				Scores.sBkoutGap = 0;
			}
			break;
		case 107:
			if (Operators.CompareString(Scores.TrendStart, "Long", false) == 0)
			{
				Scores.sTrendStart = -1;
			}
			else if (Operators.CompareString(Scores.TrendStart, "Short", false) == 0)
			{
				Scores.sTrendStart = 1;
			}
			else
			{
				Scores.sTrendStart = 1;
			}
			switch (Scores.YrlyRange)
			{
			case "Low":
				Scores.sYrlyRange = 0;
				break;
			case "Middle":
				Scores.sYrlyRange = 1;
				break;
			case "High":
				Scores.sYrlyRange = -1;
				break;
			}
			Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
			Scores.sVolume = 0;
			Scores.sBkoutVol = 0;
			if (Scores.qThrowPull)
			{
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
			}
			else
			{
				Scores.sThrowPull = -1;
			}
			Scores.sBkoutGap = 0;
			break;
		case 102:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0)
			{
				if (Operators.CompareString(Scores.TrendStart, "Long", false) == 0)
				{
					Scores.sTrendStart = -1;
				}
				else if (Operators.CompareString(Scores.TrendStart, "Short", false) == 0)
				{
					Scores.sTrendStart = 1;
				}
				else
				{
					Scores.sTrendStart = 1;
				}
				switch (Scores.YrlyRange)
				{
				case "Low":
					Scores.sYrlyRange = 1;
					break;
				case "Middle":
					Scores.sYrlyRange = 1;
					break;
				case "High":
					Scores.sYrlyRange = -1;
					break;
				}
				Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
				Scores.sVolume = Conversions.ToInteger(Interaction.IIf(Scores.Volume == 1, (object)1, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)(-1), (object)0));
				if (Scores.qThrowPull)
				{
					Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
				}
				else
				{
					Scores.sThrowPull = -1;
				}
				if (Scores.qBkoutGap)
				{
					Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.BkoutGap, (object)(-1), (object)0));
				}
				else
				{
					Scores.sBkoutGap = 0;
				}
			}
			else
			{
				if (Operators.CompareString(Scores.TrendStart, "Long", false) == 0)
				{
					Scores.sTrendStart = -1;
				}
				else if (Operators.CompareString(Scores.TrendStart, "Short", false) == 0)
				{
					Scores.sTrendStart = 0;
				}
				else
				{
					Scores.sTrendStart = 1;
				}
				switch (Scores.YrlyRange)
				{
				case "Low":
					Scores.sYrlyRange = 1;
					break;
				case "Middle":
					Scores.sYrlyRange = -1;
					break;
				case "High":
					Scores.sYrlyRange = -1;
					break;
				}
				Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
				Scores.sVolume = Conversions.ToInteger(Interaction.IIf(Scores.Volume == 1, (object)1, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)1, (object)0));
				if (Scores.qThrowPull)
				{
					Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
				}
				else
				{
					Scores.sThrowPull = -1;
				}
				Scores.sBkoutGap = 0;
			}
			break;
		case 101:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.TrendStart, "Short", false) == 0, (object)1, (object)(-1)));
				switch (Scores.YrlyRange)
				{
				case "Low":
					Scores.sYrlyRange = 1;
					break;
				case "Middle":
					Scores.sYrlyRange = -1;
					break;
				case "High":
					Scores.sYrlyRange = 1;
					break;
				}
				Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
				Scores.sVolume = Conversions.ToInteger(Interaction.IIf(Scores.Volume == 1, (object)1, (object)0));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)(-1), (object)1));
				if (Scores.qThrowPull)
				{
					Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
				}
				else
				{
					Scores.sThrowPull = -1;
				}
				if (Scores.qBkoutGap)
				{
					Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.BkoutGap, (object)(-1), (object)1));
				}
				else
				{
					Scores.sBkoutGap = 1;
				}
				break;
			}
			if (Operators.CompareString(Scores.TrendStart, "Short", false) == 0)
			{
				Scores.sTrendStart = 1;
			}
			else
			{
				Scores.sTrendStart = -1;
			}
			switch (Scores.YrlyRange)
			{
			case "Low":
				Scores.sYrlyRange = 1;
				break;
			case "Middle":
				Scores.sYrlyRange = 1;
				break;
			case "High":
				Scores.sYrlyRange = -1;
				break;
			}
			Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
			Scores.sVolume = 0;
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)(-1), (object)1));
			if (Scores.qThrowPull)
			{
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)0, (object)1));
			}
			else
			{
				Scores.sThrowPull = 0;
			}
			if (Scores.qBkoutGap)
			{
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.BkoutGap, (object)(-1), (object)0));
			}
			else
			{
				Scores.sBkoutGap = 0;
			}
			break;
		case 89:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.TrendStart, "Long", false) == 0, (object)(-1), (object)1));
				switch (Scores.YrlyRange)
				{
				case "Low":
					Scores.sYrlyRange = -1;
					break;
				case "Middle":
					Scores.sYrlyRange = -1;
					break;
				case "High":
					Scores.sYrlyRange = 1;
					break;
				}
				Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
				Scores.sVolume = Conversions.ToInteger(Interaction.IIf(Scores.Volume == 1, (object)1, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)(-1), (object)1));
				if (Scores.qThrowPull)
				{
					Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
				}
				else
				{
					Scores.sThrowPull = -1;
				}
				Scores.sBkoutGap = 0;
				break;
			}
			if (Operators.CompareString(Scores.TrendStart, "Short", false) == 0)
			{
				Scores.sTrendStart = 1;
			}
			else if (Operators.CompareString(Scores.TrendStart, "Long", false) == 0)
			{
				Scores.sTrendStart = -1;
			}
			else
			{
				Scores.sTrendStart = 0;
			}
			switch (Scores.YrlyRange)
			{
			case "Low":
				Scores.sYrlyRange = 1;
				break;
			case "Middle":
				Scores.sYrlyRange = 1;
				break;
			case "High":
				Scores.sYrlyRange = -1;
				break;
			}
			Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
			Scores.sVolume = Conversions.ToInteger(Interaction.IIf(Scores.Volume == 1, (object)(-1), (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)(-1), (object)1));
			if (Scores.qThrowPull)
			{
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
			}
			else
			{
				Scores.sThrowPull = -1;
			}
			Scores.sBkoutGap = 0;
			break;
		case 88:
			if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.TrendStart, "Long", false) == 0, (object)(-1), (object)1));
				switch (Scores.YrlyRange)
				{
				case "Low":
					Scores.sYrlyRange = 1;
					break;
				case "Middle":
					Scores.sYrlyRange = -1;
					break;
				case "High":
					Scores.sYrlyRange = 0;
					break;
				}
				Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
				Scores.sVolume = Conversions.ToInteger(Interaction.IIf(Scores.Volume == 1, (object)(-1), (object)0));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)(-1), (object)1));
				if (Scores.qThrowPull)
				{
					Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
				}
				else
				{
					Scores.sThrowPull = -1;
				}
				if (Scores.qBkoutGap)
				{
					Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.BkoutGap, (object)1, (object)(-1)));
				}
				else
				{
					Scores.sBkoutGap = -1;
				}
				break;
			}
			if (Operators.CompareString(Scores.TrendStart, "Long", false) == 0)
			{
				Scores.sTrendStart = -1;
			}
			else
			{
				Scores.sTrendStart = 1;
			}
			switch (Scores.YrlyRange)
			{
			case "Low":
				Scores.sYrlyRange = 1;
				break;
			case "Middle":
				Scores.sYrlyRange = 0;
				break;
			case "High":
				Scores.sYrlyRange = -1;
				break;
			}
			Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
			Scores.sVolume = Conversions.ToInteger(Interaction.IIf(Scores.Volume == 1, (object)(-1), (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)(-1), (object)1));
			if (Scores.qThrowPull)
			{
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
			}
			else
			{
				Scores.sThrowPull = -1;
			}
			if (Scores.qBkoutGap)
			{
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.BkoutGap, (object)1, (object)0));
			}
			else
			{
				Scores.sBkoutGap = 0;
			}
			break;
		case 86:
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.TrendStart, "Short", false) == 0, (object)1, (object)(-1)));
			switch (Scores.YrlyRange)
			{
			case "Low":
				Scores.sYrlyRange = 1;
				break;
			case "Middle":
				Scores.sYrlyRange = 1;
				break;
			case "High":
				Scores.sYrlyRange = -1;
				break;
			}
			Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
			Scores.sVolume = Conversions.ToInteger(Interaction.IIf(Scores.Volume == 1, (object)(-1), (object)1));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Operators.CompareString(Scores.BkoutVol, "Light", false) == 0, (object)(-1), (object)1));
			if (Scores.qThrowPull)
			{
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
			}
			else
			{
				Scores.sThrowPull = -1;
			}
			if (Scores.qBkoutGap)
			{
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.BkoutGap, (object)1, (object)0));
			}
			else
			{
				Scores.sBkoutGap = 0;
			}
			break;
		case 85:
			if (Operators.CompareString(Scores.TrendStart, "Long", false) == 0)
			{
				Scores.sTrendStart = -1;
			}
			else if (Operators.CompareString(Scores.TrendStart, "Short", false) == 0)
			{
				Scores.sTrendStart = 1;
			}
			else
			{
				Scores.sTrendStart = 0;
			}
			switch (Scores.YrlyRange)
			{
			case "Low":
				Scores.sYrlyRange = 1;
				break;
			case "Middle":
				Scores.sYrlyRange = 0;
				break;
			case "High":
				Scores.sYrlyRange = 0;
				break;
			}
			Scores.sHeight = Conversions.ToInteger(Interaction.IIf(Scores.Tall, (object)1, (object)(-1)));
			Scores.sVolume = 0;
			Scores.sBkoutVol = 0;
			if (Scores.qThrowPull)
			{
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.ThrowPull, (object)(-1), (object)1));
			}
			else
			{
				Scores.sThrowPull = -1;
			}
			if (Scores.qBkoutGap)
			{
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.BkoutGap, (object)1, (object)0));
			}
			else
			{
				Scores.sBkoutGap = 0;
			}
			break;
		}
	}

	private void TestButton_Click(object sender, EventArgs e)
	{
		//IL_0395: Unknown result type (might be due to invalid IL or missing references)
		//IL_03ab: Unknown result type (might be due to invalid IL or missing references)
		decimal[,,] array = new decimal[2, 21, 2];
		checked
		{
			int num = DataGridView1.RowCount - 1;
			int i;
			string text2;
			for (i = 0; i <= num; i++)
			{
				string text = DataGridView1.Rows[i].Cells[17].Value.ToString();
				int num2 = ((Operators.CompareString(text, "Up", false) == 0) ? 1 : ((Operators.CompareString(text, "Down", false) == 0) ? (-1) : 0));
				try
				{
					int num3 = 10 + Conversions.ToInteger(DataGridView1.Rows[i].Cells[2].Value);
					text2 = Strings.Trim(DataGridView1.Rows[i].Cells[3].Value.ToString());
					if (Operators.CompareString(text2, "?", false) != 0)
					{
						switch (num2)
						{
						case 1:
						{
							ref decimal reference3 = ref array[1, num3, 0];
							reference3 = decimal.Add(reference3, new decimal(double.Parse(text2.TrimEnd(new char[1] { '%' })) / 100.0));
							ref decimal reference4 = ref array[1, num3, 1];
							reference4 = decimal.Add(reference4, 1m);
							break;
						}
						case -1:
						{
							ref decimal reference = ref array[0, num3, 0];
							reference = decimal.Add(reference, new decimal(double.Parse(text2.TrimEnd(new char[1] { '%' })) / 100.0));
							ref decimal reference2 = ref array[0, num3, 1];
							reference2 = decimal.Add(reference2, 1m);
							break;
						}
						}
					}
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					ProjectData.ClearProjectError();
				}
			}
			text2 = "On average, patterns with scores above 0 tend to perform better than do those with scores below 0. Generally, the lower the number (10 is best, -10 is worst), the worse the performance. Sample counts more than 30 tend to be reliable.\r\n\r\n";
			text2 += "Use this information to gauge how well the scoring system works for your markets. Be sure to score as many stocks as possible to get accurate results.\r\n\r\nThe gains represent PERFECT TRADES, so your actual trading results will vary. Past performance doesn't guarantee future results. You alone are responsible for your investment decisions.\r\n\r\nThis information has been pasted onto the clipboard.";
			text2 += "\r\n\r\nUp breakouts\t\tDown breakouts\r\nScore\tGain\tSamples\tScore\tGain\tSamples\r\n";
			i = 20;
			do
			{
				int num4 = Convert.ToInt32(array[1, i, 1]);
				text2 = ((num4 == 0) ? (text2 + Strings.Format((object)(i - 10), "") + "\t0\t0\t") : (text2 + Strings.Format((object)(i - 10), "") + "\t" + Strings.Format((object)decimal.Divide(array[1, i, 0], new decimal(num4)), "0.0%") + "\t" + Strings.Format((object)array[1, i, 1], "") + "\t"));
				num4 = Convert.ToInt32(array[0, i, 1]);
				text2 = ((num4 == 0) ? (text2 + Strings.Format((object)(i - 10), "") + "\t0\t0\r\n") : (text2 + Strings.Format((object)(i - 10), "") + "\t" + Strings.Format((object)decimal.Divide(array[0, i, 0], new decimal(num4)), "0.0%") + "\t" + Strings.Format((object)array[0, i, 1], "") + "\r\n"));
				i += -1;
			}
			while (i >= 0);
			try
			{
				Clipboard.SetText(text2);
			}
			catch (Exception ex3)
			{
				ProjectData.SetProjectError(ex3);
				Exception ex4 = ex3;
				MessageBox.Show("Clipboard is busy with another user. Error: " + ex4.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				ProjectData.ClearProjectError();
			}
			MessageBox.Show(text2, "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
	}

	private void LinkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
	{
		LinkLabel1.LinkVisited = true;
		Process.Start("https://iexcloud.io");
	}
}
