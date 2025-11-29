using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.Net;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class ManualScoreForm : Form
{
	private struct ScoreInfo
	{
		public int TrendStart;

		public int YrlyRange;

		public int MarketCap;

		public bool bFlatBase;

		public bool bHCR;

		public bool bTall;

		public int VolumeTrend;

		public int BkoutVol;

		public bool bThrowPull;

		public bool bBkoutGap;

		public int sTrendStart;

		public int sYrlyRange;

		public int sMarketCap;

		public int sFlatBase;

		public int sHCR;

		public int sTall;

		public int sVolumeTrend;

		public int sBkoutVol;

		public int sThrowPull;

		public int sBkoutGap;
	}

	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("ToDatePicker")]
	private DateTimePicker _ToDatePicker;

	[CompilerGenerated]
	[AccessedThroughProperty("FromDatePicker")]
	private DateTimePicker _FromDatePicker;

	[CompilerGenerated]
	[AccessedThroughProperty("HelpButton1")]
	private Button _HelpButton1;

	[CompilerGenerated]
	[AccessedThroughProperty("SymbolTextBox")]
	private TextBox _SymbolTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("Chart1")]
	private Chart _Chart1;

	[CompilerGenerated]
	[AccessedThroughProperty("GroupBox1")]
	private GroupBox _GroupBox1;

	[CompilerGenerated]
	[AccessedThroughProperty("TrendLongRB")]
	private RadioButton _TrendLongRB;

	[CompilerGenerated]
	[AccessedThroughProperty("TrendIntermediateRB")]
	private RadioButton _TrendIntermediateRB;

	[CompilerGenerated]
	[AccessedThroughProperty("TrendShortRB")]
	private RadioButton _TrendShortRB;

	[CompilerGenerated]
	[AccessedThroughProperty("GroupBox2")]
	private GroupBox _GroupBox2;

	[CompilerGenerated]
	[AccessedThroughProperty("FlatBaseYRB")]
	private RadioButton _FlatBaseYRB;

	[CompilerGenerated]
	[AccessedThroughProperty("FlatBaseNoRB")]
	private RadioButton _FlatBaseNoRB;

	[CompilerGenerated]
	[AccessedThroughProperty("GroupBox3")]
	private GroupBox _GroupBox3;

	[CompilerGenerated]
	[AccessedThroughProperty("HCRYRB")]
	private RadioButton _HCRYRB;

	[CompilerGenerated]
	[AccessedThroughProperty("HCRNRB")]
	private RadioButton _HCRNRB;

	[CompilerGenerated]
	[AccessedThroughProperty("GroupBox4")]
	private GroupBox _GroupBox4;

	[CompilerGenerated]
	[AccessedThroughProperty("LowThirdRB")]
	private RadioButton _LowThirdRB;

	[CompilerGenerated]
	[AccessedThroughProperty("MiddleThirdRB")]
	private RadioButton _MiddleThirdRB;

	[CompilerGenerated]
	[AccessedThroughProperty("HighThirdRB")]
	private RadioButton _HighThirdRB;

	[CompilerGenerated]
	[AccessedThroughProperty("GroupBox5")]
	private GroupBox _GroupBox5;

	[CompilerGenerated]
	[AccessedThroughProperty("TallRB")]
	private RadioButton _TallRB;

	[CompilerGenerated]
	[AccessedThroughProperty("ShortRB")]
	private RadioButton _ShortRB;

	[CompilerGenerated]
	[AccessedThroughProperty("GroupBox6")]
	private GroupBox _GroupBox6;

	[CompilerGenerated]
	[AccessedThroughProperty("LRVolDRB")]
	private RadioButton _LRVolDRB;

	[CompilerGenerated]
	[AccessedThroughProperty("LRVolURB")]
	private RadioButton _LRVolURB;

	[CompilerGenerated]
	[AccessedThroughProperty("GroupBox7")]
	private GroupBox _GroupBox7;

	[CompilerGenerated]
	[AccessedThroughProperty("BreakVolNRB")]
	private RadioButton _BreakVolNRB;

	[CompilerGenerated]
	[AccessedThroughProperty("BreakVolYRB")]
	private RadioButton _BreakVolYRB;

	[CompilerGenerated]
	[AccessedThroughProperty("GroupBox8")]
	private GroupBox _GroupBox8;

	[CompilerGenerated]
	[AccessedThroughProperty("ThrowNRB")]
	private RadioButton _ThrowNRB;

	[CompilerGenerated]
	[AccessedThroughProperty("ThrowYRB")]
	private RadioButton _ThrowYRB;

	[CompilerGenerated]
	[AccessedThroughProperty("GroupBox9")]
	private GroupBox _GroupBox9;

	[CompilerGenerated]
	[AccessedThroughProperty("GapNRB")]
	private RadioButton _GapNRB;

	[CompilerGenerated]
	[AccessedThroughProperty("GapYRB")]
	private RadioButton _GapYRB;

	[CompilerGenerated]
	[AccessedThroughProperty("GroupBox10")]
	private GroupBox _GroupBox10;

	[CompilerGenerated]
	[AccessedThroughProperty("LargeRB")]
	private RadioButton _LargeRB;

	[CompilerGenerated]
	[AccessedThroughProperty("MediumRB")]
	private RadioButton _MediumRB;

	[CompilerGenerated]
	[AccessedThroughProperty("SmallRB")]
	private RadioButton _SmallRB;

	[CompilerGenerated]
	[AccessedThroughProperty("BrowseButton")]
	private Button _BrowseButton;

	[CompilerGenerated]
	[AccessedThroughProperty("GroupBox11")]
	private GroupBox _GroupBox11;

	[CompilerGenerated]
	[AccessedThroughProperty("BkoutDRB")]
	private RadioButton _BkoutDRB;

	[CompilerGenerated]
	[AccessedThroughProperty("BkoutURB")]
	private RadioButton _BkoutURB;

	[CompilerGenerated]
	[AccessedThroughProperty("GraphButton")]
	private Button _GraphButton;

	[CompilerGenerated]
	[AccessedThroughProperty("MarketCapButton")]
	private Button _MarketCapButton;

	[CompilerGenerated]
	[AccessedThroughProperty("TrendStartButton")]
	private Button _TrendStartButton;

	[CompilerGenerated]
	[AccessedThroughProperty("YearRangeButton")]
	private Button _YearRangeButton;

	[CompilerGenerated]
	[AccessedThroughProperty("FindHeightButton")]
	private Button _FindHeightButton;

	[CompilerGenerated]
	[AccessedThroughProperty("LRVolButton")]
	private Button _LRVolButton;

	[CompilerGenerated]
	[AccessedThroughProperty("BkoutVolButton")]
	private Button _BkoutVolButton;

	[CompilerGenerated]
	[AccessedThroughProperty("BkoutPriceTextBox")]
	private TextBox _BkoutPriceTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("LLTextBox")]
	private TextBox _LLTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("HHTextBox")]
	private TextBox _HHTextBox;

	[CompilerGenerated]
	[AccessedThroughProperty("BkoutDayPicker")]
	private DateTimePicker _BkoutDayPicker;

	[CompilerGenerated]
	[AccessedThroughProperty("UsePatternButton")]
	private Button _UsePatternButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ComboBox1")]
	private ComboBox _ComboBox1;

	[CompilerGenerated]
	[AccessedThroughProperty("CalculateButton")]
	private Button _CalculateButton;

	private string YAHOOURLeod;

	private ScoreInfo Scores;

	private const int LOWTHIRD = 1;

	private const int MIDTHIRD = 2;

	private const int HIGHTHIRD = 3;

	private const int SHORTTERM = 1;

	private const int INTERTERM = 2;

	private const int LONGTERM = 3;

	private const int SMALLCAP = 1;

	private const int MIDCAP = 2;

	private const int LARGECAP = 3;

	private const int HEAVY = 1;

	private const int LIGHT = 2;

	private const int pHIGH = 0;

	private const int pLOW = 1;

	private const int pOPEN = 2;

	private const int pCLOSE = 3;

	private const int NONE = 0;

	private const int FROMDATEP = 1;

	private const int TODATEP = 2;

	private const int BKOUTPICKER = 3;

	private const int HHMTB = 4;

	private const int LLMTB = 5;

	private const int BPMTB = 6;

	private int LastFocus;

	private string lsOpenPath;

	private bool lsChartVolume;

	private string SymbolPlusExtension;

	private Point StartPoint;

	private Point EndPoint;

	private bool Crosshair;

	private Point CrosshairPoint;

	private Pen CrosshairPen;

	private int iPatternStart;

	private int iPatternEnd;

	private byte[] lsPatternArray;

	private bool LockFlag;

	private bool Exiting;

	private DateTime TrendStart;

	private CalloutAnnotation CurrentAnnotation;

	private bool StopPressed;

	internal virtual DateTimePicker ToDatePicker
	{
		[CompilerGenerated]
		get
		{
			return _ToDatePicker;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ToDatePicker_gotFocus;
			DateTimePicker val = _ToDatePicker;
			if (val != null)
			{
				((Control)val).GotFocus -= eventHandler;
			}
			_ToDatePicker = value;
			val = _ToDatePicker;
			if (val != null)
			{
				((Control)val).GotFocus += eventHandler;
			}
		}
	}

	internal virtual DateTimePicker FromDatePicker
	{
		[CompilerGenerated]
		get
		{
			return _FromDatePicker;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = FromDatePicker_GotFocus;
			DateTimePicker val = _FromDatePicker;
			if (val != null)
			{
				((Control)val).GotFocus -= eventHandler;
			}
			_FromDatePicker = value;
			val = _FromDatePicker;
			if (val != null)
			{
				((Control)val).GotFocus += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("ErrorLabel")]
	internal virtual Label ErrorLabel
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
			EventHandler eventHandler = FindHeightButton_GotFocus;
			EventHandler eventHandler2 = HelpButton1_Click;
			Button val = _HelpButton1;
			if (val != null)
			{
				((Control)val).GotFocus -= eventHandler;
				((Control)val).Click -= eventHandler2;
			}
			_HelpButton1 = value;
			val = _HelpButton1;
			if (val != null)
			{
				((Control)val).GotFocus += eventHandler;
				((Control)val).Click += eventHandler2;
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
			EventHandler eventHandler = FindHeightButton_GotFocus;
			EventHandler eventHandler2 = SymbolTextBox_TextChanged;
			TextBox val = _SymbolTextBox;
			if (val != null)
			{
				((Control)val).GotFocus -= eventHandler;
				((Control)val).TextChanged -= eventHandler2;
			}
			_SymbolTextBox = value;
			val = _SymbolTextBox;
			if (val != null)
			{
				((Control)val).GotFocus += eventHandler;
				((Control)val).TextChanged += eventHandler2;
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
			//IL_0021: Unknown result type (might be due to invalid IL or missing references)
			//IL_0027: Expected O, but got Unknown
			//IL_002e: Unknown result type (might be due to invalid IL or missing references)
			//IL_0034: Expected O, but got Unknown
			MouseEventHandler val = new MouseEventHandler(Chart1_MouseDown);
			MouseEventHandler val2 = new MouseEventHandler(Chart1_MouseUp);
			MouseEventHandler val3 = new MouseEventHandler(Chart1_MouseMove);
			PaintEventHandler val4 = new PaintEventHandler(Chart1_Paint);
			EventHandler<ChartPaintEventArgs> eventHandler = Chart1_PostPaint;
			Chart val5 = _Chart1;
			if (val5 != null)
			{
				((Control)val5).MouseDown -= val;
				((Control)val5).MouseUp -= val2;
				((Control)val5).MouseMove -= val3;
				((Control)val5).Paint -= val4;
				val5.PostPaint -= eventHandler;
			}
			_Chart1 = value;
			val5 = _Chart1;
			if (val5 != null)
			{
				((Control)val5).MouseDown += val;
				((Control)val5).MouseUp += val2;
				((Control)val5).MouseMove += val3;
				((Control)val5).Paint += val4;
				val5.PostPaint += eventHandler;
			}
		}
	}

	internal virtual GroupBox GroupBox1
	{
		[CompilerGenerated]
		get
		{
			return _GroupBox1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GroupBox4_Enter;
			GroupBox val = _GroupBox1;
			if (val != null)
			{
				((Control)val).Enter -= eventHandler;
			}
			_GroupBox1 = value;
			val = _GroupBox1;
			if (val != null)
			{
				((Control)val).Enter += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label4")]
	internal virtual Label Label4
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton TrendLongRB
	{
		[CompilerGenerated]
		get
		{
			return _TrendLongRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _TrendLongRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_TrendLongRB = value;
			val = _TrendLongRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual RadioButton TrendIntermediateRB
	{
		[CompilerGenerated]
		get
		{
			return _TrendIntermediateRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _TrendIntermediateRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_TrendIntermediateRB = value;
			val = _TrendIntermediateRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual RadioButton TrendShortRB
	{
		[CompilerGenerated]
		get
		{
			return _TrendShortRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _TrendShortRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_TrendShortRB = value;
			val = _TrendShortRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual GroupBox GroupBox2
	{
		[CompilerGenerated]
		get
		{
			return _GroupBox2;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GroupBox4_Enter;
			GroupBox val = _GroupBox2;
			if (val != null)
			{
				((Control)val).Enter -= eventHandler;
			}
			_GroupBox2 = value;
			val = _GroupBox2;
			if (val != null)
			{
				((Control)val).Enter += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label5")]
	internal virtual Label Label5
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton FlatBaseYRB
	{
		[CompilerGenerated]
		get
		{
			return _FlatBaseYRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _FlatBaseYRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_FlatBaseYRB = value;
			val = _FlatBaseYRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual RadioButton FlatBaseNoRB
	{
		[CompilerGenerated]
		get
		{
			return _FlatBaseNoRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _FlatBaseNoRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_FlatBaseNoRB = value;
			val = _FlatBaseNoRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual GroupBox GroupBox3
	{
		[CompilerGenerated]
		get
		{
			return _GroupBox3;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GroupBox4_Enter;
			GroupBox val = _GroupBox3;
			if (val != null)
			{
				((Control)val).Enter -= eventHandler;
			}
			_GroupBox3 = value;
			val = _GroupBox3;
			if (val != null)
			{
				((Control)val).Enter += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label6")]
	internal virtual Label Label6
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton HCRYRB
	{
		[CompilerGenerated]
		get
		{
			return _HCRYRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _HCRYRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_HCRYRB = value;
			val = _HCRYRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual RadioButton HCRNRB
	{
		[CompilerGenerated]
		get
		{
			return _HCRNRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _HCRNRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_HCRNRB = value;
			val = _HCRNRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual GroupBox GroupBox4
	{
		[CompilerGenerated]
		get
		{
			return _GroupBox4;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GroupBox4_Enter;
			GroupBox val = _GroupBox4;
			if (val != null)
			{
				((Control)val).Enter -= eventHandler;
			}
			_GroupBox4 = value;
			val = _GroupBox4;
			if (val != null)
			{
				((Control)val).Enter += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label7")]
	internal virtual Label Label7
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton LowThirdRB
	{
		[CompilerGenerated]
		get
		{
			return _LowThirdRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _LowThirdRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_LowThirdRB = value;
			val = _LowThirdRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual RadioButton MiddleThirdRB
	{
		[CompilerGenerated]
		get
		{
			return _MiddleThirdRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _MiddleThirdRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_MiddleThirdRB = value;
			val = _MiddleThirdRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual RadioButton HighThirdRB
	{
		[CompilerGenerated]
		get
		{
			return _HighThirdRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _HighThirdRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_HighThirdRB = value;
			val = _HighThirdRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual GroupBox GroupBox5
	{
		[CompilerGenerated]
		get
		{
			return _GroupBox5;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GroupBox4_Enter;
			GroupBox val = _GroupBox5;
			if (val != null)
			{
				((Control)val).Enter -= eventHandler;
			}
			_GroupBox5 = value;
			val = _GroupBox5;
			if (val != null)
			{
				((Control)val).Enter += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label10")]
	internal virtual Label Label10
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

	[field: AccessedThroughProperty("Label8")]
	internal virtual Label Label8
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton TallRB
	{
		[CompilerGenerated]
		get
		{
			return _TallRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _TallRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_TallRB = value;
			val = _TallRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual RadioButton ShortRB
	{
		[CompilerGenerated]
		get
		{
			return _ShortRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _ShortRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_ShortRB = value;
			val = _ShortRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual GroupBox GroupBox6
	{
		[CompilerGenerated]
		get
		{
			return _GroupBox6;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GroupBox4_Enter;
			GroupBox val = _GroupBox6;
			if (val != null)
			{
				((Control)val).Enter -= eventHandler;
			}
			_GroupBox6 = value;
			val = _GroupBox6;
			if (val != null)
			{
				((Control)val).Enter += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label11")]
	internal virtual Label Label11
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton LRVolDRB
	{
		[CompilerGenerated]
		get
		{
			return _LRVolDRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _LRVolDRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_LRVolDRB = value;
			val = _LRVolDRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual RadioButton LRVolURB
	{
		[CompilerGenerated]
		get
		{
			return _LRVolURB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _LRVolURB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_LRVolURB = value;
			val = _LRVolURB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual GroupBox GroupBox7
	{
		[CompilerGenerated]
		get
		{
			return _GroupBox7;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GroupBox4_Enter;
			GroupBox val = _GroupBox7;
			if (val != null)
			{
				((Control)val).Enter -= eventHandler;
			}
			_GroupBox7 = value;
			val = _GroupBox7;
			if (val != null)
			{
				((Control)val).Enter += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label12")]
	internal virtual Label Label12
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton BreakVolNRB
	{
		[CompilerGenerated]
		get
		{
			return _BreakVolNRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _BreakVolNRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_BreakVolNRB = value;
			val = _BreakVolNRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual RadioButton BreakVolYRB
	{
		[CompilerGenerated]
		get
		{
			return _BreakVolYRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _BreakVolYRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_BreakVolYRB = value;
			val = _BreakVolYRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual GroupBox GroupBox8
	{
		[CompilerGenerated]
		get
		{
			return _GroupBox8;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GroupBox4_Enter;
			GroupBox val = _GroupBox8;
			if (val != null)
			{
				((Control)val).Enter -= eventHandler;
			}
			_GroupBox8 = value;
			val = _GroupBox8;
			if (val != null)
			{
				((Control)val).Enter += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label13")]
	internal virtual Label Label13
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton ThrowNRB
	{
		[CompilerGenerated]
		get
		{
			return _ThrowNRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _ThrowNRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_ThrowNRB = value;
			val = _ThrowNRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual RadioButton ThrowYRB
	{
		[CompilerGenerated]
		get
		{
			return _ThrowYRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _ThrowYRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_ThrowYRB = value;
			val = _ThrowYRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual GroupBox GroupBox9
	{
		[CompilerGenerated]
		get
		{
			return _GroupBox9;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GroupBox4_Enter;
			GroupBox val = _GroupBox9;
			if (val != null)
			{
				((Control)val).Enter -= eventHandler;
			}
			_GroupBox9 = value;
			val = _GroupBox9;
			if (val != null)
			{
				((Control)val).Enter += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label14")]
	internal virtual Label Label14
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton GapNRB
	{
		[CompilerGenerated]
		get
		{
			return _GapNRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _GapNRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_GapNRB = value;
			val = _GapNRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual RadioButton GapYRB
	{
		[CompilerGenerated]
		get
		{
			return _GapYRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _GapYRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_GapYRB = value;
			val = _GapYRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual GroupBox GroupBox10
	{
		[CompilerGenerated]
		get
		{
			return _GroupBox10;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GroupBox4_Enter;
			GroupBox val = _GroupBox10;
			if (val != null)
			{
				((Control)val).Enter -= eventHandler;
			}
			_GroupBox10 = value;
			val = _GroupBox10;
			if (val != null)
			{
				((Control)val).Enter += eventHandler;
			}
		}
	}

	internal virtual RadioButton LargeRB
	{
		[CompilerGenerated]
		get
		{
			return _LargeRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _LargeRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_LargeRB = value;
			val = _LargeRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	[field: AccessedThroughProperty("Label15")]
	internal virtual Label Label15
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton MediumRB
	{
		[CompilerGenerated]
		get
		{
			return _MediumRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _MediumRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_MediumRB = value;
			val = _MediumRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual RadioButton SmallRB
	{
		[CompilerGenerated]
		get
		{
			return _SmallRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _SmallRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_SmallRB = value;
			val = _SmallRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	[field: AccessedThroughProperty("Label16")]
	internal virtual Label Label16
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
			EventHandler eventHandler2 = FindHeightButton_GotFocus;
			Button val = _BrowseButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_BrowseButton = value;
			val = _BrowseButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual GroupBox GroupBox11
	{
		[CompilerGenerated]
		get
		{
			return _GroupBox11;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = GroupBox4_Enter;
			GroupBox val = _GroupBox11;
			if (val != null)
			{
				((Control)val).Enter -= eventHandler;
			}
			_GroupBox11 = value;
			val = _GroupBox11;
			if (val != null)
			{
				((Control)val).Enter += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label17")]
	internal virtual Label Label17
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual RadioButton BkoutDRB
	{
		[CompilerGenerated]
		get
		{
			return _BkoutDRB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _BkoutDRB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_BkoutDRB = value;
			val = _BkoutDRB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual RadioButton BkoutURB
	{
		[CompilerGenerated]
		get
		{
			return _BkoutURB;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ShortRB_CheckedChanged;
			EventHandler eventHandler2 = ShortRB_GotFocus;
			RadioButton val = _BkoutURB;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_BkoutURB = value;
			val = _BkoutURB;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
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
			EventHandler eventHandler = FindHeightButton_GotFocus;
			EventHandler eventHandler2 = GraphButton_Click;
			Button val = _GraphButton;
			if (val != null)
			{
				((Control)val).GotFocus -= eventHandler;
				((Control)val).Click -= eventHandler2;
			}
			_GraphButton = value;
			val = _GraphButton;
			if (val != null)
			{
				((Control)val).GotFocus += eventHandler;
				((Control)val).Click += eventHandler2;
			}
		}
	}

	[field: AccessedThroughProperty("ScoreLabel")]
	internal virtual Label ScoreLabel
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

	[field: AccessedThroughProperty("Label19")]
	internal virtual Label Label19
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button MarketCapButton
	{
		[CompilerGenerated]
		get
		{
			return _MarketCapButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = FindHeightButton_GotFocus;
			EventHandler eventHandler2 = MarketCapButton_Click;
			Button val = _MarketCapButton;
			if (val != null)
			{
				((Control)val).GotFocus -= eventHandler;
				((Control)val).Click -= eventHandler2;
			}
			_MarketCapButton = value;
			val = _MarketCapButton;
			if (val != null)
			{
				((Control)val).GotFocus += eventHandler;
				((Control)val).Click += eventHandler2;
			}
		}
	}

	internal virtual Button TrendStartButton
	{
		[CompilerGenerated]
		get
		{
			return _TrendStartButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = FindHeightButton_GotFocus;
			EventHandler eventHandler2 = TrendStartButton_Click;
			Button val = _TrendStartButton;
			if (val != null)
			{
				((Control)val).GotFocus -= eventHandler;
				((Control)val).Click -= eventHandler2;
			}
			_TrendStartButton = value;
			val = _TrendStartButton;
			if (val != null)
			{
				((Control)val).GotFocus += eventHandler;
				((Control)val).Click += eventHandler2;
			}
		}
	}

	internal virtual Button YearRangeButton
	{
		[CompilerGenerated]
		get
		{
			return _YearRangeButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = FindHeightButton_GotFocus;
			EventHandler eventHandler2 = YearRangeButton_Click;
			Button val = _YearRangeButton;
			if (val != null)
			{
				((Control)val).GotFocus -= eventHandler;
				((Control)val).Click -= eventHandler2;
			}
			_YearRangeButton = value;
			val = _YearRangeButton;
			if (val != null)
			{
				((Control)val).GotFocus += eventHandler;
				((Control)val).Click += eventHandler2;
			}
		}
	}

	internal virtual Button FindHeightButton
	{
		[CompilerGenerated]
		get
		{
			return _FindHeightButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = FindHeightButton_Click;
			EventHandler eventHandler2 = FindHeightButton_GotFocus;
			Button val = _FindHeightButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_FindHeightButton = value;
			val = _FindHeightButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual Button LRVolButton
	{
		[CompilerGenerated]
		get
		{
			return _LRVolButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = FindHeightButton_GotFocus;
			EventHandler eventHandler2 = LRVolButton_Click;
			Button val = _LRVolButton;
			if (val != null)
			{
				((Control)val).GotFocus -= eventHandler;
				((Control)val).Click -= eventHandler2;
			}
			_LRVolButton = value;
			val = _LRVolButton;
			if (val != null)
			{
				((Control)val).GotFocus += eventHandler;
				((Control)val).Click += eventHandler2;
			}
		}
	}

	internal virtual Button BkoutVolButton
	{
		[CompilerGenerated]
		get
		{
			return _BkoutVolButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BkoutVolButton_Click;
			EventHandler eventHandler2 = FindHeightButton_GotFocus;
			Button val = _BkoutVolButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_BkoutVolButton = value;
			val = _BkoutVolButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	[field: AccessedThroughProperty("OpenFileDialog1")]
	internal virtual OpenFileDialog OpenFileDialog1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label18")]
	internal virtual Label Label18
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual TextBox BkoutPriceTextBox
	{
		[CompilerGenerated]
		get
		{
			return _BkoutPriceTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0014: Unknown result type (might be due to invalid IL or missing references)
			//IL_001a: Expected O, but got Unknown
			EventHandler eventHandler = BkoutPriceTextBox_GotFocus;
			KeyPressEventHandler val = new KeyPressEventHandler(HHTextBox_KeyPress);
			EventHandler eventHandler2 = HHTextBox_TextChanged;
			TextBox val2 = _BkoutPriceTextBox;
			if (val2 != null)
			{
				((Control)val2).GotFocus -= eventHandler;
				((Control)val2).KeyPress -= val;
				((Control)val2).TextChanged -= eventHandler2;
			}
			_BkoutPriceTextBox = value;
			val2 = _BkoutPriceTextBox;
			if (val2 != null)
			{
				((Control)val2).GotFocus += eventHandler;
				((Control)val2).KeyPress += val;
				((Control)val2).TextChanged += eventHandler2;
			}
		}
	}

	internal virtual TextBox LLTextBox
	{
		[CompilerGenerated]
		get
		{
			return _LLTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0007: Unknown result type (might be due to invalid IL or missing references)
			//IL_000d: Expected O, but got Unknown
			KeyPressEventHandler val = new KeyPressEventHandler(HHTextBox_KeyPress);
			EventHandler eventHandler = HHTextBox_TextChanged;
			EventHandler eventHandler2 = LLTextBox_GotFocus;
			TextBox val2 = _LLTextBox;
			if (val2 != null)
			{
				((Control)val2).KeyPress -= val;
				((Control)val2).TextChanged -= eventHandler;
				((Control)val2).GotFocus -= eventHandler2;
			}
			_LLTextBox = value;
			val2 = _LLTextBox;
			if (val2 != null)
			{
				((Control)val2).KeyPress += val;
				((Control)val2).TextChanged += eventHandler;
				((Control)val2).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual TextBox HHTextBox
	{
		[CompilerGenerated]
		get
		{
			return _HHTextBox;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0007: Unknown result type (might be due to invalid IL or missing references)
			//IL_000d: Expected O, but got Unknown
			KeyPressEventHandler val = new KeyPressEventHandler(HHTextBox_KeyPress);
			EventHandler eventHandler = HHTextBox_TextChanged;
			EventHandler eventHandler2 = HHTextBox_GotFocus;
			TextBox val2 = _HHTextBox;
			if (val2 != null)
			{
				((Control)val2).KeyPress -= val;
				((Control)val2).TextChanged -= eventHandler;
				((Control)val2).GotFocus -= eventHandler2;
			}
			_HHTextBox = value;
			val2 = _HHTextBox;
			if (val2 != null)
			{
				((Control)val2).KeyPress += val;
				((Control)val2).TextChanged += eventHandler;
				((Control)val2).GotFocus += eventHandler2;
			}
		}
	}

	[field: AccessedThroughProperty("Label20")]
	internal virtual Label Label20
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual DateTimePicker BkoutDayPicker
	{
		[CompilerGenerated]
		get
		{
			return _BkoutDayPicker;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BkoutDayPicker_GotFocus;
			DateTimePicker val = _BkoutDayPicker;
			if (val != null)
			{
				((Control)val).GotFocus -= eventHandler;
			}
			_BkoutDayPicker = value;
			val = _BkoutDayPicker;
			if (val != null)
			{
				((Control)val).GotFocus += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label21")]
	internal virtual Label Label21
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button UsePatternButton
	{
		[CompilerGenerated]
		get
		{
			return _UsePatternButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = UsePatternButton_Click;
			Button val = _UsePatternButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_UsePatternButton = value;
			val = _UsePatternButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual ComboBox ComboBox1
	{
		[CompilerGenerated]
		get
		{
			return _ComboBox1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ComboBox1_SelectedIndexChanged;
			EventHandler eventHandler2 = FindHeightButton_GotFocus;
			ComboBox val = _ComboBox1;
			if (val != null)
			{
				val.SelectedIndexChanged -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_ComboBox1 = value;
			val = _ComboBox1;
			if (val != null)
			{
				val.SelectedIndexChanged += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	internal virtual Button CalculateButton
	{
		[CompilerGenerated]
		get
		{
			return _CalculateButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CalculateButton_Click;
			EventHandler eventHandler2 = FindHeightButton_GotFocus;
			Button val = _CalculateButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
				((Control)val).GotFocus -= eventHandler2;
			}
			_CalculateButton = value;
			val = _CalculateButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
				((Control)val).GotFocus += eventHandler2;
			}
		}
	}

	[field: AccessedThroughProperty("Label22")]
	internal virtual Label Label22
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

	public ManualScoreForm()
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		//IL_0020: Unknown result type (might be due to invalid IL or missing references)
		//IL_002a: Expected O, but got Unknown
		//IL_0087: Unknown result type (might be due to invalid IL or missing references)
		//IL_0091: Expected O, but got Unknown
		((Form)this).FormClosing += new FormClosingEventHandler(ManualScoreForm_FormClosing);
		((Form)this).FormClosed += new FormClosedEventHandler(ManualScoreForm_FormClosed);
		((Form)this).Load += ManualScoreForm_Load;
		((Form)this).Activated += ManualScoreForm_Activated;
		YAHOOURLeod = "http://download.finance.yahoo.com/d/quotes.csv?s=";
		lsOpenPath = "";
		Crosshair = false;
		CrosshairPen = null;
		lsPatternArray = new byte[124];
		Exiting = false;
		CurrentAnnotation = new CalloutAnnotation();
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
		//IL_0000: Unknown result type (might be due to invalid IL or missing references)
		//IL_0006: Expected O, but got Unknown
		//IL_0006: Unknown result type (might be due to invalid IL or missing references)
		//IL_000c: Expected O, but got Unknown
		//IL_000c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0012: Expected O, but got Unknown
		//IL_0013: Unknown result type (might be due to invalid IL or missing references)
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
		//IL_0173: Unknown result type (might be due to invalid IL or missing references)
		//IL_017d: Expected O, but got Unknown
		//IL_017e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0188: Expected O, but got Unknown
		//IL_0189: Unknown result type (might be due to invalid IL or missing references)
		//IL_0193: Expected O, but got Unknown
		//IL_0194: Unknown result type (might be due to invalid IL or missing references)
		//IL_019e: Expected O, but got Unknown
		//IL_019f: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a9: Expected O, but got Unknown
		//IL_01aa: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b4: Expected O, but got Unknown
		//IL_01b5: Unknown result type (might be due to invalid IL or missing references)
		//IL_01bf: Expected O, but got Unknown
		//IL_01c0: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ca: Expected O, but got Unknown
		//IL_01cb: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d5: Expected O, but got Unknown
		//IL_01d6: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e0: Expected O, but got Unknown
		//IL_01e1: Unknown result type (might be due to invalid IL or missing references)
		//IL_01eb: Expected O, but got Unknown
		//IL_01ec: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f6: Expected O, but got Unknown
		//IL_01f7: Unknown result type (might be due to invalid IL or missing references)
		//IL_0201: Expected O, but got Unknown
		//IL_0202: Unknown result type (might be due to invalid IL or missing references)
		//IL_020c: Expected O, but got Unknown
		//IL_020d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0217: Expected O, but got Unknown
		//IL_0218: Unknown result type (might be due to invalid IL or missing references)
		//IL_0222: Expected O, but got Unknown
		//IL_0223: Unknown result type (might be due to invalid IL or missing references)
		//IL_022d: Expected O, but got Unknown
		//IL_022e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0238: Expected O, but got Unknown
		//IL_0239: Unknown result type (might be due to invalid IL or missing references)
		//IL_0243: Expected O, but got Unknown
		//IL_0244: Unknown result type (might be due to invalid IL or missing references)
		//IL_024e: Expected O, but got Unknown
		//IL_024f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0259: Expected O, but got Unknown
		//IL_025a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0264: Expected O, but got Unknown
		//IL_0265: Unknown result type (might be due to invalid IL or missing references)
		//IL_026f: Expected O, but got Unknown
		//IL_0270: Unknown result type (might be due to invalid IL or missing references)
		//IL_027a: Expected O, but got Unknown
		//IL_027b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0285: Expected O, but got Unknown
		//IL_0286: Unknown result type (might be due to invalid IL or missing references)
		//IL_0290: Expected O, but got Unknown
		//IL_0291: Unknown result type (might be due to invalid IL or missing references)
		//IL_029b: Expected O, but got Unknown
		//IL_029c: Unknown result type (might be due to invalid IL or missing references)
		//IL_02a6: Expected O, but got Unknown
		//IL_02a7: Unknown result type (might be due to invalid IL or missing references)
		//IL_02b1: Expected O, but got Unknown
		//IL_02b2: Unknown result type (might be due to invalid IL or missing references)
		//IL_02bc: Expected O, but got Unknown
		//IL_02bd: Unknown result type (might be due to invalid IL or missing references)
		//IL_02c7: Expected O, but got Unknown
		//IL_02c8: Unknown result type (might be due to invalid IL or missing references)
		//IL_02d2: Expected O, but got Unknown
		//IL_02d3: Unknown result type (might be due to invalid IL or missing references)
		//IL_02dd: Expected O, but got Unknown
		//IL_02de: Unknown result type (might be due to invalid IL or missing references)
		//IL_02e8: Expected O, but got Unknown
		//IL_02e9: Unknown result type (might be due to invalid IL or missing references)
		//IL_02f3: Expected O, but got Unknown
		//IL_02f4: Unknown result type (might be due to invalid IL or missing references)
		//IL_02fe: Expected O, but got Unknown
		//IL_02ff: Unknown result type (might be due to invalid IL or missing references)
		//IL_0309: Expected O, but got Unknown
		//IL_030a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0314: Expected O, but got Unknown
		//IL_0315: Unknown result type (might be due to invalid IL or missing references)
		//IL_031f: Expected O, but got Unknown
		//IL_0320: Unknown result type (might be due to invalid IL or missing references)
		//IL_032a: Expected O, but got Unknown
		//IL_032b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0335: Expected O, but got Unknown
		//IL_0336: Unknown result type (might be due to invalid IL or missing references)
		//IL_0340: Expected O, but got Unknown
		//IL_0341: Unknown result type (might be due to invalid IL or missing references)
		//IL_034b: Expected O, but got Unknown
		//IL_034c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0356: Expected O, but got Unknown
		//IL_0357: Unknown result type (might be due to invalid IL or missing references)
		//IL_0361: Expected O, but got Unknown
		//IL_0362: Unknown result type (might be due to invalid IL or missing references)
		//IL_036c: Expected O, but got Unknown
		//IL_036d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0377: Expected O, but got Unknown
		//IL_0378: Unknown result type (might be due to invalid IL or missing references)
		//IL_0382: Expected O, but got Unknown
		//IL_0383: Unknown result type (might be due to invalid IL or missing references)
		//IL_038d: Expected O, but got Unknown
		//IL_038e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0398: Expected O, but got Unknown
		//IL_0399: Unknown result type (might be due to invalid IL or missing references)
		//IL_03a3: Expected O, but got Unknown
		//IL_03a4: Unknown result type (might be due to invalid IL or missing references)
		//IL_03ae: Expected O, but got Unknown
		//IL_09f3: Unknown result type (might be due to invalid IL or missing references)
		//IL_2a20: Unknown result type (might be due to invalid IL or missing references)
		//IL_2a2a: Expected O, but got Unknown
		//IL_2b3d: Unknown result type (might be due to invalid IL or missing references)
		//IL_2b47: Expected O, but got Unknown
		ChartArea val = new ChartArea();
		Series val2 = new Series();
		Series val3 = new Series();
		ToDatePicker = new DateTimePicker();
		FromDatePicker = new DateTimePicker();
		ErrorLabel = new Label();
		HelpButton1 = new Button();
		Label1 = new Label();
		SymbolTextBox = new TextBox();
		DoneButton = new Button();
		Label3 = new Label();
		Label2 = new Label();
		Chart1 = new Chart();
		GroupBox1 = new GroupBox();
		TrendStartButton = new Button();
		Label4 = new Label();
		TrendLongRB = new RadioButton();
		TrendIntermediateRB = new RadioButton();
		TrendShortRB = new RadioButton();
		GroupBox2 = new GroupBox();
		Label5 = new Label();
		FlatBaseYRB = new RadioButton();
		FlatBaseNoRB = new RadioButton();
		GroupBox3 = new GroupBox();
		Label6 = new Label();
		HCRYRB = new RadioButton();
		HCRNRB = new RadioButton();
		GroupBox4 = new GroupBox();
		YearRangeButton = new Button();
		Label7 = new Label();
		LowThirdRB = new RadioButton();
		MiddleThirdRB = new RadioButton();
		HighThirdRB = new RadioButton();
		GroupBox5 = new GroupBox();
		Label20 = new Label();
		ShortRB = new RadioButton();
		TallRB = new RadioButton();
		BkoutPriceTextBox = new TextBox();
		LLTextBox = new TextBox();
		HHTextBox = new TextBox();
		FindHeightButton = new Button();
		Label10 = new Label();
		Label9 = new Label();
		Label8 = new Label();
		GroupBox6 = new GroupBox();
		LRVolButton = new Button();
		Label11 = new Label();
		LRVolDRB = new RadioButton();
		LRVolURB = new RadioButton();
		GroupBox7 = new GroupBox();
		BkoutVolButton = new Button();
		Label12 = new Label();
		BreakVolNRB = new RadioButton();
		BreakVolYRB = new RadioButton();
		GroupBox8 = new GroupBox();
		Label13 = new Label();
		ThrowNRB = new RadioButton();
		ThrowYRB = new RadioButton();
		GroupBox9 = new GroupBox();
		Label14 = new Label();
		GapNRB = new RadioButton();
		GapYRB = new RadioButton();
		GroupBox10 = new GroupBox();
		MarketCapButton = new Button();
		LargeRB = new RadioButton();
		Label15 = new Label();
		MediumRB = new RadioButton();
		SmallRB = new RadioButton();
		Label16 = new Label();
		BrowseButton = new Button();
		GroupBox11 = new GroupBox();
		Label17 = new Label();
		BkoutDRB = new RadioButton();
		BkoutURB = new RadioButton();
		GraphButton = new Button();
		ScoreLabel = new Label();
		Panel1 = new Panel();
		Label19 = new Label();
		OpenFileDialog1 = new OpenFileDialog();
		Label18 = new Label();
		BkoutDayPicker = new DateTimePicker();
		Label21 = new Label();
		UsePatternButton = new Button();
		ComboBox1 = new ComboBox();
		CalculateButton = new Button();
		Label22 = new Label();
		LoadingBar = new ProgressBar();
		((ISupportInitialize)Chart1).BeginInit();
		((Control)GroupBox1).SuspendLayout();
		((Control)GroupBox2).SuspendLayout();
		((Control)GroupBox3).SuspendLayout();
		((Control)GroupBox4).SuspendLayout();
		((Control)GroupBox5).SuspendLayout();
		((Control)GroupBox6).SuspendLayout();
		((Control)GroupBox7).SuspendLayout();
		((Control)GroupBox8).SuspendLayout();
		((Control)GroupBox9).SuspendLayout();
		((Control)GroupBox10).SuspendLayout();
		((Control)GroupBox11).SuspendLayout();
		((Control)Panel1).SuspendLayout();
		((Control)this).SuspendLayout();
		((Control)ToDatePicker).Anchor = (AnchorStyles)10;
		ToDatePicker.CustomFormat = "yyyy/MM/dd";
		ToDatePicker.Format = (DateTimePickerFormat)8;
		((Control)ToDatePicker).Location = new Point(431, 368);
		((Control)ToDatePicker).Name = "ToDatePicker";
		ToDatePicker.ShowUpDown = true;
		((Control)ToDatePicker).Size = new Size(120, 20);
		((Control)ToDatePicker).TabIndex = 13;
		ToDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)FromDatePicker).Anchor = (AnchorStyles)10;
		FromDatePicker.CustomFormat = "yyyy/MM/dd";
		FromDatePicker.Format = (DateTimePickerFormat)8;
		((Control)FromDatePicker).Location = new Point(431, 343);
		((Control)FromDatePicker).Name = "FromDatePicker";
		FromDatePicker.ShowUpDown = true;
		((Control)FromDatePicker).Size = new Size(120, 20);
		((Control)FromDatePicker).TabIndex = 11;
		FromDatePicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)ErrorLabel).Anchor = (AnchorStyles)10;
		ErrorLabel.BorderStyle = (BorderStyle)2;
		((Control)ErrorLabel).Location = new Point(11, 312);
		((Control)ErrorLabel).Name = "ErrorLabel";
		((Control)ErrorLabel).Size = new Size(540, 22);
		((Control)ErrorLabel).TabIndex = 3;
		((Control)HelpButton1).Anchor = (AnchorStyles)10;
		((Control)HelpButton1).Location = new Point(805, 679);
		((Control)HelpButton1).Name = "HelpButton1";
		((Control)HelpButton1).Size = new Size(60, 23);
		((Control)HelpButton1).TabIndex = 30;
		((ButtonBase)HelpButton1).Text = "&Help";
		((ButtonBase)HelpButton1).UseVisualStyleBackColor = true;
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(11, 371);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(44, 13);
		((Control)Label1).TabIndex = 6;
		Label1.Text = "S&ymbol:";
		((Control)SymbolTextBox).Anchor = (AnchorStyles)10;
		((Control)SymbolTextBox).Location = new Point(57, 368);
		((Control)SymbolTextBox).Name = "SymbolTextBox";
		((Control)SymbolTextBox).Size = new Size(66, 20);
		((Control)SymbolTextBox).TabIndex = 7;
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(939, 679);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(60, 23);
		((Control)DoneButton).TabIndex = 1;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)Label3).Anchor = (AnchorStyles)10;
		Label3.AutoSize = true;
		((Control)Label3).ForeColor = Color.Red;
		((Control)Label3).Location = new Point(360, 371);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(65, 13);
		((Control)Label3).TabIndex = 12;
		Label3.Text = "&Pattern end:";
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).ForeColor = Color.Red;
		((Control)Label2).Location = new Point(358, 346);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(67, 13);
		((Control)Label2).TabIndex = 10;
		Label2.Text = "&Pattern start:";
		((Control)Chart1).Anchor = (AnchorStyles)15;
		val.AxisX.Enabled = (AxisEnabled)1;
		val.AxisX.IntervalAutoMode = (IntervalAutoMode)1;
		val.AxisX.LabelAutoFitMaxFontSize = 8;
		val.AxisX.MajorGrid.Enabled = false;
		val.AxisX2.Enabled = (AxisEnabled)2;
		val.AxisY.Enabled = (AxisEnabled)2;
		val.AxisY.ScrollBar.Enabled = false;
		val.AxisY2.Enabled = (AxisEnabled)1;
		val.AxisY2.LabelAutoFitMaxFontSize = 8;
		val.AxisY2.MajorGrid.Enabled = false;
		val.AxisY2.MajorGrid.Interval = 0.0;
		val.AxisY2.MajorGrid.IntervalOffsetType = (DateTimeIntervalType)0;
		val.AxisY2.MajorGrid.IntervalType = (DateTimeIntervalType)1;
		val.AxisY2.ScrollBar.Enabled = false;
		val.BorderDashStyle = (ChartDashStyle)5;
		val.Name = "ChartArea1";
		val.Position.Auto = false;
		val.Position.Height = 100f;
		val.Position.Width = 100f;
		val.ShadowOffset = 7;
		((Collection<ChartArea>)(object)Chart1.ChartAreas).Add(val);
		((Control)Chart1).Location = new Point(1, 9);
		((Control)Chart1).Margin = new Padding(0);
		((Control)Chart1).Name = "Chart1";
		((DataPointCustomProperties)val2).BorderColor = Color.Black;
		val2.ChartArea = "ChartArea1";
		val2.ChartType = (SeriesChartType)20;
		((DataPointCustomProperties)val2).CustomProperties = "PriceDownColor=Red, PriceUpColor=green";
		val2.IsXValueIndexed = true;
		((DataPointCustomProperties)val2).MarkerBorderColor = Color.White;
		((DataPointCustomProperties)val2).MarkerColor = Color.Black;
		val2.Name = "CandleSeries";
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
		Chart1.Size = new Size(998, 299);
		((Control)Chart1).TabIndex = 2;
		((Control)Chart1).Text = "Chart1";
		((Control)GroupBox1).Anchor = (AnchorStyles)10;
		((Control)GroupBox1).Controls.Add((Control)(object)TrendStartButton);
		((Control)GroupBox1).Controls.Add((Control)(object)Label4);
		((Control)GroupBox1).Controls.Add((Control)(object)TrendLongRB);
		((Control)GroupBox1).Controls.Add((Control)(object)TrendIntermediateRB);
		((Control)GroupBox1).Controls.Add((Control)(object)TrendShortRB);
		((Control)GroupBox1).Location = new Point(569, 305);
		((Control)GroupBox1).Name = "GroupBox1";
		((Control)GroupBox1).Size = new Size(184, 117);
		((Control)GroupBox1).TabIndex = 22;
		GroupBox1.TabStop = false;
		GroupBox1.Text = "Step 5: Trend Start";
		((Control)TrendStartButton).Anchor = (AnchorStyles)10;
		((Control)TrendStartButton).Enabled = false;
		((Control)TrendStartButton).Location = new Point(135, 83);
		((Control)TrendStartButton).Name = "TrendStartButton";
		((Control)TrendStartButton).Size = new Size(43, 23);
		((Control)TrendStartButton).TabIndex = 4;
		((ButtonBase)TrendStartButton).Text = "Find";
		((ButtonBase)TrendStartButton).UseVisualStyleBackColor = true;
		((Control)Label4).Location = new Point(6, 16);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(172, 31);
		((Control)Label4).TabIndex = 0;
		Label4.Text = "How long is the price trend leading to the start of the chart pattern?";
		((ButtonBase)TrendLongRB).AutoSize = true;
		((Control)TrendLongRB).Location = new Point(21, 86);
		((Control)TrendLongRB).Name = "TrendLongRB";
		((Control)TrendLongRB).Size = new Size(74, 17);
		((Control)TrendLongRB).TabIndex = 3;
		((ButtonBase)TrendLongRB).Text = "6+ months";
		((ButtonBase)TrendLongRB).UseVisualStyleBackColor = true;
		((ButtonBase)TrendIntermediateRB).AutoSize = true;
		((Control)TrendIntermediateRB).Location = new Point(21, 68);
		((Control)TrendIntermediateRB).Name = "TrendIntermediateRB";
		((Control)TrendIntermediateRB).Size = new Size(77, 17);
		((Control)TrendIntermediateRB).TabIndex = 2;
		((ButtonBase)TrendIntermediateRB).Text = "3-6 months";
		((ButtonBase)TrendIntermediateRB).UseVisualStyleBackColor = true;
		((ButtonBase)TrendShortRB).AutoSize = true;
		TrendShortRB.Checked = true;
		((Control)TrendShortRB).Location = new Point(21, 50);
		((Control)TrendShortRB).Name = "TrendShortRB";
		((Control)TrendShortRB).Size = new Size(77, 17);
		((Control)TrendShortRB).TabIndex = 1;
		TrendShortRB.TabStop = true;
		((ButtonBase)TrendShortRB).Text = "0-3 months";
		((ButtonBase)TrendShortRB).UseVisualStyleBackColor = true;
		((Control)GroupBox2).Anchor = (AnchorStyles)10;
		((Control)GroupBox2).Controls.Add((Control)(object)Label5);
		((Control)GroupBox2).Controls.Add((Control)(object)FlatBaseYRB);
		((Control)GroupBox2).Controls.Add((Control)(object)FlatBaseNoRB);
		((Control)GroupBox2).Location = new Point(11, 594);
		((Control)GroupBox2).Name = "GroupBox2";
		((Control)GroupBox2).Size = new Size(480, 55);
		((Control)GroupBox2).TabIndex = 20;
		GroupBox2.TabStop = false;
		GroupBox2.Text = "Step 3: Flat Base";
		((Control)Label5).Location = new Point(9, 21);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(356, 32);
		((Control)Label5).TabIndex = 0;
		Label5.Text = "Does a long (3+ months long ending within 2 months of chart pattern start) flat price trend precede the chart pattern?";
		((ButtonBase)FlatBaseYRB).AutoSize = true;
		((Control)FlatBaseYRB).Location = new Point(420, 19);
		((Control)FlatBaseYRB).Name = "FlatBaseYRB";
		((Control)FlatBaseYRB).Size = new Size(43, 17);
		((Control)FlatBaseYRB).TabIndex = 2;
		((ButtonBase)FlatBaseYRB).Text = "Yes";
		((ButtonBase)FlatBaseYRB).UseVisualStyleBackColor = true;
		((ButtonBase)FlatBaseNoRB).AutoSize = true;
		FlatBaseNoRB.Checked = true;
		((Control)FlatBaseNoRB).Location = new Point(375, 19);
		((Control)FlatBaseNoRB).Name = "FlatBaseNoRB";
		((Control)FlatBaseNoRB).Size = new Size(39, 17);
		((Control)FlatBaseNoRB).TabIndex = 1;
		FlatBaseNoRB.TabStop = true;
		((ButtonBase)FlatBaseNoRB).Text = "No";
		((ButtonBase)FlatBaseNoRB).UseVisualStyleBackColor = true;
		((Control)GroupBox3).Anchor = (AnchorStyles)10;
		((Control)GroupBox3).Controls.Add((Control)(object)Label6);
		((Control)GroupBox3).Controls.Add((Control)(object)HCRYRB);
		((Control)GroupBox3).Controls.Add((Control)(object)HCRNRB);
		((Control)GroupBox3).Location = new Point(11, 655);
		((Control)GroupBox3).Name = "GroupBox3";
		((Control)GroupBox3).Size = new Size(480, 61);
		((Control)GroupBox3).TabIndex = 21;
		GroupBox3.TabStop = false;
		GroupBox3.Text = "Step 4: Horizontal Consolidation Region";
		((Control)Label6).Location = new Point(6, 26);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(363, 30);
		((Control)Label6).TabIndex = 0;
		Label6.Text = "After the breakout, will price hit overhead resistance/underlying support which may appear between the trend start and chart pattern start?";
		((ButtonBase)HCRYRB).AutoSize = true;
		HCRYRB.Checked = true;
		((Control)HCRYRB).Location = new Point(420, 26);
		((Control)HCRYRB).Name = "HCRYRB";
		((Control)HCRYRB).Size = new Size(43, 17);
		((Control)HCRYRB).TabIndex = 2;
		HCRYRB.TabStop = true;
		((ButtonBase)HCRYRB).Text = "Yes";
		((ButtonBase)HCRYRB).UseVisualStyleBackColor = true;
		((ButtonBase)HCRNRB).AutoSize = true;
		((Control)HCRNRB).Location = new Point(375, 26);
		((Control)HCRNRB).Name = "HCRNRB";
		((Control)HCRNRB).Size = new Size(39, 17);
		((Control)HCRNRB).TabIndex = 1;
		((ButtonBase)HCRNRB).Text = "No";
		((ButtonBase)HCRNRB).UseVisualStyleBackColor = true;
		((Control)GroupBox4).Anchor = (AnchorStyles)10;
		((Control)GroupBox4).Controls.Add((Control)(object)YearRangeButton);
		((Control)GroupBox4).Controls.Add((Control)(object)Label7);
		((Control)GroupBox4).Controls.Add((Control)(object)LowThirdRB);
		((Control)GroupBox4).Controls.Add((Control)(object)MiddleThirdRB);
		((Control)GroupBox4).Controls.Add((Control)(object)HighThirdRB);
		((Control)GroupBox4).Location = new Point(300, 468);
		((Control)GroupBox4).Name = "GroupBox4";
		((Control)GroupBox4).Size = new Size(191, 120);
		((Control)GroupBox4).TabIndex = 19;
		GroupBox4.TabStop = false;
		GroupBox4.Text = "Step 2: Yearly Price Range";
		((Control)YearRangeButton).Anchor = (AnchorStyles)10;
		((Control)YearRangeButton).Location = new Point(131, 86);
		((Control)YearRangeButton).Name = "YearRangeButton";
		((Control)YearRangeButton).Size = new Size(43, 23);
		((Control)YearRangeButton).TabIndex = 4;
		((ButtonBase)YearRangeButton).Text = "Find";
		((ButtonBase)YearRangeButton).UseVisualStyleBackColor = true;
		((Control)Label7).Location = new Point(6, 16);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(179, 31);
		((Control)Label7).TabIndex = 0;
		Label7.Text = "Where is the (expected) breakout price in the yearly price range?";
		((ButtonBase)LowThirdRB).AutoSize = true;
		((Control)LowThirdRB).Location = new Point(21, 96);
		((Control)LowThirdRB).Name = "LowThirdRB";
		((Control)LowThirdRB).Size = new Size(82, 17);
		((Control)LowThirdRB).TabIndex = 3;
		((ButtonBase)LowThirdRB).Text = "Lowest third";
		((ButtonBase)LowThirdRB).UseVisualStyleBackColor = true;
		((ButtonBase)MiddleThirdRB).AutoSize = true;
		MiddleThirdRB.Checked = true;
		((Control)MiddleThirdRB).Location = new Point(21, 73);
		((Control)MiddleThirdRB).Name = "MiddleThirdRB";
		((Control)MiddleThirdRB).Size = new Size(79, 17);
		((Control)MiddleThirdRB).TabIndex = 2;
		MiddleThirdRB.TabStop = true;
		((ButtonBase)MiddleThirdRB).Text = "Middle third";
		((ButtonBase)MiddleThirdRB).UseVisualStyleBackColor = true;
		((ButtonBase)HighThirdRB).AutoSize = true;
		((Control)HighThirdRB).Location = new Point(21, 50);
		((Control)HighThirdRB).Name = "HighThirdRB";
		((Control)HighThirdRB).Size = new Size(84, 17);
		((Control)HighThirdRB).TabIndex = 1;
		((ButtonBase)HighThirdRB).Text = "Highest third";
		((ButtonBase)HighThirdRB).UseVisualStyleBackColor = true;
		((Control)GroupBox5).Anchor = (AnchorStyles)10;
		((Control)GroupBox5).Controls.Add((Control)(object)Label20);
		((Control)GroupBox5).Controls.Add((Control)(object)ShortRB);
		((Control)GroupBox5).Controls.Add((Control)(object)TallRB);
		((Control)GroupBox5).Controls.Add((Control)(object)BkoutPriceTextBox);
		((Control)GroupBox5).Controls.Add((Control)(object)LLTextBox);
		((Control)GroupBox5).Controls.Add((Control)(object)HHTextBox);
		((Control)GroupBox5).Controls.Add((Control)(object)FindHeightButton);
		((Control)GroupBox5).Controls.Add((Control)(object)Label10);
		((Control)GroupBox5).Controls.Add((Control)(object)Label9);
		((Control)GroupBox5).Controls.Add((Control)(object)Label8);
		((Control)GroupBox5).Location = new Point(11, 468);
		((Control)GroupBox5).Name = "GroupBox5";
		((Control)GroupBox5).Size = new Size(283, 120);
		((Control)GroupBox5).TabIndex = 18;
		GroupBox5.TabStop = false;
		GroupBox5.Text = "Step 1: Chart Pattern Height";
		Label20.AutoSize = true;
		((Control)Label20).ForeColor = Color.Black;
		((Control)Label20).Location = new Point(6, 94);
		((Control)Label20).Name = "Label20";
		((Control)Label20).Size = new Size(13, 13);
		((Control)Label20).TabIndex = 6;
		Label20.Text = "4";
		((ButtonBase)ShortRB).AutoSize = true;
		ShortRB.Checked = true;
		((Control)ShortRB).Location = new Point(26, 93);
		((Control)ShortRB).Name = "ShortRB";
		((Control)ShortRB).Size = new Size(50, 17);
		((Control)ShortRB).TabIndex = 7;
		ShortRB.TabStop = true;
		((ButtonBase)ShortRB).Text = "Short";
		((ButtonBase)ShortRB).UseVisualStyleBackColor = true;
		((ButtonBase)TallRB).AutoSize = true;
		((Control)TallRB).Location = new Point(82, 93);
		((Control)TallRB).Name = "TallRB";
		((Control)TallRB).Size = new Size(42, 17);
		((Control)TallRB).TabIndex = 8;
		((ButtonBase)TallRB).Text = "Tall";
		((ButtonBase)TallRB).UseVisualStyleBackColor = true;
		((Control)BkoutPriceTextBox).Location = new Point(206, 68);
		((Control)BkoutPriceTextBox).Name = "BkoutPriceTextBox";
		((Control)BkoutPriceTextBox).Size = new Size(65, 20);
		((Control)BkoutPriceTextBox).TabIndex = 5;
		((Control)LLTextBox).Location = new Point(206, 42);
		((Control)LLTextBox).Name = "LLTextBox";
		((Control)LLTextBox).Size = new Size(65, 20);
		((Control)LLTextBox).TabIndex = 3;
		((Control)HHTextBox).Location = new Point(206, 16);
		((Control)HHTextBox).Name = "HHTextBox";
		((Control)HHTextBox).Size = new Size(65, 20);
		((Control)HHTextBox).TabIndex = 1;
		((Control)FindHeightButton).Anchor = (AnchorStyles)10;
		((Control)FindHeightButton).Location = new Point(175, 92);
		((Control)FindHeightButton).Name = "FindHeightButton";
		((Control)FindHeightButton).Size = new Size(96, 23);
		((Control)FindHeightButton).TabIndex = 9;
		((ButtonBase)FindHeightButton).Text = "Find 1, 2, ~3,  4";
		((ButtonBase)FindHeightButton).UseVisualStyleBackColor = true;
		((Control)Label10).ForeColor = Color.Red;
		((Control)Label10).Location = new Point(6, 68);
		((Control)Label10).Name = "Label10";
		((Control)Label10).Size = new Size(164, 19);
		((Control)Label10).TabIndex = 4;
		Label10.Text = "3. Anticipated breakout price?";
		((Control)Label9).ForeColor = Color.Red;
		((Control)Label9).Location = new Point(6, 45);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(194, 19);
		((Control)Label9).TabIndex = 2;
		Label9.Text = "2. Lowest price in the chart pattern?";
		((Control)Label8).ForeColor = Color.Red;
		((Control)Label8).Location = new Point(6, 22);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(194, 19);
		((Control)Label8).TabIndex = 0;
		Label8.Text = "1. Highest price in the chart pattern?";
		((Control)GroupBox6).Anchor = (AnchorStyles)10;
		((Control)GroupBox6).Controls.Add((Control)(object)LRVolButton);
		((Control)GroupBox6).Controls.Add((Control)(object)Label11);
		((Control)GroupBox6).Controls.Add((Control)(object)LRVolDRB);
		((Control)GroupBox6).Controls.Add((Control)(object)LRVolURB);
		((Control)GroupBox6).Location = new Point(526, 477);
		((Control)GroupBox6).Name = "GroupBox6";
		((Control)GroupBox6).Size = new Size(480, 41);
		((Control)GroupBox6).TabIndex = 25;
		GroupBox6.TabStop = false;
		GroupBox6.Text = "Step 8: Volume Trend";
		((Control)LRVolButton).Anchor = (AnchorStyles)10;
		((Control)LRVolButton).Location = new Point(322, 11);
		((Control)LRVolButton).Name = "LRVolButton";
		((Control)LRVolButton).Size = new Size(43, 23);
		((Control)LRVolButton).TabIndex = 1;
		((ButtonBase)LRVolButton).Text = "Find";
		((ButtonBase)LRVolButton).UseVisualStyleBackColor = true;
		Label11.AutoSize = true;
		((Control)Label11).Location = new Point(9, 16);
		((Control)Label11).Name = "Label11";
		((Control)Label11).Size = new Size(277, 13);
		((Control)Label11).TabIndex = 0;
		Label11.Text = "Between pattern start and end, what is the volume trend?";
		((ButtonBase)LRVolDRB).AutoSize = true;
		LRVolDRB.Checked = true;
		((Control)LRVolDRB).Location = new Point(420, 14);
		((Control)LRVolDRB).Name = "LRVolDRB";
		((Control)LRVolDRB).Size = new Size(53, 17);
		((Control)LRVolDRB).TabIndex = 3;
		LRVolDRB.TabStop = true;
		((ButtonBase)LRVolDRB).Text = "Down";
		((ButtonBase)LRVolDRB).UseVisualStyleBackColor = true;
		((ButtonBase)LRVolURB).AutoSize = true;
		((Control)LRVolURB).Location = new Point(371, 14);
		((Control)LRVolURB).Name = "LRVolURB";
		((Control)LRVolURB).Size = new Size(39, 17);
		((Control)LRVolURB).TabIndex = 2;
		((ButtonBase)LRVolURB).Text = "Up";
		((ButtonBase)LRVolURB).UseVisualStyleBackColor = true;
		((Control)GroupBox7).Anchor = (AnchorStyles)10;
		((Control)GroupBox7).Controls.Add((Control)(object)BkoutVolButton);
		((Control)GroupBox7).Controls.Add((Control)(object)Label12);
		((Control)GroupBox7).Controls.Add((Control)(object)BreakVolNRB);
		((Control)GroupBox7).Controls.Add((Control)(object)BreakVolYRB);
		((Control)GroupBox7).Location = new Point(526, 524);
		((Control)GroupBox7).Name = "GroupBox7";
		((Control)GroupBox7).Size = new Size(480, 52);
		((Control)GroupBox7).TabIndex = 26;
		GroupBox7.TabStop = false;
		GroupBox7.Text = "Step 9: Breakout Day Volume";
		((Control)BkoutVolButton).Anchor = (AnchorStyles)10;
		((Control)BkoutVolButton).Location = new Point(322, 17);
		((Control)BkoutVolButton).Name = "BkoutVolButton";
		((Control)BkoutVolButton).Size = new Size(43, 23);
		((Control)BkoutVolButton).TabIndex = 1;
		((ButtonBase)BkoutVolButton).Text = "Find";
		((ButtonBase)BkoutVolButton).UseVisualStyleBackColor = true;
		((Control)Label12).Location = new Point(9, 16);
		((Control)Label12).Name = "Label12";
		((Control)Label12).Size = new Size(283, 33);
		((Control)Label12).TabIndex = 0;
		Label12.Text = "Is breakout day volume at least 25% above the 3-month average? If no breakout yet, answer No.";
		((ButtonBase)BreakVolNRB).AutoSize = true;
		BreakVolNRB.Checked = true;
		((Control)BreakVolNRB).Location = new Point(420, 19);
		((Control)BreakVolNRB).Name = "BreakVolNRB";
		((Control)BreakVolNRB).Size = new Size(39, 17);
		((Control)BreakVolNRB).TabIndex = 3;
		BreakVolNRB.TabStop = true;
		((ButtonBase)BreakVolNRB).Text = "No";
		((ButtonBase)BreakVolNRB).UseVisualStyleBackColor = true;
		((ButtonBase)BreakVolYRB).AutoSize = true;
		((Control)BreakVolYRB).Location = new Point(371, 19);
		((Control)BreakVolYRB).Name = "BreakVolYRB";
		((Control)BreakVolYRB).Size = new Size(43, 17);
		((Control)BreakVolYRB).TabIndex = 2;
		((ButtonBase)BreakVolYRB).Text = "Yes";
		((ButtonBase)BreakVolYRB).UseVisualStyleBackColor = true;
		((Control)GroupBox8).Anchor = (AnchorStyles)10;
		((Control)GroupBox8).Controls.Add((Control)(object)Label13);
		((Control)GroupBox8).Controls.Add((Control)(object)ThrowNRB);
		((Control)GroupBox8).Controls.Add((Control)(object)ThrowYRB);
		((Control)GroupBox8).Location = new Point(526, 582);
		((Control)GroupBox8).Name = "GroupBox8";
		((Control)GroupBox8).Size = new Size(480, 37);
		((Control)GroupBox8).TabIndex = 27;
		GroupBox8.TabStop = false;
		GroupBox8.Text = "Step 10: Throwback/Pullback";
		Label13.AutoSize = true;
		((Control)Label13).Location = new Point(9, 16);
		((Control)Label13).Name = "Label13";
		((Control)Label13).Size = new Size(332, 13);
		((Control)Label13).TabIndex = 0;
		Label13.Text = "Is a throwback/pullback expected within 30-days after the breakout?";
		((ButtonBase)ThrowNRB).AutoSize = true;
		((Control)ThrowNRB).Location = new Point(420, 12);
		((Control)ThrowNRB).Name = "ThrowNRB";
		((Control)ThrowNRB).Size = new Size(39, 17);
		((Control)ThrowNRB).TabIndex = 2;
		((ButtonBase)ThrowNRB).Text = "No";
		((ButtonBase)ThrowNRB).UseVisualStyleBackColor = true;
		((ButtonBase)ThrowYRB).AutoSize = true;
		ThrowYRB.Checked = true;
		((Control)ThrowYRB).Location = new Point(371, 12);
		((Control)ThrowYRB).Name = "ThrowYRB";
		((Control)ThrowYRB).Size = new Size(43, 17);
		((Control)ThrowYRB).TabIndex = 1;
		ThrowYRB.TabStop = true;
		((ButtonBase)ThrowYRB).Text = "Yes";
		((ButtonBase)ThrowYRB).UseVisualStyleBackColor = true;
		((Control)GroupBox9).Anchor = (AnchorStyles)10;
		((Control)GroupBox9).Controls.Add((Control)(object)Label14);
		((Control)GroupBox9).Controls.Add((Control)(object)GapNRB);
		((Control)GroupBox9).Controls.Add((Control)(object)GapYRB);
		((Control)GroupBox9).Location = new Point(526, 625);
		((Control)GroupBox9).Name = "GroupBox9";
		((Control)GroupBox9).Size = new Size(480, 38);
		((Control)GroupBox9).TabIndex = 28;
		GroupBox9.TabStop = false;
		GroupBox9.Text = "Step 11: Breakout Day Gap";
		Label14.AutoSize = true;
		((Control)Label14).Location = new Point(9, 16);
		((Control)Label14).Name = "Label14";
		((Control)Label14).Size = new Size(320, 13);
		((Control)Label14).TabIndex = 0;
		Label14.Text = "Did price gap on the breakout day? If no breakout yet, answer No.";
		((ButtonBase)GapNRB).AutoSize = true;
		GapNRB.Checked = true;
		((Control)GapNRB).Location = new Point(420, 14);
		((Control)GapNRB).Name = "GapNRB";
		((Control)GapNRB).Size = new Size(39, 17);
		((Control)GapNRB).TabIndex = 2;
		GapNRB.TabStop = true;
		((ButtonBase)GapNRB).Text = "No";
		((ButtonBase)GapNRB).UseVisualStyleBackColor = true;
		((ButtonBase)GapYRB).AutoSize = true;
		((Control)GapYRB).Location = new Point(371, 14);
		((Control)GapYRB).Name = "GapYRB";
		((Control)GapYRB).Size = new Size(43, 17);
		((Control)GapYRB).TabIndex = 1;
		((ButtonBase)GapYRB).Text = "Yes";
		((ButtonBase)GapYRB).UseVisualStyleBackColor = true;
		((Control)GroupBox10).Anchor = (AnchorStyles)10;
		((Control)GroupBox10).Controls.Add((Control)(object)MarketCapButton);
		((Control)GroupBox10).Controls.Add((Control)(object)LargeRB);
		((Control)GroupBox10).Controls.Add((Control)(object)Label15);
		((Control)GroupBox10).Controls.Add((Control)(object)MediumRB);
		((Control)GroupBox10).Controls.Add((Control)(object)SmallRB);
		((Control)GroupBox10).Location = new Point(795, 305);
		((Control)GroupBox10).Name = "GroupBox10";
		((Control)GroupBox10).Size = new Size(211, 117);
		((Control)GroupBox10).TabIndex = 23;
		GroupBox10.TabStop = false;
		GroupBox10.Text = "Step 6: Market Cap";
		((Control)MarketCapButton).Anchor = (AnchorStyles)10;
		((Control)MarketCapButton).Location = new Point(162, 83);
		((Control)MarketCapButton).Name = "MarketCapButton";
		((Control)MarketCapButton).Size = new Size(43, 23);
		((Control)MarketCapButton).TabIndex = 4;
		((ButtonBase)MarketCapButton).Text = "Find";
		((ButtonBase)MarketCapButton).UseVisualStyleBackColor = true;
		((Control)MarketCapButton).Visible = false;
		((ButtonBase)LargeRB).AutoSize = true;
		((Control)LargeRB).Location = new Point(18, 86);
		((Control)LargeRB).Name = "LargeRB";
		((Control)LargeRB).Size = new Size(89, 17);
		((Control)LargeRB).TabIndex = 3;
		((ButtonBase)LargeRB).Text = "Large (> $5B)";
		((ButtonBase)LargeRB).UseVisualStyleBackColor = true;
		((Control)Label15).Location = new Point(6, 19);
		((Control)Label15).Name = "Label15";
		((Control)Label15).Size = new Size(199, 28);
		((Control)Label15).TabIndex = 0;
		Label15.Text = "Market cap is shares outstanding times breakout price. What is the market cap?";
		((ButtonBase)MediumRB).AutoSize = true;
		MediumRB.Checked = true;
		((Control)MediumRB).Location = new Point(18, 68);
		((Control)MediumRB).Name = "MediumRB";
		((Control)MediumRB).Size = new Size(99, 17);
		((Control)MediumRB).TabIndex = 2;
		MediumRB.TabStop = true;
		((ButtonBase)MediumRB).Text = "Medium ($1-5B)";
		((ButtonBase)MediumRB).UseVisualStyleBackColor = true;
		((ButtonBase)SmallRB).AutoSize = true;
		((Control)SmallRB).Location = new Point(18, 50);
		((Control)SmallRB).Name = "SmallRB";
		((Control)SmallRB).Size = new Size(87, 17);
		((Control)SmallRB).TabIndex = 1;
		((ButtonBase)SmallRB).Text = "Small (< $1B)";
		((ButtonBase)SmallRB).UseVisualStyleBackColor = true;
		((Control)Label16).Anchor = (AnchorStyles)10;
		Label16.AutoSize = true;
		((Control)Label16).Location = new Point(12, 346);
		((Control)Label16).Name = "Label16";
		((Control)Label16).Size = new Size(44, 13);
		((Control)Label16).TabIndex = 4;
		Label16.Text = "Pattern:";
		((Control)BrowseButton).Anchor = (AnchorStyles)10;
		((Control)BrowseButton).Location = new Point(126, 367);
		((Control)BrowseButton).Name = "BrowseButton";
		((Control)BrowseButton).Size = new Size(60, 23);
		((Control)BrowseButton).TabIndex = 8;
		((ButtonBase)BrowseButton).Text = "&Browse";
		((ButtonBase)BrowseButton).UseVisualStyleBackColor = true;
		((Control)GroupBox11).Anchor = (AnchorStyles)10;
		((Control)GroupBox11).Controls.Add((Control)(object)Label17);
		((Control)GroupBox11).Controls.Add((Control)(object)BkoutDRB);
		((Control)GroupBox11).Controls.Add((Control)(object)BkoutURB);
		((Control)GroupBox11).Location = new Point(526, 433);
		((Control)GroupBox11).Name = "GroupBox11";
		((Control)GroupBox11).Size = new Size(480, 38);
		((Control)GroupBox11).TabIndex = 24;
		GroupBox11.TabStop = false;
		GroupBox11.Text = "Step 7: Breakout Direction";
		Label17.AutoSize = true;
		((Control)Label17).Location = new Point(9, 16);
		((Control)Label17).Name = "Label17";
		((Control)Label17).Size = new Size(286, 13);
		((Control)Label17).TabIndex = 0;
		Label17.Text = "If no breakout yet, choose the direction you're interested in.";
		((ButtonBase)BkoutDRB).AutoSize = true;
		((Control)BkoutDRB).Location = new Point(420, 14);
		((Control)BkoutDRB).Name = "BkoutDRB";
		((Control)BkoutDRB).Size = new Size(53, 17);
		((Control)BkoutDRB).TabIndex = 2;
		((ButtonBase)BkoutDRB).Text = "Down";
		((ButtonBase)BkoutDRB).UseVisualStyleBackColor = true;
		((ButtonBase)BkoutURB).AutoSize = true;
		BkoutURB.Checked = true;
		((Control)BkoutURB).Location = new Point(371, 14);
		((Control)BkoutURB).Name = "BkoutURB";
		((Control)BkoutURB).Size = new Size(39, 17);
		((Control)BkoutURB).TabIndex = 1;
		BkoutURB.TabStop = true;
		((ButtonBase)BkoutURB).Text = "Up";
		((ButtonBase)BkoutURB).UseVisualStyleBackColor = true;
		((Control)GraphButton).Anchor = (AnchorStyles)10;
		((Control)GraphButton).Location = new Point(431, 414);
		((Control)GraphButton).Name = "GraphButton";
		((Control)GraphButton).Size = new Size(86, 23);
		((Control)GraphButton).TabIndex = 16;
		((ButtonBase)GraphButton).Text = "&Graph";
		((ButtonBase)GraphButton).UseVisualStyleBackColor = true;
		ScoreLabel.AutoSize = true;
		((Control)ScoreLabel).Font = new Font("Microsoft Sans Serif", 12f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)ScoreLabel).ForeColor = Color.Red;
		((Control)ScoreLabel).Location = new Point(64, 9);
		((Control)ScoreLabel).Name = "ScoreLabel";
		((Control)ScoreLabel).Size = new Size(19, 20);
		((Control)ScoreLabel).TabIndex = 1;
		ScoreLabel.Text = "0";
		((Control)Panel1).Anchor = (AnchorStyles)10;
		Panel1.BorderStyle = (BorderStyle)2;
		((Control)Panel1).Controls.Add((Control)(object)Label19);
		((Control)Panel1).Controls.Add((Control)(object)ScoreLabel);
		((Control)Panel1).Location = new Point(526, 668);
		((Control)Panel1).Name = "Panel1";
		((Control)Panel1).Size = new Size(101, 43);
		((Control)Panel1).TabIndex = 29;
		Label19.AutoSize = true;
		((Control)Label19).Font = new Font("Microsoft Sans Serif", 12f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label19).Location = new Point(3, 9);
		((Control)Label19).Name = "Label19";
		((Control)Label19).Size = new Size(61, 20);
		((Control)Label19).TabIndex = 0;
		Label19.Text = "Score:";
		((FileDialog)OpenFileDialog1).FileName = "OpenFileDialog1";
		((Control)Label18).Anchor = (AnchorStyles)10;
		((Control)Label18).ForeColor = Color.Red;
		((Control)Label18).Location = new Point(11, 419);
		((Control)Label18).Name = "Label18";
		((Control)Label18).Size = new Size(365, 31);
		((Control)Label18).TabIndex = 17;
		Label18.Text = "For red labels: Place the focus on  the associated field then right click a price bar (on the chart) to automatically paste a date or price into the field.";
		((Control)BkoutDayPicker).Anchor = (AnchorStyles)10;
		BkoutDayPicker.CustomFormat = "yyyy/MM/dd";
		BkoutDayPicker.Format = (DateTimePickerFormat)8;
		((Control)BkoutDayPicker).Location = new Point(431, 390);
		((Control)BkoutDayPicker).Name = "BkoutDayPicker";
		BkoutDayPicker.ShowUpDown = true;
		((Control)BkoutDayPicker).Size = new Size(120, 20);
		((Control)BkoutDayPicker).TabIndex = 15;
		BkoutDayPicker.Value = new DateTime(2017, 6, 21, 15, 29, 42, 0);
		((Control)Label21).Anchor = (AnchorStyles)10;
		Label21.AutoSize = true;
		((Control)Label21).ForeColor = Color.Red;
		((Control)Label21).Location = new Point(348, 393);
		((Control)Label21).Name = "Label21";
		((Control)Label21).Size = new Size(77, 13);
		((Control)Label21).TabIndex = 14;
		Label21.Text = "&Breakout date:";
		((Control)UsePatternButton).Anchor = (AnchorStyles)10;
		((Control)UsePatternButton).Location = new Point(186, 367);
		((Control)UsePatternButton).Name = "UsePatternButton";
		((Control)UsePatternButton).Size = new Size(156, 23);
		((Control)UsePatternButton).TabIndex = 9;
		((ButtonBase)UsePatternButton).Text = "&Get Existing Pattern's Dates";
		((ButtonBase)UsePatternButton).UseVisualStyleBackColor = true;
		((Control)ComboBox1).Anchor = (AnchorStyles)10;
		ComboBox1.DropDownStyle = (ComboBoxStyle)2;
		((ListControl)ComboBox1).FormattingEnabled = true;
		((Control)ComboBox1).Location = new Point(57, 343);
		((Control)ComboBox1).Name = "ComboBox1";
		((Control)ComboBox1).Size = new Size(285, 21);
		((Control)ComboBox1).TabIndex = 5;
		((Control)CalculateButton).Anchor = (AnchorStyles)10;
		((Control)CalculateButton).Location = new Point(873, 679);
		((Control)CalculateButton).Name = "CalculateButton";
		((Control)CalculateButton).Size = new Size(60, 23);
		((Control)CalculateButton).TabIndex = 0;
		((ButtonBase)CalculateButton).Text = "&Calculate";
		((ButtonBase)CalculateButton).UseVisualStyleBackColor = true;
		((Control)Label22).Anchor = (AnchorStyles)10;
		Label22.AutoSize = true;
		((Control)Label22).Location = new Point(8, 398);
		((Control)Label22).Name = "Label22";
		((Control)Label22).Size = new Size(48, 13);
		((Control)Label22).TabIndex = 31;
		Label22.Text = "Loading:";
		((Control)LoadingBar).Anchor = (AnchorStyles)10;
		((Control)LoadingBar).ForeColor = Color.Green;
		((Control)LoadingBar).Location = new Point(57, 397);
		((Control)LoadingBar).Name = "LoadingBar";
		((Control)LoadingBar).Size = new Size(285, 14);
		((Control)LoadingBar).TabIndex = 32;
		((Form)this).AcceptButton = (IButtonControl)(object)CalculateButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(1008, 729);
		((Control)this).Controls.Add((Control)(object)Label22);
		((Control)this).Controls.Add((Control)(object)LoadingBar);
		((Control)this).Controls.Add((Control)(object)UsePatternButton);
		((Control)this).Controls.Add((Control)(object)BkoutDayPicker);
		((Control)this).Controls.Add((Control)(object)Label21);
		((Control)this).Controls.Add((Control)(object)Label18);
		((Control)this).Controls.Add((Control)(object)Panel1);
		((Control)this).Controls.Add((Control)(object)GraphButton);
		((Control)this).Controls.Add((Control)(object)GroupBox11);
		((Control)this).Controls.Add((Control)(object)BrowseButton);
		((Control)this).Controls.Add((Control)(object)GroupBox1);
		((Control)this).Controls.Add((Control)(object)Label16);
		((Control)this).Controls.Add((Control)(object)ComboBox1);
		((Control)this).Controls.Add((Control)(object)GroupBox10);
		((Control)this).Controls.Add((Control)(object)GroupBox9);
		((Control)this).Controls.Add((Control)(object)GroupBox8);
		((Control)this).Controls.Add((Control)(object)GroupBox7);
		((Control)this).Controls.Add((Control)(object)GroupBox6);
		((Control)this).Controls.Add((Control)(object)GroupBox5);
		((Control)this).Controls.Add((Control)(object)GroupBox4);
		((Control)this).Controls.Add((Control)(object)GroupBox3);
		((Control)this).Controls.Add((Control)(object)GroupBox2);
		((Control)this).Controls.Add((Control)(object)Chart1);
		((Control)this).Controls.Add((Control)(object)CalculateButton);
		((Control)this).Controls.Add((Control)(object)ToDatePicker);
		((Control)this).Controls.Add((Control)(object)FromDatePicker);
		((Control)this).Controls.Add((Control)(object)ErrorLabel);
		((Control)this).Controls.Add((Control)(object)HelpButton1);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)SymbolTextBox);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Name = "ManualScoreForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Manual Score Form";
		((ISupportInitialize)Chart1).EndInit();
		((Control)GroupBox1).ResumeLayout(false);
		((Control)GroupBox1).PerformLayout();
		((Control)GroupBox2).ResumeLayout(false);
		((Control)GroupBox2).PerformLayout();
		((Control)GroupBox3).ResumeLayout(false);
		((Control)GroupBox3).PerformLayout();
		((Control)GroupBox4).ResumeLayout(false);
		((Control)GroupBox4).PerformLayout();
		((Control)GroupBox5).ResumeLayout(false);
		((Control)GroupBox5).PerformLayout();
		((Control)GroupBox6).ResumeLayout(false);
		((Control)GroupBox6).PerformLayout();
		((Control)GroupBox7).ResumeLayout(false);
		((Control)GroupBox7).PerformLayout();
		((Control)GroupBox8).ResumeLayout(false);
		((Control)GroupBox8).PerformLayout();
		((Control)GroupBox9).ResumeLayout(false);
		((Control)GroupBox9).PerformLayout();
		((Control)GroupBox10).ResumeLayout(false);
		((Control)GroupBox10).PerformLayout();
		((Control)GroupBox11).ResumeLayout(false);
		((Control)GroupBox11).PerformLayout();
		((Control)Panel1).ResumeLayout(false);
		((Control)Panel1).PerformLayout();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void ManualScoreForm_FormClosing(object sender, FormClosingEventArgs e)
	{
		MySettingsProperty.Settings.ManualScoreLocation = ((Form)this).Location;
		MySettingsProperty.Settings.ManualScoreSize = ((Form)this).Size;
		((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
	}

	private void ManualScoreForm_FormClosed(object sender, FormClosedEventArgs e)
	{
		try
		{
			if (CurrentAnnotation != null)
			{
				((Collection<Annotation>)(object)Chart1.Annotations).Remove((Annotation)(object)CurrentAnnotation);
				((ChartElement)CurrentAnnotation).Dispose();
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		CurrentAnnotation = null;
		Exiting = true;
		try
		{
			GlobalForm.OpenPath = lsOpenPath;
			GlobalForm.MSFCombo = ComboBox1.SelectedIndex;
			if (GlobalForm.MSFCombo != -1)
			{
				ComboBox1.SelectedIndex = Conversions.ToInteger(Interaction.IIf(GlobalForm.MSFCombo == 2, (object)1, (object)2));
			}
			Array.Copy(lsPatternArray, GlobalForm.PatternList, 124);
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			ProjectData.ClearProjectError();
		}
		GlobalForm.ChartVolume = lsChartVolume;
		LockFlag = false;
	}

	private void ManualScoreForm_Load(object sender, EventArgs e)
	{
		//IL_0051: Unknown result type (might be due to invalid IL or missing references)
		//IL_0056: Unknown result type (might be due to invalid IL or missing references)
		//IL_0061: Unknown result type (might be due to invalid IL or missing references)
		//IL_006c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0077: Unknown result type (might be due to invalid IL or missing references)
		//IL_007e: Unknown result type (might be due to invalid IL or missing references)
		//IL_008f: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b1: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00d3: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e4: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f5: Unknown result type (might be due to invalid IL or missing references)
		//IL_0106: Unknown result type (might be due to invalid IL or missing references)
		//IL_0117: Unknown result type (might be due to invalid IL or missing references)
		//IL_0128: Unknown result type (might be due to invalid IL or missing references)
		//IL_0139: Unknown result type (might be due to invalid IL or missing references)
		//IL_014a: Unknown result type (might be due to invalid IL or missing references)
		//IL_015b: Unknown result type (might be due to invalid IL or missing references)
		//IL_016c: Unknown result type (might be due to invalid IL or missing references)
		//IL_017d: Unknown result type (might be due to invalid IL or missing references)
		//IL_018e: Unknown result type (might be due to invalid IL or missing references)
		//IL_019f: Unknown result type (might be due to invalid IL or missing references)
		//IL_01b0: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c1: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d2: Unknown result type (might be due to invalid IL or missing references)
		//IL_01e3: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f4: Unknown result type (might be due to invalid IL or missing references)
		//IL_0205: Unknown result type (might be due to invalid IL or missing references)
		//IL_002a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0034: Expected O, but got Unknown
		LockFlag = false;
		GlobalForm.SetupWindow((Form)(object)this, MySettingsProperty.Settings.ManualScoreLocation, MySettingsProperty.Settings.ManualScoreSize);
		if (CurrentAnnotation == null)
		{
			CurrentAnnotation = new CalloutAnnotation();
		}
		((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)CurrentAnnotation);
		Exiting = false;
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)BkoutDayPicker, "Enter the date price breaks out of the chart pattern.");
		val.SetToolTip((Control)(object)BkoutPriceTextBox, "What is the breakout price, if known (or guess)?");
		val.SetToolTip((Control)(object)BkoutVolButton, "Calculate if the breakout volume is heavy or light.");
		val.SetToolTip((Control)(object)BrowseButton, "Click to locate a security to score.");
		val.SetToolTip((Control)(object)CalculateButton, "Click to remove the blue highlights and calculate a score.");
		val.SetToolTip((Control)(object)ComboBox1, "Select a chart pattern to score from the list.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)FindHeightButton, "Enter the chart pattern's highest peak, lowest valley, and breakout prices to calculate the height.");
		val.SetToolTip((Control)(object)FromDatePicker, "Enter the starting date of the chart pattern.");
		val.SetToolTip((Control)(object)GraphButton, "Click to redraw the chart.");
		val.SetToolTip((Control)(object)HelpButton1, "Get help for this form.");
		val.SetToolTip((Control)(object)HHTextBox, "Enter the highest high in the chart pattern.");
		val.SetToolTip((Control)(object)HighThirdRB, "Is the breakout price within a third of the yearly high?");
		val.SetToolTip((Control)(object)LLTextBox, "Enter the lowest low in the chart pattern.");
		val.SetToolTip((Control)(object)LowThirdRB, "Is the breakout price within a third of the yearly low?");
		val.SetToolTip((Control)(object)LRVolButton, "Uses linear regression to automatically determine the volume trend.");
		val.SetToolTip((Control)(object)MarketCapButton, "Find the market cap automatically. Requires an internet connection.");
		val.SetToolTip((Control)(object)MiddleThirdRB, "Is the breakout price in the middle third of the yearly price range?");
		val.SetToolTip((Control)(object)ShortRB, "The breakout price divided by the height compared to the median height for this chart pattern. Click 'Find 1, 2, 4' to calculate.");
		val.SetToolTip((Control)(object)SymbolTextBox, "Enter a symbol, if desired, to score, then click Graph.");
		val.SetToolTip((Control)(object)TallRB, "The breakout price divided by the height compared to the median height for this chart pattern. Click 'Find 1, 2, 4' to calculate.");
		val.SetToolTip((Control)(object)ToDatePicker, "Enter the ending date of the chart pattern.");
		val.SetToolTip((Control)(object)TrendStartButton, "Automatically finds the trend start. Needs the pattern's high and low price.");
		val.SetToolTip((Control)(object)UsePatternButton, "For an automatically found chart pattern, this button uses the pattern's information to fill in the start and end dates.");
		val.SetToolTip((Control)(object)YearRangeButton, "Automatically find the yearly price range. Needs Step 1 completed.");
		lsOpenPath = GlobalForm.OpenPath;
		Array.Copy(GlobalForm.PatternList, lsPatternArray, 124);
		Array.Clear(GlobalForm.PatternList, 0, 124);
		GlobalForm.ShowAllPatterns = true;
		GlobalForm.FirstPoint = default(Point);
		GlobalForm.LinesList.RemoveAll(StubBoolean);
		GlobalForm.SelectChartType(Chart1);
		lsChartVolume = GlobalForm.ChartVolume;
		GlobalForm.ChartVolume = true;
		ComboBox1.Items.Add((object)"Big M");
		ComboBox1.Items.Add((object)"Big W");
		ComboBox1.Items.Add((object)"Broadening bottom");
		ComboBox1.Items.Add((object)"Broadening formation, right-angled & ascending");
		ComboBox1.Items.Add((object)"Broadening formation, right-angled & descending");
		ComboBox1.Items.Add((object)"Broadening top");
		ComboBox1.Items.Add((object)"Broadening wedge, ascending");
		ComboBox1.Items.Add((object)"Broadening wedge, descending");
		ComboBox1.Items.Add((object)"Bump-and-run reversal, bottom");
		ComboBox1.Items.Add((object)"Bump-and-run reversal, top");
		ComboBox1.Items.Add((object)"Cup with handle");
		ComboBox1.Items.Add((object)"Diamond bottom");
		ComboBox1.Items.Add((object)"Diamond top");
		ComboBox1.Items.Add((object)"Double bottom, Adam & Adam");
		ComboBox1.Items.Add((object)"Double bottom, Adam & Eve");
		ComboBox1.Items.Add((object)"Double bottom, Eve & Adam");
		ComboBox1.Items.Add((object)"Double bottom, Eve & Eve");
		ComboBox1.Items.Add((object)"Double bottoms (all Types)");
		ComboBox1.Items.Add((object)"Double top, Adam & Adam");
		ComboBox1.Items.Add((object)"Double top, Adam & Eve");
		ComboBox1.Items.Add((object)"Double top, Eve & Adam");
		ComboBox1.Items.Add((object)"Double top, Eve & Eve");
		ComboBox1.Items.Add((object)"Double tops (all Types)");
		ComboBox1.Items.Add((object)"Falling wedge");
		ComboBox1.Items.Add((object)"Head-and-shoulders bottom");
		ComboBox1.Items.Add((object)"Head-and-shoulders complex bottom");
		ComboBox1.Items.Add((object)"Head-and-shoulders complex top");
		ComboBox1.Items.Add((object)"Head-and-shoulders top");
		ComboBox1.Items.Add((object)"Rectangle bottom");
		ComboBox1.Items.Add((object)"Rectangle top");
		ComboBox1.Items.Add((object)"Rising wedge");
		ComboBox1.Items.Add((object)"Roof");
		ComboBox1.Items.Add((object)"Roof, inverted");
		ComboBox1.Items.Add((object)"Rounding bottom");
		ComboBox1.Items.Add((object)"Rounding top");
		ComboBox1.Items.Add((object)"Scallop, ascending");
		ComboBox1.Items.Add((object)"Scallop, ascending And inverted");
		ComboBox1.Items.Add((object)"Scallop, descending");
		ComboBox1.Items.Add((object)"Scallop, descending And inverted");
		ComboBox1.Items.Add((object)"Three falling peaks");
		ComboBox1.Items.Add((object)"Three rising valleys");
		ComboBox1.Items.Add((object)"Triangle, ascending");
		ComboBox1.Items.Add((object)"Triangle, descending");
		ComboBox1.Items.Add((object)"Triangle, symmetrical");
		ComboBox1.Items.Add((object)"Triple bottom");
		ComboBox1.Items.Add((object)"Triple top");
		ComboBox1.Items.Add((object)"Ugly double bottom");
		ComboBox1.SelectedIndex = Conversions.ToInteger(Interaction.IIf(GlobalForm.MSFCombo == -1, (object)1, (object)GlobalForm.MSFCombo));
		SymbolTextBox_TextChanged(RuntimeHelpers.GetObjectValue(sender), e);
	}

	private void ManualScoreForm_Activated(object sender, EventArgs e)
	{
		//IL_009d: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			if (!LockFlag)
			{
				LockFlag = true;
				((Control)this).Refresh();
				if (MyProject.Forms.Mainform.ListBox1.SelectedIndex == -1)
				{
					return;
				}
				SymbolPlusExtension = MyProject.Forms.Mainform.ListBox1.SelectedItems[0].ToString();
				string symbolPlusExtension = SymbolPlusExtension;
				ProgressBar ProgBar = LoadingBar;
				Label ErrorLabel = this.ErrorLabel;
				bool num = GlobalForm.LoadFile(symbolPlusExtension, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
				this.ErrorLabel = ErrorLabel;
				LoadingBar = ProgBar;
				if (num)
				{
					return;
				}
				if (GlobalForm.IntradayData)
				{
					MessageBox.Show("Intraday data is not supported by the scoring system. Please exit the form and pick another symbol.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
					return;
				}
				GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
				GlobalForm.SelectChartType(Chart1);
				if (GlobalForm.IntradayData)
				{
					BkoutDayPicker.CustomFormat = "yyyy-MM-dd HH:mm";
					if ((DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MaxDate) <= 0))
					{
						if (GlobalForm.HLCRange - 262 > 0)
						{
							FromDatePicker.Value = GlobalForm.FindDate(GlobalForm.nDT[0, GlobalForm.HLCRange - 262]);
						}
						else
						{
							FromDatePicker.Value = GlobalForm.FindDate(GlobalForm.nDT[0, 0]);
						}
					}
					else
					{
						FromDatePicker.Value = DateAndTime.Now;
					}
					GlobalForm.ChartStart = FromDatePicker.Value;
				}
				else
				{
					BkoutDayPicker.CustomFormat = "yyyy-MM-dd";
					FromDatePicker.Value = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)0, -1.0, DateAndTime.Now));
					GlobalForm.ChartStart = FromDatePicker.Value.Date;
				}
				ToDatePicker.Value = GlobalForm.FindDate(DateAndTime.Now);
				BkoutDayPicker.Value = ToDatePicker.Value;
				GlobalForm.ChartEnd = ToDatePicker.Value;
				TrendStart = DateAndTime.Now.Date;
				MSCheckDates(FromDatePicker, ToDatePicker, BkoutDayPicker, GlobalForm.Quiet);
				GlobalForm.SetupDateIndexes(GlobalForm.ChartStart, GlobalForm.ChartEnd);
				AdjustDates(Quiet: false);
				bool showCandles = GlobalForm.ShowCandles;
				GlobalForm.ShowCandles = false;
				FindPatterns.EnterFindPatterns(GlobalForm.ChartStart, GlobalForm.ChartEnd, null, ref StopPressed, 3);
				GlobalForm.ShowStock(Chart1, GlobalForm.ChartStart, GlobalForm.ChartEnd, VolumeFlag: true, MAFlag: false);
				GlobalForm.ShowCandles = showCandles;
				if (GlobalForm.PatternCount != 0)
				{
					((Control)UsePatternButton).Enabled = true;
				}
				else
				{
					((Control)UsePatternButton).Enabled = false;
				}
				((Form)this).Text = "Manual Score Form: " + SymbolPlusExtension;
				int num2 = Strings.InStrRev(SymbolPlusExtension, ".", -1, (CompareMethod)0);
				if (num2 != 0)
				{
					SymbolTextBox.Text = Strings.Left(SymbolPlusExtension, num2 - 1);
				}
			}
			else
			{
				((Control)this).Refresh();
			}
		}
	}

	private void AddShowScores()
	{
		int num = 0;
		checked
		{
			num += Scores.sTrendStart;
			num += Scores.sYrlyRange;
			num += Scores.sMarketCap;
			num += Scores.sFlatBase;
			num += Scores.sHCR;
			num += Scores.sTall;
			num += Scores.sVolumeTrend;
			num += Scores.sBkoutVol;
			num += Scores.sThrowPull;
			num += Scores.sBkoutGap;
			ScoreLabel.Text = num.ToString();
		}
	}

	private void AdjustDates(bool Quiet)
	{
		checked
		{
			if (GlobalForm.IntradayData)
			{
				GlobalForm.ChartEnd = DateTime.MinValue;
				for (int i = GlobalForm.HLCRange; i >= 0; i += -1)
				{
					if ((DateTime.Compare(GlobalForm.ChartEnd, DateTime.MinValue) == 0) & (DateTime.Compare(GlobalForm.nDT[0, i], ToDatePicker.Value) <= 0))
					{
						if (i + 30 <= GlobalForm.HLCRange)
						{
							GlobalForm.ChartEnd = GlobalForm.nDT[0, i + 30];
						}
						else
						{
							GlobalForm.ChartEnd = GlobalForm.nDT[0, GlobalForm.HLCRange];
						}
					}
					if (DateTime.Compare(GlobalForm.nDT[0, i], FromDatePicker.Value) <= 0)
					{
						if (i - 262 > 0)
						{
							GlobalForm.ChartStart = GlobalForm.nDT[0, i - 262];
						}
						else
						{
							GlobalForm.ChartStart = GlobalForm.nDT[0, 0];
						}
						break;
					}
				}
			}
			else
			{
				GlobalForm.ChartStart = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)0, -1.0, FromDatePicker.Value)).Date;
				GlobalForm.ChartEnd = GlobalForm.FindDate(DateAndTime.DateAdd((DateInterval)4, 30.0, ToDatePicker.Value)).Date;
			}
			MSCheckDates(FromDatePicker, ToDatePicker, BkoutDayPicker, Quiet);
		}
	}

	private void AssessSelections()
	{
		if (TrendShortRB.Checked)
		{
			Scores.TrendStart = 1;
		}
		else if (TrendIntermediateRB.Checked)
		{
			Scores.TrendStart = 2;
		}
		else
		{
			Scores.TrendStart = 3;
		}
		if (HighThirdRB.Checked)
		{
			Scores.YrlyRange = 3;
		}
		else if (MiddleThirdRB.Checked)
		{
			Scores.YrlyRange = 2;
		}
		else
		{
			Scores.YrlyRange = 1;
		}
		if (LargeRB.Checked)
		{
			Scores.MarketCap = 3;
		}
		else if (MediumRB.Checked)
		{
			Scores.MarketCap = 2;
		}
		else
		{
			Scores.MarketCap = 1;
		}
		Scores.bFlatBase = FlatBaseYRB.Checked;
		Scores.bHCR = HCRYRB.Checked;
		Scores.bTall = TallRB.Checked;
		Scores.VolumeTrend = Conversions.ToInteger(Interaction.IIf(LRVolDRB.Checked, (object)(-1), (object)1));
		Scores.BkoutVol = Conversions.ToInteger(Interaction.IIf(BreakVolYRB.Checked, (object)1, (object)2));
		Scores.bThrowPull = ThrowYRB.Checked;
		Scores.bBkoutGap = GapYRB.Checked;
	}

	private void BkoutDayPicker_GotFocus(object sender, EventArgs e)
	{
		LastFocus = 3;
	}

	private void BkoutPriceTextBox_GotFocus(object sender, EventArgs e)
	{
		LastFocus = 6;
	}

	private void BkoutVolButton_Click(object sender, EventArgs e)
	{
		//IL_021e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0287: Unknown result type (might be due to invalid IL or missing references)
		//IL_0273: Unknown result type (might be due to invalid IL or missing references)
		long num = 0L;
		long num2 = 0L;
		int num3 = -1;
		checked
		{
			DateTime t = default(DateTime);
			if (GlobalForm.IntradayData)
			{
				for (int i = GlobalForm.HLCRange; i >= 0; i += -1)
				{
					if (DateTime.Compare(GlobalForm.nDT[0, i], BkoutDayPicker.Value) <= 0)
					{
						t = ((i < 65) ? GlobalForm.nDT[0, 0] : GlobalForm.nDT[0, i - 65]);
						break;
					}
				}
			}
			else
			{
				t = DateAndTime.DateAdd((DateInterval)2, -3.0, BkoutDayPicker.Value.Date);
			}
			for (int j = GlobalForm.HLCRange; j >= 0; j += -1)
			{
				if (GlobalForm.IntradayData)
				{
					if (DateTime.Compare(GlobalForm.nDT[0, j], BkoutDayPicker.Value) == 0)
					{
						num3 = j;
					}
					if ((DateTime.Compare(GlobalForm.nDT[0, j], BkoutDayPicker.Value) < 0) & (DateTime.Compare(GlobalForm.nDT[0, j], t) >= 0))
					{
						num2++;
						num += Convert.ToInt64(GlobalForm.nHLC[4, j]);
					}
					else if (DateTime.Compare(GlobalForm.nDT[0, j], t) < 0)
					{
						break;
					}
				}
				else
				{
					if (DateTime.Compare(GlobalForm.nDT[0, j], BkoutDayPicker.Value.Date) == 0)
					{
						num3 = j;
					}
					if ((DateTime.Compare(GlobalForm.nDT[0, j].Date, BkoutDayPicker.Value.Date) < 0) & (DateTime.Compare(GlobalForm.nDT[0, j].Date, t.Date) >= 0))
					{
						num2++;
						num += Convert.ToInt64(GlobalForm.nHLC[4, j]);
					}
					else if (DateTime.Compare(GlobalForm.nDT[0, j].Date, t.Date) < 0)
					{
						break;
					}
				}
			}
			if (num3 == -1)
			{
				MessageBox.Show("Breakout date not found. Please check it.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			}
			else if (num2 > 0)
			{
				if (Convert.ToDouble(GlobalForm.nHLC[4, num3]) >= 1.25 * (double)num / (double)num2)
				{
					BreakVolYRB.Checked = true;
				}
				else
				{
					BreakVolNRB.Checked = true;
				}
				MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
			else
			{
				MessageBox.Show("Not enough data to make calculation.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			}
		}
	}

	private void BrowseButton_Click(object sender, EventArgs e)
	{
		//IL_0000: Unknown result type (might be due to invalid IL or missing references)
		//IL_0006: Expected O, but got Unknown
		//IL_003a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0040: Invalid comparison between Unknown and I4
		OpenFileDialog val = new OpenFileDialog();
		((FileDialog)val).InitialDirectory = GlobalForm.OpenPath;
		((FileDialog)val).Filter = "csv files (*.csv)|*.csv|txt files (*.txt)|*.txt";
		((FileDialog)val).FilterIndex = 1;
		((FileDialog)val).Title = "Select the file to be scored.";
		((FileDialog)val).FileName = "";
		if ((int)((CommonDialog)val).ShowDialog() != 1)
		{
			return;
		}
		string fileName = ((FileDialog)val).FileName;
		int num = Strings.InStrRev(fileName, "\\", -1, (CompareMethod)0);
		if (num == 0)
		{
			return;
		}
		checked
		{
			GlobalForm.OpenPath = Strings.Left(fileName, num - 1);
			SymbolPlusExtension = Strings.Right(fileName, fileName.Length - num);
			num = Strings.InStrRev(SymbolPlusExtension, ".", -1, (CompareMethod)0);
			if (num == 0)
			{
				return;
			}
			SymbolTextBox.Text = Strings.Left(SymbolPlusExtension, num - 1);
			this.ErrorLabel.Text = "Loading file. If slow, then file is too long (2 years works well).";
			string symbolPlusExtension = SymbolPlusExtension;
			ProgressBar ProgBar = LoadingBar;
			Label ErrorLabel = this.ErrorLabel;
			bool num2 = GlobalForm.LoadFile(symbolPlusExtension, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
			this.ErrorLabel = ErrorLabel;
			LoadingBar = ProgBar;
			if (!num2)
			{
				GlobalForm.FormatPickers(FromDatePicker, ToDatePicker);
				GlobalForm.SelectChartType(Chart1);
				if (GlobalForm.IntradayData)
				{
					BkoutDayPicker.CustomFormat = "yyyy-MM-dd HH:mm";
				}
				else
				{
					BkoutDayPicker.CustomFormat = "yyyy-MM-dd";
				}
				GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
				this.ErrorLabel.Text = "";
			}
		}
	}

	private void CalculateButton_Click(object sender, EventArgs e)
	{
		//IL_00c3: Unknown result type (might be due to invalid IL or missing references)
		CalculateScore();
		((Control)GroupBox1).ForeColor = Color.Black;
		((Control)GroupBox2).ForeColor = Color.Black;
		((Control)GroupBox3).ForeColor = Color.Black;
		((Control)GroupBox4).ForeColor = Color.Black;
		((Control)GroupBox5).ForeColor = Color.Black;
		((Control)GroupBox6).ForeColor = Color.Black;
		((Control)GroupBox7).ForeColor = Color.Black;
		((Control)GroupBox8).ForeColor = Color.Black;
		((Control)GroupBox9).ForeColor = Color.Black;
		((Control)GroupBox10).ForeColor = Color.Black;
		((Control)GroupBox11).ForeColor = Color.Black;
		MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void CalcHeight(decimal PatternTop, decimal PatternBottom, decimal BkoutPrice)
	{
		int num = Conversions.ToInteger(Interaction.IIf(BkoutURB.Checked, (object)1, (object)(-1)));
		decimal d = default(decimal);
		switch (ComboBox1.Text)
		{
		case "Big M":
			d = 0.1163m;
			break;
		case "Big W":
			d = 0.115m;
			break;
		case "Broadening bottom":
			d = ((num != 1) ? 0.1442m : 0.1253m);
			break;
		case "Broadening formation, right-angled & ascending":
			d = ((num != 1) ? 0.1279m : 0.1132m);
			break;
		case "Broadening formation, right-angled & descending":
			d = ((num != 1) ? 0.119m : 0.1177m);
			break;
		case "Broadening top":
			d = ((num != 1) ? 0.1181m : 0.116m);
			break;
		case "Broadening wedge, ascending":
			d = ((num != 1) ? 0.1943m : 0.1686m);
			break;
		case "Broadening wedge, descending":
			d = ((num != 1) ? 0.1537m : 0.1784m);
			break;
		case "Bump-and-run reversal, bottom":
			d = 0.3587m;
			break;
		case "Bump-and-run reversal, top":
			d = 0.4348m;
			break;
		case "Cup with handle":
			d = 0.2741m;
			break;
		case "Diamond bottom":
			d = ((num != 1) ? 0.1253m : 0.1261m);
			break;
		case "Diamond top":
			d = ((num != 1) ? 0.1052m : 0.1176m);
			break;
		case "Double bottom, Adam & Adam":
			d = 0.1428m;
			break;
		case "Double bottom, Adam & Eve":
			d = 0.1611m;
			break;
		case "Double bottom, Eve & Adam":
			d = 0.1473m;
			break;
		case "Double bottom, Eve & Eve":
			d = 0.1542m;
			break;
		case "Double bottoms (all Types)":
			d = 0.1414m;
			break;
		case "Double top, Adam & Adam":
			d = 0.13m;
			break;
		case "Double top, Adam & Eve":
			d = 0.1471m;
			break;
		case "Double top, Eve & Adam":
			d = 0.1441m;
			break;
		case "Double top, Eve & Eve":
			d = 0.1421m;
			break;
		case "Double tops (all Types)":
			d = 0.1285m;
			break;
		case "Falling wedge":
			d = ((num != 1) ? 0.16m : 0.1596m);
			break;
		case "Head-and-shoulders bottom":
			d = 0.142m;
			break;
		case "Head-and-shoulders top":
			d = 0.1325m;
			break;
		case "Head-and-shoulders complex bottom":
			d = 0.177m;
			break;
		case "Head-and-shoulders complex top":
			d = 0.1603m;
			break;
		case "Rectangle bottom":
			d = ((num != 1) ? 0.105m : 0.0906m);
			break;
		case "Rectangle top":
			d = ((num != 1) ? 0.0809m : 0.0908m);
			break;
		case "Rising wedge":
			d = ((num != 1) ? 0.15m : 0.152m);
			break;
		case "Roof":
			d = ((num != 1) ? 0.0888m : 0.0812m);
			break;
		case "Roof, inverted":
			d = ((num != 1) ? 0.0933m : 0.0884m);
			break;
		case "Rounding bottom":
			d = 0.3158m;
			break;
		case "Rounding top":
			d = 0.3102m;
			break;
		case "Scallop, ascending":
			d = ((num != 1) ? 0.2147m : 0.1977m);
			break;
		case "Scallop, ascending And inverted":
			d = 0.2043m;
			break;
		case "Scallop, descending":
			d = ((num != 1) ? 0.2227m : 0.24m);
			break;
		case "Scallop, descending And inverted":
			d = 0.2046m;
			break;
		case "Three falling peaks":
			d = 0.235m;
			break;
		case "Three rising valleys":
			d = 0.238m;
			break;
		case "Triangle, ascending":
			d = ((num != 1) ? 0.0938m : 0.0978m);
			break;
		case "Triangle, descending":
			d = ((num != 1) ? 0.1176m : 0.1033m);
			break;
		case "Triangle, symmetrical":
			d = ((num != 1) ? 0.1155m : 0.1111m);
			break;
		case "Triple bottom":
			d = 0.1237m;
			break;
		case "Triple top":
			d = 0.1293m;
			break;
		case "Ugly double bottom":
			d = 0.1252m;
			break;
		}
		if (decimal.Compare(BkoutPrice, 0m) > 0)
		{
			decimal d2 = decimal.Divide(decimal.Subtract(PatternTop, PatternBottom), BkoutPrice);
			Scores.bTall = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(d2, d) > 0, (object)true, (object)false));
		}
		else
		{
			Scores.bTall = true;
		}
	}

	private void CalculateScore()
	{
		int num = Conversions.ToInteger(Interaction.IIf(BkoutURB.Checked, (object)1, (object)(-1)));
		AssessSelections();
		if (Scores.MarketCap == 1)
		{
			Scores.sMarketCap = 1;
		}
		else if (Scores.MarketCap == 2)
		{
			Scores.sMarketCap = 0;
		}
		else
		{
			Scores.sMarketCap = -1;
		}
		Scores.sFlatBase = Conversions.ToInteger(Interaction.IIf(Scores.bFlatBase, (object)1, (object)(-1)));
		Scores.sHCR = Conversions.ToInteger(Interaction.IIf(Scores.bHCR, (object)(-1), (object)1));
		switch (ComboBox1.Text)
		{
		case "Big M":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = 0;
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)0));
			break;
		case "Big W":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 2, (object)(-1), (object)1));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)1));
			break;
		case "Broadening bottom":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
				if (Scores.YrlyRange == 3)
				{
					Scores.sYrlyRange = -1;
				}
				else if (Scores.YrlyRange == 2)
				{
					Scores.sYrlyRange = 0;
				}
				else
				{
					Scores.sYrlyRange = 1;
				}
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
				break;
			}
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = -1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = 0;
			}
			else
			{
				Scores.sTrendStart = 1;
			}
			if (Scores.YrlyRange == 3)
			{
				Scores.sYrlyRange = 0;
			}
			else if (Scores.YrlyRange == 2)
			{
				Scores.sYrlyRange = -1;
			}
			else
			{
				Scores.sYrlyRange = 1;
			}
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)(-1), (object)1));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)0));
			break;
		case "Broadening formation, right-angled & ascending":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 2, (object)1, (object)(-1)));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)(-1), (object)1));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)1));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
				break;
			}
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = -1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = 0;
			}
			else
			{
				Scores.sTrendStart = 1;
			}
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)1, (object)0));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			break;
		case "Broadening formation, right-angled & descending":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)(-1), (object)1));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			}
			else
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)1, (object)(-1)));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)1, (object)(-1)));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			}
			break;
		case "Broadening top":
			if (num == 1)
			{
				if (Scores.MarketCap == 1)
				{
					Scores.sMarketCap = 1;
				}
				else if (Scores.MarketCap == 2)
				{
					Scores.sMarketCap = -1;
				}
				else
				{
					Scores.sMarketCap = 1;
				}
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)0, (object)(-1)));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)(-1), (object)1));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)0));
			}
			else
			{
				if (Scores.MarketCap == 1)
				{
					Scores.sMarketCap = 1;
				}
				else if (Scores.MarketCap == 2)
				{
					Scores.sMarketCap = 1;
				}
				else
				{
					Scores.sMarketCap = -1;
				}
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)0));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)0, (object)0));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			}
			break;
		case "Broadening wedge, ascending":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 2, (object)(-1), (object)1));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)(-1), (object)1));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)0, (object)1));
			}
			else
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)0));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			}
			break;
		case "Broadening wedge, descending":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)0));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			}
			else
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			}
			break;
		case "Bump-and-run reversal, bottom":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 2, (object)1, (object)(-1)));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			break;
		case "Bump-and-run reversal, top":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 2, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)0));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			break;
		case "Cup with handle":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
			if (Scores.YrlyRange == 3)
			{
				Scores.sYrlyRange = 0;
			}
			else if (Scores.YrlyRange == 2)
			{
				Scores.sYrlyRange = -1;
			}
			else
			{
				Scores.sYrlyRange = 1;
			}
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)1));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			break;
		case "Diamond bottom":
			if (num == 1)
			{
				if (Scores.TrendStart == 3)
				{
					Scores.sTrendStart = -1;
				}
				else if (Scores.TrendStart == 2)
				{
					Scores.sTrendStart = 1;
				}
				else
				{
					Scores.sTrendStart = 0;
				}
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)0));
			}
			else
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 2, (object)1, (object)(-1)));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)0));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)(-1), (object)1));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			}
			break;
		case "Diamond top":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)(-1), (object)1));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)1));
				break;
			}
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = -1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = 1;
			}
			else
			{
				Scores.sTrendStart = 0;
			}
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)0, (object)0));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)(-1), (object)0));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)1));
			break;
		case "Double bottom, Adam & Adam":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)1));
			break;
		case "Double bottom, Adam & Eve":
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = 0;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = -1;
			}
			else
			{
				Scores.sTrendStart = 1;
			}
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 2, (object)(-1), (object)1));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)0, (object)0));
			break;
		case "Double bottom, Eve & Adam":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 2, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)0));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)1));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)(-1), (object)1));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			break;
		case "Double bottom, Eve & Eve":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 2, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)(-1), (object)1));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)(-1), (object)1));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			break;
		case "Double bottoms (all Types)":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
			if (Scores.YrlyRange == 3)
			{
				Scores.sYrlyRange = -1;
			}
			else if (Scores.YrlyRange == 2)
			{
				Scores.sYrlyRange = 0;
			}
			else
			{
				Scores.sYrlyRange = 1;
			}
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)1));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)0));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			break;
		case "Double top, Adam & Adam":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)(-1), (object)0));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)1));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)0, (object)0));
			break;
		case "Double top, Adam & Eve":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
			if (Scores.YrlyRange == 3)
			{
				Scores.sYrlyRange = 0;
			}
			else if (Scores.YrlyRange == 2)
			{
				Scores.sYrlyRange = 1;
			}
			else
			{
				Scores.sYrlyRange = -1;
			}
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)0));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)1));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)0));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)0, (object)1));
			break;
		case "Double top, Eve & Adam":
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = -1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = 0;
			}
			else
			{
				Scores.sTrendStart = 1;
			}
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)(-1), (object)0));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)0));
			break;
		case "Double top, Eve & Eve":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
			if (Scores.YrlyRange == 3)
			{
				Scores.sYrlyRange = -1;
			}
			else if (Scores.YrlyRange == 2)
			{
				Scores.sYrlyRange = 0;
			}
			else
			{
				Scores.sYrlyRange = 1;
			}
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)(-1), (object)1));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)0));
			break;
		case "Double tops (all Types)":
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = -1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = 0;
			}
			else
			{
				Scores.sTrendStart = 1;
			}
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)0));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)0));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)0, (object)0));
			break;
		case "Falling wedge":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			}
			else
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)1, (object)(-1)));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)0, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)0, (object)(-1)));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			}
			break;
		case "Head-and-shoulders bottom":
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = -1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = 0;
			}
			else
			{
				Scores.sTrendStart = 1;
			}
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)0, (object)0));
			break;
		case "Head-and-shoulders top":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
			if (Scores.YrlyRange == 3)
			{
				Scores.sYrlyRange = -1;
			}
			else if (Scores.YrlyRange == 2)
			{
				Scores.sYrlyRange = 1;
			}
			else
			{
				Scores.sYrlyRange = 0;
			}
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)0));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)0, (object)0));
			break;
		case "Head-and-shoulders complex bottom":
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = -1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = 1;
			}
			else
			{
				Scores.sTrendStart = 0;
			}
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 2, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)0));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)1));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)0, (object)0));
			break;
		case "Head-and-shoulders complex top":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)0, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			break;
		case "Rectangle bottom":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)0));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
				break;
			}
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = 1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = -1;
			}
			else
			{
				Scores.sTrendStart = 0;
			}
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)(-1), (object)1));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			break;
		case "Rectangle top":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)0));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)0, (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
				break;
			}
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = 1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = 0;
			}
			else
			{
				Scores.sTrendStart = -1;
			}
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)0, (object)0));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)0, (object)0));
			break;
		case "Rising wedge":
			if (num == 1)
			{
				if (Scores.TrendStart == 3)
				{
					Scores.sTrendStart = 1;
				}
				else if (Scores.TrendStart == 2)
				{
					Scores.sTrendStart = 0;
				}
				else
				{
					Scores.sTrendStart = -1;
				}
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)(-1), (object)0));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)(-1), (object)0));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			}
			else
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)0));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)1));
			}
			break;
		case "Roof":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)1, (object)0));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)0, (object)0));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)1));
				break;
			}
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = -1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = 0;
			}
			else
			{
				Scores.sTrendStart = 1;
			}
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)1));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)1));
			break;
		case "Roof, inverted":
			if (num == 1)
			{
				if (Scores.TrendStart == 3)
				{
					Scores.sTrendStart = -1;
				}
				else if (Scores.TrendStart == 2)
				{
					Scores.sTrendStart = 1;
				}
				else
				{
					Scores.sTrendStart = 0;
				}
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)(-1), (object)1));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)0, (object)(-1)));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
				break;
			}
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = -1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = 1;
			}
			else
			{
				Scores.sTrendStart = 0;
			}
			if (Scores.YrlyRange == 3)
			{
				Scores.sYrlyRange = 0;
			}
			else if (Scores.YrlyRange == 2)
			{
				Scores.sYrlyRange = 1;
			}
			else
			{
				Scores.sYrlyRange = -1;
			}
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			break;
		case "Rounding bottom":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)0, (object)0));
			break;
		case "Rounding top":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			break;
		case "Scallop, ascending":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)0, (object)1));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 2, (object)(-1), (object)1));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			}
			else
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 2, (object)(-1), (object)1));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)0));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)0, (object)0));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			}
			break;
		case "Scallop, ascending And inverted":
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = -1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = 1;
			}
			else
			{
				Scores.sTrendStart = 0;
			}
			if (Scores.YrlyRange == 3)
			{
				Scores.sYrlyRange = 0;
			}
			else if (Scores.YrlyRange == 2)
			{
				Scores.sYrlyRange = -1;
			}
			else
			{
				Scores.sYrlyRange = 1;
			}
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)0, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			break;
		case "Scallop, descending":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)1, (object)1));
				if (Scores.YrlyRange == 3)
				{
					Scores.sYrlyRange = -1;
				}
				else if (Scores.YrlyRange == 2)
				{
					Scores.sYrlyRange = 0;
				}
				else
				{
					Scores.sYrlyRange = 1;
				}
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)1, (object)(-1)));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)0));
			}
			else
			{
				if (Scores.TrendStart == 3)
				{
					Scores.sTrendStart = 1;
				}
				else if (Scores.TrendStart == 2)
				{
					Scores.sTrendStart = -1;
				}
				else
				{
					Scores.sTrendStart = 0;
				}
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)(-1), (object)1));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)0, (object)0));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			}
			break;
		case "Scallop, descending And inverted":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)0));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 2, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)0));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			break;
		case "Three falling peaks":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
			if (Scores.YrlyRange == 3)
			{
				Scores.sYrlyRange = 0;
			}
			else if (Scores.YrlyRange == 2)
			{
				Scores.sYrlyRange = 1;
			}
			else
			{
				Scores.sYrlyRange = -1;
			}
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)0, (object)1));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)1));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			break;
		case "Three rising valleys":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)(-1), (object)1));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)1));
			break;
		case "Triangle, ascending":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)1, (object)(-1)));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)(-1), (object)1));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)0, (object)0));
				break;
			}
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = -1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = 0;
			}
			else
			{
				Scores.sTrendStart = 1;
			}
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)0, (object)0));
			break;
		case "Triangle, descending":
			if (num == 1)
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
				if (Scores.YrlyRange == 3)
				{
					Scores.sYrlyRange = 0;
				}
				else if (Scores.YrlyRange == 2)
				{
					Scores.sYrlyRange = -1;
				}
				else
				{
					Scores.sYrlyRange = 1;
				}
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			}
			else
			{
				Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
				if (Scores.YrlyRange == 3)
				{
					Scores.sYrlyRange = -1;
				}
				else if (Scores.YrlyRange == 2)
				{
					Scores.sYrlyRange = 0;
				}
				else
				{
					Scores.sYrlyRange = 1;
				}
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			}
			break;
		case "Triangle, symmetrical":
			if (num == 1)
			{
				if (Scores.TrendStart == 3)
				{
					Scores.sTrendStart = 1;
				}
				else if (Scores.TrendStart == 2)
				{
					Scores.sTrendStart = -1;
				}
				else
				{
					Scores.sTrendStart = 0;
				}
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)(-1), (object)0));
			}
			else
			{
				if (Scores.TrendStart == 3)
				{
					Scores.sTrendStart = -1;
				}
				else if (Scores.TrendStart == 2)
				{
					Scores.sTrendStart = 0;
				}
				else
				{
					Scores.sTrendStart = 1;
				}
				Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
				Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
				Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
				Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)0));
				Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
				Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			}
			break;
		case "Triple bottom":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 1, (object)1, (object)(-1)));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 3, (object)(-1), (object)1));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)(-1), (object)1));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			break;
		case "Triple top":
			if (Scores.TrendStart == 3)
			{
				Scores.sTrendStart = -1;
			}
			else if (Scores.TrendStart == 2)
			{
				Scores.sTrendStart = 0;
			}
			else
			{
				Scores.sTrendStart = 1;
			}
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)1, (object)(-1)));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)0, (object)0));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)0, (object)0));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)0));
			break;
		case "Ugly double bottom":
			Scores.sTrendStart = Conversions.ToInteger(Interaction.IIf(Scores.TrendStart == 3, (object)(-1), (object)1));
			Scores.sYrlyRange = Conversions.ToInteger(Interaction.IIf(Scores.YrlyRange == 1, (object)(-1), (object)1));
			Scores.sTall = Conversions.ToInteger(Interaction.IIf(Scores.bTall, (object)1, (object)(-1)));
			Scores.sVolumeTrend = Conversions.ToInteger(Interaction.IIf(Scores.VolumeTrend == -1, (object)1, (object)(-1)));
			Scores.sBkoutVol = Conversions.ToInteger(Interaction.IIf(Scores.BkoutVol == 1, (object)1, (object)(-1)));
			Scores.sThrowPull = Conversions.ToInteger(Interaction.IIf(Scores.bThrowPull, (object)(-1), (object)1));
			Scores.sBkoutGap = Conversions.ToInteger(Interaction.IIf(Scores.bBkoutGap, (object)1, (object)(-1)));
			break;
		}
		AddShowScores();
	}

	private void Chart1_MouseDown(object sender, MouseEventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_000b: Invalid comparison between Unknown and I4
		//IL_005b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0065: Invalid comparison between Unknown and I4
		//IL_0020: Unknown result type (might be due to invalid IL or missing references)
		//IL_002a: Expected O, but got Unknown
		//IL_008f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0096: Invalid comparison between Unknown and I4
		//IL_02de: Unknown result type (might be due to invalid IL or missing references)
		//IL_024f: Unknown result type (might be due to invalid IL or missing references)
		if ((int)e.Button == 1048576)
		{
			if (Information.IsNothing((object)CrosshairPen))
			{
				CrosshairPen = new Pen(Color.Black);
				CrosshairPen.DashStyle = (DashStyle)1;
			}
			CrosshairPoint = new Point(e.X, e.Y);
			Crosshair = true;
			((Control)this).Refresh();
		}
		if ((int)e.Button != 2097152)
		{
			return;
		}
		GlobalForm.ShowQuoteInfo(Chart1, e);
		try
		{
			HitTestResult val = Chart1.HitTest(e.X, e.Y);
			if ((int)val.ChartElementType != 16)
			{
				return;
			}
			int pointIndex = val.PointIndex;
			if (Operators.CompareString(val.Series.Name, "CandleSeries", false) != 0)
			{
				return;
			}
			checked
			{
				switch (LastFocus)
				{
				case 1:
					if ((DateTime.Compare(GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex], FromDatePicker.MaxDate) <= 0))
					{
						if (GlobalForm.IntradayData)
						{
							FromDatePicker.Value = GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex];
						}
						else
						{
							FromDatePicker.Value = GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex].Date;
						}
					}
					else
					{
						FromDatePicker.Value = DateAndTime.Now;
					}
					((Control)ToDatePicker).Focus();
					break;
				case 2:
					if (GlobalForm.IntradayData)
					{
						ToDatePicker.Value = GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex];
					}
					else
					{
						ToDatePicker.Value = GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex].Date;
					}
					((Control)BkoutDayPicker).Focus();
					break;
				case 3:
					if (GlobalForm.IntradayData)
					{
						BkoutDayPicker.Value = GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex];
						if (DateTime.Compare(BkoutDayPicker.Value, FromDatePicker.Value) <= 0)
						{
							MessageBox.Show("The breakout price can't be before the pattern's start. I'm setting it to the pattern's end date.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
							BkoutDayPicker.Value = ToDatePicker.Value;
						}
						else
						{
							((Control)HHTextBox).Focus();
						}
					}
					else
					{
						BkoutDayPicker.Value = GlobalForm.nDT[0, pointIndex + GlobalForm.ChartStartIndex].Date;
						if (DateTime.Compare(BkoutDayPicker.Value.Date, FromDatePicker.Value.Date) <= 0)
						{
							MessageBox.Show("The breakout price can't be before the pattern's start. I'm setting it to the pattern's end date.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
							BkoutDayPicker.Value = ToDatePicker.Value.Date;
						}
						else
						{
							((Control)HHTextBox).Focus();
						}
					}
					break;
				case 4:
					HHTextBox.Text = Strings.Format((object)GlobalForm.LimitDecimals(GlobalForm.nHLC[1, pointIndex + GlobalForm.ChartStartIndex]), "");
					((Control)LLTextBox).Focus();
					break;
				case 5:
					LLTextBox.Text = Strings.Format((object)GlobalForm.LimitDecimals(GlobalForm.nHLC[2, pointIndex + GlobalForm.ChartStartIndex]), "");
					((Control)BkoutPriceTextBox).Focus();
					break;
				case 6:
					BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.LimitDecimals(GlobalForm.nHLC[3, pointIndex + GlobalForm.ChartStartIndex]), "");
					((Control)ErrorLabel).ForeColor = Color.Blue;
					ErrorLabel.Text = "I plugged in the closing price. You may wish to adjust it.";
					break;
				}
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
	}

	private void Chart1_MouseUp(object sender, MouseEventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_000b: Invalid comparison between Unknown and I4
		//IL_011d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0127: Invalid comparison between Unknown and I4
		//IL_0042: Unknown result type (might be due to invalid IL or missing references)
		//IL_0048: Expected O, but got Unknown
		if ((int)e.Button == 1048576)
		{
			Crosshair = false;
			if (!Information.IsNothing((object)CrosshairPen))
			{
				CrosshairPen.Dispose();
				CrosshairPen = null;
			}
			Graphics obj = ((Control)this).CreateGraphics();
			Pen val = new Pen(((Form)this).BackColor);
			StartPoint = CrosshairPoint;
			StartPoint.X = 0;
			EndPoint = CrosshairPoint;
			checked
			{
				EndPoint.X = ((Control)Chart1).Right - ((Control)Chart1).Left;
				obj.DrawLine(val, StartPoint, EndPoint);
				StartPoint = CrosshairPoint;
				StartPoint.Y = 0;
				EndPoint = CrosshairPoint;
				EndPoint.Y = ((Control)Chart1).Bottom - ((Control)Chart1).Top;
				obj.DrawLine(val, StartPoint, EndPoint);
				val.Dispose();
				CrosshairPoint = new Point(e.X, e.Y);
				((Control)this).Refresh();
			}
		}
		if ((int)e.Button == 2097152)
		{
			GlobalForm.ReleaseQuoteInfo(Chart1, e);
		}
	}

	private void Chart1_MouseMove(object sender, MouseEventArgs e)
	{
		//IL_004c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0053: Invalid comparison between Unknown and I4
		//IL_0013: Unknown result type (might be due to invalid IL or missing references)
		//IL_001d: Expected O, but got Unknown
		//IL_042f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0436: Expected O, but got Unknown
		//IL_0481: Unknown result type (might be due to invalid IL or missing references)
		//IL_0488: Expected O, but got Unknown
		try
		{
			if (GlobalForm.Annotations)
			{
				if (CurrentAnnotation == null)
				{
					CurrentAnnotation = new CalloutAnnotation();
					((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)CurrentAnnotation);
				}
				HitTestResult val = Chart1.HitTest(e.X, e.Y);
				if ((int)val.ChartElementType == 16)
				{
					if (Operators.CompareString(val.Series.Name, "CandleSeries", false) == 0)
					{
						CalloutAnnotation currentAnnotation = CurrentAnnotation;
						((Annotation)currentAnnotation).AnchorDataPoint = ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex];
						double num = (double)((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Count / 5.0;
						if ((double)val.PointIndex - num <= 0.0)
						{
							((Annotation)currentAnnotation).X = (double)val.PointIndex + num;
						}
						else
						{
							((Annotation)currentAnnotation).X = (double)val.PointIndex - num;
						}
						((Annotation)currentAnnotation).Y = ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[3];
						((TextAnnotation)currentAnnotation).Text = "Open: " + GlobalForm.LimitDecimals(new decimal(((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[2])) + "\r\nHigh: " + GlobalForm.LimitDecimals(new decimal(((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[0])) + "\r\nLow: " + GlobalForm.LimitDecimals(new decimal(((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[1])) + "\r\nClose: " + GlobalForm.LimitDecimals(new decimal(((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[3]).ToString());
						((Annotation)currentAnnotation).Visible = true;
						currentAnnotation = null;
						Chart1.Invalidate();
					}
					else if (Operators.CompareString(val.Series.Name, "VolumeSeries", false) == 0)
					{
						((Annotation)CurrentAnnotation).AnchorDataPoint = ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex];
						double num = (double)((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Count / 5.0;
						if ((double)val.PointIndex - num <= 0.0)
						{
							((Annotation)CurrentAnnotation).X = (double)val.PointIndex + num;
						}
						else
						{
							((Annotation)CurrentAnnotation).X = (double)val.PointIndex - num;
						}
						((Annotation)CurrentAnnotation).Y = ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[0];
						((TextAnnotation)CurrentAnnotation).Text = ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)[val.Series.Name].Points)[val.PointIndex].YValues[0].ToString();
						((Annotation)CurrentAnnotation).Visible = true;
						Chart1.Invalidate();
					}
				}
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		if (!(GlobalForm.FirstPoint == default(Point)))
		{
			Graphics obj = ((Control)this).CreateGraphics();
			Pen val2 = new Pen(((Form)this).BackColor);
			obj.DrawLine(val2, GlobalForm.FirstPoint, GlobalForm.TempPoint);
			GlobalForm.TempPoint = new Point(e.X, e.Y);
			((Control)this).Refresh();
			val2.Dispose();
		}
		checked
		{
			if (Crosshair)
			{
				Graphics obj2 = ((Control)this).CreateGraphics();
				Pen val3 = new Pen(((Form)this).BackColor);
				StartPoint = CrosshairPoint;
				StartPoint.X = 0;
				EndPoint = CrosshairPoint;
				EndPoint.X = ((Control)Chart1).Right - ((Control)Chart1).Left;
				obj2.DrawLine(val3, StartPoint, EndPoint);
				StartPoint = CrosshairPoint;
				StartPoint.Y = 0;
				EndPoint = CrosshairPoint;
				EndPoint.Y = ((Control)Chart1).Bottom - ((Control)Chart1).Top;
				obj2.DrawLine(val3, StartPoint, EndPoint);
				val3.Dispose();
				CrosshairPoint = new Point(e.X, e.Y);
				((Control)this).Refresh();
			}
		}
	}

	private void Chart1_Paint(object sender, PaintEventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0010: Expected O, but got Unknown
		Font val = new Font("Arial", 8f);
		GlobalForm.StringSize = e.Graphics.MeasureString("C", val);
		val.Dispose();
		foreach (GlobalForm.LineEndPoints lines in GlobalForm.LinesList)
		{
			e.Graphics.DrawLine(Pens.Black, lines.StartPoint, lines.endPoint);
		}
		if (!(GlobalForm.FirstPoint == default(Point)))
		{
			e.Graphics.DrawLine(Pens.Black, GlobalForm.FirstPoint, GlobalForm.TempPoint);
		}
		checked
		{
			if (Crosshair)
			{
				StartPoint = CrosshairPoint;
				StartPoint.X = 0;
				EndPoint = CrosshairPoint;
				EndPoint.X = ((Control)Chart1).Right - ((Control)Chart1).Left;
				e.Graphics.DrawLine(CrosshairPen, StartPoint, EndPoint);
				StartPoint = CrosshairPoint;
				StartPoint.Y = 0;
				EndPoint = CrosshairPoint;
				EndPoint.Y = ((Control)Chart1).Bottom - ((Control)Chart1).Top;
				e.Graphics.DrawLine(CrosshairPen, StartPoint, EndPoint);
			}
		}
	}

	private void Chart1_PostPaint(object sender, ChartPaintEventArgs e)
	{
		//IL_0036: Unknown result type (might be due to invalid IL or missing references)
		//IL_02f0: Unknown result type (might be due to invalid IL or missing references)
		//IL_02f7: Expected O, but got Unknown
		PointF pointF = default(PointF);
		PointF pointF2 = default(PointF);
		ShowPatterns.DisplayAllPatterns(e, GlobalForm.ChartStart, GlobalForm.ChartEnd);
		if (!(e.ChartElement is Series) || Operators.CompareString(((Series)e.ChartElement).Name, "CandleSeries", false) != 0)
		{
			return;
		}
		int num = -1;
		int num2 = -1;
		int num3 = -1;
		int num4 = -1;
		int num5 = -1;
		for (int i = GlobalForm.HLCRange; i >= 0; i = checked(i + -1))
		{
			if (GlobalForm.IntradayData)
			{
				if ((num3 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i], GlobalForm.ChartStart) <= 0))
				{
					num3 = i;
				}
				if ((num == -1) & (DateTime.Compare(GlobalForm.nDT[0, i], FromDatePicker.Value) <= 0))
				{
					num = i;
				}
				if ((num2 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i], ToDatePicker.Value) <= 0))
				{
					num2 = i;
				}
				if ((num4 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i], BkoutDayPicker.Value) <= 0))
				{
					num4 = i;
				}
				if ((num5 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i], TrendStart) <= 0))
				{
					num5 = i;
				}
			}
			else
			{
				if ((num3 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i].Date, GlobalForm.ChartStart.Date) <= 0))
				{
					num3 = i;
				}
				if ((num == -1) & (DateTime.Compare(GlobalForm.nDT[0, i].Date, FromDatePicker.Value.Date) <= 0))
				{
					num = i;
				}
				if ((num2 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i].Date, ToDatePicker.Value.Date) <= 0))
				{
					num2 = i;
				}
				if ((num4 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i].Date, BkoutDayPicker.Value.Date) <= 0))
				{
					num4 = i;
				}
				if ((num5 == -1) & (DateTime.Compare(GlobalForm.nDT[0, i].Date, TrendStart.Date) <= 0))
				{
					num5 = i;
				}
			}
			if (num != -1 && num2 != -1 && num3 != -1 && num4 != -1 && (DateTime.Compare(TrendStart, DateAndTime.Now.Date) == 0 || num5 != -1))
			{
				break;
			}
		}
		if (num3 == -1)
		{
			num3 = 0;
		}
		if (num == -1 && num2 == -1 && num4 == -1 && num5 == -1)
		{
			return;
		}
		Series val = (Series)e.ChartElement;
		int num6 = 0;
		int num7 = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)val.Points)
			{
				if ((num != -1) & (num6 == num - num3 + 1))
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num6);
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					pointF2.X = pointF.X;
					pointF2.Y = ((Control)Chart1).Bottom;
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
					e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF, pointF2);
					num7++;
				}
				if ((num2 != -1) & (num6 == num2 - num3 + 1))
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num6);
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					pointF2.X = pointF.X;
					pointF2.Y = ((Control)Chart1).Bottom;
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
					e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF, pointF2);
					num7++;
				}
				if ((num4 != -1) & (num6 == num4 - num3 + 1))
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num6);
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					pointF2.X = pointF.X;
					pointF2.Y = ((Control)Chart1).Bottom;
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
					e.ChartGraphics.Graphics.DrawLine(Pens.Blue, pointF, pointF2);
					num7++;
				}
				if ((num5 != -1) & (num6 == num5 - num3 + 1))
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num6);
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					pointF2.X = pointF.X;
					pointF2.Y = ((Control)Chart1).Bottom;
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
					e.ChartGraphics.Graphics.DrawLine(Pens.DarkGreen, pointF, pointF2);
					num7++;
				}
				num6++;
				if (num7 == 4)
				{
					break;
				}
			}
		}
	}

	private void ComboBox1_SelectedIndexChanged(object sender, EventArgs e)
	{
		if (!Exiting)
		{
			switch (ComboBox1.Text)
			{
			case "Big M":
			case "Bump-and-run reversal, top":
			case "Double top, Adam & Adam":
			case "Double top, Adam & Eve":
			case "Double top, Eve & Adam":
			case "Double top, Eve & Eve":
			case "Double tops (all Types)":
			case "Head-and-shoulders top":
			case "Head-and-shoulders complex top":
			case "Rounding top":
			case "Scallop, descending And inverted":
			case "Three falling peaks":
			case "Triple top":
				BkoutDRB.Checked = true;
				break;
			case "Big W":
			case "Bump-and-run reversal, bottom":
			case "Cup with handle":
			case "Double bottom, Adam & Adam":
			case "Double bottom, Adam & Eve":
			case "Double bottom, Eve & Adam":
			case "Double bottom, Eve & Eve":
			case "Double bottoms (all Types)":
			case "Head-and-shoulders bottom":
			case "Head-and-shoulders complex bottom":
			case "Rounding bottom":
			case "Scallop, ascending And inverted":
			case "Three rising valleys":
			case "Triple bottom":
			case "Ugly double bottom":
				BkoutURB.Checked = true;
				break;
			}
			Array.Clear(GlobalForm.PatternList, 0, 124);
			object objectValue = RuntimeHelpers.GetObjectValue(GlobalForm.TranslatePatternName(ComboBox1.Text, GlobalForm.PASSNAME));
			if (Conversions.ToInteger(objectValue) != -1)
			{
				GlobalForm.PatternList[Conversions.ToInteger(objectValue)] = 1;
			}
			bool showCandles = GlobalForm.ShowCandles;
			GlobalForm.ShowCandles = false;
			FindPatterns.EnterFindPatterns(GlobalForm.ChartStart, GlobalForm.ChartEnd, null, ref StopPressed, 3);
			GlobalForm.ShowCandles = showCandles;
			if (GlobalForm.PatternCount != 0)
			{
				((Control)UsePatternButton).Enabled = true;
			}
			else
			{
				((Control)UsePatternButton).Enabled = false;
			}
			((Control)ErrorLabel).ForeColor = Color.Blue;
			ErrorLabel.Text = GlobalForm.PatternCount + " pattern" + Conversions.ToString(Interaction.IIf((GlobalForm.PatternCount > 1) | (GlobalForm.PatternCount == 0), (object)"s", (object)"")) + " found.";
			Chart1.Invalidate();
		}
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void FindHeightButton_Click(object sender, EventArgs e)
	{
		//IL_0dd0: Unknown result type (might be due to invalid IL or missing references)
		//IL_0d8e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0815: Unknown result type (might be due to invalid IL or missing references)
		//IL_08b9: Unknown result type (might be due to invalid IL or missing references)
		//IL_0ab0: Unknown result type (might be due to invalid IL or missing references)
		//IL_074b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0bf8: Unknown result type (might be due to invalid IL or missing references)
		//IL_0936: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c7f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0b57: Unknown result type (might be due to invalid IL or missing references)
		string text = "I found a confirmed downward breakout, so I set the breakout date, price, and direction.";
		string text2 = "I found a confirmed upward breakout, so I set the breakout date, price, and direction.";
		FindIndices();
		int num = iPatternStart;
		int num2 = iPatternStart;
		int num3 = iPatternStart;
		int num4 = iPatternEnd;
		checked
		{
			for (int i = num3; i <= num4; i++)
			{
				num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0, (object)i, (object)num));
				num2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num2]) < 0, (object)i, (object)num2));
			}
			HHTextBox.Text = Strings.Format((object)GlobalForm.nHLC[1, num], "");
			LLTextBox.Text = Strings.Format((object)GlobalForm.nHLC[2, num2], "");
			BkoutPriceTextBox.Text = "";
			switch (ComboBox1.Text)
			{
			case "Big M":
			case "Double top, Adam & Adam":
			case "Double top, Adam & Eve":
			case "Double top, Eve & Adam":
			case "Double top, Eve & Eve":
			case "Double tops (all Types)":
			case "Three falling peaks":
			case "Triple top":
			case "Scallop, descending And inverted":
			{
				BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[2, num2], "");
				int num9 = iPatternEnd + 1;
				int hLCRange5 = GlobalForm.HLCRange;
				for (int i = num9; i <= hLCRange5; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[2, num2]) < 0)
					{
						BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[2, num2], "");
						BkoutDayPicker.Value = GlobalForm.nDT[0, i];
						BkoutDRB.Checked = true;
						MessageBox.Show(text, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
						break;
					}
				}
				break;
			}
			case "Big W":
			case "Double bottom, Adam & Adam":
			case "Double bottom, Adam & Eve":
			case "Double bottom, Eve & Adam":
			case "Double bottom, Eve & Eve":
			case "Double bottoms (all Types)":
			case "Three rising valleys":
			case "Triple bottom":
			case "Ugly double bottom":
			case "Scallop, ascending And inverted":
			{
				BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[1, num], "");
				int num7 = iPatternEnd + 1;
				int hLCRange3 = GlobalForm.HLCRange;
				for (int i = num7; i <= hLCRange3; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[1, num]) > 0)
					{
						BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[1, num], "");
						BkoutDayPicker.Value = GlobalForm.nDT[0, i];
						BkoutURB.Checked = true;
						MessageBox.Show(text2, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
						break;
					}
				}
				break;
			}
			case "Broadening bottom":
			case "Broadening top":
			case "Broadening formation, right-angled & ascending":
			case "Broadening formation, right-angled & descending":
			case "Broadening wedge, ascending":
			case "Broadening wedge, descending":
			case "Rectangle bottom":
			case "Rectangle top":
			case "Scallop, ascending":
			case "Scallop, descending":
			{
				int num10 = iPatternEnd + 1;
				int hLCRange6 = GlobalForm.HLCRange;
				for (int i = num10; i <= hLCRange6; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[1, num]) > 0)
					{
						BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[1, num], "");
						BkoutDayPicker.Value = GlobalForm.nDT[0, i];
						BkoutURB.Checked = true;
						MessageBox.Show(text2, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
						break;
					}
					if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[2, num2]) < 0)
					{
						BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[2, num2], "");
						BkoutDayPicker.Value = GlobalForm.nDT[0, i];
						BkoutDRB.Checked = true;
						MessageBox.Show(text, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
						break;
					}
				}
				if (Operators.CompareString(BkoutPriceTextBox.Text, "", false) != 0)
				{
					break;
				}
				int num11 = iPatternEnd + 1;
				int hLCRange7 = GlobalForm.HLCRange;
				for (int i = num11; i <= hLCRange7; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0)
					{
						BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[1, num], "");
						break;
					}
					if (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num2]) < 0)
					{
						BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[2, num2], "");
						break;
					}
				}
				break;
			}
			case "Bump-and-run reversal, bottom":
			case "Cup with handle":
			case "Rounding bottom":
			{
				BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[1, iPatternEnd], "");
				int num8 = iPatternEnd + 1;
				int hLCRange4 = GlobalForm.HLCRange;
				for (int i = num8; i <= hLCRange4; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[1, iPatternEnd]) > 0)
					{
						BkoutDayPicker.Value = GlobalForm.nDT[0, i];
						BkoutURB.Checked = true;
						MessageBox.Show(text2, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
						break;
					}
				}
				break;
			}
			case "Bump-and-run reversal, top":
			{
				BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[2, iPatternEnd], "");
				int num12 = iPatternEnd + 1;
				int hLCRange8 = GlobalForm.HLCRange;
				for (int i = num12; i <= hLCRange8; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[2, iPatternEnd]) < 0)
					{
						BkoutDayPicker.Value = GlobalForm.nDT[0, i];
						BkoutDRB.Checked = true;
						MessageBox.Show(text, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
						break;
					}
				}
				break;
			}
			case "Rounding top":
			{
				int num5 = iPatternEnd + 1;
				int hLCRange = GlobalForm.HLCRange;
				for (int i = num5; i <= hLCRange; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[1, num]) > 0)
					{
						BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[1, num], "");
						BkoutDayPicker.Value = GlobalForm.nDT[0, i];
						BkoutURB.Checked = true;
						MessageBox.Show(text2, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
						break;
					}
					if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[2, iPatternEnd]) < 0)
					{
						BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[2, iPatternEnd], "");
						BkoutDayPicker.Value = GlobalForm.nDT[0, i];
						BkoutDRB.Checked = true;
						MessageBox.Show(text, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
						break;
					}
				}
				if (Operators.CompareString(BkoutPriceTextBox.Text, "", false) != 0)
				{
					break;
				}
				int num6 = iPatternEnd + 1;
				int hLCRange2 = GlobalForm.HLCRange;
				for (int i = num6; i <= hLCRange2; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0)
					{
						BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[1, num], "");
						break;
					}
					if (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, iPatternEnd]) < 0)
					{
						BkoutPriceTextBox.Text = Strings.Format((object)GlobalForm.nHLC[2, iPatternEnd], "");
						break;
					}
				}
				break;
			}
			}
			if (Operators.CompareString(BkoutPriceTextBox.Text, "", false) == 0)
			{
				MessageBox.Show("I can't calculate the height until you provide the breakout price.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				return;
			}
			CalcHeight(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num2], Conversions.ToDecimal(BkoutPriceTextBox.Text));
			MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
	}

	private void FindHeightButton_GotFocus(object sender, EventArgs e)
	{
		LastFocus = 0;
	}

	private void FindIndices()
	{
		iPatternStart = -1;
		iPatternEnd = -1;
		AdjustDates(Quiet: false);
		int hLCRange = GlobalForm.HLCRange;
		for (int i = 0; i <= hLCRange; i = checked(i + 1))
		{
			if (GlobalForm.IntradayData)
			{
				if ((iPatternStart == -1) & (DateTime.Compare(GlobalForm.nDT[0, i], FromDatePicker.Value) >= 0))
				{
					iPatternStart = i;
				}
				if (DateTime.Compare(GlobalForm.nDT[0, i], ToDatePicker.Value) >= 0)
				{
					iPatternEnd = i;
					break;
				}
			}
			else
			{
				if ((iPatternStart == -1) & (DateTime.Compare(GlobalForm.nDT[0, i].Date, FromDatePicker.Value.Date) >= 0))
				{
					iPatternStart = i;
				}
				if (DateTime.Compare(GlobalForm.nDT[0, i].Date, ToDatePicker.Value.Date) >= 0)
				{
					iPatternEnd = i;
					break;
				}
			}
		}
		if (iPatternStart == -1)
		{
			iPatternStart = 0;
		}
		if (iPatternEnd == -1)
		{
			iPatternEnd = GlobalForm.HLCRange;
		}
	}

	private void FromDatePicker_GotFocus(object sender, EventArgs e)
	{
		LastFocus = 1;
	}

	private void GraphButton_Click(object sender, EventArgs e)
	{
		//IL_014e: Unknown result type (might be due to invalid IL or missing references)
		DateTimePicker fromDatePicker = FromDatePicker;
		DateTime FromDate = fromDatePicker.Value;
		DateTimePicker toDatePicker;
		DateTime ToDate = (toDatePicker = ToDatePicker).Value;
		GlobalForm.SwapDates(ref FromDate, ref ToDate);
		toDatePicker.Value = ToDate;
		fromDatePicker.Value = FromDate;
		GlobalForm.FirstPoint = default(Point);
		GlobalForm.LinesList.RemoveAll(StubBoolean);
		if (((TextBoxBase)SymbolTextBox).TextLength > 0)
		{
			string text = SymbolTextBox.Text;
			if (Strings.InStr(text, ".", (CompareMethod)0) == 0)
			{
				string text2 = text + ".csv";
				if (!File.Exists(GlobalForm.OpenPath + "\\" + text2))
				{
					text2 = text + ".txt";
				}
				text = text2;
			}
			SymbolPlusExtension = text;
			GlobalForm.SetupDateIndexes(GlobalForm.ChartStart, GlobalForm.ChartEnd);
			AdjustDates(Quiet: false);
			bool showCandles = GlobalForm.ShowCandles;
			GlobalForm.ShowCandles = false;
			FindPatterns.EnterFindPatterns(GlobalForm.ChartStart, GlobalForm.ChartEnd, null, ref StopPressed, 3);
			GlobalForm.ShowStock(Chart1, GlobalForm.ChartStart, GlobalForm.ChartEnd, VolumeFlag: true, MAFlag: false);
			GlobalForm.ShowCandles = showCandles;
			if (GlobalForm.PatternCount != 0)
			{
				((Control)UsePatternButton).Enabled = true;
			}
			else
			{
				((Control)UsePatternButton).Enabled = false;
			}
			((Form)this).Text = "Manual Score Form: " + text;
		}
		else
		{
			MessageBox.Show("Enter a stock symbol in the text box or click Browse.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			((Control)SymbolTextBox).Focus();
		}
	}

	private void GroupBox4_Enter(object sender, EventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		((Control)(GroupBox)sender).ForeColor = Color.Blue;
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_000d: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show("DISCLAIMER: The scoring system is a tool to help you select better performing chart patterns, but there is no guarantee. Some patterns will work better than others, regardless of the score. How you trade will determine success or failure. YOU ALONE ARE RESPONSIBLE FOR YOUR INVESTMENT DECISIONS. Please understand that the Score Form does NOT make recommendations as to which security you should trade.\r\n\r\nFor more information on the scoring system, refer to my book, 'Trading Classic Chart Patterns' or visit my website at ThePatternSite.com.\r\n\r\nYou don't need a stock symbol, start, end or breakout dates to score a chart pattern. Select the chart pattern you wish to score from the combox box (middle left of form), then click options in each of the 11 steps.\r\n\r\nMost of the controls are self explanatory. The 'Get Existing Pattern's Dates' button uses the dates of a shown chart pattern and plugs the dates into the Pattern Start and End boxes.\r\n\r\nGrayed Find buttons require information such as the pattern's high, low, or breakout prices. Click the Find buttons to automatically pick a setting.\r\n\r\nRed vertical lines mark the start and end of the chart pattern, a blue line shows the breakout date, and a green line shows where the trend starts.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void HHTextBox_KeyPress(object sender, KeyPressEventArgs e)
	{
		if (!char.IsNumber(e.KeyChar) && !char.IsControl(e.KeyChar) && Operators.CompareString(Conversions.ToString(e.KeyChar), ".", false) != 0)
		{
			e.Handled = true;
		}
	}

	private void HHTextBox_TextChanged(object sender, EventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_0007: Expected O, but got Unknown
		TextBox val = (TextBox)sender;
		if (!Versioned.IsNumeric((object)val.Text))
		{
			val.Text = "";
			ErrorLabel.Text = "Only numbers and a decimal are allowed in the text box.";
			((Control)ErrorLabel).ForeColor = Color.Red;
			Interaction.Beep();
		}
		else
		{
			CalculateScore();
		}
		((Control)YearRangeButton).Enabled = Conversions.ToBoolean(Interaction.IIf((((TextBoxBase)BkoutPriceTextBox).TextLength != 0) & (Conversion.Val(BkoutPriceTextBox.Text) != 0.0) & (((TextBoxBase)SymbolTextBox).TextLength != 0), (object)true, (object)false));
		((Control)TrendStartButton).Enabled = Conversions.ToBoolean(Interaction.IIf((((TextBoxBase)HHTextBox).TextLength != 0) & (((TextBoxBase)LLTextBox).TextLength != 0) & (Conversion.Val(HHTextBox.Text) != 0.0) & (Conversion.Val(LLTextBox.Text) != 0.0) & (((TextBoxBase)SymbolTextBox).TextLength != 0), (object)true, (object)false));
	}

	private void HHTextBox_GotFocus(object sender, EventArgs e)
	{
		LastFocus = 4;
	}

	private void LLTextBox_GotFocus(object sender, EventArgs e)
	{
		LastFocus = 5;
	}

	private void LRVolButton_Click(object sender, EventArgs e)
	{
		//IL_01ef: Unknown result type (might be due to invalid IL or missing references)
		//IL_01db: Unknown result type (might be due to invalid IL or missing references)
		int num = 1;
		float num2 = 0f;
		float num3 = 0f;
		long num4 = 0L;
		float num5 = 0f;
		checked
		{
			for (int i = GlobalForm.HLCRange; i >= 0; i += -1)
			{
				if (!((GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, i], FromDatePicker.Value) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, i], ToDatePicker.Value) <= 0)) | (!GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, i].Date, FromDatePicker.Value.Date) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, i].Date, ToDatePicker.Value.Date) <= 0))))
				{
					continue;
				}
				float num6 = Convert.ToSingle(GlobalForm.nHLC[4, i]);
				num4 += num;
				num5 += num6;
				num2 += (float)(num * num);
				num3 += (float)num * num6;
				num++;
				if (!((GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, i], FromDatePicker.Value) <= 0)) | (!GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, i].Date, FromDatePicker.Value.Date) <= 0))))
				{
					continue;
				}
				int num7 = num - 1;
				if ((float)num7 * num2 - (float)(num4 * num4) != 0f)
				{
					if (((float)num7 * num3 - (float)num4 * num5) / ((float)num7 * num2 - (float)(num4 * num4)) > 0f)
					{
						LRVolDRB.Checked = true;
					}
					else
					{
						LRVolURB.Checked = true;
					}
					MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				}
				else
				{
					MessageBox.Show("Can't computer linear regression trend.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				}
				break;
			}
		}
	}

	private void MarketCapButton_Click(object sender, EventArgs e)
	{
		//IL_0240: Unknown result type (might be due to invalid IL or missing references)
		//IL_004c: Unknown result type (might be due to invalid IL or missing references)
		//IL_010d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0217: Unknown result type (might be due to invalid IL or missing references)
		string text = SymbolTextBox.Text;
		checked
		{
			if (Strings.InStrRev(text, ".", -1, (CompareMethod)0) != 0)
			{
				text = Strings.Left(text, Strings.InStrRev(text, ".", -1, (CompareMethod)0) - 1);
			}
			if (text.Length == 0)
			{
				MessageBox.Show("Please enter a security symbol.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				((Control)MarketCapButton).Enabled = false;
				((Control)SymbolTextBox).Focus();
				return;
			}
			string text2 = "&f=j1";
			string text3 = null;
			StreamReader streamReader = null;
			Stream stream = null;
			WebResponse webResponse = null;
			ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
			try
			{
				webResponse = WebRequest.CreateHttp(YAHOOURLeod + text + text2).GetResponse();
				stream = webResponse.GetResponseStream();
				streamReader = new StreamReader(stream);
				text3 = streamReader.ReadToEnd();
				streamReader.Close();
				streamReader = null;
				stream.Close();
				stream = null;
				webResponse.Close();
				webResponse = null;
				text3 = text3.Replace("\r\n", "");
				text3 = text3.Replace("\n", "");
				if (Operators.CompareString(text3, "N/A", false) == 0)
				{
					MessageBox.Show("Symbol not found.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
					((Control)SymbolTextBox).Focus();
					return;
				}
				string text4 = Strings.UCase(Strings.Right(text3, 1));
				double num = ((Operators.CompareString(text4, "B", false) == 0) ? (Conversion.Val(Strings.Left(text3, text3.Length - 1)) * 1000000000.0) : ((Operators.CompareString(text4, "M", false) != 0) ? Conversion.Val(text3) : (Conversion.Val(Strings.Left(text3, text3.Length - 1)) * 1000000.0)));
				double num2 = num;
				if (num2 < 1000000000.0)
				{
					Scores.sMarketCap = 1;
					SmallRB.Checked = true;
				}
				else if (num2 > 5000000000.0)
				{
					Scores.sMarketCap = -1;
					LargeRB.Checked = true;
				}
				else
				{
					Scores.sMarketCap = 0;
					MediumRB.Checked = true;
				}
				MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				MessageBox.Show("I had a problem connecting to the internet: " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				streamReader?.Close();
				stream?.Close();
				webResponse?.Close();
				ProjectData.ClearProjectError();
			}
		}
	}

	public void MSCheckDates(DateTimePicker FromDatePicker, DateTimePicker ToDatePicker, DateTimePicker BkoutDayPicker, bool Quiet)
	{
		//IL_0552: Unknown result type (might be due to invalid IL or missing references)
		int num = 0;
		if (GlobalForm.IntradayData)
		{
			try
			{
				if ((DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MaxDate) <= 0))
				{
					if (DateTime.Compare(FromDatePicker.Value, GlobalForm.nDT[0, 0]) < 0)
					{
						num = 1;
						FromDatePicker.Value = GlobalForm.nDT[0, 0];
						GlobalForm.ChartStart = FromDatePicker.Value;
					}
					if (DateTime.Compare(FromDatePicker.Value, GlobalForm.nDT[0, GlobalForm.HLCRange]) > 0)
					{
						num = 1;
						FromDatePicker.Value = GlobalForm.nDT[0, GlobalForm.HLCRange];
						GlobalForm.ChartStart = FromDatePicker.Value;
					}
				}
				else
				{
					FromDatePicker.Value = DateAndTime.Now;
				}
				if ((DateTime.Compare(GlobalForm.nDT[0, 0], ToDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, 0], ToDatePicker.MaxDate) <= 0))
				{
					if (DateTime.Compare(ToDatePicker.Value, GlobalForm.nDT[0, 0]) < 0)
					{
						num = 2;
						ToDatePicker.Value = GlobalForm.nDT[0, 0];
						GlobalForm.ChartEnd = ToDatePicker.Value;
					}
					if (DateTime.Compare(ToDatePicker.Value, GlobalForm.nDT[0, GlobalForm.HLCRange]) > 0)
					{
						num = 2;
						ToDatePicker.Value = GlobalForm.nDT[0, GlobalForm.HLCRange];
						GlobalForm.ChartEnd = ToDatePicker.Value;
					}
				}
				else
				{
					ToDatePicker.Value = DateAndTime.Now;
				}
				DateTime FromDate = FromDatePicker.Value;
				DateTimePicker val;
				DateTime ToDate = (val = ToDatePicker).Value;
				GlobalForm.SwapDates(ref FromDate, ref ToDate);
				val.Value = ToDate;
				FromDatePicker.Value = FromDate;
				if ((DateTime.Compare(GlobalForm.nDT[0, 0], BkoutDayPicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, 0], BkoutDayPicker.MaxDate) <= 0))
				{
					if (DateTime.Compare(BkoutDayPicker.Value, GlobalForm.nDT[0, 0]) < 0)
					{
						num = 3;
						BkoutDayPicker.Value = GlobalForm.nDT[0, 0];
					}
					if (DateTime.Compare(BkoutDayPicker.Value, GlobalForm.nDT[0, GlobalForm.HLCRange]) > 0)
					{
						num = 3;
						BkoutDayPicker.Value = GlobalForm.nDT[0, GlobalForm.HLCRange];
					}
				}
				else
				{
					BkoutDayPicker.Value = DateAndTime.Now;
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				ProjectData.ClearProjectError();
			}
		}
		else
		{
			try
			{
				if ((DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, 0], FromDatePicker.MaxDate) <= 0))
				{
					if (DateTime.Compare(FromDatePicker.Value.Date, GlobalForm.nDT[0, 0].Date) < 0)
					{
						num = 1;
						FromDatePicker.Value = GlobalForm.nDT[0, 0].Date;
						GlobalForm.ChartStart = FromDatePicker.Value.Date;
					}
					if (DateTime.Compare(FromDatePicker.Value.Date, GlobalForm.nDT[0, GlobalForm.HLCRange].Date) > 0)
					{
						num = 1;
						FromDatePicker.Value = GlobalForm.nDT[0, GlobalForm.HLCRange].Date;
						GlobalForm.ChartStart = FromDatePicker.Value.Date;
					}
				}
				else
				{
					FromDatePicker.Value = DateAndTime.Now;
				}
				if ((DateTime.Compare(GlobalForm.nDT[0, 0], ToDatePicker.MinDate) >= 0) & (DateTime.Compare(GlobalForm.nDT[0, 0], ToDatePicker.MaxDate) <= 0))
				{
					if (DateTime.Compare(ToDatePicker.Value.Date, GlobalForm.nDT[0, 0].Date) < 0)
					{
						num = 2;
						ToDatePicker.Value = GlobalForm.nDT[0, 0].Date;
						GlobalForm.ChartEnd = ToDatePicker.Value.Date;
					}
					if (DateTime.Compare(ToDatePicker.Value.Date, GlobalForm.nDT[0, GlobalForm.HLCRange].Date) > 0)
					{
						num = 2;
						ToDatePicker.Value = GlobalForm.nDT[0, GlobalForm.HLCRange].Date;
						GlobalForm.ChartEnd = ToDatePicker.Value.Date;
					}
				}
				else
				{
					ToDatePicker.Value = DateAndTime.Now;
				}
				DateTime ToDate = FromDatePicker.Value;
				DateTimePicker val;
				DateTime FromDate = (val = ToDatePicker).Value;
				GlobalForm.SwapDates(ref ToDate, ref FromDate);
				val.Value = FromDate;
				FromDatePicker.Value = ToDate;
				if (DateTime.Compare(BkoutDayPicker.Value.Date, GlobalForm.nDT[0, 0].Date) < 0)
				{
					num = 3;
					BkoutDayPicker.Value = GlobalForm.nDT[0, 0].Date;
				}
				if (DateTime.Compare(BkoutDayPicker.Value.Date, GlobalForm.nDT[0, GlobalForm.HLCRange].Date) > 0)
				{
					num = 3;
					BkoutDayPicker.Value = GlobalForm.nDT[0, GlobalForm.HLCRange].Date;
				}
			}
			catch (Exception ex3)
			{
				ProjectData.SetProjectError(ex3);
				Exception ex4 = ex3;
				ProjectData.ClearProjectError();
			}
		}
		if (num != 0 && !Quiet)
		{
			MessageBox.Show("One of the three dates ends before the stock begins or it begins after the stock ends. I've adjusted the date.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			switch (num)
			{
			case 1:
				((Control)FromDatePicker).Focus();
				break;
			case 2:
				((Control)ToDatePicker).Focus();
				break;
			case 3:
				((Control)BkoutDayPicker).Focus();
				break;
			}
		}
	}

	private void ShortRB_CheckedChanged(object sender, EventArgs e)
	{
		CalculateScore();
	}

	private void ShortRB_GotFocus(object sender, EventArgs e)
	{
		LastFocus = 0;
	}

	private bool StubBoolean(GlobalForm.LineEndPoints sPoint)
	{
		return true;
	}

	private void SymbolTextBox_TextChanged(object sender, EventArgs e)
	{
		((Control)MarketCapButton).Enabled = Conversions.ToBoolean(Interaction.IIf(((TextBoxBase)SymbolTextBox).TextLength == 0, (object)false, (object)true));
		bool enabled = ((((TextBoxBase)SymbolTextBox).TextLength != 0) ? true : false);
		((Control)BkoutVolButton).Enabled = enabled;
		((Control)FindHeightButton).Enabled = enabled;
		((Control)GraphButton).Enabled = enabled;
		((Control)LRVolButton).Enabled = enabled;
		((Control)MarketCapButton).Enabled = enabled;
		((Control)YearRangeButton).Enabled = Conversions.ToBoolean(Interaction.IIf((((TextBoxBase)BkoutPriceTextBox).TextLength != 0) & (Conversion.Val(BkoutPriceTextBox.Text) != 0.0) & (((TextBoxBase)SymbolTextBox).TextLength != 0), (object)true, (object)false));
		((Control)TrendStartButton).Enabled = Conversions.ToBoolean(Interaction.IIf((((TextBoxBase)HHTextBox).TextLength != 0) & (((TextBoxBase)LLTextBox).TextLength != 0) & (Conversion.Val(HHTextBox.Text) != 0.0) & (Conversion.Val(LLTextBox.Text) != 0.0) & (((TextBoxBase)SymbolTextBox).TextLength != 0), (object)true, (object)false));
	}

	private void ToDatePicker_gotFocus(object sender, EventArgs e)
	{
		LastFocus = 2;
	}

	private void TrendStartButton_Click(object sender, EventArgs e)
	{
		//IL_07ab: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_0197: Unknown result type (might be due to invalid IL or missing references)
		//IL_0782: Unknown result type (might be due to invalid IL or missing references)
		//IL_06c6: Unknown result type (might be due to invalid IL or missing references)
		//IL_076d: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			try
			{
				int num = -1;
				int num2 = -1;
				TrendStart = DateAndTime.Now;
				int i;
				for (i = GlobalForm.HLCRange; i >= 0; i += -1)
				{
					if ((GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, i], FromDatePicker.Value) <= 0)) | (!GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, i].Date, FromDatePicker.Value.Date) <= 0)))
					{
						num = i;
						break;
					}
				}
				if (num == -1)
				{
					MessageBox.Show("Can't find the pattern's start date. Is it correct?", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
					((Control)FromDatePicker).Focus();
					return;
				}
				DateTime t = default(DateTime);
				if (GlobalForm.IntradayData)
				{
					for (i = GlobalForm.HLCRange; i >= 0; i += -1)
					{
						if (DateTime.Compare(GlobalForm.nDT[0, i], GlobalForm.nDT[0, num]) <= 0)
						{
							t = ((i < 14) ? GlobalForm.nDT[0, 0] : GlobalForm.nDT[0, i - 14]);
							break;
						}
					}
				}
				else
				{
					t = DateAndTime.DateAdd((DateInterval)4, -14.0, GlobalForm.nDT[0, num].Date);
				}
				decimal num3 = Conversions.ToDecimal(HHTextBox.Text);
				decimal num4 = Conversions.ToDecimal(LLTextBox.Text);
				if ((decimal.Compare(num3, 0m) == 0) | (decimal.Compare(num3, num4) == 0) | (decimal.Compare(num4, 0m) == 0))
				{
					MessageBox.Show("The pattern's high and low price can't be the same and both can't be zero.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
					if ((decimal.Compare(num3, 0m) == 0) | (decimal.Compare(num3, num4) == 0))
					{
						((Control)HHTextBox).Focus();
					}
					else
					{
						((Control)LLTextBox).Focus();
					}
					return;
				}
				bool flag = false;
				for (i = num - 1; i >= 0; i += -1)
				{
					if (!((GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, i], t) <= 0)) | (!GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, i].Date, t.Date) <= 0))))
					{
						continue;
					}
					if (decimal.Compare(GlobalForm.nHLC[3, i], num4) < 0)
					{
						int num5 = i;
						for (int j = i - 1; j >= 0; j += -1)
						{
							if (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num5]) < 0)
							{
								num5 = j;
							}
							if (GlobalForm.IntradayData)
							{
								if (unchecked(Convert.ToDouble(GlobalForm.nHLC[3, j]) >= Convert.ToDouble(GlobalForm.nHLC[2, num5]) * 1.2 && j != num5) | ((double)(num - j) > 182.5))
								{
									long num6 = num - num5;
									if ((double)num6 < 91.25)
									{
										TrendShortRB.Checked = true;
									}
									else if ((double)num6 >= 182.5)
									{
										TrendLongRB.Checked = true;
									}
									else
									{
										TrendIntermediateRB.Checked = true;
									}
									num2 = num5;
									flag = true;
									break;
								}
							}
							else if (unchecked(Convert.ToDouble(GlobalForm.nHLC[3, j]) >= Convert.ToDouble(GlobalForm.nHLC[2, num5]) * 1.2 && j != num5) | ((double)DateAndTime.DateDiff((DateInterval)4, GlobalForm.nDT[0, j].Date, GlobalForm.nDT[0, num].Date, (FirstDayOfWeek)1, (FirstWeekOfYear)1) > 182.5))
							{
								long num7 = DateAndTime.DateDiff((DateInterval)4, GlobalForm.nDT[0, num5].Date, GlobalForm.nDT[0, num].Date, (FirstDayOfWeek)1, (FirstWeekOfYear)1);
								if ((double)num7 < 91.25)
								{
									TrendShortRB.Checked = true;
								}
								else if ((double)num7 >= 182.5)
								{
									TrendLongRB.Checked = true;
								}
								else
								{
									TrendIntermediateRB.Checked = true;
								}
								num2 = num5;
								flag = true;
								break;
							}
						}
						break;
					}
					if (decimal.Compare(GlobalForm.nHLC[3, i], num3) <= 0)
					{
						continue;
					}
					int num8 = i;
					for (int j = i - 1; j >= 0; j += -1)
					{
						if (decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, num8]) > 0)
						{
							num8 = j;
						}
						if (GlobalForm.IntradayData)
						{
							if (unchecked(Convert.ToDouble(GlobalForm.nHLC[3, j]) <= Convert.ToDouble(GlobalForm.nHLC[1, num8]) * 0.8 && j != num8) | ((double)(num - j) > 182.5))
							{
								long num9 = num - num8;
								if ((double)num9 < 91.25)
								{
									TrendShortRB.Checked = true;
								}
								else if ((double)num9 >= 182.5)
								{
									TrendLongRB.Checked = true;
								}
								else
								{
									TrendIntermediateRB.Checked = true;
								}
								num2 = num8;
								flag = true;
								break;
							}
						}
						else if (unchecked(Convert.ToDouble(GlobalForm.nHLC[3, j]) <= Convert.ToDouble(GlobalForm.nHLC[1, num8]) * 0.8 && j != num8) | ((double)DateAndTime.DateDiff((DateInterval)4, GlobalForm.nDT[0, j].Date, GlobalForm.nDT[0, num].Date, (FirstDayOfWeek)1, (FirstWeekOfYear)1) > 182.5))
						{
							long num10 = DateAndTime.DateDiff((DateInterval)4, GlobalForm.nDT[0, num8].Date, GlobalForm.nDT[0, num].Date, (FirstDayOfWeek)1, (FirstWeekOfYear)1);
							if ((double)num10 < 91.25)
							{
								TrendShortRB.Checked = true;
							}
							else if ((double)num10 >= 182.5)
							{
								TrendLongRB.Checked = true;
							}
							else
							{
								TrendIntermediateRB.Checked = true;
							}
							num2 = num8;
							flag = true;
							break;
						}
					}
					break;
				}
				if (!flag)
				{
					if ((GlobalForm.IntradayData & ((double)(num - i) > 182.5)) | (!GlobalForm.IntradayData & ((double)DateAndTime.DateDiff((DateInterval)4, GlobalForm.nDT[0, i].Date, GlobalForm.nDT[0, num], (FirstDayOfWeek)1, (FirstWeekOfYear)1) > 182.5)))
					{
						TrendLongRB.Checked = true;
					}
					else
					{
						MessageBox.Show("Can't find trend start.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
					}
				}
				else if (num2 != -1)
				{
					if (GlobalForm.IntradayData)
					{
						TrendStart = GlobalForm.nDT[0, num2];
					}
					else
					{
						TrendStart = GlobalForm.nDT[0, num2].Date;
					}
					GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
					ErrorLabel.Text = "Excluding overshoot/undershoot, the trend starts on or before " + Strings.Format((object)GlobalForm.nDT[0, num2], GlobalForm.UserDate) + ", show as a green vertical line.";
					MessageBox.Show("Done! " + ErrorLabel.Text, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				}
				else
				{
					MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				MessageBox.Show("Error while searching for trend start: " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				ProjectData.ClearProjectError();
			}
		}
	}

	private void UsePatternButton_Click(object sender, EventArgs e)
	{
		//IL_0061: Unknown result type (might be due to invalid IL or missing references)
		//IL_0115: Unknown result type (might be due to invalid IL or missing references)
		//IL_011b: Invalid comparison between Unknown and I4
		//IL_01ae: Unknown result type (might be due to invalid IL or missing references)
		//IL_0176: Unknown result type (might be due to invalid IL or missing references)
		if (GlobalForm.PatternCount == 1)
		{
			FromDatePicker.Value = GlobalForm.nDT[0, GlobalForm.ChartPatterns[0].iStartDate];
			ToDatePicker.Value = GlobalForm.nDT[0, GlobalForm.ChartPatterns[0].iEndDate];
			MessageBox.Show("The pattern start and end dates have been filled in.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			((Control)BkoutDayPicker).Focus();
			return;
		}
		int num = checked(GlobalForm.PatternCount - 1);
		for (int i = 0; i <= num; i = checked(i + 1))
		{
			if ((int)MessageBox.Show("The pattern starts on " + Strings.Format((object)GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStartDate], GlobalForm.UserDate) + " and ends on " + Strings.Format((object)GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEndDate], GlobalForm.UserDate) + " Is this the one you want?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32) == 6)
			{
				FromDatePicker.Value = GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iStartDate];
				ToDatePicker.Value = GlobalForm.nDT[0, GlobalForm.ChartPatterns[i].iEndDate];
				MessageBox.Show("The pattern start and end dates have been filled in.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
				GraphButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
				((Control)BkoutDayPicker).Focus();
				return;
			}
		}
		MessageBox.Show("Can't find any patterns to use. Sorry.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
	}

	private void YearRangeButton_Click(object sender, EventArgs e)
	{
		//IL_0297: Unknown result type (might be due to invalid IL or missing references)
		//IL_018b: Unknown result type (might be due to invalid IL or missing references)
		//IL_026e: Unknown result type (might be due to invalid IL or missing references)
		DateTime t = DateAndTime.DateAdd((DateInterval)0, -1.0, FromDatePicker.Value);
		int num = -1;
		int num2 = -1;
		checked
		{
			for (int i = GlobalForm.HLCRange; i >= 0; i += -1)
			{
				if (unchecked(((GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, i], FromDatePicker.Value) <= 0)) | (!GlobalForm.IntradayData & (DateTime.Compare(GlobalForm.nDT[0, i].Date, FromDatePicker.Value) <= 0))) && num == -1))
				{
					if (DateTime.Compare(GlobalForm.nDT[0, i], FromDatePicker.Value) == 0)
					{
						num = i - 1;
						num2 = i - 1;
					}
					else
					{
						num = i;
						num2 = i;
					}
				}
				else if (num != -1)
				{
					num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0, (object)i, (object)num));
					num2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num2]) < 0, (object)i, (object)num2));
				}
				if (GlobalForm.IntradayData)
				{
					if (DateTime.Compare(GlobalForm.nDT[0, i], t) <= 0)
					{
						break;
					}
				}
				else if (DateTime.Compare(GlobalForm.nDT[0, i].Date, t.Date) <= 0)
				{
					break;
				}
			}
		}
		if (num == -1 || num2 == -1)
		{
			MessageBox.Show("Not enough data to make computation (can't find start and/or end date)", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			((Control)FromDatePicker).Focus();
			return;
		}
		try
		{
			decimal d = Conversions.ToDecimal(BkoutPriceTextBox.Text);
			if (decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, num], decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num2]), 3m))) >= 0)
			{
				HighThirdRB.Checked = true;
			}
			else if (decimal.Compare(d, decimal.Add(GlobalForm.nHLC[2, num2], decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num2]), 3m))) <= 0)
			{
				LowThirdRB.Checked = true;
			}
			else
			{
				MiddleThirdRB.Checked = true;
			}
			MessageBox.Show("Done!", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			MessageBox.Show("Some is wrong with the breakout price: " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			((Control)BkoutPriceTextBox).Focus();
			ProjectData.ClearProjectError();
		}
	}
}
