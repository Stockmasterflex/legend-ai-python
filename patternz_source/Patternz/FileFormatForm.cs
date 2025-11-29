using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class FileFormatForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("ListBox1")]
	private ListBox _ListBox1;

	[CompilerGenerated]
	[AccessedThroughProperty("BrowseButton")]
	private Button _BrowseButton;

	[CompilerGenerated]
	[AccessedThroughProperty("AdjCloseCheckBox")]
	private CheckBox _AdjCloseCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("VolumeCheckBox")]
	private CheckBox _VolumeCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("OpenCheckBox")]
	private CheckBox _OpenCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("TimeCheckBox")]
	private CheckBox _TimeCheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("GraphButton")]
	private Button _GraphButton;

	[CompilerGenerated]
	[AccessedThroughProperty("SaveFileFormatButton")]
	private Button _SaveFileFormatButton;

	[CompilerGenerated]
	[AccessedThroughProperty("AdjCloseTextBox")]
	private MaskedTextBox _AdjCloseTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("VolumeTextBox")]
	private MaskedTextBox _VolumeTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("CloseTextBox")]
	private MaskedTextBox _CloseTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("LowTextBox")]
	private MaskedTextBox _LowTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("HighTextBox")]
	private MaskedTextBox _HighTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("OpenTextBox")]
	private MaskedTextBox _OpenTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("TimeTextBox")]
	private MaskedTextBox _TimeTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("DateTextBox")]
	private MaskedTextBox _DateTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("HelpButton1")]
	private Button _HelpButton1;

	[CompilerGenerated]
	[AccessedThroughProperty("Chart1")]
	private Chart _Chart1;

	[CompilerGenerated]
	[AccessedThroughProperty("sDateFormatCombo")]
	private ComboBox _sDateFormatCombo;

	private bool SaveNeeded;

	private bool LockFlag;

	private string TempsDateFormat;

	private bool Block_FormActivate;

	private string DateLine;

	private int lsChartPeriodShown;

	private bool lsVolumeChecked;

	[field: AccessedThroughProperty("Panel1")]
	internal virtual Panel Panel1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual ListBox ListBox1
	{
		[CompilerGenerated]
		get
		{
			return _ListBox1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ListBox1_SelectedIndexChanged;
			ListBox val = _ListBox1;
			if (val != null)
			{
				val.SelectedIndexChanged -= eventHandler;
			}
			_ListBox1 = value;
			val = _ListBox1;
			if (val != null)
			{
				val.SelectedIndexChanged += eventHandler;
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

	internal virtual CheckBox AdjCloseCheckBox
	{
		[CompilerGenerated]
		get
		{
			return _AdjCloseCheckBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = AdjCloseCheckBox_CheckedChanged;
			CheckBox val = _AdjCloseCheckBox;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_AdjCloseCheckBox = value;
			val = _AdjCloseCheckBox;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox VolumeCheckBox
	{
		[CompilerGenerated]
		get
		{
			return _VolumeCheckBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = VolumeCheckBox_CheckedChanged;
			CheckBox val = _VolumeCheckBox;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_VolumeCheckBox = value;
			val = _VolumeCheckBox;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox OpenCheckBox
	{
		[CompilerGenerated]
		get
		{
			return _OpenCheckBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = OpenCheckBox_CheckedChanged;
			CheckBox val = _OpenCheckBox;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_OpenCheckBox = value;
			val = _OpenCheckBox;
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

	[field: AccessedThroughProperty("Label4")]
	internal virtual Label Label4
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

	internal virtual CheckBox TimeCheckBox
	{
		[CompilerGenerated]
		get
		{
			return _TimeCheckBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = TimeCheckBox_CheckedChanged;
			CheckBox val = _TimeCheckBox;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_TimeCheckBox = value;
			val = _TimeCheckBox;
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

	internal virtual Button SaveFileFormatButton
	{
		[CompilerGenerated]
		get
		{
			return _SaveFileFormatButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SaveFileFormatButton_Click;
			Button val = _SaveFileFormatButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_SaveFileFormatButton = value;
			val = _SaveFileFormatButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("GroupBox2")]
	internal virtual GroupBox GroupBox2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual MaskedTextBox AdjCloseTextBox
	{
		[CompilerGenerated]
		get
		{
			return _AdjCloseTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DateTextBox_LostFocus;
			EventHandler eventHandler2 = DateTextBox_TextChanged;
			MaskedTextBox val = _AdjCloseTextBox;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
				((Control)val).TextChanged -= eventHandler2;
			}
			_AdjCloseTextBox = value;
			val = _AdjCloseTextBox;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
				((Control)val).TextChanged += eventHandler2;
			}
		}
	}

	internal virtual MaskedTextBox VolumeTextBox
	{
		[CompilerGenerated]
		get
		{
			return _VolumeTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DateTextBox_LostFocus;
			EventHandler eventHandler2 = DateTextBox_TextChanged;
			MaskedTextBox val = _VolumeTextBox;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
				((Control)val).TextChanged -= eventHandler2;
			}
			_VolumeTextBox = value;
			val = _VolumeTextBox;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
				((Control)val).TextChanged += eventHandler2;
			}
		}
	}

	internal virtual MaskedTextBox CloseTextBox
	{
		[CompilerGenerated]
		get
		{
			return _CloseTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DateTextBox_LostFocus;
			EventHandler eventHandler2 = DateTextBox_TextChanged;
			MaskedTextBox val = _CloseTextBox;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
				((Control)val).TextChanged -= eventHandler2;
			}
			_CloseTextBox = value;
			val = _CloseTextBox;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
				((Control)val).TextChanged += eventHandler2;
			}
		}
	}

	internal virtual MaskedTextBox LowTextBox
	{
		[CompilerGenerated]
		get
		{
			return _LowTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DateTextBox_LostFocus;
			EventHandler eventHandler2 = DateTextBox_TextChanged;
			MaskedTextBox val = _LowTextBox;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
				((Control)val).TextChanged -= eventHandler2;
			}
			_LowTextBox = value;
			val = _LowTextBox;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
				((Control)val).TextChanged += eventHandler2;
			}
		}
	}

	internal virtual MaskedTextBox HighTextBox
	{
		[CompilerGenerated]
		get
		{
			return _HighTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DateTextBox_LostFocus;
			EventHandler eventHandler2 = DateTextBox_TextChanged;
			MaskedTextBox val = _HighTextBox;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
				((Control)val).TextChanged -= eventHandler2;
			}
			_HighTextBox = value;
			val = _HighTextBox;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
				((Control)val).TextChanged += eventHandler2;
			}
		}
	}

	internal virtual MaskedTextBox OpenTextBox
	{
		[CompilerGenerated]
		get
		{
			return _OpenTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DateTextBox_LostFocus;
			EventHandler eventHandler2 = DateTextBox_TextChanged;
			MaskedTextBox val = _OpenTextBox;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
				((Control)val).TextChanged -= eventHandler2;
			}
			_OpenTextBox = value;
			val = _OpenTextBox;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
				((Control)val).TextChanged += eventHandler2;
			}
		}
	}

	internal virtual MaskedTextBox TimeTextBox
	{
		[CompilerGenerated]
		get
		{
			return _TimeTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DateTextBox_LostFocus;
			EventHandler eventHandler2 = DateTextBox_TextChanged;
			MaskedTextBox val = _TimeTextBox;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
				((Control)val).TextChanged -= eventHandler2;
			}
			_TimeTextBox = value;
			val = _TimeTextBox;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
				((Control)val).TextChanged += eventHandler2;
			}
		}
	}

	internal virtual MaskedTextBox DateTextBox
	{
		[CompilerGenerated]
		get
		{
			return _DateTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DateTextBox_LostFocus;
			EventHandler eventHandler2 = DateTextBox_TextChanged;
			MaskedTextBox val = _DateTextBox;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
				((Control)val).TextChanged -= eventHandler2;
			}
			_DateTextBox = value;
			val = _DateTextBox;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
				((Control)val).TextChanged += eventHandler2;
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

	[field: AccessedThroughProperty("FileLabel")]
	internal virtual Label FileLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
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
			MouseEventHandler val = new MouseEventHandler(Chart1_MouseDown);
			MouseEventHandler val2 = new MouseEventHandler(Chart1_MouseUp);
			Chart val3 = _Chart1;
			if (val3 != null)
			{
				((Control)val3).MouseDown -= val;
				((Control)val3).MouseUp -= val2;
			}
			_Chart1 = value;
			val3 = _Chart1;
			if (val3 != null)
			{
				((Control)val3).MouseDown += val;
				((Control)val3).MouseUp += val2;
			}
		}
	}

	[field: AccessedThroughProperty("DataGridView1")]
	internal virtual DataGridView DataGridView1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual ComboBox sDateFormatCombo
	{
		[CompilerGenerated]
		get
		{
			return _sDateFormatCombo;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = sDateFormatCombo_FormatStringChanged;
			EventHandler eventHandler2 = sDateFormatCombo_FormatStringChanged;
			EventHandler eventHandler3 = sDateFormatCombo_LostFocus;
			CancelEventHandler cancelEventHandler = sDateFormatCombo_Validating;
			ComboBox val = _sDateFormatCombo;
			if (val != null)
			{
				((ListControl)val).FormatStringChanged -= eventHandler;
				((Control)val).TextChanged -= eventHandler2;
				((Control)val).LostFocus -= eventHandler3;
				((Control)val).Validating -= cancelEventHandler;
			}
			_sDateFormatCombo = value;
			val = _sDateFormatCombo;
			if (val != null)
			{
				((ListControl)val).FormatStringChanged += eventHandler;
				((Control)val).TextChanged += eventHandler2;
				((Control)val).LostFocus += eventHandler3;
				((Control)val).Validating += cancelEventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label6")]
	internal virtual Label Label6
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("ToolTip1")]
	internal virtual ToolTip ToolTip1
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

	[field: AccessedThroughProperty("Label7")]
	internal virtual Label Label7
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

	[field: AccessedThroughProperty("DateTimeCheckBox")]
	internal virtual CheckBox DateTimeCheckBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public FileFormatForm()
	{
		//IL_0044: Unknown result type (might be due to invalid IL or missing references)
		//IL_004e: Expected O, but got Unknown
		((Form)this).Closing += FileFormatForm_Closing;
		((Form)this).Load += FileFormatForm_Load;
		((Form)this).Activated += FileFormatForm_Activated;
		((Control)this).KeyDown += new KeyEventHandler(FileFormatForm_KeyDown);
		Block_FormActivate = false;
		DateLine = null;
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
		//IL_000b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0011: Expected O, but got Unknown
		//IL_0011: Unknown result type (might be due to invalid IL or missing references)
		//IL_0017: Expected O, but got Unknown
		//IL_0017: Unknown result type (might be due to invalid IL or missing references)
		//IL_001d: Expected O, but got Unknown
		//IL_001e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0028: Expected O, but got Unknown
		//IL_0029: Unknown result type (might be due to invalid IL or missing references)
		//IL_0033: Expected O, but got Unknown
		//IL_0034: Unknown result type (might be due to invalid IL or missing references)
		//IL_003e: Expected O, but got Unknown
		//IL_003f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0049: Expected O, but got Unknown
		//IL_004a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0054: Expected O, but got Unknown
		//IL_0055: Unknown result type (might be due to invalid IL or missing references)
		//IL_005f: Expected O, but got Unknown
		//IL_0060: Unknown result type (might be due to invalid IL or missing references)
		//IL_006a: Expected O, but got Unknown
		//IL_006b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0075: Expected O, but got Unknown
		//IL_0076: Unknown result type (might be due to invalid IL or missing references)
		//IL_0080: Expected O, but got Unknown
		//IL_0081: Unknown result type (might be due to invalid IL or missing references)
		//IL_008b: Expected O, but got Unknown
		//IL_008c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0096: Expected O, but got Unknown
		//IL_0097: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a1: Expected O, but got Unknown
		//IL_00a2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ac: Expected O, but got Unknown
		//IL_00ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b7: Expected O, but got Unknown
		//IL_00b8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c2: Expected O, but got Unknown
		//IL_00c3: Unknown result type (might be due to invalid IL or missing references)
		//IL_00cd: Expected O, but got Unknown
		//IL_00ce: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d8: Expected O, but got Unknown
		//IL_00d9: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e3: Expected O, but got Unknown
		//IL_00e4: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ee: Expected O, but got Unknown
		//IL_00ef: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f9: Expected O, but got Unknown
		//IL_00fa: Unknown result type (might be due to invalid IL or missing references)
		//IL_0104: Expected O, but got Unknown
		//IL_0105: Unknown result type (might be due to invalid IL or missing references)
		//IL_010f: Expected O, but got Unknown
		//IL_0110: Unknown result type (might be due to invalid IL or missing references)
		//IL_011a: Expected O, but got Unknown
		//IL_011b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0125: Expected O, but got Unknown
		//IL_0126: Unknown result type (might be due to invalid IL or missing references)
		//IL_0130: Expected O, but got Unknown
		//IL_0131: Unknown result type (might be due to invalid IL or missing references)
		//IL_013b: Expected O, but got Unknown
		//IL_013c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0146: Expected O, but got Unknown
		//IL_0147: Unknown result type (might be due to invalid IL or missing references)
		//IL_0151: Expected O, but got Unknown
		//IL_0152: Unknown result type (might be due to invalid IL or missing references)
		//IL_015c: Expected O, but got Unknown
		//IL_015d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0167: Expected O, but got Unknown
		//IL_0168: Unknown result type (might be due to invalid IL or missing references)
		//IL_0172: Expected O, but got Unknown
		//IL_0179: Unknown result type (might be due to invalid IL or missing references)
		//IL_0183: Expected O, but got Unknown
		//IL_0184: Unknown result type (might be due to invalid IL or missing references)
		//IL_018e: Expected O, but got Unknown
		//IL_018f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0199: Expected O, but got Unknown
		//IL_019a: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a4: Expected O, but got Unknown
		//IL_03bb: Unknown result type (might be due to invalid IL or missing references)
		components = new Container();
		ChartArea val = new ChartArea();
		Series val2 = new Series();
		Series val3 = new Series();
		Panel1 = new Panel();
		Chart1 = new Chart();
		ListBox1 = new ListBox();
		BrowseButton = new Button();
		HelpButton1 = new Button();
		DoneButton = new Button();
		GroupBox2 = new GroupBox();
		DateTimeCheckBox = new CheckBox();
		AdjCloseTextBox = new MaskedTextBox();
		VolumeTextBox = new MaskedTextBox();
		CloseTextBox = new MaskedTextBox();
		LowTextBox = new MaskedTextBox();
		HighTextBox = new MaskedTextBox();
		OpenTextBox = new MaskedTextBox();
		TimeTextBox = new MaskedTextBox();
		DateTextBox = new MaskedTextBox();
		TimeCheckBox = new CheckBox();
		OpenCheckBox = new CheckBox();
		VolumeCheckBox = new CheckBox();
		AdjCloseCheckBox = new CheckBox();
		Label2 = new Label();
		Label3 = new Label();
		Label4 = new Label();
		Label5 = new Label();
		SaveFileFormatButton = new Button();
		FolderBrowserDialog1 = new FolderBrowserDialog();
		GraphButton = new Button();
		FileLabel = new Label();
		DataGridView1 = new DataGridView();
		sDateFormatCombo = new ComboBox();
		Label6 = new Label();
		ToolTip1 = new ToolTip(components);
		LoadingBar = new ProgressBar();
		Label7 = new Label();
		Label1 = new Label();
		((Control)Panel1).SuspendLayout();
		((ISupportInitialize)Chart1).BeginInit();
		((Control)GroupBox2).SuspendLayout();
		((ISupportInitialize)DataGridView1).BeginInit();
		((Control)this).SuspendLayout();
		((Control)Panel1).Anchor = (AnchorStyles)13;
		Panel1.BorderStyle = (BorderStyle)2;
		((Control)Panel1).Controls.Add((Control)(object)Chart1);
		((Control)Panel1).Controls.Add((Control)(object)ListBox1);
		((Control)Panel1).Location = new Point(12, 12);
		((Control)Panel1).Name = "Panel1";
		((Control)Panel1).Size = new Size(521, 301);
		((Control)Panel1).TabIndex = 1;
		((Control)Chart1).Anchor = (AnchorStyles)15;
		val.AxisX.Enabled = (AxisEnabled)1;
		val.AxisX.IntervalAutoMode = (IntervalAutoMode)1;
		val.AxisX.LabelAutoFitMaxFontSize = 6;
		val.AxisX.MajorGrid.Enabled = false;
		((Grid)val.AxisX.MajorTickMark).Interval = 0.0;
		val.AxisX2.Enabled = (AxisEnabled)2;
		val.AxisY.Enabled = (AxisEnabled)2;
		val.AxisY2.Enabled = (AxisEnabled)1;
		val.AxisY2.IsMarginVisible = false;
		val.AxisY2.IsMarksNextToAxis = false;
		val.AxisY2.LabelAutoFitMaxFontSize = 6;
		val.AxisY2.MajorGrid.Interval = 0.0;
		val.AxisY2.MajorGrid.IntervalOffsetType = (DateTimeIntervalType)0;
		val.AxisY2.MajorGrid.IntervalType = (DateTimeIntervalType)1;
		val.BorderDashStyle = (ChartDashStyle)5;
		val.Name = "ChartArea1";
		val.Position.Auto = false;
		val.Position.Height = 98f;
		val.Position.Width = 98f;
		val.Position.Y = 1f;
		((Collection<ChartArea>)(object)Chart1.ChartAreas).Add(val);
		((Control)Chart1).Location = new Point(4, 0);
		((Control)Chart1).Margin = new Padding(0);
		((Control)Chart1).Name = "Chart1";
		((DataPointCustomProperties)val2).BorderColor = Color.Black;
		val2.ChartArea = "ChartArea1";
		val2.ChartType = (SeriesChartType)20;
		((DataPointCustomProperties)val2).CustomProperties = "PriceDownColor=Red, PriceUpColor=green";
		val2.IsXValueIndexed = true;
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
		((Collection<Series>)(object)Chart1.Series).Add(val2);
		((Collection<Series>)(object)Chart1.Series).Add(val3);
		Chart1.Size = new Size(510, 157);
		Chart1.SuppressExceptions = true;
		((Control)Chart1).TabIndex = 0;
		((Control)Chart1).Text = "Chart1";
		((Control)ListBox1).Anchor = (AnchorStyles)15;
		((Control)ListBox1).CausesValidation = false;
		ListBox1.HorizontalScrollbar = true;
		((Control)ListBox1).Location = new Point(3, 160);
		ListBox1.MultiColumn = true;
		((Control)ListBox1).Name = "ListBox1";
		((Control)ListBox1).Size = new Size(511, 134);
		ListBox1.Sorted = true;
		((Control)ListBox1).TabIndex = 1;
		((Control)BrowseButton).Anchor = (AnchorStyles)10;
		((Control)BrowseButton).Location = new Point(357, 643);
		((Control)BrowseButton).Name = "BrowseButton";
		((Control)BrowseButton).Size = new Size(75, 23);
		((Control)BrowseButton).TabIndex = 11;
		((ButtonBase)BrowseButton).Text = "&Browse";
		((ButtonBase)BrowseButton).UseVisualStyleBackColor = true;
		((Control)HelpButton1).Anchor = (AnchorStyles)10;
		((Control)HelpButton1).Location = new Point(438, 643);
		((Control)HelpButton1).Name = "HelpButton1";
		((Control)HelpButton1).Size = new Size(75, 23);
		((Control)HelpButton1).TabIndex = 12;
		((ButtonBase)HelpButton1).Text = "&Help";
		((ButtonBase)HelpButton1).UseVisualStyleBackColor = true;
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(438, 672);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(75, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)GroupBox2).Controls.Add((Control)(object)DateTimeCheckBox);
		((Control)GroupBox2).Controls.Add((Control)(object)AdjCloseTextBox);
		((Control)GroupBox2).Controls.Add((Control)(object)VolumeTextBox);
		((Control)GroupBox2).Controls.Add((Control)(object)CloseTextBox);
		((Control)GroupBox2).Controls.Add((Control)(object)LowTextBox);
		((Control)GroupBox2).Controls.Add((Control)(object)HighTextBox);
		((Control)GroupBox2).Controls.Add((Control)(object)OpenTextBox);
		((Control)GroupBox2).Controls.Add((Control)(object)TimeTextBox);
		((Control)GroupBox2).Controls.Add((Control)(object)DateTextBox);
		((Control)GroupBox2).Controls.Add((Control)(object)TimeCheckBox);
		((Control)GroupBox2).Controls.Add((Control)(object)OpenCheckBox);
		((Control)GroupBox2).Controls.Add((Control)(object)VolumeCheckBox);
		((Control)GroupBox2).Controls.Add((Control)(object)AdjCloseCheckBox);
		((Control)GroupBox2).Controls.Add((Control)(object)Label2);
		((Control)GroupBox2).Controls.Add((Control)(object)Label3);
		((Control)GroupBox2).Controls.Add((Control)(object)Label4);
		((Control)GroupBox2).Controls.Add((Control)(object)Label5);
		((Control)GroupBox2).Location = new Point(12, 518);
		((Control)GroupBox2).Name = "GroupBox2";
		((Control)GroupBox2).Size = new Size(238, 182);
		((Control)GroupBox2).TabIndex = 4;
		GroupBox2.TabStop = false;
		GroupBox2.Text = "Column Order";
		((ButtonBase)DateTimeCheckBox).AutoSize = true;
		((Control)DateTimeCheckBox).Location = new Point(148, 25);
		((Control)DateTimeCheckBox).Name = "DateTimeCheckBox";
		((Control)DateTimeCheckBox).Size = new Size(84, 17);
		((Control)DateTimeCheckBox).TabIndex = 2;
		((ButtonBase)DateTimeCheckBox).Text = "Date && &Time";
		((ButtonBase)DateTimeCheckBox).UseVisualStyleBackColor = true;
		((TextBoxBase)AdjCloseTextBox).BorderStyle = (BorderStyle)0;
		((Control)AdjCloseTextBox).Location = new Point(11, 159);
		AdjCloseTextBox.Mask = "00";
		((Control)AdjCloseTextBox).Name = "AdjCloseTextBox";
		AdjCloseTextBox.PromptChar = ' ';
		((Control)AdjCloseTextBox).Size = new Size(13, 13);
		((Control)AdjCloseTextBox).TabIndex = 15;
		AdjCloseTextBox.Text = "08";
		((TextBoxBase)VolumeTextBox).BorderStyle = (BorderStyle)0;
		((Control)VolumeTextBox).Location = new Point(11, 141);
		VolumeTextBox.Mask = "00";
		((Control)VolumeTextBox).Name = "VolumeTextBox";
		VolumeTextBox.PromptChar = ' ';
		((Control)VolumeTextBox).Size = new Size(13, 13);
		((Control)VolumeTextBox).TabIndex = 13;
		VolumeTextBox.Text = "07";
		((TextBoxBase)CloseTextBox).BorderStyle = (BorderStyle)0;
		((Control)CloseTextBox).Location = new Point(11, 121);
		CloseTextBox.Mask = "00";
		((Control)CloseTextBox).Name = "CloseTextBox";
		CloseTextBox.PromptChar = ' ';
		((Control)CloseTextBox).Size = new Size(13, 13);
		((Control)CloseTextBox).TabIndex = 11;
		CloseTextBox.Text = "06";
		((TextBoxBase)LowTextBox).BorderStyle = (BorderStyle)0;
		((Control)LowTextBox).Location = new Point(11, 103);
		LowTextBox.Mask = "00";
		((Control)LowTextBox).Name = "LowTextBox";
		LowTextBox.PromptChar = ' ';
		((Control)LowTextBox).Size = new Size(13, 13);
		((Control)LowTextBox).TabIndex = 9;
		LowTextBox.Text = "05";
		((TextBoxBase)HighTextBox).BorderStyle = (BorderStyle)0;
		((Control)HighTextBox).Location = new Point(11, 84);
		HighTextBox.Mask = "00";
		((Control)HighTextBox).Name = "HighTextBox";
		HighTextBox.PromptChar = ' ';
		((Control)HighTextBox).Size = new Size(13, 13);
		((Control)HighTextBox).TabIndex = 7;
		HighTextBox.Text = "04";
		((TextBoxBase)OpenTextBox).BorderStyle = (BorderStyle)0;
		((Control)OpenTextBox).Location = new Point(11, 65);
		OpenTextBox.Mask = "00";
		((Control)OpenTextBox).Name = "OpenTextBox";
		OpenTextBox.PromptChar = ' ';
		((Control)OpenTextBox).Size = new Size(13, 13);
		((Control)OpenTextBox).TabIndex = 5;
		OpenTextBox.Text = "03";
		((TextBoxBase)TimeTextBox).BorderStyle = (BorderStyle)0;
		((Control)TimeTextBox).Location = new Point(11, 46);
		TimeTextBox.Mask = "00";
		((Control)TimeTextBox).Name = "TimeTextBox";
		TimeTextBox.PromptChar = ' ';
		((Control)TimeTextBox).Size = new Size(13, 13);
		((Control)TimeTextBox).TabIndex = 3;
		TimeTextBox.Text = "02";
		((TextBoxBase)DateTextBox).BorderStyle = (BorderStyle)0;
		((Control)DateTextBox).Location = new Point(11, 26);
		DateTextBox.Mask = "00";
		((Control)DateTextBox).Name = "DateTextBox";
		DateTextBox.PromptChar = ' ';
		((Control)DateTextBox).Size = new Size(13, 13);
		((Control)DateTextBox).TabIndex = 0;
		DateTextBox.Text = "01";
		((ButtonBase)TimeCheckBox).AutoSize = true;
		((Control)TimeCheckBox).Location = new Point(37, 44);
		((Control)TimeCheckBox).Name = "TimeCheckBox";
		((Control)TimeCheckBox).Size = new Size(158, 17);
		((Control)TimeCheckBox).TabIndex = 4;
		((ButtonBase)TimeCheckBox).Text = "&Time (separate column only)";
		((ButtonBase)TimeCheckBox).UseVisualStyleBackColor = true;
		((ButtonBase)OpenCheckBox).AutoSize = true;
		((Control)OpenCheckBox).Location = new Point(37, 63);
		((Control)OpenCheckBox).Name = "OpenCheckBox";
		((Control)OpenCheckBox).Size = new Size(52, 17);
		((Control)OpenCheckBox).TabIndex = 6;
		((ButtonBase)OpenCheckBox).Text = "&Open";
		((ButtonBase)OpenCheckBox).UseVisualStyleBackColor = true;
		((ButtonBase)VolumeCheckBox).AutoSize = true;
		((Control)VolumeCheckBox).Location = new Point(37, 140);
		((Control)VolumeCheckBox).Name = "VolumeCheckBox";
		((Control)VolumeCheckBox).Size = new Size(61, 17);
		((Control)VolumeCheckBox).TabIndex = 14;
		((ButtonBase)VolumeCheckBox).Text = "&Volume";
		((ButtonBase)VolumeCheckBox).UseVisualStyleBackColor = true;
		((ButtonBase)AdjCloseCheckBox).AutoSize = true;
		((Control)AdjCloseCheckBox).Location = new Point(37, 158);
		((Control)AdjCloseCheckBox).Name = "AdjCloseCheckBox";
		((Control)AdjCloseCheckBox).Size = new Size(96, 17);
		((Control)AdjCloseCheckBox).TabIndex = 16;
		((ButtonBase)AdjCloseCheckBox).Text = "Ad&justed Close";
		((ButtonBase)AdjCloseCheckBox).UseVisualStyleBackColor = true;
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(34, 26);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(103, 13);
		((Control)Label2).TabIndex = 1;
		Label2.Text = "D&ate or Date && Time";
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(34, 84);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(29, 13);
		((Control)Label3).TabIndex = 8;
		Label3.Text = "H&igh";
		Label4.AutoSize = true;
		((Control)Label4).Location = new Point(34, 103);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(27, 13);
		((Control)Label4).TabIndex = 10;
		Label4.Text = "&Low";
		Label5.AutoSize = true;
		((Control)Label5).Location = new Point(34, 121);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(33, 13);
		((Control)Label5).TabIndex = 12;
		Label5.Text = "&Close";
		((Control)SaveFileFormatButton).Anchor = (AnchorStyles)10;
		((Control)SaveFileFormatButton).Location = new Point(357, 672);
		((Control)SaveFileFormatButton).Name = "SaveFileFormatButton";
		((Control)SaveFileFormatButton).Size = new Size(75, 23);
		((Control)SaveFileFormatButton).TabIndex = 13;
		((ButtonBase)SaveFileFormatButton).Text = "&Save";
		((ButtonBase)SaveFileFormatButton).UseVisualStyleBackColor = true;
		((Control)GraphButton).Anchor = (AnchorStyles)10;
		((Control)GraphButton).Location = new Point(276, 643);
		((Control)GraphButton).Name = "GraphButton";
		((Control)GraphButton).Size = new Size(75, 23);
		((Control)GraphButton).TabIndex = 10;
		((ButtonBase)GraphButton).Text = "&Graph";
		((ButtonBase)GraphButton).UseVisualStyleBackColor = true;
		((Control)FileLabel).Anchor = (AnchorStyles)13;
		FileLabel.BorderStyle = (BorderStyle)2;
		((Control)FileLabel).Location = new Point(12, 316);
		((Control)FileLabel).Name = "FileLabel";
		((Control)FileLabel).Size = new Size(521, 64);
		((Control)FileLabel).TabIndex = 2;
		DataGridView1.AllowUserToAddRows = false;
		DataGridView1.AllowUserToDeleteRows = false;
		DataGridView1.AllowUserToResizeColumns = false;
		DataGridView1.AllowUserToResizeRows = false;
		((Control)DataGridView1).Anchor = (AnchorStyles)13;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)10;
		DataGridView1.AutoSizeRowsMode = (DataGridViewAutoSizeRowsMode)11;
		((Control)DataGridView1).CausesValidation = false;
		DataGridView1.ColumnHeadersHeightSizeMode = (DataGridViewColumnHeadersHeightSizeMode)2;
		DataGridView1.EditMode = (DataGridViewEditMode)4;
		((Control)DataGridView1).Location = new Point(12, 383);
		DataGridView1.MultiSelect = false;
		((Control)DataGridView1).Name = "DataGridView1";
		DataGridView1.ReadOnly = true;
		DataGridView1.RowTemplate.ReadOnly = true;
		DataGridView1.RowTemplate.Resizable = (DataGridViewTriState)1;
		DataGridView1.SelectionMode = (DataGridViewSelectionMode)1;
		DataGridView1.ShowCellErrors = false;
		DataGridView1.ShowCellToolTips = false;
		DataGridView1.ShowEditingIcon = false;
		DataGridView1.ShowRowErrors = false;
		((Control)DataGridView1).Size = new Size(521, 129);
		((Control)DataGridView1).TabIndex = 3;
		((Control)sDateFormatCombo).Anchor = (AnchorStyles)10;
		((ListControl)sDateFormatCombo).FormattingEnabled = true;
		sDateFormatCombo.Items.AddRange(new object[40]
		{
			"MM/dd/yyyy", "MM-dd-yyyy", "MM.dd.yyyy", "M/d/yyyy", "M-d-yyyy", "M.d.yyyy", "dd/MM/yyyy", "dd-MM-yyyy", "dd.MM.yyyy", "d/M/yyyy",
			"d-M-yyyy", "d.M.yyyy", "yyyy/MM/dd", "yyyy-MM-dd", "yyyy.MM.dd", "yyyy/M/d", "yyyy-M-d", "yyyy.M.d", "yyyyMMdd", "yyyyMd",
			"MM/dd/yy", "MM-dd-yy", "MM.dd.yy", "M/d/yy", "M-d-yy", "M.d.yy", "dd/MM/yy", "dd-MM-yy", "dd.MM.yy", "d/M/yy",
			"d-M-yy", "d.M.yy", "yy/MM/dd", "yy-MM-dd", "yy.MM.dd", "yy/M/d", "yy-M-d", "yy.M.d", "yyMMdd", "yyMd"
		});
		((Control)sDateFormatCombo).Location = new Point(370, 605);
		((Control)sDateFormatCombo).Name = "sDateFormatCombo";
		((Control)sDateFormatCombo).Size = new Size(121, 21);
		((Control)sDateFormatCombo).TabIndex = 9;
		((Control)Label6).Anchor = (AnchorStyles)10;
		Label6.AutoSize = true;
		((Control)Label6).Location = new Point(299, 609);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(65, 13);
		((Control)Label6).TabIndex = 8;
		Label6.Text = "Date &format:";
		((Control)LoadingBar).Anchor = (AnchorStyles)10;
		((Control)LoadingBar).ForeColor = Color.Green;
		((Control)LoadingBar).Location = new Point(370, 581);
		((Control)LoadingBar).Name = "LoadingBar";
		((Control)LoadingBar).Size = new Size(121, 18);
		((Control)LoadingBar).TabIndex = 7;
		((Control)Label7).Anchor = (AnchorStyles)10;
		Label7.AutoSize = true;
		((Control)Label7).Location = new Point(316, 585);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(48, 13);
		((Control)Label7).TabIndex = 6;
		Label7.Text = "Loading:";
		((Control)Label1).Anchor = (AnchorStyles)10;
		((Control)Label1).Location = new Point(256, 518);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(277, 62);
		((Control)Label1).TabIndex = 5;
		Label1.Text = "If you see a big red X on the chart, it means your column choices broke the chart. You'll need to exit the program and try again to get the chart to work.";
		((Form)this).AcceptButton = (IButtonControl)(object)GraphButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(545, 709);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)Label7);
		((Control)this).Controls.Add((Control)(object)LoadingBar);
		((Control)this).Controls.Add((Control)(object)Label6);
		((Control)this).Controls.Add((Control)(object)sDateFormatCombo);
		((Control)this).Controls.Add((Control)(object)DataGridView1);
		((Control)this).Controls.Add((Control)(object)HelpButton1);
		((Control)this).Controls.Add((Control)(object)FileLabel);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)GraphButton);
		((Control)this).Controls.Add((Control)(object)GroupBox2);
		((Control)this).Controls.Add((Control)(object)SaveFileFormatButton);
		((Control)this).Controls.Add((Control)(object)BrowseButton);
		((Control)this).Controls.Add((Control)(object)Panel1);
		((Form)this).KeyPreview = true;
		((Control)this).Name = "FileFormatForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "File Format Form";
		((Control)Panel1).ResumeLayout(false);
		((ISupportInitialize)Chart1).EndInit();
		((Control)GroupBox2).ResumeLayout(false);
		((Control)GroupBox2).PerformLayout();
		((ISupportInitialize)DataGridView1).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void FileFormatForm_Closing(object sender, CancelEventArgs e)
	{
		//IL_0075: Unknown result type (might be due to invalid IL or missing references)
		//IL_007b: Invalid comparison between Unknown and I4
		GlobalForm.ChartPeriodShown = lsChartPeriodShown;
		GlobalForm.ChartVolume = lsVolumeChecked;
		GlobalForm.ffDateTimeFormat = DateTimeCheckBox.Checked;
		if (Operators.CompareString(sDateFormatCombo.Text, "", false) == 0)
		{
			sDateFormatCombo.Text = "yyyy-MM-dd";
			GlobalForm.UserDate = "yyyy-MM-dd";
			SaveNeeded = true;
		}
		if (SaveNeeded && (int)MessageBox.Show("Did you want to save the changes?", "Patternz: ThePatternSite.com", (MessageBoxButtons)4, (MessageBoxIcon)32, (MessageBoxDefaultButton)0) == 6)
		{
			SaveInformation(RuntimeHelpers.GetObjectValue(sender), e);
		}
		Block_FormActivate = false;
	}

	private void FileFormatForm_Load(object sender, EventArgs e)
	{
		//IL_0024: Unknown result type (might be due to invalid IL or missing references)
		//IL_0029: Unknown result type (might be due to invalid IL or missing references)
		//IL_0034: Unknown result type (might be due to invalid IL or missing references)
		//IL_003f: Unknown result type (might be due to invalid IL or missing references)
		//IL_004a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0051: Unknown result type (might be due to invalid IL or missing references)
		//IL_0062: Unknown result type (might be due to invalid IL or missing references)
		//IL_0073: Unknown result type (might be due to invalid IL or missing references)
		//IL_0084: Unknown result type (might be due to invalid IL or missing references)
		//IL_0095: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a6: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d9: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ea: Unknown result type (might be due to invalid IL or missing references)
		//IL_00fb: Unknown result type (might be due to invalid IL or missing references)
		//IL_010c: Unknown result type (might be due to invalid IL or missing references)
		//IL_011d: Unknown result type (might be due to invalid IL or missing references)
		//IL_012e: Unknown result type (might be due to invalid IL or missing references)
		//IL_013f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0150: Unknown result type (might be due to invalid IL or missing references)
		//IL_0161: Unknown result type (might be due to invalid IL or missing references)
		//IL_0172: Unknown result type (might be due to invalid IL or missing references)
		//IL_0183: Unknown result type (might be due to invalid IL or missing references)
		//IL_02de: Unknown result type (might be due to invalid IL or missing references)
		LockFlag = true;
		EnableDisable(Flag: false);
		lsChartPeriodShown = GlobalForm.ChartPeriodShown;
		lsVolumeChecked = GlobalForm.ChartVolume;
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)GraphButton, "Chart the file.");
		val.SetToolTip((Control)(object)BrowseButton, "Locate files containing stock quotes for use by Patternz.");
		val.SetToolTip((Control)(object)SaveFileFormatButton, "Save any changes.");
		val.SetToolTip((Control)(object)HelpButton1, "Get help.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)sDateFormatCombo, "Select the date format that matches the format displayed in the files.");
		val.SetToolTip((Control)(object)TimeCheckBox, "Check this box if the files include time information in its own column.");
		val.SetToolTip((Control)(object)OpenCheckBox, "Check this box if the files include an opening price.");
		val.SetToolTip((Control)(object)VolumeCheckBox, "Check this box if the files includes volume data.");
		val.SetToolTip((Control)(object)AdjCloseCheckBox, "Check this box if the files include adjusted close information.");
		val.SetToolTip((Control)(object)DateTextBox, "Tells the column order where the date appears in the file.");
		val.SetToolTip((Control)(object)DateTimeCheckBox, "Check if both date and time occur in the same column in the file.");
		val.SetToolTip((Control)(object)TimeTextBox, "Tells the column order where the time appears in the file.");
		val.SetToolTip((Control)(object)OpenTextBox, "Tells the column order where the opening price appears in the file.");
		val.SetToolTip((Control)(object)HighTextBox, "Tells the column order where the high price appears in the file.");
		val.SetToolTip((Control)(object)LowTextBox, "Tells the column order where the low price appears in the file.");
		val.SetToolTip((Control)(object)CloseTextBox, "Tells the column order where the closing price appears in the file.");
		val.SetToolTip((Control)(object)VolumeTextBox, "Tells the column order where volume appears in the file.");
		val.SetToolTip((Control)(object)AdjCloseTextBox, "Tells the column order where the adjusted close appears in the file.");
		val.SetToolTip((Control)(object)ListBox1, "Click on a file to view.");
		TimeCheckBox.Checked = GlobalForm.ckFileFormat[1];
		OpenCheckBox.Checked = GlobalForm.ckFileFormat[2];
		VolumeCheckBox.Checked = GlobalForm.ckFileFormat[6];
		GlobalForm.ChartVolume = VolumeCheckBox.Checked;
		AdjCloseCheckBox.Checked = GlobalForm.ckFileFormat[7];
		DateTextBox.Text = Conversions.ToString(GlobalForm.FileFormat[0]);
		TimeTextBox.Text = Conversions.ToString(GlobalForm.FileFormat[1]);
		OpenTextBox.Text = Conversions.ToString(GlobalForm.FileFormat[2]);
		HighTextBox.Text = Conversions.ToString(GlobalForm.FileFormat[3]);
		LowTextBox.Text = Conversions.ToString(GlobalForm.FileFormat[4]);
		CloseTextBox.Text = Conversions.ToString(GlobalForm.FileFormat[5]);
		VolumeTextBox.Text = Conversions.ToString(GlobalForm.FileFormat[6]);
		AdjCloseTextBox.Text = Conversions.ToString(GlobalForm.FileFormat[7]);
		DateTimeCheckBox.Checked = GlobalForm.ffDateTimeFormat;
		FillGrid(Flag: false);
		DisplayFiles();
		MessageBox.Show("This form is no longer needed by the program unless you provide your own data (such as Metastock users who provide their own .csv files or if you choose to manually downlod .csv files from a quote provider).\r\n\r\nIt is included here for advanced users with quote files that did not, or will not, come from the Update Form.\r\n\r\nIf you use File Format, then do NOT use Update. Similarly, if you use the Update Form to get your quote data, then don't use File Format!", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void FileFormatForm_Activated(object sender, EventArgs e)
	{
		((Control)this).Refresh();
		if (Block_FormActivate)
		{
			return;
		}
		Block_FormActivate = true;
		sDateFormatCombo.Text = GlobalForm.UserDate;
		TempsDateFormat = GlobalForm.UserDate;
		if (MyProject.Forms.Mainform.ListBox1.Items.Count > 0)
		{
			if (MyProject.Forms.Mainform.ListBox1.SelectedIndex != -1)
			{
				ListBox1.SetSelected(MyProject.Forms.Mainform.ListBox1.SelectedIndex, true);
			}
			else
			{
				ListBox1.SetSelected(0, true);
			}
		}
		SaveNeeded = false;
		LockFlag = false;
		EnableDisable(Flag: true);
	}

	private void AdjCloseCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		if (!AdjCloseCheckBox.Checked)
		{
			AdjCloseTextBox.Text = "0";
		}
		else
		{
			AdjCloseTextBox.Text = GetMaxTB();
		}
		SaveNeeded = true;
	}

	private void BrowseButton_Click(object sender, EventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_000b: Expected O, but got Unknown
		//IL_0021: Unknown result type (might be due to invalid IL or missing references)
		//IL_0027: Invalid comparison between Unknown and I4
		FolderBrowserDialog1 = new FolderBrowserDialog();
		FolderBrowserDialog1.Description = "Select the path to the stock files you'd like to open.";
		if ((int)((CommonDialog)FolderBrowserDialog1).ShowDialog() == 1)
		{
			GlobalForm.PathChanged = true;
			GlobalForm.OpenPath = FolderBrowserDialog1.SelectedPath;
			DisplayFiles();
		}
	}

	private void Chart1_MouseDown(object sender, MouseEventArgs e)
	{
		GlobalForm.ShowQuoteInfo(Chart1, e);
	}

	private void Chart1_MouseUp(object sender, MouseEventArgs e)
	{
		GlobalForm.ReleaseQuoteInfo(Chart1, e);
	}

	private void ClearChartGrid(int Flag)
	{
		//IL_0105: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			switch (Flag)
			{
			case 0:
				ClearChartGrid(1);
				ClearChartGrid(2);
				ClearChartGrid(3);
				break;
			case 1:
				if (((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Count > 0)
				{
					((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Clear();
				}
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Clear();
				((Collection<Title>)(object)Chart1.Titles).Clear();
				break;
			case 2:
				try
				{
					int num = DataGridView1.RowCount - 1;
					for (int i = 1; i <= num; i++)
					{
						DataGridView1.Rows.RemoveAt(1);
					}
					if (DataGridView1.RowCount == 1)
					{
						DataGridView1.Columns.Clear();
					}
					break;
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					MessageBox.Show(ex2.Message, "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)16);
					ProjectData.ClearProjectError();
					break;
				}
			case 3:
				FileLabel.Text = "";
				break;
			case 4:
				ClearChartGrid(1);
				ClearChartGrid(2);
				break;
			}
		}
	}

	private void sDateFormatCombo_FormatStringChanged(object sender, EventArgs e)
	{
		if (!LockFlag)
		{
			SaveNeeded = true;
		}
	}

	private void sDateFormatCombo_LostFocus(object sender, EventArgs e)
	{
		//IL_0124: Unknown result type (might be due to invalid IL or missing references)
		string text = "The date format does not agree with what I read in (the date has a slash, dash, or period and the other date doesn't: \r\n\r\n" + TempsDateFormat + " versus \r\n" + DateLine + ").\r\n\r\nIt could lead to reading errors.";
		TempsDateFormat = FixTime();
		if (((Strings.InStr(TempsDateFormat, "/", (CompareMethod)0) != 0) & (Strings.InStr(DateLine, "/", (CompareMethod)0) == 0)) | ((Strings.InStr(TempsDateFormat, "-", (CompareMethod)0) != 0) & (Strings.InStr(DateLine, "-", (CompareMethod)0) == 0)) | ((Strings.InStr(TempsDateFormat, ".", (CompareMethod)0) != 0) & (Strings.InStr(DateLine, ".", (CompareMethod)0) == 0)))
		{
			((Control)FileLabel).ForeColor = Color.FromName("red");
			((Control)Label1).ForeColor = Color.FromName("red");
			Label1.Text = "Date format error: " + TempsDateFormat + " versus " + DateLine;
			MessageBox.Show(text + " Please correct.", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)16);
		}
		else
		{
			((Control)Label1).ForeColor = Color.FromName("black");
			Label1.Text = null;
			((Control)FileLabel).ForeColor = Color.FromName("black");
		}
	}

	private void sDateFormatCombo_Validating(object sender, CancelEventArgs e)
	{
		//IL_0225: Unknown result type (might be due to invalid IL or missing references)
		int num = 1;
		if (sDateFormatCombo.Text.Length == 0)
		{
			sDateFormatCombo.Text = Conversions.ToString(Interaction.IIf(GlobalForm.IntradayData, (object)"yyyy-MM-dd HH:mm", (object)"yyyy-MM-dd"));
			Label1.Text = "The date format is empty so I'm replacing it.";
			((Control)Label1).ForeColor = Color.FromName("red");
			Interaction.Beep();
			return;
		}
		do
		{
			string text = Strings.Mid(sDateFormatCombo.Text, num, 1);
			switch (text)
			{
			default:
				if (Operators.CompareString(text, "h", false) == 0)
				{
					sDateFormatCombo.Text = sDateFormatCombo.Text.Replace("h", "H");
					break;
				}
				MessageBox.Show("Please be careful changing the date/time format. You can crash the program if you get it wrong. They key you entered is not allowed.", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)16);
				return;
			case "y":
			case "M":
			case "d":
			case "-":
			case "/":
			case ".":
			case null:
			case "":
			case "H":
			case ":":
			case "m":
			case " ":
				break;
			}
			num = checked(num + 1);
		}
		while (num <= Strings.Len(sDateFormatCombo.Text));
	}

	private void DateTextBox_LostFocus(object sender, EventArgs e)
	{
		WreckCheck(RuntimeHelpers.GetObjectValue(sender), e);
	}

	private void DateTextBox_TextChanged(object sender, EventArgs e)
	{
		SaveNeeded = true;
	}

	private void DisplayFiles()
	{
		if (Operators.CompareString(GlobalForm.OpenPath, "", false) != 0)
		{
			ListBox1.Items.Clear();
			string[] files = Directory.GetFiles(GlobalForm.OpenPath, "*.txt");
			foreach (string path in files)
			{
				ListBox1.Items.Add((object)Path.GetFileName(path));
			}
			string[] files2 = Directory.GetFiles(GlobalForm.OpenPath, "*.csv");
			foreach (string path2 in files2)
			{
				ListBox1.Items.Add((object)Path.GetFileName(path2));
			}
		}
		else
		{
			BrowseButton.PerformClick();
			if (Operators.CompareString(GlobalForm.OpenPath, "", false) != 0)
			{
				DisplayFiles();
			}
		}
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void EnableDisable(bool Flag)
	{
		((Control)AdjCloseCheckBox).Enabled = Flag;
		((Control)AdjCloseTextBox).Enabled = Flag;
		((Control)BrowseButton).Enabled = Flag;
		((Control)Chart1).Enabled = Flag;
		((Control)CloseTextBox).Enabled = Flag;
		((Control)DataGridView1).Enabled = Flag;
		((Control)DateTextBox).Enabled = Flag;
		((Control)DateTimeCheckBox).Enabled = Flag;
		((Control)DoneButton).Enabled = Flag;
		((Control)GraphButton).Enabled = Flag;
		((Control)HelpButton1).Enabled = Flag;
		((Control)HighTextBox).Enabled = Flag;
		((Control)ListBox1).Enabled = Flag;
		((Control)LowTextBox).Enabled = Flag;
		((Control)OpenCheckBox).Enabled = Flag;
		((Control)OpenTextBox).Enabled = Flag;
		((Control)SaveFileFormatButton).Enabled = Flag;
		((Control)sDateFormatCombo).Enabled = Flag;
		((Control)TimeCheckBox).Enabled = Flag;
		((Control)TimeTextBox).Enabled = Flag;
		((Control)VolumeCheckBox).Enabled = Flag;
		((Control)VolumeTextBox).Enabled = Flag;
		((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
	}

	private void FileFormatForm_KeyDown(object sender, KeyEventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_0008: Invalid comparison between Unknown and I4
		if ((int)e.KeyCode == 112)
		{
			HelpButton1_Click(RuntimeHelpers.GetObjectValue(sender), (EventArgs)(object)e);
		}
	}

	private void FillGrid(bool Flag)
	{
		//IL_02af: Unknown result type (might be due to invalid IL or missing references)
		int num = 0;
		int num2 = 0;
		ClearChartGrid(2);
		DataGridView1.RowHeadersVisible = false;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)1;
		checked
		{
			try
			{
				DataGridView1.ColumnCount = 4 + Conversions.ToInteger(Interaction.IIf(GlobalForm.ckFileFormat[1], (object)1, (object)0)) + Conversions.ToInteger(Interaction.IIf(GlobalForm.ckFileFormat[2], (object)1, (object)0)) + Conversions.ToInteger(Interaction.IIf(GlobalForm.ckFileFormat[6], (object)1, (object)0)) + Conversions.ToInteger(Interaction.IIf(GlobalForm.ckFileFormat[7], (object)1, (object)0));
				int num3 = Information.UBound((Array)GlobalForm.FileFormat, 1);
				for (int i = 0; i <= num3; i++)
				{
					num2 = Conversions.ToInteger(Interaction.IIf(GlobalForm.FileFormat[i] > num2, (object)GlobalForm.FileFormat[i], (object)num2));
				}
				num = 0;
				int num4 = num2;
				for (int i = 0; i <= num4; i++)
				{
					int num5 = i;
					if (num5 == GlobalForm.FileFormat[0])
					{
						DataGridView1.Columns[num].Name = "Date";
						num++;
					}
					else if (num5 == GlobalForm.FileFormat[1])
					{
						if (GlobalForm.ckFileFormat[1])
						{
							DataGridView1.Columns[num].Name = "Time";
							num++;
						}
					}
					else if (num5 == GlobalForm.FileFormat[2])
					{
						if (GlobalForm.ckFileFormat[2])
						{
							DataGridView1.Columns[num].Name = "Open";
							num++;
						}
					}
					else if (num5 == GlobalForm.FileFormat[3])
					{
						DataGridView1.Columns[num].Name = "High";
						num++;
					}
					else if (num5 == GlobalForm.FileFormat[4])
					{
						DataGridView1.Columns[num].Name = "Low";
						num++;
					}
					else if (num5 == GlobalForm.FileFormat[5])
					{
						DataGridView1.Columns[num].Name = "Close";
						num++;
					}
					else if (num5 == GlobalForm.FileFormat[6])
					{
						if (GlobalForm.ckFileFormat[6])
						{
							DataGridView1.Columns[num].Name = "Volume";
							num++;
						}
					}
					else if (num5 == GlobalForm.FileFormat[7] && GlobalForm.ckFileFormat[7])
					{
						DataGridView1.Columns[num].Name = "Adj Close";
						num++;
					}
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				MessageBox.Show("One of the column numbers is likely incorrect.", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)16);
				ProjectData.ClearProjectError();
				return;
			}
			if (Flag)
			{
				int num6 = Conversions.ToInteger(Interaction.IIf(GlobalForm.HLCRange > 9, (object)9, (object)GlobalForm.HLCRange));
				for (int j = 0; j <= num6; j++)
				{
					DataGridView1.Rows.Add();
					num = 0;
					int num7 = num2;
					for (int i = 0; i <= num7; i++)
					{
						int num8 = i;
						if (num8 == GlobalForm.FileFormat[0])
						{
							DataGridView1.Rows[j].Cells[num].Value = Strings.Format((object)GlobalForm.nDT[0, GlobalForm.HLCRange - j], GlobalForm.UserDate);
							num++;
						}
						else if (num8 == GlobalForm.FileFormat[1])
						{
							if (GlobalForm.ckFileFormat[1])
							{
								DataGridView1.Rows[j].Cells[num].Value = Conversions.ToString(GlobalForm.nDT[1, GlobalForm.HLCRange - j]);
								num++;
							}
						}
						else if (num8 == GlobalForm.FileFormat[2])
						{
							if (GlobalForm.ckFileFormat[2])
							{
								DataGridView1.Rows[j].Cells[num].Value = Conversions.ToString(GlobalForm.nHLC[0, GlobalForm.HLCRange - j]);
								num++;
							}
						}
						else if (num8 == GlobalForm.FileFormat[3])
						{
							DataGridView1.Rows[j].Cells[num].Value = Conversions.ToString(GlobalForm.nHLC[1, GlobalForm.HLCRange - j]);
							num++;
						}
						else if (num8 == GlobalForm.FileFormat[4])
						{
							DataGridView1.Rows[j].Cells[num].Value = Conversions.ToString(GlobalForm.nHLC[2, GlobalForm.HLCRange - j]);
							num++;
						}
						else if (num8 == GlobalForm.FileFormat[5])
						{
							DataGridView1.Rows[j].Cells[num].Value = Conversions.ToString(GlobalForm.nHLC[3, GlobalForm.HLCRange - j]);
							num++;
						}
						else if (num8 == GlobalForm.FileFormat[6])
						{
							if (GlobalForm.ckFileFormat[6])
							{
								DataGridView1.Rows[j].Cells[num].Value = Conversions.ToString(GlobalForm.nHLC[4, GlobalForm.HLCRange - j]);
								num++;
							}
						}
						else if (num8 == GlobalForm.FileFormat[7] && GlobalForm.ckFileFormat[7])
						{
							DataGridView1.Rows[j].Cells[num].Value = Conversions.ToString(GlobalForm.nHLC[5, GlobalForm.HLCRange - j]);
							num++;
						}
					}
				}
			}
			int num9 = DataGridView1.ColumnCount - 1;
			for (int i = 0; i <= num9; i++)
			{
				DataGridView1.Columns[i].SortMode = (DataGridViewColumnSortMode)0;
			}
			DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)6;
			DataGridView1.RowHeadersVisible = true;
		}
	}

	private string FixTime()
	{
		string text = sDateFormatCombo.Text;
		if (!TimeCheckBox.Checked & !DateTimeCheckBox.Checked)
		{
			sDateFormatCombo.Text = Strings.Trim(text.Replace("HH:mm", ""));
		}
		else if (Strings.InStr(Strings.UCase(text), "HH:MM", (CompareMethod)0) == 0)
		{
			ComboBox val;
			(val = sDateFormatCombo).Text = val.Text + " HH:mm";
		}
		return sDateFormatCombo.Text;
	}

	private string GetMaxTB()
	{
		//IL_015e: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			if (!LockFlag)
			{
				string text = DateTextBox.Text;
				string text2 = TimeTextBox.Text;
				string text3 = OpenTextBox.Text;
				string text4 = HighTextBox.Text;
				string text5 = LowTextBox.Text;
				string text6 = CloseTextBox.Text;
				string text7 = VolumeTextBox.Text;
				string text8 = AdjCloseTextBox.Text;
				string[] array = new string[8] { text, text2, text3, text4, text5, text6, text7, text8 };
				string[] array2 = array;
				int num = default(int);
				foreach (string text9 in array2)
				{
					num = Conversions.ToInteger(Interaction.IIf(Conversions.ToInteger(text9) > num, (object)Conversions.ToInteger(text9), (object)num));
				}
				if (num + 1 > 99)
				{
					int num2 = Information.UBound((Array)array, 1);
					for (int j = 0; j <= num2; j++)
					{
						bool flag = false;
						string[] array3 = array;
						foreach (string text9 in array3)
						{
							if ((int)Math.Round(Conversion.Val(text9)) == j + 1)
							{
								flag = true;
								break;
							}
						}
						if (!flag)
						{
							num = j;
							break;
						}
					}
				}
				MessageBox.Show("Setting the column number to " + Conversions.ToString(num + 1), "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)64);
				return Conversions.ToString(num + 1);
			}
			return "0";
		}
	}

	private void GraphButton_Click(object sender, EventArgs e)
	{
		//IL_0041: Unknown result type (might be due to invalid IL or missing references)
		int[] array = new int[8];
		bool[] array2 = new bool[8];
		if (ListBox1.Items.Count == 0)
		{
			Interaction.Beep();
			return;
		}
		if (ListBox1.SelectedIndex == -1)
		{
			MessageBox.Show("Please select a symbol to chart and try again.", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)16);
			return;
		}
		WreckCheck(RuntimeHelpers.GetObjectValue(sender), e);
		int num = 0;
		checked
		{
			do
			{
				array[num] = GlobalForm.FileFormat[num];
				array2[num] = GlobalForm.ckFileFormat[num];
				num++;
			}
			while (num <= 7);
			GlobalForm.FileFormat[0] = Conversions.ToInteger(DateTextBox.Text);
			GlobalForm.FileFormat[1] = Conversions.ToInteger(TimeTextBox.Text);
			GlobalForm.FileFormat[2] = Conversions.ToInteger(OpenTextBox.Text);
			GlobalForm.FileFormat[3] = Conversions.ToInteger(HighTextBox.Text);
			GlobalForm.FileFormat[4] = Conversions.ToInteger(LowTextBox.Text);
			GlobalForm.FileFormat[5] = Conversions.ToInteger(CloseTextBox.Text);
			GlobalForm.FileFormat[6] = Conversions.ToInteger(VolumeTextBox.Text);
			GlobalForm.FileFormat[7] = Conversions.ToInteger(AdjCloseTextBox.Text);
			GlobalForm.ckFileFormat[0] = true;
			GlobalForm.ckFileFormat[1] = TimeCheckBox.Checked;
			GlobalForm.ckFileFormat[2] = OpenCheckBox.Checked;
			GlobalForm.ckFileFormat[3] = true;
			GlobalForm.ckFileFormat[4] = true;
			GlobalForm.ckFileFormat[5] = true;
			GlobalForm.ckFileFormat[6] = VolumeCheckBox.Checked;
			GlobalForm.ckFileFormat[7] = AdjCloseCheckBox.Checked;
			string userDate = GlobalForm.UserDate;
			GlobalForm.UserDate = TempsDateFormat;
			bool enabled = ((Control)DoneButton).Enabled;
			if (enabled)
			{
				EnableDisable(Flag: false);
			}
			string? fileName = ListBox1.SelectedItem.ToString();
			ProgressBar ProgBar = LoadingBar;
			Label ErrorLabel = null;
			bool num2 = GlobalForm.LoadFile(fileName, ref ProgBar, ref ErrorLabel, QuickExit: true, 0);
			LoadingBar = ProgBar;
			bool flag = num2;
			if (enabled)
			{
				EnableDisable(Flag: true);
			}
			GlobalForm.SelectChartType(Chart1);
			if (GlobalForm.ErrorCount > 25)
			{
				Label1.Text = "We had more than 25 read errors, so I'm stopping. Probable column order or date format problem.";
				((Control)Label1).ForeColor = Color.FromName("red");
				Interaction.Beep();
			}
			if (!flag)
			{
				GlobalForm.ChartEndIndex = GlobalForm.HLCRange;
				if (GlobalForm.HLCRange > 9)
				{
					GlobalForm.ChartStartIndex = GlobalForm.HLCRange - 9;
					GlobalForm.ShowStock(Chart1, GlobalForm.HLCRange - 9, GlobalForm.HLCRange, VolumeFlag: true, MAFlag: false);
				}
				else
				{
					GlobalForm.ChartStartIndex = 0;
					GlobalForm.ShowStock(Chart1, 0, GlobalForm.HLCRange, VolumeFlag: true, MAFlag: false);
				}
				FillGrid(Flag: true);
			}
			else
			{
				ClearChartGrid(4);
			}
			num = 0;
			do
			{
				GlobalForm.FileFormat[num] = array[num];
				GlobalForm.ckFileFormat[num] = array2[num];
				num++;
			}
			while (num <= 7);
			GlobalForm.UserDate = userDate;
		}
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.FileFormatHelp).ShowDialog();
	}

	private void ListBox1_SelectedIndexChanged(object sender, EventArgs e)
	{
		//IL_0106: Unknown result type (might be due to invalid IL or missing references)
		//IL_0147: Unknown result type (might be due to invalid IL or missing references)
		//IL_004e: Unknown result type (might be due to invalid IL or missing references)
		string text = GlobalForm.OpenPath + "\\" + ListBox1.SelectedItem.ToString();
		if (!File.Exists(text))
		{
			return;
		}
		try
		{
			StreamReader streamReader = new StreamReader(text);
			try
			{
				if (streamReader.Peek() == -1)
				{
					MessageBox.Show(text + " appears to be zero length.", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)16);
					ClearChartGrid(0);
				}
				else
				{
					FileLabel.Text = "This is what I read...\r\nFirst line: " + streamReader.ReadLine() + "\r\n";
					DateLine = streamReader.ReadLine();
					FileLabel.Text = FileLabel.Text + "Second line: " + DateLine + "\r\n";
					FileLabel.Text = FileLabel.Text + "Third line: " + streamReader.ReadLine();
					GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				MessageBox.Show("Error reading file " + text, "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)16);
				ClearChartGrid(0);
				ProjectData.ClearProjectError();
			}
			streamReader.Close();
			streamReader.Dispose();
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			MessageBox.Show("This file (" + text + ") appears to already be opened (perhaps by another user or process.)", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)16);
			ClearChartGrid(0);
			ProjectData.ClearProjectError();
		}
	}

	private void OpenCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		if (!OpenCheckBox.Checked)
		{
			OpenTextBox.Text = "0";
		}
		else
		{
			OpenTextBox.Text = GetMaxTB();
		}
		SaveNeeded = true;
	}

	private void SaveFileFormatButton_Click(object sender, EventArgs e)
	{
		//IL_001a: Unknown result type (might be due to invalid IL or missing references)
		SaveInformation(RuntimeHelpers.GetObjectValue(sender), e);
		MessageBox.Show("Format saved!", "Patternz: ThePatternSite.com", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void SaveInformation(object sender, EventArgs e)
	{
		WreckCheck(RuntimeHelpers.GetObjectValue(sender), e);
		GlobalForm.FileFormat[0] = Conversions.ToInteger(DateTextBox.Text);
		GlobalForm.FileFormat[1] = Conversions.ToInteger(TimeTextBox.Text);
		GlobalForm.FileFormat[2] = Conversions.ToInteger(OpenTextBox.Text);
		GlobalForm.FileFormat[3] = Conversions.ToInteger(HighTextBox.Text);
		GlobalForm.FileFormat[4] = Conversions.ToInteger(LowTextBox.Text);
		GlobalForm.FileFormat[5] = Conversions.ToInteger(CloseTextBox.Text);
		GlobalForm.FileFormat[6] = Conversions.ToInteger(VolumeTextBox.Text);
		GlobalForm.FileFormat[7] = Conversions.ToInteger(AdjCloseTextBox.Text);
		TempsDateFormat = FixTime();
		GlobalForm.UserDate = TempsDateFormat;
		GlobalForm.ckFileFormat[0] = true;
		GlobalForm.ckFileFormat[1] = TimeCheckBox.Checked;
		GlobalForm.ckFileFormat[2] = OpenCheckBox.Checked;
		GlobalForm.ckFileFormat[3] = true;
		GlobalForm.ckFileFormat[4] = true;
		GlobalForm.ckFileFormat[5] = true;
		GlobalForm.ckFileFormat[6] = VolumeCheckBox.Checked;
		GlobalForm.ckFileFormat[7] = AdjCloseCheckBox.Checked;
		GlobalForm.FileFormatChanged = true;
		SaveNeeded = false;
	}

	private void TimeCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		TempsDateFormat = FixTime();
		if (!TimeCheckBox.Checked)
		{
			TimeTextBox.Text = "0";
		}
		else
		{
			TimeTextBox.Text = GetMaxTB();
		}
		SaveNeeded = true;
	}

	private void VolumeCheckBox_CheckedChanged(object sender, EventArgs e)
	{
		if (!VolumeCheckBox.Checked)
		{
			VolumeTextBox.Text = "0";
		}
		else
		{
			VolumeTextBox.Text = GetMaxTB();
		}
		GlobalForm.ChartVolume = VolumeCheckBox.Checked;
		SaveNeeded = true;
	}

	private void WreckCheck(object sender, EventArgs e)
	{
		//IL_0480: Unknown result type (might be due to invalid IL or missing references)
		string[] array = new string[8];
		bool flag = false;
		if (!TimeCheckBox.Checked)
		{
			TimeTextBox.Text = "0";
		}
		if (!OpenCheckBox.Checked)
		{
			OpenTextBox.Text = "0";
		}
		if (!VolumeCheckBox.Checked)
		{
			VolumeTextBox.Text = "0";
		}
		if (!AdjCloseCheckBox.Checked)
		{
			AdjCloseTextBox.Text = "0";
		}
		if (TimeCheckBox.Checked & (Conversion.Val(TimeTextBox.Text) == 0.0))
		{
			TimeTextBox.Text = GetMaxTB();
		}
		if (OpenCheckBox.Checked & (Conversion.Val(OpenTextBox.Text) == 0.0))
		{
			OpenTextBox.Text = GetMaxTB();
		}
		if (VolumeCheckBox.Checked & (Conversion.Val(VolumeTextBox.Text) == 0.0))
		{
			VolumeTextBox.Text = GetMaxTB();
		}
		if (AdjCloseCheckBox.Checked & (Conversion.Val(AdjCloseTextBox.Text) == 0.0))
		{
			AdjCloseTextBox.Text = GetMaxTB();
		}
		if (Conversion.Val(DateTextBox.Text) == 0.0)
		{
			DateTextBox.Text = GetMaxTB();
		}
		if (Conversion.Val(HighTextBox.Text) == 0.0)
		{
			HighTextBox.Text = GetMaxTB();
		}
		if (Conversion.Val(LowTextBox.Text) == 0.0)
		{
			LowTextBox.Text = GetMaxTB();
		}
		if (Conversion.Val(CloseTextBox.Text) == 0.0)
		{
			CloseTextBox.Text = GetMaxTB();
		}
		array[0] = DateTextBox.Text;
		array[1] = TimeTextBox.Text;
		array[2] = OpenTextBox.Text;
		array[3] = HighTextBox.Text;
		array[4] = LowTextBox.Text;
		array[5] = CloseTextBox.Text;
		array[6] = VolumeTextBox.Text;
		array[7] = AdjCloseTextBox.Text;
		int num = Information.UBound((Array)array, 1);
		int num2 = num;
		checked
		{
			for (int i = 0; i <= num2; i++)
			{
				int num3 = num;
				for (int j = 0; j <= num3; j++)
				{
					if (!((j != i) & (Conversion.Val(array[i]) == Conversion.Val(array[j]))))
					{
						continue;
					}
					int num4 = (int)Math.Round(Conversion.Val(array[i]));
					if (!((num4 != 0) | ((num4 == 0) & (((j == 1) & TimeCheckBox.Checked) | ((j == 2) & OpenCheckBox.Checked) | ((j == 6) & VolumeCheckBox.Checked) | ((j == 7) & AdjCloseCheckBox.Checked)))))
					{
						continue;
					}
					flag = true;
					int num5 = num;
					for (int k = 0; k <= num5; k++)
					{
						num4 = (int)Math.Round(Conversion.Val(array[k]));
						if (((num4 != 0) | ((num4 == 0) & (((k == 1) & TimeCheckBox.Checked) | ((k == 2) & OpenCheckBox.Checked) | ((k == 6) & VolumeCheckBox.Checked) | ((k == 7) & AdjCloseCheckBox.Checked)))) && ((k != i) & ((double)num4 >= Conversion.Val(array[i]))))
						{
							array[k] = Conversions.ToString(Conversion.Val(array[k]) + 1.0);
						}
					}
				}
			}
			if (flag)
			{
				DateTextBox.Text = array[0];
				TimeTextBox.Text = array[1];
				OpenTextBox.Text = array[2];
				HighTextBox.Text = array[3];
				LowTextBox.Text = array[4];
				CloseTextBox.Text = array[5];
				VolumeTextBox.Text = array[6];
				AdjCloseTextBox.Text = array[7];
				MessageBox.Show("I found an error with the column order (duplicate number or zero when it shouldn't be) so I adjusted it. Please check my work.", "Patternz: ThePatternSite.com", (MessageBoxButtons)0);
			}
			((Control)Label1).ForeColor = Color.FromName("black");
			sDateFormatCombo_LostFocus(RuntimeHelpers.GetObjectValue(sender), e);
		}
	}
}
