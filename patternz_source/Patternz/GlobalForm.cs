using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Runtime.Serialization.Formatters.Binary;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;
using Microsoft.VisualBasic.Devices;
using Patternz.My;

namespace Patternz;

[StandardModule]
internal sealed class GlobalForm
{
	public struct BearMktsStruct
	{
		public DateTime StartDate;

		public DateTime EndDate;

		public string Text;
	}

	public struct InfoArray
	{
		public string BkoutDirection;

		public string BkoutDate;

		public int iBkout;

		public string BkoutPrice;

		public string Target;

		public string VolStop;

		public string UltHLPrice;

		public string UltHLDate;

		public string Status;

		public string AvgVolume;
	}

	public struct LineEndPoints
	{
		public Point StartPoint;

		public Point endPoint;
	}

	public struct DisplayFmtns
	{
		public int iStartDate;

		public int iMidDate;

		public int iEndDate;

		public int iStart2Date;

		public int iMid2Date;

		public int iEnd2Date;

		public int Type;

		public string iText;

		public Color RenderColor;

		public int iDataGridViewRow;

		public decimal PriceTarget;

		public decimal StopPrice;

		public string StopDate;

		public decimal UltHLPrice;

		public string UltHLDate;

		public bool UltHiLow;

		public decimal dBreakoutPrice;

		public decimal dChannelHeight;
	}

	public struct CandleFmtns
	{
		public int Type;

		public int iStartDate;

		public int iEndDate;

		public int iDataGridViewRow;

		public Color RenderColor;

		public decimal dPriceTarget;

		public decimal dStopPrice;

		public DateTime StopDate;

		public int iBkoutDirection;

		public decimal UltHLPrice;

		public string UltHLDate;

		public bool UltHiLow;

		public string Phrase;

		public string PriceTarget;

		public string StopPrice;

		public string BkoutDirection;

		public string TradeStatus;

		public decimal dBreakoutPrice;
	}

	[Serializable]
	public struct SimStruct
	{
		public bool Annotations;

		public bool FindCandles;

		public bool ShowPattern;

		public bool ShowCircles;

		public bool Strict;

		public bool Volume;

		public bool MovingAvg;

		public int MAType;

		public int MALength;

		public int TimeScale;

		public int Speed;

		public int Lookback;

		public decimal SECFee;

		public bool SECBool;

		public decimal Commissions;

		public bool StopUltHigh;

		public bool StopUltLow;

		public bool AutoSetTargets;

		public int FailuresOnly;

		public int Percentage;

		public bool ShowBearMarkets;

		public bool ShowPeakDrop;

		public bool ShowValleyRises;

		public int PercentageDrop;

		public int PercentageRise;

		public bool CloseAboveTL;

		public bool CloseBelowTL;

		public bool StopPctDown;

		public bool StopPctUp;
	}

	public struct SplitsInfoArray
	{
		public string Symbol;

		public DateTime SplitDate;

		public string SplitRatio;
	}

	[Serializable]
	public struct FilterStruct
	{
		public int BkoutDirRBOption;

		public int HeightRBOption;

		public int PriceRBOption;

		public int WidthRBOption;

		public decimal NumericWidthLess;

		public decimal NumericWidthLow;

		public decimal NumericWidthMore;

		public decimal NumericWidthHigh;

		public decimal NumericPriceLess;

		public decimal NumericPriceLow;

		public decimal NumericPriceMore;

		public decimal NumericPriceHigh;

		public decimal NumericVolume;

		public bool CBBkoutIncludeNone;

		public bool CBWidth;

		public bool CBPrice;

		public bool CBBkoutDirection;

		public bool CBHeight;

		public bool CBVolume;

		public bool CBMasterSwitch;

		public bool CBPriceMoves;

		public bool CBHighVolume;

		public bool CBStages;

		public bool CBStage1;

		public bool CBStage2;

		public bool CBStage3;

		public bool CBStage4;

		public decimal NumericPriceMoves;

		public decimal NumericHighVolume;
	}

	public struct PatternDeetStruct
	{
		public string sDescription;

		public string sPerformance;

		public int iReversal;

		public int iContinuation;

		public int iFailureRate;

		public int iChangeTrend;

		public int iPctMeetingTargetUp;

		public int iPctMeetingTargetDown;

		public int iThrowbacks;

		public int iPullbacks;

		public int iBreakoutUp;

		public int iBreakoutDown;

		public int iPercentageBust;

		public float iTall;

		public int iWide;

		public string sTips;
	}

	public sealed class Simple3Des
	{
		private readonly TripleDESCryptoServiceProvider TripleDes;

		private byte[] TruncateHash(string key, int length)
		{
			SHA1CryptoServiceProvider sHA1CryptoServiceProvider = new SHA1CryptoServiceProvider();
			byte[] bytes = Encoding.Unicode.GetBytes(key);
			return (byte[])Utils.CopyArray((Array)sHA1CryptoServiceProvider.ComputeHash(bytes), (Array)new byte[checked(length - 1 + 1)]);
		}

		public Simple3Des(string key)
		{
			TripleDes = new TripleDESCryptoServiceProvider();
			TripleDes.Key = TruncateHash(key, TripleDes.KeySize / 8);
			TripleDes.IV = TruncateHash("", TripleDes.BlockSize / 8);
		}

		public string EncryptData(string plaintext)
		{
			byte[] bytes = Encoding.Unicode.GetBytes(plaintext);
			MemoryStream memoryStream = new MemoryStream();
			CryptoStream cryptoStream = new CryptoStream(memoryStream, TripleDes.CreateEncryptor(), CryptoStreamMode.Write);
			cryptoStream.Write(bytes, 0, bytes.Length);
			cryptoStream.FlushFinalBlock();
			return Convert.ToBase64String(memoryStream.ToArray());
		}

		public string DecryptData(string encryptedtext)
		{
			byte[] array = Convert.FromBase64String(encryptedtext);
			MemoryStream memoryStream = new MemoryStream();
			CryptoStream cryptoStream = new CryptoStream(memoryStream, TripleDes.CreateDecryptor(), CryptoStreamMode.Write);
			cryptoStream.Write(array, 0, array.Length);
			cryptoStream.FlushFinalBlock();
			return Encoding.Unicode.GetString(memoryStream.ToArray());
		}
	}

	public static byte[] DEFAULTPATTERNLIST = new byte[124]
	{
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 1, 1, 1, 0, 0, 0,
		0, 0, 0, 1, 0, 0, 1, 1, 0, 0,
		0, 0, 1, 1, 0, 0, 1, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0
	};

	public const int NUMPATTERNS = 124;

	public const int NUMCANDLES = 105;

	private const double AXISMAX = 1.001;

	private const double AXISMIN = 0.999;

	public const bool MYDEBUG = false;

	public const string Version = "Copyright (c) 2016-2024 by Thomas Bulkowski and ThePatternSite.com. All rights reserved.";

	public const string PATTERNZCAPTION = "Patternz: ThePatternSite.com";

	public const string RegString = "HKEY_CURRENT_USER\\Software\\PatternzSoftware\\";

	public const string KEYUF = "UpdateForm";

	public const string PatName = "Patternz";

	public const decimal gSECFEE = 20.7m;

	public static bool SignedLicense;

	public const decimal VBOTTOMRETRACE = 0.382m;

	public static string TIINGOURL = "https://api.tiingo.com/tiingo/daily/";

	public static string FINNURL = "https://finnhub.io/api/v1/";

	public static string IEXURL = "https://cloud.iexapis.com/stable/stock/";

	public static string BARCHARTURL = "https://marketdata.websol.barchart.com/getHistory.csv?apikey=";

	public static string SDURL = "https://api.stockdata.org/v1/data/eod?symbols=";

	public static string EODHDURL = "https://eodhistoricaldata.com/api/eod/";

	public static string UNIBITURL = "https://api.unibit.ai/v2/stock/historical/";

	public static string ConfigLocation;

	public static string FilterConfigName = "\\Filter.cfg";

	private static readonly string sBearFile = "\\BearMarkets.dat";

	public static readonly string SimulatorCfg = "\\Sim.cfg";

	public static BearMktsStruct[] BearMkts;

	public const int UP = 1;

	public const int DOWN = -1;

	public const int NEUTRAL = 0;

	public const int FLAT = 0;

	public const int USETOPS = 1;

	public const int USEBOTTOMs = -1;

	public static int cTall = 1;

	public static int ShortPat = -1;

	public static int cUnknown = 0;

	public static byte[] PatternList = new byte[124];

	public static bool PLChanged = false;

	public static int iDCBPERCENTRISE = 15;

	public static decimal GapSize;

	public const decimal DEFAULTGAPSIZE = 0.2m;

	public static int FormTypeLoaded;

	public const int srcLISTFORM = 0;

	public const int srcLISCHARTFORM = 1;

	public const int srcCHARTFORM = 2;

	public const int srcOTHERFORM = 3;

	public const int srcSIMFORM = 4;

	public static bool NestedSpecial;

	public const int NOTUSED = -1;

	public const int TwoDance = 0;

	public const int TwoDid = 23;

	public const int TwoTall = 22;

	public const int ThreeLR = 32;

	public const int ThreeLRInv = 31;

	public const int ABCDBear = 4;

	public const int ABCDBull = 5;

	public const int BatBear = 11;

	public const int BatBull = 10;

	public const int BigM = 116;

	public const int BigW = 115;

	public const int BroadBotm = 114;

	public const int BroadTop = 111;

	public const int BroadWedgeAsc = 110;

	public const int BroadWedgeDesc = 109;

	public const int RABFA = 113;

	public const int RABFD = 112;

	public const int BARRB = 84;

	public const int BARRT = 83;

	public const int ButterflyBear = 9;

	public const int ButterflyBull = 8;

	public const int CarlVBear = 3;

	public const int CarlVBull = 2;

	public const int ChannelD = 82;

	public const int ChannelU = 1;

	public const int CPRD = 52;

	public const int CPRU = 51;

	public const int CrabBear = 7;

	public const int CrabBull = 6;

	public const int Cup = 81;

	public const int iCup = 48;

	public const int DeadCatBounce = 100;

	public const int iDCB = 99;

	public const int DiamondB = 80;

	public const int DiamondT = 79;

	public const int Diving = 30;

	public const int DoubleB = 98;

	public const int AADB = 20;

	public const int AEDB = 21;

	public const int EADB = 18;

	public const int EEDB = 19;

	public const int DoubleT = 97;

	public const int AADT = 16;

	public const int AEDT = 17;

	public const int EADT = 14;

	public const int EEDT = 15;

	public const int FakeyBear = 12;

	public const int FakeyBull = 13;

	public const int FallingWedge = 96;

	public const int FLAG = 78;

	public const int HTFlag = 95;

	public const int Gap2H = 122;

	public const int Gap2HInv = 123;

	public const int GapArea = 118;

	public const int GapBreakaway = 117;

	public const int GapContinuation = 119;

	public const int GapExhaustion = 121;

	public const int GapTypeUnkown = 120;

	public const int GartleyBear = 28;

	public const int GartleyBull = 29;

	public const int HeadSBottom = 94;

	public const int HSBComplex = 93;

	public const int HSTComplex = 108;

	public const int HeadSTop = 107;

	public const int HookRevD = 50;

	public const int HookRevU = 49;

	public const int HornB = 106;

	public const int HornT = 105;

	public const int InsideDay = 77;

	public const int IslandRevBot = 76;

	public const int IslandRevTop = 75;

	public const int KeyD = 47;

	public const int KeyU = 46;

	public const int MMD = 74;

	public const int MMU = 73;

	public const int NR4 = 72;

	public const int NR7 = 71;

	public const int ODRB = 70;

	public const int ODRT = 69;

	public const int OCRU = 44;

	public const int OCRD = 45;

	public const int OutsideDay = 68;

	public const int PENNANT = 67;

	public const int PipeB = 104;

	public const int PipeT = 103;

	public const int PivotD = 43;

	public const int PivotU = 42;

	public const int Pothole = 37;

	public const int RectB = 102;

	public const int RectT = 101;

	public const int RisingWedge = 92;

	public const int Roof = 36;

	public const int iRoof = 35;

	public const int RoundB = 66;

	public const int RoundT = 65;

	public const int ScallopD = 63;

	public const int ScallopA = 64;

	public const int iScallopA = 62;

	public const int iScallopD = 61;

	public const int Shark32 = 60;

	public const int SpikeD = 40;

	public const int SpikeU = 41;

	public const int ThreeFallPeaks = 91;

	public const int ThreeRiseValley = 90;

	public const int ThreeBar = 59;

	public const int TrendD = 58;

	public const int TrendU = 57;

	public const int TriangleAsc = 89;

	public const int TriangleDesc = 88;

	public const int TriangleSym = 87;

	public const int TripleBot = 86;

	public const int TripleTop = 85;

	public const int UDB = 34;

	public const int UDT = 33;

	public const int VBOTTOM = 56;

	public const int VTOP = 55;

	public const int VerticalD = 24;

	public const int VerticalU = 25;

	public const int WRB = 54;

	public const int WRT = 53;

	public const int WIDED = 39;

	public const int WIDEU = 38;

	public const int WolfeBear = 27;

	public const int WolfeBull = 26;

	public const string p2Dance = "2-Dance";

	public const string p2Did = "2-Did";

	public const string p2Tall = "2-Tall";

	public const string pABCDBear = "AB=CD, bearish";

	public const string pABCDBull = "AB=CD, bullish";

	public const string pBatBear = "Bat, bearish";

	public const string pBatBull = "Bat, bullish";

	public const string pBigM = "Big M";

	public const string pBigW = "Big W";

	public const string pRABFA = "Broadening formation, right-angled & ascending";

	public const string pRABFD = "Broadening formation, right-angled & descending";

	public const string pBroadBotm = "Broadening bottom";

	public const string pBroadTop = "Broadening top";

	public const string pBroadWedgeAsc = "Broadening wedge, ascending";

	public const string pBroadWedgeDesc = "Broadening wedge, descending";

	public const string pBARRB = "Bump-and-run reversal, bottom";

	public const string pBARRT = "Bump-and-run reversal, top";

	public const string pButterflyBear = "Butterfly, bearish";

	public const string pButterflyBull = "Butterfly, bullish";

	public const string pCarlVBear = "Carl V, bearish";

	public const string pCarlVBull = "Carl V, bullish";

	public const string pChannelD = "Channel, down";

	public const string pChannelU = "Channel, up";

	public const string pCrabBear = "Crab, bearish";

	public const string pCrabBull = "Crab, bullish";

	public const string pCPRD = "Closing price reversal, downtrend";

	public const string pCPRU = "Closing price reversal, uptrend";

	public const string pCUP = "Cup with handle";

	public const string pICUP = "Cup with handle, inverted";

	public const string pDeadCatBounce = "Dead-cat bounce";

	public const string piDCB = "Dead-cat bounce, inverted";

	public const string pDIAMONDB = "Diamond bottom";

	public const string pDIAMONDT = "Diamond top";

	public const string pDiving = "Diving board";

	public const string pDoubleB = "Double bottoms (all Types)";

	public const string pAADB = "Double bottom, Adam & Adam";

	public const string pAEDB = "Double bottom, Adam & Eve";

	public const string pEADB = "Double bottom, Eve & Adam";

	public const string pEEDB = "Double bottom, Eve & Eve";

	public const string pDoubleT = "Double tops (all Types)";

	public const string pAADT = "Double top, Adam & Adam";

	public const string pAEDT = "Double top, Adam & Eve";

	public const string pEADT = "Double top, Eve & Adam";

	public const string pEEDT = "Double top, Eve & Eve";

	public const string pFakeyBear = "Fakey, bearish";

	public const string pFakeyBull = "Fakey, bullish";

	public const string pFallingWedge = "Falling wedge";

	public const string pFlag = "Flag";

	public const string pFLATBASE = "Flat base";

	public const string pHTFlag = "Flag, high and tight";

	public const string pGap2H = "Gap 2H";

	public const string pGap2HInv = "Gap 2H, inverted";

	public const string pGapBreakaway = "Gap, breakaway";

	public const string pGapArea = "Gap, area or common";

	public const string pGapContinuation = "Gap, continuation";

	public const string pGapExhaustion = "Gap, exhaustion";

	public const string pGapTypeUnkown = "Gap, type unknown";

	public const string pGartleyBear = "Gartley, bearish";

	public const string pGartleyBull = "Gartley, bullish";

	public const string pHeadSBottom = "Head-and-shoulders bottom";

	public const string pHSBComplex = "Head-and-shoulders complex bottom";

	public const string pHSTComplex = "Head-and-shoulders complex top";

	public const string pHeadSTop = "Head-and-shoulders top";

	public const string pHookRevD = "Hook reversal, downtrend";

	public const string pHookRevU = "Hook reversal, uptrend";

	public const string pHCR = "Horizontal consolidation region";

	public const string pHornB = "Horn bottom";

	public const string pHornT = "Horn top";

	public const string pInsideDay = "Inside day";

	public const string pIslandRevBot = "Island reversal, bottom";

	public const string pIslandRevTop = "Island reversal, top";

	public const string pKeyD = "Key reversal, downtrend";

	public const string pKeyU = "Key reversal, uptrend";

	public const string pMMD = "Measured move down";

	public const string pMMU = "Measured move up";

	public const string pNR4 = "NR4";

	public const string pNR7 = "NR7";

	public const string pOCRD = "Open-close reversal, downtrend";

	public const string pOCRU = "Open-close reversal, uptrend";

	public const string pODRB = "One day reversal, bottom";

	public const string pODRT = "One day reversal, top";

	public const string pOutsideDay = "Outside day";

	public const string pPENNANT = "Pennant";

	public const string pPipeB = "Pipe bottom";

	public const string pPipeT = "Pipe top";

	public const string pPivotD = "Pivot point reversal, downtrend";

	public const string pPivotU = "Pivot point reversal, uptrend";

	public const string pPothole = "Pothole";

	public const string pRectB = "Rectangle bottom";

	public const string pRectT = "Rectangle top";

	public const string pRisingWedge = "Rising wedge";

	public const string pRoof = "Roof";

	public const string pIRoof = "Roof, inverted";

	public const string pRoundB = "Rounding bottom";

	public const string pRoundT = "Rounding top";

	public const string pScallopA = "Scallop, ascending";

	public const string pScallopAI = "Scallop, ascending And inverted";

	public const string pScallopD = "Scallop, descending";

	public const string pScallopDI = "Scallop, descending And inverted";

	public const string pShark32 = "Shark-32";

	public const string pSpikeD = "Spike down";

	public const string pSpikeU = "Spike up";

	public const string pThreeBar = "Three bar";

	public const string pThreeFallPeaks = "Three falling peaks";

	public const string pThreeLR = "Three LR";

	public const string pThreeLRInv = "Three LR inverted";

	public const string pThreeRiseValley = "Three rising valleys";

	public const string pTrendD = "Trendline, down";

	public const string pTrendU = "Trendline, up";

	public const string pTriangleAsc = "Triangle, ascending";

	public const string pTriangleDesc = "Triangle, descending";

	public const string pTriangleSym = "Triangle, symmetrical";

	public const string pTripleBot = "Triple bottom";

	public const string pTripleTop = "Triple top";

	public const string pUglyDB = "Ugly double bottom";

	public const string pUglyDT = "Ugly double top";

	public const string pVerticalD = "Vertical run down";

	public const string pVerticalU = "Vertical run up";

	public const string pVBottom = "V-bottom";

	public const string pVTop = "V-top";

	public const string pWRT = "Weekly reversal top";

	public const string pWRB = "Weekly reversal bottom";

	public const string pWIDEU = "Wide ranging day, upside reversal";

	public const string pWIDED = "Wide ranging day, downside reversal";

	public const string pWolfeBear = "Wolfe wave, bearish";

	public const string pWolfeBull = "Wolfe wave, bullish";

	public const int TLMAXTLENGTH = 1000;

	public static int TLUpLength;

	public static int TLDNLength;

	public static bool IntradayData = false;

	public static int pfPctRise;

	public static bool pfPRChanged;

	public static bool StrictPatterns = false;

	public const int ffDATE = 0;

	public const int ffTIME = 1;

	public const int ffOPEN = 2;

	public const int ffHIGH = 3;

	public const int ffLOW = 4;

	public const int ffCLOSE = 5;

	public const int ffVOLUME = 6;

	public const int ffADJCLOSE = 7;

	public const int ffDIV = 8;

	public const int ffSPLIT = 9;

	public const int PA_SIZE = 9;

	public const int HLC_OPEN = 0;

	public const int HLC_HIGH = 1;

	public const int HLC_LOW = 2;

	public const int HLC_CLOSE = 3;

	public const int HLC_VOLUME = 4;

	public const int HLC_ADJCLOSE = 5;

	private const int sDATE = 6;

	private const int sTIME = 7;

	public const int pHIGH = 0;

	public const int pLOW = 1;

	public const int pOPEN = 2;

	public const int pCLOSE = 3;

	public static SizeF StringSize = default(SizeF);

	public const int iDATE = 0;

	public const int iTIME = 1;

	public const int PROCESSMOREFILES = 2;

	public const int SKIPTHISONE = 1;

	public const int FILTERTHISONE = 3;

	public const bool pERROR = true;

	public const string sDateFormat = "yyyy-MM-dd";

	public const string DateTimeFormat = "yyyy-MM-dd HH:mm";

	public static string UserDate;

	public const string ShortDecimal = "0.####";

	public static string OpenPath = "";

	public static bool PathChanged;

	public static decimal[,] nHLC = new decimal[6, 1];

	public static DateTime[,] nDT = new DateTime[2, 1];

	public static object[,] sHLC = new object[8, 1];

	public static int LBIndex;

	public static int[] FileFormat = new int[8];

	public static bool[] ckFileFormat = new bool[8];

	public static bool ffDateTimeFormat;

	public static bool FileFormatChanged;

	public static bool RemovePatternzFlag;

	public static int HLCRange = 0;

	public static CalloutAnnotation Annot;

	public static string ErrorMessage;

	public static int ErrorCount;

	public static int GoodCount;

	public const int pUNKNOWN = -1;

	public const int pDAILY = 0;

	public const int pWEEKLY = 1;

	public const int pMONTHLY = 2;

	public static int ChartPeriodShown = -1;

	private const decimal MINFUTURES = 0.25m;

	private const decimal SORTAFUTURES = 2.5m;

	public static bool Futures = false;

	public static bool NearFutures = false;

	public static bool ChartVolume;

	public static bool ShowCandles;

	public static bool ShowAllPatterns = true;

	public static DateTime ChartStart;

	public static DateTime ChartEnd;

	public static int ChartStartIndex;

	public static int ChartEndIndex;

	public static long DateLookback = 400L;

	public static bool DLBChanged = false;

	public static int iFib1 = -1;

	public static int iFib2 = -1;

	public static bool Toggle = false;

	public static int MAType;

	public static int MALength = 50;

	public static bool MAUsed = false;

	public const int SMA = 1;

	public const int EMA = 2;

	public const int CANDLES = 0;

	public const int OHLC = 1;

	public static int ChartType = 0;

	public static int DecimalsUsed;

	public static int UserDecimals;

	public static int DECIMALSUSER = 1;

	public static int DECIMALSFILE = 2;

	public static int DECIMALSBOTH = 3;

	public static int DecimalsOption;

	public static int TWODECIMALS = 2;

	public const int KEEP = 1;

	public const int DISCARD = 2;

	public static int DiscardQuote = 1;

	public static int lsDiscardQuote;

	public static Color UpCandleColor;

	public static Color DownCandleColor;

	public static Color ChartBGColor;

	public static Color VolumeBGColor;

	public static Color PriceBarColor;

	public static bool Annotations;

	public static int iFFPatternTraded;

	public static int iFFPatternType;

	public static bool PatternTargets;

	public static bool LCFPatternTargets;

	public static bool ShowConfirmation;

	public static bool ShowStopLoss;

	public static bool ShowTargetprice;

	public static bool ShowUltHighLow;

	public static bool ShowUnHit;

	public static bool ShowUpTarget;

	public static int ShowUpPercentage;

	public static bool ShowDownTarget;

	public static int ShowDownPercentage;

	public static bool IncludePhrase;

	public static int SkipType;

	public static bool ShowBARRLines;

	public const int NOPATTERNS = 1;

	public const int NOOPEN = 2;

	public const int dSYMBOL = 0;

	public const int dLASTCLOSE = 1;

	public const int dDESCRIPTION = 2;

	public const int dSTART = 3;

	public const int dEND = 4;

	public const int dBREAKOUT = 5;

	public const int dBKOUTDATE = 6;

	public const int dBKOUTPRICE = 7;

	public const int dFillPRICE = 8;

	public const int dVOLUME = 9;

	public const int dULTHILOW = 10;

	public const int dULTHLDATE = 11;

	public const int dTARGET = 12;

	public const int dVOLATILITYSTOP = 13;

	public const int dSTATUS = 14;

	public const int dWidth = 15;

	public const int dHeight = 16;

	public const int dSTAGE = 17;

	public const int dSPECIAL = 18;

	public const int dSCALE = 19;

	public const int dCOLUMNCOUNT = 20;

	public static int[] WStages;

	public static int ArticleNumber;

	public static int NewsDateRB;

	public const int NewsPUBDATE = 0;

	public const int NewsHEADLINE = 1;

	public const int NewsDESCRIPTION = 2;

	public const int NewsSOURCE = 3;

	public const int NewsURL = 4;

	public const int NewsARTICLELIMIT = 5;

	public const int NewsUSEDATES = 6;

	public static byte[] NewsOptions = new byte[7];

	public static byte[] NewsDEFAULTS = new byte[7] { 1, 1, 1, 0, 0, 1, 0 };

	public static bool NewsOptionsChanged;

	public static long LFDateLookBack = 400L;

	public static bool LFPatterns = true;

	public static bool LFCandles = false;

	public const int MAXPATTERNWIDTHBars = 126;

	public static int CandleCount;

	public static int PatternCount;

	public static CandleFmtns[] CandlePatterns;

	public static DisplayFmtns[] ChartPatterns;

	public static bool UseOriginalDate = false;

	public static bool Quiet = false;

	public static bool HideMessages = false;

	public static string IndexSymbol;

	public static long CPIDateLookback = 262L;

	public static InfoArray CPInfo;

	public static int RadButton;

	public static List<LineEndPoints> LinesList = new List<LineEndPoints>();

	public static Point FirstPoint;

	public static Point TempPoint;

	public const int SimFAILS = 1;

	public const int SimNONFAILS = 2;

	public const int SimBOTH = 3;

	public static SimStruct SimGlobals;

	public const int PATSTART = 1;

	public const int PATEND = 2;

	public const int PATBKOUT = 3;

	public const int PATEARLIER = 4;

	public static int PauseSimulator = 4;

	public static int VIEWYEARS = 520;

	public static bool QuoteInfo = false;

	public static bool Recursive = false;

	public static int TimerRequests = 5;

	public static bool AutoRetry = false;

	public static long UFDateLookBack = 400L;

	public static string CurrentSymbol;

	public static bool CustomCheckbox;

	public static DialogResult CustomResult;

	public static int UpdatePeriod;

	public const int UFUPDATE = 2;

	public const int UFHISTORY = 3;

	public const int SOURCEYAHOO = 1;

	public const int SOURCETIINGO = 4;

	public const int SOURCEFINNHUB = 6;

	public const int SOURCEIEX = 7;

	public const int SOURCEBARCHART = 8;

	public const int SOURCESTOCKDATA = 9;

	public const int SOURCEUNIBIT = 10;

	public const int SOURCEEODHD = 11;

	public static string BarchartKey;

	public static string lsBarchartKey;

	public static string FinnhubKey;

	public static string lsFinnhubKey;

	public static string IEXKey;

	public static string lsIEXKey;

	public static string TiingoKey;

	public static string lsTiingoKey;

	public static string SDKey;

	public static string lsSDKey;

	public static string UnibitKey;

	public static string lsUnibitKey;

	public static string EODHDKey;

	public static string lsEODHDKey;

	public static int UpdateSource;

	public static string PDSelectionPath;

	public static string[] DBList = new string[7] { "BSE (Bombay Stock Exchange)", "FSE (Frankfurt Stock Exchange)", "HKEX (Hong Kong Exchange)", "LSE (London Stock Exchange)", "NSE (National Stock Exchange of India)", "TSE (Tokyo Stock Exchange)", "WIKI (US EOD stock prices)" };

	public static string DBName;

	public static string lsDBName;

	public static bool lsDBList;

	public static string RenameSymbolString;

	private static readonly Regex CatchDecimals = new Regex("^\\d*(?:\\.?(?<Decimals>\\d*))", RegexOptions.Multiline | RegexOptions.ExplicitCapture | RegexOptions.Compiled | RegexOptions.Singleline | RegexOptions.CultureInvariant);

	public static int PASSNAME = 1;

	public static int PASSINDEX = 2;

	public static string TiingoMsg = "Tiingo is for https://www.tiingo.com/welcome (link has been pasted to the clipboard) which is a free quote provider.\r\n\r\nVisit their website to see if they provide the quotes you seek. They limit access to 500 unique symbols per month (as well as other limits. Check their website for more information).\r\n\r\nNO access is provided unless you register for an API token. Paste the token in the space provided on this form to use Tiingo.";

	public static int SDFUpdateSource;

	public static bool Splits;

	public static bool Dividends;

	public static int SDFDateLookBack;

	public static SplitsInfoArray[] SplitArray;

	public static int SFDateLookBack;

	public static bool SFStrict;

	public static int SFDWM;

	public static int Vendor;

	public static int FINNHUB = 1;

	public static int IEX = 2;

	public static int MSFCombo;

	public static bool EntireFile;

	public static int SFDayOfWeek = 1;

	public static int SFMonthLB = 0;

	public static int SFDaily = 0;

	public static int SFMONTHLY = 1;

	public static int SFOTHER = 2;

	public static int SFRBSelected;

	public static FilterStruct FilterGlobals;

	public static PatternDeetStruct[] PDeets = new PatternDeetStruct[125];

	public static int CalcPatternHeight(int PatternType, decimal PatternTop, decimal PatternBottom, int BkoutDirection, int iEnd)
	{
		decimal[] array = new decimal[4];
		switch (PatternType)
		{
		case 0:
			return cUnknown;
		case 23:
			return cUnknown;
		case 22:
			return cUnknown;
		case 32:
			return cUnknown;
		case 31:
			return cUnknown;
		case 4:
			array = new decimal[4] { 16.1m, 21.7m, 16.9m, 30m };
			break;
		case 5:
			array = new decimal[4] { 15.6m, 20.5m, 18.8m, 15.6m };
			break;
		case 11:
			array = new decimal[4] { 16.5m, 23.3m, 15.3m, 25.1m };
			break;
		case 10:
			array = new decimal[4] { 14.5m, 16.9m, 20.5m, 31.2m };
			break;
		case 116:
			array = new decimal[4] { 0m, 0m, 12.4m, 15.1m };
			break;
		case 115:
			array = new decimal[4] { 11.9m, 16.2m, 0m, 0m };
			break;
		case 114:
			array = new decimal[4] { 12m, 18.8m, 13.2m, 21.5m };
			break;
		case 111:
			array = new decimal[4] { 10.6m, 15.2m, 10.9m, 18.5m };
			break;
		case 110:
			array = new decimal[4] { 14.8m, 14.7m, 18.7m, 18.9m };
			break;
		case 109:
			array = new decimal[4] { 15.9m, 27m, 13.8m, 34m };
			break;
		case 113:
			array = new decimal[4] { 10.6m, 14.6m, 11.4m, 18.4m };
			break;
		case 112:
			array = new decimal[4] { 9.7m, 16.6m, 10.4m, 16.2m };
			break;
		case 84:
			array = new decimal[4] { 27.2m, 39.7m, 0m, 0m };
			break;
		case 83:
			array = new decimal[4] { 0m, 0m, 32.1m, 32m };
			break;
		case 9:
			array = new decimal[4] { 16.1m, 22.3m, 16.3m, 25.4m };
			break;
		case 8:
			array = new decimal[4] { 17.5m, 31.2m, 25m, 42.8m };
			break;
		case 3:
			array = new decimal[4] { 12.6m, 0m, 11.6m, 0m };
			break;
		case 2:
			array = new decimal[4] { 12.5m, 16.4m, 14.6m, 21.6m };
			break;
		case 82:
			return cUnknown;
		case 1:
			return cUnknown;
		case 52:
			return cUnknown;
		case 51:
			return cUnknown;
		case 7:
			array = new decimal[4] { 20.9m, 25.7m, 26.6m, 35.2m };
			break;
		case 6:
			array = new decimal[4] { 20.6m, 29.8m, 33.1m, 48.5m };
			break;
		case 81:
			array = new decimal[4] { 23.2m, 31m, 0m, 0m };
			break;
		case 48:
			array = new decimal[4] { 0m, 0m, 28.8m, 44.2m };
			break;
		case 100:
			return cUnknown;
		case 99:
			return cUnknown;
		case 80:
			array = new decimal[4] { 10.9m, 19.6m, 12.1m, 18.5m };
			break;
		case 79:
			array = new decimal[4] { 9.8m, 13.9m, 9.9m, 16.7m };
			break;
		case 30:
			array = new decimal[4] { 26.9m, 37.5m, 51.2m, 84.9m };
			break;
		case 98:
			array = new decimal[4] { 14.7m, 21.8m, 0m, 0m };
			break;
		case 20:
			array = new decimal[4] { 9.4m, 17.7m, 0m, 0m };
			break;
		case 21:
			array = new decimal[4] { 12.4m, 19m, 0m, 0m };
			break;
		case 18:
			array = new decimal[4] { 11.5m, 17.1m, 0m, 0m };
			break;
		case 19:
			array = new decimal[4] { 14.7m, 21.8m, 0m, 0m };
			break;
		case 97:
			array = new decimal[4] { 0m, 0m, 13.7m, 24.9m };
			break;
		case 16:
			array = new decimal[4] { 0m, 0m, 7.1m, 15.3m };
			break;
		case 17:
			array = new decimal[4] { 0m, 0m, 11.4m, 20.6m };
			break;
		case 14:
			array = new decimal[4] { 0m, 0m, 9.6m, 18.1m };
			break;
		case 15:
			array = new decimal[4] { 0m, 0m, 13.7m, 24.9m };
			break;
		case 12:
			return cUnknown;
		case 13:
			return cUnknown;
		case 96:
			array = new decimal[4] { 15m, 22.6m, 16.1m, 26.4m };
			break;
		case 78:
			array = new decimal[4] { 4.3m, 6.7m, 4.4m, 8.8m };
			break;
		case 95:
			array = new decimal[4] { 14.8m, 15.7m, 0m, 0m };
			break;
		case 122:
			return cUnknown;
		case 123:
			return cUnknown;
		case 118:
			return cUnknown;
		case 117:
			return cUnknown;
		case 119:
			return cUnknown;
		case 121:
			return cUnknown;
		case 120:
			return cUnknown;
		case 28:
			array = new decimal[4] { 18.4m, 25.5m, 18m, 33m };
			break;
		case 29:
			array = new decimal[4] { 18m, 22.9m, 23.4m, 37.2m };
			break;
		case 94:
			array = new decimal[4] { 13.4m, 19.8m, 0m, 0m };
			break;
		case 93:
			array = new decimal[4] { 15.3m, 23.1m, 0m, 0m };
			break;
		case 108:
			array = new decimal[4] { 0m, 0m, 15.4m, 22.8m };
			break;
		case 107:
			array = new decimal[4] { 0m, 0m, 12.5m, 18.8m };
			break;
		case 50:
			return cUnknown;
		case 49:
			return cUnknown;
		case 106:
			array = new decimal[4] { 13.5m, 17.8m, 0m, 0m };
			break;
		case 105:
			array = new decimal[4] { 0m, 0m, 14m, 19.7m };
			break;
		case 77:
			return cUnknown;
		case 76:
			array = new decimal[4] { 5.2m, 9.6m, 0m, 0m };
			break;
		case 75:
			array = new decimal[4] { 0m, 0m, 5.6m, 10.4m };
			break;
		case 47:
			return cUnknown;
		case 46:
			return cUnknown;
		case 74:
			return cUnknown;
		case 73:
			return cUnknown;
		case 72:
			return cUnknown;
		case 71:
			return cUnknown;
		case 70:
			return cUnknown;
		case 69:
			return cUnknown;
		case 44:
			return cUnknown;
		case 45:
			return cUnknown;
		case 68:
			return cUnknown;
		case 67:
			array = new decimal[4] { 4.2m, 6.7m, 4.3m, 7.3m };
			break;
		case 104:
			array = new decimal[4] { 12.2m, 15.3m, 0m, 0m };
			break;
		case 103:
			array = new decimal[4] { 0m, 0m, 13m, 16.8m };
			break;
		case 43:
			return cUnknown;
		case 42:
			return cUnknown;
		case 37:
			return cUnknown;
		case 102:
			array = new decimal[4] { 8.3m, 11.2m, 9.6m, 13m };
			break;
		case 101:
			array = new decimal[4] { 7.9m, 10m, 7.1m, 11m };
			break;
		case 92:
			array = new decimal[4] { 11.9m, 18.3m, 13.7m, 20.1m };
			break;
		case 36:
			array = new decimal[4] { 9.2m, 14.4m, 8.7m, 13.8m };
			break;
		case 35:
			array = new decimal[4] { 8.7m, 13.9m, 9.1m, 15.9m };
			break;
		case 66:
			array = new decimal[4] { 21.9m, 25.2m, 0m, 0m };
			break;
		case 65:
			array = new decimal[4] { 24.9m, 25.7m, 36.2m, 52.1m };
			break;
		case 63:
			array = new decimal[4] { 17.8m, 22m, 18.4m, 30m };
			break;
		case 64:
			array = new decimal[4] { 18.2m, 22.7m, 18.7m, 25.9m };
			break;
		case 62:
			array = new decimal[4] { 17.4m, 21.4m, 17.2m, 29.8m };
			break;
		case 61:
			array = new decimal[4] { 15.5m, 23.4m, 21.1m, 37.7m };
			break;
		case 60:
			return cUnknown;
		case 40:
			return cUnknown;
		case 41:
			return cUnknown;
		case 91:
			array = new decimal[4] { 0m, 0m, 22.4m, 37.1m };
			break;
		case 90:
			array = new decimal[4] { 22.4m, 27.6m, 0m, 0m };
			break;
		case 59:
			return cUnknown;
		case 58:
			return cUnknown;
		case 57:
			return cUnknown;
		case 89:
			array = new decimal[4] { 9.5m, 14.9m, 9.4m, 17.3m };
			break;
		case 88:
			array = new decimal[4] { 9.5m, 16.8m, 11.4m, 17.4m };
			break;
		case 87:
			array = new decimal[4] { 10.1m, 18.3m, 11.4m, 19m };
			break;
		case 86:
			array = new decimal[4] { 9.9m, 14.7m, 0m, 0m };
			break;
		case 85:
			array = new decimal[4] { 0m, 0m, 9.7m, 16.9m };
			break;
		case 34:
			array = new decimal[4] { 12.5m, 0m, 0m, 0m };
			break;
		case 33:
			array = new decimal[4];
			break;
		case 56:
			array = new decimal[4] { 34m, 41.3m, 0m, 0m };
			break;
		case 55:
			array = new decimal[4] { 0m, 0m, 25.3m, 31m };
			break;
		case 24:
			return cUnknown;
		case 25:
			return cUnknown;
		case 54:
			return cUnknown;
		case 53:
			return cUnknown;
		case 39:
			return cUnknown;
		case 38:
			return cUnknown;
		case 27:
			return cUnknown;
		case 26:
			return cUnknown;
		}
		int num = 1;
		checked
		{
			int num2 = BearMkts.Length - 1;
			for (int i = 0; i <= num2; i++)
			{
				if ((DateTime.Compare(nDT[0, iEnd], BearMkts[i].StartDate) >= 0) & (DateTime.Compare(nDT[0, iEnd], BearMkts[i].EndDate) <= 0))
				{
					num = -1;
					break;
				}
			}
			decimal num3 = nHLC[3, iEnd];
			int num4 = default(int);
			switch (num)
			{
			case 1:
				switch (BkoutDirection)
				{
				case 1:
					num4 = 0;
					break;
				case -1:
					num4 = 2;
					break;
				}
				break;
			case -1:
				switch (BkoutDirection)
				{
				case 1:
					num4 = 1;
					break;
				case -1:
					num4 = 3;
					break;
				}
				break;
			}
			decimal d = array[num4];
			if (decimal.Compare(num3, 0m) > 0)
			{
				decimal d2 = decimal.Divide(decimal.Multiply(100m, decimal.Subtract(PatternTop, PatternBottom)), num3);
				if (decimal.Compare(d2, d) >= 0)
				{
					return cTall;
				}
				if (decimal.Compare(d2, d) < 0)
				{
					return ShortPat;
				}
			}
			return cUnknown;
		}
	}

