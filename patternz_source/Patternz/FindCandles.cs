using System;
using System.Drawing;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Patternz.My;

namespace Patternz;

[StandardModule]
internal sealed class FindCandles
{
	public static byte[] CandleList = new byte[105];

	public static bool CLChanged = false;

	public const int Abandonedbabybear = 104;

	public const int Abandonedbabybull = 103;

	public const int AboveStomach = 102;

	public const int Advanceblock = 101;

	public const int BelowStomach = 100;

	public const int BeltholdBearish = 99;

	public const int BeltholdBullish = 98;

	public const int BreakawayBear = 1;

	public const int BreakawayBull = 0;

	public const int CandleBlack = 97;

	public const int CandleWhite = 88;

	public const int CandleShortBlk = 87;

	public const int CandleShortWht = 86;

	public const int ConcealingBaby = 85;

	public const int DarkCloudCover = 84;

	public const int Deliberation = 83;

	public const int DojiDragonFly = 82;

	public const int DojiFourPrice = 81;

	public const int DojiGappingDn = 96;

	public const int DojiGappingUp = 95;

	public const int DojiGravestone = 94;

	public const int DojiLongLegged = 93;

	public const int DojiNorthern = 92;

	public const int DojiSouthern = 91;

	public const int DojiStarBear = 90;

	public const int DojiStarBull = 89;

	public const int DojiStarCollapse = 80;

	public const int DownsideGap3Methods = 79;

	public const int DownsideTasukiGap = 78;

	public const int EightNewPriceLines = 77;

	public const int EngulfingBearish = 76;

	public const int EngulfingBullish = 75;

	public const int EveningDojiStar = 74;

	public const int EveningStar = 73;

	public const int Falling3Method = 72;

	public const int Hammer = 71;

	public const int HammerInverted = 70;

	public const int HangingMan = 69;

	public const int HaramiBearish = 68;

	public const int HaramiBullish = 67;

	public const int HaramiCrossBearish = 66;

	public const int HaramiCrossBullish = 65;

	public const int HighWave = 64;

	public const int HomingPigeon = 63;

	public const int Identical3Crows = 62;

	public const int InNeckLine = 61;

	public const int KickerBear = 60;

	public const int KickerBull = 59;

	public const int LadderBottom = 58;

	public const int LastEngulfBot = 57;

	public const int LastEngulfTop = 56;

	public const int LongDayBlack = 55;

	public const int LongDayWhite = 54;

	public const int MarubozuBlack = 53;

	public const int MarubozuClosingB = 52;

	public const int MarubozuClosingW = 51;

	public const int MarubozuOpeningB = 50;

	public const int MarubozuOpeningW = 49;

	public const int MarubozuWhite = 48;

	public const int MatHold = 47;

	public const int MatchingLow = 46;

	public const int MeetingLinesBear = 45;

	public const int MeetingLinesBull = 44;

	public const int MorningDojiStar = 43;

	public const int MorningStar = 42;

	public const int OnNeckLine = 41;

	public const int PiercingPattern = 40;

	public const int RickshawMan = 39;

	public const int Rising3method = 38;

	public const int SeparatingLinesBear = 37;

	public const int SeparatingLinesBull = 36;

	public const int ShootingStar = 35;

	public const int ShootingStar2 = 34;

	public const int SBSWLinesBear = 33;

	public const int SBSWLinesBull = 32;

	public const int SpinningTop = 31;

	public const int SpinningTopBlk = 30;

	public const int SpinningTopWht = 29;

	public const int StickSandwich = 28;

	public const int TenNewPriceLines = 27;

	public const int ThirteenNewPriceLines = 26;

	public const int Takuri = 25;

	public const int ThreeBlackCrows = 24;

	public const int ThreeInsideDown = 23;

	public const int ThreeInsideUp = 22;

	public const int ThreeLineStrikeBear = 21;

	public const int ThreeLineStrikeBull = 20;

	public const int ThreeOutsideDown = 19;

	public const int ThreeOutsideUp = 18;

	public const int ThreeStarsSouth = 17;

	public const int ThreeWhiteSoldiers = 16;

	public const int Thrusting = 15;

	public const int TriStarBear = 14;

	public const int TriStarBull = 13;

	public const int TweezersBottom = 12;

	public const int TweezersTop = 11;

	public const int TwelveNewPriceLines = 10;

	public const int TwoBlackGapping = 9;

	public const int TwoCrows = 8;

	public const int Unique3RiverBottom = 7;

	public const int UpsideGap3Method = 6;

	public const int UpsideGap2Crows = 5;

	public const int UpsideTasukiGap = 4;

	public const int WindowFalling = 3;

	public const int WindowRising = 2;

	private const int AVGSIZE = 6;

	private const decimal PERCENT = 0.66m;

	private const decimal NEAR = 0.25m;

	private const decimal TENPERCENT = 0.1m;

	private const int LONGSHADOW = 1;

	private const int BLACKCANDLE = 1;

	private const int WHITECANDLE = 0;

	private const int NOCOLOR = -1;

	private const int LOOKBACK = 3;

	private const int MAOFFSET = 13;

	private const decimal LONGBODY = 1.3m;

	private const decimal DOJI1PCT = 0.01m;

	public const decimal PENNY = 0.01m;

	private static decimal DOJIRANGE = 0.03m;

	public static bool lsShowCandles;

	public static decimal[,] Storage = new decimal[4, 1];

	private static decimal AvgBodyHeight;

	private static decimal AvgUpShadowLen;

	private static decimal AvgDnShadowLen;

	private static decimal PrBodyTop;

	private static decimal PrBodyBottom;

	private static decimal PrHigh;

	private static decimal PrLow;

	private static decimal PrOpen;

	private static decimal PrClose;

	private static bool LongLowerShadow;

	private static bool SmallBodyYesterday;

	private static decimal yDayHigh;

	private static decimal yDayLow;

	private static decimal yDayClose;

	private static decimal yDayOpen;

	private static decimal CandleHeight;

	private static bool SmallBodyToday;

	private static decimal UpperShadowLength;

	private static decimal LowerShadowLength;

	private static decimal BodyHeight;

	private static bool LongUpperShadow;

	private static bool LongBodyToday;

	private static bool TopNear;

	private static bool BottomNear;

	private static int ColorToday;

	private static int ColorYesterday;

	private static bool AtTop;

	private static bool AtBottom;

	private static int Slope;

	private static int Slope1;

	private static int Slope2;

	private static int Slope3;

	private static int Slope4;

	private static int Slope5;

	private static bool LongBodyYesterday;

	private static bool LongCandle;

	private static bool SmallCandle;

	private static bool State;

	private static string PatternName;

	private static decimal TmpPrice;

	private static decimal Tmp2Price;

	private static int Tmp2Index;

	private static int TmpIndex;

	private static decimal Scale;

