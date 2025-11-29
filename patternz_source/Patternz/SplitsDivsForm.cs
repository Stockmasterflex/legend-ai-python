using System;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Net;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Microsoft.VisualBasic.Devices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class SplitsDivsForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("PortfolioButton")]
	private Button _PortfolioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ClipboardButton")]
	private Button _ClipboardButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StopButton")]
	private Button _StopButton;

	[CompilerGenerated]
	[AccessedThroughProperty("BrowseButton")]
	private Button _BrowseButton;

	[CompilerGenerated]
	[AccessedThroughProperty("AllButton")]
	private Button _AllButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StartButton")]
	private Button _StartButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("TiingoHelpButton")]
	private Button _TiingoHelpButton;

	[CompilerGenerated]
	[AccessedThroughProperty("TiingoRadioButton")]
	private RadioButton _TiingoRadioButton;

	[CompilerGenerated]
	[AccessedThroughProperty("APIKeyTextBox")]
	private TextBox _APIKeyTextBox;

	private bool StopPressed;

	private string ErrorList;

	private int ErrorCount;

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

	[field: AccessedThroughProperty("SymbolLabel")]
	internal virtual Label SymbolLabel
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

	[field: AccessedThroughProperty("DataGridView1")]
	internal virtual DataGridView DataGridView1
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

	[field: AccessedThroughProperty("ErrorLabel")]
	internal virtual Label ErrorLabel
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

	internal virtual Button AllButton
	{
		[CompilerGenerated]
		get
		{
			return _AllButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = AllButton_Click;
			Button val = _AllButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_AllButton = value;
			val = _AllButton;
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

	[field: AccessedThroughProperty("ListBox1")]
	internal virtual ListBox ListBox1
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

	internal virtual Button TiingoHelpButton
	{
		[CompilerGenerated]
		get
		{
			return _TiingoHelpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = TiingoHelpButton_Click;
			Button val = _TiingoHelpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_TiingoHelpButton = value;
			val = _TiingoHelpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual RadioButton TiingoRadioButton
	{
		[CompilerGenerated]
		get
		{
			return _TiingoRadioButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = TiingoRadioButton_CheckedChanged;
			RadioButton val = _TiingoRadioButton;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_TiingoRadioButton = value;
			val = _TiingoRadioButton;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("QuandlHelpButton")]
	internal virtual Button QuandlHelpButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("QuandlRadioButton")]
	internal virtual RadioButton QuandlRadioButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("QuandlComboBox")]
	internal virtual ComboBox QuandlComboBox
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

	[field: AccessedThroughProperty("Label1")]
	internal virtual Label Label1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual TextBox APIKeyTextBox
	{
		[CompilerGenerated]
		get
		{
			return _APIKeyTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = APIKeyTextBox_LostFocus;
			TextBox val = _APIKeyTextBox;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
			}
			_APIKeyTextBox = value;
			val = _APIKeyTextBox;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
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

	[field: AccessedThroughProperty("FolderBrowserDialog1")]
	internal virtual FolderBrowserDialog FolderBrowserDialog1
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

	[field: AccessedThroughProperty("SplitsCheckBox")]
	internal virtual CheckBox SplitsCheckBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("DividendsCheckBox")]
	internal virtual CheckBox DividendsCheckBox
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

	[field: AccessedThroughProperty("Label10")]
	internal virtual Label Label10
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

	[field: AccessedThroughProperty("Label12")]
	internal virtual Label Label12
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label13")]
	internal virtual Label Label13
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label14")]
	internal virtual Label Label14
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public SplitsDivsForm()
	{
		((Form)this).Closing += SplitsDivsForm_Closing;
		((Form)this).Load += SplitsDivsForm_Load;
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
		//IL_011f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0129: Expected O, but got Unknown
		//IL_012a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0134: Expected O, but got Unknown
		//IL_0135: Unknown result type (might be due to invalid IL or missing references)
		//IL_013f: Expected O, but got Unknown
		//IL_0140: Unknown result type (might be due to invalid IL or missing references)
		//IL_014a: Expected O, but got Unknown
		//IL_014b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0155: Expected O, but got Unknown
		//IL_0156: Unknown result type (might be due to invalid IL or missing references)
		//IL_0160: Expected O, but got Unknown
		//IL_0161: Unknown result type (might be due to invalid IL or missing references)
		//IL_016b: Expected O, but got Unknown
		//IL_016c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0176: Expected O, but got Unknown
		//IL_0177: Unknown result type (might be due to invalid IL or missing references)
		//IL_0181: Expected O, but got Unknown
		//IL_0182: Unknown result type (might be due to invalid IL or missing references)
		//IL_018c: Expected O, but got Unknown
		//IL_018d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0197: Expected O, but got Unknown
		//IL_0198: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a2: Expected O, but got Unknown
		//IL_01a3: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ad: Expected O, but got Unknown
		//IL_01ae: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b8: Expected O, but got Unknown
		//IL_09c5: Unknown result type (might be due to invalid IL or missing references)
		//IL_09cf: Expected O, but got Unknown
		//IL_0aec: Unknown result type (might be due to invalid IL or missing references)
		//IL_0af6: Expected O, but got Unknown
		//IL_15ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_15b7: Expected O, but got Unknown
		PortfolioButton = new Button();
		ClipboardButton = new Button();
		SymbolLabel = new Label();
		ProgressBar1 = new ProgressBar();
		DataGridView1 = new DataGridView();
		StopButton = new Button();
		ErrorLabel = new Label();
		BrowseButton = new Button();
		AllButton = new Button();
		SymbolTextBox = new TextBox();
		StartButton = new Button();
		DoneButton = new Button();
		ListBox1 = new ListBox();
		GroupBox1 = new GroupBox();
		TiingoHelpButton = new Button();
		TiingoRadioButton = new RadioButton();
		QuandlHelpButton = new Button();
		QuandlRadioButton = new RadioButton();
		QuandlComboBox = new ComboBox();
		Label5 = new Label();
		Label1 = new Label();
		APIKeyTextBox = new TextBox();
		ToDatePicker = new DateTimePicker();
		FromDatePicker = new DateTimePicker();
		Label3 = new Label();
		Label2 = new Label();
		FolderBrowserDialog1 = new FolderBrowserDialog();
		GroupBox2 = new GroupBox();
		SplitsCheckBox = new CheckBox();
		DividendsCheckBox = new CheckBox();
		Label4 = new Label();
		Label6 = new Label();
		Label7 = new Label();
		Label8 = new Label();
		Label9 = new Label();
		Label10 = new Label();
		Label11 = new Label();
		Label12 = new Label();
		Label13 = new Label();
		Label14 = new Label();
		((ISupportInitialize)DataGridView1).BeginInit();
		((Control)GroupBox1).SuspendLayout();
		((Control)GroupBox2).SuspendLayout();
		((Control)this).SuspendLayout();
		((Control)PortfolioButton).Anchor = (AnchorStyles)10;
		((Control)PortfolioButton).CausesValidation = false;
		((Control)PortfolioButton).Enabled = false;
		((Control)PortfolioButton).Location = new Point(939, 401);
		((Control)PortfolioButton).Name = "PortfolioButton";
		((Control)PortfolioButton).Size = new Size(60, 23);
		((Control)PortfolioButton).TabIndex = 19;
		((ButtonBase)PortfolioButton).Text = "&Portfolio";
		((ButtonBase)PortfolioButton).UseVisualStyleBackColor = true;
		((Control)ClipboardButton).Anchor = (AnchorStyles)10;
		((Control)ClipboardButton).Enabled = false;
		((Control)ClipboardButton).Location = new Point(939, 459);
		((Control)ClipboardButton).Name = "ClipboardButton";
		((Control)ClipboardButton).Size = new Size(60, 23);
		((Control)ClipboardButton).TabIndex = 21;
		((ButtonBase)ClipboardButton).Text = "&Clipboard";
		((ButtonBase)ClipboardButton).UseVisualStyleBackColor = true;
		((Control)SymbolLabel).Anchor = (AnchorStyles)10;
		((Control)SymbolLabel).Location = new Point(691, 447);
		((Control)SymbolLabel).Name = "SymbolLabel";
		((Control)SymbolLabel).Size = new Size(166, 20);
		((Control)SymbolLabel).TabIndex = 7;
		SymbolLabel.Text = "&New symbol(s), space separated:";
		((Control)ProgressBar1).Anchor = (AnchorStyles)10;
		((Control)ProgressBar1).ForeColor = Color.Green;
		((Control)ProgressBar1).Location = new Point(673, 324);
		((Control)ProgressBar1).Name = "ProgressBar1";
		((Control)ProgressBar1).Size = new Size(325, 21);
		((Control)ProgressBar1).TabIndex = 4;
		DataGridView1.AllowUserToAddRows = false;
		DataGridView1.AllowUserToDeleteRows = false;
		DataGridView1.AllowUserToResizeColumns = false;
		DataGridView1.AllowUserToResizeRows = false;
		((Control)DataGridView1).Anchor = (AnchorStyles)14;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)10;
		DataGridView1.AutoSizeRowsMode = (DataGridViewAutoSizeRowsMode)11;
		((Control)DataGridView1).CausesValidation = false;
		DataGridView1.ColumnHeadersHeightSizeMode = (DataGridViewColumnHeadersHeightSizeMode)2;
		DataGridView1.EditMode = (DataGridViewEditMode)4;
		((Control)DataGridView1).Location = new Point(328, 324);
		((Control)DataGridView1).Name = "DataGridView1";
		DataGridView1.ReadOnly = true;
		DataGridView1.RowTemplate.ReadOnly = true;
		DataGridView1.RowTemplate.Resizable = (DataGridViewTriState)1;
		DataGridView1.SelectionMode = (DataGridViewSelectionMode)1;
		DataGridView1.ShowCellErrors = false;
		DataGridView1.ShowCellToolTips = false;
		DataGridView1.ShowEditingIcon = false;
		DataGridView1.ShowRowErrors = false;
		((Control)DataGridView1).Size = new Size(337, 282);
		((Control)DataGridView1).TabIndex = 3;
		((Control)StopButton).Anchor = (AnchorStyles)10;
		((Control)StopButton).Enabled = false;
		((Control)StopButton).Location = new Point(939, 488);
		((Control)StopButton).Name = "StopButton";
		((Control)StopButton).Size = new Size(60, 23);
		((Control)StopButton).TabIndex = 22;
		((ButtonBase)StopButton).Text = "St&op";
		((ButtonBase)StopButton).UseVisualStyleBackColor = true;
		((Control)ErrorLabel).Anchor = (AnchorStyles)10;
		ErrorLabel.BorderStyle = (BorderStyle)2;
		ErrorLabel.FlatStyle = (FlatStyle)0;
		((Control)ErrorLabel).ForeColor = Color.Black;
		((Control)ErrorLabel).Location = new Point(673, 581);
		((Control)ErrorLabel).Name = "ErrorLabel";
		((Control)ErrorLabel).Size = new Size(325, 25);
		((Control)ErrorLabel).TabIndex = 17;
		ErrorLabel.Text = "Information is believed to be correct but check with the company";
		ErrorLabel.TextAlign = (ContentAlignment)32;
		((Control)BrowseButton).Anchor = (AnchorStyles)10;
		((Control)BrowseButton).Location = new Point(939, 372);
		((Control)BrowseButton).Name = "BrowseButton";
		((Control)BrowseButton).Size = new Size(60, 23);
		((Control)BrowseButton).TabIndex = 18;
		((ButtonBase)BrowseButton).Text = "&Browse";
		((ButtonBase)BrowseButton).UseVisualStyleBackColor = true;
		((Control)AllButton).Anchor = (AnchorStyles)10;
		((Control)AllButton).Location = new Point(939, 430);
		((Control)AllButton).Name = "AllButton";
		((Control)AllButton).Size = new Size(60, 23);
		((Control)AllButton).TabIndex = 20;
		((ButtonBase)AllButton).Text = "&Select All";
		((ButtonBase)AllButton).UseVisualStyleBackColor = true;
		((Control)SymbolTextBox).Anchor = (AnchorStyles)10;
		((Control)SymbolTextBox).Location = new Point(864, 444);
		((Control)SymbolTextBox).Name = "SymbolTextBox";
		((Control)SymbolTextBox).Size = new Size(60, 20);
		((Control)SymbolTextBox).TabIndex = 8;
		((Control)StartButton).Anchor = (AnchorStyles)10;
		((Control)StartButton).Location = new Point(939, 517);
		((Control)StartButton).Name = "StartButton";
		((Control)StartButton).Size = new Size(60, 23);
		((Control)StartButton).TabIndex = 0;
		((ButtonBase)StartButton).Text = "S&tart";
		((ButtonBase)StartButton).UseVisualStyleBackColor = true;
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(939, 546);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(60, 23);
		((Control)DoneButton).TabIndex = 1;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)ListBox1).Anchor = (AnchorStyles)15;
		ListBox1.HorizontalScrollbar = true;
		((Control)ListBox1).Location = new Point(328, 0);
		ListBox1.MultiColumn = true;
		((Control)ListBox1).Name = "ListBox1";
		ListBox1.SelectionMode = (SelectionMode)3;
		((Control)ListBox1).Size = new Size(671, 303);
		ListBox1.Sorted = true;
		((Control)ListBox1).TabIndex = 2;
		((Control)GroupBox1).Anchor = (AnchorStyles)10;
		((Control)GroupBox1).CausesValidation = false;
		((Control)GroupBox1).Controls.Add((Control)(object)TiingoHelpButton);
		((Control)GroupBox1).Controls.Add((Control)(object)TiingoRadioButton);
		((Control)GroupBox1).Controls.Add((Control)(object)QuandlHelpButton);
		((Control)GroupBox1).Controls.Add((Control)(object)QuandlRadioButton);
		((Control)GroupBox1).Location = new Point(693, 369);
		((Control)GroupBox1).Name = "GroupBox1";
		((Control)GroupBox1).Size = new Size(107, 71);
		((Control)GroupBox1).TabIndex = 5;
		GroupBox1.TabStop = false;
		GroupBox1.Text = "Quote Provider";
		((Control)TiingoHelpButton).Anchor = (AnchorStyles)10;
		((Control)TiingoHelpButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)TiingoHelpButton).Location = new Point(78, 22);
		((Control)TiingoHelpButton).Name = "TiingoHelpButton";
		((Control)TiingoHelpButton).Size = new Size(20, 20);
		((Control)TiingoHelpButton).TabIndex = 1;
		((ButtonBase)TiingoHelpButton).Text = "?";
		((ButtonBase)TiingoHelpButton).UseVisualStyleBackColor = true;
		((Control)TiingoRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)TiingoRadioButton).AutoSize = true;
		TiingoRadioButton.Checked = true;
		((Control)TiingoRadioButton).Location = new Point(13, 22);
		((Control)TiingoRadioButton).Name = "TiingoRadioButton";
		((Control)TiingoRadioButton).Size = new Size(54, 17);
		((Control)TiingoRadioButton).TabIndex = 0;
		TiingoRadioButton.TabStop = true;
		((ButtonBase)TiingoRadioButton).Text = "&Tiingo";
		((ButtonBase)TiingoRadioButton).UseVisualStyleBackColor = true;
		((Control)QuandlHelpButton).Anchor = (AnchorStyles)10;
		((Control)QuandlHelpButton).Enabled = false;
		((Control)QuandlHelpButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)QuandlHelpButton).Location = new Point(78, 45);
		((Control)QuandlHelpButton).Name = "QuandlHelpButton";
		((Control)QuandlHelpButton).Size = new Size(20, 20);
		((Control)QuandlHelpButton).TabIndex = 3;
		((ButtonBase)QuandlHelpButton).Text = "?";
		((ButtonBase)QuandlHelpButton).UseVisualStyleBackColor = true;
		((Control)QuandlHelpButton).Visible = false;
		((Control)QuandlRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)QuandlRadioButton).AutoSize = true;
		((Control)QuandlRadioButton).Enabled = false;
		((Control)QuandlRadioButton).Location = new Point(13, 48);
		((Control)QuandlRadioButton).Name = "QuandlRadioButton";
		((Control)QuandlRadioButton).Size = new Size(59, 17);
		((Control)QuandlRadioButton).TabIndex = 2;
		((ButtonBase)QuandlRadioButton).Text = "&Quandl";
		((ButtonBase)QuandlRadioButton).UseVisualStyleBackColor = true;
		((Control)QuandlRadioButton).Visible = false;
		((Control)QuandlComboBox).Anchor = (AnchorStyles)10;
		((Control)QuandlComboBox).Enabled = false;
		((ListControl)QuandlComboBox).FormattingEnabled = true;
		((Control)QuandlComboBox).Location = new Point(759, 470);
		((Control)QuandlComboBox).Name = "QuandlComboBox";
		((Control)QuandlComboBox).Size = new Size(165, 21);
		QuandlComboBox.Sorted = true;
		((Control)QuandlComboBox).TabIndex = 10;
		((Control)QuandlComboBox).Visible = false;
		((Control)Label5).Anchor = (AnchorStyles)10;
		Label5.AutoSize = true;
		((Control)Label5).Enabled = false;
		((Control)Label5).Location = new Point(691, 473);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(62, 13);
		((Control)Label5).TabIndex = 9;
		Label5.Text = "&Quandl DB:";
		Label5.TextAlign = (ContentAlignment)32;
		((Control)Label5).Visible = false;
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(669, 497);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(84, 13);
		((Control)Label1).TabIndex = 11;
		Label1.Text = "&API Key/Token:";
		((Control)APIKeyTextBox).Anchor = (AnchorStyles)10;
		((Control)APIKeyTextBox).Location = new Point(759, 494);
		((TextBoxBase)APIKeyTextBox).MaxLength = 100;
		((Control)APIKeyTextBox).Name = "APIKeyTextBox";
		((Control)APIKeyTextBox).Size = new Size(165, 20);
		((Control)APIKeyTextBox).TabIndex = 12;
		((TextBoxBase)APIKeyTextBox).WordWrap = false;
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(761, 545);
		((Control)ToDatePicker).Name = "ToDatePicker";
		((Control)ToDatePicker).Size = new Size(91, 20);
		((Control)ToDatePicker).TabIndex = 16;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(761, 519);
		((Control)FromDatePicker).Name = "FromDatePicker";
		((Control)FromDatePicker).Size = new Size(91, 20);
		((Control)FromDatePicker).TabIndex = 14;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)Label3).Anchor = (AnchorStyles)10;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(732, 546);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(23, 13);
		((Control)Label3).TabIndex = 15;
		Label3.Text = "&To:";
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(722, 523);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(33, 13);
		((Control)Label2).TabIndex = 13;
		Label2.Text = "&From:";
		((Control)GroupBox2).Anchor = (AnchorStyles)10;
		((Control)GroupBox2).CausesValidation = false;
		((Control)GroupBox2).Controls.Add((Control)(object)SplitsCheckBox);
		((Control)GroupBox2).Controls.Add((Control)(object)DividendsCheckBox);
		((Control)GroupBox2).Location = new Point(827, 369);
		((Control)GroupBox2).Name = "GroupBox2";
		((Control)GroupBox2).Size = new Size(96, 71);
		((Control)GroupBox2).TabIndex = 6;
		GroupBox2.TabStop = false;
		((ButtonBase)SplitsCheckBox).AutoSize = true;
		((Control)SplitsCheckBox).Location = new Point(10, 39);
		((Control)SplitsCheckBox).Name = "SplitsCheckBox";
		((Control)SplitsCheckBox).Size = new Size(51, 17);
		((Control)SplitsCheckBox).TabIndex = 1;
		((ButtonBase)SplitsCheckBox).Text = "Splits";
		((ButtonBase)SplitsCheckBox).UseVisualStyleBackColor = true;
		((ButtonBase)DividendsCheckBox).AutoSize = true;
		((Control)DividendsCheckBox).Location = new Point(10, 16);
		((Control)DividendsCheckBox).Name = "DividendsCheckBox";
		((Control)DividendsCheckBox).Size = new Size(73, 17);
		((Control)DividendsCheckBox).TabIndex = 0;
		((ButtonBase)DividendsCheckBox).Text = "Dividends";
		((ButtonBase)DividendsCheckBox).UseVisualStyleBackColor = true;
		((Control)Label4).Anchor = (AnchorStyles)6;
		((Control)Label4).Location = new Point(12, 33);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(292, 31);
		((Control)Label4).TabIndex = 23;
		Label4.Text = "This form shows stock splits and cash dividends. Most of the controls are self-explanatory.";
		Label4.TextAlign = (ContentAlignment)16;
		((Control)Label6).Anchor = (AnchorStyles)6;
		((Control)Label6).Location = new Point(12, 80);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(292, 31);
		((Control)Label6).TabIndex = 24;
		Label6.Text = "1. Select a stock symbol from the top list box or enter one in the 'New symbol(s), space separated' text box.";
		Label6.TextAlign = (ContentAlignment)16;
		((Control)Label7).Anchor = (AnchorStyles)6;
		((Control)Label7).Location = new Point(12, 218);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(292, 31);
		((Control)Label7).TabIndex = 27;
		Label7.Text = "4. Adjust the dates for the period you wish to study.";
		Label7.TextAlign = (ContentAlignment)16;
		((Control)Label8).Anchor = (AnchorStyles)6;
		((Control)Label8).Location = new Point(12, 266);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(292, 31);
		((Control)Label8).TabIndex = 28;
		Label8.Text = "5. Click Start to begin gathering information or Stop to stop the process.";
		Label8.TextAlign = (ContentAlignment)16;
		((Control)Label9).Anchor = (AnchorStyles)6;
		((Control)Label9).Location = new Point(12, 178);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(292, 31);
		((Control)Label9).TabIndex = 26;
		Label9.Text = "3. Check Dividends and/or Splits check boxes.";
		Label9.TextAlign = (ContentAlignment)16;
		((Control)Label10).Anchor = (AnchorStyles)6;
		((Control)Label10).Location = new Point(12, 129);
		((Control)Label10).Name = "Label10";
		((Control)Label10).Size = new Size(292, 31);
		((Control)Label10).TabIndex = 25;
		Label10.Text = "2. Select a quote provider (and key/token, if necessary).";
		Label10.TextAlign = (ContentAlignment)16;
		((Control)Label11).Anchor = (AnchorStyles)6;
		((Control)Label11).Location = new Point(12, 314);
		((Control)Label11).Name = "Label11";
		((Control)Label11).Size = new Size(292, 31);
		((Control)Label11).TabIndex = 29;
		Label11.Text = "6. After the process ends, highlight cells in the grid and click Clipboard to copy them to the clipboard if you wish.";
		Label11.TextAlign = (ContentAlignment)16;
		((Control)Label12).Anchor = (AnchorStyles)6;
		((Control)Label12).Location = new Point(12, 519);
		((Control)Label12).Name = "Label12";
		((Control)Label12).Size = new Size(292, 66);
		((Control)Label12).TabIndex = 32;
		Label12.Text = "WARNING: I have seen incorrect information displayed occasionally (such as two stock splits happening within a week), so be sure to verify the results with the associated company. ";
		Label12.TextAlign = (ContentAlignment)16;
		((Control)Label13).Anchor = (AnchorStyles)6;
		((Control)Label13).Location = new Point(12, 444);
		((Control)Label13).Name = "Label13";
		((Control)Label13).Size = new Size(292, 31);
		((Control)Label13).TabIndex = 31;
		Label13.Text = "The Browse and Portolio buttons allow you to select symbols from other locations (portfolios).";
		Label13.TextAlign = (ContentAlignment)16;
		((Control)Label14).Anchor = (AnchorStyles)6;
		((Control)Label14).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label14).Location = new Point(12, 364);
		((Control)Label14).Name = "Label14";
		((Control)Label14).Size = new Size(292, 58);
		((Control)Label14).TabIndex = 30;
		Label14.Text = "NOTE: If you select any grid rows, that information will be sent to the Fix Split Form after clicking Done.";
		Label14.TextAlign = (ContentAlignment)16;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(1016, 612);
		((Control)this).Controls.Add((Control)(object)Label14);
		((Control)this).Controls.Add((Control)(object)Label13);
		((Control)this).Controls.Add((Control)(object)Label12);
		((Control)this).Controls.Add((Control)(object)Label11);
		((Control)this).Controls.Add((Control)(object)Label8);
		((Control)this).Controls.Add((Control)(object)Label9);
		((Control)this).Controls.Add((Control)(object)Label10);
		((Control)this).Controls.Add((Control)(object)Label7);
		((Control)this).Controls.Add((Control)(object)Label6);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)GroupBox2);
		((Control)this).Controls.Add((Control)(object)ToDatePicker);
		((Control)this).Controls.Add((Control)(object)FromDatePicker);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)QuandlComboBox);
		((Control)this).Controls.Add((Control)(object)Label5);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)APIKeyTextBox);
		((Control)this).Controls.Add((Control)(object)GroupBox1);
		((Control)this).Controls.Add((Control)(object)PortfolioButton);
		((Control)this).Controls.Add((Control)(object)ClipboardButton);
		((Control)this).Controls.Add((Control)(object)SymbolLabel);
		((Control)this).Controls.Add((Control)(object)ProgressBar1);
		((Control)this).Controls.Add((Control)(object)DataGridView1);
		((Control)this).Controls.Add((Control)(object)StopButton);
		((Control)this).Controls.Add((Control)(object)ErrorLabel);
		((Control)this).Controls.Add((Control)(object)BrowseButton);
		((Control)this).Controls.Add((Control)(object)AllButton);
		((Control)this).Controls.Add((Control)(object)SymbolTextBox);
		((Control)this).Controls.Add((Control)(object)StartButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)ListBox1);
		((Control)this).Name = "SplitsDivsForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Splits and Dividends Form";
		((ISupportInitialize)DataGridView1).EndInit();
		((Control)GroupBox1).ResumeLayout(false);
		((Control)GroupBox1).PerformLayout();
		((Control)GroupBox2).ResumeLayout(false);
		((Control)GroupBox2).PerformLayout();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void SplitsDivsForm_Closing(object sender, CancelEventArgs e)
	{
		checked
		{
			if (((BaseCollection)DataGridView1.SelectedRows).Count > 0)
			{
				GlobalForm.SplitArray = null;
				GlobalForm.SplitArray = new GlobalForm.SplitsInfoArray[((BaseCollection)DataGridView1.SelectedRows).Count + 1];
				int num = 0;
				for (int i = ((BaseCollection)DataGridView1.SelectedRows).Count - 1; i >= 0; i += -1)
				{
					try
					{
						if (DataGridView1.SelectedRows[i].Cells[3].Value != null)
						{
							GlobalForm.SplitArray[num].SplitRatio = DataGridView1.SelectedRows[i].Cells[3].Value.ToString();
							GlobalForm.SplitArray[num].SplitDate = Conversions.ToDate(DataGridView1.SelectedRows[i].Cells[1].Value).Date;
							GlobalForm.SplitArray[num].Symbol = DataGridView1.SelectedRows[i].Cells[0].Value.ToString();
							num++;
						}
					}
					catch (Exception ex)
					{
						ProjectData.SetProjectError(ex);
						Exception ex2 = ex;
						ProjectData.ClearProjectError();
					}
				}
				if (num > 0)
				{
					GlobalForm.SplitArray = (GlobalForm.SplitsInfoArray[])Utils.CopyArray((Array)GlobalForm.SplitArray, (Array)new GlobalForm.SplitsInfoArray[num - 1 + 1]);
				}
			}
			bool flag = true;
			GlobalForm.SDFUpdateSource = 4;
			GlobalForm.Splits = SplitsCheckBox.Checked;
			GlobalForm.Dividends = DividendsCheckBox.Checked;
			GlobalForm.SDFDateLookBack = Math.Abs((int)DateAndTime.DateDiff((DateInterval)4, FromDatePicker.Value, ToDatePicker.Value, (FirstDayOfWeek)1, (FirstWeekOfYear)1));
			if (Operators.CompareString(GlobalForm.lsTiingoKey, GlobalForm.TiingoKey, false) != 0)
			{
				string text = new GlobalForm.Simple3Des("da9ba2681").EncryptData(GlobalForm.TiingoKey);
				try
				{
					((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "Captoff", (object)text);
				}
				catch (Exception ex3)
				{
					ProjectData.SetProjectError(ex3);
					Exception ex4 = ex3;
					ProjectData.ClearProjectError();
				}
			}
			MySettingsProperty.Settings.SplitsLocation = ((Form)this).Location;
			MySettingsProperty.Settings.SplitsSize = ((Form)this).Size;
			((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
		}
	}

	private void SplitsDivsForm_Load(object sender, EventArgs e)
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
		//IL_00f1: Unknown result type (might be due to invalid IL or missing references)
		//IL_0102: Unknown result type (might be due to invalid IL or missing references)
		//IL_0113: Unknown result type (might be due to invalid IL or missing references)
		//IL_0124: Unknown result type (might be due to invalid IL or missing references)
		//IL_0135: Unknown result type (might be due to invalid IL or missing references)
		//IL_0146: Unknown result type (might be due to invalid IL or missing references)
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.SplitsLocation, MySettingsProperty.Settings.SplitsSize);
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)AllButton, "Select all of the symbols listed.");
		val.SetToolTip((Control)(object)APIKeyTextBox, "Provide the API key/token assigned when you registered with the quote provider.");
		val.SetToolTip((Control)(object)BrowseButton, "Locate files containing stock quotes for use by Patternz.");
		val.SetToolTip((Control)(object)ClipboardButton, "Copy highlighted rows to the clipboard.");
		val.SetToolTip((Control)(object)DataGridView1, "Results are displayed here.");
		val.SetToolTip((Control)(object)DividendsCheckBox, "Check to show dividends (if any).");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)FromDatePicker, "Enter the starting date for getting information.");
		val.SetToolTip((Control)(object)ListBox1, "Quote files appear here, if any.");
		val.SetToolTip((Control)(object)PortfolioButton, "Select a portfolio to analyze.");
		val.SetToolTip((Control)(object)SplitsCheckBox, "Check to show stock splits (if any).");
		val.SetToolTip((Control)(object)StartButton, "Begin analyzing quote files.");
		val.SetToolTip((Control)(object)StopButton, "Halt the analysis.");
		val.SetToolTip((Control)(object)SymbolTextBox, "Enter new symbol(s) to analyze, each separated by a comma, then click Start.");
		val.SetToolTip((Control)(object)TiingoHelpButton, "Provides more information about Tiingo.com quote service.");
		val.SetToolTip((Control)(object)TiingoRadioButton, "Select to get information from Tiingo.com.");
		val.SetToolTip((Control)(object)ToDatePicker, "Enter the ending date for getting information.");
		SymbolTextBox.Text = "";
		ListBox ListBox = ListBox1;
		GlobalForm.DisplayFiles(ref ListBox);
		ListBox1 = ListBox;
		ProgressBar1.Value = 0;
		SplitsCheckBox.Checked = GlobalForm.Splits;
		DividendsCheckBox.Checked = GlobalForm.Dividends;
		ErrorLabel.Text = "Information is believed to be correct but check with the company.";
		StopPressed = false;
		FromDatePicker.Value = DateAndTime.DateAdd((DateInterval)4, (double)checked(-1 * GlobalForm.SDFDateLookBack), DateAndTime.Now);
		ToDatePicker.Value = DateAndTime.Now;
		try
		{
			string text = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "Captoff", (object)""));
			if (Operators.CompareString(text, "", false) != 0)
			{
				GlobalForm.TiingoKey = new GlobalForm.Simple3Des("da9ba2681").DecryptData(text);
			}
			else
			{
				GlobalForm.TiingoKey = "";
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		GlobalForm.lsTiingoKey = GlobalForm.TiingoKey;
		int sDFUpdateSource = GlobalForm.SDFUpdateSource;
		TiingoRadioButton.Checked = true;
		APIKeyTextBox.Text = GlobalForm.TiingoKey;
		((Control)AllButton).Enabled = Conversions.ToBoolean(Interaction.IIf(ListBox1.Items.Count > 0, (object)true, (object)false));
		((Control)PortfolioButton).Enabled = true;
		BuildGridHeader();
	}

	private void AllButton_Click(object sender, EventArgs e)
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

	private void APIKeyTextBox_LostFocus(object sender, EventArgs e)
	{
		GlobalForm.TiingoKey = APIKeyTextBox.Text;
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
			((Control)AllButton).Enabled = Conversions.ToBoolean(Interaction.IIf(ListBox1.Items.Count > 0, (object)true, (object)false));
		}
		ErrorLabel.Text = "File location: " + GlobalForm.OpenPath;
	}

	private void BuildGridHeader()
	{
		DataGridView1.RowCount = 0;
		DataGridView1.ColumnCount = 4;
		DataGridView1.Columns[0].Name = "Symbol";
		DataGridView1.Columns[1].Name = "Date";
		DataGridView1.Columns[2].Name = "Dividend";
		DataGridView1.Columns["Dividend"].DefaultCellStyle.Alignment = (DataGridViewContentAlignment)64;
		DataGridView1.Columns[3].Name = "Split Ratio";
		DataGridView1.Columns["Split Ratio"].DefaultCellStyle.Alignment = (DataGridViewContentAlignment)64;
	}

	private void ClipboardButton_Click(object sender, EventArgs e)
	{
		//IL_0125: Unknown result type (might be due to invalid IL or missing references)
		//IL_013f: Unknown result type (might be due to invalid IL or missing references)
		//IL_003d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0043: Expected O, but got Unknown
		string text = "";
		if (((BaseCollection)DataGridView1.SelectedRows).Count == 0)
		{
			DataGridView1.SelectAll();
		}
		foreach (DataGridViewColumn item in (BaseCollection)DataGridView1.Columns)
		{
			DataGridViewColumn val = item;
			text = text + val.Name + "\t";
		}
		text += "\r\n";
		checked
		{
			for (int i = ((BaseCollection)DataGridView1.SelectedRows).Count - 1; i >= 0; i += -1)
			{
				int num = DataGridView1.ColumnCount - 1;
				for (int j = 0; j <= num; j++)
				{
					text = text + Conversions.ToString(DataGridView1.SelectedRows[i].Cells[j].Value) + "\t";
				}
				text += "\r\n";
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
			MessageBox.Show("Done!", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	public void GetAnalylitics(string[] SymbolArray)
	{
		//IL_00fb: Unknown result type (might be due to invalid IL or missing references)
		string text = "";
		try
		{
			DateTime value = FromDatePicker.Value;
			text = "&startDate=" + Strings.Format((object)value, "yyyy") + "-" + Strings.Format((object)value, "MM") + "-" + Strings.Format((object)value, "dd");
			value = ToDatePicker.Value;
			text = text + "&endDate=" + Strings.Format((object)value, "yyyy") + "-" + Strings.Format((object)value, "MM") + "-" + Strings.Format((object)value, "dd");
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			MessageBox.Show("Check the format Of the 'from' and 'to' fields.", "GetHistoricalQuotes", (MessageBoxButtons)0, (MessageBoxIcon)16);
			ProjectData.ClearProjectError();
			return;
		}
		int num = 0;
		int iRow = 0;
		ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
		checked
		{
			do
			{
				string original = SymbolArray[num];
				original = GlobalForm.Swap("_", ":", original);
				string text2 = null;
				StreamReader streamReader = null;
				Stream stream = null;
				WebResponse webResponse = null;
				try
				{
					webResponse = WebRequest.CreateHttp(GlobalForm.TIINGOURL + original + "/prices?token=" + APIKeyTextBox.Text + "&format=csv" + text).GetResponse();
					stream = webResponse.GetResponseStream();
					streamReader = new StreamReader(stream);
					text2 = streamReader.ReadToEnd();
					streamReader.Close();
					streamReader = null;
					stream.Close();
					stream = null;
					webResponse.Close();
					webResponse = null;
					ParseBuffer(text2, ref iRow, original);
				}
				catch (Exception ex3)
				{
					ProjectData.SetProjectError(ex3);
					Exception ex4 = ex3;
					HandleInternetException(ex4, original);
					streamReader?.Close();
					stream?.Close();
					webResponse?.Close();
					ProjectData.ClearProjectError();
				}
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				ProgressBar1.Value = (int)Math.Round((double)(100 * num) / (double)SymbolArray.Length);
				num++;
			}
			while (!((num == SymbolArray.Length) | StopPressed));
		}
	}

	private string GetEOLCode(string Buffer, string Symbol)
	{
		string text = "\r\n";
		while (true)
		{
			if (Strings.InStr(Buffer, text, (CompareMethod)0) != 0)
			{
				return text;
			}
			if (Operators.CompareString(text, "\r\n", false) == 0)
			{
				text = "\n";
				continue;
			}
			if (Operators.CompareString(text, "\n", false) != 0)
			{
				break;
			}
			text = "\r";
		}
		return null;
	}

	private string GetSplitPhrase(decimal Split)
	{
		int num = 1;
		checked
		{
			do
			{
				int num2 = 1;
				do
				{
					if (decimal.Compare(GlobalForm.LimitDecimals(new decimal((double)num2 / (double)num)), GlobalForm.LimitDecimals(Split)) == 0)
					{
						return num2 + ":" + num;
					}
					num2++;
				}
				while (num2 <= 256);
				num++;
			}
			while (num <= 256);
			return Split.ToString();
		}
	}

	private void HandleInternetException(Exception ex, string Symbol)
	{
		string text = "The remote name could not be resolved";
		if (Strings.InStr(ex.Message, "404", (CompareMethod)0) != 0)
		{
			ErrorLabel.Text = "Bad symbol? Quotes not available yet? " + Symbol;
		}
		else if (Strings.InStr(ex.Message, "400", (CompareMethod)0) != 0)
		{
			ErrorLabel.Text = "Bad symbol? " + Symbol;
		}
		else if (Operators.CompareString(Strings.Left(ex.Message, text.Length), text, false) == 0)
		{
			ErrorLabel.Text = "No internet connection. Is security software blocking access?";
		}
		else
		{
			ErrorLabel.Text = ex.Message;
		}
		ref string errorList = ref ErrorList;
		errorList = errorList + ErrorLabel.Text + "\r\n";
		checked
		{
			ErrorCount++;
		}
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_0005: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("This form shows stock splits and dividends.\r\n\r\nMost of the controls are self-explanatory. 1. Select a stock symbol from the top list box or enter one in the 'New symbols' text box.\r\n2. Adjust the dates.\r\n3. Select a quote provider (and a token, if necessary), check Dividends or Splits check boxes, then click Start.");
	}

	private void ParseBuffer(string Buffer, ref int iRow, string Symbol)
	{
		string text = "";
		int[] array = new int[10];
		string text2 = "";
		_ = DateTime.MinValue;
		_ = DateTime.MinValue;
		DataGridView1.RowHeadersVisible = false;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)1;
		Buffer = Buffer.Replace("\n", "\r\n");
		string eOLCode = GetEOLCode(Buffer, Symbol);
		if (Operators.CompareString(eOLCode, (string)null, false) == 0)
		{
			return;
		}
		int num = Strings.InStr(Buffer, eOLCode, (CompareMethod)0);
		checked
		{
			string text3 = Strings.Left(Buffer, num - (eOLCode.Length - 1));
			string text4 = GlobalForm.ClosestDelimiter(text3);
			if (Operators.CompareString(text4, "-1", false) == 0)
			{
				return;
			}
			if (Strings.InStr(Strings.UCase(text3), "DATE", (CompareMethod)0) != 0)
			{
				text = Strings.Right(Buffer, Strings.Len(Buffer) - (num + 1));
			}
			if (text.Length == 0)
			{
				return;
			}
			string[] array2 = Regex.Split(text3, text4);
			int num2 = 0;
			string[] array3 = array2;
			for (int i = 0; i < array3.Length; i++)
			{
				switch (Strings.UCase(array3[i]))
				{
				case "DATE":
					array[0] = num2;
					break;
				case "DIVCASH":
				case "EX-DIVIDEND":
					array[8] = num2;
					break;
				case "SPLITFACTOR":
				case "SPLIT RATIO":
					array[9] = num2;
					break;
				}
				num2++;
			}
			num = Strings.InStr(Buffer, "\r\n", (CompareMethod)0) + "\r\n".Length;
			int num3 = num;
			while (true)
			{
				try
				{
					if (num3 >= Buffer.Length)
					{
						break;
					}
					text2 = Strings.Right(Buffer, Buffer.Length - (num3 - 1));
					if (text2.Length == 0)
					{
						break;
					}
					num = Strings.InStr(text2, "\r\n", (CompareMethod)0) + "\r\n".Length;
					if (num <= "\r\n".Length)
					{
						break;
					}
					text2 = Strings.Mid(text2, 1, num - "\r\n".Length - 1);
					if (Strings.InStr(text2, "null", (CompareMethod)0) == 0)
					{
						string[] array4 = Regex.Split(text2, text4);
						string value = Strings.Format((object)GlobalForm.MyCDate(array4[array[0]]), "yyyy-MM-dd");
						decimal num4 = Conversions.ToDecimal(array4[array[8]]);
						decimal num5 = Conversions.ToDecimal(array4[array[9]]);
						if (SplitsCheckBox.Checked & DividendsCheckBox.Checked)
						{
							if ((decimal.Compare(num5, 1m) != 0) | (decimal.Compare(num4, 0m) != 0))
							{
								DataGridView1.Rows.Add();
								DataGridView1.Rows[iRow].Cells[0].Value = Symbol;
								DataGridView1.Rows[iRow].Cells[1].Value = value;
								if (decimal.Compare(num4, 0m) != 0)
								{
									DataGridView1.Rows[iRow].Cells[2].Value = num4;
								}
								if (decimal.Compare(num5, 1m) != 0)
								{
									DataGridView1.Rows[iRow].Cells[3].Value = GetSplitPhrase(num5);
								}
								iRow++;
							}
						}
						else if (DividendsCheckBox.Checked)
						{
							if (decimal.Compare(num4, 0m) != 0)
							{
								DataGridView1.Rows.Add();
								DataGridView1.Rows[iRow].Cells[0].Value = Symbol;
								DataGridView1.Rows[iRow].Cells[1].Value = value;
								DataGridView1.Rows[iRow].Cells[2].Value = num4;
								iRow++;
							}
						}
						else if (SplitsCheckBox.Checked && decimal.Compare(num5, 1m) != 0)
						{
							DataGridView1.Rows.Add();
							DataGridView1.Rows[iRow].Cells[0].Value = Symbol;
							DataGridView1.Rows[iRow].Cells[1].Value = value;
							DataGridView1.Rows[iRow].Cells[3].Value = GetSplitPhrase(num5);
							iRow++;
						}
					}
					num3 += num - 1;
					goto IL_04c7;
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					num3 += num - 1;
					ProjectData.ClearProjectError();
					goto IL_04c7;
				}
				IL_04c7:
				if (unchecked(iRow % 50) == 0)
				{
					((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
					if (StopPressed)
					{
						break;
					}
				}
			}
			DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)6;
			DataGridView1.RowHeadersVisible = true;
		}
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
			ListBox ListBox = ListBox1;
			GlobalForm.DisplayFiles(ref ListBox);
			ListBox1 = ListBox;
		}
	}

	private void StartButton_Click(object sender, EventArgs e)
	{
		//IL_04c2: Unknown result type (might be due to invalid IL or missing references)
		//IL_0050: Unknown result type (might be due to invalid IL or missing references)
		//IL_0056: Invalid comparison between Unknown and I4
		//IL_0091: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e5: Unknown result type (might be due to invalid IL or missing references)
		//IL_013b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0141: Invalid comparison between Unknown and I4
		//IL_04dc: Unknown result type (might be due to invalid IL or missing references)
		//IL_0499: Unknown result type (might be due to invalid IL or missing references)
		((Control)ErrorLabel).ForeColor = Color.Red;
		ErrorList = "";
		ErrorCount = 0;
		if ((TiingoRadioButton.Checked & (APIKeyTextBox.Text.Length == 0)) && (int)MessageBox.Show("Tiingo requires an API token (the last time I checked). Did you want to continue anyway?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32) == 7)
		{
			((Control)APIKeyTextBox).Focus();
			return;
		}
		if (!DividendsCheckBox.Checked & !SplitsCheckBox.Checked)
		{
			MessageBox.Show("Either the dividends or splits (or both) check boxes must be checked.", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)16);
			((Control)DividendsCheckBox).Focus();
			return;
		}
		if ((ListBox1.Items.Count == 0) & (Operators.CompareString(Strings.Trim(SymbolTextBox.Text), "", false) == 0))
		{
			MessageBox.Show("Please enter one or more symbols into the text box (each of them separated by a space) then click Start.", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)64);
			((Control)SymbolTextBox).Focus();
			return;
		}
		int count = ListBox1.SelectedIndices.Count;
		if (Operators.CompareString(Strings.Trim(SymbolTextBox.Text), "", false) == 0 && count == 0)
		{
			if ((int)MessageBox.Show("No symbols have been selected in the listbox. Did you want me to select them all?", "Patternz: ThePatternSite.com", (MessageBoxButtons)4, (MessageBoxIcon)32) != 6)
			{
				return;
			}
			AllButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			count = ListBox1.SelectedIndices.Count;
		}
		checked
		{
			string[] array;
			if (Operators.CompareString(SymbolTextBox.Text, "", false) != 0)
			{
				array = Strings.Split(Strings.Trim(SymbolTextBox.Text), " ", -1, (CompareMethod)0);
				count = 0;
				int num = array.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					if (Operators.CompareString(array[i], "", false) != 0)
					{
						array[count] = array[i];
						count++;
					}
				}
				if (ListBox1.SelectedIndices.Count > 0)
				{
					array = (string[])Utils.CopyArray((Array)array, (Array)new string[count - 1 + ListBox1.SelectedIndices.Count + 1]);
					int num2 = count;
					int num3 = array.Length - 1;
					for (int i = num2; i <= num3; i++)
					{
						string text = ListBox1.SelectedItems[i - count].ToString();
						array[i] = Strings.Left(text, Strings.InStrRev(text, ".", -1, (CompareMethod)0) - 1);
					}
					count = array.Length;
				}
			}
			else
			{
				array = new string[count - 1 + 1];
				int num4 = count - 1;
				for (int i = 0; i <= num4; i++)
				{
					string text = ListBox1.SelectedItems[i].ToString();
					array[i] = Strings.Left(text, Strings.InStrRev(text, ".", -1, (CompareMethod)0) - 1);
				}
			}
			StopPressed = false;
			((Control)AllButton).Enabled = false;
			((Control)APIKeyTextBox).Enabled = false;
			((Control)BrowseButton).Enabled = false;
			((Control)ClipboardButton).Enabled = false;
			((Control)DividendsCheckBox).Enabled = false;
			((Control)DoneButton).Enabled = false;
			((Control)FromDatePicker).Enabled = false;
			((Control)ListBox1).Enabled = false;
			ListBox1.Refresh();
			((Control)PortfolioButton).Enabled = false;
			((Control)SplitsCheckBox).Enabled = false;
			((Control)StartButton).Enabled = false;
			((Control)StopButton).Enabled = true;
			((Control)SymbolTextBox).Enabled = false;
			((Control)TiingoHelpButton).Enabled = false;
			((Control)TiingoRadioButton).Enabled = false;
			((Control)ToDatePicker).Enabled = false;
			ProgressBar1.Value = 0;
			DataGridView1.RowCount = 0;
			GetAnalylitics(array);
			((Control)ToDatePicker).Enabled = true;
			((Control)TiingoRadioButton).Enabled = true;
			((Control)TiingoHelpButton).Enabled = true;
			((Control)SymbolTextBox).Enabled = true;
			((Control)StopButton).Enabled = false;
			((Control)StartButton).Enabled = true;
			((Control)SplitsCheckBox).Enabled = true;
			((Control)PortfolioButton).Enabled = true;
			((Control)ListBox1).Enabled = true;
			((Control)FromDatePicker).Enabled = true;
			((Control)DoneButton).Enabled = true;
			((Control)DividendsCheckBox).Enabled = true;
			((Control)ClipboardButton).Enabled = true;
			((Control)BrowseButton).Enabled = true;
			((Control)APIKeyTextBox).Enabled = true;
			((Control)AllButton).Enabled = true;
			ProgressBar1.Value = 100;
			if (ErrorCount > 0)
			{
				try
				{
					Clipboard.SetText(ErrorList);
					MessageBox.Show(Strings.Format((object)ErrorCount, "") + " errors have been placed on the clipboard.", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)64);
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					MessageBox.Show("Clipboard is busy with another user. Error: " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
					ProjectData.ClearProjectError();
				}
			}
			else
			{
				MessageBox.Show("Done", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
			ProgressBar1.Value = 0;
			DataGridView1.SelectAll();
		}
	}

	private void StopButton_Click(object sender, EventArgs e)
	{
		StopPressed = true;
		Interaction.Beep();
	}

	private void TiingoHelpButton_Click(object sender, EventArgs e)
	{
		//IL_0027: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			Clipboard.SetText("https://www.tiingo.com/welcome");
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		MessageBox.Show(GlobalForm.TiingoMsg, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void TiingoRadioButton_CheckedChanged(object sender, EventArgs e)
	{
		((Control)APIKeyTextBox).Enabled = true;
		APIKeyTextBox.Text = GlobalForm.TiingoKey;
	}
}
