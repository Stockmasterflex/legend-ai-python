using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class Seasonality : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ClipboardButton")]
	private Button _ClipboardButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StartButton")]
	private Button _StartButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DayButton")]
	private RadioButton _DayButton;

	[CompilerGenerated]
	[AccessedThroughProperty("MonthButton")]
	private RadioButton _MonthButton;

	[CompilerGenerated]
	[AccessedThroughProperty("OtherButton")]
	private RadioButton _OtherButton;

	[CompilerGenerated]
	[AccessedThroughProperty("HelpButton1")]
	private Button _HelpButton1;

	[CompilerGenerated]
	[AccessedThroughProperty("StopButton")]
	private Button _StopButton;

	[CompilerGenerated]
	[AccessedThroughProperty("AutoButton")]
	private Button _AutoButton;

	[CompilerGenerated]
	[AccessedThroughProperty("AutoMonthsButton")]
	private Button _AutoMonthsButton;

	private const int GRIDFILENAME = 0;

	private const int GRIDCLOSE = 1;

	private const int GRIDTARGET = 2;

	private const int GRIDTREND = 3;

	private const int GRIDCLOSEHI = 4;

	private const int GRIDGAIN = 5;

	private const int GRIDCLOSELO = 6;

	private const int GRIDLOSS = 7;

	private const int GRIDCOLCOUNT = 8;

	private const int LPAutoDays = 0;

	private const int LPAutoMonths = 1;

	private const int LPDayofWeek = 2;

	private const int LPMonthofYear = 3;

	private bool StopPressed;

	private int lsChartPeriodShown;

	private int LastPressed;

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

	internal virtual RadioButton DayButton
	{
		[CompilerGenerated]
		get
		{
			return _DayButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DayButton_CheckedChanged;
			RadioButton val = _DayButton;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_DayButton = value;
			val = _DayButton;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual RadioButton MonthButton
	{
		[CompilerGenerated]
		get
		{
			return _MonthButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = MonthButton_CheckedChanged;
			RadioButton val = _MonthButton;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_MonthButton = value;
			val = _MonthButton;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual RadioButton OtherButton
	{
		[CompilerGenerated]
		get
		{
			return _OtherButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = OtherButton_CheckedChanged;
			RadioButton val = _OtherButton;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_OtherButton = value;
			val = _OtherButton;
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

	[field: AccessedThroughProperty("FileNameLabel")]
	internal virtual Label FileNameLabel
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

	[field: AccessedThroughProperty("DayListBox")]
	internal virtual ListBox DayListBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("MonthListBox")]
	internal virtual ListBox MonthListBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
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

	internal virtual Button AutoButton
	{
		[CompilerGenerated]
		get
		{
			return _AutoButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = AutoButton_Click;
			Button val = _AutoButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_AutoButton = value;
			val = _AutoButton;
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

	internal virtual Button AutoMonthsButton
	{
		[CompilerGenerated]
		get
		{
			return _AutoMonthsButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = AutoMonthsButton_Click_1;
			Button val = _AutoMonthsButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_AutoMonthsButton = value;
			val = _AutoMonthsButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	public Seasonality()
	{
		((Form)this).Closing += Seasonality_Closing;
		((Form)this).Activated += Seasonality_Activated;
		((Form)this).Deactivate += Seasonality_Deactivate;
		((Form)this).Load += Seasonality_Load;
		StopPressed = false;
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
		//IL_06d7: Unknown result type (might be due to invalid IL or missing references)
		//IL_06e1: Expected O, but got Unknown
		//IL_07be: Unknown result type (might be due to invalid IL or missing references)
		//IL_07c8: Expected O, but got Unknown
		//IL_0829: Unknown result type (might be due to invalid IL or missing references)
		//IL_0833: Expected O, but got Unknown
		//IL_08c2: Unknown result type (might be due to invalid IL or missing references)
		//IL_08cc: Expected O, but got Unknown
		DataGridViewCellStyle val = new DataGridViewCellStyle();
		DataGridViewCellStyle val2 = new DataGridViewCellStyle();
		DataGridViewCellStyle val3 = new DataGridViewCellStyle();
		DataGridViewCellStyle val4 = new DataGridViewCellStyle();
		DoneButton = new Button();
		ClipboardButton = new Button();
		StartButton = new Button();
		ToDatePicker = new DateTimePicker();
		FromDatePicker = new DateTimePicker();
		Label3 = new Label();
		Label2 = new Label();
		DayButton = new RadioButton();
		MonthButton = new RadioButton();
		OtherButton = new RadioButton();
		HelpButton1 = new Button();
		FileNameLabel = new Label();
		DataGridView1 = new DataGridView();
		DayListBox = new ListBox();
		MonthListBox = new ListBox();
		StopButton = new Button();
		AutoButton = new Button();
		Label4 = new Label();
		LoadingBar = new ProgressBar();
		AutoMonthsButton = new Button();
		((ISupportInitialize)DataGridView1).BeginInit();
		((Control)this).SuspendLayout();
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(945, 382);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(60, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)ClipboardButton).Anchor = (AnchorStyles)10;
		((Control)ClipboardButton).Enabled = false;
		((Control)ClipboardButton).Location = new Point(791, 354);
		((Control)ClipboardButton).Name = "ClipboardButton";
		((Control)ClipboardButton).Size = new Size(60, 23);
		((Control)ClipboardButton).TabIndex = 15;
		((ButtonBase)ClipboardButton).Text = "Clip&board";
		((ButtonBase)ClipboardButton).UseVisualStyleBackColor = true;
		((Control)StartButton).Anchor = (AnchorStyles)10;
		((Control)StartButton).Location = new Point(857, 382);
		((Control)StartButton).Name = "StartButton";
		((Control)StartButton).Size = new Size(60, 23);
		((Control)StartButton).TabIndex = 19;
		((ButtonBase)StartButton).Text = "St&art";
		((ButtonBase)StartButton).UseVisualStyleBackColor = true;
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(694, 382);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(91, 20);
		((Control)ToDatePicker).TabIndex = 13;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(694, 354);
		((Control)FromDatePicker).Name = "FromDatePicker";
		FromDatePicker.ShowUpDown = true;
		((Control)FromDatePicker).Size = new Size(91, 20);
		((Control)FromDatePicker).TabIndex = 11;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)Label3).Anchor = (AnchorStyles)10;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(665, 386);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(23, 13);
		((Control)Label3).TabIndex = 12;
		Label3.Text = "&To:";
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(655, 359);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(33, 13);
		((Control)Label2).TabIndex = 10;
		Label2.Text = "&From:";
		((Control)DayButton).Anchor = (AnchorStyles)10;
		((ButtonBase)DayButton).AutoSize = true;
		DayButton.Checked = true;
		((Control)DayButton).Location = new Point(451, 359);
		((Control)DayButton).Name = "DayButton";
		((Control)DayButton).Size = new Size(85, 17);
		((Control)DayButton).TabIndex = 5;
		DayButton.TabStop = true;
		((ButtonBase)DayButton).Text = "Day of week";
		((ButtonBase)DayButton).UseVisualStyleBackColor = true;
		((Control)MonthButton).Anchor = (AnchorStyles)10;
		((ButtonBase)MonthButton).AutoSize = true;
		((Control)MonthButton).Location = new Point(451, 382);
		((Control)MonthButton).Name = "MonthButton";
		((Control)MonthButton).Size = new Size(90, 17);
		((Control)MonthButton).TabIndex = 7;
		((ButtonBase)MonthButton).Text = "Month of year";
		((ButtonBase)MonthButton).UseVisualStyleBackColor = true;
		((Control)OtherButton).Anchor = (AnchorStyles)10;
		((ButtonBase)OtherButton).AutoSize = true;
		((Control)OtherButton).Location = new Point(694, 333);
		((Control)OtherButton).Name = "OtherButton";
		((Control)OtherButton).Size = new Size(200, 17);
		((Control)OtherButton).TabIndex = 9;
		((ButtonBase)OtherButton).Text = "Other (use From and To dates below)";
		((ButtonBase)OtherButton).UseVisualStyleBackColor = true;
		((Control)HelpButton1).Anchor = (AnchorStyles)10;
		((Control)HelpButton1).Location = new Point(791, 382);
		((Control)HelpButton1).Name = "HelpButton1";
		((Control)HelpButton1).Size = new Size(60, 23);
		((Control)HelpButton1).TabIndex = 18;
		((ButtonBase)HelpButton1).Text = "&Help";
		((ButtonBase)HelpButton1).UseVisualStyleBackColor = true;
		((Control)FileNameLabel).Anchor = (AnchorStyles)14;
		FileNameLabel.BorderStyle = (BorderStyle)2;
		((Control)FileNameLabel).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)FileNameLabel).Location = new Point(3, 341);
		((Control)FileNameLabel).Name = "FileNameLabel";
		((Control)FileNameLabel).Size = new Size(442, 65);
		((Control)FileNameLabel).TabIndex = 2;
		FileNameLabel.Text = "Research says that from 1 to 10 consecutive days higher, there’s a 50% chance that a stock will close higher.";
		FileNameLabel.TextAlign = (ContentAlignment)32;
		DataGridView1.AllowUserToAddRows = false;
		DataGridView1.AllowUserToDeleteRows = false;
		DataGridView1.AllowUserToResizeRows = false;
		((Control)DataGridView1).Anchor = (AnchorStyles)15;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)10;
		((Control)DataGridView1).CausesValidation = false;
		DataGridView1.ClipboardCopyMode = (DataGridViewClipboardCopyMode)3;
		val.Alignment = (DataGridViewContentAlignment)32;
		val.BackColor = SystemColors.Control;
		val.Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		val.ForeColor = SystemColors.WindowText;
		val.SelectionBackColor = SystemColors.Highlight;
		val.SelectionForeColor = SystemColors.HighlightText;
		val.WrapMode = (DataGridViewTriState)1;
		DataGridView1.ColumnHeadersDefaultCellStyle = val;
		DataGridView1.ColumnHeadersHeightSizeMode = (DataGridViewColumnHeadersHeightSizeMode)2;
		val2.Alignment = (DataGridViewContentAlignment)64;
		val2.BackColor = SystemColors.Window;
		val2.Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		val2.ForeColor = SystemColors.ControlText;
		val2.SelectionBackColor = SystemColors.Highlight;
		val2.SelectionForeColor = SystemColors.HighlightText;
		val2.WrapMode = (DataGridViewTriState)1;
		DataGridView1.DefaultCellStyle = val2;
		DataGridView1.EditMode = (DataGridViewEditMode)4;
		((Control)DataGridView1).Location = new Point(3, 3);
		((Control)DataGridView1).Name = "DataGridView1";
		DataGridView1.ReadOnly = true;
		val3.Alignment = (DataGridViewContentAlignment)32;
		val3.BackColor = SystemColors.Control;
		val3.Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		val3.ForeColor = SystemColors.WindowText;
		val3.SelectionBackColor = SystemColors.Highlight;
		val3.SelectionForeColor = SystemColors.HighlightText;
		val3.WrapMode = (DataGridViewTriState)1;
		DataGridView1.RowHeadersDefaultCellStyle = val3;
		val4.Alignment = (DataGridViewContentAlignment)64;
		val4.WrapMode = (DataGridViewTriState)1;
		DataGridView1.RowsDefaultCellStyle = val4;
		DataGridView1.RowTemplate.ReadOnly = true;
		DataGridView1.RowTemplate.Resizable = (DataGridViewTriState)1;
		DataGridView1.SelectionMode = (DataGridViewSelectionMode)1;
		DataGridView1.ShowCellErrors = false;
		DataGridView1.ShowCellToolTips = false;
		DataGridView1.ShowEditingIcon = false;
		DataGridView1.ShowRowErrors = false;
		((Control)DataGridView1).Size = new Size(1002, 325);
		((Control)DataGridView1).TabIndex = 1;
		((Control)DayListBox).Anchor = (AnchorStyles)10;
		((Control)DayListBox).CausesValidation = false;
		((Control)DayListBox).Enabled = false;
		DayListBox.Items.AddRange(new object[7] { "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" });
		((Control)DayListBox).Location = new Point(540, 359);
		((Control)DayListBox).Name = "DayListBox";
		((Control)DayListBox).Size = new Size(100, 17);
		((Control)DayListBox).TabIndex = 6;
		((Control)MonthListBox).Anchor = (AnchorStyles)10;
		((Control)MonthListBox).Enabled = false;
		((ListControl)MonthListBox).FormattingEnabled = true;
		MonthListBox.Items.AddRange(new object[12]
		{
			"January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
			"November", "Decenber"
		});
		((Control)MonthListBox).Location = new Point(540, 383);
		((Control)MonthListBox).Name = "MonthListBox";
		((Control)MonthListBox).Size = new Size(100, 17);
		((Control)MonthListBox).TabIndex = 8;
		((Control)StopButton).Anchor = (AnchorStyles)10;
		((Control)StopButton).Enabled = false;
		((Control)StopButton).Location = new Point(857, 354);
		((Control)StopButton).Name = "StopButton";
		((Control)StopButton).Size = new Size(60, 23);
		((Control)StopButton).TabIndex = 16;
		((ButtonBase)StopButton).Text = "St&op";
		((ButtonBase)StopButton).UseVisualStyleBackColor = true;
		((Control)AutoButton).Anchor = (AnchorStyles)10;
		((Control)AutoButton).Location = new Point(920, 354);
		((Control)AutoButton).Name = "AutoButton";
		((Control)AutoButton).Size = new Size(85, 23);
		((Control)AutoButton).TabIndex = 17;
		((ButtonBase)AutoButton).Text = "&Auto Days";
		((ButtonBase)AutoButton).UseVisualStyleBackColor = true;
		((Control)Label4).Anchor = (AnchorStyles)10;
		Label4.AutoSize = true;
		((Control)Label4).Location = new Point(488, 343);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(48, 13);
		((Control)Label4).TabIndex = 3;
		Label4.Text = "Loading:";
		((Control)LoadingBar).Anchor = (AnchorStyles)10;
		((Control)LoadingBar).ForeColor = Color.Green;
		((Control)LoadingBar).Location = new Point(540, 341);
		((Control)LoadingBar).Name = "LoadingBar";
		((Control)LoadingBar).Size = new Size(100, 15);
		((Control)LoadingBar).TabIndex = 4;
		((Control)AutoMonthsButton).Anchor = (AnchorStyles)10;
		((Control)AutoMonthsButton).Location = new Point(920, 328);
		((Control)AutoMonthsButton).Name = "AutoMonthsButton";
		((Control)AutoMonthsButton).Size = new Size(85, 23);
		((Control)AutoMonthsButton).TabIndex = 14;
		((ButtonBase)AutoMonthsButton).Text = "&Auto Months";
		((ButtonBase)AutoMonthsButton).UseVisualStyleBackColor = true;
		((Form)this).AcceptButton = (IButtonControl)(object)StartButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(1008, 408);
		((Control)this).Controls.Add((Control)(object)AutoMonthsButton);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)LoadingBar);
		((Control)this).Controls.Add((Control)(object)AutoButton);
		((Control)this).Controls.Add((Control)(object)StopButton);
		((Control)this).Controls.Add((Control)(object)MonthListBox);
		((Control)this).Controls.Add((Control)(object)DayListBox);
		((Control)this).Controls.Add((Control)(object)DataGridView1);
		((Control)this).Controls.Add((Control)(object)FileNameLabel);
		((Control)this).Controls.Add((Control)(object)HelpButton1);
		((Control)this).Controls.Add((Control)(object)OtherButton);
		((Control)this).Controls.Add((Control)(object)MonthButton);
		((Control)this).Controls.Add((Control)(object)DayButton);
		((Control)this).Controls.Add((Control)(object)ToDatePicker);
		((Control)this).Controls.Add((Control)(object)FromDatePicker);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)ClipboardButton);
		((Control)this).Controls.Add((Control)(object)StartButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Name = "Seasonality";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Seasonality";
		((ISupportInitialize)DataGridView1).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void Seasonality_Closing(object sender, CancelEventArgs e)
	{
		GlobalForm.SFDayOfWeek = DayListBox.TopIndex;
		GlobalForm.SFMonthLB = checked(MonthListBox.TopIndex + 1);
		bool flag = true;
		if (flag == DayButton.Checked)
		{
			GlobalForm.SFRBSelected = GlobalForm.SFDaily;
		}
		else if (flag == MonthButton.Checked)
		{
			GlobalForm.SFRBSelected = GlobalForm.SFMONTHLY;
		}
		else if (flag == OtherButton.Checked)
		{
			GlobalForm.SFRBSelected = GlobalForm.SFOTHER;
		}
		MySettingsProperty.Settings.SeasonLocation = ((Form)this).Location;
		MySettingsProperty.Settings.SeasonSize = ((Form)this).Size;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
		GlobalForm.ChartPeriodShown = lsChartPeriodShown;
	}

	private void Seasonality_Activated(object sender, EventArgs e)
	{
		DayListBox.TopIndex = GlobalForm.SFDayOfWeek;
		MonthListBox.TopIndex = checked(GlobalForm.SFMonthLB - 1);
	}

	private void Seasonality_Deactivate(object sender, EventArgs e)
	{
		GlobalForm.SFDayOfWeek = DayListBox.TopIndex;
		GlobalForm.SFMonthLB = checked(MonthListBox.TopIndex + 1);
	}

	private void Seasonality_Load(object sender, EventArgs e)
	{
		//IL_0025: Unknown result type (might be due to invalid IL or missing references)
		//IL_002a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0035: Unknown result type (might be due to invalid IL or missing references)
		//IL_0040: Unknown result type (might be due to invalid IL or missing references)
		//IL_004b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0052: Unknown result type (might be due to invalid IL or missing references)
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
		lsChartPeriodShown = GlobalForm.ChartPeriodShown;
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.SeasonLocation, MySettingsProperty.Settings.SeasonSize);
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)AutoButton, "Automatically find the best performing days of the week.");
		val.SetToolTip((Control)(object)AutoMonthsButton, "Automatically find the best performing months of the year.");
		val.SetToolTip((Control)(object)ClipboardButton, "Copy highlighted grid rows to the clipboard.");
		val.SetToolTip((Control)(object)DayListBox, "Select the day of the week for historical performance.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)DataGridView1, "Results of the analysis are shown here. Highlight rows for clipboard copy.");
		val.SetToolTip((Control)(object)DayButton, "Find the average performance of all week days with the same name.");
		val.SetToolTip((Control)(object)FromDatePicker, "Enter the starting date to search.");
		val.SetToolTip((Control)(object)HelpButton1, "Get additional help.");
		val.SetToolTip((Control)(object)MonthButton, "Find the average performance of all months with the same name.");
		val.SetToolTip((Control)(object)MonthListBox, "Select the month for historical performance.");
		val.SetToolTip((Control)(object)OtherButton, "Fill in From and To dates. The program checks historical performance for that period.");
		val.SetToolTip((Control)(object)StartButton, "Start searching for seasonality.");
		val.SetToolTip((Control)(object)StopButton, "Halt the search.");
		val.SetToolTip((Control)(object)ToDatePicker, "Enter the ending date to search.");
		GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
		FromDatePicker.Value = Conversions.ToDate(Conversions.ToString(DateAndTime.Month(DateAndTime.Now)) + "/1/" + Conversions.ToString(DateAndTime.Year(DateAndTime.Now)));
		ToDatePicker.Value = DateAndTime.Now;
		int sFRBSelected = GlobalForm.SFRBSelected;
		if (sFRBSelected == GlobalForm.SFDaily)
		{
			DayButton.Checked = true;
			DayButton_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
		}
		else if (sFRBSelected == GlobalForm.SFMONTHLY)
		{
			MonthButton.Checked = true;
			MonthButton_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
		}
		else if (sFRBSelected == GlobalForm.SFOTHER)
		{
			OtherButton.Checked = true;
		}
		OtherButton_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
	}

	private void AutoButton_Click(object sender, EventArgs e)
	{
		//IL_0bc4: Unknown result type (might be due to invalid IL or missing references)
		LastPressed = 0;
		EnableDisable(Flag: false);
		StopPressed = false;
		DataGridView1.RowCount = 0;
		DataGridView1.ColumnCount = 15;
		DataGridView1.Columns[0].HeaderText = "Symbol";
		DataGridView1.Columns[1].HeaderText = "Last Close";
		DataGridView1.Columns[2].HeaderText = "Best Buy Day";
		DataGridView1.Columns[3].HeaderText = "Best Sell Day";
		DataGridView1.Columns[4].HeaderText = "Outlier Analysis (Buy & Sell Pivot Counts =>)";
		DataGridView1.Columns[5].HeaderText = "Buy M";
		DataGridView1.Columns[6].HeaderText = "Buy T";
		DataGridView1.Columns[7].HeaderText = "Buy W";
		DataGridView1.Columns[8].HeaderText = "Buy Th";
		DataGridView1.Columns[9].HeaderText = "Buy F";
		DataGridView1.Columns[10].HeaderText = "Sell M";
		DataGridView1.Columns[11].HeaderText = "Sell T";
		DataGridView1.Columns[12].HeaderText = "Sell W";
		DataGridView1.Columns[13].HeaderText = "Sell Th";
		DataGridView1.Columns[14].HeaderText = "Sell F";
		DateTime t = FromDatePicker.Value;
		DateTime t2 = ToDatePicker.Value;
		checked
		{
			int num = MyProject.Forms.Mainform.ListBox1.SelectedItems.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				int[] array = null;
				array = new int[5];
				int[] array2 = null;
				array2 = new int[5];
				bool flag = false;
				string text = MyProject.Forms.Mainform.ListBox1.SelectedItems[i].ToString();
				FileNameLabel.Text = text;
				((Control)FileNameLabel).Refresh();
				ProgressBar ProgBar = LoadingBar;
				Label ErrorLabel = null;
				bool num2 = GlobalForm.LoadFile(text, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
				LoadingBar = ProgBar;
				if (!OtherButton.Checked)
				{
					t = GlobalForm.nDT[0, 0];
					t2 = GlobalForm.nDT[0, GlobalForm.HLCRange];
				}
				DataGridView1.Rows.Add();
				DataGridView1.Rows[i].Cells[0].Value = text;
				if (num2)
				{
					DataGridView1.Rows[i].Cells[4].Value = "Error loading " + text;
					continue;
				}
				DataGridView1.Rows[i].Cells[1].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]).ToString();
				if (GlobalForm.IntradayData)
				{
					DataGridView1.Rows[i].Cells[4].Value = "Intraday data can't be processed.";
					continue;
				}
				int num3 = GlobalForm.HLCRange - 1;
				int j;
				int num4;
				for (j = 1; j <= num3 && DateTime.Compare(GlobalForm.nDT[0, j], t2) <= 0; j++)
				{
					if (!((DateTime.Compare(GlobalForm.nDT[0, j], t) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, j], t2) <= 0)))
					{
						continue;
					}
					flag = true;
					num4 = 2;
					do
					{
						if (DateAndTime.Weekday(GlobalForm.nDT[0, j], (FirstDayOfWeek)1) == num4)
						{
							if ((decimal.Compare(GlobalForm.nHLC[3, j - 1], GlobalForm.nHLC[3, j]) <= 0) & (decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[3, j + 1]) > 0))
							{
								array[num4 - 2]++;
							}
							else if ((decimal.Compare(GlobalForm.nHLC[3, j - 1], GlobalForm.nHLC[3, j]) >= 0) & (decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[3, j + 1]) < 0))
							{
								array2[num4 - 2]++;
							}
							break;
						}
						num4++;
					}
					while (num4 <= 6);
				}
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				if (StopPressed)
				{
					break;
				}
				if (!flag)
				{
					DataGridView1.Rows[i].Cells[4].Value = "No data available: Adjust from/to dates.";
					continue;
				}
				List<Tuple<int, int>> list = new List<Tuple<int, int>>();
				List<Tuple<int, int>> list2 = new List<Tuple<int, int>>();
				j = 2;
				do
				{
					list.Add(Tuple.Create(j, array[j - 2]));
					list2.Add(Tuple.Create(j, array2[j - 2]));
					j++;
				}
				while (j <= 6);
				list = list.OrderByDescending([SpecialName] (Tuple<int, int> z) => z.Item2).ToList();
				int item = list[0].Item2;
				string text2 = DateAndTime.WeekdayName(list[0].Item1, false, (FirstDayOfWeek)0) + " ";
				int num5 = 1;
				j = 1;
				while (list[j].Item2 == item)
				{
					text2 = text2 + DateAndTime.WeekdayName(list[j].Item1, false, (FirstDayOfWeek)0) + " ";
					num5++;
					j++;
					if (j > 4)
					{
						break;
					}
				}
				if (num5 == 5)
				{
					DataGridView1.Rows[i].Cells[3].Value = "No preference";
				}
				else
				{
					DataGridView1.Rows[i].Cells[3].Value = text2.TrimEnd(new char[0]);
				}
				list2 = list2.OrderByDescending([SpecialName] (Tuple<int, int> z) => z.Item2).ToList();
				item = list2[0].Item2;
				text2 = DateAndTime.WeekdayName(list2[0].Item1, false, (FirstDayOfWeek)0) + " ";
				num5 = 1;
				j = 1;
				while (list2[j].Item2 == item)
				{
					text2 = text2 + DateAndTime.WeekdayName(list2[j].Item1, false, (FirstDayOfWeek)0) + " ";
					num5++;
					j++;
					if (j > 4)
					{
						break;
					}
				}
				if (num5 == 5)
				{
					DataGridView1.Rows[i].Cells[2].Value = "No preference";
				}
				else
				{
					DataGridView1.Rows[i].Cells[2].Value = text2.TrimEnd(new char[0]);
				}
				_ = list2[2].Item2;
				int num6 = (int)Math.Round((double)(list2[0].Item2 + list2[1].Item2) / 2.0);
				int num7 = (int)Math.Round((double)(list2[3].Item2 + list2[4].Item2) / 2.0);
				int num8 = num6 - num7;
				int num9 = num7 + (int)Math.Round(1.5 * (double)num8);
				int num10 = num6 - (int)Math.Round(1.5 * (double)num8);
				string text3 = "";
				text2 = "";
				j = 4;
				while (list2[j].Item2 < num10)
				{
					text2 = text2 + DateAndTime.WeekdayName(list2[j].Item1, false, (FirstDayOfWeek)0) + " ";
					j += -1;
					if (j < 0)
					{
						break;
					}
				}
				text2 = text2.TrimEnd(new char[0]);
				if (text2.TrimEnd(new char[0]).Length != 0)
				{
					text3 = "Avoid buying on: " + text2 + ". ";
				}
				text2 = "";
				j = 0;
				while (list2[j].Item2 > num9)
				{
					text2 = text2 + DateAndTime.WeekdayName(list2[j].Item1, false, (FirstDayOfWeek)0) + " ";
					j++;
					if (j > 4)
					{
						break;
					}
				}
				text2 = text2.TrimEnd(new char[0]);
				if (text2.TrimEnd(new char[0]).Length != 0)
				{
					text3 = text3 + " Buy on: " + text2 + ". ";
				}
				_ = list[2].Item2;
				int num11 = (int)Math.Round((double)(list[0].Item2 + list[1].Item2) / 2.0);
				num7 = (int)Math.Round((double)(list[3].Item2 + list[4].Item2) / 2.0);
				num8 = num11 - num7;
				num9 = num7 + (int)Math.Round(1.5 * (double)num8);
				num10 = num11 - (int)Math.Round(1.5 * (double)num8);
				text2 = "";
				j = 4;
				while ((list[j].Item2 < num10) & ((list[j].Item1 != 1) & (list[j].Item1 != 7)))
				{
					text2 = text2 + DateAndTime.WeekdayName(list[j].Item1, false, (FirstDayOfWeek)0) + " ";
					j += -1;
					if (j < 0)
					{
						break;
					}
				}
				text2 = text2.TrimEnd(new char[0]);
				if (text2.TrimEnd(new char[0]).Length != 0)
				{
					text3 = text3 + "Avoid selling on: " + text2 + ". ";
				}
				text2 = "";
				j = 0;
				while ((list[j].Item2 > num9) & ((list[j].Item1 != 1) & (list[j].Item1 != 7)))
				{
					text2 = text2 + DateAndTime.WeekdayName(list[j].Item1, false, (FirstDayOfWeek)0) + " ";
					j++;
					if (j > 4)
					{
						break;
					}
				}
				text2 = text2.TrimEnd(new char[0]);
				if (text2.TrimEnd(new char[0]).Length != 0)
				{
					text3 = text3 + " Sell on: " + text2 + ". ";
				}
				if (text3.Length != 0)
				{
					DataGridView1.Rows[i].Cells[4].Value = text3.TrimEnd(new char[0]);
				}
				else
				{
					DataGridView1.Rows[i].Cells[4].Value = "There's no day which is substantially better to buy or sell.";
				}
				num4 = 0;
				do
				{
					DataGridView1.Rows[i].Cells[5 + num4].Value = array2[num4];
					DataGridView1.Rows[i].Cells[10 + num4].Value = array[num4];
					num4++;
				}
				while (num4 <= 4);
			}
			EnableDisable(Flag: true);
			MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
	}

	private void AutoMonthsButton_Click_1(object sender, EventArgs e)
	{
		//IL_0ae9: Unknown result type (might be due to invalid IL or missing references)
		LastPressed = 1;
		EnableDisable(Flag: false);
		StopPressed = false;
		DataGridView1.RowCount = 0;
		DataGridView1.ColumnCount = 29;
		DataGridView1.Columns[0].HeaderText = "Symbol";
		DataGridView1.Columns[1].HeaderText = "Last Close";
		DataGridView1.Columns[2].HeaderText = "Best Buy Month";
		DataGridView1.Columns[3].HeaderText = "Best Sell Month";
		DataGridView1.Columns[4].HeaderText = "Outlier Analysis (Buy & Sell Pivot Counts =>)";
		DateTime t = FromDatePicker.Value;
		DateTime t2 = ToDatePicker.Value;
		checked
		{
			int num = MyProject.Forms.Mainform.ListBox1.SelectedItems.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				int[] array = null;
				array = new int[12];
				int[] array2 = null;
				array2 = new int[12];
				bool flag = false;
				string text = MyProject.Forms.Mainform.ListBox1.SelectedItems[i].ToString();
				FileNameLabel.Text = text;
				((Control)FileNameLabel).Refresh();
				ProgressBar ProgBar = LoadingBar;
				Label ErrorLabel = null;
				bool num2 = GlobalForm.LoadFile(text, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
				LoadingBar = ProgBar;
				if (!OtherButton.Checked)
				{
					t = GlobalForm.nDT[0, 0];
					t2 = GlobalForm.nDT[0, GlobalForm.HLCRange];
				}
				DataGridView1.Rows.Add();
				DataGridView1.Rows[i].Cells[0].Value = text;
				if (num2)
				{
					DataGridView1.Rows[i].Cells[4].Value = "Error loading " + text;
					continue;
				}
				DataGridView1.Rows[i].Cells[1].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]).ToString();
				if (GlobalForm.IntradayData)
				{
					DataGridView1.Rows[i].Cells[4].Value = "Intraday data can't be processed.";
					continue;
				}
				int num3 = -1;
				int num4 = GlobalForm.HLCRange - 1;
				int j;
				for (j = 1; j <= num4 && DateTime.Compare(GlobalForm.nDT[0, j], t2) <= 0; j++)
				{
					if (DateAndTime.Month(GlobalForm.nDT[0, j]) != DateAndTime.Month(GlobalForm.nDT[0, j - 1]))
					{
						num3 = j - 1;
					}
					if (unchecked(DateAndTime.Month(GlobalForm.nDT[0, checked(j + 1)]) != DateAndTime.Month(GlobalForm.nDT[0, j]) && num3 != -1) && ((DateTime.Compare(GlobalForm.nDT[0, j], t) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, j], t2) <= 0)))
					{
						flag = true;
						int num5 = j;
						int nextMonth = GetNextMonth(j + 1);
						int num6 = DateAndTime.Month(GlobalForm.nDT[0, num5]);
						if ((decimal.Compare(GlobalForm.nHLC[3, num3], GlobalForm.nHLC[3, num5]) <= 0) & (decimal.Compare(GlobalForm.nHLC[3, num5], GlobalForm.nHLC[3, nextMonth]) > 0))
						{
							array[num6 - 1]++;
						}
						else if ((decimal.Compare(GlobalForm.nHLC[3, num3], GlobalForm.nHLC[3, num5]) >= 0) & (decimal.Compare(GlobalForm.nHLC[3, num5], GlobalForm.nHLC[3, nextMonth]) < 0))
						{
							array2[num6 - 1]++;
						}
					}
				}
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				if (StopPressed)
				{
					break;
				}
				if (!flag)
				{
					DataGridView1.Rows[i].Cells[4].Value = "No data available: Adjust from/to dates.";
					continue;
				}
				List<Tuple<int, int>> list = new List<Tuple<int, int>>();
				List<Tuple<int, int>> list2 = new List<Tuple<int, int>>();
				j = 0;
				do
				{
					list.Add(Tuple.Create(j + 1, array[j]));
					list2.Add(Tuple.Create(j + 1, array2[j]));
					j++;
				}
				while (j <= 11);
				list = list.OrderByDescending([SpecialName] (Tuple<int, int> z) => z.Item2).ToList();
				int item = list[0].Item2;
				string text2 = DateAndTime.MonthName(list[0].Item1, false) + " ";
				int num7 = 1;
				j = 1;
				while (list[j].Item2 == item)
				{
					text2 = text2 + DateAndTime.MonthName(list[j].Item1, false) + " ";
					num7++;
					j++;
					if (j > 11)
					{
						break;
					}
				}
				if (num7 == 12)
				{
					DataGridView1.Rows[i].Cells[3].Value = "No preference";
				}
				else
				{
					DataGridView1.Rows[i].Cells[3].Value = text2.TrimEnd(new char[0]);
				}
				list2 = list2.OrderByDescending([SpecialName] (Tuple<int, int> z) => z.Item2).ToList();
				item = list2[0].Item2;
				text2 = DateAndTime.MonthName(list2[0].Item1, false) + " ";
				num7 = 1;
				j = 1;
				while (list2[j].Item2 == item)
				{
					text2 = text2 + DateAndTime.MonthName(list2[j].Item1, false) + " ";
					num7++;
					j++;
					if (j > 11)
					{
						break;
					}
				}
				if (num7 == 12)
				{
					DataGridView1.Rows[i].Cells[2].Value = "No preference";
				}
				else
				{
					DataGridView1.Rows[i].Cells[2].Value = text2.TrimEnd(new char[0]);
				}
				_ = (int)Math.Round((double)(list2[5].Item2 + list2[6].Item2) / 2.0);
				int item2 = list2[2].Item2;
				int item3 = list2[9].Item2;
				int num8 = item2 - item3;
				int num9 = item3 + (int)Math.Round(1.5 * (double)num8);
				int num10 = item2 - (int)Math.Round(1.5 * (double)num8);
				string text3 = "";
				text2 = "";
				j = 11;
				while (list2[j].Item2 < num10)
				{
					text2 = text2 + DateAndTime.MonthName(list2[j].Item1, false) + " ";
					j += -1;
					if (j < 0)
					{
						break;
					}
				}
				text2 = text2.TrimEnd(new char[0]);
				if (text2.TrimEnd(new char[0]).Length != 0)
				{
					text3 = "Avoid buying at end of: " + text2 + ". ";
				}
				text2 = "";
				j = 0;
				while (list2[j].Item2 > num9)
				{
					text2 = text2 + DateAndTime.MonthName(list2[j].Item1, false) + " ";
					j++;
					if (j > 11)
					{
						break;
					}
				}
				text2 = text2.TrimEnd(new char[0]);
				if (text2.TrimEnd(new char[0]).Length != 0)
				{
					text3 = text3 + " Buy at end of: " + text2 + ". ";
				}
				_ = (int)Math.Round((double)(list[5].Item2 + list[6].Item2) / 2.0);
				int item4 = list[2].Item2;
				item3 = list[9].Item2;
				num8 = item4 - item3;
				num9 = item3 + (int)Math.Round(1.5 * (double)num8);
				num10 = item4 - (int)Math.Round(1.5 * (double)num8);
				text2 = "";
				j = 11;
				while (list[j].Item2 < num10)
				{
					text2 = text2 + DateAndTime.MonthName(list[j].Item1, false) + " ";
					j += -1;
					if (j < 0)
					{
						break;
					}
				}
				text2 = text2.TrimEnd(new char[0]);
				if (text2.TrimEnd(new char[0]).Length != 0)
				{
					text3 = text3 + "Avoid selling at end of: " + text2 + ". ";
				}
				text2 = "";
				j = 0;
				while (list[j].Item2 > num9)
				{
					text2 = text2 + DateAndTime.MonthName(list[j].Item1, false) + " ";
					j++;
					if (j > 11)
					{
						break;
					}
				}
				text2 = text2.TrimEnd(new char[0]);
				if (text2.TrimEnd(new char[0]).Length != 0)
				{
					text3 = text3 + " Sell at end of: " + text2 + ". ";
				}
				if (text3.Length != 0)
				{
					DataGridView1.Rows[i].Cells[4].Value = text3.TrimEnd(new char[0]);
				}
				else
				{
					DataGridView1.Rows[i].Cells[4].Value = "There's no month which is substantially better to buy or sell.";
				}
				j = 0;
				do
				{
					DataGridView1.Rows[i].Cells[5 + j].Value = array2[j];
					DataGridView1.Rows[i].Cells[17 + j].Value = array[j];
					DataGridView1.Columns[5 + j].HeaderText = "Buy " + Strings.Left(DateAndTime.MonthName(j + 1, false), 3);
					DataGridView1.Columns[17 + j].HeaderText = "Sell " + Strings.Left(DateAndTime.MonthName(j + 1, false), 3);
					j++;
				}
				while (j <= 11);
			}
			EnableDisable(Flag: true);
			MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
	}

	private void ClipboardButton_Click(object sender, EventArgs e)
	{
		//IL_01db: Unknown result type (might be due to invalid IL or missing references)
		//IL_0244: Unknown result type (might be due to invalid IL or missing references)
		if (((BaseCollection)DataGridView1.SelectedRows).Count == 0)
		{
			DataGridView1.SelectAll();
		}
		FileNameLabel.Text = "";
		((Control)this).Cursor = Cursors.WaitCursor;
		string text;
		switch (LastPressed)
		{
		case 2:
			text = "The days higher/lower counts the number of times price closes higher or lower during the day selected, starting from the day before to day's end.";
			text += "\r\nThe target is the last closing price plus the larger of the gain or loss.";
			text = text + "\r\nSelected: " + Conversions.ToString(Interaction.IIf(DayButton.Checked, (object)("Day of week, " + DayListBox.Items[DayListBox.TopIndex].ToString()), (object)("Month of year, " + MonthListBox.Items[MonthListBox.TopIndex].ToString())));
			break;
		case 3:
			text = "The months higher/lower counts the number of times price closes higher or lower during the month selected, starting from the day before the month starts to the day the month ends.";
			text += "\r\nThe target is the last closing price plus the larger of the gain or loss.";
			text = text + "\r\nSelected: " + Conversions.ToString(Interaction.IIf(DayButton.Checked, (object)("Day of week, " + DayListBox.Items[DayListBox.TopIndex].ToString()), (object)("Month of year, " + MonthListBox.Items[MonthListBox.TopIndex].ToString())));
			break;
		case 0:
		case 1:
			text = "Counts closing price turns (from down/equal to closing up, or up/equal to closing down), at the end of a price trend to determine the best buy day or month.";
			break;
		default:
			text = "";
			break;
		}
		text += "\r\nCopyright (c) 2016-2024 by Thomas Bulkowski and ThePatternSite.com. All rights reserved.";
		text += "\r\n\r\n";
		try
		{
			Clipboard.SetDataObject((object)DataGridView1.GetClipboardContent());
			text += Clipboard.GetText();
			Clipboard.SetText(text);
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			MessageBox.Show("Clipboard is busy with another user. Error: " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			ProjectData.ClearProjectError();
		}
		finally
		{
			FileNameLabel.Text = ((BaseCollection)DataGridView1.SelectedRows).Count + " rows copied.";
			MessageBox.Show("Done! " + ((BaseCollection)DataGridView1.SelectedRows).Count + " rows copied.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
		((Control)this).Cursor = Cursors.Default;
	}

	private void DayButton_CheckedChanged(object sender, EventArgs e)
	{
		((Control)DayListBox).Enabled = DayButton.Checked;
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void EnableDisable(bool Flag)
	{
		((Control)AutoButton).Enabled = Flag;
		((Control)AutoMonthsButton).Enabled = Flag;
		((Control)ClipboardButton).Enabled = Flag;
		((Control)DayButton).Enabled = Flag;
		if (DayButton.Checked)
		{
			((Control)DayListBox).Enabled = Flag;
		}
		((Control)DoneButton).Enabled = Flag;
		if (OtherButton.Checked)
		{
			((Control)FromDatePicker).Enabled = Flag;
			((Control)ToDatePicker).Enabled = Flag;
		}
		((Control)HelpButton1).Enabled = Flag;
		((Control)MonthButton).Enabled = Flag;
		if (MonthButton.Checked)
		{
			((Control)MonthListBox).Enabled = Flag;
		}
		((Control)OtherButton).Enabled = Flag;
		((Control)StopButton).Enabled = !Flag;
		((Control)StartButton).Enabled = Flag;
	}

	private int GetNextMonth(int i)
	{
		checked
		{
			int num = i + 31;
			if (num > GlobalForm.HLCRange)
			{
				num = GlobalForm.HLCRange;
			}
			int num2 = i + 1;
			int num3 = num;
			for (int j = num2; j <= num3; j++)
			{
				if (DateAndTime.Month(GlobalForm.nDT[0, j]) != DateAndTime.Month(GlobalForm.nDT[0, i]))
				{
					return j - 1;
				}
			}
			return num;
		}
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_0099: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat("Use this form to find how price has performed historically over various periods, sorted by price closing up and down. This can help you determine if performance is seasonal (periodic)." + "\r\n\r\n", "DAY OF WEEK: Select this to compare the closing price change for the weekday. For example, if you select Wednesday, the program will average the price change from Tuesday's to Wednesday's close for all matching periods in the file."), "\r\n\r\n"), "DAY OF MONTH: Same as day of week only it applies to months."), "\r\n\r\n"), "OTHER: Select the 'From' and 'To' dates. The program will use the closing price the day before the 'From' date to the close on the 'To' date to get the average performance over prior matching periods."), "\r\n\r\n"), "AUTO (days/months): This counts closing price turns (from down/equal to closing up, or up/equal to closing down), at the end of a trend. It reports the best buy and sell days/months plus outliers, where price may turn on the same day often. I include the count of closing price turns (down/equal to closing up, or up/equal to closing down)."), "\r\n\r\n"), "And yes, you can have a 'best buy and sell' on the same day. Imagine price closing down on Monday and up on Tuesday. Monday would be a buy day. Now imagine the next week price closing up on Monday and down on Tuesday. Monday would be a sell day. Monday is both a best day to buy and sell, but they occur on different weeks."), "\r\n\r\n"), "Note: The longer the data files, the better the results, but long files will tend to slow Patternz."), "\r\n\r\n"), "Grid column explanation. Target: This is the average gain or loss added to/subtracted from the last close. Consecutive closes: A count of how many times price has closed higher or lower from the most recent close. Days/months higher/lower: A count of the number of times price has closed higher or lower. Avg (average) gain/loss: The average gain or loss for when price closed higher/lower."), "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void MonthButton_CheckedChanged(object sender, EventArgs e)
	{
		((Control)MonthListBox).Enabled = MonthButton.Checked;
	}

	private void OtherButton_CheckedChanged(object sender, EventArgs e)
	{
		((Control)FromDatePicker).Enabled = OtherButton.Checked;
		((Control)ToDatePicker).Enabled = OtherButton.Checked;
	}

	private void SetupGridHeader()
	{
		DataGridView1.RowCount = 0;
		DataGridView1.ColumnCount = 8;
		DataGridView1.Columns[0].HeaderText = "Symbol";
		DataGridView1.Columns[1].HeaderText = "Last Close";
		DataGridView1.Columns[2].HeaderText = "Target";
		DataGridView1.Columns[3].HeaderText = "Consecutive Closes";
		DataGridView1.Columns[5].HeaderText = "Avg Gain";
		DataGridView1.Columns[7].HeaderText = "Avg Loss";
		if (DayButton.Checked | OtherButton.Checked)
		{
			DataGridView1.Columns[4].HeaderText = "Days Higher";
			DataGridView1.Columns[6].HeaderText = "Days Lower";
		}
		else if (MonthButton.Checked)
		{
			DataGridView1.Columns[4].HeaderText = "Months Higher";
			DataGridView1.Columns[6].HeaderText = "Months Lower";
		}
	}

	private void StartButton_Click(object sender, EventArgs e)
	{
		//IL_0c02: Unknown result type (might be due to invalid IL or missing references)
		//IL_014a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0150: Invalid comparison between Unknown and I4
		int num = 0;
		LastPressed = Conversions.ToInteger(Interaction.IIf(DayButton.Checked, (object)2, (object)3));
		DataGridView1.RowHeadersVisible = false;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)1;
		EnableDisable(Flag: false);
		SetupGridHeader();
		StopPressed = false;
		LoadingBar.Value = 1;
		int count = MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count;
		checked
		{
			int num2 = count - 1;
			for (int i = 0; i <= num2; i++)
			{
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				if (StopPressed)
				{
					break;
				}
				string text = MyProject.Forms.Mainform.ListBox1.SelectedItems[i].ToString();
				FileNameLabel.Text = text;
				((Control)FileNameLabel).Refresh();
				bool flag;
				if (count == 1)
				{
					ProgressBar ProgBar = LoadingBar;
					Label ErrorLabel = null;
					bool num3 = GlobalForm.LoadFile(text, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
					LoadingBar = ProgBar;
					flag = num3;
				}
				else
				{
					ProgressBar ProgBar = null;
					Label ErrorLabel = null;
					flag = GlobalForm.LoadFile(text, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
				}
				if (GlobalForm.IntradayData)
				{
					FileNameLabel.Text = text + " skipped!";
					if (unchecked((int)MessageBox.Show(text + " contains intraday data, so I'll skip it. Did you want to continue scanning (any other files)?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32)) == 7)
					{
						break;
					}
					continue;
				}
				if (!flag)
				{
					int num4 = 0;
					decimal d = default(decimal);
					int num5 = 0;
					decimal d2 = default(decimal);
					if (DayButton.Checked)
					{
						int num6 = DayListBox.TopIndex + 1;
						int hLCRange = GlobalForm.HLCRange;
						for (int j = 1; j <= hLCRange; j++)
						{
							if (DateAndTime.Weekday(GlobalForm.nDT[0, j], (FirstDayOfWeek)1) == num6)
							{
								if (decimal.Compare(GlobalForm.nHLC[3, j - 1], GlobalForm.nHLC[3, j]) < 0)
								{
									num4++;
									d = decimal.Add(d, decimal.Subtract(GlobalForm.nHLC[3, j], GlobalForm.nHLC[3, j - 1]));
								}
								else if (decimal.Compare(GlobalForm.nHLC[3, j - 1], GlobalForm.nHLC[3, j]) > 0)
								{
									num5++;
									d2 = decimal.Add(d2, decimal.Subtract(GlobalForm.nHLC[3, j], GlobalForm.nHLC[3, j - 1]));
								}
							}
						}
					}
					else if (MonthButton.Checked)
					{
						int num6 = MonthListBox.TopIndex + 1;
						decimal num7 = default(decimal);
						decimal num8 = default(decimal);
						int num9 = GlobalForm.HLCRange - 1;
						for (int k = 1; k <= num9; k++)
						{
							if ((DateAndTime.Month(GlobalForm.nDT[0, k]) != DateAndTime.Month(GlobalForm.nDT[0, k - 1])) & (DateAndTime.Month(GlobalForm.nDT[0, k]) == num6))
							{
								num7 = GlobalForm.nHLC[3, k - 1];
							}
							else
							{
								if (!((DateAndTime.Month(GlobalForm.nDT[0, k + 1]) != DateAndTime.Month(GlobalForm.nDT[0, k])) & (DateAndTime.Month(GlobalForm.nDT[0, k]) == num6)))
								{
									continue;
								}
								num8 = GlobalForm.nHLC[3, k];
								if (decimal.Compare(num7, 0m) != 0)
								{
									decimal num10 = decimal.Subtract(num8, num7);
									if (decimal.Compare(num10, 0m) > 0)
									{
										num4++;
										d = decimal.Add(d, num10);
									}
									else if (decimal.Compare(num10, 0m) < 0)
									{
										num5++;
										d2 = decimal.Add(d2, num10);
									}
								}
							}
						}
					}
					else if (OtherButton.Checked)
					{
						DateTime FromDate = FromDatePicker.Value.Date;
						DateTime ToDate = ToDatePicker.Value.Date;
						GlobalForm.SwapDates(ref FromDate, ref ToDate);
						FromDate = Conversions.ToDate(Conversions.ToString(DateAndTime.Month(FromDate)) + "/" + Conversions.ToString(DateAndTime.Day(FromDate)) + "/" + Conversions.ToString(DateAndTime.Year(GlobalForm.nDT[0, 1])));
						ToDate = Conversions.ToDate(Conversions.ToString(DateAndTime.Month(ToDate)) + "/" + Conversions.ToString(DateAndTime.Day(ToDate)) + "/" + Conversions.ToString(DateAndTime.Year(GlobalForm.nDT[0, 1])));
						decimal num11 = default(decimal);
						decimal num12 = default(decimal);
						int num13 = GlobalForm.HLCRange - 1;
						for (int l = 1; l <= num13; l++)
						{
							if (DateAndTime.Year(GlobalForm.nDT[0, l]) != DateAndTime.Year(GlobalForm.nDT[0, l - 1]))
							{
								FromDate = Conversions.ToDate(Conversions.ToString(DateAndTime.Month(FromDate)) + "/" + Conversions.ToString(DateAndTime.Day(FromDate)) + "/" + Conversions.ToString(DateAndTime.Year(GlobalForm.nDT[0, l])));
								ToDate = Conversions.ToDate(Conversions.ToString(DateAndTime.Month(ToDate)) + "/" + Conversions.ToString(DateAndTime.Day(ToDate)) + "/" + Conversions.ToString(DateAndTime.Year(GlobalForm.nDT[0, l])));
							}
							if ((DateTime.Compare(GlobalForm.nDT[0, l], FromDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, l - 1], FromDate) < 0))
							{
								num11 = GlobalForm.nHLC[3, l - 1];
							}
							else
							{
								if (!((DateTime.Compare(GlobalForm.nDT[0, l], ToDate) <= 0) & (DateTime.Compare(GlobalForm.nDT[0, l + 1], ToDate) > 0)))
								{
									continue;
								}
								num12 = GlobalForm.nHLC[3, l];
								if (decimal.Compare(num11, 0m) != 0)
								{
									decimal num10 = decimal.Subtract(num12, num11);
									if (decimal.Compare(num10, 0m) > 0)
									{
										num4++;
										d = decimal.Add(d, num10);
									}
									else if (decimal.Compare(num10, 0m) < 0)
									{
										num5++;
										d2 = decimal.Add(d2, num10);
									}
								}
							}
						}
					}
					if (GlobalForm.HLCRange > 0)
					{
						int num14 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[3, GlobalForm.HLCRange], GlobalForm.nHLC[3, GlobalForm.HLCRange - 1]) < 0, (object)(-1), (object)1));
						int num15 = 0;
						for (int m = GlobalForm.HLCRange; m >= 1; m += -1)
						{
							if (num14 == -1)
							{
								if (decimal.Compare(GlobalForm.nHLC[3, m - 1], GlobalForm.nHLC[3, m]) < 0)
								{
									break;
								}
								num15++;
							}
							else
							{
								if (decimal.Compare(GlobalForm.nHLC[3, m - 1], GlobalForm.nHLC[3, m]) > 0)
								{
									break;
								}
								num15++;
							}
						}
						DataGridView1.Rows.Add();
						DataGridView1.Rows[num].Cells[0].Value = text;
						DataGridView1.Rows[num].Cells[1].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]).ToString();
						DataGridView1.Rows[num].Cells[3].Value = num15 + " day" + Conversions.ToString(Interaction.IIf(num15 > 1, (object)"s ", (object)" ")) + Conversions.ToString(Interaction.IIf(num14 == 1, (object)"up", (object)"down"));
						decimal num16 = default(decimal);
						DataGridView1.Rows[num].Cells[4].Value = Strings.Format((object)num4, "");
						if (num4 != 0)
						{
							num16 = decimal.Divide(d, new decimal(num4));
						}
						DataGridView1.Rows[num].Cells[5].Value = Strings.Format((object)num16, "$0.00");
						decimal num17 = default(decimal);
						DataGridView1.Rows[num].Cells[6].Value = Strings.Format((object)num5, "");
						if (num5 != 0)
						{
							num17 = decimal.Divide(d2, new decimal(num5));
						}
						DataGridView1.Rows[num].Cells[7].Value = Strings.Format((object)num17, "$0.00");
						if (num5 == num4)
						{
							if (decimal.Compare(decimal.Add(GlobalForm.nHLC[3, GlobalForm.HLCRange], num17), 0m) > 0)
							{
								DataGridView1.Rows[num].Cells[2].Value = GlobalForm.LimitDecimals(decimal.Add(GlobalForm.nHLC[3, GlobalForm.HLCRange], num16)) + " or " + GlobalForm.LimitDecimals(decimal.Add(GlobalForm.nHLC[3, GlobalForm.HLCRange], num17));
							}
							else
							{
								DataGridView1.Rows[num].Cells[2].Value = GlobalForm.LimitDecimals(decimal.Add(GlobalForm.nHLC[3, GlobalForm.HLCRange], num16)).ToString();
							}
						}
						else if ((decimal.Compare(Math.Abs(num17), num16) > 0) & (decimal.Compare(decimal.Add(GlobalForm.nHLC[3, GlobalForm.HLCRange], num17), 0m) < 0))
						{
							DataGridView1.Rows[num].Cells[2].Value = "Unknown (below 0)";
						}
						else
						{
							string text2 = GlobalForm.LimitDecimals(decimal.Add(GlobalForm.nHLC[3, GlobalForm.HLCRange], Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num16, Math.Abs(num17)) > 0, (object)num16, (object)num17)))).ToString();
							text2 = text2 + " " + Conversions.ToString(Interaction.IIf(decimal.Compare(num16, Math.Abs(num17)) > 0, (object)("+" + GlobalForm.LimitDecimals(num16)), (object)GlobalForm.LimitDecimals(num17).ToString()));
							DataGridView1.Rows[num].Cells[2].Value = text2;
						}
						num++;
					}
				}
				if (count > 1)
				{
					LoadingBar.Value = (int)Math.Round((double)(100 * i) / (double)MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count);
				}
			}
			EnableDisable(Flag: true);
			DataGridView1.SelectAll();
			LoadingBar.Value = 100;
			FileNameLabel.Text = "Done!";
			DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)6;
			DataGridView1.RowHeadersVisible = true;
			MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			LoadingBar.Value = 0;
		}
	}

	private void StopButton_Click(object sender, EventArgs e)
	{
		StopPressed = true;
	}
}