	public static void GoFindCandles(ref Control Ctrl, string Filename, ref int Row, int Source, ProgressBar FindingBar, ref bool StopPressed)
	{
		DOJIRANGE = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.01m, (object)0.03m));
		if ((Source == 1) & (Row != -1))
		{
			Scale = Conversions.ToDecimal(MyProject.Forms.ListForm.DataGridView1.Rows[Row].Cells[19].Value);
		}
		else if (Source == 0 || Source == 2)
		{
			int num = GlobalForm.ChartStartIndex;
			int num2 = GlobalForm.ChartStartIndex;
			int chartStartIndex = GlobalForm.ChartStartIndex;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = chartStartIndex; i <= chartEndIndex; i = checked(i + 1))
			{
				num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0, (object)i, (object)num));
				num2 = Conversions.ToInteger(Interaction.IIf((decimal.Compare(GlobalForm.nHLC[2, i], 0m) != 0) & (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num2]) < 0), (object)i, (object)num2));
			}
			Scale = decimal.Divide(decimal.Divide(decimal.Add(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num2]), 2m), 100m);
		}
		checked
		{
			Storage = new decimal[4, Information.UBound((Array)GlobalForm.nHLC, 2) + 1];
			int num3 = Information.UBound((Array)GlobalForm.nHLC, 2);
			for (int i = 0; i <= num3; i++)
			{
				Storage[0, i] = GlobalForm.nHLC[0, i];
				Storage[1, i] = GlobalForm.nHLC[1, i];
				Storage[2, i] = GlobalForm.nHLC[2, i];
				Storage[3, i] = GlobalForm.nHLC[3, i];
				if (decimal.Compare(Scale, 0m) != 0)
				{
					ref decimal reference = ref GlobalForm.nHLC[0, i];
					reference = decimal.Divide(reference, Scale);
					ref decimal reference2 = ref GlobalForm.nHLC[1, i];
					reference2 = decimal.Divide(reference2, Scale);
					ref decimal reference3 = ref GlobalForm.nHLC[2, i];
					reference3 = decimal.Divide(reference3, Scale);
					ref decimal reference4 = ref GlobalForm.nHLC[3, i];
					reference4 = decimal.Divide(reference4, Scale);
				}
			}
			int chartStartIndex2 = GlobalForm.ChartStartIndex;
			int chartEndIndex2 = GlobalForm.ChartEndIndex;
			for (int i = chartStartIndex2; i <= chartEndIndex2; i++)
			{
				if (i >= 6)
				{
					NewGoFindCandles(i, ref Ctrl, Filename, ref Row, Source);
					if (!GlobalForm.Quiet && FindingBar != null && unchecked(i % 100) == 0)
					{
						FindingBar.Value = (int)Math.Round((double)(100 * (i - GlobalForm.ChartStartIndex)) / (double)(GlobalForm.ChartEndIndex - GlobalForm.ChartStartIndex));
					}
					if (unchecked(i % 20) == 0)
					{
						((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
					}
					if (StopPressed)
					{
						break;
					}
				}
			}
			int num4 = Information.UBound((Array)GlobalForm.nHLC, 2);
			for (int i = 0; i <= num4; i++)
			{
				GlobalForm.nHLC[0, i] = Storage[0, i];
				GlobalForm.nHLC[1, i] = Storage[1, i];
				GlobalForm.nHLC[2, i] = Storage[2, i];
				GlobalForm.nHLC[3, i] = Storage[3, i];
			}
		}
	}

	public static void NewGoFindCandles(int iEndDate, ref Control Ctrl, string Filename, ref int Row, int Source)
	{
		yDayHigh = default(decimal);
		yDayLow = default(decimal);
		yDayClose = default(decimal);
		yDayOpen = default(decimal);
		int num = checked(iEndDate - 2);
		int startIndex = iEndDate;
		GetCandleDefs(startIndex, iEndDate);
		int num2 = Conversions.ToInteger(Interaction.IIf(ColorToday == 0, (object)48, (object)53));
		if (CandleList[num2] == 1 && (LongBodyToday & (((decimal.Compare(PrHigh, PrOpen) == 0) & (decimal.Compare(PrClose, PrLow) == 0)) | ((decimal.Compare(PrLow, PrOpen) == 0) & (decimal.Compare(PrClose, PrHigh) == 0)))) && ((ColorToday == 0 && num2 == 48) | (ColorToday == 1 && num2 == 53)))
		{
			startIndex = iEndDate;
			PatternName = Conversions.ToString(Interaction.IIf(ColorToday == 0, (object)"White", (object)"Black")) + " marubozu";
			SaveNewCandle(num2, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
		}
		if (CandleList[52] == 1 && (LongBodyToday & (decimal.Compare(PrClose, PrLow) == 0) & (decimal.Compare(PrHigh, PrOpen) != 0) & (ColorToday == 1)))
		{
			startIndex = iEndDate;
			PatternName = "Closing black marubozu";
			SaveNewCandle(52, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
		}
		if (CandleList[51] == 1 && (LongBodyToday & (decimal.Compare(PrClose, PrHigh) == 0) & (decimal.Compare(PrLow, PrOpen) != 0) & (ColorToday == 0)))
		{
			startIndex = iEndDate;
			PatternName = "Closing white marubozu";
			SaveNewCandle(51, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
		}
		if (CandleList[50] == 1 && (LongBodyToday & (decimal.Compare(PrOpen, PrHigh) == 0) & (decimal.Compare(PrLow, PrClose) != 0) & (ColorToday == 1)))
		{
			startIndex = iEndDate;
			PatternName = "Opening black marubozu";
			SaveNewCandle(50, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
		}
		if (CandleList[49] == 1 && (LongBodyToday & (decimal.Compare(PrOpen, PrLow) == 0) & (decimal.Compare(PrHigh, PrClose) != 0) & (ColorToday == 0)))
		{
			startIndex = iEndDate;
			PatternName = "Opening white marubozu";
			SaveNewCandle(49, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
		}
		Check4Highs(77, 8, iEndDate, ref Ctrl, Filename, ref Row, Source);
		Check4Highs(27, 10, iEndDate, ref Ctrl, Filename, ref Row, Source);
		Check4Highs(10, 12, iEndDate, ref Ctrl, Filename, ref Row, Source);
		Check4Highs(26, 13, iEndDate, ref Ctrl, Filename, ref Row, Source);
		checked
		{
			if (iEndDate >= 4)
			{
				startIndex = iEndDate - 4;
				GetCandleDefs(startIndex, iEndDate);
				if (Slope5 < 0)
				{
					if (CandleList[0] == 1)
					{
						TmpIndex = iEndDate - 4;
						GetBodyHeight(TmpIndex);
						if ((LongCandle & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 4], GlobalForm.nHLC[3, iEndDate - 4]) > 0)) && ((decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 3]) > 0) & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 4]) < 0)) && ((decimal.Compare(GlobalForm.nHLC[3, num], GlobalForm.nHLC[3, iEndDate - 3]) < 0) & (decimal.Compare(yDayClose, GlobalForm.nHLC[3, num]) < 0) & (ColorYesterday == 1)) && ((decimal.Compare(GlobalForm.nHLC[1, num], GlobalForm.nHLC[1, iEndDate - 3]) < 0) & (decimal.Compare(yDayHigh, GlobalForm.nHLC[1, num]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, num], GlobalForm.nHLC[2, iEndDate - 3]) < 0) & (decimal.Compare(yDayLow, GlobalForm.nHLC[2, num]) < 0)) && (LongBodyToday & (ColorToday == 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[0, iEndDate - 3]) > 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[3, iEndDate - 4]) < 0)))
						{
							PatternName = "Bullish breakaway";
							SaveNewCandle(0, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[72] == 1)
					{
						TmpIndex = iEndDate - 4;
						GetBodyHeight(TmpIndex);
						if (LongCandle & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 4], GlobalForm.nHLC[3, iEndDate - 4]) > 0))
						{
							TmpIndex = iEndDate - 3;
							GetBodyHeight(TmpIndex);
							if (SmallCandle & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 3]) < 0))
							{
								TmpIndex = num;
								GetBodyHeight(TmpIndex);
								if ((SmallCandle & (ColorYesterday == 0) & SmallBodyYesterday & LongBodyToday & (ColorToday == 1)) && ((decimal.Compare(GlobalForm.nHLC[3, iEndDate - 3], GlobalForm.nHLC[2, iEndDate - 4]) >= 0) & (decimal.Compare(GlobalForm.nHLC[3, iEndDate - 3], GlobalForm.nHLC[1, iEndDate - 4]) <= 0) & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[2, iEndDate - 4]) >= 0) & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[1, iEndDate - 4]) <= 0)) && ((decimal.Compare(GlobalForm.nHLC[3, num], GlobalForm.nHLC[2, iEndDate - 4]) >= 0) & (decimal.Compare(GlobalForm.nHLC[3, num], GlobalForm.nHLC[1, iEndDate - 4]) <= 0) & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[2, iEndDate - 4]) >= 0) & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[1, iEndDate - 4]) <= 0)) && ((decimal.Compare(yDayClose, GlobalForm.nHLC[2, iEndDate - 4]) >= 0) & (decimal.Compare(yDayClose, GlobalForm.nHLC[1, iEndDate - 4]) <= 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[2, iEndDate - 4]) >= 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[1, iEndDate - 4]) <= 0)) && decimal.Compare(PrClose, GlobalForm.nHLC[3, iEndDate - 4]) < 0 && ((decimal.Compare(GlobalForm.nHLC[3, iEndDate - 3], GlobalForm.nHLC[3, num]) < 0) & (decimal.Compare(GlobalForm.nHLC[3, num], yDayClose) < 0)))
								{
									PatternName = "Falling 3 methods";
									SaveNewCandle(72, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
								}
							}
						}
					}
					if (CandleList[58] == 1)
					{
						TmpIndex = iEndDate - 4;
						GetBodyHeight(TmpIndex);
						if (LongCandle & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 4], GlobalForm.nHLC[3, iEndDate - 4]) > 0))
						{
							TmpIndex = iEndDate - 3;
							GetBodyHeight(TmpIndex);
							if (LongCandle & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 3]) > 0) & (decimal.Compare(GlobalForm.nHLC[3, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 4]) < 0) & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[0, iEndDate - 4]) < 0))
							{
								TmpIndex = iEndDate - 2;
								GetBodyHeight(TmpIndex);
								if ((LongCandle & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 2], GlobalForm.nHLC[3, iEndDate - 2]) > 0) & (decimal.Compare(GlobalForm.nHLC[3, iEndDate - 2], GlobalForm.nHLC[3, iEndDate - 3]) < 0) & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 2], GlobalForm.nHLC[0, iEndDate - 3]) < 0)) && ((ColorYesterday == 1) & (decimal.Compare(yDayHigh, yDayOpen) > 0)) && ((decimal.Compare(PrOpen, yDayOpen) > 0) & (ColorToday == 0)))
								{
									PatternName = "Ladder bottom";
									SaveNewCandle(58, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
								}
							}
						}
					}
				}
				else if (Slope5 > 0)
				{
					if (CandleList[1] == 1)
					{
						TmpIndex = iEndDate - 4;
						GetBodyHeight(TmpIndex);
						if ((LongCandle & (decimal.Compare(GlobalForm.nHLC[3, iEndDate - 4], GlobalForm.nHLC[0, iEndDate - 4]) > 0)) && ((decimal.Compare(GlobalForm.nHLC[3, iEndDate - 3], GlobalForm.nHLC[0, iEndDate - 3]) > 0) & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 4]) > 0)) && ((decimal.Compare(GlobalForm.nHLC[3, num], GlobalForm.nHLC[3, iEndDate - 3]) > 0) & (decimal.Compare(yDayClose, GlobalForm.nHLC[3, num]) > 0)) && ((decimal.Compare(GlobalForm.nHLC[1, num], GlobalForm.nHLC[1, iEndDate - 3]) > 0) & (decimal.Compare(yDayHigh, GlobalForm.nHLC[1, num]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, num], GlobalForm.nHLC[2, iEndDate - 3]) > 0) & (decimal.Compare(yDayLow, GlobalForm.nHLC[2, num]) > 0)) && (LongBodyToday & (ColorToday == 1) & (ColorYesterday == 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[0, iEndDate - 3]) < 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[3, iEndDate - 4]) > 0)))
						{
							PatternName = "Bearish breakaway";
							SaveNewCandle(1, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[47] == 1)
					{
						TmpIndex = iEndDate - 4;
						GetBodyHeight(TmpIndex);
						if (LongCandle & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 4], GlobalForm.nHLC[3, iEndDate - 4]) < 0))
						{
							TmpIndex = iEndDate - 3;
							GetBodyHeight(TmpIndex);
							if ((SmallCandle & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 4]) > 0) & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 3]) > 0) & (decimal.Compare(GlobalForm.nHLC[3, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 4]) > 0)) && decimal.Compare(GlobalForm.nHLC[3, num], GlobalForm.nHLC[1, iEndDate - 4]) < 0 && ((decimal.Compare(GlobalForm.nHLC[3, num], GlobalForm.nHLC[3, iEndDate - 3]) <= 0) & (decimal.Compare(yDayClose, GlobalForm.nHLC[3, num]) <= 0)) && ((decimal.Compare(GlobalForm.nHLC[3, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 4]) > 0) & (decimal.Compare(GlobalForm.nHLC[3, num], GlobalForm.nHLC[2, iEndDate - 4]) > 0) & (decimal.Compare(yDayClose, GlobalForm.nHLC[2, iEndDate - 4]) > 0)))
							{
								decimal num3 = GlobalForm.nHLC[1, iEndDate - 4];
								num3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num3, GlobalForm.nHLC[1, iEndDate - 3]) < 0, (object)GlobalForm.nHLC[1, iEndDate - 3], (object)num3));
								num3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num3, GlobalForm.nHLC[1, num]) < 0, (object)GlobalForm.nHLC[1, num], (object)num3));
								num3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num3, yDayHigh) < 0, (object)yDayHigh, (object)num3));
								if ((ColorToday == 0) & (decimal.Compare(PrClose, num3) > 0) & (ColorYesterday == 1))
								{
									PatternName = "Mat hold";
									SaveNewCandle(47, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
								}
							}
						}
					}
					if (CandleList[38] == 1)
					{
						TmpIndex = iEndDate - 4;
						GetBodyHeight(TmpIndex);
						if (LongCandle & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 4], GlobalForm.nHLC[3, iEndDate - 4]) < 0))
						{
							TmpIndex = iEndDate - 3;
							GetBodyHeight(TmpIndex);
							if (SmallCandle & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 3]) > 0))
							{
								TmpIndex = num;
								GetBodyHeight(TmpIndex);
								if ((SmallCandle & SmallBodyYesterday & (ColorYesterday == 1) & LongBodyToday & (ColorToday == 0)) && ((decimal.Compare(GlobalForm.nHLC[3, iEndDate - 3], GlobalForm.nHLC[2, iEndDate - 4]) >= 0) & (decimal.Compare(GlobalForm.nHLC[3, iEndDate - 3], GlobalForm.nHLC[1, iEndDate - 4]) <= 0) & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[2, iEndDate - 4]) >= 0) & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[1, iEndDate - 4]) <= 0)) && ((decimal.Compare(GlobalForm.nHLC[3, num], GlobalForm.nHLC[2, iEndDate - 4]) >= 0) & (decimal.Compare(GlobalForm.nHLC[3, num], GlobalForm.nHLC[1, iEndDate - 4]) <= 0) & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[2, iEndDate - 4]) >= 0) & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[1, iEndDate - 4]) <= 0)) && ((decimal.Compare(yDayClose, GlobalForm.nHLC[2, iEndDate - 4]) >= 0) & (decimal.Compare(yDayClose, GlobalForm.nHLC[1, iEndDate - 4]) <= 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[2, iEndDate - 4]) >= 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[1, iEndDate - 4]) <= 0)) && decimal.Compare(PrClose, GlobalForm.nHLC[3, iEndDate - 4]) > 0 && ((decimal.Compare(GlobalForm.nHLC[3, iEndDate - 3], GlobalForm.nHLC[3, num]) > 0) & (decimal.Compare(GlobalForm.nHLC[3, num], yDayClose) > 0)))
								{
									PatternName = "Rising 3 methods";
									SaveNewCandle(38, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
								}
							}
						}
					}
				}
			}
			if (iEndDate >= 3)
			{
				startIndex = iEndDate - 3;
				GetCandleDefs(startIndex, iEndDate);
				if (Slope4 < 0)
				{
					if (CandleList[85] == 1)
					{
						TmpIndex = iEndDate - 3;
						GetBodyHeight(TmpIndex);
						if (LongCandle & (decimal.Compare(GlobalForm.nHLC[1, iEndDate - 3], GlobalForm.nHLC[0, iEndDate - 3]) == 0) & (decimal.Compare(GlobalForm.nHLC[2, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 3]) == 0) & (decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 3]) > 0))
						{
							TmpIndex = num;
							GetBodyHeight(TmpIndex);
							if ((LongCandle & (decimal.Compare(GlobalForm.nHLC[1, num], GlobalForm.nHLC[0, num]) == 0) & (decimal.Compare(GlobalForm.nHLC[2, num], GlobalForm.nHLC[3, num]) == 0) & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) > 0)) && ((decimal.Compare(yDayOpen, GlobalForm.nHLC[3, num]) < 0) & (ColorYesterday == 1) & (decimal.Compare(yDayHigh, GlobalForm.nHLC[3, num]) >= 0)) && ((ColorToday == 1) & (decimal.Compare(PrLow, yDayLow) <= 0) & (decimal.Compare(PrHigh, yDayHigh) >= 0)))
							{
								PatternName = "Concealing baby swallow";
								SaveNewCandle(85, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
							}
						}
					}
					if (CandleList[21] == 1 && ((decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 3]) > 0) & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) > 0) & (ColorYesterday == 1) & (ColorToday == 0)) && ((decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, iEndDate - 3]) >= 0) & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[0, iEndDate - 3]) <= 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[3, num]) >= 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[0, num]) <= 0)) && ((decimal.Compare(GlobalForm.nHLC[3, num], GlobalForm.nHLC[3, iEndDate - 3]) < 0) & (decimal.Compare(yDayClose, GlobalForm.nHLC[3, num]) < 0)) && ((decimal.Compare(PrOpen, yDayLow) < 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[0, iEndDate - 3]) > 0)))
					{
						PatternName = "Bearish 3 line strike";
						SaveNewCandle(21, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
				}
				else if (Slope4 > 0 && CandleList[20] == 1 && ((decimal.Compare(GlobalForm.nHLC[0, iEndDate - 3], GlobalForm.nHLC[3, iEndDate - 3]) < 0) & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) < 0) & (ColorYesterday == 0) & (ColorToday == 1)) && ((decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, iEndDate - 3]) <= 0) & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[0, iEndDate - 3]) >= 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[3, num]) <= 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[0, num]) >= 0)) && ((decimal.Compare(GlobalForm.nHLC[3, num], GlobalForm.nHLC[3, iEndDate - 3]) > 0) & (decimal.Compare(yDayClose, GlobalForm.nHLC[3, num]) > 0)) && ((decimal.Compare(PrOpen, yDayHigh) > 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[0, iEndDate - 3]) < 0)))
				{
					PatternName = "Bullish 3 line strike";
					SaveNewCandle(20, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
				}
			}
			if (iEndDate >= 2)
			{
				startIndex = num;
				GetCandleDefs(startIndex, iEndDate);
				bool LongUpShadow = default(bool);
				bool LongDnShadow = default(bool);
				if (Slope3 > 0)
				{
					if (CandleList[104] == 1 && decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) < 0)
					{
						TmpIndex = iEndDate - 1;
						if (WithinRange(TmpIndex) & (decimal.Compare(yDayLow, GlobalForm.nHLC[1, num]) > 0) & (decimal.Compare(yDayLow, PrHigh) > 0) & (ColorToday == 1))
						{
							PatternName = "Bearish abandoned baby";
							SaveNewCandle(104, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[101] == 1 && ((decimal.Compare(GlobalForm.nHLC[3, num], yDayClose) < 0) & (decimal.Compare(yDayClose, PrClose) < 0)) && ((decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) < 0) & (ColorYesterday == 0) & (ColorToday == 0)) && ((decimal.Compare(yDayOpen, GlobalForm.nHLC[0, num]) >= 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[3, num]) <= 0) & (decimal.Compare(PrOpen, yDayOpen) >= 0) & (decimal.Compare(PrOpen, yDayClose) <= 0)))
					{
						TmpIndex = iEndDate - 1;
						GetShadows(TmpIndex, ref LongUpShadow, ref LongDnShadow);
						if (LongUpShadow & LongUpperShadow)
						{
							PatternName = "Advance block";
							SaveNewCandle(101, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[80] == 1 && ((decimal.Compare(GlobalForm.nHLC[3, num], GlobalForm.nHLC[0, num]) > 0) & (ColorToday == 1)))
					{
						TmpIndex = iEndDate - 1;
						if (WithinRange(TmpIndex) && ((decimal.Compare(GlobalForm.nHLC[2, num], yDayHigh) > 0) & (decimal.Compare(yDayLow, PrHigh) > 0)))
						{
							PatternName = "Collapsing doji star";
							SaveNewCandle(80, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[83] == 1)
					{
						TmpIndex = iEndDate - 2;
						GetBodyHeight(TmpIndex);
						if ((LongCandle & LongBodyYesterday) && ((decimal.Compare(GlobalForm.nHLC[3, num], yDayClose) < 0) & (decimal.Compare(yDayClose, PrClose) < 0) & (decimal.Compare(GlobalForm.nHLC[0, num], yDayOpen) < 0) & (decimal.Compare(yDayOpen, PrOpen) < 0)) && ((decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) < 0) & (ColorYesterday == 0) & (ColorToday == 0)) && decimal.Compare(decimal.Subtract(yDayHigh, yDayLow), 0m) != 0 && (SmallBodyToday & (decimal.Compare(decimal.Divide(decimal.Subtract(PrOpen, yDayClose), decimal.Subtract(yDayHigh, yDayLow)), 0.25m) <= 0)))
						{
							PatternName = "Deliberation";
							SaveNewCandle(83, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if ((CandleList[24] == 1) | (CandleList[62] == 1))
					{
						TmpIndex = num;
						GetBodyHeight(TmpIndex);
						if ((LongCandle & LongBodyYesterday & LongBodyToday) && ((decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) > 0) & (ColorYesterday == 1) & (ColorToday == 1)) && ((decimal.Compare(yDayClose, GlobalForm.nHLC[2, num]) < 0) & (decimal.Compare(PrClose, yDayLow) < 0)) && ((decimal.Compare(decimal.Subtract(GlobalForm.nHLC[3, num], GlobalForm.nHLC[2, num]), decimal.Multiply(0.25m, decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num]))) <= 0) & (decimal.Compare(decimal.Subtract(yDayClose, yDayLow), decimal.Multiply(0.25m, decimal.Subtract(yDayHigh, yDayLow))) <= 0) & (decimal.Compare(decimal.Subtract(PrClose, PrLow), decimal.Multiply(0.25m, CandleHeight)) <= 0)))
						{
							if (CandleList[62] == 1)
							{
								decimal d = Math.Abs(decimal.Subtract(yDayOpen, GlobalForm.nHLC[3, num]));
								decimal d2 = decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, iEndDate - 1]);
								if ((decimal.Compare(decimal.Divide(d, d2), 0.01m) < 0) | (decimal.Compare(d, DOJIRANGE) <= 0))
								{
									d = Math.Abs(decimal.Subtract(PrOpen, yDayClose));
									d2 = decimal.Subtract(yDayHigh, PrLow);
									if ((decimal.Compare(decimal.Divide(d, d2), 0.01m) < 0) | (decimal.Compare(d, DOJIRANGE) <= 0))
									{
										PatternName = "Identical 3 crows";
										SaveNewCandle(62, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
									}
								}
							}
							if ((decimal.Compare(yDayOpen, GlobalForm.nHLC[3, num]) >= 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[0, num]) <= 0) & (decimal.Compare(PrOpen, yDayClose) >= 0) & (decimal.Compare(PrOpen, yDayOpen) <= 0) & (CandleList[24] == 1))
							{
								PatternName = "3 black crows";
								SaveNewCandle(24, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
							}
						}
					}
					if (decimal.Compare(GlobalForm.nHLC[3, num], GlobalForm.nHLC[0, num]) > 0)
					{
						TmpIndex = num;
						GetBodyHeight(TmpIndex);
						if (LongCandle & SmallBodyYesterday & LongBodyToday)
						{
							decimal d3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[0, iEndDate - 1], GlobalForm.nHLC[3, iEndDate - 1]) < 0, (object)GlobalForm.nHLC[0, iEndDate - 1], (object)GlobalForm.nHLC[3, iEndDate - 1]));
							if (decimal.Compare(d3, GlobalForm.nHLC[3, num]) > 0 && ((ColorToday == 1) & (decimal.Compare(d3, PrOpen) > 0)) && decimal.Compare(PrClose, decimal.Divide(decimal.Add(GlobalForm.nHLC[3, num], GlobalForm.nHLC[0, num]), 2m)) <= 0)
							{
								TmpIndex = iEndDate - 1;
								num2 = Conversions.ToInteger(Interaction.IIf(WithinRange(TmpIndex), (object)74, (object)73));
								if (CandleList[num2] == 1)
								{
									PatternName = "Evening" + Conversions.ToString(Interaction.IIf(num2 == 73, (object)"", (object)" doji")) + " star";
									SaveNewCandle(num2, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
								}
							}
						}
					}
					if (CandleList[32] == 1 && ((decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) < 0) & (ColorYesterday == 0) & (ColorToday == 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[3, num]) > 0) & (decimal.Compare(PrOpen, GlobalForm.nHLC[3, num]) > 0)) && ((decimal.Compare(Math.Abs(decimal.Subtract(yDayClose, PrClose)), decimal.Multiply(decimal.Divide(0.25m, 2m), decimal.Subtract(PrHigh, PrLow))) <= 0) & (decimal.Compare(Math.Abs(decimal.Subtract(yDayOpen, PrOpen)), decimal.Multiply(0.05m, decimal.Subtract(PrHigh, PrLow))) <= 0)))
					{
						PatternName = "Bullish side-by-side white lines";
						SaveNewCandle(32, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[23] == 1)
					{
						Slope = Slope3;
						TmpIndex = iEndDate - 2;
						State = true;
						if (VerifyHarami(ref TmpIndex) & (decimal.Compare(PrClose, yDayClose) < 0))
						{
							PatternName = "3 Inside down";
							SaveNewCandle(23, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[19] == 1 && ((decimal.Compare(yDayOpen, GlobalForm.nHLC[3, num]) >= 0) & (decimal.Compare(yDayClose, GlobalForm.nHLC[0, num]) <= 0) & ((decimal.Compare(yDayOpen, GlobalForm.nHLC[3, num]) != 0) | (decimal.Compare(yDayClose, GlobalForm.nHLC[0, num]) != 0))) && ((decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) < 0) & (ColorYesterday == 1) & (decimal.Compare(PrClose, yDayClose) < 0)))
					{
						PatternName = "3 outside down";
						SaveNewCandle(19, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[14] == 1)
					{
						TmpIndex = num;
						if (WithinRange(TmpIndex))
						{
							TmpIndex = iEndDate - 1;
							if (WithinRange(TmpIndex))
							{
								TmpIndex = iEndDate;
								if ((WithinRange(TmpIndex) & (decimal.Compare(PrHigh, PrLow) != 0) & (decimal.Compare(yDayHigh, yDayLow) != 0) & (decimal.Compare(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num]) != 0)) && ((decimal.Compare(yDayClose, GlobalForm.nHLC[3, num]) > 0) & (decimal.Compare(yDayClose, PrClose) > 0)))
								{
									PatternName = "Bearish tri-star";
									SaveNewCandle(14, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
								}
							}
						}
					}
					if (CandleList[8] == 1)
					{
						TmpIndex = num;
						GetBodyHeight(TmpIndex);
						if ((LongCandle & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) < 0) & (ColorYesterday == 1) & (ColorToday == 1)) && ((decimal.Compare(yDayClose, GlobalForm.nHLC[3, num]) > 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[1, num]) > 0) & (decimal.Compare(PrOpen, yDayOpen) <= 0) & (decimal.Compare(PrOpen, yDayClose) >= 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[0, num]) >= 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[3, num]) <= 0)))
						{
							PatternName = "Two crows";
							SaveNewCandle(8, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[6] == 1)
					{
						TmpIndex = num;
						GetBodyHeight(TmpIndex);
						if ((LongCandle & LongBodyYesterday & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) < 0) & (ColorYesterday == 0) & (ColorToday == 1)) && ((decimal.Compare(GlobalForm.nHLC[1, num], yDayLow) < 0) & (decimal.Compare(PrOpen, yDayOpen) >= 0) & (decimal.Compare(PrOpen, yDayClose) <= 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[3, num]) <= 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[0, num]) >= 0)))
						{
							PatternName = "Upside gap 3 methods";
							SaveNewCandle(6, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[5] == 1)
					{
						TmpIndex = num;
						GetBodyHeight(TmpIndex);
						if ((LongCandle & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) < 0) & (ColorYesterday == 1) & (ColorToday == 1)) && ((decimal.Compare(GlobalForm.nHLC[3, num], yDayClose) < 0) & (decimal.Compare(PrOpen, yDayOpen) >= 0) & (decimal.Compare(PrClose, yDayClose) <= 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[3, num]) > 0)))
						{
							PatternName = "Upside gap 2 crows";
							SaveNewCandle(5, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[4] == 1 && ((decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) < 0) & (ColorYesterday == 0) & (ColorToday == 1)) && ((decimal.Compare(GlobalForm.nHLC[1, num], yDayLow) < 0) & (decimal.Compare(PrOpen, yDayClose) <= 0) & (decimal.Compare(PrOpen, yDayOpen) >= 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[1, num]) > 0) & (decimal.Compare(PrClose, yDayLow) < 0)))
					{
						PatternName = "Upside Tasuki gap";
						SaveNewCandle(4, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
				}
				else if (Slope3 < 0)
				{
					if (CandleList[103] == 1 && decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) > 0)
					{
						TmpIndex = iEndDate - 1;
						if (WithinRange(TmpIndex) & (decimal.Compare(yDayHigh, GlobalForm.nHLC[2, num]) < 0) & (decimal.Compare(yDayHigh, PrLow) < 0) & (ColorToday == 0))
						{
							PatternName = "Bullish abandoned baby";
							SaveNewCandle(103, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[79] == 1)
					{
						TmpIndex = num;
						GetBodyHeight(TmpIndex);
						if ((LongCandle & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) > 0)) && (LongBodyYesterday & (ColorYesterday == 1) & (decimal.Compare(GlobalForm.nHLC[2, num], yDayHigh) > 0)) && ((ColorToday == 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[3, num]) >= 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[0, num]) <= 0) & (decimal.Compare(PrOpen, yDayOpen) <= 0) & (decimal.Compare(PrOpen, yDayClose) >= 0)))
						{
							PatternName = "Downside gap 3 methods";
							SaveNewCandle(79, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[78] == 1 && ((decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) > 0) & (ColorYesterday == 1) & (ColorToday == 0)) && decimal.Compare(GlobalForm.nHLC[2, num], yDayHigh) > 0 && ((decimal.Compare(PrOpen, yDayClose) >= 0) & (decimal.Compare(PrOpen, yDayOpen) <= 0) & (decimal.Compare(PrClose, yDayOpen) > 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[2, num]) < 0)))
					{
						PatternName = "Downside Tasuki gap";
						SaveNewCandle(78, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[16] == 1)
					{
						TmpIndex = num;
						GetBodyHeight(TmpIndex);
						if ((LongCandle & LongBodyYesterday & LongBodyToday) && ((decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) < 0) & (ColorYesterday == 0) & (ColorToday == 0)) && ((decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[3, num]), decimal.Multiply(0.25m, decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num]))) <= 0) & (decimal.Compare(decimal.Subtract(yDayHigh, yDayClose), decimal.Multiply(0.25m, decimal.Subtract(yDayHigh, yDayLow))) <= 0) & (decimal.Compare(decimal.Subtract(PrHigh, PrClose), decimal.Multiply(0.25m, CandleHeight)) <= 0)) && ((decimal.Compare(yDayOpen, GlobalForm.nHLC[3, num]) <= 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[0, num]) >= 0) & (decimal.Compare(PrOpen, yDayClose) <= 0) & (decimal.Compare(PrOpen, yDayOpen) >= 0)) && ((decimal.Compare(yDayHigh, GlobalForm.nHLC[1, num]) > 0) & (decimal.Compare(PrHigh, yDayHigh) > 0)))
						{
							PatternName = "3 white soldiers";
							SaveNewCandle(16, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (((CandleList[42] == 1) | (CandleList[43] == 1)) && decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) > 0)
					{
						TmpIndex = num;
						GetBodyHeight(TmpIndex);
						if (LongCandle & SmallBodyYesterday & LongBodyToday)
						{
							decimal d4 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[0, iEndDate - 1], GlobalForm.nHLC[3, iEndDate - 1]) > 0, (object)GlobalForm.nHLC[0, iEndDate - 1], (object)GlobalForm.nHLC[3, iEndDate - 1]));
							if (decimal.Compare(d4, GlobalForm.nHLC[3, num]) < 0 && ((ColorToday == 0) & (decimal.Compare(d4, PrOpen) < 0)) && decimal.Compare(PrClose, decimal.Divide(decimal.Add(GlobalForm.nHLC[3, num], GlobalForm.nHLC[0, num]), 2m)) >= 0)
							{
								TmpIndex = iEndDate - 1;
								num2 = Conversions.ToInteger(Interaction.IIf(WithinRange(TmpIndex), (object)43, (object)42));
								if (CandleList[num2] == 1)
								{
									PatternName = "Morning " + Conversions.ToString(Interaction.IIf(num2 == 42, (object)"star", (object)"doji star"));
									SaveNewCandle(num2, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
								}
							}
						}
					}
					if (CandleList[18] == 1 && ((decimal.Compare(yDayOpen, GlobalForm.nHLC[3, num]) <= 0) & (decimal.Compare(yDayClose, GlobalForm.nHLC[0, num]) >= 0) & ((decimal.Compare(yDayOpen, GlobalForm.nHLC[3, num]) != 0) | (decimal.Compare(yDayClose, GlobalForm.nHLC[0, num]) != 0))) && ((decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) > 0) & (ColorYesterday == 0) & (decimal.Compare(PrClose, yDayClose) > 0)))
					{
						PatternName = "3 outside up";
						SaveNewCandle(18, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[33] == 1 && ((decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) > 0) & (ColorYesterday == 0) & (ColorToday == 0) & (decimal.Compare(yDayClose, GlobalForm.nHLC[3, num]) < 0) & (decimal.Compare(PrClose, GlobalForm.nHLC[3, num]) < 0)) && ((decimal.Compare(Math.Abs(decimal.Subtract(yDayClose, PrClose)), decimal.Multiply(decimal.Divide(0.25m, 2m), decimal.Subtract(PrHigh, PrLow))) <= 0) & (decimal.Compare(Math.Abs(decimal.Subtract(yDayOpen, PrOpen)), decimal.Multiply(0.05m, decimal.Subtract(PrHigh, PrLow))) <= 0)))
					{
						PatternName = "Bearish side-by-side white lines";
						SaveNewCandle(33, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[28] == 1)
					{
						TmpPrice = GlobalForm.nHLC[3, num];
						Tmp2Price = PrClose;
						TmpIndex = iEndDate - 2;
						Tmp2Index = iEndDate;
						if (WithinNear() & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) > 0) & (ColorYesterday == 0) & (decimal.Compare(yDayLow, GlobalForm.nHLC[3, num]) > 0) & (ColorToday == 1))
						{
							PatternName = "Stick sandwich";
							SaveNewCandle(28, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if ((CandleList[22] == 1) & (decimal.Compare(PrClose, yDayClose) > 0))
					{
						Slope = Slope3;
						TmpIndex = iEndDate - 2;
						State = true;
						if (VerifyHarami(ref TmpIndex))
						{
							PatternName = "3 Inside up";
							SaveNewCandle(22, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[17] == 1)
					{
						TmpIndex = num;
						GetBodyHeight(TmpIndex);
						GetShadows(TmpIndex, ref LongUpShadow, ref LongDnShadow);
						if (unchecked((LongCandle & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) > 0)) && LongDnShadow) && ((ColorYesterday == 1) & (decimal.Compare(yDayHigh, GlobalForm.nHLC[1, num]) <= 0) & (decimal.Compare(yDayLow, GlobalForm.nHLC[2, num]) > 0)) && ((decimal.Compare(PrHigh, yDayHigh) < 0) & (decimal.Compare(PrLow, yDayLow) > 0) & (decimal.Compare(PrHigh, PrOpen) == 0) & (decimal.Compare(PrClose, PrLow) == 0)))
						{
							PatternName = "3 Stars in the south";
							SaveNewCandle(17, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[13] == 1)
					{
						TmpIndex = num;
						if (WithinRange(TmpIndex))
						{
							TmpIndex = iEndDate - 1;
							if (WithinRange(TmpIndex))
							{
								TmpIndex = iEndDate;
								if ((WithinRange(TmpIndex) & (decimal.Compare(PrHigh, PrLow) != 0) & (decimal.Compare(yDayHigh, yDayLow) != 0) & (decimal.Compare(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num]) != 0)) && ((decimal.Compare(yDayClose, GlobalForm.nHLC[3, num]) < 0) & (decimal.Compare(yDayClose, PrClose) < 0)))
								{
									PatternName = "Bullish tri-star";
									SaveNewCandle(13, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
								}
							}
						}
					}
					if (CandleList[7] == 1)
					{
						TmpIndex = num;
						GetBodyHeight(TmpIndex);
						if ((LongCandle & (decimal.Compare(GlobalForm.nHLC[0, num], GlobalForm.nHLC[3, num]) > 0) & (ColorYesterday == 1) & (ColorToday == 0)) && ((decimal.Compare(yDayOpen, GlobalForm.nHLC[0, num]) <= 0) & (decimal.Compare(yDayOpen, GlobalForm.nHLC[3, num]) >= 0) & (decimal.Compare(yDayClose, GlobalForm.nHLC[0, num]) <= 0) & (decimal.Compare(yDayClose, GlobalForm.nHLC[3, num]) >= 0) & ((decimal.Compare(yDayClose, GlobalForm.nHLC[3, num]) != 0) | (decimal.Compare(yDayOpen, GlobalForm.nHLC[0, num]) != 0))) && ((decimal.Compare(yDayLow, GlobalForm.nHLC[2, num]) < 0) & (decimal.Compare(yDayLow, PrLow) < 0) & SmallBodyToday & (decimal.Compare(PrClose, yDayClose) < 0) & SmallBodyYesterday))
						{
							PatternName = "Unique 3 river bottom";
							SaveNewCandle(7, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
				}
			}
			if (iEndDate > 0)
			{
				startIndex = iEndDate - 1;
				GetCandleDefs(startIndex, iEndDate);
				if ((decimal.Compare(yDayOpen, yDayClose) != 0) & (decimal.Compare(PrOpen, PrClose) != 0))
				{
					if (CandleList[60] == 1 && ((decimal.Compare(yDayLow, yDayOpen) == 0) & (decimal.Compare(yDayClose, yDayHigh) == 0) & LongBodyYesterday) && (LongBodyToday & (decimal.Compare(PrHigh, PrOpen) == 0) & (decimal.Compare(PrClose, PrLow) == 0) & (decimal.Compare(PrOpen, yDayOpen) < 0)))
					{
						PatternName = "Bearish kicking";
						SaveNewCandle(60, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[59] == 1 && (LongBodyYesterday & (decimal.Compare(yDayLow, yDayClose) == 0) & (decimal.Compare(yDayOpen, yDayHigh) == 0)) && ((decimal.Compare(PrLow, PrOpen) == 0) & (decimal.Compare(PrClose, PrHigh) == 0) & LongBodyToday & (decimal.Compare(PrOpen, yDayOpen) > 0)))
					{
						PatternName = "Bullish kicking";
						SaveNewCandle(59, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
				}
				if (Slope2 < 0)
				{
					if (CandleList[102] == 1 && ((ColorYesterday == 1) & LongBodyYesterday) && ((decimal.Compare(PrOpen, decimal.Divide(decimal.Add(yDayClose, yDayOpen), 2m)) > 0) & (decimal.Compare(PrClose, decimal.Divide(decimal.Add(yDayClose, yDayOpen), 2m)) >= 0)))
					{
						PatternName = "Above the stomach";
						SaveNewCandle(102, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[61] == 1 && ((ColorYesterday == 1) & LongBodyYesterday) && ((ColorToday == 0) & (decimal.Compare(PrOpen, yDayLow) < 0)) && ((decimal.Compare(PrClose, yDayClose) >= 0) & (decimal.Compare(PrClose, decimal.Add(yDayClose, decimal.Multiply(0.05m, decimal.Subtract(yDayOpen, yDayClose)))) <= 0)))
					{
						PatternName = "In neck";
						SaveNewCandle(61, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[63] == 1 && (LongBodyYesterday & (ColorYesterday == 1)) && ((decimal.Compare(PrOpen, yDayOpen) <= 0) & (decimal.Compare(PrClose, yDayClose) >= 0) & (ColorToday == 1) & SmallBodyToday))
					{
						PatternName = "Homing pigeon";
						SaveNewCandle(63, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[70] == 1)
					{
						TmpIndex = iEndDate;
						if (!WithinRange(TmpIndex) && ((ColorYesterday == 1) & LongBodyYesterday & (decimal.Compare(decimal.Subtract(yDayClose, yDayLow), decimal.Multiply(0.25m, decimal.Subtract(yDayHigh, yDayLow))) <= 0)) && decimal.Compare(CandleHeight, 0m) != 0 && (LongUpperShadow & SmallBodyToday & (decimal.Compare(decimal.Divide(LowerShadowLength, CandleHeight), 0.05m) < 0) & (decimal.Compare(PrOpen, yDayClose) < 0)))
						{
							PatternName = "Inverted hammer";
							SaveNewCandle(70, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					Slope = Slope2;
					TmpIndex = iEndDate - 1;
					State = false;
					if (VerifyHarami(ref TmpIndex))
					{
						SaveNewCandle(67, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[46] == 1 && ((ColorYesterday == 1) & LongBodyYesterday) && ((decimal.Compare(PrClose, yDayClose) == 0) & (ColorToday == 1)))
					{
						PatternName = "Matching low";
						SaveNewCandle(46, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[44] == 1 && ((ColorYesterday == 1) & LongBodyYesterday) && (WithinNearEarly(iEndDate) & (ColorToday == 0) & LongBodyToday))
					{
						PatternName = "Bullish meeting lines";
						SaveNewCandle(44, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[41] == 1 && ((ColorYesterday == 1) & LongBodyYesterday) && ((decimal.Compare(PrOpen, yDayLow) < 0) & (decimal.Compare(PrClose, yDayLow) == 0) & (ColorToday == 0)))
					{
						PatternName = "On Neck";
						SaveNewCandle(41, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if ((ColorYesterday == 1) & (ColorToday == 0))
					{
						if (CandleList[40] == 1 && ((decimal.Compare(PrOpen, yDayLow) < 0) & (decimal.Compare(PrClose, decimal.Divide(decimal.Add(yDayOpen, yDayClose), 2m)) >= 0) & (decimal.Compare(PrClose, yDayOpen) <= 0)))
						{
							PatternName = "Piercing pattern";
							SaveNewCandle(40, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
						if (CandleList[75] == 1 && ((decimal.Compare(PrOpen, yDayClose) <= 0) & (decimal.Compare(PrClose, yDayOpen) >= 0) & ((decimal.Compare(PrOpen, yDayClose) != 0) | (decimal.Compare(PrClose, yDayOpen) != 0))))
						{
							PatternName = "Bullish engulfing";
							SaveNewCandle(75, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[57] == 1 && ((ColorYesterday == 0) & (ColorToday == 1)) && ((decimal.Compare(PrOpen, yDayClose) >= 0) & (decimal.Compare(PrClose, yDayOpen) <= 0) & ((decimal.Compare(PrOpen, yDayClose) != 0) | (decimal.Compare(PrClose, yDayOpen) != 0))))
					{
						PatternName = "Last engulfing bottom";
						SaveNewCandle(57, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[37] == 1 && (LongBodyYesterday & (ColorYesterday == 0) & LongBodyToday & (ColorToday == 1)))
					{
						TmpPrice = yDayOpen;
						Tmp2Price = PrOpen;
						TmpIndex = iEndDate - 1;
						Tmp2Index = iEndDate;
						if (WithinNear())
						{
							PatternName = "Bearish separating lines";
							SaveNewCandle(37, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[12] == 1 && (LongBodyYesterday & (ColorYesterday == 1) & (decimal.Compare(PrLow, yDayLow) == 0)))
					{
						PatternName = "Tweezers bottom";
						SaveNewCandle(12, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[15] == 1)
					{
						decimal d5 = decimal.Divide(decimal.Subtract(yDayOpen, yDayClose), 5m);
						if ((ColorYesterday == 1) & (ColorToday == 0) & (decimal.Compare(PrOpen, decimal.Subtract(yDayLow, d5)) <= 0) & (decimal.Compare(PrClose, decimal.Divide(decimal.Add(yDayOpen, yDayClose), 2m)) <= 0) & (decimal.Compare(PrClose, decimal.Add(yDayClose, d5)) >= 0))
						{
							PatternName = "Thrusting";
							SaveNewCandle(15, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[9] == 1 && ((decimal.Compare(GlobalForm.nHLC[2, num], yDayHigh) > 0) & (ColorYesterday == 1) & (ColorToday == 1) & (decimal.Compare(PrHigh, yDayHigh) < 0)))
					{
						PatternName = "2 black gapping";
						SaveNewCandle(9, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[3] == 1 && decimal.Compare(yDayLow, PrHigh) > 0)
					{
						startIndex = iEndDate - 1;
						PatternName = "Falling window";
						SaveNewCandle(3, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					TmpIndex = iEndDate;
					if (WithinRange(TmpIndex) && CandleList[89] == 1 && decimal.Compare(decimal.Add(UpperShadowLength, LowerShadowLength), Math.Abs(decimal.Subtract(yDayOpen, yDayClose))) <= 0 && ((ColorYesterday == 1) & (decimal.Compare(PrOpen, yDayClose) < 0) & (decimal.Compare(PrClose, yDayClose) < 0) & LongBodyYesterday & (decimal.Compare(PrHigh, PrLow) != 0)))
					{
						PatternName = "Bullish doji star";
						SaveNewCandle(89, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
				}
				else if (Slope2 > 0)
				{
					if (CandleList[100] == 1 && ((ColorYesterday == 0) & LongBodyYesterday) && ((decimal.Compare(PrOpen, decimal.Divide(decimal.Add(yDayClose, yDayOpen), 2m)) < 0) & (decimal.Compare(PrClose, decimal.Divide(decimal.Add(yDayClose, yDayOpen), 2m)) <= 0)))
					{
						PatternName = "Below the stomach";
						SaveNewCandle(100, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					Slope = Slope2;
					TmpIndex = iEndDate - 1;
					State = false;
					if (VerifyHarami(ref TmpIndex))
					{
						SaveNewCandle(68, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if ((ColorYesterday == 0) & (ColorToday == 1))
					{
						if (CandleList[84] == 1 && ((decimal.Compare(PrOpen, yDayHigh) > 0) & (decimal.Compare(PrClose, decimal.Divide(decimal.Add(yDayClose, yDayOpen), 2m)) <= 0) & (decimal.Compare(PrClose, yDayOpen) >= 0) & LongBodyYesterday))
						{
							PatternName = "Dark cloud cover";
							SaveNewCandle(84, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
						if (CandleList[76] == 1 && ((decimal.Compare(PrOpen, yDayClose) >= 0) & (decimal.Compare(PrClose, yDayOpen) <= 0) & ((decimal.Compare(PrOpen, yDayClose) != 0) | (decimal.Compare(PrClose, yDayOpen) != 0))))
						{
							PatternName = "Bearish engulfing";
							SaveNewCandle(76, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[56] == 1 && ((ColorYesterday == 1) & (ColorToday == 0)) && ((decimal.Compare(PrOpen, yDayClose) <= 0) & (decimal.Compare(PrClose, yDayOpen) >= 0) & ((decimal.Compare(PrOpen, yDayClose) != 0) | (decimal.Compare(PrClose, yDayOpen) != 0))))
					{
						PatternName = "Last engulfing top";
						SaveNewCandle(56, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[45] == 1 && ((ColorYesterday == 0) & LongBodyYesterday) && (WithinNearEarly(iEndDate) & (ColorToday == 1) & LongBodyToday))
					{
						PatternName = "Bearish meeting lines";
						SaveNewCandle(45, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[36] == 1 && (LongBodyYesterday & (ColorYesterday == 1) & LongBodyToday & (ColorToday == 0)))
					{
						TmpPrice = yDayOpen;
						Tmp2Price = PrOpen;
						TmpIndex = iEndDate - 1;
						Tmp2Index = iEndDate;
						if (WithinNear())
						{
							PatternName = "Bullish separating lines";
							SaveNewCandle(36, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					if (CandleList[11] == 1 && (LongBodyYesterday & (ColorYesterday == 0) & (decimal.Compare(PrHigh, yDayHigh) == 0)))
					{
						PatternName = "Tweezers top";
						SaveNewCandle(11, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[34] == 1 && ((decimal.Compare(yDayClose, PrClose) <= 0) & (decimal.Compare(yDayOpen, PrClose) <= 0)) && (LongUpperShadow & (decimal.Compare(LowerShadowLength, decimal.Multiply(0.05m, CandleHeight)) <= 0) & (decimal.Compare(PrOpen, yDayClose) > 0) & (decimal.Compare(PrClose, yDayClose) > 0) & (ColorYesterday == 0) & (decimal.Compare(UpperShadowLength, decimal.Multiply(3m, BodyHeight)) > 0)))
					{
						PatternName = "Shooting star, 2-candles";
						SaveNewCandle(34, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[2] == 1 && decimal.Compare(PrLow, yDayHigh) > 0)
					{
						startIndex = iEndDate - 1;
						PatternName = "Rising window";
						SaveNewCandle(2, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					TmpIndex = iEndDate;
					if (WithinRange(TmpIndex) && CandleList[90] == 1 && decimal.Compare(decimal.Add(UpperShadowLength, LowerShadowLength), Math.Abs(decimal.Subtract(yDayOpen, yDayClose))) <= 0 && ((ColorYesterday == 0) & (decimal.Compare(PrOpen, yDayClose) > 0) & LongBodyYesterday & (decimal.Compare(PrHigh, PrLow) != 0)))
					{
						PatternName = "Bearish doji star";
						SaveNewCandle(90, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
				}
				startIndex = iEndDate;
				GetCandleDefs(startIndex, iEndDate);
				num2 = Conversions.ToInteger(Interaction.IIf(ColorToday == 0, (object)54, (object)55));
				if (CandleList[num2] == 1 && (!LongUpperShadow & !LongLowerShadow & (decimal.Compare(BodyHeight, decimal.Multiply(3m, AvgBodyHeight)) >= 0)) && unchecked((ColorToday == 0 && num2 == 54) | (ColorToday == 1 && num2 == 55)))
				{
					PatternName = "Long " + Conversions.ToString(Interaction.IIf(ColorToday == 0, (object)"white", (object)"black")) + " day";
					SaveNewCandle(num2, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
				}
			}
			startIndex = iEndDate;
			GetCandleDefs(startIndex, iEndDate);
			TmpIndex = iEndDate;
			if (WithinRange(TmpIndex))
			{
				if (Slope1 != 0 && (((Slope1 < 0) & (CandleList[91] == 1)) | ((Slope1 > 0) & (CandleList[92] == 1))))
				{
					num2 = Conversions.ToInteger(Interaction.IIf(Slope1 < 0, (object)91, (object)92));
					PatternName = Conversions.ToString(Interaction.IIf(Slope1 < 0, (object)"Southern", (object)"Northern")) + " doji";
					SaveNewCandle(num2, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
				}
				if (CandleList[82] == 1 && ((Convert.ToDouble(LowerShadowLength) >= 1.5 * Convert.ToDouble(AvgDnShadowLen)) & (decimal.Compare(LowerShadowLength, AvgBodyHeight) > 0)) && decimal.Compare(CandleHeight, 0m) != 0 && decimal.Compare(decimal.Divide(UpperShadowLength, CandleHeight), 0.01m) < 0)
				{
					PatternName = "Dragonfly doji";
					SaveNewCandle(82, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
				}
				if (CandleList[96] == 1 && ((Slope1 < 0) & (decimal.Compare(PrHigh, yDayLow) < 0)))
				{
					PatternName = "Gapping down doji";
					SaveNewCandle(96, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
				}
				if (CandleList[95] == 1 && ((Slope1 > 0) & (decimal.Compare(PrLow, yDayHigh) > 0)))
				{
					PatternName = "Gapping up doji";
					SaveNewCandle(95, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
				}
				if (CandleList[94] == 1 && ((Convert.ToDouble(UpperShadowLength) >= 1.5 * Convert.ToDouble(AvgUpShadowLen)) & (decimal.Compare(UpperShadowLength, AvgBodyHeight) > 0)) && decimal.Compare(CandleHeight, 0m) != 0 && decimal.Compare(decimal.Divide(LowerShadowLength, CandleHeight), 0.01m) < 0)
				{
					PatternName = "Gravestone doji";
					SaveNewCandle(94, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
				}
				if (((CandleList[93] == 1) | (CandleList[39] == 1)) && ((Convert.ToDouble(UpperShadowLength) > 1.5 * Convert.ToDouble(AvgUpShadowLen)) & (decimal.Compare(UpperShadowLength, AvgBodyHeight) >= 0) & (Convert.ToDouble(LowerShadowLength) > 1.5 * Convert.ToDouble(AvgDnShadowLen)) & (decimal.Compare(LowerShadowLength, AvgBodyHeight) >= 0)))
				{
					if (CandleList[93] == 1)
					{
						PatternName = "Long legged doji";
						SaveNewCandle(93, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (CandleList[39] == 1)
					{
						decimal d6 = decimal.Divide(decimal.Add(PrHigh, PrLow), 2m);
						if (decimal.Compare(Math.Abs(decimal.Subtract(PrOpen, d6)), decimal.Multiply(CandleHeight, 0.1m)) <= 0)
						{
							PatternName = "Rickshaw man";
							SaveNewCandle(39, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
				}
				if (CandleList[81] == 1 && ((decimal.Compare(PrOpen, PrClose) == 0) & (decimal.Compare(PrOpen, PrHigh) == 0) & (decimal.Compare(PrOpen, PrLow) == 0)))
				{
					PatternName = "4 price doji";
					SaveNewCandle(81, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
				}
			}
			else if (SmallBodyToday)
			{
				if (((CandleList[31] == 1) | (CandleList[30] == 1) | (CandleList[29] == 1)) && ((decimal.Compare(UpperShadowLength, BodyHeight) > 0) & (decimal.Compare(LowerShadowLength, BodyHeight) > 0)))
				{
					if (CandleList[31] == 1)
					{
						PatternName = "Spinning top";
						SaveNewCandle(31, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
					if (((ColorToday == 1) & (CandleList[30] == 1)) | ((ColorToday == 0) & (CandleList[29] == 1)))
					{
						num2 = Conversions.ToInteger(Interaction.IIf(ColorToday == 1, (object)30, (object)29));
						PatternName = Conversions.ToString(Interaction.IIf(ColorToday == 1, (object)"Black", (object)"White")) + " spinning top";
						SaveNewCandle(num2, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
					}
				}
				if (CandleList[64] == 1 && ((decimal.Compare(LowerShadowLength, decimal.Multiply(BodyHeight, 3m)) > 0) & (decimal.Compare(UpperShadowLength, decimal.Multiply(BodyHeight, 3m)) > 0) & (decimal.Compare(UpperShadowLength, AvgUpShadowLen) > 0) & (decimal.Compare(LowerShadowLength, AvgDnShadowLen) > 0)))
				{
					PatternName = "High wave";
					SaveNewCandle(64, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
				}
				if (Slope1 != 0)
				{
					if (Slope1 < 0)
					{
						if (CandleList[71] == 1 && decimal.Compare(CandleHeight, 0m) != 0 && (((decimal.Compare(decimal.Divide(UpperShadowLength, CandleHeight), 0.05m) <= 0) | AtTop) & ((decimal.Compare(decimal.Divide(LowerShadowLength, BodyHeight), 2m) >= 0) & (decimal.Compare(decimal.Divide(LowerShadowLength, BodyHeight), 3m) <= 0))))
						{
							PatternName = "Hammer";
							SaveNewCandle(71, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
						if (CandleList[25] == 1 && decimal.Compare(CandleHeight, 0m) != 0 && (((decimal.Compare(decimal.Divide(UpperShadowLength, CandleHeight), 0.05m) <= 0) | AtTop) & (decimal.Compare(decimal.Divide(LowerShadowLength, BodyHeight), 3m) > 0)))
						{
							PatternName = "Takuri line";
							SaveNewCandle(25, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
					else
					{
						if (CandleList[69] == 1 && decimal.Compare(CandleHeight, 0m) != 0 && (((decimal.Compare(decimal.Divide(UpperShadowLength, CandleHeight), 0.05m) <= 0) | AtTop) & LongLowerShadow) && decimal.Compare(decimal.Divide(CandleHeight, new decimal(Conversions.ToInteger(Interaction.IIf(GlobalForm.StrictPatterns, (object)5, (object)4)))), BodyHeight) > 0)
						{
							PatternName = "Hanging man";
							SaveNewCandle(69, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
						if (CandleList[35] == 1 && ((decimal.Compare(yDayClose, PrClose) <= 0) & (decimal.Compare(yDayOpen, PrClose) <= 0)) && (LongUpperShadow & (decimal.Compare(LowerShadowLength, decimal.Multiply(0.05m, CandleHeight)) <= 0) & (decimal.Compare(UpperShadowLength, decimal.Multiply(2m, BodyHeight)) > 0)))
						{
							PatternName = "Shooting star, 1-candle";
							SaveNewCandle(35, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
						}
					}
				}
			}
			if (CandleList[98] == 1 && ((Slope1 < 0) & (decimal.Compare(decimal.Subtract(PrOpen, PrLow), 0m) == 0) & LongBodyToday & TopNear & (ColorToday == 0)))
			{
				PatternName = "Bullish belt hold";
				SaveNewCandle(98, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
			}
			if (CandleList[99] == 1 && ((Slope1 > 0) & (decimal.Compare(decimal.Subtract(PrHigh, PrOpen), 0m) == 0) & LongBodyToday & BottomNear & (ColorToday == 1)))
			{
				PatternName = "Bearish belt hold";
				SaveNewCandle(99, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
			}
			num2 = Conversions.ToInteger(Interaction.IIf(ColorToday == 1, (object)97, (object)88));
		}
		if (CandleList[num2] == 1 && (!LongBodyToday & !SmallBodyToday & (decimal.Compare(UpperShadowLength, BodyHeight) < 0) & (decimal.Compare(LowerShadowLength, BodyHeight) < 0) & (decimal.Compare(UpperShadowLength, 0m) > 0) & (decimal.Compare(LowerShadowLength, 0m) > 0)) && ((ColorToday == 1 && num2 == 97) | (ColorToday == 0 && num2 == 88)))
		{
			PatternName = Conversions.ToString(Interaction.IIf(ColorToday == 1, (object)"Black", (object)"White")) + " candle";
			SaveNewCandle(num2, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
		}
		num2 = Conversions.ToInteger(Interaction.IIf(ColorToday == 1, (object)87, (object)86));
		if (CandleList[num2] == 1 && ((decimal.Compare(BodyHeight, decimal.Divide(AvgBodyHeight, 3m)) <= 0) & (decimal.Compare(UpperShadowLength, BodyHeight) < 0) & (decimal.Compare(LowerShadowLength, BodyHeight) < 0) & (decimal.Compare(UpperShadowLength, 0m) > 0) & (decimal.Compare(LowerShadowLength, 0m) > 0)) && ((ColorToday == 1 && num2 == 87) | (ColorToday == 0 && num2 == 86)))
		{
			PatternName = "Short " + Conversions.ToString(Interaction.IIf(ColorToday == 1, (object)"black", (object)"white")) + " candle";
			SaveNewCandle(num2, startIndex, iEndDate, ref Ctrl, Filename, ref Row, Source);
		}
	}

	private static void SaveNewCandle(int PatternType, int iStartDate, int iEndDate, ref Control ControlType, string Filename, ref int Row, int Source)
	{
		//IL_07a3: Unknown result type (might be due to invalid IL or missing references)
		//IL_07a9: Expected O, but got Unknown
		//IL_07b5: Unknown result type (might be due to invalid IL or missing references)
		//IL_07c6: Unknown result type (might be due to invalid IL or missing references)
		//IL_07eb: Unknown result type (might be due to invalid IL or missing references)
		//IL_0828: Unknown result type (might be due to invalid IL or missing references)
		//IL_0850: Unknown result type (might be due to invalid IL or missing references)
		//IL_088e: Unknown result type (might be due to invalid IL or missing references)
		//IL_08cc: Unknown result type (might be due to invalid IL or missing references)
		//IL_08f4: Unknown result type (might be due to invalid IL or missing references)
		//IL_091c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0945: Unknown result type (might be due to invalid IL or missing references)
		//IL_096e: Unknown result type (might be due to invalid IL or missing references)
		//IL_09a3: Unknown result type (might be due to invalid IL or missing references)
		//IL_0a26: Unknown result type (might be due to invalid IL or missing references)
		//IL_0a4e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0a8d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0acb: Unknown result type (might be due to invalid IL or missing references)
		//IL_0b38: Unknown result type (might be due to invalid IL or missing references)
		//IL_0b7d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0ba3: Unknown result type (might be due to invalid IL or missing references)
		//IL_0bd4: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c0d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0f51: Unknown result type (might be due to invalid IL or missing references)
		//IL_0f79: Unknown result type (might be due to invalid IL or missing references)
		//IL_0fb8: Unknown result type (might be due to invalid IL or missing references)
		//IL_0ff6: Unknown result type (might be due to invalid IL or missing references)
		//IL_1063: Unknown result type (might be due to invalid IL or missing references)
		//IL_10a8: Unknown result type (might be due to invalid IL or missing references)
		//IL_10ce: Unknown result type (might be due to invalid IL or missing references)
		//IL_10ff: Unknown result type (might be due to invalid IL or missing references)
		//IL_1138: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c6a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c92: Unknown result type (might be due to invalid IL or missing references)
		//IL_0cd1: Unknown result type (might be due to invalid IL or missing references)
		//IL_0d0f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0d7c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0dc1: Unknown result type (might be due to invalid IL or missing references)
		//IL_0de7: Unknown result type (might be due to invalid IL or missing references)
		//IL_0e18: Unknown result type (might be due to invalid IL or missing references)
		//IL_0e51: Unknown result type (might be due to invalid IL or missing references)
		//IL_1195: Unknown result type (might be due to invalid IL or missing references)
		//IL_11bd: Unknown result type (might be due to invalid IL or missing references)
		//IL_11fc: Unknown result type (might be due to invalid IL or missing references)
		//IL_123a: Unknown result type (might be due to invalid IL or missing references)
		//IL_12a7: Unknown result type (might be due to invalid IL or missing references)
		//IL_12ec: Unknown result type (might be due to invalid IL or missing references)
		//IL_1312: Unknown result type (might be due to invalid IL or missing references)
		//IL_1343: Unknown result type (might be due to invalid IL or missing references)
		//IL_137c: Unknown result type (might be due to invalid IL or missing references)
		string TargetPhrase = "";
		string stopPrice = "";
		string priceTarget = "";
		DateTime dateTime = DateTime.MinValue;
		if ((iStartDate < GlobalForm.ChartStartIndex) | (iEndDate > GlobalForm.ChartEndIndex))
		{
			return;
		}
		string text = CandleMsgs(PatternType);
		bool flag = false;
		checked
		{
			int num = GlobalForm.CandleCount - 1;
			for (int i = 0; i <= num; i++)
			{
				if ((GlobalForm.CandlePatterns[i].iStartDate == iStartDate) & (GlobalForm.CandlePatterns[i].iEndDate == iEndDate))
				{
					flag = true;
					break;
				}
			}
			if (flag)
			{
				return;
			}
			string bkoutDirection = "None yet";
			int num2 = 0;
			decimal StopPrice = default(decimal);
			if (Source != 0)
			{
				int num3;
				int num4;
				decimal num6 = default(decimal);
				int iBkout = default(int);
				decimal dBreakoutPrice = default(decimal);
				if (unchecked(PatternType == 77 || PatternType == 27 || PatternType == 10 || PatternType == 26))
				{
					num3 = iEndDate;
					num4 = iEndDate;
					int num5 = iEndDate + 1;
					int hLCRange = GlobalForm.HLCRange;
					for (int i = num5; i <= hLCRange; i++)
					{
						if (decimal.Compare(Storage[3, i], Storage[1, num3]) > 0)
						{
							num6 = decimal.Add(Storage[1, num3], decimal.Subtract(Storage[1, num3], Storage[2, num4]));
							stopPrice = GetVolStop(i, 1, num6, ref TargetPhrase, ref StopPrice);
							iBkout = i;
							bkoutDirection = "Up on " + Strings.Format((object)GlobalForm.nDT[0, i], GlobalForm.UserDate);
							num2 = 1;
							priceTarget = Strings.Format((object)num6, "0.####") + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num6, Storage[1, num3]), Storage[1, num3]), "0%");
							dBreakoutPrice = Storage[1, num3];
							break;
						}
						if (decimal.Compare(Storage[3, i], Storage[2, num4]) < 0)
						{
							num6 = decimal.Subtract(Storage[2, num4], decimal.Subtract(Storage[1, num3], Storage[2, num4]));
							stopPrice = GetVolStop(i, -1, num6, ref TargetPhrase, ref StopPrice);
							iBkout = i;
							bkoutDirection = "Down on " + Strings.Format((object)GlobalForm.nDT[0, i], GlobalForm.UserDate);
							num2 = -1;
							priceTarget = Strings.Format((object)num6, "0.####") + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num6, Storage[2, num4]), Storage[2, num4]), "0%");
							dBreakoutPrice = Storage[2, num4];
							break;
						}
					}
				}
				else
				{
					num3 = iStartDate;
					num4 = iStartDate;
					int hLCRange2 = GlobalForm.HLCRange;
					for (int i = iStartDate; i <= hLCRange2; i++)
					{
						if (i <= iEndDate)
						{
							num3 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(Storage[1, i], Storage[1, num3]) > 0, (object)i, (object)num3));
							num4 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(Storage[2, i], Storage[2, num4]) < 0, (object)i, (object)num4));
							continue;
						}
						if (decimal.Compare(Storage[3, i], Storage[1, num3]) > 0)
						{
							num6 = decimal.Add(Storage[1, num3], decimal.Subtract(Storage[1, num3], Storage[2, num4]));
							stopPrice = GetVolStop(i, 1, num6, ref TargetPhrase, ref StopPrice);
							iBkout = i;
							bkoutDirection = "Up on " + Strings.Format((object)GlobalForm.nDT[0, i], GlobalForm.UserDate);
							num2 = 1;
							priceTarget = Strings.Format((object)num6, "0.####") + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num6, Storage[1, num3]), Storage[1, num3]), "0%");
							dBreakoutPrice = Storage[1, num3];
							break;
						}
						if (decimal.Compare(Storage[3, i], Storage[2, num4]) < 0)
						{
							num6 = decimal.Subtract(Storage[2, num4], decimal.Subtract(Storage[1, num3], Storage[2, num4]));
							stopPrice = GetVolStop(i, -1, num6, ref TargetPhrase, ref StopPrice);
							iBkout = i;
							bkoutDirection = "Down on " + Strings.Format((object)GlobalForm.nDT[0, i], GlobalForm.UserDate);
							num2 = -1;
							priceTarget = Strings.Format((object)num6, "0.####") + " or " + Strings.Format((object)decimal.Divide(decimal.Subtract(num6, Storage[2, num4]), Storage[2, num4]), "0%");
							dBreakoutPrice = Storage[2, num4];
							break;
						}
					}
				}
				int num7 = iEndDate + 1;
				int hLCRange3 = GlobalForm.HLCRange;
				for (int i = num7; i <= hLCRange3; i++)
				{
					switch (num2)
					{
					case 1:
						if ((decimal.Compare(Storage[2, i], StopPrice) <= 0) & (DateTime.Compare(dateTime, DateTime.MinValue) == 0))
						{
							dateTime = GlobalForm.nDT[0, i];
						}
						break;
					case -1:
						if ((decimal.Compare(Storage[1, i], StopPrice) >= 0) & (DateTime.Compare(dateTime, DateTime.MinValue) == 0))
						{
							dateTime = GlobalForm.nDT[0, i];
						}
						break;
					}
				}
				GlobalForm.CandlePatterns = (GlobalForm.CandleFmtns[])Utils.CopyArray((Array)GlobalForm.CandlePatterns, (Array)new GlobalForm.CandleFmtns[GlobalForm.CandleCount + 1]);
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].Type = PatternType;
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].Phrase = PatternName + ": " + text;
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].iStartDate = iStartDate;
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].iEndDate = iEndDate;
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].RenderColor = Color.Black;
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].PriceTarget = priceTarget;
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].StopPrice = stopPrice;
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].StopDate = dateTime;
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].BkoutDirection = bkoutDirection;
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].TradeStatus = TargetPhrase;
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].dPriceTarget = num6;
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].dStopPrice = StopPrice;
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].iBkoutDirection = num2;
				GlobalForm.CandlePatterns[GlobalForm.CandleCount].dBreakoutPrice = dBreakoutPrice;
				GetUltimateHighLow(iBkout, num3, num4, num2, GlobalForm.CandleCount);
				GlobalForm.CandleCount++;
			}
			else
			{
				if (Source != 0)
				{
					return;
				}
				GlobalForm.CandlePatterns = new GlobalForm.CandleFmtns[1];
				try
				{
					foreach (Control control in ControlType.Controls)
					{
						Control val = control;
						if (!(val is DataGridView))
						{
							continue;
						}
						((DataGridView)val).Rows.Add();
						((DataGridView)val).Rows[Row].Cells[0].Value = Filename;
						((DataGridView)val).Rows[Row].Cells[1].Value = GlobalForm.LimitDecimals(Storage[3, GlobalForm.HLCRange]);
						((DataGridView)val).Rows[Row].Cells[2].Value = PatternName;
						((DataGridView)val).Rows[Row].Cells[3].Value = Strings.Format((object)GlobalForm.nDT[0, iStartDate], GlobalForm.UserDate);
						((DataGridView)val).Rows[Row].Cells[4].Value = Strings.Format((object)GlobalForm.nDT[0, iEndDate], GlobalForm.UserDate);
						((DataGridView)val).Rows[Row].Cells[5].Value = "None yet";
						((DataGridView)val).Rows[Row].Cells[8].Value = "";
						((DataGridView)val).Rows[Row].Cells[10].Value = "N/A";
						((DataGridView)val).Rows[Row].Cells[11].Value = "N/A";
						((DataGridView)val).Rows[Row].Cells[9].Value = GlobalForm.Get3MoAvgVolume(GlobalForm.nDT[0, iEndDate]);
						((DataGridView)val).Rows[Row].Cells[19].Value = Scale;
						if (unchecked(PatternType == 77 || PatternType == 27 || PatternType == 10 || PatternType == 26))
						{
							int num3 = iEndDate;
							int num4 = iEndDate;
							int num8 = iEndDate + 1;
							int hLCRange4 = GlobalForm.HLCRange;
							for (int i = num8; i <= hLCRange4; i++)
							{
								if (decimal.Compare(Storage[3, i], Storage[1, num3]) > 0)
								{
									((DataGridView)val).Rows[Row].Cells[5].Value = "Up";
									((DataGridView)val).Rows[Row].Cells[6].Value = Strings.Format((object)GlobalForm.nDT[0, i], GlobalForm.UserDate);
									((DataGridView)val).Rows[Row].Cells[7].Value = Strings.Format((object)Storage[1, num3], "0.####");
									((DataGridView)val).Rows[Row].Cells[8].Value = GlobalForm.GetPriceFill(i, Storage[1, num3], 1, CandleFlag: true);
									decimal num6 = decimal.Add(Storage[1, num3], decimal.Subtract(Storage[1, num3], Storage[2, num4]));
									((DataGridView)val).Rows[Row].Cells[12].Value = Strings.Format((object)num6, "0.####");
									stopPrice = GetVolStop(i, 1, num6, ref TargetPhrase, ref StopPrice);
									((DataGridView)val).Rows[Row].Cells[13].Value = stopPrice;
									((DataGridView)val).Rows[Row].Cells[14].Value = TargetPhrase;
									GetUltimateHighLow(i, num3, num4, 1, 0);
									((DataGridView)val).Rows[Row].Cells[10].Value = GlobalForm.CandlePatterns[0].UltHLPrice;
									((DataGridView)val).Rows[Row].Cells[11].Value = GlobalForm.CandlePatterns[0].UltHLDate;
									break;
								}
								if (decimal.Compare(Storage[3, i], Storage[2, num4]) < 0)
								{
									((DataGridView)val).Rows[Row].Cells[5].Value = "Down";
									((DataGridView)val).Rows[Row].Cells[6].Value = Strings.Format((object)GlobalForm.nDT[0, i], GlobalForm.UserDate);
									((DataGridView)val).Rows[Row].Cells[7].Value = Strings.Format((object)Storage[2, num4], "0.####");
									((DataGridView)val).Rows[Row].Cells[8].Value = GlobalForm.GetPriceFill(i, Storage[2, num4], -1, CandleFlag: true);
									decimal num6 = decimal.Subtract(Storage[2, num4], decimal.Subtract(Storage[1, num3], Storage[2, num4]));
									((DataGridView)val).Rows[Row].Cells[12].Value = Strings.Format((object)num6, "0.####");
									stopPrice = GetVolStop(i, -1, num6, ref TargetPhrase, ref StopPrice);
									((DataGridView)val).Rows[Row].Cells[13].Value = stopPrice;
									((DataGridView)val).Rows[Row].Cells[14].Value = TargetPhrase;
									GetUltimateHighLow(i, num3, num4, -1, 0);
									((DataGridView)val).Rows[Row].Cells[10].Value = GlobalForm.CandlePatterns[0].UltHLPrice;
									((DataGridView)val).Rows[Row].Cells[11].Value = GlobalForm.CandlePatterns[0].UltHLDate;
									break;
								}
							}
						}
						else
						{
							int num3 = iStartDate;
							int num4 = iStartDate;
							int hLCRange5 = GlobalForm.HLCRange;
							for (int i = iStartDate; i <= hLCRange5; i++)
							{
								if (i <= iEndDate)
								{
									num3 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(Storage[1, i], Storage[1, num3]) > 0, (object)i, (object)num3));
									num4 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(Storage[2, i], Storage[2, num4]) < 0, (object)i, (object)num4));
									continue;
								}
								if (decimal.Compare(Storage[3, i], Storage[1, num3]) > 0)
								{
									((DataGridView)val).Rows[Row].Cells[5].Value = "Up";
									((DataGridView)val).Rows[Row].Cells[6].Value = Strings.Format((object)GlobalForm.nDT[0, i], GlobalForm.UserDate);
									((DataGridView)val).Rows[Row].Cells[7].Value = Strings.Format((object)Storage[1, num3], "0.####");
									((DataGridView)val).Rows[Row].Cells[8].Value = GlobalForm.GetPriceFill(i, Storage[1, num3], 1, CandleFlag: true);
									decimal num6 = decimal.Add(Storage[1, num3], decimal.Subtract(Storage[1, num3], Storage[2, num4]));
									((DataGridView)val).Rows[Row].Cells[12].Value = Strings.Format((object)num6, "0.####");
									stopPrice = GetVolStop(i, 1, num6, ref TargetPhrase, ref StopPrice);
									((DataGridView)val).Rows[Row].Cells[13].Value = stopPrice;
									((DataGridView)val).Rows[Row].Cells[14].Value = TargetPhrase;
									GetUltimateHighLow(i, num3, num4, 1, 0);
									((DataGridView)val).Rows[Row].Cells[10].Value = GlobalForm.CandlePatterns[0].UltHLPrice;
									((DataGridView)val).Rows[Row].Cells[11].Value = GlobalForm.CandlePatterns[0].UltHLDate;
									break;
								}
								if (decimal.Compare(Storage[3, i], Storage[2, num4]) < 0)
								{
									((DataGridView)val).Rows[Row].Cells[5].Value = "Down";
									((DataGridView)val).Rows[Row].Cells[6].Value = Strings.Format((object)GlobalForm.nDT[0, i], GlobalForm.UserDate);
									((DataGridView)val).Rows[Row].Cells[7].Value = Strings.Format((object)Storage[2, num4], "0.####");
									((DataGridView)val).Rows[Row].Cells[8].Value = GlobalForm.GetPriceFill(i, Storage[2, num4], -1, CandleFlag: true);
									decimal num6 = decimal.Subtract(Storage[2, num4], decimal.Subtract(Storage[1, num3], Storage[2, num4]));
									((DataGridView)val).Rows[Row].Cells[12].Value = Strings.Format((object)num6, "0.####");
									stopPrice = GetVolStop(i, -1, num6, ref TargetPhrase, ref StopPrice);
									((DataGridView)val).Rows[Row].Cells[13].Value = stopPrice;
									((DataGridView)val).Rows[Row].Cells[14].Value = TargetPhrase;
									GetUltimateHighLow(i, num3, num4, -1, 0);
									((DataGridView)val).Rows[Row].Cells[10].Value = GlobalForm.CandlePatterns[0].UltHLPrice;
									((DataGridView)val).Rows[Row].Cells[11].Value = GlobalForm.CandlePatterns[0].UltHLDate;
									break;
								}
							}
						}
						Row++;
						break;
					}
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					ProjectData.ClearProjectError();
				}
				GlobalForm.CandlePatterns = null;
			}
		}
	}

	private static void GetUltimateHighLow(int iBkout, int iTop, int iBottom, int BkoutDirection, int CPIndex)
	{
		int num = iBkout;
		int num2 = iBkout;
		int hLCRange = GlobalForm.HLCRange;
		for (int i = iBkout; i <= hLCRange; i = checked(i + 1))
		{
			if (BkoutDirection == 1)
			{
				num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(Storage[1, i], Storage[1, num]) > 0, (object)i, (object)num));
				if (Convert.ToDouble(Storage[2, i]) < Convert.ToDouble(Storage[1, num]) * 0.8)
				{
					GlobalForm.CandlePatterns[CPIndex].UltHLPrice = GlobalForm.LimitDecimals(Storage[1, num]);
					GlobalForm.CandlePatterns[CPIndex].UltHLDate = Strings.Format((object)GlobalForm.nDT[0, num], GlobalForm.UserDate);
					GlobalForm.CandlePatterns[CPIndex].UltHiLow = true;
					break;
				}
				if (iBottom != -1 && decimal.Compare(Storage[3, i], Storage[2, iBottom]) < 0)
				{
					GlobalForm.CandlePatterns[CPIndex].UltHLPrice = GlobalForm.LimitDecimals(Storage[1, num]);
					GlobalForm.CandlePatterns[CPIndex].UltHLDate = Strings.Format((object)GlobalForm.nDT[0, num], GlobalForm.UserDate);
					GlobalForm.CandlePatterns[CPIndex].UltHiLow = true;
					break;
				}
			}
			else
			{
				num2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(Storage[2, i], Storage[2, num2]) < 0, (object)i, (object)num2));
				if (Convert.ToDouble(Storage[1, i]) > Convert.ToDouble(Storage[2, num2]) * 1.2)
				{
					GlobalForm.CandlePatterns[CPIndex].UltHLPrice = GlobalForm.LimitDecimals(Storage[2, num2]);
					GlobalForm.CandlePatterns[CPIndex].UltHLDate = Strings.Format((object)GlobalForm.nDT[0, num2], GlobalForm.UserDate);
					GlobalForm.CandlePatterns[CPIndex].UltHiLow = false;
					break;
				}
				if (iTop != -1 && decimal.Compare(Storage[3, i], Storage[1, iTop]) > 0)
				{
					GlobalForm.CandlePatterns[CPIndex].UltHLPrice = GlobalForm.LimitDecimals(Storage[2, num2]);
					GlobalForm.CandlePatterns[CPIndex].UltHLDate = Strings.Format((object)GlobalForm.nDT[0, num2], GlobalForm.UserDate);
					GlobalForm.CandlePatterns[CPIndex].UltHiLow = false;
					break;
				}
			}
		}
	}

	private static string GetVolStop(int iBkout, int UpDown, decimal Target, ref string TargetPhrase, ref decimal StopPrice)
	{
		decimal num = default(decimal);
		string result = "";
		checked
		{
			if (iBkout > 19)
			{
				int num2 = iBkout - 1;
				StopPrice = default(decimal);
				int num3 = iBkout - 20;
				for (int i = num2; i >= num3; i += -1)
				{
					num = decimal.Add(num, decimal.Subtract(Storage[1, i], Storage[2, i]));
					if (i != iBkout - 20)
					{
						continue;
					}
					if (UpDown == 1)
					{
						StopPrice = decimal.Subtract(Storage[2, num2], decimal.Divide(decimal.Multiply(2m, num), 20m));
						if (decimal.Compare(Storage[2, num2], 0m) != 0)
						{
							result = Strings.Format((object)StopPrice, "0.####") + " or " + Strings.Format((object)decimal.Subtract(decimal.Divide(StopPrice, Storage[2, num2]), 1m), "0%");
						}
					}
					else
					{
						StopPrice = decimal.Add(Storage[1, num2], decimal.Divide(decimal.Multiply(2m, num), 20m));
						if (decimal.Compare(Storage[1, num2], 0m) != 0)
						{
							result = Strings.Format((object)StopPrice, "0.####") + " or " + Strings.Format((object)decimal.Subtract(decimal.Divide(StopPrice, Storage[1, num2]), 1m), "0%");
						}
					}
					TargetPhrase = CheckCandleTradeStatus(iBkout, StopPrice, Target, UpDown);
					break;
				}
			}
			else
			{
				result = "Too near data start for calculation.";
			}
			return result;
		}
	}

	private static string CheckCandleTradeStatus(int index, decimal StopPrice, decimal TargetPrice, int BkoutDirection)
	{
		string result = "";
		int hLCRange = GlobalForm.HLCRange;
		for (int i = index; i <= hLCRange; i = checked(i + 1))
		{
			if (BkoutDirection == 1)
			{
				if ((decimal.Compare(TargetPrice, 0m) != 0) & (decimal.Compare(Storage[1, i], TargetPrice) >= 0))
				{
					result = "Target (" + Strings.Format((object)TargetPrice, "0.####") + ") reached on " + Strings.Format((object)GlobalForm.nDT[0, i], GlobalForm.UserDate);
					break;
				}
				if ((decimal.Compare(StopPrice, 0m) != 0) & (decimal.Compare(Storage[2, i], StopPrice) <= 0))
				{
					result = "Stop (" + Strings.Format((object)StopPrice, "0.####") + ") triggered on " + Strings.Format((object)GlobalForm.nDT[0, i], GlobalForm.UserDate);
					break;
				}
			}
			else
			{
				if ((decimal.Compare(TargetPrice, 0m) != 0) & (decimal.Compare(Storage[2, i], TargetPrice) <= 0))
				{
					result = "Target (" + Strings.Format((object)TargetPrice, "0.####") + ") reached on " + Strings.Format((object)GlobalForm.nDT[0, i], GlobalForm.UserDate);
					break;
				}
				if ((decimal.Compare(StopPrice, 0m) != 0) & (decimal.Compare(Storage[1, i], StopPrice) >= 0))
				{
					result = "Stop (" + Strings.Format((object)StopPrice, "0.####") + ") triggered on " + Strings.Format((object)GlobalForm.nDT[0, i], GlobalForm.UserDate);
					break;
				}
			}
		}
		return result;
	}

	private static void GetShadows(int TmpIndex, ref bool LongUpShadow, ref bool LongDnShadow)
	{
		decimal num = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[3, TmpIndex], GlobalForm.nHLC[0, TmpIndex]) > 0, (object)GlobalForm.nHLC[3, TmpIndex], (object)GlobalForm.nHLC[0, TmpIndex]));
		decimal num2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[3, TmpIndex], GlobalForm.nHLC[0, TmpIndex]) > 0, (object)GlobalForm.nHLC[0, TmpIndex], (object)GlobalForm.nHLC[3, TmpIndex]));
		decimal d = decimal.Subtract(num, num2);
		LongUpShadow = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, TmpIndex], num), decimal.Multiply(1m, d)) > 0, (object)true, (object)false));
		LongDnShadow = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(decimal.Subtract(num2, GlobalForm.nHLC[2, TmpIndex]), decimal.Multiply(1m, d)) > 0, (object)true, (object)false));
	}

	private static void GetBodyHeight(int TmpIndex)
	{
		decimal d = Math.Abs(decimal.Subtract(GlobalForm.nHLC[3, TmpIndex], GlobalForm.nHLC[0, TmpIndex]));
		LongCandle = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(d, decimal.Multiply(AvgBodyHeight, 1.3m)) >= 0, (object)true, (object)false));
		if (!LongCandle & (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, TmpIndex], GlobalForm.nHLC[2, TmpIndex]), 0m) != 0))
		{
			LongCandle = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(decimal.Divide(d, decimal.Subtract(GlobalForm.nHLC[1, TmpIndex], GlobalForm.nHLC[2, TmpIndex])), 0.66m) > 0, (object)true, (object)false));
		}
		SmallCandle = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(Math.Abs(decimal.Subtract(GlobalForm.nHLC[0, TmpIndex], GlobalForm.nHLC[3, TmpIndex])), decimal.Multiply(AvgBodyHeight, 0.66m)) <= 0, (object)true, (object)false));
	}

	public static bool WithinRange(int TmpIndex)
	{
		decimal d = Math.Abs(decimal.Subtract(GlobalForm.nHLC[3, TmpIndex], GlobalForm.nHLC[0, TmpIndex]));
		decimal num = decimal.Subtract(GlobalForm.nHLC[1, TmpIndex], GlobalForm.nHLC[2, TmpIndex]);
		if (decimal.Compare(num, 0m) > 0)
		{
			return Conversions.ToBoolean(Interaction.IIf((decimal.Compare(decimal.Divide(d, num), 0.01m) < 0) | (decimal.Compare(d, DOJIRANGE) <= 0), (object)true, (object)false));
		}
		return true;
	}

	public static bool WithinRange(int TmpIndex, decimal DojiRange)
	{
		decimal d = Math.Abs(decimal.Subtract(GlobalForm.nHLC[3, TmpIndex], GlobalForm.nHLC[0, TmpIndex]));
		decimal num = decimal.Subtract(GlobalForm.nHLC[1, TmpIndex], GlobalForm.nHLC[2, TmpIndex]);
		if (decimal.Compare(num, 0m) > 0)
		{
			return Conversions.ToBoolean(Interaction.IIf((decimal.Compare(decimal.Divide(d, num), 0.01m) < 0) | (decimal.Compare(d, DojiRange) <= 0), (object)true, (object)false));
		}
		return true;
	}

	private static bool WithinNearEarly(int i)
	{
		TmpPrice = yDayClose;
		Tmp2Price = PrClose;
		TmpIndex = checked(i - 1);
		Tmp2Index = i;
		return WithinNear();
	}

	private static bool WithinNear()
	{
		decimal d = Math.Abs(decimal.Subtract(TmpPrice, Tmp2Price));
		decimal num = decimal.Subtract(GlobalForm.nHLC[1, TmpIndex], GlobalForm.nHLC[2, TmpIndex]);
		num = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num, decimal.Subtract(GlobalForm.nHLC[1, Tmp2Index], GlobalForm.nHLC[2, Tmp2Index])) < 0, (object)decimal.Subtract(GlobalForm.nHLC[1, Tmp2Index], GlobalForm.nHLC[2, Tmp2Index]), (object)num));
		if (decimal.Compare(num, 0m) > 0)
		{
			return Conversions.ToBoolean(Interaction.IIf((Convert.ToDouble(decimal.Divide(d, num)) <= 0.03) | (decimal.Compare(d, DOJIRANGE) <= 0), (object)true, (object)false));
		}
		return true;
	}

	private static void Check4Highs(int CandleType, int Lines, int i, ref Control FormControl, string Filename, ref int Row, int Source)
	{
		checked
		{
			if (i <= Lines - 1 || CandleList[CandleType] != 1)
			{
				return;
			}
			bool flag = false;
			int j;
			for (j = i - (Lines - 1); j <= i; j++)
			{
				if (decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, j - 1]) <= 0)
				{
					flag = true;
					break;
				}
			}
			if (!flag && j > Lines - 1)
			{
				PatternName = Strings.Format((object)Lines, "") + " new price lines";
				SaveNewCandle(CandleType, i - Lines + 1, i, ref FormControl, Filename, ref Row, Source);
			}
		}
	}

	private static void GetCandleDefs(int StartIndex, int i)
	{
		AvgBodyHeight = default(decimal);
		AvgUpShadowLen = default(decimal);
		AvgDnShadowLen = default(decimal);
		checked
		{
			if (StartIndex >= 6)
			{
				int num = StartIndex - 6;
				int num2 = StartIndex - 1;
				for (int j = num; j <= num2; j++)
				{
					AvgBodyHeight = decimal.Add(AvgBodyHeight, Math.Abs(decimal.Subtract(GlobalForm.nHLC[0, j], GlobalForm.nHLC[3, j])));
					AvgUpShadowLen = decimal.Subtract(decimal.Add(AvgUpShadowLen, GlobalForm.nHLC[1, j]), Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[0, j]) > 0, (object)GlobalForm.nHLC[3, j], (object)GlobalForm.nHLC[0, j])));
					AvgDnShadowLen = decimal.Subtract(decimal.Add(AvgDnShadowLen, Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[0, j]) > 0, (object)GlobalForm.nHLC[0, j], (object)GlobalForm.nHLC[3, j]))), GlobalForm.nHLC[2, j]);
				}
				AvgBodyHeight = decimal.Divide(AvgBodyHeight, 6m);
				AvgUpShadowLen = decimal.Divide(AvgUpShadowLen, 6m);
				AvgDnShadowLen = decimal.Divide(AvgDnShadowLen, 6m);
			}
			PrHigh = GlobalForm.nHLC[1, i];
			PrLow = GlobalForm.nHLC[2, i];
			PrClose = GlobalForm.nHLC[3, i];
			PrOpen = GlobalForm.nHLC[0, i];
			if (i > 0)
			{
				yDayHigh = GlobalForm.nHLC[1, i - 1];
				yDayLow = GlobalForm.nHLC[2, i - 1];
				yDayClose = GlobalForm.nHLC[3, i - 1];
				yDayOpen = GlobalForm.nHLC[0, i - 1];
			}
			CandleHeight = decimal.Subtract(PrHigh, PrLow);
			PrBodyTop = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(PrClose, PrOpen) > 0, (object)PrClose, (object)PrOpen));
			PrBodyBottom = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(PrClose, PrOpen) > 0, (object)PrOpen, (object)PrClose));
			BodyHeight = decimal.Subtract(PrBodyTop, PrBodyBottom);
			UpperShadowLength = decimal.Subtract(PrHigh, PrBodyTop);
			LowerShadowLength = decimal.Subtract(PrBodyBottom, PrLow);
			LongUpperShadow = Conversions.ToBoolean(Interaction.IIf((decimal.Compare(UpperShadowLength, 0m) > 0) & (decimal.Compare(UpperShadowLength, decimal.Multiply(1m, BodyHeight)) > 0), (object)true, (object)false));
			LongLowerShadow = Conversions.ToBoolean(Interaction.IIf((decimal.Compare(LowerShadowLength, 0m) > 0) & (decimal.Compare(LowerShadowLength, decimal.Multiply(1m, BodyHeight)) > 0), (object)true, (object)false));
			TopNear = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(decimal.Subtract(PrHigh, PrBodyTop), decimal.Multiply(0.25m, CandleHeight)) <= 0, (object)true, (object)false));
			AtTop = false;
			AtBottom = false;
			if (decimal.Compare(CandleHeight, 0m) != 0)
			{
				AtTop = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(decimal.Divide(UpperShadowLength, CandleHeight), 0.1m) <= 0, (object)true, (object)false));
				AtBottom = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(decimal.Divide(LowerShadowLength, CandleHeight), 0.1m) <= 0, (object)true, (object)false));
			}
			BottomNear = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(decimal.Subtract(PrBodyBottom, PrLow), decimal.Multiply(0.25m, CandleHeight)) <= 0, (object)true, (object)false));
			ColorToday = Conversions.ToInteger(Interaction.IIf(decimal.Compare(PrOpen, PrClose) < 0, (object)0, (object)1));
			ColorToday = Conversions.ToInteger(Interaction.IIf(decimal.Compare(PrOpen, PrClose) == 0, (object)(-1), (object)ColorToday));
			ColorYesterday = -1;
			if (i > 0)
			{
				ColorYesterday = Conversions.ToInteger(Interaction.IIf(decimal.Compare(yDayOpen, yDayClose) < 0, (object)0, (object)1));
				ColorYesterday = Conversions.ToInteger(Interaction.IIf(decimal.Compare(yDayOpen, yDayClose) == 0, (object)(-1), (object)ColorYesterday));
			}
			if (i < 13)
			{
				Slope1 = HLRegression(i - 1, 2, 3);
				Slope2 = HLRegression(i - 2, 2, 3);
				Slope3 = HLRegression(i - 3, 2, 3);
				Slope4 = HLRegression(i - 4, 2, 3);
				Slope5 = HLRegression(i - 5, 2, 3);
			}
			else
			{
				EMACalc(i - 1, ref Slope1, ref Slope2, ref Slope3, ref Slope4, ref Slope5, 0);
			}
			if (StartIndex - 2 >= 0)
			{
				if ((decimal.Compare(GlobalForm.nHLC[2, StartIndex - 1], GlobalForm.nHLC[1, StartIndex]) >= 0) | ((decimal.Compare(GlobalForm.nHLC[1, StartIndex - 2], GlobalForm.nHLC[1, StartIndex - 1]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, StartIndex - 1], GlobalForm.nHLC[1, StartIndex]) > 0) & ((decimal.Compare(GlobalForm.nHLC[2, StartIndex - 2], GlobalForm.nHLC[2, StartIndex]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, StartIndex - 1], GlobalForm.nHLC[2, StartIndex]) > 0))))
				{
					Slope1 = -1;
					Slope2 = -1;
					Slope3 = -1;
					Slope4 = -1;
					Slope5 = -1;
				}
				if ((decimal.Compare(GlobalForm.nHLC[1, StartIndex - 1], GlobalForm.nHLC[2, StartIndex]) <= 0) | ((decimal.Compare(GlobalForm.nHLC[1, StartIndex - 2], GlobalForm.nHLC[1, StartIndex - 1]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, StartIndex - 1], GlobalForm.nHLC[1, StartIndex]) < 0) & ((decimal.Compare(GlobalForm.nHLC[2, StartIndex - 2], GlobalForm.nHLC[2, StartIndex]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, StartIndex - 1], GlobalForm.nHLC[2, StartIndex]) < 0))))
				{
					Slope1 = 1;
					Slope2 = 1;
					Slope3 = 1;
					Slope4 = 1;
					Slope5 = 1;
				}
			}
			LongBodyToday = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(BodyHeight, decimal.Multiply(AvgBodyHeight, 1.3m)) >= 0, (object)true, (object)false));
			if (!LongBodyToday & (decimal.Compare(CandleHeight, 0m) != 0) & (decimal.Compare(BodyHeight, AvgBodyHeight) > 0))
			{
				LongBodyToday = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(decimal.Divide(BodyHeight, CandleHeight), 0.66m) > 0, (object)true, (object)false));
			}
			SmallBodyToday = false;
			if (decimal.Compare(Math.Abs(decimal.Subtract(PrOpen, PrClose)), decimal.Multiply(AvgBodyHeight, 0.66m)) <= 0)
			{
				SmallBodyToday = true;
			}
			SmallBodyYesterday = false;
			LongBodyYesterday = false;
			if (i > 0)
			{
				if (decimal.Compare(Math.Abs(decimal.Subtract(yDayOpen, yDayClose)), decimal.Multiply(AvgBodyHeight, 0.66m)) <= 0)
				{
					SmallBodyYesterday = true;
				}
				if (decimal.Compare(Math.Abs(decimal.Subtract(yDayOpen, yDayClose)), decimal.Multiply(AvgBodyHeight, 1.3m)) >= 0)
				{
					LongBodyYesterday = true;
				}
				if (!LongBodyYesterday & (decimal.Compare(decimal.Subtract(yDayHigh, yDayLow), 0m) > 0) & (decimal.Compare(Math.Abs(decimal.Subtract(yDayOpen, yDayClose)), AvgBodyHeight) > 0))
				{
					LongBodyYesterday = Conversions.ToBoolean(Interaction.IIf(decimal.Compare(decimal.Divide(Math.Abs(decimal.Subtract(yDayOpen, yDayClose)), decimal.Subtract(yDayHigh, yDayLow)), 0.66m) > 0, (object)true, (object)false));
				}
			}
		}
	}

	private static bool VerifyHarami(ref int TmpIndex)
	{
		GetBodyHeight(TmpIndex);
		checked
		{
			if (LongCandle)
			{
				TmpIndex++;
				GetBodyHeight(TmpIndex);
				TmpIndex--;
				if (SmallCandle)
				{
					if ((decimal.Compare(GlobalForm.nHLC[0, TmpIndex], GlobalForm.nHLC[3, TmpIndex]) > 0) & ((decimal.Compare(GlobalForm.nHLC[0, TmpIndex + 1], GlobalForm.nHLC[3, TmpIndex + 1]) < 0) | (decimal.Compare(GlobalForm.nHLC[0, TmpIndex + 1], GlobalForm.nHLC[3, TmpIndex + 1]) == 0)))
					{
						if ((decimal.Compare(GlobalForm.nHLC[0, TmpIndex + 1], GlobalForm.nHLC[0, TmpIndex]) <= 0) & (decimal.Compare(GlobalForm.nHLC[0, TmpIndex + 1], GlobalForm.nHLC[3, TmpIndex]) >= 0) & (decimal.Compare(GlobalForm.nHLC[3, TmpIndex + 1], GlobalForm.nHLC[0, TmpIndex]) <= 0) & (decimal.Compare(GlobalForm.nHLC[3, TmpIndex + 1], GlobalForm.nHLC[3, TmpIndex]) >= 0) & ((decimal.Compare(GlobalForm.nHLC[3, TmpIndex + 1], GlobalForm.nHLC[0, TmpIndex]) != 0) | (decimal.Compare(GlobalForm.nHLC[0, TmpIndex + 1], GlobalForm.nHLC[3, TmpIndex]) != 0)))
						{
							TmpIndex++;
							bool flag = WithinRange(TmpIndex);
							TmpIndex--;
							if (!flag | (flag & (decimal.Compare(GlobalForm.nHLC[1, TmpIndex + 1], GlobalForm.nHLC[1, TmpIndex]) <= 0) & (decimal.Compare(GlobalForm.nHLC[2, TmpIndex + 1], GlobalForm.nHLC[2, TmpIndex]) >= 0)))
							{
								int num = Conversions.ToInteger(Interaction.IIf(flag, (object)65, (object)67));
								if ((Slope < 0) & (State | (CandleList[num] == 1)))
								{
									PatternName = Conversions.ToString(Interaction.IIf(num == 67, (object)"Bullish harami", (object)"Bullish harami cross"));
									return true;
								}
								return false;
							}
							return false;
						}
						return false;
					}
					if ((decimal.Compare(GlobalForm.nHLC[0, TmpIndex], GlobalForm.nHLC[3, TmpIndex]) < 0) & ((decimal.Compare(GlobalForm.nHLC[0, TmpIndex + 1], GlobalForm.nHLC[3, TmpIndex + 1]) > 0) | (decimal.Compare(GlobalForm.nHLC[0, TmpIndex + 1], GlobalForm.nHLC[3, TmpIndex + 1]) == 0)))
					{
						if ((decimal.Compare(GlobalForm.nHLC[0, TmpIndex + 1], GlobalForm.nHLC[0, TmpIndex]) >= 0) & (decimal.Compare(GlobalForm.nHLC[0, TmpIndex + 1], GlobalForm.nHLC[3, TmpIndex]) <= 0) & (decimal.Compare(GlobalForm.nHLC[3, TmpIndex + 1], GlobalForm.nHLC[0, TmpIndex]) >= 0) & (decimal.Compare(GlobalForm.nHLC[3, TmpIndex + 1], GlobalForm.nHLC[3, TmpIndex]) <= 0) & ((decimal.Compare(GlobalForm.nHLC[3, TmpIndex + 1], GlobalForm.nHLC[0, TmpIndex]) != 0) | (decimal.Compare(GlobalForm.nHLC[0, TmpIndex + 1], GlobalForm.nHLC[3, TmpIndex]) != 0)))
						{
							TmpIndex++;
							bool flag = WithinRange(TmpIndex);
							TmpIndex--;
							if (!flag | (flag & (decimal.Compare(GlobalForm.nHLC[1, TmpIndex + 1], GlobalForm.nHLC[1, TmpIndex]) <= 0) & (decimal.Compare(GlobalForm.nHLC[2, TmpIndex + 1], GlobalForm.nHLC[2, TmpIndex]) >= 0)))
							{
								int num = Conversions.ToInteger(Interaction.IIf(flag, (object)65, (object)67));
								if ((Slope < 0) & (State | (CandleList[num] == 1)))
								{
									return false;
								}
								num = Conversions.ToInteger(Interaction.IIf(flag, (object)66, (object)68));
								if ((Slope > 0) & (State | (CandleList[num] == 1)))
								{
									PatternName = Conversions.ToString(Interaction.IIf(num == 68, (object)"Bearish harami", (object)"Bearish harami cross"));
									return true;
								}
								return false;
							}
							return false;
						}
						return false;
					}
					return false;
				}
				return false;
			}
			return false;
		}
	}

	private static int HLRegression(int iEnd, int DayWk, int LOOKBACK)
	{
		//IL_00c2: Unknown result type (might be due to invalid IL or missing references)
		int num = checked(iEnd - (LOOKBACK - 1));
		if (num < 0 || iEnd < 0)
		{
			return 0;
		}
		decimal num2 = 1m;
		decimal num3 = default(decimal);
		decimal num4 = default(decimal);
		decimal num5 = default(decimal);
		decimal num6 = default(decimal);
		decimal d = default(decimal);
		for (int i = num; i <= iEnd; i = checked(i + 1))
		{
			switch (DayWk)
			{
			case 0:
				d = decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]);
				break;
			case 2:
				d = decimal.Divide(decimal.Add(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 2m);
				break;
			case 3:
				d = GlobalForm.nHLC[3, i];
				break;
			default:
				Interaction.MsgBox((object)"Parm error in HLRegression.", (MsgBoxStyle)0, (object)null);
				break;
			case -1:
				break;
			}
			num3 = decimal.Add(num3, num2);
			num4 = decimal.Add(num4, d);
			num5 = decimal.Add(num5, decimal.Multiply(num2, num2));
			num6 = decimal.Add(num6, decimal.Multiply(num2, d));
			num2 = decimal.Add(num2, 1m);
		}
		int value = Convert.ToInt32(decimal.Subtract(num2, 1m));
		decimal d2 = ((decimal.Compare(decimal.Subtract(decimal.Multiply(new decimal(value), num5), decimal.Multiply(num3, num3)), 0m) == 0) ? default(decimal) : decimal.Divide(decimal.Subtract(decimal.Multiply(new decimal(value), num6), decimal.Multiply(num3, num4)), decimal.Subtract(decimal.Multiply(new decimal(value), num5), decimal.Multiply(num3, num3))));
		return (decimal.Compare(d2, 0m) < 0) ? (-1) : ((decimal.Compare(d2, 0m) != 0) ? 1 : 0);
	}

	private static void EMACalc(int EndDate, ref int Slope1, ref int Slope2, ref int Slope3, ref int Slope4, ref int Slope5, int Index)
	{
		if (EndDate < 13)
		{
			Slope5 = 0;
			Slope4 = 0;
			Slope3 = 0;
			Slope2 = 0;
			Slope1 = 0;
			return;
		}
		decimal d = 0.181818181818182m;
		checked
		{
			decimal num = GlobalForm.nHLC[Index, EndDate - 13];
			decimal d2 = num;
			for (int i = EndDate - 13; i <= EndDate; i++)
			{
				num = decimal.Add(num, decimal.Multiply(d, decimal.Subtract(GlobalForm.nHLC[Index, i], num)));
				int num2 = i;
				if (num2 == EndDate - 4)
				{
					Slope5 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(decimal.Subtract(num, d2), 0m) < 0, (object)(-1), (object)1));
				}
				else if (num2 == EndDate - 3)
				{
					Slope4 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(decimal.Subtract(num, d2), 0m) < 0, (object)(-1), (object)1));
				}
				else if (num2 == EndDate - 2)
				{
					Slope3 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(decimal.Subtract(num, d2), 0m) < 0, (object)(-1), (object)1));
				}
				else if (num2 == EndDate - 1)
				{
					Slope2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(decimal.Subtract(num, d2), 0m) < 0, (object)(-1), (object)1));
				}
				else if (num2 == EndDate)
				{
					Slope1 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(decimal.Subtract(num, d2), 0m) < 0, (object)(-1), (object)1));
				}
				d2 = num;
			}
		}
	}

	private static string CandleMsgs(int Pattern)
	{
		string text = "% of the time.";
		return Pattern switch
		{
			104 => CandlePhrase(69, 2), 
			103 => CandlePhrase(70, 0), 
			102 => CandlePhrase(66, 0), 
			101 => CandlePhrase(64, 1), 
			100 => CandlePhrase(60, 2), 
			99 => CandlePhrase(68, 2), 
			98 => CandlePhrase(71, 0), 
			1 => CandlePhrase(63, 2), 
			0 => CandlePhrase(59, 0), 
			97 => "Continuation 52" + text, 
			87 => "Reversal 52" + text, 
			86 => "Reversal 52" + text, 
			88 => "Continuation 51" + text, 
			85 => CandlePhrase(75, 3), 
			84 => CandlePhrase(60, 2), 
			83 => CandlePhrase(77, 1), 
			82 => "Random: reversal 50" + text, 
			81 => CandlePhrase(56, 2), 
			96 => CandlePhrase(56, 0), 
			95 => CandlePhrase(57, 2), 
			94 => CandlePhrase(51, 2), 
			93 => CandlePhrase(51, 1), 
			92 => CandlePhrase(51, 1), 
			91 => CandlePhrase(52, 0), 
			90 => CandlePhrase(69, 1), 
			89 => CandlePhrase(64, 3), 
			80 => CandlePhrase(63, 2), 
			79 => CandlePhrase(62, 0), 
			78 => CandlePhrase(54, 0), 
			77 => CandlePhrase(53, 1), 
			76 => CandlePhrase(79, 2), 
			75 => CandlePhrase(63, 0), 
			74 => CandlePhrase(71, 2), 
			73 => CandlePhrase(72, 2), 
			72 => CandlePhrase(71, 3), 
			71 => CandlePhrase(60, 0), 
			70 => CandlePhrase(65, 3), 
			69 => CandlePhrase(59, 1), 
			68 => CandlePhrase(53, 1), 
			67 => CandlePhrase(53, 0), 
			66 => CandlePhrase(57, 1), 
			65 => CandlePhrase(55, 3), 
			64 => "Reversal 51" + text, 
			63 => CandlePhrase(56, 3), 
			62 => CandlePhrase(79, 2), 
			61 => CandlePhrase(53, 3), 
			60 => CandlePhrase(54, 2), 
			59 => CandlePhrase(53, 0), 
			58 => CandlePhrase(56, 0), 
			57 => CandlePhrase(65, 3), 
			56 => CandlePhrase(68, 1), 
			55 => "Continuation 53" + text, 
			54 => "Continuation 58" + text, 
			53 => "Continuation 53" + text, 
			52 => "Continuation 52" + text, 
			51 => "Continuation 55" + text, 
			50 => "Continuation 52" + text, 
			49 => "Continuation 54" + text, 
			48 => "Continuation 56" + text, 
			46 => CandlePhrase(61, 3), 
			47 => CandlePhrase(78, 1), 
			45 => CandlePhrase(51, 1), 
			44 => CandlePhrase(56, 0), 
			43 => CandlePhrase(76, 0), 
			42 => CandlePhrase(78, 0), 
			41 => CandlePhrase(56, 3), 
			40 => CandlePhrase(64, 0), 
			39 => "Continuation 51" + text, 
			38 => CandlePhrase(74, 1), 
			37 => CandlePhrase(63, 3), 
			36 => CandlePhrase(72, 1), 
			35 => CandlePhrase(59, 2), 
			34 => CandlePhrase(61, 1), 
			33 => CandlePhrase(56, 3), 
			32 => CandlePhrase(66, 1), 
			31 => "Reversal 50-51" + text, 
			30 => "Reversal 51" + text, 
			29 => "Random: Reversal 50" + text, 
			28 => CandlePhrase(62, 3), 
			25 => CandlePhrase(66, 0), 
			27 => CandlePhrase(51, 2), 
			26 => CandlePhrase(57, 2), 
			24 => CandlePhrase(78, 2), 
			23 => CandlePhrase(60, 2), 
			22 => CandlePhrase(65, 0), 
			21 => CandlePhrase(84, 0), 
			20 => CandlePhrase(65, 2), 
			19 => CandlePhrase(69, 2), 
			18 => CandlePhrase(75, 0), 
			17 => CandlePhrase(86, 0), 
			16 => CandlePhrase(82, 0), 
			15 => CandlePhrase(57, 0), 
			14 => CandlePhrase(52, 2), 
			13 => CandlePhrase(60, 0), 
			12 => CandlePhrase(52, 3), 
			11 => CandlePhrase(56, 1), 
			10 => CandlePhrase(51, 1), 
			9 => CandlePhrase(68, 3), 
			8 => CandlePhrase(54, 2), 
			7 => CandlePhrase(60, 3), 
			6 => CandlePhrase(59, 2), 
			5 => CandlePhrase(60, 1), 
			4 => CandlePhrase(57, 1), 
			3 => CandlePhrase(67, 3), 
			2 => CandlePhrase(75, 1), 
			_ => "", 
		};
	}

	private static string CandlePhrase(int Percentage, int RCType)
	{
		string text = "% of the time.";
		string result = "";
		switch (RCType)
		{
		case 0:
			result = "Bullish reversal " + Strings.Format((object)Percentage, "") + text;
			break;
		case 1:
			result = "Bullish continuation " + Strings.Format((object)Percentage, "") + text;
			break;
		case 2:
			result = "Bearish reversal " + Strings.Format((object)Percentage, "") + text;
			break;
		case 3:
			result = "Bearish continuation " + Strings.Format((object)Percentage, "") + text;
			break;
		}
		return result;
	}
}
