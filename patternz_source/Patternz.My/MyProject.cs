using System;
using System.CodeDom.Compiler;
using System.Collections;
using System.ComponentModel;
using System.ComponentModel.Design;
using System.Diagnostics;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz.My;

[StandardModule]
[HideModuleName]
[GeneratedCode("MyTemplate", "11.0.0.0")]
internal sealed class MyProject
{
	[EditorBrowsable(EditorBrowsableState.Never)]
	[MyGroupCollection("System.Windows.Forms.Form", "Create__Instance__", "Dispose__Instance__", "My.MyProject.Forms")]
	internal sealed class MyForms
	{
		[ThreadStatic]
		private static Hashtable m_FormBeingCreated;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public AboutForm m_AboutForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public AnalyzeForm m_AnalyzeForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public AnalyzeFormHelp m_AnalyzeFormHelp;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public BestTradingTime m_BestTradingTime;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public BigMessageBox m_BigMessageBox;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public CandlesForm m_CandlesForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public ChartForm m_ChartForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public CPIForm m_CPIForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public CustomDialogBox m_CustomDialogBox;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public FibFinderForm m_FibFinderForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public FileFormatForm m_FileFormatForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public FileFormatHelp m_FileFormatHelp;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public FilterForm m_FilterForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public FixSplitForm m_FixSplitForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public ForecastForm m_ForecastForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public HelpBestTrade m_HelpBestTrade;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public HelpCPIForm m_HelpCPIForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public HelpFibFinder m_HelpFibFinder;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public HelpForecastForm m_HelpForecastForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public HelpListForm m_HelpListForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public HelpMainFormPortfolio m_HelpMainFormPortfolio;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public HelpScoreForm m_HelpScoreForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public HelpSimulatorForm m_HelpSimulatorForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public LicenseForm m_LicenseForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public ListChartForm m_ListChartForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public ListForm m_ListForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public Mainform m_Mainform;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public MainFormHelp m_MainFormHelp;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public ManualScoreForm m_ManualScoreForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public NewsForm m_NewsForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public PatternsForm m_PatternsForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public PortfolioDialog m_PortfolioDialog;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public RelStrengthForm m_RelStrengthForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public RemovePatternz m_RemovePatternz;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public RenameDialog m_RenameDialog;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public ScoreForm m_ScoreForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public Seasonality m_Seasonality;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public SetupForm m_SetupForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public SimSetupForm m_SimSetupForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public SimulatorForm m_SimulatorForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public SplitsDivsForm m_SplitsDivsForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public UpdateForm m_UpdateForm;

		[EditorBrowsable(EditorBrowsableState.Never)]
		public UpdateHelpForm m_UpdateHelpForm;

		public AboutForm AboutForm
		{
			get
			{
				m_AboutForm = Create__Instance__(m_AboutForm);
				return m_AboutForm;
			}
			set
			{
				if (value != m_AboutForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_AboutForm);
				}
			}
		}

