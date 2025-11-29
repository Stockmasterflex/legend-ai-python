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
public class FixSplitForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("Chart1")]
	private Chart _Chart1;

	[CompilerGenerated]
	[AccessedThroughProperty("GraphButton")]
	private Button _GraphButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ForTextBox")]
	private MaskedTextBox _ForTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("SplitTextBox")]
	private MaskedTextBox _SplitTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("ApplyButton")]
	private Button _ApplyButton;

	[CompilerGenerated]
	[AccessedThroughProperty("FindButton")]
	private Button _FindButton;

	[CompilerGenerated]
	[AccessedThroughProperty("SaveButton")]
	private Button _SaveButton;

	[CompilerGenerated]
	[AccessedThroughProperty("RestoreButton")]
	private Button _RestoreButton;

	[CompilerGenerated]
	[AccessedThroughProperty("SplitsDivsButton")]
	private Button _SplitsDivsButton;

	[CompilerGenerated]
	[AccessedThroughProperty("SplitListBox")]
	private ListBox _SplitListBox;

	private string Filename;

	private bool ShowSplit;

	private bool SaveChanges;

	private bool LockFlag;

	private bool Crosshair;

	private Point CrosshairPoint;

	private Pen CrosshairPen;

	private Point StartPoint;

	private Point EndPoint;

	private CalloutAnnotation CurrentAnnotation;

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

	[field: AccessedThroughProperty("SplitDateTimePicker")]
	internal virtual DateTimePicker SplitDateTimePicker
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

	[field: AccessedThroughProperty("GroupBox1")]
	internal virtual GroupBox GroupBox1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("GroupBox2")]
	internal virtual GroupBox GroupBox2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual MaskedTextBox ForTextBox
	{
		[CompilerGenerated]
		get
		{
			return _ForTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0021: Unknown result type (might be due to invalid IL or missing references)
			//IL_0027: Expected O, but got Unknown
			//IL_002e: Unknown result type (might be due to invalid IL or missing references)
			//IL_0034: Expected O, but got Unknown
			EventHandler eventHandler = ForTextBox_Gotfocus;
			EventHandler eventHandler2 = ForTextBox_Gotfocus;
			MouseEventHandler val = new MouseEventHandler(ForTextBox_Gotfocus);
			MaskInputRejectedEventHandler val2 = new MaskInputRejectedEventHandler(ForTextBox_MaskInputRejected);
			MaskedTextBox val3 = _ForTextBox;
			if (val3 != null)
			{
				((Control)val3).GotFocus -= eventHandler;
				((Control)val3).Enter -= eventHandler2;
				((Control)val3).MouseUp -= val;
				val3.MaskInputRejected -= val2;
			}
			_ForTextBox = value;
			val3 = _ForTextBox;
			if (val3 != null)
			{
				((Control)val3).GotFocus += eventHandler;
				((Control)val3).Enter += eventHandler2;
				((Control)val3).MouseUp += val;
				val3.MaskInputRejected += val2;
			}
		}
	}

	internal virtual MaskedTextBox SplitTextBox
	{
		[CompilerGenerated]
		get
		{
			return _SplitTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0007: Unknown result type (might be due to invalid IL or missing references)
			//IL_000d: Expected O, but got Unknown
			//IL_002e: Unknown result type (might be due to invalid IL or missing references)
			//IL_0034: Expected O, but got Unknown
			MaskInputRejectedEventHandler val = new MaskInputRejectedEventHandler(ForTextBox_MaskInputRejected);
			EventHandler eventHandler = SplitTextBox_GotFocus;
			EventHandler eventHandler2 = SplitTextBox_GotFocus;
			MouseEventHandler val2 = new MouseEventHandler(SplitTextBox_GotFocus);
			MaskedTextBox val3 = _SplitTextBox;
			if (val3 != null)
			{
				val3.MaskInputRejected -= val;
				((Control)val3).GotFocus -= eventHandler;
				((Control)val3).Enter -= eventHandler2;
				((Control)val3).MouseUp -= val2;
			}
			_SplitTextBox = value;
			val3 = _SplitTextBox;
			if (val3 != null)
			{
				val3.MaskInputRejected += val;
				((Control)val3).GotFocus += eventHandler;
				((Control)val3).Enter += eventHandler2;
				((Control)val3).MouseUp += val2;
			}
		}
	}

	[field: AccessedThroughProperty("Label5")]
	internal virtual Label Label5
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

	internal virtual Button ApplyButton
	{
		[CompilerGenerated]
		get
		{
			return _ApplyButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ApplyButton_Click;
			Button val = _ApplyButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ApplyButton = value;
			val = _ApplyButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("LoadingBar")]
	internal virtual ProgressBar LoadingBar
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

	[field: AccessedThroughProperty("Label7")]
	internal virtual Label Label7
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

	internal virtual Button FindButton
	{
		[CompilerGenerated]
		get
		{
			return _FindButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = FindButton_Click;
			Button val = _FindButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_FindButton = value;
			val = _FindButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button SaveButton
	{
		[CompilerGenerated]
		get
		{
			return _SaveButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SaveButton_Click;
			Button val = _SaveButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_SaveButton = value;
			val = _SaveButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button RestoreButton
	{
		[CompilerGenerated]
		get
		{
			return _RestoreButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = RestoreButton_Click;
			Button val = _RestoreButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_RestoreButton = value;
			val = _RestoreButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("EntireFileRB")]
	internal virtual RadioButton EntireFileRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("ChartDatesRB")]
	internal virtual RadioButton ChartDatesRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label11")]
	internal virtual Label Label11
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button SplitsDivsButton
	{
		[CompilerGenerated]
		get
		{
			return _SplitsDivsButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SplitsDivsButton_Click;
			Button val = _SplitsDivsButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_SplitsDivsButton = value;
			val = _SplitsDivsButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label12")]
	internal virtual Label Label12
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual ListBox SplitListBox
	{
		[CompilerGenerated]
		get
		{
			return _SplitListBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SplitListBox_SelectedIndexChanged;
			ListBox val = _SplitListBox;
			if (val != null)
			{
				val.SelectedIndexChanged -= eventHandler;
			}
			_SplitListBox = value;
			val = _SplitListBox;
			if (val != null)
			{
				val.SelectedIndexChanged += eventHandler;
			}
		}
	}

	public FixSplitForm()
	{
		//IL_0060: Unknown result type (might be due to invalid IL or missing references)
		//IL_006a: Expected O, but got Unknown
		((Form)this).Closing += FixSplitForm_Closing;
		((Form)this).Load += FixSplitForm_Load;
		((Form)this).Activated += FixSplitForm_Activated;
		ShowSplit = false;
		SaveChanges = false;
		LockFlag = false;
		Crosshair = false;
		CrosshairPen = null;
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
		//IL_001d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0027: Expected O, but got Unknown
		//IL_0028: Unknown result type (might be due to invalid IL or missing references)
		//IL_0032: Expected O, but got Unknown
		//IL_0033: Unknown result type (might be due to invalid IL or missing references)
		//IL_003d: Expected O, but got Unknown
		//IL_003e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0048: Expected O, but got Unknown
		//IL_0049: Unknown result type (might be due to invalid IL or missing references)
		//IL_0053: Expected O, but got Unknown
		//IL_0054: Unknown result type (might be due to invalid IL or missing references)
		//IL_005e: Expected O, but got Unknown
		//IL_005f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0069: Expected O, but got Unknown
		//IL_006a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0074: Expected O, but got Unknown
		//IL_0075: Unknown result type (might be due to invalid IL or missing references)
		//IL_007f: Expected O, but got Unknown
		//IL_0080: Unknown result type (might be due to invalid IL or missing references)
		//IL_008a: Expected O, but got Unknown
		//IL_008b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0095: Expected O, but got Unknown
		//IL_0096: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a0: Expected O, but got Unknown
		//IL_00a1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ab: Expected O, but got Unknown
		//IL_00ac: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b6: Expected O, but got Unknown
		//IL_00b7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c1: Expected O, but got Unknown
		//IL_00c2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00cc: Expected O, but got Unknown
		//IL_00cd: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d7: Expected O, but got Unknown
		//IL_00d8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e2: Expected O, but got Unknown
		//IL_00e3: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ed: Expected O, but got Unknown
		//IL_00ee: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f8: Expected O, but got Unknown
		//IL_00f9: Unknown result type (might be due to invalid IL or missing references)
		//IL_0103: Expected O, but got Unknown
		//IL_0104: Unknown result type (might be due to invalid IL or missing references)
		//IL_010e: Expected O, but got Unknown
		//IL_010f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0119: Expected O, but got Unknown
		//IL_011a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0124: Expected O, but got Unknown
		//IL_0125: Unknown result type (might be due to invalid IL or missing references)
		//IL_012f: Expected O, but got Unknown
		//IL_0130: Unknown result type (might be due to invalid IL or missing references)
		//IL_013a: Expected O, but got Unknown
		//IL_013b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0145: Expected O, but got Unknown
		//IL_0146: Unknown result type (might be due to invalid IL or missing references)
		//IL_0150: Expected O, but got Unknown
		//IL_0151: Unknown result type (might be due to invalid IL or missing references)
		//IL_015b: Expected O, but got Unknown
		//IL_015c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0166: Expected O, but got Unknown
		//IL_02f3: Unknown result type (might be due to invalid IL or missing references)
		//IL_11bf: Unknown result type (might be due to invalid IL or missing references)
		//IL_11c9: Expected O, but got Unknown
		ChartArea val = new ChartArea();
		Series val2 = new Series();
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(FixSplitForm));
		Chart1 = new Chart();
		ToDatePicker = new DateTimePicker();
		FromDatePicker = new DateTimePicker();
		Label3 = new Label();
		Label2 = new Label();
		GraphButton = new Button();
		DoneButton = new Button();
		SplitDateTimePicker = new DateTimePicker();
		Label1 = new Label();
		GroupBox1 = new GroupBox();
		Label11 = new Label();
		LoadingBar = new ProgressBar();
		GroupBox2 = new GroupBox();
		EntireFileRB = new RadioButton();
		ChartDatesRB = new RadioButton();
		FindButton = new Button();
		ApplyButton = new Button();
		ForTextBox = new MaskedTextBox();
		SplitTextBox = new MaskedTextBox();
		Label5 = new Label();
		Label4 = new Label();
		Label6 = new Label();
		Label7 = new Label();
		Label8 = new Label();
		Label9 = new Label();
		SaveButton = new Button();
		RestoreButton = new Button();
		SplitsDivsButton = new Button();
		Label12 = new Label();
		SplitListBox = new ListBox();
		((ISupportInitialize)Chart1).BeginInit();
		((Control)GroupBox1).SuspendLayout();
		((Control)GroupBox2).SuspendLayout();
		((Control)this).SuspendLayout();
		((Control)Chart1).Anchor = (AnchorStyles)15;
		Chart1.BorderSkin.BorderColor = Color.White;
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
		((Collection<Series>)(object)Chart1.Series).Add(val2);
		Chart1.Size = new Size(817, 302);
		((Control)Chart1).TabIndex = 1;
		((Control)Chart1).Text = "Chart1";
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(60, 73);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(120, 20);
		((Control)ToDatePicker).TabIndex = 5;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(60, 40);
		((Control)FromDatePicker).Name = "FromDatePicker";
		FromDatePicker.ShowUpDown = true;
		((Control)FromDatePicker).Size = new Size(120, 20);
		((Control)FromDatePicker).TabIndex = 3;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)Label3).Anchor = (AnchorStyles)10;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(31, 77);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(23, 13);
		((Control)Label3).TabIndex = 4;
		Label3.Text = "&To:";
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(21, 46);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(33, 13);
		((Control)Label2).TabIndex = 2;
		Label2.Text = "&From:";
		((Control)GraphButton).Anchor = (AnchorStyles)10;
		((Control)GraphButton).Location = new Point(186, 71);
		((Control)GraphButton).Name = "GraphButton";
		((Control)GraphButton).Size = new Size(49, 23);
		((Control)GraphButton).TabIndex = 6;
		((ButtonBase)GraphButton).Text = "&Graph";
		((ButtonBase)GraphButton).UseVisualStyleBackColor = true;
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(780, 570);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(49, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)SplitDateTimePicker).Anchor = (AnchorStyles)10;
		SplitDateTimePicker.CustomFormat = "yyyy/MM/dd";
		SplitDateTimePicker.Format = (DateTimePickerFormat)8;
		((Control)SplitDateTimePicker).Location = new Point(82, 43);
		((Control)SplitDateTimePicker).Name = "SplitDateTimePicker";
		SplitDateTimePicker.ShowUpDown = true;
		((Control)SplitDateTimePicker).Size = new Size(120, 20);
		((Control)SplitDateTimePicker).TabIndex = 3;
		SplitDateTimePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(22, 45);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(54, 13);
		((Control)Label1).TabIndex = 2;
		Label1.Text = "&Split date:";
		((Control)GroupBox1).Anchor = (AnchorStyles)10;
		((Control)GroupBox1).Controls.Add((Control)(object)Label11);
		((Control)GroupBox1).Controls.Add((Control)(object)LoadingBar);
		((Control)GroupBox1).Controls.Add((Control)(object)ToDatePicker);
		((Control)GroupBox1).Controls.Add((Control)(object)GraphButton);
		((Control)GroupBox1).Controls.Add((Control)(object)Label2);
		((Control)GroupBox1).Controls.Add((Control)(object)FromDatePicker);
		((Control)GroupBox1).Controls.Add((Control)(object)Label3);
		((Control)GroupBox1).Location = new Point(322, 314);
		((Control)GroupBox1).Name = "GroupBox1";
		((Control)GroupBox1).Size = new Size(241, 100);
		((Control)GroupBox1).TabIndex = 7;
		GroupBox1.TabStop = false;
		GroupBox1.Text = "Chart";
		((Control)Label11).Anchor = (AnchorStyles)10;
		Label11.AutoSize = true;
		((Control)Label11).Location = new Point(6, 21);
		((Control)Label11).Name = "Label11";
		((Control)Label11).Size = new Size(48, 13);
		((Control)Label11).TabIndex = 0;
		Label11.Text = "Loading:";
		((Control)LoadingBar).Anchor = (AnchorStyles)10;
		((Control)LoadingBar).ForeColor = Color.Green;
		((Control)LoadingBar).Location = new Point(60, 21);
		((Control)LoadingBar).Name = "LoadingBar";
		((Control)LoadingBar).Size = new Size(120, 15);
		((Control)LoadingBar).TabIndex = 1;
		((Control)GroupBox2).Anchor = (AnchorStyles)10;
		((Control)GroupBox2).Controls.Add((Control)(object)EntireFileRB);
		((Control)GroupBox2).Controls.Add((Control)(object)ChartDatesRB);
		((Control)GroupBox2).Controls.Add((Control)(object)FindButton);
		((Control)GroupBox2).Controls.Add((Control)(object)ApplyButton);
		((Control)GroupBox2).Controls.Add((Control)(object)ForTextBox);
		((Control)GroupBox2).Controls.Add((Control)(object)SplitTextBox);
		((Control)GroupBox2).Controls.Add((Control)(object)Label5);
		((Control)GroupBox2).Controls.Add((Control)(object)Label4);
		((Control)GroupBox2).Controls.Add((Control)(object)Label1);
		((Control)GroupBox2).Controls.Add((Control)(object)SplitDateTimePicker);
		((Control)GroupBox2).Location = new Point(569, 314);
		((Control)GroupBox2).Name = "GroupBox2";
		((Control)GroupBox2).Size = new Size(263, 100);
		((Control)GroupBox2).TabIndex = 8;
		GroupBox2.TabStop = false;
		GroupBox2.Text = "Split";
		((ButtonBase)EntireFileRB).AutoSize = true;
		((Control)EntireFileRB).Location = new Point(148, 20);
		((Control)EntireFileRB).Name = "EntireFileRB";
		((Control)EntireFileRB).Size = new Size(68, 17);
		((Control)EntireFileRB).TabIndex = 1;
		((ButtonBase)EntireFileRB).Text = "&Entire file";
		((ButtonBase)EntireFileRB).UseVisualStyleBackColor = true;
		((ButtonBase)ChartDatesRB).AutoSize = true;
		ChartDatesRB.Checked = true;
		((Control)ChartDatesRB).Location = new Point(13, 19);
		((Control)ChartDatesRB).Name = "ChartDatesRB";
		((Control)ChartDatesRB).Size = new Size(129, 17);
		((Control)ChartDatesRB).TabIndex = 0;
		ChartDatesRB.TabStop = true;
		((ButtonBase)ChartDatesRB).Text = "Find &using chart dates";
		((ButtonBase)ChartDatesRB).UseVisualStyleBackColor = true;
		((Control)FindButton).Anchor = (AnchorStyles)10;
		((Control)FindButton).Location = new Point(208, 42);
		((Control)FindButton).Name = "FindButton";
		((Control)FindButton).Size = new Size(49, 23);
		((Control)FindButton).TabIndex = 8;
		((ButtonBase)FindButton).Text = "&Find";
		((ButtonBase)FindButton).UseVisualStyleBackColor = true;
		((Control)ApplyButton).Anchor = (AnchorStyles)10;
		((Control)ApplyButton).Location = new Point(208, 71);
		((Control)ApplyButton).Name = "ApplyButton";
		((Control)ApplyButton).Size = new Size(49, 23);
		((Control)ApplyButton).TabIndex = 9;
		((ButtonBase)ApplyButton).Text = "&Apply";
		((ButtonBase)ApplyButton).UseVisualStyleBackColor = true;
		((Control)ForTextBox).Location = new Point(169, 73);
		ForTextBox.Mask = "000";
		((Control)ForTextBox).Name = "ForTextBox";
		ForTextBox.ResetOnSpace = false;
		((Control)ForTextBox).Size = new Size(33, 20);
		((Control)ForTextBox).TabIndex = 7;
		ForTextBox.TextMaskFormat = (MaskFormat)0;
		((Control)SplitTextBox).Location = new Point(82, 74);
		SplitTextBox.Mask = "000";
		((Control)SplitTextBox).Name = "SplitTextBox";
		SplitTextBox.ResetOnSpace = false;
		((Control)SplitTextBox).Size = new Size(33, 20);
		((Control)SplitTextBox).TabIndex = 5;
		SplitTextBox.TextMaskFormat = (MaskFormat)0;
		((Control)Label5).Anchor = (AnchorStyles)10;
		Label5.AutoSize = true;
		((Control)Label5).Location = new Point(141, 78);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(22, 13);
		((Control)Label5).TabIndex = 6;
		Label5.Text = "&For";
		((Control)Label4).Anchor = (AnchorStyles)10;
		Label4.AutoSize = true;
		((Control)Label4).Location = new Point(49, 77);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(27, 13);
		((Control)Label4).TabIndex = 4;
		Label4.Text = "&Split";
		((Control)Label6).Anchor = (AnchorStyles)10;
		((Control)Label6).Location = new Point(6, 330);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(310, 74);
		((Control)Label6).TabIndex = 2;
		Label6.Text = componentResourceManager.GetString("Label6.Text");
		((Control)Label7).Anchor = (AnchorStyles)10;
		Label7.AutoSize = true;
		((Control)Label7).Location = new Point(6, 409);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(209, 13);
		((Control)Label7).TabIndex = 3;
		Label7.Text = "2. Enter the split date if not found by step 1";
		((Control)Label8).Anchor = (AnchorStyles)10;
		((Control)Label8).Location = new Point(6, 440);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(278, 37);
		((Control)Label8).TabIndex = 4;
		Label8.Text = "3. Enter Split and For numbers (example: Split 2 For 1 or Split 1 For 5)";
		((Control)Label9).Anchor = (AnchorStyles)10;
		((Control)Label9).Location = new Point(6, 490);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(298, 38);
		((Control)Label9).TabIndex = 5;
		Label9.Text = "4. Click Apply then Save to make changes permanent or Restore to reload the file.";
		((Control)SaveButton).Anchor = (AnchorStyles)10;
		((Control)SaveButton).Enabled = false;
		((Control)SaveButton).Location = new Point(725, 570);
		((Control)SaveButton).Name = "SaveButton";
		((Control)SaveButton).Size = new Size(49, 23);
		((Control)SaveButton).TabIndex = 12;
		((ButtonBase)SaveButton).Text = "&Save";
		((ButtonBase)SaveButton).UseVisualStyleBackColor = true;
		((Control)RestoreButton).Anchor = (AnchorStyles)10;
		((Control)RestoreButton).Enabled = false;
		((Control)RestoreButton).Location = new Point(662, 570);
		((Control)RestoreButton).Name = "RestoreButton";
		((Control)RestoreButton).Size = new Size(57, 23);
		((Control)RestoreButton).TabIndex = 11;
		((ButtonBase)RestoreButton).Text = "&Restore";
		((ButtonBase)RestoreButton).UseVisualStyleBackColor = true;
		((Control)SplitsDivsButton).Anchor = (AnchorStyles)10;
		((Control)SplitsDivsButton).Location = new Point(530, 570);
		((Control)SplitsDivsButton).Name = "SplitsDivsButton";
		((Control)SplitsDivsButton).Size = new Size(126, 23);
		((Control)SplitsDivsButton).TabIndex = 10;
		((ButtonBase)SplitsDivsButton).Text = "&Splits/Dividends Form";
		((ButtonBase)SplitsDivsButton).UseVisualStyleBackColor = true;
		((Control)Label12).Anchor = (AnchorStyles)10;
		((Control)Label12).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label12).Location = new Point(6, 535);
		((Control)Label12).Name = "Label12";
		((Control)Label12).Size = new Size(310, 58);
		((Control)Label12).TabIndex = 6;
		Label12.Text = "Note: When updating quotes for this stock (Update Form), only use the 'Start from last update' option. DON'T use 'Get historical quotes' because you'll erase changes made by this form.";
		((Control)SplitListBox).Anchor = (AnchorStyles)10;
		((Control)SplitListBox).CausesValidation = false;
		SplitListBox.HorizontalScrollbar = true;
		((Control)SplitListBox).Location = new Point(322, 426);
		SplitListBox.MultiColumn = true;
		((Control)SplitListBox).Name = "SplitListBox";
		((Control)SplitListBox).Size = new Size(509, 134);
		((Control)SplitListBox).TabIndex = 9;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(845, 605);
		((Control)this).Controls.Add((Control)(object)SplitListBox);
		((Control)this).Controls.Add((Control)(object)Label12);
		((Control)this).Controls.Add((Control)(object)SplitsDivsButton);
		((Control)this).Controls.Add((Control)(object)RestoreButton);
		((Control)this).Controls.Add((Control)(object)SaveButton);
		((Control)this).Controls.Add((Control)(object)Label9);
		((Control)this).Controls.Add((Control)(object)Label8);
		((Control)this).Controls.Add((Control)(object)Label7);
		((Control)this).Controls.Add((Control)(object)Label6);
		((Control)this).Controls.Add((Control)(object)GroupBox2);
		((Control)this).Controls.Add((Control)(object)GroupBox1);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)Chart1);
		((Control)this).Name = "FixSplitForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Fix Split Form";
		((ISupportInitialize)Chart1).EndInit();
		((Control)GroupBox1).ResumeLayout(false);
		((Control)GroupBox1).PerformLayout();
		((Control)GroupBox2).ResumeLayout(false);
		((Control)GroupBox2).PerformLayout();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void FixSplitForm_Closing(object sender, CancelEventArgs e)
	{
		//IL_0056: Unknown result type (might be due to invalid IL or missing references)
		//IL_005c: Invalid comparison between Unknown and I4
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
		if (SaveChanges && (int)MessageBox.Show("Did you want to save changes?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32) == 6)
		{
			SaveButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		}
		GlobalForm.EntireFile = EntireFileRB.Checked;
		MySettingsProperty.Settings.FixedSplitLocation = ((Form)this).Location;
		MySettingsProperty.Settings.FixedSplitSize = ((Form)this).Size;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
		LockFlag = false;
	}

	private void FixSplitForm_Load(object sender, EventArgs e)
	{
		//IL_0058: Unknown result type (might be due to invalid IL or missing references)
		//IL_005d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0068: Unknown result type (might be due to invalid IL or missing references)
		//IL_0073: Unknown result type (might be due to invalid IL or missing references)
		//IL_007e: Unknown result type (might be due to invalid IL or missing references)
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
		//IL_0023: Unknown result type (might be due to invalid IL or missing references)
		//IL_002d: Expected O, but got Unknown
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.FixedSplitLocation, MySettingsProperty.Settings.FixedSplitSize);
		if (CurrentAnnotation == null)
		{
			CurrentAnnotation = new CalloutAnnotation();
		}
		((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)CurrentAnnotation);
		ShowSplit = false;
		SaveChanges = false;
		LockFlag = false;
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)ApplyButton, "Split the stock.");
		val.SetToolTip((Control)(object)Chart1, "Right mouse click a price bar to set the split date.");
		val.SetToolTip((Control)(object)ChartDatesRB, "Search for a split using the From and To chart dates.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)EntireFileRB, "Search for a split using the entire file's data.");
		val.SetToolTip((Control)(object)FindButton, "Click to search for a split");
		val.SetToolTip((Control)(object)ForTextBox, "A split amount such as the number 2 in the phase split 1 for 2.");
		val.SetToolTip((Control)(object)FromDatePicker, "The starting date of the charted security.");
		val.SetToolTip((Control)(object)GraphButton, "Chart the security using the associated From and To dates.");
		val.SetToolTip((Control)(object)RestoreButton, "Returns the file to its original condition. Must be done BEFORE saving.");
		val.SetToolTip((Control)(object)SaveButton, "Saves changes.");
		val.SetToolTip((Control)(object)SplitDateTimePicker, "Right mouse click a charted price bar or enter the split date.");
		val.SetToolTip((Control)(object)SplitsDivsButton, "Run the Splits and Dividends Form to help find a split.");
		val.SetToolTip((Control)(object)SplitListBox, "If the Splits and Dividends Form found a split FOR THIS SECURITY (symbols MUST match), it appears here.");
		val.SetToolTip((Control)(object)SplitTextBox, "A split amount such as the number 2 in the phase split 2 for 1.");
		val.SetToolTip((Control)(object)ToDatePicker, "The ending date of the charted security.");
		if (GlobalForm.EntireFile)
		{
			EntireFileRB.Checked = true;
		}
		else
		{
			ChartDatesRB.Checked = true;
		}
		GlobalForm.SelectChartType(Chart1);
	}

	private void FixSplitForm_Activated(object sender, EventArgs e)
	{
		if (LockFlag)
		{
			return;
		}
		LockFlag = true;
		((Control)this).Refresh();
		GlobalForm.FirstPoint = default(Point);
		GlobalForm.LinesList.RemoveAll(StubBoolean);
		if (MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count <= 0)
		{
			return;
		}
		Filename = MyProject.Forms.Mainform.ListBox1.SelectedItems[0].ToString();
		string filename = Filename;
		ProgressBar ProgBar = LoadingBar;
		Label ErrorLabel = null;
		bool num = GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
		LoadingBar = ProgBar;
		checked
		{
			if (!num)
			{
				GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
				GlobalForm.SelectChartType(Chart1);
				if (GlobalForm.IntradayData)
				{
					SplitDateTimePicker.CustomFormat = "yyyy-MM-dd HH:mm";
					if (GlobalForm.HLCRange >= 180)
					{
						if ((DateTime.Compare(GlobalForm.nDT[0, GlobalForm.HLCRange - 180], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, GlobalForm.HLCRange - 180], FromDatePicker.MaxDate) <= 0))
						{
							FromDatePicker.Value = GlobalForm.nDT[0, GlobalForm.HLCRange - 180];
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
					SplitDateTimePicker.CustomFormat = "yyyy-MM-dd";
					FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, -180.0, DateAndTime.Now);
				}
				ToDatePicker.Value = DateAndTime.Now;
				GlobalForm.CheckDates(FromDatePicker, ToDatePicker);
				GlobalForm.ShowStock(Chart1, FromDatePicker.Value, ToDatePicker.Value, VolumeFlag: false, MAFlag: false);
			}
			else
			{
				FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, -180.0, DateAndTime.Now);
				ToDatePicker.Value = DateAndTime.Now;
			}
			((Form)this).Text = "Fix Split Form: " + Filename.ToString();
			FillListBox();
		}
	}

	private void ApplyButton_Click(object sender, EventArgs e)
	{
		//IL_0046: Unknown result type (might be due to invalid IL or missing references)
		if ((Conversion.Val(SplitTextBox.Text) == 0.0) | (Conversion.Val(ForTextBox.Text) == 0.0))
		{
			MessageBox.Show("Both the 'Split' and 'For' (as in split 2 for 1) text boxes need to have a non-zero value", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			if (Conversion.Val(SplitTextBox.Text) == 0.0)
			{
				((Control)SplitTextBox).Focus();
			}
			if (Conversion.Val(ForTextBox.Text) == 0.0)
			{
				((Control)ForTextBox).Focus();
			}
			return;
		}
		decimal d = new decimal(Conversion.Val(SplitTextBox.Text) / Conversion.Val(ForTextBox.Text));
		for (int i = GlobalForm.HLCRange; i >= 0; i = checked(i + -1))
		{
			if ((GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, i], SplitDateTimePicker.Value) < 0)) | (!GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, i].Date, SplitDateTimePicker.Value.Date) < 0)))
			{
				ref decimal reference = ref GlobalForm.nHLC[0, i];
				reference = decimal.Divide(reference, d);
				ref decimal reference2 = ref GlobalForm.nHLC[1, i];
				reference2 = decimal.Divide(reference2, d);
				ref decimal reference3 = ref GlobalForm.nHLC[2, i];
				reference3 = decimal.Divide(reference3, d);
				ref decimal reference4 = ref GlobalForm.nHLC[3, i];
				reference4 = decimal.Divide(reference4, d);
				ref decimal reference5 = ref GlobalForm.nHLC[5, i];
				reference5 = decimal.Divide(reference5, d);
				ref decimal reference6 = ref GlobalForm.nHLC[4, i];
				reference6 = decimal.Multiply(reference6, d);
			}
		}
		GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		((Control)RestoreButton).Enabled = true;
		((Control)SaveButton).Enabled = true;
		SaveChanges = true;
	}

	private void Chart1_MouseDown(object sender, MouseEventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_000b: Invalid comparison between Unknown and I4
		//IL_0088: Unknown result type (might be due to invalid IL or missing references)
		//IL_0092: Invalid comparison between Unknown and I4
		//IL_0032: Unknown result type (might be due to invalid IL or missing references)
		//IL_0039: Invalid comparison between Unknown and I4
		//IL_00a7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b1: Expected O, but got Unknown
		if ((int)e.Button == 2097152)
		{
			GlobalForm.ShowQuoteInfo(Chart1, e);
			try
			{
				HitTestResult val = Chart1.HitTest(e.X, e.Y);
				if ((int)val.ChartElementType == 16)
				{
					int pointIndex = val.PointIndex;
					if (Operators.CompareString(val.Series.Name, "CandleSeries", false) == 0)
					{
						SplitDateTimePicker.Value = GlobalForm.nDT[0, checked(pointIndex + GlobalForm.ChartStartIndex)];
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
		if ((int)e.Button == 1048576)
		{
			if (Information.IsNothing((object)CrosshairPen))
			{
				CrosshairPen = new Pen(Color.Black);
				CrosshairPen.DashStyle = (DashStyle)1;
			}
			CrosshairPoint = new Point(e.X, e.Y);
			Crosshair = true;
			((Control)this).Refresh();
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
		//IL_0021: Unknown result type (might be due to invalid IL or missing references)
		//IL_0041: Unknown result type (might be due to invalid IL or missing references)
		//IL_0047: Expected O, but got Unknown
		//IL_0052: Unknown result type (might be due to invalid IL or missing references)
		//IL_0058: Expected O, but got Unknown
		//IL_005d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0063: Expected O, but got Unknown
		if (!ShowSplit || !(e.ChartElement is Series) || Operators.CompareString(((Series)e.ChartElement).Name, "CandleSeries", false) != 0)
		{
			return;
		}
		Series val = (Series)e.ChartElement;
		Font val2 = new Font("Arial", 10f, (FontStyle)1);
		SolidBrush val3 = new SolidBrush(Color.Red);
		int num = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)val.Points)
			{
				if ((GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, num + GlobalForm.ChartStartIndex], SplitDateTimePicker.Value) == 0)) | (!GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, num + GlobalForm.ChartStartIndex].Date, SplitDateTimePicker.Value.Date) == 0)))
				{
					PointF empty = PointF.Empty;
					empty.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					empty.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]) - 4f;
					empty = e.ChartGraphics.GetAbsolutePoint(empty);
					e.ChartGraphics.Graphics.DrawString("Split", val2, (Brush)(object)val3, empty);
					break;
				}
				num++;
			}
			((Brush)val3).Dispose();
			val2.Dispose();
		}
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void FillListBox()
	{
		if (GlobalForm.SplitArray == null || Information.UBound((Array)GlobalForm.SplitArray, 1) <= 0)
		{
			return;
		}
		SplitListBox.Items.Clear();
		checked
		{
			string text = Strings.Left(Filename, Filename.Length - 4);
			int num = Information.UBound((Array)GlobalForm.SplitArray, 1);
			for (int i = 0; i <= num; i++)
			{
				if (Operators.CompareString(GlobalForm.SplitArray[i].Symbol, text, false) == 0)
				{
					SplitListBox.Items.Add((object)(Conversions.ToString(GlobalForm.SplitArray[i].SplitDate) + "   " + GlobalForm.SplitArray[i].SplitRatio));
				}
			}
		}
	}

	private void FindButton_Click(object sender, EventArgs e)
	{
		//IL_0352: Unknown result type (might be due to invalid IL or missing references)
		//IL_02bf: Unknown result type (might be due to invalid IL or missing references)
		//IL_02c4: Unknown result type (might be due to invalid IL or missing references)
		//IL_02c5: Unknown result type (might be due to invalid IL or missing references)
		//IL_02c7: Invalid comparison between Unknown and I4
		//IL_02f3: Unknown result type (might be due to invalid IL or missing references)
		//IL_02f5: Invalid comparison between Unknown and I4
		//IL_0304: Unknown result type (might be due to invalid IL or missing references)
		DateTime value = FromDatePicker.Value;
		DateTime value2 = ToDatePicker.Value;
		bool flag = false;
		int hLCRange = GlobalForm.HLCRange;
		for (int i = 1; i <= hLCRange; i = checked(i + 1))
		{
			if (!(EntireFileRB.Checked | (!EntireFileRB.Checked & (DateTime.Compare(GlobalForm.nDT[0, i], value) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, i], value2) <= 0))))
			{
				continue;
			}
			DialogResult val;
			checked
			{
				decimal value3 = decimal.Divide(GlobalForm.nHLC[0, i], GlobalForm.nHLC[3, i - 1]);
				if (!((Convert.ToDouble(value3) < 0.9) | (Convert.ToDouble(value3) > 1.1)))
				{
					continue;
				}
				if (GlobalForm.IntradayData)
				{
					if (i < 30)
					{
						if ((DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MaxDate) <= 0))
						{
							FromDatePicker.Value = GlobalForm.nDT[0, 0];
						}
						else
						{
							FromDatePicker.Value = DateAndTime.Now;
						}
					}
					else if ((DateTime.Compare(GlobalForm.nDT[0, i - 30], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, i - 30], FromDatePicker.MaxDate) <= 0))
					{
						FromDatePicker.Value = GlobalForm.nDT[0, i - 30];
					}
					else
					{
						FromDatePicker.Value = DateAndTime.Now;
					}
					if (i + 30 <= GlobalForm.HLCRange)
					{
						ToDatePicker.Value = GlobalForm.nDT[0, i + 30];
					}
					else
					{
						ToDatePicker.Value = GlobalForm.nDT[0, GlobalForm.HLCRange];
					}
				}
				else
				{
					FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, -30.0, GlobalForm.nDT[0, i]);
					ToDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, 30.0, GlobalForm.nDT[0, i]);
				}
				ShowSplit = true;
				GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
				SplitDateTimePicker.Value = GlobalForm.nDT[0, i - 1];
				val = MessageBox.Show("I have found a possible split on " + Strings.Format((object)GlobalForm.nDT[0, i - 1], GlobalForm.UserDate) + ". Is this correct?", "Patternz", (MessageBoxButtons)3, (MessageBoxIcon)32);
			}
			if ((int)val == 2)
			{
				FromDatePicker.Value = value;
				ToDatePicker.Value = value2;
				GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
				flag = true;
				break;
			}
			if ((int)val == 6)
			{
				MessageBox.Show("Enter the split ratio (3 for 2, 2 for 1, etc).", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				((Control)SplitTextBox).Focus();
				flag = true;
				break;
			}
		}
		ShowSplit = false;
		if (!flag)
		{
			MessageBox.Show("I couldn't find the split. Did you select the correct security (" + Filename + ")? Perhaps it has already been adjusted.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
	}

	private void ForTextBox_Gotfocus(object sender, EventArgs e)
	{
		((TextBoxBase)ForTextBox).SelectAll();
	}

	private void ForTextBox_MaskInputRejected(object sender, MaskInputRejectedEventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("Only numbers are allowed.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
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
		if (!num)
		{
			GlobalForm.SetupDateIndexes(GlobalForm.ChartStart, GlobalForm.ChartEnd);
			GlobalForm.ShowStock(Chart1, FromDatePicker.Value, ToDatePicker.Value, VolumeFlag: false, MAFlag: false);
		}
	}

	private void RestoreButton_Click(object sender, EventArgs e)
	{
		//IL_00a0: Unknown result type (might be due to invalid IL or missing references)
		string filename = Filename;
		ProgressBar ProgBar = LoadingBar;
		Label ErrorLabel = null;
		bool num = GlobalForm.LoadFile(filename, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
		LoadingBar = ProgBar;
		if (!num)
		{
			GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
			GlobalForm.SelectChartType(Chart1);
			GlobalForm.CheckDates(FromDatePicker, ToDatePicker);
			GlobalForm.ShowStock(Chart1, FromDatePicker.Value, ToDatePicker.Value, VolumeFlag: false, MAFlag: false);
		}
		((Control)SaveButton).Enabled = false;
		((Control)RestoreButton).Enabled = false;
		SaveChanges = false;
		MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void SaveButton_Click(object sender, EventArgs e)
	{
		//IL_03af: Unknown result type (might be due to invalid IL or missing references)
		//IL_0393: Unknown result type (might be due to invalid IL or missing references)
		//IL_0399: Invalid comparison between Unknown and I4
		int num = 0;
		int num2 = Information.UBound((Array)GlobalForm.FileFormat, 1);
		checked
		{
			for (int i = 0; i <= num2; i++)
			{
				num = Conversions.ToInteger(Interaction.IIf(GlobalForm.FileFormat[i] > num, (object)GlobalForm.FileFormat[i], (object)num));
			}
			string text = "";
			int num3 = num;
			for (int i = 1; i <= num3; i++)
			{
				int num4 = i;
				text = ((num4 != GlobalForm.FileFormat[0]) ? ((num4 != GlobalForm.FileFormat[1]) ? ((num4 != GlobalForm.FileFormat[2]) ? ((num4 != GlobalForm.FileFormat[3]) ? ((num4 != GlobalForm.FileFormat[4]) ? ((num4 != GlobalForm.FileFormat[5]) ? ((num4 != GlobalForm.FileFormat[6]) ? ((num4 != GlobalForm.FileFormat[7]) ? (text + ",") : (text + "Adj Close,")) : (text + "Volume,")) : (text + "Close,")) : (text + "Low,")) : (text + "High,")) : (text + "Open,")) : (text + "Time,")) : (text + "Date,"));
			}
			text = Strings.Left(text, text.Length - 1) + "\r\n";
			string userDate = GlobalForm.UserDate;
			userDate = Strings.Trim(userDate.Replace("HH:mm", ""));
			int hLCRange = GlobalForm.HLCRange;
			for (int j = 0; j <= hLCRange; j++)
			{
				int num5 = num;
				for (int i = 1; i <= num5; i++)
				{
					int num6 = i;
					text = ((num6 != GlobalForm.FileFormat[0]) ? ((num6 != GlobalForm.FileFormat[1]) ? ((num6 != GlobalForm.FileFormat[2]) ? ((num6 != GlobalForm.FileFormat[3]) ? ((num6 != GlobalForm.FileFormat[4]) ? ((num6 != GlobalForm.FileFormat[5]) ? ((num6 != GlobalForm.FileFormat[6]) ? ((num6 != GlobalForm.FileFormat[7]) ? (text + ",") : (text + GlobalForm.nHLC[5, j] + ",")) : (text + GlobalForm.nHLC[4, j] + ",")) : (text + GlobalForm.nHLC[3, j] + ",")) : (text + GlobalForm.nHLC[2, j] + ",")) : (text + GlobalForm.nHLC[1, j] + ",")) : (text + GlobalForm.nHLC[0, j] + ",")) : (text + Strings.Format((object)GlobalForm.nDT[1, j], "HH:mm") + ",")) : (text + Strings.Format((object)GlobalForm.nDT[0, j].Date, userDate) + ","));
				}
				text = Strings.Left(text, text.Length - 1) + "\r\n";
			}
			File.WriteAllText(GlobalForm.OpenPath + "\\" + Filename, text);
			((Control)RestoreButton).Enabled = false;
			((Control)SaveButton).Enabled = false;
			SaveChanges = false;
		}
		if (GlobalForm.UpdatePeriod == 3)
		{
			if ((int)MessageBox.Show("WARNING: The Update Form uses the 'Get Historical Quotes' option which will erase changes made by this form. Did you want me to change this to use the 'Start from last update' option instead?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32) == 6)
			{
				GlobalForm.UpdatePeriod = 2;
			}
		}
		else
		{
			MessageBox.Show("Changes saved!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
	}

	private void SplitsDivsButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.SplitsDivsForm).ShowDialog();
		FillListBox();
	}

	private void SplitListBox_SelectedIndexChanged(object sender, EventArgs e)
	{
		int selectedIndex = SplitListBox.SelectedIndex;
		string splitRatio = GlobalForm.SplitArray[selectedIndex].SplitRatio;
		if (GlobalForm.IntradayData)
		{
			SplitDateTimePicker.Value = GlobalForm.SplitArray[selectedIndex].SplitDate;
		}
		else
		{
			SplitDateTimePicker.Value = GlobalForm.SplitArray[selectedIndex].SplitDate.Date;
		}
		checked
		{
			SplitTextBox.Text = Strings.Left(splitRatio, Strings.InStr(splitRatio, ":", (CompareMethod)0) - 1);
			ForTextBox.Text = Strings.Right(splitRatio, Strings.Len(splitRatio) - Strings.InStrRev(splitRatio, ":", -1, (CompareMethod)0));
			if (GlobalForm.IntradayData)
			{
				int hLCRange = GlobalForm.HLCRange;
				for (int i = 0; i <= hLCRange; i++)
				{
					if (DateTime.Compare(GlobalForm.nDT[0, i], GlobalForm.SplitArray[selectedIndex].SplitDate) < 0)
					{
						continue;
					}
					if (i < 30)
					{
						if ((DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MaxDate) <= 0))
						{
							FromDatePicker.Value = GlobalForm.nDT[0, 0];
						}
						else
						{
							FromDatePicker.Value = DateAndTime.Now;
						}
					}
					else if ((DateTime.Compare(GlobalForm.nDT[0, i - 30], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, i - 30], FromDatePicker.MaxDate) <= 0))
					{
						FromDatePicker.Value = GlobalForm.nDT[0, i - 30];
					}
					else
					{
						FromDatePicker.Value = DateAndTime.Now;
					}
					if (i + 30 <= GlobalForm.HLCRange)
					{
						ToDatePicker.Value = GlobalForm.nDT[0, i + 30];
					}
					else
					{
						ToDatePicker.Value = GlobalForm.nDT[0, GlobalForm.HLCRange];
					}
					break;
				}
			}
			else
			{
				FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, -30.0, SplitDateTimePicker.Value);
				ToDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, 30.0, SplitDateTimePicker.Value);
			}
			ShowSplit = true;
			GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		}
	}

	private void SplitTextBox_GotFocus(object sender, EventArgs e)
	{
		((TextBoxBase)SplitTextBox).SelectAll();
	}

	private bool StubBoolean(GlobalForm.LineEndPoints sPoint)
	{
		return true;
	}
}
