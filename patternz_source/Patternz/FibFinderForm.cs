using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Microsoft.VisualBasic.Devices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class FibFinderForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("AllPortfoliosButton")]
	private Button _AllPortfoliosButton;

	[CompilerGenerated]
	[AccessedThroughProperty("HelpButton1")]
	private Button _HelpButton1;

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
	[AccessedThroughProperty("DataGridView1")]
	private DataGridView _DataGridView1;

	[CompilerGenerated]
	[AccessedThroughProperty("E62CB")]
	private CheckBox _E62CB;

	[CompilerGenerated]
	[AccessedThroughProperty("E50CB")]
	private CheckBox _E50CB;

	[CompilerGenerated]
	[AccessedThroughProperty("E38CB")]
	private CheckBox _E38CB;

	[CompilerGenerated]
	[AccessedThroughProperty("R62CB")]
	private CheckBox _R62CB;

	[CompilerGenerated]
	[AccessedThroughProperty("R50CB")]
	private CheckBox _R50CB;

	[CompilerGenerated]
	[AccessedThroughProperty("R38CB")]
	private CheckBox _R38CB;

	[CompilerGenerated]
	[AccessedThroughProperty("Chart1")]
	private Chart _Chart1;

	[CompilerGenerated]
	[AccessedThroughProperty("EAllCB")]
	private CheckBox _EAllCB;

	[CompilerGenerated]
	[AccessedThroughProperty("RAllCB")]
	private CheckBox _RAllCB;

	private const string KEYFF = "FibForm";

	private const int FFDL = 180;

	private readonly int fSYMBOL;

	private readonly int fLASTCLOSE;

	private readonly int fTYPE;

	private readonly int fSTART;

	private readonly int fEND;

	private readonly int fREDATE;

	private readonly int fVALUE;

	private readonly int fPATH;

	private readonly int tCOLUMNCOUNT;

	private bool StopPressed;

	private int iRow;

	private Point StartPoint;

	private Point EndPoint;

	private bool Crosshair;

	private Point CrosshairPoint;

	private Pen CrosshairPen;

	private bool lsR38;

	private bool lsR50;

	private bool lsR62;

	private bool lsRAll;

	private bool lsE38;

	private bool lsE50;

	private bool lsE62;

	private bool lsEAll;

	private int lsRNUD;

	private int lsENUD;

	private int lsPriceBarsNUD;

	private long FFDateLookBack;

	private long lsFFDateLookBack;

	private string FileNameInUse;

	private bool LockFlag;

	private bool Busy;

	private CalloutAnnotation CurrentAnnotation;

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

	internal virtual Button AllPortfoliosButton
	{
		[CompilerGenerated]
		get
		{
			return _AllPortfoliosButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = AllPortfoliosButton_Click;
			Button val = _AllPortfoliosButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_AllPortfoliosButton = value;
			val = _AllPortfoliosButton;
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

	[field: AccessedThroughProperty("ProgressBar1")]
	internal virtual ProgressBar ProgressBar1
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

	[field: AccessedThroughProperty("SymbolTextBox")]
	internal virtual TextBox SymbolTextBox
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
			EventHandler eventHandler = DataGridView1_SelectionChanged;
			DataGridView val = _DataGridView1;
			if (val != null)
			{
				val.SelectionChanged -= eventHandler;
			}
			_DataGridView1 = value;
			val = _DataGridView1;
			if (val != null)
			{
				val.SelectionChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Panel1")]
	internal virtual Panel Panel1
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

	[field: AccessedThroughProperty("ENUD")]
	internal virtual NumericUpDown ENUD
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

	[field: AccessedThroughProperty("RNUD")]
	internal virtual NumericUpDown RNUD
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual CheckBox E62CB
	{
		[CompilerGenerated]
		get
		{
			return _E62CB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = E38CB_CheckedChanged;
			CheckBox val = _E62CB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_E62CB = value;
			val = _E62CB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox E50CB
	{
		[CompilerGenerated]
		get
		{
			return _E50CB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = E38CB_CheckedChanged;
			CheckBox val = _E50CB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_E50CB = value;
			val = _E50CB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox E38CB
	{
		[CompilerGenerated]
		get
		{
			return _E38CB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = E38CB_CheckedChanged;
			CheckBox val = _E38CB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_E38CB = value;
			val = _E38CB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox R62CB
	{
		[CompilerGenerated]
		get
		{
			return _R62CB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = E38CB_CheckedChanged;
			CheckBox val = _R62CB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_R62CB = value;
			val = _R62CB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox R50CB
	{
		[CompilerGenerated]
		get
		{
			return _R50CB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = E38CB_CheckedChanged;
			CheckBox val = _R50CB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_R50CB = value;
			val = _R50CB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox R38CB
	{
		[CompilerGenerated]
		get
		{
			return _R38CB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = E38CB_CheckedChanged;
			CheckBox val = _R38CB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_R38CB = value;
			val = _R38CB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
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

	internal virtual CheckBox EAllCB
	{
		[CompilerGenerated]
		get
		{
			return _EAllCB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = E38CB_CheckedChanged;
			CheckBox val = _EAllCB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_EAllCB = value;
			val = _EAllCB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox RAllCB
	{
		[CompilerGenerated]
		get
		{
			return _RAllCB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = E38CB_CheckedChanged;
			CheckBox val = _RAllCB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_RAllCB = value;
			val = _RAllCB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("ChartToDTP")]
	internal virtual DateTimePicker ChartToDTP
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("ChartFromDTP")]
	internal virtual DateTimePicker ChartFromDTP
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

	[field: AccessedThroughProperty("Label6")]
	internal virtual Label Label6
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

	[field: AccessedThroughProperty("PriceBarsNUD")]
	internal virtual NumericUpDown PriceBarsNUD
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

	public FibFinderForm()
	{
		//IL_00c5: Unknown result type (might be due to invalid IL or missing references)
		//IL_00cf: Expected O, but got Unknown
		((Form)this).Closing += FibFinderForm_Closing;
		((Form)this).Load += FibFinderForm_Load;
		((Form)this).Activated += FibFinderForm_Activated;
		fSYMBOL = 0;
		fLASTCLOSE = 1;
		fTYPE = 2;
		fSTART = 3;
		fEND = 4;
		fREDATE = 5;
		fVALUE = 6;
		fPATH = 7;
		tCOLUMNCOUNT = checked(fPATH + 1);
		StopPressed = false;
		iRow = 0;
		Crosshair = false;
		CrosshairPen = null;
		FFDateLookBack = 180L;
		lsFFDateLookBack = 180L;
		LockFlag = false;
		Busy = false;
		CurrentAnnotation = new CalloutAnnotation();
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
		//IL_168a: Unknown result type (might be due to invalid IL or missing references)
		ChartArea val = new ChartArea();
		Series val2 = new Series();
		Series val3 = new Series();
		Series val4 = new Series();
		ToDatePicker = new DateTimePicker();
		FromDatePicker = new DateTimePicker();
		FilenameLabel = new Label();
		ErrorLabel = new Label();
		MonthlyRadioButton = new RadioButton();
		WeeklyRadioButton = new RadioButton();
		DailyRadioButton = new RadioButton();
		AllPortfoliosButton = new Button();
		HelpButton1 = new Button();
		ProgressBar1 = new ProgressBar();
		Label1 = new Label();
		SymbolTextBox = new TextBox();
		ClipboardButton = new Button();
		StartButton = new Button();
		StopButton = new Button();
		DoneButton = new Button();
		Label3 = new Label();
		Label2 = new Label();
		DataGridView1 = new DataGridView();
		Panel1 = new Panel();
		Label8 = new Label();
		PriceBarsNUD = new NumericUpDown();
		Label7 = new Label();
		Label6 = new Label();
		EAllCB = new CheckBox();
		Label5 = new Label();
		RAllCB = new CheckBox();
		ENUD = new NumericUpDown();
		Label4 = new Label();
		RNUD = new NumericUpDown();
		E62CB = new CheckBox();
		E50CB = new CheckBox();
		E38CB = new CheckBox();
		R62CB = new CheckBox();
		R50CB = new CheckBox();
		R38CB = new CheckBox();
		Chart1 = new Chart();
		ChartToDTP = new DateTimePicker();
		ChartFromDTP = new DateTimePicker();
		Label9 = new Label();
		((ISupportInitialize)DataGridView1).BeginInit();
		((Control)Panel1).SuspendLayout();
		((ISupportInitialize)PriceBarsNUD).BeginInit();
		((ISupportInitialize)ENUD).BeginInit();
		((ISupportInitialize)RNUD).BeginInit();
		((ISupportInitialize)Chart1).BeginInit();
		((Control)this).SuspendLayout();
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(705, 536);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(120, 20);
		((Control)ToDatePicker).TabIndex = 21;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(705, 510);
		((Control)FromDatePicker).Name = "FromDatePicker";
		FromDatePicker.ShowUpDown = true;
		((Control)FromDatePicker).Size = new Size(120, 20);
		((Control)FromDatePicker).TabIndex = 17;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FilenameLabel).Anchor = (AnchorStyles)14;
		FilenameLabel.BorderStyle = (BorderStyle)2;
		((Control)FilenameLabel).Location = new Point(1, 486);
		((Control)FilenameLabel).Name = "FilenameLabel";
		((Control)FilenameLabel).Size = new Size(154, 22);
		((Control)FilenameLabel).TabIndex = 4;
		((Control)ErrorLabel).Anchor = (AnchorStyles)14;
		ErrorLabel.BorderStyle = (BorderStyle)2;
		((Control)ErrorLabel).Location = new Point(1, 511);
		((Control)ErrorLabel).Name = "ErrorLabel";
		((Control)ErrorLabel).Size = new Size(154, 48);
		((Control)ErrorLabel).TabIndex = 9;
		((Control)MonthlyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)MonthlyRadioButton).AutoSize = true;
		((Control)MonthlyRadioButton).Location = new Point(161, 526);
		((Control)MonthlyRadioButton).Name = "MonthlyRadioButton";
		((Control)MonthlyRadioButton).Size = new Size(62, 17);
		((Control)MonthlyRadioButton).TabIndex = 12;
		((Control)MonthlyRadioButton).Tag = "Monthly";
		((ButtonBase)MonthlyRadioButton).Text = "&Monthly";
		((ButtonBase)MonthlyRadioButton).UseVisualStyleBackColor = true;
		((Control)WeeklyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)WeeklyRadioButton).AutoSize = true;
		((Control)WeeklyRadioButton).Location = new Point(161, 511);
		((Control)WeeklyRadioButton).Name = "WeeklyRadioButton";
		((Control)WeeklyRadioButton).Size = new Size(61, 17);
		((Control)WeeklyRadioButton).TabIndex = 11;
		((Control)WeeklyRadioButton).Tag = "Weekly";
		((ButtonBase)WeeklyRadioButton).Text = "&Weekly";
		((ButtonBase)WeeklyRadioButton).UseVisualStyleBackColor = true;
		((Control)DailyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)DailyRadioButton).AutoSize = true;
		DailyRadioButton.Checked = true;
		((Control)DailyRadioButton).Location = new Point(161, 496);
		((Control)DailyRadioButton).Name = "DailyRadioButton";
		((Control)DailyRadioButton).Size = new Size(48, 17);
		((Control)DailyRadioButton).TabIndex = 10;
		DailyRadioButton.TabStop = true;
		((Control)DailyRadioButton).Tag = "Daily";
		((ButtonBase)DailyRadioButton).Text = "Dail&y";
		((ButtonBase)DailyRadioButton).UseVisualStyleBackColor = true;
		((Control)AllPortfoliosButton).Anchor = (AnchorStyles)10;
		((Control)AllPortfoliosButton).Location = new Point(837, 525);
		((Control)AllPortfoliosButton).Name = "AllPortfoliosButton";
		((Control)AllPortfoliosButton).Size = new Size(81, 23);
		((Control)AllPortfoliosButton).TabIndex = 1;
		((ButtonBase)AllPortfoliosButton).Text = "&All Portfolios";
		((ButtonBase)AllPortfoliosButton).UseVisualStyleBackColor = true;
		((Control)HelpButton1).Anchor = (AnchorStyles)10;
		((Control)HelpButton1).Location = new Point(973, 499);
		((Control)HelpButton1).Name = "HelpButton1";
		((Control)HelpButton1).Size = new Size(43, 23);
		((Control)HelpButton1).TabIndex = 0;
		((ButtonBase)HelpButton1).Text = "&Help";
		((ButtonBase)HelpButton1).UseVisualStyleBackColor = true;
		((Control)ProgressBar1).Anchor = (AnchorStyles)10;
		((Control)ProgressBar1).ForeColor = Color.Green;
		((Control)ProgressBar1).Location = new Point(626, 486);
		((Control)ProgressBar1).Name = "ProgressBar1";
		((Control)ProgressBar1).Size = new Size(199, 18);
		((Control)ProgressBar1).TabIndex = 15;
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(577, 538);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(44, 13);
		((Control)Label1).TabIndex = 18;
		Label1.Text = "S&ymbol:";
		((Control)SymbolTextBox).Anchor = (AnchorStyles)10;
		((Control)SymbolTextBox).Location = new Point(626, 535);
		((Control)SymbolTextBox).Name = "SymbolTextBox";
		((Control)SymbolTextBox).Size = new Size(43, 20);
		((Control)SymbolTextBox).TabIndex = 19;
		((Control)ClipboardButton).Anchor = (AnchorStyles)10;
		((Control)ClipboardButton).Enabled = false;
		((Control)ClipboardButton).Location = new Point(837, 497);
		((Control)ClipboardButton).Name = "ClipboardButton";
		((Control)ClipboardButton).Size = new Size(81, 23);
		((Control)ClipboardButton).TabIndex = 22;
		((ButtonBase)ClipboardButton).Text = "Clip&board";
		((ButtonBase)ClipboardButton).UseVisualStyleBackColor = true;
		((Control)StartButton).Anchor = (AnchorStyles)10;
		((Control)StartButton).Enabled = false;
		((Control)StartButton).Location = new Point(924, 525);
		((Control)StartButton).Name = "StartButton";
		((Control)StartButton).Size = new Size(43, 23);
		((Control)StartButton).TabIndex = 0;
		((ButtonBase)StartButton).Text = "St&art";
		((ButtonBase)StartButton).UseVisualStyleBackColor = true;
		((Control)StopButton).Anchor = (AnchorStyles)10;
		((Control)StopButton).Enabled = false;
		((Control)StopButton).Location = new Point(924, 498);
		((Control)StopButton).Name = "StopButton";
		((Control)StopButton).Size = new Size(43, 23);
		((Control)StopButton).TabIndex = 23;
		((ButtonBase)StopButton).Text = "St&op";
		((ButtonBase)StopButton).UseVisualStyleBackColor = true;
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(973, 525);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(43, 23);
		((Control)DoneButton).TabIndex = 1;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)Label3).Anchor = (AnchorStyles)10;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(676, 537);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(23, 13);
		((Control)Label3).TabIndex = 20;
		Label3.Text = "&To:";
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(666, 511);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(33, 13);
		((Control)Label2).TabIndex = 16;
		Label2.Text = "&From:";
		DataGridView1.AllowUserToAddRows = false;
		DataGridView1.AllowUserToDeleteRows = false;
		DataGridView1.AllowUserToResizeColumns = false;
		DataGridView1.AllowUserToResizeRows = false;
		((Control)DataGridView1).Anchor = (AnchorStyles)7;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)10;
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
		((Control)DataGridView1).Size = new Size(561, 468);
		((Control)DataGridView1).TabIndex = 2;
		((Control)Panel1).Anchor = (AnchorStyles)10;
		Panel1.BorderStyle = (BorderStyle)2;
		((Control)Panel1).Controls.Add((Control)(object)Label8);
		((Control)Panel1).Controls.Add((Control)(object)PriceBarsNUD);
		((Control)Panel1).Controls.Add((Control)(object)Label7);
		((Control)Panel1).Controls.Add((Control)(object)Label6);
		((Control)Panel1).Controls.Add((Control)(object)EAllCB);
		((Control)Panel1).Controls.Add((Control)(object)Label5);
		((Control)Panel1).Controls.Add((Control)(object)RAllCB);
		((Control)Panel1).Controls.Add((Control)(object)ENUD);
		((Control)Panel1).Controls.Add((Control)(object)Label4);
		((Control)Panel1).Controls.Add((Control)(object)RNUD);
		((Control)Panel1).Controls.Add((Control)(object)E62CB);
		((Control)Panel1).Controls.Add((Control)(object)E50CB);
		((Control)Panel1).Controls.Add((Control)(object)E38CB);
		((Control)Panel1).Controls.Add((Control)(object)R62CB);
		((Control)Panel1).Controls.Add((Control)(object)R50CB);
		((Control)Panel1).Controls.Add((Control)(object)R38CB);
		((Control)Panel1).Location = new Point(229, 486);
		((Control)Panel1).Name = "Panel1";
		((Control)Panel1).Size = new Size(344, 73);
		((Control)Panel1).TabIndex = 13;
		Label8.AutoSize = true;
		((Control)Label8).Location = new Point(108, 48);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(170, 13);
		((Control)Label8).TabIndex = 14;
		Label8.Text = "&Minimum price bars between turns:";
		((Control)PriceBarsNUD).Location = new Point(284, 46);
		PriceBarsNUD.Maximum = new decimal(new int[4] { 20, 0, 0, 0 });
		PriceBarsNUD.Minimum = new decimal(new int[4] { 3, 0, 0, 0 });
		((Control)PriceBarsNUD).Name = "PriceBarsNUD";
		((UpDownBase)PriceBarsNUD).ReadOnly = true;
		((Control)PriceBarsNUD).Size = new Size(50, 20);
		((Control)PriceBarsNUD).TabIndex = 15;
		((UpDownBase)PriceBarsNUD).TextAlign = (HorizontalAlignment)2;
		PriceBarsNUD.Value = new decimal(new int[4] { 5, 0, 0, 0 });
		Label7.AutoSize = true;
		((Control)Label7).Location = new Point(2, 29);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(56, 13);
		((Control)Label7).TabIndex = 7;
		Label7.Text = "&Extension:";
		Label6.AutoSize = true;
		((Control)Label6).Location = new Point(10, 13);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(48, 13);
		((Control)Label6).TabIndex = 0;
		Label6.Text = "&Retrace:";
		((ButtonBase)EAllCB).AutoSize = true;
		((Control)EAllCB).Location = new Point(220, 27);
		((Control)EAllCB).Name = "EAllCB";
		((Control)EAllCB).Size = new Size(37, 17);
		((Control)EAllCB).TabIndex = 11;
		((ButtonBase)EAllCB).Text = "&All";
		((ButtonBase)EAllCB).UseVisualStyleBackColor = true;
		Label5.AutoSize = true;
		((Control)Label5).Location = new Point(269, 29);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(21, 13);
		((Control)Label5).TabIndex = 12;
		Label5.Text = "+/-";
		((ButtonBase)RAllCB).AutoSize = true;
		((Control)RAllCB).Location = new Point(220, 10);
		((Control)RAllCB).Name = "RAllCB";
		((Control)RAllCB).Size = new Size(37, 17);
		((Control)RAllCB).TabIndex = 4;
		((ButtonBase)RAllCB).Text = "&All";
		((ButtonBase)RAllCB).UseVisualStyleBackColor = true;
		((Control)ENUD).Location = new Point(296, 25);
		ENUD.Maximum = new decimal(new int[4] { 9, 0, 0, 0 });
		ENUD.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)ENUD).Name = "ENUD";
		((UpDownBase)ENUD).ReadOnly = true;
		((Control)ENUD).Size = new Size(38, 20);
		((Control)ENUD).TabIndex = 13;
		((UpDownBase)ENUD).TextAlign = (HorizontalAlignment)2;
		ENUD.Value = new decimal(new int[4] { 1, 0, 0, 0 });
		Label4.AutoSize = true;
		((Control)Label4).Location = new Point(269, 11);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(21, 13);
		((Control)Label4).TabIndex = 5;
		Label4.Text = "+/-";
		((Control)RNUD).Location = new Point(296, 6);
		RNUD.Maximum = new decimal(new int[4] { 9, 0, 0, 0 });
		RNUD.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)RNUD).Name = "RNUD";
		((UpDownBase)RNUD).ReadOnly = true;
		((Control)RNUD).Size = new Size(38, 20);
		((Control)RNUD).TabIndex = 6;
		((UpDownBase)RNUD).TextAlign = (HorizontalAlignment)2;
		RNUD.Value = new decimal(new int[4] { 1, 0, 0, 0 });
		((ButtonBase)E62CB).AutoSize = true;
		((Control)E62CB).Location = new Point(168, 27);
		((Control)E62CB).Name = "E62CB";
		((Control)E62CB).Size = new Size(46, 17);
		((Control)E62CB).TabIndex = 10;
		((ButtonBase)E62CB).Text = "62%";
		((ButtonBase)E62CB).UseVisualStyleBackColor = true;
		((ButtonBase)E50CB).AutoSize = true;
		((Control)E50CB).Location = new Point(116, 27);
		((Control)E50CB).Name = "E50CB";
		((Control)E50CB).Size = new Size(46, 17);
		((Control)E50CB).TabIndex = 9;
		((ButtonBase)E50CB).Text = "50%";
		((ButtonBase)E50CB).UseVisualStyleBackColor = true;
		((ButtonBase)E38CB).AutoSize = true;
		((Control)E38CB).Location = new Point(64, 27);
		((Control)E38CB).Name = "E38CB";
		((Control)E38CB).Size = new Size(46, 17);
		((Control)E38CB).TabIndex = 8;
		((ButtonBase)E38CB).Text = "38%";
		((ButtonBase)E38CB).UseVisualStyleBackColor = true;
		((ButtonBase)R62CB).AutoSize = true;
		((Control)R62CB).Location = new Point(168, 10);
		((Control)R62CB).Name = "R62CB";
		((Control)R62CB).Size = new Size(46, 17);
		((Control)R62CB).TabIndex = 3;
		((ButtonBase)R62CB).Text = "62%";
		((ButtonBase)R62CB).UseVisualStyleBackColor = true;
		((ButtonBase)R50CB).AutoSize = true;
		((Control)R50CB).Location = new Point(116, 10);
		((Control)R50CB).Name = "R50CB";
		((Control)R50CB).Size = new Size(46, 17);
		((Control)R50CB).TabIndex = 2;
		((ButtonBase)R50CB).Text = "50%";
		((ButtonBase)R50CB).UseVisualStyleBackColor = true;
		((ButtonBase)R38CB).AutoSize = true;
		((Control)R38CB).Location = new Point(64, 10);
		((Control)R38CB).Name = "R38CB";
		((Control)R38CB).Size = new Size(46, 17);
		((Control)R38CB).TabIndex = 1;
		((ButtonBase)R38CB).Text = "38%";
		((ButtonBase)R38CB).UseVisualStyleBackColor = true;
		((Control)Chart1).Anchor = (AnchorStyles)15;
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
		((Control)Chart1).Location = new Point(582, 12);
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
		Chart1.Size = new Size(434, 468);
		((Control)Chart1).TabIndex = 3;
		((Control)Chart1).Text = "Chart1";
		((Control)ChartToDTP).Anchor = (AnchorStyles)10;
		ChartToDTP.CustomFormat = "yyyy/MM/dd";
		ChartToDTP.Format = (DateTimePickerFormat)8;
		((Control)ChartToDTP).Location = new Point(-6, 529);
		((Control)ChartToDTP).Name = "ChartToDTP";
		ChartToDTP.ShowUpDown = true;
		((Control)ChartToDTP).Size = new Size(85, 20);
		((Control)ChartToDTP).TabIndex = 8;
		((Control)ChartToDTP).TabStop = false;
		ChartToDTP.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)ChartToDTP).Visible = false;
		((Control)ChartFromDTP).Anchor = (AnchorStyles)10;
		ChartFromDTP.CustomFormat = "yyyy/MM/dd";
		ChartFromDTP.Format = (DateTimePickerFormat)8;
		((Control)ChartFromDTP).Location = new Point(-6, 505);
		((Control)ChartFromDTP).Name = "ChartFromDTP";
		ChartFromDTP.ShowUpDown = true;
		((Control)ChartFromDTP).Size = new Size(86, 20);
		((Control)ChartFromDTP).TabIndex = 7;
		((Control)ChartFromDTP).TabStop = false;
		ChartFromDTP.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)ChartFromDTP).Visible = false;
		((Control)Label9).Anchor = (AnchorStyles)10;
		Label9.AutoSize = true;
		((Control)Label9).Location = new Point(577, 487);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(48, 13);
		((Control)Label9).TabIndex = 14;
		Label9.Text = "Loading:";
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(1016, 560);
		((Control)this).Controls.Add((Control)(object)Label9);
		((Control)this).Controls.Add((Control)(object)ChartToDTP);
		((Control)this).Controls.Add((Control)(object)ChartFromDTP);
		((Control)this).Controls.Add((Control)(object)Chart1);
		((Control)this).Controls.Add((Control)(object)Panel1);
		((Control)this).Controls.Add((Control)(object)ToDatePicker);
		((Control)this).Controls.Add((Control)(object)FromDatePicker);
		((Control)this).Controls.Add((Control)(object)FilenameLabel);
		((Control)this).Controls.Add((Control)(object)ErrorLabel);
		((Control)this).Controls.Add((Control)(object)MonthlyRadioButton);
		((Control)this).Controls.Add((Control)(object)WeeklyRadioButton);
		((Control)this).Controls.Add((Control)(object)DailyRadioButton);
		((Control)this).Controls.Add((Control)(object)AllPortfoliosButton);
		((Control)this).Controls.Add((Control)(object)HelpButton1);
		((Control)this).Controls.Add((Control)(object)ProgressBar1);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)SymbolTextBox);
		((Control)this).Controls.Add((Control)(object)ClipboardButton);
		((Control)this).Controls.Add((Control)(object)StartButton);
		((Control)this).Controls.Add((Control)(object)StopButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)DataGridView1);
		((Control)this).Name = "FibFinderForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Fibonacci Finder";
		((ISupportInitialize)DataGridView1).EndInit();
		((Control)Panel1).ResumeLayout(false);
		((Control)Panel1).PerformLayout();
		((ISupportInitialize)PriceBarsNUD).EndInit();
		((ISupportInitialize)ENUD).EndInit();
		((ISupportInitialize)RNUD).EndInit();
		((ISupportInitialize)Chart1).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void FibFinderForm_Closing(object sender, CancelEventArgs e)
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
		try
		{
			if (lsE38 != E38CB.Checked)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "E38", (object)E38CB.Checked);
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
			if (lsE50 != E50CB.Checked)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "E50", (object)E50CB.Checked);
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
			if (lsE62 != E62CB.Checked)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "E62", (object)E62CB.Checked);
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
			if (lsEAll != EAllCB.Checked)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "EAll", (object)EAllCB.Checked);
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
			if (decimal.Compare(new decimal(lsENUD), ENUD.Value) != 0)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "ENUD", (object)ENUD.Value);
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
			if (lsR38 != R38CB.Checked)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "R38", (object)R38CB.Checked);
			}
		}
		catch (Exception ex13)
		{
			ProjectData.SetProjectError(ex13);
			Exception ex14 = ex13;
			ProjectData.ClearProjectError();
		}
		try
		{
			if (lsR50 != R50CB.Checked)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "R50", (object)R50CB.Checked);
			}
		}
		catch (Exception ex15)
		{
			ProjectData.SetProjectError(ex15);
			Exception ex16 = ex15;
			ProjectData.ClearProjectError();
		}
		try
		{
			if (lsR62 != R62CB.Checked)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "R62", (object)R62CB.Checked);
			}
		}
		catch (Exception ex17)
		{
			ProjectData.SetProjectError(ex17);
			Exception ex18 = ex17;
			ProjectData.ClearProjectError();
		}
		try
		{
			if (lsRAll != RAllCB.Checked)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "RAll", (object)RAllCB.Checked);
			}
		}
		catch (Exception ex19)
		{
			ProjectData.SetProjectError(ex19);
			Exception ex20 = ex19;
			ProjectData.ClearProjectError();
		}
		try
		{
			if (decimal.Compare(new decimal(lsRNUD), RNUD.Value) != 0)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "RNUD", (object)RNUD.Value);
			}
		}
		catch (Exception ex21)
		{
			ProjectData.SetProjectError(ex21);
			Exception ex22 = ex21;
			ProjectData.ClearProjectError();
		}
		try
		{
			if (decimal.Compare(new decimal(lsPriceBarsNUD), PriceBarsNUD.Value) != 0)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "PriceBarsNUD", (object)PriceBarsNUD.Value);
			}
		}
		catch (Exception ex23)
		{
			ProjectData.SetProjectError(ex23);
			Exception ex24 = ex23;
			ProjectData.ClearProjectError();
		}
		if (GlobalForm.IntradayData)
		{
			if (GlobalForm.ChartEndIndex == 0)
			{
				FFDateLookBack = lsFFDateLookBack;
			}
			else
			{
				FFDateLookBack = checked(GlobalForm.ChartEndIndex - GlobalForm.ChartStartIndex);
			}
			if (GlobalForm.ChartEndIndex < GlobalForm.ChartStartIndex)
			{
				FFDateLookBack = 1L;
			}
		}
		else
		{
			FFDateLookBack = DateAndTime.DateDiff((DateInterval)4, FromDatePicker.Value, ToDatePicker.Value, (FirstDayOfWeek)1, (FirstWeekOfYear)1);
		}
		try
		{
			if (FFDateLookBack != lsFFDateLookBack)
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "DateLookback", (object)FFDateLookBack);
			}
		}
		catch (Exception ex25)
		{
			ProjectData.SetProjectError(ex25);
			Exception ex26 = ex25;
			ProjectData.ClearProjectError();
		}
		MySettingsProperty.Settings.FibFinderLocation = ((Form)this).Location;
		MySettingsProperty.Settings.FibFinderSize = ((Form)this).Size;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
		LockFlag = false;
	}

	private void FibFinderForm_Load(object sender, EventArgs e)
	{
		//IL_0051: Unknown result type (might be due to invalid IL or missing references)
		//IL_0056: Unknown result type (might be due to invalid IL or missing references)
		//IL_0061: Unknown result type (might be due to invalid IL or missing references)
		//IL_006c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0077: Unknown result type (might be due to invalid IL or missing references)
		//IL_007e: Unknown result type (might be due to invalid IL or missing references)
		//IL_008f: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d3: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e4: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f5: Unknown result type (might be due to invalid IL or missing references)
		//IL_0106: Unknown result type (might be due to invalid IL or missing references)
		//IL_0117: Unknown result type (might be due to invalid IL or missing references)
		//IL_0128: Unknown result type (might be due to invalid IL or missing references)
		//IL_0139: Unknown result type (might be due to invalid IL or missing references)
		//IL_014a: Unknown result type (might be due to invalid IL or missing references)
		//IL_015b: Unknown result type (might be due to invalid IL or missing references)
		//IL_016c: Unknown result type (might be due to invalid IL or missing references)
		//IL_017d: Unknown result type (might be due to invalid IL or missing references)
		//IL_018e: Unknown result type (might be due to invalid IL or missing references)
		//IL_019f: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b0: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c1: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d2: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e3: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f4: Unknown result type (might be due to invalid IL or missing references)
		//IL_0205: Unknown result type (might be due to invalid IL or missing references)
		//IL_002a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0034: Expected O, but got Unknown
		//IL_071d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0724: Expected O, but got Unknown
		//IL_072f: Unknown result type (might be due to invalid IL or missing references)
		LockFlag = false;
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.FibFinderLocation, MySettingsProperty.Settings.FibFinderSize);
		if (CurrentAnnotation == null)
		{
			CurrentAnnotation = new CalloutAnnotation();
		}
		((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)CurrentAnnotation);
		Busy = false;
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)AllPortfoliosButton, "Search all portfolios.");
		val.SetToolTip((Control)(object)ClipboardButton, "Copy highlighted rows to the clipboard.");
		val.SetToolTip((Control)(object)Chart1, "Click on a grid row to plot the extension or retrace.");
		val.SetToolTip((Control)(object)DailyRadioButton, "Search using the daily scale.");
		val.SetToolTip((Control)(object)DataGridView1, "Highlight rows to copy to the clipboard.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)E62CB, "Find 62% extensions.");
		val.SetToolTip((Control)(object)E50CB, "Find 50% extensions.");
		val.SetToolTip((Control)(object)E38CB, "Find 38% extensions.");
		val.SetToolTip((Control)(object)EAllCB, "Find all  extensions.");
		val.SetToolTip((Control)(object)ENUD, "Find a Fibonacci retrace or extension plus or minus (in percentage points) the value shown.");
		val.SetToolTip((Control)(object)FromDatePicker, "Enter the starting date to search.");
		val.SetToolTip((Control)(object)HelpButton1, "Get help with this form.");
		val.SetToolTip((Control)(object)MonthlyRadioButton, "Search using the monthly scale.");
		val.SetToolTip((Control)(object)PriceBarsNUD, "Default is 5. Distance (price bars) between peaks/valleys. 3=minor (narrow) turns, 10+=major (wide) turns.");
		val.SetToolTip((Control)(object)RNUD, "Find a Fibonacci retrace or extension plus or minus (in percentage points) the value shown.");
		val.SetToolTip((Control)(object)StartButton, "Start searching.");
		val.SetToolTip((Control)(object)StopButton, "Halt the search for Fibonacci retraces or extension.");
		val.SetToolTip((Control)(object)SymbolTextBox, "Enter a symbol to search.");
		val.SetToolTip((Control)(object)ToDatePicker, "Enter the ending date to search.");
		val.SetToolTip((Control)(object)RAllCB, "Find all retraces.");
		val.SetToolTip((Control)(object)R62CB, "Find 62% retraces.");
		val.SetToolTip((Control)(object)R50CB, "Find 50% retraces.");
		val.SetToolTip((Control)(object)R38CB, "Find 38% retraces.");
		val.SetToolTip((Control)(object)WeeklyRadioButton, "Search using the weekly scale.");
		GlobalForm.FirstPoint = default(Point);
		GlobalForm.LinesList.RemoveAll(StubBoolean);
		ProgressBar1.Value = 0;
		SymbolTextBox.Text = "";
		StopPressed = false;
		FileNameInUse = "";
		try
		{
			E38CB.Checked = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "E38", (object)false));
			lsE38 = E38CB.Checked;
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		try
		{
			E50CB.Checked = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "E50", (object)false));
			lsE50 = E50CB.Checked;
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			ProjectData.ClearProjectError();
		}
		try
		{
			E62CB.Checked = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "E62", (object)false));
			lsE62 = E62CB.Checked;
		}
		catch (Exception ex5)
		{
			ProjectData.SetProjectError(ex5);
			Exception ex6 = ex5;
			ProjectData.ClearProjectError();
		}
		try
		{
			EAllCB.Checked = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "EAll", (object)false));
			lsEAll = EAllCB.Checked;
		}
		catch (Exception ex7)
		{
			ProjectData.SetProjectError(ex7);
			Exception ex8 = ex7;
			ProjectData.ClearProjectError();
		}
		try
		{
			R38CB.Checked = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "R38", (object)false));
			lsR38 = R38CB.Checked;
		}
		catch (Exception ex9)
		{
			ProjectData.SetProjectError(ex9);
			Exception ex10 = ex9;
			ProjectData.ClearProjectError();
		}
		try
		{
			R50CB.Checked = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "R50", (object)false));
			lsR50 = R50CB.Checked;
		}
		catch (Exception ex11)
		{
			ProjectData.SetProjectError(ex11);
			Exception ex12 = ex11;
			ProjectData.ClearProjectError();
		}
		try
		{
			R62CB.Checked = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "R62", (object)false));
			lsR62 = R62CB.Checked;
		}
		catch (Exception ex13)
		{
			ProjectData.SetProjectError(ex13);
			Exception ex14 = ex13;
			ProjectData.ClearProjectError();
		}
		try
		{
			RAllCB.Checked = Conversions.ToBoolean(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "RAll", (object)false));
			lsRAll = RAllCB.Checked;
		}
		catch (Exception ex15)
		{
			ProjectData.SetProjectError(ex15);
			Exception ex16 = ex15;
			ProjectData.ClearProjectError();
		}
		try
		{
			int value = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "ENUD", (object)1));
			if ((decimal.Compare(new decimal(value), ENUD.Minimum) < 0) | (decimal.Compare(new decimal(value), ENUD.Maximum) > 0))
			{
				ENUD.Value = ENUD.Minimum;
			}
			else
			{
				ENUD.Value = new decimal(value);
			}
			lsENUD = Convert.ToInt32(ENUD.Value);
		}
		catch (Exception ex17)
		{
			ProjectData.SetProjectError(ex17);
			Exception ex18 = ex17;
			ProjectData.ClearProjectError();
		}
		try
		{
			int value = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "RNUD", (object)1));
			if ((decimal.Compare(new decimal(value), RNUD.Minimum) < 0) | (decimal.Compare(new decimal(value), RNUD.Maximum) > 0))
			{
				RNUD.Value = RNUD.Minimum;
			}
			else
			{
				RNUD.Value = new decimal(value);
			}
			lsRNUD = Convert.ToInt32(RNUD.Value);
		}
		catch (Exception ex19)
		{
			ProjectData.SetProjectError(ex19);
			Exception ex20 = ex19;
			ProjectData.ClearProjectError();
		}
		try
		{
			int value = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "PriceBarsNUD", (object)5));
			if ((decimal.Compare(new decimal(value), PriceBarsNUD.Minimum) < 0) | (decimal.Compare(new decimal(value), PriceBarsNUD.Maximum) > 0))
			{
				PriceBarsNUD.Value = 5m;
			}
			else
			{
				PriceBarsNUD.Value = new decimal(value);
			}
			lsPriceBarsNUD = Convert.ToInt32(PriceBarsNUD.Value);
		}
		catch (Exception ex21)
		{
			ProjectData.SetProjectError(ex21);
			Exception ex22 = ex21;
			ProjectData.ClearProjectError();
		}
		bool flag = false;
		foreach (Control control in ((Control)Panel1).Controls)
		{
			Control val2 = control;
			if (val2 is CheckBox && ((CheckBox)val2).Checked)
			{
				flag = true;
				break;
			}
		}
		if (!flag)
		{
			RAllCB.Checked = true;
		}
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
		EnableDisable(EnableFlag: true);
		GlobalForm.SelectChartType(Chart1);
		((Control)DailyRadioButton).Tag = 0;
		((Control)WeeklyRadioButton).Tag = 1;
		((Control)MonthlyRadioButton).Tag = 2;
	}

	private void FibFinderForm_Activated(object sender, EventArgs e)
	{
		if (LockFlag)
		{
			return;
		}
		LockFlag = true;
		((Control)this).Refresh();
		try
		{
			FFDateLookBack = Conversions.ToInteger(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\FibForm", "DateLookback", (object)180));
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		if (FFDateLookBack == 0L)
		{
			FFDateLookBack = 180L;
		}
		lsFFDateLookBack = FFDateLookBack;
		checked
		{
			if (MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count >= 1)
			{
				string text = MyProject.Forms.Mainform.ListBox1.SelectedItems[0].ToString();
				FilenameLabel.Text = text;
				((Control)FilenameLabel).Refresh();
				bool enabled = ((Control)DoneButton).Enabled;
				if (enabled)
				{
					EnableDisable(EnableFlag: false);
				}
				ProgressBar ProgBar = ProgressBar1;
				Label ErrorLabel = null;
				bool num = GlobalForm.LoadFile(text, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
				ProgressBar1 = ProgBar;
				if (!num)
				{
					GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
					GlobalForm.SelectChartType(Chart1);
					if (GlobalForm.IntradayData)
					{
						if ((DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MaxDate) <= 0))
						{
							FromDatePicker.Value = GlobalForm.nDT[0, (int)(GlobalForm.HLCRange - FFDateLookBack)];
						}
					}
					else
					{
						FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)(-1 * FFDateLookBack), DateAndTime.Now);
					}
					FileNameInUse = text;
				}
				else
				{
					FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)(-1 * FFDateLookBack), DateAndTime.Now);
					FileNameInUse = "";
				}
				if (enabled)
				{
					EnableDisable(EnableFlag: true);
				}
				ToDatePicker.Value = DateAndTime.Now;
			}
			DataGridView1.ClipboardCopyMode = (DataGridViewClipboardCopyMode)2;
			BuildGridHeader();
		}
	}

	private void AllPortfoliosButton_Click(object sender, EventArgs e)
	{
		//IL_014e: Unknown result type (might be due to invalid IL or missing references)
		if (!TestCheckBoxes(Quiet: true, "ER"))
		{
			return;
		}
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
						ErrorLabel.Text = "Errors are on the clipboard.";
					}
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					ProjectData.ClearProjectError();
				}
				DataGridView1_SelectionChanged(RuntimeHelpers.GetObjectValue(sender), e);
				MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				ProgressBar1.Value = 0;
			}
			else
			{
				StartButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			}
		}
	}

	private void BuildGrid(string Filename)
	{
		DataGridView1.RowHeadersVisible = false;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)1;
		GlobalForm.SetupDateIndexes(FromDatePicker.Value, ToDatePicker.Value);
		FindPatterns.FindAllBottoms(Convert.ToInt32(PriceBarsNUD.Value));
		int num = Information.UBound((Array)FindPatterns.ArrayBottoms, 1);
		if (num <= 1)
		{
			return;
		}
		FindPatterns.FindAllTops(Convert.ToInt32(PriceBarsNUD.Value));
		int num2 = Information.UBound((Array)FindPatterns.ArrayTops, 1);
		if (num2 <= 1)
		{
			return;
		}
		checked
		{
			int num3 = num2 - 1;
			for (int i = 1; i <= num3; i++)
			{
				int num4 = num - 1;
				for (int j = 1; j <= num4; j++)
				{
					if ((FindPatterns.ArrayTops[i] < FindPatterns.ArrayBottoms[j]) & (FindPatterns.ArrayBottoms[j] < FindPatterns.ArrayTops[i + 1]) & (FindPatterns.ArrayBottoms[j + 1] > FindPatterns.ArrayTops[i + 1]) & (FindPatterns.ArrayTops[i] > FindPatterns.ArrayBottoms[j - 1]))
					{
						decimal num5 = decimal.Subtract(GlobalForm.nHLC[1, FindPatterns.ArrayTops[i]], GlobalForm.nHLC[2, FindPatterns.ArrayBottoms[j]]);
						if (decimal.Compare(num5, 0m) <= 0)
						{
							continue;
						}
						if (decimal.Compare(GlobalForm.nHLC[1, FindPatterns.ArrayTops[i + 1]], GlobalForm.nHLC[1, FindPatterns.ArrayTops[i]]) > 0)
						{
							if (TestCheckBoxes(Quiet: true, "E"))
							{
								decimal num6 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, FindPatterns.ArrayTops[i + 1]], GlobalForm.nHLC[1, FindPatterns.ArrayTops[i]]), num5);
								if (CheckValues("E", num6))
								{
									DataGridView1.Rows.Add();
									DataGridView1.Rows[iRow].Cells[fSYMBOL].Value = Filename;
									DataGridView1.Rows[iRow].Cells[fLASTCLOSE].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]);
									DataGridView1.Rows[iRow].Cells[fTYPE].Value = "+Extension";
									DataGridView1.Rows[iRow].Cells[fSTART].Value = Strings.Format((object)GlobalForm.nDT[0, FindPatterns.ArrayTops[i]], GlobalForm.UserDate);
									DataGridView1.Rows[iRow].Cells[fEND].Value = Strings.Format((object)GlobalForm.nDT[0, FindPatterns.ArrayBottoms[j]], GlobalForm.UserDate);
									DataGridView1.Rows[iRow].Cells[fREDATE].Value = Strings.Format((object)GlobalForm.nDT[0, FindPatterns.ArrayTops[i + 1]], GlobalForm.UserDate);
									DataGridView1.Rows[iRow].Cells[fVALUE].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, num6));
									DataGridView1.Rows[iRow].Cells[fPATH].Value = GlobalForm.OpenPath;
									iRow++;
								}
							}
						}
						else if (TestCheckBoxes(Quiet: true, "R"))
						{
							decimal num7 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, FindPatterns.ArrayTops[i + 1]], GlobalForm.nHLC[2, FindPatterns.ArrayBottoms[j]]), num5);
							if (CheckValues("R", num7))
							{
								DataGridView1.Rows.Add();
								DataGridView1.Rows[iRow].Cells[fSYMBOL].Value = Filename;
								DataGridView1.Rows[iRow].Cells[fLASTCLOSE].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]);
								DataGridView1.Rows[iRow].Cells[fTYPE].Value = "+Retrace";
								DataGridView1.Rows[iRow].Cells[fSTART].Value = Strings.Format((object)GlobalForm.nDT[0, FindPatterns.ArrayTops[i]], GlobalForm.UserDate);
								DataGridView1.Rows[iRow].Cells[fEND].Value = Strings.Format((object)GlobalForm.nDT[0, FindPatterns.ArrayBottoms[j]], GlobalForm.UserDate);
								DataGridView1.Rows[iRow].Cells[fREDATE].Value = Strings.Format((object)GlobalForm.nDT[0, FindPatterns.ArrayTops[i + 1]], GlobalForm.UserDate);
								DataGridView1.Rows[iRow].Cells[fVALUE].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, num7));
								DataGridView1.Rows[iRow].Cells[fPATH].Value = GlobalForm.OpenPath;
								iRow++;
							}
						}
					}
					else
					{
						if (!((FindPatterns.ArrayBottoms[j] < FindPatterns.ArrayTops[i]) & (FindPatterns.ArrayTops[i] < FindPatterns.ArrayBottoms[j + 1]) & (FindPatterns.ArrayTops[i + 1] > FindPatterns.ArrayBottoms[j + 1]) & (FindPatterns.ArrayTops[i - 1] < FindPatterns.ArrayBottoms[j])))
						{
							continue;
						}
						decimal num5 = decimal.Subtract(GlobalForm.nHLC[1, FindPatterns.ArrayTops[i]], GlobalForm.nHLC[2, FindPatterns.ArrayBottoms[j]]);
						if (decimal.Compare(num5, 0m) <= 0)
						{
							continue;
						}
						if (decimal.Compare(GlobalForm.nHLC[2, FindPatterns.ArrayBottoms[j + 1]], GlobalForm.nHLC[2, FindPatterns.ArrayBottoms[j]]) < 0)
						{
							if (TestCheckBoxes(Quiet: true, "E"))
							{
								decimal num6 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, FindPatterns.ArrayBottoms[j]], GlobalForm.nHLC[2, FindPatterns.ArrayBottoms[j + 1]]), num5);
								if (CheckValues("E", num6))
								{
									DataGridView1.Rows.Add();
									DataGridView1.Rows[iRow].Cells[fSYMBOL].Value = Filename;
									DataGridView1.Rows[iRow].Cells[fLASTCLOSE].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]);
									DataGridView1.Rows[iRow].Cells[fTYPE].Value = "-Extension";
									DataGridView1.Rows[iRow].Cells[fSTART].Value = Strings.Format((object)GlobalForm.nDT[0, FindPatterns.ArrayBottoms[j]], GlobalForm.UserDate);
									DataGridView1.Rows[iRow].Cells[fEND].Value = Strings.Format((object)GlobalForm.nDT[0, FindPatterns.ArrayTops[i]], GlobalForm.UserDate);
									DataGridView1.Rows[iRow].Cells[fREDATE].Value = Strings.Format((object)GlobalForm.nDT[0, FindPatterns.ArrayBottoms[j + 1]], GlobalForm.UserDate);
									DataGridView1.Rows[iRow].Cells[fVALUE].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, num6));
									DataGridView1.Rows[iRow].Cells[fPATH].Value = GlobalForm.OpenPath;
									iRow++;
								}
							}
						}
						else if (TestCheckBoxes(Quiet: true, "R"))
						{
							decimal num7 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, FindPatterns.ArrayTops[i]], GlobalForm.nHLC[2, FindPatterns.ArrayBottoms[j + 1]]), num5);
							if (CheckValues("R", num7))
							{
								DataGridView1.Rows.Add();
								DataGridView1.Rows[iRow].Cells[fSYMBOL].Value = Filename;
								DataGridView1.Rows[iRow].Cells[fLASTCLOSE].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]);
								DataGridView1.Rows[iRow].Cells[fTYPE].Value = "-Retrace";
								DataGridView1.Rows[iRow].Cells[fSTART].Value = Strings.Format((object)GlobalForm.nDT[0, FindPatterns.ArrayBottoms[j]], GlobalForm.UserDate);
								DataGridView1.Rows[iRow].Cells[fEND].Value = Strings.Format((object)GlobalForm.nDT[0, FindPatterns.ArrayTops[i]], GlobalForm.UserDate);
								DataGridView1.Rows[iRow].Cells[fREDATE].Value = Strings.Format((object)GlobalForm.nDT[0, FindPatterns.ArrayBottoms[j + 1]], GlobalForm.UserDate);
								DataGridView1.Rows[iRow].Cells[fVALUE].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, num7));
								DataGridView1.Rows[iRow].Cells[fPATH].Value = GlobalForm.OpenPath;
								iRow++;
							}
						}
					}
				}
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				if (StopPressed)
				{
					break;
				}
			}
			DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)6;
			DataGridView1.RowHeadersVisible = true;
		}
	}

	private void BuildGridHeader()
	{
		DataGridView1.RowCount = 0;
		DataGridView1.ColumnCount = tCOLUMNCOUNT;
		DataGridView1.Columns[fSYMBOL].Name = "Stock";
		DataGridView1.Columns[fLASTCLOSE].Name = "Last Close";
		DataGridView1.Columns[fTYPE].Name = "Retrace/Ext";
		DataGridView1.Columns[fSTART].Name = "Turn 1";
		DataGridView1.Columns[fEND].Name = "Turn 2";
		DataGridView1.Columns[fREDATE].Name = "Last Turn";
		DataGridView1.Columns[fVALUE].Name = "R/E %";
	}

	private void BuildList()
	{
		//IL_00d9: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d5: Unknown result type (might be due to invalid IL or missing references)
		//IL_00da: Unknown result type (might be due to invalid IL or missing references)
		//IL_00dc: Invalid comparison between Unknown and I4
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
				DialogResult val = (GlobalForm.Quiet ? ((DialogResult)6) : MessageBox.Show("No stocks were selected on the prior form. Did you want me to select all of them?", "ListForm: BuildList", (MessageBoxButtons)4, (MessageBoxIcon)64));
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
				ProgressBar1.Value = 100;
			}
			int num2 = MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count - 1;
			for (int j = 0; j <= num2 && !StopPressed; j++)
			{
				string text = MyProject.Forms.Mainform.ListBox1.SelectedItems[j].ToString();
				FilenameLabel.Text = text;
				((Control)FilenameLabel).Refresh();
				if (Operators.CompareString(text, FileNameInUse, false) != 0)
				{
					ProgressBar ProgBar = ProgressBar1;
					Label ErrorLabel = null;
					bool num3 = GlobalForm.LoadFile(text, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
					ProgressBar1 = ProgBar;
					if (num3)
					{
						FileNameInUse = "";
						continue;
					}
					FileNameInUse = text;
					if (GlobalForm.ErrorMessage != null)
					{
						(ErrorLabel = this.ErrorLabel).Text = ErrorLabel.Text + "\r\n" + GlobalForm.ErrorMessage;
					}
				}
				BuildGrid(text);
				if (StopPressed)
				{
					break;
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
				Label ErrorLabel;
				(ErrorLabel = this.ErrorLabel).Text = ErrorLabel.Text + "\r\nNumerous errors could mean the quote file received a bad update. Go to the Update Form and update using 'Get historical quotes' option to make sure the file has good information.\r\n\r\n" + this.ErrorLabel.Text;
				try
				{
					Clipboard.SetText(this.ErrorLabel.Text);
					this.ErrorLabel.Text = "Errors are on clipboard.";
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

	private void Chart1_MouseDown(object sender, MouseEventArgs e)
	{
		//IL_000f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0019: Invalid comparison between Unknown and I4
		//IL_0064: Unknown result type (might be due to invalid IL or missing references)
		//IL_006e: Invalid comparison between Unknown and I4
		//IL_002e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0033: Unknown result type (might be due to invalid IL or missing references)
		//IL_003f: Expected O, but got Unknown
		if (DataGridView1.RowCount <= 0)
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
		if (((int)e.Button == 2097152) & (DataGridView1.RowCount > 0))
		{
			GlobalForm.ShowQuoteInfo(Chart1, e);
		}
	}

	private void Chart1_MouseUp(object sender, MouseEventArgs e)
	{
		//IL_0012: Unknown result type (might be due to invalid IL or missing references)
		//IL_001c: Invalid comparison between Unknown and I4
		//IL_013a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0144: Invalid comparison between Unknown and I4
		//IL_0053: Unknown result type (might be due to invalid IL or missing references)
		//IL_0059: Expected O, but got Unknown
		if (DataGridView1.RowCount <= 0)
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
		//IL_0440: Unknown result type (might be due to invalid IL or missing references)
		//IL_0447: Expected O, but got Unknown
		//IL_0492: Unknown result type (might be due to invalid IL or missing references)
		//IL_0499: Expected O, but got Unknown
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
		checked
		{
			if (DataGridView1.RowCount > 0)
			{
				if (!(GlobalForm.FirstPoint == default(Point)))
				{
					Graphics obj = ((Control)this).CreateGraphics();
					Pen val2 = new Pen(((Form)this).BackColor);
					obj.DrawLine(val2, GlobalForm.FirstPoint, GlobalForm.TempPoint);
					GlobalForm.TempPoint = new Point(e.X, e.Y);
					((Control)this).Refresh();
					val2.Dispose();
				}
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
	}

	private void Chart1_Paint(object sender, PaintEventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0010: Expected O, but got Unknown
		Font val = new Font("Arial", 8f);
		GlobalForm.StringSize = e.Graphics.MeasureString("C", val);
		val.Dispose();
		if (DataGridView1.RowCount <= 0)
		{
			return;
		}
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
		//IL_0016: Unknown result type (might be due to invalid IL or missing references)
		//IL_0036: Unknown result type (might be due to invalid IL or missing references)
		//IL_003d: Expected O, but got Unknown
		if (!(e.ChartElement is Series) || Operators.CompareString(((Series)e.ChartElement).Name, "CandleSeries", false) != 0)
		{
			return;
		}
		Series val = (Series)e.ChartElement;
		ChartGraphics chartGraphics = e.ChartGraphics;
		int num = 4;
		string text = "";
		checked
		{
			DateTime t = default(DateTime);
			DateTime t2 = default(DateTime);
			DateTime t3 = default(DateTime);
			if (((BaseCollection)DataGridView1.SelectedRows).Count == 1)
			{
				for (int i = ((BaseCollection)DataGridView1.SelectedRows).Count - 1; i >= 0; i += -1)
				{
					try
					{
						if (DataGridView1.SelectedRows[i].Cells[fSTART].Value != null)
						{
							text = Conversions.ToString(DataGridView1.Rows[((DataGridViewBand)DataGridView1.SelectedRows[i]).Index].Cells[fTYPE].Value);
							t = Conversions.ToDate(DataGridView1.Rows[((DataGridViewBand)DataGridView1.SelectedRows[i]).Index].Cells[fSTART].Value);
							t2 = Conversions.ToDate(DataGridView1.Rows[((DataGridViewBand)DataGridView1.SelectedRows[i]).Index].Cells[fEND].Value);
							t3 = Conversions.ToDate(DataGridView1.Rows[((DataGridViewBand)DataGridView1.SelectedRows[i]).Index].Cells[fREDATE].Value);
							break;
						}
					}
					catch (Exception ex)
					{
						ProjectData.SetProjectError(ex);
						Exception ex2 = ex;
						ProjectData.ClearProjectError();
					}
				}
			}
			int chartStartIndex = GlobalForm.ChartStartIndex;
			int hLCRange = GlobalForm.HLCRange;
			int num2 = default(int);
			int num3 = default(int);
			int num4 = default(int);
			for (int i = chartStartIndex; i <= hLCRange; i++)
			{
				if (DateTime.Compare(GlobalForm.nDT[0, i], t) == 0)
				{
					num2 = i - GlobalForm.ChartStartIndex;
				}
				if (DateTime.Compare(GlobalForm.nDT[0, i], t2) == 0)
				{
					num3 = i - GlobalForm.ChartStartIndex;
				}
				if (DateTime.Compare(GlobalForm.nDT[0, i], t3) == 0)
				{
					num4 = i - GlobalForm.ChartStartIndex;
					break;
				}
			}
			int num5 = 0;
			PointF absolutePoint = default(PointF);
			PointF absolutePoint2 = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)val.Points)
			{
				if (unchecked(num5 == num2 || num5 == num4))
				{
					if (Operators.CompareString(Strings.Left(text, 1), "+", false) == 0)
					{
						absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num5 + 1));
						absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						absolutePoint.Y -= 6f;
						chartGraphics.Graphics.DrawEllipse(Pens.Red, (float)((double)absolutePoint.X - (double)num / 2.0), (float)((double)absolutePoint.Y - (double)num / 2.0), (float)num, (float)num);
					}
					else
					{
						absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num5 + 1));
						absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						absolutePoint2.Y += 4f;
						chartGraphics.Graphics.DrawEllipse(Pens.Red, (float)((double)absolutePoint2.X - (double)num / 2.0), (float)((double)absolutePoint2.Y - (double)num / 2.0), (float)num, (float)num);
					}
					if (num5 == num4)
					{
						break;
					}
				}
				else if (num5 == num3)
				{
					if (Operators.CompareString(Strings.Left(text, 1), "-", false) == 0)
					{
						absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num5 + 1));
						absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						absolutePoint.Y -= 6f;
						chartGraphics.Graphics.DrawEllipse(Pens.Red, (float)((double)absolutePoint.X - (double)num / 2.0), (float)((double)absolutePoint.Y - (double)num / 2.0), (float)num, (float)num);
					}
					else
					{
						absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num5 + 1));
						absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						absolutePoint2.Y += 4f;
						chartGraphics.Graphics.DrawEllipse(Pens.Red, (float)((double)absolutePoint2.X - (double)num / 2.0), (float)((double)absolutePoint2.Y - (double)num / 2.0), (float)num, (float)num);
					}
				}
				num5++;
			}
		}
	}

	private bool CheckValues(string Type, decimal RetraceExtension)
	{
		decimal value = decimal.Divide(ENUD.Value, 100m);
		decimal value2 = decimal.Divide(ENUD.Value, 100m);
		if (Operators.CompareString(Type, "E", false) != 0)
		{
			if (Operators.CompareString(Type, "R", false) == 0)
			{
				if (RAllCB.Checked)
				{
					return true;
				}
				if (R38CB.Checked & ((Convert.ToDouble(RetraceExtension) >= 0.38 - Convert.ToDouble(value2)) & (Convert.ToDouble(RetraceExtension) <= 0.38 + Convert.ToDouble(value2))))
				{
					return true;
				}
				if (R50CB.Checked & ((Convert.ToDouble(RetraceExtension) >= 0.5 - Convert.ToDouble(value2)) & (Convert.ToDouble(RetraceExtension) <= 0.5 + Convert.ToDouble(value2))))
				{
					return true;
				}
				if (R62CB.Checked & ((Convert.ToDouble(RetraceExtension) >= 0.62 - Convert.ToDouble(value2)) & (Convert.ToDouble(RetraceExtension) <= 0.62 + Convert.ToDouble(value2))))
				{
					return true;
				}
			}
		}
		else
		{
			if (EAllCB.Checked)
			{
				return true;
			}
			if (E38CB.Checked & ((Convert.ToDouble(RetraceExtension) >= 0.38 - Convert.ToDouble(value)) & (Convert.ToDouble(RetraceExtension) <= 0.38 + Convert.ToDouble(value))))
			{
				return true;
			}
			if (E50CB.Checked & ((Convert.ToDouble(RetraceExtension) >= 0.5 - Convert.ToDouble(value)) & (Convert.ToDouble(RetraceExtension) <= 0.5 + Convert.ToDouble(value))))
			{
				return true;
			}
			if (E62CB.Checked & ((Convert.ToDouble(RetraceExtension) >= 0.62 - Convert.ToDouble(value)) & (Convert.ToDouble(RetraceExtension) <= 0.62 + Convert.ToDouble(value))))
			{
				return true;
			}
		}
		return false;
	}

	private void ClipboardButton_Click(object sender, EventArgs e)
	{
		//IL_0132: Unknown result type (might be due to invalid IL or missing references)
		//IL_0167: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a7: Expected O, but got Unknown
		EnableDisable(EnableFlag: false);
		if (((BaseCollection)DataGridView1.SelectedRows).Count == 0)
		{
			DataGridView1.SelectAll();
		}
		StopPressed = false;
		((Control)StopButton).Focus();
		FilenameLabel.Text = "";
		((Control)this).Cursor = Cursors.WaitCursor;
		string text = "LAST CLOSE: the most recent closing price";
		text += "\r\nRetrace/Ext: + means price is moving up, - means price is moving down. For example, +Retrace means a retrace with price climbing.";
		text += "\r\nTURN 1, TURN 2, LAST TURN: The peak and valley turns followed by the extension or retrace.";
		text += "\r\nR/E %: An extension or retrace percentage using valley lows and peak highs.";
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
		EnableDisable(EnableFlag: true);
	}

	private void DataGridView1_SelectionChanged(object sender, EventArgs e)
	{
		if (((BaseCollection)DataGridView1.SelectedRows).Count != 1)
		{
			return;
		}
		((Control)this).Cursor = Cursors.WaitCursor;
		bool enabled = ((Control)DoneButton).Enabled;
		checked
		{
			for (int i = ((BaseCollection)DataGridView1.SelectedRows).Count - 1; i >= 0; i += -1)
			{
				try
				{
					if (DataGridView1.SelectedRows[i].Cells[fSTART].Value == null)
					{
						continue;
					}
					string text = Conversions.ToString(DataGridView1.Rows[((DataGridViewBand)DataGridView1.SelectedRows[i]).Index].Cells[fSYMBOL].Value);
					FilenameLabel.Text = text;
					ChartFromDTP.Value = Conversions.ToDate(DataGridView1.Rows[((DataGridViewBand)DataGridView1.SelectedRows[i]).Index].Cells[fSTART].Value);
					ChartToDTP.Value = Conversions.ToDate(DataGridView1.Rows[((DataGridViewBand)DataGridView1.SelectedRows[i]).Index].Cells[fREDATE].Value);
					string openPath = GlobalForm.OpenPath;
					GlobalForm.OpenPath = Conversions.ToString(DataGridView1.Rows[((DataGridViewBand)DataGridView1.SelectedRows[i]).Index].Cells[fPATH].Value);
					bool flag = false;
					if (Operators.CompareString(FileNameInUse, text, false) != 0)
					{
						if (enabled)
						{
							EnableDisable(EnableFlag: false);
						}
						ProgressBar ProgBar = ProgressBar1;
						Label ErrorLabel = this.ErrorLabel;
						bool num = GlobalForm.LoadFile(text, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
						this.ErrorLabel = ErrorLabel;
						ProgressBar1 = ProgBar;
						flag = num;
						if (enabled)
						{
							EnableDisable(EnableFlag: true);
						}
						FileNameInUse = text;
						GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
						GlobalForm.SelectChartType(Chart1);
					}
					if (!flag)
					{
						if (GlobalForm.IntradayData)
						{
							GlobalForm.SetupDateIndexes(ChartFromDTP.Value, ChartToDTP.Value);
							GlobalForm.ChartStartIndex -= 30;
							if (GlobalForm.ChartStartIndex < 0)
							{
								GlobalForm.ChartStartIndex = 0;
							}
							GlobalForm.ChartEndIndex += 30;
							if (GlobalForm.ChartEndIndex > GlobalForm.HLCRange)
							{
								GlobalForm.ChartEndIndex = GlobalForm.HLCRange;
							}
							GlobalForm.SetupDateIndexes(GlobalForm.nDT[0, GlobalForm.ChartStartIndex], GlobalForm.nDT[0, GlobalForm.ChartEndIndex]);
						}
						else
						{
							ChartFromDTP.Value = DateAndTime.DateAdd((DateInterval)4, -30.0, ChartFromDTP.Value);
							ChartToDTP.Value = DateAndTime.DateAdd((DateInterval)4, 30.0, ChartToDTP.Value);
							GlobalForm.SetupDateIndexes(ChartFromDTP.Value, ChartToDTP.Value);
						}
						GlobalForm.FirstPoint = default(Point);
						GlobalForm.LinesList.RemoveAll(StubBoolean);
						GlobalForm.SelectChartType(Chart1);
						GlobalForm.ShowStock(Chart1, GlobalForm.nDT[0, GlobalForm.ChartStartIndex], GlobalForm.nDT[0, GlobalForm.ChartEndIndex], VolumeFlag: false, MAFlag: false);
					}
					else
					{
						FileNameInUse = "";
					}
					GlobalForm.OpenPath = openPath;
					break;
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					ProjectData.ClearProjectError();
				}
			}
			((Control)this).Cursor = Cursors.Default;
		}
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void E38CB_CheckedChanged(object sender, EventArgs e)
	{
		if (!E38CB.Checked & !E50CB.Checked & !E62CB.Checked & !EAllCB.Checked & (!R38CB.Checked & !R50CB.Checked & !R62CB.Checked & !RAllCB.Checked))
		{
			((Control)AllPortfoliosButton).Enabled = false;
			((Control)StartButton).Enabled = false;
		}
		else
		{
			((Control)AllPortfoliosButton).Enabled = true;
			((Control)StartButton).Enabled = true;
		}
	}

	private void EnableDisable(bool EnableFlag)
	{
		((Control)DataGridView1).Enabled = EnableFlag;
		((Control)DoneButton).Enabled = EnableFlag;
		((Control)HelpButton1).Enabled = EnableFlag;
		((Control)StopButton).Enabled = !EnableFlag;
		if (!TestCheckBoxes(Quiet: true, "ER"))
		{
			((Control)StartButton).Enabled = false;
		}
		else
		{
			((Control)StartButton).Enabled = EnableFlag;
		}
		((Control)AllPortfoliosButton).Enabled = EnableFlag;
		if (EnableFlag & (DataGridView1.RowCount > 0))
		{
			((Control)ClipboardButton).Enabled = true;
		}
		else
		{
			((Control)ClipboardButton).Enabled = false;
		}
		((Control)FromDatePicker).Enabled = EnableFlag;
		((Control)ToDatePicker).Enabled = EnableFlag;
		((Control)SymbolTextBox).Enabled = EnableFlag;
		((Control)PriceBarsNUD).Enabled = EnableFlag;
		((Control)RNUD).Enabled = EnableFlag;
		((Control)ENUD).Enabled = EnableFlag;
		((Control)RAllCB).Enabled = EnableFlag;
		((Control)EAllCB).Enabled = EnableFlag;
		((Control)R62CB).Enabled = EnableFlag;
		((Control)R50CB).Enabled = EnableFlag;
		((Control)R38CB).Enabled = EnableFlag;
		((Control)E62CB).Enabled = EnableFlag;
		((Control)E50CB).Enabled = EnableFlag;
		((Control)E38CB).Enabled = EnableFlag;
		if (!GlobalForm.IntradayData)
		{
			((Control)DailyRadioButton).Enabled = EnableFlag;
			((Control)WeeklyRadioButton).Enabled = EnableFlag;
			((Control)MonthlyRadioButton).Enabled = EnableFlag;
		}
		else
		{
			GlobalForm.EnableDisableDWM(DailyRadioButton, WeeklyRadioButton, MonthlyRadioButton);
		}
		((Control)this).Refresh();
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.HelpFibFinder).ShowDialog();
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
		ProgressBar ProgBar = ProgressBar1;
		Label ErrorLabel = null;
		bool num = GlobalForm.LoadFile(fileName, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
		ProgressBar1 = ProgBar;
		if (!num)
		{
			FileNameInUse = text;
			BuildGrid(text);
		}
		else
		{
			FileNameInUse = "";
		}
	}

	private void StartButton_Click(object sender, EventArgs e)
	{
		//IL_00c3: Unknown result type (might be due to invalid IL or missing references)
		Busy = true;
		if (!TestCheckBoxes(GlobalForm.Quiet, "ER"))
		{
			return;
		}
		DateTimePicker fromDatePicker;
		DateTime FromDate = (fromDatePicker = FromDatePicker).Value;
		DateTimePicker toDatePicker;
		DateTime ToDate = (toDatePicker = ToDatePicker).Value;
		bool num = GlobalForm.SwapDates(ref FromDate, ref ToDate);
		toDatePicker.Value = ToDate;
		fromDatePicker.Value = FromDate;
		if (!num)
		{
			if (!GlobalForm.Quiet)
			{
				StopPressed = false;
			}
			EnableDisable(EnableFlag: false);
			GlobalForm.HideMessages = true;
			if (!GlobalForm.Quiet)
			{
				ErrorLabel.Text = "";
			}
			BuildList();
			GlobalForm.HideMessages = false;
			EnableDisable(EnableFlag: true);
			if (!GlobalForm.Quiet)
			{
				ProgressBar1.Value = 0;
				DataGridView1_SelectionChanged(RuntimeHelpers.GetObjectValue(sender), e);
				MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
		}
		Busy = false;
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

	private bool TestCheckBoxes(bool Quiet, string Type)
	{
		//IL_005d: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e8: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b2: Unknown result type (might be due to invalid IL or missing references)
		string text = "One of the check boxes must be checked to enable the start button.";
		switch (Type)
		{
		case "E":
			if (!E38CB.Checked & !E50CB.Checked & !E62CB.Checked & !EAllCB.Checked)
			{
				if (!Quiet)
				{
					MessageBox.Show(text, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				}
				return false;
			}
			if (!Busy)
			{
				((Control)StartButton).Enabled = true;
				((Control)AllPortfoliosButton).Enabled = true;
			}
			return true;
		case "R":
			if (!R38CB.Checked & !R50CB.Checked & !R62CB.Checked & !RAllCB.Checked)
			{
				if (!Quiet)
				{
					MessageBox.Show(text, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				}
				return false;
			}
			if (!Busy)
			{
				((Control)StartButton).Enabled = true;
				((Control)AllPortfoliosButton).Enabled = true;
			}
			return true;
		case "ER":
			if (!E38CB.Checked & !E50CB.Checked & !E62CB.Checked & !EAllCB.Checked & !R38CB.Checked & !R50CB.Checked & !R62CB.Checked & !RAllCB.Checked)
			{
				if (!Quiet)
				{
					MessageBox.Show(text, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				}
				if (!Busy)
				{
					((Control)StartButton).Enabled = false;
					((Control)AllPortfoliosButton).Enabled = false;
				}
				return false;
			}
			if (!Busy)
			{
				((Control)StartButton).Enabled = true;
				((Control)AllPortfoliosButton).Enabled = true;
			}
			return true;
		default:
			return false;
		}
	}
}
