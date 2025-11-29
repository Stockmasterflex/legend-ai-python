using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class PatternsForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DefaultButton")]
	private Button _DefaultButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ClearButton")]
	private Button _ClearButton;

	[CompilerGenerated]
	[AccessedThroughProperty("AllButton")]
	private Button _AllButton;

	[CompilerGenerated]
	[AccessedThroughProperty("GapUnknownCB")]
	private CheckBox _GapUnknownCB;

	[CompilerGenerated]
	[AccessedThroughProperty("CheckBox57")]
	private CheckBox _CheckBox57;

	[CompilerGenerated]
	[AccessedThroughProperty("CheckBox58")]
	private CheckBox _CheckBox58;

	[CompilerGenerated]
	[AccessedThroughProperty("SmallPatternsButton")]
	private Button _SmallPatternsButton;

	[CompilerGenerated]
	[AccessedThroughProperty("GapHelpButton")]
	private Button _GapHelpButton;

	[CompilerGenerated]
	[AccessedThroughProperty("WolfeHelpButton")]
	private Button _WolfeHelpButton;

	[CompilerGenerated]
	[AccessedThroughProperty("InvertButton")]
	private Button _InvertButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ThreeBarButton")]
	private Button _ThreeBarButton;

	[CompilerGenerated]
	[AccessedThroughProperty("FakeyHelpButton")]
	private Button _FakeyHelpButton;

	[CompilerGenerated]
	[AccessedThroughProperty("GapSizeMTB")]
	private MaskedTextBox _GapSizeMTB;

	[CompilerGenerated]
	[AccessedThroughProperty("BullUpButton")]
	private Button _BullUpButton;

	[CompilerGenerated]
	[AccessedThroughProperty("BearUpButton")]
	private Button _BearUpButton;

	[CompilerGenerated]
	[AccessedThroughProperty("BearDownButton")]
	private Button _BearDownButton;

	[CompilerGenerated]
	[AccessedThroughProperty("BullDownButton")]
	private Button _BullDownButton;

	[CompilerGenerated]
	[AccessedThroughProperty("BARRHelpButton")]
	private Button _BARRHelpButton;

	private bool AbortClosing;

	private bool LockFlag;

	private readonly bool[] DefaultList;

	private readonly bool[] SmallPats;

	private readonly bool[] BullUp;

	private readonly bool[] BullDown;

	private readonly bool[] BearUp;

	private readonly bool[] BearDown;

	[field: AccessedThroughProperty("CheckBox1")]
	internal virtual CheckBox CheckBox1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox2")]
	internal virtual CheckBox CheckBox2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox4")]
	internal virtual CheckBox CheckBox4
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox3")]
	internal virtual CheckBox CheckBox3
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox8")]
	internal virtual CheckBox CheckBox8
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox7")]
	internal virtual CheckBox CheckBox7
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox6")]
	internal virtual CheckBox CheckBox6
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox5")]
	internal virtual CheckBox CheckBox5
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox24")]
	internal virtual CheckBox CheckBox24
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox23")]
	internal virtual CheckBox CheckBox23
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox22")]
	internal virtual CheckBox CheckBox22
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox21")]
	internal virtual CheckBox CheckBox21
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox20")]
	internal virtual CheckBox CheckBox20
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox19")]
	internal virtual CheckBox CheckBox19
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox18")]
	internal virtual CheckBox CheckBox18
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox17")]
	internal virtual CheckBox CheckBox17
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox32")]
	internal virtual CheckBox CheckBox32
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox31")]
	internal virtual CheckBox CheckBox31
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox30")]
	internal virtual CheckBox CheckBox30
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox29")]
	internal virtual CheckBox CheckBox29
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox28")]
	internal virtual CheckBox CheckBox28
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox27")]
	internal virtual CheckBox CheckBox27
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox26")]
	internal virtual CheckBox CheckBox26
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox25")]
	internal virtual CheckBox CheckBox25
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox16")]
	internal virtual CheckBox CheckBox16
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox15")]
	internal virtual CheckBox CheckBox15
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox14")]
	internal virtual CheckBox CheckBox14
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox13")]
	internal virtual CheckBox CheckBox13
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox12")]
	internal virtual CheckBox CheckBox12
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox11")]
	internal virtual CheckBox CheckBox11
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox10")]
	internal virtual CheckBox CheckBox10
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox9")]
	internal virtual CheckBox CheckBox9
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

	internal virtual Button DefaultButton
	{
		[CompilerGenerated]
		get
		{
			return _DefaultButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DefaultButton_Click;
			Button val = _DefaultButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_DefaultButton = value;
			val = _DefaultButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button ClearButton
	{
		[CompilerGenerated]
		get
		{
			return _ClearButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ClearButton_Click;
			Button val = _ClearButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ClearButton = value;
			val = _ClearButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("PctRiseMaskedTextBox")]
	internal virtual MaskedTextBox PctRiseMaskedTextBox
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

	[field: AccessedThroughProperty("CheckBox33")]
	internal virtual CheckBox CheckBox33
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox34")]
	internal virtual CheckBox CheckBox34
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox35")]
	internal virtual CheckBox CheckBox35
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox36")]
	internal virtual CheckBox CheckBox36
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox37")]
	internal virtual CheckBox CheckBox37
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox38")]
	internal virtual CheckBox CheckBox38
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox39")]
	internal virtual CheckBox CheckBox39
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox40")]
	internal virtual CheckBox CheckBox40
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox41")]
	internal virtual CheckBox CheckBox41
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox42")]
	internal virtual CheckBox CheckBox42
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual CheckBox GapUnknownCB
	{
		[CompilerGenerated]
		get
		{
			return _GapUnknownCB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GapUnknownCB_CheckedChanged;
			CheckBox val = _GapUnknownCB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_GapUnknownCB = value;
			val = _GapUnknownCB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("CheckBox44")]
	internal virtual CheckBox CheckBox44
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox45")]
	internal virtual CheckBox CheckBox45
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox46")]
	internal virtual CheckBox CheckBox46
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox47")]
	internal virtual CheckBox CheckBox47
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox48")]
	internal virtual CheckBox CheckBox48
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox49")]
	internal virtual CheckBox CheckBox49
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox50")]
	internal virtual CheckBox CheckBox50
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox51")]
	internal virtual CheckBox CheckBox51
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox52")]
	internal virtual CheckBox CheckBox52
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox53")]
	internal virtual CheckBox CheckBox53
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox54")]
	internal virtual CheckBox CheckBox54
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox56")]
	internal virtual CheckBox CheckBox56
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox59")]
	internal virtual CheckBox CheckBox59
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox60")]
	internal virtual CheckBox CheckBox60
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox61")]
	internal virtual CheckBox CheckBox61
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox62")]
	internal virtual CheckBox CheckBox62
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox63")]
	internal virtual CheckBox CheckBox63
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox64")]
	internal virtual CheckBox CheckBox64
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox65")]
	internal virtual CheckBox CheckBox65
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox66")]
	internal virtual CheckBox CheckBox66
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox67")]
	internal virtual CheckBox CheckBox67
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox68")]
	internal virtual CheckBox CheckBox68
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox70")]
	internal virtual CheckBox CheckBox70
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox71")]
	internal virtual CheckBox CheckBox71
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox72")]
	internal virtual CheckBox CheckBox72
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox73")]
	internal virtual CheckBox CheckBox73
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox74")]
	internal virtual CheckBox CheckBox74
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox75")]
	internal virtual CheckBox CheckBox75
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox77")]
	internal virtual CheckBox CheckBox77
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox78")]
	internal virtual CheckBox CheckBox78
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox79")]
	internal virtual CheckBox CheckBox79
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox80")]
	internal virtual CheckBox CheckBox80
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox81")]
	internal virtual CheckBox CheckBox81
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox82")]
	internal virtual CheckBox CheckBox82
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox83")]
	internal virtual CheckBox CheckBox83
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox84")]
	internal virtual CheckBox CheckBox84
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox85")]
	internal virtual CheckBox CheckBox85
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox86")]
	internal virtual CheckBox CheckBox86
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox87")]
	internal virtual CheckBox CheckBox87
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox88")]
	internal virtual CheckBox CheckBox88
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox89")]
	internal virtual CheckBox CheckBox89
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox90")]
	internal virtual CheckBox CheckBox90
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox91")]
	internal virtual CheckBox CheckBox91
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox92")]
	internal virtual CheckBox CheckBox92
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox95")]
	internal virtual CheckBox CheckBox95
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox96")]
	internal virtual CheckBox CheckBox96
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox97")]
	internal virtual CheckBox CheckBox97
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox98")]
	internal virtual CheckBox CheckBox98
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox99")]
	internal virtual CheckBox CheckBox99
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox100")]
	internal virtual CheckBox CheckBox100
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox101")]
	internal virtual CheckBox CheckBox101
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox106")]
	internal virtual CheckBox CheckBox106
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox107")]
	internal virtual CheckBox CheckBox107
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual CheckBox CheckBox57
	{
		[CompilerGenerated]
		get
		{
			return _CheckBox57;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CheckBox57_CheckedChanged;
			CheckBox val = _CheckBox57;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_CheckBox57 = value;
			val = _CheckBox57;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox CheckBox58
	{
		[CompilerGenerated]
		get
		{
			return _CheckBox58;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CheckBox57_CheckedChanged;
			CheckBox val = _CheckBox58;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_CheckBox58 = value;
			val = _CheckBox58;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("CheckBox69")]
	internal virtual CheckBox CheckBox69
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox76")]
	internal virtual CheckBox CheckBox76
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox93")]
	internal virtual CheckBox CheckBox93
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox94")]
	internal virtual CheckBox CheckBox94
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

	[field: AccessedThroughProperty("GroupBox1")]
	internal virtual GroupBox GroupBox1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button SmallPatternsButton
	{
		[CompilerGenerated]
		get
		{
			return _SmallPatternsButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = SmallPatternsButton_Click;
			Button val = _SmallPatternsButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_SmallPatternsButton = value;
			val = _SmallPatternsButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button GapHelpButton
	{
		[CompilerGenerated]
		get
		{
			return _GapHelpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GapHelpButton_Click;
			Button val = _GapHelpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_GapHelpButton = value;
			val = _GapHelpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button WolfeHelpButton
	{
		[CompilerGenerated]
		get
		{
			return _WolfeHelpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = WolfeHelpButton_Click;
			Button val = _WolfeHelpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_WolfeHelpButton = value;
			val = _WolfeHelpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button InvertButton
	{
		[CompilerGenerated]
		get
		{
			return _InvertButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = InvertButton_Click;
			Button val = _InvertButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_InvertButton = value;
			val = _InvertButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button ThreeBarButton
	{
		[CompilerGenerated]
		get
		{
			return _ThreeBarButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ThreeBarButton_Click;
			Button val = _ThreeBarButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ThreeBarButton = value;
			val = _ThreeBarButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("WarningLabel")]
	internal virtual Label WarningLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox43")]
	internal virtual CheckBox CheckBox43
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox55")]
	internal virtual CheckBox CheckBox55
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox102")]
	internal virtual CheckBox CheckBox102
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox103")]
	internal virtual CheckBox CheckBox103
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox104")]
	internal virtual CheckBox CheckBox104
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox105")]
	internal virtual CheckBox CheckBox105
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox108")]
	internal virtual CheckBox CheckBox108
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox109")]
	internal virtual CheckBox CheckBox109
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox112")]
	internal virtual CheckBox CheckBox112
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox113")]
	internal virtual CheckBox CheckBox113
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button FakeyHelpButton
	{
		[CompilerGenerated]
		get
		{
			return _FakeyHelpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = FakeyHelpButton_Click;
			Button val = _FakeyHelpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_FakeyHelpButton = value;
			val = _FakeyHelpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("CheckBox110")]
	internal virtual CheckBox CheckBox110
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox111")]
	internal virtual CheckBox CheckBox111
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox114")]
	internal virtual CheckBox CheckBox114
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox115")]
	internal virtual CheckBox CheckBox115
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox116")]
	internal virtual CheckBox CheckBox116
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox117")]
	internal virtual CheckBox CheckBox117
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox118")]
	internal virtual CheckBox CheckBox118
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox119")]
	internal virtual CheckBox CheckBox119
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox120")]
	internal virtual CheckBox CheckBox120
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox121")]
	internal virtual CheckBox CheckBox121
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox122")]
	internal virtual CheckBox CheckBox122
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("NumTLUp")]
	internal virtual NumericUpDown NumTLUp
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("NumTLDown")]
	internal virtual NumericUpDown NumTLDown
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

	protected internal virtual MaskedTextBox GapSizeMTB
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

	internal virtual Button BullUpButton
	{
		[CompilerGenerated]
		get
		{
			return _BullUpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BullUpButton_Click;
			Button val = _BullUpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_BullUpButton = value;
			val = _BullUpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button BearUpButton
	{
		[CompilerGenerated]
		get
		{
			return _BearUpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BearUpButton_Click;
			Button val = _BearUpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_BearUpButton = value;
			val = _BearUpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button BearDownButton
	{
		[CompilerGenerated]
		get
		{
			return _BearDownButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BearDownButton_Click;
			Button val = _BearDownButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_BearDownButton = value;
			val = _BearDownButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button BullDownButton
	{
		[CompilerGenerated]
		get
		{
			return _BullDownButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BullDownButton_Click;
			Button val = _BullDownButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_BullDownButton = value;
			val = _BullDownButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button BARRHelpButton
	{
		[CompilerGenerated]
		get
		{
			return _BARRHelpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BARRHelpButton_Click;
			Button val = _BARRHelpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_BARRHelpButton = value;
			val = _BARRHelpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("CheckBox123")]
	internal virtual CheckBox CheckBox123
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public PatternsForm()
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		((Form)this).FormClosing += new FormClosingEventHandler(PatternsForm_FormClosing);
		((Form)this).Closed += PatternsForm_Closed;
		((Form)this).Load += PatternsForm_Load;
		AbortClosing = false;
		LockFlag = false;
		DefaultList = new bool[124]
		{
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, true, true, true, false, false,
			false, false, false, false, true, false, false, true, true, false,
			false, false, false, true, true, false, false, true, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false
		};
		SmallPats = new bool[124]
		{
			true, false, false, false, false, false, false, false, false, false,
			false, false, true, true, false, false, false, false, false, false,
			false, false, true, true, false, false, false, false, false, false,
			false, true, true, false, false, false, false, false, true, true,
			true, true, true, true, true, true, true, true, false, true,
			true, true, true, false, false, false, false, false, false, true,
			true, false, false, false, false, false, false, false, true, true,
			true, true, true, false, false, false, false, true, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false
		};
		BullUp = new bool[124]
		{
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, true,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, true, true, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, true, false, false, true, false, false, false, false, false,
			true, false, false, true, false, false, false, false, false, false,
			false, true, true, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false
		};
		BullDown = new bool[124]
		{
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, true, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, true, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, true, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, true, true, false,
			false, false, false, false, false, false, true, false, false, false,
			false, false, false, false
		};
		BearUp = new bool[124]
		{
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, true, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, true, false, false, false,
			false, false, false, false, false, false, true, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, true, false, false, false, true, false,
			false, false, false, true, true, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, true, false, false, false, false,
			false, false, false, false
		};
		BearDown = new bool[124]
		{
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, true, false,
			false, false, false, false, false, true, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, true, false, false, false, false, false, false,
			false, true, false, false, false, false, false, false, false, false,
			false, false, true, false, false, false, false, true, true, false,
			false, false, false, false, false, false, true, false, false, false,
			false, false, false, false
		};
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
		//IL_0011: Unknown result type (might be due to invalid IL or missing references)
		//IL_001b: Expected O, but got Unknown
		//IL_001c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0026: Expected O, but got Unknown
		//IL_0027: Unknown result type (might be due to invalid IL or missing references)
		//IL_0031: Expected O, but got Unknown
		//IL_0032: Unknown result type (might be due to invalid IL or missing references)
		//IL_003c: Expected O, but got Unknown
		//IL_003d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0047: Expected O, but got Unknown
		//IL_0048: Unknown result type (might be due to invalid IL or missing references)
		//IL_0052: Expected O, but got Unknown
		//IL_0053: Unknown result type (might be due to invalid IL or missing references)
		//IL_005d: Expected O, but got Unknown
		//IL_005e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0068: Expected O, but got Unknown
		//IL_0069: Unknown result type (might be due to invalid IL or missing references)
		//IL_0073: Expected O, but got Unknown
		//IL_0074: Unknown result type (might be due to invalid IL or missing references)
		//IL_007e: Expected O, but got Unknown
		//IL_007f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0089: Expected O, but got Unknown
		//IL_008a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0094: Expected O, but got Unknown
		//IL_0095: Unknown result type (might be due to invalid IL or missing references)
		//IL_009f: Expected O, but got Unknown
		//IL_00a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00aa: Expected O, but got Unknown
		//IL_00ab: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b5: Expected O, but got Unknown
		//IL_00b6: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c0: Expected O, but got Unknown
		//IL_00c1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00cb: Expected O, but got Unknown
		//IL_00cc: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d6: Expected O, but got Unknown
		//IL_00d7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e1: Expected O, but got Unknown
		//IL_00e2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ec: Expected O, but got Unknown
		//IL_00ed: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f7: Expected O, but got Unknown
		//IL_00f8: Unknown result type (might be due to invalid IL or missing references)
		//IL_0102: Expected O, but got Unknown
		//IL_0103: Unknown result type (might be due to invalid IL or missing references)
		//IL_010d: Expected O, but got Unknown
		//IL_010e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0118: Expected O, but got Unknown
		//IL_0119: Unknown result type (might be due to invalid IL or missing references)
		//IL_0123: Expected O, but got Unknown
		//IL_0124: Unknown result type (might be due to invalid IL or missing references)
		//IL_012e: Expected O, but got Unknown
		//IL_012f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0139: Expected O, but got Unknown
		//IL_013a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0144: Expected O, but got Unknown
		//IL_0145: Unknown result type (might be due to invalid IL or missing references)
		//IL_014f: Expected O, but got Unknown
		//IL_0150: Unknown result type (might be due to invalid IL or missing references)
		//IL_015a: Expected O, but got Unknown
		//IL_015b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0165: Expected O, but got Unknown
		//IL_0166: Unknown result type (might be due to invalid IL or missing references)
		//IL_0170: Expected O, but got Unknown
		//IL_0171: Unknown result type (might be due to invalid IL or missing references)
		//IL_017b: Expected O, but got Unknown
		//IL_017c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0186: Expected O, but got Unknown
		//IL_0187: Unknown result type (might be due to invalid IL or missing references)
		//IL_0191: Expected O, but got Unknown
		//IL_0192: Unknown result type (might be due to invalid IL or missing references)
		//IL_019c: Expected O, but got Unknown
		//IL_019d: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a7: Expected O, but got Unknown
		//IL_01a8: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b2: Expected O, but got Unknown
		//IL_01b3: Unknown result type (might be due to invalid IL or missing references)
		//IL_01bd: Expected O, but got Unknown
		//IL_01be: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c8: Expected O, but got Unknown
		//IL_01c9: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d3: Expected O, but got Unknown
		//IL_01d4: Unknown result type (might be due to invalid IL or missing references)
		//IL_01de: Expected O, but got Unknown
		//IL_01df: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e9: Expected O, but got Unknown
		//IL_01ea: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f4: Expected O, but got Unknown
		//IL_01f5: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ff: Expected O, but got Unknown
		//IL_0200: Unknown result type (might be due to invalid IL or missing references)
		//IL_020a: Expected O, but got Unknown
		//IL_020b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0215: Expected O, but got Unknown
		//IL_0216: Unknown result type (might be due to invalid IL or missing references)
		//IL_0220: Expected O, but got Unknown
		//IL_0221: Unknown result type (might be due to invalid IL or missing references)
		//IL_022b: Expected O, but got Unknown
		//IL_022c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0236: Expected O, but got Unknown
		//IL_0237: Unknown result type (might be due to invalid IL or missing references)
		//IL_0241: Expected O, but got Unknown
		//IL_0242: Unknown result type (might be due to invalid IL or missing references)
		//IL_024c: Expected O, but got Unknown
		//IL_024d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0257: Expected O, but got Unknown
		//IL_0258: Unknown result type (might be due to invalid IL or missing references)
		//IL_0262: Expected O, but got Unknown
		//IL_0263: Unknown result type (might be due to invalid IL or missing references)
		//IL_026d: Expected O, but got Unknown
		//IL_026e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0278: Expected O, but got Unknown
		//IL_0279: Unknown result type (might be due to invalid IL or missing references)
		//IL_0283: Expected O, but got Unknown
		//IL_0284: Unknown result type (might be due to invalid IL or missing references)
		//IL_028e: Expected O, but got Unknown
		//IL_028f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0299: Expected O, but got Unknown
		//IL_029a: Unknown result type (might be due to invalid IL or missing references)
		//IL_02a4: Expected O, but got Unknown
		//IL_02a5: Unknown result type (might be due to invalid IL or missing references)
		//IL_02af: Expected O, but got Unknown
		//IL_02b0: Unknown result type (might be due to invalid IL or missing references)
		//IL_02ba: Expected O, but got Unknown
		//IL_02bb: Unknown result type (might be due to invalid IL or missing references)
		//IL_02c5: Expected O, but got Unknown
		//IL_02c6: Unknown result type (might be due to invalid IL or missing references)
		//IL_02d0: Expected O, but got Unknown
		//IL_02d1: Unknown result type (might be due to invalid IL or missing references)
		//IL_02db: Expected O, but got Unknown
		//IL_02dc: Unknown result type (might be due to invalid IL or missing references)
		//IL_02e6: Expected O, but got Unknown
		//IL_02e7: Unknown result type (might be due to invalid IL or missing references)
		//IL_02f1: Expected O, but got Unknown
		//IL_02f2: Unknown result type (might be due to invalid IL or missing references)
		//IL_02fc: Expected O, but got Unknown
		//IL_02fd: Unknown result type (might be due to invalid IL or missing references)
		//IL_0307: Expected O, but got Unknown
		//IL_0308: Unknown result type (might be due to invalid IL or missing references)
		//IL_0312: Expected O, but got Unknown
		//IL_0313: Unknown result type (might be due to invalid IL or missing references)
		//IL_031d: Expected O, but got Unknown
		//IL_031e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0328: Expected O, but got Unknown
		//IL_0329: Unknown result type (might be due to invalid IL or missing references)
		//IL_0333: Expected O, but got Unknown
		//IL_0334: Unknown result type (might be due to invalid IL or missing references)
		//IL_033e: Expected O, but got Unknown
		//IL_033f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0349: Expected O, but got Unknown
		//IL_034a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0354: Expected O, but got Unknown
		//IL_0355: Unknown result type (might be due to invalid IL or missing references)
		//IL_035f: Expected O, but got Unknown
		//IL_0360: Unknown result type (might be due to invalid IL or missing references)
		//IL_036a: Expected O, but got Unknown
		//IL_036b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0375: Expected O, but got Unknown
		//IL_0376: Unknown result type (might be due to invalid IL or missing references)
		//IL_0380: Expected O, but got Unknown
		//IL_0381: Unknown result type (might be due to invalid IL or missing references)
		//IL_038b: Expected O, but got Unknown
		//IL_038c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0396: Expected O, but got Unknown
		//IL_0397: Unknown result type (might be due to invalid IL or missing references)
		//IL_03a1: Expected O, but got Unknown
		//IL_03a2: Unknown result type (might be due to invalid IL or missing references)
		//IL_03ac: Expected O, but got Unknown
		//IL_03ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_03b7: Expected O, but got Unknown
		//IL_03b8: Unknown result type (might be due to invalid IL or missing references)
		//IL_03c2: Expected O, but got Unknown
		//IL_03c3: Unknown result type (might be due to invalid IL or missing references)
		//IL_03cd: Expected O, but got Unknown
		//IL_03ce: Unknown result type (might be due to invalid IL or missing references)
		//IL_03d8: Expected O, but got Unknown
		//IL_03d9: Unknown result type (might be due to invalid IL or missing references)
		//IL_03e3: Expected O, but got Unknown
		//IL_03e4: Unknown result type (might be due to invalid IL or missing references)
		//IL_03ee: Expected O, but got Unknown
		//IL_03ef: Unknown result type (might be due to invalid IL or missing references)
		//IL_03f9: Expected O, but got Unknown
		//IL_03fa: Unknown result type (might be due to invalid IL or missing references)
		//IL_0404: Expected O, but got Unknown
		//IL_0405: Unknown result type (might be due to invalid IL or missing references)
		//IL_040f: Expected O, but got Unknown
		//IL_0410: Unknown result type (might be due to invalid IL or missing references)
		//IL_041a: Expected O, but got Unknown
		//IL_041b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0425: Expected O, but got Unknown
		//IL_0426: Unknown result type (might be due to invalid IL or missing references)
		//IL_0430: Expected O, but got Unknown
		//IL_0431: Unknown result type (might be due to invalid IL or missing references)
		//IL_043b: Expected O, but got Unknown
		//IL_043c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0446: Expected O, but got Unknown
		//IL_0447: Unknown result type (might be due to invalid IL or missing references)
		//IL_0451: Expected O, but got Unknown
		//IL_0452: Unknown result type (might be due to invalid IL or missing references)
		//IL_045c: Expected O, but got Unknown
		//IL_045d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0467: Expected O, but got Unknown
		//IL_0468: Unknown result type (might be due to invalid IL or missing references)
		//IL_0472: Expected O, but got Unknown
		//IL_0473: Unknown result type (might be due to invalid IL or missing references)
		//IL_047d: Expected O, but got Unknown
		//IL_047e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0488: Expected O, but got Unknown
		//IL_0489: Unknown result type (might be due to invalid IL or missing references)
		//IL_0493: Expected O, but got Unknown
		//IL_0494: Unknown result type (might be due to invalid IL or missing references)
		//IL_049e: Expected O, but got Unknown
		//IL_049f: Unknown result type (might be due to invalid IL or missing references)
		//IL_04a9: Expected O, but got Unknown
		//IL_04aa: Unknown result type (might be due to invalid IL or missing references)
		//IL_04b4: Expected O, but got Unknown
		//IL_04b5: Unknown result type (might be due to invalid IL or missing references)
		//IL_04bf: Expected O, but got Unknown
		//IL_04c0: Unknown result type (might be due to invalid IL or missing references)
		//IL_04ca: Expected O, but got Unknown
		//IL_04cb: Unknown result type (might be due to invalid IL or missing references)
		//IL_04d5: Expected O, but got Unknown
		//IL_04d6: Unknown result type (might be due to invalid IL or missing references)
		//IL_04e0: Expected O, but got Unknown
		//IL_04e1: Unknown result type (might be due to invalid IL or missing references)
		//IL_04eb: Expected O, but got Unknown
		//IL_04ec: Unknown result type (might be due to invalid IL or missing references)
		//IL_04f6: Expected O, but got Unknown
		//IL_04f7: Unknown result type (might be due to invalid IL or missing references)
		//IL_0501: Expected O, but got Unknown
		//IL_0502: Unknown result type (might be due to invalid IL or missing references)
		//IL_050c: Expected O, but got Unknown
		//IL_050d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0517: Expected O, but got Unknown
		//IL_0518: Unknown result type (might be due to invalid IL or missing references)
		//IL_0522: Expected O, but got Unknown
		//IL_0523: Unknown result type (might be due to invalid IL or missing references)
		//IL_052d: Expected O, but got Unknown
		//IL_052e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0538: Expected O, but got Unknown
		//IL_0539: Unknown result type (might be due to invalid IL or missing references)
		//IL_0543: Expected O, but got Unknown
		//IL_0544: Unknown result type (might be due to invalid IL or missing references)
		//IL_054e: Expected O, but got Unknown
		//IL_054f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0559: Expected O, but got Unknown
		//IL_055a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0564: Expected O, but got Unknown
		//IL_0565: Unknown result type (might be due to invalid IL or missing references)
		//IL_056f: Expected O, but got Unknown
		//IL_0570: Unknown result type (might be due to invalid IL or missing references)
		//IL_057a: Expected O, but got Unknown
		//IL_057b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0585: Expected O, but got Unknown
		//IL_0586: Unknown result type (might be due to invalid IL or missing references)
		//IL_0590: Expected O, but got Unknown
		//IL_0591: Unknown result type (might be due to invalid IL or missing references)
		//IL_059b: Expected O, but got Unknown
		//IL_059c: Unknown result type (might be due to invalid IL or missing references)
		//IL_05a6: Expected O, but got Unknown
		//IL_05a7: Unknown result type (might be due to invalid IL or missing references)
		//IL_05b1: Expected O, but got Unknown
		//IL_05b2: Unknown result type (might be due to invalid IL or missing references)
		//IL_05bc: Expected O, but got Unknown
		//IL_05bd: Unknown result type (might be due to invalid IL or missing references)
		//IL_05c7: Expected O, but got Unknown
		//IL_05c8: Unknown result type (might be due to invalid IL or missing references)
		//IL_05d2: Expected O, but got Unknown
		//IL_05d3: Unknown result type (might be due to invalid IL or missing references)
		//IL_05dd: Expected O, but got Unknown
		//IL_05de: Unknown result type (might be due to invalid IL or missing references)
		//IL_05e8: Expected O, but got Unknown
		//IL_05e9: Unknown result type (might be due to invalid IL or missing references)
		//IL_05f3: Expected O, but got Unknown
		//IL_05f4: Unknown result type (might be due to invalid IL or missing references)
		//IL_05fe: Expected O, but got Unknown
		//IL_05ff: Unknown result type (might be due to invalid IL or missing references)
		//IL_0609: Expected O, but got Unknown
		//IL_060a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0614: Expected O, but got Unknown
		//IL_0615: Unknown result type (might be due to invalid IL or missing references)
		//IL_061f: Expected O, but got Unknown
		//IL_0620: Unknown result type (might be due to invalid IL or missing references)
		//IL_062a: Expected O, but got Unknown
		//IL_062b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0635: Expected O, but got Unknown
		//IL_0636: Unknown result type (might be due to invalid IL or missing references)
		//IL_0640: Expected O, but got Unknown
		//IL_0641: Unknown result type (might be due to invalid IL or missing references)
		//IL_064b: Expected O, but got Unknown
		//IL_064c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0656: Expected O, but got Unknown
		//IL_0657: Unknown result type (might be due to invalid IL or missing references)
		//IL_0661: Expected O, but got Unknown
		//IL_3727: Unknown result type (might be due to invalid IL or missing references)
		//IL_3731: Expected O, but got Unknown
		//IL_38ee: Unknown result type (might be due to invalid IL or missing references)
		//IL_38f8: Expected O, but got Unknown
		//IL_39d9: Unknown result type (might be due to invalid IL or missing references)
		//IL_39e3: Expected O, but got Unknown
		//IL_3ac7: Unknown result type (might be due to invalid IL or missing references)
		//IL_3ad1: Expected O, but got Unknown
		//IL_3b48: Unknown result type (might be due to invalid IL or missing references)
		//IL_3b52: Expected O, but got Unknown
		//IL_405d: Unknown result type (might be due to invalid IL or missing references)
		//IL_4067: Expected O, but got Unknown
		//IL_46e1: Unknown result type (might be due to invalid IL or missing references)
		//IL_46eb: Expected O, but got Unknown
		//IL_490b: Unknown result type (might be due to invalid IL or missing references)
		//IL_4915: Expected O, but got Unknown
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(PatternsForm));
		CheckBox1 = new CheckBox();
		CheckBox2 = new CheckBox();
		CheckBox4 = new CheckBox();
		CheckBox3 = new CheckBox();
		CheckBox8 = new CheckBox();
		CheckBox7 = new CheckBox();
		CheckBox6 = new CheckBox();
		CheckBox5 = new CheckBox();
		CheckBox24 = new CheckBox();
		CheckBox23 = new CheckBox();
		CheckBox22 = new CheckBox();
		CheckBox21 = new CheckBox();
		CheckBox20 = new CheckBox();
		CheckBox19 = new CheckBox();
		CheckBox18 = new CheckBox();
		CheckBox17 = new CheckBox();
		CheckBox32 = new CheckBox();
		CheckBox31 = new CheckBox();
		CheckBox30 = new CheckBox();
		CheckBox29 = new CheckBox();
		CheckBox28 = new CheckBox();
		CheckBox27 = new CheckBox();
		CheckBox26 = new CheckBox();
		CheckBox25 = new CheckBox();
		CheckBox16 = new CheckBox();
		CheckBox15 = new CheckBox();
		CheckBox14 = new CheckBox();
		CheckBox13 = new CheckBox();
		CheckBox12 = new CheckBox();
		CheckBox11 = new CheckBox();
		CheckBox10 = new CheckBox();
		CheckBox9 = new CheckBox();
		DoneButton = new Button();
		DefaultButton = new Button();
		ClearButton = new Button();
		PctRiseMaskedTextBox = new MaskedTextBox();
		AllButton = new Button();
		CheckBox33 = new CheckBox();
		CheckBox34 = new CheckBox();
		CheckBox35 = new CheckBox();
		CheckBox36 = new CheckBox();
		CheckBox37 = new CheckBox();
		CheckBox38 = new CheckBox();
		CheckBox39 = new CheckBox();
		CheckBox40 = new CheckBox();
		CheckBox41 = new CheckBox();
		CheckBox42 = new CheckBox();
		GapUnknownCB = new CheckBox();
		CheckBox44 = new CheckBox();
		CheckBox45 = new CheckBox();
		CheckBox46 = new CheckBox();
		CheckBox47 = new CheckBox();
		CheckBox48 = new CheckBox();
		CheckBox49 = new CheckBox();
		CheckBox50 = new CheckBox();
		CheckBox51 = new CheckBox();
		CheckBox52 = new CheckBox();
		CheckBox53 = new CheckBox();
		CheckBox54 = new CheckBox();
		CheckBox56 = new CheckBox();
		CheckBox59 = new CheckBox();
		CheckBox60 = new CheckBox();
		CheckBox61 = new CheckBox();
		CheckBox62 = new CheckBox();
		CheckBox63 = new CheckBox();
		CheckBox64 = new CheckBox();
		CheckBox65 = new CheckBox();
		CheckBox66 = new CheckBox();
		CheckBox67 = new CheckBox();
		CheckBox68 = new CheckBox();
		CheckBox70 = new CheckBox();
		CheckBox71 = new CheckBox();
		CheckBox72 = new CheckBox();
		CheckBox73 = new CheckBox();
		CheckBox74 = new CheckBox();
		CheckBox75 = new CheckBox();
		CheckBox77 = new CheckBox();
		CheckBox78 = new CheckBox();
		CheckBox79 = new CheckBox();
		CheckBox80 = new CheckBox();
		CheckBox81 = new CheckBox();
		CheckBox82 = new CheckBox();
		CheckBox83 = new CheckBox();
		CheckBox84 = new CheckBox();
		CheckBox85 = new CheckBox();
		CheckBox86 = new CheckBox();
		CheckBox87 = new CheckBox();
		CheckBox88 = new CheckBox();
		CheckBox89 = new CheckBox();
		CheckBox90 = new CheckBox();
		CheckBox91 = new CheckBox();
		CheckBox92 = new CheckBox();
		CheckBox95 = new CheckBox();
		CheckBox96 = new CheckBox();
		CheckBox97 = new CheckBox();
		CheckBox98 = new CheckBox();
		CheckBox99 = new CheckBox();
		CheckBox100 = new CheckBox();
		CheckBox101 = new CheckBox();
		CheckBox106 = new CheckBox();
		CheckBox107 = new CheckBox();
		CheckBox57 = new CheckBox();
		CheckBox58 = new CheckBox();
		CheckBox69 = new CheckBox();
		CheckBox76 = new CheckBox();
		CheckBox93 = new CheckBox();
		CheckBox94 = new CheckBox();
		GapSizeMTB = new MaskedTextBox();
		Label2 = new Label();
		GroupBox1 = new GroupBox();
		GapHelpButton = new Button();
		SmallPatternsButton = new Button();
		WolfeHelpButton = new Button();
		InvertButton = new Button();
		ThreeBarButton = new Button();
		WarningLabel = new Label();
		CheckBox43 = new CheckBox();
		CheckBox55 = new CheckBox();
		CheckBox102 = new CheckBox();
		CheckBox103 = new CheckBox();
		CheckBox104 = new CheckBox();
		CheckBox105 = new CheckBox();
		CheckBox108 = new CheckBox();
		CheckBox109 = new CheckBox();
		CheckBox112 = new CheckBox();
		CheckBox113 = new CheckBox();
		FakeyHelpButton = new Button();
		CheckBox110 = new CheckBox();
		CheckBox111 = new CheckBox();
		CheckBox114 = new CheckBox();
		CheckBox115 = new CheckBox();
		CheckBox116 = new CheckBox();
		CheckBox117 = new CheckBox();
		CheckBox118 = new CheckBox();
		CheckBox119 = new CheckBox();
		CheckBox120 = new CheckBox();
		CheckBox121 = new CheckBox();
		CheckBox122 = new CheckBox();
		NumTLUp = new NumericUpDown();
		NumTLDown = new NumericUpDown();
		Label1 = new Label();
		BullUpButton = new Button();
		BearUpButton = new Button();
		BearDownButton = new Button();
		BullDownButton = new Button();
		BARRHelpButton = new Button();
		CheckBox123 = new CheckBox();
		((Control)GroupBox1).SuspendLayout();
		((ISupportInitialize)NumTLUp).BeginInit();
		((ISupportInitialize)NumTLDown).BeginInit();
		((Control)this).SuspendLayout();
		((ButtonBase)CheckBox1).AutoSize = true;
		((Control)CheckBox1).Location = new Point(12, 155);
		((Control)CheckBox1).Name = "CheckBox1";
		((Control)CheckBox1).Size = new Size(53, 17);
		((Control)CheckBox1).TabIndex = 10;
		((ButtonBase)CheckBox1).Text = "Big M";
		((ButtonBase)CheckBox1).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox2).AutoSize = true;
		((Control)CheckBox2).Location = new Point(12, 172);
		((Control)CheckBox2).Name = "CheckBox2";
		((Control)CheckBox2).Size = new Size(55, 17);
		((Control)CheckBox2).TabIndex = 11;
		((ButtonBase)CheckBox2).Text = "Big W";
		((ButtonBase)CheckBox2).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox4).AutoSize = true;
		((Control)CheckBox4).Location = new Point(12, 206);
		((Control)CheckBox4).Name = "CheckBox4";
		((Control)CheckBox4).Size = new Size(202, 17);
		((Control)CheckBox4).TabIndex = 13;
		((ButtonBase)CheckBox4).Text = "Broadening, right-angled && ascending";
		((ButtonBase)CheckBox4).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox3).AutoSize = true;
		((Control)CheckBox3).Location = new Point(12, 189);
		((Control)CheckBox3).Name = "CheckBox3";
		((Control)CheckBox3).Size = new Size(115, 17);
		((Control)CheckBox3).TabIndex = 12;
		((ButtonBase)CheckBox3).Text = "Broadening bottom";
		((ButtonBase)CheckBox3).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox8).AutoSize = true;
		((Control)CheckBox8).Location = new Point(12, 274);
		((Control)CheckBox8).Name = "CheckBox8";
		((Control)CheckBox8).Size = new Size(176, 17);
		((Control)CheckBox8).TabIndex = 17;
		((ButtonBase)CheckBox8).Text = "Broadening wedge, descending";
		((ButtonBase)CheckBox8).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox7).AutoSize = true;
		((Control)CheckBox7).Location = new Point(12, 257);
		((Control)CheckBox7).Name = "CheckBox7";
		((Control)CheckBox7).Size = new Size(170, 17);
		((Control)CheckBox7).TabIndex = 16;
		((ButtonBase)CheckBox7).Text = "Broadening wedge, ascending";
		((ButtonBase)CheckBox7).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox6).AutoSize = true;
		((Control)CheckBox6).Location = new Point(12, 240);
		((Control)CheckBox6).Name = "CheckBox6";
		((Control)CheckBox6).Size = new Size(98, 17);
		((Control)CheckBox6).TabIndex = 15;
		((ButtonBase)CheckBox6).Text = "Broadening top";
		((ButtonBase)CheckBox6).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox5).AutoSize = true;
		((Control)CheckBox5).Location = new Point(12, 223);
		((Control)CheckBox5).Name = "CheckBox5";
		((Control)CheckBox5).Size = new Size(208, 17);
		((Control)CheckBox5).TabIndex = 14;
		((ButtonBase)CheckBox5).Text = "Broadening, right-angled && descending";
		((ButtonBase)CheckBox5).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox24).AutoSize = true;
		((Control)CheckBox24).Location = new Point(476, 393);
		((Control)CheckBox24).Name = "CheckBox24";
		((Control)CheckBox24).Size = new Size(93, 17);
		((Control)CheckBox24).TabIndex = 88;
		((ButtonBase)CheckBox24).Text = "Rectangle top";
		((ButtonBase)CheckBox24).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox23).AutoSize = true;
		((Control)CheckBox23).Location = new Point(476, 376);
		((Control)CheckBox23).Name = "CheckBox23";
		((Control)CheckBox23).Size = new Size(110, 17);
		((Control)CheckBox23).TabIndex = 87;
		((ButtonBase)CheckBox23).Text = "Rectangle bottom";
		((ButtonBase)CheckBox23).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox22).AutoSize = true;
		((Control)CheckBox22).Location = new Point(476, 308);
		((Control)CheckBox22).Name = "CheckBox22";
		((Control)CheckBox22).Size = new Size(65, 17);
		((Control)CheckBox22).TabIndex = 83;
		((ButtonBase)CheckBox22).Text = "Pipe top";
		((ButtonBase)CheckBox22).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox21).AutoSize = true;
		((Control)CheckBox21).Location = new Point(476, 291);
		((Control)CheckBox21).Name = "CheckBox21";
		((Control)CheckBox21).Size = new Size(82, 17);
		((Control)CheckBox21).TabIndex = 82;
		((ButtonBase)CheckBox21).Text = "Pipe bottom";
		((ButtonBase)CheckBox21).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox20).AutoSize = true;
		((Control)CheckBox20).Location = new Point(476, 19);
		((Control)CheckBox20).Name = "CheckBox20";
		((Control)CheckBox20).Size = new Size(67, 17);
		((Control)CheckBox20).TabIndex = 66;
		((ButtonBase)CheckBox20).Text = "Horn top";
		((ButtonBase)CheckBox20).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox19).AutoSize = true;
		((Control)CheckBox19).Location = new Point(476, 2);
		((Control)CheckBox19).Name = "CheckBox19";
		((Control)CheckBox19).Size = new Size(84, 17);
		((Control)CheckBox19).TabIndex = 65;
		((ButtonBase)CheckBox19).Text = "Horn bottom";
		((ButtonBase)CheckBox19).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox18).AutoSize = true;
		((Control)CheckBox18).Location = new Point(241, 535);
		((Control)CheckBox18).Name = "CheckBox18";
		((Control)CheckBox18).Size = new Size(139, 17);
		((Control)CheckBox18).TabIndex = 62;
		((ButtonBase)CheckBox18).Text = "Head-and-shoulders top";
		((ButtonBase)CheckBox18).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox17).AutoSize = true;
		((Control)CheckBox17).Location = new Point(241, 518);
		((Control)CheckBox17).Name = "CheckBox17";
		((Control)CheckBox17).Size = new Size(181, 17);
		((Control)CheckBox17).TabIndex = 61;
		((ButtonBase)CheckBox17).Text = "Head-and-shoulders complex top";
		((ButtonBase)CheckBox17).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox32).AutoSize = true;
		((Control)CheckBox32).Location = new Point(685, 204);
		((Control)CheckBox32).Name = "CheckBox32";
		((Control)CheckBox32).Size = new Size(70, 17);
		((Control)CheckBox32).TabIndex = 114;
		((ButtonBase)CheckBox32).Text = "Triple top";
		((ButtonBase)CheckBox32).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox31).AutoSize = true;
		((Control)CheckBox31).Location = new Point(685, 186);
		((Control)CheckBox31).Name = "CheckBox31";
		((Control)CheckBox31).Size = new Size(87, 17);
		((Control)CheckBox31).TabIndex = 113;
		((ButtonBase)CheckBox31).Text = "Triple bottom";
		((ButtonBase)CheckBox31).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox30).AutoSize = true;
		((Control)CheckBox30).Location = new Point(685, 168);
		((Control)CheckBox30).Name = "CheckBox30";
		((Control)CheckBox30).Size = new Size(124, 17);
		((Control)CheckBox30).TabIndex = 112;
		((ButtonBase)CheckBox30).Text = "Triangle, symmetrical";
		((ButtonBase)CheckBox30).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox29).AutoSize = true;
		((Control)CheckBox29).Location = new Point(685, 150);
		((Control)CheckBox29).Name = "CheckBox29";
		((Control)CheckBox29).Size = new Size(125, 17);
		((Control)CheckBox29).TabIndex = 111;
		((ButtonBase)CheckBox29).Text = "Triangle, descending";
		((ButtonBase)CheckBox29).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox28).AutoSize = true;
		((Control)CheckBox28).Location = new Point(685, 132);
		((Control)CheckBox28).Name = "CheckBox28";
		((Control)CheckBox28).Size = new Size(119, 17);
		((Control)CheckBox28).TabIndex = 110;
		((ButtonBase)CheckBox28).Text = "Triangle, ascending";
		((ButtonBase)CheckBox28).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox27).AutoSize = true;
		((Control)CheckBox27).Location = new Point(685, 78);
		((Control)CheckBox27).Name = "CheckBox27";
		((Control)CheckBox27).Size = new Size(116, 17);
		((Control)CheckBox27).TabIndex = 104;
		((ButtonBase)CheckBox27).Text = "Three rising valleys";
		((ButtonBase)CheckBox27).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox26).AutoSize = true;
		((Control)CheckBox26).Location = new Point(685, 60);
		((Control)CheckBox26).Name = "CheckBox26";
		((Control)CheckBox26).Size = new Size(116, 17);
		((Control)CheckBox26).TabIndex = 103;
		((ButtonBase)CheckBox26).Text = "Three falling peaks";
		((ButtonBase)CheckBox26).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox25).AutoSize = true;
		((Control)CheckBox25).Location = new Point(476, 410);
		((Control)CheckBox25).Name = "CheckBox25";
		((Control)CheckBox25).Size = new Size(90, 17);
		((Control)CheckBox25).TabIndex = 89;
		((ButtonBase)CheckBox25).Text = "Rising wedge";
		((ButtonBase)CheckBox25).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox16).AutoSize = true;
		((Control)CheckBox16).Location = new Point(241, 501);
		((Control)CheckBox16).Name = "CheckBox16";
		((Control)CheckBox16).Size = new Size(198, 17);
		((Control)CheckBox16).TabIndex = 60;
		((ButtonBase)CheckBox16).Text = "Head-and-shoulders complex bottom";
		((ButtonBase)CheckBox16).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox15).AutoSize = true;
		((Control)CheckBox15).Location = new Point(241, 484);
		((Control)CheckBox15).Name = "CheckBox15";
		((Control)CheckBox15).Size = new Size(156, 17);
		((Control)CheckBox15).TabIndex = 59;
		((ButtonBase)CheckBox15).Text = "Head-and-shoulders bottom";
		((ButtonBase)CheckBox15).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox14).AutoSize = true;
		((Control)CheckBox14).Location = new Point(241, 274);
		((Control)CheckBox14).Name = "CheckBox14";
		((Control)CheckBox14).Size = new Size(116, 17);
		((Control)CheckBox14).TabIndex = 55;
		((ButtonBase)CheckBox14).Text = "Flag, high and tight";
		((ButtonBase)CheckBox14).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox13).AutoSize = true;
		((Control)CheckBox13).Location = new Point(241, 240);
		((Control)CheckBox13).Name = "CheckBox13";
		((Control)CheckBox13).Size = new Size(91, 17);
		((Control)CheckBox13).TabIndex = 53;
		((ButtonBase)CheckBox13).Text = "Falling wedge";
		((ButtonBase)CheckBox13).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox12).AutoSize = true;
		((Control)CheckBox12).Location = new Point(241, 121);
		((Control)CheckBox12).Name = "CheckBox12";
		((Control)CheckBox12).Size = new Size(78, 17);
		((Control)CheckBox12).TabIndex = 45;
		((ButtonBase)CheckBox12).Text = "Double top";
		((ButtonBase)CheckBox12).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox11).AutoSize = true;
		((Control)CheckBox11).Location = new Point(241, 36);
		((Control)CheckBox11).Name = "CheckBox11";
		((Control)CheckBox11).Size = new Size(95, 17);
		((Control)CheckBox11).TabIndex = 40;
		((ButtonBase)CheckBox11).Text = "Double bottom";
		((ButtonBase)CheckBox11).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox10).AutoSize = true;
		((Control)CheckBox10).Location = new Point(12, 546);
		((Control)CheckBox10).Name = "CheckBox10";
		((Control)CheckBox10).Size = new Size(189, 17);
		((Control)CheckBox10).TabIndex = 34;
		((ButtonBase)CheckBox10).Text = "Dead-cat bounce, inverted. % rise:";
		((ButtonBase)CheckBox10).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox9).AutoSize = true;
		((Control)CheckBox9).Location = new Point(12, 529);
		((Control)CheckBox9).Name = "CheckBox9";
		((Control)CheckBox9).Size = new Size(109, 17);
		((Control)CheckBox9).TabIndex = 33;
		((ButtonBase)CheckBox9).Text = "Dead-cat bounce";
		((ButtonBase)CheckBox9).UseVisualStyleBackColor = true;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(836, 547);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(69, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)DefaultButton).Location = new Point(836, 519);
		((Control)DefaultButton).Name = "DefaultButton";
		((Control)DefaultButton).Size = new Size(69, 23);
		((Control)DefaultButton).TabIndex = 136;
		((ButtonBase)DefaultButton).Text = "D&efault";
		((ButtonBase)DefaultButton).UseVisualStyleBackColor = true;
		((Control)ClearButton).Location = new Point(760, 518);
		((Control)ClearButton).Name = "ClearButton";
		((Control)ClearButton).Size = new Size(69, 23);
		((Control)ClearButton).TabIndex = 134;
		((ButtonBase)ClearButton).Text = "&Clear";
		((ButtonBase)ClearButton).UseVisualStyleBackColor = true;
		((Control)PctRiseMaskedTextBox).Location = new Point(201, 542);
		PctRiseMaskedTextBox.Mask = "##";
		((Control)PctRiseMaskedTextBox).Name = "PctRiseMaskedTextBox";
		((Control)PctRiseMaskedTextBox).Size = new Size(19, 20);
		((Control)PctRiseMaskedTextBox).TabIndex = 35;
		PctRiseMaskedTextBox.Text = "15";
		((Control)AllButton).Location = new Point(760, 547);
		((Control)AllButton).Name = "AllButton";
		((Control)AllButton).Size = new Size(69, 23);
		((Control)AllButton).TabIndex = 135;
		((ButtonBase)AllButton).Text = "Select &All";
		((ButtonBase)AllButton).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox33).AutoSize = true;
		((Control)CheckBox33).Location = new Point(12, 291);
		((Control)CheckBox33).Name = "CheckBox33";
		((Control)CheckBox33).Size = new Size(170, 17);
		((Control)CheckBox33).TabIndex = 18;
		((ButtonBase)CheckBox33).Text = "Bump-and-run reversal, bottom";
		((ButtonBase)CheckBox33).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox34).AutoSize = true;
		((Control)CheckBox34).Location = new Point(12, 308);
		((Control)CheckBox34).Name = "CheckBox34";
		((Control)CheckBox34).Size = new Size(153, 17);
		((Control)CheckBox34).TabIndex = 20;
		((ButtonBase)CheckBox34).Text = "Bump-and-run reversal, top";
		((ButtonBase)CheckBox34).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox35).AutoSize = true;
		((Control)CheckBox35).Location = new Point(12, 393);
		((Control)CheckBox35).Name = "CheckBox35";
		((Control)CheckBox35).Size = new Size(97, 17);
		((Control)CheckBox35).TabIndex = 25;
		((ButtonBase)CheckBox35).Text = "Channel, down";
		((ButtonBase)CheckBox35).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox36).AutoSize = true;
		((Control)CheckBox36).Location = new Point(12, 495);
		((Control)CheckBox36).Name = "CheckBox36";
		((Control)CheckBox36).Size = new Size(102, 17);
		((Control)CheckBox36).TabIndex = 31;
		((ButtonBase)CheckBox36).Text = "Cup with handle";
		((ButtonBase)CheckBox36).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox37).AutoSize = true;
		((Control)CheckBox37).Enabled = false;
		((Control)CheckBox37).Location = new Point(12, 563);
		((Control)CheckBox37).Name = "CheckBox37";
		((Control)CheckBox37).Size = new Size(103, 17);
		((Control)CheckBox37).TabIndex = 36;
		((ButtonBase)CheckBox37).Text = "Diamond bottom";
		((ButtonBase)CheckBox37).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox38).AutoSize = true;
		((Control)CheckBox38).Enabled = false;
		((Control)CheckBox38).Location = new Point(241, 2);
		((Control)CheckBox38).Name = "CheckBox38";
		((Control)CheckBox38).Size = new Size(86, 17);
		((Control)CheckBox38).TabIndex = 38;
		((ButtonBase)CheckBox38).Text = "Diamond top";
		((ButtonBase)CheckBox38).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox39).AutoSize = true;
		((Control)CheckBox39).Location = new Point(241, 257);
		((Control)CheckBox39).Name = "CheckBox39";
		((Control)CheckBox39).Size = new Size(46, 17);
		((Control)CheckBox39).TabIndex = 54;
		((ButtonBase)CheckBox39).Text = "Flag";
		((ButtonBase)CheckBox39).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox40).AutoSize = true;
		((Control)CheckBox40).Location = new Point(6, 70);
		((Control)CheckBox40).Name = "CheckBox40";
		((Control)CheckBox40).Size = new Size(104, 17);
		((Control)CheckBox40).TabIndex = 3;
		((ButtonBase)CheckBox40).Text = "Gap, breakaway";
		((ButtonBase)CheckBox40).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox41).AutoSize = true;
		((Control)CheckBox41).Location = new Point(6, 53);
		((Control)CheckBox41).Name = "CheckBox41";
		((Control)CheckBox41).Size = new Size(128, 17);
		((Control)CheckBox41).TabIndex = 2;
		((ButtonBase)CheckBox41).Text = "Gap, area or common";
		((ButtonBase)CheckBox41).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox42).AutoSize = true;
		((Control)CheckBox42).Location = new Point(6, 87);
		((Control)CheckBox42).Name = "CheckBox42";
		((Control)CheckBox42).Size = new Size(110, 17);
		((Control)CheckBox42).TabIndex = 4;
		((ButtonBase)CheckBox42).Text = "Gap, continuation";
		((ButtonBase)CheckBox42).UseVisualStyleBackColor = true;
		((ButtonBase)GapUnknownCB).AutoSize = true;
		((Control)GapUnknownCB).Location = new Point(6, 121);
		((Control)GapUnknownCB).Name = "GapUnknownCB";
		((Control)GapUnknownCB).Size = new Size(119, 17);
		((Control)GapUnknownCB).TabIndex = 6;
		((ButtonBase)GapUnknownCB).Text = "Gap, type unknown";
		((ButtonBase)GapUnknownCB).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox44).AutoSize = true;
		((Control)CheckBox44).Location = new Point(6, 104);
		((Control)CheckBox44).Name = "CheckBox44";
		((Control)CheckBox44).Size = new Size(103, 17);
		((Control)CheckBox44).TabIndex = 5;
		((ButtonBase)CheckBox44).Text = "Gap, exhaustion";
		((ButtonBase)CheckBox44).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox45).AutoSize = true;
		((Control)CheckBox45).Location = new Point(476, 36);
		((Control)CheckBox45).Name = "CheckBox45";
		((Control)CheckBox45).Size = new Size(74, 17);
		((Control)CheckBox45).TabIndex = 67;
		((ButtonBase)CheckBox45).Text = "Inside day";
		((ButtonBase)CheckBox45).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox46).AutoSize = true;
		((Control)CheckBox46).Location = new Point(476, 53);
		((Control)CheckBox46).Name = "CheckBox46";
		((Control)CheckBox46).Size = new Size(132, 17);
		((Control)CheckBox46).TabIndex = 68;
		((ButtonBase)CheckBox46).Text = "Island reversal, bottom";
		((ButtonBase)CheckBox46).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox47).AutoSize = true;
		((Control)CheckBox47).Location = new Point(476, 70);
		((Control)CheckBox47).Name = "CheckBox47";
		((Control)CheckBox47).Size = new Size(115, 17);
		((Control)CheckBox47).TabIndex = 69;
		((ButtonBase)CheckBox47).Text = "Island reversal, top";
		((ButtonBase)CheckBox47).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox48).AutoSize = true;
		((Control)CheckBox48).Location = new Point(476, 121);
		((Control)CheckBox48).Name = "CheckBox48";
		((Control)CheckBox48).Size = new Size(131, 17);
		((Control)CheckBox48).TabIndex = 72;
		((ButtonBase)CheckBox48).Text = "Measured move down";
		((ButtonBase)CheckBox48).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox49).AutoSize = true;
		((Control)CheckBox49).Location = new Point(476, 138);
		((Control)CheckBox49).Name = "CheckBox49";
		((Control)CheckBox49).Size = new Size(117, 17);
		((Control)CheckBox49).TabIndex = 73;
		((ButtonBase)CheckBox49).Text = "Measured move up";
		((ButtonBase)CheckBox49).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox50).AutoSize = true;
		((Control)CheckBox50).Location = new Point(476, 155);
		((Control)CheckBox50).Name = "CheckBox50";
		((Control)CheckBox50).Size = new Size(99, 17);
		((Control)CheckBox50).TabIndex = 74;
		((ButtonBase)CheckBox50).Text = "Narrow range 4";
		((ButtonBase)CheckBox50).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox51).AutoSize = true;
		((Control)CheckBox51).Location = new Point(476, 172);
		((Control)CheckBox51).Name = "CheckBox51";
		((Control)CheckBox51).Size = new Size(99, 17);
		((Control)CheckBox51).TabIndex = 75;
		((ButtonBase)CheckBox51).Text = "Narrow range 7";
		((ButtonBase)CheckBox51).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox52).AutoSize = true;
		((Control)CheckBox52).Location = new Point(476, 189);
		((Control)CheckBox52).Name = "CheckBox52";
		((Control)CheckBox52).Size = new Size(144, 17);
		((Control)CheckBox52).TabIndex = 76;
		((ButtonBase)CheckBox52).Text = "One day reversal, bottom";
		((ButtonBase)CheckBox52).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox53).AutoSize = true;
		((Control)CheckBox53).Location = new Point(476, 206);
		((Control)CheckBox53).Name = "CheckBox53";
		((Control)CheckBox53).Size = new Size(127, 17);
		((Control)CheckBox53).TabIndex = 77;
		((ButtonBase)CheckBox53).Text = "One day reversal, top";
		((ButtonBase)CheckBox53).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox54).AutoSize = true;
		((Control)CheckBox54).Location = new Point(476, 257);
		((Control)CheckBox54).Name = "CheckBox54";
		((Control)CheckBox54).Size = new Size(82, 17);
		((Control)CheckBox54).TabIndex = 80;
		((ButtonBase)CheckBox54).Text = "Outside day";
		((ButtonBase)CheckBox54).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox56).AutoSize = true;
		((Control)CheckBox56).Location = new Point(476, 274);
		((Control)CheckBox56).Name = "CheckBox56";
		((Control)CheckBox56).Size = new Size(66, 17);
		((Control)CheckBox56).TabIndex = 81;
		((ButtonBase)CheckBox56).Text = "Pennant";
		((ButtonBase)CheckBox56).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox59).AutoSize = true;
		((Control)CheckBox59).Location = new Point(476, 444);
		((Control)CheckBox59).Name = "CheckBox59";
		((Control)CheckBox59).Size = new Size(107, 17);
		((Control)CheckBox59).TabIndex = 91;
		((ButtonBase)CheckBox59).Text = "Rounding bottom";
		((ButtonBase)CheckBox59).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox60).AutoSize = true;
		((Control)CheckBox60).Location = new Point(476, 461);
		((Control)CheckBox60).Name = "CheckBox60";
		((Control)CheckBox60).Size = new Size(90, 17);
		((Control)CheckBox60).TabIndex = 92;
		((ButtonBase)CheckBox60).Text = "Rounding top";
		((ButtonBase)CheckBox60).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox61).AutoSize = true;
		((Control)CheckBox61).Enabled = false;
		((Control)CheckBox61).Location = new Point(476, 495);
		((Control)CheckBox61).Name = "CheckBox61";
		((Control)CheckBox61).Size = new Size(116, 17);
		((Control)CheckBox61).TabIndex = 94;
		((ButtonBase)CheckBox61).Text = "Scallop, ascending";
		((ButtonBase)CheckBox61).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox62).AutoSize = true;
		((Control)CheckBox62).Enabled = false;
		((Control)CheckBox62).Location = new Point(476, 529);
		((Control)CheckBox62).Name = "CheckBox62";
		((Control)CheckBox62).Size = new Size(119, 17);
		((Control)CheckBox62).TabIndex = 96;
		((ButtonBase)CheckBox62).Text = "Scallop descending";
		((ButtonBase)CheckBox62).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox63).AutoSize = true;
		((Control)CheckBox63).Enabled = false;
		((Control)CheckBox63).Location = new Point(476, 512);
		((Control)CheckBox63).Name = "CheckBox63";
		((Control)CheckBox63).Size = new Size(178, 17);
		((Control)CheckBox63).TabIndex = 95;
		((ButtonBase)CheckBox63).Text = "Scallop, ascending and inverted";
		((ButtonBase)CheckBox63).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox64).AutoSize = true;
		((Control)CheckBox64).Enabled = false;
		((Control)CheckBox64).Location = new Point(476, 546);
		((Control)CheckBox64).Name = "CheckBox64";
		((Control)CheckBox64).Size = new Size(184, 17);
		((Control)CheckBox64).TabIndex = 97;
		((ButtonBase)CheckBox64).Text = "Scallop, descending and inverted";
		((ButtonBase)CheckBox64).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox65).AutoSize = true;
		((Control)CheckBox65).Location = new Point(476, 563);
		((Control)CheckBox65).Name = "CheckBox65";
		((Control)CheckBox65).Size = new Size(69, 17);
		((Control)CheckBox65).TabIndex = 98;
		((ButtonBase)CheckBox65).Text = "Shark-32";
		((ButtonBase)CheckBox65).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox66).AutoSize = true;
		((Control)CheckBox66).Location = new Point(685, 42);
		((Control)CheckBox66).Name = "CheckBox66";
		((Control)CheckBox66).Size = new Size(123, 17);
		((Control)CheckBox66).TabIndex = 101;
		((ButtonBase)CheckBox66).Text = "Three-bar (long only)";
		((ButtonBase)CheckBox66).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox67).AutoSize = true;
		((Control)CheckBox67).Location = new Point(685, 96);
		((Control)CheckBox67).Name = "CheckBox67";
		((Control)CheckBox67).Size = new Size(102, 17);
		((Control)CheckBox67).TabIndex = 105;
		((ButtonBase)CheckBox67).Text = "Trendline, down";
		((ButtonBase)CheckBox67).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox68).AutoSize = true;
		((Control)CheckBox68).Location = new Point(685, 114);
		((Control)CheckBox68).Name = "CheckBox68";
		((Control)CheckBox68).Size = new Size(88, 17);
		((Control)CheckBox68).TabIndex = 108;
		((ButtonBase)CheckBox68).Text = "Trendline, up";
		((ButtonBase)CheckBox68).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox70).AutoSize = true;
		((Control)CheckBox70).Location = new Point(685, 258);
		((Control)CheckBox70).Name = "CheckBox70";
		((Control)CheckBox70).Size = new Size(68, 17);
		((Control)CheckBox70).TabIndex = 117;
		((ButtonBase)CheckBox70).Text = "V bottom";
		((ButtonBase)CheckBox70).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox71).AutoSize = true;
		((Control)CheckBox71).Location = new Point(685, 276);
		((Control)CheckBox71).Name = "CheckBox71";
		((Control)CheckBox71).Size = new Size(51, 17);
		((Control)CheckBox71).TabIndex = 118;
		((ButtonBase)CheckBox71).Text = "V top";
		((ButtonBase)CheckBox71).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox72).AutoSize = true;
		((Control)CheckBox72).Location = new Point(685, 330);
		((Control)CheckBox72).Name = "CheckBox72";
		((Control)CheckBox72).Size = new Size(140, 17);
		((Control)CheckBox72).TabIndex = 121;
		((ButtonBase)CheckBox72).Text = "Weekly reversal, bottom";
		((ButtonBase)CheckBox72).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox73).AutoSize = true;
		((Control)CheckBox73).Location = new Point(685, 348);
		((Control)CheckBox73).Name = "CheckBox73";
		((Control)CheckBox73).Size = new Size(123, 17);
		((Control)CheckBox73).TabIndex = 122;
		((ButtonBase)CheckBox73).Text = "Weekly reversal, top";
		((ButtonBase)CheckBox73).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox74).AutoSize = true;
		((Control)CheckBox74).ForeColor = SystemColors.ControlText;
		((Control)CheckBox74).Location = new Point(6, 19);
		((Control)CheckBox74).Name = "CheckBox74";
		((Control)CheckBox74).Size = new Size(63, 17);
		((Control)CheckBox74).TabIndex = 0;
		((ButtonBase)CheckBox74).Text = "Gap 2H";
		((ButtonBase)CheckBox74).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox75).AutoSize = true;
		((Control)CheckBox75).ForeColor = SystemColors.ControlText;
		((Control)CheckBox75).Location = new Point(6, 36);
		((Control)CheckBox75).Name = "CheckBox75";
		((Control)CheckBox75).Size = new Size(107, 17);
		((Control)CheckBox75).TabIndex = 1;
		((ButtonBase)CheckBox75).Text = "Gap 2H, inverted";
		((ButtonBase)CheckBox75).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox77).AutoSize = true;
		((Control)CheckBox77).Location = new Point(12, 427);
		((Control)CheckBox77).Name = "CheckBox77";
		((Control)CheckBox77).Size = new Size(182, 17);
		((Control)CheckBox77).TabIndex = 27;
		((ButtonBase)CheckBox77).Text = "Closing price reversal, downtrend";
		((ButtonBase)CheckBox77).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox78).AutoSize = true;
		((Control)CheckBox78).Location = new Point(12, 444);
		((Control)CheckBox78).Name = "CheckBox78";
		((Control)CheckBox78).Size = new Size(168, 17);
		((Control)CheckBox78).TabIndex = 28;
		((ButtonBase)CheckBox78).Text = "Closing price reversal, uptrend";
		((ButtonBase)CheckBox78).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox79).AutoSize = true;
		((Control)CheckBox79).Location = new Point(241, 552);
		((Control)CheckBox79).Name = "CheckBox79";
		((Control)CheckBox79).Size = new Size(148, 17);
		((Control)CheckBox79).TabIndex = 63;
		((ButtonBase)CheckBox79).Text = "Hook reversal, downtrend";
		((ButtonBase)CheckBox79).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox80).AutoSize = true;
		((Control)CheckBox80).Location = new Point(241, 569);
		((Control)CheckBox80).Name = "CheckBox80";
		((Control)CheckBox80).Size = new Size(134, 17);
		((Control)CheckBox80).TabIndex = 64;
		((ButtonBase)CheckBox80).Text = "Hook reversal, uptrend";
		((ButtonBase)CheckBox80).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox81).AutoSize = true;
		((Control)CheckBox81).Location = new Point(12, 512);
		((Control)CheckBox81).Name = "CheckBox81";
		((Control)CheckBox81).Size = new Size(146, 17);
		((Control)CheckBox81).TabIndex = 32;
		((ButtonBase)CheckBox81).Text = "Cup with handle, inverted";
		((ButtonBase)CheckBox81).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox82).AutoSize = true;
		((Control)CheckBox82).Location = new Point(476, 87);
		((Control)CheckBox82).Name = "CheckBox82";
		((Control)CheckBox82).Size = new Size(140, 17);
		((Control)CheckBox82).TabIndex = 70;
		((ButtonBase)CheckBox82).Text = "Key reversal, downtrend";
		((ButtonBase)CheckBox82).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox83).AutoSize = true;
		((Control)CheckBox83).Location = new Point(476, 104);
		((Control)CheckBox83).Name = "CheckBox83";
		((Control)CheckBox83).Size = new Size(126, 17);
		((Control)CheckBox83).TabIndex = 71;
		((ButtonBase)CheckBox83).Text = "Key reversal, uptrend";
		((ButtonBase)CheckBox83).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox84).AutoSize = true;
		((Control)CheckBox84).Location = new Point(476, 223);
		((Control)CheckBox84).Name = "CheckBox84";
		((Control)CheckBox84).Size = new Size(176, 17);
		((Control)CheckBox84).TabIndex = 78;
		((ButtonBase)CheckBox84).Text = "Open-close reversal, downtrend";
		((ButtonBase)CheckBox84).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox85).AutoSize = true;
		((Control)CheckBox85).Location = new Point(476, 240);
		((Control)CheckBox85).Name = "CheckBox85";
		((Control)CheckBox85).Size = new Size(162, 17);
		((Control)CheckBox85).TabIndex = 79;
		((ButtonBase)CheckBox85).Text = "Open close reversal, uptrend";
		((ButtonBase)CheckBox85).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox86).AutoSize = true;
		((Control)CheckBox86).Location = new Point(476, 325);
		((Control)CheckBox86).Name = "CheckBox86";
		((Control)CheckBox86).Size = new Size(172, 17);
		((Control)CheckBox86).TabIndex = 84;
		((ButtonBase)CheckBox86).Text = "Pivot point reversal, downtrend";
		((ButtonBase)CheckBox86).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox87).AutoSize = true;
		((Control)CheckBox87).Location = new Point(476, 342);
		((Control)CheckBox87).Name = "CheckBox87";
		((Control)CheckBox87).Size = new Size(158, 17);
		((Control)CheckBox87).TabIndex = 85;
		((ButtonBase)CheckBox87).Text = "Pivot point reversal, uptrend";
		((ButtonBase)CheckBox87).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox88).AutoSize = true;
		((Control)CheckBox88).Location = new Point(685, 25);
		((Control)CheckBox88).Name = "CheckBox88";
		((Control)CheckBox88).Size = new Size(68, 17);
		((Control)CheckBox88).TabIndex = 100;
		((ButtonBase)CheckBox88).Text = "Spike up";
		((ButtonBase)CheckBox88).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox89).AutoSize = true;
		((Control)CheckBox89).Location = new Point(685, 7);
		((Control)CheckBox89).Name = "CheckBox89";
		((Control)CheckBox89).Size = new Size(82, 17);
		((Control)CheckBox89).TabIndex = 99;
		((ButtonBase)CheckBox89).Text = "Spike down";
		((ButtonBase)CheckBox89).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox90).AutoSize = true;
		((Control)CheckBox90).Location = new Point(685, 366);
		((Control)CheckBox90).Name = "CheckBox90";
		((Control)CheckBox90).Size = new Size(181, 17);
		((Control)CheckBox90).TabIndex = 123;
		((ButtonBase)CheckBox90).Text = "Wide ranging day, down reversal";
		((ButtonBase)CheckBox90).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox91).AutoSize = true;
		((Control)CheckBox91).Location = new Point(685, 384);
		((Control)CheckBox91).Name = "CheckBox91";
		((Control)CheckBox91).Size = new Size(167, 17);
		((Control)CheckBox91).TabIndex = 124;
		((ButtonBase)CheckBox91).Text = "Wide ranging day, up reversal";
		((ButtonBase)CheckBox91).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox92).AutoSize = true;
		((Control)CheckBox92).Location = new Point(476, 359);
		((Control)CheckBox92).Name = "CheckBox92";
		((Control)CheckBox92).Size = new Size(62, 17);
		((Control)CheckBox92).TabIndex = 86;
		((ButtonBase)CheckBox92).Text = "Pothole";
		((ButtonBase)CheckBox92).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox95).AutoSize = true;
		((Control)CheckBox95).Enabled = false;
		((Control)CheckBox95).Location = new Point(476, 478);
		((Control)CheckBox95).Name = "CheckBox95";
		((Control)CheckBox95).Size = new Size(49, 17);
		((Control)CheckBox95).TabIndex = 93;
		((ButtonBase)CheckBox95).Text = "Roof";
		((ButtonBase)CheckBox95).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox96).AutoSize = true;
		((Control)CheckBox96).Enabled = false;
		((Control)CheckBox96).Location = new Point(476, 427);
		((Control)CheckBox96).Name = "CheckBox96";
		((Control)CheckBox96).Size = new Size(93, 17);
		((Control)CheckBox96).TabIndex = 90;
		((ButtonBase)CheckBox96).Text = "Roof, inverted";
		((ButtonBase)CheckBox96).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox97).AutoSize = true;
		((Control)CheckBox97).Location = new Point(685, 222);
		((Control)CheckBox97).Name = "CheckBox97";
		((Control)CheckBox97).Size = new Size(117, 17);
		((Control)CheckBox97).TabIndex = 115;
		((ButtonBase)CheckBox97).Text = "Ugly double bottom";
		((ButtonBase)CheckBox97).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox98).AutoSize = true;
		((Control)CheckBox98).Location = new Point(685, 240);
		((Control)CheckBox98).Name = "CheckBox98";
		((Control)CheckBox98).Size = new Size(100, 17);
		((Control)CheckBox98).TabIndex = 116;
		((ButtonBase)CheckBox98).Text = "Ugly double top";
		((ButtonBase)CheckBox98).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox99).AutoSize = true;
		((Control)CheckBox99).Location = new Point(12, 53);
		((Control)CheckBox99).Name = "CheckBox99";
		((Control)CheckBox99).Size = new Size(49, 17);
		((Control)CheckBox99).TabIndex = 4;
		((ButtonBase)CheckBox99).Text = "3L-R";
		((ButtonBase)CheckBox99).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox100).AutoSize = true;
		((Control)CheckBox100).Location = new Point(12, 70);
		((Control)CheckBox100).Name = "CheckBox100";
		((Control)CheckBox100).Size = new Size(93, 17);
		((Control)CheckBox100).TabIndex = 5;
		((ButtonBase)CheckBox100).Text = "3L-R, inverted";
		((ButtonBase)CheckBox100).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox101).AutoSize = true;
		((Control)CheckBox101).Location = new Point(241, 19);
		((Control)CheckBox101).Name = "CheckBox101";
		((Control)CheckBox101).Size = new Size(86, 17);
		((Control)CheckBox101).TabIndex = 39;
		((ButtonBase)CheckBox101).Text = "Diving board";
		((ButtonBase)CheckBox101).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox106).AutoSize = true;
		((Control)CheckBox106).Location = new Point(241, 467);
		((Control)CheckBox106).Name = "CheckBox106";
		((Control)CheckBox106).Size = new Size(94, 17);
		((Control)CheckBox106).TabIndex = 58;
		((ButtonBase)CheckBox106).Text = "Gartley, bullish";
		((ButtonBase)CheckBox106).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox107).AutoSize = true;
		((Control)CheckBox107).Location = new Point(241, 450);
		((Control)CheckBox107).Name = "CheckBox107";
		((Control)CheckBox107).Size = new Size(99, 17);
		((Control)CheckBox107).TabIndex = 57;
		((ButtonBase)CheckBox107).Text = "Gartley, bearish";
		((ButtonBase)CheckBox107).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox57).AutoSize = true;
		((Control)CheckBox57).Location = new Point(685, 402);
		((Control)CheckBox57).Name = "CheckBox57";
		((Control)CheckBox57).Size = new Size(131, 17);
		((Control)CheckBox57).TabIndex = 125;
		((ButtonBase)CheckBox57).Text = "Wolfe wave®, bearish";
		((ButtonBase)CheckBox57).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox58).AutoSize = true;
		((Control)CheckBox58).Location = new Point(685, 420);
		((Control)CheckBox58).Name = "CheckBox58";
		((Control)CheckBox58).Size = new Size(126, 17);
		((Control)CheckBox58).TabIndex = 126;
		((ButtonBase)CheckBox58).Text = "Wolfe wave®, bullish";
		((ButtonBase)CheckBox58).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox69).AutoSize = true;
		((Control)CheckBox69).Location = new Point(685, 312);
		((Control)CheckBox69).Name = "CheckBox69";
		((Control)CheckBox69).Size = new Size(94, 17);
		((Control)CheckBox69).TabIndex = 120;
		((ButtonBase)CheckBox69).Text = "Vertical run up";
		((ButtonBase)CheckBox69).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox76).AutoSize = true;
		((Control)CheckBox76).Location = new Point(685, 294);
		((Control)CheckBox76).Name = "CheckBox76";
		((Control)CheckBox76).Size = new Size(108, 17);
		((Control)CheckBox76).TabIndex = 119;
		((ButtonBase)CheckBox76).Text = "Vertical run down";
		((ButtonBase)CheckBox76).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox93).AutoSize = true;
		((Control)CheckBox93).Location = new Point(12, 19);
		((Control)CheckBox93).Name = "CheckBox93";
		((Control)CheckBox93).Size = new Size(51, 17);
		((Control)CheckBox93).TabIndex = 2;
		((ButtonBase)CheckBox93).Text = "2-Did";
		((ButtonBase)CheckBox93).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox94).AutoSize = true;
		((Control)CheckBox94).Location = new Point(12, 36);
		((Control)CheckBox94).Name = "CheckBox94";
		((Control)CheckBox94).Size = new Size(52, 17);
		((Control)CheckBox94).TabIndex = 3;
		((ButtonBase)CheckBox94).Text = "2-Tall";
		((ButtonBase)CheckBox94).UseVisualStyleBackColor = true;
		GapSizeMTB.AsciiOnly = true;
		((Control)GapSizeMTB).Location = new Point(122, 70);
		GapSizeMTB.Mask = "###.########";
		((Control)GapSizeMTB).Name = "GapSizeMTB";
		GapSizeMTB.ResetOnSpace = false;
		((Control)GapSizeMTB).Size = new Size(84, 20);
		GapSizeMTB.SkipLiterals = false;
		((Control)GapSizeMTB).TabIndex = 8;
		GapSizeMTB.Text = "00020000000";
		((Control)Label2).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)Label2).Location = new Point(136, 21);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(66, 41);
		((Control)Label2).TabIndex = 7;
		Label2.Text = "Min gap size (all gaps)";
		Label2.TextAlign = (ContentAlignment)32;
		((Control)GroupBox1).Controls.Add((Control)(object)GapHelpButton);
		((Control)GroupBox1).Controls.Add((Control)(object)GapSizeMTB);
		((Control)GroupBox1).Controls.Add((Control)(object)Label2);
		((Control)GroupBox1).Controls.Add((Control)(object)CheckBox40);
		((Control)GroupBox1).Controls.Add((Control)(object)CheckBox41);
		((Control)GroupBox1).Controls.Add((Control)(object)CheckBox42);
		((Control)GroupBox1).Controls.Add((Control)(object)GapUnknownCB);
		((Control)GroupBox1).Controls.Add((Control)(object)CheckBox44);
		((Control)GroupBox1).Controls.Add((Control)(object)CheckBox74);
		((Control)GroupBox1).Controls.Add((Control)(object)CheckBox75);
		((Control)GroupBox1).Location = new Point(241, 293);
		((Control)GroupBox1).Name = "GroupBox1";
		((Control)GroupBox1).Size = new Size(212, 144);
		((Control)GroupBox1).TabIndex = 56;
		GroupBox1.TabStop = false;
		((Control)GapHelpButton).Anchor = (AnchorStyles)10;
		((Control)GapHelpButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)GapHelpButton).Location = new Point(136, 118);
		((Control)GapHelpButton).Name = "GapHelpButton";
		((Control)GapHelpButton).Size = new Size(20, 20);
		((Control)GapHelpButton).TabIndex = 9;
		((ButtonBase)GapHelpButton).Text = "?";
		((ButtonBase)GapHelpButton).UseVisualStyleBackColor = true;
		((Control)SmallPatternsButton).Location = new Point(664, 547);
		((Control)SmallPatternsButton).Name = "SmallPatternsButton";
		((Control)SmallPatternsButton).Size = new Size(89, 23);
		((Control)SmallPatternsButton).TabIndex = 131;
		((ButtonBase)SmallPatternsButton).Text = "Small &Patterns";
		((ButtonBase)SmallPatternsButton).UseVisualStyleBackColor = true;
		((Control)WolfeHelpButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)WolfeHelpButton).Location = new Point(842, 400);
		((Control)WolfeHelpButton).Name = "WolfeHelpButton";
		((Control)WolfeHelpButton).Size = new Size(63, 40);
		((Control)WolfeHelpButton).TabIndex = 127;
		((ButtonBase)WolfeHelpButton).Text = "Wolfe W Note!";
		((ButtonBase)WolfeHelpButton).UseVisualStyleBackColor = true;
		((Control)InvertButton).Location = new Point(664, 518);
		((Control)InvertButton).Name = "InvertButton";
		((Control)InvertButton).Size = new Size(69, 23);
		((Control)InvertButton).TabIndex = 130;
		((ButtonBase)InvertButton).Text = "In&vert";
		((ButtonBase)InvertButton).UseVisualStyleBackColor = true;
		((Control)ThreeBarButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)ThreeBarButton).Location = new Point(814, 41);
		((Control)ThreeBarButton).Name = "ThreeBarButton";
		((Control)ThreeBarButton).Size = new Size(20, 20);
		((Control)ThreeBarButton).TabIndex = 102;
		((ButtonBase)ThreeBarButton).Text = "?";
		((ButtonBase)ThreeBarButton).UseVisualStyleBackColor = true;
		((Control)WarningLabel).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)WarningLabel).Location = new Point(-6, 589);
		((Control)WarningLabel).Name = "WarningLabel";
		((Control)WarningLabel).Size = new Size(910, 39);
		((Control)WarningLabel).TabIndex = 37;
		WarningLabel.Text = componentResourceManager.GetString("WarningLabel.Text");
		WarningLabel.TextAlign = (ContentAlignment)32;
		((ButtonBase)CheckBox43).AutoSize = true;
		((Control)CheckBox43).Location = new Point(241, 70);
		((Control)CheckBox43).Name = "CheckBox43";
		((Control)CheckBox43).Size = new Size(159, 17);
		((Control)CheckBox43).TabIndex = 42;
		((ButtonBase)CheckBox43).Text = "Double bottom, Adam && Eve";
		((ButtonBase)CheckBox43).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox55).AutoSize = true;
		((Control)CheckBox55).Location = new Point(241, 53);
		((Control)CheckBox55).Name = "CheckBox55";
		((Control)CheckBox55).Size = new Size(167, 17);
		((Control)CheckBox55).TabIndex = 41;
		((ButtonBase)CheckBox55).Text = "Double bottom, Adam && Adam";
		((ButtonBase)CheckBox55).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox102).AutoSize = true;
		((Control)CheckBox102).Location = new Point(241, 87);
		((Control)CheckBox102).Name = "CheckBox102";
		((Control)CheckBox102).Size = new Size(159, 17);
		((Control)CheckBox102).TabIndex = 43;
		((ButtonBase)CheckBox102).Text = "Double bottom, Eve && Adam";
		((ButtonBase)CheckBox102).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox103).AutoSize = true;
		((Control)CheckBox103).Location = new Point(241, 104);
		((Control)CheckBox103).Name = "CheckBox103";
		((Control)CheckBox103).Size = new Size(151, 17);
		((Control)CheckBox103).TabIndex = 44;
		((ButtonBase)CheckBox103).Text = "Double bottom, Eve && Eve";
		((ButtonBase)CheckBox103).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox104).AutoSize = true;
		((Control)CheckBox104).Location = new Point(241, 172);
		((Control)CheckBox104).Name = "CheckBox104";
		((Control)CheckBox104).Size = new Size(142, 17);
		((Control)CheckBox104).TabIndex = 48;
		((ButtonBase)CheckBox104).Text = "Double top, Eve && Adam";
		((ButtonBase)CheckBox104).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox105).AutoSize = true;
		((Control)CheckBox105).Location = new Point(241, 189);
		((Control)CheckBox105).Name = "CheckBox105";
		((Control)CheckBox105).Size = new Size(134, 17);
		((Control)CheckBox105).TabIndex = 49;
		((ButtonBase)CheckBox105).Text = "Double top, Eve && Eve";
		((ButtonBase)CheckBox105).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox108).AutoSize = true;
		((Control)CheckBox108).Location = new Point(241, 138);
		((Control)CheckBox108).Name = "CheckBox108";
		((Control)CheckBox108).Size = new Size(150, 17);
		((Control)CheckBox108).TabIndex = 46;
		((ButtonBase)CheckBox108).Text = "Double top, Adam && Adam";
		((ButtonBase)CheckBox108).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox109).AutoSize = true;
		((Control)CheckBox109).Location = new Point(241, 155);
		((Control)CheckBox109).Name = "CheckBox109";
		((Control)CheckBox109).Size = new Size(142, 17);
		((Control)CheckBox109).TabIndex = 47;
		((ButtonBase)CheckBox109).Text = "Double top, Adam && Eve";
		((ButtonBase)CheckBox109).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox112).AutoSize = true;
		((Control)CheckBox112).Location = new Point(241, 206);
		((Control)CheckBox112).Name = "CheckBox112";
		((Control)CheckBox112).Size = new Size(95, 17);
		((Control)CheckBox112).TabIndex = 50;
		((ButtonBase)CheckBox112).Text = "Fakey, bearish";
		((ButtonBase)CheckBox112).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox113).AutoSize = true;
		((Control)CheckBox113).Location = new Point(241, 223);
		((Control)CheckBox113).Name = "CheckBox113";
		((Control)CheckBox113).Size = new Size(90, 17);
		((Control)CheckBox113).TabIndex = 52;
		((ButtonBase)CheckBox113).Text = "Fakey, bullish";
		((ButtonBase)CheckBox113).UseVisualStyleBackColor = true;
		((Control)FakeyHelpButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)FakeyHelpButton).Location = new Point(342, 207);
		((Control)FakeyHelpButton).Name = "FakeyHelpButton";
		((Control)FakeyHelpButton).Size = new Size(20, 20);
		((Control)FakeyHelpButton).TabIndex = 51;
		((ButtonBase)FakeyHelpButton).Text = "?";
		((ButtonBase)FakeyHelpButton).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox110).AutoSize = true;
		((Control)CheckBox110).Location = new Point(12, 87);
		((Control)CheckBox110).Name = "CheckBox110";
		((Control)CheckBox110).Size = new Size(109, 17);
		((Control)CheckBox110).TabIndex = 6;
		((ButtonBase)CheckBox110).Text = "AB=CD®, bearish";
		((ButtonBase)CheckBox110).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox111).AutoSize = true;
		((Control)CheckBox111).Location = new Point(12, 104);
		((Control)CheckBox111).Name = "CheckBox111";
		((Control)CheckBox111).Size = new Size(104, 17);
		((Control)CheckBox111).TabIndex = 7;
		((ButtonBase)CheckBox111).Text = "AB=CD®. bullish";
		((ButtonBase)CheckBox111).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox114).AutoSize = true;
		((Control)CheckBox114).Location = new Point(12, 478);
		((Control)CheckBox114).Name = "CheckBox114";
		((Control)CheckBox114).Size = new Size(91, 17);
		((Control)CheckBox114).TabIndex = 30;
		((ButtonBase)CheckBox114).Text = "Crab®, bullish";
		((ButtonBase)CheckBox114).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox115).AutoSize = true;
		((Control)CheckBox115).Location = new Point(12, 461);
		((Control)CheckBox115).Name = "CheckBox115";
		((Control)CheckBox115).Size = new Size(96, 17);
		((Control)CheckBox115).TabIndex = 29;
		((ButtonBase)CheckBox115).Text = "Crab®, bearish";
		((ButtonBase)CheckBox115).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox116).AutoSize = true;
		((Control)CheckBox116).Location = new Point(12, 342);
		((Control)CheckBox116).Name = "CheckBox116";
		((Control)CheckBox116).Size = new Size(107, 17);
		((Control)CheckBox116).TabIndex = 22;
		((ButtonBase)CheckBox116).Text = "Butterfly®, bullish";
		((ButtonBase)CheckBox116).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox117).AutoSize = true;
		((Control)CheckBox117).Location = new Point(12, 325);
		((Control)CheckBox117).Name = "CheckBox117";
		((Control)CheckBox117).Size = new Size(112, 17);
		((Control)CheckBox117).TabIndex = 21;
		((ButtonBase)CheckBox117).Text = "Butterfly®, bearish";
		((ButtonBase)CheckBox117).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox118).AutoSize = true;
		((Control)CheckBox118).Location = new Point(12, 138);
		((Control)CheckBox118).Name = "CheckBox118";
		((Control)CheckBox118).Size = new Size(85, 17);
		((Control)CheckBox118).TabIndex = 9;
		((ButtonBase)CheckBox118).Text = "Bat®, bullish";
		((ButtonBase)CheckBox118).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox119).AutoSize = true;
		((Control)CheckBox119).Location = new Point(12, 121);
		((Control)CheckBox119).Name = "CheckBox119";
		((Control)CheckBox119).Size = new Size(90, 17);
		((Control)CheckBox119).TabIndex = 8;
		((ButtonBase)CheckBox119).Text = "Bat®, bearish";
		((ButtonBase)CheckBox119).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox120).AutoSize = true;
		((Control)CheckBox120).Location = new Point(12, 359);
		((Control)CheckBox120).Name = "CheckBox120";
		((Control)CheckBox120).Size = new Size(94, 17);
		((Control)CheckBox120).TabIndex = 23;
		((ButtonBase)CheckBox120).Text = "Carl V, bearish";
		((ButtonBase)CheckBox120).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox121).AutoSize = true;
		((Control)CheckBox121).Location = new Point(12, 376);
		((Control)CheckBox121).Name = "CheckBox121";
		((Control)CheckBox121).Size = new Size(89, 17);
		((Control)CheckBox121).TabIndex = 24;
		((ButtonBase)CheckBox121).Text = "Carl V, bullish";
		((ButtonBase)CheckBox121).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox122).AutoSize = true;
		((Control)CheckBox122).Location = new Point(12, 410);
		((Control)CheckBox122).Name = "CheckBox122";
		((Control)CheckBox122).Size = new Size(83, 17);
		((Control)CheckBox122).TabIndex = 26;
		((ButtonBase)CheckBox122).Text = "Channel, up";
		((ButtonBase)CheckBox122).UseVisualStyleBackColor = true;
		((Control)NumTLUp).Location = new Point(852, 115);
		NumTLUp.Maximum = new decimal(new int[4] { 1000, 0, 0, 0 });
		NumTLUp.Minimum = new decimal(new int[4] { 5, 0, 0, 0 });
		((Control)NumTLUp).Name = "NumTLUp";
		((Control)NumTLUp).Size = new Size(52, 20);
		((Control)NumTLUp).TabIndex = 109;
		NumTLUp.Value = new decimal(new int[4] { 252, 0, 0, 0 });
		((Control)NumTLDown).Location = new Point(852, 95);
		NumTLDown.Maximum = new decimal(new int[4] { 1000, 0, 0, 0 });
		NumTLDown.Minimum = new decimal(new int[4] { 5, 0, 0, 0 });
		((Control)NumTLDown).Name = "NumTLDown";
		((Control)NumTLDown).Size = new Size(52, 20);
		((Control)NumTLDown).TabIndex = 107;
		NumTLDown.Value = new decimal(new int[4] { 252, 0, 0, 0 });
		((Control)Label1).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)0, (GraphicsUnit)3, (byte)0);
		((Control)Label1).Location = new Point(786, 94);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(66, 41);
		((Control)Label1).TabIndex = 106;
		Label1.Text = "Max length (price bars):";
		Label1.TextAlign = (ContentAlignment)32;
		((Control)BullUpButton).Location = new Point(664, 462);
		((Control)BullUpButton).Name = "BullUpButton";
		((Control)BullUpButton).Size = new Size(69, 23);
		((Control)BullUpButton).TabIndex = 128;
		((ButtonBase)BullUpButton).Text = "10 &Bull Up";
		((ButtonBase)BullUpButton).UseVisualStyleBackColor = true;
		((Control)BearUpButton).Location = new Point(836, 463);
		((Control)BearUpButton).Name = "BearUpButton";
		((Control)BearUpButton).Size = new Size(69, 23);
		((Control)BearUpButton).TabIndex = 132;
		((ButtonBase)BearUpButton).Text = "10 &Bear Up";
		((ButtonBase)BearUpButton).UseVisualStyleBackColor = true;
		((Control)BearDownButton).Location = new Point(816, 492);
		((Control)BearDownButton).Name = "BearDownButton";
		((Control)BearDownButton).Size = new Size(89, 23);
		((Control)BearDownButton).TabIndex = 133;
		((ButtonBase)BearDownButton).Text = "10 &Bear Down";
		((ButtonBase)BearDownButton).UseVisualStyleBackColor = true;
		((Control)BullDownButton).Location = new Point(664, 490);
		((Control)BullDownButton).Name = "BullDownButton";
		((Control)BullDownButton).Size = new Size(89, 23);
		((Control)BullDownButton).TabIndex = 129;
		((ButtonBase)BullDownButton).Text = "10 &Bull Down";
		((ButtonBase)BullDownButton).UseVisualStyleBackColor = true;
		((Control)BARRHelpButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)BARRHelpButton).Location = new Point(188, 297);
		((Control)BARRHelpButton).Name = "BARRHelpButton";
		((Control)BARRHelpButton).Size = new Size(20, 20);
		((Control)BARRHelpButton).TabIndex = 19;
		((ButtonBase)BARRHelpButton).Text = "?";
		((ButtonBase)BARRHelpButton).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox123).AutoSize = true;
		((Control)CheckBox123).Location = new Point(12, 2);
		((Control)CheckBox123).Name = "CheckBox123";
		((Control)CheckBox123).Size = new Size(67, 17);
		((Control)CheckBox123).TabIndex = 1;
		((ButtonBase)CheckBox123).Text = "2-Dance";
		((ButtonBase)CheckBox123).UseVisualStyleBackColor = true;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(917, 638);
		((Control)this).Controls.Add((Control)(object)CheckBox123);
		((Control)this).Controls.Add((Control)(object)BARRHelpButton);
		((Control)this).Controls.Add((Control)(object)BullDownButton);
		((Control)this).Controls.Add((Control)(object)BearDownButton);
		((Control)this).Controls.Add((Control)(object)BearUpButton);
		((Control)this).Controls.Add((Control)(object)BullUpButton);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)NumTLUp);
		((Control)this).Controls.Add((Control)(object)NumTLDown);
		((Control)this).Controls.Add((Control)(object)CheckBox122);
		((Control)this).Controls.Add((Control)(object)CheckBox121);
		((Control)this).Controls.Add((Control)(object)CheckBox120);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)CheckBox110);
		((Control)this).Controls.Add((Control)(object)CheckBox111);
		((Control)this).Controls.Add((Control)(object)CheckBox114);
		((Control)this).Controls.Add((Control)(object)CheckBox115);
		((Control)this).Controls.Add((Control)(object)CheckBox116);
		((Control)this).Controls.Add((Control)(object)CheckBox117);
		((Control)this).Controls.Add((Control)(object)CheckBox118);
		((Control)this).Controls.Add((Control)(object)CheckBox119);
		((Control)this).Controls.Add((Control)(object)FakeyHelpButton);
		((Control)this).Controls.Add((Control)(object)CheckBox112);
		((Control)this).Controls.Add((Control)(object)CheckBox113);
		((Control)this).Controls.Add((Control)(object)CheckBox104);
		((Control)this).Controls.Add((Control)(object)CheckBox105);
		((Control)this).Controls.Add((Control)(object)CheckBox108);
		((Control)this).Controls.Add((Control)(object)CheckBox109);
		((Control)this).Controls.Add((Control)(object)CheckBox102);
		((Control)this).Controls.Add((Control)(object)CheckBox103);
		((Control)this).Controls.Add((Control)(object)CheckBox55);
		((Control)this).Controls.Add((Control)(object)CheckBox43);
		((Control)this).Controls.Add((Control)(object)WarningLabel);
		((Control)this).Controls.Add((Control)(object)ThreeBarButton);
		((Control)this).Controls.Add((Control)(object)InvertButton);
		((Control)this).Controls.Add((Control)(object)WolfeHelpButton);
		((Control)this).Controls.Add((Control)(object)SmallPatternsButton);
		((Control)this).Controls.Add((Control)(object)GroupBox1);
		((Control)this).Controls.Add((Control)(object)CheckBox94);
		((Control)this).Controls.Add((Control)(object)CheckBox93);
		((Control)this).Controls.Add((Control)(object)CheckBox76);
		((Control)this).Controls.Add((Control)(object)CheckBox69);
		((Control)this).Controls.Add((Control)(object)CheckBox58);
		((Control)this).Controls.Add((Control)(object)CheckBox57);
		((Control)this).Controls.Add((Control)(object)CheckBox107);
		((Control)this).Controls.Add((Control)(object)CheckBox106);
		((Control)this).Controls.Add((Control)(object)CheckBox101);
		((Control)this).Controls.Add((Control)(object)CheckBox100);
		((Control)this).Controls.Add((Control)(object)CheckBox99);
		((Control)this).Controls.Add((Control)(object)CheckBox98);
		((Control)this).Controls.Add((Control)(object)CheckBox97);
		((Control)this).Controls.Add((Control)(object)CheckBox96);
		((Control)this).Controls.Add((Control)(object)CheckBox95);
		((Control)this).Controls.Add((Control)(object)CheckBox92);
		((Control)this).Controls.Add((Control)(object)CheckBox91);
		((Control)this).Controls.Add((Control)(object)CheckBox90);
		((Control)this).Controls.Add((Control)(object)CheckBox89);
		((Control)this).Controls.Add((Control)(object)CheckBox88);
		((Control)this).Controls.Add((Control)(object)CheckBox87);
		((Control)this).Controls.Add((Control)(object)CheckBox86);
		((Control)this).Controls.Add((Control)(object)CheckBox85);
		((Control)this).Controls.Add((Control)(object)CheckBox84);
		((Control)this).Controls.Add((Control)(object)CheckBox83);
		((Control)this).Controls.Add((Control)(object)CheckBox82);
		((Control)this).Controls.Add((Control)(object)CheckBox81);
		((Control)this).Controls.Add((Control)(object)CheckBox80);
		((Control)this).Controls.Add((Control)(object)CheckBox79);
		((Control)this).Controls.Add((Control)(object)CheckBox78);
		((Control)this).Controls.Add((Control)(object)CheckBox77);
		((Control)this).Controls.Add((Control)(object)CheckBox73);
		((Control)this).Controls.Add((Control)(object)CheckBox72);
		((Control)this).Controls.Add((Control)(object)CheckBox71);
		((Control)this).Controls.Add((Control)(object)CheckBox70);
		((Control)this).Controls.Add((Control)(object)CheckBox68);
		((Control)this).Controls.Add((Control)(object)CheckBox67);
		((Control)this).Controls.Add((Control)(object)CheckBox66);
		((Control)this).Controls.Add((Control)(object)CheckBox65);
		((Control)this).Controls.Add((Control)(object)CheckBox64);
		((Control)this).Controls.Add((Control)(object)CheckBox63);
		((Control)this).Controls.Add((Control)(object)CheckBox62);
		((Control)this).Controls.Add((Control)(object)CheckBox61);
		((Control)this).Controls.Add((Control)(object)CheckBox60);
		((Control)this).Controls.Add((Control)(object)CheckBox59);
		((Control)this).Controls.Add((Control)(object)CheckBox56);
		((Control)this).Controls.Add((Control)(object)CheckBox54);
		((Control)this).Controls.Add((Control)(object)CheckBox53);
		((Control)this).Controls.Add((Control)(object)CheckBox52);
		((Control)this).Controls.Add((Control)(object)CheckBox51);
		((Control)this).Controls.Add((Control)(object)CheckBox50);
		((Control)this).Controls.Add((Control)(object)CheckBox49);
		((Control)this).Controls.Add((Control)(object)CheckBox48);
		((Control)this).Controls.Add((Control)(object)CheckBox47);
		((Control)this).Controls.Add((Control)(object)CheckBox46);
		((Control)this).Controls.Add((Control)(object)CheckBox45);
		((Control)this).Controls.Add((Control)(object)CheckBox39);
		((Control)this).Controls.Add((Control)(object)CheckBox38);
		((Control)this).Controls.Add((Control)(object)CheckBox37);
		((Control)this).Controls.Add((Control)(object)CheckBox36);
		((Control)this).Controls.Add((Control)(object)CheckBox35);
		((Control)this).Controls.Add((Control)(object)CheckBox34);
		((Control)this).Controls.Add((Control)(object)CheckBox33);
		((Control)this).Controls.Add((Control)(object)AllButton);
		((Control)this).Controls.Add((Control)(object)PctRiseMaskedTextBox);
		((Control)this).Controls.Add((Control)(object)ClearButton);
		((Control)this).Controls.Add((Control)(object)DefaultButton);
		((Control)this).Controls.Add((Control)(object)CheckBox32);
		((Control)this).Controls.Add((Control)(object)CheckBox31);
		((Control)this).Controls.Add((Control)(object)CheckBox30);
		((Control)this).Controls.Add((Control)(object)CheckBox29);
		((Control)this).Controls.Add((Control)(object)CheckBox28);
		((Control)this).Controls.Add((Control)(object)CheckBox27);
		((Control)this).Controls.Add((Control)(object)CheckBox26);
		((Control)this).Controls.Add((Control)(object)CheckBox25);
		((Control)this).Controls.Add((Control)(object)CheckBox16);
		((Control)this).Controls.Add((Control)(object)CheckBox15);
		((Control)this).Controls.Add((Control)(object)CheckBox14);
		((Control)this).Controls.Add((Control)(object)CheckBox13);
		((Control)this).Controls.Add((Control)(object)CheckBox12);
		((Control)this).Controls.Add((Control)(object)CheckBox11);
		((Control)this).Controls.Add((Control)(object)CheckBox10);
		((Control)this).Controls.Add((Control)(object)CheckBox9);
		((Control)this).Controls.Add((Control)(object)CheckBox24);
		((Control)this).Controls.Add((Control)(object)CheckBox23);
		((Control)this).Controls.Add((Control)(object)CheckBox22);
		((Control)this).Controls.Add((Control)(object)CheckBox21);
		((Control)this).Controls.Add((Control)(object)CheckBox20);
		((Control)this).Controls.Add((Control)(object)CheckBox19);
		((Control)this).Controls.Add((Control)(object)CheckBox18);
		((Control)this).Controls.Add((Control)(object)CheckBox17);
		((Control)this).Controls.Add((Control)(object)CheckBox8);
		((Control)this).Controls.Add((Control)(object)CheckBox7);
		((Control)this).Controls.Add((Control)(object)CheckBox6);
		((Control)this).Controls.Add((Control)(object)CheckBox5);
		((Control)this).Controls.Add((Control)(object)CheckBox4);
		((Control)this).Controls.Add((Control)(object)CheckBox3);
		((Control)this).Controls.Add((Control)(object)CheckBox2);
		((Control)this).Controls.Add((Control)(object)CheckBox1);
		((Control)this).Name = "PatternsForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Patterns Form";
		((Control)GroupBox1).ResumeLayout(false);
		((Control)GroupBox1).PerformLayout();
		((ISupportInitialize)NumTLUp).EndInit();
		((ISupportInitialize)NumTLDown).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void PatternsForm_FormClosing(object sender, FormClosingEventArgs e)
	{
		if (AbortClosing)
		{
			AbortClosing = false;
			((CancelEventArgs)(object)e).Cancel = true;
		}
		else
		{
			MySettingsProperty.Settings.PatternsLocation = ((Form)this).Location;
			MySettingsProperty.Settings.PatternsSize = ((Form)this).Size;
			((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
		}
	}

	private void PatternsForm_Closed(object sender, EventArgs e)
	{
		if (!Versioned.IsNumeric((object)PctRiseMaskedTextBox.Text))
		{
			GlobalForm.pfPctRise = GlobalForm.iDCBPERCENTRISE;
			PctRiseMaskedTextBox.Text = Strings.Format((object)GlobalForm.pfPctRise, "##");
		}
		if (Conversions.ToInteger(PctRiseMaskedTextBox.Text) != GlobalForm.pfPctRise)
		{
			GlobalForm.pfPRChanged = true;
			GlobalForm.pfPctRise = Conversions.ToInteger(PctRiseMaskedTextBox.Text);
		}
		if (!Versioned.IsNumeric((object)GapSizeMTB.Text))
		{
			GlobalForm.GapSize = 0.2m;
		}
		else
		{
			GlobalForm.GapSize = Conversions.ToDecimal(GapSizeMTB.Text);
		}
		GlobalForm.TLDNLength = Convert.ToInt32(NumTLDown.Value);
		GlobalForm.TLUpLength = Convert.ToInt32(NumTLUp.Value);
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		list.AddRange(((IEnumerable)((Control)GroupBox1).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				if (GlobalForm.PatternList[i] != Conversions.ToByte(Interaction.IIf(list[i].Checked, (object)1, (object)0)))
				{
					GlobalForm.PLChanged = true;
				}
				GlobalForm.PatternList[i] = Conversions.ToByte(Interaction.IIf(list[i].Checked, (object)1, (object)0));
			}
		}
	}

	private void PatternsForm_Load(object sender, EventArgs e)
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
		//IL_0157: Unknown result type (might be due to invalid IL or missing references)
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.PatternsLocation, MySettingsProperty.Settings.PatternsSize);
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)AllButton, "Check all boxes.");
		val.SetToolTip((Control)(object)BearDownButton, "Top performing patterns in bear markets with downward breakouts.");
		val.SetToolTip((Control)(object)BearUpButton, "Top performing patterns in bear markets with upward breakouts.");
		val.SetToolTip((Control)(object)BullDownButton, "Top performing patterns in bull markets with downward breakouts.");
		val.SetToolTip((Control)(object)BullUpButton, "Top performing patterns in bull markets with upward breakouts.");
		val.SetToolTip((Control)(object)ClearButton, "Uncheck all boxes.");
		val.SetToolTip((Control)(object)DefaultButton, "Restore the check boxes to the factory default.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)FakeyHelpButton, "Important information on fakey patterns.");
		val.SetToolTip((Control)(object)GapUnknownCB, "When all gap types are checked (except gap 2H and inverted 2H), then show gaps that can't be identified.");
		val.SetToolTip((Control)(object)GapHelpButton, "An explanation of gap unknown.");
		val.SetToolTip((Control)(object)InvertButton, "Uncheck those checked and check those unchecked.");
		val.SetToolTip((Control)(object)NumTLDown, "Enter length of trendline in price bars (252 is 1 year, daily chart. 1000 means unlimited length. Longer means slower finding.");
		val.SetToolTip((Control)(object)NumTLUp, "Enter length of trendline in price bars (252 is 1 year, daily chart. 1000 means unlimited length. Longer means slower finding.");
		val.SetToolTip((Control)(object)PctRiseMaskedTextBox, "Enter the minimum percentage rise to trigger an event.");
		val.SetToolTip((Control)(object)SmallPatternsButton, "Select to highlight small patterns (patterns a few bars long).");
		val.SetToolTip((Control)(object)ThreeBarButton, "'Strict' checkbox on Chart Form changes confirmation of the 3-bar pattern.");
		val.SetToolTip((Control)(object)WolfeHelpButton, "Important information about recognizing Wolfe waves.");
		((Control)WarningLabel).ForeColor = Color.Black;
		AbortClosing = false;
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		list.AddRange(((IEnumerable)((Control)GroupBox1).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				list[i].Checked = Conversions.ToBoolean(Interaction.IIf(GlobalForm.PatternList[i] == 1, (object)true, (object)false));
			}
			GlobalForm.pfPctRise = Conversions.ToInteger(Interaction.IIf(GlobalForm.pfPctRise == 0, (object)GlobalForm.iDCBPERCENTRISE, (object)GlobalForm.pfPctRise));
			GapSizeMTB.Text = Strings.Format((object)GlobalForm.GapSize, "000.0#######");
			PctRiseMaskedTextBox.Text = Strings.Format((object)GlobalForm.pfPctRise, "##");
			NumTLDown.Value = new decimal(GlobalForm.TLDNLength);
			NumTLUp.Value = new decimal(GlobalForm.TLUpLength);
		}
	}

	private void AllButton_Click(object sender, EventArgs e)
	{
		((Control)WarningLabel).ForeColor = Color.Red;
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		list.AddRange(((IEnumerable)((Control)GroupBox1).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				if (((Control)list[i]).Enabled)
				{
					list[i].Checked = true;
				}
			}
		}
	}

	private void BARRHelpButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("On the Chart Form click the Setup button. There you have the option of showing warning, buy, and sell lines. These are lines parallel to the main pattern trendline so you can better time your entry and exit.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void BullUpButton_Click(object sender, EventArgs e)
	{
		//IL_005b: Unknown result type (might be due to invalid IL or missing references)
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				if (((Control)list[i]).Enabled)
				{
					list[i].Checked = BullUp[i];
				}
			}
			MessageBox.Show("I've checked the top performing chart patterns with upward breakouts in a bull market (some remain grayed and unchecked).", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
	}

	private void BullDownButton_Click(object sender, EventArgs e)
	{
		//IL_005b: Unknown result type (might be due to invalid IL or missing references)
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				if (((Control)list[i]).Enabled)
				{
					list[i].Checked = BullDown[i];
				}
			}
			MessageBox.Show("I've checked the top performing chart patterns with downward breakouts in a bull market (most remain grayed and unchecked).", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
	}

	private void BearUpButton_Click(object sender, EventArgs e)
	{
		//IL_005b: Unknown result type (might be due to invalid IL or missing references)
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				if (((Control)list[i]).Enabled)
				{
					list[i].Checked = BearUp[i];
				}
			}
			MessageBox.Show("I've checked the top performing chart patterns with upward breakouts in a bear market (some remain grayed and unchecked).", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
	}

	private void BearDownButton_Click(object sender, EventArgs e)
	{
		//IL_005b: Unknown result type (might be due to invalid IL or missing references)
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				if (((Control)list[i]).Enabled)
				{
					list[i].Checked = BearDown[i];
				}
			}
			MessageBox.Show("I've checked the top performing chart patterns with downward breakouts in a bear market (some remain grayed and unchecked).", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
	}

	private void CheckBox57_CheckedChanged(object sender, EventArgs e)
	{
		if (CheckBox57.Checked | CheckBox58.Checked)
		{
			((Control)WolfeHelpButton).ForeColor = Color.Red;
		}
		else if (!CheckBox57.Checked & !CheckBox58.Checked)
		{
			((Control)WolfeHelpButton).ForeColor = Color.Black;
		}
	}

	private void ClearButton_Click(object sender, EventArgs e)
	{
		((Control)WarningLabel).ForeColor = Color.Black;
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		list.AddRange(((IEnumerable)((Control)GroupBox1).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				list[i].Checked = false;
			}
		}
	}

	private void DefaultButton_Click(object sender, EventArgs e)
	{
		((Control)WarningLabel).ForeColor = Color.Black;
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		list.AddRange(((IEnumerable)((Control)GroupBox1).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				if (((Control)list[i]).Enabled)
				{
					list[i].Checked = DefaultList[i];
				}
			}
			PctRiseMaskedTextBox.Text = GlobalForm.iDCBPERCENTRISE.ToString();
			GlobalForm.GapSize = 0.2m;
			GapSizeMTB.Text = Strings.Format((object)GlobalForm.GapSize, "000.0#######");
		}
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		//IL_0067: Unknown result type (might be due to invalid IL or missing references)
		//IL_006d: Invalid comparison between Unknown and I4
		bool flag = false;
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		list.AddRange(((IEnumerable)((Control)GroupBox1).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				if (list[i].Checked)
				{
					flag = true;
					break;
				}
			}
		}
		if (!flag)
		{
			if ((int)MessageBox.Show("No pattern has been checked, meaning you'll be wondering why no patterns will appear on the chart or list forms. Did you want to correct this?", "PatternsForm: DoneButton_Click", (MessageBoxButtons)4, (MessageBoxIcon)32, (MessageBoxDefaultButton)0) == 7)
			{
				((Form)this).Close();
			}
			else
			{
				AbortClosing = true;
			}
		}
		else
		{
			((Form)this).Close();
		}
	}

	private void FakeyHelpButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("The bullish and bearish fakey patterns displayed in Patternz are an improved variety. See: http://thepatternsite.com/FakeyBear.html and http://thepatternsite.com/FakeyBull.html for more information.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)32);
	}

	private void GapHelpButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("Not all gaps can be identified (such as an ex-dividend gap). When all gap types are checked (except gap 2H and inverted 2H), then show gaps which can't be identified. They will appear as G? on the chart.\r\n\r\nI will automatically check the other gap types when unknown gap type is checked.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)32);
	}

	private void GapSizeMTB_Validating(object sender, CancelEventArgs e)
	{
		//IL_0024: Unknown result type (might be due to invalid IL or missing references)
		if (!Versioned.IsNumeric((object)GapSizeMTB.Text))
		{
			Interaction.Beep();
			MessageBox.Show("Only numbers and a decimal are allowed in the text box. Default is 00.20.", "PatternsForm: GapSizeMTB_Validating", (MessageBoxButtons)0, (MessageBoxIcon)64);
			((Control)GapSizeMTB).Focus();
		}
	}

	private void GapUnknownCB_CheckedChanged(object sender, EventArgs e)
	{
		if (!LockFlag && GapUnknownCB.Checked)
		{
			CheckBox40.Checked = true;
			CheckBox41.Checked = true;
			CheckBox42.Checked = true;
			CheckBox44.Checked = true;
		}
	}

	private void InvertButton_Click(object sender, EventArgs e)
	{
		List<CheckBox> list = new List<CheckBox>();
		LockFlag = true;
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		list.AddRange(((IEnumerable)((Control)GroupBox1).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				if (((Control)list[i]).Enabled)
				{
					list[i].Checked = !list[i].Checked;
				}
			}
			LockFlag = false;
		}
	}

	private void SmallPatternsButton_Click(object sender, EventArgs e)
	{
		((Control)WarningLabel).ForeColor = Color.Red;
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		list.AddRange(((IEnumerable)((Control)GroupBox1).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				if (((Control)list[i]).Enabled)
				{
					list[i].Checked = SmallPats[i];
				}
			}
		}
	}

	private void ThreeBarButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("When Strict is unchecked (see Chart Form), Patternz looks for a 3-bar with a close above the high of the middle bar. When strict is checked, Patternz looks for a close above the high of the prior two bars (a more strict confirmation signal).", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void WolfeHelpButton_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("The configuration of Wolfe waves are proprietary and I have NO knowledge of those details. What you'll see are patterns based on PUBLICALLY AVAILABLE information from Bill Wolfe's website, not his proprietary patterns, so any patterns that appear might not be actual Wolfe waves.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}
}
