using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Microsoft.VisualBasic.Devices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class ForecastForm : Form
{
	public struct Setting
	{
		public int Rules;

		public int DWM;
	}

	public struct SigStruct
	{
		public int Move;

		public int iTurnStart;

		public int iTurnEnd;

		public decimal Price;

		public int iTrendEnd;
	}

	public struct ResetStruct
	{
		public DateTime ChartStart;

		public DateTime ChartEnd;

		public DateTime PatStart;

		public DateTime PatEnd;

		public string Symbol;

		public string sFilename;

		public int Predict;

		public bool Intraday;

		public int DYMSetting;
	}

	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("Chart1")]
	private Chart _Chart1;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StartButton")]
	private Button _StartButton;

	[CompilerGenerated]
	[AccessedThroughProperty("HelpButton1")]
	private Button _HelpButton1;

	[CompilerGenerated]
	[AccessedThroughProperty("ClipboardButton")]
	private Button _ClipboardButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StopButton")]
	private Button _StopButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ResultsGrid")]
	private DataGridView _ResultsGrid;

	[CompilerGenerated]
	[AccessedThroughProperty("GraphButton")]
	private Button _GraphButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PatternToPicker")]
	private DateTimePicker _PatternToPicker;

	[CompilerGenerated]
	[AccessedThroughProperty("PatternFromPicker")]
	private DateTimePicker _PatternFromPicker;

	[CompilerGenerated]
	[AccessedThroughProperty("ResultsButton")]
	private Button _ResultsButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PreviewButton")]
	private Button _PreviewButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ResetButton")]
	private Button _ResetButton;

	[CompilerGenerated]
	[AccessedThroughProperty("BrowseButton")]
	private Button _BrowseButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ToDatePicker")]
	private DateTimePicker _ToDatePicker;

	[CompilerGenerated]
	[AccessedThroughProperty("FromDatePicker")]
	private DateTimePicker _FromDatePicker;

	[CompilerGenerated]
	[AccessedThroughProperty("TipsButton")]
	private Button _TipsButton;

	[CompilerGenerated]
	[AccessedThroughProperty("WeeklyRadioButton")]
	private RadioButton _WeeklyRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DailyRadioButton")]
	private RadioButton _DailyRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("MonthlyRadioButton")]
	private RadioButton _MonthlyRadioButton;

	private const int BOXCONTINUATION = 1;

	private const int BOXREVERSAL = 3;

	private const string KEYPRE = "PredictionForm";

	private const int GSTOCK = 0;

	private const int GSTART = 1;

	private const int GEND = 2;

	private const int GNEXT = 3;

	private const int GCOMMENT = 4;

	private const int GNEXTTREND = 5;

	private const int MULT10 = 10;

	private const int MULT2 = 2;

	private const int MULT1 = 1;

	private readonly int RLOOSE;

	private readonly int RNORMAL;

	private readonly int RSTRICT;

	private Setting Settings;

	private SigStruct[] Signature;

	private SigStruct[] Profile;

	private ResetStruct RestoreStructure;

	private Point StartPoint;

	private Point EndPoint;

	private string Filename;

	private string lsFilename;

	private bool Crosshair;

	private Point CrosshairPoint;

	private Pen CrosshairPen;

	private int PredictionLookBack;

	private int lsPredictionLookBack;

	private decimal[,] BoxSize;

	private CalloutAnnotation CurrentAnnotation;

	private bool StopPressed;

	private string lsSymbolTB;

	private readonly string SymbolMessage;

	private string ResultsMessage;

	private int TradesUp;

	private int TradesDown;

	private int TradesContinued;

	private int TradesTally;

	private decimal ProfitUp;

	private decimal ProfitDown;

	private bool ShowProfile;

	private bool FormLockFlag;

	private bool LockFlag;

	private bool DatePickerLockFlag;

	private bool ErrorFlag;

	private bool PreviewButtonClicked;

	private decimal[] Sorted;

	private decimal[] NextSorted;

	private decimal[] NextPercentSorted;

	private bool GridClicked;

	private decimal TargetUp1;

	private decimal TargetDown1;

	private decimal TargetUp2;

	private decimal TargetDown2;

	private decimal TargetContinue;

	private decimal SignatureHigh;

	private decimal SignatureLow;

	private decimal EndSigClose;

	private decimal SigMove;

	private string SigFilename;

	private DateTime SigStart;

	private DateTime SigEnd;

	private int lsDWM;

	private int DWM;

	private int lsMultiplier;

	internal virtual Chart Chart1
	{
		[CompilerGenerated]
		get
		{
			return _Chart1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0007: Unknown result type (might be due to invalid IL or missing references)
			//IL_000d: Expected O, but got Unknown
			//IL_0014: Unknown result type (might be due to invalid IL or missing references)
			//IL_001a: Expected O, but got Unknown
			//IL_0021: Unknown result type (might be due to invalid IL or missing references)
			//IL_0027: Expected O, but got Unknown
			//IL_002e: Unknown result type (might be due to invalid IL or missing references)
			//IL_0034: Expected O, but got Unknown
			MouseEventHandler val = new MouseEventHandler(Chart1_MouseDown);
			MouseEventHandler val2 = new MouseEventHandler(Chart1_MouseUp);
			MouseEventHandler val3 = new MouseEventHandler(Chart1_MouseMove);
			PaintEventHandler val4 = new PaintEventHandler(Chart1_Paint);
			EventHandler<ChartPaintEventArgs> eventHandler = Chart1_PostPaint;
			Chart val5 = _Chart1;
			if (val5 != null)
			{
				((Control)val5).MouseDown -= val;
				((Control)val5).MouseUp -= val2;
				((Control)val5).MouseMove -= val3;
				((Control)val5).Paint -= val4;
				val5.PostPaint -= eventHandler;
			}
			_Chart1 = value;
			val5 = _Chart1;
			if (val5 != null)
			{
				((Control)val5).MouseDown += val;
				((Control)val5).MouseUp += val2;
				((Control)val5).MouseMove += val3;
				((Control)val5).Paint += val4;
				val5.PostPaint += eventHandler;
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

	internal virtual DataGridView ResultsGrid
	{
		[CompilerGenerated]
		get
		{
			return _ResultsGrid;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0007: Unknown result type (might be due to invalid IL or missing references)
			//IL_000d: Expected O, but got Unknown
			DataGridViewCellEventHandler val = new DataGridViewCellEventHandler(ResultsGrid_RowEnter);
			DataGridView val2 = _ResultsGrid;
			if (val2 != null)
			{
				val2.RowEnter -= val;
			}
			_ResultsGrid = value;
			val2 = _ResultsGrid;
			if (val2 != null)
			{
				val2.RowEnter += val;
			}
		}
	}

	internal virtual Button GraphButton
	{
		[CompilerGenerated]
		get
		{
			return _GraphButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GraphButton_Click;
			Button val = _GraphButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_GraphButton = value;
			val = _GraphButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("ErrorLabel")]
	internal virtual Label ErrorLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label4")]
	internal virtual Label Label4
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("LoadingBar")]
	internal virtual ProgressBar LoadingBar
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

	[field: AccessedThroughProperty("FindingBar")]
	internal virtual ProgressBar FindingBar
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

	[field: AccessedThroughProperty("Label6")]
	internal virtual Label Label6
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("ToRB")]
	internal virtual RadioButton ToRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("FromRB")]
	internal virtual RadioButton FromRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Panel2")]
	internal virtual Panel Panel2
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

	internal virtual DateTimePicker PatternToPicker
	{
		[CompilerGenerated]
		get
		{
			return _PatternToPicker;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PatternFromPicker_Validated;
			DateTimePicker val = _PatternToPicker;
			if (val != null)
			{
				((Control)val).Validated -= eventHandler;
			}
			_PatternToPicker = value;
			val = _PatternToPicker;
			if (val != null)
			{
				((Control)val).Validated += eventHandler;
			}
		}
	}

	internal virtual DateTimePicker PatternFromPicker
	{
		[CompilerGenerated]
		get
		{
			return _PatternFromPicker;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PatternFromPicker_Validated;
			DateTimePicker val = _PatternFromPicker;
			if (val != null)
			{
				((Control)val).Validated -= eventHandler;
			}
			_PatternFromPicker = value;
			val = _PatternFromPicker;
			if (val != null)
			{
				((Control)val).Validated += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label7")]
	internal virtual Label Label7
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

	internal virtual Button ResultsButton
	{
		[CompilerGenerated]
		get
		{
			return _ResultsButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ResultsButton_Click;
			Button val = _ResultsButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ResultsButton = value;
			val = _ResultsButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("StockLabel")]
	internal virtual Label StockLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button PreviewButton
	{
		[CompilerGenerated]
		get
		{
			return _PreviewButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PreviewButton_Click;
			Button val = _PreviewButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_PreviewButton = value;
			val = _PreviewButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button ResetButton
	{
		[CompilerGenerated]
		get
		{
			return _ResetButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ResetButton_Click;
			Button val = _ResetButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ResetButton = value;
			val = _ResetButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
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

	[field: AccessedThroughProperty("OpenFileDialog1")]
	internal virtual OpenFileDialog OpenFileDialog1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("PatternLabel")]
	internal virtual Label PatternLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual DateTimePicker ToDatePicker
	{
		[CompilerGenerated]
		get
		{
			return _ToDatePicker;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ToDatePicker_Validated;
			DateTimePicker val = _ToDatePicker;
			if (val != null)
			{
				((Control)val).Validated -= eventHandler;
			}
			_ToDatePicker = value;
			val = _ToDatePicker;
			if (val != null)
			{
				((Control)val).Validated += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label2")]
	internal virtual Label Label2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label3")]
	internal virtual Label Label3
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual DateTimePicker FromDatePicker
	{
		[CompilerGenerated]
		get
		{
			return _FromDatePicker;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ToDatePicker_Validated;
			DateTimePicker val = _FromDatePicker;
			if (val != null)
			{
				((Control)val).Validated -= eventHandler;
			}
			_FromDatePicker = value;
			val = _FromDatePicker;
			if (val != null)
			{
				((Control)val).Validated += eventHandler;
			}
		}
	}

	internal virtual Button TipsButton
	{
		[CompilerGenerated]
		get
		{
			return _TipsButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = TipsButton_Click;
			Button val = _TipsButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_TipsButton = value;
			val = _TipsButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Panel5")]
	internal virtual Panel Panel5
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("NormalRB")]
	internal virtual RadioButton NormalRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("LooseRB")]
	internal virtual RadioButton LooseRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("StrictRB")]
	internal virtual RadioButton StrictRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label8")]
	internal virtual Label Label8
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label9")]
	internal virtual Label Label9
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton WeeklyRadioButton
	{
		[CompilerGenerated]
		get
		{
			return _WeeklyRadioButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = WeeklyRadioButton_CheckedChanged;
			RadioButton val = _WeeklyRadioButton;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_WeeklyRadioButton = value;
			val = _WeeklyRadioButton;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual RadioButton DailyRadioButton
	{
		[CompilerGenerated]
		get
		{
			return _DailyRadioButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = WeeklyRadioButton_CheckedChanged;
			RadioButton val = _DailyRadioButton;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_DailyRadioButton = value;
			val = _DailyRadioButton;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual RadioButton MonthlyRadioButton
	{
		[CompilerGenerated]
		get
		{
			return _MonthlyRadioButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = WeeklyRadioButton_CheckedChanged;
			RadioButton val = _MonthlyRadioButton;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_MonthlyRadioButton = value;
			val = _MonthlyRadioButton;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("SignatureLabel")]
	internal virtual Label SignatureLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public ForecastForm()
	{
		//IL_0086: Unknown result type (might be due to invalid IL or missing references)
		//IL_0090: Expected O, but got Unknown
		((Form)this).Closing += PredictionForm_Closing;
		((Form)this).Load += PredictionForm_Load;
		((Form)this).Activated += PredictionForm_Activated;
		RLOOSE = 1;
		RNORMAL = 0;
		RSTRICT = -1;
		Signature = new SigStruct[1];
		Profile = new SigStruct[1];
		Crosshair = false;
		CrosshairPen = null;
		BoxSize = new decimal[10, 2];
		CurrentAnnotation = new CalloutAnnotation();
		StopPressed = false;
		SymbolMessage = "No symbol has been entered or I can't find the associated file, so I'll use the first highlighted symbol on the Main Form's list.";
		FormLockFlag = false;
		LockFlag = false;
		DatePickerLockFlag = false;
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
		//IL_0000: Unknown result type (might be due to invalid IL or missing references)
		//IL_0006: Expected O, but got Unknown
		//IL_0006: Unknown result type (might be due to invalid IL or missing references)
		//IL_000c: Expected O, but got Unknown
		//IL_000c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0012: Expected O, but got Unknown
		//IL_0012: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		//IL_0019: Unknown result type (might be due to invalid IL or missing references)
		//IL_0023: Expected O, but got Unknown
		//IL_0024: Unknown result type (might be due to invalid IL or missing references)
		//IL_002e: Expected O, but got Unknown
		//IL_002f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0039: Expected O, but got Unknown
		//IL_003a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0044: Expected O, but got Unknown
		//IL_0045: Unknown result type (might be due to invalid IL or missing references)
		//IL_004f: Expected O, but got Unknown
		//IL_0050: Unknown result type (might be due to invalid IL or missing references)
		//IL_005a: Expected O, but got Unknown
		//IL_005b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0065: Expected O, but got Unknown
		//IL_0066: Unknown result type (might be due to invalid IL or missing references)
		//IL_0070: Expected O, but got Unknown
		//IL_0071: Unknown result type (might be due to invalid IL or missing references)
		//IL_007b: Expected O, but got Unknown
		//IL_007c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0086: Expected O, but got Unknown
		//IL_0087: Unknown result type (might be due to invalid IL or missing references)
		//IL_0091: Expected O, but got Unknown
		//IL_0092: Unknown result type (might be due to invalid IL or missing references)
		//IL_009c: Expected O, but got Unknown
		//IL_009d: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a7: Expected O, but got Unknown
		//IL_00a8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b2: Expected O, but got Unknown
		//IL_00b3: Unknown result type (might be due to invalid IL or missing references)
		//IL_00bd: Expected O, but got Unknown
		//IL_00be: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c8: Expected O, but got Unknown
		//IL_00c9: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d3: Expected O, but got Unknown
		//IL_00d4: Unknown result type (might be due to invalid IL or missing references)
		//IL_00de: Expected O, but got Unknown
		//IL_00df: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e9: Expected O, but got Unknown
		//IL_00ea: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f4: Expected O, but got Unknown
		//IL_00f5: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ff: Expected O, but got Unknown
		//IL_0100: Unknown result type (might be due to invalid IL or missing references)
		//IL_010a: Expected O, but got Unknown
		//IL_010b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0115: Expected O, but got Unknown
		//IL_0116: Unknown result type (might be due to invalid IL or missing references)
		//IL_0120: Expected O, but got Unknown
		//IL_0121: Unknown result type (might be due to invalid IL or missing references)
		//IL_012b: Expected O, but got Unknown
		//IL_012c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0136: Expected O, but got Unknown
		//IL_0137: Unknown result type (might be due to invalid IL or missing references)
		//IL_0141: Expected O, but got Unknown
		//IL_0142: Unknown result type (might be due to invalid IL or missing references)
		//IL_014c: Expected O, but got Unknown
		//IL_014d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0157: Expected O, but got Unknown
		//IL_0158: Unknown result type (might be due to invalid IL or missing references)
		//IL_0162: Expected O, but got Unknown
		//IL_0163: Unknown result type (might be due to invalid IL or missing references)
		//IL_016d: Expected O, but got Unknown
		//IL_016e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0178: Expected O, but got Unknown
		//IL_0179: Unknown result type (might be due to invalid IL or missing references)
		//IL_0183: Expected O, but got Unknown
		//IL_0184: Unknown result type (might be due to invalid IL or missing references)
		//IL_018e: Expected O, but got Unknown
		//IL_018f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0199: Expected O, but got Unknown
		//IL_019a: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a4: Expected O, but got Unknown
		//IL_01a5: Unknown result type (might be due to invalid IL or missing references)
		//IL_01af: Expected O, but got Unknown
		//IL_01b0: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ba: Expected O, but got Unknown
		//IL_01bb: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c5: Expected O, but got Unknown
		//IL_01c6: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d0: Expected O, but got Unknown
		//IL_01d1: Unknown result type (might be due to invalid IL or missing references)
		//IL_01db: Expected O, but got Unknown
		//IL_01dc: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e6: Expected O, but got Unknown
		//IL_01e7: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f1: Expected O, but got Unknown
		//IL_01f2: Unknown result type (might be due to invalid IL or missing references)
		//IL_01fc: Expected O, but got Unknown
		//IL_01fd: Unknown result type (might be due to invalid IL or missing references)
		//IL_0207: Expected O, but got Unknown
		//IL_03b4: Unknown result type (might be due to invalid IL or missing references)
		//IL_0d30: Unknown result type (might be due to invalid IL or missing references)
		//IL_0d3a: Expected O, but got Unknown
		//IL_0fba: Unknown result type (might be due to invalid IL or missing references)
		//IL_0fc4: Expected O, but got Unknown
		//IL_18aa: Unknown result type (might be due to invalid IL or missing references)
		//IL_18b4: Expected O, but got Unknown
		//IL_194b: Unknown result type (might be due to invalid IL or missing references)
		//IL_1955: Expected O, but got Unknown
		ChartArea val = new ChartArea();
		Series val2 = new Series();
		Series val3 = new Series();
		Series val4 = new Series();
		Chart1 = new Chart();
		DoneButton = new Button();
		StartButton = new Button();
		HelpButton1 = new Button();
		ClipboardButton = new Button();
		StopButton = new Button();
		ResultsGrid = new DataGridView();
		GraphButton = new Button();
		ErrorLabel = new Label();
		Label4 = new Label();
		LoadingBar = new ProgressBar();
		Label5 = new Label();
		FindingBar = new ProgressBar();
		Panel1 = new Panel();
		PatternToPicker = new DateTimePicker();
		PatternFromPicker = new DateTimePicker();
		Label6 = new Label();
		ToRB = new RadioButton();
		FromRB = new RadioButton();
		Panel2 = new Panel();
		Label1 = new Label();
		ToDatePicker = new DateTimePicker();
		Label2 = new Label();
		Label3 = new Label();
		FromDatePicker = new DateTimePicker();
		Label7 = new Label();
		SymbolTextBox = new TextBox();
		ResultsButton = new Button();
		StockLabel = new Label();
		PreviewButton = new Button();
		ResetButton = new Button();
		BrowseButton = new Button();
		OpenFileDialog1 = new OpenFileDialog();
		PatternLabel = new Label();
		TipsButton = new Button();
		Panel5 = new Panel();
		NormalRB = new RadioButton();
		LooseRB = new RadioButton();
		StrictRB = new RadioButton();
		Label8 = new Label();
		Label9 = new Label();
		WeeklyRadioButton = new RadioButton();
		DailyRadioButton = new RadioButton();
		MonthlyRadioButton = new RadioButton();
		SignatureLabel = new Label();
		((ISupportInitialize)Chart1).BeginInit();
		((ISupportInitialize)ResultsGrid).BeginInit();
		((Control)Panel1).SuspendLayout();
		((Control)Panel2).SuspendLayout();
		((Control)Panel5).SuspendLayout();
		((Control)this).SuspendLayout();
		((Control)Chart1).Anchor = (AnchorStyles)15;
		Chart1.BorderlineColor = Color.FromArgb(192, 0, 192);
		val.AxisX.Enabled = (AxisEnabled)1;
		val.AxisX.IntervalAutoMode = (IntervalAutoMode)1;
		val.AxisX.LabelAutoFitMaxFontSize = 8;
		val.AxisX.MajorGrid.Enabled = false;
		val.AxisX2.Enabled = (AxisEnabled)2;
		val.AxisY.Enabled = (AxisEnabled)2;
		val.AxisY.ScrollBar.Enabled = false;
		val.AxisY2.Enabled = (AxisEnabled)1;
		val.AxisY2.LabelAutoFitMaxFontSize = 8;
		val.AxisY2.MajorGrid.Enabled = false;
		val.AxisY2.MajorGrid.Interval = 0.0;
		val.AxisY2.MajorGrid.IntervalOffsetType = (DateTimeIntervalType)0;
		val.AxisY2.MajorGrid.IntervalType = (DateTimeIntervalType)1;
		val.AxisY2.ScrollBar.Enabled = false;
		val.BackColor = Color.White;
		val.BorderDashStyle = (ChartDashStyle)5;
		val.Name = "ChartArea1";
		val.Position.Auto = false;
		val.Position.Height = 100f;
		val.Position.Width = 100f;
		((Collection<ChartArea>)(object)Chart1.ChartAreas).Add(val);
		((Control)Chart1).Location = new Point(9, 9);
		((Control)Chart1).Margin = new Padding(0);
		((Control)Chart1).Name = "Chart1";
		((DataPointCustomProperties)val2).BorderColor = Color.Black;
		val2.ChartArea = "ChartArea1";
		val2.ChartType = (SeriesChartType)20;
		((DataPointCustomProperties)val2).CustomProperties = "PriceDownColor=Red, PriceUpColor=green";
		val2.IsXValueIndexed = true;
		((DataPointCustomProperties)val2).MarkerBorderColor = Color.White;
		val2.Name = "CandleSeries";
		val2.ShadowColor = Color.Black;
		val2.XValueType = (ChartValueType)8;
		val2.YAxisType = (AxisType)1;
		val2.YValuesPerPoint = 4;
		((DataPointCustomProperties)val3).BorderColor = Color.Black;
		val3.ChartArea = "ChartArea1";
		((DataPointCustomProperties)val3).Color = Color.FromArgb(255, 128, 0);
		val3.IsXValueIndexed = true;
		val3.Name = "VolumeSeries";
		val3.XValueType = (ChartValueType)8;
		val4.ChartArea = "ChartArea1";
		val4.ChartType = (SeriesChartType)3;
		((DataPointCustomProperties)val4).Color = Color.Blue;
		((DataPointCustomProperties)val4).IsVisibleInLegend = false;
		val4.IsXValueIndexed = true;
		val4.Name = "MASeries";
		val4.XValueType = (ChartValueType)8;
		val4.YAxisType = (AxisType)1;
		((Collection<Series>)(object)Chart1.Series).Add(val2);
		((Collection<Series>)(object)Chart1.Series).Add(val3);
		((Collection<Series>)(object)Chart1.Series).Add(val4);
		Chart1.Size = new Size(990, 531);
		((Control)Chart1).TabIndex = 1;
		((Control)Chart1).Text = "Chart1";
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(954, 694);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(52, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)StartButton).Anchor = (AnchorStyles)10;
		((Control)StartButton).Location = new Point(838, 694);
		((Control)StartButton).Name = "StartButton";
		((Control)StartButton).Size = new Size(44, 23);
		((Control)StartButton).TabIndex = 28;
		((ButtonBase)StartButton).Text = "St&art";
		((ButtonBase)StartButton).UseVisualStyleBackColor = true;
		((Control)HelpButton1).Anchor = (AnchorStyles)10;
		((Control)HelpButton1).Location = new Point(717, 694);
		((Control)HelpButton1).Name = "HelpButton1";
		((Control)HelpButton1).Size = new Size(49, 23);
		((Control)HelpButton1).TabIndex = 26;
		((ButtonBase)HelpButton1).Text = "&Help";
		((ButtonBase)HelpButton1).UseVisualStyleBackColor = true;
		((Control)ClipboardButton).Anchor = (AnchorStyles)10;
		((Control)ClipboardButton).Location = new Point(888, 694);
		((Control)ClipboardButton).Name = "ClipboardButton";
		((Control)ClipboardButton).Size = new Size(60, 23);
		((Control)ClipboardButton).TabIndex = 29;
		((ButtonBase)ClipboardButton).Text = "Clip&board";
		((ButtonBase)ClipboardButton).UseVisualStyleBackColor = true;
		((Control)StopButton).Anchor = (AnchorStyles)10;
		((Control)StopButton).Location = new Point(838, 666);
		((Control)StopButton).Name = "StopButton";
		((Control)StopButton).Size = new Size(44, 23);
		((Control)StopButton).TabIndex = 23;
		((ButtonBase)StopButton).Text = "St&op";
		((ButtonBase)StopButton).UseVisualStyleBackColor = true;
		ResultsGrid.AllowUserToAddRows = false;
		ResultsGrid.AllowUserToDeleteRows = false;
		((Control)ResultsGrid).Anchor = (AnchorStyles)14;
		ResultsGrid.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)10;
		((Control)ResultsGrid).CausesValidation = false;
		ResultsGrid.ColumnHeadersHeightSizeMode = (DataGridViewColumnHeadersHeightSizeMode)2;
		ResultsGrid.EditMode = (DataGridViewEditMode)4;
		ResultsGrid.EnableHeadersVisualStyles = false;
		((Control)ResultsGrid).Location = new Point(9, 573);
		((Control)ResultsGrid).Name = "ResultsGrid";
		ResultsGrid.ReadOnly = true;
		ResultsGrid.SelectionMode = (DataGridViewSelectionMode)1;
		ResultsGrid.ShowCellErrors = false;
		ResultsGrid.ShowCellToolTips = false;
		ResultsGrid.ShowEditingIcon = false;
		ResultsGrid.ShowRowErrors = false;
		((Control)ResultsGrid).Size = new Size(523, 144);
		((Control)ResultsGrid).TabIndex = 3;
		((Control)GraphButton).Anchor = (AnchorStyles)10;
		((Control)GraphButton).Location = new Point(954, 666);
		((Control)GraphButton).Name = "GraphButton";
		((Control)GraphButton).Size = new Size(52, 23);
		((Control)GraphButton).TabIndex = 25;
		((ButtonBase)GraphButton).Text = "&Graph";
		((ButtonBase)GraphButton).UseVisualStyleBackColor = true;
		((Control)ErrorLabel).Anchor = (AnchorStyles)10;
		((Control)ErrorLabel).CausesValidation = false;
		((Control)ErrorLabel).ForeColor = Color.Red;
		((Control)ErrorLabel).Location = new Point(888, 540);
		((Control)ErrorLabel).Name = "ErrorLabel";
		((Control)ErrorLabel).Size = new Size(118, 15);
		((Control)ErrorLabel).TabIndex = 12;
		((Control)Label4).Anchor = (AnchorStyles)10;
		Label4.AutoSize = true;
		((Control)Label4).Location = new Point(885, 579);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(48, 13);
		((Control)Label4).TabIndex = 15;
		Label4.Text = "Loading:";
		((Control)LoadingBar).Anchor = (AnchorStyles)10;
		((Control)LoadingBar).ForeColor = Color.Green;
		((Control)LoadingBar).Location = new Point(940, 580);
		((Control)LoadingBar).Name = "LoadingBar";
		((Control)LoadingBar).Size = new Size(60, 13);
		((Control)LoadingBar).TabIndex = 16;
		((Control)Label5).Anchor = (AnchorStyles)10;
		Label5.AutoSize = true;
		((Control)Label5).Location = new Point(890, 560);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(44, 13);
		((Control)Label5).TabIndex = 13;
		Label5.Text = "Finding:";
		((Control)FindingBar).Anchor = (AnchorStyles)10;
		((Control)FindingBar).ForeColor = Color.Green;
		((Control)FindingBar).Location = new Point(940, 561);
		((Control)FindingBar).Name = "FindingBar";
		((Control)FindingBar).Size = new Size(60, 13);
		((Control)FindingBar).TabIndex = 14;
		((Control)Panel1).Anchor = (AnchorStyles)10;
		((Control)Panel1).Controls.Add((Control)(object)PatternToPicker);
		((Control)Panel1).Controls.Add((Control)(object)PatternFromPicker);
		((Control)Panel1).Controls.Add((Control)(object)Label6);
		((Control)Panel1).Controls.Add((Control)(object)ToRB);
		((Control)Panel1).Controls.Add((Control)(object)FromRB);
		((Control)Panel1).Location = new Point(538, 573);
		((Control)Panel1).Name = "Panel1";
		((Control)Panel1).Size = new Size(187, 75);
		((Control)Panel1).TabIndex = 4;
		((Control)PatternToPicker).Anchor = (AnchorStyles)10;
		PatternToPicker.CustomFormat = "yyyy/MM/dd";
		PatternToPicker.Format = (DateTimePickerFormat)8;
		((Control)PatternToPicker).Location = new Point(60, 55);
		((Control)PatternToPicker).Name = "PatternToPicker";
		PatternToPicker.ShowUpDown = true;
		((Control)PatternToPicker).Size = new Size(120, 20);
		((Control)PatternToPicker).TabIndex = 4;
		PatternToPicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)PatternFromPicker).Anchor = (AnchorStyles)10;
		PatternFromPicker.CustomFormat = "yyyy/MM/dd";
		PatternFromPicker.Format = (DateTimePickerFormat)8;
		((Control)PatternFromPicker).Location = new Point(60, 29);
		((Control)PatternFromPicker).Name = "PatternFromPicker";
		PatternFromPicker.ShowUpDown = true;
		((Control)PatternFromPicker).Size = new Size(120, 20);
		((Control)PatternFromPicker).TabIndex = 2;
		PatternFromPicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)Label6).Anchor = (AnchorStyles)10;
		Label6.AutoSize = true;
		((Control)Label6).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label6).ForeColor = Color.Blue;
		((Control)Label6).Location = new Point(7, 6);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(76, 13);
		((Control)Label6).TabIndex = 0;
		Label6.Text = "Find Pattern";
		((Control)ToRB).Anchor = (AnchorStyles)10;
		((ButtonBase)ToRB).AutoSize = true;
		((Control)ToRB).Location = new Point(10, 55);
		((Control)ToRB).Name = "ToRB";
		((Control)ToRB).Size = new Size(44, 17);
		((Control)ToRB).TabIndex = 3;
		((Control)ToRB).Tag = "-1";
		((ButtonBase)ToRB).Text = "End";
		((ButtonBase)ToRB).UseVisualStyleBackColor = true;
		((Control)FromRB).Anchor = (AnchorStyles)10;
		((ButtonBase)FromRB).AutoSize = true;
		FromRB.Checked = true;
		((Control)FromRB).Location = new Point(10, 35);
		((Control)FromRB).Name = "FromRB";
		((Control)FromRB).Size = new Size(47, 17);
		((Control)FromRB).TabIndex = 1;
		FromRB.TabStop = true;
		((Control)FromRB).Tag = "-1";
		((ButtonBase)FromRB).Text = "Start";
		((ButtonBase)FromRB).UseVisualStyleBackColor = true;
		((Control)Panel2).Anchor = (AnchorStyles)10;
		((Control)Panel2).Controls.Add((Control)(object)Label1);
		((Control)Panel2).Controls.Add((Control)(object)ToDatePicker);
		((Control)Panel2).Controls.Add((Control)(object)Label2);
		((Control)Panel2).Controls.Add((Control)(object)Label3);
		((Control)Panel2).Controls.Add((Control)(object)FromDatePicker);
		((Control)Panel2).Location = new Point(538, 656);
		((Control)Panel2).Name = "Panel2";
		((Control)Panel2).Size = new Size(173, 74);
		((Control)Panel2).TabIndex = 5;
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label1).ForeColor = Color.Blue;
		((Control)Label1).Location = new Point(7, 6);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(37, 13);
		((Control)Label1).TabIndex = 0;
		Label1.Text = "Chart";
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(50, 44);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(120, 20);
		((Control)ToDatePicker).TabIndex = 4;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(11, 21);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(33, 13);
		((Control)Label2).TabIndex = 1;
		Label2.Text = "&From:";
		((Control)Label3).Anchor = (AnchorStyles)10;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(21, 44);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(23, 13);
		((Control)Label3).TabIndex = 3;
		Label3.Text = "&To:";
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(50, 18);
		((Control)FromDatePicker).Name = "FromDatePicker";
		FromDatePicker.ShowUpDown = true;
		((Control)FromDatePicker).Size = new Size(120, 20);
		((Control)FromDatePicker).TabIndex = 2;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)Label7).Anchor = (AnchorStyles)10;
		Label7.AutoSize = true;
		((Control)Label7).Location = new Point(890, 619);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(44, 13);
		((Control)Label7).TabIndex = 18;
		Label7.Text = "S&ymbol:";
		((Control)SymbolTextBox).Anchor = (AnchorStyles)10;
		((Control)SymbolTextBox).Location = new Point(940, 615);
		((Control)SymbolTextBox).Name = "SymbolTextBox";
		((Control)SymbolTextBox).Size = new Size(60, 20);
		((Control)SymbolTextBox).TabIndex = 19;
		((Control)ResultsButton).Anchor = (AnchorStyles)10;
		((Control)ResultsButton).Location = new Point(772, 666);
		((Control)ResultsButton).Name = "ResultsButton";
		((Control)ResultsButton).Size = new Size(60, 23);
		((Control)ResultsButton).TabIndex = 22;
		((ButtonBase)ResultsButton).Text = "&Results";
		((ButtonBase)ResultsButton).UseVisualStyleBackColor = true;
		((Control)StockLabel).Anchor = (AnchorStyles)10;
		((Control)StockLabel).Location = new Point(897, 599);
		((Control)StockLabel).Name = "StockLabel";
		((Control)StockLabel).Size = new Size(102, 13);
		((Control)StockLabel).TabIndex = 17;
		StockLabel.TextAlign = (ContentAlignment)64;
		((Control)PreviewButton).Anchor = (AnchorStyles)10;
		((Control)PreviewButton).Location = new Point(772, 694);
		((Control)PreviewButton).Name = "PreviewButton";
		((Control)PreviewButton).Size = new Size(60, 23);
		((Control)PreviewButton).TabIndex = 27;
		((ButtonBase)PreviewButton).Text = "&Preview";
		((ButtonBase)PreviewButton).UseVisualStyleBackColor = true;
		((Control)ResetButton).Anchor = (AnchorStyles)10;
		((Control)ResetButton).Location = new Point(772, 640);
		((Control)ResetButton).Name = "ResetButton";
		((Control)ResetButton).Size = new Size(60, 23);
		((Control)ResetButton).TabIndex = 20;
		((ButtonBase)ResetButton).Text = "&Reset";
		((ButtonBase)ResetButton).UseVisualStyleBackColor = true;
		((Control)BrowseButton).Anchor = (AnchorStyles)10;
		((Control)BrowseButton).Location = new Point(888, 666);
		((Control)BrowseButton).Name = "BrowseButton";
		((Control)BrowseButton).Size = new Size(60, 23);
		((Control)BrowseButton).TabIndex = 24;
		((ButtonBase)BrowseButton).Text = "&Browse";
		((ButtonBase)BrowseButton).UseVisualStyleBackColor = true;
		((FileDialog)OpenFileDialog1).FileName = "OpenFileDialog1";
		((Control)PatternLabel).Anchor = (AnchorStyles)14;
		((Control)PatternLabel).CausesValidation = false;
		((Control)PatternLabel).ForeColor = Color.Black;
		((Control)PatternLabel).Location = new Point(9, 548);
		((Control)PatternLabel).Name = "PatternLabel";
		((Control)PatternLabel).Size = new Size(523, 19);
		((Control)PatternLabel).TabIndex = 2;
		PatternLabel.TextAlign = (ContentAlignment)32;
		((Control)TipsButton).Anchor = (AnchorStyles)10;
		((Control)TipsButton).Location = new Point(717, 666);
		((Control)TipsButton).Name = "TipsButton";
		((Control)TipsButton).Size = new Size(49, 23);
		((Control)TipsButton).TabIndex = 21;
		((ButtonBase)TipsButton).Text = "&Tips";
		((ButtonBase)TipsButton).UseVisualStyleBackColor = true;
		((Control)Panel5).Anchor = (AnchorStyles)10;
		((Control)Panel5).Controls.Add((Control)(object)NormalRB);
		((Control)Panel5).Controls.Add((Control)(object)LooseRB);
		((Control)Panel5).Controls.Add((Control)(object)StrictRB);
		((Control)Panel5).Location = new Point(811, 564);
		((Control)Panel5).Name = "Panel5";
		((Control)Panel5).Size = new Size(70, 68);
		((Control)Panel5).TabIndex = 11;
		((Control)NormalRB).Anchor = (AnchorStyles)10;
		((ButtonBase)NormalRB).AutoSize = true;
		((Control)NormalRB).Location = new Point(3, 25);
		((Control)NormalRB).Name = "NormalRB";
		((Control)NormalRB).Size = new Size(58, 17);
		((Control)NormalRB).TabIndex = 1;
		((Control)NormalRB).Tag = "-1";
		((ButtonBase)NormalRB).Text = "&Normal";
		((ButtonBase)NormalRB).UseVisualStyleBackColor = true;
		((Control)LooseRB).Anchor = (AnchorStyles)10;
		((ButtonBase)LooseRB).AutoSize = true;
		((Control)LooseRB).Location = new Point(3, 5);
		((Control)LooseRB).Name = "LooseRB";
		((Control)LooseRB).Size = new Size(54, 17);
		((Control)LooseRB).TabIndex = 0;
		((Control)LooseRB).Tag = "-1";
		((ButtonBase)LooseRB).Text = "&Loose";
		((ButtonBase)LooseRB).UseVisualStyleBackColor = true;
		((Control)StrictRB).Anchor = (AnchorStyles)10;
		((ButtonBase)StrictRB).AutoSize = true;
		StrictRB.Checked = true;
		((Control)StrictRB).Location = new Point(3, 45);
		((Control)StrictRB).Name = "StrictRB";
		((Control)StrictRB).Size = new Size(49, 17);
		((Control)StrictRB).TabIndex = 2;
		StrictRB.TabStop = true;
		((Control)StrictRB).Tag = "-1";
		((ButtonBase)StrictRB).Text = "&Strict";
		((ButtonBase)StrictRB).UseVisualStyleBackColor = true;
		((Control)Label8).Anchor = (AnchorStyles)10;
		Label8.AutoSize = true;
		((Control)Label8).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label8).ForeColor = Color.Blue;
		((Control)Label8).Location = new Point(808, 551);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(39, 13);
		((Control)Label8).TabIndex = 10;
		Label8.Text = "Rules";
		((Control)Label9).Anchor = (AnchorStyles)10;
		Label9.AutoSize = true;
		((Control)Label9).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label9).ForeColor = Color.Blue;
		((Control)Label9).Location = new Point(727, 551);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(39, 13);
		((Control)Label9).TabIndex = 6;
		Label9.Text = "Scale";
		((Control)WeeklyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)WeeklyRadioButton).AutoSize = true;
		((Control)WeeklyRadioButton).Location = new Point(731, 590);
		((Control)WeeklyRadioButton).Name = "WeeklyRadioButton";
		((Control)WeeklyRadioButton).Size = new Size(61, 17);
		((Control)WeeklyRadioButton).TabIndex = 8;
		((Control)WeeklyRadioButton).Tag = "Weekly";
		((ButtonBase)WeeklyRadioButton).Text = "&Weekly";
		((ButtonBase)WeeklyRadioButton).UseVisualStyleBackColor = true;
		((Control)DailyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)DailyRadioButton).AutoSize = true;
		DailyRadioButton.Checked = true;
		((Control)DailyRadioButton).Location = new Point(731, 569);
		((Control)DailyRadioButton).Name = "DailyRadioButton";
		((Control)DailyRadioButton).Size = new Size(48, 17);
		((Control)DailyRadioButton).TabIndex = 7;
		DailyRadioButton.TabStop = true;
		((Control)DailyRadioButton).Tag = "Daily";
		((ButtonBase)DailyRadioButton).Text = "Dail&y";
		((ButtonBase)DailyRadioButton).UseVisualStyleBackColor = true;
		((Control)MonthlyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)MonthlyRadioButton).AutoSize = true;
		((Control)MonthlyRadioButton).Location = new Point(731, 612);
		((Control)MonthlyRadioButton).Name = "MonthlyRadioButton";
		((Control)MonthlyRadioButton).Size = new Size(62, 17);
		((Control)MonthlyRadioButton).TabIndex = 9;
		((Control)MonthlyRadioButton).Tag = "Monthly";
		((ButtonBase)MonthlyRadioButton).Text = "&Monthly";
		((ButtonBase)MonthlyRadioButton).UseVisualStyleBackColor = true;
		((Control)SignatureLabel).Anchor = (AnchorStyles)10;
		((Control)SignatureLabel).CausesValidation = false;
		((Control)SignatureLabel).ForeColor = Color.Black;
		((Control)SignatureLabel).Location = new Point(538, 545);
		((Control)SignatureLabel).Name = "SignatureLabel";
		((Control)SignatureLabel).Size = new Size(187, 19);
		((Control)SignatureLabel).TabIndex = 30;
		SignatureLabel.TextAlign = (ContentAlignment)32;
		((Form)this).AcceptButton = (IButtonControl)(object)StartButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(1008, 729);
		((Control)this).Controls.Add((Control)(object)SignatureLabel);
		((Control)this).Controls.Add((Control)(object)Panel5);
		((Control)this).Controls.Add((Control)(object)WeeklyRadioButton);
		((Control)this).Controls.Add((Control)(object)DailyRadioButton);
		((Control)this).Controls.Add((Control)(object)MonthlyRadioButton);
		((Control)this).Controls.Add((Control)(object)Label9);
		((Control)this).Controls.Add((Control)(object)Label8);
		((Control)this).Controls.Add((Control)(object)TipsButton);
		((Control)this).Controls.Add((Control)(object)PatternLabel);
		((Control)this).Controls.Add((Control)(object)BrowseButton);
		((Control)this).Controls.Add((Control)(object)ResetButton);
		((Control)this).Controls.Add((Control)(object)PreviewButton);
		((Control)this).Controls.Add((Control)(object)StockLabel);
		((Control)this).Controls.Add((Control)(object)ResultsButton);
		((Control)this).Controls.Add((Control)(object)Label7);
		((Control)this).Controls.Add((Control)(object)SymbolTextBox);
		((Control)this).Controls.Add((Control)(object)Panel2);
		((Control)this).Controls.Add((Control)(object)Panel1);
		((Control)this).Controls.Add((Control)(object)Label5);
		((Control)this).Controls.Add((Control)(object)FindingBar);
		((Control)this).Controls.Add((Control)(object)ErrorLabel);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)LoadingBar);
		((Control)this).Controls.Add((Control)(object)GraphButton);
		((Control)this).Controls.Add((Control)(object)ResultsGrid);
		((Control)this).Controls.Add((Control)(object)HelpButton1);
		((Control)this).Controls.Add((Control)(object)ClipboardButton);
		((Control)this).Controls.Add((Control)(object)StopButton);
		((Control)this).Controls.Add((Control)(object)StartButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)Chart1);
		((Control)this).Name = "ForecastForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Forecast Form";
		((ISupportInitialize)Chart1).EndInit();
		((ISupportInitialize)ResultsGrid).EndInit();
		((Control)Panel1).ResumeLayout(false);
		((Control)Panel1).PerformLayout();
		((Control)Panel2).ResumeLayout(false);
		((Control)Panel2).PerformLayout();
		((Control)Panel5).ResumeLayout(false);
		((Control)Panel5).PerformLayout();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void PredictionForm_Closing(object sender, CancelEventArgs e)
	{
		try
		{
			if (CurrentAnnotation != null)
			{
				((Collection<Annotation>)(object)Chart1.Annotations).Remove((Annotation)(object)CurrentAnnotation);
				((ChartElement)CurrentAnnotation).Dispose();
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		CurrentAnnotation = null;
		if (GridClicked)
		{
			PredictionLookBack = RestoreStructure.Predict;
		}
		else
		{
			PredictionLookBack = checked((int)DateAndTime.DateDiff((DateInterval)4, FromDatePicker.Value, ToDatePicker.Value, (FirstDayOfWeek)1, (FirstWeekOfYear)1));
		}
		if (lsPredictionLookBack != PredictionLookBack)
		{
			try
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PredictionForm", "Lookback", (object)PredictionLookBack);
			}
			catch (Exception ex3)
			{
				ProjectData.SetProjectError(ex3);
				Exception ex4 = ex3;
				ProjectData.ClearProjectError();
			}
		}
		try
		{
			if (Operators.CompareString(SymbolTextBox.Text, lsSymbolTB, false) != 0)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PredictionForm", "Symbol", (object)SymbolTextBox.Text);
			}
		}
		catch (Exception ex5)
		{
			ProjectData.SetProjectError(ex5);
			Exception ex6 = ex5;
			ProjectData.ClearProjectError();
		}
		bool flag = true;
		int num = default(int);
		if (flag == LooseRB.Checked)
		{
			num = 10;
		}
		else if (flag == NormalRB.Checked)
		{
			num = 2;
		}
		else if (flag == StrictRB.Checked)
		{
			num = 1;
		}
		try
		{
			if (num != lsMultiplier)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PredictionForm", "Strict", (object)num);
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
			if (lsDWM != DWM)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PredictionForm", "TimePeriod", (object)DWM);
			}
		}
		catch (Exception ex9)
		{
			ProjectData.SetProjectError(ex9);
			Exception ex10 = ex9;
			ProjectData.ClearProjectError();
		}
		MySettingsProperty.Settings.ForecastLocation = ((Form)this).Location;
		MySettingsProperty.Settings.ForecastSize = ((Form)this).Size;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
	}

	private void PredictionForm_Load(object sender, EventArgs e)
	{
		//IL_02da: Unknown result type (might be due to invalid IL or missing references)
		//IL_02df: Unknown result type (might be due to invalid IL or missing references)
		//IL_02ea: Unknown result type (might be due to invalid IL or missing references)
		//IL_02f5: Unknown result type (might be due to invalid IL or missing references)
		//IL_0300: Unknown result type (might be due to invalid IL or missing references)
		//IL_0307: Unknown result type (might be due to invalid IL or missing references)
		//IL_0318: Unknown result type (might be due to invalid IL or missing references)
		//IL_0329: Unknown result type (might be due to invalid IL or missing references)
		//IL_033a: Unknown result type (might be due to invalid IL or missing references)
		//IL_034b: Unknown result type (might be due to invalid IL or missing references)
		//IL_035c: Unknown result type (might be due to invalid IL or missing references)
		//IL_036d: Unknown result type (might be due to invalid IL or missing references)
		//IL_037e: Unknown result type (might be due to invalid IL or missing references)
		//IL_038f: Unknown result type (might be due to invalid IL or missing references)
		//IL_03a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_03b1: Unknown result type (might be due to invalid IL or missing references)
		//IL_03c2: Unknown result type (might be due to invalid IL or missing references)
		//IL_03d3: Unknown result type (might be due to invalid IL or missing references)
		//IL_03e4: Unknown result type (might be due to invalid IL or missing references)
		//IL_03f5: Unknown result type (might be due to invalid IL or missing references)
		//IL_0406: Unknown result type (might be due to invalid IL or missing references)
		//IL_0417: Unknown result type (might be due to invalid IL or missing references)
		//IL_0428: Unknown result type (might be due to invalid IL or missing references)
		//IL_0439: Unknown result type (might be due to invalid IL or missing references)
		//IL_044a: Unknown result type (might be due to invalid IL or missing references)
		//IL_045b: Unknown result type (might be due to invalid IL or missing references)
		//IL_046c: Unknown result type (might be due to invalid IL or missing references)
		//IL_047d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0277: Unknown result type (might be due to invalid IL or missing references)
		//IL_0281: Expected O, but got Unknown
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.ForecastLocation, MySettingsProperty.Settings.ForecastSize);
		ShowProfile = false;
		PreviewButtonClicked = false;
		FormLockFlag = false;
		ErrorFlag = false;
		GlobalForm.Quiet = false;
		GridClicked = false;
		TargetUp1 = default(decimal);
		TargetDown1 = default(decimal);
		TargetUp2 = default(decimal);
		TargetDown2 = default(decimal);
		TargetContinue = default(decimal);
		((Control)ClipboardButton).Enabled = false;
		((Control)ResetButton).Enabled = false;
		((Control)ResultsButton).Enabled = false;
		((Control)StopButton).Enabled = false;
		BoxSize[0, 0] = 0.25m;
		BoxSize[0, 1] = 0.0625m;
		BoxSize[1, 0] = 1m;
		BoxSize[1, 1] = 0.125m;
		BoxSize[2, 0] = 5m;
		BoxSize[2, 1] = 0.25m;
		BoxSize[3, 0] = 20m;
		BoxSize[3, 1] = 0.5m;
		BoxSize[4, 0] = 100m;
		BoxSize[4, 1] = 1m;
		BoxSize[5, 0] = 200m;
		BoxSize[5, 1] = 2m;
		BoxSize[6, 0] = 500m;
		BoxSize[6, 1] = 4m;
		BoxSize[7, 0] = 1000m;
		BoxSize[7, 1] = 5m;
		BoxSize[8, 0] = 25000m;
		BoxSize[8, 1] = 50m;
		BoxSize[9, 0] = -1m;
		BoxSize[9, 1] = 500m;
		BuildGridHeader();
		try
		{
			if (CurrentAnnotation == null)
			{
				CurrentAnnotation = new CalloutAnnotation();
			}
			((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)CurrentAnnotation);
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		((Control)DailyRadioButton).Tag = 0;
		((Control)WeeklyRadioButton).Tag = 1;
		((Control)MonthlyRadioButton).Tag = 2;
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)BrowseButton, "Select a symbol to chart.");
		val.SetToolTip((Control)(object)ClipboardButton, "Copy selected results to clipboard.");
		val.SetToolTip((Control)(object)DailyRadioButton, "Select the time scale to chart.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)FromDatePicker, "The chart's starting price.");
		val.SetToolTip((Control)(object)FromRB, "Change the pattern's start date by clicking a price bar on the chart.");
		val.SetToolTip((Control)(object)GraphButton, "Chart the symbol.");
		val.SetToolTip((Control)(object)HelpButton1, "Get help.");
		val.SetToolTip((Control)(object)LooseRB, "Finds matches for complex patterns using loose rules (works best with 6-7 segment patterns).");
		val.SetToolTip((Control)(object)MonthlyRadioButton, "Select the time scale to chart.");
		val.SetToolTip((Control)(object)NormalRB, "Finds matches using not-so-strict rules (works best with 4-5 segment patterns).");
		val.SetToolTip((Control)(object)PatternFromPicker, "Pattern's start date. Change by clicking a price bar.");
		val.SetToolTip((Control)(object)PatternToPicker, "Pattern's end date. Change by clicking a price bar.");
		val.SetToolTip((Control)(object)PreviewButton, "Show the pattern. Often used before starting a run.");
		val.SetToolTip((Control)(object)ResetButton, "Reload chart and restore settings when Start pressed.");
		val.SetToolTip((Control)(object)ResultsButton, "List the run's results.");
		val.SetToolTip((Control)(object)ResultsGrid, "Results are posted here.");
		val.SetToolTip((Control)(object)StartButton, "Begin the hunt for similar patterns.");
		val.SetToolTip((Control)(object)StopButton, "Halt a run.");
		val.SetToolTip((Control)(object)StrictRB, "Strict finds almost exact matches (works best with 3 segment patterns).");
		val.SetToolTip((Control)(object)SymbolTextBox, "Enter a stock symbol to chart and search for a pattern.");
		val.SetToolTip((Control)(object)ToDatePicker, "The chart's ending price.");
		val.SetToolTip((Control)(object)ToRB, "Change the pattern's end date by clicking a price bar on the chart.");
		val.SetToolTip((Control)(object)WeeklyRadioButton, "Select the time scale to chart.");
		GlobalForm.FirstPoint = default(Point);
		GlobalForm.LinesList.RemoveAll(StubBoolean);
		LoadingBar.Value = 0;
		try
		{
			PredictionLookBack = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PredictionForm", "Lookback", (object)90));
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			ProjectData.ClearProjectError();
		}
		if (PredictionLookBack == 0)
		{
			PredictionLookBack = 90;
		}
		lsPredictionLookBack = PredictionLookBack;
		FromDatePicker.Value = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)4, (double)checked(-1 * PredictionLookBack), DateAndTime.Now));
		ToDatePicker.Value = GlobalForm.FindDate(DateAndTime.Now);
		GlobalForm.ChartStart = FromDatePicker.Value.Date;
		GlobalForm.ChartEnd = ToDatePicker.Value.Date;
		PatternFromPicker.Value = GlobalForm.FindDate(DateAndTime.Now);
		PatternToPicker.Value = GlobalForm.FindDate(DateAndTime.Now);
	}

	private void PredictionForm_Activated(object sender, EventArgs e)
	{
		//IL_0194: Unknown result type (might be due to invalid IL or missing references)
		//IL_0262: Unknown result type (might be due to invalid IL or missing references)
		if (FormLockFlag)
		{
			return;
		}
		FormLockFlag = true;
		((Control)this).Refresh();
		int num = default(int);
		try
		{
			num = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PredictionForm", "Strict", (object)1));
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		lsMultiplier = num;
		switch (num)
		{
		case 10:
			LooseRB.Checked = true;
			break;
		case 2:
			NormalRB.Checked = true;
			break;
		case 1:
			StrictRB.Checked = true;
			break;
		}
		SymbolTextBox.Text = "";
		try
		{
			SymbolTextBox.Text = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PredictionForm", "Symbol", (object)""));
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			ProjectData.ClearProjectError();
		}
		lsSymbolTB = SymbolTextBox.Text;
		if (((TextBoxBase)SymbolTextBox).TextLength == 0)
		{
			goto IL_0180;
		}
		Filename = SymbolTextBox.Text + ".csv";
		if (!((ServerComputer)MyProject.Computer).FileSystem.FileExists(GlobalForm.OpenPath + "\\" + Filename))
		{
			Filename = SymbolTextBox.Text + ".txt";
			if (!((ServerComputer)MyProject.Computer).FileSystem.FileExists(GlobalForm.OpenPath + "\\" + Filename))
			{
				goto IL_0180;
			}
			((Control)this).Refresh();
		}
		goto IL_0209;
		IL_0180:
		((Control)this).Refresh();
		MessageBox.Show(SymbolMessage, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		Filename = MyProject.Forms.Mainform.ListBox1.SelectedItems[0].ToString();
		SymbolTextBox.Text = Strings.Left(Filename, checked(Strings.InStrRev(Filename, ".", -1, (CompareMethod)0) - 1));
		((Control)SymbolTextBox).Enabled = true;
		((Control)SymbolTextBox).Focus();
		goto IL_0209;
		IL_0209:
		lsFilename = Filename;
		string filename = Filename;
		ProgressBar ProgBar = LoadingBar;
		Label ErrorLabel = this.ErrorLabel;
		bool num2 = GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
		this.ErrorLabel = ErrorLabel;
		LoadingBar = ProgBar;
		if (num2)
		{
			return;
		}
		if (GlobalForm.IntradayData)
		{
			MessageBox.Show("The price range of intraday files is often too narrow upon which to base a forecast so I don't recommended you use this form.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
		EnableDisableDWM(DailyRadioButton, WeeklyRadioButton, MonthlyRadioButton);
		GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
		GlobalForm.FormatPickers(PatternFromPicker, PatternToPicker);
		GlobalForm.SelectChartType(Chart1);
		checked
		{
			if (GlobalForm.IntradayData)
			{
				if (GlobalForm.HLCRange - PredictionLookBack > 0)
				{
					if ((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.HLCRange - PredictionLookBack], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.HLCRange - PredictionLookBack], FromDatePicker.MaxDate) <= 0))
					{
						FromDatePicker.Value = GlobalForm.FindDate(GlobalForm.nDT[0, GlobalForm.HLCRange - PredictionLookBack]);
					}
					else
					{
						FromDatePicker.Value = GlobalForm.FindDate(DateAndTime.Now);
					}
				}
				else if ((DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MaxDate) <= 0))
				{
					FromDatePicker.Value = GlobalForm.nDT[0, 0];
				}
				else
				{
					FromDatePicker.Value = GlobalForm.FindDate(DateAndTime.Now);
				}
			}
			else
			{
				FromDatePicker.Value = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)4, (double)(-1 * PredictionLookBack), DateAndTime.Now));
			}
			ToDatePicker.Value = GlobalForm.FindDate(DateAndTime.Now);
			DateTimePicker fromDatePicker;
			DateTime FromDate = (fromDatePicker = FromDatePicker).Value;
			DateTimePicker toDatePicker;
			DateTime ToDate = (toDatePicker = ToDatePicker).Value;
			bool num3 = GlobalForm.SwapDates(ref FromDate, ref ToDate);
			toDatePicker.Value = ToDate;
			fromDatePicker.Value = FromDate;
			if (!num3)
			{
				if (GlobalForm.IntradayData)
				{
					GlobalForm.ChartStart = FromDatePicker.Value;
					GlobalForm.ChartEnd = ToDatePicker.Value;
				}
				else
				{
					GlobalForm.ChartStart = FromDatePicker.Value.Date;
					GlobalForm.ChartEnd = ToDatePicker.Value.Date;
				}
			}
			GlobalForm.CheckDates(FromDatePicker, ToDatePicker);
			try
			{
				DWM = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\PredictionForm", "TimePeriod", (object)0));
			}
			catch (Exception ex5)
			{
				ProjectData.SetProjectError(ex5);
				Exception ex6 = ex5;
				ProjectData.ClearProjectError();
			}
			lsDWM = DWM;
			switch (DWM)
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
			}
			GlobalForm.ShowStock(Chart1, FromDatePicker.Value, ToDatePicker.Value, VolumeFlag: false, MAFlag: false);
			FindingBar.Maximum = 100;
			((Form)this).Text = "Forecast Form: " + Filename;
		}
	}

	private void BrowseButton_Click(object sender, EventArgs e)
	{
		//IL_0006: Unknown result type (might be due to invalid IL or missing references)
		//IL_000b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0016: Unknown result type (might be due to invalid IL or missing references)
		//IL_0021: Unknown result type (might be due to invalid IL or missing references)
		//IL_0028: Unknown result type (might be due to invalid IL or missing references)
		//IL_0033: Unknown result type (might be due to invalid IL or missing references)
		//IL_003f: Expected O, but got Unknown
		//IL_0040: Unknown result type (might be due to invalid IL or missing references)
		//IL_0046: Invalid comparison between Unknown and I4
		//IL_0098: Unknown result type (might be due to invalid IL or missing references)
		string text = ".csv";
		OpenFileDialog val = new OpenFileDialog
		{
			InitialDirectory = GlobalForm.OpenPath,
			Filter = "csv files (*.csv)|*.csv|txt files (*.txt)|*.txt",
			FilterIndex = 1,
			Title = "Select the file to be used as the stock where the pattern resides. DO NOT CHANGE FOLDERS",
			FileName = ""
		};
		if ((int)((CommonDialog)val).ShowDialog() != 1)
		{
			return;
		}
		string text2 = ((FileDialog)val).FileName;
		int num = Strings.InStrRev(text2, "\\", -1, (CompareMethod)0);
		if (num == 0)
		{
			return;
		}
		checked
		{
			if (Operators.CompareString(Strings.Left(text2, num - 1), GlobalForm.OpenPath, false) != 0)
			{
				MessageBox.Show("The path you selected for the file is not the same as where the rest of the files are located. The file must be in the same folder (manually move the file to " + GlobalForm.OpenPath + " and click Browse again or select a different file).", "BrowseButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)16);
				return;
			}
			num = Strings.InStrRev(text2, ".", -1, (CompareMethod)0);
			if (num != 0)
			{
				text = Strings.Right(text2, text2.Length - (num - 1));
				text2 = Strings.Left(text2, num - 1);
			}
			num = Strings.InStrRev(text2, "\\", -1, (CompareMethod)0);
			if (num != 0)
			{
				text2 = Strings.Right(text2, text2.Length - num);
			}
			SymbolTextBox.Text = text2;
			Filename = text2 + text;
			((Form)this).Text = "Forecast Form: " + Filename;
			string filename = Filename;
			ProgressBar ProgBar = LoadingBar;
			Label ErrorLabel = this.ErrorLabel;
			GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
			this.ErrorLabel = ErrorLabel;
			LoadingBar = ProgBar;
			EnableDisableDWM(DailyRadioButton, WeeklyRadioButton, MonthlyRadioButton);
			GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
			GlobalForm.SelectChartType(Chart1);
			GlobalForm.ShowStock(Chart1, FromDatePicker.Value, ToDatePicker.Value, VolumeFlag: false, MAFlag: false);
		}
	}

	private void BuildGridHeader()
	{
		ResultsGrid.RowCount = 0;
		ResultsGrid.ColumnCount = 6;
		ResultsGrid.Columns[0].HeaderText = "Stock";
		ResultsGrid.Columns[1].HeaderText = "Start";
		ResultsGrid.Columns[2].HeaderText = "End";
		ResultsGrid.Columns[3].HeaderText = "Next Move";
		ResultsGrid.Columns[4].HeaderText = "Explanation";
		ResultsGrid.Columns[5].Visible = false;
		((DataGridViewCell)ResultsGrid.Columns[3].HeaderCell).Style.ForeColor = Color.Green;
	}

	public void BuildSorted(decimal Move, decimal NextMove, decimal NextPS)
	{
		checked
		{
			if (decimal.Compare(Move, 0m) > 0)
			{
				Sorted[Sorted.Length - 1] = Move;
				ref decimal[] sorted = ref Sorted;
				sorted = (decimal[])Utils.CopyArray((Array)sorted, (Array)new decimal[Information.UBound((Array)Sorted, 1) + 1 + 1]);
				Sorted[Information.UBound((Array)Sorted, 1)] = 0.01m;
			}
			NextSorted[NextSorted.Length - 1] = NextMove;
			ref decimal[] nextSorted = ref NextSorted;
			nextSorted = (decimal[])Utils.CopyArray((Array)nextSorted, (Array)new decimal[Information.UBound((Array)NextSorted, 1) + 1 + 1]);
			NextSorted[Information.UBound((Array)NextSorted, 1)] = 0.01m;
			NextPercentSorted[NextPercentSorted.Length - 1] = NextPS;
			ref decimal[] nextPercentSorted = ref NextPercentSorted;
			nextPercentSorted = (decimal[])Utils.CopyArray((Array)nextPercentSorted, (Array)new decimal[Information.UBound((Array)NextPercentSorted, 1) + 1 + 1]);
			NextPercentSorted[Information.UBound((Array)NextPercentSorted, 1)] = 0.01m;
		}
	}

	private void Chart1_MouseDown(object sender, MouseEventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_000b: Invalid comparison between Unknown and I4
		//IL_0056: Unknown result type (might be due to invalid IL or missing references)
		//IL_0060: Invalid comparison between Unknown and I4
		//IL_0020: Unknown result type (might be due to invalid IL or missing references)
		//IL_0025: Unknown result type (might be due to invalid IL or missing references)
		//IL_0031: Expected O, but got Unknown
		//IL_008a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0091: Invalid comparison between Unknown and I4
		if ((int)e.Button == 1048576)
		{
			if (Information.IsNothing((object)CrosshairPen))
			{
				CrosshairPen = new Pen(Color.Black)
				{
					DashStyle = (DashStyle)1
				};
			}
			CrosshairPoint = new Point(e.X, e.Y);
			Crosshair = true;
			((Control)this).Refresh();
		}
		if ((int)e.Button != 2097152)
		{
			return;
		}
		GlobalForm.ShowQuoteInfo(Chart1, e);
		try
		{
			HitTestResult val = Chart1.HitTest(e.X, e.Y);
			if ((int)val.ChartElementType != 16)
			{
				return;
			}
			int pointIndex = val.PointIndex;
			checked
			{
				if (Operators.CompareString(val.Series.Name, "CandleSeries", false) == 0)
				{
					if (FromRB.Checked)
					{
						if ((DateTime.Compare(GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex], FromDatePicker.MaxDate) <= 0))
						{
							if (GlobalForm.IntradayData)
							{
								PatternFromPicker.Value = GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex];
							}
							else
							{
								PatternFromPicker.Value = GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex].Date;
							}
						}
						else
						{
							PatternFromPicker.Value = GlobalForm.FindDate(DateAndTime.Now);
						}
					}
					else if ((DateTime.Compare(GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex], FromDatePicker.MaxDate) <= 0))
					{
						if (GlobalForm.IntradayData)
						{
							PatternToPicker.Value = GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex];
						}
						else
						{
							PatternToPicker.Value = GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex].Date;
						}
					}
					else
					{
						PatternToPicker.Value = GlobalForm.FindDate(DateAndTime.Now);
					}
				}
				if (FromRB.Checked)
				{
					ToRB.Checked = true;
				}
				else
				{
					FromRB.Checked = true;
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

	private void Chart1_MouseUp(object sender, MouseEventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_000b: Invalid comparison between Unknown and I4
		//IL_011d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0127: Invalid comparison between Unknown and I4
		//IL_0042: Unknown result type (might be due to invalid IL or missing references)
		//IL_0048: Expected O, but got Unknown
		if ((int)e.Button == 1048576)
		{
			Crosshair = false;
			if (!Information.IsNothing((object)CrosshairPen))
			{
				CrosshairPen.Dispose();
				CrosshairPen = null;
			}
			Graphics obj = ((Control)this).CreateGraphics();
			Pen val = new Pen(((Form)this).BackColor);
			StartPoint = CrosshairPoint;
			StartPoint.X = 0;
			EndPoint = CrosshairPoint;
			checked
			{
				EndPoint.X = ((Control)Chart1).Right - ((Control)Chart1).Left;
				obj.DrawLine(val, StartPoint, EndPoint);
				StartPoint = CrosshairPoint;
				StartPoint.Y = 0;
				EndPoint = CrosshairPoint;
				EndPoint.Y = ((Control)Chart1).Bottom - ((Control)Chart1).Top;
				obj.DrawLine(val, StartPoint, EndPoint);
				val.Dispose();
				CrosshairPoint = new Point(e.X, e.Y);
				((Control)this).Refresh();
			}
		}
		if ((int)e.Button == 2097152)
		{
			GlobalForm.ReleaseQuoteInfo(Chart1, e);
		}
	}

	private void Chart1_MouseMove(object sender, MouseEventArgs e)
	{
		//IL_004c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0053: Invalid comparison between Unknown and I4
		//IL_0013: Unknown result type (might be due to invalid IL or missing references)
		//IL_001d: Expected O, but got Unknown
		//IL_02d6: Unknown result type (might be due to invalid IL or missing references)
		//IL_02dd: Expected O, but got Unknown
		//IL_0328: Unknown result type (might be due to invalid IL or missing references)
		//IL_032f: Expected O, but got Unknown
		try
		{
			if (GlobalForm.Annotations)
			{
				if (CurrentAnnotation == null)
				{
					CurrentAnnotation = new CalloutAnnotation();
					((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)CurrentAnnotation);
				}
				HitTestResult val = Chart1.HitTest(e.X, e.Y);
				if ((int)val.ChartElementType == 16 && Operators.CompareString(val.Series.Name, "CandleSeries", false) == 0)
				{
					CalloutAnnotation currentAnnotation = CurrentAnnotation;
					((Annotation)currentAnnotation).AnchorDataPoint = ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex];
					double num = (double)((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Count / 5.0;
					if ((double)val.PointIndex - num <= 0.0)
					{
						((Annotation)currentAnnotation).X = (double)val.PointIndex + num;
					}
					else
					{
						((Annotation)currentAnnotation).X = (double)val.PointIndex - num;
					}
					((Annotation)currentAnnotation).Y = ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[3];
					((TextAnnotation)currentAnnotation).Text = "Open: " + GlobalForm.LimitDecimals(new decimal(((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[2])) + "\r\nHigh: " + GlobalForm.LimitDecimals(new decimal(((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[0])) + "\r\nLow: " + GlobalForm.LimitDecimals(new decimal(((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[1])) + "\r\nClose: " + GlobalForm.LimitDecimals(new decimal(((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[3]).ToString());
					((Annotation)currentAnnotation).Visible = true;
					currentAnnotation = null;
					Chart1.Invalidate();
				}
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		if (!(GlobalForm.FirstPoint == default(Point)))
		{
			Graphics obj = ((Control)this).CreateGraphics();
			Pen val2 = new Pen(((Form)this).BackColor);
			obj.DrawLine(val2, GlobalForm.FirstPoint, GlobalForm.TempPoint);
			GlobalForm.TempPoint = new Point(e.X, e.Y);
			((Control)this).Refresh();
			val2.Dispose();
		}
		checked
		{
			if (Crosshair)
			{
				Graphics obj2 = ((Control)this).CreateGraphics();
				Pen val3 = new Pen(((Form)this).BackColor);
				StartPoint = CrosshairPoint;
				StartPoint.X = 0;
				EndPoint = CrosshairPoint;
				EndPoint.X = ((Control)Chart1).Right - ((Control)Chart1).Left;
				obj2.DrawLine(val3, StartPoint, EndPoint);
				StartPoint = CrosshairPoint;
				StartPoint.Y = 0;
				EndPoint = CrosshairPoint;
				EndPoint.Y = ((Control)Chart1).Bottom - ((Control)Chart1).Top;
				obj2.DrawLine(val3, StartPoint, EndPoint);
				val3.Dispose();
				CrosshairPoint = new Point(e.X, e.Y);
				((Control)this).Refresh();
			}
		}
	}

	private void Chart1_Paint(object sender, PaintEventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0010: Expected O, but got Unknown
		Font val = new Font("Arial", 8f);
		GlobalForm.StringSize = e.Graphics.MeasureString("C", val);
		val.Dispose();
		foreach (GlobalForm.LineEndPoints lines in GlobalForm.LinesList)
		{
			e.Graphics.DrawLine(Pens.Black, lines.StartPoint, lines.endPoint);
		}
		if (!(GlobalForm.FirstPoint == default(Point)))
		{
			e.Graphics.DrawLine(Pens.Black, GlobalForm.FirstPoint, GlobalForm.TempPoint);
		}
		checked
		{
			if (Crosshair)
			{
				StartPoint = CrosshairPoint;
				StartPoint.X = 0;
				EndPoint = CrosshairPoint;
				EndPoint.X = ((Control)Chart1).Right - ((Control)Chart1).Left;
				e.Graphics.DrawLine(CrosshairPen, StartPoint, EndPoint);
				StartPoint = CrosshairPoint;
				StartPoint.Y = 0;
				EndPoint = CrosshairPoint;
				EndPoint.Y = ((Control)Chart1).Bottom - ((Control)Chart1).Top;
				e.Graphics.DrawLine(CrosshairPen, StartPoint, EndPoint);
			}
		}
	}

	private void Chart1_PostPaint(object sender, ChartPaintEventArgs e)
	{
		//IL_0053: Unknown result type (might be due to invalid IL or missing references)
		//IL_0231: Unknown result type (might be due to invalid IL or missing references)
		//IL_0238: Expected O, but got Unknown
		//IL_023d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0244: Expected O, but got Unknown
		//IL_024e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0255: Expected O, but got Unknown
		PointF pointF = default(PointF);
		PointF pointF2 = default(PointF);
		if (PreviewButtonClicked)
		{
			DisplayProfile(e, Signature);
		}
		else if (ShowProfile)
		{
			DisplayProfile(e, Profile);
			return;
		}
		if (!(e.ChartElement is Series) || Operators.CompareString(((Series)e.ChartElement).Name, "CandleSeries", false) != 0)
		{
			return;
		}
		int num = 0;
		int num2;
		int num3;
		int num4;
		while (true)
		{
			num2 = -1;
			num3 = -1;
			num4 = -1;
			for (int i = GlobalForm.HLCRange; i >= 0; i = checked(i + -1))
			{
				if (GlobalForm.IntradayData)
				{
					if ((num4 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i], GlobalForm.ChartStart) == 0))
					{
						num4 = i;
					}
					if ((num2 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i], PatternFromPicker.Value) == 0))
					{
						num2 = i;
					}
					if ((num3 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i], PatternToPicker.Value) == 0))
					{
						num3 = i;
					}
				}
				else
				{
					if ((num4 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i].Date, GlobalForm.ChartStart.Date) == 0))
					{
						num4 = i;
					}
					if ((num2 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i].Date, PatternFromPicker.Value.Date) == 0))
					{
						num2 = i;
					}
					if ((num3 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i].Date, PatternToPicker.Value.Date) == 0))
					{
						num3 = i;
					}
				}
				if (num2 != -1 && num3 != -1 && num4 != -1)
				{
					break;
				}
			}
			if (num4 != -1)
			{
				break;
			}
			if (num == 0)
			{
				GlobalForm.ChartStart = DateAndTime.DateAdd((DateInterval)4, -1.0, GlobalForm.ChartStart);
				FromDatePicker.Value = GlobalForm.ChartStart;
				num = checked(num + 1);
				continue;
			}
			num4 = 0;
			break;
		}
		if (num2 == -1 && num3 == -1)
		{
			return;
		}
		Series val = (Series)e.ChartElement;
		SolidBrush val2 = new SolidBrush(Color.Red);
		Font val3 = new Font("Arial", 8f);
		int num5 = 0;
		int num6 = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)val.Points)
			{
				if ((num2 != -1) & (num5 == num2 - num4 + 0))
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num5 + 1));
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					pointF2.X = pointF.X;
					pointF2.Y = ((Control)Chart1).Bottom;
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
					e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF, pointF2);
					num6++;
				}
				if ((num3 != -1) & (num5 == num3 - num4 + 0))
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num5 + 1));
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					pointF2.X = pointF.X;
					pointF2.Y = ((Control)Chart1).Bottom;
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
					e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF, pointF2);
					num6++;
					if (decimal.Compare(TargetContinue, 0m) != 0)
					{
						pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num5 - 10));
						pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(TargetContinue));
						pointF2.Y = pointF.Y;
						pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
						pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)((Collection<DataPoint>)(object)val.Points).Count);
						pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
						e.ChartGraphics.Graphics.DrawLine(Pens.DarkGreen, pointF, pointF2);
						e.ChartGraphics.Graphics.DrawString("Continue Target: " + Strings.Format((object)TargetContinue, "#0.00"), val3, (Brush)(object)val2, pointF);
					}
					if (decimal.Compare(TargetUp1, 0m) != 0)
					{
						pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num5 - 10));
						pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(TargetUp1));
						pointF2.Y = pointF.Y;
						pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
						pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)((Collection<DataPoint>)(object)val.Points).Count);
						pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
						e.ChartGraphics.Graphics.DrawLine(Pens.Blue, pointF, pointF2);
						e.ChartGraphics.Graphics.DrawString("Rev Target 1: " + Strings.Format((object)TargetUp1, "#0.00"), val3, (Brush)(object)val2, pointF);
					}
					if (decimal.Compare(TargetUp2, 0m) != 0)
					{
						pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num5 - 10));
						pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(TargetUp2));
						pointF2.Y = pointF.Y;
						pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
						pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)((Collection<DataPoint>)(object)val.Points).Count);
						pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
						e.ChartGraphics.Graphics.DrawLine(Pens.Blue, pointF, pointF2);
						e.ChartGraphics.Graphics.DrawString("Rev Target 2: " + Strings.Format((object)TargetUp2, "#0.00"), val3, (Brush)(object)val2, pointF);
					}
					if (decimal.Compare(TargetDown1, 0m) != 0)
					{
						pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num5 - 10));
						pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(TargetDown1));
						pointF2.Y = pointF.Y;
						pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
						pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)((Collection<DataPoint>)(object)val.Points).Count);
						pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
						e.ChartGraphics.Graphics.DrawLine(Pens.Blue, pointF, pointF2);
						e.ChartGraphics.Graphics.DrawString("Rev Target 1: " + Strings.Format((object)TargetDown1, "#0.00"), val3, (Brush)(object)val2, pointF);
					}
					if (decimal.Compare(TargetDown2, 0m) != 0)
					{
						pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num5 - 10));
						pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(TargetDown2));
						pointF2.Y = pointF.Y;
						pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
						pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)((Collection<DataPoint>)(object)val.Points).Count);
						pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
						e.ChartGraphics.Graphics.DrawLine(Pens.Blue, pointF, pointF2);
						e.ChartGraphics.Graphics.DrawString("Rev Target 2: " + Strings.Format((object)TargetDown2, "#0.00"), val3, (Brush)(object)val2, pointF);
					}
				}
				num5++;
				if (num6 == 2)
				{
					break;
				}
			}
			val3.Dispose();
			((Brush)val2).Dispose();
		}
	}

	private void ClipboardButton_Click(object sender, EventArgs e)
	{
		//IL_0201: Unknown result type (might be due to invalid IL or missing references)
		//IL_0249: Unknown result type (might be due to invalid IL or missing references)
		//IL_0169: Unknown result type (might be due to invalid IL or missing references)
		//IL_0170: Expected O, but got Unknown
		if (ResultsGrid.RowCount == 0)
		{
			return;
		}
		if (((BaseCollection)ResultsGrid.SelectedRows).Count == 0)
		{
			ResultsGrid.SelectAll();
		}
		StopPressed = false;
		((Control)StopButton).Focus();
		((Control)this).Cursor = Cursors.WaitCursor;
		string text = "Copyright (c) " + Conversions.ToString(DateAndTime.Year(DateAndTime.Now)) + " by ThePatternSite.com. All rights reserved. For personal use only. \r\n\r\n";
		text = text + ResultsMessage + "\r\n\r\n";
		int rules = Settings.Rules;
		string text2 = ((rules == RLOOSE) ? "loose" : ((rules == RNORMAL) ? "normal" : ((rules != RSTRICT) ? "error!" : "strict")));
		text = text + "Using " + text2 + " rules on the ";
		text = text + Settings.DWM switch
		{
			0 => "daily", 
			1 => "weekly", 
			2 => "monthly", 
			_ => "Error!", 
		} + " scale.";
		text += "\r\n\r\nStart and End dates are the pattern's start and end dates.";
		text += "\r\nNext Move: The move after the pattern ends.";
		text += "\r\nMinor retraces or extensions are ignored. All prices are approximate.";
		text += "\r\n\r\n\t";
		foreach (DataGridViewColumn item in (BaseCollection)ResultsGrid.Columns)
		{
			DataGridViewColumn val = item;
			text = text + val.HeaderText + "\t";
		}
		text += "\r\n";
		try
		{
			Clipboard.SetDataObject((object)ResultsGrid.GetClipboardContent());
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
		MessageBox.Show("Done! " + ((BaseCollection)ResultsGrid.SelectedRows).Count + " results copied.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	public bool Compact(ref SigStruct[] Profile)
	{
		//IL_009e: Unknown result type (might be due to invalid IL or missing references)
		if (Information.UBound((Array)Profile, 1) == 1 && Math.Abs(Profile[1].Move) <= 3)
		{
			if (!GlobalForm.Quiet)
			{
				string text;
				if (DateTime.Compare(PatternFromPicker.Value, PatternToPicker.Value) == 0)
				{
					text = "The pattern's Start and End dates are the same.\r\n\r\n";
					text += "To change, click the Start or End radio button then RIGHT mouse click on a price bar on the chart. The date will be filled in automatically for the associated radio button.\r\n\r\n";
					text += "Click Preview. You're looking for patterns with 3 to 7 turns (segments), depending on the Rules (Strict, Normal, or Loose) you select.";
				}
				else
				{
					text = "Stock file name: " + Filename + ". If this is the benchmark stock (the one we are trying to find in other stocks), the pattern is not long enough or complex enough to chart. Try selecting different Start and End dates and then click Preview. This also might not work for new issues (out of data).\r\n\r\n";
					text += "For other stocks, the pattern might not be long enough to display.";
				}
				MessageBox.Show(text, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			}
			return true;
		}
		if (Signature.Length == 0)
		{
			return true;
		}
		SigStruct[] array = new SigStruct[1];
		bool flag = false;
		bool flag2 = false;
		int num = Information.UBound((Array)Profile, 1);
		checked
		{
			int iTurnStart = default(int);
			for (int i = 0; i <= num; i++)
			{
				if (Math.Abs(Profile[i].Move) > 3)
				{
					int num2 = array.Length - 1;
					array = (SigStruct[])Utils.CopyArray((Array)array, (Array)new SigStruct[num2 + 1 + 1]);
					array[num2].Move = Profile[i].Move;
					if (unchecked(!flag && iTurnStart != 0))
					{
						array[num2].iTurnStart = iTurnStart;
					}
					else
					{
						array[num2].iTurnStart = Profile[i].iTurnStart;
					}
					array[num2].iTurnEnd = Profile[i].iTurnEnd;
					array[num2].Price = Profile[i].Price;
					array[num2].iTrendEnd = Profile[i].iTrendEnd;
					flag = true;
				}
				else if (unchecked(!flag && !flag2) & (Profile[i].iTurnStart != 0))
				{
					iTurnStart = Profile[i].iTurnStart;
					flag2 = true;
				}
			}
			int num3 = Information.UBound((Array)array, 1);
			for (int j = 1; j <= num3; j++)
			{
				array[j].iTurnStart = array[j - 1].iTurnEnd;
			}
			SigStruct[] array2 = new SigStruct[1];
			int num4 = 0;
			int num5 = array.Length - 2;
			for (int k = 0; k <= num5; k++)
			{
				if (array[num4].Move == 0)
				{
					break;
				}
				array2[k].Move = array[num4].Move;
				array2[k].iTurnStart = array[num4].iTurnStart;
				array2[k].iTurnEnd = array[num4].iTurnEnd;
				array2[k].Price = array[num4].Price;
				array2[k].iTrendEnd = array[num4].iTrendEnd;
				num4++;
				if (array[num4].Move == 0)
				{
					break;
				}
				array2 = (SigStruct[])Utils.CopyArray((Array)array2, (Array)new SigStruct[k + 1 + 1]);
				if (num4 >= array.Length)
				{
					break;
				}
				while ((Math.Sign(array2[k].Move) == Math.Sign(array[num4].Move)) & (array[num4].Move != 0))
				{
					array2[k].Move += array[num4].Move;
					array2[k].iTurnEnd = array[num4].iTurnEnd;
					array2[k].Price = array[num4].Price;
					array2[k].iTrendEnd = array[num4].iTrendEnd;
					num4++;
					if (num4 >= array.Length)
					{
						goto end_IL_03e6;
					}
				}
				if (num4 >= array.Length)
				{
					break;
				}
				continue;
				end_IL_03e6:
				break;
			}
			Profile = null;
			Profile = new SigStruct[array2.Length - 1 + 1];
			array2.CopyTo(Profile, 0);
			if (Profile[Information.UBound((Array)Profile, 1)].Move == 0)
			{
				Profile = (SigStruct[])Utils.CopyArray((Array)Profile, (Array)new SigStruct[Information.UBound((Array)Profile, 1) - 1 + 1]);
			}
			return false;
		}
	}

	public void CompareResults(SigStruct[] Signature, ref SigStruct[] Target)
	{
		if ((Information.UBound((Array)Target, 1) < Information.UBound((Array)Signature, 1)) | (Signature.Length == 0))
		{
			return;
		}
		int num = Information.UBound((Array)Signature, 1);
		bool flag = true;
		int num2 = default(int);
		if (flag == LooseRB.Checked)
		{
			num2 = 10;
		}
		else if (flag == NormalRB.Checked)
		{
			num2 = 2;
		}
		else if (flag == StrictRB.Checked)
		{
			num2 = 1;
		}
		int num3 = Information.UBound((Array)Target, 1);
		checked
		{
			for (int i = 0; i <= num3 && i + num <= Information.UBound((Array)Target, 1); i++)
			{
				int num4 = num;
				int num5 = 0;
				while (true)
				{
					if (num5 <= num4)
					{
						if (((Math.Sign(Target[i + num5].Move) != Math.Sign(Signature[num5].Move)) | (Math.Abs(Target[i + num5].Move) < Math.Abs(Signature[num5].Move))) || Math.Abs(Target[i + num5].Move) > num2 * Math.Abs(Signature[num5].Move))
						{
							break;
						}
						num5++;
						continue;
					}
					if (Target[i + num].iTurnEnd == GlobalForm.HLCRange)
					{
						return;
					}
					if ((i + num + 1 < Target.Length && decimal.Compare(GlobalForm.nHLC[2, Target[i + num + 1].iTurnStart], 0m) == 0) || ((decimal.Compare(GlobalForm.nHLC[2, Target[i + num].iTurnStart], 0m) == 0) | (decimal.Compare(GlobalForm.nHLC[2, Target[i + num].iTurnEnd], 0m) == 0)))
					{
						break;
					}
					ResultsGrid.Rows.Add();
					ResultsGrid.Rows[ResultsGrid.RowCount - 1].Cells[0].Value = Filename;
					PatternLabel.Text = "Pattern count: " + ResultsGrid.RowCount;
					((Control)PatternLabel).Refresh();
					decimal value;
					decimal d;
					decimal value2;
					decimal num6;
					decimal d2;
					if (Target[i + num].Move > 0)
					{
						value = decimal.Subtract(GlobalForm.nHLC[1, Target[i + num].iTurnEnd], GlobalForm.nHLC[2, Target[i + num].iTurnStart]);
						d = GlobalForm.nHLC[2, Target[i + num].iTurnStart];
						value2 = decimal.Multiply(SigMove, GlobalForm.nHLC[2, Target[i + num].iTurnStart]);
						if (i + num + 1 < Target.Length)
						{
							num6 = decimal.Subtract(GlobalForm.nHLC[2, Target[i + num + 1].iTurnEnd], GlobalForm.nHLC[1, Target[i + num + 1].iTurnStart]);
							d2 = GlobalForm.nHLC[1, Target[i + num + 1].iTurnStart];
						}
						else
						{
							num6 = decimal.Subtract(GlobalForm.nHLC[2, GlobalForm.HLCRange], GlobalForm.nHLC[1, Target[i + num].iTurnEnd]);
							d2 = GlobalForm.nHLC[1, Target[i + num].iTurnEnd];
						}
					}
					else
					{
						value = decimal.Subtract(GlobalForm.nHLC[2, Target[i + num].iTurnEnd], GlobalForm.nHLC[1, Target[i + num].iTurnStart]);
						d = GlobalForm.nHLC[1, Target[i + num].iTurnStart];
						value2 = decimal.Multiply(SigMove, GlobalForm.nHLC[1, Target[i + num].iTurnStart]);
						if (i + num + 1 < Target.Length)
						{
							num6 = decimal.Subtract(GlobalForm.nHLC[1, Target[i + num + 1].iTurnEnd], GlobalForm.nHLC[2, Target[i + num + 1].iTurnStart]);
							d2 = GlobalForm.nHLC[2, Target[i + num + 1].iTurnStart];
						}
						else
						{
							num6 = decimal.Subtract(GlobalForm.nHLC[1, GlobalForm.HLCRange], GlobalForm.nHLC[2, Target[i + num].iTurnEnd]);
							d2 = GlobalForm.nHLC[2, Target[i + num].iTurnEnd];
						}
					}
					string text = Conversions.ToString(Interaction.IIf(decimal.Compare(num6, 0m) < 0, (object)"Down: ", (object)"Up: "));
					ResultsGrid.Rows[ResultsGrid.RowCount - 1].Cells[1].Value = Strings.Format((object)GlobalForm.nDT[0, Target[i].iTurnStart], GlobalForm.UserDate);
					ResultsGrid.Rows[ResultsGrid.RowCount - 1].Cells[2].Value = Strings.Format((object)GlobalForm.nDT[0, Target[i + num].iTurnEnd], GlobalForm.UserDate);
					ResultsGrid.Rows[ResultsGrid.RowCount - 1].Cells[3].Value = text + Strings.Format((object)Math.Abs(num6), "$#,##0.00") + " or " + Strings.Format((object)decimal.Divide(Math.Abs(num6), d2), "0%");
					if (i + num + 1 < Target.Length)
					{
						ResultsGrid.Rows[ResultsGrid.RowCount - 1].Cells[5].Value = Target[i + num + 1].iTurnEnd;
					}
					else
					{
						ResultsGrid.Rows[ResultsGrid.RowCount - 1].Cells[5].Value = GlobalForm.HLCRange;
					}
					string text2 = "";
					if (decimal.Compare(Math.Abs(value), Math.Abs(value2)) > 0)
					{
						text2 = text2 + "The last segment in the pattern trends longer than the benchmark by " + Strings.Format((object)decimal.Divide(Math.Abs(decimal.Subtract(Math.Abs(value), Math.Abs(value2))), d), "#0.0%") + ", suggesting a longer trend coming. ";
						TradesContinued++;
					}
					text2 = text2 + "After the pattern ends, the next move is " + Conversions.ToString(Interaction.IIf(decimal.Compare(num6, 0m) > 0, (object)"up", (object)"down")) + " by " + Strings.Format((object)Math.Abs(num6), "$#,##0.00") + " or " + Strings.Format((object)Math.Abs(decimal.Divide(num6, d2)), "0%");
					ResultsGrid.Rows[ResultsGrid.RowCount - 1].Cells[4].Value = text2;
					TradesTally++;
					if (decimal.Compare(num6, 0m) > 0)
					{
						TradesUp++;
						ref decimal profitUp = ref ProfitUp;
						profitUp = decimal.Add(profitUp, num6);
					}
					else if (decimal.Compare(num6, 0m) < 0)
					{
						TradesDown++;
						ref decimal profitDown = ref ProfitDown;
						profitDown = decimal.Add(profitDown, num6);
					}
					if (decimal.Compare(num6, 0m) != 0)
					{
						BuildSorted(decimal.Divide(decimal.Subtract(Math.Abs(value), Math.Abs(value2)), d), num6, decimal.Divide(num6, d2));
					}
					break;
				}
			}
		}
	}

	public int CountBoxes(decimal StartPrice, decimal EndPrice, int Direction)
	{
		if (decimal.Compare(StartPrice, EndPrice) == 0)
		{
			return 0;
		}
		int num = 0;
		EndPrice = FindBoxPrice(Direction, EndPrice);
		checked
		{
			if (Direction == -1)
			{
				do
				{
					StartPrice = FindTarget(Direction, StartPrice, 1);
					num++;
				}
				while (decimal.Compare(StartPrice, EndPrice) > 0);
			}
			else
			{
				do
				{
					StartPrice = FindTarget(Direction, StartPrice, 1);
					num++;
				}
				while (decimal.Compare(StartPrice, EndPrice) < 0);
			}
			return num;
		}
	}

	private void DisableEnable(bool EnableFlag)
	{
		if (EnableFlag)
		{
			((Control)BrowseButton).Enabled = true;
			((Control)DoneButton).Enabled = true;
			((Control)GraphButton).Enabled = true;
			((Control)HelpButton1).Enabled = true;
			((Control)PreviewButton).Enabled = true;
			((Control)ResetButton).Enabled = true;
			((Control)StartButton).Enabled = true;
			((Control)StopButton).Enabled = false;
			((Control)TipsButton).Enabled = true;
			if (ResultsGrid.RowCount > 0)
			{
				((Control)ClipboardButton).Enabled = true;
				((Control)ResultsButton).Enabled = true;
			}
			else
			{
				((Control)ClipboardButton).Enabled = false;
				((Control)ResultsButton).Enabled = false;
			}
			((Control)Chart1).Enabled = true;
			((Control)DailyRadioButton).Enabled = true;
			((Control)FromDatePicker).Enabled = true;
			((Control)FromRB).Enabled = true;
			((Control)LooseRB).Enabled = true;
			((Control)MonthlyRadioButton).Enabled = true;
			((Control)NormalRB).Enabled = true;
			((Control)PatternFromPicker).Enabled = true;
			((Control)PatternToPicker).Enabled = true;
			((Control)ResultsGrid).Enabled = true;
			((Control)StrictRB).Enabled = true;
			((Control)SymbolTextBox).Enabled = true;
			((Control)ToDatePicker).Enabled = true;
			((Control)ToRB).Enabled = true;
			((Control)WeeklyRadioButton).Enabled = true;
			EnableDisableDWM(DailyRadioButton, WeeklyRadioButton, MonthlyRadioButton);
		}
		else
		{
			((Control)BrowseButton).Enabled = false;
			((Control)ClipboardButton).Enabled = false;
			((Control)DoneButton).Enabled = false;
			((Control)GraphButton).Enabled = false;
			((Control)HelpButton1).Enabled = false;
			((Control)PreviewButton).Enabled = false;
			((Control)ResetButton).Enabled = false;
			((Control)ResultsButton).Enabled = false;
			((Control)StartButton).Enabled = false;
			((Control)StopButton).Enabled = true;
			((Control)TipsButton).Enabled = false;
			((Control)Chart1).Enabled = false;
			((Control)DailyRadioButton).Enabled = false;
			((Control)FromDatePicker).Enabled = false;
			((Control)FromRB).Enabled = false;
			((Control)LooseRB).Enabled = false;
			((Control)MonthlyRadioButton).Enabled = false;
			((Control)NormalRB).Enabled = false;
			((Control)PatternFromPicker).Enabled = false;
			((Control)PatternToPicker).Enabled = false;
			((Control)ResultsGrid).Enabled = false;
			((Control)StrictRB).Enabled = false;
			((Control)SymbolTextBox).Enabled = false;
			((Control)ToDatePicker).Enabled = false;
			((Control)ToRB).Enabled = false;
			((Control)WeeklyRadioButton).Enabled = false;
		}
	}

	public void DisplayProfile(ChartPaintEventArgs e, SigStruct[] ThisProfile)
	{
		//IL_0016: Unknown result type (might be due to invalid IL or missing references)
		//IL_018c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0193: Expected O, but got Unknown
		//IL_019d: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a4: Expected O, but got Unknown
		//IL_01ae: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b5: Expected O, but got Unknown
		if (!(e.ChartElement is Series) || Operators.CompareString(((Series)e.ChartElement).Name, "CandleSeries", false) != 0 || ThisProfile.Length == 0)
		{
			return;
		}
		int num = -1;
		int num2 = 0;
		int j;
		int num3 = default(int);
		int num4;
		bool flag;
		Series val;
		Pen val2;
		Pen val3;
		Pen val4;
		checked
		{
			while (true)
			{
				for (int i = GlobalForm.HLCRange; i >= 0; i += -1)
				{
					if (GlobalForm.IntradayData)
					{
						if ((num == -1) & (DateTime.Compare(GlobalForm.nDT[0, i], GlobalForm.ChartStart) <= 0))
						{
							num = i;
							break;
						}
					}
					else if ((num == -1) & (DateTime.Compare(GlobalForm.nDT[0, i].Date, GlobalForm.ChartStart.Date) <= 0))
					{
						num = i;
						break;
					}
				}
				if (num != -1)
				{
					break;
				}
				if (num2 == 0)
				{
					if (DailyRadioButton.Checked)
					{
						GlobalForm.ChartStart = DateAndTime.DateAdd((DateInterval)4, -1.0, GlobalForm.ChartStart);
					}
					FromDatePicker.Value = GlobalForm.ChartStart;
					num2++;
					continue;
				}
				num = 0;
				break;
			}
			for (j = 0; ThisProfile[j].iTurnStart - num < 0 && j + 1 < Information.UBound((Array)ThisProfile, 1); j++)
			{
			}
			if (ThisProfile[j].iTurnStart - num < 0)
			{
				return;
			}
			if (ShowProfile)
			{
				num3 = -1;
				if (((BaseCollection)ResultsGrid.SelectedRows).Count > 0)
				{
					int i = Conversions.ToInteger(ResultsGrid.SelectedRows[0].Cells[5].Value);
					if (i != -1)
					{
						num3 = i;
					}
				}
			}
			num4 = 0;
			flag = false;
			val = (Series)e.ChartElement;
			val2 = new Pen(Color.Red, 3f);
			val3 = new Pen(Color.Green, 3f);
			val4 = val2;
		}
		PointF absolutePoint = default(PointF);
		PointF pointF = default(PointF);
		foreach (DataPoint item in (Collection<DataPoint>)(object)val.Points)
		{
			if (num4 == checked(num3 - num) && flag)
			{
				val4 = val3;
				absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[Conversions.ToInteger(Interaction.IIf(ThisProfile[j].Move > 0, (object)1, (object)0))]);
				absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)checked(num4 + 1));
				absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				e.ChartGraphics.Graphics.DrawLine(val4, pointF, absolutePoint);
				break;
			}
			if (num4 == checked(ThisProfile[j].iTurnStart - num) && !flag)
			{
				pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[Conversions.ToInteger(Interaction.IIf(ThisProfile[j].Move < 0, (object)1, (object)0))]);
				checked
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num4 + 1));
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					flag = true;
					if (ThisProfile[j].iTurnStart == ThisProfile[j].iTurnEnd)
					{
						j++;
					}
					if (j > Information.UBound((Array)ThisProfile, 1))
					{
						break;
					}
				}
			}
			else if (num4 == checked(ThisProfile[j].iTurnEnd - num) && flag)
			{
				absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[Conversions.ToInteger(Interaction.IIf(ThisProfile[j].Move < 0, (object)1, (object)0))]);
				checked
				{
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num4 + 1));
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					e.ChartGraphics.Graphics.DrawLine(val4, pointF, absolutePoint);
					pointF = absolutePoint;
					if (j + 1 <= Information.UBound((Array)ThisProfile, 1))
					{
						j++;
					}
				}
			}
			num4 = checked(num4 + 1);
		}
		val3.Dispose();
		val2.Dispose();
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	public void EnableDisableDWM(RadioButton Daily, RadioButton Weekly, RadioButton Monthly)
	{
		if (!GlobalForm.IntradayData)
		{
			((Control)Daily).Enabled = true;
			((Control)Weekly).Enabled = true;
			((Control)Monthly).Enabled = true;
		}
		else
		{
			((Control)Daily).Enabled = false;
			((Control)Weekly).Enabled = false;
			((Control)Monthly).Enabled = false;
		}
	}

	private decimal FindBoxPrice(int Direction, decimal Price)
	{
		decimal num;
		if (Direction == 1)
		{
			num = FindBoxSize(1, Price);
			if (decimal.Compare(Price, num) < 0)
			{
				return num;
			}
			Price = decimal.Subtract(Price, decimal.Remainder(Price, num));
			return Price;
		}
		num = FindBoxSize(-1, Price);
		if (decimal.Compare(Price, num) < 0)
		{
			return num;
		}
		if (decimal.Compare(decimal.Remainder(Price, num), 0m) == 0)
		{
			return Price;
		}
		Price = decimal.Add(Price, num);
		Price = decimal.Subtract(Price, decimal.Remainder(Price, num));
		return Price;
	}

	private decimal FindBoxSize(int UpDown, decimal Price)
	{
		int num = Information.UBound((Array)BoxSize, 1);
		for (int i = 0; i <= num; i = checked(i + 1))
		{
			if (UpDown == -1)
			{
				if (decimal.Compare(Price, BoxSize[i, 0]) <= 0)
				{
					return BoxSize[i, 1];
				}
			}
			else if (decimal.Compare(Price, BoxSize[i, 0]) < 0)
			{
				return BoxSize[i, 1];
			}
		}
		return BoxSize[Information.UBound((Array)BoxSize, 1), 1];
	}

	private decimal FindTarget(int Direction, decimal Price, int Boxes)
	{
		if (Direction == 1)
		{
			decimal num = FindBoxPrice(1, Price);
			if (decimal.Compare(num, Price) <= 0 || Boxes == 3)
			{
				Price = num;
				for (int i = 1; i <= Boxes; i = checked(i + 1))
				{
					Price = decimal.Add(Price, FindBoxSize(1, Price));
				}
			}
			decimal num2 = FindBoxSize(1, Price);
			if (decimal.Compare(Price, num2) < 0)
			{
				Price = num2;
			}
		}
		else
		{
			decimal num = FindBoxPrice(-1, Price);
			Price = num;
			for (int j = 1; j <= Boxes; j = checked(j + 1))
			{
				Price = decimal.Subtract(Price, FindBoxSize(-1, Price));
			}
			decimal num2 = FindBoxSize(-1, Price);
			if (decimal.Compare(Price, num2) < 0)
			{
				Price = num2;
			}
		}
		return Price;
	}

	private void GetProfile(int iPatternStart, int iPatternEnd, ref SigStruct[] ProfileArray)
	{
		ProfileArray = null;
		ProfileArray = new SigStruct[1];
		checked
		{
			int num = LinearRegression(iPatternStart - 1);
			decimal d;
			decimal d2;
			decimal startPrice;
			if (num == 1)
			{
				d = FindTarget(1, GlobalForm.nHLC[1, iPatternStart], 1);
				d2 = FindTarget(-1, GlobalForm.nHLC[1, iPatternStart], 3);
				ProfileArray[0].Move = 3;
				startPrice = FindBoxPrice(-1, GlobalForm.nHLC[1, iPatternStart]);
			}
			else
			{
				d = FindTarget(1, GlobalForm.nHLC[2, iPatternStart], 3);
				d2 = FindTarget(-1, GlobalForm.nHLC[2, iPatternStart], 1);
				ProfileArray[0].Move = -3;
				startPrice = FindBoxPrice(-1, GlobalForm.nHLC[2, iPatternStart]);
			}
			ProfileArray[0].iTurnStart = iPatternStart;
			ProfileArray[0].iTurnEnd = iPatternStart;
			ProfileArray[0].Price = GlobalForm.nHLC[3, iPatternStart];
			int num2 = 0;
			for (int i = iPatternStart; i <= iPatternEnd; i++)
			{
				if (num == 1)
				{
					if (decimal.Compare(GlobalForm.nHLC[1, i], d) >= 0)
					{
						d2 = FindTarget(-1, FindBoxPrice(-1, GlobalForm.nHLC[1, i]), 3);
						ProfileArray[num2].Move += CountBoxes(startPrice, GlobalForm.nHLC[1, i], 1);
						ProfileArray[num2].iTurnEnd = i;
						d = FindTarget(1, GlobalForm.nHLC[1, i], 1);
						startPrice = GlobalForm.nHLC[1, i];
						ProfileArray[num2].Price = GlobalForm.nHLC[3, i];
					}
					else if (decimal.Compare(GlobalForm.nHLC[2, i], d2) <= 0)
					{
						num2 = Information.UBound((Array)ProfileArray, 1) + 1;
						d = FindTarget(1, FindBoxPrice(1, GlobalForm.nHLC[2, i]), 3);
						ProfileArray = (SigStruct[])Utils.CopyArray((Array)ProfileArray, (Array)new SigStruct[num2 + 1]);
						ProfileArray[num2].Move -= CountBoxes(startPrice, GlobalForm.nHLC[2, i], -1);
						ProfileArray[num2].iTurnStart = ProfileArray[num2 - 1].iTurnEnd;
						ProfileArray[num2].iTurnEnd = i;
						d2 = FindTarget(-1, GlobalForm.nHLC[2, i], 1);
						num = -1;
						startPrice = GlobalForm.nHLC[2, i];
						ProfileArray[num2].Price = GlobalForm.nHLC[3, i];
					}
				}
				else if (decimal.Compare(GlobalForm.nHLC[2, i], d2) <= 0)
				{
					d = FindTarget(1, FindBoxPrice(1, GlobalForm.nHLC[2, i]), 3);
					ProfileArray[num2].Move -= CountBoxes(startPrice, GlobalForm.nHLC[2, i], -1);
					ProfileArray[num2].iTurnEnd = i;
					d2 = FindTarget(-1, GlobalForm.nHLC[2, i], 1);
					startPrice = GlobalForm.nHLC[2, i];
					ProfileArray[num2].Price = GlobalForm.nHLC[3, i];
				}
				else if (decimal.Compare(GlobalForm.nHLC[1, i], d) >= 0)
				{
					num2 = Information.UBound((Array)ProfileArray, 1) + 1;
					d2 = FindTarget(-1, FindBoxPrice(-1, GlobalForm.nHLC[1, i]), 3);
					ProfileArray = (SigStruct[])Utils.CopyArray((Array)ProfileArray, (Array)new SigStruct[num2 + 1]);
					ProfileArray[num2].Move += CountBoxes(startPrice, GlobalForm.nHLC[1, i], 1);
					ProfileArray[num2].iTurnStart = ProfileArray[num2 - 1].iTurnEnd;
					ProfileArray[num2].iTurnEnd = i;
					d = FindTarget(1, GlobalForm.nHLC[1, i], 1);
					num = 1;
					startPrice = GlobalForm.nHLC[1, i];
					ProfileArray[num2].Price = GlobalForm.nHLC[3, i];
				}
			}
		}
	}

	private void GraphButton_Click(object sender, EventArgs e)
	{
		//IL_0145: Unknown result type (might be due to invalid IL or missing references)
		DateTimePicker fromDatePicker = FromDatePicker;
		DateTime FromDate = fromDatePicker.Value;
		DateTimePicker toDatePicker;
		DateTime ToDate = (toDatePicker = ToDatePicker).Value;
		GlobalForm.SwapDates(ref FromDate, ref ToDate);
		toDatePicker.Value = ToDate;
		fromDatePicker.Value = FromDate;
		PredictionLookBack = checked((int)Math.Round((double)DateAndTime.DateDiff((DateInterval)4, FromDatePicker.Value, ToDatePicker.Value, (FirstDayOfWeek)1, (FirstWeekOfYear)1) / 2.0));
		GlobalForm.FirstPoint = default(Point);
		GlobalForm.LinesList.RemoveAll(StubBoolean);
		if (Operators.CompareString(SymbolTextBox.Text, "", false) == 0)
		{
			SymbolTextBox.Text = lsSymbolTB;
		}
		Filename = SymbolTextBox.Text + ".csv";
		if (!((ServerComputer)MyProject.Computer).FileSystem.FileExists(GlobalForm.OpenPath + "\\" + Filename))
		{
			Filename = SymbolTextBox.Text + ".txt";
			if (!((ServerComputer)MyProject.Computer).FileSystem.FileExists(GlobalForm.OpenPath + "\\" + Filename))
			{
				MessageBox.Show(SymbolMessage, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				Filename = MyProject.Forms.Mainform.ListBox1.SelectedItems[0].ToString();
				((Control)SymbolTextBox).Enabled = true;
				((Control)SymbolTextBox).Focus();
			}
		}
		string filename = Filename;
		ProgressBar ProgBar = LoadingBar;
		Label ErrorLabel = this.ErrorLabel;
		GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
		this.ErrorLabel = ErrorLabel;
		LoadingBar = ProgBar;
		((Form)this).Text = "Forecast Form: " + Filename;
		GlobalForm.SetupDateIndexes(GlobalForm.ChartStart, GlobalForm.ChartEnd);
		GlobalForm.ShowStock(Chart1, GlobalForm.ChartStartIndex, GlobalForm.ChartEndIndex, VolumeFlag: false, MAFlag: false);
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.HelpForecastForm).ShowDialog();
	}

	private int LinearRegression(int iEnd)
	{
		checked
		{
			int num = iEnd - 9;
			if (num < 0)
			{
				return 1;
			}
			decimal num2 = 1m;
			decimal num3 = default(decimal);
			decimal num4 = default(decimal);
			decimal num5 = default(decimal);
			decimal num6 = default(decimal);
			for (int i = num; i <= iEnd; i++)
			{
				decimal d = decimal.Divide(decimal.Add(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 2m);
				num3 = decimal.Add(num3, num2);
				num4 = decimal.Add(num4, d);
				num5 = decimal.Add(num5, decimal.Multiply(num2, num2));
				num6 = decimal.Add(num6, decimal.Multiply(num2, d));
				num2 = decimal.Add(num2, 1m);
			}
			int value = Convert.ToInt32(decimal.Subtract(num2, 1m));
			decimal d2 = ((decimal.Compare(decimal.Subtract(decimal.Multiply(new decimal(value), num5), decimal.Multiply(num3, num3)), 0m) == 0) ? default(decimal) : decimal.Divide(decimal.Subtract(decimal.Multiply(new decimal(value), num6), decimal.Multiply(num3, num4)), decimal.Subtract(decimal.Multiply(new decimal(value), num5), decimal.Multiply(num3, num3))));
			if (decimal.Compare(d2, 0m) < 0)
			{
				return -1;
			}
			return 1;
		}
	}

	private void PatternFromPicker_Validated(object sender, EventArgs e)
	{
		if (!DatePickerLockFlag)
		{
			DatePickerLockFlag = true;
			PatternFromPicker.Value = GlobalForm.FindDate(PatternFromPicker.Value);
			PatternToPicker.Value = GlobalForm.FindDate(PatternToPicker.Value);
			DateTimePicker patternFromPicker = PatternFromPicker;
			DateTime FromDate = patternFromPicker.Value;
			DateTimePicker patternToPicker;
			DateTime ToDate = (patternToPicker = PatternToPicker).Value;
			GlobalForm.SwapDates(ref FromDate, ref ToDate);
			patternToPicker.Value = ToDate;
			patternFromPicker.Value = FromDate;
			DatePickerLockFlag = false;
		}
	}

	private void PreviewButton_Click(object sender, EventArgs e)
	{
		//IL_00b4: Unknown result type (might be due to invalid IL or missing references)
		DateTimePicker patternFromPicker = PatternFromPicker;
		DateTime FromDate = patternFromPicker.Value;
		DateTimePicker patternToPicker;
		DateTime ToDate = (patternToPicker = PatternToPicker).Value;
		GlobalForm.SwapDates(ref FromDate, ref ToDate);
		patternToPicker.Value = ToDate;
		patternFromPicker.Value = FromDate;
		int chartStartIndex = GlobalForm.ChartStartIndex;
		int chartEndIndex = GlobalForm.ChartEndIndex;
		GlobalForm.SetupDateIndexes(PatternFromPicker.Value, PatternToPicker.Value);
		int chartStartIndex2 = GlobalForm.ChartStartIndex;
		int chartEndIndex2 = GlobalForm.ChartEndIndex;
		GlobalForm.ChartStartIndex = chartStartIndex;
		GlobalForm.ChartEndIndex = chartEndIndex;
		GetProfile(chartStartIndex2, chartEndIndex2, ref Signature);
		if (Compact(ref Signature) | (Signature.Length == 0))
		{
			if (Signature.Length == 0)
			{
				MessageBox.Show("Right mouse click different start or end points on the chart to include more price bars in the search. Click Preview to check your work. Forecast works best for patterns with 4 or 5 turns (see Help).", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
			ErrorFlag = true;
			return;
		}
		checked
		{
			SignatureHigh = GlobalForm.nHLC[1, Signature[Signature.Length - 1].iTurnEnd];
			SignatureLow = GlobalForm.nHLC[2, Signature[Signature.Length - 1].iTurnEnd];
			EndSigClose = GlobalForm.nHLC[3, GlobalForm.HLCRange];
			SigFilename = SymbolTextBox.Text.ToUpper();
			SigStart = GlobalForm.nDT[0, Signature[0].iTurnStart];
			SigEnd = GlobalForm.nDT[0, Signature[Signature.Length - 1].iTurnEnd];
			int num = Signature.Length - 1;
			decimal num2 = decimal.Subtract(GlobalForm.nHLC[1, Signature[num].iTurnEnd], GlobalForm.nHLC[2, Signature[num].iTurnStart]);
			decimal num3 = decimal.Subtract(GlobalForm.nHLC[1, Signature[num].iTurnStart], GlobalForm.nHLC[2, Signature[num].iTurnEnd]);
			if (decimal.Compare(Math.Abs(num2), Math.Abs(num3)) > 0)
			{
				SigMove = decimal.Divide(num2, GlobalForm.nHLC[2, Signature[Signature.Length - 1].iTurnStart]);
			}
			else
			{
				SigMove = decimal.Divide(num3, GlobalForm.nHLC[1, Signature[Signature.Length - 1].iTurnStart]);
			}
			PreviewButtonClicked = true;
			Chart1.Invalidate();
		}
	}

	private void ResetButton_Click(object sender, EventArgs e)
	{
		ShowProfile = false;
		PreviewButtonClicked = false;
		if (DateTime.Compare(RestoreStructure.ChartStart, FromDatePicker.MinDate) > 0)
		{
			FromDatePicker.Value = RestoreStructure.ChartStart;
			ToDatePicker.Value = RestoreStructure.ChartEnd;
			PatternFromPicker.Value = RestoreStructure.PatStart;
			PatternToPicker.Value = RestoreStructure.PatEnd;
			SymbolTextBox.Text = RestoreStructure.Symbol;
			Filename = RestoreStructure.sFilename;
			PredictionLookBack = checked((int)DateAndTime.DateDiff((DateInterval)4, FromDatePicker.Value, ToDatePicker.Value, (FirstDayOfWeek)1, (FirstWeekOfYear)1));
			if (PredictionLookBack > RestoreStructure.Predict)
			{
				PredictionLookBack = RestoreStructure.Predict;
			}
			GlobalForm.IntradayData = RestoreStructure.Intraday;
			switch (RestoreStructure.DYMSetting)
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
			}
			DateTimePicker fromDatePicker = FromDatePicker;
			DateTime FromDate = fromDatePicker.Value;
			DateTimePicker toDatePicker;
			DateTime ToDate = (toDatePicker = ToDatePicker).Value;
			GlobalForm.SwapDates(ref FromDate, ref ToDate);
			toDatePicker.Value = ToDate;
			fromDatePicker.Value = FromDate;
			if (GlobalForm.IntradayData)
			{
				GlobalForm.ChartStart = GlobalForm.FindDate(FromDatePicker.Value);
				GlobalForm.ChartEnd = GlobalForm.FindDate(ToDatePicker.Value);
			}
			else
			{
				GlobalForm.ChartStart = GlobalForm.FindDate(FromDatePicker.Value.Date);
				GlobalForm.ChartEnd = GlobalForm.FindDate(ToDatePicker.Value.Date);
			}
			GlobalForm.FirstPoint = default(Point);
			GlobalForm.LinesList.RemoveAll(StubBoolean);
			string filename = Filename;
			ProgressBar ProgBar = LoadingBar;
			Label ErrorLabel = this.ErrorLabel;
			GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
			this.ErrorLabel = ErrorLabel;
			LoadingBar = ProgBar;
			EnableDisableDWM(DailyRadioButton, WeeklyRadioButton, MonthlyRadioButton);
			((Form)this).Text = "Forecast Form: " + Filename;
			GlobalForm.SetupDateIndexes(GlobalForm.ChartStart, GlobalForm.ChartEnd);
			GlobalForm.ShowStock(Chart1, GlobalForm.ChartStartIndex, GlobalForm.ChartEndIndex, VolumeFlag: false, MAFlag: false);
			ShowProfile = true;
			PreviewButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		}
	}

	private void ResultsButton_Click(object sender, EventArgs e)
	{
		//IL_0063: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c0f: Unknown result type (might be due to invalid IL or missing references)
		if (ResultsGrid.RowCount == 0)
		{
			string text = "There are no results to discuss. Try these suggestions.\r\n\r\n1. Have you selected plenty of files to compare against? If not, return to the Main Form and click the Select All button.";
			text += "\r\n\r\n2. RIGHT mouse click two different price bars on the chart to highlight a pattern you wish to find in other stocks. Click Preview.";
			text += " Preview will show the pattern, if any. You're looking for a pattern with about 3-7 segments, depending on the Rules selected (Strict, Normal, Loose). If a pattern is too complex, it";
			text += " won't be found. Too simple, and you'll get too many hits.";
			if (StrictRB.Checked)
			{
				text += "\r\n\r\n3. Try selecting Loose or Normal radio button instead of Strict and click Preview or Start.";
			}
			MessageBox.Show(text, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			return;
		}
		checked
		{
			decimal[] array = new decimal[Sorted.Length - 1 + 1];
			Array.Copy(Sorted, array, Sorted.Length);
			if (array.Length > 1 && Convert.ToDouble(array[array.Length - 1]) == 0.01)
			{
				array = (decimal[])Utils.CopyArray((Array)array, (Array)new decimal[array.Length - 2 + 1]);
			}
			decimal num = default(decimal);
			if (array.Length > 1)
			{
				Array.Sort(array);
				num = (((double)array.Length / 2.0 == Conversion.Int((double)array.Length / 2.0)) ? decimal.Divide(decimal.Add(array[(int)Math.Round((double)array.Length / 2.0)], array[(int)Math.Round((double)array.Length / 2.0) - 1]), 2m) : array[(int)Math.Round((double)array.Length / 2.0)]);
			}
			else if (array.Length == 1)
			{
				num = array[0];
			}
			decimal[] array2 = new decimal[NextPercentSorted.Length - 1 + 1];
			Array.Copy(NextPercentSorted, array2, NextPercentSorted.Length);
			decimal[] array3 = new decimal[NextSorted.Length - 1 + 1];
			Array.Copy(NextSorted, array3, NextSorted.Length);
			if (array3.Length > 1 && Convert.ToDouble(array3[array3.Length - 1]) == 0.01)
			{
				ref decimal[] nextSorted = ref NextSorted;
				nextSorted = (decimal[])Utils.CopyArray((Array)nextSorted, (Array)new decimal[NextSorted.Length - 2 + 1]);
				array3 = (decimal[])Utils.CopyArray((Array)array3, (Array)new decimal[array3.Length - 2 + 1]);
				ref decimal[] nextPercentSorted = ref NextPercentSorted;
				nextPercentSorted = (decimal[])Utils.CopyArray((Array)nextPercentSorted, (Array)new decimal[NextPercentSorted.Length - 2 + 1]);
				array2 = (decimal[])Utils.CopyArray((Array)array2, (Array)new decimal[array2.Length - 2 + 1]);
			}
			decimal num2 = default(decimal);
			decimal num3 = default(decimal);
			if (array3.Length > 1)
			{
				Array.Sort(array3, array2);
				if ((double)array3.Length / 2.0 != Conversion.Int((double)array3.Length / 2.0))
				{
					num2 = array3[(int)Math.Round((double)array3.Length / 2.0)];
					num3 = array2[(int)Math.Round((double)array2.Length / 2.0)];
				}
				else
				{
					num2 = decimal.Divide(decimal.Add(array3[(int)Math.Round((double)array3.Length / 2.0)], array3[(int)Math.Round((double)array3.Length / 2.0) - 1]), 2m);
					num3 = decimal.Divide(decimal.Add(array2[(int)Math.Round((double)array2.Length / 2.0)], array2[(int)Math.Round((double)array2.Length / 2.0) - 1]), 2m);
				}
			}
			else if (array3.Length == 1)
			{
				num2 = array3[0];
				num3 = array2[0];
			}
			if (Signature.Length > 0)
			{
				ResultsMessage = "Results for " + SigFilename + " from " + Strings.Format((object)SigStart, GlobalForm.UserDate) + " to " + Strings.Format((object)SigEnd, GlobalForm.UserDate) + "\r\n";
				ref string resultsMessage = ref ResultsMessage;
				resultsMessage = resultsMessage + "     Pattern's ending high: " + Strings.Format((object)SignatureHigh, "$#,##0.00") + "\r\n";
				ref string resultsMessage2 = ref ResultsMessage;
				resultsMessage2 = resultsMessage2 + "     Pattern's ending low: " + Strings.Format((object)SignatureLow, "$#,##0.00") + "\r\n";
				ref string resultsMessage3 = ref ResultsMessage;
				resultsMessage3 = resultsMessage3 + "     Stock's current close: " + Strings.Format((object)EndSigClose, "$#,##0.00") + "\r\n";
				ResultsMessage += "\r\n";
				ref string resultsMessage4 = ref ResultsMessage;
				resultsMessage4 = resultsMessage4 + "Number of patterns found: " + Strings.Format((object)(TradesUp + TradesDown), "") + "\r\n\r\n";
				TargetContinue = default(decimal);
				if (TradesContinued > 0)
				{
					ref string resultsMessage5 = ref ResultsMessage;
					ref string reference = ref resultsMessage5;
					resultsMessage5 = reference + "The last segment in the pattern has a trend longer than the benchmark pattern " + Strings.Format((object)((double)TradesContinued / (double)TradesTally), "0%") + " of the time (or " + Strings.Format((object)TradesContinued, "") + " out of " + Strings.Format((object)TradesTally, "") + " trades).\r\n";
					ref string resultsMessage6 = ref ResultsMessage;
					reference = ref resultsMessage6;
					resultsMessage6 = reference + "     " + SigFilename + " may continue trending " + Conversions.ToString(Interaction.IIf(TradesUp > TradesDown, (object)"lower", (object)"higher")) + " by a median of " + Strings.Format((object)num, "0%") + " before reversing.\r\n";
					TargetContinue = Conversions.ToDecimal(Interaction.IIf(TradesUp < TradesDown, (object)decimal.Multiply(decimal.Add(1m, num), SignatureHigh), (object)decimal.Multiply(decimal.Subtract(1m, num), SignatureLow)));
					ref string resultsMessage7 = ref ResultsMessage;
					resultsMessage7 = resultsMessage7 + "     CONTINUATION TARGET: " + Strings.Format((object)TargetContinue, "$#,##0.00");
					ref string resultsMessage8 = ref ResultsMessage;
					resultsMessage8 = resultsMessage8 + " measured from pattern's ending " + Conversions.ToString(Interaction.IIf(TradesUp < TradesDown, (object)"high", (object)"low")) + ".\r\n\r\n";
					if (Convert.ToDouble(Math.Abs(num)) > 0.2)
					{
						ResultsMessage += "\r\n* WARNING: I consider moves greater than 20% as unrealistic. They can still happen, but it's unlikely. *\r\n\r\n";
					}
				}
				TargetUp1 = default(decimal);
				TargetDown1 = default(decimal);
				TargetUp2 = default(decimal);
				TargetDown2 = default(decimal);
				if (TradesUp > TradesDown)
				{
					ResultsMessage += "After the pattern ends, trends reversing from down to up:\r\n";
					ref string resultsMessage9 = ref ResultsMessage;
					resultsMessage9 = resultsMessage9 + "     Number of trades: " + Strings.Format((object)TradesUp, "") + "\r\n";
					ref string resultsMessage10 = ref ResultsMessage;
					resultsMessage10 = resultsMessage10 + "     Average gain: " + Strings.Format((object)decimal.Divide(ProfitUp, new decimal(TradesUp)), "$#,##0.00") + "\r\n";
					ref string resultsMessage11 = ref ResultsMessage;
					ref string reference = ref resultsMessage11;
					resultsMessage11 = reference + "     Median gain: " + Strings.Format((object)num2, "$#,##0.00") + " or " + Strings.Format((object)num3, "0%") + "\r\n";
					if ((decimal.Compare(TargetContinue, 0m) != 0) & ((double)TradesContinued / (double)TradesTally >= 0.5))
					{
						TargetUp1 = decimal.Multiply(decimal.Add(1m, num3), TargetContinue);
						ref string resultsMessage12 = ref ResultsMessage;
						reference = ref resultsMessage12;
						resultsMessage12 = reference + "     Reversal target 1 for " + SigFilename + " (measured from CONTINUATION TARGET): " + Strings.Format((object)TargetUp1, "$#,##0.00") + "\r\n";
					}
					TargetUp2 = decimal.Multiply(decimal.Add(1m, num3), SignatureLow);
					ref string resultsMessage13 = ref ResultsMessage;
					reference = ref resultsMessage13;
					resultsMessage13 = reference + "     Reversal target 2 for " + SigFilename + " (measured from pattern's ending low): " + Strings.Format((object)TargetUp2, "$#,##0.00") + "\r\n";
					ResultsMessage += "\r\n";
				}
				else if (TradesDown > 0)
				{
					ResultsMessage += "After the pattern ends, trends reversing from up to down:\r\n";
					ref string resultsMessage14 = ref ResultsMessage;
					resultsMessage14 = resultsMessage14 + "     Number of trades: " + Strings.Format((object)TradesDown, "") + "\r\n";
					ref string resultsMessage15 = ref ResultsMessage;
					resultsMessage15 = resultsMessage15 + "     Average loss: " + Strings.Format((object)decimal.Divide(Math.Abs(ProfitDown), new decimal(TradesDown)), "$#,##0.00") + "\r\n";
					ref string resultsMessage16 = ref ResultsMessage;
					ref string reference = ref resultsMessage16;
					resultsMessage16 = reference + "     Median loss: " + Strings.Format((object)Math.Abs(num2), "$#,##0.00") + " or " + Strings.Format((object)Math.Abs(num3), "0%") + "\r\n";
					if ((decimal.Compare(TargetContinue, 0m) != 0) & ((double)TradesContinued / (double)TradesTally >= 0.5))
					{
						TargetDown1 = decimal.Multiply(decimal.Add(1m, num3), TargetContinue);
						ref string resultsMessage17 = ref ResultsMessage;
						reference = ref resultsMessage17;
						resultsMessage17 = reference + "     Reversal target 1 for " + SigFilename + " (measured from CONTINUATION TARGET): " + Strings.Format((object)TargetDown1, "$#,##0.00") + "\r\n";
					}
					TargetDown2 = decimal.Multiply(decimal.Add(1m, num3), SignatureHigh);
					ref string resultsMessage18 = ref ResultsMessage;
					reference = ref resultsMessage18;
					resultsMessage18 = reference + "     Reversal target 2 for " + SigFilename + " (measured from pattern's ending high): " + Strings.Format((object)TargetDown2, "$#,##0.00") + "\r\n";
					ResultsMessage += "\r\n";
				}
				if (Convert.ToDouble(Math.Abs(num3)) > 0.2)
				{
					ResultsMessage += "\r\n* WARNING: I consider moves greater than 20% as unrealistic. They can still happen, but it's unlikely. *\r\n";
				}
			}
			ResultsMessage += "\r\n";
			ResultsMessage += "DISCLAIMER: Past performance is no guarantee of future results. You and you alone are responsible for your investment decisions. Do not depend on the information provided by Patternz";
			ResultsMessage += " to be accurate or correct. Read the software license for more information (Main Form, Help menu option near form top, License menu item).";
			MessageBox.Show(ResultsMessage, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)0);
			Chart1.Invalidate();
		}
	}

	private void ResultsGrid_RowEnter(object sender, DataGridViewCellEventArgs e)
	{
		PreviewButtonClicked = false;
		GlobalForm.FirstPoint = default(Point);
		GlobalForm.LinesList.RemoveAll(StubBoolean);
		if (!((e.RowIndex != -1) & !LockFlag))
		{
			return;
		}
		GlobalForm.Quiet = true;
		Filename = Conversions.ToString(ResultsGrid.Rows[e.RowIndex].Cells[0].Value);
		checked
		{
			if (Filename != null)
			{
				((Form)this).Text = "Forecast Form: " + Filename;
				SymbolTextBox.Text = Strings.Left(Filename, Strings.InStrRev(Filename, ".", -1, (CompareMethod)0) - 1);
				string filename = Filename;
				ProgressBar ProgBar = LoadingBar;
				Label ErrorLabel = this.ErrorLabel;
				bool num = GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
				this.ErrorLabel = ErrorLabel;
				LoadingBar = ProgBar;
				if (!num)
				{
					EnableDisableDWM(DailyRadioButton, WeeklyRadioButton, MonthlyRadioButton);
					GridClicked = true;
					PatternFromPicker.Value = Conversions.ToDate(ResultsGrid.Rows[e.RowIndex].Cells[1].Value);
					FromDatePicker.Value = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)4, (double)(-PredictionLookBack), PatternFromPicker.Value));
					PatternToPicker.Value = Conversions.ToDate(ResultsGrid.Rows[e.RowIndex].Cells[2].Value);
					ToDatePicker.Value = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)4, (double)PredictionLookBack, PatternToPicker.Value));
					if (DateTime.Compare(ToDatePicker.Value, DateAndTime.Now) > 0)
					{
						ToDatePicker.Value = DateAndTime.Now;
					}
					GlobalForm.SetupDateIndexes(PatternFromPicker.Value, PatternToPicker.Value);
					GetProfile(GlobalForm.ChartStartIndex, GlobalForm.ChartEndIndex, ref Profile);
					Compact(ref Profile);
					if (GlobalForm.IntradayData)
					{
						GlobalForm.ChartStart = FromDatePicker.Value;
						GlobalForm.ChartEnd = ToDatePicker.Value;
					}
					else
					{
						GlobalForm.ChartStart = FromDatePicker.Value.Date;
						GlobalForm.ChartEnd = ToDatePicker.Value.Date;
					}
					GlobalForm.CheckDates(FromDatePicker, ToDatePicker);
					ShowProfile = true;
					GlobalForm.ShowStock(Chart1, FromDatePicker.Value, ToDatePicker.Value, VolumeFlag: false, MAFlag: false);
				}
			}
			GlobalForm.Quiet = false;
		}
	}

	private void StartButton_Click(object sender, EventArgs e)
	{
		ErrorFlag = false;
		ShowProfile = false;
		PatternFromPicker.Value = PatternFromPicker.Value;
		PatternToPicker.Value = PatternToPicker.Value;
		FromDatePicker.Value = FromDatePicker.Value;
		ToDatePicker.Value = ToDatePicker.Value;
		DateTimePicker patternFromPicker = PatternFromPicker;
		DateTime FromDate = patternFromPicker.Value;
		DateTimePicker patternToPicker;
		DateTime ToDate = (patternToPicker = PatternToPicker).Value;
		GlobalForm.SwapDates(ref FromDate, ref ToDate);
		patternToPicker.Value = ToDate;
		patternFromPicker.Value = FromDate;
		ResultsGrid.RowCount = 0;
		StopPressed = false;
		((Control)StopButton).Focus();
		ResultsMessage = "";
		Sorted = null;
		Sorted = new decimal[1];
		NextSorted = null;
		NextSorted = new decimal[1];
		NextPercentSorted = null;
		NextPercentSorted = new decimal[1];
		TradesContinued = 0;
		TradesTally = 0;
		RestoreStructure.ChartStart = FromDatePicker.Value;
		RestoreStructure.ChartEnd = ToDatePicker.Value;
		RestoreStructure.PatStart = PatternFromPicker.Value;
		RestoreStructure.PatEnd = PatternToPicker.Value;
		RestoreStructure.Symbol = SymbolTextBox.Text;
		RestoreStructure.sFilename = Filename;
		RestoreStructure.Predict = PredictionLookBack;
		RestoreStructure.Intraday = GlobalForm.IntradayData;
		RestoreStructure.DYMSetting = GlobalForm.GetOptions((Form)(object)this);
		bool flag = true;
		int num = default(int);
		if (flag == LooseRB.Checked)
		{
			num = RLOOSE;
		}
		else if (flag == NormalRB.Checked)
		{
			num = RNORMAL;
		}
		else if (flag == StrictRB.Checked)
		{
			num = RSTRICT;
		}
		Settings.Rules = num;
		bool flag2 = true;
		if (flag2 == DailyRadioButton.Checked)
		{
			num = 0;
		}
		else if (flag2 == WeeklyRadioButton.Checked)
		{
			num = 1;
		}
		else if (flag2 == MonthlyRadioButton.Checked)
		{
			num = 2;
		}
		Settings.DWM = num;
		string filename = Filename;
		PreviewButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		if (ErrorFlag)
		{
			return;
		}
		DisableEnable(EnableFlag: false);
		((Control)StopButton).Enabled = true;
		PatternLabel.Text = "Pattern count: 0";
		((Control)PatternLabel).Refresh();
		FindingBar.Maximum = MyProject.Forms.Mainform.ListBox1.SelectedItems.Count;
		LockFlag = true;
		TradesUp = 0;
		TradesDown = 0;
		ProfitUp = default(decimal);
		ProfitDown = default(decimal);
		GlobalForm.Quiet = true;
		ResultsGrid.RowHeadersVisible = false;
		ResultsGrid.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)1;
		checked
		{
			int num2 = MyProject.Forms.Mainform.ListBox1.SelectedItems.Count - 1;
			ProgressBar ProgBar;
			Label ErrorLabel;
			for (int i = 0; i <= num2; i++)
			{
				Filename = MyProject.Forms.Mainform.ListBox1.SelectedItems[i].ToString();
				if (!((Operators.CompareString(Filename.ToUpper(), (SymbolTextBox.Text + ".csv").ToUpper(), false) != 0) & (Operators.CompareString(Filename.ToUpper(), (SymbolTextBox.Text + ".txt").ToUpper(), false) != 0)))
				{
					continue;
				}
				StockLabel.Text = Filename;
				((Control)StockLabel).Refresh();
				string filename2 = Filename;
				ProgBar = LoadingBar;
				ErrorLabel = this.ErrorLabel;
				bool num3 = GlobalForm.LoadFile(filename2, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
				this.ErrorLabel = ErrorLabel;
				LoadingBar = ProgBar;
				if (!num3)
				{
					GetProfile(0, GlobalForm.HLCRange, ref Profile);
					if (!Compact(ref Profile))
					{
						CompareResults(Signature, ref Profile);
					}
				}
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				if (StopPressed)
				{
					break;
				}
				FindingBar.Value = i;
			}
			ResultsGrid.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)6;
			ResultsGrid.RowHeadersVisible = true;
			GlobalForm.Quiet = false;
			LockFlag = false;
			FindingBar.Value = 0;
			StockLabel.Text = "";
			Filename = filename;
			string filename3 = Filename;
			ProgBar = LoadingBar;
			ErrorLabel = this.ErrorLabel;
			GlobalForm.LoadFile(filename3, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
			this.ErrorLabel = ErrorLabel;
			LoadingBar = ProgBar;
			ResultsButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			if (ResultsGrid.RowCount > 0)
			{
				((Control)ClipboardButton).Enabled = true;
			}
			else
			{
				((Control)ClipboardButton).Enabled = false;
			}
			DisableEnable(EnableFlag: true);
		}
	}

	private void StopButton_Click(object sender, EventArgs e)
	{
		StopPressed = true;
		Interaction.Beep();
	}

	private bool StubBoolean(GlobalForm.LineEndPoints sPoint)
	{
		return true;
	}

	private void TipsButton_Click(object sender, EventArgs e)
	{
		//IL_007b: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat("Use a number of stocks in the search (I use about 500. Shorter files process faster). On the Main Form, click Select All to use all stocks in the search (except the symbol listed in the Symbol text box).\r\n\r\n" + "Right mouse click two price bars, one on the far right and one on the far left of the chart. Click Preview. If you don't see a red pattern, then adjust the chart's From date to include more data. Otherwise you ", "should see a waveform. Count the segments starting from the right (most recent) to the left. When you get to 3, the 3 segments might be a good pattern to use for Strict rules. Click Strict, and the Start radio button (in Find Pattern near the grid) then right mouse click on the price bar where the third segment begins. "), "Four or 5 segments work well for Normal rules and 6 to 8 work well for loose rules.\r\n\r\n"), "Click Help to see an example.\r\n\r\n"), "After clicking Start, if the program finds no patterns, then adjust the Rules options (Strict, Normal, Loose) and try again (or use fewer segments in the pattern).\r\n\r\n"), "Forecasts are short-term, often valuable for two weeks to a month.\r\n\r\n"), "Small moves in the stock are ignored which is why the end points you clicked on the chart may not match where the pattern starts or ends.\r\n\r\n"), "After a successful run, two targets may appear: The Continue Target appears only if the existing trend (the last segment in the pattern) continues trending. The Reversal Target appears after a reversal. Both may not appear if off the scale.\r\n\r\n"), "Play with the forecast (by changing pattern start date, end date, or Rules) and compare to actual behavior to learn when the forecast works best.\r\n\r\n"), "Use with daily price data that bounces around. It's not recommended for intraday, weekly, or monthly data, but you can try it.\r\n\r\n"), "Past performance is no guarantee of future results. The forecast is not always correct. All numbers are approximate. YOU AND YOU ALONE ARE RESPONSIBLE FOR YOUR INVESTMENT OR TRADING DECISIONS."), "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void ToDatePicker_Validated(object sender, EventArgs e)
	{
		if (!DatePickerLockFlag)
		{
			DatePickerLockFlag = true;
			FromDatePicker.Value = GlobalForm.FindDate(FromDatePicker.Value);
			ToDatePicker.Value = GlobalForm.FindDate(ToDatePicker.Value);
			DateTimePicker fromDatePicker = FromDatePicker;
			DateTime FromDate = fromDatePicker.Value;
			DateTimePicker toDatePicker;
			DateTime ToDate = (toDatePicker = ToDatePicker).Value;
			GlobalForm.SwapDates(ref FromDate, ref ToDate);
			toDatePicker.Value = ToDate;
			fromDatePicker.Value = FromDate;
			if (GlobalForm.IntradayData)
			{
				GlobalForm.ChartStart = GlobalForm.FindDate(FromDatePicker.Value);
				GlobalForm.ChartEnd = GlobalForm.FindDate(ToDatePicker.Value);
			}
			else
			{
				GlobalForm.ChartStart = FromDatePicker.Value.Date;
				GlobalForm.ChartEnd = ToDatePicker.Value.Date;
			}
			DatePickerLockFlag = false;
		}
	}

	private void WeeklyRadioButton_CheckedChanged(object sender, EventArgs e)
	{
		if (GlobalForm.IntradayData)
		{
			return;
		}
		RadioButton val = (RadioButton)((sender is RadioButton) ? sender : null);
		if (val != null && (val.Checked & (((ButtonBase)val).Text.Length > 0)))
		{
			switch (Conversions.ToInteger(((Control)val).Tag))
			{
			case 0:
				DWM = 0;
				break;
			case 1:
				DWM = 1;
				break;
			case 2:
				DWM = 2;
				break;
			}
			GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		}
	}
}
