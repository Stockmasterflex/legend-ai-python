using System;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class ListForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("DataGridView1")]
	private DataGridView _DataGridView1;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StopButton")]
	private Button _StopButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StartButton")]
	private Button _StartButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ClipboardButton")]
	private Button _ClipboardButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PatternsButton")]
	private Button _PatternsButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StrictCheckBox")]
	private CheckBox _StrictCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("HelpButton1")]
	private Button _HelpButton1;

	[CompilerGenerated]
	[AccessedThroughProperty("ListAllPortfoliosButton")]
	private Button _ListAllPortfoliosButton;

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
	[AccessedThroughProperty("CandlesButton")]
	private Button _CandlesButton;

	[CompilerGenerated]
	[AccessedThroughProperty("CandlesCheckBox")]
	private CheckBox _CandlesCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("GraphButton")]
	private Button _GraphButton;

	[CompilerGenerated]
	[AccessedThroughProperty("FiltersButton")]
	private Button _FiltersButton;

	private bool StopPressed;

	private bool LockFlag;

	private int iRow;

	private bool LFStrict;

	public bool lsShowCandles;

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
			EventHandler eventHandler = DataGridView1_DoubleClick;
			DataGridView val = _DataGridView1;
			if (val != null)
			{
				((Control)val).DoubleClick -= eventHandler;
			}
			_DataGridView1 = value;
			val = _DataGridView1;
			if (val != null)
			{
				((Control)val).DoubleClick += eventHandler;
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

	[field: AccessedThroughProperty("ProgressBar1")]
	internal virtual ProgressBar ProgressBar1
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

	internal virtual Button ListAllPortfoliosButton
	{
		[CompilerGenerated]
		get
		{
			return _ListAllPortfoliosButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ListAllPortfoliosButton_Click;
			Button val = _ListAllPortfoliosButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ListAllPortfoliosButton = value;
			val = _ListAllPortfoliosButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
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

	[field: AccessedThroughProperty("FilenameLabel")]
	internal virtual Label FilenameLabel
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

	[field: AccessedThroughProperty("PatternsCheckBox")]
	internal virtual CheckBox PatternsCheckBox
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

	internal virtual Button FiltersButton
	{
		[CompilerGenerated]
		get
		{
			return _FiltersButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = FiltersButton_Click;
			Button val = _FiltersButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_FiltersButton = value;
			val = _FiltersButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	public ListForm()
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		((Form)this).FormClosing += new FormClosingEventHandler(ListForm_FormClosing);
		((Form)this).Load += ListForm_Load;
		StopPressed = false;
		LockFlag = false;
		iRow = 0;
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
		//IL_00a6: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b0: Expected O, but got Unknown
		//IL_00b1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00bb: Expected O, but got Unknown
		//IL_00bc: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c6: Expected O, but got Unknown
		//IL_00c7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d1: Expected O, but got Unknown
		//IL_00d2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00dc: Expected O, but got Unknown
		//IL_00dd: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e7: Expected O, but got Unknown
		//IL_00e8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f2: Expected O, but got Unknown
		//IL_00f3: Unknown result type (might be due to invalid IL or missing references)
		//IL_00fd: Expected O, but got Unknown
		//IL_00fe: Unknown result type (might be due to invalid IL or missing references)
		//IL_0108: Expected O, but got Unknown
		//IL_0109: Unknown result type (might be due to invalid IL or missing references)
		//IL_0113: Expected O, but got Unknown
		//IL_0114: Unknown result type (might be due to invalid IL or missing references)
		//IL_011e: Expected O, but got Unknown
		DataGridView1 = new DataGridView();
		Label3 = new Label();
		Label2 = new Label();
		DoneButton = new Button();
		StopButton = new Button();
		StartButton = new Button();
		ClipboardButton = new Button();
		PatternsButton = new Button();
		Label1 = new Label();
		SymbolTextBox = new TextBox();
		StrictCheckBox = new CheckBox();
		ProgressBar1 = new ProgressBar();
		HelpButton1 = new Button();
		ListAllPortfoliosButton = new Button();
		MonthlyRadioButton = new RadioButton();
		WeeklyRadioButton = new RadioButton();
		DailyRadioButton = new RadioButton();
		ErrorLabel = new Label();
		FilenameLabel = new Label();
		ToDatePicker = new DateTimePicker();
		FromDatePicker = new DateTimePicker();
		CandlesButton = new Button();
		PatternsCheckBox = new CheckBox();
		CandlesCheckBox = new CheckBox();
		GraphButton = new Button();
		FiltersButton = new Button();
		((ISupportInitialize)DataGridView1).BeginInit();
		((Control)this).SuspendLayout();
		DataGridView1.AllowUserToAddRows = false;
		DataGridView1.AllowUserToDeleteRows = false;
		DataGridView1.AllowUserToResizeColumns = false;
		DataGridView1.AllowUserToResizeRows = false;
		((Control)DataGridView1).Anchor = (AnchorStyles)15;
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
		((Control)DataGridView1).Size = new Size(984, 444);
		((Control)DataGridView1).TabIndex = 1;
		((Control)Label3).Anchor = (AnchorStyles)10;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(545, 497);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(23, 13);
		((Control)Label3).TabIndex = 16;
		Label3.Text = "&To:";
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(535, 472);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(33, 13);
		((Control)Label2).TabIndex = 14;
		Label2.Text = "&From:";
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(943, 495);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(53, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)StopButton).Anchor = (AnchorStyles)10;
		((Control)StopButton).Enabled = false;
		((Control)StopButton).Location = new Point(831, 467);
		((Control)StopButton).Name = "StopButton";
		((Control)StopButton).Size = new Size(40, 23);
		((Control)StopButton).TabIndex = 22;
		((ButtonBase)StopButton).Text = "St&op";
		((ButtonBase)StopButton).UseVisualStyleBackColor = true;
		((Control)StartButton).Anchor = (AnchorStyles)10;
		((Control)StartButton).Location = new Point(811, 495);
		((Control)StartButton).Name = "StartButton";
		((Control)StartButton).Size = new Size(60, 23);
		((Control)StartButton).TabIndex = 21;
		((ButtonBase)StartButton).Text = "St&art";
		((ButtonBase)StartButton).UseVisualStyleBackColor = true;
		((Control)ClipboardButton).Anchor = (AnchorStyles)10;
		((Control)ClipboardButton).Enabled = false;
		((Control)ClipboardButton).Location = new Point(765, 467);
		((Control)ClipboardButton).Name = "ClipboardButton";
		((Control)ClipboardButton).Size = new Size(60, 23);
		((Control)ClipboardButton).TabIndex = 20;
		((ButtonBase)ClipboardButton).Text = "Clip&board";
		((ButtonBase)ClipboardButton).UseVisualStyleBackColor = true;
		((Control)PatternsButton).Anchor = (AnchorStyles)10;
		((Control)PatternsButton).Location = new Point(877, 495);
		((Control)PatternsButton).Name = "PatternsButton";
		((Control)PatternsButton).Size = new Size(60, 23);
		((Control)PatternsButton).TabIndex = 24;
		((ButtonBase)PatternsButton).Text = "&Patterns";
		((ButtonBase)PatternsButton).UseVisualStyleBackColor = true;
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Enabled = false;
		((Control)Label1).Location = new Point(431, 497);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(44, 13);
		((Control)Label1).TabIndex = 12;
		Label1.Text = "S&ymbol:";
		((Control)Label1).Visible = false;
		((Control)SymbolTextBox).Anchor = (AnchorStyles)10;
		((Control)SymbolTextBox).Enabled = false;
		((Control)SymbolTextBox).Location = new Point(475, 494);
		((Control)SymbolTextBox).Name = "SymbolTextBox";
		((Control)SymbolTextBox).Size = new Size(75, 20);
		((Control)SymbolTextBox).TabIndex = 13;
		((Control)SymbolTextBox).Visible = false;
		((Control)StrictCheckBox).Anchor = (AnchorStyles)10;
		((ButtonBase)StrictCheckBox).AutoSize = true;
		((Control)StrictCheckBox).Location = new Point(303, 501);
		((Control)StrictCheckBox).Name = "StrictCheckBox";
		((Control)StrictCheckBox).Size = new Size(50, 17);
		((Control)StrictCheckBox).TabIndex = 9;
		((ButtonBase)StrictCheckBox).Text = "St&rict";
		((ButtonBase)StrictCheckBox).UseVisualStyleBackColor = true;
		((Control)ProgressBar1).Anchor = (AnchorStyles)10;
		((Control)ProgressBar1).ForeColor = Color.Green;
		((Control)ProgressBar1).Location = new Point(407, 466);
		((Control)ProgressBar1).Name = "ProgressBar1";
		((Control)ProgressBar1).Size = new Size(122, 23);
		((Control)ProgressBar1).TabIndex = 11;
		((Control)HelpButton1).Anchor = (AnchorStyles)10;
		((Control)HelpButton1).Location = new Point(707, 467);
		((Control)HelpButton1).Name = "HelpButton1";
		((Control)HelpButton1).Size = new Size(52, 23);
		((Control)HelpButton1).TabIndex = 18;
		((ButtonBase)HelpButton1).Text = "&Help";
		((ButtonBase)HelpButton1).UseVisualStyleBackColor = true;
		((Control)ListAllPortfoliosButton).Anchor = (AnchorStyles)10;
		((Control)ListAllPortfoliosButton).Enabled = false;
		((Control)ListAllPortfoliosButton).Location = new Point(707, 495);
		((Control)ListAllPortfoliosButton).Name = "ListAllPortfoliosButton";
		((Control)ListAllPortfoliosButton).Size = new Size(98, 23);
		((Control)ListAllPortfoliosButton).TabIndex = 19;
		((ButtonBase)ListAllPortfoliosButton).Text = "L&ist All Portfolios";
		((ButtonBase)ListAllPortfoliosButton).UseVisualStyleBackColor = true;
		((Control)MonthlyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)MonthlyRadioButton).AutoSize = true;
		((Control)MonthlyRadioButton).Location = new Point(235, 496);
		((Control)MonthlyRadioButton).Name = "MonthlyRadioButton";
		((Control)MonthlyRadioButton).Size = new Size(62, 17);
		((Control)MonthlyRadioButton).TabIndex = 6;
		((Control)MonthlyRadioButton).Tag = "Monthly";
		((ButtonBase)MonthlyRadioButton).Text = "&Monthly";
		((ButtonBase)MonthlyRadioButton).UseVisualStyleBackColor = true;
		((Control)WeeklyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)WeeklyRadioButton).AutoSize = true;
		((Control)WeeklyRadioButton).Location = new Point(235, 481);
		((Control)WeeklyRadioButton).Name = "WeeklyRadioButton";
		((Control)WeeklyRadioButton).Size = new Size(61, 17);
		((Control)WeeklyRadioButton).TabIndex = 5;
		((Control)WeeklyRadioButton).Tag = "Weekly";
		((ButtonBase)WeeklyRadioButton).Text = "&Weekly";
		((ButtonBase)WeeklyRadioButton).UseVisualStyleBackColor = true;
		((Control)DailyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)DailyRadioButton).AutoSize = true;
		DailyRadioButton.Checked = true;
		((Control)DailyRadioButton).Location = new Point(235, 466);
		((Control)DailyRadioButton).Name = "DailyRadioButton";
		((Control)DailyRadioButton).Size = new Size(48, 17);
		((Control)DailyRadioButton).TabIndex = 4;
		DailyRadioButton.TabStop = true;
		((Control)DailyRadioButton).Tag = "Daily";
		((ButtonBase)DailyRadioButton).Text = "Dail&y";
		((ButtonBase)DailyRadioButton).UseVisualStyleBackColor = true;
		((Control)ErrorLabel).Anchor = (AnchorStyles)14;
		ErrorLabel.BorderStyle = (BorderStyle)2;
		((Control)ErrorLabel).Location = new Point(12, 486);
		((Control)ErrorLabel).Name = "ErrorLabel";
		((Control)ErrorLabel).Size = new Size(217, 29);
		((Control)ErrorLabel).TabIndex = 3;
		((Control)FilenameLabel).Anchor = (AnchorStyles)14;
		FilenameLabel.BorderStyle = (BorderStyle)2;
		((Control)FilenameLabel).Location = new Point(12, 463);
		((Control)FilenameLabel).Name = "FilenameLabel";
		((Control)FilenameLabel).Size = new Size(217, 22);
		((Control)FilenameLabel).TabIndex = 2;
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(574, 494);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(120, 20);
		((Control)ToDatePicker).TabIndex = 17;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(574, 468);
		((Control)FromDatePicker).Name = "FromDatePicker";
		FromDatePicker.ShowUpDown = true;
		((Control)FromDatePicker).Size = new Size(120, 20);
		((Control)FromDatePicker).TabIndex = 15;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)CandlesButton).Anchor = (AnchorStyles)10;
		((Control)CandlesButton).Location = new Point(877, 467);
		((Control)CandlesButton).Name = "CandlesButton";
		((Control)CandlesButton).Size = new Size(60, 23);
		((Control)CandlesButton).TabIndex = 23;
		((ButtonBase)CandlesButton).Text = "&Candles";
		((ButtonBase)CandlesButton).UseVisualStyleBackColor = true;
		((Control)PatternsCheckBox).Anchor = (AnchorStyles)10;
		((ButtonBase)PatternsCheckBox).AutoSize = true;
		((Control)PatternsCheckBox).Location = new Point(303, 481);
		((Control)PatternsCheckBox).Name = "PatternsCheckBox";
		((Control)PatternsCheckBox).Size = new Size(95, 17);
		((Control)PatternsCheckBox).TabIndex = 8;
		((ButtonBase)PatternsCheckBox).Text = "&Show Patterns";
		((ButtonBase)PatternsCheckBox).UseVisualStyleBackColor = true;
		((Control)CandlesCheckBox).Anchor = (AnchorStyles)10;
		((ButtonBase)CandlesCheckBox).AutoSize = true;
		((Control)CandlesCheckBox).Location = new Point(303, 463);
		((Control)CandlesCheckBox).Name = "CandlesCheckBox";
		((Control)CandlesCheckBox).Size = new Size(94, 17);
		((Control)CandlesCheckBox).TabIndex = 7;
		((ButtonBase)CandlesCheckBox).Text = "Show Cand&les";
		((ButtonBase)CandlesCheckBox).UseVisualStyleBackColor = true;
		((Control)GraphButton).Anchor = (AnchorStyles)10;
		((Control)GraphButton).Enabled = false;
		((Control)GraphButton).Location = new Point(943, 467);
		((Control)GraphButton).Name = "GraphButton";
		((Control)GraphButton).Size = new Size(53, 23);
		((Control)GraphButton).TabIndex = 25;
		((ButtonBase)GraphButton).Text = "&Graph";
		((ButtonBase)GraphButton).UseVisualStyleBackColor = true;
		((Control)FiltersButton).Anchor = (AnchorStyles)10;
		((Control)FiltersButton).Location = new Point(407, 495);
		((Control)FiltersButton).Name = "FiltersButton";
		((Control)FiltersButton).Size = new Size(45, 23);
		((Control)FiltersButton).TabIndex = 10;
		((ButtonBase)FiltersButton).Text = "&Filters";
		((ButtonBase)FiltersButton).UseVisualStyleBackColor = true;
		((Form)this).AcceptButton = (IButtonControl)(object)StartButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(1008, 521);
		((Control)this).Controls.Add((Control)(object)FiltersButton);
		((Control)this).Controls.Add((Control)(object)GraphButton);
		((Control)this).Controls.Add((Control)(object)ToDatePicker);
		((Control)this).Controls.Add((Control)(object)FromDatePicker);
		((Control)this).Controls.Add((Control)(object)FilenameLabel);
		((Control)this).Controls.Add((Control)(object)ErrorLabel);
		((Control)this).Controls.Add((Control)(object)MonthlyRadioButton);
		((Control)this).Controls.Add((Control)(object)WeeklyRadioButton);
		((Control)this).Controls.Add((Control)(object)DailyRadioButton);
		((Control)this).Controls.Add((Control)(object)ListAllPortfoliosButton);
		((Control)this).Controls.Add((Control)(object)HelpButton1);
		((Control)this).Controls.Add((Control)(object)CandlesCheckBox);
		((Control)this).Controls.Add((Control)(object)PatternsCheckBox);
		((Control)this).Controls.Add((Control)(object)CandlesButton);
		((Control)this).Controls.Add((Control)(object)ProgressBar1);
		((Control)this).Controls.Add((Control)(object)StrictCheckBox);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)SymbolTextBox);
		((Control)this).Controls.Add((Control)(object)PatternsButton);
		((Control)this).Controls.Add((Control)(object)ClipboardButton);
		((Control)this).Controls.Add((Control)(object)StartButton);
		((Control)this).Controls.Add((Control)(object)StopButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)DataGridView1);
		((Control)this).Name = "ListForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "List Form";
		((ISupportInitialize)DataGridView1).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void ListForm_FormClosing(object sender, FormClosingEventArgs e)
	{
		GlobalForm.LFDateLookBack = DateAndTime.DateDiff((DateInterval)4, FromDatePicker.Value, ToDatePicker.Value, (FirstDayOfWeek)1, (FirstWeekOfYear)1);
		GlobalForm.StrictPatterns = LFStrict;
		GlobalForm.LFPatterns = PatternsCheckBox.Checked;
		GlobalForm.LFCandles = CandlesCheckBox.Checked;
		GlobalForm.ShowCandles = lsShowCandles;
		MySettingsProperty.Settings.ListFormLocation = ((Form)this).Location;
		MySettingsProperty.Settings.ListFormSize = ((Form)this).Size;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
	}

	private void ListForm_Load(object sender, EventArgs e)
	{
		//IL_0021: Unknown result type (might be due to invalid IL or missing references)
		//IL_0026: Unknown result type (might be due to invalid IL or missing references)
		//IL_0031: Unknown result type (might be due to invalid IL or missing references)
		//IL_003c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0047: Unknown result type (might be due to invalid IL or missing references)
		//IL_004e: Unknown result type (might be due to invalid IL or missing references)
		//IL_005f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0070: Unknown result type (might be due to invalid IL or missing references)
		//IL_0081: Unknown result type (might be due to invalid IL or missing references)
		//IL_0092: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a3: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b4: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c5: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d6: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f8: Unknown result type (might be due to invalid IL or missing references)
		//IL_0109: Unknown result type (might be due to invalid IL or missing references)
		//IL_011a: Unknown result type (might be due to invalid IL or missing references)
		//IL_012b: Unknown result type (might be due to invalid IL or missing references)
		//IL_013c: Unknown result type (might be due to invalid IL or missing references)
		//IL_014d: Unknown result type (might be due to invalid IL or missing references)
		//IL_015e: Unknown result type (might be due to invalid IL or missing references)
		LockFlag = true;
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.ListFormLocation, MySettingsProperty.Settings.ListFormSize);
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)GraphButton, "Chart the highlighted pattern.");
		val.SetToolTip((Control)(object)StartButton, "Start listing patterns.");
		val.SetToolTip((Control)(object)StopButton, "Halt the listing process.");
		val.SetToolTip((Control)(object)PatternsButton, "Load the Chart Patterns Form.");
		val.SetToolTip((Control)(object)CandlesButton, "Load the Candles Form.");
		val.SetToolTip((Control)(object)ClipboardButton, "Copy highlighted rows to the clipboard.");
		val.SetToolTip((Control)(object)FiltersButton, "Setup filters to screen chart patterns.");
		val.SetToolTip((Control)(object)FromDatePicker, "Enter the starting date to search.");
		val.SetToolTip((Control)(object)ToDatePicker, "Enter the ending date to search.");
		val.SetToolTip((Control)(object)DataGridView1, "Highlight rows to copy to the clipboard.");
		val.SetToolTip((Control)(object)PatternsCheckBox, "If checked, find chart patterns.");
		val.SetToolTip((Control)(object)CandlesCheckBox, "If checked, find candlesticks.");
		val.SetToolTip((Control)(object)StrictCheckBox, "Use strict or loose rules when finding chart patterns or candlesticks.");
		val.SetToolTip((Control)(object)ListAllPortfoliosButton, "Open all portfolios and list each file.");
		val.SetToolTip((Control)(object)DailyRadioButton, "Find patterns using the daily scale.");
		val.SetToolTip((Control)(object)WeeklyRadioButton, "Find patterns using the weekly scale.");
		val.SetToolTip((Control)(object)MonthlyRadioButton, "Find patterns using the monthly scale.");
		ProgressBar1.Value = 0;
		SymbolTextBox.Text = "";
		StopPressed = false;
		BuildGridHeader();
		((Control)DailyRadioButton).Tag = 0;
		((Control)WeeklyRadioButton).Tag = 1;
		((Control)MonthlyRadioButton).Tag = 2;
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
		DisableEnable(EnableFlag: true);
		GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
		FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)checked(-1 * GlobalForm.LFDateLookBack), DateAndTime.Now);
		ToDatePicker.Value = DateAndTime.Now;
		LFStrict = GlobalForm.StrictPatterns;
		StrictCheckBox.Checked = GlobalForm.StrictPatterns;
		PatternsCheckBox.Checked = GlobalForm.LFPatterns;
		CandlesCheckBox.Checked = GlobalForm.LFCandles;
		lsShowCandles = GlobalForm.ShowCandles;
		GlobalForm.ShowCandles = GlobalForm.LFCandles;
		GlobalForm.ShowAllPatterns = true;
		LockFlag = false;
		DataGridView1.ClipboardCopyMode = (DataGridViewClipboardCopyMode)2;
		GlobalForm.ReadFilterConfigFile(RuntimeHelpers.GetObjectValue(sender), e);
	}

	private void BuildGrid(string Filename)
	{
		checked
		{
			if (GlobalForm.FilterGlobals.CBMasterSwitch & GlobalForm.FilterGlobals.CBStages)
			{
				FindPatterns.FindWeinsteinStages(Filename, 0);
				int num = GlobalForm.WStages[GlobalForm.WStages.Length - 1];
				if (unchecked((GlobalForm.FilterGlobals.CBStage1 && num == 1) | (GlobalForm.FilterGlobals.CBStage2 && num == 2) | (GlobalForm.FilterGlobals.CBStage3 && num == 3) | (GlobalForm.FilterGlobals.CBStage4 && num == 4)))
				{
					DataGridView1.Rows.Add();
					DataGridView1.Rows[iRow].Cells[0].Value = Filename;
					DataGridView1.Rows[iRow].Cells[1].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]);
					DataGridView1.Rows[iRow].Cells[2].Value = "Stage";
					DataGridView1.Rows[iRow].Cells[3].Value = FromDatePicker.Value;
					DataGridView1.Rows[iRow].Cells[4].Value = ToDatePicker.Value;
					DataGridView1.Rows[iRow].Cells[17].Value = num.ToString();
					DataGridView1.Rows[iRow].Cells[18].Value = "S";
					iRow++;
				}
			}
			int num2 = GlobalForm.PatternCount - 1;
			long iWidth = default(long);
			int iHeight = default(int);
			for (int i = 0; i <= num2; i++)
			{
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				if (StopPressed)
				{
					break;
				}
				if (!((GlobalForm.ChartPatterns[i].iStartDate >= GlobalForm.ChartStartIndex) & (GlobalForm.ChartPatterns[i].iEndDate <= GlobalForm.ChartEndIndex)))
				{
					continue;
				}
				GlobalForm.UseOriginalDate = false;
				GlobalForm.GetCPInformation(i);
				int num3 = FilterPatterns(i, ref iWidth, ref iHeight);
				if (unchecked(num3 == 2 || num3 == 3))
				{
					DataGridView1.Rows.Add();
					DataGridView1.Rows[iRow].Cells[0].Value = Filename;
					DataGridView1.Rows[iRow].Cells[1].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]);
					DataGridView1.Rows[iRow].Cells[2].Value = GlobalForm.GetPatternPhrase(i);
					int num4 = ((GlobalForm.ChartPatterns[i].iStart2Date == 0) ? GlobalForm.ChartPatterns[i].iStartDate : Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iStartDate < GlobalForm.ChartPatterns[i].iStart2Date, (object)GlobalForm.ChartPatterns[i].iStartDate, (object)GlobalForm.ChartPatterns[i].iStart2Date)));
					int num5 = ((!GlobalForm.UseOriginalDate) ? Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iEndDate > GlobalForm.ChartPatterns[i].iEnd2Date, (object)GlobalForm.ChartPatterns[i].iEndDate, (object)GlobalForm.ChartPatterns[i].iEnd2Date)) : GlobalForm.ChartPatterns[i].iEndDate);
					if ((GlobalForm.ChartPatterns[i].Type == 82) | (GlobalForm.ChartPatterns[i].Type == 1))
					{
						num5 = GlobalForm.ChartPatterns[i].iMidDate;
					}
					DataGridView1.Rows[iRow].Cells[3].Value = Strings.Format((object)GlobalForm.nDT[0, num4], GlobalForm.UserDate);
					DataGridView1.Rows[iRow].Cells[4].Value = Strings.Format((object)GlobalForm.nDT[0, num5], GlobalForm.UserDate);
					DataGridView1.Rows[iRow].Cells[5].Value = RuntimeHelpers.GetObjectValue(Interaction.IIf(Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, (string)null, false) == 0, (object)"None yet", (object)GlobalForm.CPInfo.BkoutDirection));
					DataGridView1.Rows[iRow].Cells[6].Value = GlobalForm.CPInfo.BkoutDate;
					string text = GlobalForm.LimitDecimals(GlobalForm.CPInfo.BkoutPrice);
					if (Operators.CompareString(text, "0", false) == 0)
					{
						text = "";
					}
					DataGridView1.Rows[iRow].Cells[7].Value = text;
					if ((GlobalForm.CPInfo.iBkout == -1) | (Operators.CompareString(text, "", false) == 0) | (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "N/A", false) == 0) | (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "N/A ", false) == 0))
					{
						DataGridView1.Rows[iRow].Cells[8].Value = 0m;
					}
					else
					{
						DataGridView1.Rows[iRow].Cells[8].Value = GlobalForm.GetPriceFill(GlobalForm.CPInfo.iBkout, Conversions.ToDecimal(GlobalForm.CPInfo.BkoutPrice), Conversions.ToInteger(Interaction.IIf(Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0, (object)1, (object)(-1))), CandleFlag: false);
					}
					DataGridView1.Rows[iRow].Cells[9].Value = GlobalForm.CPInfo.AvgVolume;
					text = GlobalForm.LimitDecimals(GlobalForm.CPInfo.UltHLPrice);
					if (Operators.CompareString(text, "0", false) == 0)
					{
						text = "";
					}
					DataGridView1.Rows[iRow].Cells[10].Value = text;
					DataGridView1.Rows[iRow].Cells[11].Value = GlobalForm.CPInfo.UltHLDate;
					DataGridView1.Rows[iRow].Cells[12].Value = GlobalForm.CPInfo.Target;
					DataGridView1.Rows[iRow].Cells[13].Value = GlobalForm.CPInfo.VolStop;
					DataGridView1.Rows[iRow].Cells[14].Value = RuntimeHelpers.GetObjectValue(Interaction.IIf(Operators.CompareString(GlobalForm.CPInfo.Status, (string)null, false) == 0, (object)"Open", (object)GlobalForm.CPInfo.Status));
					DataGridView1.Rows[iRow].Cells[15].Value = iWidth.ToString();
					DataGridView1.Rows[iRow].Cells[18].Value = "";
					int num6 = iHeight;
					text = ((num6 == GlobalForm.cTall) ? "Tall" : ((num6 != GlobalForm.ShortPat) ? "Unknown" : "Short"));
					DataGridView1.Rows[iRow].Cells[16].Value = text;
					iRow++;
				}
			}
			if (GlobalForm.FilterGlobals.CBPriceMoves & !GlobalForm.FilterGlobals.CBHighVolume)
			{
				decimal numericPriceMoves = GlobalForm.FilterGlobals.NumericPriceMoves;
				if ((GlobalForm.HLCRange > 0) & (decimal.Compare(GlobalForm.nHLC[3, GlobalForm.HLCRange - 1], 0m) != 0))
				{
					decimal num7 = decimal.Divide(decimal.Multiply(100m, decimal.Subtract(GlobalForm.nHLC[3, GlobalForm.HLCRange], GlobalForm.nHLC[3, GlobalForm.HLCRange - 1])), GlobalForm.nHLC[3, GlobalForm.HLCRange - 1]);
					if (((decimal.Compare(numericPriceMoves, 0m) > 0) & (decimal.Compare(num7, numericPriceMoves) >= 0)) | ((decimal.Compare(numericPriceMoves, 0m) < 0) & (decimal.Compare(num7, 0m) < 0) & (decimal.Compare(Math.Abs(num7), Math.Abs(numericPriceMoves)) > 0)))
					{
						DataGridView1.Rows.Add();
						DataGridView1.Rows[iRow].Cells[0].Value = Filename;
						DataGridView1.Rows[iRow].Cells[1].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]);
						DataGridView1.Rows[iRow].Cells[2].Value = "Big price move: " + Strings.Format((object)decimal.Divide(num7, 100m), "0.0%");
						DataGridView1.Rows[iRow].Cells[3].Value = Strings.Format((object)GlobalForm.nDT[0, GlobalForm.HLCRange], GlobalForm.UserDate);
						DataGridView1.Rows[iRow].Cells[4].Value = Strings.Format((object)GlobalForm.nDT[0, GlobalForm.HLCRange], GlobalForm.UserDate);
						DataGridView1.Rows[iRow].Cells[18].Value = "P";
						iRow++;
					}
				}
			}
			else if (!GlobalForm.FilterGlobals.CBPriceMoves & GlobalForm.FilterGlobals.CBHighVolume)
			{
				decimal d = GlobalForm.nHLC[4, GlobalForm.HLCRange];
				if (GlobalForm.HLCRange > 0)
				{
					decimal num8 = Conversions.ToDecimal(GlobalForm.Get3MoAvgVolume(GlobalForm.nDT[0, GlobalForm.HLCRange - 1]));
					if (decimal.Compare(d, decimal.Multiply(num8, GlobalForm.FilterGlobals.NumericHighVolume)) >= 0)
					{
						DataGridView1.Rows.Add();
						DataGridView1.Rows[iRow].Cells[0].Value = Filename;
						DataGridView1.Rows[iRow].Cells[1].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]);
						DataGridView1.Rows[iRow].Cells[2].Value = "High volume: " + Strings.Format((object)GlobalForm.nHLC[4, GlobalForm.HLCRange], "#,0");
						DataGridView1.Rows[iRow].Cells[3].Value = Strings.Format((object)GlobalForm.nDT[0, GlobalForm.HLCRange], GlobalForm.UserDate);
						DataGridView1.Rows[iRow].Cells[4].Value = Strings.Format((object)GlobalForm.nDT[0, GlobalForm.HLCRange], GlobalForm.UserDate);
						DataGridView1.Rows[iRow].Cells[9].Value = Strings.Format((object)num8, "#,0");
						DataGridView1.Rows[iRow].Cells[18].Value = "V";
						iRow++;
					}
				}
			}
			else
			{
				if (!(GlobalForm.FilterGlobals.CBPriceMoves & GlobalForm.FilterGlobals.CBHighVolume))
				{
					return;
				}
				decimal numericPriceMoves2 = GlobalForm.FilterGlobals.NumericPriceMoves;
				if (!((GlobalForm.HLCRange > 0) & (decimal.Compare(GlobalForm.nHLC[3, GlobalForm.HLCRange - 1], 0m) != 0)))
				{
					return;
				}
				decimal num9 = decimal.Divide(decimal.Multiply(100m, decimal.Subtract(GlobalForm.nHLC[3, GlobalForm.HLCRange], GlobalForm.nHLC[3, GlobalForm.HLCRange - 1])), GlobalForm.nHLC[3, GlobalForm.HLCRange - 1]);
				if (!(((decimal.Compare(numericPriceMoves2, 0m) > 0) & (decimal.Compare(num9, numericPriceMoves2) >= 0)) | ((decimal.Compare(numericPriceMoves2, 0m) < 0) & (decimal.Compare(num9, 0m) < 0) & (decimal.Compare(Math.Abs(num9), Math.Abs(numericPriceMoves2)) > 0))))
				{
					return;
				}
				numericPriceMoves2 = GlobalForm.nHLC[4, GlobalForm.HLCRange];
				if (GlobalForm.HLCRange > 0)
				{
					decimal num10 = Conversions.ToDecimal(GlobalForm.Get3MoAvgVolume(GlobalForm.nDT[0, GlobalForm.HLCRange - 1]));
					if (decimal.Compare(numericPriceMoves2, decimal.Multiply(num10, GlobalForm.FilterGlobals.NumericHighVolume)) >= 0)
					{
						DataGridView1.Rows.Add();
						DataGridView1.Rows[iRow].Cells[0].Value = Filename;
						DataGridView1.Rows[iRow].Cells[1].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]);
						DataGridView1.Rows[iRow].Cells[2].Value = "Big price move, " + Strings.Format((object)decimal.Divide(num9, 100m), "0.0%") + ", on high volume: " + Strings.Format((object)GlobalForm.nHLC[4, GlobalForm.HLCRange], "#,0") + " shares.";
						DataGridView1.Rows[iRow].Cells[3].Value = Strings.Format((object)GlobalForm.nDT[0, GlobalForm.HLCRange], GlobalForm.UserDate);
						DataGridView1.Rows[iRow].Cells[4].Value = Strings.Format((object)GlobalForm.nDT[0, GlobalForm.HLCRange], GlobalForm.UserDate);
						DataGridView1.Rows[iRow].Cells[9].Value = Strings.Format((object)num10, "#,0");
						DataGridView1.Rows[iRow].Cells[18].Value = "VP";
						iRow++;
					}
				}
			}
		}
	}

	private void BuildGridHeader()
	{
		DataGridView1.RowCount = 0;
		DataGridView1.ColumnCount = 20;
		DataGridView1.Columns[0].HeaderText = "Stock";
		DataGridView1.Columns[1].HeaderText = "Last Close";
		DataGridView1.Columns[2].HeaderText = "Pattern Description";
		DataGridView1.Columns[3].HeaderText = "Start";
		DataGridView1.Columns[4].HeaderText = "End";
		DataGridView1.Columns[5].HeaderText = "Breakout";
		DataGridView1.Columns[6].HeaderText = "Breakout Date";
		DataGridView1.Columns[7].HeaderText = "Approx. Breakout Price";
		DataGridView1.Columns[8].HeaderText = "Fill Price";
		DataGridView1.Columns[10].HeaderText = "Ultimate High/Low";
		DataGridView1.Columns[11].HeaderText = "Ultimate H/L Date";
		DataGridView1.Columns[12].HeaderText = "Approx. Target";
		DataGridView1.Columns[13].HeaderText = "Volatility Stop";
		DataGridView1.Columns[9].HeaderText = "Avg 3 Mo. Volume";
		DataGridView1.Columns[14].HeaderText = "Trade Status";
		DataGridView1.Columns[15].HeaderText = "Pattern Width (days/price bars)";
		DataGridView1.Columns[16].HeaderText = "Height";
		DataGridView1.Columns[17].HeaderText = "Stage";
		DataGridView1.Columns[18].Visible = false;
		DataGridView1.Columns[19].Visible = false;
	}

	private void BuildList()
	{
		//IL_00db: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00dc: Unknown result type (might be due to invalid IL or missing references)
		//IL_00de: Invalid comparison between Unknown and I4
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
		ProgressBar1.Value = 1;
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
				string text = Strings.Trim(SymbolTextBox.Text);
				if ((Operators.CompareString(Strings.Right(text, 4).ToUpper(), ".CSV", false) != 0) & (Operators.CompareString(Strings.Right(text, 4).ToUpper(), ".TXT", false) != 0))
				{
					string text2 = text + ".csv";
					if (!File.Exists(GlobalForm.OpenPath + "\\" + text2))
					{
						text2 = text + ".txt";
					}
					text = text2;
				}
				int num2 = MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count - 1;
				int num3 = 0;
				while (true)
				{
					if (num3 <= num2)
					{
						if (Operators.CompareString(text, MyProject.Forms.Mainform.ListBox1.SelectedItems[num3].ToString(), false) == 0)
						{
							SymbolTextBox.Text = "";
							break;
						}
						num3++;
						continue;
					}
					ProcessSymbol();
					ProgressBar1.Value = 25;
					break;
				}
			}
			if (CandlesCheckBox.Checked)
			{
				GlobalForm.ShowCandles = true;
			}
			else
			{
				GlobalForm.ShowCandles = false;
				if (GlobalForm.CandleCount > 0)
				{
					GlobalForm.CandlePatterns = null;
					GlobalForm.CandleCount = 0;
				}
			}
			if (PatternsCheckBox.Checked)
			{
				GlobalForm.ShowAllPatterns = true;
			}
			else
			{
				GlobalForm.ShowAllPatterns = false;
				if (GlobalForm.PatternCount > 0)
				{
					GlobalForm.ChartPatterns = null;
					GlobalForm.PatternCount = 0;
				}
			}
			int count = MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count;
			DataGridView1.RowHeadersVisible = false;
			DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)1;
			int num4 = count - 1;
			for (int j = 0; j <= num4; j++)
			{
				string text = MyProject.Forms.Mainform.ListBox1.SelectedItems[j].ToString();
				FilenameLabel.Text = text;
				((Control)FilenameLabel).Refresh();
				if ((this.ErrorLabel.Text.Length == 0) | (Operators.CompareString(this.ErrorLabel.Text, "Finding...", false) == 0))
				{
					this.ErrorLabel.Text = "Loading...";
					((Control)this.ErrorLabel).Refresh();
				}
				bool flag;
				if (count == 1)
				{
					string fileName = text;
					ProgressBar ProgBar = ProgressBar1;
					Label ErrorLabel = null;
					bool num5 = GlobalForm.LoadFile(fileName, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
					ProgressBar1 = ProgBar;
					flag = num5;
				}
				else
				{
					string fileName2 = text;
					ProgressBar ProgBar = null;
					Label ErrorLabel = null;
					flag = GlobalForm.LoadFile(fileName2, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this));
				}
				if (Operators.CompareString(this.ErrorLabel.Text, "Loading...", false) == 0)
				{
					this.ErrorLabel.Text = "Finding...";
					((Control)this.ErrorLabel).Refresh();
				}
				if (!flag)
				{
					if (GlobalForm.ErrorMessage != null)
					{
						Label ErrorLabel;
						(ErrorLabel = this.ErrorLabel).Text = ErrorLabel.Text + "\r\n" + GlobalForm.ErrorMessage;
					}
					if (count == 1)
					{
						ProgressBar1.Value = 50;
					}
					FindPatterns.EnterFindPatterns(GlobalForm.ChartStart, GlobalForm.ChartEnd, null, ref StopPressed, 0, text, ref iRow, (Control)(object)this);
					if ((GlobalForm.PatternCount > 0) | GlobalForm.FilterGlobals.CBPriceMoves | GlobalForm.FilterGlobals.CBHighVolume | GlobalForm.FilterGlobals.CBStages)
					{
						BuildGrid(text);
					}
					if (count == 1)
					{
						ProgressBar1.Value = 75;
					}
					if (StopPressed)
					{
						break;
					}
					ProgressBar1.Value = (int)Math.Round((double)(100 * j) / (double)MyProject.Forms.Mainform.ListBox1.SelectedIndices.Count);
				}
			}
			DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)6;
			DataGridView1.RowHeadersVisible = true;
			ProgressBar1.Value = 100;
			if (GlobalForm.Quiet)
			{
				return;
			}
			if (this.ErrorLabel.Text.Length > 0)
			{
				this.ErrorLabel.Text = this.ErrorLabel.Text + "\r\nNumerous errors could mean the quote file received a bad update. Go to the Update Form and update using 'Get historical quotes' option to make sure the file has good information.\r\n\r\n" + this.ErrorLabel.Text;
				try
				{
					Clipboard.SetText(this.ErrorLabel.Text);
					this.ErrorLabel.Text = "Error messages are on the clipboard.";
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					ProjectData.ClearProjectError();
				}
			}
			FilenameLabel.Text = DataGridView1.RowCount + " patterns found.";
		}
	}

	private void CandlesButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.CandlesForm).ShowDialog();
	}

	private void CandlesCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		GlobalForm.ShowCandles = CandlesCheckBox.Checked;
	}

	private void ClipboardButton_Click(object sender, EventArgs e)
	{
		//IL_017e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0204: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ed: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f3: Expected O, but got Unknown
		if (((BaseCollection)DataGridView1.SelectedRows).Count == 0)
		{
			DataGridView1.SelectAll();
		}
		DisableEnable(EnableFlag: false);
		StopPressed = false;
		((Control)StopButton).Focus();
		ErrorLabel.Text = "This could take a while. If needed, click Stop to cancel.";
		FilenameLabel.Text = "";
		((Control)this).Cursor = Cursors.WaitCursor;
		string text = "BREAKOUT DATE, PRICE: Only the approximate breakout date appears because it can be difficult with some patterns (such as those with sloping trendlines) to determine the exact breakout price or date.";
		text += "\r\nFILL PRICE: The price at which a trade would fill. This is either the opening price the day after price closes above/below the pattern or trendline boundary (day after a breakout), or the confirmation price.";
		text += "\r\nULTIMATE HIGH/LOW: The highest high/lowest low after which price drops/rises at least 20%. Consider this the perfect exit price. It's left blank if price hasn't moved by 20% yet.";
		text += "\r\nAPPROX TARGET: If a target, based on the measure rule (often the pattern's height added to/subtracted from the breakout price) can be determined, it is shown.";
		text += "\r\nVOLATILITY STOP: A stop based on how volatile a stock is, applied to the breakout price. This will be blank if no breakout has occurred.";
		text += "\r\nTRADE STATUS: A trade is assumed to be open if price has broken out. If price reaches the target or is stopped out, then the status reflects that.";
		text += "\r\nN/A means not applicable.";
		text += "\r\n";
		text += "\r\nFor more information on terms, read the glossary on ThePatternSite.com. Copyright (c) 2016-2024 by Thomas Bulkowski and ThePatternSite.com. All rights reserved.";
		text += "\r\n\r\n";
		foreach (DataGridViewColumn item in (BaseCollection)DataGridView1.Columns)
		{
			DataGridViewColumn val = item;
			text = text + val.HeaderText + "\t";
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
		FilenameLabel.Text = ((BaseCollection)DataGridView1.SelectedRows).Count + " patterns copied.";
		ErrorLabel.Text = "";
		MessageBox.Show("Done! " + ((BaseCollection)DataGridView1.SelectedRows).Count + " patterns copied.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		DisableEnable(EnableFlag: true);
	}

	private void DataGridView1_DoubleClick(object sender, EventArgs e)
	{
		if (((BaseCollection)DataGridView1.SelectedRows).Count > 0)
		{
			GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		}
	}

	private void DisableEnable(bool EnableFlag)
	{
		if (EnableFlag)
		{
			((Control)StrictCheckBox).Enabled = true;
			((Control)CandlesCheckBox).Enabled = true;
			((Control)PatternsCheckBox).Enabled = true;
			((Control)ToDatePicker).Enabled = true;
			((Control)FromDatePicker).Enabled = true;
			((Control)HelpButton1).Enabled = true;
			if (DataGridView1.RowCount > 0)
			{
				((Control)ClipboardButton).Enabled = true;
				((Control)GraphButton).Enabled = true;
			}
			else
			{
				((Control)ClipboardButton).Enabled = false;
				((Control)GraphButton).Enabled = false;
			}
			((Control)CandlesButton).Enabled = true;
			((Control)PatternsButton).Enabled = true;
			((Control)StopButton).Enabled = false;
			((Control)StartButton).Enabled = true;
			((Control)DoneButton).Enabled = true;
			((Control)ListAllPortfoliosButton).Enabled = true;
			if (GlobalForm.IntradayData)
			{
				GlobalForm.EnableDisableDWM(DailyRadioButton, WeeklyRadioButton, MonthlyRadioButton);
				return;
			}
			((Control)DailyRadioButton).Enabled = true;
			((Control)WeeklyRadioButton).Enabled = true;
			((Control)MonthlyRadioButton).Enabled = true;
		}
		else
		{
			((Control)DoneButton).Enabled = false;
			((Control)StartButton).Enabled = false;
			((Control)StopButton).Enabled = true;
			((Control)PatternsButton).Enabled = false;
			((Control)CandlesButton).Enabled = false;
			((Control)ClipboardButton).Enabled = false;
			((Control)HelpButton1).Enabled = false;
			((Control)GraphButton).Enabled = false;
			((Control)FromDatePicker).Enabled = false;
			((Control)ToDatePicker).Enabled = false;
			((Control)PatternsCheckBox).Enabled = false;
			((Control)CandlesCheckBox).Enabled = false;
			((Control)StrictCheckBox).Enabled = false;
			((Control)ListAllPortfoliosButton).Enabled = false;
			((Control)DailyRadioButton).Enabled = false;
			((Control)WeeklyRadioButton).Enabled = false;
			((Control)MonthlyRadioButton).Enabled = false;
		}
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void FiltersButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.FilterForm).ShowDialog();
	}

	private int FilterPatterns(int index, ref long iWidth, ref int iHeight)
	{
		int iStartDate = GlobalForm.ChartPatterns[index].iStartDate;
		int iEndDate = GlobalForm.ChartPatterns[index].iEndDate;
		iStartDate = Conversions.ToInteger(Interaction.IIf((iStartDate < GlobalForm.ChartPatterns[index].iStart2Date) | (GlobalForm.ChartPatterns[index].iStart2Date == 0), (object)iStartDate, (object)GlobalForm.ChartPatterns[index].iStart2Date));
		iEndDate = Conversions.ToInteger(Interaction.IIf(iEndDate > GlobalForm.ChartPatterns[index].iEnd2Date, (object)iEndDate, (object)GlobalForm.ChartPatterns[index].iEnd2Date));
		checked
		{
			if (GlobalForm.IntradayData)
			{
				iWidth = iEndDate - iStartDate + 1;
			}
			else
			{
				iWidth = 1 + DateAndTime.DateDiff((DateInterval)4, GlobalForm.nDT[0, iStartDate], GlobalForm.nDT[0, iEndDate], (FirstDayOfWeek)1, (FirstWeekOfYear)1);
			}
			int num = iStartDate;
			int num2 = iStartDate;
			int num3 = iStartDate + 1;
			int num4 = iEndDate;
			for (int i = num3; i <= num4; i++)
			{
				num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0, (object)i, (object)num));
				num2 = Conversions.ToInteger(Interaction.IIf((decimal.Compare(GlobalForm.nHLC[2, i], 0m) == 0) | (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num2]) < 0), (object)i, (object)num2));
			}
			string bkoutDirection = GlobalForm.CPInfo.BkoutDirection;
			iHeight = GlobalForm.CalcPatternHeight(BkoutDirection: (Operators.CompareString(bkoutDirection, "Up", false) == 0) ? 1 : ((Operators.CompareString(bkoutDirection, "Down", false) == 0) ? (-1) : 0), PatternType: GlobalForm.ChartPatterns[index].Type, PatternTop: GlobalForm.nHLC[1, num], PatternBottom: GlobalForm.nHLC[2, num2], iEnd: iEndDate);
			if (!GlobalForm.FilterGlobals.CBMasterSwitch)
			{
				return 2;
			}
			if (!GlobalForm.FilterGlobals.CBBkoutDirection & !GlobalForm.FilterGlobals.CBWidth & !GlobalForm.FilterGlobals.CBPrice & !GlobalForm.FilterGlobals.CBHeight & !GlobalForm.FilterGlobals.CBVolume)
			{
				return 2;
			}
		}
		if (GlobalForm.FilterGlobals.CBBkoutDirection)
		{
			bool flag = false;
			if (GlobalForm.FilterGlobals.CBBkoutIncludeNone && ((Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, (string)null, false) == 0) | (Operators.CompareString(Strings.Left(GlobalForm.CPInfo.BkoutDirection, 3), "N/A", false) == 0)))
			{
				flag = true;
			}
			switch (GlobalForm.FilterGlobals.BkoutDirRBOption)
			{
			case 0:
				if (!(Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0 || flag))
				{
					return 1;
				}
				break;
			case 1:
				if (!(Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Down", false) == 0 || flag))
				{
					return 1;
				}
				break;
			case 2:
				if (!(((Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Up", false) == 0) | (Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, "Down", false) == 0)) || flag))
				{
					return 1;
				}
				break;
			case 3:
				if (!((Operators.CompareString(GlobalForm.CPInfo.BkoutDirection, (string)null, false) == 0) | (Operators.CompareString(Strings.Left(GlobalForm.CPInfo.BkoutDirection, 3), "N/A", false) == 0)))
				{
					return 1;
				}
				break;
			}
		}
		if (GlobalForm.FilterGlobals.CBWidth)
		{
			if ((GlobalForm.FilterGlobals.WidthRBOption == 0) & (decimal.Compare(new decimal(iWidth), GlobalForm.FilterGlobals.NumericWidthLess) >= 0))
			{
				return 1;
			}
			if ((GlobalForm.FilterGlobals.WidthRBOption == 1) & ((decimal.Compare(new decimal(iWidth), GlobalForm.FilterGlobals.NumericWidthLow) <= 0) | (decimal.Compare(new decimal(((Control)this).Width), GlobalForm.FilterGlobals.NumericWidthHigh) >= 0)))
			{
				return 1;
			}
			if ((GlobalForm.FilterGlobals.WidthRBOption == 2) & (decimal.Compare(new decimal(iWidth), GlobalForm.FilterGlobals.NumericWidthMore) <= 0))
			{
				return 1;
			}
		}
		if (GlobalForm.FilterGlobals.CBPrice)
		{
			switch (GlobalForm.FilterGlobals.PriceRBOption)
			{
			case 0:
				if (decimal.Compare(GlobalForm.nHLC[3, iEndDate], GlobalForm.FilterGlobals.NumericPriceLess) >= 0)
				{
					return 1;
				}
				break;
			case 2:
				if (decimal.Compare(GlobalForm.nHLC[3, iEndDate], GlobalForm.FilterGlobals.NumericPriceMore) <= 0)
				{
					return 1;
				}
				break;
			case 1:
				if ((decimal.Compare(GlobalForm.nHLC[3, iEndDate], GlobalForm.FilterGlobals.NumericPriceLow) <= 0) | (decimal.Compare(GlobalForm.nHLC[3, iEndDate], GlobalForm.FilterGlobals.NumericPriceHigh) >= 0))
				{
					return 1;
				}
				break;
			}
		}
		if (GlobalForm.FilterGlobals.CBHeight)
		{
			switch (GlobalForm.FilterGlobals.HeightRBOption)
			{
			case 2:
				if ((iHeight != GlobalForm.cTall) & (iHeight != GlobalForm.ShortPat))
				{
					return 1;
				}
				break;
			case 0:
				if (iHeight != GlobalForm.cTall)
				{
					return 1;
				}
				break;
			case 1:
				if (iHeight != GlobalForm.ShortPat)
				{
					return 1;
				}
				break;
			}
		}
		if (GlobalForm.FilterGlobals.CBVolume && Convert.ToDouble(GlobalForm.FilterGlobals.NumericVolume) >= Conversions.ToDouble(Strings.Format((object)GlobalForm.CPInfo.AvgVolume, "")))
		{
			return 1;
		}
		return 3;
	}

	private void GraphButton_Click(object sender, EventArgs e)
	{
		//IL_0027: Unknown result type (might be due to invalid IL or missing references)
		if (((BaseCollection)DataGridView1.SelectedRows).Count == 0)
		{
			DataGridView1.SelectAll();
		}
		((Form)MyProject.Forms.ListChartForm).ShowDialog();
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.HelpListForm).ShowDialog();
	}

	private void ListAllPortfoliosButton_Click(object sender, EventArgs e)
	{
		//IL_017e: Unknown result type (might be due to invalid IL or missing references)
		StopPressed = false;
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
						ErrorLabel.Text = "Error messages are on the clipboard.";
					}
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					ProjectData.ClearProjectError();
				}
				FilenameLabel.Text = DataGridView1.RowCount + " patterns found.";
				MessageBox.Show("Done!" + DataGridView1.RowCount + " patterns found.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				ProgressBar1.Value = 0;
			}
			else
			{
				StartButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			}
		}
	}

	private void PatternsButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.PatternsForm).ShowDialog();
	}

	private void ProcessSymbol()
	{
		//IL_002c: Unknown result type (might be due to invalid IL or missing references)
		//IL_042a: Unknown result type (might be due to invalid IL or missing references)
		if (Regex.Split(Strings.Trim(SymbolTextBox.Text), " ").Length > 1)
		{
			MessageBox.Show("Only one symbol is allowed in the Symbol text box.", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)64);
			((Control)SymbolTextBox).Focus();
			return;
		}
		string text = Strings.Trim(SymbolTextBox.Text);
		if ((Operators.CompareString(Strings.Right(text, 4).ToUpper(), ".CSV", false) != 0) & (Operators.CompareString(Strings.Right(text, 4).ToUpper(), ".TXT", false) != 0))
		{
			string text2 = text + ".csv";
			if (!File.Exists(GlobalForm.OpenPath + "\\" + text2))
			{
				text2 = text + ".txt";
			}
			text = text2;
		}
		FilenameLabel.Text = text;
		((Control)FilenameLabel).Refresh();
		this.ErrorLabel.Text = "Loading...";
		((Control)this.ErrorLabel).Refresh();
		string fileName = text;
		ProgressBar ProgBar = null;
		Label ErrorLabel = null;
		checked
		{
			if (!GlobalForm.LoadFile(fileName, ref ProgBar, ref ErrorLabel, QuickExit: false, GlobalForm.GetOptions((Form)(object)this)))
			{
				GlobalForm.SetupDateIndexes(GlobalForm.ChartStart, GlobalForm.ChartEnd);
				ProgressBar1.Value = 25;
				if (PatternsCheckBox.Checked)
				{
					FindPatterns.EnterFindPatterns(GlobalForm.ChartStart, GlobalForm.ChartEnd, null, ref StopPressed, 0);
					if ((GlobalForm.PatternCount > 0) | GlobalForm.FilterGlobals.CBPriceMoves | GlobalForm.FilterGlobals.CBHighVolume | GlobalForm.FilterGlobals.CBStages)
					{
						DataGridView1.RowHeadersVisible = false;
						DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)1;
						BuildGrid(text);
						DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)6;
						DataGridView1.RowHeadersVisible = true;
					}
				}
				else
				{
					ProgressBar1.Value = 50;
					if (GlobalForm.FilterGlobals.CBMasterSwitch & GlobalForm.FilterGlobals.CBStages)
					{
						FindPatterns.FindWeinsteinStages(text, 0);
						int num = GlobalForm.WStages[GlobalForm.WStages.Length - 1];
						if (unchecked((GlobalForm.FilterGlobals.CBStage1 && num == 1) | (GlobalForm.FilterGlobals.CBStage2 && num == 2) | (GlobalForm.FilterGlobals.CBStage3 && num == 3) | (GlobalForm.FilterGlobals.CBStage4 && num == 4)))
						{
							DataGridView1.Rows.Add();
							DataGridView1.Rows[iRow].Cells[0].Value = text;
							DataGridView1.Rows[iRow].Cells[1].Value = GlobalForm.LimitDecimals(GlobalForm.nHLC[3, GlobalForm.HLCRange]);
							DataGridView1.Rows[iRow].Cells[2].Value = "Stage";
							DataGridView1.Rows[iRow].Cells[3].Value = FromDatePicker.Value;
							DataGridView1.Rows[iRow].Cells[4].Value = ToDatePicker.Value;
							DataGridView1.Rows[iRow].Cells[17].Value = num.ToString();
							DataGridView1.Rows[iRow].Cells[18].Value = "S";
							iRow++;
						}
					}
				}
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				if (!StopPressed && CandlesCheckBox.Checked)
				{
					if (GlobalForm.CandleCount > 0)
					{
						GlobalForm.CandlePatterns = null;
						GlobalForm.CandleCount = 0;
					}
					this.ErrorLabel.Text = "Finding...";
					((Control)this.ErrorLabel).Refresh();
					Control Ctrl = (Control)(object)this;
					FindCandles.GoFindCandles(ref Ctrl, text, ref iRow, 0, ProgressBar1, ref StopPressed);
				}
			}
			else
			{
				MessageBox.Show("Symbol in text box not found. Is it spelled correctly?", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)16);
			}
		}
	}

	private void StartButton_Click(object sender, EventArgs e)
	{
		//IL_014b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0124: Unknown result type (might be due to invalid IL or missing references)
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
		if (PatternsCheckBox.Checked | CandlesCheckBox.Checked | (GlobalForm.FilterGlobals.CBMasterSwitch & GlobalForm.FilterGlobals.CBStages & (GlobalForm.FilterGlobals.CBStage1 | GlobalForm.FilterGlobals.CBStage2 | GlobalForm.FilterGlobals.CBStage3 | GlobalForm.FilterGlobals.CBStage4)))
		{
			if (!GlobalForm.Quiet)
			{
				StopPressed = false;
			}
			DisableEnable(EnableFlag: false);
			GlobalForm.HideMessages = true;
			if (!GlobalForm.Quiet)
			{
				ErrorLabel.Text = "";
			}
			BuildList();
			GlobalForm.HideMessages = false;
			DisableEnable(EnableFlag: true);
			if (!GlobalForm.Quiet)
			{
				ProgressBar1.Value = 0;
				DataGridView1.SelectAll();
				MessageBox.Show("Done! " + DataGridView1.RowCount + " patterns found.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
		}
		else if (!GlobalForm.Quiet)
		{
			((Control)PatternsCheckBox).Focus();
			MessageBox.Show("Either the Patterns, Candles, (this form) or Stages (see Filters) must be checked.", "Listform: StartButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
	}

	private void StopButton_Click(object sender, EventArgs e)
	{
		StopPressed = true;
		Interaction.Beep();
	}

	private void StrictCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		if (!LockFlag)
		{
			GlobalForm.StrictPatterns = StrictCheckBox.Checked;
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
				GlobalForm.ChartPeriodShown = 0;
				break;
			case 1:
				GlobalForm.ChartPeriodShown = 1;
				break;
			case 2:
				GlobalForm.ChartPeriodShown = 2;
				break;
			}
		}
	}
}
