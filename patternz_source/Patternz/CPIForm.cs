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
public class CPIForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("HelpButton1")]
	private Button _HelpButton1;

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
	[AccessedThroughProperty("Chart1")]
	private Chart _Chart1;

	[CompilerGenerated]
	[AccessedThroughProperty("BrowseButton")]
	private Button _BrowseButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ShowChangesRB")]
	private RadioButton _ShowChangesRB;

	[CompilerGenerated]
	[AccessedThroughProperty("ShowAllSignalsRB")]
	private RadioButton _ShowAllSignalsRB;

	[CompilerGenerated]
	[AccessedThroughProperty("ShowIndicatorOnlyRB")]
	private RadioButton _ShowIndicatorOnlyRB;

	[CompilerGenerated]
	[AccessedThroughProperty("ClipboardButton")]
	private Button _ClipboardButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ResultsButton")]
	private Button _ResultsButton;

	private const int WAITBKOUT = 3;

	private const int DATEINDEX = 2;

	private const int BULLINDEX = 0;

	private const int BEARINDEX = 1;

	private const int SHOWCHANGES = 0;

	private const int SHOWALL = 1;

	private const int SHOWNONE = 2;

	private const int BULLISH = 1;

	private const int BEARISH = -1;

	private bool StopPressed;

	private DateTime EndDate;

	private DateTime StartDate;

	private object[,] List;

	private readonly string IndexMessage;

	private Point StartPoint;

	private Point EndPoint;

	private bool Crosshair;

	private Point CrosshairPoint;

	private Pen CrosshairPen;

	private bool LockFlag;

	private int lsChartPeriodShown;

	private bool lsVolumeChecked;

	private bool CPIAvailable;

	private string Finn;

	private CalloutAnnotation CurrentAnnotation;

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
			MouseEventHandler val2 = new MouseEventHandler(Chart1_MouseMove);
			MouseEventHandler val3 = new MouseEventHandler(Chart1_MouseUp);
			PaintEventHandler val4 = new PaintEventHandler(Chart1_Paint);
			Chart val5 = _Chart1;
			if (val5 != null)
			{
				((Control)val5).MouseDown -= val;
				((Control)val5).MouseMove -= val2;
				((Control)val5).MouseUp -= val3;
				((Control)val5).Paint -= val4;
			}
			_Chart1 = value;
			val5 = _Chart1;
			if (val5 != null)
			{
				((Control)val5).MouseDown += val;
				((Control)val5).MouseMove += val2;
				((Control)val5).MouseUp += val3;
				((Control)val5).Paint += val4;
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

	[field: AccessedThroughProperty("ProgressBar1")]
	internal virtual ProgressBar ProgressBar1
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

	[field: AccessedThroughProperty("Label2")]
	internal virtual Label Label2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("ResultsLabel")]
	internal virtual Label ResultsLabel
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

	[field: AccessedThroughProperty("OpenFileDialog1")]
	internal virtual OpenFileDialog OpenFileDialog1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton ShowChangesRB
	{
		[CompilerGenerated]
		get
		{
			return _ShowChangesRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShowIndicatorOnlyRB_CheckedChanged;
			RadioButton val = _ShowChangesRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_ShowChangesRB = value;
			val = _ShowChangesRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual RadioButton ShowAllSignalsRB
	{
		[CompilerGenerated]
		get
		{
			return _ShowAllSignalsRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShowIndicatorOnlyRB_CheckedChanged;
			RadioButton val = _ShowAllSignalsRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_ShowAllSignalsRB = value;
			val = _ShowAllSignalsRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual RadioButton ShowIndicatorOnlyRB
	{
		[CompilerGenerated]
		get
		{
			return _ShowIndicatorOnlyRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShowIndicatorOnlyRB_CheckedChanged;
			RadioButton val = _ShowIndicatorOnlyRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_ShowIndicatorOnlyRB = value;
			val = _ShowIndicatorOnlyRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

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

	public CPIForm()
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		//IL_006e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0078: Expected O, but got Unknown
		((Form)this).FormClosing += new FormClosingEventHandler(CPIForm_FormClosing);
		((Form)this).Load += CPIForm_Load;
		((Form)this).Activated += CPIForm_Activated;
		List = new object[4, 1];
		IndexMessage = "The index symbol cannot be found. Please enter a valid symbol of a stock market index in the index text box.";
		Crosshair = false;
		CrosshairPen = null;
		Finn = "";
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
		//IL_0018: Unknown result type (might be due to invalid IL or missing references)
		//IL_001f: Expected O, but got Unknown
		//IL_0020: Unknown result type (might be due to invalid IL or missing references)
		//IL_002a: Expected O, but got Unknown
		//IL_002b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0035: Expected O, but got Unknown
		//IL_0036: Unknown result type (might be due to invalid IL or missing references)
		//IL_0040: Expected O, but got Unknown
		//IL_0041: Unknown result type (might be due to invalid IL or missing references)
		//IL_004b: Expected O, but got Unknown
		//IL_004c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0056: Expected O, but got Unknown
		//IL_0057: Unknown result type (might be due to invalid IL or missing references)
		//IL_0061: Expected O, but got Unknown
		//IL_0062: Unknown result type (might be due to invalid IL or missing references)
		//IL_006c: Expected O, but got Unknown
		//IL_006d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0077: Expected O, but got Unknown
		//IL_0078: Unknown result type (might be due to invalid IL or missing references)
		//IL_0082: Expected O, but got Unknown
		//IL_0083: Unknown result type (might be due to invalid IL or missing references)
		//IL_008d: Expected O, but got Unknown
		//IL_008e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0098: Expected O, but got Unknown
		//IL_0099: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a3: Expected O, but got Unknown
		//IL_00a4: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ae: Expected O, but got Unknown
		//IL_00af: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b9: Expected O, but got Unknown
		//IL_00ba: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c4: Expected O, but got Unknown
		//IL_00c5: Unknown result type (might be due to invalid IL or missing references)
		//IL_00cf: Expected O, but got Unknown
		//IL_00d0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00da: Expected O, but got Unknown
		//IL_00db: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e5: Expected O, but got Unknown
		//IL_00e6: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f0: Expected O, but got Unknown
		//IL_00f1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00fb: Expected O, but got Unknown
		//IL_0443: Unknown result type (might be due to invalid IL or missing references)
		ChartArea val = new ChartArea();
		Series val2 = new Series();
		Series val3 = new Series();
		Series val4 = new Series();
		Series val5 = new Series();
		HelpButton1 = new Button();
		StartButton = new Button();
		StopButton = new Button();
		DoneButton = new Button();
		Chart1 = new Chart();
		Label1 = new Label();
		SymbolTextBox = new TextBox();
		ProgressBar1 = new ProgressBar();
		Label3 = new Label();
		Label2 = new Label();
		ResultsLabel = new Label();
		BrowseButton = new Button();
		OpenFileDialog1 = new OpenFileDialog();
		ShowChangesRB = new RadioButton();
		ShowAllSignalsRB = new RadioButton();
		ShowIndicatorOnlyRB = new RadioButton();
		ToDatePicker = new DateTimePicker();
		FromDatePicker = new DateTimePicker();
		ClipboardButton = new Button();
		ResultsButton = new Button();
		((ISupportInitialize)Chart1).BeginInit();
		((Control)this).SuspendLayout();
		((Control)HelpButton1).Anchor = (AnchorStyles)10;
		((Control)HelpButton1).Location = new Point(858, 440);
		((Control)HelpButton1).Name = "HelpButton1";
		((Control)HelpButton1).Size = new Size(60, 23);
		((Control)HelpButton1).TabIndex = 16;
		((ButtonBase)HelpButton1).Text = "&Help";
		((ButtonBase)HelpButton1).UseVisualStyleBackColor = true;
		((Control)StartButton).Anchor = (AnchorStyles)10;
		((Control)StartButton).Location = new Point(792, 468);
		((Control)StartButton).Name = "StartButton";
		((Control)StartButton).Size = new Size(60, 23);
		((Control)StartButton).TabIndex = 0;
		((ButtonBase)StartButton).Text = "St&art";
		((ButtonBase)StartButton).UseVisualStyleBackColor = true;
		((Control)StopButton).Anchor = (AnchorStyles)10;
		((Control)StopButton).Enabled = false;
		((Control)StopButton).Location = new Point(792, 440);
		((Control)StopButton).Name = "StopButton";
		((Control)StopButton).Size = new Size(60, 23);
		((Control)StopButton).TabIndex = 15;
		((ButtonBase)StopButton).Text = "St&op";
		((ButtonBase)StopButton).UseVisualStyleBackColor = true;
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(858, 468);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(60, 23);
		((Control)DoneButton).TabIndex = 1;
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
		val.AxisY2.Enabled = (AxisEnabled)2;
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
		((Control)Chart1).Location = new Point(12, 9);
		((Control)Chart1).Margin = new Padding(0);
		((Control)Chart1).Name = "Chart1";
		((Control)Chart1).RightToLeft = (RightToLeft)0;
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
		val3.ChartArea = "ChartArea1";
		val3.ChartType = (SeriesChartType)3;
		((DataPointCustomProperties)val3).Color = Color.Blue;
		val3.IsXValueIndexed = true;
		val3.Name = "CPILine";
		val3.XValueType = (ChartValueType)8;
		val4.ChartArea = "ChartArea1";
		((DataPointCustomProperties)val4).Color = Color.Green;
		val4.IsXValueIndexed = true;
		val4.Name = "CPIBull";
		val4.XValueType = (ChartValueType)8;
		val4.YAxisType = (AxisType)1;
		val4.YValuesPerPoint = 3;
		val5.ChartArea = "ChartArea1";
		((DataPointCustomProperties)val5).Color = Color.Red;
		val5.IsXValueIndexed = true;
		val5.Name = "CPIBear";
		val5.XValueType = (ChartValueType)8;
		val5.YAxisType = (AxisType)1;
		val5.YValuesPerPoint = 3;
		((Collection<Series>)(object)Chart1.Series).Add(val2);
		((Collection<Series>)(object)Chart1.Series).Add(val3);
		((Collection<Series>)(object)Chart1.Series).Add(val4);
		((Collection<Series>)(object)Chart1.Series).Add(val5);
		Chart1.Size = new Size(906, 425);
		((Control)Chart1).TabIndex = 2;
		((Control)Chart1).Text = "Chart1";
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(628, 444);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(36, 13);
		((Control)Label1).TabIndex = 12;
		Label1.Text = "Inde&x:";
		((Control)SymbolTextBox).Anchor = (AnchorStyles)10;
		((Control)SymbolTextBox).Location = new Point(670, 441);
		((Control)SymbolTextBox).Name = "SymbolTextBox";
		((Control)SymbolTextBox).Size = new Size(52, 20);
		((Control)SymbolTextBox).TabIndex = 13;
		((Control)ProgressBar1).Anchor = (AnchorStyles)14;
		((Control)ProgressBar1).ForeColor = Color.Green;
		((Control)ProgressBar1).Location = new Point(9, 440);
		((Control)ProgressBar1).Name = "ProgressBar1";
		((Control)ProgressBar1).Size = new Size(323, 20);
		((Control)ProgressBar1).TabIndex = 3;
		((Control)Label3).Anchor = (AnchorStyles)10;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(348, 468);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(23, 13);
		((Control)Label3).TabIndex = 7;
		Label3.Text = "&To:";
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(338, 444);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(33, 13);
		((Control)Label2).TabIndex = 5;
		Label2.Text = "&From:";
		((Control)ResultsLabel).Anchor = (AnchorStyles)14;
		ResultsLabel.BorderStyle = (BorderStyle)2;
		((Control)ResultsLabel).Location = new Point(11, 463);
		((Control)ResultsLabel).Name = "ResultsLabel";
		((Control)ResultsLabel).Size = new Size(323, 30);
		((Control)ResultsLabel).TabIndex = 4;
		ResultsLabel.TextAlign = (ContentAlignment)32;
		((Control)BrowseButton).Anchor = (AnchorStyles)10;
		((Control)BrowseButton).Location = new Point(726, 440);
		((Control)BrowseButton).Name = "BrowseButton";
		((Control)BrowseButton).Size = new Size(60, 23);
		((Control)BrowseButton).TabIndex = 14;
		((ButtonBase)BrowseButton).Text = "&Browse";
		((ButtonBase)BrowseButton).UseVisualStyleBackColor = true;
		((FileDialog)OpenFileDialog1).DefaultExt = "csv";
		((FileDialog)OpenFileDialog1).FileName = "OpenFileDialog1";
		((Control)ShowChangesRB).Anchor = (AnchorStyles)10;
		((ButtonBase)ShowChangesRB).AutoSize = true;
		ShowChangesRB.Checked = true;
		((Control)ShowChangesRB).Location = new Point(504, 440);
		((Control)ShowChangesRB).Name = "ShowChangesRB";
		((Control)ShowChangesRB).Size = new Size(118, 17);
		((Control)ShowChangesRB).TabIndex = 9;
		ShowChangesRB.TabStop = true;
		((Control)ShowChangesRB).Tag = "0";
		((ButtonBase)ShowChangesRB).Text = "&Show changes only";
		((ButtonBase)ShowChangesRB).UseVisualStyleBackColor = true;
		((Control)ShowAllSignalsRB).Anchor = (AnchorStyles)10;
		((ButtonBase)ShowAllSignalsRB).AutoSize = true;
		((Control)ShowAllSignalsRB).Location = new Point(504, 457);
		((Control)ShowAllSignalsRB).Name = "ShowAllSignalsRB";
		((Control)ShowAllSignalsRB).Size = new Size(100, 17);
		((Control)ShowAllSignalsRB).TabIndex = 10;
		((Control)ShowAllSignalsRB).Tag = "1";
		((ButtonBase)ShowAllSignalsRB).Text = "Sho&w all signals";
		((ButtonBase)ShowAllSignalsRB).UseVisualStyleBackColor = true;
		((Control)ShowIndicatorOnlyRB).Anchor = (AnchorStyles)10;
		((ButtonBase)ShowIndicatorOnlyRB).AutoSize = true;
		((Control)ShowIndicatorOnlyRB).Location = new Point(504, 473);
		((Control)ShowIndicatorOnlyRB).Name = "ShowIndicatorOnlyRB";
		((Control)ShowIndicatorOnlyRB).Size = new Size(117, 17);
		((Control)ShowIndicatorOnlyRB).TabIndex = 11;
		((Control)ShowIndicatorOnlyRB).Tag = "2";
		((ButtonBase)ShowIndicatorOnlyRB).Text = "Show i&ndicator only";
		((ButtonBase)ShowIndicatorOnlyRB).UseVisualStyleBackColor = true;
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(378, 467);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(120, 20);
		((Control)ToDatePicker).TabIndex = 8;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(378, 441);
		((Control)FromDatePicker).Name = "FromDatePicker";
		FromDatePicker.ShowUpDown = true;
		((Control)FromDatePicker).Size = new Size(120, 20);
		((Control)FromDatePicker).TabIndex = 6;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)ClipboardButton).Anchor = (AnchorStyles)10;
		((Control)ClipboardButton).Enabled = false;
		((Control)ClipboardButton).Location = new Point(726, 468);
		((Control)ClipboardButton).Name = "ClipboardButton";
		((Control)ClipboardButton).Size = new Size(60, 23);
		((Control)ClipboardButton).TabIndex = 18;
		((ButtonBase)ClipboardButton).Text = "Clip&board";
		((ButtonBase)ClipboardButton).UseVisualStyleBackColor = true;
		((Control)ResultsButton).Anchor = (AnchorStyles)10;
		((Control)ResultsButton).Enabled = false;
		((Control)ResultsButton).Location = new Point(660, 468);
		((Control)ResultsButton).Name = "ResultsButton";
		((Control)ResultsButton).Size = new Size(60, 23);
		((Control)ResultsButton).TabIndex = 17;
		((ButtonBase)ResultsButton).Text = "&Results";
		((ButtonBase)ResultsButton).UseVisualStyleBackColor = true;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(924, 493);
		((Control)this).Controls.Add((Control)(object)ResultsButton);
		((Control)this).Controls.Add((Control)(object)ClipboardButton);
		((Control)this).Controls.Add((Control)(object)ToDatePicker);
		((Control)this).Controls.Add((Control)(object)FromDatePicker);
		((Control)this).Controls.Add((Control)(object)ShowIndicatorOnlyRB);
		((Control)this).Controls.Add((Control)(object)ShowAllSignalsRB);
		((Control)this).Controls.Add((Control)(object)ShowChangesRB);
		((Control)this).Controls.Add((Control)(object)BrowseButton);
		((Control)this).Controls.Add((Control)(object)ResultsLabel);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)ProgressBar1);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)SymbolTextBox);
		((Control)this).Controls.Add((Control)(object)Chart1);
		((Control)this).Controls.Add((Control)(object)HelpButton1);
		((Control)this).Controls.Add((Control)(object)StartButton);
		((Control)this).Controls.Add((Control)(object)StopButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Name = "CPIForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "CPI Form";
		((ISupportInitialize)Chart1).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void CPIForm_FormClosing(object sender, FormClosingEventArgs e)
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
		GlobalForm.ChartPeriodShown = lsChartPeriodShown;
		GlobalForm.ChartVolume = lsVolumeChecked;
		if (Operators.CompareString(GlobalForm.IndexSymbol, SymbolTextBox.Text, false) != 0)
		{
			GlobalForm.IndexSymbol = SymbolTextBox.Text;
		}
		StartDate = FromDatePicker.Value;
		EndDate = ToDatePicker.Value;
		if (DateTime.Compare(EndDate, StartDate) < 0)
		{
			GlobalForm.CPIDateLookback = DateAndTime.DateDiff((DateInterval)4, EndDate, StartDate, (FirstDayOfWeek)1, (FirstWeekOfYear)1);
		}
		else
		{
			GlobalForm.CPIDateLookback = DateAndTime.DateDiff((DateInterval)4, StartDate, EndDate, (FirstDayOfWeek)1, (FirstWeekOfYear)1);
		}
		if (ShowChangesRB.Checked)
		{
			GlobalForm.RadButton = Conversions.ToInteger(((Control)ShowChangesRB).Tag);
		}
		if (ShowAllSignalsRB.Checked)
		{
			GlobalForm.RadButton = Conversions.ToInteger(((Control)ShowAllSignalsRB).Tag);
		}
		if (ShowIndicatorOnlyRB.Checked)
		{
			GlobalForm.RadButton = Conversions.ToInteger(((Control)ShowIndicatorOnlyRB).Tag);
		}
		MySettingsProperty.Settings.CPIFormLocation = ((Form)this).Location;
		MySettingsProperty.Settings.CPIFormSize = ((Form)this).Size;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
		LockFlag = false;
	}

	private void CPIForm_Load(object sender, EventArgs e)
	{
		//IL_005c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0061: Unknown result type (might be due to invalid IL or missing references)
		//IL_006c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0077: Unknown result type (might be due to invalid IL or missing references)
		//IL_0082: Unknown result type (might be due to invalid IL or missing references)
		//IL_0089: Unknown result type (might be due to invalid IL or missing references)
		//IL_009a: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ab: Unknown result type (might be due to invalid IL or missing references)
		//IL_00bc: Unknown result type (might be due to invalid IL or missing references)
		//IL_00cd: Unknown result type (might be due to invalid IL or missing references)
		//IL_00de: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ef: Unknown result type (might be due to invalid IL or missing references)
		//IL_0100: Unknown result type (might be due to invalid IL or missing references)
		//IL_0111: Unknown result type (might be due to invalid IL or missing references)
		//IL_0122: Unknown result type (might be due to invalid IL or missing references)
		//IL_0133: Unknown result type (might be due to invalid IL or missing references)
		//IL_0144: Unknown result type (might be due to invalid IL or missing references)
		//IL_0155: Unknown result type (might be due to invalid IL or missing references)
		//IL_0166: Unknown result type (might be due to invalid IL or missing references)
		//IL_0023: Unknown result type (might be due to invalid IL or missing references)
		//IL_002d: Expected O, but got Unknown
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.CPIFormLocation, MySettingsProperty.Settings.CPIFormSize);
		if (CurrentAnnotation == null)
		{
			CurrentAnnotation = new CalloutAnnotation();
		}
		((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)CurrentAnnotation);
		CPIAvailable = false;
		LockFlag = false;
		lsVolumeChecked = GlobalForm.ChartVolume;
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)BrowseButton, "Select a file to be used as the market index.");
		val.SetToolTip((Control)(object)FromDatePicker, "Enter the starting date for calculating the indicator.");
		val.SetToolTip((Control)(object)Chart1, "Chart the index and indicator here.");
		val.SetToolTip((Control)(object)ClipboardButton, "After completing scan, copy numerical results to clipboard.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)ToDatePicker, "Enter the ending date for calculating the indicator.");
		val.SetToolTip((Control)(object)HelpButton1, "Get help.");
		val.SetToolTip((Control)(object)ProgressBar1, "Show the progress of loading files.");
		val.SetToolTip((Control)(object)ResultsButton, "Show the results for the last week.");
		val.SetToolTip((Control)(object)StartButton, "Begin the indicator calculation.");
		val.SetToolTip((Control)(object)StopButton, "Stop the indicator calculation.");
		val.SetToolTip((Control)(object)SymbolTextBox, "Enter one symbol (often an index) to chart against the CPI indicator.");
		val.SetToolTip((Control)(object)ShowChangesRB, "Show only the indicator signal changes.");
		val.SetToolTip((Control)(object)ShowAllSignalsRB, "Shows all indicator signals.");
		val.SetToolTip((Control)(object)ShowIndicatorOnlyRB, "Do not show any indicator signal changes.");
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Clear();
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPILine"].Points).Clear();
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBull"].Points).Clear();
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBear"].Points).Clear();
		ProgressBar1.Value = 0;
		SymbolTextBox.Text = "";
	}

	private void CPIForm_Activated(object sender, EventArgs e)
	{
		//IL_01e9: Unknown result type (might be due to invalid IL or missing references)
		if (LockFlag)
		{
			return;
		}
		LockFlag = true;
		GlobalForm.FirstPoint = default(Point);
		GlobalForm.LinesList.RemoveAll(StubBoolean);
		((Control)FromDatePicker).Enabled = false;
		((Control)BrowseButton).Enabled = false;
		((Control)ClipboardButton).Enabled = false;
		((Control)DoneButton).Enabled = false;
		((Control)ToDatePicker).Enabled = false;
		((Control)HelpButton1).Enabled = false;
		((Control)ResultsButton).Enabled = false;
		((Control)StartButton).Enabled = false;
		((Control)StopButton).Enabled = false;
		((Control)ShowChangesRB).Enabled = false;
		((Control)ShowAllSignalsRB).Enabled = false;
		((Control)ShowIndicatorOnlyRB).Enabled = false;
		SymbolTextBox.Text = GlobalForm.IndexSymbol;
		((Control)SymbolTextBox).Enabled = false;
		ResultsLabel.Text = "Loading index file. If slow, then file is too long (2 years long works good).";
		int radButton = GlobalForm.RadButton;
		if (radButton == Conversions.ToInteger(((Control)ShowChangesRB).Tag))
		{
			ShowChangesRB.Checked = true;
		}
		else if (radButton == Conversions.ToInteger(((Control)ShowAllSignalsRB).Tag))
		{
			ShowAllSignalsRB.Checked = true;
		}
		else if (radButton == Conversions.ToInteger(((Control)ShowIndicatorOnlyRB).Tag))
		{
			ShowIndicatorOnlyRB.Checked = true;
		}
		((Control)this).Refresh();
		string text = SymbolTextBox.Text + ".csv";
		if (!((ServerComputer)MyProject.Computer).FileSystem.FileExists(GlobalForm.OpenPath + "\\" + text))
		{
			text = SymbolTextBox.Text + ".txt";
			if (!((ServerComputer)MyProject.Computer).FileSystem.FileExists(GlobalForm.OpenPath + "\\" + text))
			{
				ResultsLabel.Text = "";
				MessageBox.Show(IndexMessage, "CPIForm_Load", (MessageBoxButtons)0, (MessageBoxIcon)16);
				((Control)SymbolTextBox).Enabled = true;
				((Control)SymbolTextBox).Focus();
				goto IL_0511;
			}
		}
		lsChartPeriodShown = GlobalForm.ChartPeriodShown;
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Clear();
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPILine"].Points).Clear();
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBull"].Points).Clear();
		((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBear"].Points).Clear();
		try
		{
			string fileName = text;
			ProgressBar ProgBar = ProgressBar1;
			Label ErrorLabel = null;
			GlobalForm.LoadFile(fileName, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
			ProgressBar1 = ProgBar;
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
		GlobalForm.SelectChartType(Chart1);
		GlobalForm.CPIDateLookback = Conversions.ToInteger(Interaction.IIf(GlobalForm.CPIDateLookback == 0, (object)262, (object)GlobalForm.CPIDateLookback));
		checked
		{
			if (GlobalForm.IntradayData)
			{
				if (GlobalForm.HLCRange - GlobalForm.CPIDateLookback > 0)
				{
					if ((DateTime.Compare(GlobalForm.nDT[0, (int)(GlobalForm.HLCRange - GlobalForm.CPIDateLookback)], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, (int)(GlobalForm.HLCRange - GlobalForm.CPIDateLookback)], FromDatePicker.MaxDate) <= 0))
					{
						FromDatePicker.Value = GlobalForm.nDT[0, (int)(GlobalForm.HLCRange - GlobalForm.CPIDateLookback)];
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
				FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)(-1 * GlobalForm.CPIDateLookback), DateAndTime.Now);
				ToDatePicker.Value = DateAndTime.Now;
			}
			ToDatePicker.Value = DateAndTime.Now;
			StartDate = FromDatePicker.Value;
			EndDate = ToDatePicker.Value;
			GlobalForm.ShowStock(Chart1, StartDate, EndDate, VolumeFlag: false, MAFlag: false);
			if (GlobalForm.ErrorCount > 0)
			{
				ResultsLabel.Text = "There were " + Strings.Format((object)GlobalForm.ErrorCount, "") + " read errors. They are on the clipboard.";
			}
			else if (GlobalForm.IntradayData)
			{
				ResultsLabel.Text = "Note: The indicator works best with daily price data.";
			}
			else
			{
				ResultsLabel.Text = "";
			}
			goto IL_0511;
		}
		IL_0511:
		((Control)BrowseButton).Enabled = true;
		((Control)FromDatePicker).Enabled = true;
		((Control)DoneButton).Enabled = true;
		((Control)ToDatePicker).Enabled = true;
		((Control)HelpButton1).Enabled = true;
		((Control)StartButton).Enabled = true;
		((Control)StopButton).Enabled = false;
		((Control)SymbolTextBox).Enabled = true;
		((Control)ShowChangesRB).Enabled = true;
		((Control)ShowAllSignalsRB).Enabled = true;
		((Control)ShowIndicatorOnlyRB).Enabled = true;
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
			Title = "Select the file to be used as the market index. DO NOT CHANGE FOLDERS",
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
				MessageBox.Show("The path you selected for the index file is not the same as where the rest of the files are located. The index file must be in the same folder (manually move the file to " + GlobalForm.OpenPath + " and click Browse again or select a different index file).", "BrowseButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)16);
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
			ResultsLabel.Text = "Loading index file. If slow, then file is too long (2 years works best).";
			((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Clear();
			((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPILine"].Points).Clear();
			((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBull"].Points).Clear();
			((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBear"].Points).Clear();
			string fileName = text2 + text;
			ProgressBar ProgBar = ProgressBar1;
			Label ErrorLabel = null;
			GlobalForm.LoadFile(fileName, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
			ProgressBar1 = ProgBar;
			GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
			GlobalForm.SelectChartType(Chart1);
			GlobalForm.ShowStock(Chart1, StartDate, EndDate, VolumeFlag: false, MAFlag: false);
			ResultsLabel.Text = "";
		}
	}

	private void BuildCPI()
	{
		int HighestHigh = 0;
		int LowestLow = 0;
		int num = 0;
		bool flag = true;
		checked
		{
			try
			{
				int hLCRange = GlobalForm.HLCRange;
				int Direction = default(int);
				int BkoutIndex = default(int);
				for (int i = 6; i <= hLCRange; i++)
				{
					if ((DateTime.Compare(GlobalForm.nDT[0, i], StartDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, i], EndDate) <= 0))
					{
						if (flag)
						{
							flag = false;
							num = i;
						}
						if (!FindNR7(i, ref HighestHigh, ref LowestLow, ref Direction, ref BkoutIndex))
						{
							continue;
						}
						if (BkoutIndex != -1)
						{
							int num2 = i;
							int num3 = BkoutIndex;
							for (int j = num2; j <= num3; j++)
							{
								FindIndex(j - num, GlobalForm.nDT[0, j], Direction);
							}
							continue;
						}
						DateTime t = DateAndTime.DateAdd((DateInterval)4, 7.0, GlobalForm.nDT[0, i]);
						int num4 = i;
						int hLCRange2 = GlobalForm.HLCRange;
						for (int j = num4; j <= hLCRange2 && DateTime.Compare(GlobalForm.nDT[0, j], t) <= 0; j++)
						{
							FindIndex(j - num, GlobalForm.nDT[0, j], 0);
						}
					}
					else if (DateTime.Compare(GlobalForm.nDT[0, i], EndDate) > 0)
					{
						break;
					}
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				ResultsLabel.Text = Finn + ". BuildCPI: " + ex2.Message;
				((Control)ResultsLabel).Refresh();
				ProjectData.ClearProjectError();
			}
		}
	}

	private void ClipboardButton_Click(object sender, EventArgs e)
	{
		//IL_01dc: Unknown result type (might be due to invalid IL or missing references)
		//IL_0225: Unknown result type (might be due to invalid IL or missing references)
		//IL_0211: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			if (Information.UBound((Array)List, 2) > 0)
			{
				((Control)this).Cursor = Cursors.WaitCursor;
				ResultsLabel.Text = "Working . . .";
				((Control)ResultsLabel).Refresh();
				string text = "Date\tBull Total\tBear Total\tCPI\tStatus\tNR7s Awaiting Breakout\r\n";
				int num = Information.UBound((Array)List, 2);
				for (int i = 0; i <= num; i++)
				{
					int num2 = Conversions.ToInteger(List[0, i]);
					int num3 = Conversions.ToInteger(List[1, i]);
					text = text + Strings.Format(RuntimeHelpers.GetObjectValue(List[2, i]), GlobalForm.UserDate) + "\t";
					text = text + num2 + "\t";
					text = text + num3 + "\t";
					if (num2 + num3 > 0)
					{
						int num4 = (int)Math.Round((double)(100 * num2) / (double)(num2 + num3));
						text = text + Strings.Format((object)((double)num4 / 100.0), "0%") + "\t";
						int num5 = num4;
						text = ((num5 >= 36) ? ((num5 <= 64) ? (text + "Neutral") : (text + "Bullish")) : (text + "Bearish"));
					}
					else
					{
						text += "50%\tNeutral";
					}
					text = text + "\t" + Strings.Format((object)Conversions.ToInteger(Interaction.IIf(Information.IsNothing(RuntimeHelpers.GetObjectValue(List[3, i])), (object)0, RuntimeHelpers.GetObjectValue(List[3, i]))), "") + "\r\n";
				}
				try
				{
					Clipboard.SetText(text);
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					MessageBox.Show("Clipboard is busy with another user. Error: " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
					ProjectData.ClearProjectError();
				}
				ResultsLabel.Text = "";
				((Control)this).Cursor = Cursors.Default;
				MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
			else
			{
				MessageBox.Show("CPI results are not available.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			}
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

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private int FindDate(int Index, DateTime PointDate)
	{
		int num = Information.UBound((Array)List, 2);
		for (int i = Index; i <= num; i = checked(i + 1))
		{
			if (GlobalForm.IntradayData)
			{
				if (DateTime.Compare(GlobalForm.MyCDate(RuntimeHelpers.GetObjectValue(List[2, i])), PointDate) == 0)
				{
					return i;
				}
			}
			else if (DateTime.Compare(GlobalForm.MyCDate(RuntimeHelpers.GetObjectValue(List[2, i])).Date, PointDate.Date) == 0)
			{
				return i;
			}
		}
		return -1;
	}

	private void FindIndex(int ListIndex, DateTime NewDate, int Direction)
	{
		if (ListIndex > Information.UBound((Array)List, 2))
		{
			return;
		}
		int num = Information.UBound((Array)List, 2);
		int num2 = ListIndex;
		checked
		{
			while (true)
			{
				if (num2 <= num)
				{
					if (DateTime.Compare(NewDate, GlobalForm.MyCDate(RuntimeHelpers.GetObjectValue(List[2, num2]))) == 0)
					{
						if (Direction == 1)
						{
							List[0, num2] = Conversions.ToInteger(List[0, num2]) + 1;
						}
						if (Direction == -1)
						{
							List[1, num2] = Conversions.ToInteger(List[1, num2]) + 1;
						}
						if (Direction == 0)
						{
							List[3, num2] = Conversions.ToInteger(List[3, num2]) + 1;
						}
						break;
					}
					if (DateTime.Compare(GlobalForm.MyCDate(RuntimeHelpers.GetObjectValue(List[2, num2])), NewDate) <= 0)
					{
						num2++;
						continue;
					}
				}
				for (num2 = ListIndex - 1; num2 >= 0; num2 += -1)
				{
					if (DateTime.Compare(NewDate, GlobalForm.MyCDate(RuntimeHelpers.GetObjectValue(List[2, num2]))) == 0)
					{
						if (Direction == 1)
						{
							List[0, num2] = Conversions.ToInteger(List[0, num2]) + 1;
						}
						if (Direction == -1)
						{
							List[1, num2] = Conversions.ToInteger(List[1, num2]) + 1;
						}
						if (Direction == 0)
						{
							List[3, num2] = Conversions.ToInteger(List[3, num2]) + 1;
						}
						break;
					}
					if (DateTime.Compare(GlobalForm.MyCDate(RuntimeHelpers.GetObjectValue(List[2, num2])), NewDate) < 0)
					{
						break;
					}
				}
				break;
			}
		}
	}

	private bool FindNR7(int i, ref int HighestHigh, ref int LowestLow, ref int Direction, ref int BkoutIndex)
	{
		bool result = false;
		decimal d = decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]);
		checked
		{
			if ((decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[2, i - 1])) < 0) & (decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 2], GlobalForm.nHLC[2, i - 2])) < 0) & (decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 3], GlobalForm.nHLC[2, i - 3])) < 0) & (decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 4], GlobalForm.nHLC[2, i - 4])) < 0) & (decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 5], GlobalForm.nHLC[2, i - 5])) < 0) & (decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 6], GlobalForm.nHLC[2, i - 6])) < 0))
			{
				result = true;
				Direction = 0;
				BkoutIndex = -1;
				HighestHigh = i;
				LowestLow = i;
				int num = i + 7;
				if (num > GlobalForm.HLCRange)
				{
					num = GlobalForm.HLCRange;
				}
				DateTime t = DateAndTime.DateAdd((DateInterval)4, 7.0, GlobalForm.nDT[0, i]);
				int num2 = i - 6;
				int num3 = num;
				for (int j = num2; j <= num3; j++)
				{
					if (j <= i)
					{
						if (decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, HighestHigh]) > 0)
						{
							HighestHigh = j;
						}
						if ((decimal.Compare(GlobalForm.nHLC[2, j], 0m) != 0) & (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, LowestLow]) < 0))
						{
							LowestLow = j;
						}
						continue;
					}
					if (DateTime.Compare(GlobalForm.nDT[0, j], t) > 0)
					{
						return true;
					}
					if (decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[1, HighestHigh]) > 0)
					{
						Direction = 1;
						BkoutIndex = j;
						return result;
					}
					if (decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[2, LowestLow]) < 0)
					{
						Direction = -1;
						BkoutIndex = j;
						return result;
					}
				}
			}
			return result;
		}
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.HelpCPIForm).ShowDialog();
	}

	private void ResultsButton_Click(object sender, EventArgs e)
	{
		//IL_035c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0348: Unknown result type (might be due to invalid IL or missing references)
		int num = 0;
		checked
		{
			if (Information.UBound((Array)List, 2) > 5)
			{
				MyProject.Forms.BigMessageBox.DataGridView1.RowCount = 0;
				int num2 = Information.UBound((Array)List, 2) - 6;
				int num3 = Information.UBound((Array)List, 2);
				for (int i = num2; i <= num3; i++)
				{
					MyProject.Forms.BigMessageBox.DataGridView1.Rows.Add();
					MyProject.Forms.BigMessageBox.DataGridView1.Rows[num].Cells[0].Value = Strings.Format(RuntimeHelpers.GetObjectValue(List[2, i]), GlobalForm.UserDate);
					int num4 = Conversions.ToInteger(List[0, i]);
					MyProject.Forms.BigMessageBox.DataGridView1.Rows[num].Cells[1].Value = num4;
					int num5 = Conversions.ToInteger(List[1, i]);
					MyProject.Forms.BigMessageBox.DataGridView1.Rows[num].Cells[2].Value = num5;
					string text = Strings.Format(RuntimeHelpers.GetObjectValue(Interaction.IIf(Information.IsNothing(RuntimeHelpers.GetObjectValue(List[3, i])), (object)0, (object)Conversions.ToInteger(List[3, i]))), "") + " or ";
					text += Strings.Format(RuntimeHelpers.GetObjectValue(Interaction.IIf(Information.IsNothing(RuntimeHelpers.GetObjectValue(List[3, i])), (object)0, (object)((double)Conversions.ToInteger(List[3, i]) / (double)(num4 + num5 + Conversions.ToInteger(List[3, i]))))), "0%");
					MyProject.Forms.BigMessageBox.DataGridView1.Rows[num].Cells[3].Value = text;
					if (num4 + num5 > 0)
					{
						int num6 = (int)Math.Round((double)(100 * num4) / (double)(num4 + num5));
						MyProject.Forms.BigMessageBox.DataGridView1.Rows[num].Cells[4].Value = Conversion.Str((object)num6) + "%";
						int num7 = num6;
						text = ((num7 < 36) ? "Bearish" : ((num7 <= 64) ? "Neutral" : "Bullish"));
						MyProject.Forms.BigMessageBox.DataGridView1.Rows[num].Cells[5].Value = text;
					}
					else
					{
						MyProject.Forms.BigMessageBox.DataGridView1.Rows[num].Cells[4].Value = "50%";
						MyProject.Forms.BigMessageBox.DataGridView1.Rows[num].Cells[5].Value = "Neutral";
					}
					num++;
				}
				((Form)MyProject.Forms.BigMessageBox).ShowDialog();
			}
			else
			{
				MessageBox.Show("CPI results are not available.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			}
		}
	}

	private void ShowCPI()
	{
		//IL_0798: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			try
			{
				if (((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Count == 0)
				{
					ResultsLabel.Text = "Error: Check your quote files.";
					return;
				}
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPILine"].Points).Clear();
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBull"].Points).Clear();
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBear"].Points).Clear();
				int num = 0;
				int num2 = 0;
				int num3 = 0;
				bool flag = ShowChangesRB.Checked;
				int num4 = ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Count - 1;
				DateTime dateTime = default(DateTime);
				for (int i = 0; i <= num4; i++)
				{
					DataPoint val = ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points)[i];
					dateTime = DateTime.FromOADate(val.XValue);
					decimal num5 = new decimal(val.YValues[1]);
					int num6 = FindDate(num3, dateTime);
					if (num6 != -1)
					{
						num3 = num6;
						if (Conversions.ToInteger(List[0, num3]) + Conversions.ToInteger(List[1, num3]) != 0)
						{
							num2 = (int)Math.Round((double)(100 * Conversions.ToInteger(List[0, num3])) / (double)(Conversions.ToInteger(List[0, num3]) + Conversions.ToInteger(List[1, num3])));
						}
						DateTime dateTime2 = GlobalForm.MyCDate(RuntimeHelpers.GetObjectValue(List[2, num3]));
						((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPILine"].Points.AddXY((object)dateTime2, new object[1] { num2 });
						unchecked
						{
							if (!ShowIndicatorOnlyRB.Checked)
							{
								if (num2 >= 65)
								{
									if (num == -1 || !flag)
									{
										((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBull"].Points.AddXY((object)dateTime2, new object[1] { num5 });
									}
									else
									{
										((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBull"].Points.AddXY((object)dateTime2, new object[1] { 0 });
									}
									((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBear"].Points.AddXY((object)dateTime2, new object[1] { 0 });
									num = 1;
								}
								else if (num2 <= 35)
								{
									if (num == 1 || !flag)
									{
										((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBear"].Points.AddXY((object)dateTime2, new object[1] { num5 });
									}
									else
									{
										((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBear"].Points.AddXY((object)dateTime2, new object[1] { 0 });
									}
									((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBull"].Points.AddXY((object)dateTime2, new object[1] { 0 });
									num = -1;
								}
								else
								{
									((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBull"].Points.AddXY((object)dateTime2, new object[1] { 0 });
									((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBear"].Points.AddXY((object)dateTime2, new object[1] { 0 });
								}
							}
							else
							{
								((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBull"].Points.AddXY((object)dateTime2, new object[1] { 0 });
								((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBear"].Points.AddXY((object)dateTime2, new object[1] { 0 });
							}
						}
					}
					else
					{
						((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPILine"].Points.AddXY((object)dateTime, new object[1] { num2 });
						((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBull"].Points.AddXY((object)dateTime, new object[1] { 0 });
						((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBear"].Points.AddXY((object)dateTime, new object[1] { 0 });
					}
					num3++;
				}
				ResultsLabel.Text = "CPI on " + Strings.Format((object)dateTime, GlobalForm.UserDate) + " is " + Strings.Format((object)num2, "") + ", ";
				Label resultsLabel;
				if (num2 >= 65)
				{
					(resultsLabel = ResultsLabel).Text = resultsLabel.Text + "bullish (>= 65";
				}
				else if (num2 <= 35)
				{
					(resultsLabel = ResultsLabel).Text = resultsLabel.Text + "bearish (<= 35";
				}
				else
				{
					(resultsLabel = ResultsLabel).Text = resultsLabel.Text + "neutral (36-64";
				}
				(resultsLabel = ResultsLabel).Text = resultsLabel.Text + "). Counts up: " + Strings.Format((object)Conversions.ToInteger(Interaction.IIf(Information.IsNothing(RuntimeHelpers.GetObjectValue(List[0, Information.UBound((Array)List, 2)])), (object)0, RuntimeHelpers.GetObjectValue(List[0, Information.UBound((Array)List, 2)]))), "") + ", down: " + Strings.Format((object)Conversions.ToInteger(Interaction.IIf(Information.IsNothing(RuntimeHelpers.GetObjectValue(List[1, Information.UBound((Array)List, 2)])), (object)0, RuntimeHelpers.GetObjectValue(List[1, Information.UBound((Array)List, 2)]))), "") + ", waiting breakout: " + Strings.Format((object)Conversions.ToInteger(Interaction.IIf(Information.IsNothing(RuntimeHelpers.GetObjectValue(List[3, Information.UBound((Array)List, 2)])), (object)0, RuntimeHelpers.GetObjectValue(List[3, Information.UBound((Array)List, 2)]))), "") + ". Signals can change for 1 week.";
				((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY.Maximum = 400.0;
				((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY.Minimum = 0.0;
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				MessageBox.Show("If you see a big red X on the chart, then the charting module has crashed. You'll have to exit Patternz and run it again to clear the error.\r\n\r\nTo prevent it from happening again, try running the CPI during a week day or change the end date to a week day. This is a bug I've been unable to fix.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				ProjectData.ClearProjectError();
			}
		}
	}

	private void ShowIndicatorOnlyRB_CheckedChanged(object sender, EventArgs e)
	{
		if (CPIAvailable)
		{
			ShowCPI();
		}
	}

	private void StartButton_Click(object sender, EventArgs e)
	{
		//IL_0844: Unknown result type (might be due to invalid IL or missing references)
		//IL_0086: Unknown result type (might be due to invalid IL or missing references)
		//IL_008c: Invalid comparison between Unknown and I4
		//IL_04cb: Unknown result type (might be due to invalid IL or missing references)
		//IL_0238: Unknown result type (might be due to invalid IL or missing references)
		//IL_07e9: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			try
			{
				GlobalForm.ErrorCount = 0;
				GlobalForm.ErrorMessage = null;
				string text = "";
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
				if (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.HLCRange], FromDatePicker.Value) < 0)
				{
					if (unchecked((int)MessageBox.Show("The index file doesn't have enough data to match the start or end date (Have the quote files been updated? Ideally, you'll want all files to end with the same date). Did you want me to change the start/end dates?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32)) != 6)
					{
						return;
					}
					if (GlobalForm.HLCRange - GlobalForm.CPIDateLookback >= 0)
					{
						FromDatePicker.Value = GlobalForm.nDT[0, (int)(GlobalForm.HLCRange - GlobalForm.CPIDateLookback)];
					}
					else
					{
						FromDatePicker.Value = GlobalForm.nDT[0, 0];
					}
					ToDatePicker.Value = GlobalForm.nDT[0, GlobalForm.HLCRange];
				}
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Clear();
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPILine"].Points).Clear();
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBull"].Points).Clear();
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CPIBear"].Points).Clear();
				GlobalForm.FirstPoint = default(Point);
				GlobalForm.LinesList.RemoveAll(StubBoolean);
				StartDate = FromDatePicker.Value;
				EndDate = ToDatePicker.Value;
				string text2 = SymbolTextBox.Text + ".csv";
				if (!((ServerComputer)MyProject.Computer).FileSystem.FileExists(GlobalForm.OpenPath + "\\" + text2))
				{
					text2 = SymbolTextBox.Text + ".txt";
					if (!((ServerComputer)MyProject.Computer).FileSystem.FileExists(GlobalForm.OpenPath + "\\" + text2))
					{
						MessageBox.Show(IndexMessage, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
						((Control)SymbolTextBox).Focus();
						ResultsLabel.Text = "";
						return;
					}
				}
				string text3 = Strings.UCase(text2);
				((Control)BrowseButton).Enabled = false;
				((Control)ClipboardButton).Enabled = false;
				((Control)FromDatePicker).Enabled = false;
				((Control)DoneButton).Enabled = false;
				((Control)ToDatePicker).Enabled = false;
				((Control)HelpButton1).Enabled = false;
				((Control)ResultsButton).Enabled = false;
				((Control)StartButton).Enabled = false;
				((Control)StopButton).Enabled = true;
				((Control)SymbolTextBox).Enabled = false;
				((Control)ShowChangesRB).Enabled = false;
				((Control)ShowAllSignalsRB).Enabled = false;
				((Control)ShowIndicatorOnlyRB).Enabled = false;
				GlobalForm.ShowStock(Chart1, StartDate, EndDate, VolumeFlag: false, MAFlag: false);
				List = null;
				if (GlobalForm.IntradayData)
				{
					List = new object[4, GlobalForm.ChartEndIndex - GlobalForm.ChartStartIndex + 1];
					try
					{
						int num2 = 0;
						int chartStartIndex = GlobalForm.ChartStartIndex;
						int chartEndIndex = GlobalForm.ChartEndIndex;
						for (int i = chartStartIndex; i <= chartEndIndex; i++)
						{
							List[2, num2] = GlobalForm.nDT[0, i];
							num2++;
						}
						ref object[,] list = ref List;
						list = (object[,])Utils.CopyArray((Array)list, (Array)new object[4, num2 - 1 + 1]);
					}
					catch (Exception ex)
					{
						ProjectData.SetProjectError(ex);
						Exception ex2 = ex;
						ProjectData.ClearProjectError();
					}
				}
				else
				{
					List = new object[4, (int)DateAndTime.DateDiff((DateInterval)4, StartDate, EndDate, (FirstDayOfWeek)1, (FirstWeekOfYear)1) + 1];
					try
					{
						int num3 = 0;
						int hLCRange = GlobalForm.HLCRange;
						for (int i = 0; i <= hLCRange; i++)
						{
							if ((DateTime.Compare(GlobalForm.nDT[0, i].Date, StartDate.Date) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, i].Date, EndDate.Date) <= 0))
							{
								List[2, num3] = GlobalForm.nDT[0, i].Date;
								num3++;
							}
						}
						ref object[,] list2 = ref List;
						list2 = (object[,])Utils.CopyArray((Array)list2, (Array)new object[4, num3 - 1 + 1]);
					}
					catch (Exception ex3)
					{
						ProjectData.SetProjectError(ex3);
						Exception ex4 = ex3;
						ProjectData.ClearProjectError();
					}
				}
				int num4 = default(int);
				if (Information.UBound((Array)List, 2) <= 0)
				{
					MessageBox.Show("The index file doesn't have enough data to match the start or end date. Has the quote file been updated? You can try adjusting the start and end dates.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
					GlobalForm.HideMessages = false;
					ProgressBar1.Value = 0;
					((Control)FromDatePicker).Enabled = true;
					((Control)BrowseButton).Enabled = true;
					if (num4 > 1)
					{
						((Control)ClipboardButton).Enabled = true;
						((Control)ResultsButton).Enabled = true;
					}
					((Control)DoneButton).Enabled = true;
					((Control)ToDatePicker).Enabled = true;
					((Control)HelpButton1).Enabled = true;
					((Control)StartButton).Enabled = true;
					((Control)StopButton).Enabled = false;
					((Control)SymbolTextBox).Enabled = true;
					((Control)ShowChangesRB).Enabled = true;
					((Control)ShowAllSignalsRB).Enabled = true;
					((Control)ShowIndicatorOnlyRB).Enabled = true;
					return;
				}
				ProgressBar1.Value = 1;
				StopPressed = false;
				num4 = MyProject.Forms.Mainform.ListBox1.SelectedItems.Count;
				GlobalForm.HideMessages = true;
				int num5 = num4 - 1;
				for (int i = 0; i <= num5; i++)
				{
					text2 = MyProject.Forms.Mainform.ListBox1.SelectedItems[i].ToString();
					if (Operators.CompareString(Strings.UCase(text2), text3, false) != 0)
					{
						ResultsLabel.Text = text2;
						((Control)ResultsLabel).Refresh();
						string fileName = text2;
						ProgressBar ProgBar = null;
						Label ErrorLabel = null;
						GlobalForm.LoadFile(fileName, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
						if (GlobalForm.ErrorMessage != null)
						{
							text = text + "\r\n" + GlobalForm.ErrorMessage;
						}
						Finn = text2;
						ResizeData();
						BuildCPI();
						ProgressBar1.Value = unchecked(i % 100);
						((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
						if (StopPressed)
						{
							break;
						}
					}
				}
				try
				{
					if (ResultsLabel.Text.Length > 0)
					{
						Clipboard.SetText(ResultsLabel.Text);
						ResultsLabel.Text = "Error messages are on the clipboard.";
					}
				}
				catch (Exception ex5)
				{
					ProjectData.SetProjectError(ex5);
					Exception ex6 = ex5;
					ProjectData.ClearProjectError();
				}
				if (num4 > 1)
				{
					ProgressBar ProgBar = ProgressBar1;
					Label ErrorLabel = null;
					GlobalForm.LoadFile(text3, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
					ProgressBar1 = ProgBar;
					GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
					GlobalForm.SelectChartType(Chart1);
					GlobalForm.ShowStock(Chart1, StartDate, EndDate, VolumeFlag: false, MAFlag: false);
					ShowCPI();
					CPIAvailable = true;
				}
				GlobalForm.HideMessages = false;
				ProgressBar1.Value = 0;
				((Control)FromDatePicker).Enabled = true;
				((Control)BrowseButton).Enabled = true;
				if (num4 > 1)
				{
					((Control)ClipboardButton).Enabled = true;
					((Control)ResultsButton).Enabled = true;
				}
				((Control)DoneButton).Enabled = true;
				((Control)ToDatePicker).Enabled = true;
				((Control)HelpButton1).Enabled = true;
				((Control)StartButton).Enabled = true;
				((Control)StopButton).Enabled = false;
				((Control)SymbolTextBox).Enabled = true;
				((Control)ShowChangesRB).Enabled = true;
				((Control)ShowAllSignalsRB).Enabled = true;
				((Control)ShowIndicatorOnlyRB).Enabled = true;
				if (num4 <= 1)
				{
					MessageBox.Show("There are not enough symbols selected to show a valid CPI. I will return you to the Main Form so you can highlight more symbols.", "StartButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)64);
					DoneButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
					return;
				}
				if (text.Length > 0)
				{
					try
					{
						Clipboard.SetText(text);
					}
					catch (Exception ex7)
					{
						ProjectData.SetProjectError(ex7);
						Exception ex8 = ex7;
						ProjectData.ClearProjectError();
					}
				}
				ResultsButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			}
			catch (Exception ex9)
			{
				ProjectData.SetProjectError(ex9);
				Exception ex10 = ex9;
				MessageBox.Show("If you see a big red X on the chart, then the charting module has crashed. You'll have to exit Patternz and run it again to clear the error.\r\n\r\nTo prevent it from happening again, try running the CPI during a week day or change the end date to a week day. This is a bug I've been unable to find.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				ProjectData.ClearProjectError();
			}
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

	private void ResizeData()
	{
		checked
		{
			for (int i = GlobalForm.HLCRange; i >= 0; i += -1)
			{
				if (DateTime.Compare(GlobalForm.nDT[0, i], EndDate) <= 0)
				{
					GlobalForm.nDT = (DateTime[,])Utils.CopyArray((Array)GlobalForm.nDT, (Array)new DateTime[2, i + 1]);
					GlobalForm.nHLC = (decimal[,])Utils.CopyArray((Array)GlobalForm.nHLC, (Array)new decimal[6, i + 1]);
					GlobalForm.HLCRange = i;
					break;
				}
			}
		}
	}
}
