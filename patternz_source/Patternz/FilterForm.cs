using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Runtime.CompilerServices;
using System.Runtime.Serialization.Formatters.Binary;
using System.Windows.Forms;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz;

[DesignerGenerated]
public class FilterForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("NumericWidthHigh")]
	private NumericUpDown _NumericWidthHigh;

	[CompilerGenerated]
	[AccessedThroughProperty("NumericWidthLow")]
	private NumericUpDown _NumericWidthLow;

	[CompilerGenerated]
	[AccessedThroughProperty("ButtonWidthDefault")]
	private Button _ButtonWidthDefault;

	[CompilerGenerated]
	[AccessedThroughProperty("ButtonPriceDefault")]
	private Button _ButtonPriceDefault;

	[CompilerGenerated]
	[AccessedThroughProperty("NumericPriceHigh")]
	private NumericUpDown _NumericPriceHigh;

	[CompilerGenerated]
	[AccessedThroughProperty("NumericPriceLow")]
	private NumericUpDown _NumericPriceLow;

	[CompilerGenerated]
	[AccessedThroughProperty("ButtonVolumeDefault")]
	private Button _ButtonVolumeDefault;

	[CompilerGenerated]
	[AccessedThroughProperty("CBWidth")]
	private CheckBox _CBWidth;

	[CompilerGenerated]
	[AccessedThroughProperty("CBPrice")]
	private CheckBox _CBPrice;

	[CompilerGenerated]
	[AccessedThroughProperty("CBHeight")]
	private CheckBox _CBHeight;

	[CompilerGenerated]
	[AccessedThroughProperty("CBBkoutDirection")]
	private CheckBox _CBBkoutDirection;

	[CompilerGenerated]
	[AccessedThroughProperty("CBVolume")]
	private CheckBox _CBVolume;

	[CompilerGenerated]
	[AccessedThroughProperty("ButtonDirectionDefault")]
	private Button _ButtonDirectionDefault;

	[CompilerGenerated]
	[AccessedThroughProperty("ButtonHeightDefault")]
	private Button _ButtonHeightDefault;

	[CompilerGenerated]
	[AccessedThroughProperty("CBStages")]
	private CheckBox _CBStages;

	[CompilerGenerated]
	[AccessedThroughProperty("CBHighVolume")]
	private CheckBox _CBHighVolume;

	[CompilerGenerated]
	[AccessedThroughProperty("CBPriceMoves")]
	private CheckBox _CBPriceMoves;

	[CompilerGenerated]
	[AccessedThroughProperty("StagesHelpButton")]
	private Button _StagesHelpButton;

	private bool LockFlag;

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

	[field: AccessedThroughProperty("RBWidthLess")]
	internal virtual RadioButton RBWidthLess
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

	[field: AccessedThroughProperty("RBWidthBetween")]
	internal virtual RadioButton RBWidthBetween
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBWidthMore")]
	internal virtual RadioButton RBWidthMore
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("GroupWidth")]
	internal virtual GroupBox GroupWidth
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual NumericUpDown NumericWidthHigh
	{
		[CompilerGenerated]
		get
		{
			return _NumericWidthHigh;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = NumericWidthLow_LostFocus;
			NumericUpDown val = _NumericWidthHigh;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
			}
			_NumericWidthHigh = value;
			val = _NumericWidthHigh;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("NumericWidthMore")]
	internal virtual NumericUpDown NumericWidthMore
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual NumericUpDown NumericWidthLow
	{
		[CompilerGenerated]
		get
		{
			return _NumericWidthLow;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = NumericWidthLow_LostFocus;
			NumericUpDown val = _NumericWidthLow;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
			}
			_NumericWidthLow = value;
			val = _NumericWidthLow;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("NumericWidthLess")]
	internal virtual NumericUpDown NumericWidthLess
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button ButtonWidthDefault
	{
		[CompilerGenerated]
		get
		{
			return _ButtonWidthDefault;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ButtonWidthDefault_Click;
			Button val = _ButtonWidthDefault;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ButtonWidthDefault = value;
			val = _ButtonWidthDefault;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("GroupPrice")]
	internal virtual GroupBox GroupPrice
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button ButtonPriceDefault
	{
		[CompilerGenerated]
		get
		{
			return _ButtonPriceDefault;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ButtonPriceDefault_Click;
			Button val = _ButtonPriceDefault;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ButtonPriceDefault = value;
			val = _ButtonPriceDefault;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual NumericUpDown NumericPriceHigh
	{
		[CompilerGenerated]
		get
		{
			return _NumericPriceHigh;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = NumericPriceLow_LostFocus;
			NumericUpDown val = _NumericPriceHigh;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
			}
			_NumericPriceHigh = value;
			val = _NumericPriceHigh;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("NumericPriceMore")]
	internal virtual NumericUpDown NumericPriceMore
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual NumericUpDown NumericPriceLow
	{
		[CompilerGenerated]
		get
		{
			return _NumericPriceLow;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = NumericPriceLow_LostFocus;
			NumericUpDown val = _NumericPriceLow;
			if (val != null)
			{
				((Control)val).LostFocus -= eventHandler;
			}
			_NumericPriceLow = value;
			val = _NumericPriceLow;
			if (val != null)
			{
				((Control)val).LostFocus += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("NumericPriceLess")]
	internal virtual NumericUpDown NumericPriceLess
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBPriceBetween")]
	internal virtual RadioButton RBPriceBetween
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBPriceMore")]
	internal virtual RadioButton RBPriceMore
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBPriceLess")]
	internal virtual RadioButton RBPriceLess
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("GroupHeight")]
	internal virtual GroupBox GroupHeight
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

	[field: AccessedThroughProperty("RBHeightShort")]
	internal virtual RadioButton RBHeightShort
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBHeightEither")]
	internal virtual RadioButton RBHeightEither
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBHeightTall")]
	internal virtual RadioButton RBHeightTall
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("GroupVolume")]
	internal virtual GroupBox GroupVolume
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

	internal virtual Button ButtonVolumeDefault
	{
		[CompilerGenerated]
		get
		{
			return _ButtonVolumeDefault;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ButtonVolumeDefault_Click;
			Button val = _ButtonVolumeDefault;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ButtonVolumeDefault = value;
			val = _ButtonVolumeDefault;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("NumericVolume")]
	internal virtual NumericUpDown NumericVolume
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("GroupBkoutDirection")]
	internal virtual GroupBox GroupBkoutDirection
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CBBkoutIncludeNone")]
	internal virtual CheckBox CBBkoutIncludeNone
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBBkoutNoneYet")]
	internal virtual RadioButton RBBkoutNoneYet
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBBkoutDown")]
	internal virtual RadioButton RBBkoutDown
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBBkoutUpDown")]
	internal virtual RadioButton RBBkoutUpDown
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RBBkoutUp")]
	internal virtual RadioButton RBBkoutUp
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CBMasterSwitch")]
	internal virtual CheckBox CBMasterSwitch
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual CheckBox CBWidth
	{
		[CompilerGenerated]
		get
		{
			return _CBWidth;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CBWidth_CheckedChanged;
			CheckBox val = _CBWidth;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_CBWidth = value;
			val = _CBWidth;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox CBPrice
	{
		[CompilerGenerated]
		get
		{
			return _CBPrice;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CBPrice_CheckedChanged;
			CheckBox val = _CBPrice;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_CBPrice = value;
			val = _CBPrice;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox CBHeight
	{
		[CompilerGenerated]
		get
		{
			return _CBHeight;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CBHeight_CheckedChanged;
			CheckBox val = _CBHeight;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_CBHeight = value;
			val = _CBHeight;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox CBBkoutDirection
	{
		[CompilerGenerated]
		get
		{
			return _CBBkoutDirection;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CBBkoutDirection_CheckedChanged;
			CheckBox val = _CBBkoutDirection;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_CBBkoutDirection = value;
			val = _CBBkoutDirection;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox CBVolume
	{
		[CompilerGenerated]
		get
		{
			return _CBVolume;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CBVolume_CheckedChanged;
			CheckBox val = _CBVolume;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_CBVolume = value;
			val = _CBVolume;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label4")]
	internal virtual Label Label4
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button ButtonDirectionDefault
	{
		[CompilerGenerated]
		get
		{
			return _ButtonDirectionDefault;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ButtonDirectionDefault_Click;
			Button val = _ButtonDirectionDefault;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ButtonDirectionDefault = value;
			val = _ButtonDirectionDefault;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button ButtonHeightDefault
	{
		[CompilerGenerated]
		get
		{
			return _ButtonHeightDefault;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ButtonHeightDefault_Click;
			Button val = _ButtonHeightDefault;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ButtonHeightDefault = value;
			val = _ButtonHeightDefault;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("Label5")]
	internal virtual Label Label5
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

	[field: AccessedThroughProperty("GroupHighVolume")]
	internal virtual GroupBox GroupHighVolume
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

	[field: AccessedThroughProperty("NumericHighVolume")]
	internal virtual NumericUpDown NumericHighVolume
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("GroupPriceMoves")]
	internal virtual GroupBox GroupPriceMoves
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

	[field: AccessedThroughProperty("NumericPriceMoves")]
	internal virtual NumericUpDown NumericPriceMoves
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CBStage1")]
	internal virtual CheckBox CBStage1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("GroupStages")]
	internal virtual GroupBox GroupStages
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CBStage4")]
	internal virtual CheckBox CBStage4
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CBStage3")]
	internal virtual CheckBox CBStage3
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("CBStage2")]
	internal virtual CheckBox CBStage2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual CheckBox CBStages
	{
		[CompilerGenerated]
		get
		{
			return _CBStages;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CBStages_CheckedChanged;
			CheckBox val = _CBStages;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_CBStages = value;
			val = _CBStages;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox CBHighVolume
	{
		[CompilerGenerated]
		get
		{
			return _CBHighVolume;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CBHighVolume_CheckedChanged;
			CheckBox val = _CBHighVolume;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_CBHighVolume = value;
			val = _CBHighVolume;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual CheckBox CBPriceMoves
	{
		[CompilerGenerated]
		get
		{
			return _CBPriceMoves;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CBPriceMoves_CheckedChanged;
			CheckBox val = _CBPriceMoves;
			if (val != null)
			{
				val.CheckedChanged -= eventHandler;
			}
			_CBPriceMoves = value;
			val = _CBPriceMoves;
			if (val != null)
			{
				val.CheckedChanged += eventHandler;
			}
		}
	}

	internal virtual Button StagesHelpButton
	{
		[CompilerGenerated]
		get
		{
			return _StagesHelpButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = StagesHelpButton_Click;
			Button val = _StagesHelpButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_StagesHelpButton = value;
			val = _StagesHelpButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	public FilterForm()
	{
		((Form)this).Closing += FilterForm_Closing;
		((Form)this).Closed += FilterForm_Closed;
		((Form)this).Load += FilterForm_Load;
		((Form)this).Activated += FilterForm_Activated;
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
		//IL_1753: Unknown result type (might be due to invalid IL or missing references)
		//IL_175d: Expected O, but got Unknown
		//IL_21e1: Unknown result type (might be due to invalid IL or missing references)
		//IL_21eb: Expected O, but got Unknown
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(FilterForm));
		DoneButton = new Button();
		RBWidthLess = new RadioButton();
		Label1 = new Label();
		RBWidthBetween = new RadioButton();
		RBWidthMore = new RadioButton();
		GroupWidth = new GroupBox();
		ButtonWidthDefault = new Button();
		NumericWidthHigh = new NumericUpDown();
		NumericWidthMore = new NumericUpDown();
		NumericWidthLow = new NumericUpDown();
		NumericWidthLess = new NumericUpDown();
		GroupPrice = new GroupBox();
		Label4 = new Label();
		ButtonPriceDefault = new Button();
		NumericPriceHigh = new NumericUpDown();
		NumericPriceMore = new NumericUpDown();
		NumericPriceLow = new NumericUpDown();
		NumericPriceLess = new NumericUpDown();
		RBPriceBetween = new RadioButton();
		RBPriceMore = new RadioButton();
		RBPriceLess = new RadioButton();
		GroupHeight = new GroupBox();
		ButtonHeightDefault = new Button();
		Label3 = new Label();
		RBHeightShort = new RadioButton();
		RBHeightEither = new RadioButton();
		RBHeightTall = new RadioButton();
		GroupVolume = new GroupBox();
		Label2 = new Label();
		ButtonVolumeDefault = new Button();
		NumericVolume = new NumericUpDown();
		GroupBkoutDirection = new GroupBox();
		ButtonDirectionDefault = new Button();
		CBBkoutIncludeNone = new CheckBox();
		RBBkoutNoneYet = new RadioButton();
		RBBkoutDown = new RadioButton();
		RBBkoutUpDown = new RadioButton();
		RBBkoutUp = new RadioButton();
		CBMasterSwitch = new CheckBox();
		CBWidth = new CheckBox();
		CBPrice = new CheckBox();
		CBHeight = new CheckBox();
		CBBkoutDirection = new CheckBox();
		CBVolume = new CheckBox();
		Label5 = new Label();
		Label6 = new Label();
		GroupHighVolume = new GroupBox();
		Label7 = new Label();
		NumericHighVolume = new NumericUpDown();
		GroupPriceMoves = new GroupBox();
		Label8 = new Label();
		NumericPriceMoves = new NumericUpDown();
		CBStage1 = new CheckBox();
		GroupStages = new GroupBox();
		CBStage4 = new CheckBox();
		CBStage3 = new CheckBox();
		CBStage2 = new CheckBox();
		CBStages = new CheckBox();
		CBHighVolume = new CheckBox();
		CBPriceMoves = new CheckBox();
		StagesHelpButton = new Button();
		((Control)GroupWidth).SuspendLayout();
		((ISupportInitialize)NumericWidthHigh).BeginInit();
		((ISupportInitialize)NumericWidthMore).BeginInit();
		((ISupportInitialize)NumericWidthLow).BeginInit();
		((ISupportInitialize)NumericWidthLess).BeginInit();
		((Control)GroupPrice).SuspendLayout();
		((ISupportInitialize)NumericPriceHigh).BeginInit();
		((ISupportInitialize)NumericPriceMore).BeginInit();
		((ISupportInitialize)NumericPriceLow).BeginInit();
		((ISupportInitialize)NumericPriceLess).BeginInit();
		((Control)GroupHeight).SuspendLayout();
		((Control)GroupVolume).SuspendLayout();
		((ISupportInitialize)NumericVolume).BeginInit();
		((Control)GroupBkoutDirection).SuspendLayout();
		((Control)GroupHighVolume).SuspendLayout();
		((ISupportInitialize)NumericHighVolume).BeginInit();
		((Control)GroupPriceMoves).SuspendLayout();
		((ISupportInitialize)NumericPriceMoves).BeginInit();
		((Control)GroupStages).SuspendLayout();
		((Control)this).SuspendLayout();
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(612, 388);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(53, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((ButtonBase)RBWidthLess).AutoSize = true;
		RBWidthLess.Checked = true;
		((Control)RBWidthLess).Location = new Point(7, 20);
		((Control)RBWidthLess).Name = "RBWidthLess";
		((Control)RBWidthLess).Size = new Size(71, 17);
		((Control)RBWidthLess).TabIndex = 0;
		RBWidthLess.TabStop = true;
		((ButtonBase)RBWidthLess).Text = "&Less than";
		((ButtonBase)RBWidthLess).UseVisualStyleBackColor = true;
		((Control)Label1).Location = new Point(15, 95);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(135, 40);
		((Control)Label1).TabIndex = 7;
		Label1.Text = "If quotes are intraday, the width will use price bars, otherwise days.";
		((ButtonBase)RBWidthBetween).AutoSize = true;
		((Control)RBWidthBetween).Location = new Point(7, 43);
		((Control)RBWidthBetween).Name = "RBWidthBetween";
		((Control)RBWidthBetween).Size = new Size(67, 17);
		((Control)RBWidthBetween).TabIndex = 2;
		((ButtonBase)RBWidthBetween).Text = "Between";
		((ButtonBase)RBWidthBetween).UseVisualStyleBackColor = true;
		((ButtonBase)RBWidthMore).AutoSize = true;
		((Control)RBWidthMore).Location = new Point(7, 66);
		((Control)RBWidthMore).Name = "RBWidthMore";
		((Control)RBWidthMore).Size = new Size(73, 17);
		((Control)RBWidthMore).TabIndex = 5;
		((ButtonBase)RBWidthMore).Text = "More than";
		((ButtonBase)RBWidthMore).UseVisualStyleBackColor = true;
		((Control)GroupWidth).Controls.Add((Control)(object)ButtonWidthDefault);
		((Control)GroupWidth).Controls.Add((Control)(object)Label1);
		((Control)GroupWidth).Controls.Add((Control)(object)NumericWidthHigh);
		((Control)GroupWidth).Controls.Add((Control)(object)NumericWidthMore);
		((Control)GroupWidth).Controls.Add((Control)(object)NumericWidthLow);
		((Control)GroupWidth).Controls.Add((Control)(object)NumericWidthLess);
		((Control)GroupWidth).Controls.Add((Control)(object)RBWidthBetween);
		((Control)GroupWidth).Controls.Add((Control)(object)RBWidthMore);
		((Control)GroupWidth).Controls.Add((Control)(object)RBWidthLess);
		((Control)GroupWidth).Location = new Point(12, 12);
		((Control)GroupWidth).Name = "GroupWidth";
		((Control)GroupWidth).Size = new Size(240, 141);
		((Control)GroupWidth).TabIndex = 1;
		GroupWidth.TabStop = false;
		GroupWidth.Text = "Pattern Width";
		((Control)ButtonWidthDefault).Anchor = (AnchorStyles)10;
		((Control)ButtonWidthDefault).Location = new Point(167, 95);
		((Control)ButtonWidthDefault).Name = "ButtonWidthDefault";
		((Control)ButtonWidthDefault).Size = new Size(61, 23);
		((Control)ButtonWidthDefault).TabIndex = 8;
		((ButtonBase)ButtonWidthDefault).Text = "&Default";
		((ButtonBase)ButtonWidthDefault).UseVisualStyleBackColor = true;
		((Control)NumericWidthHigh).Location = new Point(167, 40);
		NumericWidthHigh.Maximum = new decimal(new int[4] { 180, 0, 0, 0 });
		NumericWidthHigh.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)NumericWidthHigh).Name = "NumericWidthHigh";
		((Control)NumericWidthHigh).Size = new Size(49, 20);
		((Control)NumericWidthHigh).TabIndex = 4;
		NumericWidthHigh.Value = new decimal(new int[4] { 180, 0, 0, 0 });
		((Control)NumericWidthMore).Location = new Point(87, 60);
		NumericWidthMore.Maximum = new decimal(new int[4] { 180, 0, 0, 0 });
		((Control)NumericWidthMore).Name = "NumericWidthMore";
		((Control)NumericWidthMore).Size = new Size(49, 20);
		((Control)NumericWidthMore).TabIndex = 6;
		((Control)NumericWidthLow).Location = new Point(87, 40);
		NumericWidthLow.Maximum = new decimal(new int[4] { 180, 0, 0, 0 });
		((Control)NumericWidthLow).Name = "NumericWidthLow";
		((Control)NumericWidthLow).Size = new Size(49, 20);
		((Control)NumericWidthLow).TabIndex = 3;
		((Control)NumericWidthLess).Location = new Point(87, 20);
		NumericWidthLess.Maximum = new decimal(new int[4] { 180, 0, 0, 0 });
		NumericWidthLess.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)NumericWidthLess).Name = "NumericWidthLess";
		((Control)NumericWidthLess).Size = new Size(49, 20);
		((Control)NumericWidthLess).TabIndex = 1;
		NumericWidthLess.Value = new decimal(new int[4] { 180, 0, 0, 0 });
		((Control)GroupPrice).Controls.Add((Control)(object)Label4);
		((Control)GroupPrice).Controls.Add((Control)(object)ButtonPriceDefault);
		((Control)GroupPrice).Controls.Add((Control)(object)NumericPriceHigh);
		((Control)GroupPrice).Controls.Add((Control)(object)NumericPriceMore);
		((Control)GroupPrice).Controls.Add((Control)(object)NumericPriceLow);
		((Control)GroupPrice).Controls.Add((Control)(object)NumericPriceLess);
		((Control)GroupPrice).Controls.Add((Control)(object)RBPriceBetween);
		((Control)GroupPrice).Controls.Add((Control)(object)RBPriceMore);
		((Control)GroupPrice).Controls.Add((Control)(object)RBPriceLess);
		((Control)GroupPrice).Location = new Point(12, 159);
		((Control)GroupPrice).Name = "GroupPrice";
		((Control)GroupPrice).Size = new Size(240, 126);
		((Control)GroupPrice).TabIndex = 2;
		GroupPrice.TabStop = false;
		GroupPrice.Text = "Pattern Price";
		((Control)Label4).Location = new Point(15, 89);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(142, 29);
		((Control)Label4).TabIndex = 7;
		Label4.Text = "Based on the last close in the pattern.";
		((Control)ButtonPriceDefault).Anchor = (AnchorStyles)10;
		((Control)ButtonPriceDefault).Location = new Point(167, 89);
		((Control)ButtonPriceDefault).Name = "ButtonPriceDefault";
		((Control)ButtonPriceDefault).Size = new Size(61, 23);
		((Control)ButtonPriceDefault).TabIndex = 8;
		((ButtonBase)ButtonPriceDefault).Text = "&Default";
		((ButtonBase)ButtonPriceDefault).UseVisualStyleBackColor = true;
		((Control)NumericPriceHigh).Location = new Point(158, 43);
		NumericPriceHigh.Maximum = new decimal(new int[4] { 1000000, 0, 0, 0 });
		NumericPriceHigh.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)NumericPriceHigh).Name = "NumericPriceHigh";
		((Control)NumericPriceHigh).Size = new Size(74, 20);
		((Control)NumericPriceHigh).TabIndex = 4;
		NumericPriceHigh.Value = new decimal(new int[4] { 100000, 0, 0, 0 });
		((Control)NumericPriceMore).Location = new Point(87, 66);
		NumericPriceMore.Maximum = new decimal(new int[4] { 1000000, 0, 0, 0 });
		((Control)NumericPriceMore).Name = "NumericPriceMore";
		((Control)NumericPriceMore).Size = new Size(65, 20);
		((Control)NumericPriceMore).TabIndex = 6;
		NumericPriceMore.Value = new decimal(new int[4] { 5, 0, 0, 0 });
		((Control)NumericPriceLow).Location = new Point(87, 43);
		NumericPriceLow.Maximum = new decimal(new int[4] { 180, 0, 0, 0 });
		((Control)NumericPriceLow).Name = "NumericPriceLow";
		((Control)NumericPriceLow).Size = new Size(65, 20);
		((Control)NumericPriceLow).TabIndex = 3;
		NumericPriceLow.Value = new decimal(new int[4] { 5, 0, 0, 0 });
		((Control)NumericPriceLess).Location = new Point(87, 20);
		NumericPriceLess.Maximum = new decimal(new int[4] { 1000000, 0, 0, 0 });
		((Control)NumericPriceLess).Name = "NumericPriceLess";
		((Control)NumericPriceLess).Size = new Size(65, 20);
		((Control)NumericPriceLess).TabIndex = 1;
		NumericPriceLess.Value = new decimal(new int[4] { 500, 0, 0, 0 });
		((ButtonBase)RBPriceBetween).AutoSize = true;
		((Control)RBPriceBetween).Location = new Point(7, 43);
		((Control)RBPriceBetween).Name = "RBPriceBetween";
		((Control)RBPriceBetween).Size = new Size(67, 17);
		((Control)RBPriceBetween).TabIndex = 2;
		((ButtonBase)RBPriceBetween).Text = "Between";
		((ButtonBase)RBPriceBetween).UseVisualStyleBackColor = true;
		((ButtonBase)RBPriceMore).AutoSize = true;
		RBPriceMore.Checked = true;
		((Control)RBPriceMore).Location = new Point(7, 66);
		((Control)RBPriceMore).Name = "RBPriceMore";
		((Control)RBPriceMore).Size = new Size(73, 17);
		((Control)RBPriceMore).TabIndex = 5;
		RBPriceMore.TabStop = true;
		((ButtonBase)RBPriceMore).Text = "More than";
		((ButtonBase)RBPriceMore).UseVisualStyleBackColor = true;
		((ButtonBase)RBPriceLess).AutoSize = true;
		((Control)RBPriceLess).Location = new Point(7, 20);
		((Control)RBPriceLess).Name = "RBPriceLess";
		((Control)RBPriceLess).Size = new Size(71, 17);
		((Control)RBPriceLess).TabIndex = 0;
		((ButtonBase)RBPriceLess).Text = "&Less than";
		((ButtonBase)RBPriceLess).UseVisualStyleBackColor = true;
		((Control)GroupHeight).Controls.Add((Control)(object)ButtonHeightDefault);
		((Control)GroupHeight).Controls.Add((Control)(object)Label3);
		((Control)GroupHeight).Controls.Add((Control)(object)RBHeightShort);
		((Control)GroupHeight).Controls.Add((Control)(object)RBHeightEither);
		((Control)GroupHeight).Controls.Add((Control)(object)RBHeightTall);
		((Control)GroupHeight).Location = new Point(271, 12);
		((Control)GroupHeight).Name = "GroupHeight";
		((Control)GroupHeight).Size = new Size(192, 141);
		((Control)GroupHeight).TabIndex = 4;
		GroupHeight.TabStop = false;
		GroupHeight.Text = "Pattern Height";
		((Control)ButtonHeightDefault).Anchor = (AnchorStyles)10;
		((Control)ButtonHeightDefault).Location = new Point(110, 60);
		((Control)ButtonHeightDefault).Name = "ButtonHeightDefault";
		((Control)ButtonHeightDefault).Size = new Size(61, 23);
		((Control)ButtonHeightDefault).TabIndex = 3;
		((ButtonBase)ButtonHeightDefault).Text = "&Default";
		((ButtonBase)ButtonHeightDefault).UseVisualStyleBackColor = true;
		((Control)Label3).Location = new Point(6, 98);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(178, 40);
		((Control)Label3).TabIndex = 4;
		Label3.Text = "Based on last price in the chart pattern and median height for similar patterns.";
		((ButtonBase)RBHeightShort).AutoSize = true;
		((Control)RBHeightShort).Location = new Point(7, 43);
		((Control)RBHeightShort).Name = "RBHeightShort";
		((Control)RBHeightShort).Size = new Size(50, 17);
		((Control)RBHeightShort).TabIndex = 1;
		((ButtonBase)RBHeightShort).Text = "Short";
		((ButtonBase)RBHeightShort).UseVisualStyleBackColor = true;
		((ButtonBase)RBHeightEither).AutoSize = true;
		RBHeightEither.Checked = true;
		((Control)RBHeightEither).Location = new Point(7, 66);
		((Control)RBHeightEither).Name = "RBHeightEither";
		((Control)RBHeightEither).Size = new Size(52, 17);
		((Control)RBHeightEither).TabIndex = 2;
		RBHeightEither.TabStop = true;
		((ButtonBase)RBHeightEither).Text = "Either";
		((ButtonBase)RBHeightEither).UseVisualStyleBackColor = true;
		((ButtonBase)RBHeightTall).AutoSize = true;
		((Control)RBHeightTall).Location = new Point(7, 20);
		((Control)RBHeightTall).Name = "RBHeightTall";
		((Control)RBHeightTall).Size = new Size(42, 17);
		((Control)RBHeightTall).TabIndex = 0;
		((ButtonBase)RBHeightTall).Text = "&Tall";
		((ButtonBase)RBHeightTall).UseVisualStyleBackColor = true;
		((Control)GroupVolume).Controls.Add((Control)(object)Label2);
		((Control)GroupVolume).Controls.Add((Control)(object)ButtonVolumeDefault);
		((Control)GroupVolume).Controls.Add((Control)(object)NumericVolume);
		((Control)GroupVolume).Location = new Point(271, 157);
		((Control)GroupVolume).Name = "GroupVolume";
		((Control)GroupVolume).Size = new Size(192, 88);
		((Control)GroupVolume).TabIndex = 5;
		GroupVolume.TabStop = false;
		GroupVolume.Text = "Volume";
		((Control)Label2).Location = new Point(6, 25);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(98, 40);
		((Control)Label2).TabIndex = 0;
		Label2.Text = "Minimum 3-month average volume is above this:";
		((Control)ButtonVolumeDefault).Anchor = (AnchorStyles)10;
		((Control)ButtonVolumeDefault).Location = new Point(110, 59);
		((Control)ButtonVolumeDefault).Name = "ButtonVolumeDefault";
		((Control)ButtonVolumeDefault).Size = new Size(61, 23);
		((Control)ButtonVolumeDefault).TabIndex = 2;
		((ButtonBase)ButtonVolumeDefault).Text = "&Default";
		((ButtonBase)ButtonVolumeDefault).UseVisualStyleBackColor = true;
		((Control)NumericVolume).Location = new Point(110, 33);
		NumericVolume.Maximum = new decimal(new int[4] { 1409065408, 2, 0, 0 });
		((Control)NumericVolume).Name = "NumericVolume";
		((Control)NumericVolume).Size = new Size(74, 20);
		((Control)NumericVolume).TabIndex = 1;
		NumericVolume.Value = new decimal(new int[4] { 100000, 0, 0, 0 });
		((Control)GroupBkoutDirection).Controls.Add((Control)(object)ButtonDirectionDefault);
		((Control)GroupBkoutDirection).Controls.Add((Control)(object)CBBkoutIncludeNone);
		((Control)GroupBkoutDirection).Controls.Add((Control)(object)RBBkoutNoneYet);
		((Control)GroupBkoutDirection).Controls.Add((Control)(object)RBBkoutDown);
		((Control)GroupBkoutDirection).Controls.Add((Control)(object)RBBkoutUpDown);
		((Control)GroupBkoutDirection).Controls.Add((Control)(object)RBBkoutUp);
		((Control)GroupBkoutDirection).Location = new Point(12, 291);
		((Control)GroupBkoutDirection).Name = "GroupBkoutDirection";
		((Control)GroupBkoutDirection).Size = new Size(240, 123);
		((Control)GroupBkoutDirection).TabIndex = 3;
		GroupBkoutDirection.TabStop = false;
		GroupBkoutDirection.Text = "Breakout Direction";
		((Control)ButtonDirectionDefault).Anchor = (AnchorStyles)10;
		((Control)ButtonDirectionDefault).Location = new Point(167, 83);
		((Control)ButtonDirectionDefault).Name = "ButtonDirectionDefault";
		((Control)ButtonDirectionDefault).Size = new Size(61, 23);
		((Control)ButtonDirectionDefault).TabIndex = 5;
		((ButtonBase)ButtonDirectionDefault).Text = "&Default";
		((ButtonBase)ButtonDirectionDefault).UseVisualStyleBackColor = true;
		((ButtonBase)CBBkoutIncludeNone).AutoSize = true;
		CBBkoutIncludeNone.Checked = true;
		CBBkoutIncludeNone.CheckState = (CheckState)1;
		((Control)CBBkoutIncludeNone).Location = new Point(96, 21);
		((Control)CBBkoutIncludeNone).Name = "CBBkoutIncludeNone";
		((Control)CBBkoutIncludeNone).Size = new Size(138, 17);
		((Control)CBBkoutIncludeNone).TabIndex = 1;
		((ButtonBase)CBBkoutIncludeNone).Text = "Include no breakout yet";
		((ButtonBase)CBBkoutIncludeNone).UseVisualStyleBackColor = true;
		((ButtonBase)RBBkoutNoneYet).AutoSize = true;
		((Control)RBBkoutNoneYet).Location = new Point(7, 89);
		((Control)RBBkoutNoneYet).Name = "RBBkoutNoneYet";
		((Control)RBBkoutNoneYet).Size = new Size(101, 17);
		((Control)RBBkoutNoneYet).TabIndex = 4;
		((ButtonBase)RBBkoutNoneYet).Text = "&No breakout yet";
		((ButtonBase)RBBkoutNoneYet).UseVisualStyleBackColor = true;
		((ButtonBase)RBBkoutDown).AutoSize = true;
		((Control)RBBkoutDown).Location = new Point(7, 43);
		((Control)RBBkoutDown).Name = "RBBkoutDown";
		((Control)RBBkoutDown).Size = new Size(75, 17);
		((Control)RBBkoutDown).TabIndex = 2;
		((ButtonBase)RBBkoutDown).Text = "&Down only";
		((ButtonBase)RBBkoutDown).UseVisualStyleBackColor = true;
		((ButtonBase)RBBkoutUpDown).AutoSize = true;
		RBBkoutUpDown.Checked = true;
		((Control)RBBkoutUpDown).Location = new Point(7, 66);
		((Control)RBBkoutUpDown).Name = "RBBkoutUpDown";
		((Control)RBBkoutUpDown).Size = new Size(103, 17);
		((Control)RBBkoutUpDown).TabIndex = 3;
		RBBkoutUpDown.TabStop = true;
		((ButtonBase)RBBkoutUpDown).Text = "&Both up or down";
		((ButtonBase)RBBkoutUpDown).UseVisualStyleBackColor = true;
		((ButtonBase)RBBkoutUp).AutoSize = true;
		((Control)RBBkoutUp).Location = new Point(7, 20);
		((Control)RBBkoutUp).Name = "RBBkoutUp";
		((Control)RBBkoutUp).Size = new Size(61, 17);
		((Control)RBBkoutUp).TabIndex = 0;
		((ButtonBase)RBBkoutUp).Text = "&Up only";
		((ButtonBase)RBBkoutUp).UseVisualStyleBackColor = true;
		((ButtonBase)CBMasterSwitch).AutoSize = true;
		((Control)CBMasterSwitch).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)CBMasterSwitch).Location = new Point(271, 397);
		((Control)CBMasterSwitch).Name = "CBMasterSwitch";
		((Control)CBMasterSwitch).Size = new Size(184, 17);
		((Control)CBMasterSwitch).TabIndex = 12;
		((ButtonBase)CBMasterSwitch).Text = "Use filters ONLY if checked";
		((ButtonBase)CBMasterSwitch).UseVisualStyleBackColor = true;
		((ButtonBase)CBWidth).AutoSize = true;
		((Control)CBWidth).Location = new Point(271, 292);
		((Control)CBWidth).Name = "CBWidth";
		((Control)CBWidth).Size = new Size(88, 17);
		((Control)CBWidth).TabIndex = 7;
		((ButtonBase)CBWidth).Text = "&Pattern width";
		((ButtonBase)CBWidth).UseVisualStyleBackColor = true;
		((ButtonBase)CBPrice).AutoSize = true;
		((Control)CBPrice).Location = new Point(271, 313);
		((Control)CBPrice).Name = "CBPrice";
		((Control)CBPrice).Size = new Size(50, 17);
		((Control)CBPrice).TabIndex = 8;
		((ButtonBase)CBPrice).Text = "&Price";
		((ButtonBase)CBPrice).UseVisualStyleBackColor = true;
		((ButtonBase)CBHeight).AutoSize = true;
		((Control)CBHeight).Location = new Point(271, 355);
		((Control)CBHeight).Name = "CBHeight";
		((Control)CBHeight).Size = new Size(92, 17);
		((Control)CBHeight).TabIndex = 10;
		((ButtonBase)CBHeight).Text = "Pattern &height";
		((ButtonBase)CBHeight).UseVisualStyleBackColor = true;
		((ButtonBase)CBBkoutDirection).AutoSize = true;
		((Control)CBBkoutDirection).Location = new Point(271, 334);
		((Control)CBBkoutDirection).Name = "CBBkoutDirection";
		((Control)CBBkoutDirection).Size = new Size(112, 17);
		((Control)CBBkoutDirection).TabIndex = 9;
		((ButtonBase)CBBkoutDirection).Text = "&Breakout direction";
		((ButtonBase)CBBkoutDirection).UseVisualStyleBackColor = true;
		((ButtonBase)CBVolume).AutoSize = true;
		((Control)CBVolume).Location = new Point(271, 376);
		((Control)CBVolume).Name = "CBVolume";
		((Control)CBVolume).Size = new Size(61, 17);
		((Control)CBVolume).TabIndex = 11;
		((ButtonBase)CBVolume).Text = "&Volume";
		((ButtonBase)CBVolume).UseVisualStyleBackColor = true;
		Label5.AutoSize = true;
		((Control)Label5).ForeColor = Color.FromArgb(0, 0, 192);
		((Control)Label5).Location = new Point(268, 260);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(365, 13);
		((Control)Label5).TabIndex = 6;
		Label5.Text = "Click the filter(s) you wish to use, then click 'Use filters...' (bottom checkbox).";
		((Control)Label6).ForeColor = Color.Black;
		((Control)Label6).Location = new Point(12, 424);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(688, 39);
		((Control)Label6).TabIndex = 13;
		Label6.Text = componentResourceManager.GetString("Label6.Text");
		((Control)GroupHighVolume).Controls.Add((Control)(object)Label7);
		((Control)GroupHighVolume).Controls.Add((Control)(object)NumericHighVolume);
		((Control)GroupHighVolume).Location = new Point(488, 78);
		((Control)GroupHighVolume).Name = "GroupHighVolume";
		((Control)GroupHighVolume).Size = new Size(204, 88);
		((Control)GroupHighVolume).TabIndex = 15;
		GroupHighVolume.TabStop = false;
		GroupHighVolume.Text = "High Volume";
		((Control)Label7).Location = new Point(6, 25);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(97, 55);
		((Control)Label7).TabIndex = 0;
		Label7.Text = "Number of times recent volume is above 3-month average.";
		NumericHighVolume.DecimalPlaces = 1;
		((Control)NumericHighVolume).Location = new Point(139, 31);
		NumericHighVolume.Maximum = new decimal(new int[4] { 10, 0, 0, 0 });
		NumericHighVolume.Minimum = new decimal(new int[4] { 1, 0, 0, 0 });
		((Control)NumericHighVolume).Name = "NumericHighVolume";
		((Control)NumericHighVolume).Size = new Size(48, 20);
		((Control)NumericHighVolume).TabIndex = 1;
		NumericHighVolume.Value = new decimal(new int[4] { 2, 0, 0, 0 });
		((Control)GroupPriceMoves).Controls.Add((Control)(object)Label8);
		((Control)GroupPriceMoves).Controls.Add((Control)(object)NumericPriceMoves);
		((Control)GroupPriceMoves).Location = new Point(488, 12);
		((Control)GroupPriceMoves).Name = "GroupPriceMoves";
		((Control)GroupPriceMoves).Size = new Size(204, 60);
		((Control)GroupPriceMoves).TabIndex = 14;
		GroupPriceMoves.TabStop = false;
		GroupPriceMoves.Text = "Price Moves";
		((Control)Label8).Location = new Point(15, 16);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(125, 44);
		((Control)Label8).TabIndex = 0;
		Label8.Text = "Percentage price is above or below prior day's close.";
		((Control)NumericPriceMoves).Location = new Point(146, 22);
		NumericPriceMoves.Maximum = new decimal(new int[4] { 99, 0, 0, 0 });
		NumericPriceMoves.Minimum = new decimal(new int[4] { 99, 0, 0, -2147483648 });
		((Control)NumericPriceMoves).Name = "NumericPriceMoves";
		((Control)NumericPriceMoves).Size = new Size(41, 20);
		((Control)NumericPriceMoves).TabIndex = 1;
		NumericPriceMoves.Value = new decimal(new int[4] { 5, 0, 0, 0 });
		((ButtonBase)CBStage1).AutoSize = true;
		((Control)CBStage1).Location = new Point(31, 19);
		((Control)CBStage1).Name = "CBStage1";
		((Control)CBStage1).Size = new Size(63, 17);
		((Control)CBStage1).TabIndex = 0;
		((ButtonBase)CBStage1).Text = "&Stage 1";
		((ButtonBase)CBStage1).UseVisualStyleBackColor = true;
		((Control)GroupStages).Controls.Add((Control)(object)CBStage4);
		((Control)GroupStages).Controls.Add((Control)(object)CBStage3);
		((Control)GroupStages).Controls.Add((Control)(object)CBStage2);
		((Control)GroupStages).Controls.Add((Control)(object)CBStage1);
		((Control)GroupStages).Location = new Point(488, 182);
		((Control)GroupStages).Name = "GroupStages";
		((Control)GroupStages).Size = new Size(204, 70);
		((Control)GroupStages).TabIndex = 16;
		GroupStages.TabStop = false;
		GroupStages.Text = "Weinstein Stages";
		((ButtonBase)CBStage4).AutoSize = true;
		((Control)CBStage4).Location = new Point(100, 42);
		((Control)CBStage4).Name = "CBStage4";
		((Control)CBStage4).Size = new Size(63, 17);
		((Control)CBStage4).TabIndex = 3;
		((ButtonBase)CBStage4).Text = "&Stage 4";
		((ButtonBase)CBStage4).UseVisualStyleBackColor = true;
		((ButtonBase)CBStage3).AutoSize = true;
		((Control)CBStage3).Location = new Point(100, 19);
		((Control)CBStage3).Name = "CBStage3";
		((Control)CBStage3).Size = new Size(63, 17);
		((Control)CBStage3).TabIndex = 1;
		((ButtonBase)CBStage3).Text = "&Stage 3";
		((ButtonBase)CBStage3).UseVisualStyleBackColor = true;
		((ButtonBase)CBStage2).AutoSize = true;
		((Control)CBStage2).Location = new Point(31, 42);
		((Control)CBStage2).Name = "CBStage2";
		((Control)CBStage2).Size = new Size(63, 17);
		((Control)CBStage2).TabIndex = 2;
		((ButtonBase)CBStage2).Text = "&Stage 2";
		((ButtonBase)CBStage2).UseVisualStyleBackColor = true;
		((ButtonBase)CBStages).AutoSize = true;
		((Control)CBStages).Location = new Point(488, 334);
		((Control)CBStages).Name = "CBStages";
		((Control)CBStages).Size = new Size(107, 17);
		((Control)CBStages).TabIndex = 19;
		((ButtonBase)CBStages).Text = "&Weinstein stages";
		((ButtonBase)CBStages).UseVisualStyleBackColor = true;
		((ButtonBase)CBHighVolume).AutoSize = true;
		((Control)CBHighVolume).Location = new Point(488, 313);
		((Control)CBHighVolume).Name = "CBHighVolume";
		((Control)CBHighVolume).Size = new Size(85, 17);
		((Control)CBHighVolume).TabIndex = 18;
		((ButtonBase)CBHighVolume).Text = "&High volume";
		((ButtonBase)CBHighVolume).UseVisualStyleBackColor = true;
		((ButtonBase)CBPriceMoves).AutoSize = true;
		((Control)CBPriceMoves).Location = new Point(488, 292);
		((Control)CBPriceMoves).Name = "CBPriceMoves";
		((Control)CBPriceMoves).Size = new Size(84, 17);
		((Control)CBPriceMoves).TabIndex = 17;
		((ButtonBase)CBPriceMoves).Text = "&Price moves";
		((ButtonBase)CBPriceMoves).UseVisualStyleBackColor = true;
		((Control)StagesHelpButton).Font = new Font("Microsoft Sans Serif", 6f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)StagesHelpButton).Location = new Point(601, 334);
		((Control)StagesHelpButton).Name = "StagesHelpButton";
		((Control)StagesHelpButton).Size = new Size(20, 20);
		((Control)StagesHelpButton).TabIndex = 0;
		((ButtonBase)StagesHelpButton).Text = "?";
		((ButtonBase)StagesHelpButton).UseVisualStyleBackColor = true;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(702, 473);
		((Control)this).Controls.Add((Control)(object)StagesHelpButton);
		((Control)this).Controls.Add((Control)(object)CBStages);
		((Control)this).Controls.Add((Control)(object)CBHighVolume);
		((Control)this).Controls.Add((Control)(object)CBPriceMoves);
		((Control)this).Controls.Add((Control)(object)GroupStages);
		((Control)this).Controls.Add((Control)(object)GroupPriceMoves);
		((Control)this).Controls.Add((Control)(object)GroupHighVolume);
		((Control)this).Controls.Add((Control)(object)Label6);
		((Control)this).Controls.Add((Control)(object)Label5);
		((Control)this).Controls.Add((Control)(object)CBVolume);
		((Control)this).Controls.Add((Control)(object)CBHeight);
		((Control)this).Controls.Add((Control)(object)CBBkoutDirection);
		((Control)this).Controls.Add((Control)(object)CBPrice);
		((Control)this).Controls.Add((Control)(object)CBWidth);
		((Control)this).Controls.Add((Control)(object)CBMasterSwitch);
		((Control)this).Controls.Add((Control)(object)GroupBkoutDirection);
		((Control)this).Controls.Add((Control)(object)GroupVolume);
		((Control)this).Controls.Add((Control)(object)GroupHeight);
		((Control)this).Controls.Add((Control)(object)GroupPrice);
		((Control)this).Controls.Add((Control)(object)GroupWidth);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Control)this).Name = "FilterForm";
		((Form)this).StartPosition = (FormStartPosition)1;
		((Form)this).Text = "Filter Form";
		((Control)GroupWidth).ResumeLayout(false);
		((Control)GroupWidth).PerformLayout();
		((ISupportInitialize)NumericWidthHigh).EndInit();
		((ISupportInitialize)NumericWidthMore).EndInit();
		((ISupportInitialize)NumericWidthLow).EndInit();
		((ISupportInitialize)NumericWidthLess).EndInit();
		((Control)GroupPrice).ResumeLayout(false);
		((Control)GroupPrice).PerformLayout();
		((ISupportInitialize)NumericPriceHigh).EndInit();
		((ISupportInitialize)NumericPriceMore).EndInit();
		((ISupportInitialize)NumericPriceLow).EndInit();
		((ISupportInitialize)NumericPriceLess).EndInit();
		((Control)GroupHeight).ResumeLayout(false);
		((Control)GroupHeight).PerformLayout();
		((Control)GroupVolume).ResumeLayout(false);
		((ISupportInitialize)NumericVolume).EndInit();
		((Control)GroupBkoutDirection).ResumeLayout(false);
		((Control)GroupBkoutDirection).PerformLayout();
		((Control)GroupHighVolume).ResumeLayout(false);
		((ISupportInitialize)NumericHighVolume).EndInit();
		((Control)GroupPriceMoves).ResumeLayout(false);
		((ISupportInitialize)NumericPriceMoves).EndInit();
		((Control)GroupStages).ResumeLayout(false);
		((Control)GroupStages).PerformLayout();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void FilterForm_Closing(object sender, CancelEventArgs e)
	{
		//IL_007c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0081: Invalid comparison between I4 and Unknown
		if ((CBWidth.Checked | CBBkoutDirection.Checked | CBVolume.Checked | CBHeight.Checked | CBPrice.Checked | CBPriceMoves.Checked | CBHighVolume.Checked | CBStages.Checked) && !CBMasterSwitch.Checked && 6 == (int)MessageBox.Show("The 'Use filters ONLY if checked' check box is NOT checked so you won't be filtering anything. Did you want me to check it?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32))
		{
			CBMasterSwitch.Checked = true;
		}
	}

	private void FilterForm_Closed(object sender, EventArgs e)
	{
		WriteConfigFile();
	}

	private void FilterForm_Load(object sender, EventArgs e)
	{
		//IL_0007: Unknown result type (might be due to invalid IL or missing references)
		//IL_000c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0017: Unknown result type (might be due to invalid IL or missing references)
		//IL_0022: Unknown result type (might be due to invalid IL or missing references)
		//IL_002d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0034: Unknown result type (might be due to invalid IL or missing references)
		//IL_0045: Unknown result type (might be due to invalid IL or missing references)
		//IL_0056: Unknown result type (might be due to invalid IL or missing references)
		//IL_0067: Unknown result type (might be due to invalid IL or missing references)
		//IL_0078: Unknown result type (might be due to invalid IL or missing references)
		//IL_0089: Unknown result type (might be due to invalid IL or missing references)
		//IL_009a: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ab: Unknown result type (might be due to invalid IL or missing references)
		//IL_00bc: Unknown result type (might be due to invalid IL or missing references)
		//IL_00cd: Unknown result type (might be due to invalid IL or missing references)
		//IL_00de: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ef: Unknown result type (might be due to invalid IL or missing references)
		//IL_0100: Unknown result type (might be due to invalid IL or missing references)
		//IL_0111: Unknown result type (might be due to invalid IL or missing references)
		//IL_0122: Unknown result type (might be due to invalid IL or missing references)
		//IL_0133: Unknown result type (might be due to invalid IL or missing references)
		//IL_0144: Unknown result type (might be due to invalid IL or missing references)
		//IL_0155: Unknown result type (might be due to invalid IL or missing references)
		//IL_0166: Unknown result type (might be due to invalid IL or missing references)
		//IL_0177: Unknown result type (might be due to invalid IL or missing references)
		//IL_0188: Unknown result type (might be due to invalid IL or missing references)
		//IL_0199: Unknown result type (might be due to invalid IL or missing references)
		//IL_01aa: Unknown result type (might be due to invalid IL or missing references)
		//IL_01bb: Unknown result type (might be due to invalid IL or missing references)
		//IL_01cc: Unknown result type (might be due to invalid IL or missing references)
		//IL_01dd: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ee: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ff: Unknown result type (might be due to invalid IL or missing references)
		//IL_0210: Unknown result type (might be due to invalid IL or missing references)
		//IL_0221: Unknown result type (might be due to invalid IL or missing references)
		//IL_0232: Unknown result type (might be due to invalid IL or missing references)
		//IL_0243: Unknown result type (might be due to invalid IL or missing references)
		//IL_0254: Unknown result type (might be due to invalid IL or missing references)
		//IL_0265: Unknown result type (might be due to invalid IL or missing references)
		//IL_0276: Unknown result type (might be due to invalid IL or missing references)
		//IL_0287: Unknown result type (might be due to invalid IL or missing references)
		//IL_0298: Unknown result type (might be due to invalid IL or missing references)
		//IL_02a9: Unknown result type (might be due to invalid IL or missing references)
		//IL_02ba: Unknown result type (might be due to invalid IL or missing references)
		//IL_02cb: Unknown result type (might be due to invalid IL or missing references)
		//IL_02dc: Unknown result type (might be due to invalid IL or missing references)
		//IL_02ed: Unknown result type (might be due to invalid IL or missing references)
		//IL_02fe: Unknown result type (might be due to invalid IL or missing references)
		//IL_030f: Unknown result type (might be due to invalid IL or missing references)
		LockFlag = true;
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)RBWidthLess, "Pattern width less than the adjacent number of days or price bars.");
		val.SetToolTip((Control)(object)RBWidthBetween, "Pattern width between the two adjacent number of days or price bars.");
		val.SetToolTip((Control)(object)RBWidthMore, "Pattern width more than the adjacent number of days or price bars.");
		val.SetToolTip((Control)(object)NumericWidthLess, "The maximum width of the pattern you'd like to find (range: 1-180).");
		val.SetToolTip((Control)(object)NumericWidthMore, "The minimum width of the pattern you'd like to find (in days or price bars.");
		val.SetToolTip((Control)(object)NumericWidthHigh, "Pattern width: the high end of the range to allow.");
		val.SetToolTip((Control)(object)NumericWidthLow, "Pattern width: the low end of the range to allow.");
		val.SetToolTip((Control)(object)RBPriceLess, "The maximum pattern price you'd like to find (range: up to 1,000,000).");
		val.SetToolTip((Control)(object)RBPriceBetween, "Find a stock pattern priced between the adjacent text boxes.");
		val.SetToolTip((Control)(object)RBPriceMore, "The minimum pattern price you'd like to find (range up to 1,000,000).");
		val.SetToolTip((Control)(object)NumericPriceLess, "The maximum pattern price you'd like to find (range: up to 1,000,000).");
		val.SetToolTip((Control)(object)NumericPriceMore, "The minimum patternprice you'd like to find, up to 1,000,000.");
		val.SetToolTip((Control)(object)NumericPriceHigh, "Pattern price: the high end of the range to allow, up to 1 million.");
		val.SetToolTip((Control)(object)NumericPriceLow, "Pattern price: the low end of the range to allow.");
		val.SetToolTip((Control)(object)ButtonWidthDefault, "Restore the factory settings.");
		val.SetToolTip((Control)(object)ButtonPriceDefault, "Restore the factory settings.");
		val.SetToolTip((Control)(object)ButtonDirectionDefault, "Restore the factory settings.");
		val.SetToolTip((Control)(object)ButtonHeightDefault, "Restore the factory settings.");
		val.SetToolTip((Control)(object)ButtonVolumeDefault, "Restore the factory settings.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)RBBkoutUp, "Find patterns with upward breakouts.");
		val.SetToolTip((Control)(object)RBBkoutDown, "Find patterns with downward breakouts.");
		val.SetToolTip((Control)(object)RBBkoutUpDown, "Find patterns with up and down breakouts.");
		val.SetToolTip((Control)(object)RBBkoutNoneYet, "Find patterns still waiting for a breakout.");
		val.SetToolTip((Control)(object)CBBkoutIncludeNone, "Include pattens will waiting for a breakout.");
		val.SetToolTip((Control)(object)RBHeightTall, "Find only tall patterns (those with a last price higher than the median for this pattern type).");
		val.SetToolTip((Control)(object)RBHeightShort, "Find only short patterns (those with a last price lower than the median for this pattern type).");
		val.SetToolTip((Control)(object)RBHeightEither, "Disregard pattern height.");
		val.SetToolTip((Control)(object)NumericVolume, "Find patterns with at least a minimum volume. The 3-month average is used.");
		val.SetToolTip((Control)(object)CBWidth, "When checked, include pattern width when searching for patterns.");
		val.SetToolTip((Control)(object)CBPrice, "When checked, include pattern price when searching for patterns.");
		val.SetToolTip((Control)(object)CBBkoutDirection, "When checked, include pattern breakout direction when searching for patterns.");
		val.SetToolTip((Control)(object)CBHeight, "When checked, include pattern height when searching for patterns.");
		val.SetToolTip((Control)(object)CBVolume, "When checked, include pattern volume when searching for patterns.");
		val.SetToolTip((Control)(object)CBMasterSwitch, "When checked, allow use of filters. If not checked, patterns won't be filtered.");
		val.SetToolTip((Control)(object)NumericPriceMoves, "Percentage from (plus/minus) 1 to 99 for close-to-close price change from prior day, using more recent quote.");
		val.SetToolTip((Control)(object)NumericHighVolume, "Multiplier of unusually high volume, from 1 to 10 using more recent quote versus prior 3 months.");
		val.SetToolTip((Control)(object)CBStage1, "Check to look for stocks in stage 1.");
		val.SetToolTip((Control)(object)CBStage2, "Check to look for stocks in stage 2.");
		val.SetToolTip((Control)(object)CBStage3, "Check to look for stocks in stage 3.");
		val.SetToolTip((Control)(object)CBStage4, "Check to look for stocks in stage 4.");
		val.SetToolTip((Control)(object)CBPriceMoves, "Check to look for a big price change in the two most recent price bars.");
		val.SetToolTip((Control)(object)CBHighVolume, "Check to look for unusually high volume on the most recent price bar.");
		val.SetToolTip((Control)(object)CBStages, "Check to include a chart of Weinstein stages.");
		val.SetToolTip((Control)(object)StagesHelpButton, "Help for Weinstein stages.");
		InitControls(RuntimeHelpers.GetObjectValue(sender), e);
	}

	private void FilterForm_Activated(object sender, EventArgs e)
	{
		LockFlag = false;
	}

	private void ButtonDirectionDefault_Click(object sender, EventArgs e)
	{
		RBBkoutUpDown.Checked = true;
		CBBkoutIncludeNone.Checked = true;
		GlobalForm.FilterGlobals.BkoutDirRBOption = 2;
		GlobalForm.FilterGlobals.CBBkoutIncludeNone = CBBkoutIncludeNone.Checked;
	}

	private void ButtonHeightDefault_Click(object sender, EventArgs e)
	{
		RBHeightEither.Checked = true;
		GlobalForm.FilterGlobals.HeightRBOption = 2;
	}

	private void ButtonPriceDefault_Click(object sender, EventArgs e)
	{
		NumericPriceLess.Value = 500m;
		NumericPriceLow.Value = 5m;
		NumericPriceHigh.Value = 1000000m;
		NumericPriceMore.Value = 5m;
		RBPriceMore.Checked = true;
		GlobalForm.FilterGlobals.PriceRBOption = 2;
		GlobalForm.FilterGlobals.NumericPriceLess = NumericPriceLess.Value;
		GlobalForm.FilterGlobals.NumericPriceLow = NumericPriceLow.Value;
		GlobalForm.FilterGlobals.NumericPriceHigh = NumericPriceHigh.Value;
		GlobalForm.FilterGlobals.NumericPriceMore = NumericPriceMore.Value;
	}

	private void ButtonVolumeDefault_Click(object sender, EventArgs e)
	{
		NumericVolume.Value = 100000m;
		GlobalForm.FilterGlobals.NumericVolume = NumericVolume.Value;
	}

	private void ButtonWidthDefault_Click(object sender, EventArgs e)
	{
		NumericWidthLess.Value = 180m;
		NumericWidthLow.Value = 0m;
		NumericWidthHigh.Value = 180m;
		NumericWidthMore.Value = 0m;
		RBWidthLess.Checked = true;
		GlobalForm.FilterGlobals.WidthRBOption = 0;
		GlobalForm.FilterGlobals.NumericWidthLess = NumericWidthLess.Value;
		GlobalForm.FilterGlobals.NumericWidthLow = NumericWidthLow.Value;
		GlobalForm.FilterGlobals.NumericWidthHigh = NumericWidthHigh.Value;
		GlobalForm.FilterGlobals.NumericWidthMore = NumericWidthMore.Value;
	}

	public void CBBkoutDirection_CheckedChanged(object sender, EventArgs e)
	{
		((Control)GroupBkoutDirection).Visible = CBBkoutDirection.Checked;
		if (CBBkoutDirection.Checked & !LockFlag)
		{
			CBMasterSwitch.Checked = true;
		}
	}

	public void CBHeight_CheckedChanged(object sender, EventArgs e)
	{
		((Control)GroupHeight).Visible = CBHeight.Checked;
		if (CBHeight.Checked & !LockFlag)
		{
			CBMasterSwitch.Checked = true;
		}
	}

	private void CBHighVolume_CheckedChanged(object sender, EventArgs e)
	{
		((Control)GroupHighVolume).Visible = CBHighVolume.Checked;
		if (CBHighVolume.Checked & !LockFlag)
		{
			CBMasterSwitch.Checked = true;
		}
	}

	public void CBPrice_CheckedChanged(object sender, EventArgs e)
	{
		((Control)GroupPrice).Visible = CBPrice.Checked;
		if (CBPrice.Checked & !LockFlag)
		{
			CBMasterSwitch.Checked = true;
		}
	}

	private void CBPriceMoves_CheckedChanged(object sender, EventArgs e)
	{
		((Control)GroupPriceMoves).Visible = CBPriceMoves.Checked;
		if (CBPriceMoves.Checked & !LockFlag)
		{
			CBMasterSwitch.Checked = true;
		}
	}

	private void CBStages_CheckedChanged(object sender, EventArgs e)
	{
		((Control)GroupStages).Visible = CBStages.Checked;
		if (CBStages.Checked & !LockFlag)
		{
			CBMasterSwitch.Checked = true;
		}
	}

	public void CBVolume_CheckedChanged(object sender, EventArgs e)
	{
		((Control)GroupVolume).Visible = CBVolume.Checked;
		if (CBVolume.Checked & !LockFlag)
		{
			CBMasterSwitch.Checked = true;
		}
	}

	public void CBWidth_CheckedChanged(object sender, EventArgs e)
	{
		((Control)GroupWidth).Visible = CBWidth.Checked;
		if (CBWidth.Checked & !LockFlag)
		{
			CBMasterSwitch.Checked = true;
		}
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void InitControls(object sender, EventArgs e)
	{
		switch (GlobalForm.FilterGlobals.WidthRBOption)
		{
		case 0:
			RBWidthLess.Checked = true;
			break;
		case 1:
			RBWidthBetween.Checked = true;
			break;
		case 2:
			RBWidthMore.Checked = true;
			break;
		}
		switch (GlobalForm.FilterGlobals.PriceRBOption)
		{
		case 0:
			RBPriceLess.Checked = true;
			break;
		case 1:
			RBPriceBetween.Checked = true;
			break;
		case 2:
			RBPriceMore.Checked = true;
			break;
		}
		switch (GlobalForm.FilterGlobals.HeightRBOption)
		{
		case 0:
			RBHeightTall.Checked = true;
			break;
		case 1:
			RBHeightShort.Checked = true;
			break;
		case 2:
			RBHeightEither.Checked = true;
			break;
		}
		switch (GlobalForm.FilterGlobals.BkoutDirRBOption)
		{
		case 0:
			RBBkoutUp.Checked = true;
			break;
		case 1:
			RBBkoutDown.Checked = true;
			break;
		case 2:
			RBBkoutUpDown.Checked = true;
			break;
		case 3:
			RBBkoutNoneYet.Checked = true;
			break;
		}
		NumericWidthLess.Value = GlobalForm.FilterGlobals.NumericWidthLess;
		NumericWidthLow.Value = GlobalForm.FilterGlobals.NumericWidthLow;
		NumericWidthMore.Value = GlobalForm.FilterGlobals.NumericWidthMore;
		NumericWidthHigh.Value = GlobalForm.FilterGlobals.NumericWidthHigh;
		NumericPriceLess.Value = GlobalForm.FilterGlobals.NumericPriceLess;
		NumericPriceLow.Value = GlobalForm.FilterGlobals.NumericPriceLow;
		NumericPriceMore.Value = GlobalForm.FilterGlobals.NumericPriceMore;
		NumericPriceHigh.Value = GlobalForm.FilterGlobals.NumericPriceHigh;
		NumericVolume.Value = GlobalForm.FilterGlobals.NumericVolume;
		try
		{
			NumericPriceMoves.Value = GlobalForm.FilterGlobals.NumericPriceMoves;
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			NumericPriceMoves.Value = 5m;
			GlobalForm.FilterGlobals.NumericPriceMoves = 5m;
			ProjectData.ClearProjectError();
		}
		try
		{
			NumericHighVolume.Value = GlobalForm.FilterGlobals.NumericHighVolume;
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			NumericHighVolume.Value = 2m;
			GlobalForm.FilterGlobals.NumericHighVolume = 2m;
			ProjectData.ClearProjectError();
		}
		CBBkoutIncludeNone.Checked = GlobalForm.FilterGlobals.CBBkoutIncludeNone;
		CBWidth.Checked = GlobalForm.FilterGlobals.CBWidth;
		CBPrice.Checked = GlobalForm.FilterGlobals.CBPrice;
		CBBkoutDirection.Checked = GlobalForm.FilterGlobals.CBBkoutDirection;
		CBHeight.Checked = GlobalForm.FilterGlobals.CBHeight;
		CBVolume.Checked = GlobalForm.FilterGlobals.CBVolume;
		CBMasterSwitch.Checked = GlobalForm.FilterGlobals.CBMasterSwitch;
		CBPriceMoves.Checked = GlobalForm.FilterGlobals.CBPriceMoves;
		CBHighVolume.Checked = GlobalForm.FilterGlobals.CBHighVolume;
		CBStages.Checked = GlobalForm.FilterGlobals.CBStages;
		CBStage1.Checked = GlobalForm.FilterGlobals.CBStage1;
		CBStage2.Checked = GlobalForm.FilterGlobals.CBStage2;
		CBStage3.Checked = GlobalForm.FilterGlobals.CBStage3;
		CBStage4.Checked = GlobalForm.FilterGlobals.CBStage4;
		CBBkoutDirection_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
		CBHeight_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
		CBPrice_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
		CBVolume_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
		CBWidth_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
		CBPriceMoves_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
		CBHighVolume_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
		CBStages_CheckedChanged(RuntimeHelpers.GetObjectValue(sender), e);
	}

	private void NumericPriceLow_LostFocus(object sender, EventArgs e)
	{
		if (decimal.Compare(NumericPriceLow.Value, NumericPriceHigh.Value) > 0)
		{
			decimal value = NumericPriceHigh.Value;
			NumericPriceHigh.Value = NumericPriceLow.Value;
			NumericPriceLow.Value = value;
		}
	}

	private void NumericWidthLow_LostFocus(object sender, EventArgs e)
	{
		if (decimal.Compare(NumericWidthLow.Value, NumericWidthHigh.Value) > 0)
		{
			decimal value = NumericWidthHigh.Value;
			NumericWidthHigh.Value = NumericWidthLow.Value;
			NumericWidthLow.Value = value;
		}
	}

	private void StagesHelpButton_Click(object sender, EventArgs e)
	{
		//IL_0037: Unknown result type (might be due to invalid IL or missing references)
		MessageBox.Show(string.Concat(string.Concat(string.Concat(string.Concat("Weinstein stages, as implemented in Patternz, is EXPERIMENTAL so be careful when using it. The stages may be incorrect. Only use stages on the WEEKLY scale. Unreliable results may come if using other scales" + " (Patternz will automatically switch to the weekly scale when charting a stage).", "\r\n\r\nStages: Picture the letter M. In stage 1, price is flat (cycling up and down but moving horizontally in a trading range) leading to the start of the M. Stocks in stage 2 form the left side of the M as price rises."), " Stage 3 is the top of the M where price cycles up and down but stays in a trading range (moves horizontally). Stage 4 happens when price breaks through support and drops, forming the right side of the M."), " After that, Stage 1 begins again."), "\r\n\r\nFor more information, see Weinstein's book, 'Secrets for profiting in bull and bear markets' or my website at https://thepatternsite.com/WeinsteinStops.html (search for 'weinstein stops')."));
	}

	private void WriteConfigFile()
	{
		//IL_03b8: Unknown result type (might be due to invalid IL or missing references)
		BinaryFormatter binaryFormatter = new BinaryFormatter();
		bool flag = true;
		if (flag == RBWidthLess.Checked)
		{
			GlobalForm.FilterGlobals.WidthRBOption = 0;
		}
		else if (flag == RBWidthBetween.Checked)
		{
			GlobalForm.FilterGlobals.WidthRBOption = 1;
		}
		else if (flag == RBWidthMore.Checked)
		{
			GlobalForm.FilterGlobals.WidthRBOption = 2;
		}
		bool flag2 = true;
		if (flag2 == RBPriceLess.Checked)
		{
			GlobalForm.FilterGlobals.PriceRBOption = 0;
		}
		else if (flag2 == RBPriceBetween.Checked)
		{
			GlobalForm.FilterGlobals.PriceRBOption = 1;
		}
		else if (flag2 == RBPriceMore.Checked)
		{
			GlobalForm.FilterGlobals.PriceRBOption = 2;
		}
		bool flag3 = true;
		if (flag3 == RBHeightTall.Checked)
		{
			GlobalForm.FilterGlobals.HeightRBOption = 0;
		}
		else if (flag3 == RBHeightShort.Checked)
		{
			GlobalForm.FilterGlobals.HeightRBOption = 1;
		}
		else if (flag3 == RBHeightEither.Checked)
		{
			GlobalForm.FilterGlobals.HeightRBOption = 2;
		}
		bool flag4 = true;
		if (flag4 == RBBkoutUp.Checked)
		{
			GlobalForm.FilterGlobals.BkoutDirRBOption = 0;
		}
		else if (flag4 == RBBkoutDown.Checked)
		{
			GlobalForm.FilterGlobals.BkoutDirRBOption = 1;
		}
		else if (flag4 == RBBkoutUpDown.Checked)
		{
			GlobalForm.FilterGlobals.BkoutDirRBOption = 2;
		}
		else if (flag4 == RBBkoutNoneYet.Checked)
		{
			GlobalForm.FilterGlobals.BkoutDirRBOption = 3;
		}
		GlobalForm.FilterGlobals.NumericWidthLess = NumericWidthLess.Value;
		GlobalForm.FilterGlobals.NumericWidthLow = NumericWidthLow.Value;
		GlobalForm.FilterGlobals.NumericWidthMore = NumericWidthMore.Value;
		GlobalForm.FilterGlobals.NumericWidthHigh = NumericWidthHigh.Value;
		GlobalForm.FilterGlobals.NumericPriceLess = NumericPriceLess.Value;
		GlobalForm.FilterGlobals.NumericPriceLow = NumericPriceLow.Value;
		GlobalForm.FilterGlobals.NumericPriceMore = NumericPriceMore.Value;
		GlobalForm.FilterGlobals.NumericPriceHigh = NumericPriceHigh.Value;
		GlobalForm.FilterGlobals.NumericVolume = NumericVolume.Value;
		GlobalForm.FilterGlobals.NumericPriceMoves = NumericPriceMoves.Value;
		GlobalForm.FilterGlobals.NumericHighVolume = NumericHighVolume.Value;
		GlobalForm.FilterGlobals.CBBkoutIncludeNone = CBBkoutIncludeNone.Checked;
		GlobalForm.FilterGlobals.CBWidth = CBWidth.Checked;
		GlobalForm.FilterGlobals.CBPrice = CBPrice.Checked;
		GlobalForm.FilterGlobals.CBBkoutDirection = CBBkoutDirection.Checked;
		GlobalForm.FilterGlobals.CBHeight = CBHeight.Checked;
		GlobalForm.FilterGlobals.CBVolume = CBVolume.Checked;
		GlobalForm.FilterGlobals.CBMasterSwitch = CBMasterSwitch.Checked;
		GlobalForm.FilterGlobals.CBPriceMoves = CBPriceMoves.Checked;
		GlobalForm.FilterGlobals.CBHighVolume = CBHighVolume.Checked;
		GlobalForm.FilterGlobals.CBStages = CBStages.Checked;
		GlobalForm.FilterGlobals.CBStage1 = CBStage1.Checked;
		GlobalForm.FilterGlobals.CBStage2 = CBStage2.Checked;
		GlobalForm.FilterGlobals.CBStage3 = CBStage3.Checked;
		GlobalForm.FilterGlobals.CBStage4 = CBStage4.Checked;
		try
		{
			Stream stream = File.OpenWrite(GlobalForm.ConfigLocation + GlobalForm.FilterConfigName);
			binaryFormatter.Serialize(stream, GlobalForm.FilterGlobals);
			stream.Close();
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			MessageBox.Show(ex2.Message);
			ProjectData.ClearProjectError();
		}
	}
}