		public AnalyzeForm AnalyzeForm
		{
			get
			{
				m_AnalyzeForm = Create__Instance__(m_AnalyzeForm);
				return m_AnalyzeForm;
			}
			set
			{
				if (value != m_AnalyzeForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_AnalyzeForm);
				}
			}
		}

		public AnalyzeFormHelp AnalyzeFormHelp
		{
			get
			{
				m_AnalyzeFormHelp = Create__Instance__(m_AnalyzeFormHelp);
				return m_AnalyzeFormHelp;
			}
			set
			{
				if (value != m_AnalyzeFormHelp)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_AnalyzeFormHelp);
				}
			}
		}

		public BestTradingTime BestTradingTime
		{
			get
			{
				m_BestTradingTime = Create__Instance__(m_BestTradingTime);
				return m_BestTradingTime;
			}
			set
			{
				if (value != m_BestTradingTime)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_BestTradingTime);
				}
			}
		}

		public BigMessageBox BigMessageBox
		{
			get
			{
				m_BigMessageBox = Create__Instance__(m_BigMessageBox);
				return m_BigMessageBox;
			}
			set
			{
				if (value != m_BigMessageBox)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_BigMessageBox);
				}
			}
		}

		public CandlesForm CandlesForm
		{
			get
			{
				m_CandlesForm = Create__Instance__(m_CandlesForm);
				return m_CandlesForm;
			}
			set
			{
				if (value != m_CandlesForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_CandlesForm);
				}
			}
		}

		public ChartForm ChartForm
		{
			get
			{
				m_ChartForm = Create__Instance__(m_ChartForm);
				return m_ChartForm;
			}
			set
			{
				if (value != m_ChartForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_ChartForm);
				}
			}
		}

		public CPIForm CPIForm
		{
			get
			{
				m_CPIForm = Create__Instance__(m_CPIForm);
				return m_CPIForm;
			}
			set
			{
				if (value != m_CPIForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_CPIForm);
				}
			}
		}

		public CustomDialogBox CustomDialogBox
		{
			get
			{
				m_CustomDialogBox = Create__Instance__(m_CustomDialogBox);
				return m_CustomDialogBox;
			}
			set
			{
				if (value != m_CustomDialogBox)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_CustomDialogBox);
				}
			}
		}

		public FibFinderForm FibFinderForm
		{
			get
			{
				m_FibFinderForm = Create__Instance__(m_FibFinderForm);
				return m_FibFinderForm;
			}
			set
			{
				if (value != m_FibFinderForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_FibFinderForm);
				}
			}
		}

		public FileFormatForm FileFormatForm
		{
			get
			{
				m_FileFormatForm = Create__Instance__(m_FileFormatForm);
				return m_FileFormatForm;
			}
			set
			{
				if (value != m_FileFormatForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_FileFormatForm);
				}
			}
		}

		public FileFormatHelp FileFormatHelp
		{
			get
			{
				m_FileFormatHelp = Create__Instance__(m_FileFormatHelp);
				return m_FileFormatHelp;
			}
			set
			{
				if (value != m_FileFormatHelp)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_FileFormatHelp);
				}
			}
		}

		public FilterForm FilterForm
		{
			get
			{
				m_FilterForm = Create__Instance__(m_FilterForm);
				return m_FilterForm;
			}
			set
			{
				if (value != m_FilterForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_FilterForm);
				}
			}
		}

		public FixSplitForm FixSplitForm
		{
			get
			{
				m_FixSplitForm = Create__Instance__(m_FixSplitForm);
				return m_FixSplitForm;
			}
			set
			{
				if (value != m_FixSplitForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_FixSplitForm);
				}
			}
		}

		public ForecastForm ForecastForm
		{
			get
			{
				m_ForecastForm = Create__Instance__(m_ForecastForm);
				return m_ForecastForm;
			}
			set
			{
				if (value != m_ForecastForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_ForecastForm);
				}
			}
		}

		public HelpBestTrade HelpBestTrade
		{
			get
			{
				m_HelpBestTrade = Create__Instance__(m_HelpBestTrade);
				return m_HelpBestTrade;
			}
			set
			{
				if (value != m_HelpBestTrade)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_HelpBestTrade);
				}
			}
		}

		public HelpCPIForm HelpCPIForm
		{
			get
			{
				m_HelpCPIForm = Create__Instance__(m_HelpCPIForm);
				return m_HelpCPIForm;
			}
			set
			{
				if (value != m_HelpCPIForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_HelpCPIForm);
				}
			}
		}

		public HelpFibFinder HelpFibFinder
		{
			get
			{
				m_HelpFibFinder = Create__Instance__(m_HelpFibFinder);
				return m_HelpFibFinder;
			}
			set
			{
				if (value != m_HelpFibFinder)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_HelpFibFinder);
				}
			}
		}

		public HelpForecastForm HelpForecastForm
		{
			get
			{
				m_HelpForecastForm = Create__Instance__(m_HelpForecastForm);
				return m_HelpForecastForm;
			}
			set
			{
				if (value != m_HelpForecastForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_HelpForecastForm);
				}
			}
		}

		public HelpListForm HelpListForm
		{
			get
			{
				m_HelpListForm = Create__Instance__(m_HelpListForm);
				return m_HelpListForm;
			}
			set
			{
				if (value != m_HelpListForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_HelpListForm);
				}
			}
		}

		public HelpMainFormPortfolio HelpMainFormPortfolio
		{
			get
			{
				m_HelpMainFormPortfolio = Create__Instance__(m_HelpMainFormPortfolio);
				return m_HelpMainFormPortfolio;
			}
			set
			{
				if (value != m_HelpMainFormPortfolio)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_HelpMainFormPortfolio);
				}
			}
		}

		public HelpScoreForm HelpScoreForm
		{
			get
			{
				m_HelpScoreForm = Create__Instance__(m_HelpScoreForm);
				return m_HelpScoreForm;
			}
			set
			{
				if (value != m_HelpScoreForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_HelpScoreForm);
				}
			}
		}

		public HelpSimulatorForm HelpSimulatorForm
		{
			get
			{
				m_HelpSimulatorForm = Create__Instance__(m_HelpSimulatorForm);
				return m_HelpSimulatorForm;
			}
			set
			{
				if (value != m_HelpSimulatorForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_HelpSimulatorForm);
				}
			}
		}

		public LicenseForm LicenseForm
		{
			get
			{
				m_LicenseForm = Create__Instance__(m_LicenseForm);
				return m_LicenseForm;
			}
			set
			{
				if (value != m_LicenseForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_LicenseForm);
				}
			}
		}

		public ListChartForm ListChartForm
		{
			get
			{
				m_ListChartForm = Create__Instance__(m_ListChartForm);
				return m_ListChartForm;
			}
			set
			{
				if (value != m_ListChartForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_ListChartForm);
				}
			}
		}

		public ListForm ListForm
		{
			get
			{
				m_ListForm = Create__Instance__(m_ListForm);
				return m_ListForm;
			}
			set
			{
				if (value != m_ListForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_ListForm);
				}
			}
		}

		public Mainform Mainform
		{
			get
			{
				m_Mainform = Create__Instance__(m_Mainform);
				return m_Mainform;
			}
			set
			{
				if (value != m_Mainform)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_Mainform);
				}
			}
		}

		public MainFormHelp MainFormHelp
		{
			get
			{
				m_MainFormHelp = Create__Instance__(m_MainFormHelp);
				return m_MainFormHelp;
			}
			set
			{
				if (value != m_MainFormHelp)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_MainFormHelp);
				}
			}
		}

		public ManualScoreForm ManualScoreForm
		{
			get
			{
				m_ManualScoreForm = Create__Instance__(m_ManualScoreForm);
				return m_ManualScoreForm;
			}
			set
			{
				if (value != m_ManualScoreForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_ManualScoreForm);
				}
			}
		}

		public NewsForm NewsForm
		{
			get
			{
				m_NewsForm = Create__Instance__(m_NewsForm);
				return m_NewsForm;
			}
			set
			{
				if (value != m_NewsForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_NewsForm);
				}
			}
		}

		public PatternsForm PatternsForm
		{
			get
			{
				m_PatternsForm = Create__Instance__(m_PatternsForm);
				return m_PatternsForm;
			}
			set
			{
				if (value != m_PatternsForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_PatternsForm);
				}
			}
		}

		public PortfolioDialog PortfolioDialog
		{
			get
			{
				m_PortfolioDialog = Create__Instance__(m_PortfolioDialog);
				return m_PortfolioDialog;
			}
			set
			{
				if (value != m_PortfolioDialog)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_PortfolioDialog);
				}
			}
		}

		public RelStrengthForm RelStrengthForm
		{
			get
			{
				m_RelStrengthForm = Create__Instance__(m_RelStrengthForm);
				return m_RelStrengthForm;
			}
			set
			{
				if (value != m_RelStrengthForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_RelStrengthForm);
				}
			}
		}

		public RemovePatternz RemovePatternz
		{
			get
			{
				m_RemovePatternz = Create__Instance__(m_RemovePatternz);
				return m_RemovePatternz;
			}
			set
			{
				if (value != m_RemovePatternz)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_RemovePatternz);
				}
			}
		}

		public RenameDialog RenameDialog
		{
			get
			{
				m_RenameDialog = Create__Instance__(m_RenameDialog);
				return m_RenameDialog;
			}
			set
			{
				if (value != m_RenameDialog)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_RenameDialog);
				}
			}
		}

		public ScoreForm ScoreForm
		{
			get
			{
				m_ScoreForm = Create__Instance__(m_ScoreForm);
				return m_ScoreForm;
			}
			set
			{
				if (value != m_ScoreForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_ScoreForm);
				}
			}
		}

		public Seasonality Seasonality
		{
			get
			{
				m_Seasonality = Create__Instance__(m_Seasonality);
				return m_Seasonality;
			}
			set
			{
				if (value != m_Seasonality)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_Seasonality);
				}
			}
		}

		public SetupForm SetupForm
		{
			get
			{
				m_SetupForm = Create__Instance__(m_SetupForm);
				return m_SetupForm;
			}
			set
			{
				if (value != m_SetupForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_SetupForm);
				}
			}
		}

		public SimSetupForm SimSetupForm
		{
			get
			{
				m_SimSetupForm = Create__Instance__(m_SimSetupForm);
				return m_SimSetupForm;
			}
			set
			{
				if (value != m_SimSetupForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_SimSetupForm);
				}
			}
		}

		public SimulatorForm SimulatorForm
		{
			get
			{
				m_SimulatorForm = Create__Instance__(m_SimulatorForm);
				return m_SimulatorForm;
			}
			set
			{
				if (value != m_SimulatorForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_SimulatorForm);
				}
			}
		}

		public SplitsDivsForm SplitsDivsForm
		{
			get
			{
				m_SplitsDivsForm = Create__Instance__(m_SplitsDivsForm);
				return m_SplitsDivsForm;
			}
			set
			{
				if (value != m_SplitsDivsForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_SplitsDivsForm);
				}
			}
		}

		public UpdateForm UpdateForm
		{
			get
			{
				m_UpdateForm = Create__Instance__(m_UpdateForm);
				return m_UpdateForm;
			}
			set
			{
				if (value != m_UpdateForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_UpdateForm);
				}
			}
		}

		public UpdateHelpForm UpdateHelpForm
		{
			get
			{
				m_UpdateHelpForm = Create__Instance__(m_UpdateHelpForm);
				return m_UpdateHelpForm;
			}
			set
			{
				if (value != m_UpdateHelpForm)
				{
					if (value != null)
					{
						throw new ArgumentException("Property can only be set to Nothing");
					}
					Dispose__Instance__(ref m_UpdateHelpForm);
				}
			}
		}

		[DebuggerHidden]
		private static T Create__Instance__<T>(T Instance) where T : Form, new()
		{
			if (Instance == null || ((Control)Instance).IsDisposed)
			{
				if (m_FormBeingCreated != null)
				{
					if (m_FormBeingCreated.ContainsKey(typeof(T)))
					{
						throw new InvalidOperationException(Utils.GetResourceString("WinForms_RecursiveFormCreate", new string[0]));
					}
				}
				else
				{
					m_FormBeingCreated = new Hashtable();
				}
				m_FormBeingCreated.Add(typeof(T), null);
				try
				{
					return new T();
				}
				catch (TargetInvocationException ex) when (((Func<bool>)delegate
				{
					// Could not convert BlockContainer to single expression
					ProjectData.SetProjectError((Exception)ex);
					return ex.InnerException != null;
				}).Invoke())
				{
					throw new InvalidOperationException(Utils.GetResourceString("WinForms_SeeInnerException", new string[1] { ex.InnerException.Message }), ex.InnerException);
				}
				finally
				{
					m_FormBeingCreated.Remove(typeof(T));
				}
			}
			return Instance;
		}

		[DebuggerHidden]
		private void Dispose__Instance__<T>(ref T instance) where T : Form
		{
			((Component)instance/*cast due to .constrained prefix*/).Dispose();
			instance = default(T);
		}

		[DebuggerHidden]
		[EditorBrowsable(EditorBrowsableState.Never)]
		public MyForms()
		{
		}

		[EditorBrowsable(EditorBrowsableState.Never)]
		public override bool Equals(object o)
		{
			return base.Equals(RuntimeHelpers.GetObjectValue(o));
		}

		[EditorBrowsable(EditorBrowsableState.Never)]
		public override int GetHashCode()
		{
			return base.GetHashCode();
		}

		[EditorBrowsable(EditorBrowsableState.Never)]
		internal new Type GetType()
		{
			return typeof(MyForms);
		}

		[EditorBrowsable(EditorBrowsableState.Never)]
		public override string ToString()
		{
			return base.ToString();
		}
	}

	[EditorBrowsable(EditorBrowsableState.Never)]
	[MyGroupCollection("System.Web.Services.Protocols.SoapHttpClientProtocol", "Create__Instance__", "Dispose__Instance__", "")]
	internal sealed class MyWebServices
	{
		[EditorBrowsable(EditorBrowsableState.Never)]
		[DebuggerHidden]
		public override bool Equals(object o)
		{
			return base.Equals(RuntimeHelpers.GetObjectValue(o));
		}

		[EditorBrowsable(EditorBrowsableState.Never)]
		[DebuggerHidden]
		public override int GetHashCode()
		{
			return base.GetHashCode();
		}

		[EditorBrowsable(EditorBrowsableState.Never)]
		[DebuggerHidden]
		internal new Type GetType()
		{
			return typeof(MyWebServices);
		}

		[EditorBrowsable(EditorBrowsableState.Never)]
		[DebuggerHidden]
		public override string ToString()
		{
			return base.ToString();
		}

		[DebuggerHidden]
		private static T Create__Instance__<T>(T instance) where T : new()
		{
			if (instance == null)
			{
				return new T();
			}
			return instance;
		}

		[DebuggerHidden]
		private void Dispose__Instance__<T>(ref T instance)
		{
			instance = default(T);
		}

		[DebuggerHidden]
		[EditorBrowsable(EditorBrowsableState.Never)]
		public MyWebServices()
		{
		}
	}

	[EditorBrowsable(EditorBrowsableState.Never)]
	[ComVisible(false)]
	internal sealed class ThreadSafeObjectProvider<T> where T : new()
	{
		[CompilerGenerated]
		[ThreadStatic]
		private static T m_ThreadStaticValue;

		internal T GetInstance
		{
			[DebuggerHidden]
			get
			{
				if (m_ThreadStaticValue == null)
				{
					m_ThreadStaticValue = new T();
				}
				return m_ThreadStaticValue;
			}
		}

		[DebuggerHidden]
		[EditorBrowsable(EditorBrowsableState.Never)]
		public ThreadSafeObjectProvider()
		{
		}
	}

	private static readonly ThreadSafeObjectProvider<MyComputer> m_ComputerObjectProvider = new ThreadSafeObjectProvider<MyComputer>();

	private static readonly ThreadSafeObjectProvider<MyApplication> m_AppObjectProvider = new ThreadSafeObjectProvider<MyApplication>();

	private static readonly ThreadSafeObjectProvider<User> m_UserObjectProvider = new ThreadSafeObjectProvider<User>();

	private static ThreadSafeObjectProvider<MyForms> m_MyFormsObjectProvider = new ThreadSafeObjectProvider<MyForms>();

	private static readonly ThreadSafeObjectProvider<MyWebServices> m_MyWebServicesObjectProvider = new ThreadSafeObjectProvider<MyWebServices>();

	[HelpKeyword("My.Computer")]
	internal static MyComputer Computer
	{
		[DebuggerHidden]
		get
		{
			return m_ComputerObjectProvider.GetInstance;
		}
	}

	[HelpKeyword("My.Application")]
	internal static MyApplication Application
	{
		[DebuggerHidden]
		get
		{
			return m_AppObjectProvider.GetInstance;
		}
	}

	[HelpKeyword("My.User")]
	internal static User User
	{
		[DebuggerHidden]
		get
		{
			return m_UserObjectProvider.GetInstance;
		}
	}

	[HelpKeyword("My.Forms")]
	internal static MyForms Forms
	{
		[DebuggerHidden]
		get
		{
			return m_MyFormsObjectProvider.GetInstance;
		}
	}

	[HelpKeyword("My.WebServices")]
	internal static MyWebServices WebServices
	{
		[DebuggerHidden]
		get
		{
			return m_MyWebServicesObjectProvider.GetInstance;
		}
	}
}
