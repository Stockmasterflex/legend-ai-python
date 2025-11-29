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
public class SimSetupForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("MACheckBox")]
	private CheckBox _MACheckBox;

	[CompilerGenerated]
	[AccessedThroughProperty("StartHelpBtn")]
	private Button _StartHelpBtn;

	[CompilerGenerated]
	[AccessedThroughProperty("QualifyHelpButton")]
	private Button _QualifyHelpButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PctBelowPeakCB")]
	private CheckBox _PctBelowPeakCB;

	[CompilerGenerated]
	[AccessedThroughProperty("PctAboveValleyCB")]
	private CheckBox _PctAboveValleyCB;

	[CompilerGenerated]
	[AccessedThroughProperty("PercentageHelpButton")]
	private Button _PercentageHelpButton;

	[CompilerGenerated]
	[AccessedThroughProperty("TLHelpButton")]
	private Button _TLHelpButton;

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

	[field: AccessedThroughProperty("Panel2")]
	internal virtual Panel Panel2
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

	[field: AccessedThroughProperty("Label3")]
	internal virtual Label Label3
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("LookbackNum")]
	internal virtual NumericUpDown LookbackNum
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("AnnotationsCheckBox")]
	internal virtual CheckBox AnnotationsCheckBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("VolumeCheckBox")]
	internal virtual CheckBox VolumeCheckBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("StrictCheckBox")]
	internal virtual CheckBox StrictCheckBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CandlesCheckBox")]
	internal virtual CheckBox CandlesCheckBox
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

	[field: AccessedThroughProperty("DailyRadioButton")]
	internal virtual RadioButton DailyRadioButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("WeeklyRadioButton")]
	internal virtual RadioButton WeeklyRadioButton
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("MonthlyRadioButton")]
	internal virtual RadioButton MonthlyRadioButton
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

	[field: AccessedThroughProperty("SECFeeCB")]
	internal virtual CheckBox SECFeeCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("SECFeeNum")]
	internal virtual NumericUpDown SECFeeNum
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

	[field: AccessedThroughProperty("CommissionsNum")]
	internal virtual NumericUpDown CommissionsNum
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

	[field: AccessedThroughProperty("Panel3")]
	internal virtual Panel Panel3
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

	[field: AccessedThroughProperty("AtStartBtn")]
	internal virtual RadioButton AtStartBtn
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("AtEndBtn")]
	internal virtual RadioButton AtEndBtn
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("AtBkoutBtn")]
	internal virtual RadioButton AtBkoutBtn
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button StartHelpBtn
	{
		[CompilerGenerated]
		get
		{
			return _StartHelpBtn;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = StartHelpBtn_Click;
			Button val = _StartHelpBtn;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_StartHelpBtn = value;
			val = _StartHelpBtn;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("AtEarlierBtn")]
	internal virtual RadioButton AtEarlierBtn
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

	[field: AccessedThroughProperty("ShowCirclesCB")]
	internal virtual CheckBox ShowCirclesCB
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

	[field: AccessedThroughProperty("Panel4")]
	internal virtual Panel Panel4
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("UltHiFoundCB")]
	internal virtual CheckBox UltHiFoundCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("UltLowFoundCB")]
	internal virtual CheckBox UltLowFoundCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("AutoSetTargetsCB")]
	internal virtual CheckBox AutoSetTargetsCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Panel5")]
	internal virtual Panel Panel5
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button QualifyHelpButton
	{
		[CompilerGenerated]
		get
		{
			return _QualifyHelpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = QualifyHelpButton_Click;
			Button val = _QualifyHelpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_QualifyHelpButton = value;
			val = _QualifyHelpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label9")]
	internal virtual Label Label9
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("FailPercent")]
	internal virtual NumericUpDown FailPercent
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

	[field: AccessedThroughProperty("FailRB")]
	internal virtual RadioButton FailRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("NonFailRB")]
	internal virtual RadioButton NonFailRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("BothRB")]
	internal virtual RadioButton BothRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("BearCB")]
	internal virtual CheckBox BearCB
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

	internal virtual CheckBox PctBelowPeakCB
	{
		[CompilerGenerated]
		get
		{
			return _PctBelowPeakCB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PctBelowPeakCB_CheckedChanged;
			CheckBox val = _PctBelowPeakCB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_PctBelowPeakCB = value;
			val = _PctBelowPeakCB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox PctAboveValleyCB
	{
		[CompilerGenerated]
		get
		{
			return _PctAboveValleyCB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PctAboveValleyCB_CheckedChanged;
			CheckBox val = _PctAboveValleyCB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_PctAboveValleyCB = value;
			val = _PctAboveValleyCB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual Button PercentageHelpButton
	{
		[CompilerGenerated]
		get
		{
			return _PercentageHelpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PercentageHelpButton_Click;
			Button val = _PercentageHelpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_PercentageHelpButton = value;
			val = _PercentageHelpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("NumAboveValley")]
	internal virtual NumericUpDown NumAboveValley
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("NumBelowPeak")]
	internal virtual NumericUpDown NumBelowPeak
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CloseBelowTLCB")]
	internal virtual CheckBox CloseBelowTLCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CloseAboveTLCB")]
	internal virtual CheckBox CloseAboveTLCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button TLHelpButton
	{
		[CompilerGenerated]
		get
		{
			return _TLHelpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = TLHelpButton_Click;
			Button val = _TLHelpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_TLHelpButton = value;
			val = _TLHelpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("StopPctUpCB")]
	internal virtual CheckBox StopPctUpCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("StopPctDownCB")]
	internal virtual CheckBox StopPctDownCB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public SimSetupForm()
	{
		((Form)this).Closing += SimSetupForm_Closing;
		((Form)this).Load += SimSetupForm_Load;
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
		//IL_0c6e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c78: Expected O, but got Unknown
		DoneButton = new Button();
		Panel2 = new Panel();
		MANumericUpDown = new NumericUpDown();
		MACheckBox = new CheckBox();
		SMARadioButton = new RadioButton();
		EMARadioButton = new RadioButton();
		LengthLabel = new Label();
		Label3 = new Label();
		LookbackNum = new NumericUpDown();
		AnnotationsCheckBox = new CheckBox();
		VolumeCheckBox = new CheckBox();
		StrictCheckBox = new CheckBox();
		CandlesCheckBox = new CheckBox();
		Panel1 = new Panel();
		Label6 = new Label();
		DailyRadioButton = new RadioButton();
		WeeklyRadioButton = new RadioButton();
		MonthlyRadioButton = new RadioButton();
		Label1 = new Label();
		SECFeeCB = new CheckBox();
		SECFeeNum = new NumericUpDown();
		Label2 = new Label();
		CommissionsNum = new NumericUpDown();
		Label4 = new Label();
		Panel3 = new Panel();
		AtEarlierBtn = new RadioButton();
		StartHelpBtn = new Button();
		Label5 = new Label();
		AtStartBtn = new RadioButton();
		AtEndBtn = new RadioButton();
		AtBkoutBtn = new RadioButton();
		ShowCirclesCB = new CheckBox();
		Label7 = new Label();
		Panel4 = new Panel();
		TLHelpButton = new Button();
		CloseBelowTLCB = new CheckBox();
		CloseAboveTLCB = new CheckBox();
		UltHiFoundCB = new CheckBox();
		UltLowFoundCB = new CheckBox();
		AutoSetTargetsCB = new CheckBox();
		Panel5 = new Panel();
		QualifyHelpButton = new Button();
		Label9 = new Label();
		FailPercent = new NumericUpDown();
		Label8 = new Label();
		FailRB = new RadioButton();
		NonFailRB = new RadioButton();
		BothRB = new RadioButton();
		BearCB = new CheckBox();
		Panel6 = new Panel();
		StopPctUpCB = new CheckBox();
		StopPctDownCB = new CheckBox();
		PercentageHelpButton = new Button();
		NumAboveValley = new NumericUpDown();
		NumBelowPeak = new NumericUpDown();
		PctBelowPeakCB = new CheckBox();
		PctAboveValleyCB = new CheckBox();
		((Control)Panel2).SuspendLayout();
		((ISupportInitialize)MANumericUpDown).BeginInit();
		((ISupportInitialize)LookbackNum).BeginInit();
		((Control)Panel1).SuspendLayout();
		((ISupportInitialize)SECFeeNum).BeginInit();
		((ISupportInitialize)CommissionsNum).BeginInit();
		((Control)Panel3).SuspendLayout();
		((Control)Panel4).SuspendLayout();
		((Control)Panel5).SuspendLayout();
		((ISupportInitialize)FailPercent).BeginInit();
		((Control)Panel6).SuspendLayout();
		((ISupportInitialize)NumAboveValley).BeginInit();
		((ISupportInitialize)NumBelowPeak).BeginInit();
		((Control)this).SuspendLayout();
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(351, 442);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(52, 23);
		((Control)DoneButton).TabIndex = 21;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		Panel2.BorderStyle = (BorderStyle)1;
		((Control)Panel2).Controls.Add((Control)(object)MANumericUpDown);
		((Control)Panel2).Controls.Add((Control)(object)MACheckBox);
		((Control)Panel2).Controls.Add((Control)(object)SMARadioButton);
		((Control)Panel2).Controls.Add((Control)(object)EMARadioButton);
		((Control)Panel2).Controls.Add((Control)(object)LengthLabel);
		((Control)Panel2).Location = new Point(192, 202);
		((Control)Panel2).Name = "Panel2";
		((Control)Panel2).Size = new Size(280, 65);
		((Control)Panel2).TabIndex = 10;
		((Control)MANumericUpDown).Location = new Point(181, 12);
		MANumericUpDown.Maximum = new decimal(new int[4] { 999, 0, 0, 0 });
		MANumericUpDown.Minimum = new decimal(new int[4] { 2, 0, 0, 0 });
		((Control)MANumericUpDown).Name = "MANumericUpDown";
		((Control)MANumericUpDown).Size = new Size(66, 20);
		((Control)MANumericUpDown).TabIndex = 2;
		MANumericUpDown.Value = new decimal(new int[4] { 50, 0, 0, 0 });
		((Control)MANumericUpDown).Visible = false;
		((ButtonBase)MACheckBox).AutoSize = true;
		((Control)MACheckBox).Location = new Point(12, 12);
		((Control)MACheckBox).Name = "MACheckBox";
		((Control)MACheckBox).Size = new Size(103, 17);
		((Control)MACheckBox).TabIndex = 0;
		((ButtonBase)MACheckBox).Text = "&Moving average";
		((ButtonBase)MACheckBox).UseVisualStyleBackColor = true;
		((ButtonBase)SMARadioButton).AutoSize = true;
		SMARadioButton.Checked = true;
		((Control)SMARadioButton).Location = new Point(33, 38);
		((Control)SMARadioButton).Name = "SMARadioButton";
		((Control)SMARadioButton).Size = new Size(56, 17);
		((Control)SMARadioButton).TabIndex = 3;
		SMARadioButton.TabStop = true;
		((ButtonBase)SMARadioButton).Text = "&Simple";
		((ButtonBase)SMARadioButton).UseVisualStyleBackColor = true;
		((Control)SMARadioButton).Visible = false;
		((ButtonBase)EMARadioButton).AutoSize = true;
		((Control)EMARadioButton).Location = new Point(160, 38);
		((Control)EMARadioButton).Name = "EMARadioButton";
		((Control)EMARadioButton).Size = new Size(80, 17);
		((Control)EMARadioButton).TabIndex = 4;
		((ButtonBase)EMARadioButton).Text = "&Exponential";
		((ButtonBase)EMARadioButton).UseVisualStyleBackColor = true;
		((Control)EMARadioButton).Visible = false;
		LengthLabel.AutoSize = true;
		((Control)LengthLabel).Location = new Point(132, 12);
		((Control)LengthLabel).Name = "LengthLabel";
		((Control)LengthLabel).Size = new Size(43, 13);
		((Control)LengthLabel).TabIndex = 1;
		LengthLabel.Text = "&Length:";
		((Control)LengthLabel).Visible = false;
		Label3.AutoSize = true;
		((Control)Label3).Location = new Point(7, 327);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(123, 13);
		((Control)Label3).TabIndex = 16;
		Label3.Text = "&Lookback (default: 262):";
		((Control)LookbackNum).Location = new Point(133, 325);
		LookbackNum.Maximum = new decimal(new int[4] { 2600, 0, 0, 0 });
		LookbackNum.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)LookbackNum).Name = "LookbackNum";
		((Control)LookbackNum).Size = new Size(52, 20);
		((Control)LookbackNum).TabIndex = 17;
		LookbackNum.Value = new decimal(new int[4] { 262, 0, 0, 0 });
		((ButtonBase)AnnotationsCheckBox).AutoSize = true;
		((Control)AnnotationsCheckBox).Location = new Point(26, 130);
		((Control)AnnotationsCheckBox).Name = "AnnotationsCheckBox";
		((Control)AnnotationsCheckBox).Size = new Size(82, 17);
		((Control)AnnotationsCheckBox).TabIndex = 3;
		((ButtonBase)AnnotationsCheckBox).Text = "&Annotations";
		((ButtonBase)AnnotationsCheckBox).UseVisualStyleBackColor = true;
		((ButtonBase)VolumeCheckBox).AutoSize = true;
		((Control)VolumeCheckBox).Location = new Point(26, 250);
		((Control)VolumeCheckBox).Name = "VolumeCheckBox";
		((Control)VolumeCheckBox).Size = new Size(61, 17);
		((Control)VolumeCheckBox).TabIndex = 9;
		((ButtonBase)VolumeCheckBox).Text = "&Volume";
		((ButtonBase)VolumeCheckBox).UseVisualStyleBackColor = true;
		((ButtonBase)StrictCheckBox).AutoSize = true;
		((Control)StrictCheckBox).Location = new Point(26, 230);
		((Control)StrictCheckBox).Name = "StrictCheckBox";
		((Control)StrictCheckBox).Size = new Size(50, 17);
		((Control)StrictCheckBox).TabIndex = 8;
		((ButtonBase)StrictCheckBox).Text = "St&rict";
		((ButtonBase)StrictCheckBox).UseVisualStyleBackColor = true;
		((ButtonBase)CandlesCheckBox).AutoSize = true;
		((Control)CandlesCheckBox).Location = new Point(26, 170);
		((Control)CandlesCheckBox).Name = "CandlesCheckBox";
		((Control)CandlesCheckBox).Size = new Size(86, 17);
		((Control)CandlesCheckBox).TabIndex = 5;
		((ButtonBase)CandlesCheckBox).Text = "Find cand&les";
		((ButtonBase)CandlesCheckBox).UseVisualStyleBackColor = true;
		Panel1.BorderStyle = (BorderStyle)1;
		((Control)Panel1).Controls.Add((Control)(object)Label6);
		((Control)Panel1).Controls.Add((Control)(object)DailyRadioButton);
		((Control)Panel1).Controls.Add((Control)(object)WeeklyRadioButton);
		((Control)Panel1).Controls.Add((Control)(object)MonthlyRadioButton);
		((Control)Panel1).Location = new Point(226, 11);
		((Control)Panel1).Name = "Panel1";
		((Control)Panel1).Size = new Size(89, 113);
		((Control)Panel1).TabIndex = 1;
		((Control)Label6).Anchor = (AnchorStyles)10;
		Label6.AutoSize = true;
		((Control)Label6).Location = new Point(10, 12);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(62, 13);
		((Control)Label6).TabIndex = 0;
		Label6.Text = "Chart Scale";
		((Control)DailyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)DailyRadioButton).AutoSize = true;
		DailyRadioButton.Checked = true;
		((Control)DailyRadioButton).Location = new Point(13, 40);
		((Control)DailyRadioButton).Name = "DailyRadioButton";
		((Control)DailyRadioButton).Size = new Size(48, 17);
		((Control)DailyRadioButton).TabIndex = 1;
		DailyRadioButton.TabStop = true;
		((Control)DailyRadioButton).Tag = "Daily";
		((ButtonBase)DailyRadioButton).Text = "Dail&y";
		((ButtonBase)DailyRadioButton).UseVisualStyleBackColor = true;
		((Control)WeeklyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)WeeklyRadioButton).AutoSize = true;
		((Control)WeeklyRadioButton).Location = new Point(13, 63);
		((Control)WeeklyRadioButton).Name = "WeeklyRadioButton";
		((Control)WeeklyRadioButton).Size = new Size(61, 17);
		((Control)WeeklyRadioButton).TabIndex = 2;
		((Control)WeeklyRadioButton).Tag = "Weekly";
		((ButtonBase)WeeklyRadioButton).Text = "&Weekly";
		((ButtonBase)WeeklyRadioButton).UseVisualStyleBackColor = true;
		((Control)MonthlyRadioButton).Anchor = (AnchorStyles)10;
		((ButtonBase)MonthlyRadioButton).AutoSize = true;
		((Control)MonthlyRadioButton).Location = new Point(13, 86);
		((Control)MonthlyRadioButton).Name = "MonthlyRadioButton";
		((Control)MonthlyRadioButton).Size = new Size(62, 17);
		((Control)MonthlyRadioButton).TabIndex = 3;
		((Control)MonthlyRadioButton).Tag = "Monthly";
		((ButtonBase)MonthlyRadioButton).Text = "&Monthly";
		((ButtonBase)MonthlyRadioButton).UseVisualStyleBackColor = true;
		((Control)Label1).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label1).Location = new Point(306, 385);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(152, 35);
		((Control)Label1).TabIndex = 20;
		Label1.Text = "Hover mouse over a control for help.";
		Label1.TextAlign = (ContentAlignment)512;
		((ButtonBase)SECFeeCB).AutoSize = true;
		((Control)SECFeeCB).Location = new Point(26, 270);
		((Control)SECFeeCB).Name = "SECFeeCB";
		((Control)SECFeeCB).Size = new Size(107, 17);
		((Control)SECFeeCB).TabIndex = 11;
		((ButtonBase)SECFeeCB).Text = "&SEC fee on sales";
		((ButtonBase)SECFeeCB).UseVisualStyleBackColor = true;
		SECFeeNum.DecimalPlaces = 2;
		SECFeeNum.Increment = new decimal(new int[4] { 1, 0, 0, 131072 });
		((Control)SECFeeNum).Location = new Point(133, 273);
		SECFeeNum.Maximum = new decimal(new int[4] { 500, 0, 0, 0 });
		((Control)SECFeeNum).Name = "SECFeeNum";
		((Control)SECFeeNum).Size = new Size(52, 20);
		((Control)SECFeeNum).TabIndex = 12;
		SECFeeNum.Value = new decimal(new int[4] { 2070, 0, 0, 131072 });
		Label2.AutoSize = true;
		((Control)Label2).Location = new Point(190, 275);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(53, 13);
		((Control)Label2).TabIndex = 13;
		Label2.Text = "per million";
		CommissionsNum.DecimalPlaces = 2;
		CommissionsNum.Increment = new decimal(new int[4] { 1, 0, 0, 131072 });
		((Control)CommissionsNum).Location = new Point(133, 299);
		CommissionsNum.Maximum = new decimal(new int[4] { 500, 0, 0, 0 });
		((Control)CommissionsNum).Name = "CommissionsNum";
		((Control)CommissionsNum).Size = new Size(52, 20);
		((Control)CommissionsNum).TabIndex = 15;
		CommissionsNum.Value = new decimal(new int[4] { 495, 0, 0, 131072 });
		Label4.AutoSize = true;
		((Control)Label4).Location = new Point(60, 301);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(70, 13);
		((Control)Label4).TabIndex = 14;
		Label4.Text = "Commissions:";
		Panel3.BorderStyle = (BorderStyle)1;
		((Control)Panel3).Controls.Add((Control)(object)AtEarlierBtn);
		((Control)Panel3).Controls.Add((Control)(object)StartHelpBtn);
		((Control)Panel3).Controls.Add((Control)(object)Label5);
		((Control)Panel3).Controls.Add((Control)(object)AtStartBtn);
		((Control)Panel3).Controls.Add((Control)(object)AtEndBtn);
		((Control)Panel3).Controls.Add((Control)(object)AtBkoutBtn);
		((Control)Panel3).Location = new Point(17, 11);
		((Control)Panel3).Name = "Panel3";
		((Control)Panel3).Size = new Size(194, 113);
		((Control)Panel3).TabIndex = 0;
		((Control)AtEarlierBtn).Anchor = (AnchorStyles)10;
		((ButtonBase)AtEarlierBtn).AutoSize = true;
		((Control)AtEarlierBtn).Location = new Point(10, 84);
		((Control)AtEarlierBtn).Name = "AtEarlierBtn";
		((Control)AtEarlierBtn).Size = new Size(180, 17);
		((Control)AtEarlierBtn).TabIndex = 5;
		((Control)AtEarlierBtn).Tag = "Monthly";
		((ButtonBase)AtEarlierBtn).Text = "Earlier of pattern end or breakout";
		((ButtonBase)AtEarlierBtn).UseVisualStyleBackColor = true;
		((Control)StartHelpBtn).Anchor = (AnchorStyles)10;
		((Control)StartHelpBtn).Location = new Point(135, 40);
		((Control)StartHelpBtn).Name = "StartHelpBtn";
		((Control)StartHelpBtn).Size = new Size(32, 23);
		((Control)StartHelpBtn).TabIndex = 3;
		((ButtonBase)StartHelpBtn).Text = "?";
		((ButtonBase)StartHelpBtn).UseVisualStyleBackColor = true;
		((Control)Label5).Anchor = (AnchorStyles)10;
		Label5.AutoSize = true;
		((Control)Label5).Location = new Point(10, 12);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(134, 13);
		((Control)Label5).TabIndex = 0;
		Label5.Text = "Pause the simulator when?";
		((Control)AtStartBtn).Anchor = (AnchorStyles)10;
		((ButtonBase)AtStartBtn).AutoSize = true;
		AtStartBtn.Checked = true;
		((Control)AtStartBtn).Location = new Point(10, 27);
		((Control)AtStartBtn).Name = "AtStartBtn";
		((Control)AtStartBtn).Size = new Size(94, 17);
		((Control)AtStartBtn).TabIndex = 1;
		AtStartBtn.TabStop = true;
		((Control)AtStartBtn).Tag = "Daily";
		((ButtonBase)AtStartBtn).Text = "&At pattern start";
		((ButtonBase)AtStartBtn).UseVisualStyleBackColor = true;
		((Control)AtEndBtn).Anchor = (AnchorStyles)10;
		((ButtonBase)AtEndBtn).AutoSize = true;
		((Control)AtEndBtn).Location = new Point(10, 46);
		((Control)AtEndBtn).Name = "AtEndBtn";
		((Control)AtEndBtn).Size = new Size(92, 17);
		((Control)AtEndBtn).TabIndex = 2;
		((Control)AtEndBtn).Tag = "Weekly";
		((ButtonBase)AtEndBtn).Text = "At pattern &end";
		((ButtonBase)AtEndBtn).UseVisualStyleBackColor = true;
		((Control)AtBkoutBtn).Anchor = (AnchorStyles)10;
		((ButtonBase)AtBkoutBtn).AutoSize = true;
		((Control)AtBkoutBtn).Location = new Point(10, 65);
		((Control)AtBkoutBtn).Name = "AtBkoutBtn";
		((Control)AtBkoutBtn).Size = new Size(80, 17);
		((Control)AtBkoutBtn).TabIndex = 4;
		((Control)AtBkoutBtn).Tag = "Monthly";
		((ButtonBase)AtBkoutBtn).Text = "At &breakout";
		((ButtonBase)AtBkoutBtn).UseVisualStyleBackColor = true;
		((ButtonBase)ShowCirclesCB).AutoSize = true;
		((Control)ShowCirclesCB).Location = new Point(26, 210);
		((Control)ShowCirclesCB).Name = "ShowCirclesCB";
		((Control)ShowCirclesCB).Size = new Size(86, 17);
		((Control)ShowCirclesCB).TabIndex = 7;
		((ButtonBase)ShowCirclesCB).Text = "&Show circles";
		((ButtonBase)ShowCirclesCB).UseVisualStyleBackColor = true;
		Label7.AutoSize = true;
		((Control)Label7).Location = new Point(2, 5);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(102, 13);
		((Control)Label7).TabIndex = 0;
		Label7.Text = "Stop simulator when";
		Panel4.BorderStyle = (BorderStyle)1;
		((Control)Panel4).Controls.Add((Control)(object)TLHelpButton);
		((Control)Panel4).Controls.Add((Control)(object)CloseBelowTLCB);
		((Control)Panel4).Controls.Add((Control)(object)CloseAboveTLCB);
		((Control)Panel4).Controls.Add((Control)(object)UltHiFoundCB);
		((Control)Panel4).Controls.Add((Control)(object)UltLowFoundCB);
		((Control)Panel4).Controls.Add((Control)(object)Label7);
		((Control)Panel4).Location = new Point(17, 359);
		((Control)Panel4).Name = "Panel4";
		((Control)Panel4).Size = new Size(236, 106);
		((Control)Panel4).TabIndex = 19;
		((Control)TLHelpButton).Anchor = (AnchorStyles)10;
		((Control)TLHelpButton).Location = new Point(199, 77);
		((Control)TLHelpButton).Name = "TLHelpButton";
		((Control)TLHelpButton).Size = new Size(32, 23);
		((Control)TLHelpButton).TabIndex = 5;
		((ButtonBase)TLHelpButton).Text = "?";
		((ButtonBase)TLHelpButton).UseVisualStyleBackColor = true;
		((ButtonBase)CloseBelowTLCB).AutoSize = true;
		((Control)CloseBelowTLCB).Location = new Point(8, 83);
		((Control)CloseBelowTLCB).Name = "CloseBelowTLCB";
		((Control)CloseBelowTLCB).Size = new Size(177, 17);
		((Control)CloseBelowTLCB).TabIndex = 4;
		((ButtonBase)CloseBelowTLCB).Text = "&Close below up-sloping trendline";
		((ButtonBase)CloseBelowTLCB).UseVisualStyleBackColor = true;
		((ButtonBase)CloseAboveTLCB).AutoSize = true;
		((Control)CloseAboveTLCB).Location = new Point(8, 63);
		((Control)CloseAboveTLCB).Name = "CloseAboveTLCB";
		((Control)CloseAboveTLCB).Size = new Size(193, 17);
		((Control)CloseAboveTLCB).TabIndex = 3;
		((ButtonBase)CloseAboveTLCB).Text = "Close above down-sloping trendline";
		((ButtonBase)CloseAboveTLCB).UseVisualStyleBackColor = true;
		((ButtonBase)UltHiFoundCB).AutoSize = true;
		((Control)UltHiFoundCB).Location = new Point(8, 23);
		((Control)UltHiFoundCB).Name = "UltHiFoundCB";
		((Control)UltHiFoundCB).Size = new Size(117, 17);
		((Control)UltHiFoundCB).TabIndex = 1;
		((ButtonBase)UltHiFoundCB).Text = "Ultimate &high found";
		((ButtonBase)UltHiFoundCB).UseVisualStyleBackColor = true;
		((ButtonBase)UltLowFoundCB).AutoSize = true;
		((Control)UltLowFoundCB).Location = new Point(8, 43);
		((Control)UltLowFoundCB).Name = "UltLowFoundCB";
		((Control)UltLowFoundCB).Size = new Size(113, 17);
		((Control)UltLowFoundCB).TabIndex = 2;
		((ButtonBase)UltLowFoundCB).Text = "Ultimate &low found";
		((ButtonBase)UltLowFoundCB).UseVisualStyleBackColor = true;
		((ButtonBase)AutoSetTargetsCB).AutoSize = true;
		((Control)AutoSetTargetsCB).Location = new Point(26, 150);
		((Control)AutoSetTargetsCB).Name = "AutoSetTargetsCB";
		((Control)AutoSetTargetsCB).Size = new Size(100, 17);
		((Control)AutoSetTargetsCB).TabIndex = 4;
		((ButtonBase)AutoSetTargetsCB).Text = "&Auto set targets";
		((ButtonBase)AutoSetTargetsCB).UseVisualStyleBackColor = true;
		Panel5.BorderStyle = (BorderStyle)1;
		((Control)Panel5).Controls.Add((Control)(object)QualifyHelpButton);
		((Control)Panel5).Controls.Add((Control)(object)Label9);
		((Control)Panel5).Controls.Add((Control)(object)FailPercent);
		((Control)Panel5).Controls.Add((Control)(object)Label8);
		((Control)Panel5).Controls.Add((Control)(object)FailRB);
		((Control)Panel5).Controls.Add((Control)(object)NonFailRB);
		((Control)Panel5).Controls.Add((Control)(object)BothRB);
		((Control)Panel5).Location = new Point(325, 11);
		((Control)Panel5).Name = "Panel5";
		((Control)Panel5).Size = new Size(147, 185);
		((Control)Panel5).TabIndex = 2;
		((Control)QualifyHelpButton).Anchor = (AnchorStyles)10;
		((Control)QualifyHelpButton).Location = new Point(102, 155);
		((Control)QualifyHelpButton).Name = "QualifyHelpButton";
		((Control)QualifyHelpButton).Size = new Size(32, 23);
		((Control)QualifyHelpButton).TabIndex = 6;
		((ButtonBase)QualifyHelpButton).Text = "?";
		((ButtonBase)QualifyHelpButton).UseVisualStyleBackColor = true;
		((Control)Label9).Location = new Point(3, 110);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(73, 67);
		((Control)Label9).TabIndex = 4;
		Label9.Text = "A rise/fall of what percent represents a failure (default is 5%)?";
		((Control)FailPercent).Location = new Point(82, 118);
		FailPercent.Maximum = new decimal(new int[4] { 99, 0, 0, 0 });
		FailPercent.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)FailPercent).Name = "FailPercent";
		((Control)FailPercent).Size = new Size(52, 20);
		((Control)FailPercent).TabIndex = 5;
		FailPercent.Value = new decimal(new int[4] { 5, 0, 0, 0 });
		((Control)Label8).Anchor = (AnchorStyles)10;
		Label8.AutoSize = true;
		((Control)Label8).Location = new Point(10, 13);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(81, 13);
		((Control)Label8).TabIndex = 0;
		Label8.Text = "Qualify Patterns";
		((Control)FailRB).Anchor = (AnchorStyles)10;
		((ButtonBase)FailRB).AutoSize = true;
		((Control)FailRB).Location = new Point(13, 40);
		((Control)FailRB).Name = "FailRB";
		((Control)FailRB).Size = new Size(110, 17);
		((Control)FailRB).TabIndex = 1;
		((Control)FailRB).Tag = "Daily";
		((ButtonBase)FailRB).Text = "&Show failures only";
		((ButtonBase)FailRB).UseVisualStyleBackColor = true;
		((Control)NonFailRB).Anchor = (AnchorStyles)10;
		((ButtonBase)NonFailRB).AutoSize = true;
		((Control)NonFailRB).Location = new Point(13, 63);
		((Control)NonFailRB).Name = "NonFailRB";
		((Control)NonFailRB).Size = new Size(131, 17);
		((Control)NonFailRB).TabIndex = 2;
		((Control)NonFailRB).Tag = "Weekly";
		((ButtonBase)NonFailRB).Text = "Show &non-failures only";
		((ButtonBase)NonFailRB).UseVisualStyleBackColor = true;
		((Control)BothRB).Anchor = (AnchorStyles)10;
		((ButtonBase)BothRB).AutoSize = true;
		BothRB.Checked = true;
		((Control)BothRB).Location = new Point(13, 86);
		((Control)BothRB).Name = "BothRB";
		((Control)BothRB).Size = new Size(76, 17);
		((Control)BothRB).TabIndex = 3;
		BothRB.TabStop = true;
		((Control)BothRB).Tag = "Monthly";
		((ButtonBase)BothRB).Text = "Show &both";
		((ButtonBase)BothRB).UseVisualStyleBackColor = true;
		((ButtonBase)BearCB).AutoSize = true;
		((Control)BearCB).Location = new Point(26, 190);
		((Control)BearCB).Name = "BearCB";
		((Control)BearCB).Size = new Size(117, 17);
		((Control)BearCB).TabIndex = 6;
		((ButtonBase)BearCB).Text = "Show &bear markets";
		((ButtonBase)BearCB).UseVisualStyleBackColor = true;
		Panel6.BorderStyle = (BorderStyle)1;
		((Control)Panel6).Controls.Add((Control)(object)StopPctUpCB);
		((Control)Panel6).Controls.Add((Control)(object)StopPctDownCB);
		((Control)Panel6).Controls.Add((Control)(object)PercentageHelpButton);
		((Control)Panel6).Controls.Add((Control)(object)NumAboveValley);
		((Control)Panel6).Controls.Add((Control)(object)NumBelowPeak);
		((Control)Panel6).Controls.Add((Control)(object)PctBelowPeakCB);
		((Control)Panel6).Controls.Add((Control)(object)PctAboveValleyCB);
		((Control)Panel6).Location = new Point(261, 273);
		((Control)Panel6).Name = "Panel6";
		((Control)Panel6).Size = new Size(211, 105);
		((Control)Panel6).TabIndex = 18;
		((ButtonBase)StopPctUpCB).AutoSize = true;
		((Control)StopPctUpCB).Enabled = false;
		((Control)StopPctUpCB).Location = new Point(3, 77);
		((Control)StopPctUpCB).Name = "StopPctUpCB";
		((Control)StopPctUpCB).Size = new Size(145, 17);
		((Control)StopPctUpCB).TabIndex = 6;
		((ButtonBase)StopPctUpCB).Text = "&Stop when % up reached";
		((ButtonBase)StopPctUpCB).UseVisualStyleBackColor = true;
		((ButtonBase)StopPctDownCB).AutoSize = true;
		((Control)StopPctDownCB).Enabled = false;
		((Control)StopPctDownCB).Location = new Point(3, 54);
		((Control)StopPctDownCB).Name = "StopPctDownCB";
		((Control)StopPctDownCB).Size = new Size(159, 17);
		((Control)StopPctDownCB).TabIndex = 4;
		((ButtonBase)StopPctDownCB).Text = "&Stop when % down reached";
		((ButtonBase)StopPctDownCB).UseVisualStyleBackColor = true;
		((Control)PercentageHelpButton).Anchor = (AnchorStyles)10;
		((Control)PercentageHelpButton).Location = new Point(169, 66);
		((Control)PercentageHelpButton).Name = "PercentageHelpButton";
		((Control)PercentageHelpButton).Size = new Size(32, 23);
		((Control)PercentageHelpButton).TabIndex = 5;
		((ButtonBase)PercentageHelpButton).Text = "?";
		((ButtonBase)PercentageHelpButton).UseVisualStyleBackColor = true;
		((Control)NumAboveValley).Location = new Point(149, 31);
		NumAboveValley.Maximum = new decimal(new int[4] { 1000, 0, 0, 0 });
		NumAboveValley.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)NumAboveValley).Name = "NumAboveValley";
		((Control)NumAboveValley).Size = new Size(52, 20);
		((Control)NumAboveValley).TabIndex = 3;
		NumAboveValley.Value = new decimal(new int[4] { 20, 0, 0, 0 });
		((Control)NumBelowPeak).Location = new Point(149, 5);
		NumBelowPeak.Maximum = new decimal(new int[4] { 99, 0, 0, 0 });
		NumBelowPeak.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)NumBelowPeak).Name = "NumBelowPeak";
		((Control)NumBelowPeak).Size = new Size(52, 20);
		((Control)NumBelowPeak).TabIndex = 1;
		NumBelowPeak.Value = new decimal(new int[4] { 20, 0, 0, 0 });
		((ButtonBase)PctBelowPeakCB).AutoSize = true;
		((Control)PctBelowPeakCB).Location = new Point(3, 8);
		((Control)PctBelowPeakCB).Name = "PctBelowPeakCB";
		((Control)PctBelowPeakCB).Size = new Size(143, 17);
		((Control)PctBelowPeakCB).TabIndex = 0;
		((ButtonBase)PctBelowPeakCB).Text = "Show % down from &peak";
		((ButtonBase)PctBelowPeakCB).UseVisualStyleBackColor = true;
		((ButtonBase)PctAboveValleyCB).AutoSize = true;
		((Control)PctAboveValleyCB).Location = new Point(3, 31);
		((Control)PctAboveValleyCB).Name = "PctAboveValleyCB";
		((Control)PctAboveValleyCB).Size = new Size(132, 17);
		((Control)PctAboveValleyCB).TabIndex = 2;
		((ButtonBase)PctAboveValleyCB).Text = "Show % up from &valley";
		((ButtonBase)PctAboveValleyCB).UseVisualStyleBackColor = true;
		((Form)this).AcceptButton = (IButtonControl)(object)DoneButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(494, 478);
		((Control)this).Controls.Add((Control)(object)Panel6);
		((Control)this).Controls.Add((Control)(object)BearCB);
		((Control)this).Controls.Add((Control)(object)Panel5);
		((Control)this).Controls.Add((Control)(object)AutoSetTargetsCB);
		((Control)this).Controls.Add((Control)(object)Panel4);
		((Control)this).Controls.Add((Control)(object)ShowCirclesCB);
		((Control)this).Controls.Add((Control)(object)Panel3);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)CommissionsNum);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)SECFeeNum);
		((Control)this).Controls.Add((Control)(object)SECFeeCB);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)Panel1);
		((Control)this).Controls.Add((Control)(object)AnnotationsCheckBox);
		((Control)this).Controls.Add((Control)(object)VolumeCheckBox);
		((Control)this).Controls.Add((Control)(object)StrictCheckBox);
		((Control)this).Controls.Add((Control)(object)CandlesCheckBox);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)LookbackNum);
		((Control)this).Controls.Add((Control)(object)Panel2);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Name = "SimSetupForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Simulator Setup Form";
		((Control)Panel2).ResumeLayout(false);
		((Control)Panel2).PerformLayout();
		((ISupportInitialize)MANumericUpDown).EndInit();
		((ISupportInitialize)LookbackNum).EndInit();
		((Control)Panel1).ResumeLayout(false);
		((Control)Panel1).PerformLayout();
		((ISupportInitialize)SECFeeNum).EndInit();
		((ISupportInitialize)CommissionsNum).EndInit();
		((Control)Panel3).ResumeLayout(false);
		((Control)Panel3).PerformLayout();
		((Control)Panel4).ResumeLayout(false);
		((Control)Panel4).PerformLayout();
		((Control)Panel5).ResumeLayout(false);
		((Control)Panel5).PerformLayout();
		((ISupportInitialize)FailPercent).EndInit();
		((Control)Panel6).ResumeLayout(false);
		((Control)Panel6).PerformLayout();
		((ISupportInitialize)NumAboveValley).EndInit();
		((ISupportInitialize)NumBelowPeak).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void SimSetupForm_Closing(object sender, CancelEventArgs e)
	{
		GlobalForm.Annotations = AnnotationsCheckBox.Checked;
		GlobalForm.SimGlobals.ShowCircles = ShowCirclesCB.Checked;
		GlobalForm.ShowCandles = CandlesCheckBox.Checked;
		GlobalForm.StrictPatterns = StrictCheckBox.Checked;
		GlobalForm.ChartVolume = VolumeCheckBox.Checked;
		GlobalForm.SimGlobals.Lookback = Convert.ToInt32(LookbackNum.Value);
		GlobalForm.SimGlobals.SECFee = SECFeeNum.Value;
		GlobalForm.SimGlobals.SECBool = SECFeeCB.Checked;
		GlobalForm.SimGlobals.Commissions = CommissionsNum.Value;
		GlobalForm.SimGlobals.StopUltHigh = UltHiFoundCB.Checked;
		GlobalForm.SimGlobals.StopUltLow = UltLowFoundCB.Checked;
		GlobalForm.SimGlobals.AutoSetTargets = AutoSetTargetsCB.Checked;
		GlobalForm.SimGlobals.ShowBearMarkets = BearCB.Checked;
		GlobalForm.SimGlobals.ShowPeakDrop = PctBelowPeakCB.Checked;
		GlobalForm.SimGlobals.ShowValleyRises = PctAboveValleyCB.Checked;
		GlobalForm.SimGlobals.PercentageDrop = Convert.ToInt32(NumBelowPeak.Value);
		GlobalForm.SimGlobals.PercentageRise = Convert.ToInt32(NumAboveValley.Value);
		GlobalForm.SimGlobals.CloseAboveTL = CloseAboveTLCB.Checked;
		GlobalForm.SimGlobals.CloseBelowTL = CloseBelowTLCB.Checked;
		if (!PctAboveValleyCB.Checked)
		{
			StopPctUpCB.Checked = false;
		}
		if (!PctBelowPeakCB.Checked)
		{
			StopPctDownCB.Checked = false;
		}
		GlobalForm.SimGlobals.StopPctDown = StopPctDownCB.Checked;
		GlobalForm.SimGlobals.StopPctUp = StopPctUpCB.Checked;
		GlobalForm.MAUsed = MACheckBox.Checked;
		GlobalForm.MALength = Convert.ToInt32(MANumericUpDown.Value);
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
		if (flag2 == DailyRadioButton.Checked)
		{
			GlobalForm.ChartPeriodShown = 0;
		}
		else if (flag2 == WeeklyRadioButton.Checked)
		{
			GlobalForm.ChartPeriodShown = 1;
		}
		else if (flag2 == MonthlyRadioButton.Checked)
		{
			GlobalForm.ChartPeriodShown = 2;
		}
		bool flag3 = true;
		if (flag3 == AtStartBtn.Checked)
		{
			GlobalForm.PauseSimulator = 1;
		}
		else if (flag3 == AtEndBtn.Checked)
		{
			GlobalForm.PauseSimulator = 2;
		}
		else if (flag3 == AtBkoutBtn.Checked)
		{
			GlobalForm.PauseSimulator = 3;
		}
		else if (flag3 == AtEarlierBtn.Checked)
		{
			GlobalForm.PauseSimulator = 4;
		}
		bool flag4 = true;
		if (flag4 == FailRB.Checked)
		{
			GlobalForm.SimGlobals.FailuresOnly = 1;
		}
		else if (flag4 == NonFailRB.Checked)
		{
			GlobalForm.SimGlobals.FailuresOnly = 2;
		}
		else
		{
			GlobalForm.SimGlobals.FailuresOnly = 3;
		}
		GlobalForm.SimGlobals.Percentage = Convert.ToInt32(FailPercent.Value);
	}

	private void SimSetupForm_Load(object sender, EventArgs e)
	{
		//IL_0000: Unknown result type (might be due to invalid IL or missing references)
		//IL_0005: Unknown result type (might be due to invalid IL or missing references)
		//IL_0010: Unknown result type (might be due to invalid IL or missing references)
		//IL_001b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0026: Unknown result type (might be due to invalid IL or missing references)
		//IL_002d: Unknown result type (might be due to invalid IL or missing references)
		//IL_003e: Unknown result type (might be due to invalid IL or missing references)
		//IL_004f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0060: Unknown result type (might be due to invalid IL or missing references)
		//IL_0071: Unknown result type (might be due to invalid IL or missing references)
		//IL_0082: Unknown result type (might be due to invalid IL or missing references)
		//IL_0093: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a4: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b5: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c6: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e8: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f9: Unknown result type (might be due to invalid IL or missing references)
		//IL_010a: Unknown result type (might be due to invalid IL or missing references)
		//IL_011b: Unknown result type (might be due to invalid IL or missing references)
		//IL_012c: Unknown result type (might be due to invalid IL or missing references)
		//IL_013d: Unknown result type (might be due to invalid IL or missing references)
		//IL_014e: Unknown result type (might be due to invalid IL or missing references)
		//IL_015f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0170: Unknown result type (might be due to invalid IL or missing references)
		//IL_0181: Unknown result type (might be due to invalid IL or missing references)
		//IL_0192: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a3: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b4: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c5: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d6: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e7: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f8: Unknown result type (might be due to invalid IL or missing references)
		//IL_0209: Unknown result type (might be due to invalid IL or missing references)
		//IL_0241: Unknown result type (might be due to invalid IL or missing references)
		//IL_0252: Unknown result type (might be due to invalid IL or missing references)
		//IL_0263: Unknown result type (might be due to invalid IL or missing references)
		//IL_0274: Unknown result type (might be due to invalid IL or missing references)
		//IL_0285: Unknown result type (might be due to invalid IL or missing references)
		//IL_0296: Unknown result type (might be due to invalid IL or missing references)
		//IL_02a7: Unknown result type (might be due to invalid IL or missing references)
		//IL_02b8: Unknown result type (might be due to invalid IL or missing references)
		//IL_02c9: Unknown result type (might be due to invalid IL or missing references)
		//IL_02da: Unknown result type (might be due to invalid IL or missing references)
		//IL_02eb: Unknown result type (might be due to invalid IL or missing references)
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)AnnotationsCheckBox, "Show a small box which displays price and volume data on the chart.");
		val.SetToolTip((Control)(object)AtBkoutBtn, "Pause simulation at pattern's breakout so you can adjust buy/sell/target information.");
		val.SetToolTip((Control)(object)AtEarlierBtn, "Pause simulation at earlier of pattern's end or breakout so you can adjust buy/sell/target information.");
		val.SetToolTip((Control)(object)AtEndBtn, "Pause simulation at pattern's end so you can adjust buy/sell/target information.");
		val.SetToolTip((Control)(object)AtStartBtn, "Pause simulation at pattern's start so you can adjust buy/sell/target information.");
		val.SetToolTip((Control)(object)AutoSetTargetsCB, "After picking a chart pattern from the list box, setup targets automatically (saves a button press).");
		val.SetToolTip((Control)(object)BearCB, "If checked, highlight bear markets.");
		val.SetToolTip((Control)(object)BothRB, "Find all chart patterns whether they work or not.");
		val.SetToolTip((Control)(object)CandlesCheckBox, "Check to show candles, not on the chart by in a message bar below the chart.");
		val.SetToolTip((Control)(object)CloseAboveTLCB, "If price closes above a down-sloping trendline chart pattern, stop the simulator.");
		val.SetToolTip((Control)(object)CloseBelowTLCB, "If price closes below an up-sloping trendline chart pattern, stop the simulator.");
		val.SetToolTip((Control)(object)CommissionsNum, "Enter commissions per trade or 0 if none.");
		val.SetToolTip((Control)(object)DailyRadioButton, "Select to show charts on the daily scale (except intraday).");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)EMARadioButton, "Chart an exponential moving average.");
		val.SetToolTip((Control)(object)FailPercent, "Enter how far price has to move before the chart pattern 'works'.");
		val.SetToolTip((Control)(object)FailRB, "Find patterns where price fails to move by the specified percentage.");
		val.SetToolTip((Control)(object)LookbackNum, "Tells how many price bars you want charted before it scrolls.");
		val.SetToolTip((Control)(object)MACheckBox, "Check to enable charting of moving averages.");
		val.SetToolTip((Control)(object)MANumericUpDown, "Enter the number of price bars in the moving average.");
		val.SetToolTip((Control)(object)MonthlyRadioButton, "Select to show charts on the monthly scale (except intraday).");
		val.SetToolTip((Control)(object)NonFailRB, "Find patterns where price moves by at least the specified percentage.");
		val.SetToolTip((Control)(object)NumAboveValley, "Enter a number (1-1000) representing a percentage rise above a valley.");
		val.SetToolTip((Control)(object)NumBelowPeak, "Enter a number (1-99) representing a percentage drop below a peak.");
		val.SetToolTip((Control)(object)PctAboveValleyCB, "Show with an asterisk the valley and percentage rise above the valley.");
		val.SetToolTip((Control)(object)PctBelowPeakCB, "Show with an asterisk the peak and percentage down from a peak.");
		val.SetToolTip((Control)(object)PercentageHelpButton, "Click for additional help.");
		val.SetToolTip((Control)(object)QualifyHelpButton, "Help with the Qualify Patterns options.");
		val.SetToolTip((Control)(object)SECFeeNum, "The SEC charges " + Strings.Format((object)20.7m, "$0#.00") + " per million on each sale (as of Patternz release date).");
		val.SetToolTip((Control)(object)SECFeeCB, "Check to include the SEC fee on sales.");
		val.SetToolTip((Control)(object)ShowCirclesCB, "Draw circles on chart showing buy, sell, ultimate high/low. Location is approximate.");
		val.SetToolTip((Control)(object)SMARadioButton, "Chart a simple moving average.");
		val.SetToolTip((Control)(object)StartHelpBtn, "Click for help with pausing the simulator options.");
		val.SetToolTip((Control)(object)StrictCheckBox, "Find patterns using loose or strict rules.");
		val.SetToolTip((Control)(object)TLHelpButton, "Discover when the simulator stops for trendlines.");
		val.SetToolTip((Control)(object)VolumeCheckBox, "Show volume at bottom of chart.");
		val.SetToolTip((Control)(object)WeeklyRadioButton, "Select to show charts on the weekly scale (except intraday).");
		val.SetToolTip((Control)(object)UltHiFoundCB, "Stop simulator if ultimate high found (after upward breakout).");
		val.SetToolTip((Control)(object)UltLowFoundCB, "Stop simulator if ultimate low found (after downward breakout).");
		val.SetToolTip((Control)(object)StopPctDownCB, "Stop simulator if price drops by the specified percentage.");
		val.SetToolTip((Control)(object)StopPctUpCB, "Stop simulator if price rises by the specified percentage.");
		AnnotationsCheckBox.Checked = GlobalForm.Annotations;
		CandlesCheckBox.Checked = GlobalForm.ShowCandles;
		ShowCirclesCB.Checked = GlobalForm.SimGlobals.ShowCircles;
		StrictCheckBox.Checked = GlobalForm.StrictPatterns;
		VolumeCheckBox.Checked = GlobalForm.ChartVolume;
		MACheckBox.Checked = GlobalForm.MAUsed;
		MANumericUpDown.Value = new decimal(Conversions.ToInteger(Interaction.IIf((decimal.Compare(new decimal(GlobalForm.MALength), MANumericUpDown.Minimum) < 0) | (decimal.Compare(new decimal(GlobalForm.MALength), MANumericUpDown.Maximum) > 0), (object)MANumericUpDown.Minimum, (object)GlobalForm.MALength)));
		UltHiFoundCB.Checked = GlobalForm.SimGlobals.StopUltHigh;
		UltLowFoundCB.Checked = GlobalForm.SimGlobals.StopUltLow;
		AutoSetTargetsCB.Checked = GlobalForm.SimGlobals.AutoSetTargets;
		BearCB.Checked = GlobalForm.SimGlobals.ShowBearMarkets;
		PctBelowPeakCB.Checked = GlobalForm.SimGlobals.ShowPeakDrop;
		PctAboveValleyCB.Checked = GlobalForm.SimGlobals.ShowValleyRises;
		CloseAboveTLCB.Checked = GlobalForm.SimGlobals.CloseAboveTL;
		CloseBelowTLCB.Checked = GlobalForm.SimGlobals.CloseBelowTL;
		StopPctDownCB.Checked = GlobalForm.SimGlobals.StopPctDown;
		StopPctUpCB.Checked = GlobalForm.SimGlobals.StopPctUp;
		NumBelowPeak.Value = new decimal(Conversions.ToInteger(Interaction.IIf((decimal.Compare(new decimal(GlobalForm.SimGlobals.PercentageDrop), NumBelowPeak.Minimum) < 0) | (decimal.Compare(new decimal(GlobalForm.SimGlobals.PercentageDrop), NumBelowPeak.Maximum) > 0), (object)NumBelowPeak.Minimum, (object)GlobalForm.SimGlobals.PercentageDrop)));
		NumAboveValley.Value = new decimal(Conversions.ToInteger(Interaction.IIf((decimal.Compare(new decimal(GlobalForm.SimGlobals.PercentageRise), NumAboveValley.Minimum) < 0) | (decimal.Compare(new decimal(GlobalForm.SimGlobals.PercentageRise), NumAboveValley.Maximum) > 0), (object)NumAboveValley.Minimum, (object)GlobalForm.SimGlobals.PercentageRise)));
		switch (GlobalForm.MAType)
		{
		case 1:
			SMARadioButton.Checked = true;
			break;
		case 2:
			EMARadioButton.Checked = true;
			break;
		}
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
		switch (GlobalForm.PauseSimulator)
		{
		case 1:
			AtStartBtn.Checked = true;
			break;
		case 2:
			AtEndBtn.Checked = true;
			break;
		case 3:
			AtBkoutBtn.Checked = true;
			break;
		case 4:
			AtEarlierBtn.Checked = true;
			break;
		}
		LookbackNum.Value = new decimal(Conversions.ToInteger(Interaction.IIf((decimal.Compare(new decimal(GlobalForm.SimGlobals.Lookback), LookbackNum.Minimum) < 0) | (decimal.Compare(new decimal(GlobalForm.SimGlobals.Lookback), LookbackNum.Maximum) > 0), (object)LookbackNum.Minimum, (object)GlobalForm.SimGlobals.Lookback)));
		SECFeeNum.Value = GlobalForm.SimGlobals.SECFee;
		SECFeeCB.Checked = GlobalForm.SimGlobals.SECBool;
		CommissionsNum.Value = GlobalForm.SimGlobals.Commissions;
		switch (GlobalForm.SimGlobals.FailuresOnly)
		{
		case 1:
			FailRB.Checked = true;
			break;
		case 2:
			NonFailRB.Checked = true;
			break;
		default:
			BothRB.Checked = true;
			break;
		}
		FailPercent.Value = new decimal(Conversions.ToInteger(Interaction.IIf((GlobalForm.SimGlobals.Percentage < 1) | (GlobalForm.SimGlobals.Percentage > 99), (object)5, (object)GlobalForm.SimGlobals.Percentage)));
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void MACheckBox_CheckedChanged(object sender, EventArgs e)
	{
		bool visible = MACheckBox.Checked;
		((Control)MANumericUpDown).Visible = visible;
		((Control)SMARadioButton).Visible = visible;
		((Control)EMARadioButton).Visible = visible;
		((Control)LengthLabel).Visible = visible;
	}

	private void QualifyHelpButton_Click(object sender, EventArgs e)
	{
		//IL_0035: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show(string.Concat(string.Concat(string.Concat("If you wish to find only chart patterns which fail (to learn to avoid patterns which fail) or only those which work, you've come to the right place.\r\n\r\n" + "To search for failures only, click the 'Show failures only' radio button.\r\n\r\n", "To search for working patterns only, click the 'Show non-failures only' radio button.\r\n\r\n"), "To search for both working and non-working patterns, click the 'Show both' radio button (default).\r\n\r\n"), "Enter a percentage which determines what a failure is. Default is 5% which means if price fails to move more than 5% away from the breakout price, the chart pattern is a failure.\r\n\r\nNote that a failure can occur if price drops below the bottom of the chart pattern (after an upward breakout) or above the pattern after a downward breakout."), "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void StartHelpBtn_Click(object sender, EventArgs e)
	{
		//IL_0021: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show(string.Concat("When you run a simulation, the program will pause at one of four points so you can plan your trade.\r\n\r\n   1) At pattern start,\r\n   2) At pattern end,\r\n   3) The breakout or\r\n   4) The earlier of the breakout or pattern's end.\r\n\r\n" + "If you want to buy in early, select pattern start. In some patterns, the breakout may come before or after the pattern's end, so choose accordingly for options 2 and 3 or select option 4.\r\n\r\n", "If I can't determine a breakout, I'll use the pattern's end."), "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void PercentageHelpButton_Click(object sender, EventArgs e)
	{
		//IL_0021: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show(string.Concat("Use these controls to highlight when price drops or rises by the chosen percentage. The high/low is marked with an asterisk (*).\r\n\r\n" + "By using this feature, you can train your eyes to anticipate large declines or rises.\r\n\r\n", "The 'Stop when %...' checkboxes allow you to pause the program when price reaches the percentage. You can practice buying-the-dip or testing for a trend change."), "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void TLHelpButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("For up-sloping trendlines, the simulator stops after two closes below the trendline provided the second bar has a lower close and lower low than the first bar. The reverse is true for down-sloping trendlines.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void PctBelowPeakCB_CheckedChanged(object sender, EventArgs e)
	{
		if (PctBelowPeakCB.Checked)
		{
			((Control)StopPctDownCB).Enabled = true;
			return;
		}
		((Control)StopPctDownCB).Enabled = false;
		StopPctDownCB.Checked = false;
	}

	private void PctAboveValleyCB_CheckedChanged(object sender, EventArgs e)
	{
		if (PctAboveValleyCB.Checked)
		{
			((Control)StopPctUpCB).Enabled = true;
			return;
		}
		((Control)StopPctUpCB).Enabled = false;
		StopPctUpCB.Checked = false;
	}
}