	public static float CalculateCharacterWidth(ChartPaintEventArgs e)
	{
		PointF empty = PointF.Empty;
		empty.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, 1.0);
		empty = e.ChartGraphics.GetAbsolutePoint(empty);
		float x = empty.X;
		empty.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, 2.0);
		empty = e.ChartGraphics.GetAbsolutePoint(empty);
		if (StringSize.Width == 0f)
		{
			return empty.X - x - 5.7f;
		}
		return empty.X - x - StringSize.Width / 2f;
	}

	public static void CheckDates(DateTimePicker FromDatePicker, DateTimePicker ToDatePicker)
	{
		//IL_014b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0072: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			try
			{
				if (DateTime.Compare(nDT[0, 0], FromDatePicker.MinDate) < 0)
				{
					return;
				}
				if (IntradayData)
				{
					if ((DateTime.Compare(nDT[0, HLCRange], FromDatePicker.Value) < 0) | (DateTime.Compare(nDT[0, 0], ToDatePicker.Value) > 0))
					{
						MessageBox.Show("The stock ends before the begin date or it begins after the end date. I'll adjust the dates.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
						int num = (int)DateAndTime.DateDiff((DateInterval)4, ToDatePicker.Value, FromDatePicker.Value, (FirstDayOfWeek)1, (FirstWeekOfYear)1);
						ToDatePicker.Value = nDT[0, HLCRange];
						FromDatePicker.Value = DateAndTime.DateAdd("d", (double)num, (object)nDT[0, HLCRange]);
						ChartStart = FromDatePicker.Value;
						ChartEnd = ToDatePicker.Value;
					}
				}
				else if ((DateTime.Compare(nDT[0, HLCRange].Date, FromDatePicker.Value.Date) < 0) | (DateTime.Compare(nDT[0, 0].Date, ToDatePicker.Value.Date) > 0))
				{
					MessageBox.Show("The stock ends before the begin date or it begins after the end date. I'll adjust the dates.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
					int num2 = (int)DateAndTime.DateDiff((DateInterval)4, ToDatePicker.Value.Date, FromDatePicker.Value.Date, (FirstDayOfWeek)1, (FirstWeekOfYear)1);
					ToDatePicker.Value = nDT[0, HLCRange].Date;
					FromDatePicker.Value = DateAndTime.DateAdd("d", (double)num2, (object)nDT[0, HLCRange]);
					ChartStart = FromDatePicker.Value.Date;
					ChartEnd = ToDatePicker.Value.Date;
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				ProjectData.ClearProjectError();
			}
		}
	}

	public static string CheckTradeStatus(int index, decimal StopPrice, decimal TargetPrice, int BkoutDirection)
	{
		string result = "Open";
		if (decimal.Compare(StopPrice, -1m) == 0)
		{
			result = "Not enough data to calculate stop.";
		}
		int hLCRange = HLCRange;
		for (int i = index; i <= hLCRange; i = checked(i + 1))
		{
			switch (BkoutDirection)
			{
			case 1:
				if ((decimal.Compare(TargetPrice, 0m) > 0) & (decimal.Compare(nHLC[1, i], TargetPrice) >= 0))
				{
					result = "Target (" + Conversions.ToString(LimitDecimals(TargetPrice)) + ") reached on " + Strings.Format((object)nDT[0, i], UserDate);
					break;
				}
				if (!((decimal.Compare(StopPrice, 0m) > 0) & (decimal.Compare(nHLC[2, i], StopPrice) <= 0)))
				{
					continue;
				}
				result = "Stop (" + Conversions.ToString(LimitDecimals(StopPrice)) + ") triggered on " + Strings.Format((object)nDT[0, i], UserDate);
				break;
			case -1:
				if ((decimal.Compare(TargetPrice, 0m) > 0) & (decimal.Compare(nHLC[2, i], TargetPrice) <= 0))
				{
					result = "Target (" + Conversions.ToString(LimitDecimals(TargetPrice)) + ") reached on " + Strings.Format((object)nDT[0, i], UserDate);
					break;
				}
				if (!((decimal.Compare(StopPrice, 0m) > 0) & (decimal.Compare(nHLC[1, i], StopPrice) >= 0)))
				{
					continue;
				}
				result = "Stop (" + Conversions.ToString(LimitDecimals(StopPrice)) + ") triggered on " + Strings.Format((object)nDT[0, i], UserDate);
				break;
			default:
				continue;
			}
			break;
		}
		return result;
	}

	public static string ClosestDelimiter(string row)
	{
		int num = 0;
		bool flag = false;
		string[] array = new string[4] { ",", ";", " ", "\t" };
		string text = "-1";
		if (string.IsNullOrWhiteSpace(row))
		{
			return "-1";
		}
		string[] array2 = array;
		foreach (string text2 in array2)
		{
			int num2 = row.Split(new string[1] { text2 }, StringSplitOptions.None).Count();
			if (num2 > num)
			{
				text = text2;
				num = num2;
				flag = false;
			}
			else if (num2 > 0 && num2 == num && Operators.CompareString(text2, " ", false) != 0)
			{
				if (Operators.CompareString(text, " ", false) == 0)
				{
					text = text2;
					num = num2;
					flag = false;
				}
				else
				{
					flag = true;
				}
			}
		}
		if (flag)
		{
			return "-1";
		}
		if (num == 0)
		{
			return "-1";
		}
		return text;
	}

	private static int CountDecimalPlaces(ref string Number)
	{
		return CatchDecimals.Match(Number).Groups["Decimals"].ToString().Length;
	}

	public static void DataPeriodConverter(int PeriodType)
	{
		nHLC = null;
		nDT = null;
		HLCRange = Information.UBound((Array)sHLC, 2);
		checked
		{
			nHLC = new decimal[6, HLCRange + 1];
			nDT = new DateTime[2, HLCRange + 1];
			int i = default(int);
			if ((PeriodType == 0) | IntradayData)
			{
				int hLCRange = HLCRange;
				for (i = 0; i <= hLCRange; i++)
				{
					nHLC[0, i] = Conversions.ToDecimal(sHLC[0, i]);
					nHLC[1, i] = Conversions.ToDecimal(sHLC[1, i]);
					nHLC[2, i] = Conversions.ToDecimal(sHLC[2, i]);
					nHLC[3, i] = Conversions.ToDecimal(sHLC[3, i]);
					nHLC[4, i] = Conversions.ToDecimal(sHLC[4, i]);
					nHLC[5, i] = Conversions.ToDecimal(sHLC[5, i]);
					nDT[1, i] = MyCDate(RuntimeHelpers.GetObjectValue(sHLC[7, i]));
					nDT[0, i] = Conversions.ToDate(Interaction.IIf(IntradayData, (object)MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, i])), (object)MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, i])).Date));
				}
				ChartPeriodShown = 0;
				return;
			}
			switch (PeriodType)
			{
			case 1:
			{
				int num = 0;
				nDT[0, 0] = MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, 0])).Date;
				nHLC[0, 0] = Conversions.ToDecimal(sHLC[0, 0]);
				decimal num2 = Conversions.ToDecimal(sHLC[1, 0]);
				decimal num3 = Conversions.ToDecimal(sHLC[2, 0]);
				nHLC[3, 0] = Conversions.ToDecimal(sHLC[3, 0]);
				nHLC[5, 0] = Conversions.ToDecimal(sHLC[5, 0]);
				decimal num4 = Conversions.ToDecimal(sHLC[4, 0]);
				if (HLCRange - 1 == 0)
				{
					nHLC[4, 0] = Conversions.ToDecimal(sHLC[4, 0]);
					nHLC[1, 0] = num2;
					nHLC[2, 0] = num3;
					num = 1;
				}
				else
				{
					int hLCRange3 = HLCRange;
					for (i = 1; i <= hLCRange3; i++)
					{
						if ((DateAndTime.Weekday(MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, i])), (FirstDayOfWeek)1) == 2) | ((DateAndTime.Weekday(MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, i])), (FirstDayOfWeek)1) < DateAndTime.Weekday(MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, i - 1])), (FirstDayOfWeek)1)) & (DateAndTime.Weekday(MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, i])), (FirstDayOfWeek)1) != 1) & (DateAndTime.Weekday(MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, i])), (FirstDayOfWeek)1) != 7)) | (DateAndTime.DateDiff((DateInterval)4, MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, i - 1])), MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, i])), (FirstDayOfWeek)1, (FirstWeekOfYear)1) > 7))
						{
							nHLC[1, num] = num2;
							nHLC[2, num] = num3;
							nHLC[3, num] = Conversions.ToDecimal(sHLC[3, i - 1]);
							nHLC[5, num] = Conversions.ToDecimal(sHLC[5, i - 1]);
							nHLC[4, num] = num4;
							num4 = default(decimal);
							num++;
							nDT[0, num] = MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, i])).Date;
							nHLC[0, num] = Conversions.ToDecimal(sHLC[0, i]);
							num2 = Conversions.ToDecimal(sHLC[1, i]);
							num3 = Conversions.ToDecimal(sHLC[2, i]);
						}
						if (decimal.Compare(num2, Conversions.ToDecimal(sHLC[1, i])) < 0)
						{
							num2 = Conversions.ToDecimal(sHLC[1, i]);
						}
						if (decimal.Compare(num3, Conversions.ToDecimal(sHLC[2, i])) > 0)
						{
							num3 = Conversions.ToDecimal(sHLC[2, i]);
						}
						num4 = decimal.Add(num4, Conversions.ToDecimal(sHLC[4, i]));
					}
				}
				nHLC[1, num] = num2;
				nHLC[2, num] = num3;
				nHLC[3, num] = Conversions.ToDecimal(sHLC[3, i - 1]);
				nHLC[5, num] = Conversions.ToDecimal(sHLC[5, i - 1]);
				nHLC[4, num] = num4;
				HLCRange = num;
				nHLC = (decimal[,])Utils.CopyArray((Array)nHLC, (Array)new decimal[6, HLCRange + 1]);
				nDT = (DateTime[,])Utils.CopyArray((Array)nDT, (Array)new DateTime[2, HLCRange + 1]);
				ChartPeriodShown = 1;
				break;
			}
			case 2:
			{
				int num = 0;
				nDT[0, 0] = MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, 0])).Date;
				nHLC[0, 0] = Conversions.ToDecimal(sHLC[0, 0]);
				decimal num2 = Conversions.ToDecimal(sHLC[1, 0]);
				decimal num3 = Conversions.ToDecimal(sHLC[2, 0]);
				nHLC[3, 0] = Conversions.ToDecimal(sHLC[3, 0]);
				nHLC[5, 0] = Conversions.ToDecimal(sHLC[5, 0]);
				decimal num4 = Conversions.ToDecimal(sHLC[4, 0]);
				if (HLCRange - 1 == 0)
				{
					nHLC[4, 0] = Conversions.ToDecimal(sHLC[4, 0]);
					nHLC[1, 0] = num2;
					nHLC[2, 0] = num3;
					num = 1;
				}
				else
				{
					int hLCRange2 = HLCRange;
					for (i = 1; i <= hLCRange2; i++)
					{
						if (DateAndTime.Month(MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, i]))) != DateAndTime.Month(MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, i - 1]))))
						{
							nHLC[1, num] = num2;
							nHLC[2, num] = num3;
							nHLC[3, num] = Conversions.ToDecimal(sHLC[3, i - 1]);
							nHLC[5, num] = Conversions.ToDecimal(sHLC[5, i - 1]);
							nHLC[4, num] = num4;
							num4 = default(decimal);
							num++;
							nDT[0, num] = MyCDate(RuntimeHelpers.GetObjectValue(sHLC[6, i])).Date;
							nHLC[0, num] = Conversions.ToDecimal(sHLC[0, i]);
							num2 = Conversions.ToDecimal(sHLC[1, i]);
							num3 = Conversions.ToDecimal(sHLC[2, i]);
						}
						if (decimal.Compare(num2, Conversions.ToDecimal(sHLC[1, i])) < 0)
						{
							num2 = Conversions.ToDecimal(sHLC[1, i]);
						}
						if (decimal.Compare(num3, Conversions.ToDecimal(sHLC[2, i])) > 0)
						{
							num3 = Conversions.ToDecimal(sHLC[2, i]);
						}
						num4 = decimal.Add(num4, Conversions.ToDecimal(sHLC[4, i]));
					}
				}
				nHLC[1, num] = num2;
				nHLC[2, num] = num3;
				nHLC[3, num] = Conversions.ToDecimal(sHLC[3, i - 1]);
				nHLC[5, num] = Conversions.ToDecimal(sHLC[5, i - 1]);
				nHLC[4, num] = num4;
				HLCRange = num;
				nHLC = (decimal[,])Utils.CopyArray((Array)nHLC, (Array)new decimal[6, HLCRange + 1]);
				nDT = (DateTime[,])Utils.CopyArray((Array)nDT, (Array)new DateTime[2, HLCRange + 1]);
				ChartPeriodShown = 2;
				break;
			}
			}
		}
	}

	public static void DisplayFiles(ref ListBox ListBox1)
	{
		if ((Operators.CompareString(OpenPath, "", false) != 0) & Directory.Exists(OpenPath))
		{
			ListBox1.Items.Clear();
			string[] files = Directory.GetFiles(OpenPath, "*.txt");
			foreach (string path in files)
			{
				ListBox1.Items.Add((object)Path.GetFileName(path));
			}
			string[] files2 = Directory.GetFiles(OpenPath, "*.csv");
			foreach (string path2 in files2)
			{
				ListBox1.Items.Add((object)Path.GetFileName(path2));
			}
		}
	}

	public static void EnableDisableDWM(RadioButton Daily, RadioButton Weekly, RadioButton Monthly)
	{
		if (!IntradayData)
		{
			((Control)Daily).Enabled = true;
			((Control)Weekly).Enabled = true;
			((Control)Monthly).Enabled = true;
		}
		else
		{
			((Control)Daily).Enabled = false;
			((Control)Weekly).Enabled = false;
			((Control)Monthly).Enabled = false;
		}
	}

	public static void FillDetails()
	{
		string sPerformance = "Not ranked.";
		string sTips = "No information is available.";
		string text = "Information applies to upward breakouts.";
		string text2 = "Information applies to downward breakouts.";
		PDeets[1].sDescription = "Channel, up";
		PDeets[1].sPerformance = sPerformance;
		PDeets[1].iReversal = -1;
		PDeets[1].iContinuation = -1;
		PDeets[1].iFailureRate = -1;
		PDeets[1].iChangeTrend = -1;
		PDeets[1].iPctMeetingTargetUp = -1;
		PDeets[1].iPctMeetingTargetDown = -1;
		PDeets[1].iThrowbacks = -1;
		PDeets[1].iPullbacks = -1;
		PDeets[1].iBreakoutUp = -1;
		PDeets[1].iBreakoutDown = -1;
		PDeets[1].iPercentageBust = -1;
		PDeets[1].iTall = -1f;
		PDeets[1].iWide = -1;
		PDeets[1].sTips = sTips;
		PDeets[2].sDescription = "Carl V, bullish";
		PDeets[2].sPerformance = sPerformance;
		PDeets[2].iReversal = -1;
		PDeets[2].iContinuation = -1;
		PDeets[2].iFailureRate = 1;
		PDeets[2].iChangeTrend = -1;
		PDeets[2].iPctMeetingTargetUp = 57;
		PDeets[2].iPctMeetingTargetDown = -1;
		PDeets[2].iThrowbacks = 65;
		PDeets[2].iPullbacks = -1;
		PDeets[2].iBreakoutUp = -1;
		PDeets[2].iBreakoutDown = -1;
		PDeets[2].iPercentageBust = -1;
		PDeets[2].iTall = -1f;
		PDeets[2].iWide = -1;
		PDeets[2].sTips = "See ThePatternSite.com for more details.";
		PDeets[3].sDescription = "Carl V, bearish";
		PDeets[3].sPerformance = sPerformance;
		PDeets[3].iReversal = -1;
		PDeets[3].iContinuation = -1;
		PDeets[3].iFailureRate = 24;
		PDeets[3].iChangeTrend = -1;
		PDeets[3].iPctMeetingTargetUp = -1;
		PDeets[3].iPctMeetingTargetDown = 36;
		PDeets[3].iThrowbacks = -1;
		PDeets[3].iPullbacks = 63;
		PDeets[3].iBreakoutUp = -1;
		PDeets[3].iBreakoutDown = -1;
		PDeets[3].iPercentageBust = -1;
		PDeets[3].iTall = -1f;
		PDeets[3].iWide = -1;
		PDeets[3].sTips = "See ThePatternSite.com for more details.";
		PDeets[4].sDescription = "AB=CD, bearish";
		PDeets[4].sPerformance = "5 out of 5 (5 is worst)";
		PDeets[4].iReversal = -1;
		PDeets[4].iContinuation = -1;
		PDeets[4].iFailureRate = 26;
		PDeets[4].iChangeTrend = -1;
		PDeets[4].iPctMeetingTargetUp = 95;
		PDeets[4].iPctMeetingTargetDown = -1;
		PDeets[4].iThrowbacks = -1;
		PDeets[4].iPullbacks = -1;
		PDeets[4].iBreakoutUp = -1;
		PDeets[4].iBreakoutDown = -1;
		PDeets[4].iPercentageBust = -1;
		PDeets[4].sTips = "Reaches point D 95% of the time, but only 32% drop after point D.";
		PDeets[4].iTall = -1f;
		PDeets[4].iWide = -1;
		PDeets[5].sDescription = "AB=CD, bullish";
		PDeets[5].sPerformance = "4 out of 5 (5 is worst)";
		PDeets[5].iReversal = -1;
		PDeets[5].iContinuation = -1;
		PDeets[5].iFailureRate = 12;
		PDeets[5].iChangeTrend = -1;
		PDeets[5].iPctMeetingTargetUp = -1;
		PDeets[5].iPctMeetingTargetDown = 100;
		PDeets[5].iThrowbacks = -1;
		PDeets[5].iPullbacks = -1;
		PDeets[5].iBreakoutUp = -1;
		PDeets[5].iBreakoutDown = -1;
		PDeets[5].iPercentageBust = -1;
		PDeets[5].sTips = "Reaches point D 100% of the time, but only 38% rise after point D.";
		PDeets[5].iTall = -1f;
		PDeets[5].iWide = -1;
		PDeets[6].sDescription = "Crab, bullish";
		PDeets[6].sPerformance = "3 out of 5 (5 is worst)";
		PDeets[6].iReversal = -1;
		PDeets[6].iContinuation = -1;
		PDeets[6].iFailureRate = 7;
		PDeets[6].iChangeTrend = -1;
		PDeets[6].iPctMeetingTargetUp = -1;
		PDeets[6].iPctMeetingTargetDown = -1;
		PDeets[6].iThrowbacks = -1;
		PDeets[6].iPullbacks = -1;
		PDeets[6].iBreakoutUp = -1;
		PDeets[6].iBreakoutDown = -1;
		PDeets[6].iPercentageBust = -1;
		PDeets[6].sTips = "92% turn up (reverse) at point D.";
		PDeets[6].iTall = -1f;
		PDeets[6].iWide = -1;
		PDeets[7].sDescription = "Crab, bearish";
		PDeets[7].sPerformance = "1 (best) out of 5.";
		PDeets[7].iReversal = -1;
		PDeets[7].iContinuation = -1;
		PDeets[7].iFailureRate = 20;
		PDeets[7].iChangeTrend = -1;
		PDeets[7].iPctMeetingTargetUp = -1;
		PDeets[7].iPctMeetingTargetDown = -1;
		PDeets[7].iThrowbacks = -1;
		PDeets[7].iPullbacks = -1;
		PDeets[7].iBreakoutUp = -1;
		PDeets[7].iBreakoutDown = -1;
		PDeets[7].iPercentageBust = -1;
		PDeets[7].sTips = "87% turn down (reverse) at point D.";
		PDeets[7].iTall = -1f;
		PDeets[7].iWide = -1;
		PDeets[8].sDescription = "Butterfly, bullish";
		PDeets[8].sPerformance = "2 out of 5 (5 is worst)";
		PDeets[8].iReversal = -1;
		PDeets[8].iContinuation = -1;
		PDeets[8].iFailureRate = 11;
		PDeets[8].iChangeTrend = -1;
		PDeets[8].iPctMeetingTargetUp = -1;
		PDeets[8].iPctMeetingTargetDown = -1;
		PDeets[8].iThrowbacks = -1;
		PDeets[8].iPullbacks = -1;
		PDeets[8].iBreakoutUp = -1;
		PDeets[8].iBreakoutDown = -1;
		PDeets[8].iPercentageBust = -1;
		PDeets[8].sTips = "91% turn up (reverse) at D";
		PDeets[8].iTall = -1f;
		PDeets[8].iWide = -1;
		PDeets[9].sDescription = "Butterfly, bearish";
		PDeets[9].sPerformance = "4 out of 5 (5 is worst)";
		PDeets[9].iReversal = -1;
		PDeets[9].iContinuation = -1;
		PDeets[9].iFailureRate = 27;
		PDeets[9].iChangeTrend = -1;
		PDeets[9].iPctMeetingTargetUp = -1;
		PDeets[9].iPctMeetingTargetDown = -1;
		PDeets[9].iThrowbacks = -1;
		PDeets[9].iPullbacks = -1;
		PDeets[9].iBreakoutUp = -1;
		PDeets[9].iBreakoutDown = -1;
		PDeets[9].iPercentageBust = -1;
		PDeets[9].sTips = "86% turn down (reverse) at point D.";
		PDeets[9].iTall = -1f;
		PDeets[9].iWide = -1;
		PDeets[10].sDescription = "Bat, bullish";
		PDeets[10].sPerformance = "1 (best) out of 5";
		PDeets[10].iReversal = -1;
		PDeets[10].iContinuation = -1;
		PDeets[10].iFailureRate = 10;
		PDeets[10].iChangeTrend = -1;
		PDeets[10].iPctMeetingTargetUp = -1;
		PDeets[10].iPctMeetingTargetDown = -1;
		PDeets[10].iThrowbacks = -1;
		PDeets[10].iPullbacks = -1;
		PDeets[10].iBreakoutUp = -1;
		PDeets[10].iBreakoutDown = -1;
		PDeets[10].iPercentageBust = -1;
		PDeets[10].sTips = "91% turn up (reverse) at point D.";
		PDeets[10].iTall = -1f;
		PDeets[10].iWide = -1;
		PDeets[11].sDescription = "Bat, bearish";
		PDeets[11].sPerformance = "1 (best) out of 5";
		PDeets[11].iReversal = -1;
		PDeets[11].iContinuation = -1;
		PDeets[11].iFailureRate = 18;
		PDeets[11].iChangeTrend = -1;
		PDeets[11].iPctMeetingTargetUp = -1;
		PDeets[11].iPctMeetingTargetDown = -1;
		PDeets[11].iThrowbacks = -1;
		PDeets[11].iPullbacks = -1;
		PDeets[11].iBreakoutUp = -1;
		PDeets[11].iBreakoutDown = -1;
		PDeets[11].iPercentageBust = -1;
		PDeets[11].sTips = "86% turn down (reverse) at point D.";
		PDeets[11].iTall = -1f;
		PDeets[11].iWide = -1;
		PDeets[12].sDescription = "Fakey, bearish";
		PDeets[12].sPerformance = sPerformance;
		PDeets[12].iReversal = -1;
		PDeets[12].iContinuation = -1;
		PDeets[12].iFailureRate = 56;
		PDeets[12].iChangeTrend = -1;
		PDeets[12].iPctMeetingTargetUp = -1;
		PDeets[12].iPctMeetingTargetDown = -1;
		PDeets[12].iThrowbacks = -1;
		PDeets[12].iPullbacks = -1;
		PDeets[12].iBreakoutUp = -1;
		PDeets[12].iBreakoutDown = -1;
		PDeets[12].iPercentageBust = -1;
		PDeets[12].sTips = "It's a 4 bar pattern.";
		PDeets[12].iTall = -1f;
		PDeets[12].iWide = -1;
		PDeets[13].sDescription = "Fakey, bullish";
		PDeets[13].sPerformance = sPerformance;
		PDeets[13].iReversal = -1;
		PDeets[13].iContinuation = -1;
		PDeets[13].iFailureRate = 47;
		PDeets[13].iChangeTrend = -1;
		PDeets[13].iPctMeetingTargetUp = -1;
		PDeets[13].iPctMeetingTargetDown = -1;
		PDeets[13].iThrowbacks = -1;
		PDeets[13].iPullbacks = -1;
		PDeets[13].iBreakoutUp = -1;
		PDeets[13].iBreakoutDown = -1;
		PDeets[13].iPercentageBust = -1;
		PDeets[13].sTips = "It's a 4 bar pattern.";
		PDeets[13].iTall = -1f;
		PDeets[13].iWide = -1;
		PDeets[14].sDescription = "Double top, Eve & Adam";
		PDeets[14].sPerformance = "16 out of 36 (36 is worst)";
		PDeets[14].iReversal = 100;
		PDeets[14].iContinuation = -1;
		PDeets[14].iFailureRate = 21;
		PDeets[14].iChangeTrend = 27;
		PDeets[14].iPctMeetingTargetUp = -1;
		PDeets[14].iPctMeetingTargetDown = 55;
		PDeets[14].iThrowbacks = -1;
		PDeets[14].iPullbacks = 64;
		PDeets[14].iBreakoutUp = -1;
		PDeets[14].iBreakoutDown = 100;
		PDeets[14].iPercentageBust = 44;
		PDeets[14].sTips = "Patterns without pullbacks see price drop further, on average.";
		PDeets[14].iTall = 9.6f;
		PDeets[14].iWide = 22;
		PDeets[15].sDescription = "Double top, Eve & Eve";
		PDeets[15].sPerformance = "12 out of 36 (36 is worst)";
		PDeets[15].iReversal = 100;
		PDeets[15].iContinuation = -1;
		PDeets[15].iFailureRate = 20;
		PDeets[15].iChangeTrend = 29;
		PDeets[15].iPctMeetingTargetUp = -1;
		PDeets[15].iPctMeetingTargetDown = 43;
		PDeets[15].iThrowbacks = -1;
		PDeets[15].iPullbacks = 65;
		PDeets[15].iBreakoutUp = -1;
		PDeets[15].iBreakoutDown = 100;
		PDeets[15].iPercentageBust = 36;
		PDeets[15].sTips = "Patterns without pullbacks see price drop further, on average.";
		PDeets[15].iTall = 13.7f;
		PDeets[15].iWide = -1;
		PDeets[16].sDescription = "Double top, Adam & Adam";
		PDeets[16].sPerformance = "19 out of 36 (36 is worst)";
		PDeets[16].iReversal = 100;
		PDeets[16].iContinuation = -1;
		PDeets[16].iFailureRate = 25;
		PDeets[16].iChangeTrend = 28;
		PDeets[16].iPctMeetingTargetUp = -1;
		PDeets[16].iPctMeetingTargetDown = 64;
		PDeets[16].iThrowbacks = -1;
		PDeets[16].iPullbacks = 64;
		PDeets[16].iBreakoutUp = -1;
		PDeets[16].iBreakoutDown = 100;
		PDeets[16].iPercentageBust = 44;
		PDeets[16].sTips = "Patterns without pullbacks see price drop further, on average.";
		PDeets[16].iTall = 7.1f;
		PDeets[16].iWide = 15;
		PDeets[17].sDescription = "Double top, Adam & Eve";
		PDeets[17].sPerformance = "10 out of 36 (36 is worst)";
		PDeets[17].iReversal = 100;
		PDeets[17].iContinuation = -1;
		PDeets[17].iFailureRate = 21;
		PDeets[17].iChangeTrend = 30;
		PDeets[17].iPctMeetingTargetUp = -1;
		PDeets[17].iPctMeetingTargetDown = 54;
		PDeets[17].iThrowbacks = -1;
		PDeets[17].iPullbacks = 64;
		PDeets[17].iBreakoutUp = -1;
		PDeets[17].iBreakoutDown = 100;
		PDeets[17].iPercentageBust = 40;
		PDeets[17].sTips = "Patterns without pullbacks see price drop further, on average.";
		PDeets[17].iTall = 11.4f;
		PDeets[17].iWide = -1;
		PDeets[18].sDescription = "Double bottom, Eve & Adam";
		PDeets[18].sPerformance = "20 out of 39 (39 is worst)";
		PDeets[18].iReversal = 100;
		PDeets[18].iContinuation = -1;
		PDeets[18].iFailureRate = 12;
		PDeets[18].iChangeTrend = 59;
		PDeets[18].iPctMeetingTargetUp = 72;
		PDeets[18].iPctMeetingTargetDown = -1;
		PDeets[18].iThrowbacks = 67;
		PDeets[18].iPullbacks = -1;
		PDeets[18].iBreakoutUp = 100;
		PDeets[18].iBreakoutDown = -1;
		PDeets[18].iPercentageBust = 21;
		PDeets[18].sTips = "Patterns without throwbacks see price rise further, on average.";
		PDeets[18].iTall = 11.5f;
		PDeets[18].iWide = 23;
		PDeets[19].sDescription = "Double bottom, Eve & Eve";
		PDeets[19].sPerformance = "5 out of 39 (39 is worst)";
		PDeets[19].iReversal = 100;
		PDeets[19].iContinuation = -1;
		PDeets[19].iFailureRate = 12;
		PDeets[19].iChangeTrend = 61;
		PDeets[19].iPctMeetingTargetUp = 65;
		PDeets[19].iPctMeetingTargetDown = -1;
		PDeets[19].iThrowbacks = 65;
		PDeets[19].iPullbacks = -1;
		PDeets[19].iBreakoutUp = 100;
		PDeets[19].iBreakoutDown = 20;
		PDeets[19].iPercentageBust = -1;
		PDeets[19].sTips = "Patterns without throwbacks see price rise further, on average.";
		PDeets[19].iTall = -1f;
		PDeets[19].iWide = 36;
		PDeets[20].sDescription = "Double bottom, Adam & Adam";
		PDeets[20].sPerformance = "26 out of 39 (39 is worst)";
		PDeets[20].iReversal = 100;
		PDeets[20].iContinuation = -1;
		PDeets[20].iFailureRate = 16;
		PDeets[20].iChangeTrend = 52;
		PDeets[20].iPctMeetingTargetUp = 73;
		PDeets[20].iPctMeetingTargetDown = -1;
		PDeets[20].iThrowbacks = 67;
		PDeets[20].iPullbacks = -1;
		PDeets[20].iBreakoutUp = 100;
		PDeets[20].iBreakoutDown = -1;
		PDeets[20].iPercentageBust = 29;
		PDeets[20].sTips = "Patterns without throwbacks see price rise further, on average.";
		PDeets[20].iTall = 9.4f;
		PDeets[20].iWide = 16;
		PDeets[21].sDescription = "Double bottom, Adam & Eve";
		PDeets[21].sPerformance = "17 out of 39 (39 is worst)";
		PDeets[21].iReversal = 100;
		PDeets[21].iContinuation = -1;
		PDeets[21].iFailureRate = 12;
		PDeets[21].iChangeTrend = 57;
		PDeets[21].iPctMeetingTargetUp = 69;
		PDeets[21].iPctMeetingTargetDown = -1;
		PDeets[21].iThrowbacks = 67;
		PDeets[21].iPullbacks = -1;
		PDeets[21].iBreakoutUp = 100;
		PDeets[21].iBreakoutDown = -1;
		PDeets[21].iPercentageBust = 23;
		PDeets[21].sTips = "Patterns without throwbacks see price rise further, on average.";
		PDeets[21].iTall = 12.5f;
		PDeets[21].iWide = 25;
		PDeets[24].sDescription = "Vertical run down";
		PDeets[24].sPerformance = sPerformance;
		PDeets[24].iReversal = -1;
		PDeets[24].iContinuation = -1;
		PDeets[24].iFailureRate = -1;
		PDeets[24].iChangeTrend = -1;
		PDeets[24].iPctMeetingTargetUp = -1;
		PDeets[24].iPctMeetingTargetDown = -1;
		PDeets[24].iThrowbacks = -1;
		PDeets[24].iPullbacks = -1;
		PDeets[24].iBreakoutUp = -1;
		PDeets[24].iBreakoutDown = -1;
		PDeets[24].iPercentageBust = -1;
		PDeets[24].sTips = "See ThePatternSite.com for more details.";
		PDeets[24].iTall = -1f;
		PDeets[24].iWide = -1;
		PDeets[25].sDescription = "Vertical run up";
		PDeets[25].sPerformance = sPerformance;
		PDeets[25].iReversal = -1;
		PDeets[25].iContinuation = -1;
		PDeets[25].iFailureRate = -1;
		PDeets[25].iChangeTrend = -1;
		PDeets[25].iPctMeetingTargetUp = -1;
		PDeets[25].iPctMeetingTargetDown = -1;
		PDeets[25].iThrowbacks = -1;
		PDeets[25].iPullbacks = -1;
		PDeets[25].iBreakoutUp = -1;
		PDeets[25].iBreakoutDown = -1;
		PDeets[25].iPercentageBust = -1;
		PDeets[25].sTips = "See ThePatternSite.com for more details.";
		PDeets[25].iTall = -1f;
		PDeets[25].iWide = -1;
		PDeets[26].sDescription = "Wolfe wave, bullish";
		PDeets[26].sPerformance = "34 out of 39 (39 is worst)";
		PDeets[26].iReversal = -1;
		PDeets[26].iContinuation = -1;
		PDeets[26].iFailureRate = 15;
		PDeets[26].iChangeTrend = 40;
		PDeets[26].iPctMeetingTargetUp = 47;
		PDeets[26].iPctMeetingTargetDown = -1;
		PDeets[26].iThrowbacks = -1;
		PDeets[26].iPullbacks = -1;
		PDeets[26].iBreakoutUp = -1;
		PDeets[26].iBreakoutDown = -1;
		PDeets[26].iPercentageBust = -1;
		PDeets[26].sTips = "Up target refers to those reaching the estimated price at arrival point (EPA).";
		PDeets[26].iTall = -1f;
		PDeets[26].iWide = -1;
		PDeets[27].sDescription = "Wolfe wave, bearish";
		PDeets[27].sPerformance = "35 out of 36 (36 is worst)";
		PDeets[27].iReversal = -1;
		PDeets[27].iContinuation = -1;
		PDeets[27].iFailureRate = 30;
		PDeets[27].iChangeTrend = 18;
		PDeets[27].iPctMeetingTargetUp = -1;
		PDeets[27].iPctMeetingTargetDown = 37;
		PDeets[27].iThrowbacks = -1;
		PDeets[27].iPullbacks = -1;
		PDeets[27].iBreakoutUp = -1;
		PDeets[27].iBreakoutDown = -1;
		PDeets[27].iPercentageBust = -1;
		PDeets[27].sTips = "Down target refers to those reaching the estimated price at arrival point (EPA)";
		PDeets[27].iTall = -1f;
		PDeets[27].iWide = -1;
		PDeets[28].sDescription = "Gartley, bearish";
		PDeets[28].sPerformance = "3 out of 5 (5 is worst)";
		PDeets[28].iReversal = -1;
		PDeets[28].iContinuation = -1;
		PDeets[28].iFailureRate = 22;
		PDeets[28].iChangeTrend = -1;
		PDeets[28].iPctMeetingTargetUp = 87;
		PDeets[28].iPctMeetingTargetDown = -1;
		PDeets[28].iThrowbacks = -1;
		PDeets[28].iPullbacks = -1;
		PDeets[28].iBreakoutUp = -1;
		PDeets[28].iBreakoutDown = -1;
		PDeets[28].iPercentageBust = -1;
		PDeets[28].sTips = "Up target refers to price reversing at point D.";
		PDeets[28].iTall = -1f;
		PDeets[28].iWide = -1;
		PDeets[29].sDescription = "Gartley, bullish";
		PDeets[29].sPerformance = "5 (worst) out of 5";
		PDeets[29].iReversal = -1;
		PDeets[29].iContinuation = -1;
		PDeets[29].iFailureRate = 14;
		PDeets[29].iChangeTrend = -1;
		PDeets[29].iPctMeetingTargetUp = -1;
		PDeets[29].iPctMeetingTargetDown = 90;
		PDeets[29].iThrowbacks = -1;
		PDeets[29].iPullbacks = -1;
		PDeets[29].iBreakoutUp = -1;
		PDeets[29].iBreakoutDown = -1;
		PDeets[29].iPercentageBust = -1;
		PDeets[29].sTips = "Down target refers to price reversing at point D.";
		PDeets[29].iTall = -1f;
		PDeets[29].iWide = -1;
		PDeets[30].sDescription = "Diving board";
		PDeets[30].sPerformance = "1 (best) out of 3";
		PDeets[30].iReversal = 37;
		PDeets[30].iContinuation = 63;
		PDeets[30].iFailureRate = 4;
		PDeets[30].iChangeTrend = 72;
		PDeets[30].iPctMeetingTargetUp = 62;
		PDeets[30].iPctMeetingTargetDown = -1;
		PDeets[30].iThrowbacks = -1;
		PDeets[30].iPullbacks = -1;
		PDeets[30].iBreakoutUp = 100;
		PDeets[30].iBreakoutDown = -1;
		PDeets[30].iPercentageBust = -1;
		PDeets[30].sTips = "Performance refers to patterns found on the weekly scale.";
		PDeets[30].iTall = 26.9f;
		PDeets[30].iWide = 204;
		PDeets[31].sDescription = "Three LR inverted";
		PDeets[31].sPerformance = "10 out of 23 (23 is worst)";
		PDeets[31].iReversal = 52;
		PDeets[31].iContinuation = 48;
		PDeets[31].iFailureRate = 46;
		PDeets[31].iChangeTrend = -1;
		PDeets[31].iPctMeetingTargetUp = -1;
		PDeets[31].iPctMeetingTargetDown = 45;
		PDeets[31].iThrowbacks = -1;
		PDeets[31].iPullbacks = -1;
		PDeets[31].iBreakoutUp = -1;
		PDeets[31].iBreakoutDown = -1;
		PDeets[31].iPercentageBust = -1;
		PDeets[31].sTips = "This is a four bar pattern. Performance references the trend low, not ultimate low.";
		PDeets[31].iTall = -1f;
		PDeets[31].iWide = -1;
		PDeets[32].sDescription = "Three LR";
		PDeets[32].sPerformance = "14 out of 23 (23 is worst)";
		PDeets[32].iReversal = 47;
		PDeets[32].iContinuation = 53;
		PDeets[32].iFailureRate = 38;
		PDeets[32].iChangeTrend = -1;
		PDeets[32].iPctMeetingTargetUp = 56;
		PDeets[32].iPctMeetingTargetDown = -1;
		PDeets[32].iThrowbacks = -1;
		PDeets[32].iPullbacks = -1;
		PDeets[32].iBreakoutUp = -1;
		PDeets[32].iBreakoutDown = -1;
		PDeets[32].iPercentageBust = -1;
		PDeets[32].sTips = "This is a four bar pattern. Performance references the trend high, not ultimate high.";
		PDeets[32].iTall = -1f;
		PDeets[32].iWide = -1;
		PDeets[33].sDescription = "Ugly double top";
		PDeets[33].sPerformance = sPerformance;
		PDeets[33].iReversal = -1;
		PDeets[33].iContinuation = -1;
		PDeets[33].iFailureRate = -1;
		PDeets[33].iChangeTrend = -1;
		PDeets[33].iPctMeetingTargetUp = -1;
		PDeets[33].iPctMeetingTargetDown = -1;
		PDeets[33].iThrowbacks = -1;
		PDeets[33].iPullbacks = -1;
		PDeets[33].iBreakoutUp = -1;
		PDeets[33].iBreakoutDown = 100;
		PDeets[33].iPercentageBust = -1;
		PDeets[33].sTips = sTips;
		PDeets[33].iTall = -1f;
		PDeets[33].iWide = -1;
		PDeets[34].sDescription = "Ugly double bottom";
		PDeets[34].sPerformance = "14.5 (I think it means it's been inserted between two other patterns) out of 23 (23 is worst)";
		PDeets[34].iReversal = 100;
		PDeets[34].iContinuation = -1;
		PDeets[34].iFailureRate = 8;
		PDeets[34].iChangeTrend = -1;
		PDeets[34].iPctMeetingTargetUp = 76;
		PDeets[34].iPctMeetingTargetDown = -1;
		PDeets[34].iThrowbacks = 59;
		PDeets[34].iPullbacks = -1;
		PDeets[34].iBreakoutUp = 100;
		PDeets[34].iBreakoutDown = -1;
		PDeets[34].iPercentageBust = -1;
		PDeets[34].sTips = text;
		PDeets[34].iTall = -1f;
		PDeets[34].iWide = -1;
		PDeets[35].sDescription = "Roof, inverted";
		PDeets[35].sPerformance = "37 out of 39 (39 is worst)";
		PDeets[35].iReversal = 37;
		PDeets[35].iContinuation = 63;
		PDeets[35].iFailureRate = 23;
		PDeets[35].iChangeTrend = 47;
		PDeets[35].iPctMeetingTargetUp = 65;
		PDeets[35].iPctMeetingTargetDown = 47;
		PDeets[35].iThrowbacks = 58;
		PDeets[35].iPullbacks = 64;
		PDeets[35].iBreakoutUp = 51;
		PDeets[35].iBreakoutDown = 49;
		PDeets[35].iPercentageBust = 35;
		PDeets[35].sTips = text;
		PDeets[35].iTall = -1f;
		PDeets[35].iWide = 45;
		PDeets[36].sDescription = "Roof";
		PDeets[36].sPerformance = "Roof out of 39 (39 is worst)";
		PDeets[36].iReversal = 24;
		PDeets[36].iContinuation = 76;
		PDeets[36].iFailureRate = 26;
		PDeets[36].iChangeTrend = 44;
		PDeets[36].iPctMeetingTargetUp = 62;
		PDeets[36].iPctMeetingTargetDown = 63;
		PDeets[36].iThrowbacks = 60;
		PDeets[36].iPullbacks = 66;
		PDeets[36].iBreakoutUp = 42;
		PDeets[36].iBreakoutDown = 58;
		PDeets[36].iPercentageBust = 32;
		PDeets[36].sTips = text;
		PDeets[36].iTall = 9.2f;
		PDeets[36].iWide = 50;
		PDeets[38].sDescription = "Wide ranging day, upside reversal";
		PDeets[38].sPerformance = "12 out of 23 (23 is worst)";
		PDeets[38].iReversal = 38;
		PDeets[38].iContinuation = 62;
		PDeets[38].iFailureRate = 39;
		PDeets[38].iChangeTrend = -1;
		PDeets[38].iPctMeetingTargetUp = 40;
		PDeets[38].iPctMeetingTargetDown = -1;
		PDeets[38].iThrowbacks = -1;
		PDeets[38].iPullbacks = -1;
		PDeets[38].iBreakoutUp = -1;
		PDeets[38].iBreakoutDown = -1;
		PDeets[38].iPercentageBust = -1;
		PDeets[38].sTips = "One-bar pattern that's supposed to be a reversal but isn't.";
		PDeets[38].iTall = -1f;
		PDeets[38].iWide = -1;
		PDeets[39].sDescription = "Wide ranging day, downside reversal";
		PDeets[39].sPerformance = "4 out of 23 (23 is worst)";
		PDeets[39].iReversal = 43;
		PDeets[39].iContinuation = 57;
		PDeets[39].iFailureRate = 43;
		PDeets[39].iChangeTrend = -1;
		PDeets[39].iPctMeetingTargetUp = -1;
		PDeets[39].iPctMeetingTargetDown = 42;
		PDeets[39].iThrowbacks = -1;
		PDeets[39].iPullbacks = -1;
		PDeets[39].iBreakoutUp = -1;
		PDeets[39].iBreakoutDown = -1;
		PDeets[39].iPercentageBust = -1;
		PDeets[39].sTips = "One-bar pattern that's supposed to be a reversal but isn't.";
		PDeets[39].iTall = -1f;
		PDeets[39].iWide = -1;
		PDeets[40].sDescription = "Spike down";
		PDeets[40].sPerformance = sPerformance;
		PDeets[40].iReversal = -1;
		PDeets[40].iContinuation = -1;
		PDeets[40].iFailureRate = -1;
		PDeets[40].iChangeTrend = -1;
		PDeets[40].iPctMeetingTargetUp = -1;
		PDeets[40].iPctMeetingTargetDown = -1;
		PDeets[40].iThrowbacks = -1;
		PDeets[40].iPullbacks = -1;
		PDeets[40].iBreakoutUp = -1;
		PDeets[40].iBreakoutDown = -1;
		PDeets[40].iPercentageBust = -1;
		PDeets[40].sTips = sTips;
		PDeets[40].iTall = -1f;
		PDeets[40].iWide = -1;
		PDeets[41].sDescription = "Spike up";
		PDeets[41].sPerformance = sPerformance;
		PDeets[41].iReversal = -1;
		PDeets[41].iContinuation = -1;
		PDeets[41].iFailureRate = -1;
		PDeets[41].iChangeTrend = -1;
		PDeets[41].iPctMeetingTargetUp = -1;
		PDeets[41].iPctMeetingTargetDown = -1;
		PDeets[41].iThrowbacks = -1;
		PDeets[41].iPullbacks = -1;
		PDeets[41].iBreakoutUp = -1;
		PDeets[41].iBreakoutDown = -1;
		PDeets[41].iPercentageBust = -1;
		PDeets[41].sTips = sTips;
		PDeets[41].iTall = -1f;
		PDeets[41].iWide = -1;
		PDeets[42].sDescription = "Pivot point reversal, uptrend";
		PDeets[42].sPerformance = "15 out of 23 (23 is worst)";
		PDeets[42].iReversal = 33;
		PDeets[42].iContinuation = 67;
		PDeets[42].iFailureRate = 43;
		PDeets[42].iChangeTrend = -1;
		PDeets[42].iPctMeetingTargetUp = 80;
		PDeets[42].iPctMeetingTargetDown = -1;
		PDeets[42].iThrowbacks = -1;
		PDeets[42].iPullbacks = -1;
		PDeets[42].iBreakoutUp = -1;
		PDeets[42].iBreakoutDown = -1;
		PDeets[42].iPercentageBust = -1;
		PDeets[42].sTips = "One-bar pattern that's supposed to be a reversal but isn't. " + text;
		PDeets[42].iTall = -1f;
		PDeets[42].iWide = -1;
		PDeets[43].sDescription = "Pivot point reversal, downtrend";
		PDeets[43].sPerformance = "17 out of 23 (23 is worst)";
		PDeets[43].iReversal = 31;
		PDeets[43].iContinuation = 69;
		PDeets[43].iFailureRate = 43;
		PDeets[43].iChangeTrend = -1;
		PDeets[43].iPctMeetingTargetUp = 77;
		PDeets[43].iPctMeetingTargetDown = -1;
		PDeets[43].iThrowbacks = -1;
		PDeets[43].iPullbacks = -1;
		PDeets[43].iBreakoutUp = -1;
		PDeets[43].iBreakoutDown = -1;
		PDeets[43].iPercentageBust = -1;
		PDeets[43].sTips = "One-bar pattern that's supposed to be a reversal but isn't. " + text2;
		PDeets[43].iTall = -1f;
		PDeets[43].iWide = -1;
		PDeets[44].sDescription = "Open-close reversal, uptrend";
		PDeets[44].sPerformance = "23 (worst) out of 23";
		PDeets[44].iReversal = -1;
		PDeets[44].iContinuation = -1;
		PDeets[44].iFailureRate = 52;
		PDeets[44].iChangeTrend = -1;
		PDeets[44].iPctMeetingTargetUp = -1;
		PDeets[44].iPctMeetingTargetDown = 64;
		PDeets[44].iThrowbacks = -1;
		PDeets[44].iPullbacks = -1;
		PDeets[44].iBreakoutUp = -1;
		PDeets[44].iBreakoutDown = -1;
		PDeets[44].iPercentageBust = -1;
		PDeets[44].sTips = text2;
		PDeets[44].iTall = -1f;
		PDeets[44].iWide = -1;
		PDeets[45].sDescription = "Open-close reversal, downtrend";
		PDeets[45].sPerformance = "23 (worst) out of 23";
		PDeets[45].iReversal = -1;
		PDeets[45].iContinuation = -1;
		PDeets[45].iFailureRate = 43;
		PDeets[45].iChangeTrend = -1;
		PDeets[45].iPctMeetingTargetUp = 72;
		PDeets[45].iPctMeetingTargetDown = -1;
		PDeets[45].iThrowbacks = -1;
		PDeets[45].iPullbacks = -1;
		PDeets[45].iBreakoutUp = -1;
		PDeets[45].iBreakoutDown = -1;
		PDeets[45].iPercentageBust = -1;
		PDeets[45].sTips = "One-bar pattern that's supposed to be a reversal of the downtrend. " + text;
		PDeets[45].iTall = -1f;
		PDeets[45].iWide = -1;
		PDeets[46].sDescription = "Key reversal, uptrend";
		PDeets[46].sPerformance = "16 out of 23 (23 is worst)";
		PDeets[46].iReversal = 49;
		PDeets[46].iContinuation = 51;
		PDeets[46].iFailureRate = 45;
		PDeets[46].iChangeTrend = -1;
		PDeets[46].iPctMeetingTargetUp = 71;
		PDeets[46].iPctMeetingTargetDown = -1;
		PDeets[46].iThrowbacks = -1;
		PDeets[46].iPullbacks = -1;
		PDeets[46].iBreakoutUp = -1;
		PDeets[46].iBreakoutDown = -1;
		PDeets[46].iPercentageBust = -1;
		PDeets[46].sTips = "Two-bar pattern is supposed to act as reversal of the uptrend but is random. " + text;
		PDeets[46].iTall = -1f;
		PDeets[46].iWide = -1;
		PDeets[47].sDescription = "Key reversal, downtrend";
		PDeets[47].sPerformance = "3 out of 23 (23 is worst)";
		PDeets[47].iReversal = 49;
		PDeets[47].iContinuation = 51;
		PDeets[47].iFailureRate = 43;
		PDeets[47].iChangeTrend = -1;
		PDeets[47].iPctMeetingTargetUp = 69;
		PDeets[47].iPctMeetingTargetDown = -1;
		PDeets[47].iThrowbacks = -1;
		PDeets[47].iPullbacks = -1;
		PDeets[47].iBreakoutUp = -1;
		PDeets[47].iBreakoutDown = -1;
		PDeets[47].iPercentageBust = -1;
		PDeets[47].sTips = "Two-bar pattern is supposed to act as reversal of the downtrend but is random. " + text;
		PDeets[47].iTall = -1f;
		PDeets[47].iWide = -1;
		PDeets[48].sDescription = "Cup with handle, inverted";
		PDeets[48].sPerformance = "6 out orf 36 (36 is worst)";
		PDeets[48].iReversal = 55;
		PDeets[48].iContinuation = 45;
		PDeets[48].iFailureRate = 18;
		PDeets[48].iChangeTrend = 35;
		PDeets[48].iPctMeetingTargetUp = -1;
		PDeets[48].iPctMeetingTargetDown = 62;
		PDeets[48].iThrowbacks = -1;
		PDeets[48].iPullbacks = 67;
		PDeets[48].iBreakoutUp = -1;
		PDeets[48].iBreakoutDown = 100;
		PDeets[48].iPercentageBust = 29;
		PDeets[48].sTips = text2;
		PDeets[48].iTall = -1f;
		PDeets[48].iWide = -1;
		PDeets[49].sDescription = "Hook reversal, uptrend";
		PDeets[49].sPerformance = "16 out of 23 (23 is worst)";
		PDeets[49].iReversal = 48;
		PDeets[49].iContinuation = 52;
		PDeets[49].iFailureRate = 49;
		PDeets[49].iChangeTrend = -1;
		PDeets[49].iPctMeetingTargetUp = -1;
		PDeets[49].iPctMeetingTargetDown = 63;
		PDeets[49].iThrowbacks = -1;
		PDeets[49].iPullbacks = -1;
		PDeets[49].iBreakoutUp = -1;
		PDeets[49].iBreakoutDown = -1;
		PDeets[49].iPercentageBust = -1;
		PDeets[49].sTips = text2 + " Two-bar pattern is supposed to act as uptrend reversal but is random.";
		PDeets[49].iTall = -1f;
		PDeets[49].iWide = -1;
		PDeets[50].sDescription = "Hook reversal, downtrend";
		PDeets[50].sPerformance = "9 out of 23 (23 is worst)";
		PDeets[50].iReversal = 49;
		PDeets[50].iContinuation = 51;
		PDeets[50].iFailureRate = 42;
		PDeets[50].iChangeTrend = -1;
		PDeets[50].iPctMeetingTargetUp = 69;
		PDeets[50].iPctMeetingTargetDown = -1;
		PDeets[50].iThrowbacks = -1;
		PDeets[50].iPullbacks = -1;
		PDeets[50].iBreakoutUp = -1;
		PDeets[50].iBreakoutDown = -1;
		PDeets[50].iPercentageBust = -1;
		PDeets[50].sTips = text + " Two-bar pattern is supposed to act as a downtrend reversal but is random.";
		PDeets[50].iTall = -1f;
		PDeets[50].iWide = -1;
		PDeets[51].sDescription = "Closing price reversal, uptrend";
		PDeets[51].sPerformance = "23 (worst) out of 23";
		PDeets[51].iReversal = -1;
		PDeets[51].iContinuation = -1;
		PDeets[51].iFailureRate = 52;
		PDeets[51].iChangeTrend = -1;
		PDeets[51].iPctMeetingTargetUp = -1;
		PDeets[51].iPctMeetingTargetDown = 64;
		PDeets[51].iThrowbacks = -1;
		PDeets[51].iPullbacks = -1;
		PDeets[51].iBreakoutUp = -1;
		PDeets[51].iBreakoutDown = -1;
		PDeets[51].iPercentageBust = -1;
		PDeets[51].sTips = text2;
		PDeets[51].iTall = -1f;
		PDeets[51].iWide = -1;
		PDeets[52].sDescription = "Closing price reversal, downtrend";
		PDeets[52].sPerformance = "23 (worst) out of 23";
		PDeets[52].iReversal = -1;
		PDeets[52].iContinuation = -1;
		PDeets[52].iFailureRate = 43;
		PDeets[52].iChangeTrend = -1;
		PDeets[52].iPctMeetingTargetUp = 72;
		PDeets[52].iPctMeetingTargetDown = -1;
		PDeets[52].iThrowbacks = -1;
		PDeets[52].iPullbacks = -1;
		PDeets[52].iBreakoutUp = -1;
		PDeets[52].iBreakoutDown = -1;
		PDeets[52].iPercentageBust = -1;
		PDeets[52].sTips = text;
		PDeets[52].iTall = -1f;
		PDeets[52].iWide = -1;
		PDeets[53].sDescription = "Weekly reversal top";
		PDeets[53].sPerformance = "22 out of 23 (23 is worst)";
		PDeets[53].iReversal = 62;
		PDeets[53].iContinuation = 38;
		PDeets[53].iFailureRate = 24;
		PDeets[53].iChangeTrend = -1;
		PDeets[53].iPctMeetingTargetUp = -1;
		PDeets[53].iPctMeetingTargetDown = 52;
		PDeets[53].iThrowbacks = -1;
		PDeets[53].iPullbacks = -1;
		PDeets[53].iBreakoutUp = -1;
		PDeets[53].iBreakoutDown = -1;
		PDeets[53].iPercentageBust = -1;
		PDeets[53].sTips = text2;
		PDeets[53].iTall = -1f;
		PDeets[53].iWide = -1;
		PDeets[54].sDescription = "Weekly reversal bottom";
		PDeets[54].sPerformance = "8 out of 23 (23 is worst)";
		PDeets[54].iReversal = 67;
		PDeets[54].iContinuation = 33;
		PDeets[54].iFailureRate = 16;
		PDeets[54].iChangeTrend = -1;
		PDeets[54].iPctMeetingTargetUp = 70;
		PDeets[54].iPctMeetingTargetDown = -1;
		PDeets[54].iThrowbacks = -1;
		PDeets[54].iPullbacks = -1;
		PDeets[54].iBreakoutUp = -1;
		PDeets[54].iBreakoutDown = -1;
		PDeets[54].iPercentageBust = -1;
		PDeets[54].sTips = text;
		PDeets[54].iTall = -1f;
		PDeets[54].iWide = -1;
		PDeets[55].sDescription = "V-top";
		PDeets[55].sPerformance = "20 out of 36 (36 is worst)";
		PDeets[55].iReversal = 55;
		PDeets[55].iContinuation = 45;
		PDeets[55].iFailureRate = 29;
		PDeets[55].iChangeTrend = 29;
		PDeets[55].iPctMeetingTargetUp = -1;
		PDeets[55].iPctMeetingTargetDown = 37;
		PDeets[55].iThrowbacks = -1;
		PDeets[55].iPullbacks = 56;
		PDeets[55].iBreakoutUp = -1;
		PDeets[55].iBreakoutDown = 100;
		PDeets[55].iPercentageBust = 46;
		PDeets[55].sTips = text2;
		PDeets[55].iTall = 25.3f;
		PDeets[55].iWide = -1;
		PDeets[56].sDescription = "V-bottom";
		PDeets[56].sPerformance = "24 out of 39 (39 is worst)";
		PDeets[56].iReversal = 64;
		PDeets[56].iContinuation = 36;
		PDeets[56].iFailureRate = 19;
		PDeets[56].iChangeTrend = 53;
		PDeets[56].iPctMeetingTargetUp = 52;
		PDeets[56].iPctMeetingTargetDown = -1;
		PDeets[56].iThrowbacks = 55;
		PDeets[56].iPullbacks = -1;
		PDeets[56].iBreakoutUp = 100;
		PDeets[56].iBreakoutDown = -1;
		PDeets[56].iPercentageBust = 30;
		PDeets[56].sTips = text;
		PDeets[56].iTall = 34f;
		PDeets[56].iWide = 28;
		PDeets[57].sDescription = "Trendline, up";
		PDeets[57].sPerformance = sPerformance;
		PDeets[57].iReversal = -1;
		PDeets[57].iContinuation = -1;
		PDeets[57].iFailureRate = -1;
		PDeets[57].iChangeTrend = -1;
		PDeets[57].iPctMeetingTargetUp = -1;
		PDeets[57].iPctMeetingTargetDown = -1;
		PDeets[57].iThrowbacks = -1;
		PDeets[57].iPullbacks = -1;
		PDeets[57].iBreakoutUp = -1;
		PDeets[57].iBreakoutDown = -1;
		PDeets[57].iPercentageBust = -1;
		PDeets[57].sTips = sTips;
		PDeets[57].iTall = -1f;
		PDeets[57].iWide = -1;
		PDeets[58].sDescription = "Trendline, down";
		PDeets[58].sPerformance = sPerformance;
		PDeets[58].iReversal = -1;
		PDeets[58].iContinuation = -1;
		PDeets[58].iFailureRate = -1;
		PDeets[58].iChangeTrend = -1;
		PDeets[58].iPctMeetingTargetUp = -1;
		PDeets[58].iPctMeetingTargetDown = -1;
		PDeets[58].iThrowbacks = -1;
		PDeets[58].iPullbacks = -1;
		PDeets[58].iBreakoutUp = -1;
		PDeets[58].iBreakoutDown = -1;
		PDeets[58].iPercentageBust = -1;
		PDeets[58].sTips = sTips;
		PDeets[58].iTall = -1f;
		PDeets[58].iWide = -1;
		PDeets[59].sDescription = "Three bar";
		PDeets[59].sPerformance = sPerformance;
		PDeets[59].iReversal = -1;
		PDeets[59].iContinuation = -1;
		PDeets[59].iFailureRate = -1;
		PDeets[59].iChangeTrend = -1;
		PDeets[59].iPctMeetingTargetUp = -1;
		PDeets[59].iPctMeetingTargetDown = -1;
		PDeets[59].iThrowbacks = -1;
		PDeets[59].iPullbacks = -1;
		PDeets[59].iBreakoutUp = -1;
		PDeets[59].iBreakoutDown = -1;
		PDeets[59].iPercentageBust = -1;
		PDeets[59].sTips = sTips;
		PDeets[59].iTall = -1f;
		PDeets[59].iWide = -1;
		PDeets[60].sDescription = "Shark-32";
		PDeets[60].sPerformance = "18 out of 23 (23 is worst)";
		PDeets[60].iReversal = 40;
		PDeets[60].iContinuation = 60;
		PDeets[60].iFailureRate = 32;
		PDeets[60].iChangeTrend = -1;
		PDeets[60].iPctMeetingTargetUp = 72;
		PDeets[60].iPctMeetingTargetDown = -1;
		PDeets[60].iThrowbacks = 64;
		PDeets[60].iPullbacks = -1;
		PDeets[60].iBreakoutUp = -1;
		PDeets[60].iBreakoutDown = -1;
		PDeets[60].iPercentageBust = -1;
		PDeets[60].sTips = sTips;
		PDeets[60].iTall = -1f;
		PDeets[60].iWide = -1;
		PDeets[61].sDescription = "Scallop, descending And inverted";
		PDeets[61].sPerformance = "9 out of 39 (39 is worst)";
		PDeets[61].iReversal = 69;
		PDeets[61].iContinuation = 31;
		PDeets[61].iFailureRate = 16;
		PDeets[61].iChangeTrend = -1;
		PDeets[61].iPctMeetingTargetUp = 62;
		PDeets[61].iPctMeetingTargetDown = 29;
		PDeets[61].iThrowbacks = 58;
		PDeets[61].iPullbacks = 66;
		PDeets[61].iBreakoutUp = 30;
		PDeets[61].iBreakoutDown = 70;
		PDeets[61].iPercentageBust = -1;
		PDeets[61].sTips = text;
		PDeets[61].iTall = 15.5f;
		PDeets[61].iWide = 36;
		PDeets[62].sDescription = "Scallop, ascending And inverted";
		PDeets[62].sPerformance = "14 out of 39 (39 is worst)";
		PDeets[62].iReversal = 31;
		PDeets[62].iContinuation = 69;
		PDeets[62].iFailureRate = 9;
		PDeets[62].iChangeTrend = -62;
		PDeets[62].iPctMeetingTargetUp = 64;
		PDeets[62].iPctMeetingTargetDown = -1;
		PDeets[62].iThrowbacks = 66;
		PDeets[62].iPullbacks = -1;
		PDeets[62].iBreakoutUp = 95;
		PDeets[62].iBreakoutDown = 5;
		PDeets[62].iPercentageBust = 17;
		PDeets[62].sTips = text;
		PDeets[62].iTall = 17.4f;
		PDeets[62].iWide = -1;
		PDeets[63].sDescription = "Scallop, descending";
		PDeets[63].sPerformance = "29 out of 39 (39 is worst)";
		PDeets[63].iReversal = 60;
		PDeets[63].iContinuation = 40;
		PDeets[63].iFailureRate = 14;
		PDeets[63].iChangeTrend = 52;
		PDeets[63].iPctMeetingTargetUp = 52;
		PDeets[63].iPctMeetingTargetDown = -1;
		PDeets[63].iThrowbacks = 67;
		PDeets[63].iPullbacks = -1;
		PDeets[63].iBreakoutUp = 22;
		PDeets[63].iBreakoutDown = 78;
		PDeets[63].iPercentageBust = 24;
		PDeets[63].sTips = text;
		PDeets[63].iTall = -1f;
		PDeets[63].iWide = -1;
		PDeets[64].sDescription = "Scallop, ascending";
		PDeets[64].sPerformance = "20 out of 39 (39 is worst)";
		PDeets[64].iReversal = 11;
		PDeets[64].iContinuation = 89;
		PDeets[64].iFailureRate = 11;
		PDeets[64].iChangeTrend = 61;
		PDeets[64].iPctMeetingTargetUp = 62;
		PDeets[64].iPctMeetingTargetDown = -1;
		PDeets[64].iThrowbacks = 68;
		PDeets[64].iPullbacks = -1;
		PDeets[64].iBreakoutUp = 83;
		PDeets[64].iBreakoutDown = 17;
		PDeets[64].iPercentageBust = 15;
		PDeets[64].sTips = text;
		PDeets[64].iTall = -1f;
		PDeets[64].iWide = 41;
		PDeets[65].sDescription = "Rounding top";
		PDeets[65].sPerformance = "2 out of 39 (39 is worst)";
		PDeets[65].iReversal = 35;
		PDeets[65].iContinuation = 65;
		PDeets[65].iFailureRate = 9;
		PDeets[65].iChangeTrend = 65;
		PDeets[65].iPctMeetingTargetUp = 58;
		PDeets[65].iPctMeetingTargetDown = -1;
		PDeets[65].iThrowbacks = 63;
		PDeets[65].iPullbacks = -1;
		PDeets[65].iBreakoutUp = 58;
		PDeets[65].iBreakoutDown = 42;
		PDeets[65].iPercentageBust = -1;
		PDeets[65].sTips = text;
		PDeets[65].iTall = 24.9f;
		PDeets[65].iWide = 145;
		PDeets[66].sDescription = "Rounding bottom";
		PDeets[66].sPerformance = "7 out of 39 (39 is worst)";
		PDeets[66].iReversal = 33;
		PDeets[66].iContinuation = 67;
		PDeets[66].iFailureRate = 4;
		PDeets[66].iChangeTrend = -1;
		PDeets[66].iPctMeetingTargetUp = 65;
		PDeets[66].iPctMeetingTargetDown = -1;
		PDeets[66].iThrowbacks = 64;
		PDeets[66].iPullbacks = -1;
		PDeets[66].iBreakoutUp = 100;
		PDeets[66].iBreakoutDown = -1;
		PDeets[66].iPercentageBust = -1;
		PDeets[66].sTips = text;
		PDeets[66].iTall = 21.9f;
		PDeets[66].iWide = 174;
		PDeets[67].sDescription = "Pennant";
		PDeets[67].sPerformance = sPerformance;
		PDeets[67].iReversal = 24;
		PDeets[67].iContinuation = 76;
		PDeets[67].iFailureRate = 54;
		PDeets[67].iChangeTrend = -1;
		PDeets[67].iPctMeetingTargetUp = 35;
		PDeets[67].iPctMeetingTargetDown = 32;
		PDeets[67].iThrowbacks = -1;
		PDeets[67].iPullbacks = -1;
		PDeets[67].iBreakoutUp = 57;
		PDeets[67].iBreakoutDown = 43;
		PDeets[67].iPercentageBust = -1;
		PDeets[67].sTips = "See 'Encyclopedia of Chart Patterns, 3rd Edition' for more information on price trend, breakout direction, tilt and resulting performance.";
		PDeets[67].iTall = 4.2f;
		PDeets[67].iWide = 7;
		PDeets[68].sDescription = "Outside day";
		PDeets[68].sPerformance = "6 out of 23 (23 is worst)";
		PDeets[68].iReversal = 37;
		PDeets[68].iContinuation = 63;
		PDeets[68].iFailureRate = 32;
		PDeets[68].iChangeTrend = -1;
		PDeets[68].iPctMeetingTargetUp = 82;
		PDeets[68].iPctMeetingTargetDown = -1;
		PDeets[68].iThrowbacks = -1;
		PDeets[68].iPullbacks = -1;
		PDeets[68].iBreakoutUp = -1;
		PDeets[68].iBreakoutDown = -1;
		PDeets[68].iPercentageBust = -1;
		PDeets[68].sTips = text;
		PDeets[68].iTall = -1f;
		PDeets[68].iWide = -1;
		PDeets[69].sDescription = "One day reversal, top";
		PDeets[69].sPerformance = "20 out out 23 (23 is worst)";
		PDeets[69].iReversal = -1;
		PDeets[69].iContinuation = -1;
		PDeets[69].iFailureRate = 48;
		PDeets[69].iChangeTrend = -1;
		PDeets[69].iPctMeetingTargetUp = -1;
		PDeets[69].iPctMeetingTargetDown = 67;
		PDeets[69].iThrowbacks = -1;
		PDeets[69].iPullbacks = -1;
		PDeets[69].iBreakoutUp = -1;
		PDeets[69].iBreakoutDown = -1;
		PDeets[69].iPercentageBust = -1;
		PDeets[69].sTips = text2 + " Only trade those that reverse a short-term uptrend.";
		PDeets[69].iTall = -1f;
		PDeets[69].iWide = -1;
		PDeets[70].sDescription = "One day reversal, bottom";
		PDeets[70].sPerformance = "20 out out 23 (23 is worst)";
		PDeets[70].iReversal = -1;
		PDeets[70].iContinuation = -1;
		PDeets[70].iFailureRate = 39;
		PDeets[70].iChangeTrend = -1;
		PDeets[70].iPctMeetingTargetUp = 73;
		PDeets[70].iPctMeetingTargetDown = -1;
		PDeets[70].iThrowbacks = -1;
		PDeets[70].iPullbacks = -1;
		PDeets[70].iBreakoutUp = -1;
		PDeets[70].iBreakoutDown = -1;
		PDeets[70].iPercentageBust = -1;
		PDeets[70].sTips = text + "Only trade those that reverse the short-term down trend.";
		PDeets[70].iTall = -1f;
		PDeets[70].iWide = -1;
		PDeets[71].sDescription = "NR7";
		PDeets[71].sPerformance = "11 out of 23 (23 is worst)";
		PDeets[71].iReversal = -1;
		PDeets[71].iContinuation = -1;
		PDeets[71].iFailureRate = 46;
		PDeets[71].iChangeTrend = -1;
		PDeets[71].iPctMeetingTargetUp = 43;
		PDeets[71].iPctMeetingTargetDown = -1;
		PDeets[71].iThrowbacks = -1;
		PDeets[71].iPullbacks = -1;
		PDeets[71].iBreakoutUp = -1;
		PDeets[71].iBreakoutDown = -1;
		PDeets[71].iPercentageBust = -1;
		PDeets[71].sTips = text;
		PDeets[71].iTall = -1f;
		PDeets[71].iWide = -1;
		PDeets[72].sDescription = "NR4";
		PDeets[72].sPerformance = "7 out of 23 (23 is worst)";
		PDeets[72].iReversal = -1;
		PDeets[72].iContinuation = -1;
		PDeets[72].iFailureRate = 46;
		PDeets[72].iChangeTrend = -1;
		PDeets[72].iPctMeetingTargetUp = 55;
		PDeets[72].iPctMeetingTargetDown = -1;
		PDeets[72].iThrowbacks = -1;
		PDeets[72].iPullbacks = -1;
		PDeets[72].iBreakoutUp = -1;
		PDeets[72].iBreakoutDown = -1;
		PDeets[72].iPercentageBust = -1;
		PDeets[72].sTips = text;
		PDeets[72].iTall = -1f;
		PDeets[72].iWide = -1;
		PDeets[73].sDescription = "Measured move up";
		PDeets[73].sPerformance = sPerformance;
		PDeets[73].iReversal = -1;
		PDeets[73].iContinuation = -1;
		PDeets[73].iFailureRate = -1;
		PDeets[73].iChangeTrend = -1;
		PDeets[73].iPctMeetingTargetUp = 60;
		PDeets[73].iPctMeetingTargetDown = -1;
		PDeets[73].iThrowbacks = -1;
		PDeets[73].iPullbacks = -1;
		PDeets[73].iBreakoutUp = -1;
		PDeets[73].iBreakoutDown = -1;
		PDeets[73].iPercentageBust = -1;
		PDeets[73].sTips = "Second leg is longer than first leg 41% of time. Price retraces to corrective phase (or below it) 57% of the time.";
		PDeets[73].iTall = -1f;
		PDeets[73].iWide = -1;
		PDeets[74].sDescription = "Measured move down";
		PDeets[74].sPerformance = sPerformance;
		PDeets[74].iReversal = -1;
		PDeets[74].iContinuation = -1;
		PDeets[74].iFailureRate = -1;
		PDeets[74].iChangeTrend = -1;
		PDeets[74].iPctMeetingTargetUp = -1;
		PDeets[74].iPctMeetingTargetDown = 43;
		PDeets[74].iThrowbacks = -1;
		PDeets[74].iPullbacks = -1;
		PDeets[74].iBreakoutUp = -1;
		PDeets[74].iBreakoutDown = -1;
		PDeets[74].iPercentageBust = -1;
		PDeets[74].sTips = "Second leg is longer than first leg 43% of time. Price retraces to corrective phase (or above it) 48% of the time.";
		PDeets[74].iTall = -1f;
		PDeets[74].iWide = -1;
		PDeets[75].sDescription = "Island reversal, top";
		PDeets[75].sPerformance = "31 out of 36 (36 is worst)";
		PDeets[75].iReversal = 100;
		PDeets[75].iContinuation = -1;
		PDeets[75].iFailureRate = 34;
		PDeets[75].iChangeTrend = 21;
		PDeets[75].iPctMeetingTargetUp = -1;
		PDeets[75].iPctMeetingTargetDown = 62;
		PDeets[75].iThrowbacks = -1;
		PDeets[75].iPullbacks = 55;
		PDeets[75].iBreakoutUp = -1;
		PDeets[75].iBreakoutDown = 100;
		PDeets[75].iPercentageBust = 39;
		PDeets[75].sTips = text2;
		PDeets[75].iTall = 5.6f;
		PDeets[75].iWide = -1;
		PDeets[76].sDescription = "Island reversal, bottom";
		PDeets[76].sPerformance = "38 out of 39 (39 is worst)";
		PDeets[76].iReversal = 100;
		PDeets[76].iContinuation = -1;
		PDeets[76].iFailureRate = 31;
		PDeets[76].iChangeTrend = 39;
		PDeets[76].iPctMeetingTargetUp = 82;
		PDeets[76].iPctMeetingTargetDown = -1;
		PDeets[76].iThrowbacks = 54;
		PDeets[76].iPullbacks = -1;
		PDeets[76].iBreakoutUp = 100;
		PDeets[76].iBreakoutDown = -1;
		PDeets[76].iPercentageBust = 33;
		PDeets[76].sTips = text;
		PDeets[76].iTall = 5.2f;
		PDeets[76].iWide = 6;
		PDeets[77].sDescription = "Inside day";
		PDeets[77].sPerformance = "10 out of 23 (23 is worst)";
		PDeets[77].iReversal = 38;
		PDeets[77].iContinuation = 62;
		PDeets[77].iFailureRate = 32;
		PDeets[77].iChangeTrend = -1;
		PDeets[77].iPctMeetingTargetUp = 80;
		PDeets[77].iPctMeetingTargetDown = -1;
		PDeets[77].iThrowbacks = -1;
		PDeets[77].iPullbacks = -1;
		PDeets[77].iBreakoutUp = -1;
		PDeets[77].iBreakoutDown = -1;
		PDeets[77].iPercentageBust = -1;
		PDeets[77].sTips = text;
		PDeets[77].iTall = -1f;
		PDeets[77].iWide = -1;
		PDeets[78].sDescription = "Flag";
		PDeets[78].sPerformance = sPerformance;
		PDeets[78].iReversal = 8;
		PDeets[78].iContinuation = 92;
		PDeets[78].iFailureRate = 44;
		PDeets[78].iChangeTrend = -1;
		PDeets[78].iPctMeetingTargetUp = 46;
		PDeets[78].iPctMeetingTargetDown = 46;
		PDeets[78].iThrowbacks = -1;
		PDeets[78].iPullbacks = -1;
		PDeets[78].iBreakoutUp = 60;
		PDeets[78].iBreakoutDown = 40;
		PDeets[78].iPercentageBust = -1;
		PDeets[78].sTips = text;
		PDeets[78].iTall = 4.3f;
		PDeets[78].iWide = -1;
		PDeets[79].sDescription = "Diamond top";
		PDeets[79].sPerformance = "39 (worst) out of 39";
		PDeets[79].iReversal = 100;
		PDeets[79].iContinuation = 100;
		PDeets[79].iFailureRate = 21;
		PDeets[79].iChangeTrend = 48;
		PDeets[79].iPctMeetingTargetUp = 65;
		PDeets[79].iPctMeetingTargetDown = -1;
		PDeets[79].iThrowbacks = 57;
		PDeets[79].iPullbacks = 58;
		PDeets[79].iBreakoutUp = 46;
		PDeets[79].iBreakoutDown = 54;
		PDeets[79].iPercentageBust = 34;
		PDeets[79].sTips = text + " Reversal (100%) is for upward breakouts. Continuations (100%) is for downward breakouts.";
		PDeets[79].iTall = 9.8f;
		PDeets[79].iWide = 38;
		PDeets[80].sDescription = "Diamond bottom";
		PDeets[80].sPerformance = "27 out of 39 (39 is worst)";
		PDeets[80].iReversal = 100;
		PDeets[80].iContinuation = 100;
		PDeets[80].iFailureRate = 13;
		PDeets[80].iChangeTrend = 56;
		PDeets[80].iPctMeetingTargetUp = 73;
		PDeets[80].iPctMeetingTargetDown = 55;
		PDeets[80].iThrowbacks = 52;
		PDeets[80].iPullbacks = 67;
		PDeets[80].iBreakoutUp = 74;
		PDeets[80].iBreakoutDown = 26;
		PDeets[80].iPercentageBust = 22;
		PDeets[80].sTips = text + " Reversal (100%) is for upward breakouts. Continuations (100%) is for downward breakouts.";
		PDeets[80].iTall = 10.9f;
		PDeets[80].iWide = 34;
		PDeets[81].sDescription = "Cup with handle";
		PDeets[81].sPerformance = "3 out of 39 (39 is worst)";
		PDeets[81].iReversal = 0;
		PDeets[81].iContinuation = 100;
		PDeets[81].iFailureRate = 5;
		PDeets[81].iChangeTrend = 69;
		PDeets[81].iPctMeetingTargetUp = 61;
		PDeets[81].iPctMeetingTargetDown = -1;
		PDeets[81].iThrowbacks = 62;
		PDeets[81].iPullbacks = -1;
		PDeets[81].iBreakoutUp = 100;
		PDeets[81].iBreakoutDown = -1;
		PDeets[81].iPercentageBust = 10;
		PDeets[81].sTips = text;
		PDeets[81].iTall = -1f;
		PDeets[81].iWide = -1;
		PDeets[82].sDescription = "Channel, down";
		PDeets[82].sPerformance = sPerformance;
		PDeets[82].iReversal = -1;
		PDeets[82].iContinuation = -1;
		PDeets[82].iFailureRate = -1;
		PDeets[82].iChangeTrend = -1;
		PDeets[82].iPctMeetingTargetUp = -1;
		PDeets[82].iPctMeetingTargetDown = -1;
		PDeets[82].iThrowbacks = -1;
		PDeets[82].iPullbacks = -1;
		PDeets[82].iBreakoutUp = -1;
		PDeets[82].iBreakoutDown = -1;
		PDeets[82].iPercentageBust = -1;
		PDeets[82].sTips = sTips;
		PDeets[82].iTall = -1f;
		PDeets[82].iWide = -1;
		PDeets[83].sDescription = "Bump-and-run reversal, top";
		PDeets[83].sPerformance = "3 out of 36 (36 is worst)";
		PDeets[83].iReversal = 76;
		PDeets[83].iContinuation = 24;
		PDeets[83].iFailureRate = 14;
		PDeets[83].iChangeTrend = 33;
		PDeets[83].iPctMeetingTargetUp = -1;
		PDeets[83].iPctMeetingTargetDown = 44;
		PDeets[83].iThrowbacks = -1;
		PDeets[83].iPullbacks = 64;
		PDeets[83].iBreakoutUp = -1;
		PDeets[83].iBreakoutDown = 100;
		PDeets[83].iPercentageBust = 22;
		PDeets[83].sTips = text2;
		PDeets[83].iTall = -1f;
		PDeets[83].iWide = -1;
		PDeets[84].sDescription = "Bump-and-run reversal, bottom";
		PDeets[84].sPerformance = "1 (best) out of 39";
		PDeets[84].iReversal = 52;
		PDeets[84].iContinuation = 48;
		PDeets[84].iFailureRate = 9;
		PDeets[84].iChangeTrend = 67;
		PDeets[84].iPctMeetingTargetUp = 76;
		PDeets[84].iPctMeetingTargetDown = -1;
		PDeets[84].iThrowbacks = 61;
		PDeets[84].iPullbacks = -1;
		PDeets[84].iBreakoutUp = 100;
		PDeets[84].iBreakoutDown = -1;
		PDeets[84].iPercentageBust = 12;
		PDeets[84].sTips = text;
		PDeets[84].iTall = 27.2f;
		PDeets[84].iWide = -1;
		PDeets[85].sDescription = "Triple top";
		PDeets[85].sPerformance = "24 out of 36 (36 is worst)";
		PDeets[85].iReversal = 100;
		PDeets[85].iContinuation = -1;
		PDeets[85].iFailureRate = 25;
		PDeets[85].iChangeTrend = 26;
		PDeets[85].iPctMeetingTargetUp = -1;
		PDeets[85].iPctMeetingTargetDown = 49;
		PDeets[85].iThrowbacks = -1;
		PDeets[85].iPullbacks = 66;
		PDeets[85].iBreakoutUp = -1;
		PDeets[85].iBreakoutDown = 100;
		PDeets[85].iPercentageBust = 43;
		PDeets[85].sTips = text2;
		PDeets[85].iTall = 9.7f;
		PDeets[85].iWide = 38;
		PDeets[86].sDescription = "Triple bottom";
		PDeets[86].sPerformance = "12 out of 39 (39 is worst)";
		PDeets[86].iReversal = 100;
		PDeets[86].iContinuation = -1;
		PDeets[86].iFailureRate = 13;
		PDeets[86].iChangeTrend = 58;
		PDeets[86].iPctMeetingTargetUp = 74;
		PDeets[86].iPctMeetingTargetDown = -1;
		PDeets[86].iThrowbacks = 65;
		PDeets[86].iPullbacks = -1;
		PDeets[86].iBreakoutUp = -100;
		PDeets[86].iBreakoutDown = -1;
		PDeets[86].iPercentageBust = 23;
		PDeets[86].sTips = text;
		PDeets[86].iTall = 9.9f;
		PDeets[86].iWide = 39;
		PDeets[87].sDescription = "Triangle, symmetrical";
		PDeets[87].sPerformance = "36 out of 39 (39 is worst)";
		PDeets[87].iReversal = 40;
		PDeets[87].iContinuation = 60;
		PDeets[87].iFailureRate = 25;
		PDeets[87].iChangeTrend = 45;
		PDeets[87].iPctMeetingTargetUp = 58;
		PDeets[87].iPctMeetingTargetDown = 36;
		PDeets[87].iThrowbacks = 62;
		PDeets[87].iPullbacks = 65;
		PDeets[87].iBreakoutUp = 60;
		PDeets[87].iBreakoutDown = 40;
		PDeets[87].iPercentageBust = 32;
		PDeets[87].sTips = text;
		PDeets[87].iTall = 10.1f;
		PDeets[87].iWide = 35;
		PDeets[88].sDescription = "Triangle, descending";
		PDeets[88].sPerformance = "33 out of 39 (39 is worst)";
		PDeets[88].iReversal = 37;
		PDeets[88].iContinuation = 63;
		PDeets[88].iFailureRate = 22;
		PDeets[88].iChangeTrend = 50;
		PDeets[88].iPctMeetingTargetUp = 64;
		PDeets[88].iPctMeetingTargetDown = 50;
		PDeets[88].iThrowbacks = 60;
		PDeets[88].iPullbacks = 58;
		PDeets[88].iBreakoutUp = 53;
		PDeets[88].iBreakoutDown = 47;
		PDeets[88].iPercentageBust = 28;
		PDeets[88].sTips = text;
		PDeets[88].iTall = 9.5f;
		PDeets[88].iWide = 42;
		PDeets[89].sDescription = "Triangle, ascending";
		PDeets[89].sPerformance = "16 out of 39 (39 is worst)";
		PDeets[89].iReversal = 40;
		PDeets[89].iContinuation = 60;
		PDeets[89].iFailureRate = 17;
		PDeets[89].iChangeTrend = 51;
		PDeets[89].iPctMeetingTargetUp = 70;
		PDeets[89].iPctMeetingTargetDown = 44;
		PDeets[89].iThrowbacks = 64;
		PDeets[89].iPullbacks = 63;
		PDeets[89].iBreakoutUp = 63;
		PDeets[89].iBreakoutDown = 37;
		PDeets[89].iPercentageBust = 29;
		PDeets[89].sTips = text;
		PDeets[89].iTall = 9.5f;
		PDeets[89].iWide = -1;
		PDeets[90].sDescription = "Three rising valleys";
		PDeets[90].sPerformance = "6 out of 39 (39 is worst)";
		PDeets[90].iReversal = 48;
		PDeets[90].iContinuation = 52;
		PDeets[90].iFailureRate = 10;
		PDeets[90].iChangeTrend = 61;
		PDeets[90].iPctMeetingTargetUp = 57;
		PDeets[90].iPctMeetingTargetDown = -1;
		PDeets[90].iThrowbacks = 66;
		PDeets[90].iPullbacks = -1;
		PDeets[90].iBreakoutUp = 100;
		PDeets[90].iBreakoutDown = -1;
		PDeets[90].iPercentageBust = 14;
		PDeets[90].sTips = text;
		PDeets[90].iTall = -1f;
		PDeets[90].iWide = -1;
		PDeets[91].sDescription = "Three falling peaks";
		PDeets[91].sPerformance = "21 out of 36 (36 is worst)";
		PDeets[91].iReversal = 71;
		PDeets[91].iContinuation = 29;
		PDeets[91].iFailureRate = 22;
		PDeets[91].iChangeTrend = 27;
		PDeets[91].iPctMeetingTargetUp = -1;
		PDeets[91].iPctMeetingTargetDown = 23;
		PDeets[91].iThrowbacks = -1;
		PDeets[91].iPullbacks = 66;
		PDeets[91].iBreakoutUp = -1;
		PDeets[91].iBreakoutDown = 100;
		PDeets[91].iPercentageBust = 35;
		PDeets[91].sTips = text2;
		PDeets[91].iTall = -1f;
		PDeets[91].iWide = -1;
		PDeets[92].sDescription = "Rising wedge";
		PDeets[92].sPerformance = "32 out of 39 (39 is worst)";
		PDeets[92].iReversal = 31;
		PDeets[92].iContinuation = 69;
		PDeets[92].iFailureRate = 19;
		PDeets[92].iChangeTrend = 51;
		PDeets[92].iPctMeetingTargetUp = 63;
		PDeets[92].iPctMeetingTargetDown = 32;
		PDeets[92].iThrowbacks = 72;
		PDeets[92].iPullbacks = 72;
		PDeets[92].iBreakoutUp = 40;
		PDeets[92].iBreakoutDown = 60;
		PDeets[92].iPercentageBust = 21;
		PDeets[92].sTips = text;
		PDeets[92].iTall = -1f;
		PDeets[92].iWide = 42;
		PDeets[93].sDescription = "Head-and-shoulders complex bottom";
		PDeets[93].sPerformance = "9 out of 39 (39 is worst)";
		PDeets[93].iReversal = 100;
		PDeets[93].iContinuation = -1;
		PDeets[93].iFailureRate = 7;
		PDeets[93].iChangeTrend = 64;
		PDeets[93].iPctMeetingTargetUp = 71;
		PDeets[93].iPctMeetingTargetDown = -1;
		PDeets[93].iThrowbacks = 66;
		PDeets[93].iPullbacks = -1;
		PDeets[93].iBreakoutUp = 100;
		PDeets[93].iBreakoutDown = -1;
		PDeets[93].iPercentageBust = 12;
		PDeets[93].sTips = text;
		PDeets[93].iTall = 15.3f;
		PDeets[93].iWide = 62;
		PDeets[94].sDescription = "Head-and-shoulders bottom";
		PDeets[94].sPerformance = "13 out of 39 (39 is worst)";
		PDeets[94].iReversal = 100;
		PDeets[94].iContinuation = -1;
		PDeets[94].iFailureRate = 11;
		PDeets[94].iChangeTrend = 61;
		PDeets[94].iPctMeetingTargetUp = 71;
		PDeets[94].iPctMeetingTargetDown = -1;
		PDeets[94].iThrowbacks = 65;
		PDeets[94].iPullbacks = -1;
		PDeets[94].iBreakoutUp = 100;
		PDeets[94].iBreakoutDown = -1;
		PDeets[94].iPercentageBust = 16;
		PDeets[94].sTips = text;
		PDeets[94].iTall = 13.4f;
		PDeets[94].iWide = -1;
		PDeets[95].sDescription = "Flag, high and tight";
		PDeets[95].sPerformance = "30 out of 39 (39 is worst)";
		PDeets[95].iReversal = -1;
		PDeets[95].iContinuation = 100;
		PDeets[95].iFailureRate = 15;
		PDeets[95].iChangeTrend = 55;
		PDeets[95].iPctMeetingTargetUp = 82;
		PDeets[95].iPctMeetingTargetDown = -1;
		PDeets[95].iThrowbacks = 67;
		PDeets[95].iPullbacks = -1;
		PDeets[95].iBreakoutUp = 100;
		PDeets[95].iBreakoutDown = -1;
		PDeets[95].iPercentageBust = -1;
		PDeets[95].sTips = text;
		PDeets[95].iTall = -1f;
		PDeets[95].iWide = 60;
		PDeets[96].sDescription = "Falling wedge";
		PDeets[96].sPerformance = "31 out of 39 (39 is worst)";
		PDeets[96].iReversal = 49;
		PDeets[96].iContinuation = 51;
		PDeets[96].iFailureRate = 26;
		PDeets[96].iChangeTrend = 46;
		PDeets[96].iPctMeetingTargetUp = 62;
		PDeets[96].iPctMeetingTargetDown = 29;
		PDeets[96].iThrowbacks = 62;
		PDeets[96].iPullbacks = 74;
		PDeets[96].iBreakoutUp = 68;
		PDeets[96].iBreakoutDown = 32;
		PDeets[96].iPercentageBust = 31;
		PDeets[96].sTips = text;
		PDeets[96].iTall = 15f;
		PDeets[96].iWide = 38;
		PDeets[97].sDescription = "Double tops (all Types)";
		PDeets[97].sPerformance = "12 out of 36 (36 is worst)";
		PDeets[97].iReversal = 100;
		PDeets[97].iContinuation = -1;
		PDeets[97].iFailureRate = 20;
		PDeets[97].iChangeTrend = 29;
		PDeets[97].iPctMeetingTargetUp = -1;
		PDeets[97].iPctMeetingTargetDown = 43;
		PDeets[97].iThrowbacks = -1;
		PDeets[97].iPullbacks = 65;
		PDeets[97].iBreakoutUp = -1;
		PDeets[97].iBreakoutDown = 100;
		PDeets[97].iPercentageBust = 36;
		PDeets[97].sTips = "For double tops, I used Eve and Eve double top for statistics.";
		PDeets[97].iTall = 13.7f;
		PDeets[97].iWide = -1;
		PDeets[98].sDescription = "Double bottoms (all Types)";
		PDeets[98].sPerformance = "5 out of 39 (39 is worst)";
		PDeets[98].iReversal = 100;
		PDeets[98].iContinuation = -1;
		PDeets[98].iFailureRate = 12;
		PDeets[98].iChangeTrend = 61;
		PDeets[98].iPctMeetingTargetUp = 65;
		PDeets[98].iPctMeetingTargetDown = -1;
		PDeets[98].iThrowbacks = 65;
		PDeets[98].iPullbacks = -1;
		PDeets[98].iBreakoutUp = 100;
		PDeets[98].iBreakoutDown = 20;
		PDeets[98].iPercentageBust = 20;
		PDeets[98].sTips = "For double bottoms, I used Eve and Eve double bottom for statistics.";
		PDeets[98].iTall = -1f;
		PDeets[98].iWide = 36;
		PDeets[99].sDescription = "Dead-cat bounce, inverted";
		PDeets[99].sPerformance = sPerformance;
		PDeets[99].iReversal = -1;
		PDeets[99].iContinuation = -1;
		PDeets[99].iFailureRate = -1;
		PDeets[99].iChangeTrend = -1;
		PDeets[99].iPctMeetingTargetUp = -1;
		PDeets[99].iPctMeetingTargetDown = -1;
		PDeets[99].iThrowbacks = -1;
		PDeets[99].iPullbacks = -1;
		PDeets[99].iBreakoutUp = -1;
		PDeets[99].iBreakoutDown = -1;
		PDeets[99].iPercentageBust = -1;
		PDeets[99].sTips = sTips;
		PDeets[99].iTall = -1f;
		PDeets[99].iWide = -1;
		PDeets[100].sDescription = "Dead-cat bounce";
		PDeets[100].sPerformance = sPerformance;
		PDeets[100].iReversal = -1;
		PDeets[100].iContinuation = -1;
		PDeets[100].iFailureRate = -1;
		PDeets[100].iChangeTrend = -1;
		PDeets[100].iPctMeetingTargetUp = -1;
		PDeets[100].iPctMeetingTargetDown = -1;
		PDeets[100].iThrowbacks = -1;
		PDeets[100].iPullbacks = -1;
		PDeets[100].iBreakoutUp = -1;
		PDeets[100].iBreakoutDown = -1;
		PDeets[100].iPercentageBust = -1;
		PDeets[100].sTips = "Event decline: 31% in 7 days, bounce rise: 28% in 23 days, postbounce drop: 30% in 49 days (all numbers are averages).";
		PDeets[100].iTall = -1f;
		PDeets[100].iWide = -1;
		PDeets[101].sDescription = "Rectangle top";
		PDeets[101].sPerformance = "4 out of 39 (39 is worst)";
		PDeets[101].iReversal = -1;
		PDeets[101].iContinuation = 100;
		PDeets[101].iFailureRate = 15;
		PDeets[101].iChangeTrend = 59;
		PDeets[101].iPctMeetingTargetUp = 78;
		PDeets[101].iPctMeetingTargetDown = 54;
		PDeets[101].iThrowbacks = 66;
		PDeets[101].iPullbacks = 64;
		PDeets[101].iBreakoutUp = 63;
		PDeets[101].iBreakoutDown = 37;
		PDeets[101].iPercentageBust = 26;
		PDeets[101].sTips = text;
		PDeets[101].iTall = 7.9f;
		PDeets[101].iWide = 53;
		PDeets[102].sDescription = "Rectangle bottom";
		PDeets[102].sPerformance = "8 out of 39 (39 is worst)";
		PDeets[102].iReversal = 100;
		PDeets[102].iContinuation = -1;
		PDeets[102].iFailureRate = 15;
		PDeets[102].iChangeTrend = 56;
		PDeets[102].iPctMeetingTargetUp = 79;
		PDeets[102].iPctMeetingTargetDown = 55;
		PDeets[102].iThrowbacks = 64;
		PDeets[102].iPullbacks = 66;
		PDeets[102].iBreakoutUp = 59;
		PDeets[102].iBreakoutDown = 41;
		PDeets[102].iPercentageBust = 26;
		PDeets[102].sTips = text;
		PDeets[102].iTall = 8.3f;
		PDeets[102].iWide = 55;
		PDeets[103].sDescription = "Pipe top";
		PDeets[103].sPerformance = "1 (best) out of 2";
		PDeets[103].iReversal = 100;
		PDeets[103].iContinuation = -1;
		PDeets[103].iFailureRate = 13;
		PDeets[103].iChangeTrend = 38;
		PDeets[103].iPctMeetingTargetUp = -1;
		PDeets[103].iPctMeetingTargetDown = 54;
		PDeets[103].iThrowbacks = -1;
		PDeets[103].iPullbacks = -1;
		PDeets[103].iBreakoutUp = -1;
		PDeets[103].iBreakoutDown = 100;
		PDeets[103].iPercentageBust = 27;
		PDeets[103].sTips = text2;
		PDeets[103].iTall = 13f;
		PDeets[103].iWide = -1;
		PDeets[104].sDescription = "Pipe bottom";
		PDeets[104].sPerformance = "3 (worst) out of 3";
		PDeets[104].iReversal = 100;
		PDeets[104].iContinuation = -1;
		PDeets[104].iFailureRate = 8;
		PDeets[104].iChangeTrend = 63;
		PDeets[104].iPctMeetingTargetUp = 77;
		PDeets[104].iPctMeetingTargetDown = -1;
		PDeets[104].iThrowbacks = -1;
		PDeets[104].iPullbacks = -1;
		PDeets[104].iBreakoutUp = 100;
		PDeets[104].iBreakoutDown = -1;
		PDeets[104].iPercentageBust = 16;
		PDeets[104].sTips = text;
		PDeets[104].iTall = 12.2f;
		PDeets[104].iWide = -1;
		PDeets[105].sDescription = "Horn top";
		PDeets[105].sPerformance = "1 (best) out of 2";
		PDeets[105].iReversal = 100;
		PDeets[105].iContinuation = -1;
		PDeets[105].iFailureRate = 9;
		PDeets[105].iChangeTrend = 36;
		PDeets[105].iPctMeetingTargetUp = -1;
		PDeets[105].iPctMeetingTargetDown = 54;
		PDeets[105].iThrowbacks = -1;
		PDeets[105].iPullbacks = -1;
		PDeets[105].iBreakoutUp = -1;
		PDeets[105].iBreakoutDown = 100;
		PDeets[105].iPercentageBust = 28;
		PDeets[105].sTips = text2;
		PDeets[105].iTall = 13.95f;
		PDeets[105].iWide = -1;
		PDeets[106].sDescription = "Horn bottom";
		PDeets[106].sPerformance = "2 out of 3 (3 is worst)";
		PDeets[106].iReversal = 100;
		PDeets[106].iContinuation = -1;
		PDeets[106].iFailureRate = 6;
		PDeets[106].iChangeTrend = 65;
		PDeets[106].iPctMeetingTargetUp = 74;
		PDeets[106].iPctMeetingTargetDown = -1;
		PDeets[106].iThrowbacks = -1;
		PDeets[106].iPullbacks = -1;
		PDeets[106].iBreakoutUp = 100;
		PDeets[106].iBreakoutDown = -1;
		PDeets[106].iPercentageBust = 16;
		PDeets[106].sTips = text;
		PDeets[106].iTall = 13.5f;
		PDeets[106].iWide = -1;
		PDeets[107].sDescription = "Head-and-shoulders top";
		PDeets[107].sPerformance = "9 out of 36 (36 is worst)";
		PDeets[107].iReversal = 100;
		PDeets[107].iContinuation = -1;
		PDeets[107].iFailureRate = 19;
		PDeets[107].iChangeTrend = 29;
		PDeets[107].iPctMeetingTargetUp = -1;
		PDeets[107].iPctMeetingTargetDown = 51;
		PDeets[107].iThrowbacks = -1;
		PDeets[107].iPullbacks = 68;
		PDeets[107].iBreakoutUp = -1;
		PDeets[107].iBreakoutDown = 100;
		PDeets[107].iPercentageBust = 32;
		PDeets[107].sTips = text2;
		PDeets[107].iTall = 12.5f;
		PDeets[107].iWide = -1;
		PDeets[108].sDescription = "Head-and-shoulders complex top";
		PDeets[108].sPerformance = "7 out of 36 (36 is worst)";
		PDeets[108].iReversal = 100;
		PDeets[108].iContinuation = -1;
		PDeets[108].iFailureRate = 18;
		PDeets[108].iChangeTrend = 32;
		PDeets[108].iPctMeetingTargetUp = -1;
		PDeets[108].iPctMeetingTargetDown = 47;
		PDeets[108].iThrowbacks = -1;
		PDeets[108].iPullbacks = 66;
		PDeets[108].iBreakoutUp = -1;
		PDeets[108].iBreakoutDown = 100;
		PDeets[108].iPercentageBust = 29;
		PDeets[108].sTips = text2;
		PDeets[108].iTall = 15.4f;
		PDeets[108].iWide = 60;
		PDeets[109].sDescription = "Broadening wedge, descending";
		PDeets[109].sPerformance = "27 out of 39 (39 is worst)";
		PDeets[109].iReversal = 58;
		PDeets[109].iContinuation = 42;
		PDeets[109].iFailureRate = 18;
		PDeets[109].iChangeTrend = 55;
		PDeets[109].iPctMeetingTargetUp = 83;
		PDeets[109].iPctMeetingTargetDown = 32;
		PDeets[109].iThrowbacks = 62;
		PDeets[109].iPullbacks = 64;
		PDeets[109].iBreakoutUp = 72;
		PDeets[109].iBreakoutDown = 28;
		PDeets[109].iPercentageBust = 21;
		PDeets[109].sTips = text;
		PDeets[109].iTall = 15.9f;
		PDeets[109].iWide = 50;
		PDeets[110].sDescription = "Broadening wedge, ascending";
		PDeets[110].sPerformance = "23 out of 39 (39 is worst)";
		PDeets[110].iReversal = 19;
		PDeets[110].iContinuation = 81;
		PDeets[110].iFailureRate = 15;
		PDeets[110].iChangeTrend = 54;
		PDeets[110].iPctMeetingTargetUp = 61;
		PDeets[110].iPctMeetingTargetDown = 71;
		PDeets[110].iThrowbacks = 68;
		PDeets[110].iPullbacks = 62;
		PDeets[110].iBreakoutUp = 48;
		PDeets[110].iBreakoutDown = 52;
		PDeets[110].iPercentageBust = 19;
		PDeets[110].sTips = text;
		PDeets[110].iTall = -1f;
		PDeets[110].iWide = -1;
		PDeets[111].sDescription = "Broadening top";
		PDeets[111].sPerformance = "22 out of 39 (39 is worst)";
		PDeets[111].iReversal = -1;
		PDeets[111].iContinuation = 100;
		PDeets[111].iFailureRate = 18;
		PDeets[111].iChangeTrend = 52;
		PDeets[111].iPctMeetingTargetUp = 66;
		PDeets[111].iPctMeetingTargetDown = 42;
		PDeets[111].iThrowbacks = 67;
		PDeets[111].iPullbacks = 67;
		PDeets[111].iBreakoutUp = 60;
		PDeets[111].iBreakoutDown = 40;
		PDeets[111].iPercentageBust = 29;
		PDeets[111].sTips = text;
		PDeets[111].iTall = 10.6f;
		PDeets[111].iWide = 45;
		PDeets[112].sDescription = "Broadening formation, right-angled & descending";
		PDeets[112].sPerformance = "19 out of 39 (39 is worst)";
		PDeets[112].iReversal = 38;
		PDeets[112].iContinuation = 62;
		PDeets[112].iFailureRate = 21;
		PDeets[112].iChangeTrend = 54;
		PDeets[112].iPctMeetingTargetUp = 65;
		PDeets[112].iPctMeetingTargetDown = 51;
		PDeets[112].iThrowbacks = 64;
		PDeets[112].iPullbacks = 69;
		PDeets[112].iBreakoutUp = 64;
		PDeets[112].iBreakoutDown = 36;
		PDeets[112].iPercentageBust = 29;
		PDeets[112].sTips = text;
		PDeets[112].iTall = 9.7f;
		PDeets[112].iWide = 50;
		PDeets[113].sDescription = "Broadening formation, right-angled & ascending";
		PDeets[113].sPerformance = "18 out of 39 (39 is worst)";
		PDeets[113].iReversal = 25;
		PDeets[113].iContinuation = 75;
		PDeets[113].iFailureRate = 15;
		PDeets[113].iChangeTrend = 55;
		PDeets[113].iPctMeetingTargetUp = 67;
		PDeets[113].iPctMeetingTargetDown = 40;
		PDeets[113].iThrowbacks = 68;
		PDeets[113].iPullbacks = 63;
		PDeets[113].iBreakoutUp = 55;
		PDeets[113].iBreakoutDown = 45;
		PDeets[113].iPercentageBust = 26;
		PDeets[113].sTips = text;
		PDeets[113].iTall = 10.6f;
		PDeets[113].iWide = 50;
		PDeets[114].sDescription = "Broadening bottom";
		PDeets[114].sPerformance = "15 out of 39 (39 is worst)";
		PDeets[114].iReversal = 100;
		PDeets[114].iContinuation = -1;
		PDeets[114].iFailureRate = 16;
		PDeets[114].iChangeTrend = 52;
		PDeets[114].iPctMeetingTargetUp = 65;
		PDeets[114].iPctMeetingTargetDown = 41;
		PDeets[114].iThrowbacks = 69;
		PDeets[114].iPullbacks = 62;
		PDeets[114].iBreakoutUp = 60;
		PDeets[114].iBreakoutDown = 40;
		PDeets[114].iPercentageBust = 25;
		PDeets[114].sTips = text;
		PDeets[114].iTall = 12f;
		PDeets[114].iWide = 41;
		PDeets[115].sDescription = "Big W";
		PDeets[115].sPerformance = "11 out of 39 (39 is worst)";
		PDeets[115].iReversal = 100;
		PDeets[115].iContinuation = -1;
		PDeets[115].iFailureRate = -1;
		PDeets[115].iChangeTrend = 62;
		PDeets[115].iPctMeetingTargetUp = 74;
		PDeets[115].iPctMeetingTargetDown = -1;
		PDeets[115].iThrowbacks = 64;
		PDeets[115].iPullbacks = -1;
		PDeets[115].iBreakoutUp = 100;
		PDeets[115].iBreakoutDown = -1;
		PDeets[115].iPercentageBust = 18;
		PDeets[115].sTips = text;
		PDeets[115].iTall = 11.9f;
		PDeets[115].iWide = -1;
		PDeets[116].sDescription = "Big M";
		PDeets[116].sPerformance = "8 out of 36 (36 is worst)";
		PDeets[116].iReversal = 100;
		PDeets[116].iContinuation = -1;
		PDeets[116].iFailureRate = 14;
		PDeets[116].iChangeTrend = 32;
		PDeets[116].iPctMeetingTargetUp = -1;
		PDeets[116].iPctMeetingTargetDown = 55;
		PDeets[116].iThrowbacks = -1;
		PDeets[116].iPullbacks = 67;
		PDeets[116].iBreakoutUp = -1;
		PDeets[116].iBreakoutDown = 100;
		PDeets[116].iPercentageBust = 38;
		PDeets[116].sTips = text2;
		PDeets[116].iTall = -1f;
		PDeets[116].iWide = -1;
		PDeets[117].sDescription = "Gap, breakaway";
		PDeets[117].sPerformance = sPerformance;
		PDeets[117].iReversal = -1;
		PDeets[117].iContinuation = -1;
		PDeets[117].iFailureRate = -1;
		PDeets[117].iChangeTrend = -1;
		PDeets[117].iPctMeetingTargetUp = -1;
		PDeets[117].iPctMeetingTargetDown = -1;
		PDeets[117].iThrowbacks = -1;
		PDeets[117].iPullbacks = -1;
		PDeets[117].iBreakoutUp = -1;
		PDeets[117].iBreakoutDown = -1;
		PDeets[117].iPercentageBust = -1;
		PDeets[117].sTips = "Only 1% close within a week (for both breakout directions), taking an average of 337 days to close.";
		PDeets[117].iTall = -1f;
		PDeets[117].iWide = -1;
		PDeets[118].sDescription = "Gap, area or common";
		PDeets[118].sPerformance = sPerformance;
		PDeets[118].iReversal = -1;
		PDeets[118].iContinuation = -1;
		PDeets[118].iFailureRate = -1;
		PDeets[118].iChangeTrend = -1;
		PDeets[118].iPctMeetingTargetUp = -1;
		PDeets[118].iPctMeetingTargetDown = -1;
		PDeets[118].iThrowbacks = -1;
		PDeets[118].iPullbacks = -1;
		PDeets[118].iBreakoutUp = -1;
		PDeets[118].iBreakoutDown = -1;
		PDeets[118].iPercentageBust = -1;
		PDeets[118].sTips = "Most (85% to 90%) close within a week (for both breakout directions), taking an average of 4 to 5 days to close.";
		PDeets[118].iTall = -1f;
		PDeets[118].iWide = -1;
		PDeets[119].sDescription = "Gap, continuation";
		PDeets[119].sPerformance = sPerformance;
		PDeets[119].iReversal = -1;
		PDeets[119].iContinuation = -1;
		PDeets[119].iFailureRate = -1;
		PDeets[119].iChangeTrend = -1;
		PDeets[119].iPctMeetingTargetUp = -1;
		PDeets[119].iPctMeetingTargetDown = -1;
		PDeets[119].iThrowbacks = -1;
		PDeets[119].iPullbacks = -1;
		PDeets[119].iBreakoutUp = -1;
		PDeets[119].iBreakoutDown = -1;
		PDeets[119].iPercentageBust = -1;
		PDeets[119].sTips = "Eight percent (up breakouts) and 15% of down breakouts close within a week. The average time to close is 168 day (up breakouts) to 104 days (down breakouts).";
		PDeets[119].iTall = -1f;
		PDeets[119].iWide = -1;
		PDeets[120].sDescription = "Gap, type unknown";
		PDeets[120].sPerformance = sPerformance;
		PDeets[120].iReversal = -1;
		PDeets[120].iContinuation = -1;
		PDeets[120].iFailureRate = -1;
		PDeets[120].iChangeTrend = -1;
		PDeets[120].iPctMeetingTargetUp = -1;
		PDeets[120].iPctMeetingTargetDown = -1;
		PDeets[120].iThrowbacks = -1;
		PDeets[120].iPullbacks = -1;
		PDeets[120].iBreakoutUp = -1;
		PDeets[120].iBreakoutDown = -1;
		PDeets[120].iPercentageBust = -1;
		PDeets[120].sTips = "Could be a dividend gap.";
		PDeets[120].iTall = -1f;
		PDeets[120].iWide = -1;
		PDeets[121].sDescription = "Gap, exhaustion";
		PDeets[121].sPerformance = sPerformance;
		PDeets[121].iReversal = -1;
		PDeets[121].iContinuation = -1;
		PDeets[121].iFailureRate = -1;
		PDeets[121].iChangeTrend = -1;
		PDeets[121].iPctMeetingTargetUp = -1;
		PDeets[121].iPctMeetingTargetDown = -1;
		PDeets[121].iThrowbacks = -1;
		PDeets[121].iPullbacks = -1;
		PDeets[121].iBreakoutUp = -1;
		PDeets[121].iBreakoutDown = -1;
		PDeets[121].iPercentageBust = -1;
		PDeets[121].sTips = "Sixty percent close in a week after an upward breakout, and 66% after a downward breakout.";
		PDeets[121].iTall = -1f;
		PDeets[121].iWide = -1;
		PDeets[122].sDescription = "Gap 2H";
		PDeets[122].sPerformance = "21 out of 23 (23 is worst)";
		PDeets[122].iReversal = 28;
		PDeets[122].iContinuation = 72;
		PDeets[122].iFailureRate = 34;
		PDeets[122].iChangeTrend = 53;
		PDeets[122].iPctMeetingTargetUp = -1;
		PDeets[122].iPctMeetingTargetDown = -1;
		PDeets[122].iThrowbacks = -1;
		PDeets[122].iPullbacks = -1;
		PDeets[122].iBreakoutUp = -1;
		PDeets[122].iBreakoutDown = -1;
		PDeets[122].iPercentageBust = -1;
		PDeets[122].sTips = text;
		PDeets[122].iTall = -1f;
		PDeets[122].iWide = -1;
		PDeets[123].sDescription = "Gap 2H, inverted";
		PDeets[123].sPerformance = "17 out of 23 (23 is worst)";
		PDeets[123].iReversal = 31;
		PDeets[123].iContinuation = 69;
		PDeets[123].iFailureRate = 39;
		PDeets[123].iChangeTrend = -1;
		PDeets[123].iPctMeetingTargetUp = -1;
		PDeets[123].iPctMeetingTargetDown = 44;
		PDeets[123].iThrowbacks = -1;
		PDeets[123].iPullbacks = -1;
		PDeets[123].iBreakoutUp = -1;
		PDeets[123].iBreakoutDown = -1;
		PDeets[123].iPercentageBust = -1;
		PDeets[123].sTips = text2;
		PDeets[123].iTall = -1f;
		PDeets[123].iWide = -1;
		PDeets[0].sDescription = "2-Dance";
		PDeets[0].sPerformance = sPerformance;
		PDeets[0].iReversal = -1;
		PDeets[0].iContinuation = -1;
		PDeets[0].iFailureRate = -1;
		PDeets[0].iChangeTrend = -1;
		PDeets[0].iPctMeetingTargetUp = -1;
		PDeets[0].iPctMeetingTargetDown = -1;
		PDeets[0].iThrowbacks = -1;
		PDeets[0].iPullbacks = -1;
		PDeets[0].iBreakoutUp = -1;
		PDeets[0].iBreakoutDown = -1;
		PDeets[0].iPercentageBust = -1;
		PDeets[0].sTips = "See ThePatternSite.com for more details.";
		PDeets[0].iTall = -1f;
		PDeets[0].iWide = -1;
		PDeets[23].sDescription = "2-Did";
		PDeets[23].sPerformance = sPerformance;
		PDeets[23].iReversal = -1;
		PDeets[23].iContinuation = -1;
		PDeets[23].iFailureRate = -1;
		PDeets[23].iChangeTrend = -1;
		PDeets[23].iPctMeetingTargetUp = -1;
		PDeets[23].iPctMeetingTargetDown = -1;
		PDeets[23].iThrowbacks = -1;
		PDeets[23].iPullbacks = -1;
		PDeets[23].iBreakoutUp = -1;
		PDeets[23].iBreakoutDown = -1;
		PDeets[23].iPercentageBust = -1;
		PDeets[23].sTips = "See ThePatternSite.com for more details.";
		PDeets[23].iTall = -1f;
		PDeets[23].iWide = -1;
		PDeets[22].sDescription = "2-Tall";
		PDeets[22].sPerformance = sPerformance;
		PDeets[22].iReversal = -1;
		PDeets[22].iContinuation = -1;
		PDeets[22].iFailureRate = -1;
		PDeets[22].iChangeTrend = -1;
		PDeets[22].iPctMeetingTargetUp = -1;
		PDeets[22].iPctMeetingTargetDown = -1;
		PDeets[22].iThrowbacks = -1;
		PDeets[22].iPullbacks = -1;
		PDeets[22].iBreakoutUp = -1;
		PDeets[22].iBreakoutDown = -1;
		PDeets[22].iPercentageBust = -1;
		PDeets[22].sTips = "See ThePatternSite.com for more details.";
		PDeets[22].iTall = -1f;
		PDeets[22].iWide = -1;
		PDeets[37].sDescription = "Pothole";
		PDeets[37].sPerformance = sPerformance;
		PDeets[37].iReversal = -1;
		PDeets[37].iContinuation = -1;
		PDeets[37].iFailureRate = -1;
		PDeets[37].iChangeTrend = -1;
		PDeets[37].iPctMeetingTargetUp = -1;
		PDeets[37].iPctMeetingTargetDown = -1;
		PDeets[37].iThrowbacks = -1;
		PDeets[37].iPullbacks = -1;
		PDeets[37].iBreakoutUp = -1;
		PDeets[37].iBreakoutDown = -1;
		PDeets[37].iPercentageBust = -1;
		PDeets[37].sTips = "See ThePatternSite.com for more details.";
		PDeets[37].iTall = -1f;
		PDeets[37].iWide = -1;
	}

	public static DateTime FindDate(DateTime CurrentDate)
	{
		List<DateTime> holidayList = GetHolidayList(DateAndTime.Year(CurrentDate));
		while (true)
		{
			IL_000c:
			int num = DateAndTime.Weekday(CurrentDate, (FirstDayOfWeek)1);
			if (num == 1 || num == 7)
			{
				CurrentDate = DateAndTime.DateAdd((DateInterval)4, -1.0, CurrentDate);
				continue;
			}
			foreach (DateTime item in holidayList)
			{
				if (DateTime.Compare(item.Date, CurrentDate.Date) == 0)
				{
					CurrentDate = DateAndTime.DateAdd((DateInterval)4, -1.0, CurrentDate);
					goto IL_000c;
				}
			}
			holidayList = GetHolidayList(checked(DateAndTime.Year(CurrentDate) - 1));
			using List<DateTime>.Enumerator enumerator2 = holidayList.GetEnumerator();
			do
			{
				if (!enumerator2.MoveNext())
				{
					return CurrentDate;
				}
			}
			while (DateTime.Compare(enumerator2.Current.Date, CurrentDate.Date) != 0);
			CurrentDate = DateAndTime.DateAdd((DateInterval)4, -1.0, CurrentDate);
		}
	}

	public static void FormatPickers(DateTimePicker FromDatePicker, DateTimePicker ToDatePicker)
	{
		FromDatePicker.CustomFormat = "yyyy-MM-dd HH:mm";
		ToDatePicker.CustomFormat = "yyyy-MM-dd HH:mm";
	}

	public static decimal GetPriceFill(int Index, decimal ConfirmationPrice, int BkoutDirection, bool CandleFlag)
	{
		int num = checked(Index + 1);
		decimal originalNumber = ((num > HLCRange) ? ConfirmationPrice : ((BkoutDirection == 1) ? (CandleFlag ? ((decimal.Compare(FindCandles.Storage[0, num], ConfirmationPrice) < 0) ? ConfirmationPrice : FindCandles.Storage[0, num]) : ((decimal.Compare(nHLC[0, num], ConfirmationPrice) < 0) ? ConfirmationPrice : nHLC[0, num])) : (CandleFlag ? ((decimal.Compare(FindCandles.Storage[0, num], ConfirmationPrice) > 0) ? ConfirmationPrice : FindCandles.Storage[0, num]) : ((decimal.Compare(nHLC[0, num], ConfirmationPrice) > 0) ? ConfirmationPrice : nHLC[0, num]))));
		return LimitDecimals(originalNumber);
	}

	public static List<DateTime> GetHolidayList(int vYear)
	{
		int whichWeek = 1;
		int whichWeek2 = 3;
		int whichWeek3 = 4;
		int whichWeek4 = 5;
		List<DateTime> list = new List<DateTime>
		{
			DateAndTime.DateSerial(vYear, 1, 1),
			GetNthDayOfNthWeek(DateAndTime.DateSerial(vYear, 1, 1), 1, whichWeek2),
			GetNthDayOfNthWeek(DateAndTime.DateSerial(vYear, 2, 1), 1, whichWeek2),
			GetNthDayOfNthWeek(DateAndTime.DateSerial(vYear, 5, 1), 1, whichWeek4),
			DateAndTime.DateSerial(vYear, 6, 19),
			DateAndTime.DateSerial(vYear, 7, 4),
			GetNthDayOfNthWeek(DateAndTime.DateSerial(vYear, 9, 1), 1, whichWeek),
			GetNthDayOfNthWeek(DateAndTime.DateSerial(vYear, 11, 1), 4, whichWeek3),
			DateAndTime.DateSerial(vYear, 12, 25)
		};
		checked
		{
			int num = list.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				DateTime dateTime = list[i];
				if (dateTime.DayOfWeek == DayOfWeek.Saturday)
				{
					list[i] = dateTime.AddDays(-1.0);
				}
				if (dateTime.DayOfWeek == DayOfWeek.Sunday)
				{
					list[i] = dateTime.AddDays(1.0);
				}
			}
			return list;
		}
	}

	public static void GetCPInformation(int Index)
	{
		int num = -1;
		int num2 = -1;
		decimal num3 = default(decimal);
		int num4 = 0;
		int num5 = 0;
		int num6 = 0;
		int num7 = 0;
		CPInfo.BkoutDirection = null;
		CPInfo.BkoutDate = null;
		CPInfo.iBkout = -1;
		CPInfo.BkoutPrice = null;
		CPInfo.Target = null;
		CPInfo.VolStop = null;
		CPInfo.UltHLPrice = null;
		CPInfo.UltHLDate = null;
		CPInfo.Status = null;
		CPInfo.AvgVolume = null;
		ChartPatterns[Index].PriceTarget = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(ChartPatterns[Index].PriceTarget, 0m) < 0, (object)0, (object)ChartPatterns[Index].PriceTarget));
		int type = ChartPatterns[Index].Type;
		int ReturnStart = ChartPatterns[Index].iStartDate;
		int ReturnEnd = ChartPatterns[Index].iEndDate;
		GetStartEndDates(Index, ref ReturnStart, ref ReturnEnd);
		int num8 = Conversions.ToInteger(Interaction.IIf((ChartPatterns[Index].iEnd2Date != 0) & (ChartPatterns[Index].iEnd2Date < ReturnEnd), (object)ChartPatterns[Index].iEnd2Date, (object)ReturnEnd));
		int hLCRange = HLCRange;
		checked
		{
			int num9 = default(int);
			int num10 = default(int);
			int num11 = default(int);
			decimal num12 = default(decimal);
			decimal num13 = default(decimal);
			decimal num17 = default(decimal);
			int breakoutType = default(int);
			for (int i = 0; i <= hLCRange; i++)
			{
				try
				{
					num3 = decimal.Add(num3, decimal.Subtract(nHLC[1, i], nHLC[2, i]));
					if (i > 19)
					{
						num3 = decimal.Subtract(num3, decimal.Subtract(nHLC[1, i - 20], nHLC[2, i - 20]));
					}
					unchecked
					{
						if (i >= ReturnStart && i <= ReturnEnd)
						{
							if (type == 67 || type == 78)
							{
								if (i == ChartPatterns[Index].iMidDate)
								{
									num9 = i;
									num10 = i;
								}
								else if (i > ChartPatterns[Index].iMidDate)
								{
									if (decimal.Compare(nHLC[2, i], nHLC[2, num10]) < 0)
									{
										num10 = i;
									}
									if (decimal.Compare(nHLC[1, i], nHLC[1, num9]) > 0)
									{
										num9 = i;
									}
								}
								if (i == ChartPatterns[Index].iStartDate)
								{
									num = i;
									num2 = i;
								}
								if (decimal.Compare(nHLC[2, i], nHLC[2, num2]) < 0)
								{
									num2 = i;
								}
								if (decimal.Compare(nHLC[1, i], nHLC[1, num]) > 0)
								{
									num = i;
								}
							}
							else if (type == 110 || type == 109)
							{
								if (i == ChartPatterns[Index].iStartDate)
								{
									num = i;
								}
								if (i == ChartPatterns[Index].iStart2Date)
								{
									num2 = i;
								}
								if (i == ChartPatterns[Index].iEndDate)
								{
									num11 = i;
								}
								if ((type == 110) & (i == ChartPatterns[Index].iEnd2Date))
								{
									num7 = i;
								}
								else if (type == 109)
								{
									if (num7 == 0)
									{
										num7 = i;
									}
									num7 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(nHLC[2, i], nHLC[2, num7]) < 0, (object)i, (object)num7));
								}
								num8 = ReturnEnd;
							}
							else if (type == 89 || type == 88 || type == 87 || type == 92 || type == 96)
							{
								if (type == 88)
								{
									if (i == ChartPatterns[Index].iStart2Date)
									{
										num = i;
									}
									if ((ChartPatterns[Index].iStartDate != 0) & (i == ChartPatterns[Index].iStartDate))
									{
										num2 = i;
									}
									if (((num2 != -1) & (i <= ChartPatterns[Index].iEndDate)) && decimal.Compare(nHLC[2, i], nHLC[2, num2]) < 0)
									{
										num2 = i;
									}
									if (i == ChartPatterns[Index].iEnd2Date)
									{
										num11 = i;
									}
									if ((ChartPatterns[Index].iEndDate != 0) & (i == ChartPatterns[Index].iEndDate))
									{
										num7 = i;
									}
								}
								else
								{
									if (i == ChartPatterns[Index].iStartDate)
									{
										num = i;
									}
									if (type == 89 && ((num != -1) & (i <= ChartPatterns[Index].iEndDate)) && decimal.Compare(nHLC[1, i], nHLC[1, num]) > 0)
									{
										num = i;
									}
									if ((ChartPatterns[Index].iStart2Date != 0) & (i == ChartPatterns[Index].iStart2Date))
									{
										num2 = i;
									}
									if (i == ChartPatterns[Index].iEndDate)
									{
										num11 = i;
									}
									if ((ChartPatterns[Index].iEnd2Date != 0) & (i == ChartPatterns[Index].iEnd2Date))
									{
										num7 = i;
									}
								}
							}
							else
							{
								checked
								{
									switch (type)
									{
									case 58:
									case 82:
										if (i == ReturnStart)
										{
											num2 = i;
										}
										if (decimal.Compare(nHLC[2, i], nHLC[2, num2]) < 0)
										{
											num2 = i;
										}
										if (i == ReturnEnd)
										{
											num = ReturnEnd;
											num12 = decimal.Divide(decimal.Subtract(nHLC[1, ChartPatterns[Index].iMidDate], nHLC[1, ReturnStart]), new decimal(ChartPatterns[Index].iMidDate - ReturnStart));
										}
										break;
									case 1:
									case 57:
										if (i == ReturnStart)
										{
											num = i;
										}
										if (decimal.Compare(nHLC[1, i], nHLC[1, num]) > 0)
										{
											num = i;
										}
										if (i == ReturnEnd)
										{
											num2 = ReturnEnd;
											num13 = decimal.Divide(decimal.Subtract(nHLC[2, ChartPatterns[Index].iMidDate], nHLC[2, ReturnStart]), new decimal(ChartPatterns[Index].iMidDate - ReturnStart));
										}
										break;
									case 14:
									case 15:
									case 16:
									case 17:
									case 18:
									case 19:
									case 20:
									case 21:
									case 33:
									case 34:
									case 85:
									case 86:
									case 97:
									case 98:
									case 115:
									case 116:
										if (i == ReturnStart + 1)
										{
											num = i;
											num2 = i;
										}
										if (i > ReturnStart)
										{
											if (decimal.Compare(nHLC[2, i], nHLC[2, num2]) < 0)
											{
												num2 = i;
											}
											if (decimal.Compare(nHLC[1, i], nHLC[1, num]) > 0)
											{
												num = i;
											}
										}
										break;
									default:
										if (i == ReturnStart)
										{
											num = i;
											num2 = i;
										}
										if (decimal.Compare(nHLC[2, i], nHLC[2, num2]) < 0)
										{
											num2 = i;
										}
										if (decimal.Compare(nHLC[1, i], nHLC[1, num]) > 0)
										{
											num = i;
										}
										break;
									}
								}
							}
							if (type == 94 || type == 93)
							{
								checked
								{
									if (i == ChartPatterns[Index].iMidDate)
									{
										num4 = i;
										num5 = i + 1;
									}
									if ((ChartPatterns[Index].iMid2Date != 0) & (i == ChartPatterns[Index].iMid2Date))
									{
										num4 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(nHLC[2, num4], nHLC[2, i]) < 0, (object)num4, (object)i));
										num5 = i + 1;
									}
									if (i == ReturnStart)
									{
										num6 = i + 1;
									}
									if (i < ChartPatterns[Index].iMidDate && num6 != 0)
									{
										num6 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(nHLC[1, i], nHLC[1, num6]) > 0, (object)i, (object)num6));
									}
									if (num4 != 0)
									{
										num5 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(nHLC[1, i], nHLC[1, num5]) > 0, (object)i, (object)num5));
									}
								}
							}
							else if (type == 107 || type == 108)
							{
								checked
								{
									if (i == ChartPatterns[Index].iMidDate)
									{
										num4 = i;
										num5 = i + 1;
									}
									if ((ChartPatterns[Index].iMid2Date != 0) & (i == ChartPatterns[Index].iMid2Date))
									{
										num4 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(nHLC[1, num4], nHLC[1, i]) > 0, (object)num4, (object)i));
										num5 = i + 1;
									}
									if (i == ReturnStart)
									{
										num6 = i + 1;
									}
									if (i < ChartPatterns[Index].iMidDate && num6 != 0)
									{
										num6 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(nHLC[2, i], nHLC[2, num6]) < 0, (object)i, (object)num6));
									}
									if (num4 != 0)
									{
										num5 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(nHLC[2, i], nHLC[2, num5]) < 0, (object)i, (object)num5));
									}
								}
							}
						}
						if (i < num8)
						{
							continue;
						}
					}
					switch (type)
					{
					case 84:
						if (decimal.Compare(nHLC[3, i], nHLC[1, ReturnEnd]) > 0)
						{
							CPInfo.BkoutDirection = "Up";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, ReturnEnd]);
							float num20 = Convert.ToSingle(decimal.Divide(decimal.Subtract(nHLC[1, ReturnEnd], nHLC[1, ReturnStart]), new decimal(ReturnEnd - ReturnStart)));
							decimal num21 = default(decimal);
							int num22 = ReturnStart + 1;
							int num23 = (int)Math.Round((double)ReturnStart + (double)(ReturnEnd - ReturnStart) / 4.0);
							for (int l = num22; l <= num23; l++)
							{
								decimal num19 = new decimal(num20 * (float)(l - ReturnStart) + Convert.ToSingle(nHLC[1, ReturnStart]));
								num21 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(decimal.Subtract(num19, nHLC[2, l]), num21) > 0, (object)decimal.Subtract(num19, nHLC[2, l]), (object)num21));
							}
							num17 = LimitDecimals(decimal.Add(nHLC[1, ReturnEnd], num21));
							ChartPatterns[Index].PriceTarget = num17;
							CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, ReturnEnd]), nHLC[1, ReturnEnd]), "0%");
							decimal num14 = ReportVolStop(i, num3, Index, 1);
							GetUltimateHighLow(i, ReturnEnd, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						goto end_IL_0177;
					case 83:
					{
						if (decimal.Compare(nHLC[3, i], nHLC[2, ReturnEnd]) >= 0)
						{
							continue;
						}
						CPInfo.BkoutDirection = "Down";
						CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
						CPInfo.iBkout = i;
						CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, ReturnEnd]);
						float num26 = Convert.ToSingle(decimal.Divide(decimal.Subtract(nHLC[2, ReturnEnd], nHLC[2, ReturnStart]), new decimal(ReturnEnd - ReturnStart)));
						decimal num27 = default(decimal);
						int num28 = ReturnStart + 1;
						int num29 = (int)Math.Round((double)ReturnStart + (double)(ReturnEnd - ReturnStart) / 4.0);
						for (int n = num28; n <= num29; n++)
						{
							decimal num19 = new decimal(num26 * (float)(n - ReturnStart) + Convert.ToSingle(nHLC[2, ReturnStart]));
							num27 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(decimal.Subtract(nHLC[1, n], num19), num27) > 0, (object)decimal.Subtract(nHLC[1, n], num19), (object)num27));
						}
						num17 = LimitDecimals(decimal.Subtract(nHLC[2, ReturnEnd], num27));
						if (decimal.Compare(num17, 0m) > 0)
						{
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(nHLC[2, ReturnEnd], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[2, ReturnEnd]), nHLC[2, ReturnEnd]), "0%");
							}
						}
						else
						{
							num17 = default(decimal);
							CPInfo.Target = "?";
						}
						decimal num14 = ReportVolStop(i, num3, Index, -1);
						GetUltimateHighLow(i, num, ReturnEnd, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
						CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
						break;
					}
					case 81:
						if (decimal.Compare(nHLC[3, i], nHLC[1, ChartPatterns[Index].iMidDate]) > 0)
						{
							CPInfo.BkoutDirection = "Up";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, ChartPatterns[Index].iMidDate]);
							num17 = ChartPatterns[Index].PriceTarget;
							if (decimal.Compare(nHLC[1, num], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, ChartPatterns[Index].iMidDate]), nHLC[1, ChartPatterns[Index].iMidDate]), "0%");
							}
							decimal num14 = ReportVolStop(i, num3, Index, 1);
							GetUltimateHighLow(i, ChartPatterns[Index].iMidDate, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						if ((i == ChartEndIndex) | (i == HLCRange))
						{
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, ChartPatterns[Index].iMidDate]);
							num17 = ChartPatterns[Index].PriceTarget;
							if (decimal.Compare(nHLC[1, num], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, ChartPatterns[Index].iMidDate]), nHLC[1, ChartPatterns[Index].iMidDate]), "0%");
							}
							decimal num14 = ReportVolStop(i, num3, Index, 1);
						}
						goto end_IL_0177;
					case 66:
						if (decimal.Compare(nHLC[3, i], nHLC[1, ReturnStart]) > 0)
						{
							CPInfo.BkoutDirection = "Up";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, ReturnStart]);
							num17 = ChartPatterns[Index].PriceTarget;
							if (decimal.Compare(nHLC[1, num], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, ReturnStart]), nHLC[1, ReturnStart]), "0%");
							}
							decimal num14 = ReportVolStop(i, num3, Index, 1);
							GetUltimateHighLow(i, ReturnEnd, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						if (decimal.Compare(nHLC[3, i], nHLC[2, num2]) < 0)
						{
							CPInfo.BkoutDirection = "Down";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num2]);
							num17 = LimitDecimals(decimal.Subtract(nHLC[2, num2], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
							if (decimal.Compare(num17, 0m) > 0)
							{
								ChartPatterns[Index].PriceTarget = num17;
								if (decimal.Compare(nHLC[2, num2], 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[2, num2]), nHLC[2, num2]), "0%");
								}
							}
							else
							{
								num17 = default(decimal);
								CPInfo.Target = "?";
							}
							decimal num14 = ReportVolStop(i, num3, Index, -1);
							GetUltimateHighLow(i, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
							break;
						}
						if (((i == ChartEndIndex) | (i == HLCRange)) && decimal.Compare(nHLC[3, i], nHLC[1, ReturnEnd]) <= 0)
						{
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, ReturnEnd]);
							num17 = ChartPatterns[Index].PriceTarget;
							if (decimal.Compare(nHLC[1, num], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, ReturnEnd]), nHLC[1, ReturnEnd]), "0%");
							}
							decimal num14 = ReportVolStop(i, num3, Index, 1);
						}
						goto end_IL_0177;
					case 48:
					case 65:
						if (decimal.Compare(nHLC[3, i], nHLC[2, num2]) < 0)
						{
							CPInfo.BkoutDirection = "Down";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num2]);
							num17 = LimitDecimals(decimal.Subtract(nHLC[2, num2], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
							if (decimal.Compare(num17, 0m) > 0)
							{
								ChartPatterns[Index].PriceTarget = num17;
								if (decimal.Compare(nHLC[2, num2], 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[2, num2]), nHLC[2, num2]), "0%");
								}
							}
							else
							{
								num17 = default(decimal);
								CPInfo.Target = "?";
							}
							decimal num14 = ReportVolStop(i, num3, Index, -1);
							GetUltimateHighLow(i, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
							break;
						}
						if (decimal.Compare(nHLC[3, i], nHLC[1, num]) > 0)
						{
							CPInfo.BkoutDirection = "Up";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num]);
							num17 = ChartPatterns[Index].PriceTarget;
							if (decimal.Compare(nHLC[1, num], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, num]), nHLC[1, num]), "0%");
							}
							decimal num14 = ReportVolStop(i, num3, Index, 1);
							GetUltimateHighLow(i, ReturnEnd, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						if (((i == ChartEndIndex) | (i == HLCRange)) && decimal.Compare(nHLC[3, i], nHLC[1, num]) <= 0)
						{
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num2]);
							num17 = ChartPatterns[Index].PriceTarget;
							if (decimal.Compare(nHLC[2, num2], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[2, num2]), nHLC[2, num2]), "0%");
							}
							decimal num14 = ReportVolStop(i, num3, Index, -1);
						}
						goto end_IL_0177;
					case 82:
					{
						CPInfo.BkoutDirection = "N/A";
						decimal num19 = decimal.Add(decimal.Multiply(num12, new decimal(i - ChartPatterns[Index].iMidDate)), nHLC[1, ChartPatterns[Index].iMidDate]);
						if (decimal.Compare(nHLC[1, i], num19) > 0)
						{
							if (!FindPatterns.CheckNearness(nHLC[1, i], num19, -1m, 0.1m))
							{
								CPInfo.BkoutDirection = "Up";
								CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
								CPInfo.iBkout = i;
								CPInfo.BkoutPrice = Conversions.ToString(LimitDecimals(num19));
								num17 = decimal.Add(num19, ChartPatterns[Index].dChannelHeight);
								ChartPatterns[Index].PriceTarget = num17;
								if (decimal.Compare(num19, 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(LimitDecimals(num17)) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
								}
								GetUltimateHighLow(i, num2, -1, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
								decimal num14 = ReportVolStop(i, num3, Index, 1);
								CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
								break;
							}
						}
						else if ((i == ChartEndIndex) | (i == HLCRange))
						{
							num17 = decimal.Add(num19, ChartPatterns[Index].dChannelHeight);
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(num19, 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(LimitDecimals(num17)) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
							}
							decimal num14 = ReportVolStop(i, num3, Index, 0);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 0);
							break;
						}
						goto end_IL_0177;
					}
					case 1:
					{
						CPInfo.BkoutDirection = "N/A";
						decimal num19 = decimal.Add(decimal.Multiply(num13, new decimal(i - ChartPatterns[Index].iMidDate)), nHLC[2, ChartPatterns[Index].iMidDate]);
						if (decimal.Compare(nHLC[2, i], num19) < 0)
						{
							if (!FindPatterns.CheckNearness(nHLC[2, i], num19, -1m, 0.1m))
							{
								CPInfo.BkoutDirection = "Down";
								CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
								CPInfo.iBkout = i;
								CPInfo.BkoutPrice = Conversions.ToString(LimitDecimals(num19));
								num17 = decimal.Subtract(num19, ChartPatterns[Index].dChannelHeight);
								ChartPatterns[Index].PriceTarget = num17;
								if (decimal.Compare(num19, 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(LimitDecimals(num17)) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
								}
								GetUltimateHighLow(i, -1, i, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
								decimal num14 = ReportVolStop(i, num3, Index, -1);
								CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
								break;
							}
						}
						else if ((i == ChartEndIndex) | (i == HLCRange))
						{
							num17 = decimal.Subtract(num19, ChartPatterns[Index].dChannelHeight);
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(num19, 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(LimitDecimals(num17)) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
							}
							decimal num14 = ReportVolStop(i, num3, Index, 0);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 0);
							break;
						}
						goto end_IL_0177;
					}
					case 58:
					{
						CPInfo.BkoutDirection = "N/A";
						decimal num19 = decimal.Add(decimal.Multiply(num12, new decimal(i - ChartPatterns[Index].iMidDate)), nHLC[1, ChartPatterns[Index].iMidDate]);
						bool flag2 = false;
						if (i == 0)
						{
							if (decimal.Compare(nHLC[3, i], num19) > 0)
							{
								flag2 = true;
							}
						}
						else if ((decimal.Compare(nHLC[3, i], num19) > 0) & (decimal.Compare(nHLC[3, i - 1], num19) > 0) & (decimal.Compare(nHLC[3, i], nHLC[3, i - 1]) > 0) & (decimal.Compare(nHLC[1, i], nHLC[1, i - 1]) > 0))
						{
							flag2 = true;
						}
						if (flag2)
						{
							if (!FindPatterns.CheckNearness(nHLC[1, i], num19, -1m, 0.1m))
							{
								CPInfo.BkoutDirection = "Up";
								CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
								CPInfo.iBkout = i;
								CPInfo.BkoutPrice = Conversions.ToString(LimitDecimals(num19));
								num17 = decimal.Add(num19, GetTLTarget(type, ReturnStart, i - 1, num12, ChartPatterns[Index].iMidDate));
								ChartPatterns[Index].PriceTarget = num17;
								if (decimal.Compare(num19, 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(LimitDecimals(num17)) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
								}
								GetUltimateHighLow(i, num2, i, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
								decimal num14 = ReportVolStop(i, num3, Index, 1);
								CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
								break;
							}
						}
						else if ((i == ChartEndIndex) | (i == HLCRange))
						{
							num17 = decimal.Add(num19, GetTLTarget(type, ReturnStart, i - 1, num12, ChartPatterns[Index].iMidDate));
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(num19, 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(LimitDecimals(num17)) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
							}
							decimal num14 = ReportVolStop(i, num3, Index, 0);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 0);
						}
						goto end_IL_0177;
					}
					case 57:
					{
						CPInfo.BkoutDirection = "N/A";
						decimal num19 = decimal.Add(decimal.Multiply(num13, new decimal(i - ChartPatterns[Index].iMidDate)), nHLC[2, ChartPatterns[Index].iMidDate]);
						bool flag = false;
						if (i == 0)
						{
							if (decimal.Compare(nHLC[3, i], num19) < 0)
							{
								flag = true;
							}
						}
						else if ((decimal.Compare(nHLC[3, i], num19) < 0) & (decimal.Compare(nHLC[3, i - 1], num19) < 0) & (decimal.Compare(nHLC[3, i], nHLC[3, i - 1]) < 0) & (decimal.Compare(nHLC[2, i], nHLC[2, i - 1]) < 0))
						{
							flag = true;
						}
						if (flag)
						{
							if (!FindPatterns.CheckNearness(nHLC[2, i], num19, -1m, 0.1m))
							{
								CPInfo.BkoutDirection = "Down";
								CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
								CPInfo.iBkout = i;
								CPInfo.BkoutPrice = Conversions.ToString(LimitDecimals(num19));
								num17 = decimal.Subtract(num19, GetTLTarget(type, ReturnStart, i - 1, num13, ChartPatterns[Index].iMidDate));
								ChartPatterns[Index].PriceTarget = num17;
								if (decimal.Compare(num19, 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(LimitDecimals(num17)) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
								}
								GetUltimateHighLow(i, num, i, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
								decimal num14 = ReportVolStop(i, num3, Index, -1);
								CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
								break;
							}
						}
						else if ((i == ChartEndIndex) | (i == HLCRange))
						{
							num17 = decimal.Subtract(num19, GetTLTarget(type, ReturnStart, i - 1, num13, ChartPatterns[Index].iMidDate));
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(num19, 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(LimitDecimals(num17)) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
							}
							decimal num14 = ReportVolStop(i, num3, Index, 0);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 0);
						}
						goto end_IL_0177;
					}
					case 3:
						num17 = ChartPatterns[Index].PriceTarget;
						CPInfo.Target = num17.ToString();
						CPInfo.BkoutDirection = "N/A";
						if (decimal.Compare(nHLC[3, i], nHLC[2, num2]) < 0)
						{
							CPInfo.BkoutDirection = "Down";
							decimal num14 = ReportVolStop(i, num3, Index, -1);
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num2]);
							GetUltimateHighLow(i, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
							break;
						}
						if (decimal.Compare(nHLC[1, i], nHLC[1, ReturnEnd]) > 0)
						{
							decimal num14 = new decimal(Convert.ToDouble(nHLC[1, ReturnEnd]) + 0.01);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
							break;
						}
						goto end_IL_0177;
					case 2:
						num17 = ChartPatterns[Index].PriceTarget;
						CPInfo.Target = num17.ToString();
						CPInfo.BkoutDirection = "N/A";
						if (decimal.Compare(nHLC[2, i], nHLC[2, ReturnEnd]) < 0)
						{
							decimal num14 = new decimal(Convert.ToDouble(nHLC[2, ReturnEnd]) - 0.01);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						if (decimal.Compare(nHLC[3, i], nHLC[1, num]) > 0)
						{
							CPInfo.BkoutDirection = "Up";
							decimal num14 = ReportVolStop(i, num3, Index, 1);
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num]);
							GetUltimateHighLow(i, num, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						goto end_IL_0177;
					case 74:
						CPInfo.Target = ChartPatterns[Index].PriceTarget.ToString();
						num17 = ChartPatterns[Index].PriceTarget;
						if (decimal.Compare(nHLC[2, i], num17) <= 0)
						{
							CPInfo.BkoutDirection = "Down";
							decimal num14 = ReportVolStop(i, num3, Index, -1);
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num2]);
							GetUltimateHighLow(i, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
							break;
						}
						if (decimal.Compare(nHLC[3, i], nHLC[1, num]) > 0)
						{
							CPInfo.BkoutDirection = "Up";
							decimal num14 = nHLC[1, num];
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num]);
							GetUltimateHighLow(i, num, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
							break;
						}
						CPInfo.BkoutDirection = "N/A";
						goto end_IL_0177;
					case 73:
						CPInfo.Target = ChartPatterns[Index].PriceTarget.ToString();
						num17 = ChartPatterns[Index].PriceTarget;
						if (decimal.Compare(nHLC[1, i], num17) >= 0)
						{
							CPInfo.BkoutDirection = "Up";
							decimal num14 = ReportVolStop(i, num3, Index, 1);
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num]);
							GetUltimateHighLow(i, num, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						if (decimal.Compare(nHLC[3, i], nHLC[2, num2]) < 0)
						{
							CPInfo.BkoutDirection = "Down";
							decimal num14 = nHLC[2, num2];
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num2]);
							GetUltimateHighLow(i, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						CPInfo.BkoutDirection = "N/A";
						goto end_IL_0177;
					case 4:
					case 5:
					{
						CPInfo.BkoutDirection = "N/A";
						CPInfo.Status = "See Chart. At target, expect a reversal.";
						CPInfo.Target = ChartPatterns[Index].PriceTarget.ToString();
						decimal num14 = ReportVolStop(i, num3, Index, Conversions.ToInteger(Interaction.IIf(type == 4, (object)(-1), (object)1)));
						if (((type == 4) & (decimal.Compare(num14, ChartPatterns[Index].PriceTarget) <= 0)) | ((type == 5) & (decimal.Compare(num14, ChartPatterns[Index].PriceTarget) >= 0)))
						{
							num14 = -1m;
							ChartPatterns[Index].StopPrice = -1m;
						}
						break;
					}
					case 6:
					case 7:
					case 8:
					case 9:
					case 10:
					case 11:
					case 28:
					case 29:
					{
						CPInfo.BkoutDirection = "N/A";
						CPInfo.Status = "See Chart";
						switch (type)
						{
						case 6:
						case 8:
						case 10:
						case 29:
							breakoutType = 1;
							break;
						case 7:
						case 9:
						case 11:
						case 28:
							breakoutType = -1;
							break;
						}
						CPInfo.Target = ChartPatterns[Index].PriceTarget.ToString();
						decimal num14 = ReportVolStop(i, num3, Index, breakoutType);
						break;
					}
					case 109:
					case 110:
					{
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						decimal num19;
						if (num7 != 0)
						{
							decimal d2 = nHLC[2, num2];
							if (num7 - num2 == 0)
							{
								break;
							}
							num13 = decimal.Divide(decimal.Subtract(nHLC[2, num7], nHLC[2, num2]), new decimal(num7 - num2));
							num19 = decimal.Add(decimal.Multiply(num13, new decimal(i - num2)), d2);
							if (type == 109)
							{
								num19 = nHLC[2, num7];
							}
							if (decimal.Compare(nHLC[3, i], num19) < 0)
							{
								CPInfo.BkoutDirection = "Down";
								CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
								CPInfo.iBkout = i;
								CPInfo.BkoutPrice = Conversions.ToString(LimitDecimals(num19));
								num17 = ((type != 110) ? LimitDecimals(decimal.Subtract(num19, decimal.Subtract(nHLC[1, num], nHLC[2, num7]))) : nHLC[2, num2]);
								if (decimal.Compare(num17, 0m) > 0)
								{
									ChartPatterns[Index].PriceTarget = num17;
									CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
								}
								else
								{
									num17 = default(decimal);
									CPInfo.Target = "?";
								}
								if (type == 110)
								{
									GetUltimateHighLow(i, num11, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
								}
								else
								{
									GetUltimateHighLow(i, num, num7, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
								}
								num14 = ReportVolStop(i, num3, Index, -1);
								CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
								break;
							}
						}
						if (num11 == 0)
						{
							continue;
						}
						decimal d = nHLC[1, num];
						if (num11 - num == 0)
						{
							break;
						}
						num12 = decimal.Divide(decimal.Subtract(nHLC[1, num11], nHLC[1, num]), new decimal(num11 - num));
						num19 = decimal.Add(decimal.Multiply(num12, new decimal(i - num)), d);
						if (type == 110)
						{
							num19 = nHLC[1, num11];
						}
						if (decimal.Compare(nHLC[3, i], num19) > 0)
						{
							CPInfo.BkoutDirection = "Up";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(LimitDecimals(num19));
							num17 = ((type != 109) ? LimitDecimals(decimal.Add(num19, decimal.Subtract(nHLC[1, num11], nHLC[2, num2]))) : nHLC[1, num]);
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(num19, 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
							}
							if (type == 110)
							{
								GetUltimateHighLow(i, num11, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							}
							else
							{
								GetUltimateHighLow(i, num, num7, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							}
							num14 = ReportVolStop(i, num3, Index, 1);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						continue;
					}
					case 100:
						CPInfo.BkoutDirection = "N/A ";
						if (i + 4 <= HLCRange)
						{
							int num24 = i;
							int num25 = i + 4;
							for (int m = num24; m <= num25; m++)
							{
								num2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(nHLC[2, m], nHLC[2, num2]) < 0, (object)m, (object)num2));
							}
							num17 = LimitDecimals(new decimal(Convert.ToDouble(nHLC[2, num2]) * 0.82));
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(nHLC[2, num2], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + "? or " + Strings.Format((object)decimal.Subtract(decimal.Divide(num17, nHLC[2, num2]), 1m), "0%");
							}
							GetUltimateHighLow(i, -1, -1, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, 0m, num17, -1);
							decimal num14 = ReportVolStop(i, num3, Index, -1);
						}
						break;
					case 12:
					{
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						if (decimal.Compare(nHLC[3, i], nHLC[2, num2]) < 0)
						{
							CPInfo.BkoutDirection = "Down";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num2]);
							num17 = LimitDecimals(decimal.Subtract(nHLC[2, num2], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
							if (decimal.Compare(num17, 0m) > 0)
							{
								ChartPatterns[Index].PriceTarget = num17;
								if (decimal.Compare(nHLC[2, num2], 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[2, num2]), nHLC[2, num2]), "0%");
								}
							}
							else
							{
								num17 = default(decimal);
								CPInfo.Target = "?";
							}
							num14 = ReportVolStop(i, num3, Index, -1);
							GetUltimateHighLow(i, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
							break;
						}
						CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num2]);
						num17 = LimitDecimals(decimal.Subtract(nHLC[2, num2], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
						if (decimal.Compare(num17, 0m) > 0)
						{
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(nHLC[2, num2], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[2, num2]), nHLC[2, num2]), "0%");
							}
						}
						else
						{
							num17 = default(decimal);
							CPInfo.Target = "?";
						}
						num14 = ReportVolStop(i, num3, Index, -1);
						goto end_IL_0177;
					}
					case 13:
					{
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						if (decimal.Compare(nHLC[3, i], nHLC[1, num]) > 0)
						{
							CPInfo.BkoutDirection = "Up";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num]);
							num17 = LimitDecimals(decimal.Add(nHLC[1, num], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(nHLC[1, num], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, num]), nHLC[1, num]), "0%");
							}
							num14 = ReportVolStop(i, num3, Index, 1);
							GetUltimateHighLow(i, num, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num]);
						num17 = LimitDecimals(decimal.Add(nHLC[1, num], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
						ChartPatterns[Index].PriceTarget = num17;
						if (decimal.Compare(nHLC[1, num], 0m) != 0)
						{
							CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, num]), nHLC[1, num]), "0%");
						}
						num14 = ReportVolStop(i, num3, Index, 1);
						goto end_IL_0177;
					}
					case 99:
					{
						CPInfo.BkoutDirection = "N/A ";
						GetUltimateHighLow(i, -1, -1, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
						ChartPatterns[Index].PriceTarget = default(decimal);
						decimal num14 = ReportVolStop(i, num3, Index, 1);
						break;
					}
					case 0:
					case 14:
					case 15:
					case 16:
					case 17:
					case 18:
					case 19:
					case 20:
					case 21:
					case 22:
					case 23:
					case 30:
					case 31:
					case 32:
					case 33:
					case 34:
					case 37:
					case 38:
					case 39:
					case 40:
					case 41:
					case 42:
					case 43:
					case 44:
					case 45:
					case 46:
					case 47:
					case 49:
					case 50:
					case 51:
					case 52:
					case 53:
					case 54:
					case 59:
					case 60:
					case 68:
					case 69:
					case 70:
					case 71:
					case 72:
					case 75:
					case 76:
					case 77:
					case 85:
					case 86:
					case 90:
					case 91:
					case 97:
					case 98:
					case 103:
					case 104:
					case 105:
					case 106:
					case 111:
					case 112:
					case 113:
					case 114:
					case 115:
					case 116:
					case 117:
					case 118:
					case 119:
					case 120:
					case 121:
					case 122:
					case 123:
					{
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						if (decimal.Compare(nHLC[3, i], nHLC[1, num]) > 0)
						{
							CPInfo.BkoutDirection = "Up";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num]);
							num17 = LimitDecimals(decimal.Add(nHLC[1, num], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(nHLC[1, num], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, num]), nHLC[1, num]), "0%");
							}
							num14 = ReportVolStop(i, num3, Index, 1);
							GetUltimateHighLow(i, num, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						unchecked
						{
							if (decimal.Compare(nHLC[3, i], nHLC[1, num]) <= 0 && (type == 115 || type == 20 || type == 21 || type == 18 || type == 19 || type == 98 || type == 106 || type == 104 || type == 37 || type == 90 || type == 86 || type == 34))
							{
								CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num]);
								num17 = LimitDecimals(decimal.Add(nHLC[1, num], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
								ChartPatterns[Index].PriceTarget = num17;
								if (decimal.Compare(nHLC[1, num], 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, num]), nHLC[1, num]), "0%");
								}
								num14 = ReportVolStop(i, num3, Index, 1);
							}
							if (decimal.Compare(nHLC[3, i], nHLC[2, num2]) < 0)
							{
								CPInfo.BkoutDirection = "Down";
								CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
								CPInfo.iBkout = i;
								CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num2]);
								num17 = LimitDecimals(decimal.Subtract(nHLC[2, num2], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
								if (decimal.Compare(num17, 0m) > 0)
								{
									ChartPatterns[Index].PriceTarget = num17;
									if (decimal.Compare(nHLC[2, num2], 0m) != 0)
									{
										CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[2, num2]), nHLC[2, num2]), "0%");
									}
								}
								else
								{
									num17 = default(decimal);
									CPInfo.Target = "?";
								}
								num14 = ReportVolStop(i, num3, Index, -1);
								GetUltimateHighLow(i, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
								CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
								break;
							}
							if (decimal.Compare(nHLC[3, i], nHLC[2, num2]) >= 0 && (type == 16 || type == 17 || type == 15 || type == 14 || type == 116 || type == 97 || type == 105 || type == 103 || type == 91 || type == 85 || type == 33))
							{
								CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num2]);
								num17 = LimitDecimals(decimal.Subtract(nHLC[2, num2], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
								if (decimal.Compare(num17, 0m) > 0)
								{
									ChartPatterns[Index].PriceTarget = num17;
									if (decimal.Compare(nHLC[2, num2], 0m) != 0)
									{
										CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[2, num2]), nHLC[2, num2]), "0%");
									}
								}
								else
								{
									num17 = default(decimal);
									CPInfo.Target = "?";
								}
								num14 = ReportVolStop(i, num3, Index, -1);
							}
							if (!(type == 117 || type == 118 || type == 119 || type == 121 || type == 120))
							{
								continue;
							}
							if (decimal.Compare(nHLC[3, i], nHLC[1, num]) <= 0)
							{
								CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num2]);
								num17 = LimitDecimals(decimal.Subtract(nHLC[2, num2], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
								if (decimal.Compare(num17, 0m) > 0)
								{
									ChartPatterns[Index].PriceTarget = num17;
									if (decimal.Compare(nHLC[2, num2], 0m) != 0)
									{
										CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[2, num2]), nHLC[2, num2]), "0%");
									}
								}
								else
								{
									num17 = default(decimal);
									CPInfo.Target = "?";
								}
								num14 = ReportVolStop(i, num3, Index, -1);
							}
							else
							{
								CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num]);
								num17 = LimitDecimals(decimal.Add(nHLC[1, num], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
								ChartPatterns[Index].PriceTarget = num17;
								if (decimal.Compare(nHLC[1, num], 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, num]), nHLC[1, num]), "0%");
								}
								num14 = ReportVolStop(i, num3, Index, 1);
							}
							goto end_IL_0177;
						}
					}
					case 95:
					{
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						if (decimal.Compare(nHLC[3, i], nHLC[1, num]) > 0)
						{
							CPInfo.BkoutDirection = "Up";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num]);
							num17 = LimitDecimals(decimal.Add(nHLC[1, num], decimal.Divide(decimal.Subtract(nHLC[1, num], nHLC[2, num2]), 2m)));
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(nHLC[1, num], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, num]), nHLC[1, num]), "0%");
							}
							num14 = ReportVolStop(i, num3, Index, 1);
							GetUltimateHighLow(i, num, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num]);
						num17 = LimitDecimals(decimal.Add(nHLC[1, num], decimal.Divide(decimal.Subtract(nHLC[1, num], nHLC[2, num2]), 2m)));
						ChartPatterns[Index].PriceTarget = num17;
						if (decimal.Compare(nHLC[1, num], 0m) != 0)
						{
							CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, num]), nHLC[1, num]), "0%");
						}
						num14 = ReportVolStop(i, num3, Index, 1);
						goto end_IL_0177;
					}
					case 93:
					case 94:
					{
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						if (num5 == 0)
						{
							continue;
						}
						if (decimal.Compare(nHLC[3, i], nHLC[1, num5]) > 0)
						{
							CPInfo.BkoutDirection = "Up";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num5]);
							num17 = decimal.Divide(decimal.Add(nHLC[1, num6], nHLC[1, num5]), 2m);
							num17 = LimitDecimals(decimal.Add(nHLC[1, num5], decimal.Subtract(num17, nHLC[2, num4])));
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(nHLC[1, num5], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, num5]), nHLC[1, num5]), "0%");
							}
							num14 = ReportVolStop(i, num3, Index, 1);
							GetUltimateHighLow(i, num, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num5]);
						num17 = decimal.Divide(decimal.Add(nHLC[1, num6], nHLC[1, num5]), 2m);
						num17 = LimitDecimals(decimal.Add(nHLC[1, num5], decimal.Subtract(num17, nHLC[2, num4])));
						ChartPatterns[Index].PriceTarget = num17;
						if (decimal.Compare(nHLC[1, num5], 0m) != 0)
						{
							CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, num5]), nHLC[1, num5]), "0%");
						}
						num14 = ReportVolStop(i, num3, Index, 1);
						goto end_IL_0177;
					}
					case 107:
					case 108:
					{
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						if (num5 == 0)
						{
							continue;
						}
						if (decimal.Compare(nHLC[3, i], nHLC[2, num5]) < 0)
						{
							CPInfo.BkoutDirection = "Down";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num5]);
							num17 = decimal.Divide(decimal.Add(nHLC[2, num6], nHLC[2, num5]), 2m);
							num17 = LimitDecimals(decimal.Subtract(nHLC[2, num5], decimal.Subtract(nHLC[1, num4], num17)));
							if (decimal.Compare(num17, 0m) > 0)
							{
								ChartPatterns[Index].PriceTarget = num17;
								if (decimal.Compare(nHLC[2, num5], 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[2, num5]), nHLC[2, num5]), "0%");
								}
							}
							else
							{
								num17 = default(decimal);
								CPInfo.Target = "?";
							}
							num14 = ReportVolStop(i, num3, Index, -1);
							GetUltimateHighLow(i, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
							break;
						}
						CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num5]);
						num17 = decimal.Divide(decimal.Add(nHLC[2, num6], nHLC[2, num5]), 2m);
						num17 = LimitDecimals(decimal.Subtract(nHLC[2, num5], decimal.Subtract(nHLC[1, num4], num17)));
						if (decimal.Compare(num17, 0m) > 0)
						{
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(nHLC[2, num5], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[2, num5]), nHLC[2, num5]), "0%");
							}
						}
						else
						{
							num17 = default(decimal);
							CPInfo.Target = "?";
						}
						num14 = ReportVolStop(i, num3, Index, -1);
						goto end_IL_0177;
					}
					case 67:
					case 78:
					{
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						if (decimal.Compare(nHLC[3, i], nHLC[1, num9]) > 0)
						{
							CPInfo.BkoutDirection = "Up";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, ReturnEnd]);
							if (decimal.Compare(decimal.Divide(decimal.Add(nHLC[1, ReturnStart], nHLC[2, ReturnStart]), 2m), decimal.Divide(decimal.Add(nHLC[1, num9], nHLC[2, num9]), 2m)) <= 0)
							{
								num17 = LimitDecimals(decimal.Add(nHLC[2, num10], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
								if (decimal.Compare(nHLC[2, num10], 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(nHLC[1, num], nHLC[2, num2]), nHLC[2, num10]), "0%");
								}
							}
							else
							{
								num17 = LimitDecimals(nHLC[1, num]);
								if (decimal.Compare(nHLC[2, num2], 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(nHLC[1, num], nHLC[2, num2]), nHLC[2, num2]), "0%");
								}
							}
							ChartPatterns[Index].PriceTarget = num17;
							num14 = ReportVolStop(i, num3, Index, 1);
							GetUltimateHighLow(i, num, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						if (decimal.Compare(nHLC[3, i], nHLC[2, num10]) >= 0)
						{
							continue;
						}
						CPInfo.BkoutDirection = "Down";
						CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
						CPInfo.iBkout = i;
						CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, ReturnEnd]);
						if (decimal.Compare(decimal.Divide(decimal.Add(nHLC[1, ReturnStart], nHLC[2, ReturnStart]), 2m), decimal.Divide(decimal.Add(nHLC[1, num9], nHLC[2, num9]), 2m)) <= 0)
						{
							num17 = LimitDecimals(nHLC[2, num2]);
							if (decimal.Compare(nHLC[1, num], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(nHLC[1, num], nHLC[2, num2]), nHLC[1, num]), "0%");
							}
						}
						else
						{
							num17 = LimitDecimals(decimal.Subtract(nHLC[1, num9], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
							if (decimal.Compare(num17, 0m) < 0)
							{
								num17 = default(decimal);
							}
							if (decimal.Compare(nHLC[1, num9], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(nHLC[1, num], nHLC[2, num2]), nHLC[1, num9]), "0%");
							}
						}
						ChartPatterns[Index].PriceTarget = num17;
						num14 = ReportVolStop(i, num3, Index, -1);
						GetUltimateHighLow(i, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
						CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
						break;
					}
					case 24:
					case 25:
					case 101:
					case 102:
					{
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						if ((decimal.Compare(nHLC[3, i], nHLC[1, num]) > 0) & (i > ChartPatterns[Index].iEndDate))
						{
							CPInfo.BkoutDirection = "Up";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num]);
							num17 = LimitDecimals(decimal.Add(nHLC[1, num], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(nHLC[1, num], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, num]), nHLC[1, num]), "0%");
							}
							num14 = ReportVolStop(i, num3, Index, 1);
							GetUltimateHighLow(i, num, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						if (decimal.Compare(nHLC[3, i], nHLC[2, num2]) >= 0)
						{
							continue;
						}
						CPInfo.BkoutDirection = "Down";
						CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
						CPInfo.iBkout = i;
						CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num2]);
						num17 = LimitDecimals(decimal.Subtract(nHLC[2, num2], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
						if (decimal.Compare(num17, 0m) > 0)
						{
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(nHLC[2, num2], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[2, num2]), nHLC[2, num2]), "0%");
							}
						}
						else
						{
							num17 = default(decimal);
							CPInfo.Target = "?";
						}
						num14 = ReportVolStop(i, num3, Index, -1);
						GetUltimateHighLow(i, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
						CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
						break;
					}
					case 89:
					{
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						if ((decimal.Compare(nHLC[3, i], nHLC[1, num]) > 0) & (i > ChartPatterns[Index].iEndDate))
						{
							CPInfo.BkoutDirection = "Up";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[1, num]);
							num17 = LimitDecimals(decimal.Add(nHLC[1, num], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
							ChartPatterns[Index].PriceTarget = num17;
							if (decimal.Compare(nHLC[1, num], 0m) != 0)
							{
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[1, num]), nHLC[1, num]), "0%");
							}
							num14 = ReportVolStop(i, num3, Index, 1);
							GetUltimateHighLow(i, num, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
							break;
						}
						if (num7 == 0)
						{
							continue;
						}
						decimal d2 = nHLC[2, num2];
						if (num7 - num2 == 0)
						{
							break;
						}
						num13 = decimal.Divide(decimal.Subtract(nHLC[2, num7], nHLC[2, num2]), new decimal(num7 - num2));
						decimal num19 = decimal.Add(decimal.Multiply(num13, new decimal(i - num2)), d2);
						if (decimal.Compare(nHLC[3, i], num19) < 0)
						{
							CPInfo.BkoutDirection = "Down";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(LimitDecimals(num19));
							num17 = LimitDecimals(decimal.Subtract(num19, decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
							if ((decimal.Compare(num17, 0m) > 0) & (decimal.Compare(num19, 0m) != 0))
							{
								ChartPatterns[Index].PriceTarget = num17;
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
							}
							else
							{
								num17 = default(decimal);
								CPInfo.Target = "?";
							}
							num14 = ReportVolStop(i, num3, Index, -1);
							GetUltimateHighLow(i, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
							break;
						}
						continue;
					}
					case 88:
					{
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						if (num11 != 0)
						{
							decimal d = nHLC[1, num];
							if (num11 - num == 0)
							{
								break;
							}
							num12 = decimal.Divide(decimal.Subtract(nHLC[1, num11], nHLC[1, num]), new decimal(num11 - num));
							decimal num19 = decimal.Add(decimal.Multiply(num12, new decimal(i - num)), d);
							if (decimal.Compare(nHLC[3, i], num19) > 0)
							{
								CPInfo.BkoutDirection = "Up";
								CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
								CPInfo.iBkout = i;
								CPInfo.BkoutPrice = Conversions.ToString(LimitDecimals(num19));
								num17 = LimitDecimals(decimal.Add(num19, decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
								ChartPatterns[Index].PriceTarget = num17;
								if (decimal.Compare(num19, 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
								}
								num14 = ReportVolStop(i, num3, Index, 1);
								GetUltimateHighLow(i, num, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
								CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
								break;
							}
						}
						if (decimal.Compare(nHLC[3, i], nHLC[2, num2]) < 0)
						{
							CPInfo.BkoutDirection = "Down";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(nHLC[2, num2]);
							num17 = LimitDecimals(decimal.Subtract(nHLC[2, num2], decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
							if ((decimal.Compare(num17, 0m) > 0) & (decimal.Compare(nHLC[2, num2], 0m) != 0))
							{
								ChartPatterns[Index].PriceTarget = num17;
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, nHLC[2, num2]), nHLC[2, num2]), "0%");
							}
							else
							{
								num17 = default(decimal);
								CPInfo.Target = "?";
							}
							num14 = ReportVolStop(i, num3, Index, -1);
							GetUltimateHighLow(i, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
							break;
						}
						goto end_IL_0177;
					}
					case 87:
					case 92:
					case 96:
					{
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						decimal num19;
						if (num11 != 0)
						{
							decimal d = nHLC[1, num];
							if (num11 - num == 0)
							{
								break;
							}
							num12 = decimal.Divide(decimal.Subtract(nHLC[1, num11], nHLC[1, num]), new decimal(num11 - num));
							num19 = decimal.Add(decimal.Multiply(num12, new decimal(i - num)), d);
							if (decimal.Compare(nHLC[3, i], num19) > 0)
							{
								CPInfo.BkoutDirection = "Up";
								CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
								CPInfo.iBkout = i;
								CPInfo.BkoutPrice = Conversions.ToString(LimitDecimals(num19));
								if (decimal.Compare(num19, 0m) != 0)
								{
									if (type == 96)
									{
										num17 = nHLC[1, num];
										CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
									}
									else
									{
										num17 = LimitDecimals(decimal.Add(num19, decimal.Subtract(nHLC[1, num], nHLC[2, num2])));
										CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
									}
									ChartPatterns[Index].PriceTarget = num17;
								}
								num14 = ReportVolStop(i, num3, Index, 1);
								GetUltimateHighLow(i, num, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
								CPInfo.Status = CheckTradeStatus(i, num14, num17, 1);
								break;
							}
						}
						if (num7 == 0)
						{
							continue;
						}
						decimal d2 = nHLC[2, num2];
						if (num7 - num2 == 0)
						{
							break;
						}
						num13 = decimal.Divide(decimal.Subtract(nHLC[2, num7], nHLC[2, num2]), new decimal(num7 - num2));
						num19 = decimal.Add(decimal.Multiply(num13, new decimal(i - num2)), d2);
						if (decimal.Compare(nHLC[3, i], num19) < 0)
						{
							CPInfo.BkoutDirection = "Down";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, i], UserDate);
							CPInfo.iBkout = i;
							CPInfo.BkoutPrice = Conversions.ToString(LimitDecimals(num19));
							num17 = ((type != 92) ? LimitDecimals(decimal.Subtract(num19, decimal.Subtract(nHLC[1, num], nHLC[2, num2]))) : nHLC[2, num2]);
							if ((decimal.Compare(num17, 0m) > 0) & (decimal.Compare(num19, 0m) != 0))
							{
								ChartPatterns[Index].PriceTarget = num17;
								CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num19), num19), "0%");
							}
							else
							{
								num17 = default(decimal);
								CPInfo.Target = "?";
							}
							num14 = ReportVolStop(i, num3, Index, -1);
							GetUltimateHighLow(i, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(i, num14, num17, -1);
							break;
						}
						continue;
					}
					case 56:
					{
						decimal num15 = decimal.Add(nHLC[2, num2], decimal.Multiply(decimal.Subtract(nHLC[1, ReturnStart], nHLC[2, num2]), 0.382m));
						int num18 = ChartPatterns[Index].iMidDate + 1;
						int hLCRange3 = HLCRange;
						for (int k = num18; k <= hLCRange3; k++)
						{
							if (decimal.Compare(nHLC[3, k], num15) >= 0)
							{
								decimal num14 = ReportVolStop(k, num3, Index, 0);
								CPInfo.BkoutDirection = "Up";
								CPInfo.BkoutDate = Strings.Format((object)nDT[0, k], UserDate);
								CPInfo.iBkout = k;
								CPInfo.BkoutPrice = Conversions.ToString(Interaction.IIf(decimal.Compare(nHLC[0, k], num15) > 0, (object)nHLC[0, k], (object)num15));
								num17 = nHLC[1, ReturnStart];
								ChartPatterns[Index].PriceTarget = num17;
								if (decimal.Compare(num15, 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num15), num15), "0%");
								}
								num14 = ReportVolStop(k, num3, Index, 1);
								GetUltimateHighLow(k, num, num2, 1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
								CPInfo.Status = CheckTradeStatus(k, num14, num17, 1);
								break;
							}
						}
						break;
					}
					case 55:
					{
						decimal num15 = decimal.Subtract(nHLC[1, num], decimal.Multiply(decimal.Subtract(nHLC[1, num], nHLC[2, ReturnStart]), 0.382m));
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						int num16 = ChartPatterns[Index].iMidDate + 1;
						int hLCRange2 = HLCRange;
						for (int j = num16; j <= hLCRange2; j++)
						{
							if (decimal.Compare(nHLC[3, j], num15) > 0)
							{
								continue;
							}
							CPInfo.BkoutDirection = "Down";
							CPInfo.BkoutDate = Strings.Format((object)nDT[0, j], UserDate);
							CPInfo.iBkout = j;
							CPInfo.BkoutPrice = Conversions.ToString(Interaction.IIf(decimal.Compare(nHLC[0, j], num15) < 0, (object)nHLC[0, j], (object)num15));
							num17 = nHLC[2, ReturnStart];
							if (decimal.Compare(num17, 0m) > 0)
							{
								ChartPatterns[Index].PriceTarget = num17;
								if (decimal.Compare(num15, 0m) != 0)
								{
									CPInfo.Target = Conversions.ToString(num17) + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num17, num15), num15), "0%");
								}
							}
							else
							{
								num17 = default(decimal);
								CPInfo.Target = "?";
							}
							num14 = ReportVolStop(j, num3, Index, -1);
							GetUltimateHighLow(j, num, num2, -1, ref CPInfo.UltHLDate, ref CPInfo.UltHLPrice, Index);
							CPInfo.Status = CheckTradeStatus(j, num14, num17, -1);
							break;
						}
						break;
					}
					case 26:
					case 27:
					{
						CPInfo.BkoutDirection = "N/A ";
						CPInfo.Status = "See Chart";
						decimal num14 = ReportVolStop(i, num3, Index, 0);
						break;
					}
					}
					break;
					end_IL_0177:;
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					Debugger.Break();
					ProjectData.ClearProjectError();
				}
			}
			ChartPatterns[Index].dBreakoutPrice = new decimal(Conversion.Val(CPInfo.BkoutPrice));
			if (decimal.Compare(ChartPatterns[Index].PriceTarget, 0m) < 0)
			{
				ChartPatterns[Index].PriceTarget = default(decimal);
			}
			try
			{
				if (Conversion.Val(CPInfo.Target) < 0.0)
				{
					CPInfo.Target = "0";
				}
			}
			catch (Exception ex3)
			{
				ProjectData.SetProjectError(ex3);
				Exception ex4 = ex3;
				ProjectData.ClearProjectError();
			}
			if (IntradayData)
			{
				CPInfo.AvgVolume = Get3MoAvgVolume(MyCDate(RuntimeHelpers.GetObjectValue(Interaction.IIf(CPInfo.BkoutDate != null, (object)CPInfo.BkoutDate, (object)nDT[0, HLCRange]))));
			}
			else
			{
				CPInfo.AvgVolume = Get3MoAvgVolume(MyCDate(RuntimeHelpers.GetObjectValue(Interaction.IIf(CPInfo.BkoutDate != null, (object)CPInfo.BkoutDate, (object)nDT[0, HLCRange].Date))));
			}
		}
	}

	public static string Get3MoAvgVolume(DateTime StartDate)
	{
		decimal d = default(decimal);
		int num = 0;
		checked
		{
			long num2 = default(long);
			DateTime dateTime = default(DateTime);
			if (IntradayData)
			{
				num2 = -1L;
				for (int i = HLCRange; i >= 0; i += -1)
				{
					if (DateTime.Compare(nDT[0, i], StartDate) <= 0)
					{
						num2 = (long)Math.Round((double)i - 65.5);
						break;
					}
				}
				if (num2 < 0)
				{
					num2 = 0L;
				}
			}
			else
			{
				dateTime = DateAndTime.DateAdd((DateInterval)4, -91.25, StartDate);
			}
			for (int j = HLCRange; j >= 0; j += -1)
			{
				if (IntradayData)
				{
					if (unchecked(DateTime.Compare(nDT[0, j], StartDate) <= 0 && j >= num2))
					{
						d = decimal.Add(d, nHLC[4, j]);
						num++;
					}
					if (j <= num2)
					{
						break;
					}
				}
				else
				{
					if ((DateTime.Compare(nDT[0, j].Date, StartDate.Date) <= 0) & (DateTime.Compare(nDT[0, j].Date, dateTime.Date) >= 0))
					{
						d = decimal.Add(d, nHLC[4, j]);
						num++;
					}
					if (DateTime.Compare(nDT[0, j].Date, dateTime.Date) <= 0)
					{
						break;
					}
				}
			}
			object obj = 0;
			if (num != 0)
			{
				obj = decimal.Divide(d, new decimal(num));
			}
			return Strings.Format(RuntimeHelpers.GetObjectValue(obj), "#,##0");
		}
	}

	public static int GetOptions(Form ctrl)
	{
		//IL_0014: Unknown result type (might be due to invalid IL or missing references)
		//IL_001a: Expected O, but got Unknown
		//IL_0023: Unknown result type (might be due to invalid IL or missing references)
		//IL_002e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0047: Unknown result type (might be due to invalid IL or missing references)
		foreach (Control control in ((Control)ctrl).Controls)
		{
			Control val = control;
			if (val is RadioButton && (((RadioButton)val).Checked & (Conversions.ToInteger(((Control)(RadioButton)val).Tag) != -1)))
			{
				return Conversions.ToInteger(((Control)(RadioButton)val).Tag);
			}
		}
		return -1;
	}

	private static DateTime GetNthDayOfNthWeek(DateTime dt, int DayofWeek, int WhichWeek)
	{
		DateTime dateTime = DateAndTime.DateSerial(dt.Year, dt.Month, 1);
		DateTime dateTime2 = checked(dateTime.AddDays((double)(6 - dateTime.AddDays(-(DayofWeek + 1)).DayOfWeek)).AddDays((WhichWeek - 1) * 7));
		if (DateTime.Compare(dateTime2, dateTime.AddMonths(1)) >= 0)
		{
			dateTime2 = dateTime2.AddDays(-7.0);
		}
		return dateTime2;
	}

	public static string GetPatternPhrase(int Index)
	{
		string result = "";
		switch (ChartPatterns[Index].Type)
		{
		case 116:
			result = "Big M (BigM)";
			break;
		case 115:
			result = "Big W (BigW)";
			break;
		case 4:
			result = "AB=CD, bearish (ABCD Be)";
			break;
		case 5:
			result = "AB=CD, bullish (ABCD Bu)";
			break;
		case 84:
			result = "Bump-and-run reversal bottom (BARRB)";
			break;
		case 83:
			result = "Bump-and-run reversal top (BARRT)";
			break;
		case 11:
			result = "Bat, bearish, (Bat Be)";
			break;
		case 10:
			result = "Bat, bullish, (Bat Bu)";
			break;
		case 114:
			result = "Broadening bottom (BB)";
			break;
		case 111:
			result = "Broadening top (BT)";
			break;
		case 113:
			result = "Right-angled broadening fmtn, ascend (RABFA)";
			break;
		case 112:
			result = "Right-angled broadening fmtn, descend (RABFD)";
			break;
		case 110:
			result = "Broadening wedge, ascending (BWA)";
			break;
		case 109:
			result = "Broadening wedge, descending (BWD)";
			break;
		case 9:
			result = "Butterfly, bearish (Butt Be)";
			break;
		case 8:
			result = "Butterfly, bullish (Butt Bu)";
			break;
		case 3:
			result = "Carl V, Bearish (Carl Be)";
			break;
		case 2:
			result = "Carl V, bullish (Carl Bu)";
			break;
		case 82:
			result = "Channel, down";
			break;
		case 1:
			result = "Channel, up";
			break;
		case 7:
			result = "Crab, bearish (Crab Be)";
			break;
		case 6:
			result = "Crab, bullish (Crab Bu)";
			break;
		case 52:
			result = "Closing price reversal, downtrend (c)";
			break;
		case 51:
			result = "Closing price reversal, uptrend (C)";
			break;
		case 81:
			result = "Cup with handle";
			break;
		case 48:
			result = "Cup with handle, inverted";
			break;
		case 100:
			result = "Dead cat bounce (DCB, % drop)";
			break;
		case 30:
			result = "Diving board";
			break;
		case 99:
			result = "Inverted dead cat bounce (iDCB, % rise)";
			break;
		case 98:
			result = "Double bottom (DB)";
			break;
		case 20:
			result = "Double bottom, Adam & Adam (AADB)";
			break;
		case 21:
			result = "Double bottom, Adam & Eve (AEDB)";
			break;
		case 18:
			result = "Double bottom, Eve & Adam (EADB)";
			break;
		case 19:
			result = "Double bottom, Eve & Eve (EEDB)";
			break;
		case 97:
			result = "Double top (DT)";
			break;
		case 16:
			result = "Double Top, Adam & Adam (AADT)";
			break;
		case 17:
			result = "Double Top, Adam & Eve (AEDT)";
			break;
		case 14:
			result = "Double Top, Eve & Adam (EADT)";
			break;
		case 15:
			result = "Double Top, Eve & Eve (EEDT)";
			break;
		case 78:
			result = "Flag";
			break;
		case 12:
			result = "Fakey, bearish (FakeBe)";
			break;
		case 13:
			result = "Fakey, bullish (FakeBu)";
			break;
		case 96:
			result = "Falling wedge (FW)";
			break;
		case 122:
			result = "Gap 2H (2H)";
			break;
		case 123:
			result = "Gap 2H, inverted (2Hi)";
			break;
		case 117:
			result = "Gap, breakaway (Gb)";
			break;
		case 118:
			result = "Gap, area or common (Ga)";
			break;
		case 119:
			result = "Gap, continuation (Gc)";
			break;
		case 121:
			result = "Gap, exhaustion (Ge)";
			break;
		case 120:
			result = "Gap, type unknown (G?)";
			break;
		case 28:
			result = "Gartley, bearish (Gar Be)";
			break;
		case 29:
			result = "Gartley, bullish (Gar Bu)";
			break;
		case 95:
			result = "High & tight flag (HTF)";
			break;
		case 94:
			result = "Head-and-shoulders bottom (HSB)";
			break;
		case 93:
			result = "Complex head-and-shoulders bottom (cHSB)";
			break;
		case 108:
			result = "Complex head-and-shoulders top (cHST)";
			break;
		case 107:
			result = "Head-and-shoulders top (HST)";
			break;
		case 50:
			result = "Hook reversal, downtrend (HD)";
			break;
		case 49:
			result = "Hook reversal, uptrend (HU)";
			break;
		case 106:
			result = "Horn bottom (HB)";
			break;
		case 105:
			result = "Horn top (HT)";
			break;
		case 77:
			result = "Inside day (ID)";
			break;
		case 76:
			result = "Island reversal, bottom (IRB)";
			break;
		case 75:
			result = "Island reversal, top (IRT)";
			break;
		case 47:
			result = "Key reversal, downtrend (KD)";
			break;
		case 46:
			result = "Key reversal, uptrend (KU)";
			break;
		case 74:
			result = "Measured move down (MMD)";
			break;
		case 73:
			result = "Measured move up (MMU)";
			break;
		case 72:
			result = "Narrow range 4 (NR4)";
			break;
		case 71:
			result = "Narrow range 7 (NR7)";
			break;
		case 45:
			result = "Open-close reversal, downtrend (o)";
			break;
		case 44:
			result = "Open-close reversal, uptrend (O)";
			break;
		case 70:
			result = "One day reversal, bottom (r)";
			break;
		case 69:
			result = "One day reversal, top (R)";
			break;
		case 68:
			result = "Outside day (OD)";
			break;
		case 67:
			result = "Pennant (PEN)";
			break;
		case 104:
			result = "Pipe bottom (PB)";
			break;
		case 103:
			result = "Pipe top (PT)";
			break;
		case 43:
			result = "Pivot point reversal, downtrend (p)";
			break;
		case 42:
			result = "Pivot point reversal, uptrend (P)";
			break;
		case 37:
			result = "Pothole";
			break;
		case 102:
			result = "Rectangle bottom (RB)";
			break;
		case 101:
			result = "Rectangle top (RT)";
			break;
		case 92:
			result = "Rising wedge (RW)";
			break;
		case 36:
			result = "Roof (Ro)";
			break;
		case 35:
			result = "Roof, inverted (iR)";
			break;
		case 66:
			result = "Rounding bottom (RoundB)";
			break;
		case 65:
			result = "Rounding top (RoundT)";
			break;
		case 60:
			result = "Shark-32 (S32)";
			break;
		case 40:
			result = "Spike down (s)";
			break;
		case 41:
			result = "Spike up (S)";
			break;
		case 59:
			result = "Three bar (3Bar)";
			break;
		case 91:
			result = "Three falling peaks (3FP)";
			break;
		case 32:
			result = "Three LR (3L-R)";
			break;
		case 31:
			result = "Three LR, inverted (i3LR)";
			break;
		case 90:
			result = "Three rising valleys (3RV)";
			break;
		case 58:
			result = "Trendline, down";
			break;
		case 57:
			result = "Trendline, up";
			break;
		case 89:
			result = "Ascending triangle (AscT)";
			break;
		case 88:
			result = "Descending triangle (DesT)";
			break;
		case 87:
			result = "Symmetrical triangle (SymT)";
			break;
		case 86:
			result = "Triple bottom (B)";
			break;
		case 85:
			result = "Triple top (T)";
			break;
		case 0:
			result = "2-Dance (2D)";
			break;
		case 23:
			result = "2-Did (2Did)";
			break;
		case 22:
			result = "2-Tall (2T)";
			break;
		case 34:
			result = "Ugly double bottom (UDB)";
			break;
		case 33:
			result = "Ugly double top (UDT)";
			break;
		case 24:
			result = "Vertical run down (VRD)";
			break;
		case 25:
			result = "Vertical run up (VRU)";
			break;
		case 55:
			result = "V-top";
			break;
		case 56:
			result = "V-bottom";
			break;
		case 53:
			result = "Weekly reversal top";
			break;
		case 54:
			result = "Weekly reversal bottom";
			break;
		case 38:
			result = "Wide ranging day, upside reversal (W)";
			break;
		case 39:
			result = "Wide ranging day, downside reversal (w)";
			break;
		case 27:
			result = "Wolfe wave, bearish (WW Be)";
			break;
		case 26:
			result = "Wolfe wave, bullish (WW Bu)";
			break;
		}
		return result;
	}

	public static void GetStartEndDates(int Index, ref int ReturnStart, ref int ReturnEnd)
	{
		ReturnStart = ChartPatterns[Index].iStartDate;
		ReturnStart = Conversions.ToInteger(Interaction.IIf((ChartPatterns[Index].iStart2Date != 0) & (ChartPatterns[Index].iStart2Date < ReturnStart), (object)ChartPatterns[Index].iStart2Date, (object)ReturnStart));
		ReturnEnd = ChartPatterns[Index].iEndDate;
		ReturnEnd = Conversions.ToInteger(Interaction.IIf((ChartPatterns[Index].iEnd2Date != 0) & (ChartPatterns[Index].iEnd2Date > ReturnEnd), (object)ChartPatterns[Index].iEnd2Date, (object)ReturnEnd));
	}

	private static decimal GetTLTarget(int iType, int iStart, int iEnd, decimal Slope, int iTLEnd)
	{
		checked
		{
			int num = (int)Math.Round((double)iEnd - (double)(iEnd - iStart) / 2.0);
			decimal d;
			if (iType == 58)
			{
				int num2 = num;
				d = nHLC[1, num];
				for (int i = num; i <= iEnd; i++)
				{
					decimal num3 = decimal.Add(decimal.Multiply(Slope, new decimal(i - iTLEnd)), nHLC[1, iTLEnd]);
					if (decimal.Compare(decimal.Subtract(num3, nHLC[2, i]), decimal.Subtract(d, nHLC[2, num2])) > 0)
					{
						num2 = i;
						d = num3;
					}
				}
				return decimal.Subtract(decimal.Add(decimal.Multiply(Slope, new decimal(num2 - iTLEnd)), nHLC[1, iTLEnd]), nHLC[2, num2]);
			}
			int num4 = num;
			d = nHLC[2, num];
			for (int i = num; i <= iEnd; i++)
			{
				decimal num3 = decimal.Add(decimal.Multiply(Slope, new decimal(i - iTLEnd)), nHLC[2, iTLEnd]);
				if (decimal.Compare(decimal.Subtract(nHLC[1, i], num3), decimal.Subtract(nHLC[1, num4], d)) > 0)
				{
					num4 = i;
					d = num3;
				}
			}
			return decimal.Subtract(nHLC[1, num4], decimal.Add(decimal.Multiply(Slope, new decimal(num4 - iTLEnd)), nHLC[2, iTLEnd]));
		}
	}

	private static void GetUltimateHighLow(int iBkout, int iTop, int iBottom, int BkoutDirection, ref string HLDate, ref string HLPrice, int CPIndex)
	{
		int num = iBkout;
		int num2 = iBkout;
		int hLCRange = HLCRange;
		for (int i = iBkout; i <= hLCRange; i = checked(i + 1))
		{
			if (BkoutDirection == 1)
			{
				num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(nHLC[1, i], nHLC[1, num]) > 0, (object)i, (object)num));
				if (Convert.ToDouble(nHLC[2, i]) < Convert.ToDouble(nHLC[1, num]) * 0.8)
				{
					HLDate = Strings.Format((object)nDT[0, num], UserDate);
					HLPrice = Conversions.ToString(nHLC[1, num]);
					ChartPatterns[CPIndex].UltHLPrice = LimitDecimals(nHLC[1, num]);
					ChartPatterns[CPIndex].UltHLDate = HLDate;
					ChartPatterns[CPIndex].UltHiLow = true;
					break;
				}
				if (iBottom != -1 && decimal.Compare(nHLC[3, i], nHLC[2, iBottom]) < 0)
				{
					HLDate = Strings.Format((object)nDT[0, num], UserDate);
					HLPrice = Conversions.ToString(nHLC[1, num]);
					ChartPatterns[CPIndex].UltHLPrice = LimitDecimals(nHLC[1, num]);
					ChartPatterns[CPIndex].UltHLDate = HLDate;
					ChartPatterns[CPIndex].UltHiLow = true;
					break;
				}
			}
			else
			{
				num2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(nHLC[2, i], nHLC[2, num2]) < 0, (object)i, (object)num2));
				if (Convert.ToDouble(nHLC[1, i]) > Convert.ToDouble(nHLC[2, num2]) * 1.2)
				{
					HLDate = Strings.Format((object)nDT[0, num2], UserDate);
					HLPrice = Conversions.ToString(nHLC[2, num2]);
					ChartPatterns[CPIndex].UltHLPrice = LimitDecimals(nHLC[2, num2]);
					ChartPatterns[CPIndex].UltHLDate = HLDate;
					ChartPatterns[CPIndex].UltHiLow = false;
					break;
				}
				if (iTop != -1 && decimal.Compare(nHLC[3, i], nHLC[1, iTop]) > 0)
				{
					HLDate = Strings.Format((object)nDT[0, num2], UserDate);
					HLPrice = Conversions.ToString(nHLC[2, num2]);
					ChartPatterns[CPIndex].UltHLPrice = LimitDecimals(nHLC[2, num2]);
					ChartPatterns[CPIndex].UltHLDate = HLDate;
					ChartPatterns[CPIndex].UltHiLow = false;
					break;
				}
			}
		}
	}

	public static bool IsDate(object Phrase)
	{
		bool result;
		try
		{
			string text = Phrase.ToString();
			result = DateTime.TryParseExact(Strings.Trim(text), UserDate, CultureInfo.InvariantCulture, DateTimeStyles.None, out var result2) || DateTime.TryParseExact(Strings.Trim(text), UserDate, CultureInfo.CurrentCulture, DateTimeStyles.None, out result2) || (DateTime.TryParse(Strings.Trim(text), out result2) ? true : false);
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			result = false;
			ProjectData.ClearProjectError();
		}
		return result;
	}

	public static decimal LimitDecimals(decimal OriginalNumber)
	{
		return new decimal(Math.Round(Convert.ToDouble(OriginalNumber), DecimalsUsed));
	}

	public static string LimitDecimals(string OriginalNumber)
	{
		string result;
		if (Operators.CompareString(OriginalNumber, "null", false) == 0)
		{
			result = "0";
		}
		else
		{
			try
			{
				if (!Versioned.IsNumeric((object)Conversions.ToDecimal(OriginalNumber)))
				{
					result = "0";
					goto IL_0058;
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				result = "0";
				ProjectData.ClearProjectError();
				goto IL_0058;
			}
			result = Conversions.ToString(LimitDecimals(Conversions.ToDecimal(OriginalNumber)));
		}
		goto IL_0058;
		IL_0058:
		return result;
	}

	public static bool ListBoxHandler(KeyEventArgs e, ListBox Control, bool ColonChange)
	{
		//IL_009d: Unknown result type (might be due to invalid IL or missing references)
		//IL_019b: Unknown result type (might be due to invalid IL or missing references)
		//IL_000f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0016: Invalid comparison between Unknown and I4
		//IL_00b2: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b9: Invalid comparison between Unknown and I4
		//IL_0043: Unknown result type (might be due to invalid IL or missing references)
		//IL_0049: Invalid comparison between Unknown and I4
		//IL_00f7: Unknown result type (might be due to invalid IL or missing references)
		//IL_00fd: Invalid comparison between Unknown and I4
		int selectedIndex = Control.SelectedIndex;
		if (selectedIndex != -1)
		{
			if ((int)e.KeyCode == 46)
			{
				if ((int)MessageBox.Show("Are you sure you want to delete the file " + Control.SelectedItems[0].ToString() + "?", "Patternz", (MessageBoxButtons)4, (MessageBoxIcon)32) == 6)
				{
					try
					{
						File.Delete(OpenPath + "\\" + Control.SelectedItems[0].ToString());
						Control.Items.RemoveAt(selectedIndex);
					}
					catch (Exception ex)
					{
						ProjectData.SetProjectError(ex);
						Exception ex2 = ex;
						MessageBox.Show("The delete failed. Go figure..." + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
						ProjectData.ClearProjectError();
					}
				}
				return true;
			}
			if ((int)e.KeyCode == 113)
			{
				RenameSymbolString = Control.SelectedItems[0].ToString();
				RenameSymbolString = RenameSymbolString.Replace(": ", "_");
				if ((int)((Form)MyProject.Forms.RenameDialog).ShowDialog() == 1)
				{
					try
					{
						string text = Control.SelectedItems[0].ToString();
						text = text.Replace(":", "_");
						((ServerComputer)MyProject.Computer).FileSystem.RenameFile(OpenPath + "\\" + text, RenameSymbolString);
						Control.Items.RemoveAt(selectedIndex);
						if (ColonChange)
						{
							RenameSymbolString = RenameSymbolString.Replace("_", ":");
						}
						Control.Items.Add((object)RenameSymbolString);
					}
					catch (Exception ex3)
					{
						ProjectData.SetProjectError(ex3);
						Exception ex4 = ex3;
						MessageBox.Show(ex4.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
						ProjectData.ClearProjectError();
					}
				}
				return true;
			}
		}
		return false;
	}

	public static bool LoadFile(string FileName, ref ProgressBar ProgBar, ref Label ErrorLabel, bool QuickExit, int DisplayPeriod)
	{
		//IL_008a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0130: Unknown result type (might be due to invalid IL or missing references)
		//IL_0180: Unknown result type (might be due to invalid IL or missing references)
		//IL_0049: Unknown result type (might be due to invalid IL or missing references)
		string text = OpenPath + "\\" + FileName;
		long fileSize = 0L;
		bool result;
		if (File.Exists(text))
		{
			try
			{
				StreamReader streamReader = new StreamReader(text);
				try
				{
					if (streamReader.Peek() != -1)
					{
						goto end_IL_0026;
					}
					if (!HideMessages)
					{
						MessageBox.Show(text + " appears to be zero length.", "Global: LoadFile", (MessageBoxButtons)0, (MessageBoxIcon)16);
					}
					streamReader.Close();
					streamReader.Dispose();
					result = true;
					goto end_IL_001f;
					end_IL_0026:;
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					string text2 = "Error reading file " + text;
					if (!HideMessages)
					{
						MessageBox.Show(text2, "Global: LoadFile", (MessageBoxButtons)0, (MessageBoxIcon)16);
					}
					streamReader.Close();
					streamReader.Dispose();
					result = true;
					ProjectData.ClearProjectError();
					goto end_IL_001f;
				}
				if (ProgBar != null)
				{
					try
					{
						fileSize = ((ServerComputer)MyProject.Computer).FileSystem.GetFileInfo(text).Length;
					}
					catch (Exception ex3)
					{
						ProjectData.SetProjectError(ex3);
						Exception ex4 = ex3;
						fileSize = 0L;
						ProjectData.ClearProjectError();
					}
				}
				if (!ReadStock(streamReader, fileSize, ref ProgBar, ref ErrorLabel, QuickExit, DisplayPeriod, FileName))
				{
					streamReader.Close();
					streamReader.Dispose();
					goto IL_018a;
				}
				streamReader.Close();
				streamReader.Dispose();
				result = true;
				end_IL_001f:;
			}
			catch (Exception ex5)
			{
				ProjectData.SetProjectError(ex5);
				Exception ex6 = ex5;
				if (!HideMessages)
				{
					MessageBox.Show("This file (" + text + ") appears to already be opened (perhaps by another user or process.)", "Global: LoadFile", (MessageBoxButtons)0, (MessageBoxIcon)16);
				}
				result = true;
				ProjectData.ClearProjectError();
			}
		}
		else
		{
			string text3 = "Can't find " + text;
			if (ErrorLabel != null)
			{
				ErrorLabel.Text = text3;
			}
			ErrorMessage = ErrorMessage + text3 + "\r\n";
			if (!HideMessages)
			{
				MessageBox.Show(text3, "Global: LoadFile", (MessageBoxButtons)0, (MessageBoxIcon)16);
			}
			result = true;
		}
		goto IL_018c;
		IL_018c:
		return result;
		IL_018a:
		result = false;
		goto IL_018c;
	}

	public static DateTime MyCDate(object Phrase)
	{
		DateTime result;
		try
		{
			result = Conversions.ToDate(Phrase);
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			result = DateTime.ParseExact(Phrase.ToString(), UserDate, CultureInfo.InvariantCulture);
			ProjectData.ClearProjectError();
		}
		return result;
	}

	private static int DecimalCount(string Match, int iMaxDecimals)
	{
		int num = Strings.InStr(1, Match, ".", (CompareMethod)0);
		if (num > 0)
		{
			int num2 = checked(Match.Length - num);
			if (num2 > 15)
			{
				num2 = 15;
			}
			return Conversions.ToInteger(Interaction.IIf(num2 > iMaxDecimals, (object)num2, (object)iMaxDecimals));
		}
		return iMaxDecimals;
	}

	public static void ReadFilterConfigFile(object sender, EventArgs e)
	{
		//IL_0073: Unknown result type (might be due to invalid IL or missing references)
		BinaryFormatter binaryFormatter = new BinaryFormatter();
		if (File.Exists(ConfigLocation + FilterConfigName))
		{
			try
			{
				Stream stream = File.OpenRead(ConfigLocation + FilterConfigName);
				object obj = binaryFormatter.Deserialize(stream);
				FilterGlobals = ((obj != null) ? ((FilterStruct)obj) : default(FilterStruct));
				stream.Close();
				return;
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				MessageBox.Show(ex2.Message + "  I'll use defaults for Filter.cfg.");
				ProjectData.ClearProjectError();
			}
		}
		FilterGlobals.BkoutDirRBOption = 2;
		FilterGlobals.HeightRBOption = 2;
		FilterGlobals.PriceRBOption = 2;
		FilterGlobals.WidthRBOption = 0;
		FilterGlobals.NumericWidthLess = 180m;
		FilterGlobals.NumericWidthLow = default(decimal);
		FilterGlobals.NumericWidthHigh = 180m;
		FilterGlobals.NumericWidthMore = default(decimal);
		FilterGlobals.NumericPriceLess = 500m;
		FilterGlobals.NumericPriceLow = 5m;
		FilterGlobals.NumericPriceHigh = 1000000m;
		FilterGlobals.NumericPriceMore = 5m;
		FilterGlobals.NumericVolume = 100000m;
		FilterGlobals.NumericPriceMoves = 5m;
		FilterGlobals.NumericHighVolume = 2m;
		FilterGlobals.CBStage1 = false;
		FilterGlobals.CBStage2 = false;
		FilterGlobals.CBStage3 = false;
		FilterGlobals.CBStage4 = false;
		FilterGlobals.CBBkoutIncludeNone = true;
		FilterGlobals.CBWidth = false;
		FilterGlobals.CBPrice = false;
		FilterGlobals.CBBkoutDirection = false;
		FilterGlobals.CBHeight = false;
		FilterGlobals.CBVolume = false;
		FilterGlobals.CBMasterSwitch = false;
		FilterGlobals.CBPriceMoves = false;
		FilterGlobals.CBHighVolume = false;
	}

	private static bool ReadStock(StreamReader StockFile, long FileSize, ref ProgressBar ProgBar, ref Label ErrorLabel, bool QuickExit, int DisplayPeriod, string Filename)
	{
		//IL_0074: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b3: Unknown result type (might be due to invalid IL or missing references)
		//IL_1000: Unknown result type (might be due to invalid IL or missing references)
		//IL_1006: Invalid comparison between Unknown and I4
		bool flag = false;
		HLCRange = 0;
		ErrorCount = 0;
		ErrorMessage = null;
		int num = 0;
		if (ProgBar != null)
		{
			ProgBar.Value = 0;
		}
		if (ErrorLabel != null)
		{
			ErrorLabel.Text = "";
		}
		nHLC = null;
		nDT = null;
		string text = StockFile.ReadToEnd();
		if (text == null)
		{
			return true;
		}
		if (text.Length == 0)
		{
			if (!HideMessages)
			{
				MessageBox.Show(Filename + " does not appear to have a header.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			}
			return true;
		}
		string text2 = ClosestDelimiter(text);
		if (Operators.CompareString(text2, "-1", false) == 0)
		{
			if (!HideMessages)
			{
				MessageBox.Show(Filename + ": Can't find the file delimiter (number separator).", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			}
			return true;
		}
		checked
		{
			if (Strings.InStr(Strings.UCase(text), "DATE", (CompareMethod)0) != 0)
			{
				int num2 = Strings.InStr(text, "\r\n", (CompareMethod)0);
				if (num2 == 0)
				{
					num2 = Strings.InStr(text, "\r", (CompareMethod)0);
					if (num2 == 0)
					{
						num2 = Strings.InStr(text, "\n", (CompareMethod)0);
						if (num2 == 0)
						{
							return true;
						}
						text = Strings.Right(text, text.Length + 1 - num2 - "\n".Length);
					}
					else
					{
						text = Strings.Right(text, text.Length + 1 - num2 - "\r".Length);
					}
				}
				else
				{
					text = Strings.Right(text, text.Length - num2 - "\r\n".Length + 1);
				}
				if (text == null)
				{
					return true;
				}
			}
			text = Strings.Trim(text.Replace('"', ' '));
			text = text.Replace("\r\n", "\r").Replace("\n", "\r").Replace("\r\r", "\r");
			string[] array = Regex.Split(text, "\r");
			nHLC = new decimal[6, array.Length - 1 + 1];
			nDT = new DateTime[2, array.Length - 1 + 1];
			HLCRange = array.Length - 1;
			int num3 = 0;
			string[] array2 = array;
			bool flag2 = default(bool);
			decimal num6 = default(decimal);
			foreach (string text3 in array2)
			{
				if (Strings.Trim(text3).Length == 0)
				{
					continue;
				}
				int num4 = 1;
				string[] array3 = Regex.Split(text3, text2);
				foreach (string text4 in array3)
				{
					if (Strings.Trim(text4).Length == 0)
					{
						continue;
					}
					int num5 = num4;
					if (num5 == FileFormat[0])
					{
						try
						{
							DateTime result = DateTime.MinValue;
							if (DateTime.TryParseExact(Strings.Trim(text4), UserDate, CultureInfo.InvariantCulture, DateTimeStyles.None, out result))
							{
								if (ckFileFormat[1])
								{
									nDT[0, num3] = MyCDate(Conversions.ToString(result) + " " + Strings.Format((object)nDT[1, num3], ""));
								}
								else
								{
									nDT[0, num3] = result;
								}
								goto IL_08e0;
							}
							if (DateTime.TryParseExact(Strings.Trim(text4), UserDate, CultureInfo.CurrentCulture, DateTimeStyles.None, out result))
							{
								if (ckFileFormat[1])
								{
									nDT[0, num3] = MyCDate(Conversions.ToString(result) + " " + Strings.Format((object)nDT[1, num3], ""));
								}
								else
								{
									nDT[0, num3] = result;
								}
								goto IL_08e0;
							}
							if (DateTime.TryParse(Strings.Trim(text4), out result))
							{
								if (ckFileFormat[1])
								{
									nDT[0, num3] = MyCDate(Conversions.ToString(result) + " " + Strings.Format((object)nDT[1, num3], ""));
								}
								else
								{
									nDT[0, num3] = result;
								}
								goto IL_08e0;
							}
							if (Operators.CompareString(Strings.Right(UserDate, 5), "HH:mm", false) == 0)
							{
								UserDate = Strings.Trim(Strings.Left(UserDate, Strings.Len(UserDate) - 5));
							}
							ErrorCount++;
							if (num3 > 0)
							{
								ErrorMessage = ErrorMessage + Filename + ": Date error after " + Strings.Format((object)nDT[0, num3 - 1], UserDate) + ", " + Strings.Format((object)nDT[1, num3 - 1], "") + "\r\n";
							}
							else
							{
								ErrorMessage = ErrorMessage + Filename + ": Date error at file start. \r\n";
							}
							flag2 = true;
						}
						catch (Exception ex)
						{
							ProjectData.SetProjectError(ex);
							Exception ex2 = ex;
							ErrorCount++;
							if (num3 > 0)
							{
								ErrorMessage = ErrorMessage + Filename + ": Date error after " + Strings.Format((object)nDT[0, num3 - 1], UserDate) + ", " + Strings.Format((object)nDT[1, num3 - 1], "") + "\r\n";
							}
							else
							{
								ErrorMessage = ErrorMessage + Filename + ": Date error at file start. \r\n";
							}
							flag2 = true;
							ProjectData.ClearProjectError();
						}
						break;
					}
					if (num5 == FileFormat[1])
					{
						if (ckFileFormat[1])
						{
							try
							{
								nDT[1, num3] = MyCDate(text4);
								nDT[0, num3] = MyCDate(Strings.Format((object)nDT[0, num3], "") + " " + text4);
							}
							catch (Exception ex3)
							{
								ProjectData.SetProjectError(ex3);
								Exception ex4 = ex3;
								ErrorCount++;
								if (num3 > 0)
								{
									ErrorMessage = ErrorMessage + Filename + ": Time error on " + Strings.Format((object)nDT[0, num3], UserDate) + ", after " + Strings.Format((object)nDT[1, num3 - 1], "") + "\r\n";
								}
								else
								{
									ErrorMessage = ErrorMessage + Filename + ": Time error at file start: " + Strings.Format((object)nDT[0, num3], UserDate) + "\r\n";
								}
								flag2 = true;
								ProjectData.ClearProjectError();
								break;
							}
						}
					}
					else if (num5 == FileFormat[2])
					{
						try
						{
							if (ckFileFormat[2])
							{
								num = DecimalCount(text4, num);
								nHLC[0, num3] = Conversions.ToDecimal(text4);
							}
						}
						catch (Exception ex5)
						{
							ProjectData.SetProjectError(ex5);
							Exception ex6 = ex5;
							ReadStockErrorHandler(num3, Filename + ": Opening price");
							flag2 = true;
							ProjectData.ClearProjectError();
							break;
						}
					}
					else if (num5 == FileFormat[3])
					{
						try
						{
							num = DecimalCount(text4, num);
							nHLC[1, num3] = Conversions.ToDecimal(text4);
						}
						catch (Exception ex7)
						{
							ProjectData.SetProjectError(ex7);
							Exception ex8 = ex7;
							ReadStockErrorHandler(num3, Filename + ": High price");
							flag2 = true;
							ProjectData.ClearProjectError();
							break;
						}
					}
					else if (num5 == FileFormat[4])
					{
						try
						{
							num = DecimalCount(text4, num);
							nHLC[2, num3] = Conversions.ToDecimal(text4);
						}
						catch (Exception ex9)
						{
							ProjectData.SetProjectError(ex9);
							Exception ex10 = ex9;
							ReadStockErrorHandler(num3, Filename + ": Low price");
							flag2 = true;
							ProjectData.ClearProjectError();
							break;
						}
					}
					else if (num5 == FileFormat[5])
					{
						try
						{
							num = DecimalCount(text4, num);
							nHLC[3, num3] = Conversions.ToDecimal(text4);
						}
						catch (Exception ex11)
						{
							ProjectData.SetProjectError(ex11);
							Exception ex12 = ex11;
							ReadStockErrorHandler(num3, Filename + ": Closing price");
							flag2 = true;
							ProjectData.ClearProjectError();
							break;
						}
					}
					else if (num5 == FileFormat[6])
					{
						try
						{
							if (ckFileFormat[6])
							{
								nHLC[4, num3] = Conversions.ToDecimal(text4);
								if ((decimal.Compare(nHLC[4, num3], 0m) == 0) & (DiscardQuote == 2))
								{
									flag2 = true;
									break;
								}
							}
						}
						catch (Exception ex13)
						{
							ProjectData.SetProjectError(ex13);
							Exception ex14 = ex13;
							ReadStockErrorHandler(num3, Filename + ": Volume");
							flag2 = true;
							ProjectData.ClearProjectError();
							break;
						}
					}
					else if (num5 == FileFormat[7])
					{
						try
						{
							if (ckFileFormat[7])
							{
								num = DecimalCount(text4, num);
								nHLC[5, num3] = Conversions.ToDecimal(text4);
								num6 = Conversions.ToDecimal(text4);
							}
						}
						catch (Exception ex15)
						{
							ProjectData.SetProjectError(ex15);
							Exception ex16 = ex15;
							ReadStockErrorHandler(num3, Filename + ": Adjusted closing price");
							flag2 = true;
							ProjectData.ClearProjectError();
							break;
						}
					}
					goto IL_08e0;
					IL_08e0:
					if (Operators.CompareString(text4, "\r\n", false) == 0)
					{
						break;
					}
					num4++;
				}
				num3++;
				if (!Quiet && ProgBar != null && ((unchecked(num3 % 100) == 0) & (HLCRange != 0)))
				{
					ProgBar.Value = (int)Math.Round((double)(100 * num3) / (double)HLCRange);
				}
			}
			int decimalsOption = DecimalsOption;
			if (decimalsOption == DECIMALSUSER)
			{
				DecimalsUsed = UserDecimals;
			}
			else if (decimalsOption == DECIMALSFILE)
			{
				DecimalsUsed = num;
			}
			else if (decimalsOption == DECIMALSBOTH)
			{
				DecimalsUsed = Conversions.ToInteger(Interaction.IIf(UserDecimals < num, (object)UserDecimals, (object)num));
			}
			int hLCRange = HLCRange;
			decimal d = default(decimal);
			for (num3 = 0; num3 <= hLCRange; num3++)
			{
				nHLC[0, num3] = LimitDecimals(nHLC[0, num3]);
				nHLC[1, num3] = LimitDecimals(nHLC[1, num3]);
				nHLC[2, num3] = LimitDecimals(nHLC[2, num3]);
				nHLC[3, num3] = LimitDecimals(nHLC[3, num3]);
				if (!flag2)
				{
					if (ckFileFormat[7])
					{
						if (decimal.Compare(num6, 0m) != 0)
						{
							d = decimal.Divide(nHLC[3, num3], num6);
						}
						if (decimal.Compare(d, 0m) == 0)
						{
							d = 1m;
						}
					}
					if ((decimal.Compare(nHLC[1, num3], 0m) == 0) & (decimal.Compare(nHLC[2, num3], 0m) == 0) & (decimal.Compare(nHLC[3, num3], 0m) == 0))
					{
						nHLC[1, num3] = 1m;
						nHLC[2, num3] = 1m;
						nHLC[3, num3] = 1m;
						if (ckFileFormat[2] & (decimal.Compare(nHLC[0, num3], 0m) == 0))
						{
							nHLC[0, num3] = 1m;
						}
						if (num3 != HLCRange)
						{
							ReadStockErrorHandler(num3, Filename + ": Zero price quote");
						}
					}
					if (decimal.Compare(nHLC[1, num3], 0m) == 0)
					{
						if (ckFileFormat[2])
						{
							nHLC[1, num3] = Math.Max(Math.Max(nHLC[2, num3], nHLC[3, num3]), nHLC[0, num3]);
						}
						else
						{
							nHLC[1, num3] = Math.Max(nHLC[2, num3], nHLC[3, num3]);
						}
						ReadStockErrorHandler(num3, Filename + ": High price is zero");
					}
					if (decimal.Compare(nHLC[2, num3], 0m) == 0)
					{
						if (ckFileFormat[2] & (decimal.Compare(nHLC[0, num3], 0m) != 0))
						{
							nHLC[2, num3] = Math.Min(Math.Min(nHLC[1, num3], nHLC[3, num3]), nHLC[0, num3]);
						}
						else
						{
							nHLC[2, num3] = Math.Min(nHLC[1, num3], nHLC[3, num3]);
						}
						ReadStockErrorHandler(num3, Filename + ": Low price is zero");
					}
					if (decimal.Compare(nHLC[3, num3], 0m) == 0)
					{
						nHLC[3, num3] = decimal.Divide(decimal.Add(nHLC[1, num3], nHLC[2, num3]), 2m);
						ReadStockErrorHandler(num3, Filename + ": Closing price is zero");
					}
					if (ckFileFormat[2])
					{
						if (decimal.Compare(nHLC[0, num3], 0m) == 0)
						{
							nHLC[0, num3] = nHLC[3, num3];
							ErrorCount++;
							ErrorMessage = ErrorMessage + Filename + ": Opening price is zero: " + Strings.Format((object)nDT[0, num3], UserDate) + ".\r\n";
						}
						if (decimal.Compare(nHLC[0, num3], nHLC[2, num3]) < 0)
						{
							decimal num7 = nHLC[0, num3];
							nHLC[0, num3] = nHLC[2, num3];
							nHLC[2, num3] = num7;
							ReadStockErrorHandler(num3, Filename + ": Opening price is below the low");
						}
						if (decimal.Compare(nHLC[0, num3], nHLC[1, num3]) > 0)
						{
							decimal num7 = nHLC[0, num3];
							nHLC[0, num3] = nHLC[1, num3];
							nHLC[1, num3] = num7;
							ReadStockErrorHandler(num3, Filename + ": Opening price is above the high");
						}
					}
					if (decimal.Compare(nHLC[1, num3], nHLC[2, num3]) < 0)
					{
						decimal num7 = nHLC[1, num3];
						nHLC[1, num3] = nHLC[2, num3];
						nHLC[2, num3] = num7;
						ReadStockErrorHandler(num3, Filename + ": High price is below the low");
					}
					if (decimal.Compare(nHLC[3, num3], nHLC[2, num3]) < 0)
					{
						decimal num7 = nHLC[3, num3];
						nHLC[3, num3] = nHLC[2, num3];
						nHLC[2, num3] = num7;
						ReadStockErrorHandler(num3, Filename + ": Closing price is below the low");
					}
					if (decimal.Compare(nHLC[3, num3], nHLC[1, num3]) > 0)
					{
						decimal num7 = nHLC[3, num3];
						nHLC[3, num3] = nHLC[1, num3];
						nHLC[1, num3] = num7;
						ReadStockErrorHandler(num3, Filename + ": Closing price is above the high");
					}
				}
				if (!Quiet && ProgBar != null && ((unchecked(num3 % 100) == 0) & (HLCRange != 0)))
				{
					ProgBar.Value = (int)Math.Round((double)(100 * num3) / (double)HLCRange);
				}
				if (QuickExit & (ErrorCount > 25))
				{
					break;
				}
				if (HideMessages)
				{
					flag = true;
				}
				if (!flag & (ErrorCount > 100))
				{
					if (unchecked((int)MessageBox.Show(Filename + ": I'm encountering a lot of quote errors. Possible causes:\r\n\r\n1. Not enough decimal places for this file. Change the 'When possible limit decimal places to' the number of allowed decimal places on the Chart's Setup Form to match the number of decimals in the data (use Notepad, Excel, or other editor to open a stock quote file and look). Exit the Setup and Chart Forms, and then chart it again.\r\n\r\nFor example, if you have 2 decimal places set but your currency file has 8 places, the file may not render properly.\r\n\r\n2. Possible bad update or file formats which vary from file to file (such as an intraday file with hours and minutes and a daily file without hours and minutes).\r\n\r\nDid you want me to stop loading the file?", "GlobalForm: ReadStock", (MessageBoxButtons)4, (MessageBoxIcon)32, (MessageBoxDefaultButton)0)) == 6)
					{
						break;
					}
					flag = true;
				}
			}
			if (HLCRange > 0 && ((DateAndTime.Year(nDT[0, HLCRange]) < 1900) | ((decimal.Compare(nHLC[3, HLCRange], 0m) == 0) & (decimal.Compare(nHLC[1, HLCRange], 0m) == 0))))
			{
				HLCRange--;
				nDT = (DateTime[,])Utils.CopyArray((Array)nDT, (Array)new DateTime[2, HLCRange + 1]);
				nHLC = (decimal[,])Utils.CopyArray((Array)nHLC, (Array)new decimal[6, HLCRange + 1]);
			}
			IntradayData = false;
			if (HLCRange > 1)
			{
				if (HLCRange >= 3)
				{
					if ((DateTime.Compare(nDT[0, 0].Date, nDT[0, 1].Date) == 0) | (DateTime.Compare(nDT[0, 1].Date, nDT[0, 2].Date) == 0))
					{
						IntradayData = true;
						if (Operators.CompareString(Strings.Right(UserDate, 6), " HH:mm", false) != 0)
						{
							UserDate += " HH:mm";
						}
					}
					else if (Operators.CompareString(Strings.Right(UserDate, 6), " HH:mm", false) == 0)
					{
						UserDate = Strings.Left(UserDate, Strings.Len(UserDate) - Strings.Len(" HH:mm"));
					}
				}
				if ((IntradayData & (DateTime.Compare(nDT[0, 0], nDT[0, 1]) > 0)) | (!IntradayData & (DateTime.Compare(nDT[0, 0].Date, nDT[0, 1].Date) > 0)))
				{
					decimal[,] array4 = new decimal[6, HLCRange + 1];
					DateTime[,] array5 = new DateTime[2, HLCRange + 1];
					int hLCRange2 = HLCRange;
					for (num3 = 0; num3 <= hLCRange2; num3++)
					{
						array5[0, num3] = Conversions.ToDate(Interaction.IIf(IntradayData, (object)nDT[0, num3], (object)nDT[0, num3].Date));
						array5[1, num3] = nDT[1, num3];
						array4[0, num3] = nHLC[0, num3];
						array4[1, num3] = nHLC[1, num3];
						array4[2, num3] = nHLC[2, num3];
						array4[3, num3] = nHLC[3, num3];
						array4[4, num3] = nHLC[4, num3];
						array4[5, num3] = nHLC[5, num3];
					}
					int hLCRange3 = HLCRange;
					for (num3 = 0; num3 <= hLCRange3; num3++)
					{
						nDT[0, num3] = Conversions.ToDate(Interaction.IIf(IntradayData, (object)array5[0, HLCRange - num3], (object)array5[0, HLCRange - num3].Date));
						nDT[1, num3] = array5[1, HLCRange - num3];
						nHLC[0, num3] = array4[0, HLCRange - num3];
						nHLC[1, num3] = array4[1, HLCRange - num3];
						nHLC[2, num3] = array4[2, HLCRange - num3];
						nHLC[3, num3] = array4[3, HLCRange - num3];
						nHLC[4, num3] = array4[4, HLCRange - num3];
						nHLC[5, num3] = array4[5, HLCRange - num3];
					}
				}
			}
			sHLC = null;
			sHLC = new object[8, HLCRange + 1];
			decimal num8 = default(decimal);
			decimal num9 = default(decimal);
			int hLCRange4 = HLCRange;
			for (num3 = 0; num3 <= hLCRange4; num3++)
			{
				sHLC[6, num3] = Conversions.ToDate(Interaction.IIf(IntradayData, (object)nDT[0, num3], (object)nDT[0, num3].Date));
				sHLC[7, num3] = nDT[1, num3];
				sHLC[0, num3] = nHLC[0, num3];
				sHLC[1, num3] = nHLC[1, num3];
				sHLC[2, num3] = nHLC[2, num3];
				sHLC[3, num3] = nHLC[3, num3];
				sHLC[4, num3] = nHLC[4, num3];
				sHLC[5, num3] = nHLC[5, num3];
				if (decimal.Compare(nHLC[1, num3], num8) > 0)
				{
					num8 = nHLC[1, num3];
				}
				if (((decimal.Compare(nHLC[2, num3], num9) < 0) & (decimal.Compare(nHLC[2, num3], 0m) != 0)) | (decimal.Compare(num9, 0m) == 0))
				{
					num9 = nHLC[2, num3];
				}
			}
			if ((DisplayPeriod != 0) | (ChartPeriodShown != 0))
			{
				DataPeriodConverter(DisplayPeriod);
			}
			if (ErrorCount != 0)
			{
				if (ErrorLabel != null)
				{
					ErrorLabel.Text = "Quote errors: " + Strings.Format((object)ErrorCount, "");
				}
				try
				{
					if (ErrorMessage.Length > 0)
					{
						Clipboard.SetText(ErrorMessage);
					}
				}
				catch (Exception ex17)
				{
					ProjectData.SetProjectError(ex17);
					Exception ex18 = ex17;
					ProjectData.ClearProjectError();
				}
			}
			Futures = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(decimal.Subtract(num8, num9), 0.25m) <= 0, (object)true, (object)false));
			NearFutures = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(decimal.Subtract(num8, num9), 2.5m) <= 0, (object)true, (object)false));
			if (!Quiet && ProgBar != null)
			{
				ProgBar.Value = 0;
			}
			return false;
		}
	}

	private static void ReadStockErrorHandler(int i, string Phrase)
	{
		checked
		{
			ErrorCount++;
			if (i > 0)
			{
				ErrorMessage = ErrorMessage + Phrase + " error on " + Strings.Format((object)nDT[0, i], UserDate) + ".\r\n";
			}
			else
			{
				ErrorMessage = ErrorMessage + Phrase + " error at file start.\r\n";
			}
		}
	}

	public static void ReadWriteBearFile()
	{
		//IL_03ba: Unknown result type (might be due to invalid IL or missing references)
		//IL_01f9: Unknown result type (might be due to invalid IL or missing references)
		string text = ConfigLocation + sBearFile;
		checked
		{
			string text2;
			if (File.Exists(text))
			{
				text2 = ((ServerComputer)MyProject.Computer).FileSystem.ReadAllText(text);
				int num = Strings.InStr(text2, "\r\n", (CompareMethod)0) + 1;
				text2 = Strings.Right(text2, text2.Length - num);
				text2 = text2.Replace("\r\n", ",");
				text2 = Strings.Left(text2, text2.Length - 1);
				string[] array = Regex.Split(text2, ",");
				num = 0;
				int num2 = 0;
				int num3 = 1;
				string text3 = "";
				string[] array2 = array;
				foreach (string text4 in array2)
				{
					switch (num)
					{
					case 0:
						BearMkts = (BearMktsStruct[])Utils.CopyArray((Array)BearMkts, (Array)new BearMktsStruct[num2 + 1]);
						try
						{
							BearMkts[num2].StartDate = Conversions.ToDate(text4);
						}
						catch (Exception ex3)
						{
							ProjectData.SetProjectError(ex3);
							Exception ex4 = ex3;
							text3 = text3 + "Start date incorrect in line " + num3 + "\r\n";
							ProjectData.ClearProjectError();
						}
						num++;
						break;
					case 1:
						num++;
						try
						{
							BearMkts[num2].EndDate = Conversions.ToDate(text4);
						}
						catch (Exception ex5)
						{
							ProjectData.SetProjectError(ex5);
							Exception ex6 = ex5;
							text3 = text3 + "End date incorrect in line " + num3 + "\r\n";
							ProjectData.ClearProjectError();
						}
						break;
					case 2:
						try
						{
							BearMkts[num2].Text = text4;
						}
						catch (Exception ex)
						{
							ProjectData.SetProjectError(ex);
							Exception ex2 = ex;
							text3 = text3 + "Description is missing in line " + num3 + "\r\n";
							ProjectData.ClearProjectError();
						}
						num2++;
						num = 0;
						num3++;
						break;
					}
				}
				if (Operators.CompareString(text3, "", false) != 0)
				{
					MessageBox.Show("The file " + text + " has these errors.\r\n\r\n" + text3 + "\r\n\r\nThe file should hold information about the start and end of bear markets. The first line in the file is a header describing the format. The remainder of the TEXT file follows this format: start date,end date,description<carriage return line feed>\r\n\r\nIf you delete the file, I'll create a new one (or you can fix the errors yourself).", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				}
				return;
			}
			BearMkts = new BearMktsStruct[3];
			BearMkts[0].StartDate = Conversions.ToDate("3/24/2000");
			BearMkts[0].EndDate = Conversions.ToDate("10/10/2002");
			BearMkts[0].Text = "2000-2002 Bear Market";
			BearMkts[1].StartDate = Conversions.ToDate("10/12/2007");
			BearMkts[1].EndDate = Conversions.ToDate("3/6/2009");
			BearMkts[1].Text = "2007-2009 Bear Market";
			BearMkts[2].StartDate = Conversions.ToDate("2/19/2020");
			BearMkts[2].EndDate = Conversions.ToDate("4/6/2020");
			BearMkts[2].Text = "2020 Covid-19";
			text2 = "Start date,End date,description\r\n";
			int num4 = BearMkts.Length - 1;
			for (int j = 0; j <= num4; j++)
			{
				text2 = text2 + Strings.Format((object)BearMkts[j].StartDate, UserDate) + "," + Strings.Format((object)BearMkts[j].EndDate, UserDate) + "," + BearMkts[j].Text + "\r\n";
			}
			try
			{
				File.WriteAllText(text, text2);
			}
			catch (Exception ex7)
			{
				ProjectData.SetProjectError(ex7);
				Exception ex8 = ex7;
				MessageBox.Show("Couldn't write " + text + ".", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				ProjectData.ClearProjectError();
			}
		}
	}

	public static void ReleaseQuoteInfo(Chart Chart1, MouseEventArgs e)
	{
		//IL_0056: Unknown result type (might be due to invalid IL or missing references)
		if (QuoteInfo)
		{
			QuoteInfo = false;
			try
			{
				if (Annot != null)
				{
					((Collection<Annotation>)(object)Chart1.Annotations).Remove((Annotation)(object)Annot);
					((ChartElement)Annot).Dispose();
					Annot = null;
				}
				return;
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				MessageBox.Show("ReleaseQuoteInfo(): " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				ProjectData.ClearProjectError();
				return;
			}
		}
		LineEndPoints item = new LineEndPoints
		{
			StartPoint = FirstPoint,
			endPoint = new Point(e.X, e.Y)
		};
		LinesList.Add(item);
		FirstPoint = default(Point);
	}

	private static decimal ReportVolStop(int i, decimal StopTally, int Index, int BreakoutType)
	{
		checked
		{
			decimal num = default(decimal);
			if (StrictPatterns)
			{
				if (i > 19)
				{
					switch (BreakoutType)
					{
					case 1:
						num = LimitDecimals(decimal.Subtract(nHLC[2, i], decimal.Divide(decimal.Multiply(2m, StopTally), 20m)));
						if (decimal.Compare(num, 0m) > 0 && decimal.Compare(nHLC[2, i], 0m) != 0)
						{
							CPInfo.VolStop = Conversions.ToString(num) + " or " + Strings.Format((object)decimal.Subtract(decimal.Divide(num, nHLC[2, i]), 1m), "0%");
						}
						break;
					case -1:
						num = LimitDecimals(decimal.Add(nHLC[1, i], decimal.Divide(decimal.Multiply(2m, StopTally), 20m)));
						if (decimal.Compare(nHLC[1, i], 0m) != 0)
						{
							CPInfo.VolStop = Conversions.ToString(num) + " or " + Strings.Format((object)decimal.Subtract(decimal.Divide(num, nHLC[1, i]), 1m), "0%");
						}
						break;
					case 0:
						num = LimitDecimals(decimal.Subtract(nHLC[3, i], decimal.Divide(decimal.Multiply(2m, StopTally), 20m)));
						if (decimal.Compare(num, 0m) > 0 && decimal.Compare(nHLC[3, i], 0m) != 0)
						{
							CPInfo.VolStop = Conversions.ToString(num) + " or " + Strings.Format((object)decimal.Subtract(decimal.Divide(num, nHLC[3, i]), 1m), "0%");
						}
						break;
					}
					if (decimal.Compare(num, 0m) < 0)
					{
						num = default(decimal);
					}
				}
				else
				{
					num = -1m;
				}
			}
			else if (i > 19)
			{
				switch (BreakoutType)
				{
				case 1:
					num = LimitDecimals(decimal.Subtract(nHLC[2, i - 1], decimal.Divide(decimal.Multiply(2m, StopTally), 20m)));
					if (decimal.Compare(num, 0m) > 0 && decimal.Compare(nHLC[2, i - 1], 0m) != 0)
					{
						CPInfo.VolStop = Conversions.ToString(num) + " or " + Strings.Format((object)decimal.Subtract(decimal.Divide(num, nHLC[2, i - 1]), 1m), "0%");
					}
					break;
				case -1:
					num = LimitDecimals(decimal.Add(nHLC[1, i - 1], decimal.Divide(decimal.Multiply(2m, StopTally), 20m)));
					if (decimal.Compare(nHLC[1, i - 1], 0m) != 0)
					{
						CPInfo.VolStop = Conversions.ToString(num) + " or " + Strings.Format((object)decimal.Subtract(decimal.Divide(num, nHLC[1, i - 1]), 1m), "0%");
					}
					break;
				case 0:
					num = LimitDecimals(decimal.Subtract(nHLC[3, i], decimal.Divide(decimal.Multiply(2m, StopTally), 20m)));
					if (decimal.Compare(num, 0m) > 0 && decimal.Compare(nHLC[3, i], 0m) != 0)
					{
						CPInfo.VolStop = Conversions.ToString(num) + " or " + Strings.Format((object)decimal.Subtract(decimal.Divide(num, nHLC[3, i]), 1m), "0%");
					}
					break;
				}
				if (decimal.Compare(num, 0m) < 0)
				{
					num = default(decimal);
				}
			}
			else
			{
				num = -1m;
			}
			ChartPatterns[Index].StopPrice = num;
			ChartPatterns[Index].StopDate = Strings.Format((object)nDT[0, Conversions.ToInteger(Interaction.IIf(BreakoutType == 0, (object)i, (object)(i - 1)))], UserDate);
			return num;
		}
	}

	public static void SelectChartType(Chart Chart1)
	{
		//IL_0089: Unknown result type (might be due to invalid IL or missing references)
		//IL_00e6: Unknown result type (might be due to invalid IL or missing references)
		//IL_013e: Unknown result type (might be due to invalid IL or missing references)
		((Collection<ChartArea>)(object)Chart1.ChartAreas)[0].AxisY2.LabelStyle.Format = $"F{DecimalsUsed:D}";
		if (IntradayData)
		{
			((Collection<ChartArea>)(object)Chart1.ChartAreas)[0].AxisX.LabelStyle.Format = "M/d HH:mm";
		}
		else
		{
			((Collection<ChartArea>)(object)Chart1.ChartAreas)[0].AxisX.LabelStyle.Format = UserDate;
		}
		SeriesChartType chartType = default(SeriesChartType);
		switch (ChartType)
		{
		case 0:
			chartType = (SeriesChartType)20;
			((DataPointCustomProperties)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"])["PriceUpColor"] = UpCandleColor.ToArgb().ToString();
			((DataPointCustomProperties)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"])["PriceDownColor"] = DownCandleColor.ToArgb().ToString();
			break;
		case 1:
			chartType = (SeriesChartType)19;
			break;
		}
		if (((ChartNamedElementCollection<Series>)(object)Chart1.Series).IndexOf("VolumeSeries") != -1)
		{
			((DataPointCustomProperties)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"]).Color = VolumeBGColor;
		}
		((DataPointCustomProperties)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"]).Color = PriceBarColor;
		((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].ChartType = chartType;
		((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].BackColor = ChartBGColor;
	}

	public static void SetupDateIndexes(DateTime ChStart, DateTime ChEnd)
	{
		ChartStartIndex = -1;
		ChartEndIndex = -1;
		checked
		{
			try
			{
				int hLCRange = HLCRange;
				for (int i = 0; i <= hLCRange; i++)
				{
					if (IntradayData)
					{
						if ((ChartStartIndex == -1) & (DateTime.Compare(nDT[0, i], ChStart) >= 0))
						{
							ChartStartIndex = i;
						}
						if (DateTime.Compare(nDT[0, i], ChEnd) >= 0)
						{
							if ((i > 0) & (DateTime.Compare(nDT[0, i], ChEnd) > 0))
							{
								ChartEndIndex = i - 1;
							}
							else
							{
								ChartEndIndex = i;
							}
							break;
						}
						continue;
					}
					if ((ChartStartIndex == -1) & (DateTime.Compare(nDT[0, i].Date, ChStart.Date) >= 0))
					{
						ChartStartIndex = i;
					}
					if (DateTime.Compare(nDT[0, i].Date, ChEnd.Date) == 0)
					{
						ChartEndIndex = i;
						break;
					}
					if (DateTime.Compare(nDT[0, i].Date, ChEnd.Date) > 0)
					{
						ChartEndIndex = i - 1;
						break;
					}
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				HLCRange = 0;
				ProjectData.ClearProjectError();
			}
			if (ChartStartIndex == -1)
			{
				ChartStartIndex = HLCRange;
			}
			if (ChartEndIndex == -1)
			{
				ChartEndIndex = HLCRange;
			}
			if (ChartStartIndex > ChartEndIndex)
			{
				ChartStartIndex = ChartEndIndex;
			}
		}
	}

	public static void ShowQuoteInfo(Chart Chart1, MouseEventArgs e)
	{
		//IL_0014: Unknown result type (might be due to invalid IL or missing references)
		//IL_001b: Invalid comparison between Unknown and I4
		//IL_03aa: Unknown result type (might be due to invalid IL or missing references)
		//IL_0053: Unknown result type (might be due to invalid IL or missing references)
		//IL_005d: Expected O, but got Unknown
		//IL_0184: Unknown result type (might be due to invalid IL or missing references)
		//IL_018e: Expected O, but got Unknown
		try
		{
			HitTestResult val = Chart1.HitTest(e.X, e.Y);
			if ((int)val.ChartElementType == 16)
			{
				int pointIndex = val.PointIndex;
				checked
				{
					if (pointIndex + ChartStartIndex > HLCRange)
					{
						return;
					}
					if (Operators.CompareString(val.Series.Name, "VolumeSeries", false) == 0)
					{
						Annot = new CalloutAnnotation();
						QuoteInfo = true;
						((TextAnnotation)Annot).Text = Strings.Format((object)nDT[0, pointIndex + ChartStartIndex], UserDate) + "\r\n";
						((TextAnnotation)Annot).Text = ((TextAnnotation)Annot).Text + "Volume: " + Strings.Format((object)nHLC[4, pointIndex + ChartStartIndex], "");
						((Annotation)Annot).AnchorDataPoint = ((Collection<DataPoint>)(object)((Collection<Series>)(object)Chart1.Series)[1].Points)[pointIndex];
						((Annotation)Annot).Visible = true;
						((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)Annot);
					}
					else if ((Operators.CompareString(val.Series.Name, "CandleSeries", false) == 0) | (Operators.CompareString(val.Series.Name, "CPILine", false) == 0) | (Operators.CompareString(val.Series.Name, "CPIBull", false) == 0) | (Operators.CompareString(val.Series.Name, "CPIBear", false) == 0))
					{
						Annot = new CalloutAnnotation();
						QuoteInfo = true;
						((TextAnnotation)Annot).Text = Strings.Format((object)nDT[0, pointIndex + ChartStartIndex], UserDate) + "\r\n";
						if (ckFileFormat[2])
						{
							((TextAnnotation)Annot).Text = ((TextAnnotation)Annot).Text + "Open: " + Strings.Format((object)LimitDecimals(nHLC[0, pointIndex + ChartStartIndex]), "") + "\r\n";
						}
						((TextAnnotation)Annot).Text = ((TextAnnotation)Annot).Text + "High: " + Strings.Format((object)LimitDecimals(nHLC[1, pointIndex + ChartStartIndex]), "") + "\r\n";
						((TextAnnotation)Annot).Text = ((TextAnnotation)Annot).Text + "Low: " + Strings.Format((object)LimitDecimals(nHLC[2, pointIndex + ChartStartIndex]), "") + "\r\n";
						((TextAnnotation)Annot).Text = ((TextAnnotation)Annot).Text + "Close: " + Strings.Format((object)LimitDecimals(nHLC[3, pointIndex + ChartStartIndex]), "");
						((Annotation)Annot).AnchorDataPoint = ((Collection<DataPoint>)(object)((Collection<Series>)(object)Chart1.Series)[0].Points)[pointIndex];
						((Annotation)Annot).Visible = true;
						((Collection<Annotation>)(object)Chart1.Annotations).Add((Annotation)(object)Annot);
						if (!Toggle)
						{
							iFib1 = pointIndex + ChartStartIndex;
						}
						else
						{
							iFib2 = pointIndex + ChartStartIndex;
						}
						Toggle = !Toggle;
					}
				}
			}
			else
			{
				FirstPoint = new Point(e.X, e.Y);
				TempPoint = new Point(e.X, e.Y);
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			MessageBox.Show("ShowQuoteInfo(): " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			ProjectData.ClearProjectError();
		}
	}

	public static bool ShowStock(Chart Chart1, DateTime StartDate, DateTime EndDate, bool VolumeFlag, bool MAFlag)
	{
		//IL_0807: Unknown result type (might be due to invalid IL or missing references)
		//IL_0028: Unknown result type (might be due to invalid IL or missing references)
		//IL_004f: Unknown result type (might be due to invalid IL or missing references)
		bool result;
		checked
		{
			try
			{
				if (HLCRange == 0)
				{
					result = true;
					goto IL_0818;
				}
				if (!IsDate(StartDate))
				{
					MessageBox.Show("The beginning date is incorrect.", "Global: ShowStock", (MessageBoxButtons)0, (MessageBoxIcon)16);
					result = true;
					goto IL_0818;
				}
				if (!IsDate(EndDate))
				{
					MessageBox.Show("The ending date is incorrect.", "Global: ShowStock", (MessageBoxButtons)0, (MessageBoxIcon)16);
					result = true;
					goto IL_0818;
				}
				if (VolumeFlag && ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Count > 0)
				{
					((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Clear();
				}
				decimal d = default(decimal);
				if (MAFlag)
				{
					if (((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points).Count > 0)
					{
						((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points).Clear();
					}
					if (MAType == 2)
					{
						d = new decimal(2.0 / (double)(MALength + 1));
					}
				}
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Clear();
				if (DateTime.Compare(StartDate, EndDate) > 0)
				{
					DateTime dateTime = StartDate;
					StartDate = EndDate;
					EndDate = dateTime;
				}
				if (IntradayData)
				{
					if (DateTime.Compare(nDT[0, HLCRange], StartDate) <= 0)
					{
						EndDate = nDT[0, HLCRange];
						StartDate = ((HLCRange <= 524) ? nDT[0, 0] : nDT[0, HLCRange - 524]);
					}
				}
				else if (DateTime.Compare(nDT[0, HLCRange].Date, StartDate.Date) <= 0)
				{
					EndDate = nDT[0, HLCRange].Date;
					StartDate = DateAndTime.DateAdd("yyyy", -2.0, (object)EndDate);
				}
				decimal num = default(decimal);
				decimal num2 = default(decimal);
				long num3 = 0L;
				decimal d2 = default(decimal);
				bool flag = true;
				ChartStartIndex = -1;
				ChartEndIndex = -1;
				int hLCRange = HLCRange;
				decimal num4 = default(decimal);
				for (int i = 0; i <= hLCRange; i++)
				{
					if (IntradayData)
					{
						if (DateTime.Compare(nDT[0, i], EndDate) > 0)
						{
							ChartEndIndex = i - 1;
							break;
						}
					}
					else if (DateTime.Compare(nDT[0, i].Date, EndDate.Date) > 0)
					{
						ChartEndIndex = i - 1;
						break;
					}
					if (unchecked(MAUsed && MAFlag && ((MAType == 1) | (MAType == 2 && flag))))
					{
						d2 = decimal.Add(d2, nHLC[3, i]);
						if (i > MALength - 1)
						{
							d2 = decimal.Subtract(d2, nHLC[3, i - MALength]);
						}
					}
					unchecked
					{
						if ((!IntradayData & (DateTime.Compare(nDT[0, i].Date, StartDate.Date) >= 0)) | (IntradayData & (DateTime.Compare(nDT[0, i], StartDate) >= 0)))
						{
							if (ChartStartIndex == -1)
							{
								ChartStartIndex = i;
							}
							if (ChartVolume && VolumeFlag)
							{
								((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points.AddXY((object)nDT[0, i], new object[1] { nHLC[4, i] });
								num3 = Conversions.ToLong(Interaction.IIf(decimal.Compare(nHLC[4, i], new decimal(num3)) > 0, (object)nHLC[4, i], (object)num3));
							}
							((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points.AddXY((object)nDT[0, i], new object[4]
							{
								nHLC[1, i],
								nHLC[2, i],
								nHLC[0, i],
								nHLC[3, i]
							});
							num2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(nHLC[1, i], num2) > 0, (object)nHLC[1, i], (object)num2));
							num = Conversions.ToDecimal(Interaction.IIf((decimal.Compare(num, 0m) == 0) | ((decimal.Compare(nHLC[2, i], num) < 0) & (decimal.Compare(nHLC[2, i], 0m) > 0)), (object)nHLC[2, i], (object)num));
							if (MAUsed && MAFlag)
							{
								if (i >= checked(MALength - 1))
								{
									if (MAType == 1)
									{
										((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points.AddXY((object)nDT[0, i], new object[1] { decimal.Divide(d2, new decimal(MALength)) });
									}
									else if (MAType == 2)
									{
										if (i == checked(MALength - 1) || flag)
										{
											flag = false;
											num4 = decimal.Divide(d2, new decimal(MALength));
										}
										else if (i > checked(MALength - 1))
										{
											num4 = decimal.Add(num4, decimal.Multiply(d, decimal.Subtract(nHLC[3, i], num4)));
										}
										((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points.AddXY((object)nDT[0, i], new object[1] { num4 });
									}
								}
								else
								{
									((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points.AddXY((object)nDT[0, i], new object[1] { 0 });
								}
							}
						}
						if (IntradayData)
						{
							if (DateTime.Compare(nDT[0, i], EndDate) >= 0)
							{
								ChartEndIndex = i;
								break;
							}
						}
						else if (DateTime.Compare(nDT[0, i].Date, EndDate.Date) >= 0)
						{
							ChartEndIndex = i;
							break;
						}
					}
				}
				if (unchecked(MAUsed && MAFlag))
				{
					int num5 = Conversions.ToInteger(Interaction.IIf(MALength >= HLCRange, (object)(((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Count - 1), (object)MALength));
					int chartStartIndex = ChartStartIndex;
					int num6 = num5;
					for (int i = chartStartIndex; i <= num6; i++)
					{
						((DataPointCustomProperties)((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points)[i - ChartStartIndex]).Color = Color.Transparent;
					}
				}
				if (ChartStartIndex == -1)
				{
					ChartStartIndex = 0;
				}
				if (ChartEndIndex == -1)
				{
					ChartEndIndex = HLCRange;
				}
				((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY2.Maximum = Convert.ToDouble(num2) * 1.001;
				if (VolumeFlag & ChartVolume)
				{
					((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY.Maximum = 4 * num3;
					((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY2.Minimum = 0.989 * Convert.ToDouble(decimal.Subtract(num, decimal.Divide(decimal.Subtract(num2, num), 4m)));
				}
				else
				{
					((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY2.Minimum = Convert.ToDouble(num) * 0.999;
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				MessageBox.Show("Unknown error in ShowStock 1: " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				result = true;
				ProjectData.ClearProjectError();
				goto IL_0818;
			}
			result = false;
			goto IL_0818;
		}
		IL_0818:
		return result;
	}

	public static bool ShowStock(Chart Chart1, int StartIndex, int Endindex, bool VolumeFlag, bool MAFlag)
	{
		//IL_0665: Unknown result type (might be due to invalid IL or missing references)
		bool result;
		checked
		{
			try
			{
				if (HLCRange == 0)
				{
					result = true;
					goto IL_0676;
				}
				if (VolumeFlag && ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Count > 0)
				{
					((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points).Clear();
				}
				decimal d = default(decimal);
				if (MAFlag)
				{
					if (((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points).Count > 0)
					{
						((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points).Clear();
					}
					if (MAType == 2)
					{
						d = new decimal(2.0 / (double)(MALength + 1));
					}
				}
				((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Clear();
				decimal num = default(decimal);
				decimal num2 = default(decimal);
				long num3 = 0L;
				bool flag = true;
				decimal d2 = default(decimal);
				if (unchecked(MAUsed && MAFlag))
				{
					d2 = default(decimal);
					int num4 = Conversions.ToInteger(Interaction.IIf(StartIndex - MALength < 0, (object)0, (object)(StartIndex - MALength)));
					int num5 = StartIndex - 1;
					for (int i = num4; i <= num5; i++)
					{
						d2 = decimal.Add(d2, nHLC[3, i]);
					}
				}
				decimal num6 = default(decimal);
				for (int i = StartIndex; i <= Endindex; i++)
				{
					if (unchecked(MAUsed && MAFlag && ((MAType == 1) | (MAType == 2 && flag))))
					{
						d2 = decimal.Add(d2, nHLC[3, i]);
						if (i > MALength - 1)
						{
							d2 = decimal.Subtract(d2, nHLC[3, i - MALength]);
						}
					}
					unchecked
					{
						if (ChartVolume && VolumeFlag)
						{
							((ChartNamedElementCollection<Series>)(object)Chart1.Series)["VolumeSeries"].Points.AddXY((object)nDT[0, i], new object[1] { nHLC[4, i] });
							num3 = Conversions.ToLong(Interaction.IIf(decimal.Compare(nHLC[4, i], new decimal(num3)) > 0, (object)nHLC[4, i], (object)num3));
						}
						((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points.AddXY((object)nDT[0, i], new object[4]
						{
							nHLC[1, i],
							nHLC[2, i],
							nHLC[0, i],
							nHLC[3, i]
						});
						num2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(nHLC[1, i], num2) > 0, (object)nHLC[1, i], (object)num2));
						num = Conversions.ToDecimal(Interaction.IIf((decimal.Compare(num, 0m) == 0) | ((decimal.Compare(nHLC[2, i], num) < 0) & (decimal.Compare(nHLC[2, i], 0m) > 0)), (object)nHLC[2, i], (object)num));
						if (!(MAUsed && MAFlag))
						{
							continue;
						}
						if (i >= checked(MALength - 1))
						{
							if (MAType == 1)
							{
								((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points.AddXY((object)nDT[0, i], new object[1] { decimal.Divide(d2, new decimal(MALength)) });
							}
							else if (MAType == 2)
							{
								if (i == checked(MALength - 1) || flag)
								{
									flag = false;
									num6 = decimal.Divide(d2, new decimal(MALength));
								}
								else if (i > checked(MALength - 1))
								{
									flag = false;
									num6 = decimal.Add(num6, decimal.Multiply(d, decimal.Subtract(nHLC[3, i], num6)));
								}
								((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points.AddXY((object)nDT[0, i], new object[1] { num6 });
							}
						}
						else
						{
							((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points.AddXY((object)nDT[0, i], new object[1] { 0 });
						}
					}
				}
				if (unchecked(MAUsed && MAFlag))
				{
					int num7 = Conversions.ToInteger(Interaction.IIf(MALength >= HLCRange, (object)(((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Count - 1), (object)MALength));
					num7 = Conversions.ToInteger(Interaction.IIf(num7 > ((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Count - 1, (object)(((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["CandleSeries"].Points).Count - 1), (object)num7));
					int chartStartIndex = ChartStartIndex;
					int num8 = num7;
					for (int i = chartStartIndex; i <= num8; i++)
					{
						((DataPointCustomProperties)((Collection<DataPoint>)(object)((ChartNamedElementCollection<Series>)(object)Chart1.Series)["MASeries"].Points)[i - ChartStartIndex]).Color = Color.Transparent;
					}
				}
				((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY2.Maximum = Convert.ToDouble(num2) * 1.001;
				if (VolumeFlag & ChartVolume)
				{
					((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY.Maximum = 4 * num3;
					((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY2.Minimum = 0.989 * Convert.ToDouble(decimal.Subtract(num, decimal.Divide(decimal.Subtract(num2, num), 4m)));
				}
				else
				{
					((ChartNamedElementCollection<ChartArea>)(object)Chart1.ChartAreas)["ChartArea1"].AxisY2.Minimum = Convert.ToDouble(num) * 0.999;
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				MessageBox.Show("Unknown error in ShowStock 2: " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				result = true;
				ProjectData.ClearProjectError();
				goto IL_0676;
			}
			result = false;
			goto IL_0676;
		}
		IL_0676:
		return result;
	}

	public static string StripDBName(string Name)
	{
		int num = Strings.InStr(Name, "(", (CompareMethod)0);
		if (num > 0)
		{
			return Strings.Trim(Strings.Left(Name, checked(num - 1)));
		}
		return Name;
	}

	public static string Swap(string sFrom, string sTo, string Original)
	{
		return Original.Replace(sFrom, sTo);
	}

	public static bool SwapDates(ref DateTime FromDate, ref DateTime ToDate)
	{
		if (DateTime.Compare(FromDate, ToDate) > 0)
		{
			DateTime dateTime = ToDate;
			ToDate = FromDate;
			FromDate = dateTime;
		}
		return false;
	}

	public static object TranslatePatternName(object PatternName, int Type)
	{
		if (Type == PASSNAME)
		{
			switch (Conversions.ToString(PatternName))
			{
			case "AB=CD, bearish (ABCD Be)":
			case "AB=CD, bearish":
				return 4;
			case "AB=CD, bullish (ABCD Bu)":
			case "AB=CD, bullish":
				return 5;
			case "Bat, bearish, (Bat Be)":
			case "Bat, bearish":
				return 11;
			case "Bat, bullish, (Bat Bu)":
			case "Bat, bullish":
				return 10;
			case "Big M (BigM)":
			case "Big M":
				return 116;
			case "Big W (BigW)":
			case "Big W":
				return 115;
			case "Broadening bottom (BB)":
			case "Broadening bottom":
				return 114;
			case "Right-angled broadening fmtn, ascend (RABFA)":
			case "Broadening formation, right-angled & ascending":
				return 113;
			case "Right-angled broadening fmtn, descend (RABFD)":
			case "Broadening formation, right-angled & descending":
				return 112;
			case "Broadening top (BT)":
			case "Broadening top":
				return 111;
			case "Broadening wedge, ascending (BWA)":
			case "Broadening wedge, ascending":
				return 110;
			case "Broadening wedge, descending (BWD)":
			case "Broadening wedge, descending":
				return 109;
			case "Bump-and-run reversal bottom (BARRB)":
			case "Bump-and-run reversal, bottom":
				return 84;
			case "Bump-and-run reversal top (BARRT)":
			case "Bump-and-run reversal, top":
				return 83;
			case "Butterfly, bearish (Butt Be)":
			case "Butterfly, bearish":
				return 9;
			case "Butterfly, bullish (Butt Bu)":
			case "Butterfly, bullish":
				return 8;
			case "Carl V, Bearish (Carl Be)":
			case "Carl V, bearish":
				return 3;
			case "Carl V, bullish (Carl Bu)":
			case "Carl V, bullish":
				return 2;
			case "Channel, down":
				return 82;
			case "Channel, up":
				return 1;
			case "Closing price reversal, downtrend (c)":
			case "Closing price reversal, downtrend":
				return 52;
			case "Closing price reversal, uptrend (C)":
			case "Closing price reversal, uptrend":
				return 51;
			case "Crab, bearish (Crab Be)":
			case "Crab, bearish":
				return 7;
			case "Crab, bullish (Crab Bu)":
			case "Crab, bullish":
				return 6;
			case "Cup with handle":
				return 81;
			case "Cup with handle, inverted":
				return 48;
			case "Dead cat bounce (DCB, % drop)":
			case "Dead-cat bounce":
				return 100;
			case "Inverted dead cat bounce (iDCB, % rise)":
			case "Dead-cat bounce, inverted":
				return 99;
			case "Diving board":
				return 30;
			case "Double bottom (DB)":
			case "Double bottoms (all Types)":
				return 98;
			case "Double bottom, Adam & Adam (AADB)":
			case "Double bottom, Adam & Adam":
				return 20;
			case "Double bottom, Adam & Eve (AEDB)":
			case "Double bottom, Adam & Eve":
				return 21;
			case "Double bottom, Eve & Adam (EADB)":
			case "Double bottom, Eve & Adam":
				return 18;
			case "Double bottom, Eve & Eve (EEDB)":
			case "Double bottom, Eve & Eve":
				return 19;
			case "Double top (DT)":
			case "Double tops (all Types)":
				return 97;
			case "Double Top, Adam & Adam (AADT)":
			case "Double top, Adam & Adam":
				return 16;
			case "Double Top, Adam & Eve (AEDT)":
			case "Double top, Adam & Eve":
				return 17;
			case "Double Top, Eve & Adam (EADT)":
			case "Double top, Eve & Adam":
				return 14;
			case "Double Top, Eve & Eve (EEDT)":
			case "Double top, Eve & Eve":
				return 15;
			case "Fakey, bearish (FakeBe)":
			case "Fakey, bearish":
				return 12;
			case "Fakey, bullish (FakeBu)":
			case "Fakey, bullish":
				return 13;
			case "Falling wedge (FW)":
			case "Falling wedge":
				return 96;
			case "Flag":
				return 78;
			case "Gap 2H (2H)":
			case "Gap 2H":
				return 122;
			case "Gap 2H, inverted (2Hi)":
				return 123;
			case "Gap, breakaway (Gb)":
			case "Gap, breakaway":
				return 117;
			case "Gap, area or common (Ga)":
			case "Gap, area or common":
				return 118;
			case "Gap, continuation (Gc)":
			case "Gap, continuation":
				return 119;
			case "Gap, exhaustion (Ge)":
			case "Gap, exhaustion":
				return 121;
			case "Gap, type unknown (G?)":
			case "Gap, type unknown":
				return 120;
			case "Gartley, bearish (Gar Be)":
			case "Gartley, bearish":
				return 28;
			case "Gartley, bullish (Gar Bu)":
			case "Gartley, bullish":
				return 29;
			case "High & tight flag (HTF)":
			case "Flag, high and tight":
				return 95;
			case "Head-and-shoulders bottom (HSB)":
			case "Head-and-shoulders bottom":
				return 94;
			case "Complex head-and-shoulders bottom (cHSB)":
			case "Head-and-shoulders complex bottom":
				return 93;
			case "Complex head-and-shoulders top (cHST)":
			case "Head-and-shoulders complex top":
				return 108;
			case "Head-and-shoulders top (HST)":
			case "Head-and-shoulders top":
				return 107;
			case "Hook reversal, downtrend (HD)":
			case "Hook reversal, downtrend":
				return 50;
			case "Hook reversal, uptrend (HU)":
			case "Hook reversal, uptrend":
				return 49;
			case "Horn bottom (HB)":
			case "Horn bottom":
				return 106;
			case "Horn top (HT)":
			case "Horn top":
				return 105;
			case "Inside day (ID)":
			case "Inside day":
				return 77;
			case "Island reversal, bottom (IRB)":
			case "Island reversal, bottom":
				return 76;
			case "Island reversal, top (IRT)":
			case "Island reversal, top":
				return 75;
			case "Key reversal, downtrend (KD)":
			case "Key reversal, downtrend":
				return 47;
			case "Key reversal, uptrend (KU)":
			case "Key reversal, uptrend":
				return 46;
			case "Measured move down (MMD)":
			case "Measured move down":
				return 74;
			case "Measured move up (MMU)":
			case "Measured move up":
				return 73;
			case "Narrow range 4 (NR4)":
			case "NR4":
				return 72;
			case "Narrow range 7 (NR7)":
			case "NR7":
				return 71;
			case "Open-close reversal, downtrend (o)":
			case "Open-close reversal, downtrend":
				return 45;
			case "Open-close reversal, uptrend (O)":
			case "Open-close reversal, uptrend":
				return 44;
			case "One day reversal, bottom (r)":
			case "One day reversal, bottom":
				return 70;
			case "One day reversal, top (R)":
			case "One day reversal, top":
				return 69;
			case "Outside day (OD)":
			case "Outside day":
				return 68;
			case "Pennant (PEN)":
			case "Pennant":
				return 67;
			case "Pipe bottom (PB)":
			case "Pipe bottom":
				return 104;
			case "Pipe top (PT)":
			case "Pipe top":
				return 103;
			case "Pivot point reversal, downtrend (p)":
			case "Pivot point reversal, downtrend":
				return 43;
			case "Pivot point reversal, uptrend (P)":
			case "Pivot point reversal, uptrend":
				return 42;
			case "Pothole":
				return 37;
			case "Rectangle bottom (RB)":
			case "Rectangle bottom":
				return 102;
			case "Rectangle top (RT)":
			case "Rectangle top":
				return 101;
			case "Rising wedge (RW)":
			case "Rising wedge":
				return 92;
			case "Roof (Ro)":
			case "Roof":
				return 36;
			case "Roof, inverted (iR)":
			case "Roof, inverted":
				return 35;
			case "Rounding bottom (RoundB)":
			case "Rounding bottom":
				return 66;
			case "Rounding top (RoundT)":
			case "Rounding top":
				return 65;
			case "Shark-32 (S32)":
			case "Shark-32":
				return 60;
			case "Spike down (s)":
			case "Spike down":
				return 40;
			case "Spike up (S)":
			case "Spike up":
				return 41;
			case "Three bar (3Bar)":
			case "Three bar":
				return 59;
			case "Three falling peaks (3FP)":
			case "Three falling peaks":
				return 91;
			case "Three LR (3L-R)":
			case "Three LR":
				return 32;
			case "Three LR, inverted (i3LR)":
			case "Three LR inverted":
				return 31;
			case "Three rising valleys (3RV)":
			case "Three rising valleys":
				return 90;
			case "Ascending triangle (AscT)":
			case "Triangle, ascending":
				return 89;
			case "Descending triangle (DesT)":
			case "Triangle, descending":
				return 88;
			case "Symmetrical triangle (SymT)":
			case "Triangle, symmetrical":
				return 87;
			case "Trendline, down":
				return 58;
			case "Trendline, up":
				return 57;
			case "Triple bottom (B)":
			case "Triple bottom":
				return 86;
			case "Triple top (T)":
			case "Triple top":
				return 85;
			case "2-Dance (2D)":
			case "2-Dance":
				return 0;
			case "2-Did (2Did)":
			case "2-Did":
				return 23;
			case "2-Tall (2T)":
			case "2-Tall":
				return 22;
			case "Ugly double bottom (UDB)":
			case "Ugly double bottom":
				return 34;
			case "Ugly double top (UDT)":
			case "Ugly double top":
				return 33;
			case "Vertical run down (VRD)":
			case "Vertical run down":
				return 24;
			case "Vertical run up (VRU)":
			case "Vertical run up":
				return 25;
			case "V-bottom":
				return 56;
			case "V-top":
				return 55;
			case "Weekly reversal top":
				return 53;
			case "Weekly reversal bottom":
				return 54;
			case "Wide ranging day, upside reversal (W)":
			case "Wide ranging day, upside reversal":
				return 38;
			case "Wide ranging day, downside reversal (w)":
			case "Wide ranging day, downside reversal":
				return 39;
			case "Wolfe wave, bearish (WW Be)":
			case "Wolfe wave, bearish":
				return 27;
			case "Wolfe wave, bullish (WW Bu)":
			case "Wolfe wave, bullish":
				return 26;
			default:
				return -1;
			}
		}
		return Conversions.ToInteger(PatternName) switch
		{
			4 => "AB=CD, bearish", 
			5 => "AB=CD, bullish", 
			84 => "Bump-and-run reversal, bottom", 
			83 => "Bump-and-run reversal, top", 
			11 => "Bat, bearish", 
			10 => "Bat, bullish", 
			116 => "Big M", 
			115 => "Big W", 
			113 => "Broadening formation, right-angled & ascending", 
			112 => "Broadening formation, right-angled & descending", 
			114 => "Broadening bottom", 
			111 => "Broadening top", 
			110 => "Broadening wedge, ascending", 
			109 => "Broadening wedge, descending", 
			9 => "Butterfly, bearish", 
			8 => "Butterfly, bullish", 
			3 => "Carl V, bearish", 
			2 => "Carl V, bullish", 
			82 => "Channel, down", 
			1 => "Channel, up", 
			52 => "Closing price reversal, downtrend", 
			51 => "Closing price reversal, uptrend", 
			7 => "Crab, bearish", 
			6 => "Crab, bullish", 
			81 => "Cup with handle", 
			48 => "Cup with handle, inverted", 
			100 => "Dead-cat bounce", 
			30 => "Diving board", 
			99 => "Dead-cat bounce, inverted", 
			98 => "Double bottoms (all Types)", 
			20 => "Double bottom, Adam & Adam", 
			21 => "Double bottom, Adam & Eve", 
			18 => "Double bottom, Eve & Adam", 
			19 => "Double bottom, Eve & Eve", 
			97 => "Double tops (all Types)", 
			16 => "Double top, Adam & Adam", 
			17 => "Double top, Adam & Eve", 
			14 => "Double top, Eve & Adam", 
			15 => "Double top, Eve & Eve", 
			12 => "Fakey, bearish", 
			13 => "Fakey, bullish", 
			96 => "Falling wedge", 
			78 => "Flag", 
			122 => "Gap 2H", 
			123 => "Gap 2H, inverted", 
			117 => "Gap, breakaway", 
			118 => "Gap, area or common", 
			119 => "Gap, continuation", 
			121 => "Gap, exhaustion", 
			120 => "Gap, type unknown", 
			28 => "Gartley, bearish", 
			29 => "Gartley, bullish", 
			95 => "Flag, high and tight", 
			94 => "Head-and-shoulders bottom", 
			93 => "Head-and-shoulders complex bottom", 
			108 => "Head-and-shoulders complex top", 
			107 => "Head-and-shoulders top", 
			50 => "Hook reversal, downtrend", 
			49 => "Hook reversal, uptrend", 
			106 => "Horn bottom", 
			105 => "Horn top", 
			77 => "Inside day", 
			76 => "Island reversal, bottom", 
			75 => "Island reversal, top", 
			47 => "Key reversal, downtrend", 
			46 => "Key reversal, uptrend", 
			74 => "Measured move down", 
			73 => "Measured move up", 
			72 => "NR4", 
			71 => "NR7", 
			45 => "Open-close reversal, downtrend", 
			44 => "Open-close reversal, uptrend", 
			70 => "One day reversal, bottom", 
			69 => "One day reversal, top", 
			68 => "Outside day", 
			67 => "Pennant", 
			104 => "Pipe bottom", 
			103 => "Pipe top", 
			43 => "Pivot point reversal, downtrend", 
			42 => "Pivot point reversal, uptrend", 
			37 => "Pothole", 
			102 => "Rectangle bottom", 
			101 => "Rectangle top", 
			92 => "Rising wedge", 
			36 => "Roof", 
			35 => "Roof, inverted", 
			66 => "Rounding bottom", 
			65 => "Rounding top", 
			60 => "Shark-32", 
			40 => "Spike down", 
			41 => "Spike up", 
			59 => "Three bar", 
			91 => "Three falling peaks", 
			32 => "Three LR", 
			31 => "Three LR inverted", 
			90 => "Three rising valleys", 
			58 => "Trendline, down", 
			57 => "Trendline, up", 
			89 => "Triangle, ascending", 
			88 => "Triangle, descending", 
			87 => "Triangle, symmetrical", 
			86 => "Triple bottom", 
			85 => "Triple top", 
			0 => "2-Dance", 
			23 => "2-Did", 
			22 => "2-Tall", 
			34 => "Ugly double bottom", 
			33 => "Ugly double top", 
			56 => "V-bottom", 
			24 => "Vertical run down", 
			25 => "Vertical run up", 
			55 => "V-top", 
			53 => "Weekly reversal top", 
			54 => "Weekly reversal bottom", 
			39 => "Wide ranging day, downside reversal", 
			38 => "Wide ranging day, upside reversal", 
			27 => "Wolfe wave, bearish", 
			26 => "Wolfe wave, bullish", 
			_ => "-1", 
		};
	}

	public static void SetupWindow(Form ThisForm, Point FormLocation, Size FormSize)
	{
		if (!((FormLocation.X == -1) & (FormLocation.Y == -1)))
		{
			ThisForm.StartPosition = (FormStartPosition)0;
			ThisForm.Location = FormLocation;
			ThisForm.Size = FormSize;
		}
	}
}
