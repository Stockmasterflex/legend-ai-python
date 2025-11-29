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
using Microsoft.VisualBasic.CompilerServices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class ListChartForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("ToDatePicker")]
	private DateTimePicker _ToDatePicker;

	[CompilerGenerated]
	[AccessedThroughProperty("FromDatePicker")]
	private DateTimePicker _FromDatePicker;

	[CompilerGenerated]
	[AccessedThroughProperty("MonthlyRadioButton")]
	private RadioButton _MonthlyRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("WeeklyRadioButton")]
	private RadioButton _WeeklyRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DailyRadioButton")]
	private RadioButton _DailyRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("NextButton")]
	private Button _NextButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PreviousButton")]
	private Button _PreviousButton;

	[CompilerGenerated]
	[AccessedThroughProperty("GraphButton")]
	private Button _GraphButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("Chart1")]
	private Chart _Chart1;

	[CompilerGenerated]
	[AccessedThroughProperty("TargetCheckBox")]
	private CheckBox _TargetCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("PercentButton")]
	private Button _PercentButton;

	[CompilerGenerated]
	[AccessedThroughProperty("MinusButton")]
	private Button _MinusButton;

	[CompilerGenerated]
	[AccessedThroughProperty("OriginalButton")]
	private Button _OriginalButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PlusButton")]
	private Button _PlusButton;

	private Point StartPoint;

	private Point EndPoint;

	private string Filename;

	private bool Crosshair;

	private Point CrosshairPoint;

	private Pen CrosshairPen;

	private DateTime PatternFromDate;

	private DateTime PatternToDate;

	private string OldFilename;

	private byte[] lsPatternList;

	private int ListchartLookback;

	private bool MyPatternTargets;

	private bool LockFlag;

	private CalloutAnnotation CurrentAnnotation;

	private bool StopPressed;

	private bool PercentCircles;

	private DateTime[] OriginalDates;

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

	[field: AccessedThroughProperty("PatternInfoLabel")]
	internal virtual Label PatternInfoLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
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

	public ListChartForm()
	{
		//IL_0044: Unknown result type (might be due to invalid IL or missing references)
		//IL_004e: Expected O, but got Unknown
		//IL_007c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0086: Expected O, but got Unknown
		((Form)this).Closing += ListChartForm_Closing;
		((Form)this).Load += ListChartForm_Load;
		((Form)this).Activated += ListChartForm_Activated;
		((Control)this).KeyDown += new KeyEventHandler(ListChartForm_KeyDown);
		Crosshair = false;
		CrosshairPen = null;
		OldFilename = "";
		lsPatternList = new byte[124];
		LockFlag = false;
		CurrentAnnotation = new CalloutAnnotation();
		StopPressed = false;
		PercentCircles = false;
		OriginalDates = new DateTime[2];
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
		//IL_0587: Unknown result type (might be due to invalid IL or missing references)
		//IL_0591: Expected O, but got Unknown
		//IL_0618: Unknown result type (might be due to invalid IL or missing references)
		//IL_0622: Expected O, but got Unknown
		//IL_09b5: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c33: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c3d: Expected O, but got Unknown
		//IL_0cc3: Unknown result type (might be due to invalid IL or missing references)
		//IL_0ccd: Expected O, but got Unknown
		//IL_0d63: Unknown result type (might be due to invalid IL or missing references)
		//IL_0d6d: Expected O, but got Unknown
		//IL_0df3: Unknown result type (might be due to invalid IL or missing references)
		//IL_0dfd: Expected O, but got Unknown
		ChartArea val = new ChartArea();
		Series val2 = new Series();
		Series val3 = new Series();
		Series val4 = new Series();
		ToDatePicker = new DateTimePicker();
		FromDatePicker = new DateTimePicker();
		MonthlyRadioButton = new RadioButton();
		WeeklyRadioButton = new RadioButton();
		DailyRadioButton = new RadioButton();
		ErrorLabel = new Label();
		Label4 = new Label();
		LoadingBar = new ProgressBar();
		NextButton = new Button();
		PreviousButton = new Button();
		Label3 = new Label();
		Label2 = new Label();
		GraphButton = new Button();
		DoneButton = new Button();
		Chart1 = new Chart();
		PatternInfoLabel = new Label();
		TargetCheckBox = new CheckBox();
		PercentButton = new Button();
		MinusButton = new Button();
		OriginalButton = new Button();
		PlusButton = new Button();
		((ISupportInitialize)Chart1).BeginInit();
		((Control)this).SuspendLayout();
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(671, 458);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(118, 20);
		((Control)ToDatePicker).TabIndex = 16;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(671, 432);
		((Control)FromDatePicker).Name = "FromDatePicker";
		FromDatePicker.ShowUpDown = true;
		((Control)FromDatePicker).Size = new Size(118, 20);
		((Control)FromDatePicker).TabIndex = 14;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)MonthlyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)MonthlyRadioButton).AutoSize = true;
		((Control)MonthlyRadioButton).Location = new Point(580, 461);
		((Control)MonthlyRadioButton).Name = "MonthlyRadioButton";
		((Control)MonthlyRadioButton).Size = new Size(62, 17);
		((Control)MonthlyRadioButton).TabIndex = 12;
		((Control)MonthlyRadioButton).Tag = "Monthly";
		((ButtonBase)MonthlyRadioButton).Text = "&Monthly";
		((ButtonBase)MonthlyRadioButton).UseVisualStyleBackColor = true;
		((Control)WeeklyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)WeeklyRadioButton).AutoSize = true;
		((Control)WeeklyRadioButton).Location = new Point(580, 443);
		((Control)WeeklyRadioButton).Name = "WeeklyRadioButton";
		((Control)WeeklyRadioButton).Size = new Size(61, 17);
		((Control)WeeklyRadioButton).TabIndex = 11;
		((Control)WeeklyRadioButton).Tag = "Weekly";
		((ButtonBase)WeeklyRadioButton).Text = "&Weekly";
		((ButtonBase)WeeklyRadioButton).UseVisualStyleBackColor = true;
		((Control)DailyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)DailyRadioButton).AutoSize = true;
		DailyRadioButton.Checked = true;
		((Control)DailyRadioButton).Location = new Point(580, 425);
		((Control)DailyRadioButton).Name = "DailyRadioButton";
		((Control)DailyRadioButton).Size = new Size(48, 17);
		((Control)DailyRadioButton).TabIndex = 10;
		DailyRadioButton.TabStop = true;
		((Control)DailyRadioButton).Tag = "Daily";
		((ButtonBase)DailyRadioButton).Text = "Dail&y";
		((ButtonBase)DailyRadioButton).UseVisualStyleBackColor = true;
		((Control)ErrorLabel).Anchor = (AnchorStyles)10;
		((Control)ErrorLabel).CausesValidation = false;
		((Control)ErrorLabel).ForeColor = Color.Red;
		((Control)ErrorLabel).Location = new Point(410, 435);
		((Control)ErrorLabel).Name = "ErrorLabel";
		((Control)ErrorLabel).Size = new Size(164, 17);
		((Control)ErrorLabel).TabIndex = 4;
		((Control)Label4).Anchor = (AnchorStyles)10;
		Label4.AutoSize = true;
		((Control)Label4).Location = new Point(465, 464);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(48, 13);
		((Control)Label4).TabIndex = 8;
		Label4.Text = "Loading:";
		((Control)LoadingBar).Anchor = (AnchorStyles)10;
		((Control)LoadingBar).ForeColor = Color.Green;
		((Control)LoadingBar).Location = new Point(514, 465);
		((Control)LoadingBar).Name = "LoadingBar";
		((Control)LoadingBar).Size = new Size(60, 13);
		((Control)LoadingBar).TabIndex = 9;
		((Control)NextButton).Anchor = (AnchorStyles)10;
		((Control)NextButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)NextButton).Location = new Point(822, 454);
		((Control)NextButton).Name = "NextButton";
		((Control)NextButton).Size = new Size(29, 23);
		((Control)NextButton).TabIndex = 20;
		((ButtonBase)NextButton).Text = ">";
		((ButtonBase)NextButton).UseVisualStyleBackColor = true;
		((Control)PreviousButton).Anchor = (AnchorStyles)10;
		((Control)PreviousButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)PreviousButton).Location = new Point(795, 454);
		((Control)PreviousButton).Name = "PreviousButton";
		((Control)PreviousButton).Size = new Size(27, 23);
		((Control)PreviousButton).TabIndex = 19;
		((ButtonBase)PreviousButton).Text = "<";
		((ButtonBase)PreviousButton).UseVisualStyleBackColor = true;
		((Control)Label3).Anchor = (AnchorStyles)10;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(648, 461);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(23, 13);
		((Control)Label3).TabIndex = 15;
		Label3.Text = "&To:";
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(638, 437);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(33, 13);
		((Control)Label2).TabIndex = 13;
		Label2.Text = "&From:";
		((Control)GraphButton).Anchor = (AnchorStyles)10;
		((Control)GraphButton).Location = new Point(857, 427);
		((Control)GraphButton).Name = "GraphButton";
		((Control)GraphButton).Size = new Size(49, 23);
		((Control)GraphButton).TabIndex = 18;
		((ButtonBase)GraphButton).Text = "&Graph";
		((ButtonBase)GraphButton).UseVisualStyleBackColor = true;
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(857, 455);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(49, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
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
		val.BorderDashStyle = (ChartDashStyle)5;
		val.Name = "ChartArea1";
		val.Position.Auto = false;
		val.Position.Height = 100f;
		val.Position.Width = 100f;
		val.ShadowOffset = 7;
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
		((DataPointCustomProperties)val2).MarkerColor = Color.Black;
		val2.Name = "CandleSeries";
		val2.ShadowColor = Color.Black;
		val2.XValueType = (ChartValueType)8;
		val2.YAxisType = (AxisType)1;
		val2.YValuesPerPoint = 4;
		((DataPointCustomProperties)val3).BorderColor = Color.Black;
		val3.ChartArea = "ChartArea1";
		val3.IsXValueIndexed = true;
		val3.Name = "VolumeSeries";
		val3.XValueType = (ChartValueType)8;
		val4.ChartArea = "ChartArea1";
		val4.ChartType = (SeriesChartType)3;
		((DataPointCustomProperties)val4).Color = Color.Blue;
		val4.IsXValueIndexed = true;
		val4.Name = "MASeries";
		val4.XValueType = (ChartValueType)8;
		val4.YAxisType = (AxisType)1;
		((Collection<Series>)(object)Chart1.Series).Add(val2);
		((Collection<Series>)(object)Chart1.Series).Add(val3);
		((Collection<Series>)(object)Chart1.Series).Add(val4);
		Chart1.Size = new Size(897, 415);
		((Control)Chart1).TabIndex = 1;
		((Control)Chart1).Text = "Chart1";
		((Control)PatternInfoLabel).Anchor = (AnchorStyles)10;
		PatternInfoLabel.BorderStyle = (BorderStyle)2;
		((Control)PatternInfoLabel).CausesValidation = false;
		((Control)PatternInfoLabel).ForeColor = Color.Red;
		((Control)PatternInfoLabel).Location = new Point(8, 427);
		((Control)PatternInfoLabel).Name = "PatternInfoLabel";
		((Control)PatternInfoLabel).Size = new Size(372, 59);
		((Control)PatternInfoLabel).TabIndex = 2;
		((Control)TargetCheckBox).Anchor = (AnchorStyles)10;
		((ButtonBase)TargetCheckBox).AutoSize = true;
		((Control)TargetCheckBox).Location = new Point(795, 432);
		((Control)TargetCheckBox).Name = "TargetCheckBox";
		((Control)TargetCheckBox).Size = new Size(62, 17);
		((Control)TargetCheckBox).TabIndex = 17;
		((ButtonBase)TargetCheckBox).Text = "&Targets";
		((ButtonBase)TargetCheckBox).UseVisualStyleBackColor = true;
		((Control)PercentButton).Anchor = (AnchorStyles)10;
		((Control)PercentButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)PercentButton).Location = new Point(383, 432);
		((Control)PercentButton).Name = "PercentButton";
		((Control)PercentButton).Size = new Size(29, 23);
		((Control)PercentButton).TabIndex = 3;
		((ButtonBase)PercentButton).Text = "%";
		((ButtonBase)PercentButton).UseVisualStyleBackColor = true;
		((Control)MinusButton).Anchor = (AnchorStyles)10;
		((Control)MinusButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)MinusButton).Location = new Point(437, 461);
		((Control)MinusButton).Name = "MinusButton";
		((Control)MinusButton).Size = new Size(29, 20);
		((Control)MinusButton).TabIndex = 7;
		((Control)MinusButton).Tag = "";
		((ButtonBase)MinusButton).Text = "-";
		((ButtonBase)MinusButton).UseVisualStyleBackColor = true;
		((Control)OriginalButton).Anchor = (AnchorStyles)10;
		((Control)OriginalButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)OriginalButton).Location = new Point(410, 461);
		((Control)OriginalButton).Name = "OriginalButton";
		((Control)OriginalButton).Size = new Size(29, 20);
		((Control)OriginalButton).TabIndex = 6;
		((ButtonBase)OriginalButton).Text = "0";
		((ButtonBase)OriginalButton).UseVisualStyleBackColor = true;
		((Control)PlusButton).Anchor = (AnchorStyles)10;
		((Control)PlusButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)PlusButton).Location = new Point(383, 461);
		((Control)PlusButton).Name = "PlusButton";
		((Control)PlusButton).Size = new Size(29, 20);
		((Control)PlusButton).TabIndex = 5;
		((ButtonBase)PlusButton).Text = "+";
		((ButtonBase)PlusButton).UseVisualStyleBackColor = true;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(915, 488);
		((Control)this).Controls.Add((Control)(object)MinusButton);
		((Control)this).Controls.Add((Control)(object)OriginalButton);
		((Control)this).Controls.Add((Control)(object)PlusButton);
		((Control)this).Controls.Add((Control)(object)PercentButton);
		((Control)this).Controls.Add((Control)(object)TargetCheckBox);
		((Control)this).Controls.Add((Control)(object)PatternInfoLabel);
		((Control)this).Controls.Add((Control)(object)ToDatePicker);
		((Control)this).Controls.Add((Control)(object)FromDatePicker);
		((Control)this).Controls.Add((Control)(object)MonthlyRadioButton);
		((Control)this).Controls.Add((Control)(object)WeeklyRadioButton);
		((Control)this).Controls.Add((Control)(object)DailyRadioButton);
		((Control)this).Controls.Add((Control)(object)ErrorLabel);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)LoadingBar);
		((Control)this).Controls.Add((Control)(object)NextButton);
		((Control)this).Controls.Add((Control)(object)PreviousButton);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)GraphButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)Chart1);
		((Form)this).KeyPreview = true;
		((Control)this).Name = "ListChartForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "List's Chart Form";
		((ISupportInitialize)Chart1).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void ListChartForm_Closing(object sender, CancelEventArgs e)
	{
		LockFlag = false;
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
		GlobalForm.LCFPatternTargets = TargetCheckBox.Checked;
		GlobalForm.PatternTargets = MyPatternTargets;
		int num = 0;
		do
		{
			GlobalForm.PatternList[num] = lsPatternList[num];
			num = checked(num + 1);
		}
		while (num <= 123);
		MySettingsProperty.Settings.ListChartLocation = ((Form)this).Location;
		MySettingsProperty.Settings.ListChartSize = ((Form)this).Size;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
		switch (GlobalForm.ChartPeriodShown)
		{
		case 0:
			if (!MyProject.Forms.ListForm.DailyRadioButton.Checked)
			{
				if (MyProject.Forms.ListForm.WeeklyRadioButton.Checked)
				{
					GlobalForm.ChartPeriodShown = 1;
				}
				else
				{
					GlobalForm.ChartPeriodShown = 2;
				}
			}
			break;
		case 1:
			if (!MyProject.Forms.ListForm.WeeklyRadioButton.Checked)
			{
				if (MyProject.Forms.ListForm.DailyRadioButton.Checked)
				{
					GlobalForm.ChartPeriodShown = 0;
				}
				else
				{
					GlobalForm.ChartPeriodShown = 2;
				}
			}
			break;
		case 2:
			if (!MyProject.Forms.ListForm.MonthlyRadioButton.Checked)
			{
				if (MyProject.Forms.ListForm.DailyRadioButton.Checked)
				{
					GlobalForm.ChartPeriodShown = 0;
				}
				else
				{
					GlobalForm.ChartPeriodShown = 1;
				}
			}
			break;
		}
	}

	private void ListChartForm_Load(object sender, EventArgs e)
	{
		//IL_002e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0038: Expected O, but got Unknown
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.ListChartLocation, MySettingsProperty.Settings.ListChartSize);
		OldFilename = "";
		if (CurrentAnnotation == null)
		{
			CurrentAnnotation = new CalloutAnnotation();
		}
		((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)CurrentAnnotation);
	}

	private void ListChartForm_Activated(object sender, EventArgs e)
	{
		//IL_012b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0130: Unknown result type (might be due to invalid IL or missing references)
		//IL_013b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0146: Unknown result type (might be due to invalid IL or missing references)
		//IL_0151: Unknown result type (might be due to invalid IL or missing references)
		//IL_0158: Unknown result type (might be due to invalid IL or missing references)
		//IL_0169: Unknown result type (might be due to invalid IL or missing references)
		//IL_017a: Unknown result type (might be due to invalid IL or missing references)
		//IL_018b: Unknown result type (might be due to invalid IL or missing references)
		//IL_019c: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_01be: Unknown result type (might be due to invalid IL or missing references)
		//IL_01cf: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e0: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f1: Unknown result type (might be due to invalid IL or missing references)
		//IL_0202: Unknown result type (might be due to invalid IL or missing references)
		//IL_0213: Unknown result type (might be due to invalid IL or missing references)
		//IL_0224: Unknown result type (might be due to invalid IL or missing references)
		//IL_0235: Unknown result type (might be due to invalid IL or missing references)
		if (!LockFlag)
		{
			LockFlag = true;
			((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Clear();
			((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points).Clear();
			((Control)DoneButton).Enabled = false;
			((Control)GraphButton).Enabled = false;
			((Control)NextButton).Enabled = false;
			((Control)PercentButton).Enabled = false;
			((Control)MinusButton).Enabled = false;
			((Control)OriginalButton).Enabled = false;
			((Control)PlusButton).Enabled = false;
			((Control)PreviousButton).Enabled = false;
			((Control)FromDatePicker).Enabled = false;
			((Control)ToDatePicker).Enabled = false;
			((Control)DailyRadioButton).Enabled = false;
			((Control)WeeklyRadioButton).Enabled = false;
			((Control)MonthlyRadioButton).Enabled = false;
			((Control)TargetCheckBox).Enabled = false;
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
			val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
			val.SetToolTip((Control)(object)ToDatePicker, "The ending date in the file you wish to view.");
			val.SetToolTip((Control)(object)GraphButton, "Redraw the chart.");
			val.SetToolTip((Control)(object)LoadingBar, "Shows file loading progress. Keep files short for speed.");
			val.SetToolTip((Control)(object)MinusButton, "Zoom out the chart.");
			val.SetToolTip((Control)(object)NextButton, "Load the next pattern.");
			val.SetToolTip((Control)(object)OriginalButton, "Restore the original dates.");
			val.SetToolTip((Control)(object)PercentButton, "Right mouse click two price bars then % to show percentage move.");
			val.SetToolTip((Control)(object)PlusButton, "Zoom in the chart.");
			val.SetToolTip((Control)(object)PreviousButton, "Load the previous pattern.");
			val.SetToolTip((Control)(object)TargetCheckBox, "Show targets or not.");
			val.SetToolTip((Control)(object)DailyRadioButton, "Show quote information using the daily scale.");
			val.SetToolTip((Control)(object)WeeklyRadioButton, "Show quote information using the weekly scale.");
			val.SetToolTip((Control)(object)MonthlyRadioButton, "Show quote information using the monthly scale.");
			GlobalForm.iFib1 = -1;
			GlobalForm.iFib2 = -1;
			MyPatternTargets = GlobalForm.PatternTargets;
			TargetCheckBox.Checked = GlobalForm.LCFPatternTargets;
			GlobalForm.PatternTargets = GlobalForm.LCFPatternTargets;
			Array.Copy(GlobalForm.PatternList, lsPatternList, 124);
			Array.Clear(GlobalForm.PatternList, 0, 124);
			GlobalForm.SelectChartType(Chart1);
			GlobalForm.FirstPoint = default(Point);
			GlobalForm.LinesList.RemoveAll(StubBoolean);
			LoadingBar.Value = 0;
			ListchartLookback = 122;
			GlobalForm.LBIndex = 0;
			int index = ((DataGridViewBand)MyProject.Forms.ListForm.DataGridView1.SelectedRows[GlobalForm.LBIndex]).Index;
			try
			{
				FindAndShowThisPattern(index);
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				ProjectData.ClearProjectError();
			}
			((Control)DoneButton).Enabled = true;
			((Control)GraphButton).Enabled = true;
			((Control)NextButton).Enabled = true;
			((Control)PreviousButton).Enabled = true;
			((Control)PercentButton).Enabled = true;
			((Control)FromDatePicker).Enabled = true;
			((Control)ToDatePicker).Enabled = true;
			((Control)MinusButton).Enabled = true;
			((Control)OriginalButton).Enabled = true;
			((Control)PlusButton).Enabled = true;
			GlobalForm.EnableDisableDWM(DailyRadioButton, WeeklyRadioButton, MonthlyRadioButton);
			((Control)TargetCheckBox).Enabled = true;
			OriginalDates[0] = FromDatePicker.Value;
			OriginalDates[1] = ToDatePicker.Value;
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
		if (((GlobalForm.ChartPeriodShown == 1) & !WeeklyRadioButton.Checked) || (GlobalForm.PatternCount > 0 && GlobalForm.ChartPatterns[0].iEndDate > GlobalForm.HLCRange) || (GlobalForm.CandleCount > 0 && GlobalForm.CandlePatterns[0].iEndDate > GlobalForm.HLCRange))
		{
			return;
		}
		checked
		{
			try
			{
				int num = GlobalForm.PatternCount - 1;
				for (int i = 0; i <= num; i++)
				{
					if ((GlobalForm.ChartPatterns[i].Type == 82) | (GlobalForm.ChartPatterns[i].Type == 1))
					{
						if ((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStartDate], PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iMidDate], PatternToDate) == 0))
						{
							GlobalForm.ChartPatterns[i].RenderColor = Color.Red;
						}
						else
						{
							GlobalForm.ChartPatterns[i].RenderColor = Color.Black;
						}
					}
					else if ((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStartDate], PatternFromDate) == 0) | ((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStart2Date], PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEndDate], PatternToDate) == 0)) | (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEnd2Date], PatternToDate) == 0))
					{
						GlobalForm.ChartPatterns[i].RenderColor = Color.Red;
					}
					else
					{
						GlobalForm.ChartPatterns[i].RenderColor = Color.Black;
					}
				}
				int num2 = GlobalForm.CandleCount - 1;
				for (int j = 0; j <= num2; j++)
				{
					if ((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.CandlePatterns[j].iStartDate], PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.CandlePatterns[j].iEndDate], PatternToDate) == 0))
					{
						GlobalForm.CandlePatterns[j].RenderColor = Color.Red;
					}
					else
					{
						GlobalForm.CandlePatterns[j].RenderColor = Color.Black;
					}
				}
				ShowPatterns.DisplayAllPatterns(e, FromDatePicker.Value, GlobalForm.nDT[0, GlobalForm.HLCRange]);
				if ((GlobalForm.FilterGlobals.CBMasterSwitch & GlobalForm.FilterGlobals.CBStages & (GlobalForm.FilterGlobals.CBStage1 | GlobalForm.FilterGlobals.CBStage2 | GlobalForm.FilterGlobals.CBStage3 | GlobalForm.FilterGlobals.CBStage4)) && Operators.CompareString(MyProject.Forms.ListForm.DataGridView1.Rows[((DataGridViewBand)MyProject.Forms.ListForm.DataGridView1.SelectedRows[GlobalForm.LBIndex]).Index].Cells[2].Value.ToString(), "Stage", false) == 0)
				{
					ShowStages(e);
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				ProjectData.ClearProjectError();
			}
			ShowPercent(e);
		}
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		LockFlag = false;
		((Form)this).Close();
	}

	private void FindAndShowThisPattern(int RowIndex)
	{
		bool flag = false;
		if (Operators.CompareString(MyProject.Forms.ListForm.DataGridView1.Rows[RowIndex].Cells[2].Value.ToString(), "Stage", false) == 0)
		{
			if (!WeeklyRadioButton.Checked)
			{
				flag = true;
			}
			WeeklyRadioButton.Checked = true;
		}
		else if (!GlobalForm.IntradayData)
		{
			bool flag2 = true;
			if (flag2 == MyProject.Forms.ListForm.DailyRadioButton.Checked)
			{
				if (!DailyRadioButton.Checked)
				{
					flag = true;
				}
				DailyRadioButton.Checked = true;
			}
			else if (flag2 == MyProject.Forms.ListForm.WeeklyRadioButton.Checked)
			{
				if (!WeeklyRadioButton.Checked)
				{
					flag = true;
				}
				WeeklyRadioButton.Checked = true;
			}
			else if (flag2 == MyProject.Forms.ListForm.MonthlyRadioButton.Checked)
			{
				if (!MonthlyRadioButton.Checked)
				{
					flag = true;
				}
				MonthlyRadioButton.Checked = true;
			}
		}
		Filename = MyProject.Forms.ListForm.DataGridView1.Rows[RowIndex].Cells[0].Value.ToString();
		if (Operators.CompareString(Filename, OldFilename, false) != 0 || flag)
		{
			string filename = Filename;
			ProgressBar ProgBar = LoadingBar;
			Label ErrorLabel = this.ErrorLabel;
			bool num = GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
			this.ErrorLabel = ErrorLabel;
			LoadingBar = ProgBar;
			if (num)
			{
				return;
			}
			OldFilename = Filename;
		}
		GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
		GlobalForm.SelectChartType(Chart1);
		PatternFromDate = Conversions.ToDate(MyProject.Forms.ListForm.DataGridView1.Rows[RowIndex].Cells[3].Value);
		PatternToDate = Conversions.ToDate(MyProject.Forms.ListForm.DataGridView1.Rows[RowIndex].Cells[4].Value);
		checked
		{
			if (GlobalForm.IntradayData)
			{
				int num2 = -1;
				int num3 = -1;
				if ((DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MaxDate) <= 0))
				{
					FromDatePicker.Value = GlobalForm.nDT[0, 0];
				}
				else
				{
					FromDatePicker.Value = DateAndTime.Now;
				}
				if ((DateTime.Compare(GlobalForm.nDT[0, 0], ToDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, 0], ToDatePicker.MaxDate) <= 0))
				{
					ToDatePicker.Value = GlobalForm.nDT[0, GlobalForm.HLCRange];
				}
				else
				{
					ToDatePicker.Value = DateAndTime.Now;
				}
				int hLCRange = GlobalForm.HLCRange;
				for (int i = 0; i <= hLCRange; i++)
				{
					if ((num2 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i], PatternFromDate) >= 0))
					{
						if (i >= ListchartLookback)
						{
							FromDatePicker.Value = GlobalForm.nDT[0, i - ListchartLookback];
						}
						num2 = i;
					}
					if ((num3 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i], PatternToDate) >= 0))
					{
						if (i + ListchartLookback <= GlobalForm.HLCRange)
						{
							ToDatePicker.Value = GlobalForm.nDT[0, i + ListchartLookback];
						}
						num3 = i;
					}
					if (unchecked(num2 != -1 && num3 != -1))
					{
						break;
					}
				}
			}
			else
			{
				FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)(-1 * ListchartLookback), PatternFromDate);
				ToDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)ListchartLookback, PatternToDate);
			}
			DateTimePicker fromDatePicker = FromDatePicker;
			DateTime FromDate = fromDatePicker.Value;
			DateTimePicker toDatePicker;
			DateTime ToDate = (toDatePicker = ToDatePicker).Value;
			GlobalForm.SwapDates(ref FromDate, ref ToDate);
			toDatePicker.Value = ToDate;
			fromDatePicker.Value = FromDate;
			GlobalForm.ChartStart = FromDatePicker.Value;
			GlobalForm.ChartEnd = ToDatePicker.Value;
			string text = MyProject.Forms.ListForm.DataGridView1.Rows[RowIndex].Cells[2].Value.ToString();
			PatternInfoLabel.Text = Filename + ": " + text + " from " + Strings.Format((object)PatternFromDate, GlobalForm.UserDate) + " to " + Strings.Format((object)PatternToDate, GlobalForm.UserDate) + ". A pattern may not be highlighted. To fix, zoom out (- button) until it appears, but some may remain hidden.";
			GlobalForm.CheckDates(FromDatePicker, ToDatePicker);
			if (!GlobalForm.ChartVolume && ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Count > 0)
			{
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Clear();
			}
			bool chartVolume = GlobalForm.ChartVolume;
			if (Strings.InStr(Conversions.ToString(MyProject.Forms.ListForm.DataGridView1.Rows[RowIndex].Cells[18].Value), "V", (CompareMethod)0) != 0)
			{
				GlobalForm.ChartVolume = true;
			}
			if (!GlobalForm.ShowStock(Chart1, FromDatePicker.Value, ToDatePicker.Value, GlobalForm.ChartVolume, GlobalForm.MAUsed))
			{
				Array.Clear(GlobalForm.PatternList, 0, 124);
				object objectValue = RuntimeHelpers.GetObjectValue(GlobalForm.TranslatePatternName(text, GlobalForm.PASSNAME));
				if (Conversions.ToInteger(objectValue) != -1)
				{
					if ((Conversions.ToInteger(objectValue) == 82) | (Conversions.ToInteger(objectValue) == 1))
					{
						Label ErrorLabel;
						(ErrorLabel = PatternInfoLabel).Text = ErrorLabel.Text + " Channel targets measure from where price crosses the channel trendline, extended into the future.";
					}
					GlobalForm.PatternList[Conversions.ToByte(objectValue)] = 1;
					FindPatterns.EnterFindPatterns(FromDatePicker.Value, GlobalForm.nDT[0, GlobalForm.HLCRange], null, ref StopPressed, 1);
					if (GlobalForm.PatternCount == 0)
					{
						bool nearFutures = GlobalForm.NearFutures;
						GlobalForm.NearFutures = false;
						FindPatterns.EnterFindPatterns(FromDatePicker.Value, ToDatePicker.Value, null, ref StopPressed, 1);
						GlobalForm.NearFutures = nearFutures;
					}
					int num4 = GlobalForm.PatternCount - 1;
					for (int j = 0; j <= num4; j++)
					{
						if ((GlobalForm.ChartPatterns[j].Type == 82) | (GlobalForm.ChartPatterns[j].Type == 1))
						{
							if (GlobalForm.IntradayData)
							{
								if ((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iStartDate], PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iMidDate], PatternToDate) == 0))
								{
									GlobalForm.GetCPInformation(j);
									break;
								}
							}
							else if ((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iStartDate].Date, PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iMidDate].Date, PatternToDate) == 0))
							{
								GlobalForm.GetCPInformation(j);
								break;
							}
						}
						else if (GlobalForm.IntradayData)
						{
							if (((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iStartDate], PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iEndDate], PatternToDate) == 0)) | (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iEnd2Date], PatternToDate) == 0) | (((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iStart2Date], PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iEndDate], PatternToDate) == 0)) | (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iEnd2Date], PatternToDate) == 0)))
							{
								GlobalForm.GetCPInformation(j);
								break;
							}
						}
						else if (((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iStartDate].Date, PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iEndDate].Date, PatternToDate) == 0)) | (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iEnd2Date].Date, PatternToDate) == 0) | (((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iStart2Date].Date, PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iEndDate].Date, PatternToDate) == 0)) | (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[j].iEnd2Date].Date, PatternToDate) == 0)))
						{
							GlobalForm.GetCPInformation(j);
							break;
						}
					}
				}
				else
				{
					FindPatterns.EnterFindPatterns(FromDatePicker.Value, ToDatePicker.Value, null, ref StopPressed, 1, null, ref RowIndex, null);
					FindPatterns.FindWeinsteinStages(Filename, 1);
				}
			}
			GlobalForm.ChartVolume = chartVolume;
			Chart1.Invalidate();
			((Form)this).Text = "List Chart Form: " + Filename;
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
		GlobalForm.ChartStart = FromDatePicker.Value;
		GlobalForm.ChartEnd = ToDatePicker.Value;
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
		GlobalForm.SetupDateIndexes(GlobalForm.ChartStart, GlobalForm.ChartEnd);
		checked
		{
			if (!GlobalForm.ShowStock(Chart1, GlobalForm.ChartStartIndex, GlobalForm.ChartEndIndex, GlobalForm.ChartVolume, GlobalForm.MAUsed))
			{
				FindPatterns.EnterFindPatterns(GlobalForm.ChartStart, GlobalForm.nDT[0, GlobalForm.HLCRange], null, ref StopPressed, 3);
				int num2 = GlobalForm.PatternCount - 1;
				for (int i = 0; i <= num2; i++)
				{
					if ((GlobalForm.ChartPatterns[i].Type == 82) | (GlobalForm.ChartPatterns[i].Type == 1))
					{
						if (GlobalForm.IntradayData)
						{
							if ((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStartDate], PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iMidDate], PatternToDate) == 0))
							{
								GlobalForm.GetCPInformation(i);
								break;
							}
						}
						else if ((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStartDate].Date, PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iMidDate].Date, PatternToDate) == 0))
						{
							GlobalForm.GetCPInformation(i);
							break;
						}
					}
					else if (GlobalForm.IntradayData)
					{
						if (((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStartDate], PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEndDate], PatternToDate) == 0)) | (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEnd2Date], PatternToDate) == 0) | (((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStart2Date], PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEndDate], PatternToDate) == 0)) | (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEnd2Date], PatternToDate) == 0)))
						{
							GlobalForm.GetCPInformation(i);
							break;
						}
					}
					else if (((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStartDate].Date, PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEndDate].Date, PatternToDate) == 0)) | (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEnd2Date].Date, PatternToDate) == 0) | (((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStart2Date].Date, PatternFromDate) == 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEndDate].Date, PatternToDate) == 0)) | (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEnd2Date].Date, PatternToDate) == 0)))
					{
						GlobalForm.GetCPInformation(i);
						break;
					}
				}
				((Form)this).Text = "List Chart Form: " + Filename;
			}
			Chart1.Invalidate();
		}
	}

	private void ListChartForm_KeyDown(object sender, KeyEventArgs e)
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
		//IL_007a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0084: Expected O, but got Unknown
		checked
		{
			GlobalForm.LBIndex++;
			if (GlobalForm.LBIndex >= ((BaseCollection)MyProject.Forms.ListForm.DataGridView1.SelectedRows).Count)
			{
				GlobalForm.LBIndex--;
				Interaction.Beep();
				return;
			}
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
			int index = ((DataGridViewBand)MyProject.Forms.ListForm.DataGridView1.SelectedRows[GlobalForm.LBIndex]).Index;
			GlobalForm.FirstPoint = default(Point);
			GlobalForm.LinesList.RemoveAll(StubBoolean);
			FindAndShowThisPattern(index);
			OriginalDates[0] = FromDatePicker.Value;
			OriginalDates[1] = ToDatePicker.Value;
		}
	}

	private void PreviousButton_Click(object sender, EventArgs e)
	{
		//IL_005c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0066: Expected O, but got Unknown
		checked
		{
			GlobalForm.LBIndex--;
			if (GlobalForm.LBIndex < 0)
			{
				GlobalForm.LBIndex = 0;
				Interaction.Beep();
				return;
			}
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
			int index = ((DataGridViewBand)MyProject.Forms.ListForm.DataGridView1.SelectedRows[GlobalForm.LBIndex]).Index;
			GlobalForm.FirstPoint = default(Point);
			GlobalForm.LinesList.RemoveAll(StubBoolean);
			FindAndShowThisPattern(index);
			OriginalDates[0] = FromDatePicker.Value;
			OriginalDates[1] = ToDatePicker.Value;
		}
	}

	private void ShowStages(ChartPaintEventArgs e)
	{
		//IL_001c: Unknown result type (might be due to invalid IL or missing references)
		//IL_003c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0043: Expected O, but got Unknown
		//IL_0079: Unknown result type (might be due to invalid IL or missing references)
		//IL_0080: Expected O, but got Unknown
		PointF empty = PointF.Empty;
		if (!(e.ChartElement is Series) || Operators.CompareString(((Series)e.ChartElement).Name, "CandleSeries", false) != 0)
		{
			return;
		}
		Series val = (Series)e.ChartElement;
		checked
		{
			if ((((Collection<DataPoint>)(object)val.Points).Count <= 2) | (GlobalForm.WStages.Length - 1 != GlobalForm.HLCRange))
			{
				return;
			}
			Font val2 = new Font("Arial", 10f, (FontStyle)1);
			float num = GlobalForm.CalculateCharacterWidth(e);
			int num2 = GlobalForm.ChartStartIndex;
			int num3 = GlobalForm.WStages[num2];
			PointF pointF = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)val.Points)
			{
				if (num2 > GlobalForm.WStages.Length - 1)
				{
					break;
				}
				if (num2 == GlobalForm.ChartStartIndex)
				{
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num2 - GlobalForm.ChartStartIndex));
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					e.ChartGraphics.Graphics.DrawString(num3.ToString(), val2, Brushes.Red, pointF);
				}
				if ((GlobalForm.WStages[num2] != num3) | (num2 - GlobalForm.ChartStartIndex == ((Collection<DataPoint>)(object)val.Points).Count - 1))
				{
					empty.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num2 - GlobalForm.ChartStartIndex));
					PointF absolutePoint;
					if (unchecked(num3 == 1 || num3 == 3))
					{
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(empty);
						absolutePoint.Y = pointF.Y;
					}
					else
					{
						empty.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(empty);
					}
					e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF, absolutePoint);
					absolutePoint.X += num;
					e.ChartGraphics.Graphics.DrawString(GlobalForm.WStages[num2].ToString(), val2, Brushes.Red, absolutePoint);
					absolutePoint.X -= num;
					pointF = absolutePoint;
					num3 = GlobalForm.WStages[num2];
				}
				num2++;
			}
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

	private bool StubBoolean(GlobalForm.LineEndPoints sPoint)
	{
		return true;
	}

	private void TargetCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		GlobalForm.PatternTargets = TargetCheckBox.Checked;
		GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
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
		GlobalForm.ChartStart = FromDatePicker.Value;
		GlobalForm.ChartEnd = ToDatePicker.Value;
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
}
