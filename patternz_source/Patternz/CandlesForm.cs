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
public class CandlesForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("AllButton")]
	private Button _AllButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ClearButton")]
	private Button _ClearButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DefaultButton")]
	private Button _DefaultButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PerformingButton")]
	private Button _PerformingButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ReversalsButton")]
	private Button _ReversalsButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ContinuationsButton")]
	private Button _ContinuationsButton;

	[CompilerGenerated]
	[AccessedThroughProperty("InvertButton")]
	private Button _InvertButton;

	private bool AbortClosing;

	private readonly bool[] PerformingUp;

	private readonly bool[] PerformingDown;

	private readonly bool[] ReversalsUp;

	private readonly bool[] ReversalsDown;

	private readonly bool[] ContinuationsUp;

	private readonly bool[] ContinuationsDown;

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

	[field: AccessedThroughProperty("CheckBox2")]
	internal virtual CheckBox CheckBox2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox1")]
	internal virtual CheckBox CheckBox1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
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

	[field: AccessedThroughProperty("CheckBox43")]
	internal virtual CheckBox CheckBox43
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
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

	[field: AccessedThroughProperty("CheckBox55")]
	internal virtual CheckBox CheckBox55
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

	[field: AccessedThroughProperty("CheckBox57")]
	internal virtual CheckBox CheckBox57
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CheckBox58")]
	internal virtual CheckBox CheckBox58
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

	[field: AccessedThroughProperty("CheckBox69")]
	internal virtual CheckBox CheckBox69
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

	[field: AccessedThroughProperty("CheckBox76")]
	internal virtual CheckBox CheckBox76
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

	internal virtual Button PerformingButton
	{
		[CompilerGenerated]
		get
		{
			return _PerformingButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BestPerformingButton_Click;
			Button val = _PerformingButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_PerformingButton = value;
			val = _PerformingButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button ReversalsButton
	{
		[CompilerGenerated]
		get
		{
			return _ReversalsButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ReversalsButton_Click;
			Button val = _ReversalsButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ReversalsButton = value;
			val = _ReversalsButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button ContinuationsButton
	{
		[CompilerGenerated]
		get
		{
			return _ContinuationsButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ContinuationsButton_Click;
			Button val = _ContinuationsButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ContinuationsButton = value;
			val = _ContinuationsButton;
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

	[field: AccessedThroughProperty("UpBkoutRB")]
	internal virtual RadioButton UpBkoutRB
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("DownBkoutRB")]
	internal virtual RadioButton DownBkoutRB
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

	[field: AccessedThroughProperty("Label1")]
	internal virtual Label Label1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public CandlesForm()
	{
		//IL_0020: Unknown result type (might be due to invalid IL or missing references)
		//IL_002a: Expected O, but got Unknown
		((Form)this).Closed += CandlesForm_Closed;
		((Form)this).FormClosing += new FormClosingEventHandler(CandlesForm_FormClosing);
		((Form)this).Load += CandlesForm_Load;
		AbortClosing = false;
		PerformingUp = new bool[105]
		{
			false, false, false, false, true, false, false, false, false, false,
			false, false, false, false, false, true, false, false, false, false,
			false, true, true, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			true, false, true, true, true, true, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, true, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false
		};
		PerformingDown = new bool[105]
		{
			false, true, false, true, false, false, false, false, false, true,
			false, false, false, false, false, false, false, false, false, false,
			true, false, false, false, true, false, false, false, true, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, true, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, true, false, false, false, false, false, false, false, false,
			true, false, false, true, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false
		};
		ReversalsUp = new bool[105]
		{
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, true, true, true, false,
			false, true, false, false, false, true, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, true, true, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, true, false,
			false, false, true, true, false
		};
		ReversalsDown = new bool[105]
		{
			false, true, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, true,
			true, false, false, false, true, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, true, false, false, false, false, false, false, false,
			false, false, false, true, true, false, true, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, true,
			false, false, false, false, true
		};
		ContinuationsUp = new bool[105]
		{
			false, false, false, false, false, true, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, true, false, true, false, true, false, true, false,
			false, false, false, false, false, false, false, true, false, false,
			false, false, false, false, false, false, true, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, true, false, false, false, false, false, false,
			true, false, false, false, false, false, false, false, false, false,
			false, true, false, false, false
		};
		ContinuationsDown = new bool[105]
		{
			false, false, false, false, false, false, false, true, false, true,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false, false, false, false, true, false,
			false, false, false, false, false, false, false, true, false, false,
			false, false, false, false, false, false, true, false, false, false,
			false, false, false, false, false, false, false, true, false, false,
			false, false, false, false, false, false, false, false, false, false,
			true, false, true, false, false, false, false, false, false, false,
			false, false, false, false, false, true, false, false, false, true,
			false, false, false, false, false, false, false, false, false, false,
			false, false, false, false, false
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
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(CandlesForm));
		AllButton = new Button();
		ClearButton = new Button();
		DefaultButton = new Button();
		DoneButton = new Button();
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
		CheckBox24 = new CheckBox();
		CheckBox23 = new CheckBox();
		CheckBox22 = new CheckBox();
		CheckBox21 = new CheckBox();
		CheckBox20 = new CheckBox();
		CheckBox19 = new CheckBox();
		CheckBox18 = new CheckBox();
		CheckBox17 = new CheckBox();
		CheckBox8 = new CheckBox();
		CheckBox7 = new CheckBox();
		CheckBox6 = new CheckBox();
		CheckBox5 = new CheckBox();
		CheckBox4 = new CheckBox();
		CheckBox3 = new CheckBox();
		CheckBox2 = new CheckBox();
		CheckBox1 = new CheckBox();
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
		CheckBox43 = new CheckBox();
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
		CheckBox55 = new CheckBox();
		CheckBox56 = new CheckBox();
		CheckBox57 = new CheckBox();
		CheckBox58 = new CheckBox();
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
		CheckBox69 = new CheckBox();
		CheckBox70 = new CheckBox();
		CheckBox71 = new CheckBox();
		CheckBox72 = new CheckBox();
		CheckBox73 = new CheckBox();
		CheckBox74 = new CheckBox();
		CheckBox75 = new CheckBox();
		CheckBox76 = new CheckBox();
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
		CheckBox93 = new CheckBox();
		CheckBox94 = new CheckBox();
		CheckBox95 = new CheckBox();
		CheckBox96 = new CheckBox();
		CheckBox97 = new CheckBox();
		CheckBox98 = new CheckBox();
		CheckBox99 = new CheckBox();
		CheckBox100 = new CheckBox();
		CheckBox101 = new CheckBox();
		CheckBox102 = new CheckBox();
		CheckBox103 = new CheckBox();
		CheckBox104 = new CheckBox();
		CheckBox105 = new CheckBox();
		PerformingButton = new Button();
		ReversalsButton = new Button();
		ContinuationsButton = new Button();
		InvertButton = new Button();
		UpBkoutRB = new RadioButton();
		DownBkoutRB = new RadioButton();
		GroupBox1 = new GroupBox();
		Label1 = new Label();
		((Control)GroupBox1).SuspendLayout();
		((Control)this).SuspendLayout();
		((Control)AllButton).Location = new Point(683, 507);
		((Control)AllButton).Name = "AllButton";
		((Control)AllButton).Size = new Size(75, 23);
		((Control)AllButton).TabIndex = 107;
		((ButtonBase)AllButton).Text = "Select &All";
		((ButtonBase)AllButton).UseVisualStyleBackColor = true;
		((Control)ClearButton).ForeColor = Color.Black;
		((Control)ClearButton).Location = new Point(200, 19);
		((Control)ClearButton).Name = "ClearButton";
		((Control)ClearButton).Size = new Size(82, 23);
		((Control)ClearButton).TabIndex = 4;
		((ButtonBase)ClearButton).Text = "&Clear";
		((ButtonBase)ClearButton).UseVisualStyleBackColor = true;
		((Control)DefaultButton).Location = new Point(764, 507);
		((Control)DefaultButton).Name = "DefaultButton";
		((Control)DefaultButton).Size = new Size(75, 23);
		((Control)DefaultButton).TabIndex = 109;
		((ButtonBase)DefaultButton).Text = "D&efault";
		((ButtonBase)DefaultButton).UseVisualStyleBackColor = true;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(764, 534);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(75, 23);
		((Control)DoneButton).TabIndex = 110;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox32).AutoSize = true;
		((Control)CheckBox32).Location = new Point(172, 280);
		((Control)CheckBox32).Name = "CheckBox32";
		((Control)CheckBox32).Size = new Size(85, 17);
		((Control)CheckBox32).TabIndex = 33;
		((ButtonBase)CheckBox32).Text = "Evening star";
		((ButtonBase)CheckBox32).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox31).AutoSize = true;
		((Control)CheckBox31).Location = new Point(172, 257);
		((Control)CheckBox31).Name = "CheckBox31";
		((Control)CheckBox31).Size = new Size(104, 17);
		((Control)CheckBox31).TabIndex = 32;
		((ButtonBase)CheckBox31).Text = "Evening doji star";
		((ButtonBase)CheckBox31).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox30).AutoSize = true;
		((Control)CheckBox30).Location = new Point(172, 234);
		((Control)CheckBox30).Name = "CheckBox30";
		((Control)CheckBox30).Size = new Size(105, 17);
		((Control)CheckBox30).TabIndex = 31;
		((ButtonBase)CheckBox30).Text = "Engulfing, bullish";
		((ButtonBase)CheckBox30).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox29).AutoSize = true;
		((Control)CheckBox29).Location = new Point(172, 211);
		((Control)CheckBox29).Name = "CheckBox29";
		((Control)CheckBox29).Size = new Size(110, 17);
		((Control)CheckBox29).TabIndex = 30;
		((ButtonBase)CheckBox29).Text = "Engulfing, bearish";
		((ButtonBase)CheckBox29).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox28).AutoSize = true;
		((Control)CheckBox28).Location = new Point(172, 188);
		((Control)CheckBox28).Name = "CheckBox28";
		((Control)CheckBox28).Size = new Size(105, 17);
		((Control)CheckBox28).TabIndex = 29;
		((ButtonBase)CheckBox28).Text = "8 new price lines";
		((ButtonBase)CheckBox28).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox27).AutoSize = true;
		((Control)CheckBox27).Location = new Point(172, 165);
		((Control)CheckBox27).Name = "CheckBox27";
		((Control)CheckBox27).Size = new Size(129, 17);
		((Control)CheckBox27).TabIndex = 28;
		((ButtonBase)CheckBox27).Text = "Downside Tasuki gap";
		((ButtonBase)CheckBox27).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox26).AutoSize = true;
		((Control)CheckBox26).Location = new Point(172, 142);
		((Control)CheckBox26).Name = "CheckBox26";
		((Control)CheckBox26).Size = new Size(164, 17);
		((Control)CheckBox26).TabIndex = 27;
		((ButtonBase)CheckBox26).Text = "Downside gap three methods";
		((ButtonBase)CheckBox26).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox25).AutoSize = true;
		((Control)CheckBox25).Location = new Point(172, 119);
		((Control)CheckBox25).Name = "CheckBox25";
		((Control)CheckBox25).Size = new Size(117, 17);
		((Control)CheckBox25).TabIndex = 26;
		((ButtonBase)CheckBox25).Text = "Doji star, collapsing";
		((ButtonBase)CheckBox25).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox16).AutoSize = true;
		((Control)CheckBox16).Location = new Point(9, 391);
		((Control)CheckBox16).Name = "CheckBox16";
		((Control)CheckBox16).Size = new Size(94, 17);
		((Control)CheckBox16).TabIndex = 17;
		((ButtonBase)CheckBox16).Text = "Doji, four price";
		((ButtonBase)CheckBox16).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox15).AutoSize = true;
		((Control)CheckBox15).Location = new Point(9, 368);
		((Control)CheckBox15).Name = "CheckBox15";
		((Control)CheckBox15).Size = new Size(96, 17);
		((Control)CheckBox15).TabIndex = 16;
		((ButtonBase)CheckBox15).Text = "Doji, dragonFly";
		((ButtonBase)CheckBox15).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox14).AutoSize = true;
		((Control)CheckBox14).Location = new Point(9, 345);
		((Control)CheckBox14).Name = "CheckBox14";
		((Control)CheckBox14).Size = new Size(82, 17);
		((Control)CheckBox14).TabIndex = 15;
		((ButtonBase)CheckBox14).Text = "Deliberation";
		((ButtonBase)CheckBox14).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox13).AutoSize = true;
		((Control)CheckBox13).Location = new Point(9, 322);
		((Control)CheckBox13).Name = "CheckBox13";
		((Control)CheckBox13).Size = new Size(108, 17);
		((Control)CheckBox13).TabIndex = 14;
		((ButtonBase)CheckBox13).Text = "Dark cloud cover";
		((ButtonBase)CheckBox13).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox12).AutoSize = true;
		((Control)CheckBox12).Location = new Point(9, 299);
		((Control)CheckBox12).Name = "CheckBox12";
		((Control)CheckBox12).Size = new Size(145, 17);
		((Control)CheckBox12).TabIndex = 13;
		((ButtonBase)CheckBox12).Text = "Concealing baby swallow";
		((ButtonBase)CheckBox12).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox11).AutoSize = true;
		((Control)CheckBox11).Location = new Point(9, 276);
		((Control)CheckBox11).Name = "CheckBox11";
		((Control)CheckBox11).Size = new Size(116, 17);
		((Control)CheckBox11).TabIndex = 12;
		((ButtonBase)CheckBox11).Text = "Candle, short white";
		((ButtonBase)CheckBox11).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox10).AutoSize = true;
		((Control)CheckBox10).Location = new Point(9, 253);
		((Control)CheckBox10).Name = "CheckBox10";
		((Control)CheckBox10).Size = new Size(117, 17);
		((Control)CheckBox10).TabIndex = 11;
		((ButtonBase)CheckBox10).Text = "Candle, short black";
		((ButtonBase)CheckBox10).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox9).AutoSize = true;
		((Control)CheckBox9).Location = new Point(9, 230);
		((Control)CheckBox9).Name = "CheckBox9";
		((Control)CheckBox9).Size = new Size(90, 17);
		((Control)CheckBox9).TabIndex = 10;
		((ButtonBase)CheckBox9).Text = "Candle, white";
		((ButtonBase)CheckBox9).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox24).AutoSize = true;
		((Control)CheckBox24).Location = new Point(172, 96);
		((Control)CheckBox24).Name = "CheckBox24";
		((Control)CheckBox24).Size = new Size(99, 17);
		((Control)CheckBox24).TabIndex = 25;
		((ButtonBase)CheckBox24).Text = "Doji star, bullish";
		((ButtonBase)CheckBox24).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox23).AutoSize = true;
		((Control)CheckBox23).Location = new Point(172, 73);
		((Control)CheckBox23).Name = "CheckBox23";
		((Control)CheckBox23).Size = new Size(104, 17);
		((Control)CheckBox23).TabIndex = 24;
		((ButtonBase)CheckBox23).Text = "Doji star, bearish";
		((ButtonBase)CheckBox23).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox22).AutoSize = true;
		((Control)CheckBox22).Location = new Point(172, 50);
		((Control)CheckBox22).Name = "CheckBox22";
		((Control)CheckBox22).Size = new Size(91, 17);
		((Control)CheckBox22).TabIndex = 23;
		((ButtonBase)CheckBox22).Text = "Doji, southern";
		((ButtonBase)CheckBox22).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox21).AutoSize = true;
		((Control)CheckBox21).Location = new Point(172, 31);
		((Control)CheckBox21).Name = "CheckBox21";
		((Control)CheckBox21).Size = new Size(89, 17);
		((Control)CheckBox21).TabIndex = 22;
		((ButtonBase)CheckBox21).Text = "Doji, northern";
		((ButtonBase)CheckBox21).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox20).AutoSize = true;
		((Control)CheckBox20).Location = new Point(172, 8);
		((Control)CheckBox20).Name = "CheckBox20";
		((Control)CheckBox20).Size = new Size(105, 17);
		((Control)CheckBox20).TabIndex = 21;
		((ButtonBase)CheckBox20).Text = "Doji, long legged";
		((ButtonBase)CheckBox20).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox19).AutoSize = true;
		((Control)CheckBox19).Location = new Point(9, 459);
		((Control)CheckBox19).Name = "CheckBox19";
		((Control)CheckBox19).Size = new Size(103, 17);
		((Control)CheckBox19).TabIndex = 20;
		((ButtonBase)CheckBox19).Text = "Doji, gravestone";
		((ButtonBase)CheckBox19).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox18).AutoSize = true;
		((Control)CheckBox18).Location = new Point(9, 436);
		((Control)CheckBox18).Name = "CheckBox18";
		((Control)CheckBox18).Size = new Size(103, 17);
		((Control)CheckBox18).TabIndex = 19;
		((ButtonBase)CheckBox18).Text = "Doji, gapping up";
		((ButtonBase)CheckBox18).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox17).AutoSize = true;
		((Control)CheckBox17).Location = new Point(9, 413);
		((Control)CheckBox17).Name = "CheckBox17";
		((Control)CheckBox17).Size = new Size(117, 17);
		((Control)CheckBox17).TabIndex = 18;
		((ButtonBase)CheckBox17).Text = "Doji, gapping down";
		((ButtonBase)CheckBox17).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox8).AutoSize = true;
		((Control)CheckBox8).Location = new Point(9, 207);
		((Control)CheckBox8).Name = "CheckBox8";
		((Control)CheckBox8).Size = new Size(91, 17);
		((Control)CheckBox8).TabIndex = 9;
		((ButtonBase)CheckBox8).Text = "Candle, black";
		((ButtonBase)CheckBox8).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox7).AutoSize = true;
		CheckBox7.Checked = true;
		CheckBox7.CheckState = (CheckState)1;
		((Control)CheckBox7).Location = new Point(9, 146);
		((Control)CheckBox7).Name = "CheckBox7";
		((Control)CheckBox7).Size = new Size(102, 17);
		((Control)CheckBox7).TabIndex = 6;
		((ButtonBase)CheckBox7).Text = "Belt hold, bullish";
		((ButtonBase)CheckBox7).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox6).AutoSize = true;
		((Control)CheckBox6).Location = new Point(9, 123);
		((Control)CheckBox6).Name = "CheckBox6";
		((Control)CheckBox6).Size = new Size(107, 17);
		((Control)CheckBox6).TabIndex = 5;
		((ButtonBase)CheckBox6).Text = "Belt hold, bearish";
		((ButtonBase)CheckBox6).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox5).AutoSize = true;
		((Control)CheckBox5).Location = new Point(9, 100);
		((Control)CheckBox5).Name = "CheckBox5";
		((Control)CheckBox5).Size = new Size(116, 17);
		((Control)CheckBox5).TabIndex = 4;
		((ButtonBase)CheckBox5).Text = "Below the stomach";
		((ButtonBase)CheckBox5).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox4).AutoSize = true;
		((Control)CheckBox4).Location = new Point(9, 77);
		((Control)CheckBox4).Name = "CheckBox4";
		((Control)CheckBox4).Size = new Size(98, 17);
		((Control)CheckBox4).TabIndex = 3;
		((ButtonBase)CheckBox4).Text = "Advance block";
		((ButtonBase)CheckBox4).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox3).AutoSize = true;
		CheckBox3.Checked = true;
		CheckBox3.CheckState = (CheckState)1;
		((Control)CheckBox3).Location = new Point(9, 54);
		((Control)CheckBox3).Name = "CheckBox3";
		((Control)CheckBox3).Size = new Size(118, 17);
		((Control)CheckBox3).TabIndex = 2;
		((ButtonBase)CheckBox3).Text = "Above the stomach";
		((ButtonBase)CheckBox3).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox2).AutoSize = true;
		((Control)CheckBox2).Location = new Point(9, 31);
		((Control)CheckBox2).Name = "CheckBox2";
		((Control)CheckBox2).Size = new Size(142, 17);
		((Control)CheckBox2).TabIndex = 1;
		((ButtonBase)CheckBox2).Text = "Abandoned baby, bullish";
		((ButtonBase)CheckBox2).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox1).AutoSize = true;
		((Control)CheckBox1).Location = new Point(9, 8);
		((Control)CheckBox1).Name = "CheckBox1";
		((Control)CheckBox1).Size = new Size(147, 17);
		((Control)CheckBox1).TabIndex = 0;
		((ButtonBase)CheckBox1).Text = "Abandoned baby, bearish";
		((ButtonBase)CheckBox1).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox33).AutoSize = true;
		((Control)CheckBox33).Location = new Point(342, 161);
		((Control)CheckBox33).Name = "CheckBox33";
		((Control)CheckBox33).Size = new Size(127, 17);
		((Control)CheckBox33).TabIndex = 49;
		((ButtonBase)CheckBox33).Text = "Last engulfing bottom";
		((ButtonBase)CheckBox33).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox34).AutoSize = true;
		((Control)CheckBox34).Location = new Point(342, 138);
		((Control)CheckBox34).Name = "CheckBox34";
		((Control)CheckBox34).Size = new Size(94, 17);
		((Control)CheckBox34).TabIndex = 48;
		((ButtonBase)CheckBox34).Text = "Ladder bottom";
		((ButtonBase)CheckBox34).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox35).AutoSize = true;
		((Control)CheckBox35).Location = new Point(342, 115);
		((Control)CheckBox35).Name = "CheckBox35";
		((Control)CheckBox35).Size = new Size(96, 17);
		((Control)CheckBox35).TabIndex = 47;
		((ButtonBase)CheckBox35).Text = "Kicking, bullish";
		((ButtonBase)CheckBox35).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox36).AutoSize = true;
		((Control)CheckBox36).Location = new Point(342, 92);
		((Control)CheckBox36).Name = "CheckBox36";
		((Control)CheckBox36).Size = new Size(101, 17);
		((Control)CheckBox36).TabIndex = 46;
		((ButtonBase)CheckBox36).Text = "Kicking, bearish";
		((ButtonBase)CheckBox36).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox37).AutoSize = true;
		((Control)CheckBox37).Location = new Point(342, 69);
		((Control)CheckBox37).Name = "CheckBox37";
		((Control)CheckBox37).Size = new Size(62, 17);
		((Control)CheckBox37).TabIndex = 45;
		((ButtonBase)CheckBox37).Text = "In neck";
		((ButtonBase)CheckBox37).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox38).AutoSize = true;
		((Control)CheckBox38).Location = new Point(342, 50);
		((Control)CheckBox38).Name = "CheckBox38";
		((Control)CheckBox38).Size = new Size(124, 17);
		((Control)CheckBox38).TabIndex = 44;
		((ButtonBase)CheckBox38).Text = "Identical three crows";
		((ButtonBase)CheckBox38).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox39).AutoSize = true;
		((Control)CheckBox39).Location = new Point(342, 31);
		((Control)CheckBox39).Name = "CheckBox39";
		((Control)CheckBox39).Size = new Size(97, 17);
		((Control)CheckBox39).TabIndex = 43;
		((ButtonBase)CheckBox39).Text = "Homing pigeon";
		((ButtonBase)CheckBox39).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox40).AutoSize = true;
		((Control)CheckBox40).Location = new Point(342, 8);
		((Control)CheckBox40).Name = "CheckBox40";
		((Control)CheckBox40).Size = new Size(77, 17);
		((Control)CheckBox40).TabIndex = 42;
		((ButtonBase)CheckBox40).Text = "High wave";
		((ButtonBase)CheckBox40).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox41).AutoSize = true;
		((Control)CheckBox41).Location = new Point(172, 463);
		((Control)CheckBox41).Name = "CheckBox41";
		((Control)CheckBox41).Size = new Size(122, 17);
		((Control)CheckBox41).TabIndex = 41;
		((ButtonBase)CheckBox41).Text = "Harami cross, bullish";
		((ButtonBase)CheckBox41).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox42).AutoSize = true;
		((Control)CheckBox42).Location = new Point(172, 440);
		((Control)CheckBox42).Name = "CheckBox42";
		((Control)CheckBox42).Size = new Size(127, 17);
		((Control)CheckBox42).TabIndex = 40;
		((ButtonBase)CheckBox42).Text = "Harami cross, bearish";
		((ButtonBase)CheckBox42).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox43).AutoSize = true;
		((Control)CheckBox43).Location = new Point(172, 417);
		((Control)CheckBox43).Name = "CheckBox43";
		((Control)CheckBox43).Size = new Size(94, 17);
		((Control)CheckBox43).TabIndex = 39;
		((ButtonBase)CheckBox43).Text = "Harami, bullish";
		((ButtonBase)CheckBox43).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox44).AutoSize = true;
		((Control)CheckBox44).Location = new Point(172, 394);
		((Control)CheckBox44).Name = "CheckBox44";
		((Control)CheckBox44).Size = new Size(99, 17);
		((Control)CheckBox44).TabIndex = 38;
		((ButtonBase)CheckBox44).Text = "Harami, bearish";
		((ButtonBase)CheckBox44).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox45).AutoSize = true;
		((Control)CheckBox45).Location = new Point(172, 371);
		((Control)CheckBox45).Name = "CheckBox45";
		((Control)CheckBox45).Size = new Size(89, 17);
		((Control)CheckBox45).TabIndex = 37;
		((ButtonBase)CheckBox45).Text = "Hanging man";
		((ButtonBase)CheckBox45).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox46).AutoSize = true;
		((Control)CheckBox46).Location = new Point(172, 348);
		((Control)CheckBox46).Name = "CheckBox46";
		((Control)CheckBox46).Size = new Size(109, 17);
		((Control)CheckBox46).TabIndex = 36;
		((ButtonBase)CheckBox46).Text = "Hammer, inverted";
		((ButtonBase)CheckBox46).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox47).AutoSize = true;
		((Control)CheckBox47).Location = new Point(172, 325);
		((Control)CheckBox47).Name = "CheckBox47";
		((Control)CheckBox47).Size = new Size(65, 17);
		((Control)CheckBox47).TabIndex = 35;
		((ButtonBase)CheckBox47).Text = "Hammer";
		((ButtonBase)CheckBox47).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox48).AutoSize = true;
		((Control)CheckBox48).Location = new Point(172, 302);
		((Control)CheckBox48).Name = "CheckBox48";
		((Control)CheckBox48).Size = new Size(126, 17);
		((Control)CheckBox48).TabIndex = 34;
		((ButtonBase)CheckBox48).Text = "Falling three methods";
		((ButtonBase)CheckBox48).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox49).AutoSize = true;
		((Control)CheckBox49).Location = new Point(499, 54);
		((Control)CheckBox49).Name = "CheckBox49";
		((Control)CheckBox49).Size = new Size(67, 17);
		((Control)CheckBox49).TabIndex = 65;
		((ButtonBase)CheckBox49).Text = "On neck";
		((ButtonBase)CheckBox49).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox50).AutoSize = true;
		CheckBox50.Checked = true;
		CheckBox50.CheckState = (CheckState)1;
		((Control)CheckBox50).Location = new Point(499, 31);
		((Control)CheckBox50).Name = "CheckBox50";
		((Control)CheckBox50).Size = new Size(84, 17);
		((Control)CheckBox50).TabIndex = 64;
		((ButtonBase)CheckBox50).Text = "Morning star";
		((ButtonBase)CheckBox50).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox51).AutoSize = true;
		CheckBox51.Checked = true;
		CheckBox51.CheckState = (CheckState)1;
		((Control)CheckBox51).Location = new Point(499, 8);
		((Control)CheckBox51).Name = "CheckBox51";
		((Control)CheckBox51).Size = new Size(103, 17);
		((Control)CheckBox51).TabIndex = 63;
		((ButtonBase)CheckBox51).Text = "Morning doji star";
		((ButtonBase)CheckBox51).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox52).AutoSize = true;
		((Control)CheckBox52).Location = new Point(342, 460);
		((Control)CheckBox52).Name = "CheckBox52";
		((Control)CheckBox52).Size = new Size(123, 17);
		((Control)CheckBox52).TabIndex = 62;
		((ButtonBase)CheckBox52).Text = "Meeting lines, bullish";
		((ButtonBase)CheckBox52).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox53).AutoSize = true;
		((Control)CheckBox53).Location = new Point(342, 437);
		((Control)CheckBox53).Name = "CheckBox53";
		((Control)CheckBox53).Size = new Size(128, 17);
		((Control)CheckBox53).TabIndex = 61;
		((ButtonBase)CheckBox53).Text = "Meeting lines, bearish";
		((ButtonBase)CheckBox53).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox54).AutoSize = true;
		((Control)CheckBox54).Location = new Point(342, 414);
		((Control)CheckBox54).Name = "CheckBox54";
		((Control)CheckBox54).Size = new Size(89, 17);
		((Control)CheckBox54).TabIndex = 60;
		((ButtonBase)CheckBox54).Text = "Matching low";
		((ButtonBase)CheckBox54).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox55).AutoSize = true;
		((Control)CheckBox55).Location = new Point(342, 391);
		((Control)CheckBox55).Name = "CheckBox55";
		((Control)CheckBox55).Size = new Size(67, 17);
		((Control)CheckBox55).TabIndex = 59;
		((ButtonBase)CheckBox55).Text = "Mat hold";
		((ButtonBase)CheckBox55).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox56).AutoSize = true;
		((Control)CheckBox56).Location = new Point(342, 368);
		((Control)CheckBox56).Name = "CheckBox56";
		((Control)CheckBox56).Size = new Size(104, 17);
		((Control)CheckBox56).TabIndex = 58;
		((ButtonBase)CheckBox56).Text = "Marubozu, white";
		((ButtonBase)CheckBox56).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox57).AutoSize = true;
		((Control)CheckBox57).Location = new Point(342, 345);
		((Control)CheckBox57).Name = "CheckBox57";
		((Control)CheckBox57).Size = new Size(145, 17);
		((Control)CheckBox57).TabIndex = 57;
		((ButtonBase)CheckBox57).Text = "Marubozu, opening white";
		((ButtonBase)CheckBox57).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox58).AutoSize = true;
		((Control)CheckBox58).Location = new Point(342, 322);
		((Control)CheckBox58).Name = "CheckBox58";
		((Control)CheckBox58).Size = new Size(146, 17);
		((Control)CheckBox58).TabIndex = 56;
		((ButtonBase)CheckBox58).Text = "Marubozu, opening black";
		((ButtonBase)CheckBox58).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox59).AutoSize = true;
		((Control)CheckBox59).Location = new Point(342, 299);
		((Control)CheckBox59).Name = "CheckBox59";
		((Control)CheckBox59).Size = new Size(140, 17);
		((Control)CheckBox59).TabIndex = 55;
		((ButtonBase)CheckBox59).Text = "Marubozu, closing white";
		((ButtonBase)CheckBox59).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox60).AutoSize = true;
		((Control)CheckBox60).Location = new Point(342, 276);
		((Control)CheckBox60).Name = "CheckBox60";
		((Control)CheckBox60).Size = new Size(141, 17);
		((Control)CheckBox60).TabIndex = 54;
		((ButtonBase)CheckBox60).Text = "Marubozu, closing black";
		((ButtonBase)CheckBox60).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox61).AutoSize = true;
		((Control)CheckBox61).Location = new Point(342, 253);
		((Control)CheckBox61).Name = "CheckBox61";
		((Control)CheckBox61).Size = new Size(105, 17);
		((Control)CheckBox61).TabIndex = 53;
		((ButtonBase)CheckBox61).Text = "Marubozu, black";
		((ButtonBase)CheckBox61).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox62).AutoSize = true;
		((Control)CheckBox62).Location = new Point(342, 230);
		((Control)CheckBox62).Name = "CheckBox62";
		((Control)CheckBox62).Size = new Size(101, 17);
		((Control)CheckBox62).TabIndex = 52;
		((ButtonBase)CheckBox62).Text = "Long day, white";
		((ButtonBase)CheckBox62).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox63).AutoSize = true;
		((Control)CheckBox63).Location = new Point(342, 207);
		((Control)CheckBox63).Name = "CheckBox63";
		((Control)CheckBox63).Size = new Size(102, 17);
		((Control)CheckBox63).TabIndex = 51;
		((ButtonBase)CheckBox63).Text = "Long day, black";
		((ButtonBase)CheckBox63).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox64).AutoSize = true;
		((Control)CheckBox64).Location = new Point(342, 184);
		((Control)CheckBox64).Name = "CheckBox64";
		((Control)CheckBox64).Size = new Size(110, 17);
		((Control)CheckBox64).TabIndex = 50;
		((ButtonBase)CheckBox64).Text = "Last engulfing top";
		((ButtonBase)CheckBox64).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox65).AutoSize = true;
		CheckBox65.Checked = true;
		CheckBox65.CheckState = (CheckState)1;
		((Control)CheckBox65).Location = new Point(499, 414);
		((Control)CheckBox65).Name = "CheckBox65";
		((Control)CheckBox65).Size = new Size(75, 17);
		((Control)CheckBox65).TabIndex = 81;
		((ButtonBase)CheckBox65).Text = "Takuri line";
		((ButtonBase)CheckBox65).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox66).AutoSize = true;
		((Control)CheckBox66).Location = new Point(499, 391);
		((Control)CheckBox66).Name = "CheckBox66";
		((Control)CheckBox66).Size = new Size(111, 17);
		((Control)CheckBox66).TabIndex = 80;
		((ButtonBase)CheckBox66).Text = "13 new price lines";
		((ButtonBase)CheckBox66).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox67).AutoSize = true;
		((Control)CheckBox67).Location = new Point(499, 368);
		((Control)CheckBox67).Name = "CheckBox67";
		((Control)CheckBox67).Size = new Size(111, 17);
		((Control)CheckBox67).TabIndex = 79;
		((ButtonBase)CheckBox67).Text = "10 new price lines";
		((ButtonBase)CheckBox67).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox68).AutoSize = true;
		((Control)CheckBox68).Location = new Point(499, 345);
		((Control)CheckBox68).Name = "CheckBox68";
		((Control)CheckBox68).Size = new Size(98, 17);
		((Control)CheckBox68).TabIndex = 78;
		((ButtonBase)CheckBox68).Text = "Stick sandwich";
		((ButtonBase)CheckBox68).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox69).AutoSize = true;
		((Control)CheckBox69).Location = new Point(499, 322);
		((Control)CheckBox69).Name = "CheckBox69";
		((Control)CheckBox69).Size = new Size(116, 17);
		((Control)CheckBox69).TabIndex = 77;
		((ButtonBase)CheckBox69).Text = "Spinning top, white";
		((ButtonBase)CheckBox69).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox70).AutoSize = true;
		((Control)CheckBox70).Location = new Point(499, 299);
		((Control)CheckBox70).Name = "CheckBox70";
		((Control)CheckBox70).Size = new Size(117, 17);
		((Control)CheckBox70).TabIndex = 76;
		((ButtonBase)CheckBox70).Text = "Spinning top, black";
		((ButtonBase)CheckBox70).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox71).AutoSize = true;
		((Control)CheckBox71).Location = new Point(499, 276);
		((Control)CheckBox71).Name = "CheckBox71";
		((Control)CheckBox71).Size = new Size(85, 17);
		((Control)CheckBox71).TabIndex = 75;
		((ButtonBase)CheckBox71).Text = "Spinning top";
		((ButtonBase)CheckBox71).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox72).AutoSize = true;
		((Control)CheckBox72).Location = new Point(499, 253);
		((Control)CheckBox72).Name = "CheckBox72";
		((Control)CheckBox72).Size = new Size(170, 17);
		((Control)CheckBox72).TabIndex = 74;
		((ButtonBase)CheckBox72).Text = "Side-by-side white lines, bullish";
		((ButtonBase)CheckBox72).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox73).AutoSize = true;
		((Control)CheckBox73).Location = new Point(499, 230);
		((Control)CheckBox73).Name = "CheckBox73";
		((Control)CheckBox73).Size = new Size(175, 17);
		((Control)CheckBox73).TabIndex = 73;
		((ButtonBase)CheckBox73).Text = "Side-by-side white lines, bearish";
		((ButtonBase)CheckBox73).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox74).AutoSize = true;
		((Control)CheckBox74).Location = new Point(499, 207);
		((Control)CheckBox74).Name = "CheckBox74";
		((Control)CheckBox74).Size = new Size(140, 17);
		((Control)CheckBox74).TabIndex = 72;
		((ButtonBase)CheckBox74).Text = "Shooting star, 2 candles";
		((ButtonBase)CheckBox74).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox75).AutoSize = true;
		((Control)CheckBox75).Location = new Point(499, 184);
		((Control)CheckBox75).Name = "CheckBox75";
		((Control)CheckBox75).Size = new Size(88, 17);
		((Control)CheckBox75).TabIndex = 71;
		((ButtonBase)CheckBox75).Text = "Shooting star";
		((ButtonBase)CheckBox75).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox76).AutoSize = true;
		((Control)CheckBox76).Location = new Point(499, 161);
		((Control)CheckBox76).Name = "CheckBox76";
		((Control)CheckBox76).Size = new Size(136, 17);
		((Control)CheckBox76).TabIndex = 70;
		((ButtonBase)CheckBox76).Text = "Separating lines, bullish";
		((ButtonBase)CheckBox76).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox77).AutoSize = true;
		((Control)CheckBox77).Location = new Point(499, 138);
		((Control)CheckBox77).Name = "CheckBox77";
		((Control)CheckBox77).Size = new Size(141, 17);
		((Control)CheckBox77).TabIndex = 69;
		((ButtonBase)CheckBox77).Text = "Separating lines, bearish";
		((ButtonBase)CheckBox77).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox78).AutoSize = true;
		((Control)CheckBox78).Location = new Point(499, 115);
		((Control)CheckBox78).Name = "CheckBox78";
		((Control)CheckBox78).Size = new Size(125, 17);
		((Control)CheckBox78).TabIndex = 68;
		((ButtonBase)CheckBox78).Text = "Rising three methods";
		((ButtonBase)CheckBox78).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox79).AutoSize = true;
		((Control)CheckBox79).Location = new Point(499, 92);
		((Control)CheckBox79).Name = "CheckBox79";
		((Control)CheckBox79).Size = new Size(96, 17);
		((Control)CheckBox79).TabIndex = 67;
		((ButtonBase)CheckBox79).Text = "Rickshaw man";
		((ButtonBase)CheckBox79).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox80).AutoSize = true;
		((Control)CheckBox80).Location = new Point(499, 73);
		((Control)CheckBox80).Name = "CheckBox80";
		((Control)CheckBox80).Size = new Size(100, 17);
		((Control)CheckBox80).TabIndex = 66;
		((ButtonBase)CheckBox80).Text = "Piercing pattern";
		((ButtonBase)CheckBox80).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox81).AutoSize = true;
		((Control)CheckBox81).Location = new Point(683, 303);
		((Control)CheckBox81).Name = "CheckBox81";
		((Control)CheckBox81).Size = new Size(157, 17);
		((Control)CheckBox81).TabIndex = 97;
		((ButtonBase)CheckBox81).Text = "Two black gapping candles";
		((ButtonBase)CheckBox81).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox82).AutoSize = true;
		((Control)CheckBox82).Location = new Point(683, 280);
		((Control)CheckBox82).Name = "CheckBox82";
		((Control)CheckBox82).Size = new Size(111, 17);
		((Control)CheckBox82).TabIndex = 96;
		((ButtonBase)CheckBox82).Text = "12 new price lines";
		((ButtonBase)CheckBox82).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox83).AutoSize = true;
		((Control)CheckBox83).Location = new Point(683, 257);
		((Control)CheckBox83).Name = "CheckBox83";
		((Control)CheckBox83).Size = new Size(93, 17);
		((Control)CheckBox83).TabIndex = 95;
		((ButtonBase)CheckBox83).Text = "Tweezers, top";
		((ButtonBase)CheckBox83).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox84).AutoSize = true;
		((Control)CheckBox84).Location = new Point(683, 234);
		((Control)CheckBox84).Name = "CheckBox84";
		((Control)CheckBox84).Size = new Size(110, 17);
		((Control)CheckBox84).TabIndex = 94;
		((ButtonBase)CheckBox84).Text = "Tweezers, bottom";
		((ButtonBase)CheckBox84).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox85).AutoSize = true;
		((Control)CheckBox85).Location = new Point(683, 211);
		((Control)CheckBox85).Name = "CheckBox85";
		((Control)CheckBox85).Size = new Size(93, 17);
		((Control)CheckBox85).TabIndex = 93;
		((ButtonBase)CheckBox85).Text = "Tri-star, bullish";
		((ButtonBase)CheckBox85).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox86).AutoSize = true;
		((Control)CheckBox86).Location = new Point(683, 188);
		((Control)CheckBox86).Name = "CheckBox86";
		((Control)CheckBox86).Size = new Size(98, 17);
		((Control)CheckBox86).TabIndex = 92;
		((ButtonBase)CheckBox86).Text = "Tri-star, bearish";
		((ButtonBase)CheckBox86).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox87).AutoSize = true;
		((Control)CheckBox87).Location = new Point(683, 165);
		((Control)CheckBox87).Name = "CheckBox87";
		((Control)CheckBox87).Size = new Size(70, 17);
		((Control)CheckBox87).TabIndex = 91;
		((ButtonBase)CheckBox87).Text = "Thrusting";
		((ButtonBase)CheckBox87).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox88).AutoSize = true;
		CheckBox88.Checked = true;
		CheckBox88.CheckState = (CheckState)1;
		((Control)CheckBox88).Location = new Point(683, 142);
		((Control)CheckBox88).Name = "CheckBox88";
		((Control)CheckBox88).Size = new Size(120, 17);
		((Control)CheckBox88).TabIndex = 90;
		((ButtonBase)CheckBox88).Text = "Three white soldiers";
		((ButtonBase)CheckBox88).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox89).AutoSize = true;
		((Control)CheckBox89).Location = new Point(683, 119);
		((Control)CheckBox89).Name = "CheckBox89";
		((Control)CheckBox89).Size = new Size(139, 17);
		((Control)CheckBox89).TabIndex = 89;
		((ButtonBase)CheckBox89).Text = "Three stars in the South";
		((ButtonBase)CheckBox89).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox90).AutoSize = true;
		CheckBox90.Checked = true;
		CheckBox90.CheckState = (CheckState)1;
		((Control)CheckBox90).Location = new Point(683, 96);
		((Control)CheckBox90).Name = "CheckBox90";
		((Control)CheckBox90).Size = new Size(106, 17);
		((Control)CheckBox90).TabIndex = 88;
		((ButtonBase)CheckBox90).Text = "Three outside up";
		((ButtonBase)CheckBox90).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox91).AutoSize = true;
		((Control)CheckBox91).Location = new Point(683, 73);
		((Control)CheckBox91).Name = "CheckBox91";
		((Control)CheckBox91).Size = new Size(120, 17);
		((Control)CheckBox91).TabIndex = 87;
		((ButtonBase)CheckBox91).Text = "Three outside down";
		((ButtonBase)CheckBox91).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox92).AutoSize = true;
		((Control)CheckBox92).Location = new Point(683, 50);
		((Control)CheckBox92).Name = "CheckBox92";
		((Control)CheckBox92).Size = new Size(136, 17);
		((Control)CheckBox92).TabIndex = 86;
		((ButtonBase)CheckBox92).Text = "Three-line strike, bullish";
		((ButtonBase)CheckBox92).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox93).AutoSize = true;
		((Control)CheckBox93).Location = new Point(683, 27);
		((Control)CheckBox93).Name = "CheckBox93";
		((Control)CheckBox93).Size = new Size(141, 17);
		((Control)CheckBox93).TabIndex = 85;
		((ButtonBase)CheckBox93).Text = "Three-line strike, bearish";
		((ButtonBase)CheckBox93).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox94).AutoSize = true;
		((Control)CheckBox94).Location = new Point(683, 4);
		((Control)CheckBox94).Name = "CheckBox94";
		((Control)CheckBox94).Size = new Size(99, 17);
		((Control)CheckBox94).TabIndex = 84;
		((ButtonBase)CheckBox94).Text = "Three inside up";
		((ButtonBase)CheckBox94).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox95).AutoSize = true;
		((Control)CheckBox95).Location = new Point(499, 462);
		((Control)CheckBox95).Name = "CheckBox95";
		((Control)CheckBox95).Size = new Size(113, 17);
		((Control)CheckBox95).TabIndex = 83;
		((ButtonBase)CheckBox95).Text = "Three inside down";
		((ButtonBase)CheckBox95).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox96).AutoSize = true;
		((Control)CheckBox96).Location = new Point(499, 439);
		((Control)CheckBox96).Name = "CheckBox96";
		((Control)CheckBox96).Size = new Size(114, 17);
		((Control)CheckBox96).TabIndex = 82;
		((ButtonBase)CheckBox96).Text = "Three black crows";
		((ButtonBase)CheckBox96).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox97).AutoSize = true;
		((Control)CheckBox97).Location = new Point(683, 464);
		((Control)CheckBox97).Name = "CheckBox97";
		((Control)CheckBox97).Size = new Size(95, 17);
		((Control)CheckBox97).TabIndex = 104;
		((ButtonBase)CheckBox97).Text = "Window, rising";
		((ButtonBase)CheckBox97).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox98).AutoSize = true;
		((Control)CheckBox98).Location = new Point(683, 441);
		((Control)CheckBox98).Name = "CheckBox98";
		((Control)CheckBox98).Size = new Size(98, 17);
		((Control)CheckBox98).TabIndex = 103;
		((ButtonBase)CheckBox98).Text = "Window, falling";
		((ButtonBase)CheckBox98).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox99).AutoSize = true;
		((Control)CheckBox99).Location = new Point(683, 418);
		((Control)CheckBox99).Name = "CheckBox99";
		((Control)CheckBox99).Size = new Size(115, 17);
		((Control)CheckBox99).TabIndex = 102;
		((ButtonBase)CheckBox99).Text = "Upside Tasuki gap";
		((ButtonBase)CheckBox99).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox100).AutoSize = true;
		((Control)CheckBox100).Location = new Point(683, 395);
		((Control)CheckBox100).Name = "CheckBox100";
		((Control)CheckBox100).Size = new Size(131, 17);
		((Control)CheckBox100).TabIndex = 101;
		((ButtonBase)CheckBox100).Text = "Upside gap two crows";
		((ButtonBase)CheckBox100).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox101).AutoSize = true;
		((Control)CheckBox101).Location = new Point(683, 372);
		((Control)CheckBox101).Name = "CheckBox101";
		((Control)CheckBox101).Size = new Size(150, 17);
		((Control)CheckBox101).TabIndex = 100;
		((ButtonBase)CheckBox101).Text = "Upside gap three methods";
		((ButtonBase)CheckBox101).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox102).AutoSize = true;
		((Control)CheckBox102).Location = new Point(683, 349);
		((Control)CheckBox102).Name = "CheckBox102";
		((Control)CheckBox102).Size = new Size(145, 17);
		((Control)CheckBox102).TabIndex = 99;
		((ButtonBase)CheckBox102).Text = "Unique three river bottom";
		((ButtonBase)CheckBox102).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox103).AutoSize = true;
		((Control)CheckBox103).Location = new Point(683, 326);
		((Control)CheckBox103).Name = "CheckBox103";
		((Control)CheckBox103).Size = new Size(78, 17);
		((Control)CheckBox103).TabIndex = 98;
		((ButtonBase)CheckBox103).Text = "Two crows";
		((ButtonBase)CheckBox103).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox104).AutoSize = true;
		((Control)CheckBox104).Location = new Point(9, 188);
		((Control)CheckBox104).Name = "CheckBox104";
		((Control)CheckBox104).Size = new Size(114, 17);
		((Control)CheckBox104).TabIndex = 8;
		((ButtonBase)CheckBox104).Text = "Breakaway, bullish";
		((ButtonBase)CheckBox104).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox105).AutoSize = true;
		((Control)CheckBox105).Location = new Point(9, 165);
		((Control)CheckBox105).Name = "CheckBox105";
		((Control)CheckBox105).Size = new Size(119, 17);
		((Control)CheckBox105).TabIndex = 7;
		((ButtonBase)CheckBox105).Text = "Breakaway, bearish";
		((ButtonBase)CheckBox105).UseVisualStyleBackColor = true;
		((Control)PerformingButton).ForeColor = Color.Black;
		((Control)PerformingButton).Location = new Point(199, 48);
		((Control)PerformingButton).Name = "PerformingButton";
		((Control)PerformingButton).Size = new Size(97, 23);
		((Control)PerformingButton).TabIndex = 5;
		((ButtonBase)PerformingButton).Text = "Best &Performing";
		((ButtonBase)PerformingButton).UseVisualStyleBackColor = true;
		((Control)ReversalsButton).ForeColor = Color.Black;
		((Control)ReversalsButton).Location = new Point(111, 19);
		((Control)ReversalsButton).Name = "ReversalsButton";
		((Control)ReversalsButton).Size = new Size(83, 23);
		((Control)ReversalsButton).TabIndex = 2;
		((ButtonBase)ReversalsButton).Text = "&Reversals";
		((ButtonBase)ReversalsButton).UseVisualStyleBackColor = true;
		((Control)ContinuationsButton).ForeColor = Color.Black;
		((Control)ContinuationsButton).Location = new Point(111, 48);
		((Control)ContinuationsButton).Name = "ContinuationsButton";
		((Control)ContinuationsButton).Size = new Size(83, 23);
		((Control)ContinuationsButton).TabIndex = 3;
		((ButtonBase)ContinuationsButton).Text = "C&ontinuations";
		((ButtonBase)ContinuationsButton).UseVisualStyleBackColor = true;
		((Control)InvertButton).Location = new Point(683, 534);
		((Control)InvertButton).Name = "InvertButton";
		((Control)InvertButton).Size = new Size(75, 23);
		((Control)InvertButton).TabIndex = 108;
		((ButtonBase)InvertButton).Text = "In&vert";
		((ButtonBase)InvertButton).UseVisualStyleBackColor = true;
		((ButtonBase)UpBkoutRB).AutoSize = true;
		UpBkoutRB.Checked = true;
		((Control)UpBkoutRB).ForeColor = Color.Black;
		((Control)UpBkoutRB).Location = new Point(6, 25);
		((Control)UpBkoutRB).Name = "UpBkoutRB";
		((Control)UpBkoutRB).Size = new Size(85, 17);
		((Control)UpBkoutRB).TabIndex = 0;
		UpBkoutRB.TabStop = true;
		((ButtonBase)UpBkoutRB).Text = "&Up Breakout";
		((ButtonBase)UpBkoutRB).UseVisualStyleBackColor = true;
		((ButtonBase)DownBkoutRB).AutoSize = true;
		((Control)DownBkoutRB).ForeColor = Color.Black;
		((Control)DownBkoutRB).Location = new Point(6, 54);
		((Control)DownBkoutRB).Name = "DownBkoutRB";
		((Control)DownBkoutRB).Size = new Size(99, 17);
		((Control)DownBkoutRB).TabIndex = 1;
		((ButtonBase)DownBkoutRB).Text = "Down &Breakout";
		((ButtonBase)DownBkoutRB).UseVisualStyleBackColor = true;
		((Control)GroupBox1).Controls.Add((Control)(object)PerformingButton);
		((Control)GroupBox1).Controls.Add((Control)(object)DownBkoutRB);
		((Control)GroupBox1).Controls.Add((Control)(object)UpBkoutRB);
		((Control)GroupBox1).Controls.Add((Control)(object)ReversalsButton);
		((Control)GroupBox1).Controls.Add((Control)(object)ContinuationsButton);
		((Control)GroupBox1).Controls.Add((Control)(object)ClearButton);
		((Control)GroupBox1).ForeColor = Color.Blue;
		((Control)GroupBox1).Location = new Point(366, 485);
		((Control)GroupBox1).Name = "GroupBox1";
		((Control)GroupBox1).Size = new Size(303, 80);
		((Control)GroupBox1).TabIndex = 106;
		GroupBox1.TabStop = false;
		GroupBox1.Text = "Top 10";
		((Control)Label1).Location = new Point(12, 498);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(335, 67);
		((Control)Label1).TabIndex = 105;
		Label1.Text = componentResourceManager.GetString("Label1.Text");
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(853, 571);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)GroupBox1);
		((Control)this).Controls.Add((Control)(object)InvertButton);
		((Control)this).Controls.Add((Control)(object)CheckBox104);
		((Control)this).Controls.Add((Control)(object)CheckBox105);
		((Control)this).Controls.Add((Control)(object)CheckBox97);
		((Control)this).Controls.Add((Control)(object)CheckBox98);
		((Control)this).Controls.Add((Control)(object)CheckBox99);
		((Control)this).Controls.Add((Control)(object)CheckBox100);
		((Control)this).Controls.Add((Control)(object)CheckBox101);
		((Control)this).Controls.Add((Control)(object)CheckBox102);
		((Control)this).Controls.Add((Control)(object)CheckBox103);
		((Control)this).Controls.Add((Control)(object)CheckBox81);
		((Control)this).Controls.Add((Control)(object)CheckBox82);
		((Control)this).Controls.Add((Control)(object)CheckBox83);
		((Control)this).Controls.Add((Control)(object)CheckBox84);
		((Control)this).Controls.Add((Control)(object)CheckBox85);
		((Control)this).Controls.Add((Control)(object)CheckBox86);
		((Control)this).Controls.Add((Control)(object)CheckBox87);
		((Control)this).Controls.Add((Control)(object)CheckBox88);
		((Control)this).Controls.Add((Control)(object)CheckBox89);
		((Control)this).Controls.Add((Control)(object)CheckBox90);
		((Control)this).Controls.Add((Control)(object)CheckBox91);
		((Control)this).Controls.Add((Control)(object)CheckBox92);
		((Control)this).Controls.Add((Control)(object)CheckBox93);
		((Control)this).Controls.Add((Control)(object)CheckBox94);
		((Control)this).Controls.Add((Control)(object)CheckBox95);
		((Control)this).Controls.Add((Control)(object)CheckBox96);
		((Control)this).Controls.Add((Control)(object)CheckBox65);
		((Control)this).Controls.Add((Control)(object)CheckBox66);
		((Control)this).Controls.Add((Control)(object)CheckBox67);
		((Control)this).Controls.Add((Control)(object)CheckBox68);
		((Control)this).Controls.Add((Control)(object)CheckBox69);
		((Control)this).Controls.Add((Control)(object)CheckBox70);
		((Control)this).Controls.Add((Control)(object)CheckBox71);
		((Control)this).Controls.Add((Control)(object)CheckBox72);
		((Control)this).Controls.Add((Control)(object)CheckBox73);
		((Control)this).Controls.Add((Control)(object)CheckBox74);
		((Control)this).Controls.Add((Control)(object)CheckBox75);
		((Control)this).Controls.Add((Control)(object)CheckBox76);
		((Control)this).Controls.Add((Control)(object)CheckBox77);
		((Control)this).Controls.Add((Control)(object)CheckBox78);
		((Control)this).Controls.Add((Control)(object)CheckBox79);
		((Control)this).Controls.Add((Control)(object)CheckBox80);
		((Control)this).Controls.Add((Control)(object)CheckBox49);
		((Control)this).Controls.Add((Control)(object)CheckBox50);
		((Control)this).Controls.Add((Control)(object)CheckBox51);
		((Control)this).Controls.Add((Control)(object)CheckBox52);
		((Control)this).Controls.Add((Control)(object)CheckBox53);
		((Control)this).Controls.Add((Control)(object)CheckBox54);
		((Control)this).Controls.Add((Control)(object)CheckBox55);
		((Control)this).Controls.Add((Control)(object)CheckBox56);
		((Control)this).Controls.Add((Control)(object)CheckBox57);
		((Control)this).Controls.Add((Control)(object)CheckBox58);
		((Control)this).Controls.Add((Control)(object)CheckBox59);
		((Control)this).Controls.Add((Control)(object)CheckBox60);
		((Control)this).Controls.Add((Control)(object)CheckBox61);
		((Control)this).Controls.Add((Control)(object)CheckBox62);
		((Control)this).Controls.Add((Control)(object)CheckBox63);
		((Control)this).Controls.Add((Control)(object)CheckBox64);
		((Control)this).Controls.Add((Control)(object)CheckBox33);
		((Control)this).Controls.Add((Control)(object)CheckBox34);
		((Control)this).Controls.Add((Control)(object)CheckBox35);
		((Control)this).Controls.Add((Control)(object)CheckBox36);
		((Control)this).Controls.Add((Control)(object)CheckBox37);
		((Control)this).Controls.Add((Control)(object)CheckBox38);
		((Control)this).Controls.Add((Control)(object)CheckBox39);
		((Control)this).Controls.Add((Control)(object)CheckBox40);
		((Control)this).Controls.Add((Control)(object)CheckBox41);
		((Control)this).Controls.Add((Control)(object)CheckBox42);
		((Control)this).Controls.Add((Control)(object)CheckBox43);
		((Control)this).Controls.Add((Control)(object)CheckBox44);
		((Control)this).Controls.Add((Control)(object)CheckBox45);
		((Control)this).Controls.Add((Control)(object)CheckBox46);
		((Control)this).Controls.Add((Control)(object)CheckBox47);
		((Control)this).Controls.Add((Control)(object)CheckBox48);
		((Control)this).Controls.Add((Control)(object)AllButton);
		((Control)this).Controls.Add((Control)(object)DefaultButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
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
		((Control)this).Name = "CandlesForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Candles Form";
		((Control)GroupBox1).ResumeLayout(false);
		((Control)GroupBox1).PerformLayout();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void CandlesForm_Closed(object sender, EventArgs e)
	{
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				if (FindCandles.CandleList[i] != Conversions.ToByte(Interaction.IIf(list[i].Checked, (object)1, (object)0)))
				{
					FindCandles.CLChanged = true;
				}
				FindCandles.CandleList[i] = Conversions.ToByte(Interaction.IIf(list[i].Checked, (object)1, (object)0));
			}
		}
	}

	private void CandlesForm_FormClosing(object sender, FormClosingEventArgs e)
	{
		if (AbortClosing)
		{
			AbortClosing = false;
			((CancelEventArgs)(object)e).Cancel = true;
		}
		else
		{
			MySettingsProperty.Settings.CandlesFormLocation = ((Form)this).Location;
			MySettingsProperty.Settings.CandlesFormSize = ((Form)this).Size;
			((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
		}
	}

	private void CandlesForm_Load(object sender, EventArgs e)
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
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.CandlesFormLocation, MySettingsProperty.Settings.CandlesFormSize);
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)AllButton, "Check all boxes.");
		val.SetToolTip((Control)(object)ClearButton, "Uncheck all boxes.");
		val.SetToolTip((Control)(object)ContinuationsButton, "Show the top 10 candles where price continues the trend most often.");
		val.SetToolTip((Control)(object)DefaultButton, "Restore check boxes to factory default (best performing candles).");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)DownBkoutRB, "Select breakout direction before choosing top 10 candles.");
		val.SetToolTip((Control)(object)InvertButton, "Check unchecked boxes and vice versa.");
		val.SetToolTip((Control)(object)PerformingButton, "Show the top 10 best performing candles.");
		val.SetToolTip((Control)(object)ReversalsButton, "Show top 10 candles which lead to price reversals most often.");
		val.SetToolTip((Control)(object)UpBkoutRB, "Select breakout direction before choosing top 10 candles.");
		AbortClosing = false;
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				list[i].Checked = Conversions.ToBoolean(Interaction.IIf(FindCandles.CandleList[i] == 1, (object)true, (object)false));
			}
		}
	}

	private void AllButton_Click(object sender, EventArgs e)
	{
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
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

	private void BestPerformingButton_Click(object sender, EventArgs e)
	{
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		checked
		{
			int num = PerformingUp.Count() - 1;
			for (int i = 0; i <= num; i++)
			{
				if (UpBkoutRB.Checked)
				{
					if (PerformingUp[i])
					{
						list[i].Checked = true;
					}
				}
				else if (PerformingDown[i])
				{
					list[i].Checked = true;
				}
			}
		}
	}

	private void ClearButton_Click(object sender, EventArgs e)
	{
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				list[i].Checked = false;
			}
		}
	}

	private void ContinuationsButton_Click(object sender, EventArgs e)
	{
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		checked
		{
			int num = PerformingUp.Count() - 1;
			for (int i = 0; i <= num; i++)
			{
				if (UpBkoutRB.Checked)
				{
					if (ContinuationsUp[i])
					{
						list[i].Checked = true;
					}
				}
				else if (ContinuationsDown[i])
				{
					list[i].Checked = true;
				}
			}
		}
	}

	private void DefaultButton_Click(object sender, EventArgs e)
	{
		ClearButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		BestPerformingButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		//IL_0051: Unknown result type (might be due to invalid IL or missing references)
		//IL_0057: Invalid comparison between Unknown and I4
		bool flag = false;
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
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
			if ((int)MessageBox.Show("No candles have been checked, meaning you'll be wondering why none appear on the chart or list forms. Did you want to correct this?", "CandlesForm: DoneButton_Click", (MessageBoxButtons)4, (MessageBoxIcon)32, (MessageBoxDefaultButton)0) == 7)
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

	private void InvertButton_Click(object sender, EventArgs e)
	{
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				list[i].Checked = !list[i].Checked;
			}
		}
	}

	private void ReversalsButton_Click(object sender, EventArgs e)
	{
		List<CheckBox> list = new List<CheckBox>();
		list.AddRange(((IEnumerable)((Control)this).Controls).OfType<CheckBox>());
		checked
		{
			int num = PerformingUp.Count() - 1;
			for (int i = 0; i <= num; i++)
			{
				if (UpBkoutRB.Checked)
				{
					if (ReversalsUp[i])
					{
						list[i].Checked = true;
					}
				}
				else if (ReversalsDown[i])
				{
					list[i].Checked = true;
				}
			}
		}
	}
}
