using System;
using System.CodeDom.Compiler;
using System.ComponentModel;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Threading;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz.My;

[CompilerGenerated]
[GeneratedCode("Microsoft.VisualStudio.Editors.SettingsDesigner.SettingsSingleFileGenerator", "17.8.0.0")]
[EditorBrowsable(EditorBrowsableState.Advanced)]
internal sealed class MySettings : ApplicationSettingsBase
{
	private static MySettings defaultInstance = (MySettings)(object)SettingsBase.Synchronized((SettingsBase)(object)new MySettings());

	private static bool addedHandler;

	private static object addedHandlerLockObject = RuntimeHelpers.GetObjectValue(new object());

	public static MySettings Default
	{
		get
		{
			//IL_0030: Unknown result type (might be due to invalid IL or missing references)
			//IL_003a: Expected O, but got Unknown
			if (!addedHandler)
			{
				object obj = addedHandlerLockObject;
				ObjectFlowControl.CheckForSyncLockOnValueType(obj);
				bool lockTaken = false;
				try
				{
					Monitor.Enter(obj, ref lockTaken);
					if (!addedHandler)
					{
						((WindowsFormsApplicationBase)MyProject.Application).Shutdown += new ShutdownEventHandler(AutoSaveSettings);
						addedHandler = true;
					}
				}
				finally
				{
					if (lockTaken)
					{
						Monitor.Exit(obj);
					}
				}
			}
			return defaultInstance;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point MainFormLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["MainFormLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["MainFormLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("")]
	public string OpenPath
	{
		get
		{
			return Conversions.ToString(((ApplicationSettingsBase)this)["OpenPath"]);
		}
		set
		{
			((ApplicationSettingsBase)this)["OpenPath"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point ListFormLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["ListFormLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["ListFormLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size ListFormSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["ListFormSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["ListFormSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point CandlesFormLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["CandlesFormLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["CandlesFormLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size CandlesFormSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["CandlesFormSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["CandlesFormSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point ChartFormLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["ChartFormLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["ChartFormLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size ChartFormSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["ChartFormSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["ChartFormSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point CPIFormLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["CPIFormLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["CPIFormLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size CPIFormSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["CPIFormSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["CPIFormSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point FibFinderLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["FibFinderLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["FibFinderLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size FibFinderSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["FibFinderSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["FibFinderSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point FixedSplitLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["FixedSplitLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["FixedSplitLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size FixedSplitSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["FixedSplitSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["FixedSplitSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point ForecastLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["ForecastLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["ForecastLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size ForecastSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["ForecastSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["ForecastSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point ListChartLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["ListChartLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["ListChartLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size ListChartSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["ListChartSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["ListChartSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size MainFormSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["MainFormSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["MainFormSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point ManualScoreLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["ManualScoreLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["ManualScoreLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size ManualScoreSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["ManualScoreSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["ManualScoreSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point NewsFormLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["NewsFormLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["NewsFormLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size NewsFormSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["NewsFormSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["NewsFormSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point PatternsLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["PatternsLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["PatternsLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size PatternsSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["PatternsSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["PatternsSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point RelStrengthLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["RelStrengthLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["RelStrengthLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size RelStrengthSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["RelStrengthSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["RelStrengthSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point ScoreLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["ScoreLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["ScoreLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size ScoreSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["ScoreSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["ScoreSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point SeasonLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["SeasonLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["SeasonLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size SeasonSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["SeasonSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["SeasonSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point SimLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["SimLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["SimLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size SimSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["SimSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["SimSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point SplitsLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["SplitsLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["SplitsLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size SplitsSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["SplitsSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["SplitsSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point UpdateLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["UpdateLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["UpdateLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size UpdateSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["UpdateSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["UpdateSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Point BestTradingTimeLocation
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["BestTradingTimeLocation"];
			if (obj == null)
			{
				return default(Point);
			}
			return (Point)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["BestTradingTimeLocation"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("-1, -1")]
	public Size BestTradingTimeSize
	{
		get
		{
			object obj = ((ApplicationSettingsBase)this)["BestTradingTimeSize"];
			if (obj == null)
			{
				return default(Size);
			}
			return (Size)obj;
		}
		set
		{
			((ApplicationSettingsBase)this)["BestTradingTimeSize"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("5")]
	public int BestTradingTimePct
	{
		get
		{
			return Conversions.ToInteger(((ApplicationSettingsBase)this)["BestTradingTimePct"]);
		}
		set
		{
			((ApplicationSettingsBase)this)["BestTradingTimePct"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("10")]
	public int BestTradingTimeBars
	{
		get
		{
			return Conversions.ToInteger(((ApplicationSettingsBase)this)["BestTradingTimeBars"]);
		}
		set
		{
			((ApplicationSettingsBase)this)["BestTradingTimeBars"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("False")]
	public bool BestTradingTimeUseDates
	{
		get
		{
			return Conversions.ToBoolean(((ApplicationSettingsBase)this)["BestTradingTimeUseDates"]);
		}
		set
		{
			((ApplicationSettingsBase)this)["BestTradingTimeUseDates"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("True")]
	public bool BestTradingTimeClose2Close
	{
		get
		{
			return Conversions.ToBoolean(((ApplicationSettingsBase)this)["BestTradingTimeClose2Close"]);
		}
		set
		{
			((ApplicationSettingsBase)this)["BestTradingTimeClose2Close"] = value;
		}
	}

	[UserScopedSetting]
	[DebuggerNonUserCode]
	[DefaultSettingValue("False")]
	public bool ReplaceQuoteCB
	{
		get
		{
			return Conversions.ToBoolean(((ApplicationSettingsBase)this)["ReplaceQuoteCB"]);
		}
		set
		{
			((ApplicationSettingsBase)this)["ReplaceQuoteCB"] = value;
		}
	}

	[DebuggerNonUserCode]
	[EditorBrowsable(EditorBrowsableState.Advanced)]
	private static void AutoSaveSettings(object sender, EventArgs e)
	{
		if (((WindowsFormsApplicationBase)MyProject.Application).SaveMySettingsOnExit)
		{
			((ApplicationSettingsBase)MySettingsProperty.Settings).Save();
		}
	}
}
