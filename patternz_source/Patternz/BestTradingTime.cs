using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class BestTradingTime : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("StopButton")]
	private Button _StopButton;

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
	[AccessedThroughProperty("UseDatesCheckBox")]
	private CheckBox _UseDatesCheckBox;

	private const int GRIDFILENAME = 0;

	private const int GRIDCOLCOUNT = 13;

	private bool StopPressed;

	private int[] MonthTotals;

	private int[] Outliers;

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

	[field: AccessedThroughProperty("DataGridView1")]
	internal virtual DataGridView DataGridView1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("FileNameLabel")]
	internal virtual Label FileNameLabel
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

	[field: AccessedThroughProperty("Low2HighButton")]
	internal virtual RadioButton Low2HighButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Close2CloseButton")]
	internal virtual RadioButton Close2CloseButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
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

	[field: AccessedThroughProperty("DoneButton")]
	internal virtual Button DoneButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("TargetGain")]
	internal virtual NumericUpDown TargetGain
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

	[field: AccessedThroughProperty("Label5")]
	internal virtual Label Label5
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("PriceBars")]
	internal virtual NumericUpDown PriceBars
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

	internal virtual CheckBox UseDatesCheckBox
	{
		[CompilerGenerated]
		get
		{
			return _UseDatesCheckBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = UseDatesCheckBox_CheckedChanged;
			CheckBox val = _UseDatesCheckBox;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_UseDatesCheckBox = value;
			val = _UseDatesCheckBox;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	public BestTradingTime()
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		((Form)this).FormClosing += new FormClosingEventHandler(BestTradingTime_FormClosing);
		((Form)this).Load += BestTradingTime_Load;
		StopPressed = false;
		MonthTotals = new int[13];
		Outliers = new int[13];
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
		//IL_0302: Unknown result type (might be due to invalid IL or missing references)
		//IL_030c: Expected O, but got Unknown
		//IL_036d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0377: Expected O, but got Unknown
		//IL_0412: Unknown result type (might be due to invalid IL or missing references)
		//IL_041c: Expected O, but got Unknown
		//IL_051b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0525: Expected O, but got Unknown
		DataGridViewCellStyle val = new DataGridViewCellStyle();
		DataGridViewCellStyle val2 = new DataGridViewCellStyle();
		DataGridViewCellStyle val3 = new DataGridViewCellStyle();
		DataGridViewCellStyle val4 = new DataGridViewCellStyle();
		Label4 = new Label();
		LoadingBar = new ProgressBar();
		StopButton = new Button();
		DataGridView1 = new DataGridView();
		FileNameLabel = new Label();
		HelpButton1 = new Button();
		Low2HighButton = new RadioButton();
		Close2CloseButton = new RadioButton();
		ToDatePicker = new DateTimePicker();
		FromDatePicker = new DateTimePicker();
		Label3 = new Label();
		Label2 = new Label();
		ClipboardButton = new Button();
		StartButton = new Button();
		DoneButton = new Button();
		TargetGain = new NumericUpDown();
		Label1 = new Label();
		Label5 = new Label();
		PriceBars = new NumericUpDown();
		Panel1 = new Panel();
		UseDatesCheckBox = new CheckBox();
		((ISupportInitialize)DataGridView1).BeginInit();
		((ISupportInitialize)TargetGain).BeginInit();
		((ISupportInitialize)PriceBars).BeginInit();
		((Control)Panel1).SuspendLayout();
		((Control)this).SuspendLayout();
		((Control)Label4).Anchor = (AnchorStyles)10;
		Label4.AutoSize = true;
		((Control)Label4).Location = new Point(692, 333);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(45, 13);
		((Control)Label4).TabIndex = 1;
		Label4.Text = "Loading";
		((Control)LoadingBar).Anchor = (AnchorStyles)10;
		((Control)LoadingBar).ForeColor = Color.Green;
		((Control)LoadingBar).Location = new Point(684, 353);
		((Control)LoadingBar).Name = "LoadingBar";
		((Control)LoadingBar).Size = new Size(60, 23);
		((Control)LoadingBar).TabIndex = 2;
		((Control)StopButton).Anchor = (AnchorStyles)10;
		((Control)StopButton).Enabled = false;
		((Control)StopButton).Location = new Point(618, 353);
		((Control)StopButton).Name = "StopButton";
		((Control)StopButton).Size = new Size(60, 23);
		((Control)StopButton).TabIndex = 13;
		((ButtonBase)StopButton).Text = "St&op";
		((ButtonBase)StopButton).UseVisualStyleBackColor = true;
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
		DataGridView1.MultiSelect = false;
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
		DataGridView1.SelectionMode = (DataGridViewSelectionMode)0;
		DataGridView1.ShowCellErrors = false;
		DataGridView1.ShowCellToolTips = false;
		DataGridView1.ShowEditingIcon = false;
		DataGridView1.ShowRowErrors = false;
		((Control)DataGridView1).Size = new Size(741, 324);
		((Control)DataGridView1).TabIndex = 4;
		((Control)FileNameLabel).Anchor = (AnchorStyles)10;
		FileNameLabel.BorderStyle = (BorderStyle)2;
		((Control)FileNameLabel).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)FileNameLabel).Location = new Point(3, 338);
		((Control)FileNameLabel).Name = "FileNameLabel";
		((Control)FileNameLabel).Size = new Size(202, 66);
		((Control)FileNameLabel).TabIndex = 5;
		FileNameLabel.TextAlign = (ContentAlignment)32;
		((Control)HelpButton1).Anchor = (AnchorStyles)10;
		((Control)HelpButton1).Location = new Point(552, 381);
		((Control)HelpButton1).Name = "HelpButton1";
		((Control)HelpButton1).Size = new Size(60, 23);
		((Control)HelpButton1).TabIndex = 14;
		((ButtonBase)HelpButton1).Text = "&Help";
		((ButtonBase)HelpButton1).UseVisualStyleBackColor = true;
		((Control)Low2HighButton).Anchor = (AnchorStyles)10;
		((ButtonBase)Low2HighButton).AutoSize = true;
		((Control)Low2HighButton).Location = new Point(116, 44);
		((Control)Low2HighButton).Name = "Low2HighButton";
		((Control)Low2HighButton).Size = new Size(80, 17);
		((Control)Low2HighButton).TabIndex = 5;
		((ButtonBase)Low2HighButton).Text = "Low to high";
		((ButtonBase)Low2HighButton).UseVisualStyleBackColor = true;
		((Control)Close2CloseButton).Anchor = (AnchorStyles)10;
		((ButtonBase)Close2CloseButton).AutoSize = true;
		Close2CloseButton.Checked = true;
		((Control)Close2CloseButton).Location = new Point(9, 44);
		((Control)Close2CloseButton).Name = "Close2CloseButton";
		((Control)Close2CloseButton).Size = new Size(91, 17);
		((Control)Close2CloseButton).TabIndex = 4;
		Close2CloseButton.TabStop = true;
		((ButtonBase)Close2CloseButton).Text = "Close to close";
		((ButtonBase)Close2CloseButton).UseVisualStyleBackColor = true;
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(455, 381);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(91, 20);
		((Control)ToDatePicker).TabIndex = 11;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(455, 353);
		((Control)FromDatePicker).Name = "FromDatePicker";
		FromDatePicker.ShowUpDown = true;
		((Control)FromDatePicker).Size = new Size(91, 20);
		((Control)FromDatePicker).TabIndex = 9;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)Label3).Anchor = (AnchorStyles)10;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(426, 385);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(23, 13);
		((Control)Label3).TabIndex = 10;
		Label3.Text = "&To:";
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(416, 358);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(33, 13);
		((Control)Label2).TabIndex = 8;
		Label2.Text = "&From:";
		((Control)ClipboardButton).Anchor = (AnchorStyles)10;
		((Control)ClipboardButton).Enabled = false;
		((Control)ClipboardButton).Location = new Point(552, 353);
		((Control)ClipboardButton).Name = "ClipboardButton";
		((Control)ClipboardButton).Size = new Size(60, 23);
		((Control)ClipboardButton).TabIndex = 12;
		((ButtonBase)ClipboardButton).Text = "Clip&board";
		((ButtonBase)ClipboardButton).UseVisualStyleBackColor = true;
		((Control)StartButton).Anchor = (AnchorStyles)10;
		((Control)StartButton).Location = new Point(618, 381);
		((Control)StartButton).Name = "StartButton";
		((Control)StartButton).Size = new Size(60, 23);
		((Control)StartButton).TabIndex = 0;
		((ButtonBase)StartButton).Text = "St&art";
		((ButtonBase)StartButton).UseVisualStyleBackColor = true;
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(684, 382);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(60, 23);
		((Control)DoneButton).TabIndex = 3;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)TargetGain).Anchor = (AnchorStyles)10;
		((Control)TargetGain).Location = new Point(136, 0);
		TargetGain.Maximum = new decimal(new int[4] { 1000, 0, 0, 0 });
		TargetGain.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)TargetGain).Name = "TargetGain";
		((Control)TargetGain).Size = new Size(58, 20);
		((Control)TargetGain).TabIndex = 1;
		TargetGain.Value = new decimal(new int[4] { 5, 0, 0, 0 });
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(6, 2);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(126, 13);
		((Control)Label1).TabIndex = 0;
		Label1.Text = "I want this gain (percent):";
		((Control)Label5).Anchor = (AnchorStyles)10;
		Label5.AutoSize = true;
		((Control)Label5).Location = new Point(6, 23);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(118, 13);
		((Control)Label5).TabIndex = 2;
		Label5.Text = "In this time (price bars): ";
		((Control)PriceBars).Anchor = (AnchorStyles)10;
		((Control)PriceBars).Location = new Point(136, 21);
		PriceBars.Maximum = new decimal(new int[4] { 261, 0, 0, 0 });
		PriceBars.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)PriceBars).Name = "PriceBars";
		((Control)PriceBars).Size = new Size(58, 20);
		((Control)PriceBars).TabIndex = 3;
		PriceBars.Value = new decimal(new int[4] { 10, 0, 0, 0 });
		((Control)Panel1).Anchor = (AnchorStyles)10;
		((Control)Panel1).Controls.Add((Control)(object)TargetGain);
		((Control)Panel1).Controls.Add((Control)(object)Label5);
		((Control)Panel1).Controls.Add((Control)(object)PriceBars);
		((Control)Panel1).Controls.Add((Control)(object)Label1);
		((Control)Panel1).Controls.Add((Control)(object)Close2CloseButton);
		((Control)Panel1).Controls.Add((Control)(object)Low2HighButton);
		((Control)Panel1).Location = new Point(211, 337);
		((Control)Panel1).Name = "Panel1";
		((Control)Panel1).Size = new Size(199, 67);
		((Control)Panel1).TabIndex = 6;
		((Control)UseDatesCheckBox).Anchor = (AnchorStyles)10;
		((ButtonBase)UseDatesCheckBox).AutoSize = true;
		((Control)UseDatesCheckBox).Location = new Point(458, 333);
		((Control)UseDatesCheckBox).Name = "UseDatesCheckBox";
		((Control)UseDatesCheckBox).Size = new Size(105, 17);
		((Control)UseDatesCheckBox).TabIndex = 7;
		((ButtonBase)UseDatesCheckBox).Text = "Use dates below";
		((ButtonBase)UseDatesCheckBox).UseVisualStyleBackColor = true;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(754, 407);
		((Control)this).Controls.Add((Control)(object)UseDatesCheckBox);
		((Control)this).Controls.Add((Control)(object)Panel1);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)LoadingBar);
		((Control)this).Controls.Add((Control)(object)StopButton);
		((Control)this).Controls.Add((Control)(object)DataGridView1);
		((Control)this).Controls.Add((Control)(object)FileNameLabel);
		((Control)this).Controls.Add((Control)(object)HelpButton1);
		((Control)this).Controls.Add((Control)(object)ToDatePicker);
		((Control)this).Controls.Add((Control)(object)FromDatePicker);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)ClipboardButton);
		((Control)this).Controls.Add((Control)(object)StartButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Name = "BestTradingTime";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Best Trading Time";
		((ISupportInitialize)DataGridView1).EndInit();
		((ISupportInitialize)TargetGain).EndInit();
		((ISupportInitialize)PriceBars).EndInit();
		((Control)Panel1).ResumeLayout(false);
		((Control)Panel1).PerformLayout();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void BestTradingTime_FormClosing(object sender, FormClosingEventArgs e)
	{
		MySettingsProperty.Settings.BestTradingTimeLocation = ((Form)this).Location;
		MySettingsProperty.Settings.BestTradingTimeSize = ((Form)this).Size;
		MySettingsProperty.Settings.BestTradingTimePct = Convert.ToInt32(TargetGain.Value);
		MySettingsProperty.Settings.BestTradingTimeBars = Convert.ToInt32(PriceBars.Value);
		MySettingsProperty.Settings.BestTradingTimeUseDates = UseDatesCheckBox.Checked;
		MySettingsProperty.Settings.BestTradingTimeClose2Close = Close2CloseButton.Checked;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
	}

	private void BestTradingTime_Load(object sender, EventArgs e)
	{
		//IL_00b5: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ba: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c5: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00db: Unknown result type (might be due to invalid IL or missing references)
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
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.BestTradingTimeLocation, MySettingsProperty.Settings.BestTradingTimeSize);
		TargetGain.Value = new decimal(MySettingsProperty.Settings.BestTradingTimePct);
		PriceBars.Value = new decimal(MySettingsProperty.Settings.BestTradingTimeBars);
		UseDatesCheckBox.Checked = MySettingsProperty.Settings.BestTradingTimeUseDates;
		((Control)FromDatePicker).Enabled = UseDatesCheckBox.Checked;
		((Control)ToDatePicker).Enabled = UseDatesCheckBox.Checked;
		if (MySettingsProperty.Settings.BestTradingTimeClose2Close)
		{
			Close2CloseButton.Checked = true;
		}
		else
		{
			Low2HighButton.Checked = true;
		}
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)ClipboardButton, "Copy all grid rows to clipboard.");
		val.SetToolTip((Control)(object)Close2CloseButton, "Measure the gain using closing prices instead of low to high.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)DataGridView1, "Results of analysis shown here.");
		val.SetToolTip((Control)(object)FromDatePicker, "Enter the starting date to search.");
		val.SetToolTip((Control)(object)HelpButton1, "Get additional help.");
		val.SetToolTip((Control)(object)Low2HighButton, "Measure the gain using low to high prices instead of close to close.");
		val.SetToolTip((Control)(object)PriceBars, "Specify amount of time for price to rise. Max: 261 (1 year), in price bars");
		val.SetToolTip((Control)(object)StartButton, "Start searching for gains.");
		val.SetToolTip((Control)(object)StopButton, "Halt the search.");
		val.SetToolTip((Control)(object)TargetGain, "Search the stock for this percentage gain.");
		val.SetToolTip((Control)(object)ToDatePicker, "Enter the ending date to search.");
		val.SetToolTip((Control)(object)UseDatesCheckBox, "Check to use 'from' and 'to' dates. Unchecked means use all dates.");
		GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
		FromDatePicker.Value = Conversions.ToDate("1/1/" + Conversions.ToString(DateAndTime.Year(DateAndTime.Now)));
		ToDatePicker.Value = DateAndTime.Now;
	}

	private void ClipboardButton_Click(object sender, EventArgs e)
	{
		//IL_0170: Unknown result type (might be due to invalid IL or missing references)
		//IL_01dd: Unknown result type (might be due to invalid IL or missing references)
		((Control)this).Cursor = Cursors.WaitCursor;
		DataGridView1.MultiSelect = true;
		DataGridView1.SelectAll();
		string text = ((!UseDatesCheckBox.Checked) ? "Using ALL data in the files" : ("Using data from " + FromDatePicker.Text + " to " + ToDatePicker.Text));
		text = text + ", measured using " + Conversions.ToString(Interaction.IIf(Close2CloseButton.Checked, (object)"close to close prices", (object)"low to high prices")) + " as of " + Strings.Format((object)DateAndTime.Now, GlobalForm.UserDate) + ".";
		text += "\r\n";
		text = text + "Searching for a " + TargetGain.Value + " percent gain in " + PriceBars.Value + " price bars. Table numbers reflect how often that happens each month.";
		text += "\r\nCopyright (c) 2016-2024 by Thomas Bulkowski and ThePatternSite.com. All rights reserved.\r\n\r\n";
		checked
		{
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
				FileNameLabel.Text = 1 + DataGridView1.Rows.Count + " rows copied.";
				MessageBox.Show("Done! " + (1 + DataGridView1.Rows.Count) + " rows copied.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
			DataGridView1.MultiSelect = false;
			((Control)this).Cursor = Cursors.Default;
		}
	}

	private void EnableDisable(bool Flag)
	{
		((Control)ClipboardButton).Enabled = Flag;
		((Control)Close2CloseButton).Enabled = Flag;
		((Control)DoneButton).Enabled = Flag;
		((Control)DataGridView1).Enabled = Flag;
		((Control)HelpButton1).Enabled = Flag;
		((Control)Low2HighButton).Enabled = Flag;
		((Control)PriceBars).Enabled = Flag;
		((Control)StartButton).Enabled = Flag;
		((Control)StopButton).Enabled = !Flag;
		((Control)TargetGain).Enabled = Flag;
		if (UseDatesCheckBox.Checked)
		{
			((Control)FromDatePicker).Enabled = Flag;
			((Control)ToDatePicker).Enabled = Flag;
		}
		((Control)UseDatesCheckBox).Enabled = Flag;
	}

	private void ColorOutliers()
	{
		List<int> list = new List<int>();
		Array.Clear(Outliers, 0, Outliers.Length);
		checked
		{
			int num = DataGridView1.RowCount - 1;
			for (int i = 0; i <= num; i++)
			{
				int num2 = 1;
				do
				{
					list.Add(Conversions.ToInteger(DataGridView1.Rows[i].Cells[num2].Value));
					num2++;
				}
				while (num2 <= 12);
				list.Sort();
				float num3 = (float)((double)(list[2] + list[3]) / 2.0);
				float num4 = (float)((double)(list[8] + list[9]) / 2.0);
				float num5 = num4 - num3;
				float num6 = num4 + (float)(int)Math.Round(1.5 * (double)num5);
				float num7 = num3 - (float)(int)Math.Round(1.5 * (double)num5);
				num2 = 1;
				do
				{
					if ((float)Conversions.ToInteger(DataGridView1.Rows[i].Cells[num2].Value) < num7)
					{
						DataGridView1.Rows[i].Cells[num2].Style.BackColor = Color.LightPink;
					}
					if ((float)Conversions.ToInteger(DataGridView1.Rows[i].Cells[num2].Value) > num6)
					{
						DataGridView1.Rows[i].Cells[num2].Style.BackColor = Color.LightGreen;
						Outliers[num2 - 1]++;
					}
					num2++;
				}
				while (num2 <= 12);
				list.Clear();
			}
		}
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.HelpBestTrade).ShowDialog();
	}

	private void SetupGridHeader()
	{
		DataGridView1.RowCount = 0;
		DataGridView1.ColumnCount = 13;
		DataGridView1.Columns[0].HeaderText = "Symbol";
		int num = 1;
		checked
		{
			do
			{
				DataGridView1.Columns[0 + num].HeaderText = DateAndTime.MonthName(num, true);
				num++;
			}
			while (num <= 12);
		}
	}

	private void StartButton_Click(object sender, EventArgs e)
	{
		//IL_08ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_0147: Unknown result type (might be due to invalid IL or missing references)
		//IL_014d: Invalid comparison between Unknown and I4
		EnableDisable(Flag: false);
		SetupGridHeader();
		if (UseDatesCheckBox.Checked)
		{
			DateTimePicker fromDatePicker = FromDatePicker;
			DateTime FromDate = fromDatePicker.Value;
			DateTimePicker toDatePicker;
			DateTime ToDate = (toDatePicker = ToDatePicker).Value;
			GlobalForm.SwapDates(ref FromDate, ref ToDate);
			toDatePicker.Value = ToDate;
			fromDatePicker.Value = FromDate;
		}
		StopPressed = false;
		LoadingBar.Value = 1;
		int count = MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count;
		int num = -1;
		bool flag = false;
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
				bool flag2;
				if (count == 1)
				{
					ProgressBar ProgBar = LoadingBar;
					Label ErrorLabel = null;
					bool num3 = GlobalForm.LoadFile(text, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
					LoadingBar = ProgBar;
					flag2 = num3;
				}
				else
				{
					ProgressBar ProgBar = null;
					Label ErrorLabel = null;
					flag2 = GlobalForm.LoadFile(text, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
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
				if (!flag2)
				{
					Array.Clear(MonthTotals, 0, MonthTotals.Length);
					if (count == 1)
					{
						DataGridView1.Rows.Add();
						num++;
						if (!UseDatesCheckBox.Checked)
						{
							DataGridView1.Rows[num].Cells[0].Value = DateAndTime.Year(GlobalForm.nDT[0, 0]);
						}
						int hLCRange = GlobalForm.HLCRange;
						for (int j = 0; j <= hLCRange; j++)
						{
							if (!UseDatesCheckBox.Checked | (UseDatesCheckBox.Checked & (DateTime.Compare(GlobalForm.nDT[0, j], FromDatePicker.Value) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, j], ToDatePicker.Value) <= 0)))
							{
								if (unchecked(UseDatesCheckBox.Checked && !flag))
								{
									flag = true;
									DataGridView1.Rows[num].Cells[0].Value = DateAndTime.Year(GlobalForm.nDT[0, j]);
								}
								int num4 = Convert.ToInt32(PriceBars.Value) - 1;
								for (int k = 1; k <= num4; k++)
								{
									if (j + k <= GlobalForm.HLCRange && decimal.Compare(GlobalForm.nHLC[3, j], 0m) != 0)
									{
										decimal d = ((!Close2CloseButton.Checked) ? decimal.Divide(decimal.Multiply(100m, decimal.Subtract(GlobalForm.nHLC[1, j + k], GlobalForm.nHLC[2, j])), GlobalForm.nHLC[2, j]) : decimal.Divide(decimal.Multiply(100m, decimal.Subtract(GlobalForm.nHLC[3, j + k], GlobalForm.nHLC[3, j])), GlobalForm.nHLC[3, j]));
										if (decimal.Compare(d, TargetGain.Value) >= 0)
										{
											MonthTotals[DateAndTime.Month(GlobalForm.nDT[0, j]) - 1]++;
											break;
										}
									}
								}
								if (j == GlobalForm.HLCRange)
								{
									int num5 = 1;
									do
									{
										DataGridView1.Rows[num].Cells[0 + num5].Value = MonthTotals[num5 - 1];
										num5++;
									}
									while (num5 <= 12);
								}
								if (((j > 0) & (j + 1 <= GlobalForm.HLCRange)) && DateAndTime.Year(GlobalForm.nDT[0, j]) != DateAndTime.Year(GlobalForm.nDT[0, j + 1]))
								{
									int num6 = 1;
									do
									{
										DataGridView1.Rows[num].Cells[0 + num6].Value = MonthTotals[num6 - 1];
										num6++;
									}
									while (num6 <= 12);
									if (j != GlobalForm.HLCRange)
									{
										DataGridView1.Rows.Add();
										num++;
										DataGridView1.Rows[num].Cells[0].Value = DateAndTime.Year(GlobalForm.nDT[0, j + 1]);
									}
									Array.Clear(MonthTotals, 0, MonthTotals.Length);
								}
							}
							else if (UseDatesCheckBox.Checked & (DateTime.Compare(GlobalForm.nDT[0, j], ToDatePicker.Value) > 0))
							{
								int num7 = 1;
								do
								{
									DataGridView1.Rows[num].Cells[0 + num7].Value = MonthTotals[num7 - 1];
									num7++;
								}
								while (num7 <= 12);
								break;
							}
						}
					}
					else
					{
						DataGridView1.Rows.Add();
						num++;
						DataGridView1.Rows[num].Cells[0].Value = text;
						int hLCRange2 = GlobalForm.HLCRange;
						for (int l = 0; l <= hLCRange2; l++)
						{
							if (!(!UseDatesCheckBox.Checked | (UseDatesCheckBox.Checked & (DateTime.Compare(GlobalForm.nDT[0, l], FromDatePicker.Value) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, l], ToDatePicker.Value) <= 0))))
							{
								continue;
							}
							int num8 = Convert.ToInt32(PriceBars.Value) - 1;
							for (int m = 1; m <= num8; m++)
							{
								if (l + m <= GlobalForm.HLCRange && decimal.Compare(GlobalForm.nHLC[3, l], 0m) != 0)
								{
									decimal d = ((!Close2CloseButton.Checked) ? decimal.Divide(decimal.Multiply(100m, decimal.Subtract(GlobalForm.nHLC[1, l + m], GlobalForm.nHLC[2, l])), GlobalForm.nHLC[2, l]) : decimal.Divide(decimal.Multiply(100m, decimal.Subtract(GlobalForm.nHLC[3, l + m], GlobalForm.nHLC[3, l])), GlobalForm.nHLC[3, l]));
									if (decimal.Compare(d, TargetGain.Value) >= 0)
									{
										MonthTotals[DateAndTime.Month(GlobalForm.nDT[0, l]) - 1]++;
										break;
									}
								}
							}
						}
						int num9 = 1;
						do
						{
							DataGridView1.Rows[num].Cells[0 + num9].Value = MonthTotals[num9 - 1];
							num9++;
						}
						while (num9 <= 12);
					}
				}
				if (count > 1)
				{
					LoadingBar.Value = (int)Math.Round((double)(100 * i) / (double)MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count);
				}
			}
			ColorOutliers();
			DataGridView1.Rows.Add();
			num++;
			int num10 = 1;
			do
			{
				DataGridView1.Rows[num].Cells[0 + num10].Value = Outliers[num10 - 1];
				num10++;
			}
			while (num10 <= 12);
			DataGridView1.Rows[num].Cells[0].Value = "Outlier Totals";
			EnableDisable(Flag: true);
			LoadingBar.Value = 100;
			FileNameLabel.Text = "Done!";
			MessageBox.Show("Done! Outliers: Green shaded cells show unusually high numbers of matches, red shaded cells show unusually few numbers of matches.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			LoadingBar.Value = 0;
			if (count == 1)
			{
				FileNameLabel.Text = MyProject.Forms.Mainform.ListBox1.SelectedItems[0].ToString();
			}
		}
	}

	private void StopButton_Click(object sender, EventArgs e)
	{
		StopPressed = true;
	}

	private void UseDatesCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		((Control)FromDatePicker).Enabled = UseDatesCheckBox.Checked;
		((Control)ToDatePicker).Enabled = UseDatesCheckBox.Checked;
	}
}
