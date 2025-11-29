using System;
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
public class RelStrengthForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("HelpButton1")]
	private Button _HelpButton1;

	[CompilerGenerated]
	[AccessedThroughProperty("SelectAllButton")]
	private Button _SelectAllButton;

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
	[AccessedThroughProperty("ClipboardButton")]
	private Button _ClipboardButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ScanAllPortfoliosButton")]
	private Button _ScanAllPortfoliosButton;

	[CompilerGenerated]
	[AccessedThroughProperty("BrowseButton")]
	private Button _BrowseButton;

	private bool StopPressed;

	private int RRSIZE;

	private object[,] Results;

	private const int rSYMBOL = 0;

	private const int rLASTCLOSE = 1;

	private const int rDAYCHG = 2;

	private const int rPRIORDAY = 3;

	private const int rWEEKCHG = 4;

	private const int rPRIORWEEK = 5;

	private const int rMONTHCHG = 6;

	private const int rPRIORMONTH = 7;

	private const int r3MOSCHG = 8;

	private const int rPRIOR3MOS = 9;

	private const int r6MOSCHG = 10;

	private const int rPRIOR6MOS = 11;

	private bool[] bFound;

	private DateTime[] TargetDates;

	private const int tDAYCHG = 0;

	private const int tPRIORDAY = 1;

	private const int tPRIORPRIORDAY = 2;

	private const int tWEEKCHG = 3;

	private const int tPRIORWEEK = 4;

	private const int tPRIORPRIORWEEK = 5;

	private const int tMONTHCHG = 6;

	private const int tPRIORMONTH = 7;

	private const int tPRIORPRIORMONTH = 8;

	private const int t3MOSCHG = 9;

	private const int tPRIOR3MOS = 10;

	private const int tPRIORPRIOR3MOS = 11;

	private const int t6MOSCHG = 12;

	private const int tPRIOR6MOS = 13;

	private const int tPRIORPRIOR6MOS = 14;

	private const int dSYMBOL = 0;

	private const int dTOTAL = 1;

	private const int dLASTCLOSE = 2;

	private const int dDAYCHG = 3;

	private const int dPRIORDAY = 4;

	private const int dWEEKCHG = 5;

	private const int dPRIORWEEK = 6;

	private const int dMONTHCHG = 7;

	private const int dPRIORMONTH = 8;

	private const int d3MOSCHG = 9;

	private const int dPRIOR3MOS = 10;

	private const int d6MOSCHG = 11;

	private const int dPRIOR6MOS = 12;

	private const int dCOLUMNCOUNT = 13;

	private int iRow;

	[field: AccessedThroughProperty("ListBox1")]
	internal virtual ListBox ListBox1
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

	internal virtual Button SelectAllButton
	{
		[CompilerGenerated]
		get
		{
			return _SelectAllButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SelectAllButton_Click;
			Button val = _SelectAllButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_SelectAllButton = value;
			val = _SelectAllButton;
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

	[field: AccessedThroughProperty("DataGridView1")]
	internal virtual DataGridView DataGridView1
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

	[field: AccessedThroughProperty("ProgressBar1")]
	internal virtual ProgressBar ProgressBar1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("MessagesLabel")]
	internal virtual Label MessagesLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("EndDatePicker")]
	internal virtual DateTimePicker EndDatePicker
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

	internal virtual Button ScanAllPortfoliosButton
	{
		[CompilerGenerated]
		get
		{
			return _ScanAllPortfoliosButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ScanAllPortfoliosButton_Click;
			Button val = _ScanAllPortfoliosButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ScanAllPortfoliosButton = value;
			val = _ScanAllPortfoliosButton;
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

	[field: AccessedThroughProperty("FolderBrowserDialog1")]
	internal virtual FolderBrowserDialog FolderBrowserDialog1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public RelStrengthForm()
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		((Form)this).FormClosing += new FormClosingEventHandler(RelStrengthForm_FormClosing);
		((Form)this).Load += RelStrengthForm_Load;
		StopPressed = false;
		RRSIZE = 11;
		Results = new object[checked(RRSIZE + 1), 1];
		bFound = new bool[16];
		TargetDates = new DateTime[16];
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
		ListBox1 = new ListBox();
		HelpButton1 = new Button();
		SelectAllButton = new Button();
		StartButton = new Button();
		StopButton = new Button();
		DoneButton = new Button();
		DataGridView1 = new DataGridView();
		ClipboardButton = new Button();
		ProgressBar1 = new ProgressBar();
		MessagesLabel = new Label();
		EndDatePicker = new DateTimePicker();
		Label2 = new Label();
		ScanAllPortfoliosButton = new Button();
		BrowseButton = new Button();
		FolderBrowserDialog1 = new FolderBrowserDialog();
		((ISupportInitialize)DataGridView1).BeginInit();
		((Control)this).SuspendLayout();
		((Control)ListBox1).Anchor = (AnchorStyles)13;
		ListBox1.HorizontalScrollbar = true;
		((Control)ListBox1).Location = new Point(12, 12);
		ListBox1.MultiColumn = true;
		((Control)ListBox1).Name = "ListBox1";
		ListBox1.SelectionMode = (SelectionMode)3;
		((Control)ListBox1).Size = new Size(992, 225);
		ListBox1.Sorted = true;
		((Control)ListBox1).TabIndex = 2;
		((Control)HelpButton1).Anchor = (AnchorStyles)10;
		((Control)HelpButton1).Location = new Point(946, 694);
		((Control)HelpButton1).Name = "HelpButton1";
		((Control)HelpButton1).Size = new Size(60, 23);
		((Control)HelpButton1).TabIndex = 11;
		((ButtonBase)HelpButton1).Text = "&Help";
		((ButtonBase)HelpButton1).UseVisualStyleBackColor = true;
		((Control)SelectAllButton).Anchor = (AnchorStyles)10;
		((Control)SelectAllButton).Location = new Point(814, 718);
		((Control)SelectAllButton).Name = "SelectAllButton";
		((Control)SelectAllButton).Size = new Size(60, 23);
		((Control)SelectAllButton).TabIndex = 13;
		((ButtonBase)SelectAllButton).Text = "&Select All";
		((ButtonBase)SelectAllButton).UseVisualStyleBackColor = true;
		((Control)StartButton).Anchor = (AnchorStyles)10;
		((Control)StartButton).Location = new Point(880, 718);
		((Control)StartButton).Name = "StartButton";
		((Control)StartButton).Size = new Size(60, 23);
		((Control)StartButton).TabIndex = 0;
		((ButtonBase)StartButton).Text = "St&art";
		((ButtonBase)StartButton).UseVisualStyleBackColor = true;
		((Control)StopButton).Anchor = (AnchorStyles)10;
		((Control)StopButton).Enabled = false;
		((Control)StopButton).Location = new Point(880, 694);
		((Control)StopButton).Name = "StopButton";
		((Control)StopButton).Size = new Size(60, 23);
		((Control)StopButton).TabIndex = 10;
		((ButtonBase)StopButton).Text = "St&op";
		((ButtonBase)StopButton).UseVisualStyleBackColor = true;
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(946, 719);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(60, 23);
		((Control)DoneButton).TabIndex = 1;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		DataGridView1.AllowUserToAddRows = false;
		DataGridView1.AllowUserToDeleteRows = false;
		DataGridView1.AllowUserToResizeColumns = false;
		DataGridView1.AllowUserToResizeRows = false;
		((Control)DataGridView1).Anchor = (AnchorStyles)15;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)10;
		((Control)DataGridView1).CausesValidation = false;
		DataGridView1.ColumnHeadersHeightSizeMode = (DataGridViewColumnHeadersHeightSizeMode)2;
		DataGridView1.EditMode = (DataGridViewEditMode)4;
		((Control)DataGridView1).Location = new Point(12, 243);
		((Control)DataGridView1).Name = "DataGridView1";
		DataGridView1.ReadOnly = true;
		DataGridView1.RowTemplate.ReadOnly = true;
		DataGridView1.RowTemplate.Resizable = (DataGridViewTriState)1;
		DataGridView1.SelectionMode = (DataGridViewSelectionMode)1;
		DataGridView1.ShowCellErrors = false;
		DataGridView1.ShowCellToolTips = false;
		DataGridView1.ShowEditingIcon = false;
		DataGridView1.ShowRowErrors = false;
		((Control)DataGridView1).Size = new Size(992, 445);
		((Control)DataGridView1).TabIndex = 3;
		((Control)ClipboardButton).Anchor = (AnchorStyles)10;
		((Control)ClipboardButton).Enabled = false;
		((Control)ClipboardButton).Location = new Point(748, 694);
		((Control)ClipboardButton).Name = "ClipboardButton";
		((Control)ClipboardButton).Size = new Size(60, 23);
		((Control)ClipboardButton).TabIndex = 8;
		((ButtonBase)ClipboardButton).Text = "Clip&board";
		((ButtonBase)ClipboardButton).UseVisualStyleBackColor = true;
		((Control)ProgressBar1).Anchor = (AnchorStyles)14;
		((Control)ProgressBar1).ForeColor = Color.Green;
		((Control)ProgressBar1).Location = new Point(12, 694);
		((Control)ProgressBar1).Name = "ProgressBar1";
		((Control)ProgressBar1).Size = new Size(540, 23);
		((Control)ProgressBar1).TabIndex = 4;
		((Control)MessagesLabel).Anchor = (AnchorStyles)14;
		MessagesLabel.BorderStyle = (BorderStyle)2;
		((Control)MessagesLabel).Location = new Point(12, 717);
		((Control)MessagesLabel).Name = "MessagesLabel";
		((Control)MessagesLabel).Size = new Size(540, 21);
		((Control)MessagesLabel).TabIndex = 5;
		MessagesLabel.TextAlign = (ContentAlignment)32;
		((Control)EndDatePicker).Anchor = (AnchorStyles)10;
		EndDatePicker.CustomFormat = "yyyy/MM/dd";
		EndDatePicker.Format = (DateTimePickerFormat)8;
		((Control)EndDatePicker).Location = new Point(614, 719);
		((Control)EndDatePicker).Name = "EndDatePicker";
		EndDatePicker.ShowUpDown = true;
		((Control)EndDatePicker).Size = new Size(88, 20);
		((Control)EndDatePicker).TabIndex = 7;
		EndDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(558, 721);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(50, 13);
		((Control)Label2).TabIndex = 6;
		Label2.Text = "&End date";
		((Control)ScanAllPortfoliosButton).Anchor = (AnchorStyles)10;
		((Control)ScanAllPortfoliosButton).Location = new Point(707, 718);
		((Control)ScanAllPortfoliosButton).Name = "ScanAllPortfoliosButton";
		((Control)ScanAllPortfoliosButton).Size = new Size(101, 23);
		((Control)ScanAllPortfoliosButton).TabIndex = 12;
		((ButtonBase)ScanAllPortfoliosButton).Text = "&Scan All Portfolios";
		((ButtonBase)ScanAllPortfoliosButton).UseVisualStyleBackColor = true;
		((Control)BrowseButton).Anchor = (AnchorStyles)10;
		((Control)BrowseButton).Location = new Point(814, 694);
		((Control)BrowseButton).Name = "BrowseButton";
		((Control)BrowseButton).Size = new Size(60, 23);
		((Control)BrowseButton).TabIndex = 9;
		((ButtonBase)BrowseButton).Text = "&Browse";
		((ButtonBase)BrowseButton).UseVisualStyleBackColor = true;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(1016, 741);
		((Control)this).Controls.Add((Control)(object)BrowseButton);
		((Control)this).Controls.Add((Control)(object)ScanAllPortfoliosButton);
		((Control)this).Controls.Add((Control)(object)EndDatePicker);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)MessagesLabel);
		((Control)this).Controls.Add((Control)(object)ProgressBar1);
		((Control)this).Controls.Add((Control)(object)ClipboardButton);
		((Control)this).Controls.Add((Control)(object)DataGridView1);
		((Control)this).Controls.Add((Control)(object)HelpButton1);
		((Control)this).Controls.Add((Control)(object)SelectAllButton);
		((Control)this).Controls.Add((Control)(object)StartButton);
		((Control)this).Controls.Add((Control)(object)StopButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)ListBox1);
		((Control)this).Name = "RelStrengthForm";
		((Form)this).StartPosition = (FormStartPosition)1;
		((Form)this).Text = "Relative Strength Form";
		((ISupportInitialize)DataGridView1).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void RelStrengthForm_FormClosing(object sender, FormClosingEventArgs e)
	{
		//IL_001a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0020: Invalid comparison between Unknown and I4
		if (((Control)StopButton).Enabled)
		{
			if ((int)MessageBox.Show("Did you want to stop the process and exit the form?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32) != 6)
			{
				((CancelEventArgs)(object)e).Cancel = true;
				return;
			}
			StopPressed = true;
			((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
		}
		MySettingsProperty.Settings.RelStrengthLocation = ((Form)this).Location;
		MySettingsProperty.Settings.RelStrengthSize = ((Form)this).Size;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
	}

	private void RelStrengthForm_Load(object sender, EventArgs e)
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
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.RelStrengthLocation, MySettingsProperty.Settings.RelStrengthSize);
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)BrowseButton, "Find another location of quote files.");
		val.SetToolTip((Control)(object)ClipboardButton, "After completing scan, copy results to clipboard.");
		val.SetToolTip((Control)(object)DataGridView1, "Results appear here.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)EndDatePicker, "End scanning on this date.");
		val.SetToolTip((Control)(object)HelpButton1, "Get help.");
		val.SetToolTip((Control)(object)ListBox1, "Quote files appear here, if any.");
		val.SetToolTip((Control)(object)ScanAllPortfoliosButton, "Analyze each stock in all portfolios.");
		val.SetToolTip((Control)(object)SelectAllButton, "Select all of the symbols listed.");
		val.SetToolTip((Control)(object)StartButton, "Begin compiling relative strength results.");
		val.SetToolTip((Control)(object)StopButton, "Halt the process.");
		EndDatePicker.Value = DateAndTime.Now;
		StopPressed = false;
		ProgressBar1.Value = 0;
		ListBox ListBox = ListBox1;
		GlobalForm.DisplayFiles(ref ListBox);
		ListBox1 = ListBox;
		SelectAllButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		BuildGridHeader();
		if (GlobalForm.IntradayData)
		{
			MessagesLabel.Text = "This form is meant for daily data, not intraday.";
		}
	}

	private void BrowseButton_Click(object sender, EventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_000b: Expected O, but got Unknown
		//IL_0021: Unknown result type (might be due to invalid IL or missing references)
		//IL_0027: Invalid comparison between Unknown and I4
		FolderBrowserDialog1 = new FolderBrowserDialog();
		FolderBrowserDialog1.Description = "Select the path to the stock quote files.";
		if ((int)((CommonDialog)FolderBrowserDialog1).ShowDialog() == 1)
		{
			GlobalForm.PathChanged = true;
			GlobalForm.OpenPath = FolderBrowserDialog1.SelectedPath;
			ListBox ListBox = ListBox1;
			GlobalForm.DisplayFiles(ref ListBox);
			ListBox1 = ListBox;
			SelectAllButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		}
	}

	private void BuildGridHeader()
	{
		DataGridView1.RowCount = 0;
		DataGridView1.ColumnCount = 13;
		DataGridView1.Columns[0].Name = "Stock";
		DataGridView1.Columns[1].Name = "# Green";
		DataGridView1.Columns[2].Name = "Last Close";
		DataGridView1.Columns[3].Name = "Day Chg";
		DataGridView1.Columns[4].Name = "Prior Day";
		DataGridView1.Columns[5].Name = "Wk Change";
		DataGridView1.Columns[6].Name = "Prior Wk";
		DataGridView1.Columns[7].Name = "Month Chg";
		DataGridView1.Columns[8].Name = "Prior Mo.";
		DataGridView1.Columns[9].Name = "3 Mos. Chg";
		DataGridView1.Columns[10].Name = "Prior 3 Mos.";
		DataGridView1.Columns[11].Name = "6 Mos. Chg";
		DataGridView1.Columns[12].Name = "Prior 6 Mos.";
	}

	private void ClipboardButton_Click(object sender, EventArgs e)
	{
		//IL_0153: Unknown result type (might be due to invalid IL or missing references)
		//IL_016d: Unknown result type (might be due to invalid IL or missing references)
		//IL_012a: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b4: Unknown result type (might be due to invalid IL or missing references)
		//IL_00bb: Expected O, but got Unknown
		bool flag = false;
		checked
		{
			if (((BaseCollection)DataGridView1.SelectedRows).Count > 0)
			{
				string text = "The Relative Strength Form shows the performance of selected stocks over various periods. Performance over 6 months ('6 Mos. Chg', far right column) is more significant than shorter periods. ";
				text += "\r\nDefinitions: Chg is change, Wk is week, Mo. is month, Mos. is months.";
				text += "\r\nThe form shows the close to close difference over the various periods, expressed as a percentage gain or loss.";
				text += "\r\nCopyright (c) 2016-2024 by Thomas Bulkowski and ThePatternSite.com. All rights reserved.";
				text += "\r\n\r\n";
				int num = ((BaseCollection)DataGridView1.SelectedRows).Count - 1;
				for (int i = 0; i <= num; i++)
				{
					if (((DataGridViewBand)DataGridView1.SelectedRows[i]).Index == 1)
					{
						flag = true;
						break;
					}
				}
				if (!flag)
				{
					text += "\t";
					foreach (DataGridViewColumn item in (BaseCollection)DataGridView1.Columns)
					{
						DataGridViewColumn val = item;
						text = text + val.Name + "\t";
					}
				}
				text += "\r\n";
				try
				{
					Clipboard.SetDataObject((object)DataGridView1.GetClipboardContent());
					text += Clipboard.GetText();
					Clipboard.SetText(text);
					MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
					return;
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					MessageBox.Show("Clipboard is busy with another user. Error: " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
					ProjectData.ClearProjectError();
					return;
				}
			}
			MessageBox.Show("Please select some grid rows.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
		}
	}

	private void CrunchNumbers(int Index)
	{
		decimal d = default(decimal);
		decimal d2 = default(decimal);
		bFound = null;
		bFound = new bool[16];
		Results[1, Index] = GlobalForm.nHLC[3, GlobalForm.HLCRange];
		for (int i = GlobalForm.HLCRange; i >= 0; i = checked(i + -1))
		{
			if (!bFound[0] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[0].Date) <= 0))
			{
				bFound[0] = true;
				d = GlobalForm.nHLC[3, i];
			}
			if (!bFound[1] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[1].Date) <= 0))
			{
				bFound[1] = true;
				if ((decimal.Compare(d, 0m) != 0) & (decimal.Compare(GlobalForm.nHLC[3, i], 0m) != 0))
				{
					Results[2, Index] = decimal.Divide(decimal.Subtract(d, GlobalForm.nHLC[3, i]), GlobalForm.nHLC[3, i]);
				}
				d2 = GlobalForm.nHLC[3, i];
				d = default(decimal);
			}
			if (!bFound[2] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[2].Date) <= 0))
			{
				bFound[2] = true;
				if ((decimal.Compare(d2, 0m) != 0) & (decimal.Compare(GlobalForm.nHLC[3, i], 0m) != 0))
				{
					Results[3, Index] = decimal.Divide(decimal.Subtract(d2, GlobalForm.nHLC[3, i]), GlobalForm.nHLC[3, i]);
				}
				d2 = default(decimal);
			}
			if (!bFound[3] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[3].Date) <= 0))
			{
				bFound[3] = true;
				d = GlobalForm.nHLC[3, i];
			}
			if (!bFound[4] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[4].Date) <= 0))
			{
				bFound[4] = true;
				if ((decimal.Compare(d, 0m) != 0) & (decimal.Compare(GlobalForm.nHLC[3, i], 0m) != 0))
				{
					Results[4, Index] = decimal.Divide(decimal.Subtract(d, GlobalForm.nHLC[3, i]), GlobalForm.nHLC[3, i]);
				}
				d2 = GlobalForm.nHLC[3, i];
				d = default(decimal);
			}
			if (!bFound[5] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[5].Date) <= 0))
			{
				bFound[5] = true;
				if ((decimal.Compare(d2, 0m) != 0) & (decimal.Compare(GlobalForm.nHLC[3, i], 0m) != 0))
				{
					Results[5, Index] = decimal.Divide(decimal.Subtract(d2, GlobalForm.nHLC[3, i]), GlobalForm.nHLC[3, i]);
				}
				d2 = default(decimal);
			}
			if (!bFound[6] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[6].Date) <= 0))
			{
				bFound[6] = true;
				d = GlobalForm.nHLC[3, i];
			}
			if (!bFound[7] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[7].Date) <= 0))
			{
				bFound[7] = true;
				if ((decimal.Compare(d, 0m) != 0) & (decimal.Compare(GlobalForm.nHLC[3, i], 0m) != 0))
				{
					Results[6, Index] = decimal.Divide(decimal.Subtract(d, GlobalForm.nHLC[3, i]), GlobalForm.nHLC[3, i]);
				}
				d2 = GlobalForm.nHLC[3, i];
				d = default(decimal);
			}
			if (!bFound[8] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[8].Date) <= 0))
			{
				bFound[8] = true;
				if ((decimal.Compare(d2, 0m) != 0) & (decimal.Compare(GlobalForm.nHLC[3, i], 0m) != 0))
				{
					Results[7, Index] = decimal.Divide(decimal.Subtract(d2, GlobalForm.nHLC[3, i]), GlobalForm.nHLC[3, i]);
				}
				d2 = default(decimal);
			}
			if (!bFound[9] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[9].Date) <= 0))
			{
				bFound[9] = true;
				d = GlobalForm.nHLC[3, i];
			}
			if (!bFound[10] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[10].Date) <= 0))
			{
				bFound[10] = true;
				if ((decimal.Compare(d, 0m) != 0) & (decimal.Compare(GlobalForm.nHLC[3, i], 0m) != 0))
				{
					Results[8, Index] = decimal.Divide(decimal.Subtract(d, GlobalForm.nHLC[3, i]), GlobalForm.nHLC[3, i]);
				}
				d2 = GlobalForm.nHLC[3, i];
				d = default(decimal);
			}
			if (!bFound[11] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[11].Date) <= 0))
			{
				bFound[11] = true;
				if ((decimal.Compare(d2, 0m) != 0) & (decimal.Compare(GlobalForm.nHLC[3, i], 0m) != 0))
				{
					Results[9, Index] = decimal.Divide(decimal.Subtract(d2, GlobalForm.nHLC[3, i]), GlobalForm.nHLC[3, i]);
				}
				d2 = default(decimal);
			}
			if (!bFound[12] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[12].Date) <= 0))
			{
				bFound[12] = true;
				d = GlobalForm.nHLC[3, i];
			}
			if (!bFound[13] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[13].Date) <= 0))
			{
				bFound[13] = true;
				if ((decimal.Compare(d, 0m) != 0) & (decimal.Compare(GlobalForm.nHLC[3, i], 0m) != 0))
				{
					Results[10, Index] = decimal.Divide(decimal.Subtract(d, GlobalForm.nHLC[3, i]), GlobalForm.nHLC[3, i]);
				}
				d2 = GlobalForm.nHLC[3, i];
				d = default(decimal);
			}
			if (!bFound[14] & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TargetDates[14].Date) <= 0))
			{
				bFound[14] = true;
				if ((decimal.Compare(d2, 0m) != 0) & (decimal.Compare(GlobalForm.nHLC[3, i], 0m) != 0))
				{
					Results[11, Index] = decimal.Divide(decimal.Subtract(d2, GlobalForm.nHLC[3, i]), GlobalForm.nHLC[3, i]);
				}
				break;
			}
		}
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void GridDisplay(int Count)
	{
		DataGridView1.RowHeadersVisible = false;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)1;
		int decimalsUsed = GlobalForm.DecimalsUsed;
		GlobalForm.DecimalsUsed = 1;
		checked
		{
			int num = Count - 1;
			for (int i = 0; i <= num; i++)
			{
				if (Results[0, i] == null)
				{
					continue;
				}
				int num2 = 0;
				DataGridView1.Rows.Add();
				DataGridView1.Rows[i].Cells[0].Value = RuntimeHelpers.GetObjectValue(Results[0, i]);
				GlobalForm.DecimalsUsed = decimalsUsed;
				DataGridView1.Rows[i].Cells[2].Value = GlobalForm.LimitDecimals(Conversions.ToDecimal(Results[1, i]));
				GlobalForm.DecimalsUsed = 1;
				if ((Results[3, i] != null) & (Results[2, i] != null))
				{
					if (decimal.Compare(Conversions.ToDecimal(Results[3, i]), Conversions.ToDecimal(Results[2, i])) < 0)
					{
						num2++;
					}
					DataGridViewCellStyle style = DataGridView1.Rows[i].Cells[3].Style;
					object obj = Interaction.IIf(decimal.Compare(Conversions.ToDecimal(Results[3, i]), Conversions.ToDecimal(Results[2, i])) < 0, (object)Color.LightGreen, (object)Color.LightPink);
					style.BackColor = ((obj != null) ? ((Color)obj) : default(Color));
				}
				if (Results[3, i] != null)
				{
					DataGridView1.Rows[i].Cells[4].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, Conversions.ToDecimal(Results[3, i])));
				}
				if (Results[2, i] != null)
				{
					DataGridView1.Rows[i].Cells[3].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, Conversions.ToDecimal(Results[2, i])));
				}
				if ((Results[5, i] != null) & (Results[4, i] != null))
				{
					if (decimal.Compare(Conversions.ToDecimal(Results[5, i]), Conversions.ToDecimal(Results[4, i])) < 0)
					{
						num2++;
					}
					DataGridViewCellStyle style2 = DataGridView1.Rows[i].Cells[5].Style;
					object obj2 = Interaction.IIf(decimal.Compare(Conversions.ToDecimal(Results[5, i]), Conversions.ToDecimal(Results[4, i])) < 0, (object)Color.LightGreen, (object)Color.LightPink);
					style2.BackColor = ((obj2 != null) ? ((Color)obj2) : default(Color));
				}
				if (Results[5, i] != null)
				{
					DataGridView1.Rows[i].Cells[6].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, Conversions.ToDecimal(Results[5, i])));
				}
				if (Results[4, i] != null)
				{
					DataGridView1.Rows[i].Cells[5].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, Conversions.ToDecimal(Results[4, i])));
				}
				if ((Results[7, i] != null) & (Results[6, i] != null))
				{
					if (decimal.Compare(Conversions.ToDecimal(Results[7, i]), Conversions.ToDecimal(Results[6, i])) < 0)
					{
						num2++;
					}
					DataGridViewCellStyle style3 = DataGridView1.Rows[i].Cells[7].Style;
					object obj3 = Interaction.IIf(decimal.Compare(Conversions.ToDecimal(Results[7, i]), Conversions.ToDecimal(Results[6, i])) < 0, (object)Color.LightGreen, (object)Color.LightPink);
					style3.BackColor = ((obj3 != null) ? ((Color)obj3) : default(Color));
				}
				if (Results[7, i] != null)
				{
					DataGridView1.Rows[i].Cells[8].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, Conversions.ToDecimal(Results[7, i])));
				}
				if (Results[6, i] != null)
				{
					DataGridView1.Rows[i].Cells[7].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, Conversions.ToDecimal(Results[6, i])));
				}
				if ((Results[9, i] != null) & (Results[8, i] != null))
				{
					if (decimal.Compare(Conversions.ToDecimal(Results[9, i]), Conversions.ToDecimal(Results[8, i])) < 0)
					{
						num2++;
					}
					DataGridViewCellStyle style4 = DataGridView1.Rows[i].Cells[9].Style;
					object obj4 = Interaction.IIf(decimal.Compare(Conversions.ToDecimal(Results[9, i]), Conversions.ToDecimal(Results[8, i])) < 0, (object)Color.LightGreen, (object)Color.LightPink);
					style4.BackColor = ((obj4 != null) ? ((Color)obj4) : default(Color));
				}
				if (Results[9, i] != null)
				{
					DataGridView1.Rows[i].Cells[10].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, Conversions.ToDecimal(Results[9, i])));
				}
				if (Results[8, i] != null)
				{
					DataGridView1.Rows[i].Cells[9].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, Conversions.ToDecimal(Results[8, i])));
				}
				if ((Results[11, i] != null) & (Results[10, i] != null))
				{
					if (decimal.Compare(Conversions.ToDecimal(Results[11, i]), Conversions.ToDecimal(Results[10, i])) < 0)
					{
						num2++;
					}
					DataGridViewCellStyle style5 = DataGridView1.Rows[i].Cells[11].Style;
					object obj5 = Interaction.IIf(decimal.Compare(Conversions.ToDecimal(Results[11, i]), Conversions.ToDecimal(Results[10, i])) < 0, (object)Color.LightGreen, (object)Color.LightPink);
					style5.BackColor = ((obj5 != null) ? ((Color)obj5) : default(Color));
				}
				if (Results[11, i] != null)
				{
					DataGridView1.Rows[i].Cells[12].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, Conversions.ToDecimal(Results[11, i])));
				}
				if (Results[10, i] != null)
				{
					DataGridView1.Rows[i].Cells[11].Value = GlobalForm.LimitDecimals(decimal.Multiply(100m, Conversions.ToDecimal(Results[10, i])));
				}
				DataGridView1.Rows[i].Cells[1].Value = num2;
			}
			DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)6;
			DataGridView1.RowHeadersVisible = true;
			GlobalForm.DecimalsUsed = decimalsUsed;
		}
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("For momentum traders, the Relative Strength Form shows the performance of selected stocks over various periods. Performance over 6 months ('6 Mos. Chg', far right column) is more significant than the 3 month period. The 3 month period is more significant than the 1 month period, and so on.\r\n\r\nTo begin, highlight stocks in the top list box, adjust the end date (performance is measured ending on this date, excluding weekends and holidays), and click 'Start.'\r\n\r\nGreen cells mean improved performance (increasing momentum) over the prior period. Red cells mean worse performance (momentum slowing). The '# Green' column (far left) shows the total number of green cells for that row.\r\n\r\nNote: Any missing quote data in your files could mean inaccurate results.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void ScanAllPortfoliosButton_Click(object sender, EventArgs e)
	{
		//IL_016d: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			if (MyProject.Forms.Mainform.PortfolioDataGridView.RowCount > 0)
			{
				GlobalForm.Quiet = true;
				string openPath = GlobalForm.OpenPath;
				DataGridView1.RowCount = 0;
				iRow = 0;
				int num = MyProject.Forms.Mainform.PortfolioDataGridView.RowCount - 1;
				ListBox ListBox;
				for (int i = 0; i <= num; i++)
				{
					GlobalForm.OpenPath = MyProject.Forms.Mainform.PortfolioDataGridView.Rows[i].Cells[1].Value.ToString();
					ListBox = ListBox1;
					GlobalForm.DisplayFiles(ref ListBox);
					ListBox1 = ListBox;
					SelectAllButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
					ref object[,] results = ref Results;
					results = (object[,])Utils.CopyArray((Array)results, (Array)new object[RRSIZE + 1, Information.UBound((Array)Results, 2) + ListBox1.SelectedIndices.Count + 1]);
					StartButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
					if (StopPressed)
					{
						break;
					}
				}
				GridDisplay(Information.UBound((Array)Results, 2));
				GlobalForm.OpenPath = openPath;
				ListBox = ListBox1;
				GlobalForm.DisplayFiles(ref ListBox);
				ListBox1 = ListBox;
				GlobalForm.Quiet = false;
				ProgressBar1.Value = 100;
				MessagesLabel.Text = "We're done, boss!";
				MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				MessagesLabel.Text = "Numbers are percentages except '# Green' and 'Last Close'. Missing quote data gives inaccurate results.";
				ProgressBar1.Value = 0;
				if ((DataGridView1.RowCount > 0) & !GlobalForm.Quiet)
				{
					((Control)ClipboardButton).Enabled = true;
				}
			}
			else
			{
				SelectAllButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
				StartButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			}
		}
	}

	private void StartButton_Click(object sender, EventArgs e)
	{
		//IL_0021: Unknown result type (might be due to invalid IL or missing references)
		//IL_0470: Unknown result type (might be due to invalid IL or missing references)
		int count = ListBox1.SelectedIndices.Count;
		if (count == 0)
		{
			MessageBox.Show("Please select some symbols to scan or click 'Select All.'", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			((Control)ListBox1).Focus();
			return;
		}
		if (!GlobalForm.Quiet)
		{
			StopPressed = false;
			DataGridView1.RowCount = 0;
			iRow = 0;
		}
		((Control)BrowseButton).Enabled = false;
		((Control)ClipboardButton).Enabled = false;
		((Control)DataGridView1).Enabled = false;
		((Control)DoneButton).Enabled = false;
		((Control)EndDatePicker).Enabled = false;
		((Control)HelpButton1).Enabled = false;
		((Control)ListBox1).Enabled = false;
		((Control)ScanAllPortfoliosButton).Enabled = false;
		((Control)SelectAllButton).Enabled = false;
		((Control)StartButton).Enabled = false;
		((Control)StopButton).Enabled = true;
		ProgressBar1.Value = 0;
		EndDatePicker.Value = GlobalForm.FindDate(EndDatePicker.Value);
		DateTime currentDate = GlobalForm.FindDate(EndDatePicker.Value);
		currentDate = GlobalForm.FindDate(currentDate);
		TargetDates[0] = currentDate;
		TargetDates[1] = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)4, -1.0, TargetDates[0]));
		TargetDates[2] = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)4, -1.0, TargetDates[1]));
		TargetDates[3] = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)4, -7.0, currentDate));
		TargetDates[4] = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)4, -14.0, currentDate));
		TargetDates[5] = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)4, -21.0, currentDate));
		TargetDates[6] = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)2, -1.0, currentDate));
		TargetDates[7] = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)2, -2.0, currentDate));
		TargetDates[8] = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)2, -3.0, currentDate));
		TargetDates[9] = TargetDates[8];
		TargetDates[10] = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)2, -6.0, currentDate));
		TargetDates[11] = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)2, -9.0, currentDate));
		TargetDates[12] = TargetDates[10];
		TargetDates[13] = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)2, -12.0, currentDate));
		TargetDates[14] = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)2, -18.0, currentDate));
		checked
		{
			if (!GlobalForm.Quiet)
			{
				Results = new object[RRSIZE + 1, count - 1 + 1];
			}
			int num = count - 1;
			for (int i = 0; i <= num; i++)
			{
				if (StopPressed)
				{
					break;
				}
				string text = ListBox1.SelectedItems[i].ToString();
				MessagesLabel.Text = text;
				((Control)MessagesLabel).Refresh();
				bool flag;
				if (count == 1)
				{
					ProgressBar ProgBar = ProgressBar1;
					Label ErrorLabel = null;
					bool num2 = GlobalForm.LoadFile(text, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
					ProgressBar1 = ProgBar;
					flag = num2;
				}
				else
				{
					ProgressBar ProgBar = null;
					Label ErrorLabel = null;
					flag = GlobalForm.LoadFile(text, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
				}
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				if (StopPressed)
				{
					break;
				}
				if (!flag)
				{
					Results[0, iRow] = text;
					CrunchNumbers(iRow);
					ProgressBar1.Value = (int)Math.Round((double)(100 * i) / (double)ListBox1.SelectedIndices.Count);
					iRow++;
				}
			}
			if (!GlobalForm.Quiet)
			{
				GridDisplay(count);
			}
			ProgressBar1.Value = 100;
			if (!GlobalForm.Quiet)
			{
				if (GlobalForm.IntradayData)
				{
					MessagesLabel.Text = "This form is meant for daily data, not intraday.";
				}
				else
				{
					MessagesLabel.Text = "We're done, boss!";
				}
				MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				MessagesLabel.Text = "Numbers are percentages except '# Green' and 'Last Close'. Missing quote data gives inaccurate results.";
				ProgressBar1.Value = 0;
			}
			((Control)BrowseButton).Enabled = true;
			if ((DataGridView1.RowCount > 0) & !GlobalForm.Quiet)
			{
				((Control)ClipboardButton).Enabled = true;
			}
			((Control)DataGridView1).Enabled = true;
			((Control)DoneButton).Enabled = true;
			((Control)EndDatePicker).Enabled = true;
			((Control)HelpButton1).Enabled = true;
			((Control)ListBox1).Enabled = true;
			((Control)ScanAllPortfoliosButton).Enabled = true;
			((Control)SelectAllButton).Enabled = true;
			((Control)StartButton).Enabled = true;
			((Control)StopButton).Enabled = false;
		}
	}

	private void SelectAllButton_Click(object sender, EventArgs e)
	{
		ListBox1.BeginUpdate();
		checked
		{
			int num = ListBox1.Items.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				ListBox1.SetSelected(i, true);
			}
			ListBox1.EndUpdate();
		}
	}

	private void StopButton_Click(object sender, EventArgs e)
	{
		StopPressed = true;
		Interaction.Beep();
	}
}
