using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz;

[DesignerGenerated]
public class SetupForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("MACheckBox")]
	private CheckBox _MACheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("OhlcRB")]
	private RadioButton _OhlcRB;

	[CompilerGenerated]
	[AccessedThroughProperty("CandleRB")]
	private RadioButton _CandleRB;

	[CompilerGenerated]
	[AccessedThroughProperty("UpColorButton")]
	private Button _UpColorButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DownColorButton")]
	private Button _DownColorButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ChartColorButton")]
	private Button _ChartColorButton;

	[CompilerGenerated]
	[AccessedThroughProperty("VolumeColorButton")]
	private Button _VolumeColorButton;

	[CompilerGenerated]
	[AccessedThroughProperty("RestoreDefaultButton")]
	private Button _RestoreDefaultButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PriceBarColorButton")]
	private Button _PriceBarColorButton;

	[CompilerGenerated]
	[AccessedThroughProperty("GapSizeMTB")]
	private MaskedTextBox _GapSizeMTB;

	[CompilerGenerated]
	[AccessedThroughProperty("AllButton")]
	private Button _AllButton;

	[CompilerGenerated]
	[AccessedThroughProperty("TargetsHelpBtn")]
	private Button _TargetsHelpBtn;

	[CompilerGenerated]
	[AccessedThroughProperty("AnnotationsCB")]
	private CheckBox _AnnotationsCB;

	[CompilerGenerated]
	[AccessedThroughProperty("BARRLinesButton")]
	private Button _BARRLinesButton;

	private readonly int tUP;

	private readonly int tDOWN;

	private readonly int tCHART;

	private readonly int tVOLUME;

	private readonly int tPRICE;

	internal virtual CheckBox MACheckBox
	{
		[CompilerGenerated]
		get
		{
			return _MACheckBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = MACheckBox_CheckedChanged;
			CheckBox val = _MACheckBox;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_MACheckBox = value;
			val = _MACheckBox;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("SMARadioButton")]
	internal virtual RadioButton SMARadioButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("EMARadioButton")]
	internal virtual RadioButton EMARadioButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("LengthLabel")]
	internal virtual Label LengthLabel
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

	[field: AccessedThroughProperty("Label1")]
	internal virtual Label Label1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton OhlcRB
	{
		[CompilerGenerated]
		get
		{
			return _OhlcRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = OhlcRB_CheckedChanged;
			RadioButton val = _OhlcRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_OhlcRB = value;
			val = _OhlcRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual RadioButton CandleRB
	{
		[CompilerGenerated]
		get
		{
			return _CandleRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = OhlcRB_CheckedChanged;
			RadioButton val = _CandleRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_CandleRB = value;
			val = _CandleRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("DecimalsUsedNumericUpDown")]
	internal virtual NumericUpDown DecimalsUsedNumericUpDown
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

	[field: AccessedThroughProperty("Panel1")]
	internal virtual Panel Panel1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Panel3")]
	internal virtual Panel Panel3
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("MANumericUpDown")]
	internal virtual NumericUpDown MANumericUpDown
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Panel4")]
	internal virtual Panel Panel4
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

	[field: AccessedThroughProperty("ChartVolRB")]
	internal virtual RadioButton ChartVolRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("DiscardVolRB")]
	internal virtual RadioButton DiscardVolRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("DownLabel")]
	internal virtual Label DownLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("UpLabel")]
	internal virtual Label UpLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("ColorDialog1")]
	internal virtual ColorDialog ColorDialog1
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

	internal virtual Button UpColorButton
	{
		[CompilerGenerated]
		get
		{
			return _UpColorButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = UpColorButton_Click;
			Button val = _UpColorButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_UpColorButton = value;
			val = _UpColorButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button DownColorButton
	{
		[CompilerGenerated]
		get
		{
			return _DownColorButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = UpColorButton_Click;
			Button val = _DownColorButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_DownColorButton = value;
			val = _DownColorButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button ChartColorButton
	{
		[CompilerGenerated]
		get
		{
			return _ChartColorButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = UpColorButton_Click;
			Button val = _ChartColorButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ChartColorButton = value;
			val = _ChartColorButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Panel5")]
	internal virtual Panel Panel5
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button VolumeColorButton
	{
		[CompilerGenerated]
		get
		{
			return _VolumeColorButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = UpColorButton_Click;
			Button val = _VolumeColorButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_VolumeColorButton = value;
			val = _VolumeColorButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label7")]
	internal virtual Label Label7
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button RestoreDefaultButton
	{
		[CompilerGenerated]
		get
		{
			return _RestoreDefaultButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = RestoreDefaultButton_Click;
			Button val = _RestoreDefaultButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_RestoreDefaultButton = value;
			val = _RestoreDefaultButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button PriceBarColorButton
	{
		[CompilerGenerated]
		get
		{
			return _PriceBarColorButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = UpColorButton_Click;
			Button val = _PriceBarColorButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_PriceBarColorButton = value;
			val = _PriceBarColorButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label8")]
	internal virtual Label Label8
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Panel6")]
	internal virtual Panel Panel6
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

	internal virtual MaskedTextBox GapSizeMTB
	{
		[CompilerGenerated]
		get
		{
			return _GapSizeMTB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			CancelEventHandler cancelEventHandler = GapSizeMTB_Validating;
			MaskedTextBox val = _GapSizeMTB;
			if (val != null)
			{
				((Control)val).Validating -= cancelEventHandler;
			}
			_GapSizeMTB = value;
			val = _GapSizeMTB;
			if (val != null)
			{
				((Control)val).Validating += cancelEventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Panel7")]
	internal virtual Panel Panel7
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

	[field: AccessedThroughProperty("UltimateHiLoCB")]
	internal virtual CheckBox UltimateHiLoCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("TargetPriceCB")]
	internal virtual CheckBox TargetPriceCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("StopLossCB")]
	internal virtual CheckBox StopLossCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("ConfirmationCB")]
	internal virtual CheckBox ConfirmationCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("ShowTargetsCB")]
	internal virtual CheckBox ShowTargetsCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
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

	[field: AccessedThroughProperty("UnHitCB")]
	internal virtual CheckBox UnHitCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button TargetsHelpBtn
	{
		[CompilerGenerated]
		get
		{
			return _TargetsHelpBtn;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = TargetsHelpBtn_Click;
			Button val = _TargetsHelpBtn;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_TargetsHelpBtn = value;
			val = _TargetsHelpBtn;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("DownTargetNum")]
	internal virtual NumericUpDown DownTargetNum
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("UpTargetNum")]
	internal virtual NumericUpDown UpTargetNum
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("DownTargetCB")]
	internal virtual CheckBox DownTargetCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("UpTargetCB")]
	internal virtual CheckBox UpTargetCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual CheckBox AnnotationsCB
	{
		[CompilerGenerated]
		get
		{
			return _AnnotationsCB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = AnnotationsCB_CheckedChanged;
			CheckBox val = _AnnotationsCB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_AnnotationsCB = value;
			val = _AnnotationsCB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("IncludeCB")]
	internal virtual CheckBox IncludeCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Panel8")]
	internal virtual Panel Panel8
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

	[field: AccessedThroughProperty("SkipNoPatternsRB")]
	internal virtual RadioButton SkipNoPatternsRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("SkipDoneTradesRB")]
	internal virtual RadioButton SkipDoneTradesRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBBoth")]
	internal virtual RadioButton RBBoth
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBFile")]
	internal virtual RadioButton RBFile
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBHuman")]
	internal virtual RadioButton RBHuman
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

	internal virtual Button BARRLinesButton
	{
		[CompilerGenerated]
		get
		{
			return _BARRLinesButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BARRLinesButton_Click;
			Button val = _BARRLinesButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_BARRLinesButton = value;
			val = _BARRLinesButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("BARRLinesCB")]
	internal virtual CheckBox BARRLinesCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public SetupForm()
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		((Form)this).FormClosing += new FormClosingEventHandler(SetupForm_FormClosing);
		((Form)this).Load += SetupForm_Load;
		tUP = 0;
		tDOWN = 1;
		tCHART = 2;
		tVOLUME = 3;
		tPRICE = 4;
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
		//IL_01b9: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c3: Expected O, but got Unknown
		//IL_01c4: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ce: Expected O, but got Unknown
		//IL_01cf: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d9: Expected O, but got Unknown
		//IL_01da: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e4: Expected O, but got Unknown
		//IL_01e5: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ef: Expected O, but got Unknown
		//IL_01f0: Unknown result type (might be due to invalid IL or missing references)
		//IL_01fa: Expected O, but got Unknown
		//IL_01fb: Unknown result type (might be due to invalid IL or missing references)
		//IL_0205: Expected O, but got Unknown
		//IL_0206: Unknown result type (might be due to invalid IL or missing references)
		//IL_0210: Expected O, but got Unknown
		//IL_0211: Unknown result type (might be due to invalid IL or missing references)
		//IL_021b: Expected O, but got Unknown
		//IL_021c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0226: Expected O, but got Unknown
		//IL_0227: Unknown result type (might be due to invalid IL or missing references)
		//IL_0231: Expected O, but got Unknown
		//IL_0232: Unknown result type (might be due to invalid IL or missing references)
		//IL_023c: Expected O, but got Unknown
		//IL_023d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0247: Expected O, but got Unknown
		//IL_0248: Unknown result type (might be due to invalid IL or missing references)
		//IL_0252: Expected O, but got Unknown
		//IL_0253: Unknown result type (might be due to invalid IL or missing references)
		//IL_025d: Expected O, but got Unknown
		//IL_025e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0268: Expected O, but got Unknown
		//IL_0269: Unknown result type (might be due to invalid IL or missing references)
		//IL_0273: Expected O, but got Unknown
		//IL_0274: Unknown result type (might be due to invalid IL or missing references)
		//IL_027e: Expected O, but got Unknown
		//IL_027f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0289: Expected O, but got Unknown
		MACheckBox = new CheckBox();
		SMARadioButton = new RadioButton();
		EMARadioButton = new RadioButton();
		LengthLabel = new Label();
		DoneButton = new Button();
		Label1 = new Label();
		OhlcRB = new RadioButton();
		CandleRB = new RadioButton();
		DecimalsUsedNumericUpDown = new NumericUpDown();
		Panel2 = new Panel();
		MANumericUpDown = new NumericUpDown();
		Panel1 = new Panel();
		AnnotationsCB = new CheckBox();
		UpColorButton = new Button();
		Label6 = new Label();
		DownLabel = new Label();
		UpLabel = new Label();
		Panel3 = new Panel();
		Label2 = new Label();
		RBBoth = new RadioButton();
		RBFile = new RadioButton();
		RBHuman = new RadioButton();
		Panel4 = new Panel();
		Label3 = new Label();
		ChartVolRB = new RadioButton();
		DiscardVolRB = new RadioButton();
		ColorDialog1 = new ColorDialog();
		DownColorButton = new Button();
		ChartColorButton = new Button();
		Panel5 = new Panel();
		PriceBarColorButton = new Button();
		Label8 = new Label();
		RestoreDefaultButton = new Button();
		VolumeColorButton = new Button();
		Label7 = new Label();
		Panel6 = new Panel();
		GapSizeMTB = new MaskedTextBox();
		Label4 = new Label();
		Panel7 = new Panel();
		BARRLinesButton = new Button();
		BARRLinesCB = new CheckBox();
		IncludeCB = new CheckBox();
		TargetsHelpBtn = new Button();
		DownTargetNum = new NumericUpDown();
		UpTargetNum = new NumericUpDown();
		DownTargetCB = new CheckBox();
		UpTargetCB = new CheckBox();
		UnHitCB = new CheckBox();
		AllButton = new Button();
		ShowTargetsCB = new CheckBox();
		Label5 = new Label();
		UltimateHiLoCB = new CheckBox();
		TargetPriceCB = new CheckBox();
		StopLossCB = new CheckBox();
		ConfirmationCB = new CheckBox();
		Panel8 = new Panel();
		Label9 = new Label();
		SkipNoPatternsRB = new RadioButton();
		SkipDoneTradesRB = new RadioButton();
		((ISupportInitialize)DecimalsUsedNumericUpDown).BeginInit();
		((Control)Panel2).SuspendLayout();
		((ISupportInitialize)MANumericUpDown).BeginInit();
		((Control)Panel1).SuspendLayout();
		((Control)Panel3).SuspendLayout();
		((Control)Panel4).SuspendLayout();
		((Control)Panel5).SuspendLayout();
		((Control)Panel6).SuspendLayout();
		((Control)Panel7).SuspendLayout();
		((ISupportInitialize)DownTargetNum).BeginInit();
		((ISupportInitialize)UpTargetNum).BeginInit();
		((Control)Panel8).SuspendLayout();
		((Control)this).SuspendLayout();
		((ButtonBase)MACheckBox).AutoSize = true;
		((Control)MACheckBox).Location = new Point(8, 12);
		((Control)MACheckBox).Name = "MACheckBox";
		((Control)MACheckBox).Size = new Size(103, 17);
		((Control)MACheckBox).TabIndex = 0;
		((ButtonBase)MACheckBox).Text = "&Moving average";
		((ButtonBase)MACheckBox).UseVisualStyleBackColor = true;
		((ButtonBase)SMARadioButton).AutoSize = true;
		SMARadioButton.Checked = true;
		((Control)SMARadioButton).Location = new Point(31, 39);
		((Control)SMARadioButton).Name = "SMARadioButton";
		((Control)SMARadioButton).Size = new Size(56, 17);
		((Control)SMARadioButton).TabIndex = 3;
		SMARadioButton.TabStop = true;
		((ButtonBase)SMARadioButton).Text = "&Simple";
		((ButtonBase)SMARadioButton).UseVisualStyleBackColor = true;
		((ButtonBase)EMARadioButton).AutoSize = true;
		((Control)EMARadioButton).Location = new Point(158, 39);
		((Control)EMARadioButton).Name = "EMARadioButton";
		((Control)EMARadioButton).Size = new Size(80, 17);
		((Control)EMARadioButton).TabIndex = 4;
		((ButtonBase)EMARadioButton).Text = "&Exponential";
		((ButtonBase)EMARadioButton).UseVisualStyleBackColor = true;
		LengthLabel.AutoSize = true;
		((Control)LengthLabel).Location = new Point(132, 16);
		((Control)LengthLabel).Name = "LengthLabel";
		((Control)LengthLabel).Size = new Size(43, 13);
		((Control)LengthLabel).TabIndex = 1;
		LengthLabel.Text = "&Length:";
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(424, 494);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(52, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(5, 11);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(32, 13);
		((Control)Label1).TabIndex = 0;
		Label1.Text = "Chart";
		((Control)OhlcRB).Anchor = (AnchorStyles)10;
		((ButtonBase)OhlcRB).AutoSize = true;
		((Control)OhlcRB).Location = new Point(158, 30);
		((Control)OhlcRB).Name = "OhlcRB";
		((Control)OhlcRB).Size = new Size(78, 17);
		((Control)OhlcRB).TabIndex = 3;
		((ButtonBase)OhlcRB).Text = "&OHLC (bar)";
		((ButtonBase)OhlcRB).UseVisualStyleBackColor = true;
		((Control)CandleRB).Anchor = (AnchorStyles)10;
		((ButtonBase)CandleRB).AutoSize = true;
		CandleRB.Checked = true;
		((Control)CandleRB).Location = new Point(31, 29);
		((Control)CandleRB).Name = "CandleRB";
		((Control)CandleRB).Size = new Size(121, 17);
		((Control)CandleRB).TabIndex = 2;
		CandleRB.TabStop = true;
		((ButtonBase)CandleRB).Text = "&Candlestick (default)";
		((ButtonBase)CandleRB).UseVisualStyleBackColor = true;
		((Control)DecimalsUsedNumericUpDown).Location = new Point(178, 10);
		DecimalsUsedNumericUpDown.Maximum = new decimal(new int[4] { 15, 0, 0, 0 });
		DecimalsUsedNumericUpDown.Minimum = new decimal(new int[4] { 2, 0, 0, 0 });
		((Control)DecimalsUsedNumericUpDown).Name = "DecimalsUsedNumericUpDown";
		((Control)DecimalsUsedNumericUpDown).Size = new Size(53, 20);
		((Control)DecimalsUsedNumericUpDown).TabIndex = 1;
		DecimalsUsedNumericUpDown.Value = new decimal(new int[4] { 2, 0, 0, 0 });
		Panel2.BorderStyle = (BorderStyle)2;
		((Control)Panel2).Controls.Add((Control)(object)MANumericUpDown);
		((Control)Panel2).Controls.Add((Control)(object)MACheckBox);
		((Control)Panel2).Controls.Add((Control)(object)SMARadioButton);
		((Control)Panel2).Controls.Add((Control)(object)EMARadioButton);
		((Control)Panel2).Controls.Add((Control)(object)LengthLabel);
		((Control)Panel2).Location = new Point(12, 374);
		((Control)Panel2).Name = "Panel2";
		((Control)Panel2).Size = new Size(253, 68);
		((Control)Panel2).TabIndex = 5;
		((Control)MANumericUpDown).Location = new Point(181, 12);
		MANumericUpDown.Maximum = new decimal(new int[4] { 999, 0, 0, 0 });
		MANumericUpDown.Minimum = new decimal(new int[4] { 2, 0, 0, 0 });
		((Control)MANumericUpDown).Name = "MANumericUpDown";
		((Control)MANumericUpDown).Size = new Size(66, 20);
		((Control)MANumericUpDown).TabIndex = 2;
		MANumericUpDown.Value = new decimal(new int[4] { 50, 0, 0, 0 });
		Panel1.BorderStyle = (BorderStyle)2;
		((Control)Panel1).Controls.Add((Control)(object)AnnotationsCB);
		((Control)Panel1).Controls.Add((Control)(object)Label1);
		((Control)Panel1).Controls.Add((Control)(object)OhlcRB);
		((Control)Panel1).Controls.Add((Control)(object)CandleRB);
		((Control)Panel1).Location = new Point(12, 12);
		((Control)Panel1).Name = "Panel1";
		((Control)Panel1).Size = new Size(253, 53);
		((Control)Panel1).TabIndex = 1;
		((ButtonBase)AnnotationsCB).AutoSize = true;
		((Control)AnnotationsCB).Location = new Point(149, 7);
		((Control)AnnotationsCB).Name = "AnnotationsCB";
		((Control)AnnotationsCB).Size = new Size(82, 17);
		((Control)AnnotationsCB).TabIndex = 1;
		((ButtonBase)AnnotationsCB).Text = "&Annotations";
		((ButtonBase)AnnotationsCB).UseVisualStyleBackColor = true;
		((ButtonBase)UpColorButton).BackColor = SystemColors.Control;
		((Control)UpColorButton).Location = new Point(191, 4);
		((Control)UpColorButton).Name = "UpColorButton";
		((Control)UpColorButton).Size = new Size(40, 23);
		((Control)UpColorButton).TabIndex = 1;
		((ButtonBase)UpColorButton).Text = "&Pick";
		((ButtonBase)UpColorButton).UseVisualStyleBackColor = false;
		Label6.AutoSize = true;
		((Control)Label6).Location = new Point(124, 98);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(61, 13);
		((Control)Label6).TabIndex = 7;
		Label6.Text = "&Chart color:";
		DownLabel.AutoSize = true;
		((Control)DownLabel).Location = new Point(60, 38);
		((Control)DownLabel).Name = "DownLabel";
		((Control)DownLabel).Size = new Size(125, 13);
		((Control)DownLabel).TabIndex = 2;
		DownLabel.Text = "&Down candle body color:";
		UpLabel.AutoSize = true;
		((Control)UpLabel).Location = new Point(74, 9);
		((Control)UpLabel).Name = "UpLabel";
		((Control)UpLabel).Size = new Size(111, 13);
		((Control)UpLabel).TabIndex = 0;
		UpLabel.Text = "&Up candle body color:";
		Panel3.BorderStyle = (BorderStyle)2;
		((Control)Panel3).Controls.Add((Control)(object)Label2);
		((Control)Panel3).Controls.Add((Control)(object)RBBoth);
		((Control)Panel3).Controls.Add((Control)(object)RBFile);
		((Control)Panel3).Controls.Add((Control)(object)RBHuman);
		((Control)Panel3).Controls.Add((Control)(object)DecimalsUsedNumericUpDown);
		((Control)Panel3).Location = new Point(12, 237);
		((Control)Panel3).Name = "Panel3";
		((Control)Panel3).Size = new Size(253, 126);
		((Control)Panel3).TabIndex = 4;
		((Control)Label2).ForeColor = Color.Red;
		((Control)Label2).Location = new Point(5, 80);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(241, 52);
		((Control)Label2).TabIndex = 4;
		Label2.Text = "Warning: Too few decimals will chart as flat or vertical lines. It often happens with futures and cryptocurrency (or any non-stock) data.";
		((ButtonBase)RBBoth).AutoSize = true;
		RBBoth.Checked = true;
		((Control)RBBoth).Location = new Point(31, 53);
		((Control)RBBoth).Name = "RBBoth";
		((Control)RBBoth).Size = new Size(134, 17);
		((Control)RBBoth).TabIndex = 3;
		RBBoth.TabStop = true;
		((ButtonBase)RBBoth).Text = "&Shorter of both (above)";
		((ButtonBase)RBBoth).UseVisualStyleBackColor = true;
		((ButtonBase)RBFile).AutoSize = true;
		((Control)RBFile).Location = new Point(31, 33);
		((Control)RBFile).Name = "RBFile";
		((Control)RBFile).Size = new Size(179, 17);
		((Control)RBFile).TabIndex = 2;
		((ButtonBase)RBFile).Text = "Let &quote file determine decimals";
		((ButtonBase)RBFile).UseVisualStyleBackColor = true;
		((ButtonBase)RBHuman).AutoSize = true;
		((Control)RBHuman).Location = new Point(31, 13);
		((Control)RBHuman).Name = "RBHuman";
		((Control)RBHuman).Size = new Size(134, 17);
		((Control)RBHuman).TabIndex = 0;
		((ButtonBase)RBHuman).Text = "&Limit decimal places to:";
		((ButtonBase)RBHuman).UseVisualStyleBackColor = true;
		Panel4.BorderStyle = (BorderStyle)2;
		((Control)Panel4).Controls.Add((Control)(object)Label3);
		((Control)Panel4).Controls.Add((Control)(object)ChartVolRB);
		((Control)Panel4).Controls.Add((Control)(object)DiscardVolRB);
		((Control)Panel4).Location = new Point(12, 448);
		((Control)Panel4).Name = "Panel4";
		((Control)Panel4).Size = new Size(253, 99);
		((Control)Panel4).TabIndex = 6;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(11, 10);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(217, 13);
		((Control)Label3).TabIndex = 0;
		Label3.Text = "How should I chart securities with 0 volume?";
		((ButtonBase)ChartVolRB).AutoSize = true;
		ChartVolRB.Checked = true;
		((Control)ChartVolRB).Location = new Point(31, 39);
		((Control)ChartVolRB).Name = "ChartVolRB";
		((Control)ChartVolRB).Size = new Size(97, 17);
		((Control)ChartVolRB).TabIndex = 1;
		ChartVolRB.TabStop = true;
		((ButtonBase)ChartVolRB).Text = "&Chart it anyway";
		((ButtonBase)ChartVolRB).UseVisualStyleBackColor = true;
		((ButtonBase)DiscardVolRB).AutoSize = true;
		((Control)DiscardVolRB).Location = new Point(31, 62);
		((Control)DiscardVolRB).Name = "DiscardVolRB";
		((Control)DiscardVolRB).Size = new Size(167, 17);
		((Control)DiscardVolRB).TabIndex = 2;
		((ButtonBase)DiscardVolRB).Text = "&Throw out all 0 volume quotes";
		((ButtonBase)DiscardVolRB).UseVisualStyleBackColor = true;
		ColorDialog1.AllowFullOpen = false;
		ColorDialog1.SolidColorOnly = true;
		((ButtonBase)DownColorButton).BackColor = SystemColors.Control;
		((Control)DownColorButton).Location = new Point(191, 33);
		((Control)DownColorButton).Name = "DownColorButton";
		((Control)DownColorButton).Size = new Size(40, 23);
		((Control)DownColorButton).TabIndex = 3;
		((ButtonBase)DownColorButton).Text = "&Pick";
		((ButtonBase)DownColorButton).UseVisualStyleBackColor = false;
		((ButtonBase)ChartColorButton).BackColor = SystemColors.Control;
		((Control)ChartColorButton).Location = new Point(191, 93);
		((Control)ChartColorButton).Name = "ChartColorButton";
		((Control)ChartColorButton).Size = new Size(40, 23);
		((Control)ChartColorButton).TabIndex = 8;
		((ButtonBase)ChartColorButton).Text = "&Pick";
		((ButtonBase)ChartColorButton).UseVisualStyleBackColor = false;
		Panel5.BorderStyle = (BorderStyle)2;
		((Control)Panel5).Controls.Add((Control)(object)PriceBarColorButton);
		((Control)Panel5).Controls.Add((Control)(object)Label8);
		((Control)Panel5).Controls.Add((Control)(object)RestoreDefaultButton);
		((Control)Panel5).Controls.Add((Control)(object)VolumeColorButton);
		((Control)Panel5).Controls.Add((Control)(object)Label7);
		((Control)Panel5).Controls.Add((Control)(object)ChartColorButton);
		((Control)Panel5).Controls.Add((Control)(object)DownLabel);
		((Control)Panel5).Controls.Add((Control)(object)DownColorButton);
		((Control)Panel5).Controls.Add((Control)(object)UpLabel);
		((Control)Panel5).Controls.Add((Control)(object)UpColorButton);
		((Control)Panel5).Controls.Add((Control)(object)Label6);
		((Control)Panel5).Location = new Point(12, 71);
		((Control)Panel5).Name = "Panel5";
		((Control)Panel5).Size = new Size(253, 160);
		((Control)Panel5).TabIndex = 3;
		((ButtonBase)PriceBarColorButton).BackColor = SystemColors.Control;
		((Control)PriceBarColorButton).Location = new Point(191, 127);
		((Control)PriceBarColorButton).Name = "PriceBarColorButton";
		((Control)PriceBarColorButton).Size = new Size(40, 23);
		((Control)PriceBarColorButton).TabIndex = 10;
		((ButtonBase)PriceBarColorButton).Text = "&Pick";
		((ButtonBase)PriceBarColorButton).UseVisualStyleBackColor = false;
		Label8.AutoSize = true;
		((Control)Label8).Location = new Point(107, 132);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(78, 13);
		((Control)Label8).TabIndex = 9;
		Label8.Text = "&Price bar color:";
		((ButtonBase)RestoreDefaultButton).BackColor = SystemColors.Control;
		((Control)RestoreDefaultButton).Location = new Point(6, 93);
		((Control)RestoreDefaultButton).Name = "RestoreDefaultButton";
		((Control)RestoreDefaultButton).Size = new Size(102, 23);
		((Control)RestoreDefaultButton).TabIndex = 6;
		((ButtonBase)RestoreDefaultButton).Text = "&Restore Defaults";
		((ButtonBase)RestoreDefaultButton).UseVisualStyleBackColor = false;
		((ButtonBase)VolumeColorButton).BackColor = SystemColors.Control;
		((Control)VolumeColorButton).Location = new Point(191, 62);
		((Control)VolumeColorButton).Name = "VolumeColorButton";
		((Control)VolumeColorButton).Size = new Size(40, 23);
		((Control)VolumeColorButton).TabIndex = 5;
		((ButtonBase)VolumeColorButton).Text = "&Pick";
		((ButtonBase)VolumeColorButton).UseVisualStyleBackColor = false;
		Label7.AutoSize = true;
		((Control)Label7).Location = new Point(114, 67);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(71, 13);
		((Control)Label7).TabIndex = 4;
		Label7.Text = "&Volume color:";
		Panel6.BorderStyle = (BorderStyle)2;
		((Control)Panel6).Controls.Add((Control)(object)GapSizeMTB);
		((Control)Panel6).Controls.Add((Control)(object)Label4);
		((Control)Panel6).Location = new Point(271, 12);
		((Control)Panel6).Name = "Panel6";
		((Control)Panel6).Size = new Size(196, 53);
		((Control)Panel6).TabIndex = 7;
		GapSizeMTB.AsciiOnly = true;
		((Control)GapSizeMTB).Location = new Point(110, 26);
		GapSizeMTB.Mask = "###.########";
		((Control)GapSizeMTB).Name = "GapSizeMTB";
		GapSizeMTB.ResetOnSpace = false;
		((Control)GapSizeMTB).Size = new Size(70, 20);
		GapSizeMTB.SkipLiterals = false;
		((Control)GapSizeMTB).TabIndex = 1;
		GapSizeMTB.Text = "00020000000";
		((Control)Label4).Location = new Point(3, 9);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(122, 37);
		((Control)Label4).TabIndex = 0;
		Label4.Text = "&Minimum gap size (same as on Patterns form):";
		Panel7.BorderStyle = (BorderStyle)2;
		((Control)Panel7).Controls.Add((Control)(object)BARRLinesButton);
		((Control)Panel7).Controls.Add((Control)(object)BARRLinesCB);
		((Control)Panel7).Controls.Add((Control)(object)IncludeCB);
		((Control)Panel7).Controls.Add((Control)(object)TargetsHelpBtn);
		((Control)Panel7).Controls.Add((Control)(object)DownTargetNum);
		((Control)Panel7).Controls.Add((Control)(object)UpTargetNum);
		((Control)Panel7).Controls.Add((Control)(object)DownTargetCB);
		((Control)Panel7).Controls.Add((Control)(object)UpTargetCB);
		((Control)Panel7).Controls.Add((Control)(object)UnHitCB);
		((Control)Panel7).Controls.Add((Control)(object)AllButton);
		((Control)Panel7).Controls.Add((Control)(object)ShowTargetsCB);
		((Control)Panel7).Controls.Add((Control)(object)Label5);
		((Control)Panel7).Controls.Add((Control)(object)UltimateHiLoCB);
		((Control)Panel7).Controls.Add((Control)(object)TargetPriceCB);
		((Control)Panel7).Controls.Add((Control)(object)StopLossCB);
		((Control)Panel7).Controls.Add((Control)(object)ConfirmationCB);
		((Control)Panel7).Location = new Point(271, 71);
		((Control)Panel7).Name = "Panel7";
		((Control)Panel7).Size = new Size(196, 297);
		((Control)Panel7).TabIndex = 8;
		((Control)BARRLinesButton).Location = new Point(148, 223);
		((Control)BARRLinesButton).Name = "BARRLinesButton";
		((Control)BARRLinesButton).Size = new Size(24, 18);
		((Control)BARRLinesButton).TabIndex = 13;
		((ButtonBase)BARRLinesButton).Text = "?";
		((ButtonBase)BARRLinesButton).UseVisualStyleBackColor = true;
		((ButtonBase)BARRLinesCB).AutoSize = true;
		((Control)BARRLinesCB).ForeColor = Color.Blue;
		((Control)BARRLinesCB).Location = new Point(21, 223);
		((Control)BARRLinesCB).Name = "BARRLinesCB";
		((Control)BARRLinesCB).Size = new Size(110, 17);
		((Control)BARRLinesCB).TabIndex = 12;
		((ButtonBase)BARRLinesCB).Text = "Show &BARR lines";
		((ButtonBase)BARRLinesCB).UseVisualStyleBackColor = true;
		((ButtonBase)IncludeCB).AutoSize = true;
		((Control)IncludeCB).Location = new Point(11, 273);
		((Control)IncludeCB).Name = "IncludeCB";
		((Control)IncludeCB).Size = new Size(115, 17);
		((Control)IncludeCB).TabIndex = 15;
		((ButtonBase)IncludeCB).Text = "&Include description";
		((ButtonBase)IncludeCB).UseVisualStyleBackColor = true;
		((Control)TargetsHelpBtn).Location = new Point(148, 98);
		((Control)TargetsHelpBtn).Name = "TargetsHelpBtn";
		((Control)TargetsHelpBtn).Size = new Size(32, 23);
		((Control)TargetsHelpBtn).TabIndex = 4;
		((ButtonBase)TargetsHelpBtn).Text = "?";
		((ButtonBase)TargetsHelpBtn).UseVisualStyleBackColor = true;
		((Control)DownTargetNum).Location = new Point(125, 200);
		DownTargetNum.Maximum = new decimal(new int[4] { 99, 0, 0, 0 });
		DownTargetNum.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)DownTargetNum).Name = "DownTargetNum";
		((Control)DownTargetNum).Size = new Size(53, 20);
		((Control)DownTargetNum).TabIndex = 11;
		DownTargetNum.Value = new decimal(new int[4] { 8, 0, 0, 0 });
		((Control)UpTargetNum).Location = new Point(125, 177);
		UpTargetNum.Maximum = new decimal(new int[4] { 999, 0, 0, 0 });
		UpTargetNum.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)UpTargetNum).Name = "UpTargetNum";
		((Control)UpTargetNum).Size = new Size(53, 20);
		((Control)UpTargetNum).TabIndex = 9;
		UpTargetNum.Value = new decimal(new int[4] { 20, 0, 0, 0 });
		((ButtonBase)DownTargetCB).AutoSize = true;
		((Control)DownTargetCB).ForeColor = Color.Green;
		((Control)DownTargetCB).Location = new Point(21, 200);
		((Control)DownTargetCB).Name = "DownTargetCB";
		((Control)DownTargetCB).Size = new Size(104, 17);
		((Control)DownTargetCB).TabIndex = 10;
		((ButtonBase)DownTargetCB).Text = "&Down target:   %";
		((ButtonBase)DownTargetCB).UseVisualStyleBackColor = true;
		((ButtonBase)UpTargetCB).AutoSize = true;
		((Control)UpTargetCB).ForeColor = Color.Green;
		((Control)UpTargetCB).Location = new Point(21, 177);
		((Control)UpTargetCB).Name = "UpTargetCB";
		((Control)UpTargetCB).Size = new Size(105, 17);
		((Control)UpTargetCB).TabIndex = 8;
		((ButtonBase)UpTargetCB).Text = "&Up target:        %";
		((ButtonBase)UpTargetCB).UseVisualStyleBackColor = true;
		((ButtonBase)UnHitCB).AutoSize = true;
		((Control)UnHitCB).Location = new Point(11, 250);
		((Control)UnHitCB).Name = "UnHitCB";
		((Control)UnHitCB).Size = new Size(170, 17);
		((Control)UnHitCB).TabIndex = 14;
		((ButtonBase)UnHitCB).Text = "&Show target/stop only if not hit";
		((ButtonBase)UnHitCB).UseVisualStyleBackColor = true;
		((Control)AllButton).Location = new Point(148, 123);
		((Control)AllButton).Name = "AllButton";
		((Control)AllButton).Size = new Size(32, 23);
		((Control)AllButton).TabIndex = 6;
		((ButtonBase)AllButton).Text = "&All";
		((ButtonBase)AllButton).UseVisualStyleBackColor = true;
		((ButtonBase)ShowTargetsCB).AutoSize = true;
		((Control)ShowTargetsCB).Location = new Point(12, 66);
		((Control)ShowTargetsCB).Name = "ShowTargetsCB";
		((Control)ShowTargetsCB).Size = new Size(119, 17);
		((Control)ShowTargetsCB).TabIndex = 1;
		((ButtonBase)ShowTargetsCB).Text = "Show &below targets";
		((ButtonBase)ShowTargetsCB).UseVisualStyleBackColor = true;
		((Control)Label5).Location = new Point(3, 9);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(186, 47);
		((Control)Label5).TabIndex = 0;
		Label5.Text = "Targets, when available, will appear as lines in the color shown by the check box below.";
		((ButtonBase)UltimateHiLoCB).AutoSize = true;
		((Control)UltimateHiLoCB).ForeColor = Color.Gray;
		((Control)UltimateHiLoCB).Location = new Point(21, 154);
		((Control)UltimateHiLoCB).Name = "UltimateHiLoCB";
		((Control)UltimateHiLoCB).Size = new Size(136, 17);
		((Control)UltimateHiLoCB).TabIndex = 7;
		((ButtonBase)UltimateHiLoCB).Text = "Show &ultimate high/low";
		((ButtonBase)UltimateHiLoCB).UseVisualStyleBackColor = true;
		((ButtonBase)TargetPriceCB).AutoSize = true;
		((Control)TargetPriceCB).ForeColor = Color.FromArgb(192, 0, 0);
		((Control)TargetPriceCB).Location = new Point(21, 131);
		((Control)TargetPriceCB).Name = "TargetPriceCB";
		((Control)TargetPriceCB).Size = new Size(109, 17);
		((Control)TargetPriceCB).TabIndex = 5;
		((ButtonBase)TargetPriceCB).Text = "Show &target price";
		((ButtonBase)TargetPriceCB).UseVisualStyleBackColor = true;
		((ButtonBase)StopLossCB).AutoSize = true;
		((Control)StopLossCB).ForeColor = Color.FromArgb(192, 0, 192);
		((Control)StopLossCB).Location = new Point(21, 108);
		((Control)StopLossCB).Name = "StopLossCB";
		((Control)StopLossCB).Size = new Size(97, 17);
		((Control)StopLossCB).TabIndex = 3;
		((ButtonBase)StopLossCB).Text = "Show &stop loss";
		((ButtonBase)StopLossCB).UseVisualStyleBackColor = true;
		((ButtonBase)ConfirmationCB).AutoSize = true;
		((Control)ConfirmationCB).ForeColor = Color.Blue;
		((Control)ConfirmationCB).Location = new Point(21, 88);
		((Control)ConfirmationCB).Name = "ConfirmationCB";
		((Control)ConfirmationCB).Size = new Size(113, 17);
		((Control)ConfirmationCB).TabIndex = 2;
		((ButtonBase)ConfirmationCB).Text = "Show &confirmation";
		((ButtonBase)ConfirmationCB).UseVisualStyleBackColor = true;
		Panel8.BorderStyle = (BorderStyle)2;
		((Control)Panel8).Controls.Add((Control)(object)Label9);
		((Control)Panel8).Controls.Add((Control)(object)SkipNoPatternsRB);
		((Control)Panel8).Controls.Add((Control)(object)SkipDoneTradesRB);
		((Control)Panel8).Location = new Point(271, 374);
		((Control)Panel8).Name = "Panel8";
		((Control)Panel8).Size = new Size(205, 99);
		((Control)Panel8).TabIndex = 0;
		Label9.AutoSize = true;
		((Control)Label9).Location = new Point(11, 10);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(149, 13);
		((Control)Label9).TabIndex = 0;
		Label9.Text = "Skip Options (Chart Form only)";
		((ButtonBase)SkipNoPatternsRB).AutoSize = true;
		SkipNoPatternsRB.Checked = true;
		((Control)SkipNoPatternsRB).Location = new Point(31, 39);
		((Control)SkipNoPatternsRB).Name = "SkipNoPatternsRB";
		((Control)SkipNoPatternsRB).Size = new Size(162, 17);
		((Control)SkipNoPatternsRB).TabIndex = 1;
		SkipNoPatternsRB.TabStop = true;
		((ButtonBase)SkipNoPatternsRB).Text = "No candles or patterns found";
		((ButtonBase)SkipNoPatternsRB).UseVisualStyleBackColor = true;
		((ButtonBase)SkipDoneTradesRB).AutoSize = true;
		((Control)SkipDoneTradesRB).Location = new Point(31, 62);
		((Control)SkipDoneTradesRB).Name = "SkipDoneTradesRB";
		((Control)SkipDoneTradesRB).Size = new Size(130, 17);
		((Control)SkipDoneTradesRB).TabIndex = 2;
		((ButtonBase)SkipDoneTradesRB).Text = "&Until open trade found";
		((ButtonBase)SkipDoneTradesRB).UseVisualStyleBackColor = true;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(484, 555);
		((Control)this).Controls.Add((Control)(object)Panel8);
		((Control)this).Controls.Add((Control)(object)Panel7);
		((Control)this).Controls.Add((Control)(object)Panel6);
		((Control)this).Controls.Add((Control)(object)Panel5);
		((Control)this).Controls.Add((Control)(object)Panel4);
		((Control)this).Controls.Add((Control)(object)Panel3);
		((Control)this).Controls.Add((Control)(object)Panel2);
		((Control)this).Controls.Add((Control)(object)Panel1);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Control)this).Name = "SetupForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Setup Form";
		((ISupportInitialize)DecimalsUsedNumericUpDown).EndInit();
		((Control)Panel2).ResumeLayout(false);
		((Control)Panel2).PerformLayout();
		((ISupportInitialize)MANumericUpDown).EndInit();
		((Control)Panel1).ResumeLayout(false);
		((Control)Panel1).PerformLayout();
		((Control)Panel3).ResumeLayout(false);
		((Control)Panel3).PerformLayout();
		((Control)Panel4).ResumeLayout(false);
		((Control)Panel4).PerformLayout();
		((Control)Panel5).ResumeLayout(false);
		((Control)Panel5).PerformLayout();
		((Control)Panel6).ResumeLayout(false);
		((Control)Panel6).PerformLayout();
		((Control)Panel7).ResumeLayout(false);
		((Control)Panel7).PerformLayout();
		((ISupportInitialize)DownTargetNum).EndInit();
		((ISupportInitialize)UpTargetNum).EndInit();
		((Control)Panel8).ResumeLayout(false);
		((Control)Panel8).PerformLayout();
		((Control)this).ResumeLayout(false);
	}

	private void SetupForm_FormClosing(object sender, FormClosingEventArgs e)
	{
		if (!Versioned.IsNumeric((object)GapSizeMTB.Text))
		{
			GlobalForm.GapSize = 0.2m;
		}
		else
		{
			GlobalForm.GapSize = Conversions.ToDecimal(GapSizeMTB.Text);
		}
		GlobalForm.MALength = Convert.ToInt32(MANumericUpDown.Value);
		GlobalForm.MAUsed = MACheckBox.Checked;
		bool flag = true;
		if (flag == SMARadioButton.Checked)
		{
			GlobalForm.MAType = 1;
		}
		else if (flag == EMARadioButton.Checked)
		{
			GlobalForm.MAType = 2;
		}
		bool flag2 = true;
		if (flag2 == OhlcRB.Checked)
		{
			GlobalForm.ChartType = 1;
		}
		else if (flag2 == CandleRB.Checked)
		{
			GlobalForm.ChartType = 0;
		}
		GlobalForm.UserDecimals = Convert.ToInt32(DecimalsUsedNumericUpDown.Value);
		bool flag3 = true;
		if (flag3 == RBHuman.Checked)
		{
			GlobalForm.DecimalsOption = GlobalForm.DECIMALSUSER;
			GlobalForm.DecimalsUsed = GlobalForm.UserDecimals;
		}
		else if (flag3 == RBFile.Checked)
		{
			GlobalForm.DecimalsOption = GlobalForm.DECIMALSFILE;
		}
		else if (flag3 == RBBoth.Checked)
		{
			GlobalForm.DecimalsOption = GlobalForm.DECIMALSBOTH;
		}
		GlobalForm.DiscardQuote = Conversions.ToInteger(Interaction.IIf(ChartVolRB.Checked, (object)1, (object)2));
		GlobalForm.PatternTargets = ShowTargetsCB.Checked;
		GlobalForm.ShowConfirmation = ConfirmationCB.Checked;
		GlobalForm.ShowStopLoss = StopLossCB.Checked;
		GlobalForm.ShowTargetprice = TargetPriceCB.Checked;
		GlobalForm.ShowUltHighLow = UltimateHiLoCB.Checked;
		GlobalForm.ShowUnHit = UnHitCB.Checked;
		GlobalForm.ShowUpTarget = UpTargetCB.Checked;
		GlobalForm.ShowUpPercentage = Convert.ToInt32(UpTargetNum.Value);
		GlobalForm.ShowDownTarget = DownTargetCB.Checked;
		GlobalForm.ShowDownPercentage = Convert.ToInt32(DownTargetNum.Value);
		GlobalForm.ShowBARRLines = BARRLinesCB.Checked;
		GlobalForm.IncludePhrase = IncludeCB.Checked;
		GlobalForm.SkipType = Conversions.ToInteger(Interaction.IIf(SkipNoPatternsRB.Checked, (object)1, (object)2));
	}

	private void SetupForm_Load(object sender, EventArgs e)
	{
		//IL_0078: Unknown result type (might be due to invalid IL or missing references)
		//IL_007d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0088: Unknown result type (might be due to invalid IL or missing references)
		//IL_0093: Unknown result type (might be due to invalid IL or missing references)
		//IL_009e: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a5: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b6: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e9: Unknown result type (might be due to invalid IL or missing references)
		//IL_00fa: Unknown result type (might be due to invalid IL or missing references)
		//IL_010b: Unknown result type (might be due to invalid IL or missing references)
		//IL_011c: Unknown result type (might be due to invalid IL or missing references)
		//IL_012d: Unknown result type (might be due to invalid IL or missing references)
		//IL_013e: Unknown result type (might be due to invalid IL or missing references)
		//IL_014f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0160: Unknown result type (might be due to invalid IL or missing references)
		//IL_0171: Unknown result type (might be due to invalid IL or missing references)
		//IL_0182: Unknown result type (might be due to invalid IL or missing references)
		//IL_0193: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a4: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b5: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c6: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d7: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e8: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f9: Unknown result type (might be due to invalid IL or missing references)
		//IL_020a: Unknown result type (might be due to invalid IL or missing references)
		//IL_021b: Unknown result type (might be due to invalid IL or missing references)
		//IL_022c: Unknown result type (might be due to invalid IL or missing references)
		//IL_023d: Unknown result type (might be due to invalid IL or missing references)
		//IL_024e: Unknown result type (might be due to invalid IL or missing references)
		//IL_025f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0270: Unknown result type (might be due to invalid IL or missing references)
		//IL_0281: Unknown result type (might be due to invalid IL or missing references)
		//IL_0292: Unknown result type (might be due to invalid IL or missing references)
		//IL_02a3: Unknown result type (might be due to invalid IL or missing references)
		//IL_02b4: Unknown result type (might be due to invalid IL or missing references)
		//IL_02c5: Unknown result type (might be due to invalid IL or missing references)
		//IL_02d6: Unknown result type (might be due to invalid IL or missing references)
		//IL_02e7: Unknown result type (might be due to invalid IL or missing references)
		//IL_02f8: Unknown result type (might be due to invalid IL or missing references)
		//IL_0309: Unknown result type (might be due to invalid IL or missing references)
		((Control)UpColorButton).Tag = tUP;
		((Control)DownColorButton).Tag = tDOWN;
		((Control)ChartColorButton).Tag = tCHART;
		((Control)VolumeColorButton).Tag = tVOLUME;
		AnnotationsCB.Checked = GlobalForm.Annotations;
		IncludeCB.Checked = GlobalForm.IncludePhrase;
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)AllButton, "Check all of the target check boxes.");
		val.SetToolTip((Control)(object)AnnotationsCB, "Show a small box which displays price and volume data on most charts.");
		val.SetToolTip((Control)(object)BARRLinesCB, "Show or hide buy, sell, and warning lines for bump-and-run reversal chart patterns.");
		val.SetToolTip((Control)(object)BARRLinesButton, "Bump-and-run reversal  buy, sell, and warning lines explanation.");
		val.SetToolTip((Control)(object)CandleRB, "When charting, draw candlestick charts.");
		val.SetToolTip((Control)(object)ChartColorButton, "The background color of the chart.");
		val.SetToolTip((Control)(object)ChartVolRB, "If a security has a quote with 0 volume, chart it normally. Useful for mutual funds and other securities which don't have volume.");
		val.SetToolTip((Control)(object)ConfirmationCB, "For chart patterns needing confirmation to be a valid, show the confirmation price when checked.");
		val.SetToolTip((Control)(object)DecimalsUsedNumericUpDown, "Number of decimal places used for SOME price targets.");
		val.SetToolTip((Control)(object)DiscardVolRB, "When charting, throw out any quotes with 0 volume. WARNING: Doing so could mean nothing gets charted (if every quote has 0 volume).");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)DownColorButton, "Pick a color for candlesticks when the closing price is below the open.");
		val.SetToolTip((Control)(object)DownTargetCB, "Set a percentage stop loss value.");
		val.SetToolTip((Control)(object)DownTargetNum, "Set a percentage stop loss value.");
		val.SetToolTip((Control)(object)EMARadioButton, "Chart an exponential moving average.");
		val.SetToolTip((Control)(object)GapSizeMTB, "For pattern recognition of gaps, enter the minimum gap size to qualify as a gap.");
		val.SetToolTip((Control)(object)IncludeCB, "When checked, show a short phrase describing the line, such as 'Target: 38.45'.");
		val.SetToolTip((Control)(object)MACheckBox, "Check to enable charting of moving averages.");
		val.SetToolTip((Control)(object)MANumericUpDown, "Enter the number of price bars in the moving average.");
		val.SetToolTip((Control)(object)OhlcRB, "When charting, draw open-high-low-close charts.");
		val.SetToolTip((Control)(object)PriceBarColorButton, "Pick a color for the price bars graphed on the chart.");
		val.SetToolTip((Control)(object)RBHuman, "Limit number of decimals shown from 2 to 15.");
		val.SetToolTip((Control)(object)RBFile, "Let file data determine number of decimals shown.");
		val.SetToolTip((Control)(object)RBBoth, "Let file, or your pick, limit number of decimals shown.");
		val.SetToolTip((Control)(object)RestoreDefaultButton, "Restore all colors to the factory default.");
		val.SetToolTip((Control)(object)ShowTargetsCB, "Show targets on chart. Also appears as a checkbox on the Chart Form as 'Targets'.");
		val.SetToolTip((Control)(object)SkipDoneTradesRB, "Skip to the next security until an open trade is found.");
		val.SetToolTip((Control)(object)SkipNoPatternsRB, "Skip to the next security until a candle or chart pattern is found.");
		val.SetToolTip((Control)(object)SMARadioButton, "Chart a simple moving average.");
		val.SetToolTip((Control)(object)StopLossCB, "Show volatility stop price, if available, based on day before breakout (if any).");
		val.SetToolTip((Control)(object)TargetPriceCB, "Show target price, based on chart pattern's full height and breakout direction (if none, up breakout is assumed).");
		val.SetToolTip((Control)(object)TargetsHelpBtn, "Get additional help on targets.");
		val.SetToolTip((Control)(object)UltimateHiLoCB, "If price has reached the ultimate high/low (highest high/lowest low before 20% reversal), show it.");
		val.SetToolTip((Control)(object)UnHitCB, "When checked, show measure rule target and stop if price has NOT reached them.");
		val.SetToolTip((Control)(object)UpColorButton, "Pick a color for candlesticks when the closing price is above the open.");
		val.SetToolTip((Control)(object)UpTargetCB, "Set a goal for the stock to reach.");
		val.SetToolTip((Control)(object)UpTargetNum, "Set a percentage above the breakout price for the stock to reach .");
		val.SetToolTip((Control)(object)VolumeColorButton, "The color of volume.");
		MACheckBox.Checked = GlobalForm.MAUsed;
		MANumericUpDown.Value = new decimal(GlobalForm.MALength);
		GapSizeMTB.Text = Strings.Format((object)GlobalForm.GapSize, "000.0#######");
		if (GlobalForm.MAType == 1)
		{
			SMARadioButton.Checked = true;
		}
		else
		{
			EMARadioButton.Checked = true;
		}
		MACheckBox_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
		((ButtonBase)UpColorButton).BackColor = GlobalForm.UpCandleColor;
		((ButtonBase)DownColorButton).BackColor = GlobalForm.DownCandleColor;
		((ButtonBase)ChartColorButton).BackColor = GlobalForm.ChartBGColor;
		((ButtonBase)VolumeColorButton).BackColor = GlobalForm.VolumeBGColor;
		((ButtonBase)PriceBarColorButton).BackColor = GlobalForm.PriceBarColor;
		switch (GlobalForm.ChartType)
		{
		case 1:
			OhlcRB.Checked = true;
			break;
		case 0:
			CandleRB.Checked = true;
			break;
		}
		GlobalForm.DecimalsUsed = GlobalForm.UserDecimals;
		if (decimal.Compare(new decimal(GlobalForm.UserDecimals), DecimalsUsedNumericUpDown.Minimum) < 0)
		{
			GlobalForm.UserDecimals = GlobalForm.TWODECIMALS;
		}
		if (decimal.Compare(new decimal(GlobalForm.UserDecimals), DecimalsUsedNumericUpDown.Maximum) > 0)
		{
			GlobalForm.UserDecimals = Convert.ToInt32(DecimalsUsedNumericUpDown.Maximum);
		}
		DecimalsUsedNumericUpDown.Value = new decimal(GlobalForm.UserDecimals);
		int decimalsOption = GlobalForm.DecimalsOption;
		if (decimalsOption == GlobalForm.DECIMALSUSER)
		{
			RBHuman.Checked = true;
		}
		else if (decimalsOption == GlobalForm.DECIMALSFILE)
		{
			RBFile.Checked = true;
		}
		else if (decimalsOption == GlobalForm.DECIMALSBOTH)
		{
			RBBoth.Checked = true;
		}
		if (GlobalForm.DiscardQuote == 1)
		{
			ChartVolRB.Checked = true;
		}
		else
		{
			DiscardVolRB.Checked = true;
		}
		ShowTargetsCB.Checked = GlobalForm.PatternTargets;
		ConfirmationCB.Checked = GlobalForm.ShowConfirmation;
		StopLossCB.Checked = GlobalForm.ShowStopLoss;
		TargetPriceCB.Checked = GlobalForm.ShowTargetprice;
		UltimateHiLoCB.Checked = GlobalForm.ShowUltHighLow;
		UnHitCB.Checked = GlobalForm.ShowUnHit;
		UpTargetCB.Checked = GlobalForm.ShowUpTarget;
		UpTargetNum.Value = new decimal(GlobalForm.ShowUpPercentage);
		DownTargetCB.Checked = GlobalForm.ShowDownTarget;
		DownTargetNum.Value = new decimal(GlobalForm.ShowDownPercentage);
		BARRLinesCB.Checked = GlobalForm.ShowBARRLines;
		switch (GlobalForm.SkipType)
		{
		case 1:
			SkipNoPatternsRB.Checked = true;
			break;
		case 2:
			SkipDoneTradesRB.Checked = true;
			break;
		}
	}

	private void AllButton_Click(object sender, EventArgs e)
	{
		ShowTargetsCB.Checked = true;
		ConfirmationCB.Checked = true;
		DownTargetCB.Checked = true;
		StopLossCB.Checked = true;
		TargetPriceCB.Checked = true;
		UltimateHiLoCB.Checked = true;
		UpTargetCB.Checked = true;
		GlobalForm.ShowBARRLines = true;
	}

	private void AnnotationsCB_CheckedChanged(object sender, EventArgs e)
	{
		GlobalForm.Annotations = AnnotationsCB.Checked;
	}

	private void BARRLinesButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("When displaying bump-and-run reversal patterns, show buy, sell, and warning lines.\r\n\r\nI draw a warning line parallel to the main trendline and lead-in height above/below it (lead-in phase on the pattern's trendline appears blue). It warns that a BARR pattern could be forming. Use the buy or sell lines to help time your entry and exit.\r\n\r\nFor example, when price rises above a sell line, reverses to plunge through the sell line to touch the one below it (that is, the second sell line below the top), you might consider selling. With a buy line, you might wait for price to CLOSE above the second buy line from the bottom.\r\n\r\nSee: https://thepatternsite.com/barrt.html#BART2 for a sell-line example.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void GapSizeMTB_Validating(object sender, CancelEventArgs e)
	{
		//IL_0024: Unknown result type (might be due to invalid IL or missing references)
		if (!Versioned.IsNumeric((object)GapSizeMTB.Text))
		{
			Interaction.Beep();
			MessageBox.Show("Only numbers and a decimal are allowed in the text box", "PatternsForm: GapSizeMTB_Validating", (MessageBoxButtons)0, (MessageBoxIcon)64);
			((Control)GapSizeMTB).Focus();
		}
	}

	private void MACheckBox_CheckedChanged(object sender, EventArgs e)
	{
		bool visible = MACheckBox.Checked;
		((Control)MANumericUpDown).Visible = visible;
		((Control)SMARadioButton).Visible = visible;
		((Control)EMARadioButton).Visible = visible;
		((Control)LengthLabel).Visible = visible;
	}

	private void OhlcRB_CheckedChanged(object sender, EventArgs e)
	{
		if (OhlcRB.Checked)
		{
			((Control)UpColorButton).Enabled = false;
			((Control)DownColorButton).Enabled = false;
			((Control)UpLabel).Enabled = false;
			((Control)DownLabel).Enabled = false;
		}
		else if (CandleRB.Checked)
		{
			((Control)UpColorButton).Enabled = true;
			((Control)DownColorButton).Enabled = true;
			((Control)UpLabel).Enabled = true;
			((Control)DownLabel).Enabled = true;
		}
	}

	private void RestoreDefaultButton_Click(object sender, EventArgs e)
	{
		GlobalForm.UpCandleColor = Color.FromArgb(255, 255, 255, 255);
		GlobalForm.DownCandleColor = Color.FromArgb(255, 0, 0, 0);
		GlobalForm.ChartBGColor = Color.FromArgb(255, 255, 255, 255);
		GlobalForm.VolumeBGColor = Color.FromArgb(255, 255, 128, 0);
		GlobalForm.PriceBarColor = Color.FromArgb(255, 0, 0, 0);
		((ButtonBase)UpColorButton).BackColor = Color.FromArgb(255, 255, 255, 255);
		((ButtonBase)DownColorButton).BackColor = Color.FromArgb(255, 0, 0, 0);
		((ButtonBase)ChartColorButton).BackColor = Color.FromArgb(255, 255, 255, 255);
		((ButtonBase)VolumeColorButton).BackColor = Color.FromArgb(255, 255, 128, 0);
		((ButtonBase)PriceBarColorButton).BackColor = Color.FromArgb(255, 0, 0, 0);
	}

	private void TargetsHelpBtn_Click(object sender, EventArgs e)
	{
		//IL_005d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat(string.Concat("Show below targets\r\nEnable/disable the showing of target information.\r\n\r\n" + "Show confirmation\r\nSome patterns require confirmation before they are valid. When checked, a blue confirmation line appears at the confirmation price.\r\n\r\n", "Show stop loss, target price, ultimate high/low\r\nEnable/disable the display of price based on a volatility stop loss calculation (violet line, based on a 20-trading day calculation ending the day before the breakout),"), " price target (red line, often the height of the pattern added to/subtracted from the breakout price), "), "or ultimate high/low (gray line, usually the highest peak/lowest valley before a 20% reversal).\r\n\r\n"), "Up/Down target %\r\nThe program draws horizontal green lines at the associated distance from the breakout price. Check the associated box then enter an appropriate percentage. Defaults are 20% for up profit target and 8% for down (stop loss) target.\r\n\r\n"), "Show target/stop only if not hit\r\nDo not show price targets or stop loss prices if the stock has already exceeded them. This feature removes clutter from the chart.\r\n\r\n"), "Include description\r\nLines appear with an associated phrase which may become unreadable when targets merge. To show the colored lines only, uncheck the box.\r\n\r\n"), "Not all patterns have available targeting information. The lines begin at the end of the pattern and end where they cross price."), "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void UpColorButton_Click(object sender, EventArgs e)
	{
		//IL_0000: Unknown result type (might be due to invalid IL or missing references)
		//IL_0006: Expected O, but got Unknown
		//IL_00b9: Unknown result type (might be due to invalid IL or missing references)
		//IL_00bf: Invalid comparison between Unknown and I4
		ColorDialog val = new ColorDialog();
		Button val2 = (Button)((sender is Button) ? sender : null);
		val.AllowFullOpen = false;
		val.SolidColorOnly = true;
		val.AnyColor = false;
		int num = Conversions.ToInteger(((Control)val2).Tag);
		if (num == tUP)
		{
			val.Color = ((ButtonBase)UpColorButton).BackColor;
		}
		else if (num == tDOWN)
		{
			val.Color = ((ButtonBase)DownColorButton).BackColor;
		}
		else if (num == tCHART)
		{
			val.Color = ((ButtonBase)ChartColorButton).BackColor;
		}
		else if (num == tVOLUME)
		{
			val.Color = ((ButtonBase)VolumeColorButton).BackColor;
		}
		else if (num == tPRICE)
		{
			val.Color = ((ButtonBase)PriceBarColorButton).BackColor;
		}
		if ((int)((CommonDialog)val).ShowDialog() == 1)
		{
			int num2 = Conversions.ToInteger(((Control)val2).Tag);
			if (num2 == tUP)
			{
				((ButtonBase)UpColorButton).BackColor = val.Color;
				GlobalForm.UpCandleColor = val.Color;
			}
			else if (num2 == tDOWN)
			{
				((ButtonBase)DownColorButton).BackColor = val.Color;
				GlobalForm.DownCandleColor = val.Color;
			}
			else if (num2 == tCHART)
			{
				((ButtonBase)ChartColorButton).BackColor = val.Color;
				GlobalForm.ChartBGColor = val.Color;
			}
			else if (num2 == tVOLUME)
			{
				((ButtonBase)VolumeColorButton).BackColor = val.Color;
				GlobalForm.VolumeBGColor = val.Color;
			}
			else if (num2 == tPRICE)
			{
				((ButtonBase)PriceBarColorButton).BackColor = val.Color;
				GlobalForm.PriceBarColor = val.Color;
			}
		}
		((Component)(object)val).Dispose();
	}
}
