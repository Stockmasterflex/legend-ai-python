using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.Runtime.CompilerServices;
using System.Runtime.Serialization.Formatters.Binary;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Microsoft.VisualBasic.Devices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class SimulatorForm : Form
{
	private struct BuySellStruct
	{
		public bool InProgress;

		public bool TradeReady;

		public bool tShort;

		public int UpBreakoutDirection;

		public decimal BuyPrice;

		public DateTime BuyDate;

		public int iBuy;

		public int iBkout;

		public decimal SellPrice;

		public DateTime SellDate;

		public int iSell;

		public int Shares;

		public decimal Fees;

		public decimal Commissions;

		public decimal PriceTarget;

		public decimal PriceStop;

		public int BuyStatus;

		public int SellStatus;

		public DateTime UltHighDate;

		public int iUltHigh;

		public DateTime UltLowDate;

		public int iUltLow;
	}

	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("CandlesButton")]
	private Button _CandlesButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PatternsButton")]
	private Button _PatternsButton;

	[CompilerGenerated]
	[AccessedThroughProperty("NextButton")]
	private Button _NextButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PreviousButton")]
	private Button _PreviousButton;

	[CompilerGenerated]
	[AccessedThroughProperty("Chart1")]
	private Chart _Chart1;

	[CompilerGenerated]
	[AccessedThroughProperty("StartButton")]
	private Button _StartButton;

	[CompilerGenerated]
	[AccessedThroughProperty("Timer1")]
	private Timer _Timer1;

	[CompilerGenerated]
	[AccessedThroughProperty("ResumeButton")]
	private Button _ResumeButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StopButton")]
	private Button _StopButton;

	[CompilerGenerated]
	[AccessedThroughProperty("SpeedSB")]
	private HScrollBar _SpeedSB;

	[CompilerGenerated]
	[AccessedThroughProperty("SellButton")]
	private Button _SellButton;

	[CompilerGenerated]
	[AccessedThroughProperty("BuyButton")]
	private Button _BuyButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ClipboardButton")]
	private Button _ClipboardButton;

	[CompilerGenerated]
	[AccessedThroughProperty("FindDGV")]
	private DataGridView _FindDGV;

	[CompilerGenerated]
	[AccessedThroughProperty("SimulatorHelpButton")]
	private Button _SimulatorHelpButton;

	[CompilerGenerated]
	[AccessedThroughProperty("SetupButton")]
	private Button _SetupButton;

	[CompilerGenerated]
	[AccessedThroughProperty("HelpTradeButton")]
	private Button _HelpTradeButton;

	[CompilerGenerated]
	[AccessedThroughProperty("SetTargetsButton")]
	private Button _SetTargetsButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ClearBtn")]
	private Button _ClearBtn;

	[CompilerGenerated]
	[AccessedThroughProperty("SkipCB")]
	private CheckBox _SkipCB;

	[CompilerGenerated]
	[AccessedThroughProperty("StopSkip")]
	private Button _StopSkip;

	[CompilerGenerated]
	[AccessedThroughProperty("PercentButton")]
	private Button _PercentButton;

	private const string KEYSIM = "SimulatorForm";

	private const int INITSPEED = 1500;

	private const double AXISMAX = 1.001;

	private const double AXISMIN = 0.999;

	private const int DEFLOOKBACK = 262;

	private const decimal DEFCOMMISSIONS = 4.95m;

	private const int dgvNAME = 0;

	private const int dgvSTART = 1;

	private const int dgvEND = 2;

	private const int sPROFIT = 0;

	private const int sBUYPRICE = 1;

	private const int sBUYDATE = 2;

	private const int sSELLPRICE = 3;

	private const int sSELLDATE = 4;

	private const int sSHARES = 5;

	private const int sFEES = 6;

	private const int sLONGSHORT = 7;

	private const int sTARGET = 8;

	private const int sSTOP = 9;

	private const int sSTATUS = 10;

	private const int sSYMBOL = 11;

	private const int sPATTERN = 12;

	private const int sULTHIGH = 13;

	private const int sULTHIGHDATE = 14;

	private const int sULTLOW = 15;

	private const int sULTLOWDATE = 16;

	private const int sENTRYPERFECT = 17;

	private const int sEXITPERFECT = 18;

	private const int sCOLUMNCOUNT = 19;

	private const int TSSTOPPEDOUT = 1;

	private const int TSTARGET = 2;

	private const int TSBUYPRICE = 3;

	private const int TSLIMITBUY = 4;

	private const int TSLIMITSELL = 5;

	private const int TSMANUAL = 6;

	private const int TSDATAOUT = 7;

	private BuySellStruct Trade;

	private string Filename;

	private string PatternName;

	private decimal StkMin;

	private decimal StkMax;

	private long VolMax;

	private CalloutAnnotation CurrentAnnotation;

	private bool TimerRunFlag;

	private bool StopPressed;

	private Point StartPoint;

	private Point EndPoint;

	private bool Crosshair;

	private Point CrosshairPoint;

	private Pen CrosshairPen;

	private int DataPointsCount;

	private int lsShares;

	private bool lsPatternTargets;

	private int PatternIndex;

	private GlobalForm.SimStruct GlobalStorage;

	private string ConfigPath;

	private decimal MovAvg;

	private decimal Alpha;

	private decimal EMAYesterday;

	private bool EMASeed;

	private int lsPauseSimulator;

	private bool SilentMode;

	private bool bStopSkip;

	private bool LockFlag;

	private Font BoldFont;

	private Pen MyPen;

	private PointF HighPoint;

	private PointF LowPoint;

	private bool HighTrigger;

	private bool LowTrigger;

	private bool PercentCircles;

	private bool ResetPctDownTrade;

	private bool ResetPctUpTrade;

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

	internal virtual Button CandlesButton
	{
		[CompilerGenerated]
		get
		{
			return _CandlesButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CandlesButton_Click;
			Button val = _CandlesButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_CandlesButton = value;
			val = _CandlesButton;
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

	[field: AccessedThroughProperty("LoadingBar")]
	internal virtual ProgressBar LoadingBar
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("BuySellDGV")]
	internal virtual DataGridView BuySellDGV
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

	internal virtual Button NextButton
	{
		[CompilerGenerated]
		get
		{
			return _NextButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = NextButton_Click;
			Button val = _NextButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_NextButton = value;
			val = _NextButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button PreviousButton
	{
		[CompilerGenerated]
		get
		{
			return _PreviousButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PreviousButton_Click;
			Button val = _PreviousButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_PreviousButton = value;
			val = _PreviousButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("DoneButton")]
	internal virtual Button DoneButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

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

	internal virtual Button ResumeButton
	{
		[CompilerGenerated]
		get
		{
			return _ResumeButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ResumeButton_Click;
			Button val = _ResumeButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ResumeButton = value;
			val = _ResumeButton;
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

	internal virtual HScrollBar SpeedSB
	{
		[CompilerGenerated]
		get
		{
			return _SpeedSB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0007: Unknown result type (might be due to invalid IL or missing references)
			//IL_000d: Expected O, but got Unknown
			ScrollEventHandler val = new ScrollEventHandler(SpeedSB_Scroll);
			HScrollBar val2 = _SpeedSB;
			if (val2 != null)
			{
				((ScrollBar)val2).Scroll -= val;
			}
			_SpeedSB = value;
			val2 = _SpeedSB;
			if (val2 != null)
			{
				((ScrollBar)val2).Scroll += val;
			}
		}
	}

	[field: AccessedThroughProperty("Label6")]
	internal virtual Label Label6
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

	[field: AccessedThroughProperty("FindPanel")]
	internal virtual Panel FindPanel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Panel3")]
	internal virtual Panel Panel3
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

	[field: AccessedThroughProperty("RadioButton2")]
	internal virtual RadioButton RadioButton2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RadioButton1")]
	internal virtual RadioButton RadioButton1
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

	internal virtual Button SellButton
	{
		[CompilerGenerated]
		get
		{
			return _SellButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SellButton_Click;
			Button val = _SellButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_SellButton = value;
			val = _SellButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button BuyButton
	{
		[CompilerGenerated]
		get
		{
			return _BuyButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BuyButton_Click;
			Button val = _BuyButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_BuyButton = value;
			val = _BuyButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("MessageLabel")]
	internal virtual Label MessageLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label10")]
	internal virtual Label Label10
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
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

	internal virtual DataGridView FindDGV
	{
		[CompilerGenerated]
		get
		{
			return _FindDGV;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0007: Unknown result type (might be due to invalid IL or missing references)
			//IL_000d: Expected O, but got Unknown
			//IL_0014: Unknown result type (might be due to invalid IL or missing references)
			//IL_001a: Expected O, but got Unknown
			DataGridViewCellEventHandler val = new DataGridViewCellEventHandler(FindDGV_CellClick);
			DataGridViewCellEventHandler val2 = new DataGridViewCellEventHandler(FindDGV_RowEnter);
			DataGridView val3 = _FindDGV;
			if (val3 != null)
			{
				val3.CellClick -= val;
				val3.RowEnter -= val2;
			}
			_FindDGV = value;
			val3 = _FindDGV;
			if (val3 != null)
			{
				val3.CellClick += val;
				val3.RowEnter += val2;
			}
		}
	}

	[field: AccessedThroughProperty("Column1")]
	internal virtual DataGridViewTextBoxColumn Column1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Column2")]
	internal virtual DataGridViewTextBoxColumn Column2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Column3")]
	internal virtual DataGridViewTextBoxColumn Column3
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button SimulatorHelpButton
	{
		[CompilerGenerated]
		get
		{
			return _SimulatorHelpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SimulatorHelpButton_Click;
			Button val = _SimulatorHelpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_SimulatorHelpButton = value;
			val = _SimulatorHelpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button SetupButton
	{
		[CompilerGenerated]
		get
		{
			return _SetupButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SetupButton_Click;
			Button val = _SetupButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_SetupButton = value;
			val = _SetupButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button HelpTradeButton
	{
		[CompilerGenerated]
		get
		{
			return _HelpTradeButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = HelpTradeButton_Click;
			Button val = _HelpTradeButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_HelpTradeButton = value;
			val = _HelpTradeButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button SetTargetsButton
	{
		[CompilerGenerated]
		get
		{
			return _SetTargetsButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SetTargetsButton_Click;
			Button val = _SetTargetsButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_SetTargetsButton = value;
			val = _SetTargetsButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("StopPriceNum")]
	internal virtual NumericUpDown StopPriceNum
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("TargetNum")]
	internal virtual NumericUpDown TargetNum
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("SharesNum")]
	internal virtual NumericUpDown SharesNum
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("BuyPriceNum")]
	internal virtual NumericUpDown BuyPriceNum
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("ShortSaleCB")]
	internal virtual CheckBox ShortSaleCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("LimitOrderCB")]
	internal virtual CheckBox LimitOrderCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button ClearBtn
	{
		[CompilerGenerated]
		get
		{
			return _ClearBtn;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ClearBtn_Click;
			Button val = _ClearBtn;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ClearBtn = value;
			val = _ClearBtn;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual CheckBox SkipCB
	{
		[CompilerGenerated]
		get
		{
			return _SkipCB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SkipCB_CheckedChanged;
			CheckBox val = _SkipCB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_SkipCB = value;
			val = _SkipCB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual Button StopSkip
	{
		[CompilerGenerated]
		get
		{
			return _StopSkip;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = StopSkip_Click;
			Button val = _StopSkip;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_StopSkip = value;
			val = _StopSkip;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button PercentButton
	{
		[CompilerGenerated]
		get
		{
			return _PercentButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PercentButton_Click;
			Button val = _PercentButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_PercentButton = value;
			val = _PercentButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	public SimulatorForm()
	{
		//IL_003d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0047: Expected O, but got Unknown
		((Form)this).Closing += SimulatorForm_Closing;
		((Form)this).Load += SimulatorForm_Load;
		((Form)this).Activated += SimulatorForm_Activated;
		CurrentAnnotation = new CalloutAnnotation();
		TimerRunFlag = false;
		StopPressed = false;
		Crosshair = false;
		CrosshairPen = null;
		ConfigPath = null;
		SilentMode = false;
		bStopSkip = false;
		LockFlag = false;
		PercentCircles = false;
		ResetPctDownTrade = false;
		ResetPctUpTrade = false;
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
		//IL_000b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0011: Expected O, but got Unknown
		//IL_0011: Unknown result type (might be due to invalid IL or missing references)
		//IL_0017: Expected O, but got Unknown
		//IL_0017: Unknown result type (might be due to invalid IL or missing references)
		//IL_001d: Expected O, but got Unknown
		//IL_001d: Unknown result type (might be due to invalid IL or missing references)
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
		//IL_00c4: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ce: Expected O, but got Unknown
		//IL_00cf: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d9: Expected O, but got Unknown
		//IL_00da: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e4: Expected O, but got Unknown
		//IL_00e5: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ef: Expected O, but got Unknown
		//IL_00f0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00fa: Expected O, but got Unknown
		//IL_00fb: Unknown result type (might be due to invalid IL or missing references)
		//IL_0105: Expected O, but got Unknown
		//IL_0106: Unknown result type (might be due to invalid IL or missing references)
		//IL_0110: Expected O, but got Unknown
		//IL_0111: Unknown result type (might be due to invalid IL or missing references)
		//IL_011b: Expected O, but got Unknown
		//IL_011c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0126: Expected O, but got Unknown
		//IL_0127: Unknown result type (might be due to invalid IL or missing references)
		//IL_0131: Expected O, but got Unknown
		//IL_0132: Unknown result type (might be due to invalid IL or missing references)
		//IL_013c: Expected O, but got Unknown
		//IL_013d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0147: Expected O, but got Unknown
		//IL_0148: Unknown result type (might be due to invalid IL or missing references)
		//IL_0152: Expected O, but got Unknown
		//IL_0153: Unknown result type (might be due to invalid IL or missing references)
		//IL_015d: Expected O, but got Unknown
		//IL_015e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0168: Expected O, but got Unknown
		//IL_0169: Unknown result type (might be due to invalid IL or missing references)
		//IL_0173: Expected O, but got Unknown
		//IL_0174: Unknown result type (might be due to invalid IL or missing references)
		//IL_017e: Expected O, but got Unknown
		//IL_017f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0189: Expected O, but got Unknown
		//IL_018a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0194: Expected O, but got Unknown
		//IL_0195: Unknown result type (might be due to invalid IL or missing references)
		//IL_019f: Expected O, but got Unknown
		//IL_01a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_01aa: Expected O, but got Unknown
		//IL_01ab: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b5: Expected O, but got Unknown
		//IL_01b6: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c0: Expected O, but got Unknown
		//IL_01c1: Unknown result type (might be due to invalid IL or missing references)
		//IL_01cb: Expected O, but got Unknown
		//IL_01cc: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d6: Expected O, but got Unknown
		//IL_01d7: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e1: Expected O, but got Unknown
		//IL_01e2: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ec: Expected O, but got Unknown
		//IL_01ed: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f7: Expected O, but got Unknown
		//IL_01f8: Unknown result type (might be due to invalid IL or missing references)
		//IL_0202: Expected O, but got Unknown
		//IL_0203: Unknown result type (might be due to invalid IL or missing references)
		//IL_020d: Expected O, but got Unknown
		//IL_020e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0218: Expected O, but got Unknown
		//IL_0219: Unknown result type (might be due to invalid IL or missing references)
		//IL_0223: Expected O, but got Unknown
		//IL_0224: Unknown result type (might be due to invalid IL or missing references)
		//IL_022e: Expected O, but got Unknown
		//IL_022f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0239: Expected O, but got Unknown
		//IL_0793: Unknown result type (might be due to invalid IL or missing references)
		//IL_079d: Expected O, but got Unknown
		//IL_081e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0828: Expected O, but got Unknown
		//IL_0a71: Unknown result type (might be due to invalid IL or missing references)
		//IL_1ec0: Unknown result type (might be due to invalid IL or missing references)
		//IL_1eca: Expected O, but got Unknown
		components = new Container();
		ChartArea val = new ChartArea();
		Series val2 = new Series();
		Series val3 = new Series();
		Series val4 = new Series();
		ToDatePicker = new DateTimePicker();
		FromDatePicker = new DateTimePicker();
		Label5 = new Label();
		FindingBar = new ProgressBar();
		CandlesButton = new Button();
		Label4 = new Label();
		LoadingBar = new ProgressBar();
		BuySellDGV = new DataGridView();
		PatternsButton = new Button();
		NextButton = new Button();
		PreviousButton = new Button();
		DoneButton = new Button();
		Chart1 = new Chart();
		StartButton = new Button();
		Timer1 = new Timer(components);
		ResumeButton = new Button();
		StopButton = new Button();
		SpeedSB = new HScrollBar();
		Label6 = new Label();
		Panel1 = new Panel();
		StopSkip = new Button();
		SkipCB = new CheckBox();
		SetupButton = new Button();
		SimulatorHelpButton = new Button();
		FindPanel = new Panel();
		FindDGV = new DataGridView();
		Column1 = new DataGridViewTextBoxColumn();
		Column2 = new DataGridViewTextBoxColumn();
		Column3 = new DataGridViewTextBoxColumn();
		Panel3 = new Panel();
		ClearBtn = new Button();
		LimitOrderCB = new CheckBox();
		ShortSaleCB = new CheckBox();
		BuyPriceNum = new NumericUpDown();
		StopPriceNum = new NumericUpDown();
		TargetNum = new NumericUpDown();
		SharesNum = new NumericUpDown();
		Label10 = new Label();
		Label1 = new Label();
		Label9 = new Label();
		Label8 = new Label();
		HelpTradeButton = new Button();
		SetTargetsButton = new Button();
		ClipboardButton = new Button();
		SellButton = new Button();
		BuyButton = new Button();
		MessageLabel = new Label();
		PercentButton = new Button();
		((ISupportInitialize)BuySellDGV).BeginInit();
		((ISupportInitialize)Chart1).BeginInit();
		((Control)Panel1).SuspendLayout();
		((Control)FindPanel).SuspendLayout();
		((ISupportInitialize)FindDGV).BeginInit();
		((Control)Panel3).SuspendLayout();
		((ISupportInitialize)BuyPriceNum).BeginInit();
		((ISupportInitialize)StopPriceNum).BeginInit();
		((ISupportInitialize)TargetNum).BeginInit();
		((ISupportInitialize)SharesNum).BeginInit();
		((Control)this).SuspendLayout();
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(888, 523);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(117, 20);
		((Control)ToDatePicker).TabIndex = 2;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)ToDatePicker).Visible = false;
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(888, 497);
		((Control)FromDatePicker).Name = "FromDatePicker";
		FromDatePicker.ShowUpDown = true;
		((Control)FromDatePicker).Size = new Size(112, 20);
		((Control)FromDatePicker).TabIndex = 1;
		((Control)FromDatePicker).TabStop = false;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FromDatePicker).Visible = false;
		((Control)Label5).Anchor = (AnchorStyles)10;
		Label5.AutoSize = true;
		((Control)Label5).Location = new Point(21, 7);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(44, 13);
		((Control)Label5).TabIndex = 0;
		Label5.Text = "Finding:";
		((Control)FindingBar).Anchor = (AnchorStyles)10;
		((Control)FindingBar).ForeColor = Color.Green;
		((Control)FindingBar).Location = new Point(72, 7);
		((Control)FindingBar).Name = "FindingBar";
		((Control)FindingBar).Size = new Size(59, 13);
		((Control)FindingBar).TabIndex = 1;
		((Control)CandlesButton).Anchor = (AnchorStyles)10;
		((Control)CandlesButton).Location = new Point(73, 36);
		((Control)CandlesButton).Name = "CandlesButton";
		((Control)CandlesButton).Size = new Size(59, 23);
		((Control)CandlesButton).TabIndex = 5;
		((ButtonBase)CandlesButton).Text = "&Candles";
		((ButtonBase)CandlesButton).UseVisualStyleBackColor = true;
		((Control)Label4).Anchor = (AnchorStyles)10;
		Label4.AutoSize = true;
		((Control)Label4).Location = new Point(17, 22);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(48, 13);
		((Control)Label4).TabIndex = 2;
		Label4.Text = "Loading:";
		((Control)LoadingBar).Anchor = (AnchorStyles)10;
		((Control)LoadingBar).ForeColor = Color.Green;
		((Control)LoadingBar).Location = new Point(72, 20);
		((Control)LoadingBar).Name = "LoadingBar";
		((Control)LoadingBar).Size = new Size(59, 13);
		((Control)LoadingBar).TabIndex = 3;
		BuySellDGV.AllowUserToAddRows = false;
		BuySellDGV.AllowUserToDeleteRows = false;
		((Control)BuySellDGV).Anchor = (AnchorStyles)12;
		BuySellDGV.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)10;
		((Control)BuySellDGV).CausesValidation = false;
		BuySellDGV.ColumnHeadersHeightSizeMode = (DataGridViewColumnHeadersHeightSizeMode)2;
		BuySellDGV.EditMode = (DataGridViewEditMode)4;
		BuySellDGV.EnableHeadersVisualStyles = false;
		((Control)BuySellDGV).Location = new Point(4, 4);
		((Control)BuySellDGV).Name = "BuySellDGV";
		BuySellDGV.ReadOnly = true;
		BuySellDGV.SelectionMode = (DataGridViewSelectionMode)1;
		BuySellDGV.ShowCellErrors = false;
		BuySellDGV.ShowCellToolTips = false;
		BuySellDGV.ShowEditingIcon = false;
		BuySellDGV.ShowRowErrors = false;
		((Control)BuySellDGV).Size = new Size(298, 134);
		((Control)BuySellDGV).TabIndex = 0;
		((Control)PatternsButton).Anchor = (AnchorStyles)10;
		((Control)PatternsButton).Location = new Point(73, 61);
		((Control)PatternsButton).Name = "PatternsButton";
		((Control)PatternsButton).Size = new Size(59, 23);
		((Control)PatternsButton).TabIndex = 7;
		((ButtonBase)PatternsButton).Text = "&Patterns";
		((ButtonBase)PatternsButton).UseVisualStyleBackColor = true;
		((Control)NextButton).Anchor = (AnchorStyles)10;
		((Control)NextButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)NextButton).Location = new Point(36, 111);
		((Control)NextButton).Name = "NextButton";
		((Control)NextButton).Size = new Size(29, 23);
		((Control)NextButton).TabIndex = 12;
		((ButtonBase)NextButton).Text = ">";
		((ButtonBase)NextButton).UseVisualStyleBackColor = true;
		((Control)PreviousButton).Anchor = (AnchorStyles)10;
		((Control)PreviousButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)PreviousButton).Location = new Point(6, 111);
		((Control)PreviousButton).Name = "PreviousButton";
		((Control)PreviousButton).Size = new Size(27, 23);
		((Control)PreviousButton).TabIndex = 11;
		((ButtonBase)PreviousButton).Text = "<";
		((ButtonBase)PreviousButton).UseVisualStyleBackColor = true;
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(73, 111);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(59, 23);
		((Control)DoneButton).TabIndex = 13;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
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
		((Control)Chart1).Location = new Point(5, 9);
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
		Chart1.Size = new Size(995, 545);
		((Control)Chart1).TabIndex = 0;
		((Control)Chart1).Text = "Chart1";
		((Control)StartButton).Anchor = (AnchorStyles)10;
		((Control)StartButton).Location = new Point(14, 77);
		((Control)StartButton).Name = "StartButton";
		((Control)StartButton).Size = new Size(60, 23);
		((Control)StartButton).TabIndex = 2;
		((ButtonBase)StartButton).Text = "&Start";
		((ButtonBase)StartButton).UseVisualStyleBackColor = true;
		((Control)ResumeButton).Anchor = (AnchorStyles)10;
		((Control)ResumeButton).Enabled = false;
		((Control)ResumeButton).Location = new Point(14, 17);
		((Control)ResumeButton).Name = "ResumeButton";
		((Control)ResumeButton).Size = new Size(60, 23);
		((Control)ResumeButton).TabIndex = 0;
		((ButtonBase)ResumeButton).Text = "&Resume";
		((ButtonBase)ResumeButton).UseVisualStyleBackColor = true;
		((Control)StopButton).Anchor = (AnchorStyles)10;
		((Control)StopButton).Location = new Point(14, 47);
		((Control)StopButton).Name = "StopButton";
		((Control)StopButton).Size = new Size(60, 23);
		((Control)StopButton).TabIndex = 1;
		((ButtonBase)StopButton).Text = "&Pause";
		((ButtonBase)StopButton).UseVisualStyleBackColor = true;
		((Control)SpeedSB).Anchor = (AnchorStyles)10;
		((ScrollBar)SpeedSB).LargeChange = 1000;
		((Control)SpeedSB).Location = new Point(44, 119);
		((ScrollBar)SpeedSB).Maximum = 10000;
		((ScrollBar)SpeedSB).Minimum = 1;
		((Control)SpeedSB).Name = "SpeedSB";
		((Control)SpeedSB).Size = new Size(298, 19);
		((Control)SpeedSB).TabIndex = 4;
		((ScrollBar)SpeedSB).Value = 1500;
		((Control)Label6).Anchor = (AnchorStyles)10;
		Label6.AutoSize = true;
		((Control)Label6).Location = new Point(3, 122);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(38, 13);
		((Control)Label6).TabIndex = 3;
		Label6.Text = "&Speed";
		((Control)Panel1).Anchor = (AnchorStyles)10;
		Panel1.BorderStyle = (BorderStyle)1;
		((Control)Panel1).Controls.Add((Control)(object)PercentButton);
		((Control)Panel1).Controls.Add((Control)(object)StopSkip);
		((Control)Panel1).Controls.Add((Control)(object)SkipCB);
		((Control)Panel1).Controls.Add((Control)(object)SetupButton);
		((Control)Panel1).Controls.Add((Control)(object)SimulatorHelpButton);
		((Control)Panel1).Controls.Add((Control)(object)DoneButton);
		((Control)Panel1).Controls.Add((Control)(object)PreviousButton);
		((Control)Panel1).Controls.Add((Control)(object)NextButton);
		((Control)Panel1).Controls.Add((Control)(object)PatternsButton);
		((Control)Panel1).Controls.Add((Control)(object)LoadingBar);
		((Control)Panel1).Controls.Add((Control)(object)Label4);
		((Control)Panel1).Controls.Add((Control)(object)CandlesButton);
		((Control)Panel1).Controls.Add((Control)(object)FindingBar);
		((Control)Panel1).Controls.Add((Control)(object)Label5);
		((Control)Panel1).Location = new Point(863, 580);
		((Control)Panel1).Name = "Panel1";
		((Control)Panel1).Size = new Size(137, 143);
		((Control)Panel1).TabIndex = 6;
		((Control)StopSkip).Anchor = (AnchorStyles)10;
		((Control)StopSkip).Location = new Point(88, 86);
		((Control)StopSkip).Name = "StopSkip";
		((Control)StopSkip).Size = new Size(43, 23);
		((Control)StopSkip).TabIndex = 10;
		((ButtonBase)StopSkip).Text = "&Stop";
		((ButtonBase)StopSkip).UseVisualStyleBackColor = true;
		((Control)StopSkip).Visible = false;
		((Control)SkipCB).Anchor = (AnchorStyles)10;
		((ButtonBase)SkipCB).AutoSize = true;
		((Control)SkipCB).Location = new Point(38, 95);
		((Control)SkipCB).Name = "SkipCB";
		((Control)SkipCB).Size = new Size(47, 17);
		((Control)SkipCB).TabIndex = 9;
		((ButtonBase)SkipCB).Text = "&Skip";
		((ButtonBase)SkipCB).UseVisualStyleBackColor = true;
		((Control)SetupButton).Anchor = (AnchorStyles)10;
		((Control)SetupButton).Location = new Point(6, 36);
		((Control)SetupButton).Name = "SetupButton";
		((Control)SetupButton).Size = new Size(59, 23);
		((Control)SetupButton).TabIndex = 4;
		((ButtonBase)SetupButton).Text = "&Setup";
		((ButtonBase)SetupButton).UseVisualStyleBackColor = true;
		((Control)SimulatorHelpButton).Anchor = (AnchorStyles)10;
		((Control)SimulatorHelpButton).Location = new Point(7, 61);
		((Control)SimulatorHelpButton).Name = "SimulatorHelpButton";
		((Control)SimulatorHelpButton).Size = new Size(59, 23);
		((Control)SimulatorHelpButton).TabIndex = 6;
		((ButtonBase)SimulatorHelpButton).Text = "&Help";
		((ButtonBase)SimulatorHelpButton).UseVisualStyleBackColor = true;
		((Control)FindPanel).Anchor = (AnchorStyles)10;
		FindPanel.BorderStyle = (BorderStyle)1;
		((Control)FindPanel).Controls.Add((Control)(object)FindDGV);
		((Control)FindPanel).Controls.Add((Control)(object)StartButton);
		((Control)FindPanel).Controls.Add((Control)(object)Label6);
		((Control)FindPanel).Controls.Add((Control)(object)ResumeButton);
		((Control)FindPanel).Controls.Add((Control)(object)SpeedSB);
		((Control)FindPanel).Controls.Add((Control)(object)StopButton);
		((Control)FindPanel).Location = new Point(510, 580);
		((Control)FindPanel).Name = "FindPanel";
		((Control)FindPanel).Size = new Size(347, 143);
		((Control)FindPanel).TabIndex = 5;
		FindDGV.AllowUserToAddRows = false;
		FindDGV.AllowUserToDeleteRows = false;
		FindDGV.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)10;
		((Control)FindDGV).CausesValidation = false;
		FindDGV.ClipboardCopyMode = (DataGridViewClipboardCopyMode)0;
		FindDGV.ColumnHeadersHeightSizeMode = (DataGridViewColumnHeadersHeightSizeMode)2;
		FindDGV.Columns.AddRange((DataGridViewColumn[])(object)new DataGridViewColumn[3]
		{
			(DataGridViewColumn)Column1,
			(DataGridViewColumn)Column2,
			(DataGridViewColumn)Column3
		});
		((Control)FindDGV).Location = new Point(85, 10);
		FindDGV.MultiSelect = false;
		((Control)FindDGV).Name = "FindDGV";
		FindDGV.ReadOnly = true;
		FindDGV.SelectionMode = (DataGridViewSelectionMode)1;
		FindDGV.ShowCellErrors = false;
		FindDGV.ShowEditingIcon = false;
		FindDGV.ShowRowErrors = false;
		((Control)FindDGV).Size = new Size(257, 105);
		((Control)FindDGV).TabIndex = 5;
		((DataGridViewColumn)Column1).HeaderText = "Name";
		((DataGridViewColumn)Column1).Name = "Column1";
		((DataGridViewColumn)Column1).ReadOnly = true;
		((DataGridViewColumn)Column1).Width = 58;
		((DataGridViewColumn)Column2).HeaderText = "Start";
		((DataGridViewColumn)Column2).Name = "Column2";
		((DataGridViewColumn)Column2).ReadOnly = true;
		((DataGridViewColumn)Column2).Width = 52;
		((DataGridViewColumn)Column3).HeaderText = "End";
		((DataGridViewColumn)Column3).Name = "Column3";
		((DataGridViewColumn)Column3).ReadOnly = true;
		((DataGridViewColumn)Column3).Width = 49;
		((Control)Panel3).Anchor = (AnchorStyles)14;
		Panel3.BorderStyle = (BorderStyle)1;
		((Control)Panel3).Controls.Add((Control)(object)ClearBtn);
		((Control)Panel3).Controls.Add((Control)(object)LimitOrderCB);
		((Control)Panel3).Controls.Add((Control)(object)ShortSaleCB);
		((Control)Panel3).Controls.Add((Control)(object)BuyPriceNum);
		((Control)Panel3).Controls.Add((Control)(object)StopPriceNum);
		((Control)Panel3).Controls.Add((Control)(object)TargetNum);
		((Control)Panel3).Controls.Add((Control)(object)SharesNum);
		((Control)Panel3).Controls.Add((Control)(object)Label10);
		((Control)Panel3).Controls.Add((Control)(object)Label1);
		((Control)Panel3).Controls.Add((Control)(object)Label9);
		((Control)Panel3).Controls.Add((Control)(object)Label8);
		((Control)Panel3).Controls.Add((Control)(object)HelpTradeButton);
		((Control)Panel3).Controls.Add((Control)(object)SetTargetsButton);
		((Control)Panel3).Controls.Add((Control)(object)ClipboardButton);
		((Control)Panel3).Controls.Add((Control)(object)SellButton);
		((Control)Panel3).Controls.Add((Control)(object)BuyButton);
		((Control)Panel3).Controls.Add((Control)(object)BuySellDGV);
		((Control)Panel3).Location = new Point(0, 580);
		((Control)Panel3).Name = "Panel3";
		((Control)Panel3).Size = new Size(504, 143);
		((Control)Panel3).TabIndex = 4;
		((Control)ClearBtn).Anchor = (AnchorStyles)10;
		((Control)ClearBtn).Location = new Point(385, 87);
		((Control)ClearBtn).Name = "ClearBtn";
		((Control)ClearBtn).Size = new Size(48, 23);
		((Control)ClearBtn).TabIndex = 10;
		((ButtonBase)ClearBtn).Text = "&Clear";
		((ButtonBase)ClearBtn).UseVisualStyleBackColor = true;
		((Control)LimitOrderCB).Anchor = (AnchorStyles)10;
		((ButtonBase)LimitOrderCB).AutoSize = true;
		((Control)LimitOrderCB).Location = new Point(308, 91);
		((Control)LimitOrderCB).Name = "LimitOrderCB";
		((Control)LimitOrderCB).Size = new Size(76, 17);
		((Control)LimitOrderCB).TabIndex = 9;
		((ButtonBase)LimitOrderCB).Text = "Limit Order";
		((ButtonBase)LimitOrderCB).UseVisualStyleBackColor = true;
		((Control)ShortSaleCB).Anchor = (AnchorStyles)10;
		((ButtonBase)ShortSaleCB).AutoSize = true;
		((Control)ShortSaleCB).Location = new Point(308, 113);
		((Control)ShortSaleCB).Name = "ShortSaleCB";
		((Control)ShortSaleCB).Size = new Size(73, 17);
		((Control)ShortSaleCB).TabIndex = 11;
		((ButtonBase)ShortSaleCB).Text = "Short sale";
		((ButtonBase)ShortSaleCB).UseVisualStyleBackColor = true;
		((Control)BuyPriceNum).Anchor = (AnchorStyles)10;
		BuyPriceNum.DecimalPlaces = 4;
		BuyPriceNum.Increment = new decimal(new int[4] { 1, 0, 0, 131072 });
		((Control)BuyPriceNum).Location = new Point(369, 46);
		BuyPriceNum.Maximum = new decimal(new int[4] { 500000, 0, 0, 0 });
		((Control)BuyPriceNum).Name = "BuyPriceNum";
		((Control)BuyPriceNum).Size = new Size(64, 20);
		((Control)BuyPriceNum).TabIndex = 6;
		((Control)StopPriceNum).Anchor = (AnchorStyles)10;
		StopPriceNum.DecimalPlaces = 4;
		StopPriceNum.Increment = new decimal(new int[4] { 1, 0, 0, 131072 });
		((Control)StopPriceNum).Location = new Point(369, 65);
		StopPriceNum.Maximum = new decimal(new int[4] { 500000, 0, 0, 0 });
		((Control)StopPriceNum).Name = "StopPriceNum";
		((Control)StopPriceNum).Size = new Size(64, 20);
		((Control)StopPriceNum).TabIndex = 8;
		((Control)TargetNum).Anchor = (AnchorStyles)10;
		TargetNum.DecimalPlaces = 4;
		TargetNum.Increment = new decimal(new int[4] { 1, 0, 0, 131072 });
		((Control)TargetNum).Location = new Point(369, 27);
		TargetNum.Maximum = new decimal(new int[4] { 500000, 0, 0, 0 });
		((Control)TargetNum).Name = "TargetNum";
		((Control)TargetNum).Size = new Size(64, 20);
		((Control)TargetNum).TabIndex = 4;
		((Control)SharesNum).Anchor = (AnchorStyles)10;
		SharesNum.Increment = new decimal(new int[4] { 100, 0, 0, 0 });
		((Control)SharesNum).Location = new Point(369, 8);
		SharesNum.Maximum = new decimal(new int[4] { 1000000, 0, 0, 0 });
		((Control)SharesNum).Name = "SharesNum";
		((Control)SharesNum).Size = new Size(64, 20);
		((Control)SharesNum).TabIndex = 2;
		SharesNum.Value = new decimal(new int[4] { 100, 0, 0, 0 });
		((Control)Label10).Anchor = (AnchorStyles)10;
		Label10.AutoSize = true;
		((Control)Label10).Location = new Point(318, 47);
		((Control)Label10).Name = "Label10";
		((Control)Label10).Size = new Size(54, 13);
		((Control)Label10).TabIndex = 5;
		Label10.Text = "Buy price:";
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(314, 66);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(58, 13);
		((Control)Label1).TabIndex = 7;
		Label1.Text = "Stop price:";
		((Control)Label9).Anchor = (AnchorStyles)10;
		Label9.AutoSize = true;
		((Control)Label9).Location = new Point(305, 28);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(67, 13);
		((Control)Label9).TabIndex = 3;
		Label9.Text = "Target price:";
		((Control)Label8).Anchor = (AnchorStyles)10;
		Label8.AutoSize = true;
		((Control)Label8).Location = new Point(329, 9);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(43, 13);
		((Control)Label8).TabIndex = 1;
		Label8.Text = "Shares:";
		((Control)HelpTradeButton).Anchor = (AnchorStyles)10;
		((Control)HelpTradeButton).Location = new Point(439, 4);
		((Control)HelpTradeButton).Name = "HelpTradeButton";
		((Control)HelpTradeButton).Size = new Size(59, 23);
		((Control)HelpTradeButton).TabIndex = 12;
		((ButtonBase)HelpTradeButton).Text = "&Help";
		((ButtonBase)HelpTradeButton).UseVisualStyleBackColor = true;
		((Control)SetTargetsButton).Anchor = (AnchorStyles)10;
		((Control)SetTargetsButton).Enabled = false;
		((Control)SetTargetsButton).Location = new Point(418, 112);
		((Control)SetTargetsButton).Name = "SetTargetsButton";
		((Control)SetTargetsButton).Size = new Size(80, 23);
		((Control)SetTargetsButton).TabIndex = 16;
		((ButtonBase)SetTargetsButton).Text = "&Set Targets";
		((ButtonBase)SetTargetsButton).UseVisualStyleBackColor = true;
		((Control)ClipboardButton).Anchor = (AnchorStyles)10;
		((Control)ClipboardButton).Enabled = false;
		((Control)ClipboardButton).Location = new Point(438, 31);
		((Control)ClipboardButton).Name = "ClipboardButton";
		((Control)ClipboardButton).Size = new Size(60, 23);
		((Control)ClipboardButton).TabIndex = 13;
		((ButtonBase)ClipboardButton).Text = "Clip&board";
		((ButtonBase)ClipboardButton).UseVisualStyleBackColor = true;
		((Control)SellButton).Anchor = (AnchorStyles)10;
		((Control)SellButton).Location = new Point(438, 58);
		((Control)SellButton).Name = "SellButton";
		((Control)SellButton).Size = new Size(60, 23);
		((Control)SellButton).TabIndex = 14;
		((ButtonBase)SellButton).Text = "&Sell Now";
		((ButtonBase)SellButton).UseVisualStyleBackColor = true;
		((Control)BuyButton).Anchor = (AnchorStyles)10;
		((Control)BuyButton).Location = new Point(438, 85);
		((Control)BuyButton).Name = "BuyButton";
		((Control)BuyButton).Size = new Size(60, 23);
		((Control)BuyButton).TabIndex = 15;
		((ButtonBase)BuyButton).Text = "&Buy Now";
		((ButtonBase)BuyButton).UseVisualStyleBackColor = true;
		((Control)MessageLabel).Anchor = (AnchorStyles)14;
		MessageLabel.BorderStyle = (BorderStyle)1;
		((Control)MessageLabel).CausesValidation = false;
		((Control)MessageLabel).ForeColor = Color.Red;
		((Control)MessageLabel).Location = new Point(5, 554);
		((Control)MessageLabel).Name = "MessageLabel";
		((Control)MessageLabel).Size = new Size(995, 23);
		((Control)MessageLabel).TabIndex = 3;
		MessageLabel.TextAlign = (ContentAlignment)32;
		((Control)PercentButton).Anchor = (AnchorStyles)10;
		((Control)PercentButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)PercentButton).Location = new Point(6, 86);
		((Control)PercentButton).Name = "PercentButton";
		((Control)PercentButton).Size = new Size(29, 23);
		((Control)PercentButton).TabIndex = 8;
		((ButtonBase)PercentButton).Text = "%";
		((ButtonBase)PercentButton).UseVisualStyleBackColor = true;
		((Form)this).AcceptButton = (IButtonControl)(object)StartButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(1008, 729);
		((Control)this).Controls.Add((Control)(object)MessageLabel);
		((Control)this).Controls.Add((Control)(object)Panel3);
		((Control)this).Controls.Add((Control)(object)Panel1);
		((Control)this).Controls.Add((Control)(object)ToDatePicker);
		((Control)this).Controls.Add((Control)(object)FromDatePicker);
		((Control)this).Controls.Add((Control)(object)Chart1);
		((Control)this).Controls.Add((Control)(object)FindPanel);
		((Control)this).Name = "SimulatorForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Simulator Form";
		((Form)this).WindowState = (FormWindowState)2;
		((ISupportInitialize)BuySellDGV).EndInit();
		((ISupportInitialize)Chart1).EndInit();
		((Control)Panel1).ResumeLayout(false);
		((Control)Panel1).PerformLayout();
		((Control)FindPanel).ResumeLayout(false);
		((Control)FindPanel).PerformLayout();
		((ISupportInitialize)FindDGV).EndInit();
		((Control)Panel3).ResumeLayout(false);
		((Control)Panel3).PerformLayout();
		((ISupportInitialize)BuyPriceNum).EndInit();
		((ISupportInitialize)StopPriceNum).EndInit();
		((ISupportInitialize)TargetNum).EndInit();
		((ISupportInitialize)SharesNum).EndInit();
		((Control)this).ResumeLayout(false);
	}

	private void SimulatorForm_Closing(object sender, CancelEventArgs e)
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
		TimerRunFlag = false;
		Timer1.Enabled = false;
		if (decimal.Compare(new decimal(lsShares), SharesNum.Value) != 0)
		{
			try
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SimulatorForm", "Shares", (object)SharesNum.Value);
			}
			catch (Exception ex3)
			{
				ProjectData.SetProjectError(ex3);
				Exception ex4 = ex3;
				ProjectData.ClearProjectError();
			}
		}
		if (lsPauseSimulator != GlobalForm.PauseSimulator)
		{
			try
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SimulatorForm", "PauseSim", (object)GlobalForm.PauseSimulator);
			}
			catch (Exception ex5)
			{
				ProjectData.SetProjectError(ex5);
				Exception ex6 = ex5;
				ProjectData.ClearProjectError();
			}
		}
		WriteConfigFile();
		GlobalForm.Annotations = GlobalStorage.Annotations;
		GlobalForm.ShowCandles = GlobalStorage.FindCandles;
		GlobalForm.ShowAllPatterns = GlobalStorage.ShowPattern;
		GlobalForm.StrictPatterns = GlobalStorage.Strict;
		GlobalForm.ChartVolume = GlobalStorage.Volume;
		GlobalForm.MAUsed = GlobalStorage.MovingAvg;
		GlobalForm.MAType = GlobalStorage.MAType;
		GlobalForm.MALength = GlobalStorage.MALength;
		GlobalForm.ChartPeriodShown = GlobalStorage.TimeScale;
		GlobalForm.PatternTargets = lsPatternTargets;
		MySettingsProperty.Settings.SimLocation = ((Form)this).Location;
		MySettingsProperty.Settings.SimSize = ((Form)this).Size;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
		MyPen.Dispose();
		GlobalForm.FormTypeLoaded = 3;
	}

	private void SimulatorForm_Load(object sender, EventArgs e)
	{
		//IL_002d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0032: Unknown result type (might be due to invalid IL or missing references)
		//IL_003d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0048: Unknown result type (might be due to invalid IL or missing references)
		//IL_0053: Unknown result type (might be due to invalid IL or missing references)
		//IL_005a: Unknown result type (might be due to invalid IL or missing references)
		//IL_006b: Unknown result type (might be due to invalid IL or missing references)
		//IL_007c: Unknown result type (might be due to invalid IL or missing references)
		//IL_008d: Unknown result type (might be due to invalid IL or missing references)
		//IL_009e: Unknown result type (might be due to invalid IL or missing references)
		//IL_00af: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f3: Unknown result type (might be due to invalid IL or missing references)
		//IL_0104: Unknown result type (might be due to invalid IL or missing references)
		//IL_0115: Unknown result type (might be due to invalid IL or missing references)
		//IL_0126: Unknown result type (might be due to invalid IL or missing references)
		//IL_0137: Unknown result type (might be due to invalid IL or missing references)
		//IL_0148: Unknown result type (might be due to invalid IL or missing references)
		//IL_0159: Unknown result type (might be due to invalid IL or missing references)
		//IL_016a: Unknown result type (might be due to invalid IL or missing references)
		//IL_017b: Unknown result type (might be due to invalid IL or missing references)
		//IL_018c: Unknown result type (might be due to invalid IL or missing references)
		//IL_019d: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ae: Unknown result type (might be due to invalid IL or missing references)
		//IL_01bf: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d0: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e1: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f2: Unknown result type (might be due to invalid IL or missing references)
		//IL_0203: Unknown result type (might be due to invalid IL or missing references)
		//IL_0214: Unknown result type (might be due to invalid IL or missing references)
		//IL_0225: Unknown result type (might be due to invalid IL or missing references)
		//IL_0236: Unknown result type (might be due to invalid IL or missing references)
		//IL_0247: Unknown result type (might be due to invalid IL or missing references)
		//IL_03be: Unknown result type (might be due to invalid IL or missing references)
		//IL_03c8: Expected O, but got Unknown
		//IL_0547: Unknown result type (might be due to invalid IL or missing references)
		//IL_054c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0558: Expected O, but got Unknown
		//IL_0564: Unknown result type (might be due to invalid IL or missing references)
		//IL_056e: Expected O, but got Unknown
		LockFlag = false;
		GlobalForm.FormTypeLoaded = 4;
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.SimLocation, MySettingsProperty.Settings.SimSize);
		GlobalForm.Quiet = false;
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)SharesNum, "Enter number of shares to trade");
		val.SetToolTip((Control)(object)TargetNum, "Price at which to sell or 0 to sell manually.");
		val.SetToolTip((Control)(object)BuyPriceNum, "Price at which to buy or 0 to buy manually.");
		val.SetToolTip((Control)(object)ClearBtn, "Set target, buy, and stop prices to 0.");
		val.SetToolTip((Control)(object)StopPriceNum, "Exit price in case trade goes bad or 0 for unused.");
		val.SetToolTip((Control)(object)ShortSaleCB, "Check to sell short, uncheck to sell long.");
		val.SetToolTip((Control)(object)LimitOrderCB, "Limit order: Buy for no more or sell for no less than the buy price.");
		val.SetToolTip((Control)(object)HelpTradeButton, "Trading control help.");
		val.SetToolTip((Control)(object)ClipboardButton, "Copies ALL grid rows to clipboard.");
		val.SetToolTip((Control)(object)SellButton, "Manual sell button. Sells at the next bar's opening price.");
		val.SetToolTip((Control)(object)BuyButton, "Manual buy button. Buys at the next bar's opening price.");
		val.SetToolTip((Control)(object)SetTargetsButton, "Fills target/buy/stop prices based on the chart pattern and short sale checkbox.");
		val.SetToolTip((Control)(object)ResumeButton, "Continue the trade, continue scrolling the chart.");
		val.SetToolTip((Control)(object)StopButton, "Pause the trade.");
		val.SetToolTip((Control)(object)BuySellDGV, "Trading results shown here.");
		val.SetToolTip((Control)(object)StartButton, "Find the chart pattern.");
		val.SetToolTip((Control)(object)FindDGV, "Chart pattern list for this security.");
		val.SetToolTip((Control)(object)SpeedSB, "Chart scrolling speed.");
		val.SetToolTip((Control)(object)SetupButton, "Form has additional options.");
		val.SetToolTip((Control)(object)SimulatorHelpButton, "Help overview.");
		val.SetToolTip((Control)(object)StopSkip, "Stops Skip (checkbox) from loading the next security.");
		val.SetToolTip((Control)(object)PercentButton, "Right mouse click two price bars then % to show percentage move.");
		val.SetToolTip((Control)(object)PreviousButton, "Load previous security.");
		val.SetToolTip((Control)(object)NextButton, "Load next security.");
		val.SetToolTip((Control)(object)CandlesButton, "Shows a list of candles to identify.");
		val.SetToolTip((Control)(object)PatternsButton, "Shows patterns to trade.");
		val.SetToolTip((Control)(object)MessageLabel, "Shows candle or chart pattern information.");
		val.SetToolTip((Control)(object)FindingBar, "Progress bar for finding chart patterns, candles.");
		val.SetToolTip((Control)(object)LoadingBar, "Progress bar for loading a security.");
		val.SetToolTip((Control)(object)SkipCB, "If no chart patterns are found in this stock, load the next one.");
		GlobalForm.iFib1 = -1;
		GlobalForm.iFib2 = -1;
		SilentMode = false;
		bStopSkip = false;
		SkipCB.Checked = false;
		GlobalStorage.Annotations = GlobalForm.Annotations;
		GlobalStorage.FindCandles = GlobalForm.ShowCandles;
		GlobalStorage.ShowPattern = GlobalForm.ShowAllPatterns;
		GlobalStorage.Strict = GlobalForm.StrictPatterns;
		GlobalStorage.Volume = GlobalForm.ChartVolume;
		GlobalStorage.MovingAvg = GlobalForm.MAUsed;
		GlobalStorage.MAType = GlobalForm.MAType;
		GlobalStorage.MALength = GlobalForm.MALength;
		GlobalStorage.TimeScale = GlobalForm.ChartPeriodShown;
		lsPatternTargets = GlobalForm.PatternTargets;
		GlobalForm.PatternTargets = false;
		TargetNum.DecimalPlaces = GlobalForm.DecimalsUsed;
		BuyPriceNum.DecimalPlaces = GlobalForm.DecimalsUsed;
		StopPriceNum.DecimalPlaces = GlobalForm.DecimalsUsed;
		ReadConfigFile();
		((Control)ResumeButton).Enabled = false;
		((Control)BuyButton).Enabled = false;
		((Control)SellButton).Enabled = false;
		((Control)SetTargetsButton).Enabled = false;
		((Control)ClipboardButton).Enabled = false;
		FindingBar.Maximum = 100;
		PatternIndex = -1;
		if (CurrentAnnotation == null)
		{
			CurrentAnnotation = new CalloutAnnotation();
		}
		((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)CurrentAnnotation);
		EnableDisable(Flag: true);
		BuildGridHeader();
		Timer1.Interval = GlobalForm.SimGlobals.Speed;
		Trade.InProgress = false;
		Trade.TradeReady = false;
		try
		{
			lsShares = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SimulatorForm", "Shares", (object)100));
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		SharesNum.Value = new decimal(lsShares);
		try
		{
			lsPauseSimulator = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\SimulatorForm", "PauseSim", (object)4));
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			ProjectData.ClearProjectError();
		}
		if (lsPauseSimulator == 0)
		{
			lsPauseSimulator = 4;
		}
		GlobalForm.PauseSimulator = lsPauseSimulator;
		StopPressed = false;
		TimerRunFlag = false;
		Timer1.Enabled = false;
		DataPointsCount = 0;
		GlobalForm.LBIndex = 0;
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Clear();
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Clear();
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points).Clear();
		MyPen = new Pen(Color.Red)
		{
			DashStyle = (DashStyle)1
		};
		BoldFont = new Font("Arial", 8f, (FontStyle)0);
	}

	private void SimulatorForm_Activated(object sender, EventArgs e)
	{
		//IL_00ff: Unknown result type (might be due to invalid IL or missing references)
		//IL_0109: Expected O, but got Unknown
		((Control)this).Show();
		if (LockFlag)
		{
			return;
		}
		LockFlag = true;
		LoadingBar.Value = 5;
		((Control)LoadingBar).Refresh();
		if (MyProject.Forms.Mainform.ListBox1.Items.Count <= 0)
		{
			return;
		}
		Filename = MyProject.Forms.Mainform.ListBox1.SelectedItems[GlobalForm.LBIndex].ToString();
		string filename = Filename;
		ProgressBar ProgBar = LoadingBar;
		Label ErrorLabel = MessageLabel;
		bool num = GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.ChartPeriodShown);
		MessageLabel = ErrorLabel;
		LoadingBar = ProgBar;
		if (!num)
		{
			GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
			GlobalForm.SelectChartType(Chart1);
			AfterLoadFile();
			((Form)this).Text = "Simulator Form: " + Filename;
			FillPatternGrid();
			if (FindDGV.RowCount > 0)
			{
				FindDGV_CellClick(FindDGV, new DataGridViewCellEventArgs(0, 0));
			}
		}
	}

	private void AfterLoadFile()
	{
		if (GlobalForm.IntradayData)
		{
			FromDatePicker.Value = GlobalForm.nDT[0, 0];
			ToDatePicker.Value = GlobalForm.nDT[0, GlobalForm.HLCRange];
		}
		else
		{
			FromDatePicker.Value = GlobalForm.nDT[0, 0].Date;
			ToDatePicker.Value = GlobalForm.nDT[0, GlobalForm.HLCRange];
		}
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

	private void AnalyzeTrade(int Row)
	{
		if (Trade.iBkout != -1)
		{
			int num = ((!Trade.tShort) ? FindPriceBars(Trade.BuyDate, GlobalForm.nDT[0, Trade.iBkout]) : FindPriceBars(Trade.SellDate, GlobalForm.nDT[0, Trade.iBkout]));
			BuySellDGV.Rows[Row].Cells[17].Value = num;
		}
		else
		{
			BuySellDGV.Rows[Row].Cells[17].Value = "N/A";
		}
		if (Trade.tShort)
		{
			if (decimal.Compare(Trade.BuyPrice, 0m) == 0)
			{
				Trade.BuyDate = GlobalForm.nDT[0, GlobalForm.HLCRange];
				Trade.iBuy = GlobalForm.HLCRange;
			}
		}
		else if (decimal.Compare(Trade.SellPrice, 0m) == 0)
		{
			Trade.SellDate = GlobalForm.nDT[0, GlobalForm.HLCRange];
			Trade.iSell = GlobalForm.HLCRange;
		}
		if (Trade.UpBreakoutDirection == 1)
		{
			int num = ((!Trade.tShort) ? FindPriceBars(Trade.SellDate, Trade.UltHighDate) : FindPriceBars(Trade.BuyDate, Trade.UltHighDate));
			BuySellDGV.Rows[Row].Cells[18].Value = num;
		}
		else if (Trade.UpBreakoutDirection == -1)
		{
			int num = ((!Trade.tShort) ? FindPriceBars(Trade.SellDate, Trade.UltLowDate) : FindPriceBars(Trade.BuyDate, Trade.UltLowDate));
			BuySellDGV.Rows[Row].Cells[18].Value = num;
		}
	}

	private void BuildGridHeader()
	{
		BuySellDGV.RowCount = 0;
		BuySellDGV.ColumnCount = 19;
		BuySellDGV.Columns[0].HeaderText = "Profit";
		BuySellDGV.Columns[1].HeaderText = "Buy";
		BuySellDGV.Columns[2].HeaderText = "Buy";
		((DataGridViewCell)BuySellDGV.Columns[2].HeaderCell).Style.ForeColor = Color.Blue;
		BuySellDGV.Columns[3].HeaderText = "Sell";
		BuySellDGV.Columns[4].HeaderText = "Sell";
		((DataGridViewCell)BuySellDGV.Columns[4].HeaderCell).Style.ForeColor = Color.Red;
		BuySellDGV.Columns[5].HeaderText = "Shares";
		BuySellDGV.Columns[6].HeaderText = "Commissions";
		BuySellDGV.Columns[7].HeaderText = "Short?";
		BuySellDGV.Columns[8].HeaderText = "Target";
		BuySellDGV.Columns[9].HeaderText = "Stop";
		BuySellDGV.Columns[10].HeaderText = "Trade Status";
		BuySellDGV.Columns[11].HeaderText = "Symbol";
		BuySellDGV.Columns[12].HeaderText = "Pattern Name";
		BuySellDGV.Columns[13].HeaderText = "Ultimate High";
		BuySellDGV.Columns[14].HeaderText = "Ultimate High";
		((DataGridViewCell)BuySellDGV.Columns[14].HeaderCell).Style.ForeColor = Color.Green;
		BuySellDGV.Columns[15].HeaderText = "Ultimate Low";
		BuySellDGV.Columns[16].HeaderText = "Ultimate Low";
		((DataGridViewCell)BuySellDGV.Columns[16].HeaderCell).Style.ForeColor = Color.Violet;
		BuySellDGV.Columns[17].HeaderText = "Entry";
		BuySellDGV.Columns[18].HeaderText = "Exit";
	}

	private void BuildMessage(string Phrase, DateTime ObjectStart, DateTime ObjectEnd, bool Flag)
	{
		MessageLabel.Text = "";
		string text = ((!GlobalForm.IntradayData) ? GlobalForm.UserDate : "");
		if (Flag | (Strings.Len(MessageLabel.Text) == 0))
		{
			MessageLabel.Text = Phrase + " from " + Strings.Format((object)ObjectStart, text) + " to " + Strings.Format((object)ObjectEnd, text);
		}
		else
		{
			Label messageLabel;
			(messageLabel = MessageLabel).Text = messageLabel.Text + ". " + Phrase + " from " + Strings.Format((object)ObjectStart, text) + " to " + Strings.Format((object)ObjectEnd, text);
		}
	}

	private void BuyButton_Click(object sender, EventArgs e)
	{
		checked
		{
			if (GlobalForm.ChartEndIndex + 1 <= GlobalForm.HLCRange)
			{
				Trade.BuyPrice = GlobalForm.nHLC[0, GlobalForm.ChartEndIndex + 1];
				Trade.BuyDate = GlobalForm.nDT[0, GlobalForm.ChartEndIndex + 1];
				Trade.iBuy = GlobalForm.ChartEndIndex + 1;
			}
			else
			{
				Trade.BuyPrice = GlobalForm.nHLC[3, GlobalForm.HLCRange];
				Trade.BuyDate = GlobalForm.nDT[0, GlobalForm.HLCRange];
				Trade.iBuy = GlobalForm.HLCRange;
			}
			BuyPriceNum.Value = Trade.BuyPrice;
			MessageLabel.Text = "Buy price filled in.";
			if (Trade.InProgress)
			{
				Trade.InProgress = false;
				((Control)BuyButton).Enabled = false;
				Trade.TradeReady = false;
				ref decimal commissions = ref Trade.Commissions;
				commissions = decimal.Add(commissions, GlobalForm.SimGlobals.Commissions);
				StopPressed = true;
				Trade.SellStatus = Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartEndIndex >= GlobalForm.HLCRange, (object)7, (object)6));
				TradeReport();
			}
			else
			{
				Trade.InProgress = true;
				Trade.TradeReady = true;
				Trade.tShort = false;
				ShortSaleCB.Checked = false;
				Trade.BuyStatus = Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartEndIndex >= GlobalForm.HLCRange, (object)7, (object)6));
				Trade.Commissions = GlobalForm.SimGlobals.Commissions;
				((Control)BuyButton).Enabled = false;
				((Control)SellButton).Enabled = true;
			}
		}
	}

	private void CandlesButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.CandlesForm).ShowDialog();
		PatternIndex = -1;
	}

	private void Chart1_MouseDown(object sender, MouseEventArgs e)
	{
		//IL_0008: Unknown result type (might be due to invalid IL or missing references)
		//IL_0012: Invalid comparison between Unknown and I4
		//IL_005d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0067: Invalid comparison between Unknown and I4
		//IL_0027: Unknown result type (might be due to invalid IL or missing references)
		//IL_002c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0038: Expected O, but got Unknown
		if (GlobalForm.HLCRange == 0)
		{
			return;
		}
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
		if ((int)e.Button == 2097152)
		{
			GlobalForm.ShowQuoteInfo(Chart1, e);
		}
	}

	private void Chart1_MouseUp(object sender, MouseEventArgs e)
	{
		//IL_000b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0015: Invalid comparison between Unknown and I4
		//IL_0127: Unknown result type (might be due to invalid IL or missing references)
		//IL_0131: Invalid comparison between Unknown and I4
		//IL_004c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0052: Expected O, but got Unknown
		if (GlobalForm.HLCRange == 0)
		{
			return;
		}
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
		//IL_043a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0441: Expected O, but got Unknown
		//IL_048c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0493: Expected O, but got Unknown
		//IL_0057: Unknown result type (might be due to invalid IL or missing references)
		//IL_005e: Invalid comparison between Unknown and I4
		//IL_001e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0028: Expected O, but got Unknown
		if (GlobalForm.HLCRange == 0)
		{
			return;
		}
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
				if ((int)val.ChartElementType == 16)
				{
					if (Operators.CompareString(val.Series.Name, "CandleSeries", false) == 0)
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
					else if (Operators.CompareString(val.Series.Name, "VolumeSeries", false) == 0)
					{
						((Annotation)CurrentAnnotation).AnchorDataPoint = ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex];
						double num = (double)((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Count / 5.0;
						if ((double)val.PointIndex - num <= 0.0)
						{
							((Annotation)CurrentAnnotation).X = (double)val.PointIndex + num;
						}
						else
						{
							((Annotation)CurrentAnnotation).X = (double)val.PointIndex - num;
						}
						((Annotation)CurrentAnnotation).Y = ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[0];
						((TextAnnotation)CurrentAnnotation).Text = ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[0].ToString();
						((Annotation)CurrentAnnotation).Visible = true;
						Chart1.Invalidate();
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
		//IL_0014: Unknown result type (might be due to invalid IL or missing references)
		//IL_001a: Expected O, but got Unknown
		if (GlobalForm.HLCRange == 0)
		{
			return;
		}
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
		//IL_004e: Unknown result type (might be due to invalid IL or missing references)
		//IL_006e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0075: Expected O, but got Unknown
		//IL_008b: Unknown result type (might be due to invalid IL or missing references)
		int NumberShowPoints = 0;
		decimal ValleyPrice = default(decimal);
		decimal PeakPrice = default(decimal);
		if (GlobalForm.HLCRange == 0)
		{
			return;
		}
		ShowPatterns.DisplayAllPatterns(e, FromDatePicker.Value, ToDatePicker.Value);
		checked
		{
			if (e.ChartElement is Series && Operators.CompareString(((Series)e.ChartElement).Name, "CandleSeries", false) == 0)
			{
				Series val = (Series)e.ChartElement;
				if (e.ChartElement is Series && Operators.CompareString(((Series)e.ChartElement).Name, "CandleSeries", false) == 0)
				{
					if ((Trade.iBuy != -1) & (Trade.iBuy >= GlobalForm.ChartStartIndex) & (Trade.iBuy <= GlobalForm.ChartEndIndex))
					{
						NumberShowPoints++;
					}
					if ((Trade.iSell != -1) & (Trade.iSell >= GlobalForm.ChartStartIndex) & (Trade.iSell <= GlobalForm.ChartEndIndex))
					{
						NumberShowPoints++;
					}
					if ((Trade.iUltHigh != -1) & (Trade.iUltHigh >= GlobalForm.ChartStartIndex) & (Trade.iUltHigh <= GlobalForm.ChartEndIndex))
					{
						NumberShowPoints++;
					}
					if ((Trade.iUltLow != -1) & (Trade.iUltLow >= GlobalForm.ChartStartIndex) & (Trade.iUltLow <= GlobalForm.ChartEndIndex))
					{
						NumberShowPoints++;
					}
				}
				int num = 0;
				foreach (DataPoint item in (Collection<DataPoint>)(object)val.Points)
				{
					if (unchecked(GlobalForm.SimGlobals.ShowCircles && NumberShowPoints > 0))
					{
						ShowCircles(e, item, num, ref NumberShowPoints);
					}
					if (GlobalForm.SimGlobals.ShowBearMarkets)
					{
						ShowBearMarkets(e, num);
					}
					if (GlobalForm.SimGlobals.ShowPeakDrop | GlobalForm.SimGlobals.ShowValleyRises)
					{
						ShowPercentMoves(e, num, ref PeakPrice, ref ValleyPrice, ((Collection<DataPoint>)(object)val.Points).Count);
					}
					num++;
				}
			}
			ShowPercent(e);
		}
	}

	private void CheckTrade()
	{
		if (!Trade.TradeReady || !((GlobalForm.ChartEndIndex > 0) & (GlobalForm.ChartEndIndex <= GlobalForm.HLCRange)))
		{
			return;
		}
		decimal d = GlobalForm.nHLC[1, GlobalForm.ChartEndIndex];
		decimal d2 = GlobalForm.nHLC[2, GlobalForm.ChartEndIndex];
		decimal num = GlobalForm.nHLC[0, GlobalForm.ChartEndIndex];
		if (Trade.InProgress && decimal.Compare(Trade.PriceTarget, 0m) != 0 && ((!Trade.tShort & (decimal.Compare(d, Trade.PriceTarget) >= 0)) | (Trade.tShort & (decimal.Compare(d2, Trade.PriceTarget) <= 0))))
		{
			if (!Trade.tShort)
			{
				Trade.SellDate = GlobalForm.nDT[0, GlobalForm.ChartEndIndex];
				Trade.iSell = GlobalForm.ChartEndIndex;
				if (decimal.Compare(num, Trade.PriceTarget) > 0)
				{
					Trade.SellPrice = num;
				}
				else
				{
					Trade.SellPrice = Trade.PriceTarget;
				}
				if (GlobalForm.SimGlobals.SECBool)
				{
					Trade.Fees = decimal.Multiply(decimal.Multiply(decimal.Divide(GlobalForm.SimGlobals.SECFee, 1000000m), new decimal(Trade.Shares)), Trade.SellPrice);
				}
			}
			else if (Trade.tShort)
			{
				Trade.BuyDate = GlobalForm.nDT[0, GlobalForm.ChartEndIndex];
				Trade.iBuy = GlobalForm.ChartEndIndex;
				if (decimal.Compare(num, Trade.PriceTarget) < 0)
				{
					Trade.BuyPrice = num;
				}
				else
				{
					Trade.BuyPrice = Trade.PriceTarget;
				}
			}
			StopPressed = true;
			Trade.SellStatus = 2;
			ref decimal commissions = ref Trade.Commissions;
			commissions = decimal.Add(commissions, GlobalForm.SimGlobals.Commissions);
			TradeReport();
		}
		if (Trade.InProgress && decimal.Compare(Trade.PriceStop, 0m) != 0 && ((!Trade.tShort & (decimal.Compare(d2, Trade.PriceStop) <= 0)) | (Trade.tShort & (decimal.Compare(d, Trade.PriceStop) >= 0))))
		{
			if (!Trade.tShort)
			{
				Trade.SellDate = GlobalForm.nDT[0, GlobalForm.ChartEndIndex];
				Trade.iSell = GlobalForm.ChartEndIndex;
				if (decimal.Compare(num, Trade.PriceStop) < 0)
				{
					Trade.SellPrice = num;
				}
				else
				{
					Trade.SellPrice = Trade.PriceStop;
				}
				if (GlobalForm.SimGlobals.SECBool)
				{
					Trade.Fees = decimal.Multiply(decimal.Multiply(decimal.Divide(GlobalForm.SimGlobals.SECFee, 1000000m), new decimal(Trade.Shares)), Trade.SellPrice);
				}
			}
			else if (Trade.tShort)
			{
				Trade.BuyDate = GlobalForm.nDT[0, GlobalForm.ChartEndIndex];
				Trade.iBuy = GlobalForm.ChartEndIndex;
				if (decimal.Compare(num, Trade.PriceStop) > 0)
				{
					Trade.BuyPrice = num;
				}
				else
				{
					Trade.BuyPrice = Trade.PriceStop;
				}
			}
			StopPressed = true;
			Trade.SellStatus = 1;
			ref decimal commissions2 = ref Trade.Commissions;
			commissions2 = decimal.Add(commissions2, GlobalForm.SimGlobals.Commissions);
			TradeReport();
		}
		if (!(!Trade.InProgress & !StopPressed))
		{
			return;
		}
		decimal value = BuyPriceNum.Value;
		if (decimal.Compare(value, 0m) == 0)
		{
			return;
		}
		if (ShortSaleCB.Checked)
		{
			if (LimitOrderCB.Checked & (decimal.Compare(d, value) >= 0))
			{
				Trade.SellPrice = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num, value) >= 0, (object)num, (object)value));
				if (GlobalForm.SimGlobals.SECBool)
				{
					Trade.Fees = decimal.Multiply(decimal.Multiply(decimal.Divide(GlobalForm.SimGlobals.SECFee, 1000000m), new decimal(Trade.Shares)), Trade.SellPrice);
				}
				Trade.tShort = true;
				Trade.SellDate = GlobalForm.nDT[0, GlobalForm.ChartEndIndex];
				Trade.iSell = GlobalForm.ChartEndIndex;
				((Control)BuyButton).Enabled = true;
				((Control)SellButton).Enabled = false;
				Trade.BuyStatus = 5;
				Trade.Commissions = GlobalForm.SimGlobals.Commissions;
				Trade.InProgress = true;
			}
			else if (!LimitOrderCB.Checked && decimal.Compare(d2, value) <= 0)
			{
				Trade.SellPrice = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num, value) <= 0, (object)num, (object)value));
				if (GlobalForm.SimGlobals.SECBool)
				{
					Trade.Fees = decimal.Multiply(decimal.Multiply(decimal.Divide(GlobalForm.SimGlobals.SECFee, 1000000m), new decimal(Trade.Shares)), Trade.SellPrice);
				}
				Trade.tShort = true;
				Trade.SellDate = GlobalForm.nDT[0, GlobalForm.ChartEndIndex];
				Trade.iSell = GlobalForm.ChartEndIndex;
				((Control)BuyButton).Enabled = true;
				((Control)SellButton).Enabled = false;
				Trade.BuyStatus = 3;
				Trade.Commissions = GlobalForm.SimGlobals.Commissions;
				Trade.InProgress = true;
			}
		}
		else if (LimitOrderCB.Checked & (decimal.Compare(d2, value) <= 0))
		{
			Trade.BuyPrice = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num, value) >= 0, (object)value, (object)num));
			Trade.BuyDate = GlobalForm.nDT[0, GlobalForm.ChartEndIndex];
			Trade.iBuy = GlobalForm.ChartEndIndex;
			((Control)BuyButton).Enabled = false;
			((Control)SellButton).Enabled = true;
			Trade.BuyStatus = 4;
			Trade.Commissions = GlobalForm.SimGlobals.Commissions;
			Trade.InProgress = true;
		}
		else if (!LimitOrderCB.Checked & (decimal.Compare(d, value) >= 0))
		{
			Trade.BuyPrice = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num, value) >= 0, (object)num, (object)value));
			Trade.BuyDate = GlobalForm.nDT[0, GlobalForm.ChartEndIndex];
			Trade.iBuy = GlobalForm.ChartEndIndex;
			((Control)BuyButton).Enabled = false;
			((Control)SellButton).Enabled = true;
			Trade.BuyStatus = 3;
			Trade.Commissions = GlobalForm.SimGlobals.Commissions;
			Trade.InProgress = true;
		}
	}

	private void ClearBtn_Click(object sender, EventArgs e)
	{
		TargetNum.Value = 0m;
		BuyPriceNum.Value = 0m;
		StopPriceNum.Value = 0m;
	}

	private void ClipboardButton_Click(object sender, EventArgs e)
	{
		//IL_00c8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ed: Unknown result type (might be due to invalid IL or missing references)
		((Control)this).Cursor = Cursors.WaitCursor;
		BuySellDGV.SelectAll();
		string text = "Notes: Commissions may include the SEC fee (see Simulator Setup form).\r\n";
		text += "The search for the ultimate high/low begins the day after a trade starts.\r\n";
		text += "Ultimate high is the highest peak before price drops (measured high to close) at least 20% or closes below the pattern's low.\r\n";
		text += "The ultimate low is the lowest valley before price rises at least 20% (measured low to close) or closes above the top of the chart pattern.\r\n";
		text += "Entry and exit are in price bars, measured from the breakout (entry) and the ultimate high/low (exit). Negative values mean an entry/exit before the optimum entry/exit, plus values mean after the optimum entry/exit.\r\n";
		text += "Copyright (c) 2016-2024 by Thomas Bulkowski and ThePatternSite.com. All rights reserved.\r\n\r\n";
		int num = 3;
		while (true)
		{
			try
			{
				Clipboard.SetDataObject((object)BuySellDGV.GetClipboardContent());
				string text2 = Clipboard.GetText();
				if (text2.Length != 0)
				{
					goto IL_008e;
				}
				BuySellDGV.SelectAll();
				num = checked(num - 1);
				if (num <= 0)
				{
					goto IL_008e;
				}
				goto end_IL_005b;
				IL_008e:
				text += text2;
				Clipboard.SetText(text);
				break;
				end_IL_005b:;
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				((Control)this).Cursor = Cursors.Default;
				MessageBox.Show("Clipboard is busy with another user. Error: " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				ProjectData.ClearProjectError();
				return;
			}
		}
		((Control)this).Cursor = Cursors.Default;
		MessageBox.Show("Contents are on the clibpard for pasting into another program.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void DGVRow(int iRow)
	{
		PatternIndex = -1;
		checked
		{
			int num = GlobalForm.PatternCount - 1;
			for (int i = 0; i <= num; i++)
			{
				int num2 = Conversions.ToInteger(GlobalForm.TranslatePatternName(Conversions.ToString(FindDGV.Rows[iRow].Cells[0].Value), GlobalForm.PASSNAME));
				if (num2 != -1)
				{
					if ((GlobalForm.ChartPatterns[i].Type == num2) & (DateTime.Compare(Conversions.ToDate(FindDGV.Rows[iRow].Cells[1].Value), GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStartDate]) == 0) & (DateTime.Compare(Conversions.ToDate(FindDGV.Rows[iRow].Cells[2].Value), GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEndDate]) == 0))
					{
						GlobalForm.GetCPInformation(i);
						Trade.iBkout = GlobalForm.CPInfo.iBkout;
						GlobalForm.ChartPatterns[i].RenderColor = Color.Red;
						if (GlobalForm.ChartPatterns[i].iStartDate != 0)
						{
							ToDatePicker.Value = GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStartDate - 1];
						}
						else
						{
							ToDatePicker.Value = GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStartDate];
						}
						BuildMessage(Conversions.ToString(FindDGV.Rows[iRow].Cells[0].Value), GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStartDate], GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEndDate], Flag: true);
						PatternIndex = i;
						PatternName = FindDGV.Rows[iRow].Cells[0].Value.ToString();
					}
					else
					{
						GlobalForm.ChartPatterns[i].RenderColor = Color.Black;
					}
				}
				else
				{
					GlobalForm.ChartPatterns[i].RenderColor = Color.Black;
				}
			}
			((Control)SetTargetsButton).Enabled = true;
		}
	}

	private void EnableDisable(bool Flag)
	{
		((Control)BuyPriceNum).Enabled = Flag;
		((Control)BuySellDGV).Enabled = Flag;
		((Control)CandlesButton).Enabled = Flag;
		((Control)ClearBtn).Enabled = Flag;
		((Control)DoneButton).Enabled = Flag;
		((Control)FindDGV).Enabled = Flag;
		((Control)FromDatePicker).Enabled = Flag;
		((Control)LimitOrderCB).Enabled = Flag;
		((Control)SimulatorHelpButton).Enabled = Flag;
		((Control)HelpTradeButton).Enabled = Flag;
		((Control)NextButton).Enabled = Flag;
		((Control)PatternsButton).Enabled = Flag;
		((Control)PercentButton).Enabled = Flag;
		((Control)PreviousButton).Enabled = Flag;
		((Control)SetupButton).Enabled = Flag;
		((Control)SharesNum).Enabled = Flag;
		((Control)ShortSaleCB).Enabled = Flag;
		((Control)StartButton).Enabled = Flag;
		((Control)StopButton).Enabled = !Flag;
		((Control)StopPriceNum).Enabled = Flag;
		((Control)TargetNum).Enabled = Flag;
		((Control)ToDatePicker).Enabled = Flag;
		((Control)ClipboardButton).Enabled = false;
		if (Flag && BuySellDGV.RowCount > 0)
		{
			((Control)ClipboardButton).Enabled = Flag;
		}
	}

	private void FillPatternGrid()
	{
		//IL_0064: Unknown result type (might be due to invalid IL or missing references)
		((Control)this).Cursor = Cursors.WaitCursor;
		FindDGV.RowCount = 0;
		FindPatterns.EnterFindPatterns(GlobalForm.nDT[0, 0], GlobalForm.nDT[0, GlobalForm.HLCRange], FindingBar, ref StopPressed, 4);
		checked
		{
			if (GlobalForm.PatternCount == 0)
			{
				if (!SilentMode)
				{
					MessageBox.Show("I didn't find any chart patterns to trade in this security on this time scale (intraday/daily/weekly/monthly). Check the scale (click the Setup button), try another file ('<' or '>' buttons), or choose more patterns (Patterns button).\r\n\r\nYou can, however, continue to trade without using chart patterns (such as buying using a percentage down, up, or manually starting a trade). Just click the Start button.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				}
			}
			else
			{
				FindDGV.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)1;
				int num = 0;
				int num2 = GlobalForm.PatternCount - 1;
				for (int i = 0; i <= num2; i++)
				{
					if (GlobalForm.SimGlobals.FailuresOnly != 3)
					{
						GlobalForm.GetCPInformation(i);
					}
					decimal d = default(decimal);
					if ((decimal.Compare(GlobalForm.ChartPatterns[i].dBreakoutPrice, 0m) != 0) & (decimal.Compare(GlobalForm.ChartPatterns[i].UltHLPrice, 0m) != 0))
					{
						d = ((!GlobalForm.ChartPatterns[i].UltHiLow) ? decimal.Divide(decimal.Multiply(100m, decimal.Subtract(GlobalForm.ChartPatterns[i].dBreakoutPrice, GlobalForm.ChartPatterns[i].UltHLPrice)), GlobalForm.ChartPatterns[i].dBreakoutPrice) : decimal.Divide(decimal.Multiply(100m, decimal.Subtract(GlobalForm.ChartPatterns[i].UltHLPrice, GlobalForm.ChartPatterns[i].dBreakoutPrice)), GlobalForm.ChartPatterns[i].dBreakoutPrice));
					}
					if ((GlobalForm.SimGlobals.FailuresOnly == 3) | ((GlobalForm.SimGlobals.FailuresOnly == 1) & (decimal.Compare(d, new decimal(GlobalForm.SimGlobals.Percentage)) <= 0)) | ((GlobalForm.SimGlobals.FailuresOnly == 2) & (decimal.Compare(d, new decimal(GlobalForm.SimGlobals.Percentage)) > 0)))
					{
						FindDGV.Rows.Add();
						FindDGV.Rows[num].Cells[0].Value = GlobalForm.GetPatternPhrase(i);
						FindDGV.Rows[num].Cells[1].Value = Strings.Format((object)GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStartDate], GlobalForm.UserDate);
						FindDGV.Rows[num].Cells[2].Value = Strings.Format((object)GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEndDate], GlobalForm.UserDate);
						num++;
					}
				}
				FindDGV.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)6;
			}
			((Control)this).Cursor = Cursors.Default;
		}
	}

	private void FindDGV_CellClick(object sender, DataGridViewCellEventArgs e)
	{
		FindDGV.FirstDisplayedScrollingRowIndex = ((DataGridViewBand)FindDGV.SelectedRows[0]).Index;
		GlobalForm.Quiet = true;
		StartButton_Click(RuntimeHelpers.GetObjectValue(sender), (EventArgs)(object)e);
		if (GlobalForm.SimGlobals.AutoSetTargets)
		{
			SetTargetsButton_Click(RuntimeHelpers.GetObjectValue(sender), (EventArgs)(object)e);
		}
		if (GlobalForm.ChartPatterns[PatternIndex].iEndDate < GlobalForm.ChartStartIndex)
		{
			MessageLabel.Text = "The breakout is well after the pattern, so pattern is not visible on chart.";
		}
		GlobalForm.Quiet = false;
	}

	private void FindDGV_RowEnter(object sender, DataGridViewCellEventArgs e)
	{
		DGVRow(e.RowIndex);
	}

	private int FindPriceBars(DateTime Date1, DateTime Date2)
	{
		int result = 0;
		checked
		{
			if (DateTime.Compare(Date1, Date2) != 0)
			{
				int hLCRange = GlobalForm.HLCRange;
				int num = default(int);
				for (int i = 0; i <= hLCRange; i++)
				{
					if (DateTime.Compare(Date1, Date2) < 0)
					{
						if (DateTime.Compare(GlobalForm.nDT[0, i], Date1) == 0)
						{
							num = i;
						}
						if (DateTime.Compare(GlobalForm.nDT[0, i], Date2) == 0)
						{
							result = num - i;
							break;
						}
					}
					else if (DateTime.Compare(Date1, Date2) > 0)
					{
						if (DateTime.Compare(GlobalForm.nDT[0, i], Date2) == 0)
						{
							num = i;
						}
						if (DateTime.Compare(GlobalForm.nDT[0, i], Date1) == 0)
						{
							result = i - num;
							break;
						}
					}
				}
			}
			return result;
		}
	}

	private void HelpTradeButton_Click(object sender, EventArgs e)
	{
		//IL_007b: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat("Shares: Enter the number of shares you wish to trade.\r\n\r\n" + "Target Price: If you have a price at which you want to sell (or cover a short), then enter it. Use 0 otherwise.\r\n\r\n", "Buy Price: If you have a price at which you want to buy (or enter a short sale), then enter it. Use 0 otherwise.\r\n\r\n"), "Stop Price: If the trade goes bad, this would be the sell (or cover) price. Use 0 if you don't want to use a stop.\r\n\r\n"), "Clear button: Sets the target, buy, and stop prices to 0.\r\n\r\n"), "Limit order: This says you'll buy for no more or sell for no less than what is specified in the buy price box.\r\n\r\n"), "Short sale: Check the box to sell short. Check this box BEFORE clicking the Set Targets button (because long side and short-sale targets are different).\r\n\r\n"), "Clipboard: Copy all trading results to the clipboard.\r\n\r\n"), "Sell Now: Sell (or cover a short sale) the stock at the opening price of the next price bar.\r\n\r\n"), "Buy Now: Buy the stock (or enter a short sale) at the opening price of the next price bar.\r\n\r\n"), "The Set Targets button will fill in the target, buy, and stop prices for you (the prices depending on the state of the 'Short sale' check box)."), " Prices are a penny away from the top/bottom of the pattern and the target price is based on the pattern's height (which may be different from the pattern's measure rule target)."), "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void MeasureRuleButton_Click(object sender, EventArgs e)
	{
		//IL_0450: Unknown result type (might be due to invalid IL or missing references)
		//IL_043c: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			if ((PatternIndex != -1) & (Operators.CompareString(GlobalForm.CPInfo.BkoutPrice, (string)null, false) != 0))
			{
				int ReturnStart = default(int);
				int ReturnEnd = default(int);
				GlobalForm.GetStartEndDates(PatternIndex, ref ReturnStart, ref ReturnEnd);
				int num = ReturnStart;
				int num2 = ReturnStart;
				int num3 = ReturnStart + 1;
				int num4 = ReturnEnd;
				for (int i = num3; i <= num4; i++)
				{
					num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0, (object)i, (object)num));
					num2 = Conversions.ToInteger(Interaction.IIf((decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num2]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i], 0m) != 0), (object)i, (object)num2));
				}
				decimal num5 = decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num2]);
				string text = "The height of the patten is " + GlobalForm.LimitDecimals(Strings.Format((object)num5, "")) + ", so the measure rule target for up breakouts is:\r\n\r\n";
				text = text + "1x height: " + Strings.Format((object)GlobalForm.LimitDecimals(decimal.Add(GlobalForm.nHLC[1, num], num5)), "") + "\r\n";
				text = text + "2x height: " + Strings.Format((object)GlobalForm.LimitDecimals(decimal.Add(GlobalForm.nHLC[1, num], decimal.Multiply(2m, num5))), "") + "\r\n";
				text = text + "3x height: " + Strings.Format((object)GlobalForm.LimitDecimals(decimal.Add(GlobalForm.nHLC[1, num], decimal.Multiply(3m, num5))), "") + "\r\n";
				text = text + "4x height: " + Strings.Format((object)GlobalForm.LimitDecimals(decimal.Add(GlobalForm.nHLC[1, num], decimal.Multiply(4m, num5))), "") + "\r\n";
				text += "\r\nAnd for downward breakouts:\r\n\r\n";
				text = ((decimal.Compare(decimal.Subtract(GlobalForm.nHLC[2, num2], num5), 0m) <= 0) ? (text + "1x height: 0") : (text + "1x height: " + Strings.Format((object)GlobalForm.LimitDecimals(decimal.Subtract(GlobalForm.nHLC[2, num2], num5)), "") + "\r\n"));
				text = ((decimal.Compare(decimal.Subtract(GlobalForm.nHLC[2, num2], decimal.Multiply(2m, num5)), 0m) <= 0) ? (text + "2x height: 0") : (text + "2x height: " + Strings.Format((object)GlobalForm.LimitDecimals(decimal.Subtract(GlobalForm.nHLC[2, num2], decimal.Multiply(2m, num5))), "") + "\r\n"));
				text = ((decimal.Compare(decimal.Subtract(GlobalForm.nHLC[2, num2], decimal.Multiply(3m, num5)), 0m) <= 0) ? (text + "3x height: 0") : (text + "3x height: " + Strings.Format((object)GlobalForm.LimitDecimals(decimal.Subtract(GlobalForm.nHLC[2, num2], decimal.Multiply(3m, num5))), "") + "\r\n"));
				text = ((decimal.Compare(decimal.Subtract(GlobalForm.nHLC[2, num2], decimal.Multiply(4m, num5)), 0m) <= 0) ? (text + "4x height: 0") : (text + "4x height: " + Strings.Format((object)GlobalForm.LimitDecimals(decimal.Subtract(GlobalForm.nHLC[2, num2], decimal.Multiply(4m, num5))), "") + "\r\n"));
				MessageBox.Show(text, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
			else
			{
				MessageBox.Show("Unable to find the breakout price or chart pattern.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			}
		}
	}

	private void NextButton_Click(object sender, EventArgs e)
	{
		//IL_00b7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c1: Expected O, but got Unknown
		//IL_028a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0294: Expected O, but got Unknown
		((Control)this).Cursor = Cursors.WaitCursor;
		PatternIndex = -1;
		EnableDisable(Flag: false);
		((Control)Chart1).Enabled = false;
		((Control)StopButton).Enabled = false;
		((Control)SpeedSB).Enabled = false;
		((Control)StopSkip).Enabled = true;
		bStopSkip = false;
		((Control)ResumeButton).Enabled = false;
		((Control)SetTargetsButton).Enabled = false;
		StopPressed = false;
		ClearBtn_Click(RuntimeHelpers.GetObjectValue(sender), e);
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
		CurrentAnnotation = new CalloutAnnotation();
		((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)CurrentAnnotation);
		checked
		{
			while (!bStopSkip)
			{
				GlobalForm.LBIndex++;
				if (GlobalForm.LBIndex >= MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count)
				{
					GlobalForm.LBIndex = MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count - 1;
					Interaction.Beep();
					break;
				}
				GlobalForm.FirstPoint = default(Point);
				GlobalForm.LinesList.RemoveAll(StubBoolean);
				Filename = MyProject.Forms.Mainform.ListBox1.SelectedItems[GlobalForm.LBIndex].ToString();
				((Form)this).Text = "Simulator Form: " + Filename;
				string filename = Filename;
				ProgressBar ProgBar = LoadingBar;
				Label ErrorLabel = MessageLabel;
				bool num = GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.ChartPeriodShown);
				MessageLabel = ErrorLabel;
				LoadingBar = ProgBar;
				if (num)
				{
					break;
				}
				GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
				GlobalForm.SelectChartType(Chart1);
				AfterLoadFile();
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Clear();
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Clear();
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points).Clear();
				FillPatternGrid();
				if (!((FindDGV.RowCount == 0) & SkipCB.Checked))
				{
					if (FindDGV.RowCount > 0)
					{
						FindDGV_CellClick(FindDGV, new DataGridViewCellEventArgs(0, 0));
					}
					break;
				}
			}
			EnableDisable(Flag: true);
			((Control)Chart1).Enabled = true;
			((Control)SpeedSB).Enabled = true;
			((Control)StopSkip).Enabled = false;
			((Control)this).Cursor = Cursors.Default;
		}
	}

	private void PatternsButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.PatternsForm).ShowDialog();
		PatternIndex = -1;
		FindDGV.RowCount = 0;
		FillPatternGrid();
	}

	private void PercentButton_Click(object sender, EventArgs e)
	{
		//IL_0540: Unknown result type (might be due to invalid IL or missing references)
		string text = "Right mouse click two price bars and then the % button to show the percentage rise or fall.\r\n\r\n";
		if ((GlobalForm.iFib1 != -1) & (GlobalForm.iFib2 != -1))
		{
			string text2;
			string text3;
			string text4;
			string text5;
			string text6;
			if (GlobalForm.iFib1 < GlobalForm.iFib2)
			{
				text2 = "1 to 2";
				if (decimal.Compare(GlobalForm.nHLC[1, GlobalForm.iFib1], GlobalForm.nHLC[2, GlobalForm.iFib2]) > 0)
				{
					text3 = "high to low";
					text4 = "fall";
					text5 = Strings.Format((object)decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, GlobalForm.iFib1], GlobalForm.nHLC[2, GlobalForm.iFib2]), GlobalForm.nHLC[1, GlobalForm.iFib1]), "0.0%");
					text6 = Strings.Format((object)decimal.Divide(decimal.Subtract(GlobalForm.nHLC[3, GlobalForm.iFib1], GlobalForm.nHLC[3, GlobalForm.iFib2]), GlobalForm.nHLC[3, GlobalForm.iFib1]), "0.0%");
				}
				else
				{
					text3 = "low to high";
					text4 = "rise";
					text5 = Strings.Format((object)decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, GlobalForm.iFib2], GlobalForm.nHLC[2, GlobalForm.iFib1]), GlobalForm.nHLC[2, GlobalForm.iFib1]), "0.0%");
					text6 = Strings.Format((object)decimal.Divide(decimal.Subtract(GlobalForm.nHLC[3, GlobalForm.iFib2], GlobalForm.nHLC[3, GlobalForm.iFib1]), GlobalForm.nHLC[3, GlobalForm.iFib1]), "0.0%");
				}
			}
			else
			{
				text2 = "2 to 1";
				if (decimal.Compare(GlobalForm.nHLC[1, GlobalForm.iFib1], GlobalForm.nHLC[2, GlobalForm.iFib2]) > 0)
				{
					text3 = "low to high";
					text4 = "rise";
					text5 = Strings.Format((object)decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, GlobalForm.iFib1], GlobalForm.nHLC[2, GlobalForm.iFib2]), GlobalForm.nHLC[2, GlobalForm.iFib2]), "0.0%");
					text6 = Strings.Format((object)decimal.Divide(decimal.Subtract(GlobalForm.nHLC[3, GlobalForm.iFib1], GlobalForm.nHLC[3, GlobalForm.iFib2]), GlobalForm.nHLC[3, GlobalForm.iFib2]), "0.0%");
				}
				else
				{
					text3 = "high to low";
					text4 = "fall";
					text5 = Strings.Format((object)decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, GlobalForm.iFib2], GlobalForm.nHLC[2, GlobalForm.iFib1]), GlobalForm.nHLC[1, GlobalForm.iFib2]), "0.0%");
					text6 = Strings.Format((object)decimal.Divide(decimal.Subtract(GlobalForm.nHLC[3, GlobalForm.iFib2], GlobalForm.nHLC[3, GlobalForm.iFib1]), GlobalForm.nHLC[3, GlobalForm.iFib2]), "0.0%");
				}
			}
			text = text + "Bar 1, " + Strings.Format((object)GlobalForm.nDT[0, GlobalForm.iFib1], "yyyy-MM-dd HH:mm") + "\r\n";
			text = text + "Bar 1, open: $" + Conversions.ToString(GlobalForm.nHLC[0, GlobalForm.iFib1]) + "\r\n";
			text = text + "Bar 1, high: $" + Conversions.ToString(GlobalForm.nHLC[1, GlobalForm.iFib1]) + "\r\n";
			text = text + "Bar 1, low: $" + Conversions.ToString(GlobalForm.nHLC[2, GlobalForm.iFib1]) + "\r\n";
			text = text + "Bar 1, close: $" + Conversions.ToString(GlobalForm.nHLC[3, GlobalForm.iFib1]) + "\r\n\r\n";
			text = text + "Bar 2, " + Strings.Format((object)GlobalForm.nDT[0, GlobalForm.iFib2], "yyyy-MM-dd HH:mm") + "\r\n";
			text = text + "Bar 2, open: $" + Conversions.ToString(GlobalForm.nHLC[0, GlobalForm.iFib2]) + "\r\n";
			text = text + "Bar 2, high: $" + Conversions.ToString(GlobalForm.nHLC[1, GlobalForm.iFib2]) + "\r\n";
			text = text + "Bar 2, low: $" + Conversions.ToString(GlobalForm.nHLC[2, GlobalForm.iFib2]) + "\r\n";
			text = text + "Bar 2, close: $" + Conversions.ToString(GlobalForm.nHLC[3, GlobalForm.iFib2]) + "\r\n\r\n";
			text = text + "Percentage " + text4 + ", from bar " + text2 + ", " + text3 + ": " + text5;
			text = text + "\r\nClose to close from bar " + text2 + ": " + text6;
			PercentCircles = true;
			Chart1.Invalidate();
		}
		MessageBox.Show(text, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void PreviousButton_Click(object sender, EventArgs e)
	{
		//IL_00b7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c1: Expected O, but got Unknown
		//IL_0258: Unknown result type (might be due to invalid IL or missing references)
		//IL_0262: Expected O, but got Unknown
		((Control)this).Cursor = Cursors.WaitCursor;
		PatternIndex = -1;
		EnableDisable(Flag: false);
		((Control)Chart1).Enabled = false;
		((Control)SpeedSB).Enabled = false;
		((Control)StopButton).Enabled = false;
		((Control)StopSkip).Enabled = true;
		bStopSkip = false;
		((Control)ResumeButton).Enabled = false;
		((Control)SetTargetsButton).Enabled = false;
		StopPressed = false;
		ClearBtn_Click(RuntimeHelpers.GetObjectValue(sender), e);
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
		CurrentAnnotation = new CalloutAnnotation();
		((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)CurrentAnnotation);
		checked
		{
			while (!bStopSkip)
			{
				GlobalForm.LBIndex--;
				if (GlobalForm.LBIndex < 0)
				{
					GlobalForm.LBIndex = 0;
					Interaction.Beep();
					break;
				}
				GlobalForm.FirstPoint = default(Point);
				GlobalForm.LinesList.RemoveAll(StubBoolean);
				Filename = MyProject.Forms.Mainform.ListBox1.SelectedItems[GlobalForm.LBIndex].ToString();
				((Form)this).Text = "Simulator Form: " + Filename;
				string filename = Filename;
				ProgressBar ProgBar = LoadingBar;
				Label ErrorLabel = MessageLabel;
				bool num = GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.ChartPeriodShown);
				MessageLabel = ErrorLabel;
				LoadingBar = ProgBar;
				if (num)
				{
					break;
				}
				GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
				GlobalForm.SelectChartType(Chart1);
				AfterLoadFile();
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Clear();
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Clear();
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points).Clear();
				FillPatternGrid();
				if (!((FindDGV.RowCount == 0) & SkipCB.Checked))
				{
					if (FindDGV.RowCount > 0)
					{
						FindDGV_CellClick(FindDGV, new DataGridViewCellEventArgs(0, 0));
					}
					break;
				}
			}
			EnableDisable(Flag: true);
			((Control)Chart1).Enabled = true;
			((Control)SpeedSB).Enabled = true;
			((Control)StopSkip).Enabled = false;
			((Control)this).Cursor = Cursors.Default;
		}
	}

	private void ReadConfigFile()
	{
		//IL_006c: Unknown result type (might be due to invalid IL or missing references)
		BinaryFormatter binaryFormatter = new BinaryFormatter();
		ConfigPath = GlobalForm.ConfigLocation + GlobalForm.SimulatorCfg;
		if (File.Exists(ConfigPath))
		{
			try
			{
				Stream stream = File.OpenRead(ConfigPath);
				object obj = binaryFormatter.Deserialize(stream);
				GlobalForm.SimGlobals = ((obj != null) ? ((GlobalForm.SimStruct)obj) : default(GlobalForm.SimStruct));
				stream.Close();
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				MessageBox.Show(ex2.Message);
				ProjectData.ClearProjectError();
			}
			try
			{
				((ScrollBar)SpeedSB).Value = GlobalForm.SimGlobals.Speed;
			}
			catch (Exception ex3)
			{
				ProjectData.SetProjectError(ex3);
				Exception ex4 = ex3;
				((ScrollBar)SpeedSB).Value = 1500;
				GlobalForm.SimGlobals.Speed = 1500;
				ProjectData.ClearProjectError();
			}
		}
		else
		{
			GlobalForm.SimGlobals.Annotations = GlobalForm.Annotations;
			GlobalForm.SimGlobals.FindCandles = GlobalForm.ShowCandles;
			GlobalForm.SimGlobals.ShowCircles = true;
			GlobalForm.SimGlobals.Strict = GlobalForm.StrictPatterns;
			GlobalForm.SimGlobals.Volume = GlobalForm.ChartVolume;
			GlobalForm.SimGlobals.MovingAvg = GlobalForm.MAUsed;
			GlobalForm.SimGlobals.MAType = GlobalForm.MAType;
			GlobalForm.SimGlobals.MALength = GlobalForm.MALength;
			GlobalForm.SimGlobals.TimeScale = GlobalForm.ChartPeriodShown;
			GlobalForm.SimGlobals.Speed = 1500;
			GlobalForm.SimGlobals.Lookback = 262;
			GlobalForm.SimGlobals.SECFee = 20.7m;
			GlobalForm.SimGlobals.SECBool = true;
			GlobalForm.SimGlobals.Commissions = 4.95m;
			GlobalForm.SimGlobals.StopUltHigh = false;
			GlobalForm.SimGlobals.StopUltLow = false;
			GlobalForm.SimGlobals.FailuresOnly = 3;
			GlobalForm.SimGlobals.Percentage = 5;
			GlobalForm.SimGlobals.CloseAboveTL = false;
			GlobalForm.SimGlobals.CloseBelowTL = false;
			GlobalForm.SimGlobals.StopPctDown = false;
			GlobalForm.SimGlobals.StopPctUp = false;
		}
		GlobalForm.Annotations = GlobalForm.SimGlobals.Annotations;
		GlobalForm.ShowCandles = GlobalForm.SimGlobals.FindCandles;
		GlobalForm.ShowAllPatterns = true;
		GlobalForm.StrictPatterns = GlobalForm.SimGlobals.Strict;
		GlobalForm.ChartVolume = GlobalForm.SimGlobals.Volume;
		GlobalForm.MAUsed = GlobalForm.SimGlobals.MovingAvg;
		GlobalForm.MAType = GlobalForm.SimGlobals.MAType;
		GlobalForm.MALength = GlobalForm.SimGlobals.MALength;
		GlobalForm.ChartPeriodShown = GlobalForm.SimGlobals.TimeScale;
	}

	private void Restart()
	{
		EnableDisable(Flag: false);
		GlobalForm.FirstPoint = default(Point);
		GlobalForm.LinesList.RemoveAll(StubBoolean);
		TimerRunFlag = true;
		Timer1.Enabled = true;
		((Control)StopButton).Focus();
		Trade.PriceTarget = TargetNum.Value;
		Trade.BuyPrice = BuyPriceNum.Value;
		Trade.PriceStop = StopPriceNum.Value;
		Trade.Shares = Convert.ToInt32(SharesNum.Value);
		Trade.tShort = ShortSaleCB.Checked;
		bool flag;
		bool flag2;
		bool flag3;
		checked
		{
			if (GlobalForm.MAUsed)
			{
				MovAvg = default(decimal);
				EMASeed = true;
				if (GlobalForm.MAType == 2)
				{
					Alpha = new decimal(2.0 / (double)(GlobalForm.MALength + 1));
				}
				int chartEndIndex = GlobalForm.ChartEndIndex;
				for (int i = 0; i <= chartEndIndex; i++)
				{
					ref decimal movAvg = ref MovAvg;
					movAvg = decimal.Add(movAvg, GlobalForm.nHLC[3, i]);
					if (i > GlobalForm.MALength - 1)
					{
						ref decimal movAvg2 = ref MovAvg;
						movAvg2 = decimal.Subtract(movAvg2, GlobalForm.nHLC[3, i - GlobalForm.MALength]);
					}
				}
			}
			flag = (((GlobalForm.PatternList[57] == 1) | (GlobalForm.PatternList[58] == 1)) ? true : false);
			flag2 = false;
			flag3 = Conversions.ToBoolean(Interaction.IIf(GlobalForm.SimGlobals.StopUltHigh | GlobalForm.SimGlobals.StopUltLow, (object)false, (object)true));
		}
		do
		{
			((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
			if (StopPressed)
			{
				break;
			}
			if (!TimerRunFlag)
			{
				continue;
			}
			TimerRunFlag = false;
			UpdateChart();
			if (!flag2)
			{
				CheckTrade();
				if (StopPressed && !flag3)
				{
					flag2 = true;
					StopPressed = false;
				}
			}
			if (!flag3)
			{
				if (GlobalForm.SimGlobals.StopUltHigh & (Trade.UpBreakoutDirection == 1) & (GlobalForm.ChartEndIndex > Trade.iUltHigh) & (Trade.iUltHigh != -1))
				{
					flag3 = true;
				}
				if (GlobalForm.SimGlobals.StopUltLow & (Trade.UpBreakoutDirection == -1) & (GlobalForm.ChartEndIndex > Trade.iUltLow) & (Trade.iUltLow != -1))
				{
					flag3 = true;
				}
				if (flag3)
				{
					StopPressed = true;
				}
			}
			if (flag && GlobalForm.CPInfo.iBkout != -1 && (GlobalForm.SimGlobals.CloseAboveTL | (GlobalForm.SimGlobals.CloseBelowTL & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.CPInfo.iBkout], ToDatePicker.Value) == 0))))
			{
				StopPressed = true;
			}
			if (GlobalForm.SimGlobals.StopPctDown & ResetPctDownTrade)
			{
				StopPressed = true;
			}
			if (GlobalForm.SimGlobals.StopPctUp & ResetPctUpTrade)
			{
				StopPressed = true;
			}
		}
		while (!StopPressed);
		ResetPctDownTrade = false;
		ResetPctUpTrade = false;
		StopPressed = false;
		EnableDisable(Flag: true);
		((Control)ResumeButton).Enabled = true;
		((Control)SetTargetsButton).Enabled = true;
	}

	private void ResumeButton_Click(object sender, EventArgs e)
	{
		//IL_0090: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e6: Unknown result type (might be due to invalid IL or missing references)
		((Control)ResumeButton).Enabled = false;
		((Control)SetTargetsButton).Enabled = false;
		Restart();
		if (DateTime.Compare(ToDatePicker.Value, GlobalForm.nDT[0, GlobalForm.HLCRange]) >= 0)
		{
			((Control)ResumeButton).Enabled = false;
			if (Trade.InProgress)
			{
				if (!Trade.tShort)
				{
					SellButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
				}
				else
				{
					BuyButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
				}
			}
			MessageBox.Show("End of data reached.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
		else if (!StopPressed && (!Trade.InProgress & !Trade.TradeReady))
		{
			((Control)BuyButton).Enabled = false;
			((Control)SellButton).Enabled = false;
			MessageBox.Show("Trade complete.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			if (GlobalForm.SimGlobals.StopPctDown)
			{
				((Control)BuyButton).Enabled = true;
				((Control)SellButton).Enabled = true;
				Trade.TradeReady = true;
				BuyPriceNum.Value = 0m;
			}
		}
	}

	private void SellButton_Click(object sender, EventArgs e)
	{
		checked
		{
			if (Trade.InProgress)
			{
				if (GlobalForm.ChartEndIndex + 1 <= GlobalForm.HLCRange)
				{
					Trade.SellPrice = GlobalForm.nHLC[0, GlobalForm.ChartEndIndex + 1];
					Trade.SellDate = GlobalForm.nDT[0, GlobalForm.ChartEndIndex + 1];
					Trade.iSell = GlobalForm.ChartEndIndex + 1;
				}
				else
				{
					Trade.SellPrice = GlobalForm.nHLC[3, GlobalForm.HLCRange];
					Trade.SellDate = GlobalForm.nDT[0, GlobalForm.HLCRange];
					Trade.iSell = GlobalForm.HLCRange;
				}
				Trade.InProgress = false;
				StopPressed = true;
				Trade.SellStatus = Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartEndIndex >= GlobalForm.HLCRange, (object)7, (object)6));
				ref decimal commissions = ref Trade.Commissions;
				commissions = decimal.Add(commissions, GlobalForm.SimGlobals.Commissions);
				if (GlobalForm.SimGlobals.SECBool)
				{
					Trade.Fees = decimal.Multiply(decimal.Multiply(decimal.Divide(GlobalForm.SimGlobals.SECFee, 1000000m), new decimal(Trade.Shares)), Trade.SellPrice);
				}
				TradeReport();
			}
			else if (Trade.TradeReady)
			{
				if (GlobalForm.ChartEndIndex + 1 <= GlobalForm.HLCRange)
				{
					Trade.SellPrice = GlobalForm.nHLC[0, GlobalForm.ChartEndIndex + 1];
					Trade.SellDate = GlobalForm.nDT[0, GlobalForm.ChartEndIndex + 1];
					Trade.iSell = GlobalForm.ChartEndIndex + 1;
				}
				else
				{
					Trade.SellPrice = GlobalForm.nHLC[3, GlobalForm.HLCRange];
					Trade.SellDate = GlobalForm.nDT[0, GlobalForm.HLCRange];
					Trade.iSell = GlobalForm.HLCRange;
				}
				Trade.InProgress = true;
				Trade.tShort = true;
				ShortSaleCB.Checked = true;
				Trade.BuyStatus = Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartEndIndex >= GlobalForm.HLCRange, (object)7, (object)6));
				Trade.Commissions = GlobalForm.SimGlobals.Commissions;
				if (GlobalForm.SimGlobals.SECBool)
				{
					Trade.Fees = decimal.Multiply(decimal.Multiply(decimal.Divide(GlobalForm.SimGlobals.SECFee, 1000000m), new decimal(Trade.Shares)), Trade.SellPrice);
				}
				((Control)BuyButton).Enabled = true;
				((Control)SellButton).Enabled = false;
			}
		}
	}

	private void SetMinMax()
	{
		StkMin = GlobalForm.nHLC[2, GlobalForm.ChartStartIndex];
		StkMax = GlobalForm.nHLC[1, GlobalForm.ChartStartIndex];
		if (GlobalForm.ChartVolume)
		{
			VolMax = Convert.ToInt64(GlobalForm.nHLC[4, GlobalForm.ChartStartIndex]);
		}
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				StkMin = Conversions.ToDecimal(Interaction.IIf((decimal.Compare(StkMin, 0m) == 0) | ((decimal.Compare(GlobalForm.nHLC[2, i], StkMin) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i], 0m) > 0)), (object)GlobalForm.nHLC[2, i], (object)StkMin));
				StkMax = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], StkMax) > 0, (object)GlobalForm.nHLC[1, i], (object)StkMax));
				if (GlobalForm.ChartVolume)
				{
					VolMax = Conversions.ToLong(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[4, i], new decimal(VolMax)) > 0, (object)GlobalForm.nHLC[4, i], (object)VolMax));
				}
			}
			ref decimal stkMax = ref StkMax;
			stkMax = decimal.Add(stkMax, decimal.Divide(decimal.Subtract(StkMax, StkMin), 10m));
		}
	}

	private void SetTargetsButton_Click(object sender, EventArgs e)
	{
		//IL_02d4: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			if ((PatternIndex != -1) & (Operators.CompareString(GlobalForm.CPInfo.BkoutPrice, (string)null, false) != 0))
			{
				int ReturnStart = default(int);
				int ReturnEnd = default(int);
				GlobalForm.GetStartEndDates(PatternIndex, ref ReturnStart, ref ReturnEnd);
				int num = ReturnStart;
				int num2 = ReturnStart;
				int num3 = ReturnStart + 1;
				int num4 = ReturnEnd;
				for (int i = num3; i <= num4; i++)
				{
					num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0, (object)i, (object)num));
					num2 = Conversions.ToInteger(Interaction.IIf((decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num2]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i], 0m) != 0), (object)i, (object)num2));
				}
				decimal d = decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num2]);
				if (ShortSaleCB.Checked)
				{
					if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[2, num2], d), 0m) < 0)
					{
						TargetNum.Value = 0m;
					}
					else
					{
						TargetNum.Value = GlobalForm.LimitDecimals(decimal.Subtract(GlobalForm.nHLC[2, num2], d));
					}
					if (Operators.CompareString(GlobalForm.CPInfo.BkoutPrice, (string)null, false) == 0)
					{
						BuyPriceNum.Value = decimal.Subtract(GlobalForm.nHLC[2, num2], 0.01m);
					}
					else
					{
						BuyPriceNum.Value = GlobalForm.LimitDecimals(decimal.Subtract(Conversions.ToDecimal(GlobalForm.CPInfo.BkoutPrice), 0.01m));
					}
					StopPriceNum.Value = GlobalForm.LimitDecimals(decimal.Add(GlobalForm.nHLC[1, num], 0.01m));
				}
				else
				{
					TargetNum.Value = GlobalForm.LimitDecimals(decimal.Add(GlobalForm.nHLC[1, num], d));
					if (Operators.CompareString(GlobalForm.CPInfo.BkoutPrice, (string)null, false) == 0)
					{
						BuyPriceNum.Value = decimal.Add(GlobalForm.nHLC[1, num], 0.01m);
					}
					else
					{
						BuyPriceNum.Value = GlobalForm.LimitDecimals(decimal.Add(Conversions.ToDecimal(GlobalForm.CPInfo.BkoutPrice), 0.01m));
					}
					StopPriceNum.Value = GlobalForm.LimitDecimals(decimal.Subtract(GlobalForm.nHLC[2, num2], 0.01m));
				}
				MessageLabel.Text = "Target prices have been filled in.";
			}
			else
			{
				MessageBox.Show("Unable to find the breakout price or chart pattern.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			}
		}
	}

	private void SetupButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0131: Unknown result type (might be due to invalid IL or missing references)
		//IL_013b: Expected O, but got Unknown
		((Form)MyProject.Forms.SimSetupForm).ShowDialog();
		PatternIndex = -1;
		if (!GlobalForm.Annotations)
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
		}
		string filename = Filename;
		ProgressBar ProgBar = LoadingBar;
		Label ErrorLabel = MessageLabel;
		bool num = GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.ChartPeriodShown);
		MessageLabel = ErrorLabel;
		LoadingBar = ProgBar;
		if (!num)
		{
			GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
			GlobalForm.SelectChartType(Chart1);
			AfterLoadFile();
			((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Clear();
			((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Clear();
			((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points).Clear();
			FillPatternGrid();
			if (FindDGV.RowCount > 0)
			{
				FindDGV_CellClick(FindDGV, new DataGridViewCellEventArgs(0, 0));
			}
			else
			{
				((Control)ResumeButton).Enabled = false;
			}
		}
		else
		{
			((Control)ResumeButton).Enabled = false;
		}
	}

	private void ShowBearMarkets(ChartPaintEventArgs e, int l)
	{
		checked
		{
			int num = GlobalForm.BearMkts.Length - 1;
			PointF absolutePoint = default(PointF);
			PointF absolutePoint2 = default(PointF);
			PointF absolutePoint3 = default(PointF);
			for (int i = 0; i <= num; i++)
			{
				if (((GlobalForm.ChartPeriodShown == 0) & (DateTime.Compare(GlobalForm.nDT[0, l + GlobalForm.ChartStartIndex], GlobalForm.BearMkts[i].StartDate) == 0)) | ((GlobalForm.ChartPeriodShown == 1) & (DateTime.Compare(GlobalForm.nDT[0, l + GlobalForm.ChartStartIndex], GlobalForm.BearMkts[i].StartDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, l + GlobalForm.ChartStartIndex], DateAndTime.DateAdd((DateInterval)4, 7.0, GlobalForm.BearMkts[i].StartDate)) < 0)) | ((GlobalForm.ChartPeriodShown == 2) & (DateTime.Compare(GlobalForm.nDT[0, l + GlobalForm.ChartStartIndex], GlobalForm.BearMkts[i].StartDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, l + GlobalForm.ChartStartIndex], DateAndTime.DateAdd((DateInterval)2, 1.0, GlobalForm.BearMkts[i].StartDate)) < 0)))
				{
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(l + 1));
					absolutePoint.Y = 100f;
					absolutePoint2.X = absolutePoint.X;
					absolutePoint3.X = absolutePoint.X;
					absolutePoint2.Y = 0f;
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
					e.ChartGraphics.Graphics.DrawLine(MyPen, absolutePoint, absolutePoint2);
					absolutePoint3.Y = 90f;
					absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
					e.ChartGraphics.Graphics.DrawString(GlobalForm.BearMkts[i].Text, BoldFont, Brushes.Red, absolutePoint3);
				}
				if (((GlobalForm.ChartPeriodShown == 0) & (DateTime.Compare(GlobalForm.nDT[0, l + GlobalForm.ChartStartIndex], GlobalForm.BearMkts[i].EndDate) == 0)) | ((GlobalForm.ChartPeriodShown == 1) & (DateTime.Compare(GlobalForm.nDT[0, l + GlobalForm.ChartStartIndex], GlobalForm.BearMkts[i].EndDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, l + GlobalForm.ChartStartIndex], DateAndTime.DateAdd((DateInterval)4, 7.0, GlobalForm.BearMkts[i].EndDate)) < 0)) | ((GlobalForm.ChartPeriodShown == 2) & (DateTime.Compare(GlobalForm.nDT[0, l + GlobalForm.ChartStartIndex], GlobalForm.BearMkts[i].EndDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, l + GlobalForm.ChartStartIndex], DateAndTime.DateAdd((DateInterval)2, 1.0, GlobalForm.BearMkts[i].EndDate)) < 0)))
				{
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(l + 1));
					absolutePoint.Y = 100f;
					absolutePoint2.X = absolutePoint.X;
					absolutePoint3.X = absolutePoint.X;
					absolutePoint2.Y = 0f;
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
					e.ChartGraphics.Graphics.DrawLine(MyPen, absolutePoint, absolutePoint2);
					absolutePoint3.Y = 90f;
					absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
					absolutePoint3.X -= 4f * GlobalForm.StringSize.Width + 5f;
					e.ChartGraphics.Graphics.DrawString("Bear end", BoldFont, Brushes.Red, absolutePoint3);
				}
			}
		}
	}

	private void ShowCircles(ChartPaintEventArgs e, DataPoint point, int l, ref int NumberShowPoints)
	{
		//IL_0095: Unknown result type (might be due to invalid IL or missing references)
		//IL_009b: Expected O, but got Unknown
		//IL_0171: Unknown result type (might be due to invalid IL or missing references)
		//IL_0178: Expected O, but got Unknown
		//IL_0250: Unknown result type (might be due to invalid IL or missing references)
		//IL_0257: Expected O, but got Unknown
		//IL_032f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0336: Expected O, but got Unknown
		ChartGraphics chartGraphics = e.ChartGraphics;
		int num = 8;
		checked
		{
			PointF absolutePoint = default(PointF);
			if (Trade.iBuy != -1 && l + GlobalForm.ChartStartIndex == Trade.iBuy)
			{
				absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(l + 1));
				absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, point.YValues[1]);
				absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				absolutePoint.Y += 6f;
				SolidBrush val = new SolidBrush(Color.Blue);
				chartGraphics.Graphics.FillEllipse((Brush)(object)val, (float)((double)absolutePoint.X - (double)num / 2.0), (float)((double)absolutePoint.Y + (double)num / 2.0), (float)num, (float)num);
				((Brush)val).Dispose();
				NumberShowPoints--;
			}
			if (Trade.iSell != -1 && l + GlobalForm.ChartStartIndex == Trade.iSell)
			{
				absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(l + 1));
				absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, point.YValues[0]);
				absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				absolutePoint.Y -= 20f;
				SolidBrush val2 = new SolidBrush(Color.Red);
				chartGraphics.Graphics.FillEllipse((Brush)(object)val2, (float)((double)absolutePoint.X - (double)num / 2.0), (float)((double)absolutePoint.Y + (double)num / 2.0), (float)num, (float)num);
				((Brush)val2).Dispose();
				NumberShowPoints--;
			}
			if (Trade.iUltHigh != -1 && l + GlobalForm.ChartStartIndex == Trade.iUltHigh)
			{
				absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(l + 1));
				absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, point.YValues[0]);
				absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				absolutePoint.Y -= 25f;
				SolidBrush val3 = new SolidBrush(Color.Green);
				chartGraphics.Graphics.FillEllipse((Brush)(object)val3, (float)((double)absolutePoint.X - (double)num / 2.0), (float)((double)absolutePoint.Y + (double)num / 2.0), (float)num, (float)num);
				((Brush)val3).Dispose();
				NumberShowPoints--;
			}
			if (Trade.iUltLow != -1 && l + GlobalForm.ChartStartIndex == Trade.iUltLow)
			{
				absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(l + 1));
				absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, point.YValues[1]);
				absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				absolutePoint.Y += 12f;
				SolidBrush val4 = new SolidBrush(Color.Violet);
				chartGraphics.Graphics.FillEllipse((Brush)(object)val4, (float)((double)absolutePoint.X - (double)num / 2.0), (float)((double)absolutePoint.Y + (double)num / 2.0), (float)num, (float)num);
				((Brush)val4).Dispose();
				NumberShowPoints--;
			}
		}
	}

	private void ShowPercent(ChartPaintEventArgs e)
	{
		//IL_0024: Unknown result type (might be due to invalid IL or missing references)
		//IL_0044: Unknown result type (might be due to invalid IL or missing references)
		//IL_004b: Expected O, but got Unknown
		int num = 4;
		if (!PercentCircles || !(e.ChartElement is Series) || Operators.CompareString(((Series)e.ChartElement).Name, "CandleSeries", false) != 0)
		{
			return;
		}
		Series val = (Series)e.ChartElement;
		PercentCircles = false;
		int num2 = 0;
		int num3 = default(int);
		int num4 = default(int);
		if ((GlobalForm.iFib1 != -1) & (GlobalForm.iFib2 != -1))
		{
			num3 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, GlobalForm.iFib1], GlobalForm.nHLC[1, GlobalForm.iFib2]) > 0, (object)GlobalForm.iFib1, (object)GlobalForm.iFib2));
			num4 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, GlobalForm.iFib1], GlobalForm.nHLC[2, GlobalForm.iFib2]) < 0, (object)GlobalForm.iFib1, (object)GlobalForm.iFib2));
		}
		checked
		{
			PointF pointF = default(PointF);
			PointF pointF2 = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)val.Points)
			{
				if (num2 + GlobalForm.ChartStartIndex == num3)
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num2 + 1));
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
				}
				if (num2 + GlobalForm.ChartStartIndex == num4)
				{
					pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num2 + 1));
					pointF2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
				}
				num2++;
			}
			pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
			pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
			ChartGraphics chartGraphics = e.ChartGraphics;
			pointF.Y -= 6f;
			chartGraphics.Graphics.DrawEllipse(Pens.Blue, (float)((double)pointF.X - (double)num / 2.0), (float)((double)pointF.Y - (double)num / 2.0), (float)num, (float)num);
			pointF2.Y += 4f;
			chartGraphics.Graphics.DrawEllipse(Pens.Blue, (float)((double)pointF2.X - (double)num / 2.0), (float)((double)pointF2.Y - (double)num / 2.0), (float)num, (float)num);
		}
	}

	private void ShowPercentMoves(ChartPaintEventArgs e, int l, ref decimal PeakPrice, ref decimal ValleyPrice, long NumPoints)
	{
		checked
		{
			decimal num = GlobalForm.nHLC[1, l + GlobalForm.ChartStartIndex];
			decimal num2 = GlobalForm.nHLC[2, l + GlobalForm.ChartStartIndex];
			PointF pointF = default(PointF);
			PointF absolutePoint = default(PointF);
			if (GlobalForm.SimGlobals.ShowPeakDrop)
			{
				if (decimal.Compare(num, PeakPrice) >= 0)
				{
					PeakPrice = num;
					HighTrigger = false;
					HighPoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(l + 1));
					HighPoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(num));
					HighPoint = e.ChartGraphics.GetAbsolutePoint(HighPoint);
					HighPoint.X -= (float)((double)GlobalForm.StringSize.Width * 0.4);
					HighPoint.Y -= GlobalForm.StringSize.Height;
				}
				else if ((Convert.ToDouble(num2) <= Convert.ToDouble(PeakPrice) * (1.0 - 0.01 * (double)GlobalForm.SimGlobals.PercentageDrop)) & !HighTrigger)
				{
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(l + 1));
					absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(PeakPrice) * (1.0 - 0.01 * (double)GlobalForm.SimGlobals.PercentageDrop));
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					pointF.X = absolutePoint.X + 2f * GlobalForm.StringSize.Width;
					pointF.Y = absolutePoint.Y;
					e.ChartGraphics.Graphics.DrawLine(Pens.Red, absolutePoint, pointF);
					absolutePoint.X += 2f * GlobalForm.StringSize.Width;
					absolutePoint.Y -= GlobalForm.StringSize.Height / 2f;
					e.ChartGraphics.Graphics.DrawString(Strings.Format((object)((double)GlobalForm.SimGlobals.PercentageDrop / 100.0), "0%") + " Down", BoldFont, Brushes.Red, absolutePoint);
					e.ChartGraphics.Graphics.DrawString("*", BoldFont, Brushes.Red, HighPoint);
					HighTrigger = true;
					if (l + 1 == NumPoints)
					{
						ResetPctDownTrade = true;
					}
				}
				if (HighTrigger)
				{
					PeakPrice = num;
				}
			}
			if (!GlobalForm.SimGlobals.ShowValleyRises)
			{
				return;
			}
			if ((decimal.Compare(ValleyPrice, 0m) == 0) | ((decimal.Compare(num2, ValleyPrice) <= 0) & (decimal.Compare(num2, 0m) > 0)))
			{
				ValleyPrice = num2;
				LowTrigger = false;
				LowPoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(l + 1));
				LowPoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(num2));
				LowPoint = e.ChartGraphics.GetAbsolutePoint(LowPoint);
				LowPoint.X -= (float)((double)GlobalForm.StringSize.Width * 0.4);
				LowPoint.Y += GlobalForm.StringSize.Height / 2f;
			}
			else if ((Convert.ToDouble(num) >= Convert.ToDouble(ValleyPrice) * (1.0 + 0.01 * (double)GlobalForm.SimGlobals.PercentageRise)) & !LowTrigger)
			{
				absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(l + 1));
				absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(ValleyPrice) * (1.0 + 0.01 * (double)GlobalForm.SimGlobals.PercentageRise));
				absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				pointF.X = absolutePoint.X + 2f * GlobalForm.StringSize.Width;
				pointF.Y = absolutePoint.Y;
				e.ChartGraphics.Graphics.DrawLine(Pens.Red, absolutePoint, pointF);
				absolutePoint.X += 2f * GlobalForm.StringSize.Width;
				absolutePoint.Y -= GlobalForm.StringSize.Height / 2f;
				e.ChartGraphics.Graphics.DrawString(Strings.Format((object)((double)GlobalForm.SimGlobals.PercentageRise / 100.0), "0%") + " Up", BoldFont, Brushes.Red, absolutePoint);
				e.ChartGraphics.Graphics.DrawString("*", BoldFont, Brushes.Red, LowPoint);
				LowTrigger = true;
				if (l + 1 == NumPoints)
				{
					ResetPctUpTrade = true;
				}
			}
			if (LowTrigger)
			{
				ValleyPrice = num2;
			}
		}
	}

	private void SimulatorHelpButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.HelpSimulatorForm).ShowDialog();
	}

	private void SpeedSB_Scroll(object sender, ScrollEventArgs e)
	{
		Timer1.Interval = ((ScrollBar)SpeedSB).Value;
		GlobalForm.SimGlobals.Speed = ((ScrollBar)SpeedSB).Value;
	}

	private void StartButton_Click(object sender, EventArgs e)
	{
		//IL_005b: Unknown result type (might be due to invalid IL or missing references)
		//IL_05c4: Unknown result type (might be due to invalid IL or missing references)
		if (GlobalForm.QuoteInfo)
		{
			GlobalForm.QuoteInfo = false;
			try
			{
				if (GlobalForm.Annot != null)
				{
					((Collection<Annotation>)(object)Chart1.Annotations).Remove((Annotation)(object)GlobalForm.Annot);
					((ChartElement)GlobalForm.Annot).Dispose();
					GlobalForm.Annot = null;
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				MessageBox.Show("ReleaseQuoteInfo(): " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				ProjectData.ClearProjectError();
			}
		}
		Trade.InProgress = false;
		Trade.TradeReady = true;
		Trade.UpBreakoutDirection = 0;
		Trade.BuyDate = DateTime.MinValue;
		Trade.iBuy = -1;
		Trade.iBkout = -1;
		Trade.SellPrice = default(decimal);
		Trade.SellDate = DateTime.MinValue;
		Trade.iSell = -1;
		Trade.Fees = default(decimal);
		Trade.Commissions = default(decimal);
		Trade.BuyStatus = 0;
		Trade.SellStatus = 0;
		Trade.UltHighDate = DateTime.MinValue;
		Trade.UltLowDate = DateTime.MinValue;
		Trade.iUltHigh = -1;
		Trade.iUltLow = -1;
		StopPressed = false;
		((Control)StartButton).Enabled = false;
		((Control)ResumeButton).Enabled = false;
		((Control)BuyButton).Enabled = true;
		((Control)SellButton).Enabled = true;
		((Control)SetTargetsButton).Enabled = false;
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Clear();
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Clear();
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points).Clear();
		DataPointsCount = 0;
		if (PatternIndex == -1 && FindDGV.RowCount > 0)
		{
			DGVRow(0);
		}
		checked
		{
			if ((PatternIndex != -1) & (GlobalForm.PatternCount != 0))
			{
				GlobalForm.GetCPInformation(PatternIndex);
				Trade.iBkout = GlobalForm.CPInfo.iBkout;
				int num = default(int);
				switch (GlobalForm.PauseSimulator)
				{
				case 1:
					num = GlobalForm.ChartPatterns[PatternIndex].iStartDate;
					break;
				case 2:
					num = GlobalForm.ChartPatterns[PatternIndex].iEndDate;
					break;
				case 3:
					num = ((GlobalForm.CPInfo.iBkout != -1) ? GlobalForm.CPInfo.iBkout : GlobalForm.ChartPatterns[PatternIndex].iEndDate);
					break;
				case 4:
					num = ((GlobalForm.CPInfo.iBkout != -1) ? Conversions.ToInteger(Interaction.IIf(GlobalForm.CPInfo.iBkout < GlobalForm.ChartPatterns[PatternIndex].iEndDate, (object)GlobalForm.CPInfo.iBkout, (object)GlobalForm.ChartPatterns[PatternIndex].iEndDate)) : GlobalForm.ChartPatterns[PatternIndex].iEndDate);
					break;
				}
				ToDatePicker.Value = GlobalForm.nDT[0, num];
				if (num - GlobalForm.SimGlobals.Lookback <= 0)
				{
					FromDatePicker.Value = GlobalForm.nDT[0, 0];
					DataPointsCount = num;
				}
				else
				{
					FromDatePicker.Value = GlobalForm.nDT[0, num - GlobalForm.SimGlobals.Lookback];
					DataPointsCount = GlobalForm.SimGlobals.Lookback;
				}
				GlobalForm.SetupDateIndexes(FromDatePicker.Value, ToDatePicker.Value);
				GlobalForm.ShowStock(Chart1, GlobalForm.ChartStartIndex, GlobalForm.ChartEndIndex, GlobalForm.ChartVolume, GlobalForm.MAUsed);
			}
			else
			{
				FromDatePicker.Value = GlobalForm.nDT[0, 0];
				ToDatePicker.Value = GlobalForm.nDT[0, 0];
				DataPointsCount = 0;
				GlobalForm.SetupDateIndexes(FromDatePicker.Value, ToDatePicker.Value);
				GlobalForm.ShowStock(Chart1, GlobalForm.ChartStartIndex, GlobalForm.ChartEndIndex, GlobalForm.ChartVolume, GlobalForm.MAUsed);
			}
			SetMinMax();
			((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY2.Maximum = Convert.ToDouble(StkMax);
			if (GlobalForm.ChartVolume)
			{
				((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY.Maximum = 4 * VolMax;
				((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY2.Minimum = 0.989 * Convert.ToDouble(decimal.Subtract(StkMin, decimal.Divide(decimal.Subtract(StkMax, StkMin), 4m)));
			}
			else
			{
				((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY2.Minimum = Convert.ToDouble(StkMin) * 0.999;
			}
			StopPressed = true;
			Restart();
			if (DateTime.Compare(ToDatePicker.Value, GlobalForm.nDT[0, GlobalForm.HLCRange]) >= 0)
			{
				((Control)ResumeButton).Enabled = false;
				TradeReport();
			}
			if (!GlobalForm.Quiet)
			{
				MessageBox.Show("Simulator paused (click Setup button to change pause options).\r\n\r\nSetup your trade (shares, target, buy, and sell prices) then click RESUME (NOT start).\r\n\r\nYou can also click Resume and wait for the right time to trade and setup the trade then.\r\n\r\nIf the Resume button remains grayed, then you've reached the end of the file.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
			((Control)SharesNum).Focus();
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

	private void SkipCB_CheckedChanged(object sender, EventArgs e)
	{
		SilentMode = SkipCB.Checked;
		if (SkipCB.Checked)
		{
			((Control)StopSkip).Visible = true;
		}
		else
		{
			((Control)StopSkip).Visible = false;
		}
	}

	private void StopSkip_Click(object sender, EventArgs e)
	{
		bStopSkip = true;
	}

	private void Timer1_Tick(object sender, EventArgs e)
	{
		TimerRunFlag = true;
	}

	private void TradeReport()
	{
		bool flag = false;
		bool flag2 = false;
		string text = "";
		Trade.UpBreakoutDirection = 0;
		string text2 = Strings.Trim(GlobalForm.CPInfo.BkoutDirection);
		switch (text2)
		{
		case "Up":
			Trade.UpBreakoutDirection = 1;
			break;
		case "Down":
			Trade.UpBreakoutDirection = -1;
			break;
		default:
			if (Operators.CompareString(text2, (string)null, false) != 0)
			{
				break;
			}
			goto case "?";
		case "?":
			Trade.UpBreakoutDirection = 2;
			break;
		}
		decimal d = decimal.Multiply(new decimal(Trade.Shares), Trade.SellPrice);
		if (GlobalForm.SimGlobals.SECBool)
		{
			decimal.Divide(decimal.Multiply(d, GlobalForm.SimGlobals.SECFee), 1000000m);
		}
		((Control)SellButton).Enabled = false;
		BuySellDGV.Rows.Add();
		checked
		{
			int num = BuySellDGV.RowCount - 1;
			BuySellDGV.Rows[num].Cells[0].Value = GlobalForm.LimitDecimals(decimal.Subtract(decimal.Subtract(decimal.Subtract(d, Trade.Fees), decimal.Multiply(new decimal(Trade.Shares), Trade.BuyPrice)), Trade.Commissions));
			BuySellDGV.Rows[num].Cells[1].Value = GlobalForm.LimitDecimals(Trade.BuyPrice);
			BuySellDGV.Rows[num].Cells[2].Value = Strings.Format((object)Trade.BuyDate, GlobalForm.UserDate);
			BuySellDGV.Rows[num].Cells[3].Value = GlobalForm.LimitDecimals(Trade.SellPrice);
			BuySellDGV.Rows[num].Cells[4].Value = Strings.Format((object)Trade.SellDate, GlobalForm.UserDate);
			BuySellDGV.Rows[num].Cells[5].Value = Trade.Shares;
			BuySellDGV.Rows[num].Cells[6].Value = GlobalForm.LimitDecimals(decimal.Add(Trade.Commissions, Trade.Fees));
			BuySellDGV.Rows[num].Cells[7].Value = Conversions.ToString(Interaction.IIf(Trade.tShort, (object)"Short", (object)"Long"));
			BuySellDGV.Rows[num].Cells[8].Value = GlobalForm.LimitDecimals(Trade.PriceTarget);
			BuySellDGV.Rows[num].Cells[9].Value = GlobalForm.LimitDecimals(Trade.PriceStop);
			text = Trade.BuyStatus switch
			{
				1 => text + "Entry: Stopped out", 
				2 => text + "Entry: Hit target price", 
				3 => (!Trade.tShort) ? (text + "Entry: Hit buy price") : (text + "Entry: Hit short sale price"), 
				4 => text + "Entry: Hit limit order to buy", 
				5 => text + "Entry: Hit limit order to sell short", 
				6 => text + "Entry: Manual", 
				7 => text + "Entry: Out of data. Sold at close", 
				_ => text + "Entry: Open", 
			} + ". ";
			text = Trade.SellStatus switch
			{
				1 => text + "Exit: Stopped out", 
				2 => text + "Exit: Hit target price", 
				3 => (!Trade.tShort) ? (text + "Exit: Hit buy price") : (text + "Exit: Hit cover price"), 
				5 => text + "Entry: Hit limit order to sell short", 
				6 => text + "Exit: Manual", 
				7 => text + "Exit: Out of data. Sold at close", 
				_ => text + "Exit: Open", 
			};
			BuySellDGV.Rows[num].Cells[10].Value = text;
			BuySellDGV.Rows[num].Cells[11].Value = Filename;
			if (PatternIndex != -1)
			{
				BuySellDGV.Rows[num].Cells[12].Value = PatternName + " from " + Strings.Format((object)GlobalForm.nDT[0, GlobalForm.ChartPatterns[PatternIndex].iStartDate], GlobalForm.UserDate) + " to " + Strings.Format((object)GlobalForm.nDT[0, GlobalForm.ChartPatterns[PatternIndex].iEndDate], GlobalForm.UserDate);
			}
			DateTime t = Trade.BuyDate;
			if (Trade.tShort)
			{
				t = Trade.SellDate;
			}
			int num2 = -1;
			int num3 = -1;
			int num4 = GlobalForm.HLCRange - 1;
			int num5 = default(int);
			int num6 = default(int);
			for (int i = 0; i <= num4; i++)
			{
				if ((PatternIndex != -1) & (GlobalForm.PatternCount > 0))
				{
					if (DateTime.Compare(GlobalForm.nDT[0, i], GlobalForm.nDT[0, GlobalForm.ChartPatterns[PatternIndex].iStartDate]) == 0)
					{
						num2 = i;
						num3 = i;
					}
					else if ((num3 != -1) & (DateTime.Compare(GlobalForm.nDT[0, i], GlobalForm.nDT[0, GlobalForm.ChartPatterns[PatternIndex].iEndDate]) <= 0))
					{
						num2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num2]) < 0, (object)i, (object)num2));
						num3 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num3]) > 0, (object)i, (object)num3));
					}
				}
				if (DateTime.Compare(GlobalForm.nDT[0, i], t) == 0)
				{
					num5 = i + 1;
					num6 = i + 1;
				}
				else if (DateTime.Compare(GlobalForm.nDT[0, i], t) > 0)
				{
					num5 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num5]) > 0, (object)i, (object)num5));
					num6 = Conversions.ToInteger(Interaction.IIf((decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num6]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i], 0m) != 0), (object)i, (object)num6));
					if (!flag & (Convert.ToDouble(GlobalForm.nHLC[3, i]) <= 0.8 * Convert.ToDouble(GlobalForm.nHLC[1, num5])))
					{
						flag = true;
						BuySellDGV.Rows[num].Cells[13].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[1, num5]);
						BuySellDGV.Rows[num].Cells[14].Value = Strings.Format((object)GlobalForm.nDT[0, num5].Date, GlobalForm.UserDate);
						Trade.UltHighDate = GlobalForm.nDT[0, num5];
						Trade.iUltHigh = num5;
					}
					if (!flag2 & (Convert.ToDouble(GlobalForm.nHLC[3, i]) >= 1.2 * Convert.ToDouble(GlobalForm.nHLC[2, num6])))
					{
						flag2 = true;
						BuySellDGV.Rows[num].Cells[15].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[2, num6]);
						BuySellDGV.Rows[num].Cells[16].Value = Strings.Format((object)GlobalForm.nDT[0, num6], GlobalForm.UserDate);
						Trade.UltLowDate = GlobalForm.nDT[0, num6];
						Trade.iUltLow = num6;
					}
					if (num3 != -1)
					{
						if (!flag & (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[2, num2]) < 0))
						{
							flag = true;
							BuySellDGV.Rows[num].Cells[13].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[1, num5]);
							BuySellDGV.Rows[num].Cells[14].Value = Strings.Format((object)GlobalForm.nDT[0, num5].Date, GlobalForm.UserDate);
							Trade.UltHighDate = GlobalForm.nDT[0, num5];
							Trade.iUltHigh = num5;
						}
						if (unchecked(Trade.tShort && !flag2) & (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[1, num3]) > 0))
						{
							flag2 = true;
							BuySellDGV.Rows[num].Cells[15].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[2, num6]);
							if (GlobalForm.IntradayData)
							{
								BuySellDGV.Rows[num].Cells[16].Value = Strings.Format((object)GlobalForm.nDT[0, num6], "yyyy-MM-dd HH:mm");
							}
							else
							{
								BuySellDGV.Rows[num].Cells[16].Value = Strings.Format((object)GlobalForm.nDT[0, num6], GlobalForm.UserDate);
							}
							Trade.UltLowDate = GlobalForm.nDT[0, num6];
							Trade.iUltLow = num6;
						}
					}
				}
				if (unchecked(flag2 && flag))
				{
					break;
				}
			}
			if (!flag)
			{
				BuySellDGV.Rows[num].Cells[13].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[1, num5]);
				BuySellDGV.Rows[num].Cells[14].Value = Strings.Format((object)GlobalForm.nDT[0, num5].Date, GlobalForm.UserDate);
				Trade.UltHighDate = GlobalForm.nDT[0, num5];
				Trade.iUltHigh = num5;
			}
			if (!flag2)
			{
				BuySellDGV.Rows[num].Cells[15].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[2, num6]);
				BuySellDGV.Rows[num].Cells[16].Value = Strings.Format((object)GlobalForm.nDT[0, num6], GlobalForm.UserDate);
				Trade.UltLowDate = GlobalForm.nDT[0, num6];
				Trade.iUltLow = num6;
			}
			AnalyzeTrade(num);
			Trade.InProgress = false;
			Trade.TradeReady = false;
			BuySellDGV.FirstDisplayedScrollingRowIndex = BuySellDGV.Rows.Count - 1;
			((Control)BuySellDGV).PerformLayout();
		}
	}

	private void UpdateChart()
	{
		checked
		{
			if (DataPointsCount + 1 >= GlobalForm.SimGlobals.Lookback)
			{
				DataPointsCount = GlobalForm.SimGlobals.Lookback;
				GlobalForm.ChartStartIndex++;
				GlobalForm.ChartEndIndex++;
			}
			else
			{
				DataPointsCount++;
				GlobalForm.ChartEndIndex++;
			}
			if (GlobalForm.ChartEndIndex > GlobalForm.HLCRange)
			{
				StopPressed = true;
				return;
			}
			FromDatePicker.Value = GlobalForm.nDT[0, GlobalForm.ChartStartIndex];
			ToDatePicker.Value = GlobalForm.nDT[0, GlobalForm.ChartEndIndex];
			((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points.AddXY((object)GlobalForm.nDT[0, GlobalForm.ChartEndIndex], new object[4]
			{
				GlobalForm.nHLC[1, GlobalForm.ChartEndIndex],
				GlobalForm.nHLC[2, GlobalForm.ChartEndIndex],
				GlobalForm.nHLC[0, GlobalForm.ChartEndIndex],
				GlobalForm.nHLC[3, GlobalForm.ChartEndIndex]
			});
			if (DataPointsCount >= GlobalForm.SimGlobals.Lookback)
			{
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).RemoveAt(0);
			}
			if (GlobalForm.ChartVolume)
			{
				((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points.AddXY((object)GlobalForm.nDT[0, GlobalForm.ChartEndIndex], new object[1] { GlobalForm.nHLC[4, GlobalForm.ChartEndIndex] });
				if (DataPointsCount >= GlobalForm.SimGlobals.Lookback)
				{
					((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).RemoveAt(0);
				}
			}
			if (GlobalForm.MAUsed)
			{
				if ((GlobalForm.MAType == 1) | ((GlobalForm.MAType == 2) & EMASeed))
				{
					ref decimal movAvg = ref MovAvg;
					movAvg = decimal.Add(movAvg, GlobalForm.nHLC[3, GlobalForm.ChartEndIndex]);
					if (GlobalForm.ChartEndIndex > GlobalForm.MALength - 1)
					{
						ref decimal movAvg2 = ref MovAvg;
						movAvg2 = decimal.Subtract(movAvg2, GlobalForm.nHLC[3, GlobalForm.ChartEndIndex - GlobalForm.MALength]);
					}
				}
				if (GlobalForm.ChartEndIndex >= GlobalForm.MALength - 1)
				{
					if (GlobalForm.MAType == 1)
					{
						((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points.AddXY((object)GlobalForm.nDT[0, GlobalForm.ChartEndIndex], new object[1] { decimal.Divide(MovAvg, new decimal(GlobalForm.MALength)) });
					}
					else if (GlobalForm.MAType == 2)
					{
						if ((GlobalForm.ChartEndIndex == GlobalForm.MALength - 1) | EMASeed)
						{
							EMASeed = false;
							EMAYesterday = decimal.Divide(MovAvg, new decimal(GlobalForm.MALength));
						}
						else if (GlobalForm.ChartEndIndex > GlobalForm.MALength - 1)
						{
							ref decimal eMAYesterday = ref EMAYesterday;
							eMAYesterday = decimal.Add(eMAYesterday, decimal.Multiply(Alpha, decimal.Subtract(GlobalForm.nHLC[3, GlobalForm.ChartEndIndex], EMAYesterday)));
						}
						((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points.AddXY((object)GlobalForm.nDT[0, GlobalForm.ChartEndIndex], new object[1] { EMAYesterday });
					}
					if (DataPointsCount >= GlobalForm.SimGlobals.Lookback)
					{
						((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points).RemoveAt(0);
					}
				}
				else
				{
					((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points.AddXY((object)GlobalForm.nDT[0, GlobalForm.ChartEndIndex], new object[1] { 0 });
					if (DataPointsCount >= GlobalForm.SimGlobals.Lookback)
					{
						((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points).RemoveAt(0);
					}
				}
			}
			if (GlobalForm.PatternCount != 0)
			{
				int num = GlobalForm.PatternCount - 1;
				for (int i = 0; i <= num; i++)
				{
					int ReturnStart = GlobalForm.ChartPatterns[i].iStartDate;
					int ReturnEnd = GlobalForm.ChartPatterns[i].iEndDate;
					GlobalForm.GetStartEndDates(i, ref ReturnStart, ref ReturnEnd);
					if ((ReturnStart <= GlobalForm.ChartEndIndex) & (ReturnEnd >= GlobalForm.ChartEndIndex))
					{
						BuildMessage(GlobalForm.GetPatternPhrase(i), GlobalForm.nDT[0, ReturnStart], GlobalForm.nDT[0, ReturnEnd], Flag: false);
					}
				}
			}
			if (GlobalForm.CandleCount != 0)
			{
				int num2 = GlobalForm.CandleCount - 1;
				for (int j = 0; j <= num2; j++)
				{
					if ((GlobalForm.CandlePatterns[j].iStartDate <= GlobalForm.ChartEndIndex) & (GlobalForm.CandlePatterns[j].iEndDate >= GlobalForm.ChartEndIndex))
					{
						string phrase = GlobalForm.CandlePatterns[j].Phrase;
						phrase = Conversions.ToString(Interaction.IIf(Operators.CompareString(Strings.Right(phrase, 1), ".", false) == 0, (object)Strings.Left(phrase, Strings.Len(phrase) - 1), (object)phrase));
						BuildMessage(phrase, GlobalForm.nDT[0, GlobalForm.CandlePatterns[j].iStartDate], GlobalForm.nDT[0, GlobalForm.CandlePatterns[j].iEndDate], Flag: false);
					}
				}
			}
			SetMinMax();
			((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY2.Maximum = Convert.ToDouble(StkMax);
			if (GlobalForm.ChartVolume)
			{
				((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY.Maximum = 4 * VolMax;
				((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY2.Minimum = 0.989 * Convert.ToDouble(decimal.Subtract(StkMin, decimal.Divide(decimal.Subtract(StkMax, StkMin), 4m)));
			}
			else
			{
				((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY2.Minimum = Convert.ToDouble(StkMin) * 0.999;
			}
			Chart1.Invalidate();
		}
	}

	private void WriteConfigFile()
	{
		//IL_00b0: Unknown result type (might be due to invalid IL or missing references)
		BinaryFormatter binaryFormatter = new BinaryFormatter();
		GlobalForm.SimGlobals.Annotations = GlobalForm.Annotations;
		GlobalForm.SimGlobals.FindCandles = GlobalForm.ShowCandles;
		GlobalForm.SimGlobals.Strict = GlobalForm.StrictPatterns;
		GlobalForm.SimGlobals.Volume = GlobalForm.ChartVolume;
		GlobalForm.SimGlobals.MovingAvg = GlobalForm.MAUsed;
		GlobalForm.SimGlobals.MAType = GlobalForm.MAType;
		GlobalForm.SimGlobals.MALength = GlobalForm.MALength;
		GlobalForm.SimGlobals.TimeScale = GlobalForm.ChartPeriodShown;
		try
		{
			Stream stream = File.OpenWrite(ConfigPath);
			binaryFormatter.Serialize(stream, GlobalForm.SimGlobals);
			stream.Close();
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			MessageBox.Show(ex2.Message);
			ProjectData.ClearProjectError();
		}
	}
}
