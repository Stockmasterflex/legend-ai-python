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
using Microsoft.VisualBasic.CompilerServices;
using Microsoft.VisualBasic.Devices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class NewsForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("RichTextBox1")]
	private RichTextBox _RichTextBox1;

	[CompilerGenerated]
	[AccessedThroughProperty("SymbolTextBox")]
	private TextBox _SymbolTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("APIKeyTextBox")]
	private TextBox _APIKeyTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("StartButton")]
	private Button _StartButton;

	[CompilerGenerated]
	[AccessedThroughProperty("HeadlinesCB")]
	private CheckBox _HeadlinesCB;

	[CompilerGenerated]
	[AccessedThroughProperty("DescriptionCB")]
	private CheckBox _DescriptionCB;

	[CompilerGenerated]
	[AccessedThroughProperty("DateCB")]
	private CheckBox _DateCB;

	[CompilerGenerated]
	[AccessedThroughProperty("URLCB")]
	private CheckBox _URLCB;

	[CompilerGenerated]
	[AccessedThroughProperty("SourceCB")]
	private CheckBox _SourceCB;

	[CompilerGenerated]
	[AccessedThroughProperty("ClipboardButton")]
	private Button _ClipboardButton;

	private string TIINGONewsURL;

	internal virtual RichTextBox RichTextBox1
	{
		[CompilerGenerated]
		get
		{
			return _RichTextBox1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0007: Unknown result type (might be due to invalid IL or missing references)
			//IL_000d: Expected O, but got Unknown
			LinkClickedEventHandler val = new LinkClickedEventHandler(RichTextBox1_LinkClicked);
			RichTextBox val2 = _RichTextBox1;
			if (val2 != null)
			{
				val2.LinkClicked -= val;
			}
			_RichTextBox1 = value;
			val2 = _RichTextBox1;
			if (val2 != null)
			{
				val2.LinkClicked += val;
			}
		}
	}

	[field: AccessedThroughProperty("Label1")]
	internal virtual Label Label1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual TextBox SymbolTextBox
	{
		[CompilerGenerated]
		get
		{
			return _SymbolTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SymbolTextBox_TextChanged;
			TextBox val = _SymbolTextBox;
			if (val != null)
			{
				((Control)val).TextChanged -= eventHandler;
			}
			_SymbolTextBox = value;
			val = _SymbolTextBox;
			if (val != null)
			{
				((Control)val).TextChanged += eventHandler;
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

	[field: AccessedThroughProperty("Label2")]
	internal virtual Label Label2
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
			EventHandler eventHandler2 = APIKeyTextBox_LostFocus;
			TextBox val = _APIKeyTextBox;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
				((Control)val).TextChanged -= eventHandler2;
			}
			_APIKeyTextBox = value;
			val = _APIKeyTextBox;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
				((Control)val).TextChanged += eventHandler2;
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

	[field: AccessedThroughProperty("ArticleNumberNUM")]
	internal virtual NumericUpDown ArticleNumberNUM
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual CheckBox HeadlinesCB
	{
		[CompilerGenerated]
		get
		{
			return _HeadlinesCB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DateCB_CheckedChanged;
			CheckBox val = _HeadlinesCB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_HeadlinesCB = value;
			val = _HeadlinesCB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Panel1")]
	internal virtual Panel Panel1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("ArticleLimitCB")]
	internal virtual CheckBox ArticleLimitCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("UseDatesCB")]
	internal virtual CheckBox UseDatesCB
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

	[field: AccessedThroughProperty("Panel2")]
	internal virtual Panel Panel2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual CheckBox DescriptionCB
	{
		[CompilerGenerated]
		get
		{
			return _DescriptionCB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DateCB_CheckedChanged;
			CheckBox val = _DescriptionCB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_DescriptionCB = value;
			val = _DescriptionCB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label5")]
	internal virtual Label Label5
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual CheckBox DateCB
	{
		[CompilerGenerated]
		get
		{
			return _DateCB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DateCB_CheckedChanged;
			CheckBox val = _DateCB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_DateCB = value;
			val = _DateCB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox URLCB
	{
		[CompilerGenerated]
		get
		{
			return _URLCB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DateCB_CheckedChanged;
			CheckBox val = _URLCB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_URLCB = value;
			val = _URLCB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox SourceCB
	{
		[CompilerGenerated]
		get
		{
			return _SourceCB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DateCB_CheckedChanged;
			CheckBox val = _SourceCB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_SourceCB = value;
			val = _SourceCB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("WarningLabel")]
	internal virtual Label WarningLabel
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

	[field: AccessedThroughProperty("FolderBrowserDialog1")]
	internal virtual FolderBrowserDialog FolderBrowserDialog1
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

	[field: AccessedThroughProperty("BeforeRB")]
	internal virtual RadioButton BeforeRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("AfterRB")]
	internal virtual RadioButton AfterRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public NewsForm()
	{
		((Form)this).Closing += NewsForm_Closing;
		((Form)this).Load += NewsForm_Load;
		TIINGONewsURL = "https://api.tiingo.com/tiingo/news?tickers=";
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
		//IL_017b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0185: Expected O, but got Unknown
		//IL_0947: Unknown result type (might be due to invalid IL or missing references)
		//IL_0951: Expected O, but got Unknown
		//IL_0c09: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c13: Expected O, but got Unknown
		//IL_0d09: Unknown result type (might be due to invalid IL or missing references)
		//IL_0d13: Expected O, but got Unknown
		//IL_0e18: Unknown result type (might be due to invalid IL or missing references)
		//IL_0e22: Expected O, but got Unknown
		//IL_0e9b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0ea5: Expected O, but got Unknown
		//IL_0f1e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0f28: Expected O, but got Unknown
		RichTextBox1 = new RichTextBox();
		Label1 = new Label();
		SymbolTextBox = new TextBox();
		DoneButton = new Button();
		Label2 = new Label();
		APIKeyTextBox = new TextBox();
		StartButton = new Button();
		ToDatePicker = new DateTimePicker();
		ArticleNumberNUM = new NumericUpDown();
		HeadlinesCB = new CheckBox();
		Panel1 = new Panel();
		BeforeRB = new RadioButton();
		AfterRB = new RadioButton();
		ArticleLimitCB = new CheckBox();
		UseDatesCB = new CheckBox();
		Label6 = new Label();
		Panel2 = new Panel();
		URLCB = new CheckBox();
		SourceCB = new CheckBox();
		DescriptionCB = new CheckBox();
		Label5 = new Label();
		DateCB = new CheckBox();
		WarningLabel = new Label();
		ClipboardButton = new Button();
		FolderBrowserDialog1 = new FolderBrowserDialog();
		Label7 = new Label();
		Label8 = new Label();
		Label9 = new Label();
		((ISupportInitialize)ArticleNumberNUM).BeginInit();
		((Control)Panel1).SuspendLayout();
		((Control)Panel2).SuspendLayout();
		((Control)this).SuspendLayout();
		((Control)RichTextBox1).Anchor = (AnchorStyles)15;
		RichTextBox1.Font = new Font("Microsoft Sans Serif", 10f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)RichTextBox1).Location = new Point(12, 2);
		((Control)RichTextBox1).Name = "RichTextBox1";
		((TextBoxBase)RichTextBox1).ReadOnly = true;
		((Control)RichTextBox1).Size = new Size(669, 242);
		((Control)RichTextBox1).TabIndex = 1;
		RichTextBox1.Text = "";
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(245, 414);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(145, 13);
		((Control)Label1).TabIndex = 10;
		Label1.Text = "S&ymbol(s), comma separated:";
		((Control)SymbolTextBox).Anchor = (AnchorStyles)10;
		((Control)SymbolTextBox).Location = new Point(390, 412);
		((Control)SymbolTextBox).Name = "SymbolTextBox";
		((Control)SymbolTextBox).Size = new Size(157, 20);
		((Control)SymbolTextBox).TabIndex = 11;
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(619, 409);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(60, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(317, 382);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(73, 13);
		((Control)Label2).TabIndex = 8;
		Label2.Text = "&Tiingo Token:";
		((Control)APIKeyTextBox).Anchor = (AnchorStyles)10;
		((Control)APIKeyTextBox).Location = new Point(390, 379);
		((TextBoxBase)APIKeyTextBox).MaxLength = 100;
		((Control)APIKeyTextBox).Name = "APIKeyTextBox";
		((Control)APIKeyTextBox).Size = new Size(157, 20);
		((Control)APIKeyTextBox).TabIndex = 9;
		((TextBoxBase)APIKeyTextBox).WordWrap = false;
		((Control)StartButton).Anchor = (AnchorStyles)10;
		((Control)StartButton).Location = new Point(619, 378);
		((Control)StartButton).Name = "StartButton";
		((Control)StartButton).Size = new Size(60, 23);
		((Control)StartButton).TabIndex = 12;
		((ButtonBase)StartButton).Text = "St&art";
		((ButtonBase)StartButton).UseVisualStyleBackColor = true;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(169, 75);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(84, 20);
		((Control)ToDatePicker).TabIndex = 7;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)ArticleNumberNUM).Location = new Point(169, 26);
		ArticleNumberNUM.Maximum = new decimal(new int[4] { 1000, 0, 0, 0 });
		ArticleNumberNUM.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)ArticleNumberNUM).Name = "ArticleNumberNUM";
		((Control)ArticleNumberNUM).Size = new Size(53, 20);
		((Control)ArticleNumberNUM).TabIndex = 2;
		ArticleNumberNUM.Value = new decimal(new int[4] { 10, 0, 0, 0 });
		((ButtonBase)HeadlinesCB).AutoSize = true;
		HeadlinesCB.Checked = true;
		HeadlinesCB.CheckState = (CheckState)1;
		((Control)HeadlinesCB).Location = new Point(13, 53);
		((Control)HeadlinesCB).Name = "HeadlinesCB";
		((Control)HeadlinesCB).Size = new Size(68, 17);
		((Control)HeadlinesCB).TabIndex = 2;
		((ButtonBase)HeadlinesCB).Text = "&Headline";
		((ButtonBase)HeadlinesCB).UseVisualStyleBackColor = true;
		((Control)Panel1).Anchor = (AnchorStyles)10;
		Panel1.BorderStyle = (BorderStyle)2;
		((Control)Panel1).Controls.Add((Control)(object)BeforeRB);
		((Control)Panel1).Controls.Add((Control)(object)AfterRB);
		((Control)Panel1).Controls.Add((Control)(object)ArticleLimitCB);
		((Control)Panel1).Controls.Add((Control)(object)UseDatesCB);
		((Control)Panel1).Controls.Add((Control)(object)Label6);
		((Control)Panel1).Controls.Add((Control)(object)ToDatePicker);
		((Control)Panel1).Controls.Add((Control)(object)ArticleNumberNUM);
		((Control)Panel1).Location = new Point(241, 251);
		((Control)Panel1).Name = "Panel1";
		((Control)Panel1).Size = new Size(260, 105);
		((Control)Panel1).TabIndex = 6;
		((ButtonBase)BeforeRB).AutoSize = true;
		((Control)BeforeRB).Location = new Point(28, 75);
		((Control)BeforeRB).Name = "BeforeRB";
		((Control)BeforeRB).Size = new Size(59, 17);
		((Control)BeforeRB).TabIndex = 4;
		((ButtonBase)BeforeRB).Text = "Before:";
		((ButtonBase)BeforeRB).UseVisualStyleBackColor = true;
		((ButtonBase)AfterRB).AutoSize = true;
		AfterRB.Checked = true;
		((Control)AfterRB).Location = new Point(94, 75);
		((Control)AfterRB).Name = "AfterRB";
		((Control)AfterRB).Size = new Size(69, 17);
		((Control)AfterRB).TabIndex = 6;
		AfterRB.TabStop = true;
		((ButtonBase)AfterRB).Text = "OR &After:";
		((ButtonBase)AfterRB).UseVisualStyleBackColor = true;
		((ButtonBase)ArticleLimitCB).AutoSize = true;
		ArticleLimitCB.Checked = true;
		ArticleLimitCB.CheckState = (CheckState)1;
		((Control)ArticleLimitCB).Location = new Point(13, 27);
		((Control)ArticleLimitCB).Name = "ArticleLimitCB";
		((Control)ArticleLimitCB).Size = new Size(151, 17);
		((Control)ArticleLimitCB).TabIndex = 1;
		((ButtonBase)ArticleLimitCB).Text = "&Limit number of articles to: ";
		((ButtonBase)ArticleLimitCB).UseVisualStyleBackColor = true;
		((ButtonBase)UseDatesCB).AutoSize = true;
		((Control)UseDatesCB).Location = new Point(13, 50);
		((Control)UseDatesCB).Name = "UseDatesCB";
		((Control)UseDatesCB).Size = new Size(130, 17);
		((Control)UseDatesCB).TabIndex = 3;
		((ButtonBase)UseDatesCB).Text = "&Use news published...";
		((ButtonBase)UseDatesCB).UseVisualStyleBackColor = true;
		Label6.AutoSize = true;
		((Control)Label6).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label6).Location = new Point(10, 2);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(50, 13);
		((Control)Label6).TabIndex = 0;
		Label6.Text = "Options";
		((Control)Panel2).Anchor = (AnchorStyles)10;
		Panel2.BorderStyle = (BorderStyle)2;
		((Control)Panel2).Controls.Add((Control)(object)URLCB);
		((Control)Panel2).Controls.Add((Control)(object)SourceCB);
		((Control)Panel2).Controls.Add((Control)(object)DescriptionCB);
		((Control)Panel2).Controls.Add((Control)(object)Label5);
		((Control)Panel2).Controls.Add((Control)(object)DateCB);
		((Control)Panel2).Controls.Add((Control)(object)HeadlinesCB);
		((Control)Panel2).Location = new Point(507, 250);
		((Control)Panel2).Name = "Panel2";
		((Control)Panel2).Size = new Size(172, 106);
		((Control)Panel2).TabIndex = 7;
		((ButtonBase)URLCB).AutoSize = true;
		((Control)URLCB).Location = new Point(101, 55);
		((Control)URLCB).Name = "URLCB";
		((Control)URLCB).Size = new Size(48, 17);
		((Control)URLCB).TabIndex = 5;
		((ButtonBase)URLCB).Text = "&URL";
		((ButtonBase)URLCB).UseVisualStyleBackColor = true;
		((ButtonBase)SourceCB).AutoSize = true;
		((Control)SourceCB).Location = new Point(101, 30);
		((Control)SourceCB).Name = "SourceCB";
		((Control)SourceCB).Size = new Size(60, 17);
		((Control)SourceCB).TabIndex = 4;
		((ButtonBase)SourceCB).Text = "&Source";
		((ButtonBase)SourceCB).UseVisualStyleBackColor = true;
		((ButtonBase)DescriptionCB).AutoSize = true;
		DescriptionCB.Checked = true;
		DescriptionCB.CheckState = (CheckState)1;
		((Control)DescriptionCB).Location = new Point(13, 76);
		((Control)DescriptionCB).Name = "DescriptionCB";
		((Control)DescriptionCB).Size = new Size(79, 17);
		((Control)DescriptionCB).TabIndex = 3;
		((ButtonBase)DescriptionCB).Text = "&Description";
		((ButtonBase)DescriptionCB).UseVisualStyleBackColor = true;
		Label5.AutoSize = true;
		((Control)Label5).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label5).Location = new Point(10, 2);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(121, 13);
		((Control)Label5).TabIndex = 0;
		Label5.Text = "Show Article Details";
		((ButtonBase)DateCB).AutoSize = true;
		DateCB.Checked = true;
		DateCB.CheckState = (CheckState)1;
		((Control)DateCB).Location = new Point(13, 30);
		((Control)DateCB).Name = "DateCB";
		((Control)DateCB).Size = new Size(49, 17);
		((Control)DateCB).TabIndex = 1;
		((ButtonBase)DateCB).Text = "&Date";
		((ButtonBase)DateCB).UseVisualStyleBackColor = true;
		((Control)WarningLabel).Anchor = (AnchorStyles)6;
		((Control)WarningLabel).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)WarningLabel).Location = new Point(12, 255);
		((Control)WarningLabel).Name = "WarningLabel";
		((Control)WarningLabel).Size = new Size(221, 45);
		((Control)WarningLabel).TabIndex = 2;
		WarningLabel.Text = "To use this form, you need both a Tiingo token and a subscription to their service. Enter the token in the text box.";
		((Control)ClipboardButton).Anchor = (AnchorStyles)10;
		((Control)ClipboardButton).Enabled = false;
		((Control)ClipboardButton).Location = new Point(553, 409);
		((Control)ClipboardButton).Name = "ClipboardButton";
		((Control)ClipboardButton).Size = new Size(60, 23);
		((Control)ClipboardButton).TabIndex = 13;
		((ButtonBase)ClipboardButton).Text = "Clip&board";
		((ButtonBase)ClipboardButton).UseVisualStyleBackColor = true;
		FolderBrowserDialog1.ShowNewFolderButton = false;
		((Control)Label7).Anchor = (AnchorStyles)6;
		((Control)Label7).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)Label7).Location = new Point(12, 362);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(221, 32);
		((Control)Label7).TabIndex = 4;
		Label7.Text = "Options: Controls what Tiingo returns (how many articles, using dates). ";
		((Control)Label8).Anchor = (AnchorStyles)6;
		((Control)Label8).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)Label8).Location = new Point(12, 407);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(221, 45);
		((Control)Label8).TabIndex = 5;
		Label8.Text = "Show Article Details: Controls what kind of information is shown. At least one must be checked.";
		((Control)Label9).Anchor = (AnchorStyles)6;
		((Control)Label9).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)Label9).Location = new Point(12, 309);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(221, 43);
		((Control)Label9).TabIndex = 3;
		Label9.Text = "Provide at least one stock symbol in the Symbol(s) text box, comma separated. Spaces will be replaced with commas.";
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(693, 453);
		((Control)this).Controls.Add((Control)(object)Label9);
		((Control)this).Controls.Add((Control)(object)Label8);
		((Control)this).Controls.Add((Control)(object)Label7);
		((Control)this).Controls.Add((Control)(object)ClipboardButton);
		((Control)this).Controls.Add((Control)(object)WarningLabel);
		((Control)this).Controls.Add((Control)(object)Panel2);
		((Control)this).Controls.Add((Control)(object)Panel1);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)APIKeyTextBox);
		((Control)this).Controls.Add((Control)(object)StartButton);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)SymbolTextBox);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)RichTextBox1);
		((Control)this).Name = "NewsForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "News Form";
		((ISupportInitialize)ArticleNumberNUM).EndInit();
		((Control)Panel1).ResumeLayout(false);
		((Control)Panel1).PerformLayout();
		((Control)Panel2).ResumeLayout(false);
		((Control)Panel2).PerformLayout();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void NewsForm_Closing(object sender, CancelEventArgs e)
	{
		GlobalForm.TiingoKey = APIKeyTextBox.Text;
		if (Operators.CompareString(GlobalForm.lsTiingoKey, GlobalForm.TiingoKey, false) != 0)
		{
			string text = new GlobalForm.Simple3Des("da9ba2681").EncryptData(GlobalForm.TiingoKey);
			try
			{
				((ServerComputer)MyProject.Computer).Registry.SetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "Captoff", (object)text);
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				ProjectData.ClearProjectError();
			}
		}
		try
		{
			GlobalForm.ArticleNumber = Convert.ToInt32(ArticleNumberNUM.Value);
			GlobalForm.NewsDateRB = Conversions.ToInteger(Interaction.IIf(BeforeRB.Checked, (object)1, (object)2));
			if (DateCB.Checked != Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[0] == 0, (object)false, (object)true)))
			{
				GlobalForm.NewsOptionsChanged = true;
				GlobalForm.NewsOptions[0] = Conversions.ToByte(Interaction.IIf(DateCB.Checked, (object)1, (object)0));
			}
			if (HeadlinesCB.Checked != Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[1] == 0, (object)false, (object)true)))
			{
				GlobalForm.NewsOptionsChanged = true;
				GlobalForm.NewsOptions[1] = Conversions.ToByte(Interaction.IIf(HeadlinesCB.Checked, (object)1, (object)0));
			}
			if (DescriptionCB.Checked != Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[2] == 0, (object)false, (object)true)))
			{
				GlobalForm.NewsOptionsChanged = true;
				GlobalForm.NewsOptions[2] = Conversions.ToByte(Interaction.IIf(DescriptionCB.Checked, (object)1, (object)0));
			}
			if (SourceCB.Checked != Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[3] == 0, (object)false, (object)true)))
			{
				GlobalForm.NewsOptionsChanged = true;
				GlobalForm.NewsOptions[3] = Conversions.ToByte(Interaction.IIf(SourceCB.Checked, (object)1, (object)0));
			}
			if (URLCB.Checked != Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[4] == 0, (object)false, (object)true)))
			{
				GlobalForm.NewsOptionsChanged = true;
				GlobalForm.NewsOptions[4] = Conversions.ToByte(Interaction.IIf(URLCB.Checked, (object)1, (object)0));
			}
			if (ArticleLimitCB.Checked != Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[5] == 0, (object)false, (object)true)))
			{
				GlobalForm.NewsOptionsChanged = true;
				GlobalForm.NewsOptions[5] = Conversions.ToByte(Interaction.IIf(ArticleLimitCB.Checked, (object)1, (object)0));
			}
			if (UseDatesCB.Checked != Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[6] == 0, (object)false, (object)true)))
			{
				GlobalForm.NewsOptionsChanged = true;
				GlobalForm.NewsOptions[6] = Conversions.ToByte(Interaction.IIf(UseDatesCB.Checked, (object)1, (object)0));
			}
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			ProjectData.ClearProjectError();
		}
		MySettingsProperty.Settings.NewsFormLocation = ((Form)this).Location;
		MySettingsProperty.Settings.NewsFormSize = ((Form)this).Size;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
	}

	private void NewsForm_Load(object sender, EventArgs e)
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
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.NewsFormLocation, MySettingsProperty.Settings.NewsFormSize);
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)AfterRB, "Show news on or after this date.");
		val.SetToolTip((Control)(object)APIKeyTextBox, "Provide the token Tiingo assigned when you registered for their service.");
		val.SetToolTip((Control)(object)ArticleLimitCB, "Did you want to limit number of articles retrieved?");
		val.SetToolTip((Control)(object)ArticleNumberNUM, "Enter the number of articles to find, from 1 to 1,000");
		val.SetToolTip((Control)(object)BeforeRB, "Show news on or before this date.");
		val.SetToolTip((Control)(object)ClipboardButton, "Copy selected text to the clipboard.");
		val.SetToolTip((Control)(object)DateCB, "Show the news date.");
		val.SetToolTip((Control)(object)DescriptionCB, "Show article text.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)HeadlinesCB, "Show headlines.");
		val.SetToolTip((Control)(object)RichTextBox1, "News appears here.");
		val.SetToolTip((Control)(object)SourceCB, "Show news source.");
		val.SetToolTip((Control)(object)StartButton, "Get news.");
		val.SetToolTip((Control)(object)SymbolTextBox, "Get news on these symbols.");
		val.SetToolTip((Control)(object)ToDatePicker, "Enter from and to dates to find news.");
		val.SetToolTip((Control)(object)URLCB, "Show link to article.");
		val.SetToolTip((Control)(object)UseDatesCB, "Use dates to limit news search.");
		GlobalForm.TiingoKey = "";
		try
		{
			string text = Conversions.ToString(((ServerComputer)MyProject.Computer).Registry.GetValue("HKEY_CURRENT_USER\\Software\\PatternzSoftware\\UpdateForm", "Captoff", (object)""));
			if (Operators.CompareString(text, "", false) != 0)
			{
				GlobalForm.TiingoKey = new GlobalForm.Simple3Des("da9ba2681").DecryptData(text);
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		try
		{
			APIKeyTextBox.Text = GlobalForm.TiingoKey;
			DateCB.Checked = Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[0] == 0, (object)false, (object)true));
			HeadlinesCB.Checked = Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[1] == 0, (object)false, (object)true));
			DescriptionCB.Checked = Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[2] == 0, (object)false, (object)true));
			SourceCB.Checked = Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[3] == 0, (object)false, (object)true));
			URLCB.Checked = Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[4] == 0, (object)false, (object)true));
			ArticleLimitCB.Checked = Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[5] == 0, (object)false, (object)true));
			UseDatesCB.Checked = Conversions.ToBoolean(Interaction.IIf(GlobalForm.NewsOptions[6] == 0, (object)false, (object)true));
			ArticleNumberNUM.Value = new decimal(GlobalForm.ArticleNumber);
			ToDatePicker.Value = DateAndTime.Now;
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			ProjectData.ClearProjectError();
		}
		checked
		{
			if (MyProject.Forms.Mainform.ListBox1.SelectedItems.Count > 0)
			{
				SymbolTextBox.Text = "";
				int num = MyProject.Forms.Mainform.ListBox1.SelectedItems.Count - 1;
				for (int i = 0; i <= num; i++)
				{
					string text2 = MyProject.Forms.Mainform.ListBox1.SelectedItems[i].ToString();
					if (Strings.InStr(text2, ".", (CompareMethod)0) != 0)
					{
						text2 = Strings.Left(text2, Strings.InStr(text2, ".", (CompareMethod)0) - 1);
					}
					TextBox symbolTextBox;
					(symbolTextBox = SymbolTextBox).Text = symbolTextBox.Text + text2 + ",";
				}
				if (Operators.CompareString(Strings.Right(SymbolTextBox.Text, 1), ",", false) == 0)
				{
					SymbolTextBox.Text = Strings.Left(SymbolTextBox.Text, ((TextBoxBase)SymbolTextBox).TextLength - 1);
				}
			}
			SymbolTextBox_TextChanged(RuntimeHelpers.GetObjectValue(sender), e);
			if (GlobalForm.NewsDateRB == 1)
			{
				BeforeRB.Checked = true;
			}
			else
			{
				AfterRB.Checked = true;
			}
		}
	}

	private void APIKeyTextBox_LostFocus(object sender, EventArgs e)
	{
		GlobalForm.TiingoKey = APIKeyTextBox.Text;
		if (Operators.CompareString(APIKeyTextBox.Text, "", false) == 0)
		{
			((Control)WarningLabel).ForeColor = Color.Red;
		}
		else
		{
			((Control)WarningLabel).ForeColor = Color.Black;
		}
	}

	private void ClipboardButton_Click(object sender, EventArgs e)
	{
		//IL_005b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0080: Unknown result type (might be due to invalid IL or missing references)
		if (RichTextBox1.SelectedText.Length == 0)
		{
			((TextBoxBase)RichTextBox1).SelectAll();
		}
		string selectedText = RichTextBox1.SelectedText;
		((Control)this).Cursor = Cursors.WaitCursor;
		try
		{
			Clipboard.SetText(selectedText);
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			MessageBox.Show("Clipboard is busy with another user. Error: " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			ProjectData.ClearProjectError();
		}
		((Control)this).Cursor = Cursors.Default;
		MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void DateCB_CheckedChanged(object sender, EventArgs e)
	{
		if (!DateCB.Checked & !HeadlinesCB.Checked & !DescriptionCB.Checked & !SourceCB.Checked & !URLCB.Checked)
		{
			((Control)StartButton).Enabled = false;
		}
		else
		{
			((Control)StartButton).Enabled = true;
		}
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void ParseAndShowData(string Buffer)
	{
		string[] array = new string[5];
		Buffer = Buffer.Replace("\\\"", "");
		string[] array2 = Regex.Split(Buffer, "\"");
		int num = array2.Length;
		checked
		{
			int num2 = num - 1;
			int num3 = default(int);
			for (int i = 0; i <= num2; i++)
			{
				switch (array2[i])
				{
				case "publishedDate":
					if (DateCB.Checked && i + 2 <= num)
					{
						array[0] = array2[i + 2].Replace("T", " ");
					}
					num3++;
					break;
				case "title":
					if (HeadlinesCB.Checked && i + 2 <= num)
					{
						array[1] = array2[i + 2];
					}
					num3++;
					break;
				case "description":
					if (DescriptionCB.Checked && i + 2 <= num)
					{
						array[2] = array2[i + 2];
					}
					num3++;
					break;
				case "source":
					if (SourceCB.Checked && i + 2 <= num)
					{
						array[3] = array2[i + 2];
					}
					num3++;
					break;
				case "url":
					if (URLCB.Checked && i + 2 <= num)
					{
						array[4] = array2[i + 2];
					}
					num3++;
					break;
				}
				if (num3 == 5)
				{
					RichTextBox1.SelectionIndent = 0;
					if (DateCB.Checked)
					{
						((TextBoxBase)RichTextBox1).AppendText(array[0] + "\t");
					}
					if (HeadlinesCB.Checked)
					{
						((TextBoxBase)RichTextBox1).AppendText(array[1] + "\r\n");
					}
					RichTextBox1.SelectionIndent = 20;
					if (DescriptionCB.Checked)
					{
						((TextBoxBase)RichTextBox1).AppendText(array[2] + "\r\n");
					}
					if (SourceCB.Checked)
					{
						((TextBoxBase)RichTextBox1).AppendText(array[3] + "\r\n");
					}
					if (URLCB.Checked)
					{
						((TextBoxBase)RichTextBox1).AppendText(array[4]);
					}
					((TextBoxBase)RichTextBox1).AppendText("\r\n\r\n");
					Array.Clear(array, 0, array.Length);
					num3 = 0;
				}
			}
		}
	}

	private void RichTextBox1_LinkClicked(object sender, LinkClickedEventArgs e)
	{
		try
		{
			Process.Start(e.LinkText);
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
	}

	private void StartButton_Click(object sender, EventArgs e)
	{
		//IL_002f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0083: Unknown result type (might be due to invalid IL or missing references)
		RichTextBox1.Text = "";
		if (APIKeyTextBox.Text.Length == 0)
		{
			MessageBox.Show("Tiingo requires a token plus you must have a paid subscription to get news.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			((Control)APIKeyTextBox).Focus();
			return;
		}
		if ((Operators.CompareString(Strings.Trim(SymbolTextBox.Text), "", false) == 0) | (SymbolTextBox.Text.Length == 0))
		{
			MessageBox.Show("Enter a symbol in the text box or use the Main Form to select some.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			return;
		}
		SymbolTextBox.Text = Strings.Trim(SymbolTextBox.Text).Replace(" ", ",");
		SymbolTextBox.Text = Strings.Trim(SymbolTextBox.Text).Replace(",,", ",");
		string text = SymbolTextBox.Text;
		if (Operators.CompareString(Strings.Right(text, 1), ",", false) == 0)
		{
			text = Strings.Left(text, checked(Strings.Len(text) - 1));
		}
		if (text.Length != 0)
		{
			((Control)AfterRB).Enabled = false;
			((Control)APIKeyTextBox).Enabled = false;
			((Control)ArticleLimitCB).Enabled = false;
			((Control)ArticleNumberNUM).Enabled = false;
			((Control)BeforeRB).Enabled = false;
			((Control)ClipboardButton).Enabled = false;
			((Control)DateCB).Enabled = false;
			((Control)DescriptionCB).Enabled = false;
			((Control)DoneButton).Enabled = false;
			((Control)HeadlinesCB).Enabled = false;
			((Control)RichTextBox1).Enabled = false;
			((Control)SourceCB).Enabled = false;
			((Control)StartButton).Enabled = false;
			((Control)SymbolTextBox).Enabled = false;
			((Control)ToDatePicker).Enabled = false;
			((Control)URLCB).Enabled = false;
			((Control)UseDatesCB).Enabled = false;
			StreamReader streamReader = null;
			Stream stream = null;
			WebResponse webResponse = null;
			string text2 = "";
			string text3 = TIINGONewsURL + text;
			if (UseDatesCB.Checked)
			{
				DateTime date = ToDatePicker.Value.Date;
				text3 = ((!BeforeRB.Checked) ? (text3 + "&startDate=" + Strings.Format((object)date, "yyyy-MM-dd")) : (text3 + "&endDate=" + Strings.Format((object)date, "yyyy-MM-dd")));
			}
			if (ArticleLimitCB.Checked)
			{
				text3 = text3 + "&limit=" + ArticleNumberNUM.Value;
			}
			ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
			text3 = text3 + "&token=" + APIKeyTextBox.Text;
			try
			{
				webResponse = WebRequest.CreateHttp(text3).GetResponse();
				stream = webResponse.GetResponseStream();
				streamReader = new StreamReader(stream);
				text2 = streamReader.ReadToEnd();
				streamReader.Close();
				streamReader = null;
				stream.Close();
				stream = null;
				webResponse.Close();
				webResponse = null;
				ParseAndShowData(text2);
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				RichTextBox1.Text = ex2.Message;
				streamReader?.Close();
				stream?.Close();
				webResponse?.Close();
				ProjectData.ClearProjectError();
			}
			((Control)AfterRB).Enabled = true;
			((Control)APIKeyTextBox).Enabled = true;
			((Control)ArticleLimitCB).Enabled = true;
			((Control)ArticleNumberNUM).Enabled = true;
			((Control)BeforeRB).Enabled = true;
			if (RichTextBox1.TextLength > 0)
			{
				((Control)ClipboardButton).Enabled = true;
			}
			else
			{
				((Control)ClipboardButton).Enabled = false;
			}
			((Control)DateCB).Enabled = true;
			((Control)DescriptionCB).Enabled = true;
			((Control)DoneButton).Enabled = true;
			((Control)HeadlinesCB).Enabled = true;
			((Control)RichTextBox1).Enabled = true;
			((Control)SourceCB).Enabled = true;
			((Control)StartButton).Enabled = true;
			((Control)SymbolTextBox).Enabled = true;
			((Control)ToDatePicker).Enabled = true;
			((Control)URLCB).Enabled = true;
			((Control)UseDatesCB).Enabled = true;
		}
	}

	private void SymbolTextBox_TextChanged(object sender, EventArgs e)
	{
		if (((TextBoxBase)SymbolTextBox).TextLength == 0)
		{
			((Control)StartButton).Enabled = false;
		}
		else
		{
			((Control)StartButton).Enabled = true;
		}
	}
}
