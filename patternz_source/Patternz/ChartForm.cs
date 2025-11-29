using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
internal class ChartForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("Chart1")]
	private Chart _Chart1;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("GraphButton")]
	private Button _GraphButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PreviousButton")]
	private Button _PreviousButton;

	[CompilerGenerated]
	[AccessedThroughProperty("NextButton")]
	private Button _NextButton;

	[CompilerGenerated]
	[AccessedThroughProperty("VolumeCheckBox")]
	private CheckBox _VolumeCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("ShowPatternsCB")]
	private CheckBox _ShowPatternsCB;

	[CompilerGenerated]
	[AccessedThroughProperty("PatternsButton")]
	private Button _PatternsButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DataGridView1")]
	private DataGridView _DataGridView1;

	[CompilerGenerated]
	[AccessedThroughProperty("StrictCheckBox")]
	private CheckBox _StrictCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("CandlesCheckBox")]
	private CheckBox _CandlesCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("CandlesButton")]
	private Button _CandlesButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PortfolioButton")]
	private Button _PortfolioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("SkipCheckBox")]
	private CheckBox _SkipCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("DailyRadioButton")]
	private RadioButton _DailyRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("WeeklyRadioButton")]
	private RadioButton _WeeklyRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("MonthlyRadioButton")]
	private RadioButton _MonthlyRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("SetupButton")]
	private Button _SetupButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ToDatePicker")]
	private DateTimePicker _ToDatePicker;

	[CompilerGenerated]
	[AccessedThroughProperty("FibButton")]
	private Button _FibButton;

	[CompilerGenerated]
	[AccessedThroughProperty("TargetCheckBox")]
	private CheckBox _TargetCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("FromDatePicker")]
	private DateTimePicker _FromDatePicker;

	[CompilerGenerated]
	[AccessedThroughProperty("PercentButton")]
	private Button _PercentButton;

	[CompilerGenerated]
	[AccessedThroughProperty("SRButton")]
	private Button _SRButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PlusButton")]
	private Button _PlusButton;

	[CompilerGenerated]
	[AccessedThroughProperty("OriginalButton")]
	private Button _OriginalButton;

	[CompilerGenerated]
	[AccessedThroughProperty("MinusButton")]
	private Button _MinusButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DetailButton")]
	private Button _DetailButton;

	private const int dSTATUS = 0;

	private const int dDESCRIPTION = 1;

	private const int dSTART = 2;

	private const int dEND = 3;

	private const int dBKOUT = 4;

	private const int dTARGET = 5;

	private const int dVOLATILITY = 6;

	private const int dTRADESTATUS = 7;

	private const int dULTIMATEHL = 8;

	private const int dUPTARGET = 9;

	private const int dDOWNTARGET = 10;

	private const int INDEXROW = 11;

	private Point StartPoint;

	private Point EndPoint;

	private string Filename;

	private bool LockFlag;

	private bool Crosshair;

	private Point CrosshairPoint;

	private Pen CrosshairPen;

	private int iGridLastRow;

	private bool ShowFibs;

	private bool PercentCircles;

	private CalloutAnnotation CurrentAnnotation;

	private readonly bool StopPressed;

	private bool ActiveOnce;

	private bool SR;

	private DateTime[] OriginalDates;

	private string ConfigPath;

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

	[field: AccessedThroughProperty("SymbolTextBox")]
	internal virtual TextBox SymbolTextBox
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

	internal virtual CheckBox VolumeCheckBox
	{
		[CompilerGenerated]
		get
		{
			return _VolumeCheckBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = VolumeCheckBox_CheckedChanged;
			CheckBox val = _VolumeCheckBox;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_VolumeCheckBox = value;
			val = _VolumeCheckBox;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox ShowPatternsCB
	{
		[CompilerGenerated]
		get
		{
			return _ShowPatternsCB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShowPatternsCB_CheckedChanged;
			CheckBox val = _ShowPatternsCB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_ShowPatternsCB = value;
			val = _ShowPatternsCB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
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

	internal virtual DataGridView DataGridView1
	{
		[CompilerGenerated]
		get
		{
			return _DataGridView1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0007: Unknown result type (might be due to invalid IL or missing references)
			//IL_000d: Expected O, but got Unknown
			DataGridViewCellEventHandler val = new DataGridViewCellEventHandler(DataGridView1_RowEnter);
			DataGridView val2 = _DataGridView1;
			if (val2 != null)
			{
				val2.RowEnter -= val;
			}
			_DataGridView1 = value;
			val2 = _DataGridView1;
			if (val2 != null)
			{
				val2.RowEnter += val;
			}
		}
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

	[field: AccessedThroughProperty("LoadingBar")]
	internal virtual ProgressBar LoadingBar
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

	internal virtual CheckBox CandlesCheckBox
	{
		[CompilerGenerated]
		get
		{
			return _CandlesCheckBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CandlesCheckBox_CheckedChanged;
			CheckBox val = _CandlesCheckBox;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_CandlesCheckBox = value;
			val = _CandlesCheckBox;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
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

	[field: AccessedThroughProperty("ErrorLabel")]
	internal virtual Label ErrorLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button PortfolioButton
	{
		[CompilerGenerated]
		get
		{
			return _PortfolioButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PortfolioButton_Click;
			Button val = _PortfolioButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_PortfolioButton = value;
			val = _PortfolioButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual CheckBox SkipCheckBox
	{
		[CompilerGenerated]
		get
		{
			return _SkipCheckBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SkipCheckBox_CheckedChanged;
			CheckBox val = _SkipCheckBox;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_SkipCheckBox = value;
			val = _SkipCheckBox;
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

	internal virtual Button FibButton
	{
		[CompilerGenerated]
		get
		{
			return _FibButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = FibButton_Click;
			Button val = _FibButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_FibButton = value;
			val = _FibButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual CheckBox TargetCheckBox
	{
		[CompilerGenerated]
		get
		{
			return _TargetCheckBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = TargetCheckBox_CheckedChanged;
			CheckBox val = _TargetCheckBox;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_TargetCheckBox = value;
			val = _TargetCheckBox;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
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
			EventHandler eventHandler = FromDatePicker_Validated;
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

	internal virtual Button SRButton
	{
		[CompilerGenerated]
		get
		{
			return _SRButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SRButton_Click;
			Button val = _SRButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_SRButton = value;
			val = _SRButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button PlusButton
	{
		[CompilerGenerated]
		get
		{
			return _PlusButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PlusButton_Click_1;
			Button val = _PlusButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_PlusButton = value;
			val = _PlusButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button OriginalButton
	{
		[CompilerGenerated]
		get
		{
			return _OriginalButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = OriginalButton_Click_1;
			Button val = _OriginalButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_OriginalButton = value;
			val = _OriginalButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button MinusButton
	{
		[CompilerGenerated]
		get
		{
			return _MinusButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = MinusButton_Click_1;
			Button val = _MinusButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_MinusButton = value;
			val = _MinusButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button DetailButton
	{
		[CompilerGenerated]
		get
		{
			return _DetailButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DetailButton_Click;
			Button val = _DetailButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_DetailButton = value;
			val = _DetailButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	public ChartForm()
	{
		//IL_0044: Unknown result type (might be due to invalid IL or missing references)
		//IL_004e: Expected O, but got Unknown
		//IL_0079: Unknown result type (might be due to invalid IL or missing references)
		//IL_0083: Expected O, but got Unknown
		((Form)this).Closing += ChartForm_Closing;
		((Form)this).Load += ChartForm_Load;
		((Form)this).Activated += ChartForm_Activated;
		((Control)this).KeyDown += new KeyEventHandler(ChartForm_KeyDown);
		LockFlag = false;
		Crosshair = false;
		CrosshairPen = null;
		iGridLastRow = -1;
		ShowFibs = false;
		PercentCircles = false;
		CurrentAnnotation = new CalloutAnnotation();
		StopPressed = false;
		ActiveOnce = false;
		SR = false;
		OriginalDates = new DateTime[2];
		ConfigPath = null;
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
		//IL_0339: Unknown result type (might be due to invalid IL or missing references)
		//IL_077f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0789: Expected O, but got Unknown
		//IL_0810: Unknown result type (might be due to invalid IL or missing references)
		//IL_081a: Expected O, but got Unknown
		//IL_1337: Unknown result type (might be due to invalid IL or missing references)
		//IL_1341: Expected O, but got Unknown
		//IL_1447: Unknown result type (might be due to invalid IL or missing references)
		//IL_1451: Expected O, but got Unknown
		//IL_14d8: Unknown result type (might be due to invalid IL or missing references)
		//IL_14e2: Expected O, but got Unknown
		//IL_1569: Unknown result type (might be due to invalid IL or missing references)
		//IL_1573: Expected O, but got Unknown
		//IL_1606: Unknown result type (might be due to invalid IL or missing references)
		//IL_1610: Expected O, but got Unknown
		//IL_16a7: Unknown result type (might be due to invalid IL or missing references)
		//IL_16b1: Expected O, but got Unknown
		//IL_1744: Unknown result type (might be due to invalid IL or missing references)
		//IL_174e: Expected O, but got Unknown
		//IL_1a91: Unknown result type (might be due to invalid IL or missing references)
		//IL_1a9b: Expected O, but got Unknown
		ChartArea val = new ChartArea();
		Series val2 = new Series();
		Series val3 = new Series();
		Series val4 = new Series();
		Chart1 = new Chart();
		DoneButton = new Button();
		GraphButton = new Button();
		SymbolTextBox = new TextBox();
		Label1 = new Label();
		Label2 = new Label();
		Label3 = new Label();
		PreviousButton = new Button();
		NextButton = new Button();
		VolumeCheckBox = new CheckBox();
		ShowPatternsCB = new CheckBox();
		PatternsButton = new Button();
		DataGridView1 = new DataGridView();
		StrictCheckBox = new CheckBox();
		LoadingBar = new ProgressBar();
		Label4 = new Label();
		CandlesCheckBox = new CheckBox();
		CandlesButton = new Button();
		Label5 = new Label();
		FindingBar = new ProgressBar();
		ErrorLabel = new Label();
		PortfolioButton = new Button();
		SkipCheckBox = new CheckBox();
		DailyRadioButton = new RadioButton();
		WeeklyRadioButton = new RadioButton();
		MonthlyRadioButton = new RadioButton();
		SetupButton = new Button();
		ToDatePicker = new DateTimePicker();
		FromDatePicker = new DateTimePicker();
		FibButton = new Button();
		TargetCheckBox = new CheckBox();
		PercentButton = new Button();
		SRButton = new Button();
		OriginalButton = new Button();
		MinusButton = new Button();
		PlusButton = new Button();
		DetailButton = new Button();
		((ISupportInitialize)Chart1).BeginInit();
		((ISupportInitialize)DataGridView1).BeginInit();
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
		((Control)Chart1).Location = new Point(0, 0);
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
		Chart1.Size = new Size(1008, 367);
		((Control)Chart1).TabIndex = 0;
		((Control)Chart1).Text = "Chart1";
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.AutoSizeMode = (AutoSizeMode)0;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(960, 436);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(43, 23);
		((Control)DoneButton).TabIndex = 36;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)GraphButton).Anchor = (AnchorStyles)10;
		((Control)GraphButton).Location = new Point(957, 408);
		((Control)GraphButton).Name = "GraphButton";
		((Control)GraphButton).Size = new Size(49, 23);
		((Control)GraphButton).TabIndex = 30;
		((ButtonBase)GraphButton).Text = "&Graph";
		((ButtonBase)GraphButton).UseVisualStyleBackColor = true;
		((Control)SymbolTextBox).Anchor = (AnchorStyles)10;
		((Control)SymbolTextBox).Location = new Point(721, 390);
		((Control)SymbolTextBox).Name = "SymbolTextBox";
		((Control)SymbolTextBox).Size = new Size(41, 20);
		((Control)SymbolTextBox).TabIndex = 19;
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(675, 393);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(44, 13);
		((Control)Label1).TabIndex = 18;
		Label1.Text = "S&ymbol:";
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(611, 418);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(33, 13);
		((Control)Label2).TabIndex = 13;
		Label2.Text = "&From:";
		((Control)Label3).Anchor = (AnchorStyles)10;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(621, 441);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(23, 13);
		((Control)Label3).TabIndex = 15;
		Label3.Text = "&To:";
		((Control)PreviousButton).Anchor = (AnchorStyles)10;
		((Control)PreviousButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)PreviousButton).Location = new Point(767, 436);
		((Control)PreviousButton).Name = "PreviousButton";
		((Control)PreviousButton).Size = new Size(27, 23);
		((Control)PreviousButton).TabIndex = 31;
		((ButtonBase)PreviousButton).Text = "<";
		((ButtonBase)PreviousButton).UseVisualStyleBackColor = true;
		((Control)NextButton).Anchor = (AnchorStyles)10;
		((Control)NextButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)NextButton).Location = new Point(794, 436);
		((Control)NextButton).Name = "NextButton";
		((Control)NextButton).Size = new Size(29, 23);
		((Control)NextButton).TabIndex = 32;
		((ButtonBase)NextButton).Text = ">";
		((ButtonBase)NextButton).UseVisualStyleBackColor = true;
		((Control)VolumeCheckBox).Anchor = (AnchorStyles)10;
		((ButtonBase)VolumeCheckBox).AutoSize = true;
		((Control)VolumeCheckBox).Location = new Point(551, 423);
		((Control)VolumeCheckBox).Name = "VolumeCheckBox";
		((Control)VolumeCheckBox).Size = new Size(61, 17);
		((Control)VolumeCheckBox).TabIndex = 9;
		((ButtonBase)VolumeCheckBox).Text = "&Volume";
		((ButtonBase)VolumeCheckBox).UseVisualStyleBackColor = true;
		((Control)ShowPatternsCB).Anchor = (AnchorStyles)10;
		((ButtonBase)ShowPatternsCB).AutoSize = true;
		((Control)ShowPatternsCB).Location = new Point(551, 386);
		((Control)ShowPatternsCB).Name = "ShowPatternsCB";
		((Control)ShowPatternsCB).Size = new Size(94, 17);
		((Control)ShowPatternsCB).TabIndex = 7;
		((ButtonBase)ShowPatternsCB).Text = "&Show patterns";
		((ButtonBase)ShowPatternsCB).UseVisualStyleBackColor = true;
		((Control)PatternsButton).Anchor = (AnchorStyles)10;
		PatternsButton.AutoSizeMode = (AutoSizeMode)0;
		((Control)PatternsButton).Location = new Point(904, 436);
		((Control)PatternsButton).Name = "PatternsButton";
		((Control)PatternsButton).Size = new Size(56, 23);
		((Control)PatternsButton).TabIndex = 35;
		((ButtonBase)PatternsButton).Text = "&Patterns";
		((ButtonBase)PatternsButton).UseVisualStyleBackColor = true;
		DataGridView1.AllowUserToAddRows = false;
		DataGridView1.AllowUserToDeleteRows = false;
		((Control)DataGridView1).Anchor = (AnchorStyles)14;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)10;
		((Control)DataGridView1).CausesValidation = false;
		DataGridView1.ColumnHeadersHeightSizeMode = (DataGridViewColumnHeadersHeightSizeMode)2;
		DataGridView1.EditMode = (DataGridViewEditMode)4;
		DataGridView1.EnableHeadersVisualStyles = false;
		((Control)DataGridView1).Location = new Point(0, 370);
		DataGridView1.MultiSelect = false;
		((Control)DataGridView1).Name = "DataGridView1";
		DataGridView1.ReadOnly = true;
		DataGridView1.SelectionMode = (DataGridViewSelectionMode)1;
		DataGridView1.ShowCellErrors = false;
		DataGridView1.ShowCellToolTips = false;
		DataGridView1.ShowEditingIcon = false;
		DataGridView1.ShowRowErrors = false;
		((Control)DataGridView1).Size = new Size(477, 94);
		((Control)DataGridView1).TabIndex = 1;
		((Control)StrictCheckBox).Anchor = (AnchorStyles)10;
		((ButtonBase)StrictCheckBox).AutoSize = true;
		((Control)StrictCheckBox).Location = new Point(551, 406);
		((Control)StrictCheckBox).Name = "StrictCheckBox";
		((Control)StrictCheckBox).Size = new Size(50, 17);
		((Control)StrictCheckBox).TabIndex = 8;
		((ButtonBase)StrictCheckBox).Text = "St&rict";
		((ButtonBase)StrictCheckBox).UseVisualStyleBackColor = true;
		((Control)LoadingBar).Anchor = (AnchorStyles)10;
		((Control)LoadingBar).ForeColor = Color.Green;
		((Control)LoadingBar).Location = new Point(946, 385);
		((Control)LoadingBar).Name = "LoadingBar";
		((Control)LoadingBar).Size = new Size(60, 13);
		((Control)LoadingBar).TabIndex = 26;
		((Control)Label4).Anchor = (AnchorStyles)10;
		Label4.AutoSize = true;
		((Control)Label4).Location = new Point(903, 385);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(48, 13);
		((Control)Label4).TabIndex = 25;
		Label4.Text = "Loading:";
		((Control)CandlesCheckBox).Anchor = (AnchorStyles)10;
		((ButtonBase)CandlesCheckBox).AutoSize = true;
		((Control)CandlesCheckBox).Location = new Point(551, 367);
		((Control)CandlesCheckBox).Name = "CandlesCheckBox";
		((Control)CandlesCheckBox).Size = new Size(93, 17);
		((Control)CandlesCheckBox).TabIndex = 6;
		((ButtonBase)CandlesCheckBox).Text = "Show cand&les";
		((ButtonBase)CandlesCheckBox).UseVisualStyleBackColor = true;
		((Control)CandlesButton).Anchor = (AnchorStyles)10;
		((Control)CandlesButton).Location = new Point(892, 408);
		((Control)CandlesButton).Name = "CandlesButton";
		((Control)CandlesButton).Size = new Size(59, 23);
		((Control)CandlesButton).TabIndex = 29;
		((ButtonBase)CandlesButton).Text = "&Candles";
		((ButtonBase)CandlesButton).UseVisualStyleBackColor = true;
		((Control)Label5).Anchor = (AnchorStyles)10;
		Label5.AutoSize = true;
		((Control)Label5).Location = new Point(788, 385);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(44, 13);
		((Control)Label5).TabIndex = 23;
		Label5.Text = "Finding:";
		((Control)FindingBar).Anchor = (AnchorStyles)10;
		((Control)FindingBar).ForeColor = Color.Green;
		((Control)FindingBar).Location = new Point(838, 386);
		((Control)FindingBar).Name = "FindingBar";
		((Control)FindingBar).Size = new Size(59, 13);
		((Control)FindingBar).TabIndex = 24;
		((Control)ErrorLabel).Anchor = (AnchorStyles)10;
		((Control)ErrorLabel).CausesValidation = false;
		((Control)ErrorLabel).ForeColor = Color.Red;
		((Control)ErrorLabel).Location = new Point(808, 367);
		((Control)ErrorLabel).Name = "ErrorLabel";
		((Control)ErrorLabel).Size = new Size(188, 15);
		((Control)ErrorLabel).TabIndex = 22;
		((Control)PortfolioButton).Anchor = (AnchorStyles)10;
		((Control)PortfolioButton).Location = new Point(825, 408);
		((Control)PortfolioButton).Name = "PortfolioButton";
		((Control)PortfolioButton).Size = new Size(60, 23);
		((Control)PortfolioButton).TabIndex = 28;
		((ButtonBase)PortfolioButton).Text = "P&ortfolio";
		((ButtonBase)PortfolioButton).UseVisualStyleBackColor = true;
		((Control)SkipCheckBox).Anchor = (AnchorStyles)10;
		((ButtonBase)SkipCheckBox).AutoSize = true;
		((Control)SkipCheckBox).Location = new Point(551, 442);
		((Control)SkipCheckBox).Name = "SkipCheckBox";
		((Control)SkipCheckBox).Size = new Size(47, 17);
		((Control)SkipCheckBox).TabIndex = 10;
		((ButtonBase)SkipCheckBox).Text = "S&kip";
		((ButtonBase)SkipCheckBox).UseVisualStyleBackColor = true;
		((Control)DailyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)DailyRadioButton).AutoSize = true;
		DailyRadioButton.Checked = true;
		((Control)DailyRadioButton).Location = new Point(483, 386);
		((Control)DailyRadioButton).Name = "DailyRadioButton";
		((Control)DailyRadioButton).Size = new Size(48, 17);
		((Control)DailyRadioButton).TabIndex = 3;
		DailyRadioButton.TabStop = true;
		((Control)DailyRadioButton).Tag = "Daily";
		((ButtonBase)DailyRadioButton).Text = "Dail&y";
		((ButtonBase)DailyRadioButton).UseVisualStyleBackColor = true;
		((Control)WeeklyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)WeeklyRadioButton).AutoSize = true;
		((Control)WeeklyRadioButton).Location = new Point(483, 409);
		((Control)WeeklyRadioButton).Name = "WeeklyRadioButton";
		((Control)WeeklyRadioButton).Size = new Size(61, 17);
		((Control)WeeklyRadioButton).TabIndex = 4;
		((Control)WeeklyRadioButton).Tag = "Weekly";
		((ButtonBase)WeeklyRadioButton).Text = "&Weekly";
		((ButtonBase)WeeklyRadioButton).UseVisualStyleBackColor = true;
		((Control)MonthlyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)MonthlyRadioButton).AutoSize = true;
		((Control)MonthlyRadioButton).Location = new Point(483, 432);
		((Control)MonthlyRadioButton).Name = "MonthlyRadioButton";
		((Control)MonthlyRadioButton).Size = new Size(62, 17);
		((Control)MonthlyRadioButton).TabIndex = 5;
		((Control)MonthlyRadioButton).Tag = "Monthly";
		((ButtonBase)MonthlyRadioButton).Text = "&Monthly";
		((ButtonBase)MonthlyRadioButton).UseVisualStyleBackColor = true;
		((Control)SetupButton).Anchor = (AnchorStyles)10;
		((Control)SetupButton).Location = new Point(767, 408);
		((Control)SetupButton).Name = "SetupButton";
		((Control)SetupButton).Size = new Size(52, 23);
		((Control)SetupButton).TabIndex = 27;
		((ButtonBase)SetupButton).Text = "S&etup";
		((ButtonBase)SetupButton).UseVisualStyleBackColor = true;
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(642, 439);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(120, 20);
		((Control)ToDatePicker).TabIndex = 16;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(642, 413);
		((Control)FromDatePicker).Name = "FromDatePicker";
		FromDatePicker.ShowUpDown = true;
		((Control)FromDatePicker).Size = new Size(120, 20);
		((Control)FromDatePicker).TabIndex = 14;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FibButton).Anchor = (AnchorStyles)10;
		FibButton.AutoSizeMode = (AutoSizeMode)0;
		((Control)FibButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)FibButton).Location = new Point(873, 436);
		((Control)FibButton).Name = "FibButton";
		((Control)FibButton).Size = new Size(31, 23);
		((Control)FibButton).TabIndex = 34;
		((ButtonBase)FibButton).Text = "&Fib";
		((ButtonBase)FibButton).UseVisualStyleBackColor = true;
		((Control)TargetCheckBox).Anchor = (AnchorStyles)10;
		((ButtonBase)TargetCheckBox).AutoSize = true;
		((Control)TargetCheckBox).Location = new Point(483, 367);
		((Control)TargetCheckBox).Name = "TargetCheckBox";
		((Control)TargetCheckBox).Size = new Size(62, 17);
		((Control)TargetCheckBox).TabIndex = 2;
		((ButtonBase)TargetCheckBox).Text = "&Targets";
		((ButtonBase)TargetCheckBox).UseVisualStyleBackColor = true;
		((Control)PercentButton).Anchor = (AnchorStyles)10;
		((Control)PercentButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)PercentButton).Location = new Point(642, 390);
		((Control)PercentButton).Name = "PercentButton";
		((Control)PercentButton).Size = new Size(32, 23);
		((Control)PercentButton).TabIndex = 12;
		((ButtonBase)PercentButton).Text = "%";
		((ButtonBase)PercentButton).UseVisualStyleBackColor = true;
		((Control)SRButton).Anchor = (AnchorStyles)10;
		((Control)SRButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)SRButton).Location = new Point(642, 367);
		((Control)SRButton).Name = "SRButton";
		((Control)SRButton).Size = new Size(32, 23);
		((Control)SRButton).TabIndex = 11;
		((ButtonBase)SRButton).Text = "SR";
		((ButtonBase)SRButton).UseVisualStyleBackColor = true;
		((Control)OriginalButton).Anchor = (AnchorStyles)10;
		((Control)OriginalButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)OriginalButton).Location = new Point(712, 367);
		((Control)OriginalButton).Name = "OriginalButton";
		((Control)OriginalButton).Size = new Size(32, 23);
		((Control)OriginalButton).TabIndex = 20;
		((ButtonBase)OriginalButton).Text = "0";
		((ButtonBase)OriginalButton).UseVisualStyleBackColor = true;
		((Control)MinusButton).Anchor = (AnchorStyles)10;
		((ButtonBase)MinusButton).AutoSize = true;
		((Control)MinusButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)MinusButton).Location = new Point(744, 367);
		((Control)MinusButton).Name = "MinusButton";
		((Control)MinusButton).Size = new Size(32, 23);
		((Control)MinusButton).TabIndex = 21;
		((Control)MinusButton).Tag = "";
		((ButtonBase)MinusButton).Text = "-";
		((ButtonBase)MinusButton).UseVisualStyleBackColor = true;
		((Control)PlusButton).Anchor = (AnchorStyles)10;
		((Control)PlusButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)PlusButton).Location = new Point(680, 367);
		((Control)PlusButton).Name = "PlusButton";
		((Control)PlusButton).Size = new Size(32, 23);
		((Control)PlusButton).TabIndex = 17;
		((ButtonBase)PlusButton).Text = "+";
		((ButtonBase)PlusButton).UseVisualStyleBackColor = true;
		((Control)DetailButton).Anchor = (AnchorStyles)10;
		DetailButton.AutoSizeMode = (AutoSizeMode)0;
		((Control)DetailButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)DetailButton).Location = new Point(829, 436);
		((Control)DetailButton).Name = "DetailButton";
		((Control)DetailButton).Size = new Size(44, 23);
		((Control)DetailButton).TabIndex = 33;
		((ButtonBase)DetailButton).Text = "&Detail";
		((ButtonBase)DetailButton).UseVisualStyleBackColor = true;
		((Form)this).AcceptButton = (IButtonControl)(object)NextButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(1008, 460);
		((Control)this).Controls.Add((Control)(object)DetailButton);
		((Control)this).Controls.Add((Control)(object)MinusButton);
		((Control)this).Controls.Add((Control)(object)OriginalButton);
		((Control)this).Controls.Add((Control)(object)PlusButton);
		((Control)this).Controls.Add((Control)(object)SRButton);
		((Control)this).Controls.Add((Control)(object)PercentButton);
		((Control)this).Controls.Add((Control)(object)TargetCheckBox);
		((Control)this).Controls.Add((Control)(object)FibButton);
		((Control)this).Controls.Add((Control)(object)ToDatePicker);
		((Control)this).Controls.Add((Control)(object)FromDatePicker);
		((Control)this).Controls.Add((Control)(object)SetupButton);
		((Control)this).Controls.Add((Control)(object)MonthlyRadioButton);
		((Control)this).Controls.Add((Control)(object)WeeklyRadioButton);
		((Control)this).Controls.Add((Control)(object)DailyRadioButton);
		((Control)this).Controls.Add((Control)(object)SkipCheckBox);
		((Control)this).Controls.Add((Control)(object)PortfolioButton);
		((Control)this).Controls.Add((Control)(object)ErrorLabel);
		((Control)this).Controls.Add((Control)(object)Label5);
		((Control)this).Controls.Add((Control)(object)FindingBar);
		((Control)this).Controls.Add((Control)(object)CandlesButton);
		((Control)this).Controls.Add((Control)(object)CandlesCheckBox);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)LoadingBar);
		((Control)this).Controls.Add((Control)(object)StrictCheckBox);
		((Control)this).Controls.Add((Control)(object)DataGridView1);
		((Control)this).Controls.Add((Control)(object)PatternsButton);
		((Control)this).Controls.Add((Control)(object)ShowPatternsCB);
		((Control)this).Controls.Add((Control)(object)VolumeCheckBox);
		((Control)this).Controls.Add((Control)(object)NextButton);
		((Control)this).Controls.Add((Control)(object)PreviousButton);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)SymbolTextBox);
		((Control)this).Controls.Add((Control)(object)GraphButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)Chart1);
		((Control)this).DataBindings.Add(new Binding("Location", (object)MySettings.Default, "ChartFormLocation", true, (DataSourceUpdateMode)1));
		((Form)this).KeyPreview = true;
		((Form)this).Location = MySettings.Default.ChartFormLocation;
		((Control)this).Name = "ChartForm";
		((Form)this).StartPosition = (FormStartPosition)0;
		((Form)this).Text = "Chart Form";
		((ISupportInitialize)Chart1).EndInit();
		((ISupportInitialize)DataGridView1).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void ChartForm_Closing(object sender, CancelEventArgs e)
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
		GlobalForm.ChartVolume = VolumeCheckBox.Checked;
		GlobalForm.ShowAllPatterns = ShowPatternsCB.Checked;
		if (!GlobalForm.IntradayData)
		{
			long num = DateAndTime.DateDiff((DateInterval)4, FromDatePicker.Value, ToDatePicker.Value, (FirstDayOfWeek)1, (FirstWeekOfYear)1);
			if (num != GlobalForm.DateLookback)
			{
				GlobalForm.DateLookback = num;
				GlobalForm.DLBChanged = true;
			}
		}
		else
		{
			long num = checked(GlobalForm.ChartEndIndex - GlobalForm.ChartStartIndex);
			if (num != GlobalForm.DateLookback)
			{
				GlobalForm.DateLookback = num;
				GlobalForm.DLBChanged = true;
			}
		}
		GlobalForm.PatternTargets = TargetCheckBox.Checked;
		MySettingsProperty.Settings.ChartFormLocation = ((Form)this).Location;
		MySettingsProperty.Settings.ChartFormSize = ((Form)this).Size;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
		ActiveOnce = false;
	}

	private void ChartForm_Load(object sender, EventArgs e)
	{
		//IL_01df: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e4: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ef: Unknown result type (might be due to invalid IL or missing references)
		//IL_01fa: Unknown result type (might be due to invalid IL or missing references)
		//IL_0205: Unknown result type (might be due to invalid IL or missing references)
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
		//IL_02e9: Unknown result type (might be due to invalid IL or missing references)
		//IL_02fa: Unknown result type (might be due to invalid IL or missing references)
		//IL_030b: Unknown result type (might be due to invalid IL or missing references)
		//IL_031c: Unknown result type (might be due to invalid IL or missing references)
		//IL_032d: Unknown result type (might be due to invalid IL or missing references)
		//IL_033e: Unknown result type (might be due to invalid IL or missing references)
		//IL_034f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0360: Unknown result type (might be due to invalid IL or missing references)
		//IL_0371: Unknown result type (might be due to invalid IL or missing references)
		//IL_0382: Unknown result type (might be due to invalid IL or missing references)
		//IL_0393: Unknown result type (might be due to invalid IL or missing references)
		//IL_03a4: Unknown result type (might be due to invalid IL or missing references)
		//IL_03b5: Unknown result type (might be due to invalid IL or missing references)
		//IL_03c6: Unknown result type (might be due to invalid IL or missing references)
		//IL_03d7: Unknown result type (might be due to invalid IL or missing references)
		//IL_03e8: Unknown result type (might be due to invalid IL or missing references)
		//IL_0038: Unknown result type (might be due to invalid IL or missing references)
		//IL_0042: Expected O, but got Unknown
		LockFlag = true;
		ActiveOnce = false;
		SR = false;
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.ChartFormLocation, MySettingsProperty.Settings.ChartFormSize);
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
		((Control)CandlesButton).Enabled = false;
		((Control)CandlesCheckBox).Enabled = false;
		((Control)DailyRadioButton).Enabled = false;
		((Control)DetailButton).Enabled = false;
		((Control)DoneButton).Enabled = false;
		((Control)FibButton).Enabled = false;
		((Control)FromDatePicker).Enabled = false;
		((Control)GraphButton).Enabled = false;
		((Control)MinusButton).Enabled = false;
		((Control)MonthlyRadioButton).Enabled = false;
		((Control)NextButton).Enabled = false;
		((Control)OriginalButton).Enabled = false;
		((Control)PatternsButton).Enabled = false;
		((Control)PercentButton).Enabled = false;
		((Control)PortfolioButton).Enabled = false;
		((Control)PreviousButton).Enabled = false;
		((Control)PlusButton).Enabled = false;
		((Control)SetupButton).Enabled = false;
		((Control)ShowPatternsCB).Enabled = false;
		((Control)SkipCheckBox).Enabled = false;
		((Control)SRButton).Enabled = false;
		((Control)StrictCheckBox).Enabled = false;
		((Control)SymbolTextBox).Enabled = false;
		((Control)TargetCheckBox).Enabled = false;
		((Control)ToDatePicker).Enabled = false;
		((Control)VolumeCheckBox).Enabled = false;
		((Control)WeeklyRadioButton).Enabled = false;
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
		val.SetToolTip((Control)(object)FromDatePicker, "The starting date in the file you wish to view.");
		val.SetToolTip((Control)(object)CandlesButton, "Load the Candlestick Form to select candlesticks.");
		val.SetToolTip((Control)(object)CandlesCheckBox, "Check to find candlestick patterns.");
		val.SetToolTip((Control)(object)DataGridView1, "Click to highlight a pattern on the chart.");
		val.SetToolTip((Control)(object)DetailButton, "Click a chart pattern in the data grid (lower left of form) then click this button for pattern details.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)FibButton, "Click two major turning points then this button to show Fibonacci retrace values.");
		val.SetToolTip((Control)(object)ToDatePicker, "The ending date in the file you wish to view.");
		val.SetToolTip((Control)(object)FindingBar, "Shows pattern search progress.");
		val.SetToolTip((Control)(object)GraphButton, "Redraw the chart.");
		val.SetToolTip((Control)(object)LoadingBar, "Shows file loading progress. Keep files short for speed.");
		val.SetToolTip((Control)(object)MinusButton, "Zoom out the chart.");
		val.SetToolTip((Control)(object)NextButton, "Load the next stock.");
		val.SetToolTip((Control)(object)OriginalButton, "Restore the original dates.");
		val.SetToolTip((Control)(object)PatternsButton, "Load the Patterns Form to select chart patterns.");
		val.SetToolTip((Control)(object)PercentButton, "Right mouse click two price bars then % to show percentage move.");
		val.SetToolTip((Control)(object)PlusButton, "Zoom in the chart.");
		val.SetToolTip((Control)(object)PortfolioButton, "Select the portfolio whose files you wish to chart.");
		val.SetToolTip((Control)(object)PreviousButton, "Load the previous stock.");
		val.SetToolTip((Control)(object)ShowPatternsCB, "Show or hide chart patterns.");
		val.SetToolTip((Control)(object)SkipCheckBox, "See Setup Form. Skip to next stock that has a chart pattern or open trade.");
		val.SetToolTip((Control)(object)SRButton, "Turn on/off support/resistance lines. The thicker the line, the more future resistance/support it could have.");
		val.SetToolTip((Control)(object)StrictCheckBox, "Use strict or loose rules when finding chart patterns and candlesticks.");
		val.SetToolTip((Control)(object)SymbolTextBox, "Enter a symbol and click the Graph button to display it if it is available.");
		val.SetToolTip((Control)(object)TargetCheckBox, "Check to show target, stop loss, and ultimate high/low IF available.");
		val.SetToolTip((Control)(object)VolumeCheckBox, "Show or hide volume.");
		val.SetToolTip((Control)(object)DailyRadioButton, "Show quote information using the daily scale.");
		val.SetToolTip((Control)(object)WeeklyRadioButton, "Show quote information using the weekly scale.");
		val.SetToolTip((Control)(object)MonthlyRadioButton, "Show quote information using the monthly scale.");
		val.SetToolTip((Control)(object)SetupButton, "Show chart options.");
		GlobalForm.iFib1 = -1;
		GlobalForm.iFib2 = -1;
		GlobalForm.FirstPoint = default(Point);
		GlobalForm.LinesList.RemoveAll(StubBoolean);
		LoadingBar.Value = 0;
		GlobalForm.DateLookback = Conversions.ToInteger(Interaction.IIf(GlobalForm.DateLookback <= 0, (object)400, (object)GlobalForm.DateLookback));
		TargetCheckBox.Checked = GlobalForm.PatternTargets;
		VolumeCheckBox.Checked = GlobalForm.ChartVolume;
		ShowPatternsCB.Checked = GlobalForm.ShowAllPatterns;
		CandlesCheckBox.Checked = GlobalForm.ShowCandles;
		StrictCheckBox.Checked = GlobalForm.StrictPatterns;
		SkipCheckBox.Checked = false;
		switch (GlobalForm.ChartPeriodShown)
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
		LockFlag = false;
	}

	private void ChartForm_Activated(object sender, EventArgs e)
	{
		//IL_005c: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a7: Invalid comparison between Unknown and I4
		if (ActiveOnce)
		{
			return;
		}
		ActiveOnce = true;
		LoadingBar.Value = 25;
		((Control)LoadingBar).Refresh();
		((Control)this).Refresh();
		if (!ShowPatternsCB.Checked & !CandlesCheckBox.Checked)
		{
			MessageBox.Show("The 'Show patterns' and 'Show candles' check boxes are unchecked so no patterns will display. Check the 'Show patterns' or 'Show candles' check boxes to display patterns.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			((Control)ShowPatternsCB).Focus();
		}
		checked
		{
			if (MyProject.Forms.Mainform.ListBox1.SelectedIndex == -1)
			{
				((Control)SymbolTextBox).Focus();
				if (unchecked((int)MessageBox.Show("No stocks were selected on the prior form. Did you want me to select all of them?", "ChartForm: ChartForm_Load", (MessageBoxButtons)4, (MessageBoxIcon)64)) != 6)
				{
					FromDatePicker.CustomFormat = "yyyy/MM/dd";
					ToDatePicker.CustomFormat = "yyyy/MM/dd";
					FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)(-1 * GlobalForm.DateLookback), DateAndTime.Now);
					ToDatePicker.Value = DateAndTime.Now;
					GlobalForm.ChartStart = FromDatePicker.Value.Date;
					GlobalForm.ChartEnd = ToDatePicker.Value.Date;
					goto IL_04fc;
				}
				MyProject.Forms.Mainform.ListBox1.BeginUpdate();
				int num = MyProject.Forms.Mainform.ListBox1.Items.Count - 1;
				for (int i = 0; i <= num; i++)
				{
					MyProject.Forms.Mainform.ListBox1.SetSelected(i, true);
				}
				MyProject.Forms.Mainform.ListBox1.EndUpdate();
			}
			if (MyProject.Forms.Mainform.ListBox1.Items.Count > 0)
			{
				GlobalForm.LBIndex = 0;
				Filename = MyProject.Forms.Mainform.ListBox1.SelectedItems[GlobalForm.LBIndex].ToString();
				string filename = Filename;
				ProgressBar ProgBar = LoadingBar;
				Label ErrorLabel = this.ErrorLabel;
				bool num2 = GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
				this.ErrorLabel = ErrorLabel;
				LoadingBar = ProgBar;
				if (!num2)
				{
					LoadingBar.Value = 25;
					((Control)LoadingBar).Refresh();
					GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
					GlobalForm.SelectChartType(Chart1);
					if (GlobalForm.IntradayData)
					{
						if (GlobalForm.HLCRange - GlobalForm.DateLookback > 0)
						{
							if ((DateTime.Compare(GlobalForm.nDT[0, (int)(GlobalForm.HLCRange - GlobalForm.DateLookback)], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, (int)(GlobalForm.HLCRange - GlobalForm.DateLookback)], FromDatePicker.MaxDate) <= 0))
							{
								FromDatePicker.Value = GlobalForm.nDT[0, (int)(GlobalForm.HLCRange - GlobalForm.DateLookback)];
							}
							else
							{
								FromDatePicker.Value = DateAndTime.Now;
							}
						}
						else if ((DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MaxDate) <= 0))
						{
							FromDatePicker.Value = GlobalForm.nDT[0, 0];
						}
						else
						{
							FromDatePicker.Value = DateAndTime.Now;
						}
					}
					else
					{
						FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)(-1 * GlobalForm.DateLookback), DateAndTime.Now);
					}
					ToDatePicker.Value = DateAndTime.Now;
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
					GlobalForm.ShowStock(Chart1, FromDatePicker.Value, ToDatePicker.Value, VolumeFlag: true, MAFlag: true);
					LoadingBar.Value = 50;
					((Control)LoadingBar).Refresh();
					DateTime chartStart = GlobalForm.ChartStart;
					DateTime chartEnd = GlobalForm.ChartEnd;
					ProgressBar findingBar = FindingBar;
					bool StopPressed = this.StopPressed;
					FindPatterns.EnterFindPatterns(chartStart, chartEnd, findingBar, ref StopPressed, 2);
					LoadingBar.Value = 75;
					((Control)LoadingBar).Refresh();
					((Form)this).Text = "Chart Form: " + Filename;
					FillGrid();
					LoadingBar.Value = 100;
					((Control)LoadingBar).Refresh();
				}
			}
			goto IL_04fc;
		}
		IL_04fc:
		((Control)CandlesButton).Enabled = true;
		((Control)CandlesCheckBox).Enabled = true;
		((Control)DetailButton).Enabled = true;
		((Control)DoneButton).Enabled = true;
		((Control)FibButton).Enabled = true;
		((Control)FromDatePicker).Enabled = true;
		((Control)GraphButton).Enabled = true;
		((Control)MinusButton).Enabled = true;
		((Control)NextButton).Enabled = true;
		((Control)OriginalButton).Enabled = true;
		((Control)PatternsButton).Enabled = true;
		((Control)PercentButton).Enabled = true;
		((Control)PlusButton).Enabled = true;
		((Control)PortfolioButton).Enabled = true;
		((Control)PreviousButton).Enabled = true;
		((Control)SetupButton).Enabled = true;
		((Control)ShowPatternsCB).Enabled = true;
		((Control)SkipCheckBox).Enabled = true;
		((Control)SRButton).Enabled = true;
		((Control)StrictCheckBox).Enabled = true;
		((Control)SymbolTextBox).Enabled = true;
		((Control)TargetCheckBox).Enabled = true;
		((Control)ToDatePicker).Enabled = true;
		((Control)VolumeCheckBox).Enabled = true;
		GlobalForm.EnableDisableDWM(DailyRadioButton, WeeklyRadioButton, MonthlyRadioButton);
		LoadingBar.Value = 0;
		((Control)LoadingBar).Refresh();
		OriginalDates[0] = FromDatePicker.Value;
		OriginalDates[1] = ToDatePicker.Value;
	}

	private void CandlesButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.CandlesForm).ShowDialog();
		DateTime chartStart = GlobalForm.ChartStart;
		DateTime chartEnd = GlobalForm.ChartEnd;
		ProgressBar findingBar = FindingBar;
		bool StopPressed = this.StopPressed;
		FindPatterns.EnterFindPatterns(chartStart, chartEnd, findingBar, ref StopPressed, 2);
		FillGrid();
		Chart1.Invalidate();
	}

	private void CandlesCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		//IL_0072: Unknown result type (might be due to invalid IL or missing references)
		if (!LockFlag)
		{
			GlobalForm.ShowCandles = CandlesCheckBox.Checked;
			GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			if (!ShowPatternsCB.Checked & !CandlesCheckBox.Checked & SkipCheckBox.Checked & (GlobalForm.SkipType == 1))
			{
				SkipCheckBox.Checked = false;
				MessageBox.Show("I have unchecked the Skip check box because you're not looking for any chart or candlestick patterns. See the Setup Form for more Skip options.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
		}
	}

	private void ChartForm_KeyDown(object sender, KeyEventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_0008: Invalid comparison between Unknown and I4
		//IL_0019: Unknown result type (might be due to invalid IL or missing references)
		//IL_0020: Invalid comparison between Unknown and I4
		if ((int)e.KeyCode == 109)
		{
			PreviousButton_Click(RuntimeHelpers.GetObjectValue(sender), (EventArgs)(object)e);
		}
		else if ((int)e.KeyCode == 107)
		{
			NextButton_Click(RuntimeHelpers.GetObjectValue(sender), (EventArgs)(object)e);
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
		//IL_042f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0436: Expected O, but got Unknown
		//IL_0481: Unknown result type (might be due to invalid IL or missing references)
		//IL_0488: Expected O, but got Unknown
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
		checked
		{
			if (iGridLastRow != -1)
			{
				int num = GlobalForm.PatternCount - 1;
				for (int i = 0; i <= num; i++)
				{
					ref GlobalForm.DisplayFmtns reference = ref GlobalForm.ChartPatterns[i];
					object obj = Interaction.IIf(GlobalForm.ChartPatterns[i].iDataGridViewRow == iGridLastRow, (object)Color.Red, (object)Color.Black);
					reference.RenderColor = ((obj != null) ? ((Color)obj) : default(Color));
				}
				int num2 = GlobalForm.CandleCount - 1;
				for (int j = 0; j <= num2; j++)
				{
					ref GlobalForm.CandleFmtns reference2 = ref GlobalForm.CandlePatterns[j];
					object obj2 = Interaction.IIf(GlobalForm.CandlePatterns[j].iDataGridViewRow == iGridLastRow, (object)Color.Red, (object)Color.Black);
					reference2.RenderColor = ((obj2 != null) ? ((Color)obj2) : default(Color));
				}
				iGridLastRow = -1;
			}
			ShowPatterns.DisplayAllPatterns(e, FromDatePicker.Value, ToDatePicker.Value);
			ShowFibLines(e);
			ShowPercent(e);
			if (SR)
			{
				ShowSR(e);
			}
		}
	}

	private void DataGridView1_RowEnter(object sender, DataGridViewCellEventArgs e)
	{
		if (e.RowIndex != -1)
		{
			iGridLastRow = Conversions.ToInteger(DataGridView1.Rows[e.RowIndex].Cells[11].Value);
			Chart1.Invalidate();
		}
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void FibButton_Click(object sender, EventArgs e)
	{
		//IL_039e: Unknown result type (might be due to invalid IL or missing references)
		//IL_038a: Unknown result type (might be due to invalid IL or missing references)
		if ((GlobalForm.iFib1 != -1) & (GlobalForm.iFib2 != -1))
		{
			int num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, GlobalForm.iFib1], GlobalForm.nHLC[1, GlobalForm.iFib2]) > 0, (object)GlobalForm.iFib1, (object)GlobalForm.iFib2));
			int num2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, GlobalForm.iFib1], GlobalForm.nHLC[2, GlobalForm.iFib2]) < 0, (object)GlobalForm.iFib1, (object)GlobalForm.iFib2));
			decimal num3 = decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num2]);
			string text;
			if (decimal.Compare(num3, 0m) == 0)
			{
				text = "Both points have the same value. Right mouse click one peak, one valley, and try again.";
			}
			else
			{
				text = "Fibonacci extensions above the peak.\r\n";
				text = text + "62%: " + GlobalForm.LimitDecimals(new decimal(Convert.ToDouble(GlobalForm.nHLC[1, num]) + Convert.ToDouble(num3) * 0.62)) + "\r\n";
				text = text + "50%: " + GlobalForm.LimitDecimals(new decimal(Convert.ToDouble(GlobalForm.nHLC[1, num]) + Convert.ToDouble(num3) * 0.5)) + "\r\n";
				text = text + "38%: " + GlobalForm.LimitDecimals(new decimal(Convert.ToDouble(GlobalForm.nHLC[1, num]) + Convert.ToDouble(num3) * 0.38)) + "\r\n\r\n";
				text += "Fibonacci retrace down from the peak.\r\n";
				text = text + "38%: " + GlobalForm.LimitDecimals(new decimal(Convert.ToDouble(GlobalForm.nHLC[1, num]) - Convert.ToDouble(num3) * 0.38)) + "\r\n";
				text = text + "50%: " + GlobalForm.LimitDecimals(new decimal(Convert.ToDouble(GlobalForm.nHLC[1, num]) - Convert.ToDouble(num3) * 0.5)) + "\r\n";
				text = text + "62%: " + GlobalForm.LimitDecimals(new decimal(Convert.ToDouble(GlobalForm.nHLC[1, num]) - Convert.ToDouble(num3) * 0.62)) + "\r\n\r\n";
				text += "Fibonacci extensions below the valley.\r\n";
				text = text + "38%: " + GlobalForm.LimitDecimals(new decimal(Convert.ToDouble(GlobalForm.nHLC[2, num2]) - Convert.ToDouble(num3) * 0.38)) + "\r\n";
				text = text + "50%: " + GlobalForm.LimitDecimals(new decimal(Convert.ToDouble(GlobalForm.nHLC[2, num2]) - Convert.ToDouble(num3) * 0.5)) + "\r\n";
				text = text + "62%: " + GlobalForm.LimitDecimals(new decimal(Convert.ToDouble(GlobalForm.nHLC[2, num2]) - Convert.ToDouble(num3) * 0.62));
				ShowFibs = true;
				Chart1.Invalidate();
			}
			MessageBox.Show(text, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
		else
		{
			MessageBox.Show("Right mouse click on two consecutive major turning points (price bars, one peak and one valley) and then click the Fib button.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
		}
	}

	private void FillGrid()
	{
		//IL_082d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0cb2: Unknown result type (might be due to invalid IL or missing references)
		string text = "";
		int num = 0;
		FindingBar.Value = 50;
		((Control)FindingBar).Refresh();
		DataGridView1.RowHeadersVisible = false;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)1;
		DataGridView1.RowCount = 0;
		DataGridView1.ColumnCount = 12;
		DataGridView1.Columns[0].Name = "Trade Status";
		DataGridView1.Columns[1].Name = "Chart Pattern Description";
		DataGridView1.Columns[2].Name = "Start";
		DataGridView1.Columns[3].Name = "End";
		DataGridView1.Columns[4].Name = "Approx. Breakout";
		DataGridView1.Columns[5].Name = "Approx. Target";
		((DataGridViewCell)DataGridView1.Columns[5].HeaderCell).Style.ForeColor = Color.DarkRed;
		DataGridView1.Columns[6].Name = "Volatility Stop";
		((DataGridViewCell)DataGridView1.Columns[6].HeaderCell).Style.ForeColor = Color.FromArgb(192, 192, 0, 192);
		DataGridView1.Columns[7].Name = "Trade Status";
		DataGridView1.Columns[8].Name = "Ult High/Low";
		((DataGridViewCell)DataGridView1.Columns[8].HeaderCell).Style.ForeColor = Color.Gray;
		DataGridView1.Columns[9].Name = "Up Target";
		((DataGridViewCell)DataGridView1.Columns[9].HeaderCell).Style.ForeColor = Color.Green;
		DataGridView1.Columns[10].Name = "Down Target";
		((DataGridViewCell)DataGridView1.Columns[10].HeaderCell).Style.ForeColor = Color.Green;
		DataGridView1.Columns[11].Visible = false;
		checked
		{
			int num2 = DataGridView1.ColumnCount - 1;
			for (int i = 0; i <= num2; i++)
			{
				DataGridView1.Columns[i].SortMode = (DataGridViewColumnSortMode)0;
			}
			DataGridView1.Columns[0].SortMode = (DataGridViewColumnSortMode)1;
			if ((GlobalForm.PatternCount > 0) & GlobalForm.ShowAllPatterns)
			{
				try
				{
					int num3 = GlobalForm.PatternCount - 1;
					for (int i = 0; i <= num3; i++)
					{
						if ((GlobalForm.ChartPatterns[i].iStartDate >= GlobalForm.ChartStartIndex) & (GlobalForm.ChartPatterns[i].iEndDate <= GlobalForm.ChartEndIndex))
						{
							GlobalForm.ChartPatterns[i].iDataGridViewRow = i;
							DataGridView1.Rows.Add();
							text = GlobalForm.GetPatternPhrase(i);
							GlobalForm.UseOriginalDate = false;
							GlobalForm.GetCPInformation(i);
							int num4 = Strings.InStr(GlobalForm.CPInfo.Status, "on ", (CompareMethod)0);
							if (num4 != 0)
							{
								num4 += Strings.Len("on ") - 1;
								DataGridView1.Rows[num].Cells[0].Value = Strings.Right(GlobalForm.CPInfo.Status, Strings.Len(GlobalForm.CPInfo.Status) - num4);
							}
							else
							{
								DataGridView1.Rows[num].Cells[0].Value = "Open";
							}
							DataGridView1.Rows[num].Cells[1].Value = text;
							int num5 = ((GlobalForm.ChartPatterns[i].iStart2Date == 0) ? GlobalForm.ChartPatterns[i].iStartDate : Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iStartDate < GlobalForm.ChartPatterns[i].iStart2Date, (object)GlobalForm.ChartPatterns[i].iStartDate, (object)GlobalForm.ChartPatterns[i].iStart2Date)));
							int num6 = ((!GlobalForm.UseOriginalDate) ? Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iEndDate > GlobalForm.ChartPatterns[i].iEnd2Date, (object)GlobalForm.ChartPatterns[i].iEndDate, (object)GlobalForm.ChartPatterns[i].iEnd2Date)) : GlobalForm.ChartPatterns[i].iEndDate);
							DataGridView1.Rows[num].Cells[2].Value = Strings.Format((object)GlobalForm.nDT[0, num5], GlobalForm.UserDate);
							DataGridView1.Rows[num].Cells[3].Value = Strings.Format((object)GlobalForm.nDT[0, num6], GlobalForm.UserDate);
							if (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "N/A", false) != 0)
							{
								DataGridView1.Rows[num].Cells[4].Value = GlobalForm.CPInfo.BkoutDirection + Conversions.ToString(Interaction.IIf(Operators.CompareString(GlobalForm.CPInfo.BkoutDate, (string)null, false) != 0, (object)(" on " + GlobalForm.CPInfo.BkoutDate), (object)"None yet"));
							}
							else
							{
								DataGridView1.Rows[num].Cells[4].Value = GlobalForm.CPInfo.BkoutDirection;
							}
							DataGridView1.Rows[num].Cells[5].Value = GlobalForm.CPInfo.Target;
							DataGridView1.Rows[num].Cells[6].Value = GlobalForm.CPInfo.VolStop;
							DataGridView1.Rows[num].Cells[7].Value = RuntimeHelpers.GetObjectValue(Interaction.IIf(Operators.CompareString(GlobalForm.CPInfo.Status, (string)null, false) == 0, (object)"Open", (object)GlobalForm.CPInfo.Status));
							DataGridView1.Rows[num].Cells[8].Value = GlobalForm.LimitDecimals(GlobalForm.CPInfo.UltHLPrice);
							DataGridView1.Rows[num].Cells[9].Value = GlobalForm.LimitDecimals(new decimal(Conversion.Val(GlobalForm.CPInfo.BkoutPrice) * (1.0 + 0.01 * (double)GlobalForm.ShowUpPercentage)));
							if (Conversion.Val(GlobalForm.CPInfo.BkoutPrice) * (1.0 - 0.01 * (double)GlobalForm.ShowDownPercentage) > 0.0)
							{
								DataGridView1.Rows[num].Cells[10].Value = GlobalForm.LimitDecimals(new decimal(Conversion.Val(GlobalForm.CPInfo.BkoutPrice) * (1.0 - 0.01 * (double)GlobalForm.ShowDownPercentage)));
							}
							DataGridView1.Rows[num].Cells[11].Value = num;
							num++;
						}
					}
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					MessageBox.Show(ex2.Message, "ChartForm: FillGrid", (MessageBoxButtons)0, (MessageBoxIcon)16);
					ProjectData.ClearProjectError();
				}
			}
			if ((GlobalForm.CandleCount > 0) & GlobalForm.ShowCandles)
			{
				try
				{
					int num7 = GlobalForm.CandleCount - 1;
					for (int i = 0; i <= num7; i++)
					{
						if ((GlobalForm.CandlePatterns[i].iStartDate >= GlobalForm.ChartStartIndex) & (GlobalForm.CandlePatterns[i].iEndDate <= GlobalForm.ChartEndIndex))
						{
							GlobalForm.CandlePatterns[i].iDataGridViewRow = num;
							DataGridView1.Rows.Add();
							int num8 = Strings.InStr(GlobalForm.CandlePatterns[i].TradeStatus, "on ", (CompareMethod)0);
							if (num8 != 0)
							{
								num8 += Strings.Len("on ") - 1;
								DataGridView1.Rows[num].Cells[0].Value = Strings.Right(GlobalForm.CandlePatterns[i].TradeStatus, Strings.Len(GlobalForm.CandlePatterns[i].TradeStatus) - num8);
							}
							else
							{
								DataGridView1.Rows[num].Cells[0].Value = "Open";
							}
							DataGridView1.Rows[num].Cells[1].Value = GlobalForm.CandlePatterns[i].Phrase;
							DataGridView1.Rows[num].Cells[2].Value = Strings.Format((object)GlobalForm.nDT[0, GlobalForm.CandlePatterns[i].iStartDate], GlobalForm.UserDate);
							DataGridView1.Rows[num].Cells[3].Value = Strings.Format((object)GlobalForm.nDT[0, GlobalForm.CandlePatterns[i].iEndDate], GlobalForm.UserDate);
							DataGridView1.Rows[num].Cells[4].Value = GlobalForm.CandlePatterns[i].BkoutDirection;
							DataGridView1.Rows[num].Cells[5].Value = GlobalForm.LimitDecimals(new decimal(Conversion.Val(GlobalForm.CandlePatterns[i].PriceTarget)));
							DataGridView1.Rows[num].Cells[6].Value = GlobalForm.LimitDecimals(new decimal(Conversion.Val(GlobalForm.CandlePatterns[i].StopPrice)));
							DataGridView1.Rows[num].Cells[7].Value = GlobalForm.CandlePatterns[i].TradeStatus;
							DataGridView1.Rows[num].Cells[8].Value = GlobalForm.LimitDecimals(GlobalForm.CandlePatterns[i].UltHLPrice);
							DataGridView1.Rows[num].Cells[9].Value = GlobalForm.LimitDecimals(new decimal(Convert.ToDouble(GlobalForm.CandlePatterns[i].dBreakoutPrice) * (1.0 + 0.01 * (double)GlobalForm.ShowUpPercentage)));
							if (Convert.ToDouble(GlobalForm.CandlePatterns[i].dBreakoutPrice) * (1.0 - 0.01 * (double)GlobalForm.ShowDownPercentage) > 0.0)
							{
								DataGridView1.Rows[num].Cells[10].Value = GlobalForm.LimitDecimals(new decimal(Convert.ToDouble(GlobalForm.CandlePatterns[i].dBreakoutPrice) * (1.0 - 0.01 * (double)GlobalForm.ShowDownPercentage)));
							}
							DataGridView1.Rows[num].Cells[11].Value = num;
							num++;
						}
					}
				}
				catch (Exception ex3)
				{
					ProjectData.SetProjectError(ex3);
					Exception ex4 = ex3;
					MessageBox.Show(ex4.Message, "ChartForm: FillGrid", (MessageBoxButtons)0, (MessageBoxIcon)16);
					ProjectData.ClearProjectError();
				}
			}
			DataGridViewColumn val = DataGridView1.Columns[0];
			DataGridView1.Sort(val, ListSortDirection.Descending);
			val.HeaderCell.SortGlyphDirection = (SortOrder)2;
			DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)6;
			DataGridView1.RowHeadersVisible = true;
			FindingBar.Value = 0;
			((Control)FindingBar).Refresh();
		}
	}

	private void FromDatePicker_Validated(object sender, EventArgs e)
	{
		DateTimePicker fromDatePicker = FromDatePicker;
		DateTime FromDate = fromDatePicker.Value;
		DateTimePicker toDatePicker;
		DateTime ToDate = (toDatePicker = ToDatePicker).Value;
		GlobalForm.SwapDates(ref FromDate, ref ToDate);
		toDatePicker.Value = ToDate;
		fromDatePicker.Value = FromDate;
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

	private void GraphButton_Click(object sender, EventArgs e)
	{
		DateTimePicker fromDatePicker;
		DateTime FromDate = (fromDatePicker = FromDatePicker).Value;
		DateTimePicker toDatePicker;
		DateTime ToDate = (toDatePicker = ToDatePicker).Value;
		bool num = GlobalForm.SwapDates(ref FromDate, ref ToDate);
		toDatePicker.Value = ToDate;
		fromDatePicker.Value = FromDate;
		if (num)
		{
			return;
		}
		GlobalForm.FirstPoint = default(Point);
		GlobalForm.LinesList.RemoveAll(StubBoolean);
		if (((TextBoxBase)SymbolTextBox).TextLength > 0)
		{
			Filename = SymbolTextBox.Text;
			if (Strings.InStr(Filename, ".", (CompareMethod)0) == 0)
			{
				string text = Filename + ".csv";
				if (!File.Exists(GlobalForm.OpenPath + "\\" + text))
				{
					text = Filename + ".txt";
				}
				Filename = text;
			}
			string filename = Filename;
			ProgressBar ProgBar = LoadingBar;
			Label ErrorLabel = this.ErrorLabel;
			bool num2 = GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
			this.ErrorLabel = ErrorLabel;
			LoadingBar = ProgBar;
			if (!num2)
			{
				GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
				GlobalForm.SelectChartType(Chart1);
				GlobalForm.SetupDateIndexes(GlobalForm.ChartStart, GlobalForm.ChartEnd);
				GlobalForm.CheckDates(FromDatePicker, ToDatePicker);
				SymbolTextBox.Text = "";
				GlobalForm.ShowStock(Chart1, GlobalForm.ChartStartIndex, GlobalForm.ChartEndIndex, VolumeCheckBox.Checked, MAFlag: true);
				DateTime chartStart = GlobalForm.ChartStart;
				DateTime chartEnd = GlobalForm.ChartEnd;
				ProgressBar findingBar = FindingBar;
				bool StopPressed = this.StopPressed;
				FindPatterns.EnterFindPatterns(chartStart, chartEnd, findingBar, ref StopPressed, 2);
				((Form)this).Text = "Chart Form: " + Filename;
				FillGrid();
			}
			GlobalForm.EnableDisableDWM(DailyRadioButton, WeeklyRadioButton, MonthlyRadioButton);
		}
		else
		{
			GlobalForm.SetupDateIndexes(GlobalForm.ChartStart, GlobalForm.ChartEnd);
			if (!GlobalForm.ShowStock(Chart1, GlobalForm.ChartStartIndex, GlobalForm.ChartEndIndex, VolumeCheckBox.Checked, MAFlag: true))
			{
				DateTime chartStart2 = GlobalForm.ChartStart;
				DateTime chartEnd2 = GlobalForm.ChartEnd;
				ProgressBar findingBar2 = FindingBar;
				bool StopPressed = this.StopPressed;
				FindPatterns.EnterFindPatterns(chartStart2, chartEnd2, findingBar2, ref StopPressed, 2);
				((Form)this).Text = "Chart Form: " + Filename;
				FillGrid();
			}
		}
	}

	private void MinusButton_Click_1(object sender, EventArgs e)
	{
		long num = DateAndTime.DateDiff((DateInterval)4, OriginalDates[0], OriginalDates[1], (FirstDayOfWeek)1, (FirstWeekOfYear)1);
		if (num > 365)
		{
			num = 365L;
		}
		checked
		{
			if (DateTime.Compare(ToDatePicker.Value.Date, DateAndTime.Now.Date) != 0)
			{
				ToDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)(1 * num) / 2.0, ToDatePicker.Value);
				FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)(-1 * num) / 2.0, FromDatePicker.Value);
			}
			else
			{
				FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)(-1 * num), FromDatePicker.Value);
			}
			if (DateTime.Compare(FromDatePicker.Value, GlobalForm.nDT[0, 0]) < 0)
			{
				FromDatePicker.Value = GlobalForm.nDT[0, 0];
				Interaction.Beep();
			}
			if (DateTime.Compare(ToDatePicker.Value, DateAndTime.Now) > 0)
			{
				ToDatePicker.Value = DateAndTime.Now;
			}
			FromDatePicker_Validated(RuntimeHelpers.GetObjectValue(sender), e);
			GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		}
	}

	private void OriginalButton_Click_1(object sender, EventArgs e)
	{
		FromDatePicker.Value = OriginalDates[0];
		ToDatePicker.Value = OriginalDates[1];
		FromDatePicker_Validated(RuntimeHelpers.GetObjectValue(sender), e);
		GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
	}

	private void PlusButton_Click_1(object sender, EventArgs e)
	{
		long num = DateAndTime.DateDiff((DateInterval)4, OriginalDates[0], OriginalDates[1], (FirstDayOfWeek)1, (FirstWeekOfYear)1);
		if (num > 365)
		{
			num = 365L;
		}
		if (DateTime.Compare(ToDatePicker.Value.Date, DateAndTime.Now.Date) != 0)
		{
			ToDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)num / 2.0, ToDatePicker.Value);
			FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)num / 2.0, FromDatePicker.Value);
		}
		else
		{
			FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)num, FromDatePicker.Value);
		}
		if (DateTime.Compare(FromDatePicker.Value, DateAndTime.Now) > 0)
		{
			FromDatePicker.Value = DateAndTime.Now;
		}
		if (DateTime.Compare(ToDatePicker.Value, DateAndTime.Now) > 0)
		{
			ToDatePicker.Value = DateAndTime.Now;
			Interaction.Beep();
		}
		FromDatePicker_Validated(RuntimeHelpers.GetObjectValue(sender), e);
		GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
	}

	private void NextButton_Click(object sender, EventArgs e)
	{
		//IL_0046: Unknown result type (might be due to invalid IL or missing references)
		//IL_0050: Expected O, but got Unknown
		((Control)this).Cursor = Cursors.WaitCursor;
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
			GlobalForm.LBIndex++;
			if (GlobalForm.LBIndex >= MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count)
			{
				GlobalForm.LBIndex = MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count - 1;
				Interaction.Beep();
			}
			else
			{
				GlobalForm.FirstPoint = default(Point);
				GlobalForm.LinesList.RemoveAll(StubBoolean);
				Filename = MyProject.Forms.Mainform.ListBox1.SelectedItems[GlobalForm.LBIndex].ToString();
				string filename = Filename;
				ProgressBar ProgBar = LoadingBar;
				Label ErrorLabel = this.ErrorLabel;
				bool num = GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
				this.ErrorLabel = ErrorLabel;
				LoadingBar = ProgBar;
				if (!num)
				{
					GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
					GlobalForm.SelectChartType(Chart1);
					GlobalForm.CheckDates(FromDatePicker, ToDatePicker);
					if (!GlobalForm.ShowStock(Chart1, FromDatePicker.Value, ToDatePicker.Value, VolumeFlag: true, MAFlag: true))
					{
						DateTime value = FromDatePicker.Value;
						DateTime value2 = ToDatePicker.Value;
						ProgressBar findingBar = FindingBar;
						bool StopPressed = this.StopPressed;
						FindPatterns.EnterFindPatterns(value, value2, findingBar, ref StopPressed, 2);
						if (SkipCheckBox.Checked && GlobalForm.SkipType == 1)
						{
							if ((GlobalForm.PatternCount == 0) & (GlobalForm.CandleCount == 0))
							{
								NextButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
							}
							else
							{
								Interaction.Beep();
							}
						}
					}
					GlobalForm.EnableDisableDWM(DailyRadioButton, WeeklyRadioButton, MonthlyRadioButton);
					((Form)this).Text = "Chart Form: " + Filename;
					FillGrid();
					if (SkipCheckBox.Checked & (GlobalForm.SkipType == 2))
					{
						if (DataGridView1.RowCount != 0)
						{
							bool flag = false;
							int num2 = DataGridView1.RowCount - 1;
							for (int i = 0; i <= num2; i++)
							{
								if (Operators.CompareString(Conversions.ToString(DataGridView1.Rows[i].Cells[0].Value), "Open", false) == 0)
								{
									flag = true;
									break;
								}
							}
							if (!flag)
							{
								NextButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
							}
							else
							{
								Interaction.Beep();
							}
						}
						else
						{
							NextButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
						}
					}
				}
			}
			((Control)this).Cursor = Cursors.Default;
		}
	}

	private void PatternsButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.PatternsForm).ShowDialog();
		DateTime chartStart = GlobalForm.ChartStart;
		DateTime chartEnd = GlobalForm.ChartEnd;
		ProgressBar findingBar = FindingBar;
		bool StopPressed = this.StopPressed;
		FindPatterns.EnterFindPatterns(chartStart, chartEnd, findingBar, ref StopPressed, 2);
		FillGrid();
		Chart1.Invalidate();
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

	private void PortfolioButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0010: Unknown result type (might be due to invalid IL or missing references)
		//IL_0016: Invalid comparison between Unknown and I4
		((Form)MyProject.Forms.PortfolioDialog).ShowDialog();
		if ((int)GlobalForm.CustomResult == 1)
		{
			GlobalForm.OpenPath = GlobalForm.PDSelectionPath;
			MyProject.Forms.Mainform.MFDisplayFiles(BrowseFlag: false);
			MyProject.Forms.Mainform.AllButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			GlobalForm.LBIndex = -1;
			NextButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		}
	}

	private void PreviousButton_Click(object sender, EventArgs e)
	{
		//IL_006b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0075: Expected O, but got Unknown
		((Control)this).Cursor = Cursors.WaitCursor;
		checked
		{
			GlobalForm.LBIndex--;
			if (GlobalForm.LBIndex < 0)
			{
				GlobalForm.LBIndex = 0;
				Interaction.Beep();
			}
			else
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
				CurrentAnnotation = new CalloutAnnotation();
				((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)CurrentAnnotation);
				GlobalForm.FirstPoint = default(Point);
				GlobalForm.LinesList.RemoveAll(StubBoolean);
				Filename = MyProject.Forms.Mainform.ListBox1.SelectedItems[GlobalForm.LBIndex].ToString();
				string filename = Filename;
				ProgressBar ProgBar = LoadingBar;
				Label ErrorLabel = this.ErrorLabel;
				bool num = GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
				this.ErrorLabel = ErrorLabel;
				LoadingBar = ProgBar;
				if (!num)
				{
					GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
					GlobalForm.SelectChartType(Chart1);
					GlobalForm.CheckDates(FromDatePicker, ToDatePicker);
					if (!GlobalForm.ShowStock(Chart1, FromDatePicker.Value, ToDatePicker.Value, VolumeFlag: true, MAFlag: true))
					{
						DateTime value = FromDatePicker.Value;
						DateTime value2 = ToDatePicker.Value;
						ProgressBar findingBar = FindingBar;
						bool StopPressed = this.StopPressed;
						FindPatterns.EnterFindPatterns(value, value2, findingBar, ref StopPressed, 2);
						if (SkipCheckBox.Checked && GlobalForm.SkipType == 1)
						{
							if ((GlobalForm.PatternCount == 0) & (GlobalForm.CandleCount == 0))
							{
								PreviousButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
							}
							else
							{
								Interaction.Beep();
							}
						}
					}
					GlobalForm.EnableDisableDWM(DailyRadioButton, WeeklyRadioButton, MonthlyRadioButton);
					((Form)this).Text = "Chart Form: " + Filename;
					FillGrid();
					if (SkipCheckBox.Checked & (GlobalForm.SkipType == 2))
					{
						if (DataGridView1.RowCount != 0)
						{
							bool flag = false;
							int num2 = DataGridView1.RowCount - 1;
							for (int i = 0; i <= num2; i++)
							{
								if (Operators.CompareString(Conversions.ToString(DataGridView1.Rows[i].Cells[0].Value), "Open", false) == 0)
								{
									flag = true;
									break;
								}
							}
							if (!flag)
							{
								PreviousButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
							}
							else
							{
								Interaction.Beep();
							}
						}
						else
						{
							PreviousButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
						}
					}
				}
			}
			((Control)this).Cursor = Cursors.Default;
		}
	}

	private void SetupButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.SetupForm).ShowDialog();
		TargetCheckBox.Checked = GlobalForm.PatternTargets;
		string filename = Filename;
		ProgressBar ProgBar = LoadingBar;
		Label ErrorLabel = this.ErrorLabel;
		GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
		this.ErrorLabel = ErrorLabel;
		LoadingBar = ProgBar;
		GlobalForm.SelectChartType(Chart1);
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
		GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
	}

	private void ShowPatternsCB_CheckedChanged(object sender, EventArgs e)
	{
		//IL_0072: Unknown result type (might be due to invalid IL or missing references)
		if (!LockFlag)
		{
			GlobalForm.ShowAllPatterns = ShowPatternsCB.Checked;
			GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			if (!ShowPatternsCB.Checked & !CandlesCheckBox.Checked & SkipCheckBox.Checked & (GlobalForm.SkipType == 1))
			{
				SkipCheckBox.Checked = false;
				MessageBox.Show("I have unchecked the Skip check box because you're not looking for any chart or candlestick patterns. See the Setup Form for more Skip options.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
		}
	}

	private void ShowFibLines(ChartPaintEventArgs e)
	{
		//IL_0024: Unknown result type (might be due to invalid IL or missing references)
		//IL_0044: Unknown result type (might be due to invalid IL or missing references)
		//IL_004b: Expected O, but got Unknown
		//IL_0202: Unknown result type (might be due to invalid IL or missing references)
		//IL_0209: Expected O, but got Unknown
		//IL_020e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0215: Expected O, but got Unknown
		int num = 4;
		if (!ShowFibs || !(e.ChartElement is Series) || Operators.CompareString(((Series)e.ChartElement).Name, "CandleSeries", false) != 0)
		{
			return;
		}
		Series val = (Series)e.ChartElement;
		ShowFibs = false;
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
			PointF pointF3 = default(PointF);
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
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.HLCRange)
				{
					pointF3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num2 + 1));
					break;
				}
				num2++;
			}
			Font val2 = new Font("Arial", 8f);
			SolidBrush val3 = new SolidBrush(Color.Green);
			pointF3.Y = 0f;
			pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
			pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
			pointF3 = e.ChartGraphics.GetAbsolutePoint(pointF3);
			pointF3.X -= 11f;
			PointF pointF4 = default(PointF);
			pointF4.Y = pointF.Y - pointF2.Y;
			PointF pointF5 = default(PointF);
			pointF5.Y = (float)((double)pointF.Y + 0.38 * (double)pointF4.Y);
			pointF5.X = Conversions.ToSingle(Interaction.IIf(pointF.X > pointF2.X, (object)pointF.X, (object)pointF2.X));
			pointF3.Y = pointF5.Y;
			e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF5, pointF3);
			e.ChartGraphics.Graphics.DrawString("38%", val2, (Brush)(object)val3, pointF3);
			pointF5.Y = (float)((double)pointF.Y + 0.5 * (double)pointF4.Y);
			pointF3.Y = pointF5.Y;
			e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF5, pointF3);
			e.ChartGraphics.Graphics.DrawString("50%", val2, (Brush)(object)val3, pointF3);
			pointF5.Y = (float)((double)pointF.Y + 0.62 * (double)pointF4.Y);
			pointF3.Y = pointF5.Y;
			e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF5, pointF3);
			e.ChartGraphics.Graphics.DrawString("62%", val2, (Brush)(object)val3, pointF3);
			pointF5.Y = (float)((double)pointF.Y - 0.38 * (double)pointF4.Y);
			pointF3.Y = pointF5.Y;
			e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF5, pointF3);
			e.ChartGraphics.Graphics.DrawString("38%", val2, (Brush)(object)val3, pointF3);
			pointF5.Y = (float)((double)pointF.Y - 0.5 * (double)pointF4.Y);
			pointF3.Y = pointF5.Y;
			e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF5, pointF3);
			e.ChartGraphics.Graphics.DrawString("50%", val2, (Brush)(object)val3, pointF3);
			pointF5.Y = (float)((double)pointF.Y - 0.62 * (double)pointF4.Y);
			pointF3.Y = pointF5.Y;
			e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF5, pointF3);
			e.ChartGraphics.Graphics.DrawString("62%", val2, (Brush)(object)val3, pointF3);
			pointF5.Y = (float)((double)pointF2.Y - 0.38 * (double)pointF4.Y);
			pointF3.Y = pointF5.Y;
			e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF5, pointF3);
			e.ChartGraphics.Graphics.DrawString("38%", val2, (Brush)(object)val3, pointF3);
			pointF5.Y = (float)((double)pointF2.Y - 0.5 * (double)pointF4.Y);
			pointF3.Y = pointF5.Y;
			e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF5, pointF3);
			e.ChartGraphics.Graphics.DrawString("50%", val2, (Brush)(object)val3, pointF3);
			pointF5.Y = (float)((double)pointF2.Y - 0.62 * (double)pointF4.Y);
			pointF3.Y = pointF5.Y;
			e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF5, pointF3);
			e.ChartGraphics.Graphics.DrawString("62%", val2, (Brush)(object)val3, pointF3);
			ChartGraphics chartGraphics = e.ChartGraphics;
			pointF.Y -= 6f;
			chartGraphics.Graphics.DrawEllipse(Pens.Blue, (float)((double)pointF.X - (double)num / 2.0), (float)((double)pointF.Y - (double)num / 2.0), (float)num, (float)num);
			pointF2.Y += 4f;
			chartGraphics.Graphics.DrawEllipse(Pens.Blue, (float)((double)pointF2.X - (double)num / 2.0), (float)((double)pointF2.Y - (double)num / 2.0), (float)num, (float)num);
			((Brush)val3).Dispose();
			val2.Dispose();
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

	private void ShowSR(ChartPaintEventArgs e)
	{
		//IL_0036: Unknown result type (might be due to invalid IL or missing references)
		//IL_0056: Unknown result type (might be due to invalid IL or missing references)
		//IL_005d: Expected O, but got Unknown
		PointF pointF = default(PointF);
		PointF pointF2 = default(PointF);
		PointF pointF3 = default(PointF);
		PointF pointF4 = default(PointF);
		if (!(e.ChartElement is Series) || Operators.CompareString(((Series)e.ChartElement).Name, "CandleSeries", false) != 0)
		{
			return;
		}
		Series val = (Series)e.ChartElement;
		FindPatterns.FindAllTops(2);
		FindPatterns.FindAllBottoms(2);
		int num = 0;
		int num2 = 0;
		int num3 = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)val.Points)
			{
				if (num <= FindPatterns.ArrayTops.Length - 1 && num3 + GlobalForm.ChartStartIndex == FindPatterns.ArrayTops[num])
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num3 + 1));
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(GlobalForm.ChartEndIndex - GlobalForm.ChartStartIndex));
					pointF2.Y = pointF.Y;
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
					e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF, pointF2);
					num++;
				}
				if (num2 <= FindPatterns.ArrayBottoms.Length - 1 && num3 + GlobalForm.ChartStartIndex == FindPatterns.ArrayBottoms[num2])
				{
					pointF3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num3 + 1));
					pointF3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					pointF4.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(GlobalForm.ChartEndIndex - GlobalForm.ChartStartIndex));
					pointF4.Y = pointF3.Y;
					pointF3 = e.ChartGraphics.GetAbsolutePoint(pointF3);
					pointF4 = e.ChartGraphics.GetAbsolutePoint(pointF4);
					e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF3, pointF4);
					num2++;
				}
				if ((num == FindPatterns.ArrayTops.Length) & (num2 == FindPatterns.ArrayBottoms.Length))
				{
					break;
				}
				num3++;
			}
		}
	}

	private void SkipCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		//IL_0041: Unknown result type (might be due to invalid IL or missing references)
		if (!ShowPatternsCB.Checked & !CandlesCheckBox.Checked & SkipCheckBox.Checked & (GlobalForm.SkipType == 1))
		{
			MessageBox.Show("Skip works if the 'Show patterns' or 'Show candles' check boxes are checked. See the Setup Form for more Skip options. I'm unchecking Skip.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			SkipCheckBox.Checked = false;
			((Control)CandlesCheckBox).Focus();
		}
	}

	private void SRButton_Click(object sender, EventArgs e)
	{
		SR = !SR;
		Chart1.Invalidate();
	}

	private void StrictCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		if (!LockFlag)
		{
			GlobalForm.StrictPatterns = StrictCheckBox.Checked;
			GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		}
	}

	private bool StubBoolean(GlobalForm.LineEndPoints sPoint)
	{
		return true;
	}

	private void TargetCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		if (!LockFlag)
		{
			GlobalForm.PatternTargets = TargetCheckBox.Checked;
			Chart1.Refresh();
		}
	}

	private void ToDatePicker_Validated(object sender, EventArgs e)
	{
		DateTimePicker fromDatePicker = FromDatePicker;
		DateTime FromDate = fromDatePicker.Value;
		DateTimePicker toDatePicker;
		DateTime ToDate = (toDatePicker = ToDatePicker).Value;
		GlobalForm.SwapDates(ref FromDate, ref ToDate);
		toDatePicker.Value = ToDate;
		fromDatePicker.Value = FromDate;
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

	private void VolumeCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		if (!LockFlag)
		{
			GlobalForm.ChartVolume = VolumeCheckBox.Checked;
			GlobalForm.ShowStock(Chart1, FromDatePicker.Value, ToDatePicker.Value, VolumeFlag: true, MAFlag: true);
			((Form)this).Text = "Chart Form: " + Filename;
			FillGrid();
		}
	}

	private void WeeklyRadioButton_CheckedChanged(object sender, EventArgs e)
	{
		RadioButton val = (RadioButton)((sender is RadioButton) ? sender : null);
		if (val != null && (val.Checked & (((ButtonBase)val).Text.Length > 0)))
		{
			switch (Conversions.ToInteger(((Control)val).Tag))
			{
			case 0:
				GlobalForm.DataPeriodConverter(0);
				break;
			case 1:
				GlobalForm.DataPeriodConverter(1);
				break;
			case 2:
				GlobalForm.DataPeriodConverter(2);
				break;
			}
			GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		}
	}

	private void DetailButton_Click(object sender, EventArgs e)
	{
		//IL_0046: Unknown result type (might be due to invalid IL or missing references)
		//IL_04ef: Unknown result type (might be due to invalid IL or missing references)
		if (((BaseCollection)DataGridView1.SelectedRows).Count == 0)
		{
			if (DataGridView1.RowCount <= 0)
			{
				MessageBox.Show("There are no patterns to discuss. Try clicking the Patterns button and picking more patterns, load another file, or change the from/to dates and click Graph.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				return;
			}
			DataGridView1.Rows[0].Selected = true;
		}
		string text2;
		if (((BaseCollection)DataGridView1.SelectedRows).Count > 0)
		{
			int index = ((DataGridViewBand)DataGridView1.SelectedRows[0]).Index;
			string text = Conversions.ToString(DataGridView1.Rows[index].Cells[1].Value);
			int num = Conversions.ToInteger(GlobalForm.TranslatePatternName(text, GlobalForm.PASSNAME));
			if (num != -1)
			{
				text2 = text + "\r\n\r\n";
				text2 = text2 + "Performance rank: " + GlobalForm.PDeets[num].sPerformance + "\r\n";
				if (GlobalForm.PDeets[num].iBreakoutUp != -1)
				{
					text2 = text2 + "Upward breakout: " + GlobalForm.PDeets[num].iBreakoutUp + "% of the time.\r\n";
				}
				if (GlobalForm.PDeets[num].iBreakoutDown != -1)
				{
					text2 = text2 + "Downward breakout " + GlobalForm.PDeets[num].iBreakoutDown + "% of the time.\r\n";
				}
				if (GlobalForm.PDeets[num].iReversal != -1)
				{
					text2 = text2 + "Acts as reversal " + GlobalForm.PDeets[num].iReversal + "% of the time.\r\n";
				}
				if (GlobalForm.PDeets[num].iContinuation != -1)
				{
					text2 = text2 + "Acts as continuation " + GlobalForm.PDeets[num].iContinuation + "% of the time.\r\n";
				}
				text2 += "\r\n";
				if (GlobalForm.PDeets[num].iFailureRate != -1)
				{
					text2 = text2 + "5% failure rate: " + GlobalForm.PDeets[num].iFailureRate + "%.\r\n";
				}
				if (GlobalForm.PDeets[num].iChangeTrend != -1)
				{
					text2 = text2 + "Price moves >20% after breakout " + GlobalForm.PDeets[num].iChangeTrend + "% of the time.\r\n";
				}
				if (GlobalForm.PDeets[num].iPercentageBust != -1)
				{
					text2 = text2 + "Pattern busts " + GlobalForm.PDeets[num].iPercentageBust + "% of the time.\r\n";
				}
				if (GlobalForm.PDeets[num].iPctMeetingTargetUp != -1)
				{
					text2 = text2 + "Price reaches upward breakout target " + GlobalForm.PDeets[num].iPctMeetingTargetUp + "% of the time.\r\n";
				}
				if (GlobalForm.PDeets[num].iPctMeetingTargetDown != -1)
				{
					text2 = text2 + "Price reaches downward breakout target " + GlobalForm.PDeets[num].iPctMeetingTargetDown + "% of the time.\r\n";
				}
				text2 += "\r\n";
				if (GlobalForm.PDeets[num].iThrowbacks != -1)
				{
					text2 = text2 + "Expect a throwback " + GlobalForm.PDeets[num].iThrowbacks + "% of the time.\r\n";
				}
				if (GlobalForm.PDeets[num].iPullbacks != -1)
				{
					text2 = text2 + "Expect a pullback " + GlobalForm.PDeets[num].iPullbacks + "% of the time.\r\n";
				}
				if (GlobalForm.PDeets[num].iTall != -1f)
				{
					text2 = text2 + "Patterns taller than " + GlobalForm.PDeets[num].iTall + "% median of breakout price may outperform.\r\n";
				}
				if (GlobalForm.PDeets[num].iWide != -1)
				{
					DateTime dateTime = Conversions.ToDate(DataGridView1.Rows[index].Cells[2].Value);
					DateTime dateTime2 = Conversions.ToDate(DataGridView1.Rows[index].Cells[3].Value);
					int num2 = checked((int)DateAndTime.DateDiff((DateInterval)4, dateTime, dateTime2, (FirstDayOfWeek)1, (FirstWeekOfYear)1));
					text2 = text2 + "Patterns wider than median " + GlobalForm.PDeets[num].iWide + " days may outperform.";
					text2 = text2 + " This pattern is " + Conversions.ToString(Interaction.IIf(num2 >= GlobalForm.PDeets[num].iWide, (object)"wide.", (object)"narrow.")) + "\r\n";
				}
				if (Operators.CompareString(GlobalForm.PDeets[num].sTips, "", false) != 0)
				{
					text2 = text2 + GlobalForm.PDeets[num].sTips + "\r\n";
				}
				text2 += "\r\n";
			}
			else
			{
				text2 = "No information is available on this pattern.";
			}
			text2 += "Visit ThePatternSite.com for definitions (See Glossary) or buy the most recent edition of my 'Encyclopedia of Chart Patterns' book. Performance statistics refer to bull markets only.";
		}
		else
		{
			text2 = "Click in the grid (lower left of screen) for information on chart patterns.";
		}
		MessageBox.Show(text2, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}
}
