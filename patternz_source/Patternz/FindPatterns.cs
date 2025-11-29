using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Patternz.My;

namespace Patternz;

[StandardModule]
internal sealed class FindPatterns
{
	private const decimal Pct25 = 0.25m;

	private const decimal Pct50 = 0.5m;

	private const int PAT_TOP = 1;

	private const int PAT_BOTTOM = -1;

	private const decimal SHOULDER2SHOULDER = 0.25m;

	private const int TLSTART = 0;

	private const int TLEND = 1;

	private const int TLTOUCHCNT = 2;

	private const int TLSLOPE = 3;

	private const int SPIKELENGTH = 0;

	private const int PIPEDATE = 1;

	private static int[,] TLArray = new int[3, 1];

	private static decimal[] TLSlopeArray = new decimal[1];

	public static int[] ArrayBottoms;

	public static int[] ArrayTops;

	private static decimal ArmPit;

	private static bool NotSymmetrical;

	private static int HeadIndex;

	private static int Head2Index;

	private static int iLS2;

	private static int iRS2;

	public static double HarmonicTarget;

	[SpecialName]
	private static bool _0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag;

	[SpecialName]
	private static StaticLocalInitFlag _0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag_0024Init;

	public static void EnterFindPatterns(DateTime ChStart, DateTime ChEnd, ProgressBar Progress, ref bool StopPressed, int Source)
	{
		int Row = -1;
		EnterFindPatterns(ChStart, ChEnd, Progress, ref StopPressed, Source, null, ref Row, null);
	}

	public static void EnterFindPatterns(DateTime ChStart, DateTime ChEnd, ProgressBar Progress, ref bool StopPressed, int Source, string Filename, ref int Row, Control Ctrl)
	{
		GlobalForm.SetupDateIndexes(ChStart, ChEnd);
		if (GlobalForm.CandleCount > 0)
		{
			GlobalForm.CandlePatterns = null;
			GlobalForm.CandleCount = 0;
		}
		if (GlobalForm.ShowCandles)
		{
			FindCandles.GoFindCandles(ref Ctrl, Filename, ref Row, Source, Progress, ref StopPressed);
		}
		if (GlobalForm.PatternCount > 0)
		{
			GlobalForm.ChartPatterns = null;
			GlobalForm.PatternCount = 0;
			GlobalForm.NestedSpecial = Conversions.ToBoolean(Interaction.IIf(Source == 1, (object)true, (object)false));
		}
		if (GlobalForm.ShowAllPatterns)
		{
			if ((GlobalForm.PatternList[117] == 1) | (GlobalForm.PatternList[118] == 1) | (GlobalForm.PatternList[119] == 1) | (GlobalForm.PatternList[121] == 1) | (GlobalForm.PatternList[120] == 1))
			{
				FindAllGaps();
			}
			int num = 0;
			do
			{
				if (Progress != null)
				{
					Progress.Value = num % 100;
					((Control)Progress).Refresh();
				}
				if (GlobalForm.PatternList[num] == 1)
				{
					switch (num)
					{
					case 4:
					case 5:
						FindABCD(num);
						break;
					case 84:
						FindBARRB();
						break;
					case 83:
						FindBARRT();
						break;
					case 10:
					case 11:
						FindBat(num);
						break;
					case 111:
					case 112:
					case 113:
					case 114:
						FindBroadeningPatterns(num);
						break;
					case 109:
					case 110:
						FindBroadWedges(num);
						break;
					case 2:
					case 3:
						FindCarlV(num);
						break;
					case 52:
						FindCPRD();
						break;
					case 51:
						FindCPRU();
						break;
					case 8:
					case 9:
						FindButterfly(num);
						break;
					case 1:
					case 82:
						FindChannels(num);
						break;
					case 6:
					case 7:
						FindCrab(num);
						break;
					case 81:
						FindCup();
						break;
					case 100:
						FindDeadCatBounce();
						break;
					case 30:
						FindDivingBoard();
						break;
					case 99:
						FindIDCB();
						break;
					case 18:
					case 19:
					case 20:
					case 21:
					case 98:
					case 115:
						FindDoubleBottoms(num);
						break;
					case 14:
					case 15:
					case 16:
					case 17:
					case 97:
					case 116:
						FindDoubleTops(num);
						break;
					case 12:
					case 13:
						FindFakey(num);
						break;
					case 92:
					case 96:
						FindWedges(num);
						break;
					case 78:
						FindFlags();
						break;
					case 122:
						FindGap2H();
						break;
					case 123:
						FindGap2HInv();
						break;
					case 28:
					case 29:
						FindGartley(num);
						break;
					case 95:
						FindHTFlag();
						break;
					case 93:
					case 94:
						FindHeadShouldersBottom(num);
						break;
					case 107:
					case 108:
						FindHeadShouldersTop(num);
						break;
					case 50:
						FindHookRevD();
						break;
					case 49:
						FindHookRevU();
						break;
					case 106:
						FindHornBottoms();
						break;
					case 105:
						FindHornTops();
						break;
					case 77:
						FindInsideDay();
						break;
					case 75:
					case 76:
						FindIslands();
						break;
					case 47:
						FindKeyRevD();
						break;
					case 46:
						FindKeyRevU();
						break;
					case 73:
					case 74:
						FindMMU(num);
						break;
					case 72:
						FindNR4();
						break;
					case 71:
						FindNR7();
						break;
					case 45:
						FindOCRD();
						break;
					case 44:
						FindOCRU();
						break;
					case 70:
						FindODRB();
						break;
					case 69:
						FindODRT();
						break;
					case 68:
						FindOutsideDay();
						break;
					case 67:
						FindPennants();
						break;
					case 104:
						FindPipeBottoms();
						break;
					case 103:
						FindPipeTops();
						break;
					case 43:
						FindPivotD();
						break;
					case 42:
						FindPivotU();
						break;
					case 37:
						FindPothole();
						break;
					case 101:
					case 102:
						FindRectangles(num);
						break;
					case 66:
						FindRB();
						break;
					case 48:
					case 65:
						FindRTop(num);
						break;
					case 60:
						FindShark32();
						break;
					case 91:
						Find3FallPeaks();
						break;
					case 90:
						Find3RisingValleys();
						break;
					case 40:
						FindSpikeDown();
						break;
					case 41:
						FindSpikeUp();
						break;
					case 59:
						Find3Bar();
						break;
					case 32:
						FindThreeLR();
						break;
					case 31:
						FindThreeLRInv();
						break;
					case 57:
					case 58:
						FindTLs(num);
						break;
					case 89:
						FindAscendingTriangle();
						break;
					case 88:
						FindDescendingTriangle();
						break;
					case 87:
						FindSymTriangle();
						break;
					case 86:
						FindTripleBottoms();
						break;
					case 85:
						FindTripleTops();
						break;
					case 0:
						Findtwodance();
						break;
					case 23:
						FindTwoDid();
						break;
					case 22:
						FindTwoTall();
						break;
					case 34:
						FindUglyDoubleBottoms();
						break;
					case 33:
						FindUglyDoubleTops();
						break;
					case 56:
						FindVBottoms();
						break;
					case 55:
						FindVTops();
						break;
					case 24:
						FindVerticalRunDown();
						break;
					case 25:
						FindVerticalRunUp();
						break;
					case 53:
					case 54:
						FindWeeklyReversals(num);
						break;
					case 39:
						FindWideRangeD();
						break;
					case 38:
						FindWideRangeU();
						break;
					case 26:
					case 27:
						FindWolfeWave(num);
						break;
					}
				}
				if (num % 20 == 0)
				{
					((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				}
				if (StopPressed)
				{
					break;
				}
				num = checked(num + 1);
			}
			while (num <= 123);
		}
		if (Progress != null)
		{
			Progress.Value = 0;
		}
	}

	private static void FindBottomSpikeLength(int iPatternStart, int iPatternEnd, ref decimal LeftSpike, ref decimal RightSpike)
	{
		checked
		{
			if (iPatternStart - 1 > 0)
			{
				LeftSpike = new decimal(Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, iPatternStart - 1], GlobalForm.nHLC[2, iPatternStart + 1]) < 0, (object)(iPatternStart - 1), (object)(iPatternStart + 1))));
				if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, iPatternStart], GlobalForm.nHLC[2, iPatternStart]), 0m) != 0)
				{
					LeftSpike = decimal.Multiply(100m, decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, Convert.ToInt32(LeftSpike)], GlobalForm.nHLC[2, iPatternStart]), decimal.Subtract(GlobalForm.nHLC[1, iPatternStart], GlobalForm.nHLC[2, iPatternStart])));
				}
				else
				{
					LeftSpike = default(decimal);
				}
			}
			else
			{
				LeftSpike = default(decimal);
			}
			if (iPatternEnd + 1 <= GlobalForm.HLCRange)
			{
				RightSpike = new decimal(Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, iPatternEnd - 1], GlobalForm.nHLC[2, iPatternEnd + 1]) < 0, (object)(iPatternEnd - 1), (object)(iPatternEnd + 1))));
				if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, iPatternEnd], GlobalForm.nHLC[2, iPatternEnd]), 0m) != 0)
				{
					RightSpike = decimal.Multiply(100m, decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, Convert.ToInt32(RightSpike)], GlobalForm.nHLC[2, iPatternEnd]), decimal.Subtract(GlobalForm.nHLC[1, iPatternEnd], GlobalForm.nHLC[2, iPatternEnd])));
				}
				else
				{
					RightSpike = default(decimal);
				}
			}
			else
			{
				RightSpike = default(decimal);
			}
		}
	}

	private static void AddPattern(int iSDate, int iMDate, int iEndDate, int iS2Date, int iM2Date, int iE2Date, int pType, string pText)
	{
		checked
		{
			if (GlobalForm.PatternCount > 0)
			{
				int num = GlobalForm.PatternCount - 1;
				for (int i = 0; i <= num; i++)
				{
					if ((iSDate == GlobalForm.ChartPatterns[i].iStartDate) & (iEndDate == GlobalForm.ChartPatterns[i].iEndDate))
					{
						if ((pType == 115) & (GlobalForm.ChartPatterns[i].Type == 98))
						{
							GlobalForm.ChartPatterns[i].iText = Conversions.ToString(Interaction.IIf(Operators.CompareString(GlobalForm.ChartPatterns[i].iText, "DB?", false) == 0, (object)"BigW?", (object)"BigW"));
							GlobalForm.ChartPatterns[i].Type = 115;
							return;
						}
						if ((pType == 116) & (GlobalForm.ChartPatterns[i].Type == 97))
						{
							GlobalForm.ChartPatterns[i].iText = Conversions.ToString(Interaction.IIf(Operators.CompareString(GlobalForm.ChartPatterns[i].iText, "DT?", false) == 0, (object)"BigM?", (object)"BigM"));
							GlobalForm.ChartPatterns[i].Type = 116;
							return;
						}
					}
					unchecked
					{
						if (GlobalForm.ChartPatterns[i].Type == pType)
						{
							int iStartDate = GlobalForm.ChartPatterns[i].iStartDate;
							iStartDate = Conversions.ToInteger(Interaction.IIf((GlobalForm.ChartPatterns[i].iStart2Date != 0) & (GlobalForm.ChartPatterns[i].iStart2Date < iStartDate), (object)GlobalForm.ChartPatterns[i].iStart2Date, (object)iStartDate));
							int iEndDate2 = GlobalForm.ChartPatterns[i].iEndDate;
							iEndDate2 = Conversions.ToInteger(Interaction.IIf((GlobalForm.ChartPatterns[i].iEnd2Date != 0) & (GlobalForm.ChartPatterns[i].iEnd2Date > iEndDate2), (object)GlobalForm.ChartPatterns[i].iEnd2Date, (object)iEndDate2));
							int num2 = Conversions.ToInteger(Interaction.IIf(iS2Date != 0 && iSDate > iS2Date, (object)iS2Date, (object)iSDate));
							int num3 = Conversions.ToInteger(Interaction.IIf(iE2Date != 0 && iE2Date > iEndDate, (object)iE2Date, (object)iEndDate));
							if ((!GlobalForm.NestedSpecial && num2 >= iStartDate && num3 <= iEndDate2) || (iStartDate == num2 && iEndDate2 == num3) || (num2 >= iStartDate && num2 < iEndDate2 && num3 > iEndDate2) || (num2 <= iStartDate && num3 >= iStartDate && num3 <= iEndDate2) || (num2 >= iStartDate && num3 <= iEndDate2))
							{
								return;
							}
							if (iStartDate >= num2 && iEndDate2 <= num3 && GlobalForm.ChartPatterns[i].Type == pType && pType != 57 && pType != 58)
							{
								GlobalForm.ChartPatterns[i].iStartDate = iSDate;
								GlobalForm.ChartPatterns[i].iMidDate = iMDate;
								GlobalForm.ChartPatterns[i].iEndDate = iEndDate;
								GlobalForm.ChartPatterns[i].iStart2Date = iS2Date;
								GlobalForm.ChartPatterns[i].iMid2Date = iM2Date;
								GlobalForm.ChartPatterns[i].iEnd2Date = iE2Date;
								GlobalForm.ChartPatterns[i].PriceTarget = GlobalForm.LimitDecimals(new decimal(HarmonicTarget));
								return;
							}
							if ((pType == 102 || pType == 101) && ((num2 <= iStartDate && num3 <= iEndDate2 && num3 >= iStartDate) || (num2 >= iStartDate && num3 >= iEndDate2 && num2 <= iEndDate2)))
							{
								return;
							}
						}
					}
				}
			}
			GlobalForm.ChartPatterns = (GlobalForm.DisplayFmtns[])Utils.CopyArray((Array)GlobalForm.ChartPatterns, (Array)new GlobalForm.DisplayFmtns[GlobalForm.PatternCount + 1]);
			GlobalForm.ChartPatterns[GlobalForm.PatternCount].iStartDate = iSDate;
			GlobalForm.ChartPatterns[GlobalForm.PatternCount].iMidDate = iMDate;
			GlobalForm.ChartPatterns[GlobalForm.PatternCount].iEndDate = iEndDate;
			GlobalForm.ChartPatterns[GlobalForm.PatternCount].Type = pType;
			GlobalForm.ChartPatterns[GlobalForm.PatternCount].iText = pText;
			GlobalForm.ChartPatterns[GlobalForm.PatternCount].iStart2Date = iS2Date;
			GlobalForm.ChartPatterns[GlobalForm.PatternCount].iMid2Date = iM2Date;
			GlobalForm.ChartPatterns[GlobalForm.PatternCount].iEnd2Date = iE2Date;
			GlobalForm.ChartPatterns[GlobalForm.PatternCount].RenderColor = Color.Black;
			GlobalForm.ChartPatterns[GlobalForm.PatternCount].PriceTarget = GlobalForm.LimitDecimals(new decimal(HarmonicTarget));
			GlobalForm.PatternCount++;
		}
	}

	private static int BottomCheck(int i, int LastFound, int TLUpDown, decimal MinExcursion, bool Special, ref int TouchCnt, decimal MaxExcursion, int TLCount, int LinePart)
	{
		decimal d = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.002, (object)0.004));
		if (TLUpDown == 0 && decimal.Compare(decimal.Divide(Math.Abs(decimal.Subtract(GlobalForm.nHLC[2, ArrayBottoms[i]], GlobalForm.nHLC[2, ArrayBottoms[LastFound]])), Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[i]], GlobalForm.nHLC[2, ArrayBottoms[LastFound]]) < 0, (object)GlobalForm.nHLC[2, ArrayBottoms[i]], (object)GlobalForm.nHLC[2, ArrayBottoms[LastFound]]))), d) > 0)
		{
			return TLCount;
		}
		checked
		{
			if (ArrayBottoms[LastFound] - ArrayBottoms[i] == 0)
			{
				return TLCount;
			}
			decimal num = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, ArrayBottoms[LastFound]], GlobalForm.nHLC[2, ArrayBottoms[i]]), new decimal(ArrayBottoms[LastFound] - ArrayBottoms[i]));
			if (unchecked(((decimal.Compare(num, 0m) < 0 && TLUpDown == -1) | (decimal.Compare(num, 0m) > 0 && TLUpDown == 1)) || TLUpDown == 0))
			{
				bool flag = false;
				int num2 = ArrayBottoms[i] + 1;
				int num3 = ArrayBottoms[LastFound] - 1;
				for (int j = num2; j <= num3; j++)
				{
					decimal point = decimal.Add(decimal.Multiply(num, new decimal(j - ArrayBottoms[i])), GlobalForm.nHLC[2, ArrayBottoms[i]]);
					if (CheckOneNear(GlobalForm.nHLC[2, j], point, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)decimal.Negate(MinExcursion), (object)decimal.Negate(MaxExcursion)))))
					{
						return TLCount;
					}
				}
				if (!flag)
				{
					bool flag2 = default(bool);
					if (Special & (TouchCnt > 2))
					{
						if (LinePart == 0)
						{
							return TLCount;
						}
						int num4 = (int)Math.Round((double)(ArrayBottoms[LastFound] - ArrayBottoms[i]) / (double)LinePart);
						int num5 = ArrayBottoms[i] + num4;
						int num6 = ArrayBottoms[LastFound] - num4;
						flag2 = false;
						int num7 = num6;
						for (int k = num5; k <= num7; k++)
						{
							decimal point = decimal.Add(decimal.Multiply(num, new decimal(k - ArrayBottoms[i])), GlobalForm.nHLC[2, ArrayBottoms[i]]);
							if (CheckNearness(GlobalForm.nHLC[2, k], point, -1m, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)MinExcursion, (object)MaxExcursion))))
							{
								flag2 = true;
								break;
							}
						}
					}
					if (unchecked((Special & (TouchCnt == 2 || flag2)) || !Special))
					{
						int iStart = ArrayBottoms[i];
						int iEnd = ArrayBottoms[LastFound];
						if (!DupCheck(TLCount, iStart, iEnd))
						{
							TLArray = (int[,])Utils.CopyArray((Array)TLArray, (Array)new int[3, TLCount + 1]);
							TLSlopeArray = (decimal[])Utils.CopyArray((Array)TLSlopeArray, (Array)new decimal[TLCount + 1]);
							TLArray[0, TLCount] = ArrayBottoms[i];
							TLArray[1, TLCount] = ArrayBottoms[LastFound];
							TLArray[2, TLCount] = TouchCnt;
							TLSlopeArray[TLCount] = num;
							TLCount++;
						}
					}
				}
			}
			return TLCount;
		}
	}

	public static bool BWVerify(int PatternType, decimal SlopeBottom, decimal SlopeTop, decimal MinTLSlope, ref int iTStart, ref int iTEnd, ref int iBStart, ref int iBEnd)
	{
		bool flag = false;
		switch (PatternType)
		{
		case 110:
			if (CheckSlope(GlobalForm.nHLC[2, iBStart], GlobalForm.nHLC[2, iBEnd], 0.005m) == 0)
			{
				return false;
			}
			if (decimal.Compare(Math.Abs(SlopeBottom), decimal.Subtract(Math.Abs(SlopeTop), decimal.Multiply(7m, MinTLSlope))) < 0)
			{
				flag = true;
			}
			break;
		case 109:
			if (CheckSlope(GlobalForm.nHLC[1, iTStart], GlobalForm.nHLC[1, iTEnd], 0.005m) == 0)
			{
				return false;
			}
			if (decimal.Compare(Math.Abs(SlopeBottom), decimal.Add(Math.Abs(SlopeTop), decimal.Multiply(7m, MinTLSlope))) > 0)
			{
				flag = true;
			}
			break;
		}
		checked
		{
			decimal d = new decimal(iTEnd - iTStart);
			decimal d2 = new decimal(iBEnd - iBStart);
			decimal d3 = decimal.Subtract(GlobalForm.nHLC[1, iTEnd], GlobalForm.nHLC[1, iTStart]);
			decimal d4 = decimal.Subtract(GlobalForm.nHLC[2, iBEnd], GlobalForm.nHLC[2, iBStart]);
			decimal d5 = decimal.Divide(d3, d);
			decimal d6 = decimal.Divide(d4, d2);
			decimal d7 = Math.Abs(decimal.Divide(d5, d6));
			if (flag & (decimal.Compare(d7, 0.6m) > 0) & (decimal.Compare(d7, 1.4m) < 0))
			{
				flag = false;
			}
			return flag;
		}
	}

	private static int CheckConfirmation(int StartIndex, int EndIndex, int BotTop)
	{
		checked
		{
			int num = StartIndex + 1;
			int num2 = StartIndex;
			int hLCRange = GlobalForm.HLCRange;
			for (int i = StartIndex; i <= hLCRange; i++)
			{
				if (i <= EndIndex)
				{
					num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0, (object)i, (object)num));
					num2 = Conversions.ToInteger(Interaction.IIf((decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num2]) < 0) | (decimal.Compare(GlobalForm.nHLC[2, i], 0m) == 0), (object)i, (object)num2));
				}
				if (i <= EndIndex)
				{
					continue;
				}
				if (BotTop == -1)
				{
					if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[1, num]) > 0)
					{
						return 1;
					}
					if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[2, num2]) < 0)
					{
						return -1;
					}
				}
				else
				{
					if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[2, num2]) < 0)
					{
						return -1;
					}
					if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[1, num]) > 0)
					{
						return 1;
					}
				}
			}
			return 0;
		}
	}

	private static bool CheckDBDownTrend(int j, int l, decimal Margin, int Flag)
	{
		decimal priceScale = GetPriceScale(GlobalForm.nHLC[2, ArrayBottoms[j]], GlobalForm.nHLC[2, ArrayBottoms[l]]);
		if (decimal.Compare(priceScale, 0m) == 0)
		{
			return true;
		}
		checked
		{
			int num = ArrayBottoms[j + 1];
			int num2 = ArrayBottoms[l - 1];
			for (int i = num; i <= num2; i++)
			{
				if ((decimal.Compare(decimal.Divide(GlobalForm.nHLC[2, i], priceScale), decimal.Add(decimal.Divide(GlobalForm.nHLC[2, ArrayBottoms[j]], priceScale), decimal.Divide(Margin, 3m))) <= 0) | (decimal.Compare(decimal.Divide(GlobalForm.nHLC[2, i], priceScale), decimal.Add(decimal.Divide(GlobalForm.nHLC[2, ArrayBottoms[l]], priceScale), decimal.Divide(Margin, 3m))) <= 0))
				{
					return true;
				}
			}
			int num3 = -1;
			int num4 = Information.UBound((Array)ArrayTops, 1);
			for (int i = 0; i <= num4; i++)
			{
				if ((ArrayBottoms[j] < ArrayTops[i]) & (ArrayBottoms[l] > ArrayTops[i]))
				{
					if (num3 == -1)
					{
						num3 = i;
					}
					if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[i]], GlobalForm.nHLC[1, ArrayTops[num3]]) > 0)
					{
						num3 = i;
					}
				}
				if (ArrayTops[i] > ArrayBottoms[l])
				{
					break;
				}
			}
			if (num3 == -1)
			{
				return true;
			}
			int num5 = -1;
			int num6 = ArrayBottoms[l] + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num6; i <= chartEndIndex; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[1, ArrayTops[num3]]) > 0)
				{
					num5 = i;
					break;
				}
			}
			if (num5 == -1)
			{
				num5 = GlobalForm.ChartEndIndex;
			}
			int num7 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[j]], GlobalForm.nHLC[2, ArrayBottoms[l]]) > 0, (object)j, (object)l));
			int num8 = l + 1;
			int num9 = ArrayBottoms.Length - 1;
			for (int i = num8; i <= num9 && ArrayBottoms[i] < num5; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[i]], GlobalForm.nHLC[2, ArrayBottoms[num7]]) <= 0)
				{
					return true;
				}
			}
			decimal num10 = decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[num3]], GlobalForm.nHLC[2, ArrayBottoms[l]]);
			decimal num11 = decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[num3]], GlobalForm.nHLC[2, ArrayBottoms[j]]);
			num10 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num10, num11) > 0, (object)num10, (object)num11));
			int num12 = Convert.ToInt32(decimal.Add(decimal.Multiply(2.5m, new decimal(ArrayBottoms[j] - ArrayBottoms[l])), new decimal(ArrayBottoms[j])));
			num12 = Conversions.ToInteger(Interaction.IIf(num12 < 0, (object)0, (object)num12));
			for (int i = j - 1; i >= 0; i += -1)
			{
				if ((decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[i]], GlobalForm.nHLC[2, ArrayBottoms[j]]) <= 0) | (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[i]], GlobalForm.nHLC[2, ArrayBottoms[l]]) <= 0))
				{
					return true;
				}
				if (unchecked(Flag == 98 || Flag == 20 || Flag == 21 || Flag == 18 || Flag == 19))
				{
					if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[i]], GlobalForm.nHLC[1, ArrayTops[num3]]) > 0)
					{
						return false;
					}
				}
				else if (decimal.Compare(GlobalForm.nHLC[1, ArrayBottoms[i]], decimal.Add(decimal.Multiply(num10, 1m), GlobalForm.nHLC[1, ArrayTops[num3]])) > 0)
				{
					return false;
				}
				if (ArrayBottoms[i] < num12)
				{
					if (Flag == 115)
					{
						return true;
					}
					return false;
				}
			}
			for (int i = ArrayBottoms[j] - 1; i >= 0; i += -1)
			{
				if (unchecked(Flag == 98 || Flag == 20 || Flag == 21 || Flag == 18 || Flag == 19))
				{
					if (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[1, ArrayTops[num3]]) > 0)
					{
						return false;
					}
				}
				else if (decimal.Compare(GlobalForm.nHLC[1, i], decimal.Add(decimal.Multiply(num10, 1m), GlobalForm.nHLC[1, ArrayTops[num3]])) > 0)
				{
					return false;
				}
				if (i < num12)
				{
					if (Flag == 115)
					{
						return true;
					}
					return false;
				}
			}
			return true;
		}
	}

	private static bool CheckDTUpTrend(int i, int l, decimal Margin, int Flag)
	{
		decimal priceScale = GetPriceScale(GlobalForm.nHLC[1, ArrayTops[i]], GlobalForm.nHLC[1, ArrayTops[l]]);
		if (decimal.Compare(priceScale, 0m) == 0)
		{
			return true;
		}
		checked
		{
			int num = ArrayTops[i + 1];
			int num2 = ArrayTops[l - 1];
			for (int j = num; j <= num2; j++)
			{
				if ((decimal.Compare(decimal.Divide(GlobalForm.nHLC[1, j], priceScale), decimal.Subtract(decimal.Divide(GlobalForm.nHLC[1, ArrayTops[i]], priceScale), decimal.Divide(Margin, 3m))) >= 0) | (decimal.Compare(decimal.Divide(GlobalForm.nHLC[1, j], priceScale), decimal.Subtract(decimal.Divide(GlobalForm.nHLC[1, ArrayTops[l]], priceScale), decimal.Divide(Margin, 3m))) >= 0))
				{
					return true;
				}
			}
			int num3 = -1;
			int num4 = Information.UBound((Array)ArrayBottoms, 1);
			for (int j = 0; j <= num4; j++)
			{
				if ((ArrayBottoms[j] > ArrayTops[i]) & (ArrayBottoms[j] < ArrayTops[l]))
				{
					if (num3 == -1)
					{
						num3 = j;
					}
					if ((decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[j]], 0m) != 0) & (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[j]], GlobalForm.nHLC[2, ArrayBottoms[num3]]) < 0))
					{
						num3 = j;
					}
				}
				if (ArrayBottoms[j] > ArrayTops[l])
				{
					break;
				}
			}
			if (num3 == -1)
			{
				return true;
			}
			int num5 = -1;
			int num6 = ArrayTops[l] + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int j = num6; j <= chartEndIndex; j++)
			{
				if (decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[2, ArrayBottoms[num3]]) < 0)
				{
					num5 = j;
					break;
				}
			}
			if (num5 == -1)
			{
				num5 = GlobalForm.ChartEndIndex;
			}
			int num7 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, ArrayTops[i]], GlobalForm.nHLC[1, ArrayTops[l]]) < 0, (object)i, (object)l));
			int num8 = l + 1;
			int num9 = ArrayTops.Length - 1;
			for (int j = num8; j <= num9 && ArrayTops[j] < num5; j++)
			{
				if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[1, ArrayTops[num7]]) >= 0)
				{
					return true;
				}
			}
			decimal num10 = decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[l]], GlobalForm.nHLC[2, ArrayBottoms[num3]]);
			decimal num11 = decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[i]], GlobalForm.nHLC[2, ArrayBottoms[num3]]);
			num10 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num11, num10) > 0, (object)num11, (object)num10));
			int num12 = Convert.ToInt32(decimal.Add(decimal.Multiply(2.5m, new decimal(ArrayTops[i] - ArrayTops[l])), new decimal(ArrayTops[i])));
			num12 = Conversions.ToInteger(Interaction.IIf(num12 < 0, (object)0, (object)num12));
			for (int j = i - 1; j >= 0; j += -1)
			{
				if ((decimal.Compare(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[1, ArrayTops[i]]) >= 0) | (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[1, ArrayTops[l]]) >= 0))
				{
					return true;
				}
				if (unchecked(Flag == 97 || Flag == 16 || Flag == 17 || Flag == 15 || Flag == 14))
				{
					if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[2, ArrayBottoms[num3]]) < 0)
					{
						return false;
					}
				}
				else if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[j]], decimal.Subtract(GlobalForm.nHLC[2, ArrayBottoms[num3]], decimal.Multiply(num10, 1m))) < 0)
				{
					return false;
				}
				if (ArrayTops[j] < num12)
				{
					if (Flag == 116)
					{
						return true;
					}
					return false;
				}
			}
			for (int j = ArrayTops[i] - 1; j >= 0; j += -1)
			{
				if ((decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, ArrayTops[i]]) >= 0) | (decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, ArrayTops[l]]) >= 0))
				{
					return true;
				}
				if (unchecked(Flag == 97 || Flag == 16 || Flag == 17 || Flag == 15 || Flag == 14))
				{
					if (decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[2, ArrayBottoms[num3]]) < 0)
					{
						return false;
					}
				}
				else if (decimal.Compare(GlobalForm.nHLC[1, j], decimal.Subtract(GlobalForm.nHLC[2, ArrayBottoms[num3]], decimal.Multiply(num10, 1m))) < 0)
				{
					return false;
				}
				if (j < num12)
				{
					if (Flag == 116)
					{
						return true;
					}
					return false;
				}
			}
			return true;
		}
	}

	private static bool CheckFor3rdBottom(int iBottom1, int iBottom2, int iBottom3, decimal Close)
	{
		checked
		{
			int num = ArrayBottoms[iBottom1] + 1;
			int num2 = ArrayBottoms[iBottom1] + 1;
			int num3 = ArrayBottoms[iBottom3] - 1;
			for (int i = num2; i <= num3; i++)
			{
				num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0, (object)i, (object)num));
			}
			int num4 = -1;
			int num5 = ArrayBottoms[iBottom3] + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num5; i <= chartEndIndex; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[1, num]) > 0)
				{
					num4 = i;
					break;
				}
			}
			if (num4 == -1)
			{
				num4 = GlobalForm.ChartEndIndex;
			}
			decimal num6 = GlobalForm.nHLC[2, ArrayBottoms[iBottom1]];
			num6 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num6, GlobalForm.nHLC[2, ArrayBottoms[iBottom2]]) > 0, (object)num6, (object)GlobalForm.nHLC[2, ArrayBottoms[iBottom2]]));
			num6 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num6, GlobalForm.nHLC[2, ArrayBottoms[iBottom3]]) > 0, (object)num6, (object)GlobalForm.nHLC[2, ArrayBottoms[iBottom3]]));
			num6 = decimal.Add(num6, Close);
			if (iBottom3 + 1 < Information.UBound((Array)ArrayBottoms, 1))
			{
				int num7 = ArrayBottoms[iBottom3 + 1];
				int num8 = num4;
				for (int i = num7; i <= num8; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[2, i], num6) <= 0)
					{
						return true;
					}
				}
			}
			return false;
		}
	}

	private static bool CheckForTop(int iPatternStart, int iPatternEnd, decimal Close)
	{
		checked
		{
			int num = ArrayTops[iPatternStart] + 1;
			decimal num2 = GlobalForm.nHLC[1, ArrayTops[iPatternStart]];
			int num3 = ArrayTops[iPatternStart];
			int num4 = ArrayTops[iPatternEnd] - 1;
			for (int i = num3; i <= num4; i++)
			{
				num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num]) < 0, (object)i, (object)num));
				if (decimal.Compare(GlobalForm.nHLC[1, i], num2) > 0)
				{
					num2 = GlobalForm.nHLC[1, i];
				}
			}
			num2 = decimal.Subtract(num2, Close);
			int num5 = -1;
			int num6 = ArrayTops[iPatternEnd] + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num6; i <= chartEndIndex; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[2, num]) < 0)
				{
					num5 = i;
					break;
				}
			}
			if (num5 == -1)
			{
				num5 = GlobalForm.ChartEndIndex;
			}
			if (iPatternEnd + 1 < Information.UBound((Array)ArrayTops, 1))
			{
				int num7 = ArrayTops[iPatternEnd + 1];
				int num8 = num5;
				for (int i = num7; i <= num8; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[1, i], num2) >= 0)
					{
						return true;
					}
				}
			}
			return false;
		}
	}

	private static bool CheckHSBSlope(int LSIndex, int RSIndex, int i, int j, int z, int Flag)
	{
		int num = HeadIndex;
		checked
		{
			if (Flag == 93 && Head2Index != 0)
			{
				num = Conversions.ToInteger(Interaction.IIf(HeadIndex < Head2Index, (object)HeadIndex, (object)Head2Index));
				j = -1;
				int num2 = i + 1;
				int num3 = z - 1;
				for (int k = num2; k <= num3; k++)
				{
					if (num == ArrayBottoms[k])
					{
						j = k;
						break;
					}
				}
				if (j == -1)
				{
					return true;
				}
			}
			if (num - LSIndex == 0)
			{
				return true;
			}
			decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, num], GlobalForm.nHLC[2, LSIndex]), new decimal(num - LSIndex));
			int num4 = i + 1;
			int num5 = j - 1;
			for (int k = num4; k <= num5; k++)
			{
				decimal d2 = decimal.Add(decimal.Multiply(d, new decimal(ArrayBottoms[k] - num)), GlobalForm.nHLC[2, num]);
				if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[k]], decimal.Multiply(d2, 1m)) < 0 && !(!GlobalForm.StrictPatterns & (ArrayBottoms[j] - ArrayBottoms[k] < 5)))
				{
					return true;
				}
			}
			if (Flag == 93 && Head2Index != 0)
			{
				num = Conversions.ToInteger(Interaction.IIf(HeadIndex < Head2Index, (object)Head2Index, (object)HeadIndex));
				j = -1;
				int num6 = i + 1;
				int num7 = z - 1;
				for (int k = num6; k <= num7; k++)
				{
					if (num == ArrayBottoms[k])
					{
						j = k;
						break;
					}
				}
				if (j == -1)
				{
					return true;
				}
			}
			if (RSIndex - num == 0)
			{
				return true;
			}
			d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, RSIndex], GlobalForm.nHLC[2, num]), new decimal(RSIndex - num));
			int num8 = j + 1;
			int num9 = z - 1;
			for (int k = num8; k <= num9; k++)
			{
				decimal d2 = decimal.Add(decimal.Multiply(d, new decimal(ArrayBottoms[k] - num)), GlobalForm.nHLC[2, num]);
				if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[k]], decimal.Multiply(d2, 1m)) < 0 && !(!GlobalForm.StrictPatterns & (ArrayBottoms[k] - ArrayBottoms[j] < 5)))
				{
					return true;
				}
			}
			return false;
		}
	}

	private static bool CheckLongNeck(int LSIndex, int RSIndex, decimal ArmPitHigh, int Flag)
	{
		decimal num = GlobalForm.nHLC[2, LSIndex];
		num = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num, GlobalForm.nHLC[2, RSIndex]) > 0, (object)num, (object)GlobalForm.nHLC[2, RSIndex]));
		if ((Flag == 93) & (iLS2 != 0) & (iRS2 != 0))
		{
			num = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num, GlobalForm.nHLC[2, iLS2]) > 0, (object)num, (object)GlobalForm.nHLC[2, iLS2]));
			num = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num, GlobalForm.nHLC[2, iRS2]) > 0, (object)num, (object)GlobalForm.nHLC[2, iRS2]));
		}
		if (decimal.Compare(GlobalForm.nHLC[2, HeadIndex], 0m) != 0)
		{
			decimal d = decimal.Divide(decimal.Subtract(num, GlobalForm.nHLC[2, HeadIndex]), GlobalForm.nHLC[2, HeadIndex]);
			decimal d2 = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.065, (object)0.2));
			if (decimal.Compare(d, d2) > 0)
			{
				return true;
			}
			decimal d3 = Conversions.ToDecimal(Interaction.IIf(Flag == 93, (object)0.75, (object)0.75));
			decimal num2 = new decimal(Math.Abs(Convert.ToSingle(ArmPitHigh) - Conversions.ToSingle(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, LSIndex], GlobalForm.nHLC[2, RSIndex]) > 0, (object)GlobalForm.nHLC[2, RSIndex], (object)GlobalForm.nHLC[2, LSIndex]))));
			decimal d4 = decimal.Subtract(Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, LSIndex], GlobalForm.nHLC[2, RSIndex]) > 0, (object)GlobalForm.nHLC[2, RSIndex], (object)GlobalForm.nHLC[2, LSIndex])), GlobalForm.nHLC[2, HeadIndex]);
			if (decimal.Compare(num2, 0m) != 0 && decimal.Compare(decimal.Divide(d4, num2), d3) > 0)
			{
				return true;
			}
		}
		return false;
	}

	public static bool CheckNearness(decimal Point1, decimal Point2, decimal Percent, decimal PriceVary)
	{
		bool result;
		try
		{
			if ((decimal.Compare(Percent, -1m) == 0) & (decimal.Compare(PriceVary, -1m) == 0))
			{
				result = false;
			}
			else if ((decimal.Compare(Point1, 0m) == 0) | (decimal.Compare(Point2, 0m) == 0))
			{
				result = false;
			}
			else
			{
				if (decimal.Compare(PriceVary, -1m) != 0)
				{
					if (GlobalForm.Futures)
					{
						PriceVary = decimal.Divide(PriceVary, 4m);
					}
					else if (GlobalForm.NearFutures)
					{
						PriceVary = decimal.Divide(PriceVary, 2m);
					}
					if ((decimal.Compare(Point1, 2500m) > 0) | (decimal.Compare(Point2, 2500m) > 0))
					{
						PriceVary = decimal.Divide(PriceVary, 2m);
					}
					if ((decimal.Compare(Point1, 5000m) > 0) | (decimal.Compare(Point2, 5000m) > 0))
					{
						PriceVary = decimal.Divide(PriceVary, 2m);
					}
					if ((decimal.Compare(Point1, 10000m) > 0) | (decimal.Compare(Point2, 10000m) > 0))
					{
						PriceVary = decimal.Divide(PriceVary, 2m);
					}
					if ((decimal.Compare(Point1, 50000m) > 0) | (decimal.Compare(Point2, 50000m) > 0))
					{
						PriceVary = decimal.Divide(PriceVary, 2m);
					}
				}
				if (decimal.Compare(Percent, -1m) != 0)
				{
					Percent = GetPercent(Percent);
				}
				decimal priceScale = GetPriceScale(Point1, Point2);
				result = decimal.Compare(priceScale, 0m) != 0 && ((decimal.Compare(Percent, -1m) == 0) ? (decimal.Compare(Math.Abs(decimal.Subtract(decimal.Divide(Point1, priceScale), decimal.Divide(Point2, priceScale))), PriceVary) <= 0) : ((decimal.Compare(PriceVary, -1m) == 0) ? (GlobalForm.StrictPatterns ? (decimal.Compare(decimal.Divide(decimal.Multiply(100m, Math.Abs(decimal.Subtract(Point1, Point2))), Conversions.ToDecimal(Interaction.IIf(decimal.Compare(Point1, Point2) < 0, (object)Point1, (object)Point2))), Percent) <= 0) : (((decimal.Compare(decimal.Divide(decimal.Multiply(100m, Math.Abs(decimal.Subtract(Point1, Point2))), Point1), Percent) <= 0) | (decimal.Compare(decimal.Divide(decimal.Multiply(100m, Math.Abs(decimal.Subtract(Point1, Point2))), Point2), Percent) <= 0)) ? true : false)) : (((decimal.Compare(Math.Abs(decimal.Subtract(decimal.Divide(Point1, priceScale), decimal.Divide(Point2, priceScale))), PriceVary) <= 0) | (decimal.Compare(decimal.Divide(decimal.Multiply(100m, Math.Abs(decimal.Subtract(Point1, Point2))), Point1), Percent) <= 0) | (decimal.Compare(decimal.Divide(decimal.Multiply(100m, Math.Abs(decimal.Subtract(Point1, Point2))), Point2), Percent) <= 0)) ? true : false)));
			}
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

	public static bool CheckOneNear(decimal Point1, decimal Point2, decimal PriceVary)
	{
		decimal priceScale = GetPriceScale(Point1, Point2);
		if (decimal.Compare(priceScale, 0m) == 0)
		{
			return true;
		}
		if (decimal.Compare(PriceVary, 0m) > 0)
		{
			return Conversions.ToBoolean(Interaction.IIf(decimal.Compare(decimal.Divide(Point1, priceScale), decimal.Add(decimal.Divide(Point2, priceScale), PriceVary)) > 0, (object)true, (object)false));
		}
		return Conversions.ToBoolean(Interaction.IIf(decimal.Compare(decimal.Divide(Point1, priceScale), decimal.Add(decimal.Divide(Point2, priceScale), PriceVary)) < 0, (object)true, (object)false));
	}

	private static bool CheckShoulderDistance(int Flag, int LSIndex, int RSIndex)
	{
		NotSymmetrical = false;
		checked
		{
			int num = RSIndex - HeadIndex;
			int num2 = HeadIndex - LSIndex;
			if (num2 < num)
			{
				num = HeadIndex - LSIndex;
				num2 = RSIndex - HeadIndex;
			}
			if (num != 0 && (double)num2 / (double)num > 1.5)
			{
				if (Flag == 94)
				{
					return true;
				}
				NotSymmetrical = true;
			}
			return false;
		}
	}

	public static int CheckSlope(decimal StartPrice, decimal EndPrice, decimal MaxDeviation)
	{
		if (decimal.Compare(StartPrice, 0m) == 0)
		{
			return 0;
		}
		decimal d = decimal.Divide(decimal.Subtract(EndPrice, StartPrice), StartPrice);
		int result = default(int);
		if (decimal.Compare(d, decimal.Multiply(-1m, MaxDeviation)) >= 0 && decimal.Compare(d, decimal.Multiply(1m, MaxDeviation)) <= 0)
		{
			result = 0;
		}
		else if (decimal.Compare(d, 0m) > 0)
		{
			result = 1;
		}
		else if (decimal.Compare(d, 0m) < 0)
		{
			result = -1;
		}
		return result;
	}

	private static bool CheckSpikes(int i, decimal Spike, int SpikeCount, object[,] Spikes)
	{
		checked
		{
			if (SpikeCount > 0)
			{
				decimal d = default(decimal);
				int num = 0;
				for (int j = SpikeCount; j >= 0; j += -1)
				{
					if (decimal.Compare(Conversions.ToDecimal(Spikes[0, j]), 0m) <= 0)
					{
						continue;
					}
					if (!GlobalForm.IntradayData)
					{
						if (DateTime.Compare(DateAndTime.DateAdd((DateInterval)0, -1.0, GlobalForm.nDT[0, i + 1]), GlobalForm.MyCDate(RuntimeHelpers.GetObjectValue(Spikes[1, j]))) >= 0)
						{
							break;
						}
						d = decimal.Add(d, Conversions.ToDecimal(Spikes[0, j]));
						num++;
						continue;
					}
					int num2 = ((i + 1 >= 262) ? (i + 1 - 262) : (i + 1));
					if (DateTime.Compare(GlobalForm.nDT[0, i + 1 - num2], GlobalForm.MyCDate(RuntimeHelpers.GetObjectValue(Spikes[1, j]))) >= 0)
					{
						break;
					}
					d = decimal.Add(d, Conversions.ToDecimal(Spikes[0, j]));
					num++;
				}
				if (num == 0)
				{
					return false;
				}
				if (decimal.Compare(Spike, decimal.Divide(d, new decimal(num))) >= 0)
				{
					return false;
				}
				return true;
			}
			return false;
		}
	}

	private static bool CheckSpikesT(int i, decimal Spike, int SpikeCount, object[,] Spikes)
	{
		checked
		{
			if (SpikeCount > 0)
			{
				decimal d = default(decimal);
				int num = 0;
				for (int j = SpikeCount; j >= 0; j += -1)
				{
					if (decimal.Compare(Conversions.ToDecimal(Spikes[0, j]), 0m) <= 0)
					{
						continue;
					}
					if (!GlobalForm.IntradayData)
					{
						if (DateTime.Compare(DateAndTime.DateAdd((DateInterval)0, -1.0, GlobalForm.nDT[0, i + 1]), GlobalForm.MyCDate(RuntimeHelpers.GetObjectValue(Spikes[1, j]))) >= 0)
						{
							break;
						}
						d = decimal.Add(d, Conversions.ToDecimal(Spikes[0, j]));
						num++;
						continue;
					}
					int num2 = ((i + 1 >= 262) ? (i + 1 - 262) : (i + 1));
					if (DateTime.Compare(GlobalForm.nDT[0, i + 1 - num2], GlobalForm.MyCDate(RuntimeHelpers.GetObjectValue(Spikes[1, j]))) >= 0)
					{
						break;
					}
					d = decimal.Add(d, Conversions.ToDecimal(Spikes[0, j]));
					num++;
				}
				if (num == 0)
				{
					return false;
				}
				if (decimal.Compare(Spike, decimal.Divide(d, new decimal(num))) >= 0)
				{
					return false;
				}
				return true;
			}
			return false;
		}
	}

	private static bool CheckSymTri(int iTstart, int iTend, int iBstart, int iBend)
	{
		int num = Conversions.ToInteger(Interaction.IIf(iTstart < iBstart, (object)iTstart, (object)iBstart));
		int num2 = Conversions.ToInteger(Interaction.IIf(iTend > iBend, (object)iTend, (object)iBend));
		int num3 = num2;
		for (int i = num; i <= num3; i = checked(i + 1))
		{
			if (i != iTstart && decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, iTstart]) >= 0)
			{
				return true;
			}
			if (i != iBstart && decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, iBstart]) <= 0)
			{
				return true;
			}
		}
		return false;
	}

	private static bool CheckTopLongNeck(int LSIndex, int RSIndex, decimal ArmPitLow, int Flag)
	{
		decimal num = GlobalForm.nHLC[1, LSIndex];
		num = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num, GlobalForm.nHLC[1, RSIndex]) < 0, (object)num, (object)GlobalForm.nHLC[1, RSIndex]));
		if ((Flag == 93) & (iLS2 != 0) & (iRS2 != 0))
		{
			num = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num, GlobalForm.nHLC[1, iLS2]) < 0, (object)num, (object)GlobalForm.nHLC[1, iLS2]));
			num = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num, GlobalForm.nHLC[1, iRS2]) < 0, (object)num, (object)GlobalForm.nHLC[1, iRS2]));
		}
		if (decimal.Compare(GlobalForm.nHLC[1, HeadIndex], 0m) == 0)
		{
			return false;
		}
		decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, HeadIndex], num), GlobalForm.nHLC[1, HeadIndex]);
		decimal d2 = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.065, (object)0.2));
		if (decimal.Compare(d, d2) > 0)
		{
			return true;
		}
		decimal d3 = Conversions.ToDecimal(Interaction.IIf(Flag == 108, (object)0.5, (object)0.75));
		decimal num2 = Math.Abs(decimal.Subtract(Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, LSIndex], GlobalForm.nHLC[1, RSIndex]) < 0, (object)GlobalForm.nHLC[1, RSIndex], (object)GlobalForm.nHLC[1, LSIndex])), ArmPitLow));
		decimal d4 = decimal.Subtract(GlobalForm.nHLC[1, HeadIndex], Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, LSIndex], GlobalForm.nHLC[1, RSIndex]) < 0, (object)GlobalForm.nHLC[1, RSIndex], (object)GlobalForm.nHLC[1, LSIndex])));
		if (decimal.Compare(num2, 0m) != 0 && decimal.Compare(decimal.Divide(d4, num2), d3) > 0)
		{
			return true;
		}
		return false;
	}

	private static bool CheckTopShoulderDistance(int Flag, int LSIndex, int RSIndex)
	{
		NotSymmetrical = false;
		checked
		{
			int num = RSIndex - HeadIndex;
			int num2 = HeadIndex - LSIndex;
			if (num2 < num)
			{
				num = HeadIndex - LSIndex;
				num2 = RSIndex - HeadIndex;
			}
			if (num != 0 && (double)num2 / (double)num > 1.5)
			{
				if (Flag == 107)
				{
					return true;
				}
				NotSymmetrical = true;
			}
			return false;
		}
	}

	private static bool CheckTopSlope(int LSIndex, int RSIndex, int i, int j, int z, int Flag)
	{
		int num = HeadIndex;
		checked
		{
			if (Flag == 108 && Head2Index != 0)
			{
				num = Conversions.ToInteger(Interaction.IIf(HeadIndex < Head2Index, (object)HeadIndex, (object)Head2Index));
				j = -1;
				int num2 = i + 1;
				int num3 = z - 1;
				for (int k = num2; k <= num3; k++)
				{
					if (num == ArrayTops[k])
					{
						j = k;
						break;
					}
				}
				if (j == -1)
				{
					return true;
				}
			}
			if (num - LSIndex == 0)
			{
				return true;
			}
			decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[1, LSIndex]), new decimal(num - LSIndex));
			int num4 = i + 1;
			int num5 = j - 1;
			for (int k = num4; k <= num5; k++)
			{
				decimal d2 = decimal.Add(decimal.Multiply(d, new decimal(ArrayTops[k] - num)), GlobalForm.nHLC[1, num]);
				if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[k]], decimal.Multiply(d2, 1m)) > 0 && !(!GlobalForm.StrictPatterns & (ArrayTops[j] - ArrayTops[k] < 5)))
				{
					return true;
				}
			}
			if (Flag == 108 && Head2Index != 0)
			{
				num = Conversions.ToInteger(Interaction.IIf(HeadIndex < Head2Index, (object)Head2Index, (object)HeadIndex));
				j = -1;
				int num6 = i + 1;
				int num7 = z - 1;
				for (int k = num6; k <= num7; k++)
				{
					if (num == ArrayTops[k])
					{
						j = k;
						break;
					}
				}
				if (j == -1)
				{
					return true;
				}
			}
			if (RSIndex - num == 0)
			{
				return true;
			}
			d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, RSIndex], GlobalForm.nHLC[1, num]), new decimal(RSIndex - num));
			int num8 = j + 1;
			int num9 = z - 1;
			for (int k = num8; k <= num9; k++)
			{
				decimal d2 = decimal.Add(decimal.Multiply(d, new decimal(ArrayTops[k] - num)), GlobalForm.nHLC[1, num]);
				if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[k]], decimal.Multiply(d2, 1m)) > 0 && !(!GlobalForm.StrictPatterns & (ArrayTops[k] - ArrayTops[j] < 5)))
				{
					return true;
				}
			}
			return false;
		}
	}

	private static bool CheckTouches(int iTopStart, int iTopEnd, int iBottomStart, int iBottomEnd)
	{
		bool flag = true;
		int chartStartIndex = GlobalForm.ChartStartIndex;
		int chartEndIndex = GlobalForm.ChartEndIndex;
		checked
		{
			GlobalForm.ChartStartIndex = (int)Math.Round((double)iTopStart + (double)(iTopEnd - iTopStart) / 6.0);
			GlobalForm.ChartEndIndex = (int)Math.Round((double)iTopEnd - (double)(iTopEnd - iTopStart) / 6.0);
			if (GlobalForm.ChartEndIndex > GlobalForm.ChartStartIndex)
			{
				FindAllTops(2);
				int num = Information.UBound((Array)ArrayTops, 1);
				for (int i = 0; i <= num; i++)
				{
					if (CheckNearness(GlobalForm.nHLC[1, iTopStart], GlobalForm.nHLC[1, ArrayTops[i]], -1m, 0.25m))
					{
						flag = false;
						break;
					}
				}
			}
			else
			{
				flag = false;
			}
			if (!flag)
			{
				GlobalForm.ChartStartIndex = (int)Math.Round((double)iBottomStart + (double)(iBottomEnd - iBottomStart) / 6.0);
				GlobalForm.ChartEndIndex = (int)Math.Round((double)iBottomEnd - (double)(iBottomEnd - iBottomStart) / 6.0);
				if (GlobalForm.ChartEndIndex > GlobalForm.ChartStartIndex)
				{
					FindAllBottoms(2);
					int num2 = Information.UBound((Array)ArrayBottoms, 1);
					int i = 0;
					while (true)
					{
						if (i <= num2)
						{
							if (CheckNearness(GlobalForm.nHLC[2, iBottomStart], GlobalForm.nHLC[2, ArrayBottoms[i]], -1m, 0.25m))
							{
								break;
							}
							i++;
							continue;
						}
						flag = true;
						break;
					}
				}
				else
				{
					flag = false;
				}
			}
			GlobalForm.ChartStartIndex = chartStartIndex;
			GlobalForm.ChartEndIndex = chartEndIndex;
			return flag;
		}
	}

	private static int CheckTrend(int iStart, int iEnd, int ShortLong)
	{
		int num = 0;
		checked
		{
			decimal d;
			int num3;
			int num2;
			if (ShortLong == -1)
			{
				num2 = Conversions.ToInteger(Interaction.IIf(iStart - 21 < 0, (object)0, (object)(iStart - 21)));
				d = default(decimal);
				num3 = 0;
				int num4 = num2;
				int num5 = iStart - 1;
				for (int i = num4; i <= num5; i++)
				{
					d = decimal.Add(d, decimal.Divide(decimal.Add(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 2m));
					num3++;
				}
				if (num3 > 0)
				{
					return Conversions.ToInteger(Interaction.IIf(decimal.Compare(decimal.Divide(d, new decimal(num3)), decimal.Divide(decimal.Add(GlobalForm.nHLC[1, iStart], GlobalForm.nHLC[2, iStart]), 2m)) < 0, (object)1, (object)(-1)));
				}
				return 1;
			}
			int num6 = iStart;
			int num7 = iStart;
			for (int i = iStart + 1; i <= iEnd; i++)
			{
				num6 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num6]) > 0, (object)i, (object)num6));
				num7 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num7]) < 0, (object)i, (object)num7));
			}
			decimal d2 = decimal.Divide(decimal.Add(GlobalForm.nHLC[1, num6], GlobalForm.nHLC[2, num7]), 2m);
			num2 = Conversions.ToInteger(Interaction.IIf(iStart - 21 < 0, (object)0, (object)(iStart - 21)));
			d = default(decimal);
			num3 = 0;
			int num8 = num2;
			int num9 = iStart - 1;
			for (int i = num8; i <= num9; i++)
			{
				d = decimal.Add(d, GlobalForm.nHLC[3, i]);
				num3++;
			}
			if (num3 > 0)
			{
				decimal d3 = decimal.Divide(d, new decimal(num3));
				if (decimal.Compare(d3, d2) > 0)
				{
					num--;
				}
				if (decimal.Compare(d3, d2) < 0)
				{
					num++;
				}
			}
			for (int i = iStart - 1; i >= 0; i += -1)
			{
				if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[1, num6]) > 0)
				{
					num--;
					break;
				}
				if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[2, num7]) < 0)
				{
					num++;
					break;
				}
			}
			num2 = Conversions.ToInteger(Interaction.IIf(iStart - 63 < 0, (object)0, (object)(iStart - 63)));
			num = ((decimal.Compare(GlobalForm.nHLC[3, num2], d2) >= 0) ? (num - 1) : (num + 1));
			return Conversions.ToInteger(Interaction.IIf(num >= 0, (object)1, (object)(-1)));
		}
	}

	private static bool ConfirmHSB(int z, decimal ArmPitHigh)
	{
		decimal d = GlobalForm.nHLC[2, ArrayBottoms[z]];
		checked
		{
			int num = ArrayBottoms[z] + 1;
			int hLCRange = GlobalForm.HLCRange;
			for (int i = num; i <= hLCRange && decimal.Compare(GlobalForm.nHLC[3, i], ArmPitHigh) <= 0; i++)
			{
				if (GlobalForm.StrictPatterns)
				{
					if (decimal.Compare(GlobalForm.nHLC[2, i], d) < 0)
					{
						return true;
					}
				}
				else if (decimal.Compare(GlobalForm.nHLC[3, i], d) < 0)
				{
					return true;
				}
			}
			return false;
		}
	}

	private static bool ConfirmHST(int z, decimal ArmPitLow)
	{
		decimal d = GlobalForm.nHLC[1, ArrayTops[z]];
		checked
		{
			int num = ArrayTops[z] + 1;
			int hLCRange = GlobalForm.HLCRange;
			for (int i = num; i <= hLCRange && decimal.Compare(GlobalForm.nHLC[3, i], ArmPitLow) >= 0; i++)
			{
				if (GlobalForm.StrictPatterns)
				{
					if (decimal.Compare(GlobalForm.nHLC[1, i], d) > 0)
					{
						return true;
					}
				}
				else if (decimal.Compare(GlobalForm.nHLC[3, i], d) > 0)
				{
					return true;
				}
			}
			return false;
		}
	}

	private static bool DupCheck(int TLCount, int iStart, int iEnd)
	{
		checked
		{
			for (int i = TLCount - 1; i >= 0; i += -1)
			{
				if ((TLArray[0, i] == iStart) & (TLArray[1, i] == iEnd))
				{
					return true;
				}
			}
			return false;
		}
	}

	public static bool FinalATTests(int LowIndex, int Low2Index, int TopDays, int TopStartNdx, int LastTopTouch, decimal Margin)
	{
		bool result = true;
		decimal priceScale = GetPriceScale(GlobalForm.nHLC[1, ArrayTops[LastTopTouch]], GlobalForm.nHLC[1, ArrayTops[TopStartNdx]]);
		if (decimal.Compare(priceScale, 0m) == 0)
		{
			return result;
		}
		if (CheckSlope(GlobalForm.nHLC[2, LowIndex], GlobalForm.nHLC[2, Low2Index], 0.005m) == 0)
		{
			return result;
		}
		checked
		{
			if ((decimal.Compare(decimal.Add(decimal.Divide(GlobalForm.nHLC[2, LowIndex], priceScale), 0.04m), decimal.Divide(GlobalForm.nHLC[2, Low2Index], priceScale)) > 0) & (Math.Abs(Low2Index - LowIndex) >= TopDays))
			{
				return result;
			}
			int num = TopStartNdx;
			for (int i = TopStartNdx + 1; i <= LastTopTouch; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[i]], GlobalForm.nHLC[1, ArrayTops[num]]) > 0)
				{
					num = i;
				}
			}
			num = ArrayTops[num];
			decimal d = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.075m, (object)0.1m));
			decimal d2 = decimal.Subtract(GlobalForm.nHLC[1, num], decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, LowIndex]), d));
			int num2 = 0;
			for (int i = TopStartNdx; i <= LastTopTouch; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[i]], d2) > 0)
				{
					num2++;
				}
			}
			if (num2 < 3)
			{
				return result;
			}
			int num3 = Convert.ToInt32(decimal.Add(decimal.Multiply(new decimal(ArrayTops[LastTopTouch] - ArrayTops[TopStartNdx]), 0.25m), new decimal(ArrayTops[TopStartNdx])));
			int num4 = Convert.ToInt32(decimal.Add(decimal.Multiply(new decimal(ArrayTops[LastTopTouch] - ArrayTops[TopStartNdx]), 0.5m), new decimal(ArrayTops[TopStartNdx])));
			int num5 = num4;
			for (int i = num3; i <= num5; i++)
			{
				priceScale = GetPriceScale(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, ArrayTops[TopStartNdx]]);
				if (decimal.Compare(priceScale, 0m) == 0)
				{
					return result;
				}
				if (decimal.Compare(decimal.Divide(GlobalForm.nHLC[1, i], priceScale), decimal.Subtract(decimal.Divide(GlobalForm.nHLC[1, ArrayTops[TopStartNdx]], priceScale), Margin)) >= 0)
				{
					result = false;
					break;
				}
			}
			return result;
		}
	}

	private static bool FinalDesTriTests(int HighIndex, int High2Index, int TopDays, int BottomStartNdx, int LastBottomTouch, decimal Margin)
	{
		bool result = true;
		decimal priceScale = GetPriceScale(GlobalForm.nHLC[2, ArrayBottoms[LastBottomTouch]], GlobalForm.nHLC[2, ArrayBottoms[BottomStartNdx]]);
		if (decimal.Compare(priceScale, 0m) == 0)
		{
			return result;
		}
		if (CheckSlope(GlobalForm.nHLC[1, HighIndex], GlobalForm.nHLC[1, High2Index], 0.005m) == 0)
		{
			return result;
		}
		checked
		{
			if ((decimal.Compare(decimal.Subtract(decimal.Divide(GlobalForm.nHLC[1, HighIndex], priceScale), 0.03m), decimal.Divide(GlobalForm.nHLC[1, High2Index], priceScale)) < 0) & (Math.Abs(High2Index - HighIndex) >= TopDays))
			{
				return result;
			}
			int num = BottomStartNdx;
			for (int i = BottomStartNdx + 1; i <= LastBottomTouch; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[i]], GlobalForm.nHLC[2, ArrayBottoms[num]]) < 0)
				{
					num = i;
				}
			}
			num = ArrayBottoms[num];
			decimal d = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.075m, (object)0.1m));
			decimal d2 = decimal.Add(GlobalForm.nHLC[2, num], decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, HighIndex], GlobalForm.nHLC[2, num]), d));
			int num2 = 0;
			for (int i = BottomStartNdx; i <= LastBottomTouch; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[i]], d2) < 0)
				{
					num2++;
				}
			}
			if (num2 < 3)
			{
				return result;
			}
			int num3 = Convert.ToInt32(decimal.Multiply(new decimal(ArrayBottoms[LastBottomTouch] - ArrayBottoms[BottomStartNdx]), 0.25m)) + ArrayBottoms[BottomStartNdx];
			int num4 = Convert.ToInt32(decimal.Multiply(new decimal(ArrayBottoms[LastBottomTouch] - ArrayBottoms[BottomStartNdx]), 0.5m)) + ArrayBottoms[BottomStartNdx];
			int num5 = num4;
			for (int i = num3; i <= num5; i++)
			{
				priceScale = GetPriceScale(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, ArrayBottoms[BottomStartNdx]]);
				if (decimal.Compare(priceScale, 0m) == 0)
				{
					return result;
				}
				if (decimal.Compare(decimal.Divide(GlobalForm.nHLC[2, i], priceScale), decimal.Add(decimal.Divide(GlobalForm.nHLC[2, ArrayBottoms[BottomStartNdx]], priceScale), Margin)) <= 0)
				{
					break;
				}
			}
			return false;
		}
	}

	private static void Find3FallPeaks()
	{
		FindAllTops(Conversions.ToInteger(Interaction.IIf(GlobalForm.StrictPatterns, (object)9.0, (object)6)));
		checked
		{
			int num = Information.UBound((Array)ArrayTops, 1) - 2;
			for (int i = 0; i <= num; i++)
			{
				if (!((decimal.Compare(GlobalForm.nHLC[1, ArrayTops[i]], GlobalForm.nHLC[1, ArrayTops[i + 1]]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[i + 1]], GlobalForm.nHLC[1, ArrayTops[i + 2]]) > 0)) || ArrayTops[i + 2] - ArrayTops[i] > 126)
				{
					continue;
				}
				int num2 = ArrayTops[i + 2];
				int num3 = ArrayTops[i];
				int num4 = ArrayTops[i];
				int chartEndIndex = GlobalForm.ChartEndIndex;
				for (int j = num4; j <= chartEndIndex; j++)
				{
					if (j <= ArrayTops[i + 2])
					{
						num3 = Conversions.ToInteger(Interaction.IIf((decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num3]) < 0) | (decimal.Compare(GlobalForm.nHLC[2, j], 0m) == 0), (object)j, (object)num3));
					}
					if (j <= ArrayTops[i + 2])
					{
						continue;
					}
					if ((j == GlobalForm.ChartEndIndex) | (decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[2, num3]) < 0))
					{
						int num5 = Conversions.ToInteger(Interaction.IIf(j == GlobalForm.ChartEndIndex, (object)0, (object)(-1)));
						AddPattern(ArrayTops[i], ArrayTops[i + 1], ArrayTops[i + 2], 0, 0, 0, 91, Conversions.ToString(Interaction.IIf(num5 == -1, (object)"3FP", (object)"3FP?")));
						if (j != GlobalForm.ChartEndIndex)
						{
							break;
						}
						return;
					}
					if (decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[1, num2]) > 0)
					{
						break;
					}
				}
			}
		}
	}

	private static void Find3RisingValleys()
	{
		FindAllBottoms(Conversions.ToInteger(Interaction.IIf(GlobalForm.StrictPatterns, (object)9.0, (object)6)));
		checked
		{
			int num = Information.UBound((Array)ArrayBottoms, 1) - 2;
			for (int i = 0; i <= num; i++)
			{
				if (!((decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[i]], GlobalForm.nHLC[2, ArrayBottoms[i + 1]]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[i + 1]], GlobalForm.nHLC[2, ArrayBottoms[i + 2]]) < 0)) || ArrayBottoms[i + 2] - ArrayBottoms[i] > 126)
				{
					continue;
				}
				int num2 = ArrayBottoms[i + 2];
				int num3 = ArrayBottoms[i + 2];
				int num4 = ArrayBottoms[i];
				int chartEndIndex = GlobalForm.ChartEndIndex;
				for (int j = num4; j <= chartEndIndex; j++)
				{
					if (j <= ArrayBottoms[i + 2])
					{
						num2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, num2]) > 0, (object)j, (object)num2));
					}
					if (j <= ArrayBottoms[i + 2])
					{
						continue;
					}
					if ((j == GlobalForm.ChartEndIndex) | (decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[1, num2]) > 0))
					{
						int num5 = Conversions.ToInteger(Interaction.IIf(j == GlobalForm.ChartEndIndex, (object)0, (object)1));
						AddPattern(ArrayBottoms[i], ArrayBottoms[i + 1], ArrayBottoms[i + 2], 0, 0, 0, 90, Conversions.ToString(Interaction.IIf(num5 == 1, (object)"3RV", (object)"3RV?")));
						if (j != GlobalForm.ChartEndIndex)
						{
							break;
						}
						return;
					}
					if (decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[2, num3]) < 0)
					{
						break;
					}
				}
			}
		}
	}

	public static void FindAllBottoms(int TradeDays)
	{
		ArrayBottoms = null;
		ArrayBottoms = new int[1];
		int num = TradeDays;
		int num2 = default(int);
		ArrayBottoms[0] = num2;
		int chartStartIndex = GlobalForm.ChartStartIndex;
		int chartEndIndex = GlobalForm.ChartEndIndex;
		checked
		{
			for (num2 = chartStartIndex; num2 <= chartEndIndex; num2++)
			{
				if (decimal.Compare(GlobalForm.nHLC[2, num2], GlobalForm.nHLC[2, ArrayBottoms[Information.UBound((Array)ArrayBottoms, 1)]]) <= 0)
				{
					ArrayBottoms[Information.UBound((Array)ArrayBottoms, 1)] = num2;
					num = TradeDays - 1;
					continue;
				}
				num--;
				while (num < 0)
				{
					num = TradeDays;
					if (ArrayBottoms[Information.UBound((Array)ArrayBottoms, 1)] - TradeDays >= 0)
					{
						int num3 = ArrayBottoms[Information.UBound((Array)ArrayBottoms, 1)] - TradeDays;
						int num4 = ArrayBottoms[Information.UBound((Array)ArrayBottoms, 1)] - 1;
						int num5 = num3;
						while (num5 <= num4)
						{
							if (decimal.Compare(GlobalForm.nHLC[2, num5], GlobalForm.nHLC[2, ArrayBottoms[Information.UBound((Array)ArrayBottoms, 1)]]) >= 0)
							{
								num5++;
								continue;
							}
							goto IL_00fb;
						}
						goto IL_0156;
					}
					ArrayBottoms[Information.UBound((Array)ArrayBottoms, 1)] = num2;
					break;
					IL_0156:
					if (GlobalForm.ChartEndIndex - num2 > TradeDays)
					{
						ArrayBottoms = (int[])Utils.CopyArray((Array)ArrayBottoms, (Array)new int[Information.UBound((Array)ArrayBottoms, 1) + 1 + 1]);
						ArrayBottoms[Information.UBound((Array)ArrayBottoms, 1)] = num2;
						break;
					}
					return;
					IL_00fb:
					if (Information.UBound((Array)ArrayBottoms, 1) > 0)
					{
						ArrayBottoms = (int[])Utils.CopyArray((Array)ArrayBottoms, (Array)new int[Information.UBound((Array)ArrayBottoms, 1) - 1 + 1]);
						goto IL_0156;
					}
					ArrayBottoms[Information.UBound((Array)ArrayBottoms, 1)] = num2;
				}
			}
		}
	}

	private static void FindAllGaps()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 3;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			int PostTrend = default(int);
			for (int i = num; i <= chartEndIndex; i++)
			{
				int num2 = 0;
				if (decimal.Compare(decimal.Add(GlobalForm.nHLC[1, i - 1], GlobalForm.GapSize), GlobalForm.nHLC[2, i]) <= 0)
				{
					num2 = 1;
				}
				else if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[2, i - 1], GlobalForm.GapSize), GlobalForm.nHLC[1, i]) >= 0)
				{
					num2 = -1;
				}
				if (num2 != 0)
				{
					int closeTime = GapClosesIn(i, num2);
					int trend = GetTrend(i - 1, ref PostTrend);
					int patternCount = GlobalForm.PatternCount;
					if (GlobalForm.PatternList[118] == 1)
					{
						CheckArea(closeTime, i, num2, trend, PostTrend);
					}
					if (GlobalForm.PatternList[117] == 1)
					{
						CheckBreakaway(closeTime, i, trend, PostTrend);
					}
					if (GlobalForm.PatternList[119] == 1)
					{
						CheckContinuation(i, num2, trend, PostTrend);
					}
					if (GlobalForm.PatternList[121] == 1)
					{
						CheckExhaustion(i, num2, trend, PostTrend);
					}
					if (((GlobalForm.PatternList[117] == 1) & (GlobalForm.PatternList[118] == 1) & (GlobalForm.PatternList[119] == 1) & (GlobalForm.PatternList[121] == 1) & (GlobalForm.PatternList[120] == 1)) && ((patternCount == GlobalForm.PatternCount) & (GlobalForm.PatternList[120] == 1)))
					{
						AddPattern(i - 1, 0, i, 0, 0, 0, 120, "G?");
					}
				}
			}
		}
	}

	private static void CheckArea(int CloseTime, int i, int GapDirection, int Trend, int PostTrend)
	{
		if ((CloseTime < 0 && CloseTime > -7) || (CloseTime > 0 && CloseTime <= 7))
		{
			checked
			{
				if ((GapDirection == 1) & !((decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i - 2]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, i - 2], GlobalForm.nHLC[1, i - 3]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i - 2]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 2], GlobalForm.nHLC[2, i - 3]) > 0)))
				{
					AddPattern(i - 1, 0, i, 0, 0, 0, 118, "Ga");
				}
				else if ((GapDirection == -1) & !((decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i - 2]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, i - 2], GlobalForm.nHLC[1, i - 3]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i - 2]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 2], GlobalForm.nHLC[2, i - 3]) < 0)))
				{
					AddPattern(i - 1, 0, i, 0, 0, 0, 118, "Ga");
				}
				else if (unchecked(Trend == 0 && PostTrend == 0))
				{
					AddPattern(i - 1, 0, i, 0, 0, 0, 118, "Ga?");
				}
			}
		}
		else if (Trend == 0 && PostTrend == 0 && ((CloseTime != 0) & (Math.Abs(CloseTime) <= 7)))
		{
			AddPattern(checked(i - 1), 0, i, 0, 0, 0, 118, "Ga");
		}
	}

	private static void CheckBreakaway(int CloseTime, int i, int Trend, int PostTrend)
	{
		if (Trend == 0 && PostTrend != 0 && ((CloseTime == 0) | (Math.Abs(CloseTime) >= 14)))
		{
			AddPattern(checked(i - 1), 0, i, 0, 0, 0, 117, "Gb");
		}
	}

	private static void CheckContinuation(int i, int GapDirection, int Trend, int PostTrend)
	{
		checked
		{
			if (unchecked(GapDirection == 1 && Trend == 1 && PostTrend == 1) & (decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i - 2]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i]) < 0))
			{
				AddPattern(i - 1, 0, i, 0, 0, 0, 119, "Gc");
			}
			else if (unchecked(GapDirection == -1 && Trend == -1 && PostTrend == -1) & (decimal.Compare(GlobalForm.nHLC[1, i - 2], GlobalForm.nHLC[1, i - 1]) > 0))
			{
				AddPattern(i - 1, 0, i, 0, 0, 0, 119, "Gc");
			}
		}
	}

	private static void CheckExhaustion(int i, int GapDirection, int Trend, int PostTrend)
	{
		checked
		{
			if (unchecked(GapDirection == 1 && Trend == 1 && PostTrend != 1) & (decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i - 2]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i]) < 0))
			{
				AddPattern(i - 1, 0, i, 0, 0, 0, 121, "Ge");
			}
			else if (unchecked(GapDirection == -1 && Trend == -1 && PostTrend != -1) & (decimal.Compare(GlobalForm.nHLC[1, i - 2], GlobalForm.nHLC[1, i - 1]) > 0))
			{
				AddPattern(i - 1, 0, i, 0, 0, 0, 121, "Ge");
			}
			else
			{
				if (!unchecked(Trend == 0 && PostTrend == 0))
				{
					return;
				}
				if (GapDirection == 1)
				{
					if (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[1, i - 2]) > 0)
					{
						AddPattern(i - 1, 0, i, 0, 0, 0, 121, "Ge");
					}
				}
				else if (decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[2, i - 2]) < 0)
				{
					AddPattern(i - 1, 0, i, 0, 0, 0, 121, "Ge");
				}
			}
		}
	}

	private static int GapClosesIn(int i, int Type)
	{
		checked
		{
			int num = Conversions.ToInteger(Interaction.IIf(GlobalForm.HLCRange - i > 22, (object)22, (object)(GlobalForm.HLCRange - i)));
			int num2 = i + 1;
			int num3 = i + num;
			for (int j = num2; j <= num3; j++)
			{
				if (Type == 1)
				{
					if (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[1, i - 1]) <= 0)
					{
						return j - i;
					}
				}
				else if (decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[2, i - 1]) >= 0)
				{
					return j - i;
				}
			}
			if (num == 22)
			{
				return 0;
			}
			return -num;
		}
	}

	private static int GetTrend(int i, ref int PostTrend)
	{
		checked
		{
			int result = (((decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i - 1]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i - 2]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i - 1]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i - 2]) > 0)) ? 1 : (((decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i - 1]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i - 2]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i - 1]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i - 2]) < 0)) ? (-1) : 0));
			if (i + 3 <= GlobalForm.HLCRange)
			{
				if ((decimal.Compare(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[1, i + 2]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, i + 2], GlobalForm.nHLC[1, i + 3]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i + 1], GlobalForm.nHLC[2, i + 2]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i + 2], GlobalForm.nHLC[2, i + 3]) > 0))
				{
					PostTrend = -1;
				}
				else if ((decimal.Compare(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[1, i + 2]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, i + 2], GlobalForm.nHLC[1, i + 3]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i + 1], GlobalForm.nHLC[2, i + 2]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i + 2], GlobalForm.nHLC[2, i + 3]) < 0))
				{
					PostTrend = 1;
				}
				else
				{
					PostTrend = 0;
				}
			}
			else
			{
				PostTrend = 2;
			}
			return result;
		}
	}

	public static void FindABCD(int Flag)
	{
		double[] array = new double[6] { 0.382, 0.5, 0.618, 0.707, 0.786, 0.886 };
		double num = Conversions.ToDouble(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.005, (object)0.01));
		FindAllTops(5);
		int num2 = Information.UBound((Array)ArrayTops, 1);
		if (Information.UBound((Array)ArrayTops, 1) < 2)
		{
			return;
		}
		FindAllBottoms(5);
		int num3 = Information.UBound((Array)ArrayBottoms, 1);
		if (num3 < 2)
		{
			return;
		}
		checked
		{
			switch (Flag)
			{
			case 4:
			{
				int num20 = num3 - 1;
				for (int i = 0; i <= num20; i++)
				{
					int num5 = ArrayBottoms[i];
					int num21 = i + 1;
					int num22 = num3;
					for (int j = num21; j <= num22; j++)
					{
						int num8 = ArrayBottoms[j];
						if (decimal.Compare(GlobalForm.nHLC[2, num5], GlobalForm.nHLC[2, num8]) >= 0 || num8 - num5 > 126)
						{
							break;
						}
						int num23 = num2;
						int num10;
						decimal num15;
						int l;
						for (int k = 0; k <= num23; k++)
						{
							num10 = ArrayTops[k];
							if (!unchecked(num10 > num5 && num10 < num8))
							{
								continue;
							}
							if (decimal.Compare(GlobalForm.nHLC[1, num10], GlobalForm.nHLC[2, num8]) <= 0)
							{
								break;
							}
							int num24 = num5 + 1;
							int num25 = num10 - 1;
							for (l = num24; l <= num25; l++)
							{
								if (decimal.Compare(GlobalForm.nHLC[1, l], GlobalForm.nHLC[1, num10]) >= 0 || decimal.Compare(GlobalForm.nHLC[2, l], GlobalForm.nHLC[2, num5]) <= 0)
								{
									goto end_IL_03fe;
								}
							}
							int num26 = num10 + 1;
							int num27 = num8 - 1;
							l = num26;
							while (l <= num27)
							{
								if (decimal.Compare(GlobalForm.nHLC[1, l], GlobalForm.nHLC[1, num10]) < 0)
								{
									if (decimal.Compare(GlobalForm.nHLC[2, l], GlobalForm.nHLC[2, num8]) <= 0)
									{
										goto end_IL_03f0;
									}
									l++;
									continue;
								}
								goto IL_03ec;
							}
							if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num10], GlobalForm.nHLC[2, num5]), 0m) == 0)
							{
								continue;
							}
							num15 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num10], GlobalForm.nHLC[2, num8]), decimal.Subtract(GlobalForm.nHLC[1, num10], GlobalForm.nHLC[2, num5]));
							int num28 = array.Count() - 1;
							int num17 = 0;
							while (num17 <= num28)
							{
								if (!((Convert.ToDouble(num15) >= array[num17] - num) & (Convert.ToDouble(num15) <= array[num17] + num) & (decimal.Compare(num15, 0m) != 0)))
								{
									num17++;
									continue;
								}
								goto IL_02b7;
							}
							continue;
							end_IL_03f0:
							break;
							IL_03ec:;
						}
						continue;
						IL_02b7:
						HarmonicTarget = Convert.ToDouble(decimal.Add(GlobalForm.nHLC[2, num8], decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num10], GlobalForm.nHLC[2, num8]), num15)));
						int num18 = num8 + 1;
						if (num18 > GlobalForm.HLCRange)
						{
							break;
						}
						int num29 = num8 + 2;
						int hLCRange2 = GlobalForm.HLCRange;
						l = num29;
						while (true)
						{
							if (l <= hLCRange2 && l - num5 <= 126)
							{
								num18 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, l], GlobalForm.nHLC[1, num18]) > 0, (object)l, (object)num18));
								if (Convert.ToDouble(GlobalForm.nHLC[1, l]) >= HarmonicTarget)
								{
									AddPattern(num5, num10, l, num8, 0, 0, 4, "ABCD Be");
									break;
								}
								if (decimal.Compare(GlobalForm.nHLC[2, l], GlobalForm.nHLC[2, num8]) >= 0)
								{
									l++;
									continue;
								}
							}
							AddPattern(num5, num10, num18, num8, 0, 0, 4, "ABCD Be?");
							break;
						}
						break;
						continue;
						end_IL_03fe:
						break;
					}
				}
				break;
			}
			case 5:
			{
				int num4 = num2 - 1;
				for (int i = 0; i <= num4; i++)
				{
					int num5 = ArrayTops[i];
					int num6 = i + 1;
					int num7 = num2;
					for (int j = num6; j <= num7; j++)
					{
						int num8 = ArrayTops[j];
						if (decimal.Compare(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[1, num8]) <= 0 || num8 - num5 > 126)
						{
							break;
						}
						int num9 = num3;
						int num10;
						decimal num15;
						int l;
						for (int k = 0; k <= num9; k++)
						{
							num10 = ArrayBottoms[k];
							if (!unchecked(num10 > num5 && num10 < num8))
							{
								continue;
							}
							if (decimal.Compare(GlobalForm.nHLC[2, num10], GlobalForm.nHLC[1, num8]) >= 0)
							{
								break;
							}
							int num11 = num5 + 1;
							int num12 = num10 - 1;
							for (l = num11; l <= num12; l++)
							{
								if (decimal.Compare(GlobalForm.nHLC[2, l], GlobalForm.nHLC[2, num10]) <= 0 || decimal.Compare(GlobalForm.nHLC[1, l], GlobalForm.nHLC[1, num5]) >= 0)
								{
									goto end_IL_0794;
								}
							}
							int num13 = num10 + 1;
							int num14 = num8 - 1;
							l = num13;
							while (l <= num14)
							{
								if (decimal.Compare(GlobalForm.nHLC[2, l], GlobalForm.nHLC[2, num10]) > 0)
								{
									if (decimal.Compare(GlobalForm.nHLC[1, l], GlobalForm.nHLC[1, num8]) >= 0)
									{
										goto end_IL_0786;
									}
									l++;
									continue;
								}
								goto IL_0782;
							}
							if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[2, num10]), 0m) == 0)
							{
								continue;
							}
							num15 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num8], GlobalForm.nHLC[2, num10]), decimal.Subtract(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[2, num10]));
							int num16 = array.Count() - 1;
							int num17 = 0;
							while (num17 <= num16)
							{
								if (!((Convert.ToDouble(num15) >= array[num17] - num) & (Convert.ToDouble(num15) <= array[num17] + num) & (decimal.Compare(num15, 0m) != 0)))
								{
									num17++;
									continue;
								}
								goto IL_064d;
							}
							continue;
							end_IL_0786:
							break;
							IL_0782:;
						}
						continue;
						IL_064d:
						HarmonicTarget = Convert.ToDouble(decimal.Subtract(GlobalForm.nHLC[1, num8], decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num8], GlobalForm.nHLC[2, num10]), num15)));
						int num18 = num8 + 1;
						if (num18 > GlobalForm.HLCRange)
						{
							break;
						}
						int num19 = num8 + 2;
						int hLCRange = GlobalForm.HLCRange;
						l = num19;
						while (true)
						{
							if (l <= hLCRange)
							{
								if (l - num5 > 126)
								{
									break;
								}
								num18 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, l], GlobalForm.nHLC[2, num18]) < 0, (object)l, (object)num18));
								if (Convert.ToDouble(GlobalForm.nHLC[2, l]) <= HarmonicTarget)
								{
									AddPattern(num5, num10, num18, num8, 0, 0, 5, "ABCD Bu");
									break;
								}
								if (decimal.Compare(GlobalForm.nHLC[1, l], GlobalForm.nHLC[1, num8]) <= 0)
								{
									l++;
									continue;
								}
							}
							AddPattern(num5, num10, num18, num8, 0, 0, 5, "ABCD Bu?");
							break;
						}
						break;
						continue;
						end_IL_0794:
						break;
					}
				}
				break;
			}
			}
		}
	}

	public static void FindAllTops(int TradeDays)
	{
		ArrayTops = null;
		ArrayTops = new int[1];
		int num = TradeDays;
		ArrayTops[0] = GlobalForm.ChartStartIndex;
		int chartStartIndex = GlobalForm.ChartStartIndex;
		int chartEndIndex = GlobalForm.ChartEndIndex;
		checked
		{
			for (int i = chartStartIndex; i <= chartEndIndex; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, ArrayTops[Information.UBound((Array)ArrayTops, 1)]]) >= 0)
				{
					ArrayTops[Information.UBound((Array)ArrayTops, 1)] = i;
					num = TradeDays - 1;
					continue;
				}
				num--;
				while (num < 0)
				{
					num = TradeDays;
					if (ArrayTops[Information.UBound((Array)ArrayTops, 1)] - TradeDays >= 0)
					{
						int num2 = ArrayTops[Information.UBound((Array)ArrayTops, 1)] - TradeDays;
						int num3 = ArrayTops[Information.UBound((Array)ArrayTops, 1)] - 1;
						int num4 = num2;
						while (num4 <= num3)
						{
							if (decimal.Compare(GlobalForm.nHLC[1, num4], GlobalForm.nHLC[1, ArrayTops[Information.UBound((Array)ArrayTops, 1)]]) <= 0)
							{
								num4++;
								continue;
							}
							goto IL_00ff;
						}
						goto IL_015a;
					}
					ArrayTops[Information.UBound((Array)ArrayTops, 1)] = i;
					break;
					IL_015a:
					if (GlobalForm.ChartEndIndex - i > TradeDays)
					{
						ArrayTops = (int[])Utils.CopyArray((Array)ArrayTops, (Array)new int[Information.UBound((Array)ArrayTops, 1) + 1 + 1]);
						ArrayTops[Information.UBound((Array)ArrayTops, 1)] = i;
						break;
					}
					return;
					IL_00ff:
					if (Information.UBound((Array)ArrayTops, 1) > 0)
					{
						ArrayTops = (int[])Utils.CopyArray((Array)ArrayTops, (Array)new int[Information.UBound((Array)ArrayTops, 1) - 1 + 1]);
						goto IL_015a;
					}
					ArrayTops[Information.UBound((Array)ArrayTops, 1)] = i;
				}
			}
		}
	}

	private static void FindAscendingTriangle()
	{
		decimal d = default(decimal);
		int num = 0;
		int num2 = 0;
		FindAllTops(3);
		int num3 = Information.UBound((Array)ArrayTops, 1);
		if (num3 < 3)
		{
			return;
		}
		FindAllBottoms(2);
		if (Information.UBound((Array)ArrayBottoms, 1) < 2)
		{
			return;
		}
		checked
		{
			int num4 = num3 - 1;
			int num9 = default(int);
			for (int i = 0; i <= num4; i++)
			{
				int num5 = 1;
				int num6 = i + 1;
				int num7 = num3;
				int num8 = num6;
				while (num8 <= num7 && ArrayTops[num8] - ArrayTops[i] <= 126)
				{
					bool flag = false;
					bool flag2 = false;
					if (GlobalForm.StrictPatterns && !CheckNearness(GlobalForm.nHLC[1, ArrayTops[num8]], GlobalForm.nHLC[1, ArrayTops[i]], -1m, 0.16m))
					{
						flag2 = true;
					}
					if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[num8]], decimal.Add(GlobalForm.nHLC[1, ArrayTops[i]], 0.16m)) > 0)
					{
						flag2 = true;
					}
					if (flag2)
					{
						if ((num5 < 3) | (Math.Abs(i - num8) < 3))
						{
							break;
						}
						if ((decimal.Compare(d, 0m) != 0) | !CheckNearness(GlobalForm.nHLC[1, ArrayTops[num]], GlobalForm.nHLC[1, ArrayTops[num2]], -1m, 0.1m))
						{
							flag = true;
						}
						if (flag)
						{
							break;
						}
						if (CheckNearness(GlobalForm.nHLC[1, ArrayTops[num8]], GlobalForm.nHLC[1, ArrayTops[i]], -1m, 0.16m))
						{
							num2 = num8;
						}
						goto IL_01b5;
					}
					if (CheckNearness(GlobalForm.nHLC[1, ArrayTops[num8]], GlobalForm.nHLC[1, ArrayTops[i]], -1m, 0.16m))
					{
						if (num5 == 1)
						{
							num = i;
							d = GlobalForm.nHLC[1, ArrayTops[i]];
						}
						if (decimal.Compare(d, GlobalForm.nHLC[1, ArrayTops[num8]]) <= 0)
						{
							d = default(decimal);
						}
						else if (decimal.Compare(d, 0m) != 0)
						{
							d = GlobalForm.nHLC[1, ArrayTops[num8]];
						}
						num5++;
						if (num5 == 3)
						{
							num9 = ArrayTops[num];
							int num10 = ArrayTops[num];
							int num11 = ArrayTops[num8];
							for (int j = num10; j <= num11; j++)
							{
								if (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num9]) < 0)
								{
									num9 = j;
								}
							}
							if (num8 == num3)
							{
								num2 = num8;
								goto IL_01b5;
							}
						}
						else if (num5 > 3)
						{
							int num12 = ArrayTops[num8 - 1];
							int num13 = ArrayTops[num8];
							int j = num12;
							while (j <= num13)
							{
								if (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num9]) > 0)
								{
									j++;
									continue;
								}
								goto IL_01b5;
							}
						}
						num2 = num8;
					}
					else if (num5 >= 3)
					{
						int num14 = ArrayTops[num8 - 1];
						int num15 = ArrayTops[num8];
						int j = num14;
						while (j <= num15)
						{
							if (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num9]) > 0)
							{
								j++;
								continue;
							}
							goto IL_01b5;
						}
						if (decimal.Compare(d, GlobalForm.nHLC[1, ArrayTops[num8]]) <= 0)
						{
							d = default(decimal);
						}
						else if (decimal.Compare(d, 0m) != 0)
						{
							d = GlobalForm.nHLC[1, ArrayTops[num8]];
						}
					}
					num8++;
					continue;
					IL_01b5:
					num9 = 0;
					int num16 = 0;
					decimal d2 = new decimal((double)(ArrayTops[num] + ArrayTops[num2]) / 2.0);
					int num17 = Information.UBound((Array)ArrayBottoms, 1);
					for (int j = 0; j <= num17; j++)
					{
						if ((ArrayBottoms[j] >= ArrayTops[num]) & (ArrayBottoms[j] <= ArrayTops[num2]))
						{
							if ((num9 == 0) | (decimal.Compare(GlobalForm.nHLC[2, num9], GlobalForm.nHLC[2, ArrayBottoms[j]]) >= 0))
							{
								num9 = ArrayBottoms[j];
							}
							if (decimal.Compare(new decimal(ArrayBottoms[j]), d2) > 0 && ((num16 == 0) | (decimal.Compare(GlobalForm.nHLC[2, num16], GlobalForm.nHLC[2, ArrayBottoms[j]]) >= 0)))
							{
								num16 = ArrayBottoms[j];
							}
						}
						else if (ArrayBottoms[j] > ArrayTops[num2])
						{
							break;
						}
					}
					if (unchecked(num9 == 0 || num16 == 0))
					{
						flag = true;
					}
					if (!flag)
					{
						int num18 = Convert.ToInt32(decimal.Add(new decimal(ArrayTops[num]), decimal.Multiply(new decimal(ArrayTops[num2] - ArrayTops[num]), 0.3m)));
						if (((num9 <= num18) | (Math.Abs(num18 - num9) < 2)) && !FinalATTests(num9, num16, 3, num, num2, 0.16m) && !TriangleWhiteSpaceCheck(ArrayTops[num], ArrayTops[num2], num9, num16, 89))
						{
							AddPattern(ArrayTops[num], 0, ArrayTops[num2], num9, 0, num16, 89, "AscT");
							i = num8;
						}
					}
					break;
				}
			}
		}
	}

	private static void FindBARRB()
	{
		if (TrendLines(1, -1, 126, 0.25m, 3, Special: false) <= 0)
		{
			return;
		}
		int num = Information.UBound((Array)TLArray, 2);
		checked
		{
			int num14 = default(int);
			for (int i = 0; i <= num; i++)
			{
				if (TLArray[1, i] - TLArray[0, i] <= 22)
				{
					continue;
				}
				int num2 = TLArray[0, i];
				int num3 = TLArray[1, i];
				int num4 = Conversions.ToInteger(Interaction.IIf(num2 + 262 > GlobalForm.HLCRange, (object)GlobalForm.HLCRange, (object)(num2 + 262)));
				int num5 = num3 + 1;
				int num6 = num4;
				int j;
				for (j = num5; j <= num6; j++)
				{
					decimal d = decimal.Add(decimal.Multiply(TLSlopeArray[i], new decimal(j - num2)), GlobalForm.nHLC[1, num2]);
					if (decimal.Compare(GlobalForm.nHLC[3, j], d) > 0)
					{
						num3 = j - 1;
						break;
					}
				}
				if (!((j < num4) & (num3 - num2 > 0)))
				{
					continue;
				}
				decimal d2 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num3], GlobalForm.nHLC[1, num2]), new decimal(num3 - num2));
				decimal d3 = new decimal(0.01 * Convert.ToDouble(decimal.Subtract(GlobalForm.nHLC[1, num2], GlobalForm.nHLC[1, num3])));
				int num7 = num3;
				j = num2;
				while (true)
				{
					if (j <= num7)
					{
						decimal d = decimal.Add(decimal.Multiply(d2, new decimal(j - num2)), GlobalForm.nHLC[1, num2]);
						if (decimal.Compare(GlobalForm.nHLC[3, j], decimal.Subtract(d, d3)) > 0)
						{
							break;
						}
						j++;
						continue;
					}
					int num8 = (int)Math.Round((double)num2 + (double)(num3 - num2) / 4.0);
					decimal num9 = default(decimal);
					int num10 = num8;
					for (j = num2; j <= num10; j++)
					{
						decimal d = decimal.Add(decimal.Multiply(TLSlopeArray[i], new decimal(j - num2)), GlobalForm.nHLC[1, num2]);
						if (decimal.Compare(decimal.Subtract(d, GlobalForm.nHLC[2, j]), num9) > 0)
						{
							num9 = decimal.Subtract(d, GlobalForm.nHLC[2, j]);
						}
					}
					if (decimal.Compare(num9, 1m) < 0)
					{
						break;
					}
					decimal num11 = default(decimal);
					int num12 = num8 + 1;
					int num13 = num3;
					for (j = num12; j <= num13; j++)
					{
						decimal d = decimal.Add(decimal.Multiply(TLSlopeArray[i], new decimal(j - num2)), GlobalForm.nHLC[1, num2]);
						if (decimal.Compare(decimal.Subtract(d, GlobalForm.nHLC[2, j]), num11) > 0)
						{
							num11 = decimal.Subtract(d, GlobalForm.nHLC[2, j]);
							num14 = j;
						}
					}
					if (((decimal.Compare(num11, decimal.Multiply(2m, num9)) > 0) & ((double)num14 >= (double)num2 + (double)((num3 - num2) * 2) / 3.0)) && CheckSlope(GlobalForm.nHLC[1, num2], GlobalForm.nHLC[1, num3], 0.05m) == -1)
					{
						int patternCount = GlobalForm.PatternCount;
						AddPattern(num2, num8, num3, 0, 0, 0, 84, "BARRB");
						if (patternCount != GlobalForm.PatternCount)
						{
							GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].dChannelHeight = num9;
						}
					}
					break;
				}
			}
		}
	}

	private static void FindBARRT()
	{
		if (TrendLines(-1, 1, 126, 0.25m, 3, Special: false) <= 0)
		{
			return;
		}
		int num = Information.UBound((Array)TLArray, 2);
		checked
		{
			int num14 = default(int);
			for (int i = 0; i <= num; i++)
			{
				if (TLArray[1, i] - TLArray[0, i] <= 22)
				{
					continue;
				}
				int num2 = TLArray[0, i];
				int num3 = TLArray[1, i];
				int num4 = Conversions.ToInteger(Interaction.IIf(num2 + 262 > GlobalForm.HLCRange, (object)GlobalForm.HLCRange, (object)(num2 + 262)));
				int num5 = num3 + 1;
				int num6 = num4;
				int j;
				for (j = num5; j <= num6; j++)
				{
					decimal d = decimal.Add(decimal.Multiply(TLSlopeArray[i], new decimal(j - num2)), GlobalForm.nHLC[2, num2]);
					if (decimal.Compare(GlobalForm.nHLC[3, j], d) < 0)
					{
						num3 = j - 1;
						break;
					}
				}
				if (!((j < num4) & (num3 - num2 > 0)))
				{
					continue;
				}
				decimal d2 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, num3], GlobalForm.nHLC[2, num2]), new decimal(num3 - num2));
				decimal d3 = new decimal(0.01 * Convert.ToDouble(decimal.Subtract(GlobalForm.nHLC[2, num3], GlobalForm.nHLC[2, num2])));
				int num7 = num3;
				j = num2;
				while (true)
				{
					if (j <= num7)
					{
						decimal d = decimal.Add(decimal.Multiply(d2, new decimal(j - num2)), GlobalForm.nHLC[2, num2]);
						if (decimal.Compare(GlobalForm.nHLC[3, j], decimal.Subtract(d, d3)) < 0)
						{
							break;
						}
						j++;
						continue;
					}
					int num8 = (int)Math.Round((double)num2 + (double)(num3 - num2) / 4.0);
					decimal num9 = default(decimal);
					int num10 = num8;
					for (j = num2; j <= num10; j++)
					{
						decimal d = decimal.Add(decimal.Multiply(TLSlopeArray[i], new decimal(j - num2)), GlobalForm.nHLC[2, num2]);
						if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, j], d), num9) > 0)
						{
							num9 = decimal.Subtract(GlobalForm.nHLC[1, j], d);
						}
					}
					if (decimal.Compare(num9, 1m) < 0)
					{
						break;
					}
					decimal num11 = default(decimal);
					int num12 = num8 + 1;
					int num13 = num3;
					for (j = num12; j <= num13; j++)
					{
						decimal d = decimal.Add(decimal.Multiply(TLSlopeArray[i], new decimal(j - num2)), GlobalForm.nHLC[2, num2]);
						if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[2, j], d), num11) > 0)
						{
							num11 = decimal.Subtract(GlobalForm.nHLC[2, j], d);
							num14 = j;
						}
					}
					if (((decimal.Compare(num11, decimal.Multiply(2m, num9)) > 0) & ((double)num14 >= (double)num2 + (double)((num3 - num2) * 2) / 3.0)) && CheckSlope(GlobalForm.nHLC[2, num2], GlobalForm.nHLC[2, num3], 0.05m) == 1)
					{
						int patternCount = GlobalForm.PatternCount;
						AddPattern(num2, num8, num3, 0, 0, 0, 83, "BARRT");
						if (patternCount != GlobalForm.PatternCount)
						{
							GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].dChannelHeight = num9;
						}
					}
					break;
				}
			}
		}
	}

	private static void FindBat(int Flag)
	{
		double[] array = new double[2] { 0.382, 0.5 };
		double[] array2 = new double[6] { 0.382, 0.5, 0.618, 0.707, 0.786, 0.886 };
		double[] array3 = new double[4] { 1.618, 2.0, 2.24, 2.618 };
		double num = Conversions.ToDouble(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.01, (object)0.03));
		FindAllTops(3);
		int num2 = Information.UBound((Array)ArrayTops, 1);
		if (Information.UBound((Array)ArrayTops, 1) < 3)
		{
			return;
		}
		FindAllBottoms(3);
		int num3 = Information.UBound((Array)ArrayBottoms, 1);
		if (num3 < 3)
		{
			return;
		}
		checked
		{
			switch (Flag)
			{
			case 11:
			{
				int num20 = num2;
				for (int i = 0; i <= num20; i++)
				{
					int num5 = ArrayTops[i];
					int num21 = i + 1;
					int num22 = num2;
					for (int j = num21; j <= num22; j++)
					{
						int num8 = ArrayTops[j];
						if (decimal.Compare(GlobalForm.nHLC[1, num8], GlobalForm.nHLC[1, num5]) >= 0)
						{
							continue;
						}
						int num23 = j + 1;
						int num24 = num2;
						for (int k = num23; k <= num24; k++)
						{
							int num11 = ArrayTops[k];
							if (num11 - num5 > 126)
							{
								goto end_IL_0374;
							}
							int num25 = num3;
							for (int l = 0; l <= num25; l++)
							{
								int num13 = ArrayBottoms[l];
								if (num13 <= num5)
								{
									continue;
								}
								if (num13 >= num8)
								{
									goto end_IL_0374;
								}
								int num26 = l + 1;
								int num27 = num3;
								int num16;
								for (int m = num26; m <= num27; m++)
								{
									num16 = ArrayBottoms[m];
									if (num16 >= num11)
									{
										goto end_IL_035a;
									}
									if (num16 <= num8)
									{
										continue;
									}
									int num28 = array2.Count() - 1;
									for (int n = 0; n <= num28; n++)
									{
										if (CheckFibRetrace(num13, num8, num16, array2[n]) || !(!CheckFibRetrace(num5, num13, num8, array[0]) | !CheckFibRetrace(num5, num13, num8, array[1])) || decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[2, num13]), 0m) == 0)
										{
											continue;
										}
										decimal value = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num11], GlobalForm.nHLC[2, num13]), decimal.Subtract(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[2, num13]));
										if (!((Convert.ToDouble(value) >= 0.886 - num) & (Convert.ToDouble(value) <= 0.886 + num)) || CheckBat(num5, num13, num8, num16, num11, 11))
										{
											continue;
										}
										int num29 = array3.Count() - 1;
										int num19 = 0;
										while (num19 <= num29)
										{
											if (CheckFibExtension(num8, num16, num11, array3[num19]))
											{
												num19++;
												continue;
											}
											goto IL_02af;
										}
									}
								}
								continue;
								IL_02af:
								if ((decimal.Compare(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[1, num11]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, num13], GlobalForm.nHLC[2, num16]) < 0))
								{
									HarmonicTarget = Convert.ToDouble(GlobalForm.nHLC[2, num16]);
									AddPattern(num5, num13, num11, num8, num16, 0, 11, "Bat Be");
								}
								i = k;
								goto end_IL_0374;
								continue;
								end_IL_035a:
								break;
							}
						}
						continue;
						end_IL_0374:
						break;
					}
				}
				break;
			}
			case 10:
			{
				int num4 = num3;
				for (int i = 0; i <= num4; i++)
				{
					int num5 = ArrayBottoms[i];
					int num6 = i + 1;
					int num7 = num3;
					for (int j = num6; j <= num7; j++)
					{
						int num8 = ArrayBottoms[j];
						if (decimal.Compare(GlobalForm.nHLC[2, num8], GlobalForm.nHLC[2, num5]) <= 0)
						{
							continue;
						}
						int num9 = j + 1;
						int num10 = num3;
						for (int k = num9; k <= num10; k++)
						{
							int num11 = ArrayBottoms[k];
							if (num11 - num5 > 126)
							{
								goto end_IL_0652;
							}
							int num12 = num2;
							for (int l = 0; l <= num12; l++)
							{
								int num13 = ArrayTops[l];
								if (num13 <= num5)
								{
									continue;
								}
								if (num13 >= num8)
								{
									goto end_IL_0652;
								}
								int num14 = l + 1;
								int num15 = num2;
								int num16;
								for (int m = num14; m <= num15; m++)
								{
									num16 = ArrayTops[m];
									if (num16 >= num11)
									{
										goto end_IL_0638;
									}
									if (num16 <= num8)
									{
										continue;
									}
									int num17 = array2.Count() - 1;
									for (int n = 0; n <= num17; n++)
									{
										if (CheckFibRetrace(num13, num8, num16, array2[n]) || !(!CheckFibRetrace(num5, num13, num8, array[0]) | !CheckFibRetrace(num5, num13, num8, array[1])) || decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num13], GlobalForm.nHLC[2, num5]), 0m) == 0)
										{
											continue;
										}
										decimal value = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num13], GlobalForm.nHLC[2, num11]), decimal.Subtract(GlobalForm.nHLC[1, num13], GlobalForm.nHLC[2, num5]));
										if (!((Convert.ToDouble(value) >= 0.886 - num) & (Convert.ToDouble(value) <= 0.886 + num)) || CheckBat(num5, num13, num8, num16, num11, 10))
										{
											continue;
										}
										int num18 = array3.Count() - 1;
										int num19 = 0;
										while (num19 <= num18)
										{
											if (CheckFibExtension(num8, num16, num11, array3[num19]))
											{
												num19++;
												continue;
											}
											goto IL_058d;
										}
									}
								}
								continue;
								IL_058d:
								if ((decimal.Compare(GlobalForm.nHLC[2, num5], GlobalForm.nHLC[2, num11]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, num13], GlobalForm.nHLC[1, num16]) > 0))
								{
									HarmonicTarget = Convert.ToDouble(GlobalForm.nHLC[1, num16]);
									AddPattern(num5, num13, num11, num8, num16, 0, 10, "Bat Bu");
								}
								i = k;
								goto end_IL_0652;
								continue;
								end_IL_0638:
								break;
							}
						}
						continue;
						end_IL_0652:
						break;
					}
				}
				break;
			}
			}
		}
	}

	private static bool CheckBat(int iPointX, int iPointA, int iPointB, int iPointC, int iPointD, int Flag)
	{
		int num;
		int num2;
		checked
		{
			num = iPointX + 1;
			num2 = iPointD - 1;
		}
		for (int i = num; i <= num2; i = checked(i + 1))
		{
			if (Flag == 11 || Flag == 9 || Flag == 7 || Flag == 28)
			{
				if (i > iPointX && i < iPointA && decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, iPointX]) > 0)
				{
					return true;
				}
				if (i > iPointA && i < iPointB && decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, iPointB]) > 0)
				{
					return true;
				}
				if (i > iPointB && i < iPointC && decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, iPointB]) > 0)
				{
					return true;
				}
				if (i > iPointC && i < iPointD && decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, iPointD]) > 0)
				{
					return true;
				}
				if (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, iPointA]) < 0)
				{
					return true;
				}
				if (i > iPointB && i < iPointC && decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, iPointC]) < 0)
				{
					return true;
				}
				if (i > iPointC && i < iPointD && decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, iPointC]) < 0)
				{
					return true;
				}
			}
			else if (Flag == 10 || Flag == 8 || Flag == 6 || Flag == 29)
			{
				if (i > iPointX && i < iPointA && decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, iPointX]) < 0)
				{
					return true;
				}
				if (i > iPointA && i < iPointB && decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, iPointB]) < 0)
				{
					return true;
				}
				if (i > iPointB && i < iPointC && decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, iPointB]) < 0)
				{
					return true;
				}
				if (i > iPointC && i < iPointD && decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, iPointD]) < 0)
				{
					return true;
				}
				if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, iPointA]) > 0)
				{
					return true;
				}
				if (i > iPointB && i < iPointC && decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, iPointC]) > 0)
				{
					return true;
				}
				if (i > iPointC && i < iPointD && decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, iPointC]) > 0)
				{
					return true;
				}
			}
		}
		return false;
	}

	private static bool CheckFibRetrace(int iPointA, int iPointB, int iPointC, double Ratio)
	{
		if (decimal.Compare(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[2, iPointB]) > 0)
		{
			decimal value = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iPointC], GlobalForm.nHLC[2, iPointB]), decimal.Subtract(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[2, iPointB]));
			decimal value2 = Math.Abs(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, iPointC], GlobalForm.nHLC[2, iPointB]), decimal.Subtract(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[2, iPointB])));
			if ((Ratio <= Convert.ToDouble(value)) & (Ratio >= Convert.ToDouble(value2)))
			{
				return false;
			}
		}
		else if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, iPointB], GlobalForm.nHLC[2, iPointA]), 0m) != 0)
		{
			decimal value3 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iPointB], GlobalForm.nHLC[2, iPointC]), decimal.Subtract(GlobalForm.nHLC[1, iPointB], GlobalForm.nHLC[2, iPointA]));
			decimal value4 = Math.Abs(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iPointB], GlobalForm.nHLC[1, iPointC]), decimal.Subtract(GlobalForm.nHLC[1, iPointB], GlobalForm.nHLC[2, iPointA])));
			if ((Ratio <= Convert.ToDouble(value3)) & (Ratio >= Convert.ToDouble(value4)))
			{
				return false;
			}
		}
		return true;
	}

	private static bool CheckFibExtension(int iPointX, int iPointA, int iPointD, double Ratio)
	{
		if (decimal.Compare(GlobalForm.nHLC[1, iPointX], GlobalForm.nHLC[2, iPointA]) > 0)
		{
			decimal value = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iPointD], GlobalForm.nHLC[2, iPointA]), decimal.Subtract(GlobalForm.nHLC[1, iPointX], GlobalForm.nHLC[2, iPointA]));
			decimal value2 = decimal.Divide(Math.Abs(decimal.Subtract(GlobalForm.nHLC[2, iPointD], GlobalForm.nHLC[2, iPointA])), decimal.Subtract(GlobalForm.nHLC[1, iPointX], GlobalForm.nHLC[2, iPointA]));
			if ((Ratio <= Convert.ToDouble(value)) & (Ratio >= Convert.ToDouble(value2)))
			{
				return false;
			}
		}
		else if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[2, iPointX]), 0m) != 0)
		{
			decimal value3 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[2, iPointD]), decimal.Subtract(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[2, iPointX]));
			decimal value4 = decimal.Divide(Math.Abs(decimal.Subtract(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[1, iPointD])), decimal.Subtract(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[2, iPointX]));
			if ((Ratio <= Convert.ToDouble(value3)) & (Ratio >= Convert.ToDouble(value4)))
			{
				return false;
			}
		}
		if ((decimal.Compare(GlobalForm.nHLC[1, iPointX], GlobalForm.nHLC[2, iPointA]) > 0) & (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[2, iPointX]), 0m) != 0))
		{
			if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[2, iPointX]), 0m) != 0)
			{
				decimal value5 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[2, iPointD]), decimal.Subtract(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[2, iPointX]));
				decimal value6 = decimal.Divide(Math.Abs(decimal.Subtract(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[1, iPointD])), decimal.Subtract(GlobalForm.nHLC[1, iPointA], GlobalForm.nHLC[2, iPointX]));
				if ((Ratio <= Convert.ToDouble(value5)) & (Ratio >= Convert.ToDouble(value6)))
				{
					return false;
				}
			}
			if (decimal.Compare(GlobalForm.nHLC[1, iPointX], GlobalForm.nHLC[2, iPointA]) > 0)
			{
				decimal value7 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iPointD], GlobalForm.nHLC[2, iPointA]), decimal.Subtract(GlobalForm.nHLC[1, iPointX], GlobalForm.nHLC[2, iPointA]));
				decimal value8 = decimal.Divide(Math.Abs(decimal.Subtract(GlobalForm.nHLC[2, iPointD], GlobalForm.nHLC[2, iPointA])), decimal.Subtract(GlobalForm.nHLC[1, iPointX], GlobalForm.nHLC[2, iPointA]));
				if ((Ratio <= Convert.ToDouble(value7)) & (Ratio >= Convert.ToDouble(value8)))
				{
					return false;
				}
			}
		}
		return true;
	}

	private static bool FindBottomArmpit(int Index1, int Index2, int TopSize)
	{
		ArmPit = -1m;
		for (int i = 0; i <= TopSize; i = checked(i + 1))
		{
			if ((ArrayTops[i] >= Index1) & (ArrayTops[i] <= Index2))
			{
				if (decimal.Compare(ArmPit, -1m) == 0)
				{
					ArmPit = GlobalForm.nHLC[1, ArrayTops[i]];
				}
				if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[i]], ArmPit) > 0)
				{
					ArmPit = GlobalForm.nHLC[1, ArrayTops[i]];
				}
			}
			else if (ArrayTops[i] > Index2)
			{
				break;
			}
		}
		if (decimal.Compare(ArmPit, -1m) == 0)
		{
			return true;
		}
		return false;
	}

	private static bool FindBottomOuterShoulders(int LSIndex, int RSIndex, int i, int z, int BottomSize, decimal Symmetry, decimal HeadShoulder)
	{
		checked
		{
			for (int j = i - 1; j >= 0; j += -1)
			{
				decimal num = GlobalForm.nHLC[2, ArrayBottoms[j]];
				if (decimal.Compare(num, GlobalForm.nHLC[2, HeadIndex]) <= 0 || (Head2Index != 0 && decimal.Compare(num, GlobalForm.nHLC[2, Head2Index]) <= 0))
				{
					break;
				}
				int k;
				for (k = z + 1; k <= BottomSize; k++)
				{
					if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[k]], GlobalForm.nHLC[2, HeadIndex]) <= 0 || (Head2Index != 0 && decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[k]], GlobalForm.nHLC[2, Head2Index]) <= 0))
					{
						goto end_IL_0319;
					}
					if (!CheckNearness(GlobalForm.nHLC[2, ArrayBottoms[k]], num, -1m, 0.25m))
					{
						continue;
					}
					int num2 = ArrayBottoms[k] - HeadIndex;
					int num3 = HeadIndex - ArrayBottoms[j];
					if (num3 < num2)
					{
						num2 = HeadIndex - ArrayBottoms[j];
						num3 = ArrayBottoms[k] - HeadIndex;
					}
					if (num2 == 0)
					{
						return true;
					}
					if (!((double)num3 / (double)num2 < Convert.ToDouble(Symmetry)) || CheckNearness(GlobalForm.nHLC[2, ArrayBottoms[k]], GlobalForm.nHLC[2, HeadIndex], -1m, HeadShoulder) || CheckNearness(GlobalForm.nHLC[2, ArrayBottoms[j]], GlobalForm.nHLC[2, HeadIndex], -1m, HeadShoulder))
					{
						continue;
					}
					goto IL_01bf;
				}
				continue;
				IL_01bf:
				decimal num4 = new decimal(HeadIndex - LSIndex);
				num4 = decimal.Multiply(2m, Conversions.ToDecimal(Interaction.IIf(decimal.Compare(new decimal(RSIndex - HeadIndex), num4) > 0, (object)(RSIndex - HeadIndex), (object)num4)));
				if ((decimal.Compare(new decimal(HeadIndex - ArrayBottoms[j]), num4) <= 0) & (decimal.Compare(new decimal(ArrayBottoms[k] - HeadIndex), num4) <= 0))
				{
					if (ArrayBottoms[k] - ArrayBottoms[j] <= 126)
					{
						if (CheckNearness(GlobalForm.nHLC[2, ArrayBottoms[k]], GlobalForm.nHLC[2, LSIndex], 0.8m, -1m))
						{
							if (CheckNearness(GlobalForm.nHLC[2, ArrayBottoms[j]], GlobalForm.nHLC[2, RSIndex], 0.8m, -1m))
							{
								iLS2 = ArrayBottoms[j];
								iRS2 = ArrayBottoms[k];
								return false;
							}
							return true;
						}
						return true;
					}
					return true;
				}
				return true;
				continue;
				end_IL_0319:
				break;
			}
			return false;
		}
	}

	private static void FindBroadeningPatterns(int Flag)
	{
		int[,] array = new int[3, 1];
		int num = -1;
		if (Flag == 113)
		{
			num = 0;
		}
		int num2 = TrendLines(-1, num, 126, 0.25m, 3, Special: true);
		checked
		{
			if (num2 > 0)
			{
				array = new int[3, Information.UBound((Array)TLArray, 2) + 1];
				int num3 = 0;
				int num4 = Information.UBound((Array)TLArray, 2);
				for (num2 = 0; num2 <= num4; num2++)
				{
					if (((num == 0) & (decimal.Compare(Math.Abs(TLSlopeArray[num2]), 0.01m) <= 0)) | ((num != 0) & (decimal.Compare(Math.Abs(TLSlopeArray[num2]), 0.03m) > 0)))
					{
						array[0, num3] = TLArray[0, num2];
						array[1, num3] = TLArray[1, num2];
						array[2, num3] = TLArray[2, num2];
						num3++;
					}
				}
				if (num3 <= 0)
				{
					return;
				}
				array = (int[,])Utils.CopyArray((Array)array, (Array)new int[3, num3 - 1 + 1]);
				string pText = "";
				num = 1;
				switch (Flag)
				{
				case 113:
					pText = "RABFA";
					break;
				case 112:
					pText = "RABFD";
					num = 0;
					break;
				case 114:
					pText = "BB";
					break;
				case 111:
					pText = "BT";
					break;
				}
				num2 = TrendLines(1, num, 126, 0.25m, 3, Special: true);
				if (num2 > 0)
				{
					int num5 = Information.UBound((Array)array, 2);
					for (num2 = 0; num2 <= num5; num2++)
					{
						int num6 = Information.UBound((Array)TLArray, 2);
						for (num3 = 0; num3 <= num6; num3++)
						{
							if (decimal.Compare(GlobalForm.nHLC[1, TLArray[0, num3]], GlobalForm.nHLC[2, array[0, num2]]) < 0 || !(((num == 0) & (decimal.Compare(Math.Abs(TLSlopeArray[num3]), 0.01m) <= 0)) | ((num != 0) & (decimal.Compare(Math.Abs(TLSlopeArray[num3]), 0.03m) > 0))))
							{
								continue;
							}
							int num7 = TLArray[0, num3];
							int num8 = num7;
							int num9 = TLArray[1, num3];
							int num10 = num9;
							int num11 = array[0, num2];
							int num12 = array[1, num2];
							int num13 = num9 - num7;
							int num14 = num12 - num11;
							num13 = Conversions.ToInteger(Interaction.IIf(num13 < num14, (object)num14, (object)num13));
							num13 = Convert.ToInt32(decimal.Multiply(new decimal(num13), 0.57m));
							if (unchecked(num11 >= num7 && num12 <= num9))
							{
								if (decimal.Compare(new decimal(num12 - num11), decimal.Multiply(new decimal(num9 - num7), 0.57m)) >= 0 && Verify(Flag, TLArray[0, num3]) && !AdjustLines(num8, num10, num11, num12, Flag) && !CheckBroadeningSlope(num8, num10, num11, num12) && !WhiteSpaceCheck(num8, num10, num11, num12))
								{
									AddPattern(num8, 0, num10, num11, 0, num12, Flag, pText);
									break;
								}
							}
							else if (unchecked(num11 <= num7 && num12 >= num9))
							{
								if (decimal.Compare(new decimal(num9 - num7), decimal.Multiply(new decimal(num12 - num11), 0.57m)) >= 0 && Verify(Flag, array[0, num2]) && !AdjustLines(num8, num10, num11, num12, Flag) && !CheckBroadeningSlope(num8, num10, num11, num12) && !WhiteSpaceCheck(num8, num10, num11, num12))
								{
									AddPattern(num8, 0, num10, num11, 0, num12, Flag, pText);
									break;
								}
							}
							else if (unchecked(num11 >= num7 && num12 >= num9 && num11 < num9))
							{
								if (num9 - num11 > num13 && Verify(Flag, TLArray[0, num3]) && !AdjustLines(num8, num10, num11, num12, Flag) && !CheckBroadeningSlope(num8, num10, num11, num12) && !WhiteSpaceCheck(num8, num10, num11, num12))
								{
									AddPattern(num8, 0, num10, num11, 0, num12, Flag, pText);
									break;
								}
							}
							else if (unchecked(num11 <= num7 && num12 <= num9 && num12 > num7) && num12 - num7 > num13 && Verify(Flag, array[0, num2]) && !AdjustLines(num8, num10, num11, num12, Flag) && !CheckBroadeningSlope(num8, num10, num11, num12) && !WhiteSpaceCheck(num8, num10, num11, num12))
							{
								AddPattern(num8, 0, num10, num11, 0, num12, Flag, pText);
								break;
							}
						}
					}
				}
			}
			array = null;
			TLArray = null;
		}
	}

	public static void FindBroadWedges(int PatternType)
	{
		object[,] array = new object[3, 1];
		string pText = Conversions.ToString(Interaction.IIf(PatternType == 110, (object)"BWA", (object)"BWD"));
		int num = Conversions.ToInteger(Interaction.IIf(PatternType == 110, (object)1, (object)(-1)));
		bool nestedSpecial = GlobalForm.NestedSpecial;
		GlobalForm.NestedSpecial = false;
		int num2 = TrendLines(-1, num, 126, 0.2m, 3, Special: true);
		checked
		{
			if (num2 > 0)
			{
				array = new object[4, Information.UBound((Array)TLArray, 2) + 1];
				int num3 = 0;
				int num4 = Information.UBound((Array)TLArray, 2);
				for (num2 = 0; num2 <= num4; num2++)
				{
					if (((num == 1) & (decimal.Compare(TLSlopeArray[num2], 0.0125m) >= 0)) | ((num == -1) & (decimal.Compare(TLSlopeArray[num2], -0.0125m) <= 0)))
					{
						array[0, num3] = TLArray[0, num2];
						array[1, num3] = TLArray[1, num2];
						array[2, num3] = TLArray[2, num2];
						array[3, num3] = TLSlopeArray[num2];
						num3++;
					}
				}
				if (num3 <= 0)
				{
					return;
				}
				array = (object[,])Utils.CopyArray((Array)array, (Array)new object[4, num3 - 1 + 1]);
				num2 = TrendLines(1, num, 126, 0.2m, 3, Special: true);
				if (num2 > 0)
				{
					int num5 = Information.UBound((Array)array, 2);
					for (num2 = 0; num2 <= num5; num2++)
					{
						int num6 = Information.UBound((Array)TLArray, 2);
						for (num3 = 0; num3 <= num6; num3++)
						{
							if (!(((num == 1) & (decimal.Compare(TLSlopeArray[num3], 0.0125m) >= 0)) | ((num == -1) & (decimal.Compare(TLSlopeArray[num3], -0.0125m) <= 0))))
							{
								continue;
							}
							int iTStart = TLArray[0, num3];
							int iTEnd = TLArray[1, num3];
							int iBStart = Conversions.ToInteger(array[0, num2]);
							int iBEnd = Conversions.ToInteger(array[1, num2]);
							int num7 = iTEnd - iTStart;
							int num8 = iBEnd - iBStart;
							num7 = Conversions.ToInteger(Interaction.IIf(num7 < num8, (object)num8, (object)num7));
							num7 = Convert.ToInt32(decimal.Multiply(new decimal(num7), 0.57m));
							if (unchecked(iBStart >= iTStart && iBEnd <= iTEnd))
							{
								if (decimal.Compare(new decimal(iBEnd - iBStart), decimal.Multiply(new decimal(iTEnd - iTStart), 0.57m)) >= 0 && BWVerify(PatternType, Conversions.ToDecimal(array[3, num2]), TLSlopeArray[num3], 0.0125m, ref iTStart, ref iTEnd, ref iBStart, ref iBEnd))
								{
									AddPattern(iTStart, 0, iTEnd, iBStart, 0, iBEnd, PatternType, pText);
									break;
								}
							}
							else if (unchecked(iBStart <= iTStart && iBEnd >= iTEnd))
							{
								if (decimal.Compare(new decimal(iTEnd - iTStart), decimal.Multiply(new decimal(iBEnd - iBStart), 0.57m)) >= 0 && BWVerify(PatternType, Conversions.ToDecimal(array[3, num2]), TLSlopeArray[num3], 0.0125m, ref iTStart, ref iTEnd, ref iBStart, ref iBEnd))
								{
									AddPattern(iTStart, 0, iTEnd, iBStart, 0, iBEnd, PatternType, pText);
									break;
								}
							}
							else if (unchecked(iBStart >= iTStart && iBEnd >= iTEnd && iBStart < iTEnd))
							{
								if (iTEnd - iBStart > num7 && BWVerify(PatternType, Conversions.ToDecimal(array[3, num2]), TLSlopeArray[num3], 0.0125m, ref iTStart, ref iTEnd, ref iBStart, ref iBEnd))
								{
									AddPattern(iTStart, 0, iTEnd, iBStart, 0, iBEnd, PatternType, pText);
									break;
								}
							}
							else if (unchecked(iBStart <= iTStart && iBEnd <= iTEnd && iBEnd > iTStart) && iBEnd - iTStart > num7 && BWVerify(PatternType, Conversions.ToDecimal(array[3, num2]), TLSlopeArray[num3], 0.0125m, ref iTStart, ref iTEnd, ref iBStart, ref iBEnd))
							{
								AddPattern(iTStart, 0, iTEnd, iBStart, 0, iBEnd, PatternType, pText);
								break;
							}
						}
					}
				}
			}
			array = null;
			TLArray = null;
			GlobalForm.NestedSpecial = nestedSpecial;
		}
	}

	private static void FindCarlV(int PatternType)
	{
		FindAllTops(3);
		int num = Information.UBound((Array)ArrayTops, 1);
		if (Information.UBound((Array)ArrayTops, 1) < 3)
		{
			return;
		}
		FindAllBottoms(3);
		int num2 = Information.UBound((Array)ArrayBottoms, 1);
		if (num2 < 3)
		{
			return;
		}
		checked
		{
			if (PatternType == 2)
			{
				int num3 = num2;
				for (int i = 0; i <= num3; i++)
				{
					int num4 = ArrayBottoms[i];
					int num5 = i + 1;
					int num6 = num2;
					for (int j = num5; j <= num6; j++)
					{
						int num7 = ArrayBottoms[j];
						if (decimal.Compare(GlobalForm.nHLC[2, num4], GlobalForm.nHLC[2, num7]) >= 0)
						{
							break;
						}
						int num8 = j + 1;
						int num9 = num2;
						for (int k = num8; k <= num9; k++)
						{
							int num10 = ArrayBottoms[k];
							if ((decimal.Compare(GlobalForm.nHLC[2, num7], GlobalForm.nHLC[2, num10]) <= 0) | (decimal.Compare(GlobalForm.nHLC[2, num10], GlobalForm.nHLC[2, num4]) <= 0))
							{
								continue;
							}
							int num11 = num;
							for (int l = 0; l <= num11; l++)
							{
								int num12 = ArrayTops[l];
								int num16;
								if (unchecked(num12 > num4 && num12 < num7))
								{
									if (decimal.Compare(GlobalForm.nHLC[1, num12], GlobalForm.nHLC[2, num7]) <= 0 || decimal.Compare(GlobalForm.nHLC[1, num4], GlobalForm.nHLC[1, num12]) >= 0 || decimal.Compare(GlobalForm.nHLC[2, num12], GlobalForm.nHLC[2, num7]) <= 0)
									{
										goto end_IL_0421;
									}
									int num13 = l + 1;
									int num14 = num;
									int num15 = num13;
									while (num15 <= num14)
									{
										num16 = ArrayTops[num15];
										if (!unchecked(num16 > num7 && num16 < num10) || decimal.Compare(GlobalForm.nHLC[1, num16], GlobalForm.nHLC[1, num12]) <= 0)
										{
											num15++;
											continue;
										}
										goto IL_01df;
									}
								}
								else if (num12 > num7)
								{
									goto end_IL_0421;
								}
								continue;
								IL_01df:
								if (decimal.Compare(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[1, num16]) >= 0 || decimal.Compare(GlobalForm.nHLC[2, num16], GlobalForm.nHLC[2, num10]) <= 0)
								{
									goto end_IL_0421;
								}
								int num17 = num4 + 1;
								int num18 = num10 - 1;
								int num19 = num17;
								while (true)
								{
									if (num19 <= num18)
									{
										if (unchecked((num19 < num12 && (decimal.Compare(GlobalForm.nHLC[1, num19], GlobalForm.nHLC[1, num12]) >= 0 || decimal.Compare(GlobalForm.nHLC[2, num19], GlobalForm.nHLC[2, num4]) <= 0)) || (num19 > num12 && num19 < num7 && (decimal.Compare(GlobalForm.nHLC[2, num19], GlobalForm.nHLC[2, num7]) <= 0 || decimal.Compare(GlobalForm.nHLC[1, num19], GlobalForm.nHLC[1, num12]) >= 0)) || (num19 > num7 && num19 < num16 && (decimal.Compare(GlobalForm.nHLC[1, num19], GlobalForm.nHLC[1, num16]) >= 0 || decimal.Compare(GlobalForm.nHLC[2, num19], GlobalForm.nHLC[2, num7]) <= 0))) || (num19 > num16 && (decimal.Compare(GlobalForm.nHLC[2, num19], GlobalForm.nHLC[2, num10]) <= 0 || decimal.Compare(GlobalForm.nHLC[1, num19], GlobalForm.nHLC[1, num16]) >= 0)))
										{
											break;
										}
										num19++;
										continue;
									}
									HarmonicTarget = Convert.ToDouble(decimal.Add(GlobalForm.nHLC[2, num10], decimal.Subtract(GlobalForm.nHLC[1, num16], GlobalForm.nHLC[2, num4])));
									AddPattern(num4, num12, num10, num7, num16, 0, 2, "Carl Bu");
									break;
								}
								goto end_IL_0421;
							}
						}
						continue;
						end_IL_0421:
						break;
					}
				}
				return;
			}
			int num20 = num;
			for (int i = 0; i <= num20; i++)
			{
				int num4 = ArrayTops[i];
				int num21 = i + 1;
				int num22 = num;
				for (int j = num21; j <= num22; j++)
				{
					int num7 = ArrayTops[j];
					if (decimal.Compare(GlobalForm.nHLC[1, num4], GlobalForm.nHLC[1, num7]) <= 0)
					{
						break;
					}
					int num23 = j + 1;
					int num24 = num;
					for (int k = num23; k <= num24; k++)
					{
						int num10 = ArrayTops[k];
						if ((decimal.Compare(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[1, num10]) >= 0) | (decimal.Compare(GlobalForm.nHLC[1, num10], GlobalForm.nHLC[1, num4]) >= 0))
						{
							continue;
						}
						int num25 = num2;
						for (int l = 0; l <= num25; l++)
						{
							int num12 = ArrayBottoms[l];
							int num16;
							if (unchecked(num12 > num4 && num12 < num7))
							{
								if (decimal.Compare(GlobalForm.nHLC[2, num12], GlobalForm.nHLC[1, num7]) >= 0 || decimal.Compare(GlobalForm.nHLC[2, num4], GlobalForm.nHLC[2, num12]) <= 0 || decimal.Compare(GlobalForm.nHLC[1, num12], GlobalForm.nHLC[1, num7]) >= 0)
								{
									goto end_IL_0811;
								}
								int num26 = l + 1;
								int num27 = num2;
								int num15 = num26;
								while (num15 <= num27)
								{
									num16 = ArrayBottoms[num15];
									if (!unchecked(num16 > num7 && num16 < num10) || decimal.Compare(GlobalForm.nHLC[2, num16], GlobalForm.nHLC[2, num12]) >= 0)
									{
										num15++;
										continue;
									}
									goto IL_05cf;
								}
							}
							else if (num12 > num7)
							{
								goto end_IL_0811;
							}
							continue;
							IL_05cf:
							if (decimal.Compare(GlobalForm.nHLC[2, num7], GlobalForm.nHLC[2, num16]) <= 0 || decimal.Compare(GlobalForm.nHLC[1, num16], GlobalForm.nHLC[1, num10]) >= 0)
							{
								goto end_IL_0811;
							}
							int num28 = num4 + 1;
							int num29 = num10 - 1;
							int num19 = num28;
							while (true)
							{
								if (num19 <= num29)
								{
									if (unchecked((num19 < num12 && (decimal.Compare(GlobalForm.nHLC[2, num19], GlobalForm.nHLC[2, num12]) <= 0 || decimal.Compare(GlobalForm.nHLC[1, num19], GlobalForm.nHLC[1, num4]) >= 0)) || (num19 > num12 && num19 < num7 && (decimal.Compare(GlobalForm.nHLC[1, num19], GlobalForm.nHLC[1, num7]) >= 0 || decimal.Compare(GlobalForm.nHLC[2, num19], GlobalForm.nHLC[2, num12]) <= 0)) || (num19 > num7 && num19 < num16 && (decimal.Compare(GlobalForm.nHLC[2, num19], GlobalForm.nHLC[2, num16]) <= 0 || decimal.Compare(GlobalForm.nHLC[1, num19], GlobalForm.nHLC[1, num7]) >= 0))) || (num19 > num16 && (decimal.Compare(GlobalForm.nHLC[1, num19], GlobalForm.nHLC[1, num10]) >= 0 || decimal.Compare(GlobalForm.nHLC[2, num19], GlobalForm.nHLC[2, num16]) <= 0)))
									{
										break;
									}
									num19++;
									continue;
								}
								HarmonicTarget = Convert.ToDouble(decimal.Subtract(GlobalForm.nHLC[1, num10], decimal.Subtract(GlobalForm.nHLC[1, num4], GlobalForm.nHLC[2, num16])));
								AddPattern(num4, num12, num10, num7, num16, 0, 3, "Carl Be");
								break;
							}
							goto end_IL_0811;
						}
					}
					continue;
					end_IL_0811:
					break;
				}
			}
		}
	}

	private static void FindCPRD()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				decimal d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.25m);
				if (decimal.Compare(GlobalForm.nHLC[0, i], decimal.Add(GlobalForm.nHLC[2, i], d)) < 0 && ((decimal.Compare(GlobalForm.nHLC[3, i], decimal.Subtract(GlobalForm.nHLC[1, i], d)) > 0) & (decimal.Compare(GlobalForm.nHLC[3, i - 1], GlobalForm.nHLC[3, i]) < 0)) && HLRegression(i - 1, 2, 5) == -1)
				{
					AddPattern(i, 0, i, 0, 0, 0, 52, "C");
				}
			}
		}
	}

	private static void FindCPRU()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				decimal d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.25m);
				if (decimal.Compare(GlobalForm.nHLC[0, i], decimal.Subtract(GlobalForm.nHLC[1, i], d)) > 0 && ((decimal.Compare(GlobalForm.nHLC[3, i], decimal.Add(GlobalForm.nHLC[2, i], d)) < 0) & (decimal.Compare(GlobalForm.nHLC[3, i - 1], GlobalForm.nHLC[3, i]) > 0)) && HLRegression(i - 1, 2, 5) == 1)
				{
					AddPattern(i, 0, i, 0, 0, 0, 51, "c");
				}
			}
		}
	}

	private static void FindButterfly(int Flag)
	{
		double[] array = new double[6] { 0.382, 0.5, 0.618, 0.707, 0.786, 0.886 };
		double[] array2 = new double[3] { 1.618, 2.0, 2.24 };
		double num = Conversions.ToDouble(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.01, (object)0.03));
		FindAllTops(3);
		int num2 = Information.UBound((Array)ArrayTops, 1);
		if (Information.UBound((Array)ArrayTops, 1) < 3)
		{
			return;
		}
		FindAllBottoms(3);
		int num3 = Information.UBound((Array)ArrayBottoms, 1);
		if (num3 < 3)
		{
			return;
		}
		checked
		{
			switch (Flag)
			{
			case 9:
			{
				int num21 = num2;
				for (int i = 0; i <= num21; i++)
				{
					int num5 = ArrayTops[i];
					int num22 = num3;
					for (int j = 0; j <= num22; j++)
					{
						int num7 = ArrayBottoms[j];
						if (num7 <= num5)
						{
							continue;
						}
						int num23 = i + 1;
						int num24 = num2;
						int num10;
						int num13;
						int num16;
						for (int k = num23; k <= num24; k++)
						{
							num10 = ArrayTops[k];
							if (decimal.Compare(GlobalForm.nHLC[1, num10], GlobalForm.nHLC[1, num5]) >= 0)
							{
								break;
							}
							if (num7 >= num10 || CheckFibRetrace(num5, num7, num10, 0.786))
							{
								continue;
							}
							int num25 = k + 1;
							int num26 = num2;
							for (int l = num25; l <= num26; l++)
							{
								num13 = ArrayTops[l];
								if (num13 - num5 > 126)
								{
									break;
								}
								if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[2, num7]), 0m) == 0)
								{
									continue;
								}
								decimal value = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num13], GlobalForm.nHLC[2, num7]), decimal.Subtract(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[2, num7]));
								if (!((Convert.ToDouble(value) >= 1.27 - num) & (Convert.ToDouble(value) <= 1.27 + num)))
								{
									continue;
								}
								int num27 = j + 1;
								int num28 = num3;
								for (int m = num27; m <= num28; m++)
								{
									num16 = ArrayBottoms[m];
									if (num16 >= num13)
									{
										break;
									}
									if (num16 <= num10)
									{
										continue;
									}
									int num29 = array.Count() - 1;
									int num18 = 0;
									while (num18 <= num29)
									{
										if (CheckFibRetrace(num7, num10, num16, array[num18]))
										{
											num18++;
											continue;
										}
										goto IL_0243;
									}
									continue;
									IL_0243:
									if (CheckBat(num5, num7, num10, num16, num13, 9))
									{
										continue;
									}
									goto IL_0259;
								}
							}
							continue;
							IL_0259:
							int num30 = array2.Count() - 1;
							int num20 = 0;
							while (num20 <= num30)
							{
								if (CheckFibExtension(num10, num16, num13, array2[num20]))
								{
									num20++;
									continue;
								}
								goto IL_027e;
							}
						}
						continue;
						IL_027e:
						if ((decimal.Compare(GlobalForm.nHLC[1, num13], GlobalForm.nHLC[1, num5]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, num16], GlobalForm.nHLC[2, num7]) > 0))
						{
							HarmonicTarget = Convert.ToDouble(GlobalForm.nHLC[2, num16]);
							AddPattern(num5, num7, num13, num10, num16, 0, 9, "Butt Be");
						}
						break;
					}
				}
				break;
			}
			case 8:
			{
				int num4 = num3;
				for (int i = 0; i <= num4; i++)
				{
					int num5 = ArrayBottoms[i];
					int num6 = num2;
					for (int j = 0; j <= num6; j++)
					{
						int num7 = ArrayTops[j];
						if (num7 <= num5)
						{
							continue;
						}
						int num8 = i + 1;
						int num9 = num3;
						int num10;
						int num13;
						int num16;
						for (int k = num8; k <= num9; k++)
						{
							num10 = ArrayBottoms[k];
							if (decimal.Compare(GlobalForm.nHLC[2, num10], GlobalForm.nHLC[2, num5]) <= 0)
							{
								break;
							}
							if (num7 >= num10 || CheckFibRetrace(num5, num7, num10, 0.786))
							{
								continue;
							}
							int num11 = k + 1;
							int num12 = num3;
							for (int l = num11; l <= num12; l++)
							{
								num13 = ArrayBottoms[l];
								if (num13 - num5 > 126)
								{
									break;
								}
								if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num5]), 0m) == 0)
								{
									continue;
								}
								decimal value = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num13]), decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num5]));
								if (!((Convert.ToDouble(value) >= 1.27 - num) & (Convert.ToDouble(value) <= 1.27 + num)))
								{
									continue;
								}
								int num14 = j + 1;
								int num15 = num2;
								for (int m = num14; m <= num15; m++)
								{
									num16 = ArrayTops[m];
									if (num16 >= num13)
									{
										break;
									}
									if (num16 <= num10)
									{
										continue;
									}
									int num17 = array.Count() - 1;
									int num18 = 0;
									while (num18 <= num17)
									{
										if (CheckFibRetrace(num7, num10, num16, array[num18]))
										{
											num18++;
											continue;
										}
										goto IL_0511;
									}
									continue;
									IL_0511:
									if (CheckBat(num5, num7, num10, num16, num13, 8))
									{
										continue;
									}
									goto IL_0526;
								}
							}
							continue;
							IL_0526:
							int num19 = array2.Count() - 1;
							int num20 = 0;
							while (num20 <= num19)
							{
								if (CheckFibExtension(num10, num16, num13, array2[num20]))
								{
									num20++;
									continue;
								}
								goto IL_054b;
							}
						}
						continue;
						IL_054b:
						if ((decimal.Compare(GlobalForm.nHLC[2, num5], GlobalForm.nHLC[2, num13]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[1, num16]) > 0))
						{
							HarmonicTarget = Convert.ToDouble(GlobalForm.nHLC[1, num16]);
							AddPattern(num5, num7, num13, num10, num16, 0, 8, "Butt Bu");
						}
						break;
					}
				}
				break;
			}
			}
		}
	}

	private static void FindChannels(int iType)
	{
		GlobalForm.DisplayFmtns[] array = null;
		checked
		{
			array = new GlobalForm.DisplayFmtns[GlobalForm.PatternCount + 1];
			if (GlobalForm.PatternCount > 0)
			{
				GlobalForm.ChartPatterns.CopyTo(array, 0);
				GlobalForm.ChartPatterns = null;
			}
			int num = GlobalForm.PatternCount;
			GlobalForm.PatternCount = 0;
			int num13 = default(int);
			int num14 = default(int);
			switch (iType)
			{
			case 82:
			{
				FindTLs(58);
				int patternCount = GlobalForm.PatternCount;
				if (patternCount == 0)
				{
					break;
				}
				int num17 = patternCount - 1;
				for (int num18 = 0; num18 <= num17; num18++)
				{
					int iStartDate = GlobalForm.ChartPatterns[num18].iStartDate;
					int iEndDate = GlobalForm.ChartPatterns[num18].iMidDate;
					decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iStartDate], GlobalForm.nHLC[1, iEndDate]), new decimal(iStartDate - iEndDate));
					decimal num9 = default(decimal);
					decimal num10 = default(decimal);
					int num19 = iStartDate;
					int num20 = iEndDate;
					for (int j = num19; j <= num20; j++)
					{
						float num4 = Convert.ToSingle(decimal.Add(decimal.Multiply(d, new decimal(j - iStartDate)), GlobalForm.nHLC[1, iStartDate]));
						decimal item2 = new decimal(num4 - Convert.ToSingle(GlobalForm.nHLC[2, j]));
						if (j <= (int)Math.Round((double)(iStartDate + iEndDate) / 2.0))
						{
							if (decimal.Compare(item2, num9) > 0)
							{
								num9 = item2;
								num13 = j;
							}
						}
						else if (decimal.Compare(item2, num10) > 0)
						{
							num10 = item2;
							num14 = j;
						}
					}
					if (!CheckNearness(num9, num10, -1m, 0.25m))
					{
						continue;
					}
					int num15 = (int)Math.Round((double)(iEndDate + iStartDate) / 2.0);
					int num16 = (int)Math.Round((double)(iEndDate - iStartDate) / 8.0);
					if ((num13 <= num15 - num16) & (num14 >= num15 + num16))
					{
						int patternCount3 = GlobalForm.PatternCount;
						AddPattern(iStartDate, iEndDate, GlobalForm.ChartPatterns[num18].iEndDate, 0, 0, 0, iType, "Channel");
						if (patternCount3 != GlobalForm.PatternCount)
						{
							GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].dChannelHeight = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num9, num10) > 0, (object)num9, (object)num10));
							array = (GlobalForm.DisplayFmtns[])Utils.CopyArray((Array)array, (Array)new GlobalForm.DisplayFmtns[num + 1]);
							array[num].iStartDate = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iStartDate;
							array[num].iMidDate = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iMidDate;
							array[num].iEndDate = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iEndDate;
							array[num].Type = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].Type;
							array[num].iText = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iText;
							array[num].iStart2Date = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iStart2Date;
							array[num].iMid2Date = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iMid2Date;
							array[num].iEnd2Date = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iEnd2Date;
							array[num].RenderColor = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].RenderColor;
							array[num].PriceTarget = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].PriceTarget;
							array[num].dChannelHeight = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].dChannelHeight;
							num++;
						}
					}
				}
				break;
			}
			case 1:
			{
				FindTLs(57);
				int patternCount = GlobalForm.PatternCount;
				if (patternCount == 0)
				{
					break;
				}
				int num7 = patternCount - 1;
				for (int num8 = 0; num8 <= num7; num8++)
				{
					int iStartDate = GlobalForm.ChartPatterns[num8].iStartDate;
					int iEndDate = GlobalForm.ChartPatterns[num8].iMidDate;
					decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, iEndDate], GlobalForm.nHLC[2, iStartDate]), new decimal(iEndDate - iStartDate));
					decimal num9 = default(decimal);
					decimal num10 = default(decimal);
					int num11 = iStartDate;
					int num12 = iEndDate;
					for (int j = num11; j <= num12; j++)
					{
						float num4 = Convert.ToSingle(decimal.Add(decimal.Multiply(d, new decimal(j - iStartDate)), GlobalForm.nHLC[2, iStartDate]));
						decimal item2 = new decimal(Convert.ToSingle(GlobalForm.nHLC[1, j]) - num4);
						if (j <= (int)Math.Round((double)(iStartDate + iEndDate) / 2.0))
						{
							if (decimal.Compare(item2, num9) > 0)
							{
								num9 = item2;
								num13 = j;
							}
						}
						else if (decimal.Compare(item2, num10) > 0)
						{
							num10 = item2;
							num14 = j;
						}
					}
					if (!CheckNearness(num9, num10, -1m, 0.25m))
					{
						continue;
					}
					int num15 = (int)Math.Round((double)(iEndDate + iStartDate) / 2.0);
					int num16 = (int)Math.Round((double)(iEndDate - iStartDate) / 8.0);
					if ((num13 <= num15 - num16) & (num14 >= num15 + num16))
					{
						int patternCount2 = GlobalForm.PatternCount;
						AddPattern(iStartDate, iEndDate, GlobalForm.ChartPatterns[num8].iEndDate, 0, 0, 0, iType, "Channel");
						if (patternCount2 != GlobalForm.PatternCount)
						{
							GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].dChannelHeight = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num9, num10) > 0, (object)num9, (object)num10));
							array = (GlobalForm.DisplayFmtns[])Utils.CopyArray((Array)array, (Array)new GlobalForm.DisplayFmtns[num + 1]);
							array[num].iStartDate = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iStartDate;
							array[num].iMidDate = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iMidDate;
							array[num].iEndDate = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iEndDate;
							array[num].Type = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].Type;
							array[num].iText = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iText;
							array[num].iStart2Date = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iStart2Date;
							array[num].iMid2Date = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iMid2Date;
							array[num].iEnd2Date = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iEnd2Date;
							array[num].RenderColor = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].RenderColor;
							array[num].PriceTarget = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].PriceTarget;
							array[num].dChannelHeight = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].dChannelHeight;
							num++;
						}
					}
				}
				break;
			}
			case -1:
			{
				FindTLs(57);
				int patternCount = GlobalForm.PatternCount;
				if (patternCount == 0)
				{
					break;
				}
				int num21 = patternCount - 1;
				for (int num22 = 0; num22 <= num21; num22++)
				{
					int iStartDate = GlobalForm.ChartPatterns[num22].iStartDate;
					int iEndDate = GlobalForm.ChartPatterns[num22].iEndDate;
					decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, iEndDate], GlobalForm.nHLC[2, iStartDate]), new decimal(iEndDate - iStartDate));
					FindAllTops(2);
					if (Information.UBound((Array)ArrayTops, 1) <= 2)
					{
						break;
					}
					List<Tuple<int, decimal>> list2 = new List<Tuple<int, decimal>>();
					int num23 = Information.UBound((Array)ArrayTops, 1) - 1;
					for (int j = 0; j <= num23; j++)
					{
						if ((ArrayTops[j] >= iStartDate) & (ArrayTops[j] <= iEndDate))
						{
							float num4 = Convert.ToSingle(decimal.Add(decimal.Multiply(d, new decimal(ArrayTops[j] - iStartDate)), GlobalForm.nHLC[2, iStartDate]));
							list2.Add(Tuple.Create(ArrayTops[j], new decimal(Convert.ToSingle(GlobalForm.nHLC[1, ArrayTops[j]]) - num4)));
						}
					}
					list2 = list2.OrderByDescending([SpecialName] (Tuple<int, decimal> z) => z.Item2).ToList();
					int num5 = 0;
					int index = 0;
					int num24 = 0;
					int num25 = list2.Count - 1;
					for (int j = 0; j <= num25; j++)
					{
						num24 = j;
						int num26 = j + 1;
						int num27 = list2.Count - 1;
						for (int num28 = num26; num28 <= num27; num28++)
						{
							if (CheckNearness(list2[j].Item2, list2[num28].Item2, -1m, 0.25m))
							{
								num5++;
								index = num28;
							}
						}
						if (num5 > 1)
						{
							AddPattern(list2[num24].Item1, 0, list2[index].Item1, 0, 0, 0, iType, "Channel");
							GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].dChannelHeight = list2[num24].Item2;
							array = (GlobalForm.DisplayFmtns[])Utils.CopyArray((Array)array, (Array)new GlobalForm.DisplayFmtns[num + 1]);
							array[num].iStartDate = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iStartDate;
							array[num].iMidDate = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iMidDate;
							array[num].iEndDate = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iEndDate;
							array[num].Type = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].Type;
							array[num].iText = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iText;
							array[num].iStart2Date = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iStart2Date;
							array[num].iMid2Date = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iMid2Date;
							array[num].iEnd2Date = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iEnd2Date;
							array[num].RenderColor = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].RenderColor;
							array[num].PriceTarget = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].PriceTarget;
							array[num].dChannelHeight = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].dChannelHeight;
							num++;
							break;
						}
					}
				}
				break;
			}
			default:
			{
				FindTLs(57);
				int patternCount = GlobalForm.PatternCount;
				if (patternCount == 0)
				{
					break;
				}
				int num2 = patternCount - 1;
				for (int i = 0; i <= num2; i++)
				{
					int iStartDate = GlobalForm.ChartPatterns[i].iStartDate;
					int iEndDate = GlobalForm.ChartPatterns[i].iEndDate;
					decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, iEndDate], GlobalForm.nHLC[2, iStartDate]), new decimal(iEndDate - iStartDate));
					FindAllTops(2);
					if (Information.UBound((Array)ArrayTops, 1) <= 2)
					{
						break;
					}
					List<Tuple<int, decimal>> list = new List<Tuple<int, decimal>>();
					int num3 = Information.UBound((Array)ArrayTops, 1) - 1;
					for (int j = 0; j <= num3; j++)
					{
						if ((ArrayTops[j] >= iStartDate) & (ArrayTops[j] <= iEndDate))
						{
							float num4 = Convert.ToSingle(decimal.Add(decimal.Multiply(d, new decimal(ArrayTops[j] - iStartDate)), GlobalForm.nHLC[2, iStartDate]));
							list.Add(Tuple.Create(ArrayTops[j], new decimal(Convert.ToSingle(GlobalForm.nHLC[1, ArrayTops[j]]) - num4)));
						}
					}
					list = list.OrderByDescending([SpecialName] (Tuple<int, decimal> z) => z.Item2).ToList();
					foreach (Tuple<int, decimal> item3 in list)
					{
						int item = item3.Item1;
						decimal item2 = item3.Item2;
						int num5 = 0;
						int num6 = Information.UBound((Array)ArrayTops, 1) - 1;
						for (int j = 0; j <= num6; j++)
						{
							if ((ArrayTops[j] >= iStartDate) & (ArrayTops[j] <= iEndDate))
							{
								if (CheckNearness(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[1, item], -1m, 0.25m))
								{
									num5++;
								}
								if (num5 >= 2)
								{
									AddPattern(iStartDate, 0, iEndDate, 0, 0, 0, iType, "Channel");
									GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].dChannelHeight = item2;
									array = (GlobalForm.DisplayFmtns[])Utils.CopyArray((Array)array, (Array)new GlobalForm.DisplayFmtns[num + 1]);
									array[num].iStartDate = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iStartDate;
									array[num].iMidDate = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iMidDate;
									array[num].iEndDate = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iEndDate;
									array[num].Type = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].Type;
									array[num].iText = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iText;
									array[num].iStart2Date = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iStart2Date;
									array[num].iMid2Date = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iMid2Date;
									array[num].iEnd2Date = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].iEnd2Date;
									array[num].RenderColor = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].RenderColor;
									array[num].PriceTarget = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].PriceTarget;
									array[num].dChannelHeight = GlobalForm.ChartPatterns[GlobalForm.PatternCount - 1].dChannelHeight;
									num++;
									goto end_IL_0f6f;
								}
							}
						}
						continue;
						end_IL_0f6f:
						break;
					}
				}
				break;
			}
			}
			GlobalForm.PatternCount = num;
			GlobalForm.ChartPatterns = (GlobalForm.DisplayFmtns[])Utils.CopyArray((Array)GlobalForm.ChartPatterns, (Array)new GlobalForm.DisplayFmtns[GlobalForm.PatternCount + 1]);
			array.CopyTo(GlobalForm.ChartPatterns, 0);
		}
	}

	private static void FindCrab(int Flag)
	{
		double[] array = new double[6] { 0.382, 0.5, 0.618, 0.707, 0.786, 0.886 };
		double[] array2 = new double[3] { 2.618, 3.14, 3.618 };
		double[] array3 = new double[3] { 0.382, 0.5, 0.618 };
		double num = Conversions.ToDouble(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.01, (object)0.03));
		FindAllTops(3);
		int num2 = Information.UBound((Array)ArrayTops, 1);
		if (Information.UBound((Array)ArrayTops, 1) < 3)
		{
			return;
		}
		FindAllBottoms(3);
		int num3 = Information.UBound((Array)ArrayBottoms, 1);
		if (num3 < 3)
		{
			return;
		}
		checked
		{
			switch (Flag)
			{
			case 7:
			{
				int num22 = num2;
				for (int i = 0; i <= num22; i++)
				{
					int num5 = ArrayTops[i];
					int num23 = num3;
					for (int j = 0; j <= num23; j++)
					{
						int num7 = ArrayBottoms[j];
						if (num7 <= num5)
						{
							continue;
						}
						int num24 = i + 1;
						int num25 = num2;
						int num10;
						int num14;
						int num17;
						for (int k = num24; k <= num25; k++)
						{
							num10 = ArrayTops[k];
							if (decimal.Compare(GlobalForm.nHLC[1, num10], GlobalForm.nHLC[1, num5]) >= 0)
							{
								break;
							}
							if (num7 >= num10)
							{
								continue;
							}
							int num26 = array3.Count() - 1;
							for (int l = 0; l <= num26; l++)
							{
								if (CheckFibRetrace(num5, num7, num10, array3[l]))
								{
									continue;
								}
								int num27 = k + 1;
								int num28 = num2;
								for (int m = num27; m <= num28; m++)
								{
									num14 = ArrayTops[m];
									if (num14 - num5 > 126)
									{
										goto end_IL_0358;
									}
									if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num5]), 0m) == 0)
									{
										continue;
									}
									decimal value = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num14], GlobalForm.nHLC[2, num7]), decimal.Subtract(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[2, num7]));
									if (!((Convert.ToDouble(value) >= 1.618 - num) & (Convert.ToDouble(value) <= 1.618 + num)))
									{
										continue;
									}
									int num29 = j + 1;
									int num30 = num3;
									for (int n = num29; n <= num30; n++)
									{
										num17 = ArrayBottoms[n];
										if (num17 >= num14)
										{
											break;
										}
										if (num17 <= num10)
										{
											continue;
										}
										int num31 = array.Count() - 1;
										int num19 = 0;
										while (num19 <= num31)
										{
											if (CheckFibRetrace(num7, num10, num17, array[num19]))
											{
												num19++;
												continue;
											}
											goto IL_0264;
										}
										continue;
										IL_0264:
										if (CheckBat(num5, num7, num10, num17, num14, 7))
										{
											continue;
										}
										goto IL_0279;
									}
								}
								continue;
								end_IL_0358:
								break;
							}
							continue;
							IL_0279:
							int num32 = array2.Count() - 1;
							int num21 = 0;
							while (num21 <= num32)
							{
								if (CheckFibExtension(num10, num17, num14, array2[num21]))
								{
									num21++;
									continue;
								}
								goto IL_029e;
							}
						}
						continue;
						IL_029e:
						if ((decimal.Compare(GlobalForm.nHLC[1, num14], GlobalForm.nHLC[1, num5]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, num7], GlobalForm.nHLC[2, num17]) < 0))
						{
							HarmonicTarget = Convert.ToDouble(GlobalForm.nHLC[2, num17]);
							AddPattern(num5, num7, num14, num10, num17, 0, 7, "Crab Be");
						}
						break;
					}
				}
				break;
			}
			case 6:
			{
				int num4 = num3;
				for (int i = 0; i <= num4; i++)
				{
					int num5 = ArrayBottoms[i];
					int num6 = num2;
					for (int j = 0; j <= num6; j++)
					{
						int num7 = ArrayTops[j];
						if (num7 <= num5)
						{
							continue;
						}
						int num8 = i + 1;
						int num9 = num3;
						int num10;
						int num14;
						int num17;
						for (int k = num8; k <= num9; k++)
						{
							num10 = ArrayBottoms[k];
							if (decimal.Compare(GlobalForm.nHLC[2, num10], GlobalForm.nHLC[2, num5]) <= 0)
							{
								break;
							}
							if (num7 >= num10)
							{
								continue;
							}
							int num11 = array3.Count() - 1;
							for (int l = 0; l <= num11; l++)
							{
								if (CheckFibRetrace(num5, num7, num10, array3[l]))
								{
									continue;
								}
								int num12 = k + 1;
								int num13 = num3;
								for (int m = num12; m <= num13; m++)
								{
									num14 = ArrayBottoms[m];
									if (num14 - num5 > 126)
									{
										goto end_IL_0642;
									}
									if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num5]), 0m) == 0)
									{
										continue;
									}
									decimal value = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num14]), decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num5]));
									if (!((Convert.ToDouble(value) >= 1.618 - num) & (Convert.ToDouble(value) <= 1.618 + num)))
									{
										continue;
									}
									int num15 = j + 1;
									int num16 = num2;
									for (int n = num15; n <= num16; n++)
									{
										num17 = ArrayTops[n];
										if (num17 >= num14)
										{
											break;
										}
										if (num17 <= num10)
										{
											continue;
										}
										int num18 = array.Count() - 1;
										int num19 = 0;
										while (num19 <= num18)
										{
											if (CheckFibRetrace(num7, num10, num17, array[num19]))
											{
												num19++;
												continue;
											}
											goto IL_054e;
										}
										continue;
										IL_054e:
										if (CheckBat(num5, num7, num10, num17, num14, 6))
										{
											continue;
										}
										goto IL_0563;
									}
								}
								continue;
								end_IL_0642:
								break;
							}
							continue;
							IL_0563:
							int num20 = array2.Count() - 1;
							int num21 = 0;
							while (num21 <= num20)
							{
								if (CheckFibExtension(num10, num17, num14, array2[num21]))
								{
									num21++;
									continue;
								}
								goto IL_0588;
							}
						}
						continue;
						IL_0588:
						if ((decimal.Compare(GlobalForm.nHLC[2, num5], GlobalForm.nHLC[2, num14]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[1, num17]) > 0))
						{
							HarmonicTarget = Convert.ToDouble(GlobalForm.nHLC[1, num17]);
							AddPattern(num5, num7, num14, num10, num17, 0, 6, "Crab Bu");
						}
						break;
					}
				}
				break;
			}
			}
		}
	}

	private static void FindCup()
	{
		int tradeDays = ((!GlobalForm.StrictPatterns) ? 10 : 20);
		FindAllTops(tradeDays);
		checked
		{
			for (int i = Information.UBound((Array)ArrayTops, 1); i >= 0; i += -1)
			{
				int num = ArrayTops[i];
				for (int j = i - 1; j >= 0; j += -1)
				{
					int num2 = ArrayTops[j];
					if ((num - num2 > 325) | (num - num2 < 35))
					{
						break;
					}
					int num3 = num2 + 1;
					int num4 = num2 + 2;
					int num5 = num - 1;
					for (int k = num4; k <= num5; k++)
					{
						num3 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num3]) < 0, (object)k, (object)num3));
					}
					decimal d = decimal.Add(GlobalForm.nHLC[2, num3], decimal.Divide(decimal.Multiply(4m, decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num3])), 5m));
					decimal d2 = decimal.Add(GlobalForm.nHLC[2, num3], decimal.Divide(decimal.Multiply(6m, decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num3])), 5m));
					if ((decimal.Compare(GlobalForm.nHLC[1, num2], d2) > 0) | (decimal.Compare(GlobalForm.nHLC[1, num2], d) < 0))
					{
						continue;
					}
					int num6 = num2 + (int)Math.Round((double)(num - num2) / 5.0);
					int num7 = num2 + 2 * (int)Math.Round((double)(num - num2) / 5.0);
					int num8 = num2 + 3 * (int)Math.Round((double)(num - num2) / 5.0);
					int num9 = (int)Math.Round((double)num - (double)(num - num2) / 5.0);
					decimal d3 = decimal.Add(GlobalForm.nHLC[2, num3], decimal.Divide(decimal.Multiply(3m, decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num3])), 5m));
					decimal num10 = decimal.Add(GlobalForm.nHLC[2, num3], decimal.Divide(decimal.Multiply(2m, decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num3])), 5m));
					bool flag = false;
					int num11 = num9;
					int l;
					for (l = num6; l <= num11; l++)
					{
						if (decimal.Compare(GlobalForm.nHLC[3, l], d3) > 0)
						{
							flag = true;
							break;
						}
						if (unchecked(l >= num7 && l <= num8) && decimal.Compare(GlobalForm.nHLC[3, l], num10) > 0)
						{
							flag = true;
							break;
						}
					}
					if (flag)
					{
						continue;
					}
					int num12 = num + 1;
					int hLCRange = GlobalForm.HLCRange;
					for (l = num12; l <= hLCRange; l++)
					{
						if (decimal.Compare(GlobalForm.nHLC[2, l], decimal.Divide(decimal.Add(num10, d3), 2m)) < 0)
						{
							goto end_IL_040a;
						}
						if ((decimal.Compare(GlobalForm.nHLC[3, l], GlobalForm.nHLC[1, num]) > 0) & (l - num > 5))
						{
							if ((double)(l - num) < (double)(num - num2) / 4.0)
							{
								HarmonicTarget = Convert.ToDouble(decimal.Add(GlobalForm.nHLC[1, num], decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num3])));
								AddPattern(num2, num, l, 0, 0, 0, 81, "Cup");
							}
							goto end_IL_040a;
						}
					}
					HarmonicTarget = Convert.ToDouble(decimal.Add(GlobalForm.nHLC[1, num], decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num3])));
					AddPattern(num2, num, l - 1, 0, 0, 0, 81, "Cup?");
					continue;
					end_IL_040a:
					break;
				}
			}
		}
	}

	private static void FindDeadCatBounce()
	{
		int chartEndIndex = GlobalForm.ChartEndIndex;
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			for (int i = chartEndIndex; i >= num; i += -1)
			{
				if (decimal.Compare(GlobalForm.nHLC[3, i - 1], 0m) != 0 && decimal.Compare(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[3, i - 1], GlobalForm.nHLC[3, i]), GlobalForm.nHLC[3, i - 1]), 0.15m) >= 0)
				{
					AddPattern(i - 1, 0, i, 0, 0, 0, 100, "DCB\r\n" + Strings.Format((object)decimal.Divide(decimal.Subtract(GlobalForm.nHLC[3, i - 1], GlobalForm.nHLC[3, i]), GlobalForm.nHLC[3, i - 1]), " -#%"));
				}
			}
		}
	}

	private static void FindDescendingTriangle()
	{
		decimal priceVary = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.05, (object)0.1));
		decimal d = default(decimal);
		int num = 0;
		int num2 = 0;
		FindAllTops(2);
		if (Information.UBound((Array)ArrayTops, 1) < 2)
		{
			return;
		}
		FindAllBottoms(3);
		int num3 = Information.UBound((Array)ArrayBottoms, 1);
		if (num3 < 3)
		{
			return;
		}
		int num4 = num3;
		checked
		{
			int num9 = default(int);
			for (int i = 0; i <= num4; i++)
			{
				int num5 = 1;
				int num6 = i + 1;
				int num7 = num3;
				int num8 = num6;
				while (num8 <= num7 && ArrayBottoms[num8] - ArrayBottoms[i] <= 126)
				{
					bool flag = false;
					bool flag2 = false;
					if (GlobalForm.StrictPatterns && !CheckNearness(GlobalForm.nHLC[2, ArrayBottoms[num8]], GlobalForm.nHLC[2, ArrayBottoms[i]], -1m, 0.15m))
					{
						flag2 = true;
					}
					if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[num8]], decimal.Subtract(GlobalForm.nHLC[2, ArrayBottoms[i]], 0.15m)) < 0)
					{
						flag2 = true;
					}
					if (flag2)
					{
						if ((num5 < 3) | (Math.Abs(i - num8) < 3))
						{
							break;
						}
						if ((decimal.Compare(d, 0m) != 0) | !CheckNearness(GlobalForm.nHLC[2, ArrayBottoms[num]], GlobalForm.nHLC[2, ArrayBottoms[num2]], -1m, priceVary))
						{
							flag = true;
						}
						if (flag)
						{
							break;
						}
						if (CheckNearness(GlobalForm.nHLC[2, ArrayBottoms[num8]], GlobalForm.nHLC[2, ArrayBottoms[i]], -1m, 0.15m))
						{
							num2 = num8;
						}
						goto IL_01d6;
					}
					if (CheckNearness(GlobalForm.nHLC[2, ArrayBottoms[num8]], GlobalForm.nHLC[2, ArrayBottoms[i]], -1m, 0.15m))
					{
						if (num5 == 1)
						{
							num = i;
							d = GlobalForm.nHLC[2, ArrayBottoms[i]];
						}
						if (decimal.Compare(d, GlobalForm.nHLC[2, ArrayBottoms[num8]]) >= 0)
						{
							d = default(decimal);
						}
						else if (decimal.Compare(d, 0m) != 0)
						{
							d = GlobalForm.nHLC[2, ArrayBottoms[num8]];
						}
						num5++;
						if (num5 == 3)
						{
							num9 = ArrayBottoms[num];
							int num10 = ArrayBottoms[num];
							int num11 = ArrayBottoms[num8];
							for (int j = num10; j <= num11; j++)
							{
								if (decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, num9]) > 0)
								{
									num9 = j;
								}
							}
							if (num8 == num3)
							{
								num2 = num8;
								goto IL_01d6;
							}
						}
						else if (num5 > 3)
						{
							int num12 = ArrayBottoms[num8 - 1];
							int num13 = ArrayBottoms[num8];
							int j = num12;
							while (j <= num13)
							{
								if (decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, num9]) < 0)
								{
									j++;
									continue;
								}
								goto IL_01d6;
							}
						}
						num2 = num8;
					}
					else if (num5 >= 3)
					{
						int num14 = ArrayBottoms[num8 - 1];
						int num15 = ArrayBottoms[num8];
						int j = num14;
						while (j <= num15)
						{
							if (decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, num9]) < 0)
							{
								j++;
								continue;
							}
							goto IL_01d6;
						}
						if (decimal.Compare(d, GlobalForm.nHLC[2, ArrayBottoms[num8]]) >= 0)
						{
							d = default(decimal);
						}
						else if (decimal.Compare(d, 0m) != 0)
						{
							d = GlobalForm.nHLC[2, ArrayBottoms[num8]];
						}
					}
					num8++;
					continue;
					IL_01d6:
					num9 = 0;
					int num16 = 0;
					int num17 = (int)Math.Round((double)(ArrayBottoms[num] + ArrayBottoms[num2]) / 2.0);
					int num18 = Information.UBound((Array)ArrayTops, 1);
					for (int j = 0; j <= num18; j++)
					{
						if ((ArrayTops[j] >= ArrayBottoms[num]) & (ArrayTops[j] <= ArrayBottoms[num2]))
						{
							if ((num9 == 0) | (decimal.Compare(GlobalForm.nHLC[1, num9], GlobalForm.nHLC[1, ArrayTops[j]]) <= 0))
							{
								num9 = ArrayTops[j];
							}
							if (ArrayTops[j] > num17 && ((num16 == 0) | (decimal.Compare(GlobalForm.nHLC[1, num16], GlobalForm.nHLC[1, ArrayTops[j]]) <= 0)))
							{
								num16 = ArrayTops[j];
							}
						}
						else if (ArrayTops[j] > ArrayBottoms[num2])
						{
							break;
						}
					}
					if (unchecked(num9 == 0 || num16 == 0))
					{
						flag = true;
					}
					if (!flag)
					{
						int num19 = Convert.ToInt32(decimal.Add(new decimal(ArrayBottoms[num]), decimal.Multiply(new decimal(ArrayBottoms[num2] - ArrayBottoms[num]), 0.3m)));
						if (((num9 <= num19) | (Math.Abs(num9 - num19) < 2)) && !FinalDesTriTests(num9, num16, 2, num, num2, 0.15m) && !TriangleWhiteSpaceCheck(num9, num16, ArrayBottoms[num], ArrayBottoms[num2], 88))
						{
							AddPattern(ArrayBottoms[num], 0, ArrayBottoms[num2], num9, 0, num16, 88, "DesT");
							i = num8;
						}
					}
					break;
				}
			}
		}
	}

	private static void FindDoubleBottoms(int Flag)
	{
		FindAllBottoms(4);
		int num = Information.UBound((Array)ArrayBottoms, 1);
		if (num < 2)
		{
			return;
		}
		FindAllTops(2);
		if (Information.UBound((Array)ArrayTops, 1) == 0)
		{
			return;
		}
		int num2 = num;
		checked
		{
			for (int i = 0; i <= num2; i++)
			{
				int num3 = i + 1;
				int num4 = num;
				for (int j = num3; j <= num4 && ArrayBottoms[j] - ArrayBottoms[i] <= 126; j++)
				{
					if (!CheckNearness(GlobalForm.nHLC[2, ArrayBottoms[j]], GlobalForm.nHLC[2, ArrayBottoms[i]], 0.5m, -1m) || CheckDBDownTrend(i, j, 0.2m, Flag))
					{
						continue;
					}
					int num5 = CheckConfirmation(ArrayBottoms[i] + 1, ArrayBottoms[j] - 1, -1);
					if (!unchecked(num5 == 1 || num5 == 0))
					{
						continue;
					}
					bool flag = false;
					string text;
					switch (Flag)
					{
					case 98:
						text = Conversions.ToString(Interaction.IIf(num5 == 1, (object)"DB", (object)"DB?"));
						break;
					case 115:
						text = Conversions.ToString(Interaction.IIf(num5 == 1, (object)"BigW", (object)"BigW?"));
						break;
					default:
						flag = CheckBottomWidth(Flag, ArrayBottoms[i], ArrayBottoms[j]);
						text = Flag switch
						{
							20 => "AADB", 
							21 => "AEDB", 
							18 => "EADB", 
							19 => "EEDB", 
							_ => "?", 
						};
						if ((num5 == 0) & (Operators.CompareString(text, "?", false) != 0))
						{
							text += "?";
						}
						break;
					}
					if (!flag)
					{
						AddPattern(ArrayBottoms[i], 0, ArrayBottoms[j], 0, 0, 0, Flag, text);
					}
				}
			}
		}
	}

	private static bool CheckBottomWidth(int Flag, int iFirstBottom, int iSecondBottom)
	{
		decimal d = default(decimal);
		int num = 0;
		int num8;
		int num11;
		checked
		{
			int num2 = iFirstBottom - 21;
			if (num2 < 0)
			{
				num2 = 0;
			}
			int num3 = num2;
			for (int i = iFirstBottom; i >= num3; i += -1)
			{
				d = decimal.Add(d, decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]));
				num++;
			}
			d = decimal.Divide(d, new decimal(num));
			int num4 = Convert.ToInt32(decimal.Multiply(0.33m, new decimal(iSecondBottom - iFirstBottom)));
			decimal d2 = decimal.Add(Math.Max(GlobalForm.nHLC[2, iFirstBottom], GlobalForm.nHLC[2, iSecondBottom]), decimal.Multiply(d, 0.45m));
			if (!FindSpike(-1, iFirstBottom, d))
			{
				num = 0;
				int num5 = iFirstBottom - num4;
				num5 = Conversions.ToInteger(Interaction.IIf(num5 < 0, (object)0, (object)num5));
				int num6 = num5;
				int num7 = iFirstBottom + num4;
				for (int i = num6; i <= num7; i++)
				{
					num += Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], d2) <= 0, (object)1, (object)0));
				}
				num8 = num;
			}
			else
			{
				num8 = 1;
			}
			d2 = decimal.Add(GlobalForm.nHLC[2, iSecondBottom], decimal.Multiply(d, 0.45m));
			if (!FindSpike(-1, iSecondBottom, d))
			{
				num = 0;
				num2 = iSecondBottom + num4;
				num2 = Conversions.ToInteger(Interaction.IIf(num2 > GlobalForm.HLCRange, (object)GlobalForm.HLCRange, (object)num2));
				int num9 = iSecondBottom - num4;
				int num10 = num2;
				for (int i = num9; i <= num10; i++)
				{
					num += Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], d2) <= 0, (object)1, (object)0));
				}
				num11 = num;
			}
			else
			{
				num11 = 1;
			}
		}
		return Flag switch
		{
			20 => Conversions.ToBoolean(Interaction.IIf(num8 <= 3 && num11 <= 3, (object)false, (object)true)), 
			21 => Conversions.ToBoolean(Interaction.IIf(num8 <= 3 && num11 > 3, (object)false, (object)true)), 
			19 => Conversions.ToBoolean(Interaction.IIf(num8 > 3 && num11 > 3, (object)false, (object)true)), 
			18 => Conversions.ToBoolean(Interaction.IIf(num8 > 3 && num11 <= 3, (object)false, (object)true)), 
			_ => true, 
		};
	}

	private static bool FindSpike(int iType, int iBottomTop, decimal AvgHeight)
	{
		checked
		{
			int num = iBottomTop - 2;
			if (num < 0)
			{
				num = 0;
			}
			int num2 = iBottomTop + 2;
			if (num2 > GlobalForm.HLCRange)
			{
				num2 = GlobalForm.HLCRange;
			}
			decimal num3 = default(decimal);
			decimal d;
			if (iType == -1)
			{
				int num4 = num;
				int num5 = num2;
				for (int i = num4; i <= num5; i++)
				{
					if (i != iBottomTop)
					{
						if (decimal.Compare(num3, 0m) == 0)
						{
							num3 = GlobalForm.nHLC[2, i];
						}
						num3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], num3) < 0, (object)GlobalForm.nHLC[2, i], (object)num3));
					}
				}
				d = decimal.Subtract(num3, GlobalForm.nHLC[2, iBottomTop]);
			}
			else
			{
				int num6 = num;
				int num7 = num2;
				for (int j = num6; j <= num7; j++)
				{
					if (j != iBottomTop)
					{
						if (decimal.Compare(num3, 0m) == 0)
						{
							num3 = GlobalForm.nHLC[1, j];
						}
						num3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, j], num3) > 0, (object)GlobalForm.nHLC[1, j], (object)num3));
					}
				}
				d = decimal.Subtract(GlobalForm.nHLC[1, iBottomTop], num3);
			}
			return decimal.Compare(d, decimal.Multiply(AvgHeight, 0.5m)) > 0;
		}
	}

	private static void FindDoubleTops(int Flag)
	{
		FindAllTops(5);
		int num = Information.UBound((Array)ArrayTops, 1);
		if (num < 2)
		{
			return;
		}
		FindAllBottoms(2);
		if (Information.UBound((Array)ArrayBottoms, 1) < 1)
		{
			return;
		}
		int num2 = num;
		checked
		{
			for (int i = 0; i <= num2; i++)
			{
				int num3 = i + 1;
				int num4 = num;
				for (int j = num3; j <= num4 && ArrayTops[j] - ArrayTops[i] <= 126; j++)
				{
					if (!CheckNearness(GlobalForm.nHLC[1, ArrayTops[i]], GlobalForm.nHLC[1, ArrayTops[j]], 0.5m, -1m) || CheckDTUpTrend(i, j, 0.2m, Flag))
					{
						continue;
					}
					int num5 = CheckConfirmation(ArrayTops[i] + 1, ArrayTops[j] - 1, 1);
					if (!unchecked(num5 == 0 || num5 == -1))
					{
						continue;
					}
					bool flag = false;
					string text;
					switch (Flag)
					{
					case 97:
						text = Conversions.ToString(Interaction.IIf(num5 == -1, (object)"DT", (object)"DT?"));
						break;
					case 116:
						text = Conversions.ToString(Interaction.IIf(num5 == -1, (object)"BigM", (object)"BigM?"));
						break;
					default:
						flag = CheckTopWidth(Flag, ArrayTops[i], ArrayTops[j]);
						text = Flag switch
						{
							16 => "AADT", 
							17 => "AEDT", 
							14 => "EADT", 
							15 => "EEDT", 
							_ => "?", 
						};
						if ((num5 == 0) & (Operators.CompareString(text, "?", false) != 0))
						{
							text += "?";
						}
						break;
					}
					if (!flag)
					{
						AddPattern(ArrayTops[i], 0, ArrayTops[j], 0, 0, 0, Flag, text);
					}
				}
			}
		}
	}

	private static bool CheckTopWidth(int Flag, int iFirstTop, int iSecondTop)
	{
		decimal d = default(decimal);
		int num = 0;
		int num8;
		int num11;
		checked
		{
			int num2 = iFirstTop - 21;
			if (num2 < 0)
			{
				num2 = 0;
			}
			int num3 = num2;
			for (int i = iFirstTop; i >= num3; i += -1)
			{
				d = decimal.Add(d, decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]));
				num++;
			}
			d = decimal.Divide(d, new decimal(num));
			int num4 = Convert.ToInt32(decimal.Multiply(0.33m, new decimal(iSecondTop - iFirstTop)));
			decimal d2 = decimal.Subtract(GlobalForm.nHLC[1, iFirstTop], decimal.Multiply(d, 0.45m));
			if (!FindSpike(1, iFirstTop, d))
			{
				num = 0;
				int num5 = iFirstTop - num4;
				num5 = Conversions.ToInteger(Interaction.IIf(num5 < 0, (object)0, (object)num5));
				int num6 = num5;
				int num7 = iFirstTop + num4;
				for (int i = num6; i <= num7; i++)
				{
					num += Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], d2) >= 0, (object)1, (object)0));
				}
				num8 = num;
			}
			else
			{
				num8 = 1;
			}
			d2 = decimal.Subtract(GlobalForm.nHLC[1, iSecondTop], decimal.Multiply(d, 0.45m));
			if (!FindSpike(1, iSecondTop, d))
			{
				num = 0;
				num2 = iSecondTop + num4;
				num2 = Conversions.ToInteger(Interaction.IIf(num2 > GlobalForm.HLCRange, (object)GlobalForm.HLCRange, (object)num2));
				int num9 = iSecondTop - num4;
				int num10 = num2;
				for (int i = num9; i <= num10; i++)
				{
					num += Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], d2) >= 0, (object)1, (object)0));
				}
				num11 = num;
			}
			else
			{
				num11 = 1;
			}
		}
		return Flag switch
		{
			16 => Conversions.ToBoolean(Interaction.IIf(num8 <= 3 && num11 <= 3, (object)false, (object)true)), 
			17 => Conversions.ToBoolean(Interaction.IIf(num8 <= 3 && num11 > 3, (object)false, (object)true)), 
			15 => Conversions.ToBoolean(Interaction.IIf(num8 > 3 && num11 > 3, (object)false, (object)true)), 
			14 => Conversions.ToBoolean(Interaction.IIf(num8 > 3 && num11 <= 3, (object)false, (object)true)), 
			_ => true, 
		};
	}

	private static bool FindDualHead(int LSIndex, int RSIndex, int i, int z, decimal Symmetry)
	{
		bool result = false;
		checked
		{
			int num = i + 1;
			int num2 = z - 1;
			for (int j = num; j <= num2; j++)
			{
				if (ArrayBottoms[j] == HeadIndex || !CheckNearness(GlobalForm.nHLC[2, HeadIndex], GlobalForm.nHLC[2, ArrayBottoms[j]], -1m, 0.1m))
				{
					continue;
				}
				int num3 = Conversions.ToInteger(Interaction.IIf(HeadIndex < ArrayBottoms[j], (object)HeadIndex, (object)ArrayBottoms[j]));
				int num4 = Conversions.ToInteger(Interaction.IIf(HeadIndex < ArrayBottoms[j], (object)ArrayBottoms[j], (object)HeadIndex));
				HeadIndex = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, num3], GlobalForm.nHLC[2, num4]) < 0, (object)num3, (object)num4));
				if ((double)(num4 - num3) > (double)(RSIndex - LSIndex) / 2.0)
				{
					return true;
				}
				int num5 = RSIndex - num4;
				int num6 = num3 - LSIndex;
				if (num6 < num5)
				{
					num5 = num3 - LSIndex;
					num6 = RSIndex - num4;
				}
				if (num5 == 0)
				{
					result = true;
					break;
				}
				if ((double)num6 / (double)num5 > Convert.ToDouble(Symmetry))
				{
					result = true;
					break;
				}
				Head2Index = Conversions.ToInteger(Interaction.IIf(HeadIndex != num3, (object)num3, (object)num4));
				for (int k = i; k <= z; k++)
				{
					if (((ArrayBottoms[k] != Head2Index) & (ArrayBottoms[k] != HeadIndex)) && ((decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[k]], GlobalForm.nHLC[2, HeadIndex]) <= 0) | (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[k]], GlobalForm.nHLC[2, Head2Index]) <= 0)))
					{
						Head2Index = 0;
						break;
					}
				}
				break;
			}
			if (Head2Index == 0 && NotSymmetrical)
			{
				result = true;
			}
			NotSymmetrical = false;
			return result;
		}
	}

	private static void FindFakey(int Flag)
	{
		int chartStartIndex = GlobalForm.ChartStartIndex;
		checked
		{
			int num = GlobalForm.ChartEndIndex - 3;
			for (int i = chartStartIndex; i <= num; i++)
			{
				if (!((decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i + 1]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i + 1]) < 0)))
				{
					continue;
				}
				bool flag = false;
				int num2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i + 2]) < 0, (object)i, (object)(i + 2)));
				num2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, num2], GlobalForm.nHLC[2, i + 3]) < 0, (object)num2, (object)(i + 3)));
				int num3 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i + 2]) > 0, (object)i, (object)(i + 2)));
				num3 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, num3], GlobalForm.nHLC[1, i + 3]) > 0, (object)num3, (object)(i + 3)));
				if (Flag == 12)
				{
					if (!((decimal.Compare(GlobalForm.nHLC[1, i + 3], GlobalForm.nHLC[1, i + 2]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i + 3], GlobalForm.nHLC[2, i + 2]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i + 2], GlobalForm.nHLC[2, i]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, i + 2], GlobalForm.nHLC[1, i]) > 0)))
					{
						continue;
					}
					int num4 = i + 4;
					int hLCRange = GlobalForm.HLCRange;
					for (int j = num4; j <= hLCRange; j++)
					{
						if (decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, num3]) > 0)
						{
							flag = true;
							break;
						}
						if (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num2]) < 0)
						{
							break;
						}
					}
					if (!flag)
					{
						AddPattern(i, 0, i + 3, 0, 0, 0, 12, "FakeBe");
					}
				}
				else
				{
					if (!((decimal.Compare(GlobalForm.nHLC[2, i + 3], GlobalForm.nHLC[2, i + 2]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, i + 3], GlobalForm.nHLC[1, i + 2]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, i + 2], GlobalForm.nHLC[1, i]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i + 2], GlobalForm.nHLC[2, i]) < 0)))
					{
						continue;
					}
					int num5 = i + 4;
					int hLCRange2 = GlobalForm.HLCRange;
					for (int k = num5; k <= hLCRange2 && decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, num3]) <= 0; k++)
					{
						if (decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num2]) < 0)
						{
							flag = true;
							break;
						}
					}
					if (!flag)
					{
						AddPattern(i, 0, i + 3, 0, 0, 0, 13, "FakeBu");
					}
				}
			}
		}
	}

	private static void FindFlatBase()
	{
		//IL_0010: Unknown result type (might be due to invalid IL or missing references)
		//IL_001b: Expected O, but got Unknown
		//IL_0056: Unknown result type (might be due to invalid IL or missing references)
		//IL_01d8: Unknown result type (might be due to invalid IL or missing references)
		GlobalForm.DisplayFmtns[] array = null;
		int num = 0;
		if (_0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag_0024Init == null)
		{
			Interlocked.CompareExchange(ref _0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag_0024Init, new StaticLocalInitFlag(), null);
		}
		bool lockTaken = false;
		try
		{
			Monitor.Enter(_0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag_0024Init, ref lockTaken);
			if (_0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag_0024Init.State == 0)
			{
				_0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag_0024Init.State = 2;
				_0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag = false;
			}
			else if (_0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag_0024Init.State == 2)
			{
				throw new IncompleteInitialization();
			}
		}
		finally
		{
			_0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag_0024Init.State = 1;
			if (lockTaken)
			{
				Monitor.Exit(_0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag_0024Init);
			}
		}
		FindRectangles(102);
		checked
		{
			while (true)
			{
				if (GlobalForm.PatternCount > 0)
				{
					int num2 = GlobalForm.PatternCount - 1;
					for (int i = 0; i <= num2; i++)
					{
						if (GlobalForm.ChartPatterns[i].iEndDate - GlobalForm.ChartPatterns[i].iStartDate >= 63)
						{
							array = (GlobalForm.DisplayFmtns[])Utils.CopyArray((Array)array, (Array)new GlobalForm.DisplayFmtns[num + 1]);
							array[num].iStartDate = GlobalForm.ChartPatterns[i].iStartDate;
							array[num].iMidDate = GlobalForm.ChartPatterns[i].iMidDate;
							array[num].iEndDate = GlobalForm.ChartPatterns[i].iEndDate;
							array[num].Type = 102;
							array[num].iText = "Flat";
							array[num].iStart2Date = GlobalForm.ChartPatterns[i].iStart2Date;
							array[num].iMidDate = GlobalForm.ChartPatterns[i].iMidDate;
							array[num].iEnd2Date = GlobalForm.ChartPatterns[i].iEnd2Date;
							num++;
						}
					}
					GlobalForm.ChartPatterns = null;
					GlobalForm.PatternCount = 0;
					if (num > 0)
					{
						GlobalForm.ChartPatterns = new GlobalForm.DisplayFmtns[num + 1];
						MessageBox.Show("This next statement should be checked to be sure it correctly copies the array from cp to chartpatterns");
						Array.Copy(array, GlobalForm.ChartPatterns, num);
						GlobalForm.PatternCount = num;
					}
				}
				if (_0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag)
				{
					break;
				}
				_0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag = true;
				FindRectangles(101);
			}
			_0024STATIC_0024FindFlatBase_0024001_0024RecursionFlag = false;
		}
	}

	private static void FindFlags()
	{
		decimal d = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.075m, (object)0.15m));
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				int num2 = (((decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i]) < 0)) ? 1 : (((decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i]) > 0)) ? (-1) : 0));
				int num3 = i;
				switch (num2)
				{
				case 1:
				{
					int num9 = i;
					int chartEndIndex3 = GlobalForm.ChartEndIndex;
					for (int j = num9; j <= chartEndIndex3 && ((decimal.Compare(GlobalForm.nHLC[1, j - 1], GlobalForm.nHLC[1, j]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, j - 1], GlobalForm.nHLC[2, j]) < 0)); j++)
					{
						num3 = j;
					}
					if (num3 - i + 1 < 3)
					{
						break;
					}
					decimal num10 = default(decimal);
					int num11 = i;
					int num12 = num3;
					for (int j = num11; j <= num12; j++)
					{
						if (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[1, j - 1]) > 0)
						{
							num10 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(decimal.Subtract(GlobalForm.nHLC[2, j], GlobalForm.nHLC[1, j - 1]), num10) > 0, (object)decimal.Subtract(GlobalForm.nHLC[2, j], GlobalForm.nHLC[1, j - 1]), (object)num10));
						}
					}
					if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num3], GlobalForm.nHLC[2, i - 1]), 0m) == 0)
					{
						break;
					}
					if (decimal.Compare(decimal.Divide(num10, decimal.Subtract(GlobalForm.nHLC[1, num3], GlobalForm.nHLC[2, i - 1])), d) < 0)
					{
						int num8 = FindFlagPortion(i - 1, num3, num2);
						if (num8 != -1)
						{
							AddPattern(i - 1, num3, num8, 0, 0, 0, 78, "Flag");
						}
					}
					else
					{
						i = num3;
					}
					break;
				}
				case -1:
				{
					int num4 = i;
					int chartEndIndex2 = GlobalForm.ChartEndIndex;
					for (int j = num4; j <= chartEndIndex2 && ((decimal.Compare(GlobalForm.nHLC[1, j - 1], GlobalForm.nHLC[1, j]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, j - 1], GlobalForm.nHLC[2, j]) > 0)); j++)
					{
						num3 = j;
					}
					if (num3 - i + 1 < 3)
					{
						break;
					}
					decimal num5 = default(decimal);
					int num6 = i;
					int num7 = num3;
					for (int j = num6; j <= num7; j++)
					{
						if (decimal.Compare(GlobalForm.nHLC[2, j - 1], GlobalForm.nHLC[1, j]) > 0)
						{
							num5 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(decimal.Subtract(GlobalForm.nHLC[2, j - 1], GlobalForm.nHLC[1, j]), num5) > 0, (object)decimal.Subtract(GlobalForm.nHLC[2, j - 1], GlobalForm.nHLC[1, j]), (object)num5));
						}
					}
					if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[2, num3]), 0m) == 0)
					{
						break;
					}
					if (decimal.Compare(decimal.Divide(num5, decimal.Subtract(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[2, num3])), d) < 0)
					{
						int num8 = FindFlagPortion(i - 1, num3, num2);
						if (num8 != -1)
						{
							AddPattern(i - 1, num3, num8, 0, 0, 0, 78, "Flag");
						}
					}
					else
					{
						i = num3;
					}
					break;
				}
				}
			}
		}
	}

	private static int FindFlagPortion(int iPoleStart, int iPoleEnd, int TrendDirection)
	{
		FindAllTops(2);
		int num = Information.UBound((Array)ArrayTops, 1);
		if (num == 0)
		{
			return -1;
		}
		if (ArrayTops[num] < iPoleEnd)
		{
			return -1;
		}
		int num2 = -1;
		int num3 = num;
		checked
		{
			float num4 = default(float);
			for (int i = 0; i <= num3; i++)
			{
				if (ArrayTops[i] > iPoleEnd)
				{
					if (ArrayTops[i] - iPoleEnd > 15)
					{
						return -1;
					}
					num4 = Convert.ToSingle(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iPoleEnd], GlobalForm.nHLC[1, ArrayTops[i]]), new decimal(iPoleEnd - ArrayTops[i])));
					num2 = ArrayTops[i];
					break;
				}
			}
			if (num2 == -1)
			{
				return -1;
			}
			decimal d = ((TrendDirection != 1) ? decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iPoleStart], GlobalForm.nHLC[2, iPoleEnd]), 3m) : decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iPoleEnd], GlobalForm.nHLC[2, iPoleStart]), 3m));
			int num5 = iPoleEnd + 15;
			if (num5 > GlobalForm.HLCRange)
			{
				num5 = GlobalForm.HLCRange;
			}
			if (num5 - iPoleEnd < 3)
			{
				return -1;
			}
			int num6 = num2 + 1;
			int num7 = num5;
			for (int i = num6; i <= num7; i++)
			{
				float num8 = num4 * (float)(i - iPoleEnd) + Convert.ToSingle(GlobalForm.nHLC[1, iPoleEnd]);
				if (Convert.ToSingle(GlobalForm.nHLC[1, i]) > num8)
				{
					num2 = i - 1;
					break;
				}
				if (i == iPoleEnd + 15)
				{
					num2 = iPoleEnd + 15;
				}
			}
			int num9 = iPoleEnd + 1;
			int num10 = iPoleEnd + 1;
			int num11 = iPoleEnd + 2;
			int num12 = num2;
			for (int i = num11; i <= num12; i++)
			{
				num9 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num9]) > 0, (object)i, (object)num9));
				num10 = Conversions.ToInteger(Interaction.IIf((decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num10]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i], 0m) > 0), (object)i, (object)num10));
			}
			if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num9], GlobalForm.nHLC[2, num10]), d) > 0)
			{
				return -1;
			}
			if (TrendDirection == 1)
			{
				if (decimal.Compare(GlobalForm.nHLC[2, num10], decimal.Subtract(GlobalForm.nHLC[1, iPoleEnd], d)) < 0)
				{
					return -1;
				}
			}
			else if (decimal.Compare(GlobalForm.nHLC[1, num9], decimal.Add(GlobalForm.nHLC[2, iPoleEnd], d)) > 0)
			{
				return -1;
			}
			int num13 = (int)Math.Round((double)(iPoleEnd + num2) / 2.0);
			int num14 = iPoleEnd + 1;
			int num15 = num2;
			decimal num17 = default(decimal);
			decimal num18 = default(decimal);
			for (int i = num14; i <= num15; i++)
			{
				decimal num16 = decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]);
				if (i < num13)
				{
					num17 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num16, num17) > 0, (object)num16, (object)num17));
				}
				else
				{
					num18 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num16, num17) > 0, (object)num16, (object)num18));
				}
			}
			if (!CheckNearness(num17, num18, 15m, -1m))
			{
				return -1;
			}
			return num2;
		}
	}

	private static void FindGap2H()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 2;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[1, i - 2]), GlobalForm.GapSize) >= 0 && ((decimal.Compare(GlobalForm.nHLC[1, i - 2], GlobalForm.nHLC[2, i - 1]) < 0) & ((decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i - 1]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i - 1]) > 0)) & (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[1, i - 1]) < 0)))
				{
					AddPattern(i - 2, 0, i, 0, 0, 0, 122, "2H");
				}
			}
		}
	}

	private static void FindGap2HInv()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 2;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[2, i - 2], GlobalForm.nHLC[1, i - 1]), GlobalForm.GapSize) >= 0 && ((decimal.Compare(GlobalForm.nHLC[2, i - 2], GlobalForm.nHLC[1, i - 1]) > 0) & ((decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i - 1]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i - 1]) < 0)) & (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i - 1]) > 0)))
				{
					AddPattern(i - 2, 0, i, 0, 0, 0, 123, "2Hi");
				}
			}
		}
	}

	private static void FindGartley(int Flag)
	{
		double[] array = new double[6] { 0.382, 0.5, 0.618, 0.707, 0.786, 0.886 };
		double[] array2 = new double[4] { 1.13, 1.27, 1.41, 1.618 };
		double num = Conversions.ToDouble(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.01, (object)0.03));
		FindAllTops(3);
		int num2 = Information.UBound((Array)ArrayTops, 1);
		if (Information.UBound((Array)ArrayTops, 1) < 3)
		{
			return;
		}
		FindAllBottoms(3);
		int num3 = Information.UBound((Array)ArrayBottoms, 1);
		if (num3 < 3)
		{
			return;
		}
		checked
		{
			switch (Flag)
			{
			case 28:
			{
				int num21 = num2;
				for (int i = 0; i <= num21; i++)
				{
					int num5 = ArrayTops[i];
					int num22 = num3;
					for (int j = 0; j <= num22; j++)
					{
						int num7 = ArrayBottoms[j];
						if (num7 <= num5)
						{
							continue;
						}
						int num23 = i + 1;
						int num24 = num2;
						int num10;
						int num13;
						int num16;
						for (int k = num23; k <= num24; k++)
						{
							num10 = ArrayTops[k];
							if (decimal.Compare(GlobalForm.nHLC[1, num10], GlobalForm.nHLC[1, num5]) >= 0)
							{
								break;
							}
							if (num7 >= num10 || CheckFibRetrace(num5, num7, num10, 0.618))
							{
								continue;
							}
							int num25 = k + 1;
							int num26 = num2;
							for (int l = num25; l <= num26; l++)
							{
								num13 = ArrayTops[l];
								if (num13 - num5 > 126)
								{
									break;
								}
								if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[2, num7]), 0m) == 0)
								{
									continue;
								}
								decimal value = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num13], GlobalForm.nHLC[2, num7]), decimal.Subtract(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[2, num7]));
								if (!((Convert.ToDouble(value) >= 0.786 - num) & (Convert.ToDouble(value) <= 0.786 + num)))
								{
									continue;
								}
								int num27 = j + 1;
								int num28 = num3;
								for (int m = num27; m <= num28; m++)
								{
									num16 = ArrayBottoms[m];
									if (num16 >= num13)
									{
										break;
									}
									if (num16 <= num10)
									{
										continue;
									}
									int num29 = array.Count() - 1;
									int num18 = 0;
									while (num18 <= num29)
									{
										if (CheckFibRetrace(num7, num10, num16, array[num18]))
										{
											num18++;
											continue;
										}
										goto IL_0243;
									}
									continue;
									IL_0243:
									if (CheckBat(num5, num7, num10, num16, num13, 28))
									{
										continue;
									}
									goto IL_0259;
								}
							}
							continue;
							IL_0259:
							int num30 = array2.Count() - 1;
							int num20 = 0;
							while (num20 <= num30)
							{
								if (CheckFibExtension(num10, num16, num13, array2[num20]))
								{
									num20++;
									continue;
								}
								goto IL_027e;
							}
						}
						continue;
						IL_027e:
						if ((decimal.Compare(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[1, num13]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, num7], GlobalForm.nHLC[2, num16]) < 0))
						{
							HarmonicTarget = Convert.ToDouble(GlobalForm.nHLC[2, num16]);
							AddPattern(num5, num7, num13, num10, num16, 0, 28, "Gar Be");
						}
						break;
					}
				}
				break;
			}
			case 29:
			{
				int num4 = num3;
				for (int i = 0; i <= num4; i++)
				{
					int num5 = ArrayBottoms[i];
					int num6 = num2;
					for (int j = 0; j <= num6; j++)
					{
						int num7 = ArrayTops[j];
						if (num7 <= num5)
						{
							continue;
						}
						int num8 = i + 1;
						int num9 = num3;
						int num10;
						int num13;
						int num16;
						for (int k = num8; k <= num9; k++)
						{
							num10 = ArrayBottoms[k];
							if (decimal.Compare(GlobalForm.nHLC[2, num10], GlobalForm.nHLC[2, num5]) <= 0)
							{
								break;
							}
							if (num7 >= num10 || CheckFibRetrace(num5, num7, num10, 0.618))
							{
								continue;
							}
							int num11 = k + 1;
							int num12 = num3;
							for (int l = num11; l <= num12; l++)
							{
								num13 = ArrayBottoms[l];
								if (num13 - num5 > 126)
								{
									break;
								}
								if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num5]), 0m) == 0)
								{
									continue;
								}
								decimal value = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num13]), decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num5]));
								if (!((Convert.ToDouble(value) >= 0.786 - num) & (Convert.ToDouble(value) <= 0.786 + num)))
								{
									continue;
								}
								int num14 = j + 1;
								int num15 = num2;
								for (int m = num14; m <= num15; m++)
								{
									num16 = ArrayTops[m];
									if (num16 >= num13)
									{
										break;
									}
									if (num16 <= num10)
									{
										continue;
									}
									int num17 = array.Count() - 1;
									int num18 = 0;
									while (num18 <= num17)
									{
										if (CheckFibRetrace(num7, num10, num16, array[num18]))
										{
											num18++;
											continue;
										}
										goto IL_0512;
									}
									continue;
									IL_0512:
									if (CheckBat(num5, num7, num10, num16, num13, 29))
									{
										continue;
									}
									goto IL_0528;
								}
							}
							continue;
							IL_0528:
							int num19 = array2.Count() - 1;
							int num20 = 0;
							while (num20 <= num19)
							{
								if (CheckFibExtension(num10, num16, num13, array2[num20]))
								{
									num20++;
									continue;
								}
								goto IL_054d;
							}
						}
						continue;
						IL_054d:
						if ((decimal.Compare(GlobalForm.nHLC[2, num5], GlobalForm.nHLC[2, num13]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[1, num16]) > 0))
						{
							HarmonicTarget = Convert.ToDouble(GlobalForm.nHLC[1, num16]);
							AddPattern(num5, num7, num13, num10, num16, 0, 29, "Gar Bu");
						}
						break;
					}
				}
				break;
			}
			}
		}
	}

	private static void FindHCR()
	{
		int chartStartIndex = GlobalForm.ChartStartIndex;
		checked
		{
			int num = GlobalForm.ChartEndIndex - 1;
			decimal d3 = default(decimal);
			for (int i = chartStartIndex; i <= num; i++)
			{
				int num2 = Conversions.ToInteger(Interaction.IIf(i + 10 < GlobalForm.HLCRange, (object)(i + 10), (object)(GlobalForm.HLCRange - 1)));
				int num3 = 0;
				int num4 = i;
				int num5 = num2;
				for (int j = num4; j <= num5; j++)
				{
					decimal d = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, j + 1]) > 0, (object)GlobalForm.nHLC[1, j], (object)GlobalForm.nHLC[1, j + 1]));
					decimal d2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, j + 1]) < 0, (object)GlobalForm.nHLC[2, j], (object)GlobalForm.nHLC[2, j + 1]));
					decimal num6 = decimal.Subtract(d, d2);
					if (decimal.Compare(num6, 0m) > 0)
					{
						d3 = default(decimal);
						if ((decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, j + 1]) <= 0) & (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, j + 1]) <= 0) & (decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[2, j + 1]) >= 0))
						{
							d3 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, j], GlobalForm.nHLC[2, j + 1]), num6);
						}
						else if ((decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, j + 1]) >= 0) & (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, j + 1]) >= 0) & (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[1, j + 1]) <= 0))
						{
							d3 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, j + 1], GlobalForm.nHLC[2, j]), num6);
						}
						else if ((decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, j + 1]) >= 0) & (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, j + 1]) <= 0))
						{
							d3 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, j + 1], GlobalForm.nHLC[2, j + 1]), num6);
						}
						else if ((decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, j + 1]) <= 0) & (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, j + 1]) >= 0))
						{
							d3 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, j], GlobalForm.nHLC[2, j]), num6);
						}
					}
					if (decimal.Compare(d3, 0.55m) >= 0)
					{
						num3++;
					}
				}
				if (num3 >= 4)
				{
					decimal d4 = decimal.Divide(decimal.Add(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 2m);
					decimal d5 = decimal.Divide(decimal.Add(GlobalForm.nHLC[1, num2], GlobalForm.nHLC[2, num2]), 2m);
					decimal d6 = default(decimal);
					if (num2 - i != 0)
					{
						d6 = decimal.Divide(Math.Abs(decimal.Subtract(d5, d4)), new decimal(num2 - i));
					}
					if (decimal.Compare(d6, 0.03m) <= 0)
					{
						AddPattern(i, 0, num2, i, 0, num2, 102, "HCR");
						i = num2;
					}
				}
			}
		}
	}

	private static void FindHeadShouldersBottom(int Flag)
	{
		decimal headShoulder = Conversions.ToDecimal(Interaction.IIf(Flag == 94, (object)0.25m, (object)0.15m));
		iRS2 = 0;
		FindAllBottoms(3);
		int num = Information.UBound((Array)ArrayBottoms, 1);
		if (num < 3)
		{
			return;
		}
		FindAllTops(2);
		int num2 = Information.UBound((Array)ArrayTops, 1);
		if (num2 < 2)
		{
			return;
		}
		int num3 = num;
		checked
		{
			for (int i = 1; i <= num3; i++)
			{
				HeadIndex = ArrayBottoms[i];
				for (int j = i - 1; j >= 0; j += -1)
				{
					int num4 = ArrayBottoms[j];
					if (decimal.Compare(GlobalForm.nHLC[2, num4], GlobalForm.nHLC[2, HeadIndex]) <= 0)
					{
						break;
					}
					int num5 = i + 1;
					int num6 = num;
					int k;
					int num7;
					int num10;
					for (k = num5; k <= num6; k++)
					{
						num7 = ArrayBottoms[k];
						if (decimal.Compare(GlobalForm.nHLC[2, num7], GlobalForm.nHLC[2, HeadIndex]) <= 0)
						{
							break;
						}
						int num8 = j + 1;
						int num9 = k - 1;
						for (int l = num8; l <= num9; l++)
						{
							if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[l]], GlobalForm.nHLC[2, HeadIndex]) < 0)
							{
								goto end_IL_036d;
							}
						}
						if (FindHSB(num4, num7, headShoulder))
						{
							continue;
						}
						if (num7 - num4 > 126)
						{
							break;
						}
						if (CheckShoulderDistance(Flag, num4, num7) || FindBottomArmpit(num4, HeadIndex, num2))
						{
							continue;
						}
						decimal armPit = ArmPit;
						if (FindBottomArmpit(HeadIndex, num7, num2))
						{
							continue;
						}
						armPit = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(ArmPit, armPit) > 0, (object)ArmPit, (object)armPit));
						if (FindPriceTrend(num4, armPit) || (Flag == 94 && CheckHSBSlope(num4, num7, j, i, k, Flag)) || CheckLongNeck(num4, num7, armPit, Flag))
						{
							continue;
						}
						Head2Index = 0;
						iLS2 = 0;
						iRS2 = 0;
						if (Flag == 93)
						{
							if (FindDualHead(num4, num7, j, k, 1.5m) || CheckHSBSlope(num4, num7, j, i, k, Flag))
							{
								continue;
							}
							FindBottomOuterShoulders(num4, num7, j, k, num, 1.5m, headShoulder);
							if ((Head2Index == 0) & (iRS2 == 0) & (iLS2 == 0))
							{
								continue;
							}
							if (CheckLongNeck(num4, num7, armPit, Flag))
							{
								goto end_IL_036d;
							}
							num10 = ((iRS2 == 0) ? CheckConfirmation(HeadIndex, num7, -1) : CheckConfirmation(HeadIndex, iRS2, -1));
						}
						else
						{
							num10 = CheckConfirmation(HeadIndex, num7, -1);
						}
						if (num10 == -1)
						{
							goto end_IL_036d;
						}
						goto IL_02d2;
					}
					continue;
					IL_02d2:
					if (Flag == 94)
					{
						if (!ConfirmHSB(k, ArmPit))
						{
							AddPattern(num4, HeadIndex, num7, iLS2, Head2Index, iRS2, Flag, Conversions.ToString(Interaction.IIf(num10 == 0, (object)"HSB?", (object)"HSB")));
						}
					}
					else
					{
						AddPattern(num4, HeadIndex, num7, iLS2, Head2Index, iRS2, Flag, Conversions.ToString(Interaction.IIf(num10 == 0, (object)"cHSB?", (object)"cHSB")));
					}
					break;
					continue;
					end_IL_036d:
					break;
				}
			}
		}
	}

	private static void FindHeadShouldersTop(int Flag)
	{
		decimal headShoulder = Conversions.ToDecimal(Interaction.IIf(Flag == 107, (object)0.25m, (object)0.15m));
		iRS2 = 0;
		FindAllBottoms(2);
		int num = Information.UBound((Array)ArrayBottoms, 1);
		if (num < 2)
		{
			return;
		}
		FindAllTops(Conversions.ToInteger(Interaction.IIf(Flag == 107, (object)3, (object)5)));
		int num2 = Information.UBound((Array)ArrayTops, 1);
		if (num2 < 3)
		{
			return;
		}
		int num3 = num2;
		checked
		{
			for (int i = 1; i <= num3; i++)
			{
				HeadIndex = ArrayTops[i];
				for (int j = i - 1; j >= 0; j += -1)
				{
					int num4 = ArrayTops[j];
					if (decimal.Compare(GlobalForm.nHLC[1, num4], GlobalForm.nHLC[1, HeadIndex]) > 0)
					{
						break;
					}
					int num5 = i + 1;
					int num6 = num2;
					int k;
					int num7;
					int num10;
					for (k = num5; k <= num6; k++)
					{
						num7 = ArrayTops[k];
						if (decimal.Compare(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[1, HeadIndex]) > 0)
						{
							break;
						}
						int num8 = j + 1;
						int num9 = k - 1;
						for (int l = num8; l <= num9; l++)
						{
							if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[l]], GlobalForm.nHLC[1, HeadIndex]) > 0)
							{
								goto end_IL_037e;
							}
						}
						if (FindHST(num4, num7, headShoulder))
						{
							continue;
						}
						if (num7 - num4 > 126)
						{
							break;
						}
						if (CheckTopShoulderDistance(Flag, num4, num7))
						{
							continue;
						}
						int headIndex = HeadIndex;
						if (FindTopArmpit(num4, headIndex, num))
						{
							continue;
						}
						decimal armPit = ArmPit;
						int headIndex2 = HeadIndex;
						headIndex = num7;
						if (FindTopArmpit(headIndex2, headIndex, num))
						{
							continue;
						}
						armPit = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(ArmPit, armPit) < 0, (object)ArmPit, (object)armPit));
						if (FindTopPriceTrend(num4, armPit) || (Flag == 107 && CheckTopSlope(num4, num7, j, i, k, Flag)) || CheckTopLongNeck(num4, num7, armPit, Flag))
						{
							continue;
						}
						Head2Index = 0;
						iLS2 = 0;
						iRS2 = 0;
						if (Flag == 108)
						{
							if (FindTopDualHead(num4, num7, j, k, 1.5m) || CheckTopSlope(num4, num7, j, i, k, Flag))
							{
								continue;
							}
							FindTopOuterShoulders(num4, num7, j, k, num2, 1.5m, headShoulder);
							if ((Head2Index == 0) & (iRS2 == 0) & (iLS2 == 0))
							{
								continue;
							}
							num10 = ((iRS2 == 0) ? CheckConfirmation(HeadIndex, num7, 1) : CheckConfirmation(HeadIndex, iRS2, 1));
						}
						else
						{
							num10 = CheckConfirmation(HeadIndex, num7, 1);
						}
						if (num10 == 1)
						{
							goto end_IL_037e;
						}
						goto IL_02e3;
					}
					continue;
					IL_02e3:
					if (Flag == 107)
					{
						if (!ConfirmHST(k, ArmPit))
						{
							AddPattern(num4, HeadIndex, num7, iLS2, Head2Index, iRS2, Flag, Conversions.ToString(Interaction.IIf(num10 == 0, (object)"HST?", (object)"HST")));
						}
					}
					else
					{
						AddPattern(num4, HeadIndex, num7, iLS2, Head2Index, iRS2, Flag, Conversions.ToString(Interaction.IIf(num10 == 0, (object)"cHST?", (object)"cHST")));
					}
					break;
					continue;
					end_IL_037e:
					break;
				}
			}
		}
	}

	private static bool FindHSB(int LSIndex, int RSIndex, decimal HeadShoulder)
	{
		if (GlobalForm.StrictPatterns)
		{
			if (!CheckNearness(GlobalForm.nHLC[2, LSIndex], GlobalForm.nHLC[2, RSIndex], 1m, 0.4m))
			{
				return true;
			}
			if (CheckNearness(GlobalForm.nHLC[2, RSIndex], GlobalForm.nHLC[2, HeadIndex], -1m, HeadShoulder))
			{
				return true;
			}
			if (CheckNearness(GlobalForm.nHLC[2, LSIndex], GlobalForm.nHLC[2, HeadIndex], -1m, HeadShoulder))
			{
				return true;
			}
		}
		else
		{
			if (!CheckNearness(GlobalForm.nHLC[2, LSIndex], GlobalForm.nHLC[2, RSIndex], 0.5m, Conversions.ToDecimal(Interaction.IIf(checked(RSIndex - LSIndex) >= 42, (object)0.6000000000000001, (object)0.4m))))
			{
				return true;
			}
			if (CheckNearness(GlobalForm.nHLC[2, RSIndex], GlobalForm.nHLC[2, HeadIndex], 0.5m, HeadShoulder))
			{
				return true;
			}
			if (CheckNearness(GlobalForm.nHLC[2, LSIndex], GlobalForm.nHLC[2, HeadIndex], 0.5m, HeadShoulder))
			{
				return true;
			}
		}
		return false;
	}

	private static bool FindHST(int LSIndex, int RSIndex, decimal HeadShoulder)
	{
		if (GlobalForm.StrictPatterns)
		{
			if (!CheckNearness(GlobalForm.nHLC[1, LSIndex], GlobalForm.nHLC[1, RSIndex], 1m, 0.4m))
			{
				return true;
			}
			if (CheckNearness(GlobalForm.nHLC[1, HeadIndex], GlobalForm.nHLC[1, RSIndex], -1m, HeadShoulder))
			{
				return true;
			}
			if (CheckNearness(GlobalForm.nHLC[1, HeadIndex], GlobalForm.nHLC[1, LSIndex], -1m, HeadShoulder))
			{
				return true;
			}
		}
		else
		{
			if (!CheckNearness(GlobalForm.nHLC[1, LSIndex], GlobalForm.nHLC[1, RSIndex], 0.5m, Conversions.ToDecimal(Interaction.IIf(checked(RSIndex - LSIndex) >= 42, (object)0.6000000000000001, (object)0.4m))))
			{
				return true;
			}
			if (CheckNearness(GlobalForm.nHLC[1, HeadIndex], GlobalForm.nHLC[1, RSIndex], 0.5m, HeadShoulder))
			{
				return true;
			}
			if (CheckNearness(GlobalForm.nHLC[1, HeadIndex], GlobalForm.nHLC[1, LSIndex], 0.5m, HeadShoulder))
			{
				return true;
			}
		}
		return false;
	}

	public static void FindHookRevD()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				decimal d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.25m);
				if (((decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i]) > 0)) && decimal.Compare(GlobalForm.nHLC[0, i], decimal.Add(GlobalForm.nHLC[2, i], d)) < 0 && decimal.Compare(GlobalForm.nHLC[3, i], decimal.Subtract(GlobalForm.nHLC[1, i], d)) > 0 && HLRegression(i - 2, 2, 5) == -1)
				{
					AddPattern(i - 1, 0, i, 0, 0, 0, 50, "HD");
				}
			}
		}
	}

	public static void FindHookRevU()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				decimal d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.25m);
				if (((decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i]) > 0)) && decimal.Compare(GlobalForm.nHLC[0, i], decimal.Subtract(GlobalForm.nHLC[1, i], d)) > 0 && decimal.Compare(GlobalForm.nHLC[3, i], decimal.Add(GlobalForm.nHLC[2, i], d)) < 0 && HLRegression(i - 2, 2, 5) == 1)
				{
					AddPattern(i - 1, 0, i, 0, 0, 0, 49, "HU");
				}
			}
		}
	}

	public static void FindHornBottoms()
	{
		decimal d = 1.02m;
		if (GlobalForm.IntradayData)
		{
			d = 1.0004m;
		}
		int chartStartIndex = GlobalForm.ChartStartIndex;
		checked
		{
			int num = GlobalForm.ChartEndIndex - 4;
			for (int i = chartStartIndex; i <= num; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[2, i], decimal.Multiply(d, GlobalForm.nHLC[2, i + 1])) <= 0 || decimal.Compare(GlobalForm.nHLC[2, i + 2], decimal.Multiply(d, GlobalForm.nHLC[2, i + 1])) <= 0 || decimal.Compare(GlobalForm.nHLC[2, i + 2], decimal.Multiply(d, GlobalForm.nHLC[2, i + 3])) <= 0 || decimal.Compare(GlobalForm.nHLC[2, i + 4], decimal.Multiply(d, GlobalForm.nHLC[2, i + 3])) <= 0 || decimal.Compare(GlobalForm.nHLC[2, i], decimal.Multiply(d, GlobalForm.nHLC[2, i + 3])) <= 0 || decimal.Compare(GlobalForm.nHLC[2, i + 4], decimal.Multiply(d, GlobalForm.nHLC[2, i + 1])) <= 0)
				{
					continue;
				}
				decimal d2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i + 1], GlobalForm.nHLC[2, i + 3]) < 0, (object)GlobalForm.nHLC[2, i + 1], (object)GlobalForm.nHLC[2, i + 3]));
				decimal d3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i + 1], GlobalForm.nHLC[2, i + 3]) < 0, (object)GlobalForm.nHLC[2, i + 3], (object)GlobalForm.nHLC[2, i + 1]));
				decimal num2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[1, i + 3]) < 0, (object)GlobalForm.nHLC[1, i + 1], (object)GlobalForm.nHLC[1, i + 3]));
				Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[1, i + 3]) < 0, (object)GlobalForm.nHLC[1, i + 3], (object)GlobalForm.nHLC[1, i + 1]));
				decimal num3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i + 2]) < 0, (object)GlobalForm.nHLC[2, i], (object)GlobalForm.nHLC[2, i + 2]));
				num3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num3, GlobalForm.nHLC[2, i + 4]) < 0, (object)num3, (object)GlobalForm.nHLC[2, i + 4]));
				num2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num3, num2) < 0, (object)num3, (object)num2));
				if (decimal.Compare(decimal.Subtract(num2, d2), 0m) > 0 && decimal.Compare(decimal.Divide(Math.Abs(decimal.Subtract(d3, num2)), decimal.Subtract(num2, d2)), 0.5m) >= 0)
				{
					switch (CheckConfirmation(i + 1, i + 3, -1))
					{
					case 1:
						AddPattern(i + 1, 0, i + 3, 0, 0, 0, 106, "HB");
						break;
					case 0:
						AddPattern(i + 1, 0, i + 3, 0, 0, 0, 106, "HB?");
						break;
					}
				}
			}
		}
	}

	public static void FindHornTops()
	{
		decimal d = 0.98m;
		if (GlobalForm.IntradayData)
		{
			d = 0.9996m;
		}
		int chartStartIndex = GlobalForm.ChartStartIndex;
		checked
		{
			int num = GlobalForm.ChartEndIndex - 4;
			for (int i = chartStartIndex; i <= num; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[1, i], decimal.Multiply(d, GlobalForm.nHLC[1, i + 1])) >= 0 || decimal.Compare(GlobalForm.nHLC[1, i + 2], decimal.Multiply(d, GlobalForm.nHLC[1, i + 1])) >= 0 || decimal.Compare(GlobalForm.nHLC[1, i + 2], decimal.Multiply(d, GlobalForm.nHLC[1, i + 3])) >= 0 || decimal.Compare(GlobalForm.nHLC[1, i + 4], decimal.Multiply(d, GlobalForm.nHLC[1, i + 3])) >= 0 || decimal.Compare(GlobalForm.nHLC[1, i], decimal.Multiply(d, GlobalForm.nHLC[1, i + 3])) >= 0 || decimal.Compare(GlobalForm.nHLC[1, i + 4], decimal.Multiply(d, GlobalForm.nHLC[1, i + 1])) >= 0)
				{
					continue;
				}
				decimal d2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[1, i + 3]) > 0, (object)GlobalForm.nHLC[1, i + 1], (object)GlobalForm.nHLC[1, i + 3]));
				decimal d3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[1, i + 3]) > 0, (object)GlobalForm.nHLC[1, i + 3], (object)GlobalForm.nHLC[1, i + 1]));
				decimal num2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i + 1], GlobalForm.nHLC[2, i + 3]) > 0, (object)GlobalForm.nHLC[2, i + 1], (object)GlobalForm.nHLC[2, i + 3]));
				Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i + 1], GlobalForm.nHLC[2, i + 3]) > 0, (object)GlobalForm.nHLC[2, i + 3], (object)GlobalForm.nHLC[2, i + 1]));
				decimal num3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i + 2]) > 0, (object)GlobalForm.nHLC[1, i], (object)GlobalForm.nHLC[1, i + 2]));
				num3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num3, GlobalForm.nHLC[1, i + 4]) > 0, (object)num3, (object)GlobalForm.nHLC[1, i + 4]));
				num2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num3, num2) > 0, (object)num3, (object)num2));
				if (decimal.Compare(decimal.Subtract(d2, num2), 0m) > 0 && decimal.Compare(decimal.Divide(decimal.Subtract(d3, num2), decimal.Subtract(d2, num2)), 0.5m) >= 0)
				{
					switch (CheckConfirmation(i + 1, i + 3, 1))
					{
					case -1:
						AddPattern(i + 1, 0, i + 3, 0, 0, 0, 105, "HT");
						break;
					case 0:
						AddPattern(i + 1, 0, i + 3, 0, 0, 0, 105, "HT?");
						break;
					}
				}
			}
		}
	}

	private static void FindHTFlag()
	{
		int num = GlobalForm.ChartPeriodShown switch
		{
			1 => 8, 
			2 => 2, 
			_ => 42, 
		};
		if (GlobalForm.ChartEndIndex < num)
		{
			num = GlobalForm.ChartEndIndex;
		}
		int chartStartIndex = GlobalForm.ChartStartIndex;
		int chartEndIndex = GlobalForm.ChartEndIndex;
		checked
		{
			int num2;
			int num6 = default(int);
			for (num2 = chartStartIndex; num2 <= chartEndIndex; num2++)
			{
				int num3 = -1;
				int num4 = num2 + num;
				if (num4 > GlobalForm.ChartEndIndex)
				{
					num4 = GlobalForm.ChartEndIndex;
				}
				int num5 = num2;
				do
				{
					if (num3 == -1)
					{
						num3 = num5;
						num6 = num5;
					}
					if (((decimal.Compare(GlobalForm.nHLC[2, num5], GlobalForm.nHLC[2, num3]) <= 0) & (decimal.Compare(GlobalForm.nHLC[2, num5], 0m) != 0)) | (decimal.Compare(GlobalForm.nHLC[2, num3], 0m) == 0))
					{
						num3 = num5;
						num6 = num5;
						num4 = num5 + num;
						if (num4 > GlobalForm.ChartEndIndex)
						{
							num4 = GlobalForm.ChartEndIndex;
						}
					}
					while (true)
					{
						if (decimal.Compare(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[1, num6]) > 0)
						{
							num6 = num5;
						}
						if (decimal.Compare(GlobalForm.nHLC[2, num3], 0m) == 0 || decimal.Compare(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num6], GlobalForm.nHLC[2, num3]), GlobalForm.nHLC[2, num3]), 0.9m) < 0 || num6 == num3)
						{
							break;
						}
						if (num5 + 1 <= GlobalForm.ChartEndIndex && decimal.Compare(GlobalForm.nHLC[1, num5 + 1], GlobalForm.nHLC[1, num6]) > 0)
						{
							num5++;
							continue;
						}
						if (DateAndTime.DateDiff((DateInterval)2, GlobalForm.nDT[0, num3], GlobalForm.nDT[0, num6], (FirstDayOfWeek)1, (FirstWeekOfYear)1) <= 2)
						{
							AddPattern(num3, 0, num6, 0, 0, 0, 95, "HTF");
						}
						num3 = ((num5 > num4) ? num6 : (num6 + 1));
						break;
					}
					if (num5 != GlobalForm.ChartEndIndex)
					{
						num5++;
						continue;
					}
					return;
				}
				while (num5 <= num4);
				num2 = num3;
			}
		}
	}

	private static void FindDivingBoard()
	{
		if (TrendLines(-1, 0, 264, 0.7m, 5, Special: true) <= 0)
		{
			return;
		}
		int num = Information.UBound((Array)TLArray, 2);
		checked
		{
			for (int i = 0; i <= num; i++)
			{
				if (TLArray[1, i] - TLArray[0, i] < 66)
				{
					continue;
				}
				int num2 = TLArray[0, i];
				int num3 = TLArray[1, i];
				int num4 = num3 + 1;
				int hLCRange = GlobalForm.HLCRange;
				for (int j = num4; j <= hLCRange; j++)
				{
					if (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num3]) < 0)
					{
						num3 = j - 1;
						break;
					}
				}
				if (num3 - num2 > 264)
				{
					continue;
				}
				int num5 = Convert.ToInt32(decimal.Multiply(0.5m, new decimal(num3 - num2)));
				int num6 = num2;
				int num7 = num2;
				int num8 = num2 + 1;
				int num9 = num3;
				for (int j = num8; j <= num9; j++)
				{
					num6 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, num6]) > 0, (object)j, (object)num6));
					num7 = Conversions.ToInteger(Interaction.IIf((decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num7]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, j], 0m) > 0), (object)j, (object)num7));
				}
				if (decimal.Compare(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num6], GlobalForm.nHLC[2, num7]), GlobalForm.nHLC[1, num6]), 0.15m) > 0)
				{
					continue;
				}
				decimal d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, num6], GlobalForm.nHLC[2, num7]), 0.075m);
				int num10 = num3 + 1;
				int num11 = num3 + 22;
				for (int j = num10; j <= num11 && j + 1 <= GlobalForm.HLCRange; j++)
				{
					if (decimal.Compare(GlobalForm.nHLC[1, j], decimal.Subtract(GlobalForm.nHLC[2, num7], d)) >= 0)
					{
						continue;
					}
					int num12 = j + 1;
					int hLCRange2 = GlobalForm.HLCRange;
					int num13 = num12;
					while (num13 <= hLCRange2)
					{
						if (decimal.Compare(GlobalForm.nHLC[1, num13], GlobalForm.nHLC[2, num7]) < 0)
						{
							num13++;
							continue;
						}
						goto IL_027a;
					}
					if (GlobalForm.HLCRange - num2 < 126)
					{
						AddPattern(num2, num3, GlobalForm.HLCRange, 0, 0, 0, 30, "Diving board?");
					}
					continue;
					IL_027a:
					int num14 = j;
					int num15 = j;
					int num16 = num13;
					int k;
					for (k = num15; k <= num16; k++)
					{
						num14 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num14]) < 0, (object)k, (object)num14));
					}
					if (num14 - num3 > num3 - num2 || num13 - num14 > num5)
					{
						break;
					}
					int num17 = num14 + 1;
					int hLCRange3 = GlobalForm.HLCRange;
					k = num17;
					while (true)
					{
						if (k <= hLCRange3)
						{
							if (decimal.Compare(GlobalForm.nHLC[3, k], GlobalForm.nHLC[1, num6]) > 0)
							{
								AddPattern(num2, num3, num13, 0, num14, 0, 30, "Diving board");
								break;
							}
							if (decimal.Compare(GlobalForm.nHLC[3, k], GlobalForm.nHLC[2, num14]) < 0)
							{
								break;
							}
							k++;
							continue;
						}
						AddPattern(num2, num3, num13, 0, num14, 0, 30, "Diving board?");
						break;
					}
					break;
				}
			}
		}
	}

	private static void FindIDCB()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[3, i - 1], 0m) > 0)
				{
					int num2 = Convert.ToInt32(decimal.Divide(decimal.Multiply(100m, decimal.Subtract(GlobalForm.nHLC[3, i], GlobalForm.nHLC[3, i - 1])), GlobalForm.nHLC[3, i - 1]));
					if (num2 >= GlobalForm.pfPctRise)
					{
						AddPattern(i - 1, 0, i, 0, 0, 0, 99, "iDCB\r\n" + Strings.Format((object)((double)num2 / 100.0), "0%"));
					}
				}
			}
		}
	}

	private static void FindInsideDay()
	{
		int chartStartIndex = GlobalForm.ChartStartIndex;
		checked
		{
			int num = GlobalForm.ChartEndIndex - 1;
			for (int i = chartStartIndex; i <= num; i++)
			{
				if ((decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i + 1]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i + 1]) < 0))
				{
					AddPattern(i, 0, i + 1, 0, 0, 0, 77, "ID");
				}
			}
		}
	}

	private static void FindIslands()
	{
		object[,] array = new object[4, 1];
		int num = 0;
		checked
		{
			int num2 = GlobalForm.ChartStartIndex + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			int num3 = default(int);
			for (int i = num2; i <= chartEndIndex; i++)
			{
				decimal d = default(decimal);
				if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i - 1]) < 0)
				{
					d = decimal.Subtract(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[1, i]);
					num3 = -1;
				}
				else if (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[1, i - 1]) > 0)
				{
					d = decimal.Subtract(GlobalForm.nHLC[2, i], GlobalForm.nHLC[1, i - 1]);
					num3 = 1;
				}
				if (decimal.Compare(d, GlobalForm.GapSize) >= 0)
				{
					array = (object[,])Utils.CopyArray((Array)array, (Array)new object[4, num + 1]);
					switch (num3)
					{
					case 1:
						array[0, num] = GlobalForm.nHLC[1, i - 1];
						array[1, num] = GlobalForm.nHLC[2, i];
						break;
					case -1:
						array[0, num] = GlobalForm.nHLC[1, i];
						array[1, num] = GlobalForm.nHLC[2, i - 1];
						break;
					}
					array[2, num] = num3;
					array[3, num] = i - 1;
					num++;
				}
			}
			if (num <= 0)
			{
				return;
			}
			int num4 = Information.UBound((Array)array, 2);
			int num7 = default(int);
			for (int i = 0; i <= num4; i++)
			{
				int num5 = i + 1;
				int num6 = Information.UBound((Array)array, 2);
				for (num = num5; num <= num6; num++)
				{
					_ = GlobalForm.nDT[0, Conversions.ToInteger(array[3, num]) - 1];
					if (Conversions.ToInteger(array[3, num]) - Conversions.ToInteger(array[3, i]) > 126)
					{
						break;
					}
					if (Conversions.ToInteger(array[2, i]) == Conversions.ToInteger(array[2, num]) || !(((decimal.Compare(Conversions.ToDecimal(array[0, i]), Conversions.ToDecimal(array[0, num])) >= 0) & (decimal.Compare(Conversions.ToDecimal(array[0, i]), Conversions.ToDecimal(array[1, num])) <= 0)) | ((decimal.Compare(Conversions.ToDecimal(array[1, i]), Conversions.ToDecimal(array[0, num])) >= 0) & (decimal.Compare(Conversions.ToDecimal(array[1, i]), Conversions.ToDecimal(array[1, num])) <= 0))))
					{
						continue;
					}
					switch (Conversions.ToInteger(array[2, i]))
					{
					case 1:
						num7 = 75;
						break;
					case -1:
						num7 = 76;
						break;
					}
					if (GlobalForm.PatternList[num7] == 1)
					{
						string pText = "";
						switch (num7)
						{
						case 75:
							pText = "IRT";
							break;
						case 76:
							pText = "IRB";
							break;
						}
						if (IslandCheck(Conversions.ToInteger(array[3, i]), Conversions.ToInteger(array[3, num]) + 1, num7))
						{
							AddPattern(Conversions.ToInteger(array[3, i]) + 1, 0, Conversions.ToInteger(array[3, num]), 0, 0, 0, num7, pText);
						}
					}
				}
			}
		}
	}

	public static bool IslandCheck(int iFrom, int iTo, int Type)
	{
		checked
		{
			if (iTo + 1 <= GlobalForm.HLCRange)
			{
				decimal d = default(decimal);
				decimal d2 = default(decimal);
				if (Type == 75)
				{
					d = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, iFrom], GlobalForm.nHLC[1, iTo + 1]) > 0, (object)GlobalForm.nHLC[1, iFrom], (object)GlobalForm.nHLC[1, iTo + 1]));
				}
				else
				{
					d2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, iFrom], GlobalForm.nHLC[2, iTo + 1]) < 0, (object)GlobalForm.nHLC[2, iFrom], (object)GlobalForm.nHLC[2, iTo + 1]));
				}
				int num = iFrom + 2;
				int num2 = iTo - 2;
				for (int i = num; i <= num2; i++)
				{
					if (Type == 75)
					{
						if (decimal.Compare(GlobalForm.nHLC[2, i], d) < 0)
						{
							return false;
						}
					}
					else if (decimal.Compare(GlobalForm.nHLC[1, i], d2) > 0)
					{
						return false;
					}
				}
			}
			return true;
		}
	}

	private static void FindKeyRevD()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 2;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				if (((decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i]) < 0)) && decimal.Compare(GlobalForm.nHLC[0, i], GlobalForm.nHLC[3, i - 1]) < 0 && decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[1, i - 1]) > 0 && HLRegression(i - 2, 2, 5) == -1)
				{
					AddPattern(i - 1, 0, i, 0, 0, 0, 47, "KD");
				}
			}
		}
	}

	private static void FindKeyRevU()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 2;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				if (((decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i]) < 0)) && decimal.Compare(GlobalForm.nHLC[0, i], GlobalForm.nHLC[3, i - 1]) > 0 && decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[2, i - 1]) < 0 && HLRegression(i - 2, 2, 5) == 1)
				{
					AddPattern(i - 1, 0, i, 0, 0, 0, 46, "KU");
				}
			}
		}
	}

	private static void FindMMU(int PatternType)
	{
		FindAllBottoms(5);
		int num = Information.UBound((Array)ArrayBottoms, 1);
		if (num < 2)
		{
			return;
		}
		FindAllTops(5);
		int num2 = Information.UBound((Array)ArrayTops, 1);
		if (num2 <= 1)
		{
			return;
		}
		checked
		{
			if (PatternType == 73)
			{
				int num3 = num - 1;
				for (int i = 0; i <= num3; i++)
				{
					int num4 = ArrayBottoms[i];
					int num5 = ArrayBottoms[i + 1];
					if (decimal.Compare(GlobalForm.nHLC[2, num5], GlobalForm.nHLC[2, num4]) <= 0)
					{
						continue;
					}
					int num6 = num2 - 1;
					for (int j = 1; j <= num6; j++)
					{
						int num7 = ArrayTops[j];
						if (unchecked(num7 > num4 && num7 < num5) & (decimal.Compare(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[1, num5]) > 0))
						{
							if (!((ArrayTops[j - 1] < num4) & (ArrayTops[j + 1] > num5)) || !(Convert.ToSingle(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num5]), decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num4]))) > 0.7f))
							{
								continue;
							}
							int num8 = num5 + 1;
							HarmonicTarget = Convert.ToDouble(decimal.Add(decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num4]), GlobalForm.nHLC[2, num5]));
							int num9 = num5 + 1;
							int hLCRange = GlobalForm.HLCRange;
							for (int k = num9; k <= hLCRange; k++)
							{
								num8 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, num8]) > 0, (object)k, (object)num8));
								if (Convert.ToDouble(GlobalForm.nHLC[1, k]) >= HarmonicTarget || decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num5]) < 0)
								{
									break;
								}
							}
							AddPattern(num4, num7, num8, num5, 0, 0, PatternType, "MMU");
							break;
						}
						if (num7 > num5)
						{
							break;
						}
					}
				}
				return;
			}
			int num10 = num2 - 1;
			for (int i = 0; i <= num10; i++)
			{
				int num4 = ArrayTops[i];
				int num5 = ArrayTops[i + 1];
				if (decimal.Compare(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[1, num4]) >= 0)
				{
					continue;
				}
				int num11 = num - 1;
				for (int j = 1; j <= num11; j++)
				{
					int num7 = ArrayBottoms[j];
					if (unchecked(num7 > num4 && num7 < num5) & (decimal.Compare(GlobalForm.nHLC[2, num7], GlobalForm.nHLC[2, num5]) < 0))
					{
						if (!((ArrayBottoms[j - 1] < num4) & (ArrayBottoms[j + 1] > num5)) || !(Convert.ToSingle(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[2, num7]), decimal.Subtract(GlobalForm.nHLC[1, num4], GlobalForm.nHLC[2, num7]))) > 0.7f))
						{
							continue;
						}
						int num8 = num5 + 1;
						HarmonicTarget = Convert.ToDouble(decimal.Subtract(GlobalForm.nHLC[1, num5], decimal.Subtract(GlobalForm.nHLC[1, num4], GlobalForm.nHLC[2, num7])));
						int num12 = num5 + 1;
						int hLCRange2 = GlobalForm.HLCRange;
						for (int k = num12; k <= hLCRange2; k++)
						{
							num8 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num8]) < 0, (object)k, (object)num8));
							if (Convert.ToDouble(GlobalForm.nHLC[2, k]) <= HarmonicTarget || decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, num5]) > 0)
							{
								break;
							}
						}
						AddPattern(num4, num7, num8, num5, 0, 0, PatternType, "MMD");
						break;
					}
					if (num7 > num5)
					{
						break;
					}
				}
			}
		}
	}

	private static void FindNR4()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 3;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				decimal d = decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]);
				if ((decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[2, i - 1])) < 0) & (decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 2], GlobalForm.nHLC[2, i - 2])) < 0) & (decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 3], GlobalForm.nHLC[2, i - 3])) < 0))
				{
					AddPattern(i - 3, 0, i, 0, 0, 0, 72, "NR4");
				}
			}
		}
	}

	private static void FindNR7()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 6;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				decimal d = decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]);
				if ((decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[2, i - 1])) < 0) & (decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 2], GlobalForm.nHLC[2, i - 2])) < 0) & (decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 3], GlobalForm.nHLC[2, i - 3])) < 0) & (decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 4], GlobalForm.nHLC[2, i - 4])) < 0) & (decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 5], GlobalForm.nHLC[2, i - 5])) < 0) & (decimal.Compare(d, decimal.Subtract(GlobalForm.nHLC[1, i - 6], GlobalForm.nHLC[2, i - 6])) < 0))
				{
					AddPattern(i - 6, 0, i, 0, 0, 0, 71, "NR7");
				}
			}
		}
	}

	private static void FindOCRD()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 2;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				decimal d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.25m);
				if (decimal.Compare(GlobalForm.nHLC[0, i], decimal.Add(GlobalForm.nHLC[2, i], d)) < 0 && ((decimal.Compare(GlobalForm.nHLC[3, i], decimal.Subtract(GlobalForm.nHLC[1, i], d)) > 0) & (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[3, i - 1]) < 0)) && HLRegression(i - 1, 2, 5) == -1)
				{
					AddPattern(i, 0, i, 0, 0, 0, 45, "o");
				}
			}
		}
	}

	private static void FindOCRU()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 2;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				decimal d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.25m);
				if (decimal.Compare(GlobalForm.nHLC[0, i], decimal.Subtract(GlobalForm.nHLC[1, i], d)) > 0 && ((decimal.Compare(GlobalForm.nHLC[3, i], decimal.Add(GlobalForm.nHLC[2, i], d)) < 0) & (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[3, i - 1]) > 0)) && HLRegression(i - 1, 2, 5) == 1)
				{
					AddPattern(i, 0, i, 0, 0, 0, 44, "O");
				}
			}
		}
	}

	private static void FindODRB()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int num2 = GlobalForm.ChartEndIndex - 1;
			for (int i = num; i <= num2; i++)
			{
				decimal d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.25m);
				if (!((decimal.Compare(GlobalForm.nHLC[0, i], decimal.Subtract(GlobalForm.nHLC[1, i], d)) > 0) & (decimal.Compare(GlobalForm.nHLC[3, i], decimal.Subtract(GlobalForm.nHLC[1, i], d)) > 0)))
				{
					continue;
				}
				d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.5m);
				if ((decimal.Compare(GlobalForm.nHLC[2, i - 1], decimal.Subtract(GlobalForm.nHLC[1, i], d)) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i + 1], decimal.Subtract(GlobalForm.nHLC[1, i], d)) > 0))
				{
					d = FindWideRange(i - 1);
					if (((decimal.Compare(d, -1m) != 0) & (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), d) >= 0)) && HLRegression(i - 1, 2, 5) == -1)
					{
						AddPattern(i, 0, i, 0, 0, 0, 70, "r");
					}
				}
			}
		}
	}

	private static void FindODRT()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int num2 = GlobalForm.ChartEndIndex - 1;
			for (int i = num; i <= num2; i++)
			{
				decimal d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.25m);
				if (!((decimal.Compare(GlobalForm.nHLC[0, i], decimal.Add(GlobalForm.nHLC[2, i], d)) < 0) & (decimal.Compare(GlobalForm.nHLC[3, i], decimal.Add(GlobalForm.nHLC[2, i], d)) < 0)))
				{
					continue;
				}
				d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.5m);
				if ((decimal.Compare(GlobalForm.nHLC[1, i - 1], decimal.Add(GlobalForm.nHLC[2, i], d)) < 0) & (decimal.Compare(GlobalForm.nHLC[1, i + 1], decimal.Add(GlobalForm.nHLC[2, i], d)) < 0))
				{
					d = FindWideRange(i - 1);
					if (((decimal.Compare(d, -1m) != 0) & (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), d) > 0)) && HLRegression(i - 1, 2, 5) == 1)
					{
						AddPattern(i, 0, i, 0, 0, 0, 69, "R");
					}
				}
			}
		}
	}

	private static void FindOutsideDay()
	{
		int chartStartIndex = GlobalForm.ChartStartIndex;
		checked
		{
			int num = GlobalForm.ChartEndIndex - 1;
			for (int i = chartStartIndex; i <= num; i++)
			{
				if ((decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i + 1]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i + 1]) > 0))
				{
					AddPattern(i, 0, i + 1, 0, 0, 0, 68, "OD");
				}
			}
		}
	}

	private static void FindPennants()
	{
		FindAllBottoms(2);
		int num = Information.UBound((Array)ArrayBottoms, 1);
		if (num == 0)
		{
			return;
		}
		FindAllTops(2);
		int num2 = Information.UBound((Array)ArrayTops, 1);
		if (num2 == 0)
		{
			return;
		}
		int chartStartIndex = GlobalForm.ChartStartIndex;
		int chartEndIndex = GlobalForm.ChartEndIndex;
		checked
		{
			for (int i = chartStartIndex; i <= chartEndIndex; i++)
			{
				int num3 = i + 20;
				int num4 = i + 3;
				for (int j = num3; j >= num4 && j <= GlobalForm.ChartEndIndex; j += -1)
				{
					if (!PennantShape(i, j) && !PennantShape((int)Math.Round((double)i + (double)(j - i) / 2.0), j))
					{
						int num5 = PennnantTrend(i, j, num, num2);
						if (num5 != 0)
						{
							AddPattern(num5, i, j, 0, 0, 0, 67, "PEN");
							i = j;
							break;
						}
					}
				}
			}
		}
	}

	private static bool PennantShape(int iStart, int j)
	{
		decimal d = GlobalForm.nHLC[1, iStart];
		decimal d2 = GlobalForm.nHLC[2, iStart];
		checked
		{
			for (int i = iStart + 1; i <= j; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[1, i], d) >= 0)
				{
					return true;
				}
				if (decimal.Compare(GlobalForm.nHLC[2, i], d2) <= 0)
				{
					return true;
				}
			}
			return false;
		}
	}

	private static int PennnantTrend(int i, int j, int BottomSize, int TopSize)
	{
		int result = 0;
		int num = i;
		int num2 = i;
		checked
		{
			for (int k = i + 1; k <= j; k++)
			{
				num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, num]) > 0, (object)k, (object)num));
				num2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num2]) < 0, (object)k, (object)num2));
			}
			decimal d = decimal.Multiply(3m, decimal.Subtract(GlobalForm.nHLC[1, num], GlobalForm.nHLC[2, num2]));
			int num3 = BottomSize - 1;
			for (int l = 1; l <= num3; l++)
			{
				int num4 = ArrayBottoms[l];
				int num5 = TopSize - 1;
				for (int m = 1; m <= num5; m++)
				{
					int num6 = ArrayTops[m];
					if (decimal.Compare(GlobalForm.nHLC[1, num6], GlobalForm.nHLC[2, num4]) <= 0)
					{
						continue;
					}
					if (num6 < num4)
					{
						if (!((num4 == i) | (num4 == i - 1)))
						{
							continue;
						}
						int num7 = Conversions.ToInteger(Interaction.IIf(num4 < i, (object)num4, (object)(i - 1)));
						int num8 = 0;
						int num9 = num7;
						int num10 = Conversions.ToInteger(Interaction.IIf(num7 - 10 < 0, (object)0, (object)(num7 - 10)));
						for (int n = num7; n >= num10; n += -1)
						{
							if (decimal.Compare(GlobalForm.nHLC[1, n], GlobalForm.nHLC[1, num9]) <= 0)
							{
								num8++;
								if (num8 >= 3)
								{
									break;
								}
							}
							else
							{
								num9 = n;
								num8 = 0;
							}
						}
						int num11 = num9;
						int num12 = Conversions.ToInteger(Interaction.IIf(num4 < i, (object)num4, (object)(i - 1)));
						for (int n = num11; n <= num12; n++)
						{
							decimal num13 = decimal.Subtract(GlobalForm.nHLC[1, n], GlobalForm.nHLC[2, num4]);
							if (decimal.Compare(num13, d) < 0)
							{
								break;
							}
							decimal d2 = default(decimal);
							int num14 = n;
							int num15 = Conversions.ToInteger(Interaction.IIf(num4 < i, (object)num4, (object)(i - 1))) - 1;
							for (int k = num14; k <= num15; k++)
							{
								if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, k + 1], GlobalForm.nHLC[2, k]), 0m) > 0)
								{
									d2 = decimal.Subtract(decimal.Add(d2, GlobalForm.nHLC[1, k + 1]), GlobalForm.nHLC[2, k]);
								}
							}
							if (decimal.Compare(decimal.Multiply(decimal.Divide(d2, num13), 100m), 33m) < 0)
							{
								return n;
							}
						}
					}
					else
					{
						if (!((num6 == i) | (num6 == i - 1)))
						{
							continue;
						}
						int num16 = Conversions.ToInteger(Interaction.IIf(num6 < i, (object)num6, (object)(i - 1)));
						int num8 = 0;
						int num9 = num16;
						int num17 = Conversions.ToInteger(Interaction.IIf(num16 - 10 < 0, (object)0, (object)(num16 - 10)));
						for (int n = num16; n >= num17; n += -1)
						{
							if (decimal.Compare(GlobalForm.nHLC[2, n], GlobalForm.nHLC[2, num9]) >= 0)
							{
								num8++;
								if (num8 >= 3)
								{
									break;
								}
							}
							else
							{
								num9 = n;
								num8 = 0;
							}
						}
						int num18 = num9;
						int num19 = Conversions.ToInteger(Interaction.IIf(num6 < i, (object)num6, (object)(i - 1)));
						for (int n = num18; n <= num19; n++)
						{
							decimal num13 = decimal.Subtract(GlobalForm.nHLC[1, num6], GlobalForm.nHLC[2, n]);
							if (decimal.Compare(num13, d) < 0)
							{
								break;
							}
							decimal d2 = default(decimal);
							int num20 = n;
							int num21 = Conversions.ToInteger(Interaction.IIf(num6 < i, (object)num6, (object)(i - 1))) - 1;
							for (int k = num20; k <= num21; k++)
							{
								if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, k], GlobalForm.nHLC[2, k + 1]), 0m) > 0)
								{
									d2 = decimal.Subtract(decimal.Add(d2, GlobalForm.nHLC[1, k]), GlobalForm.nHLC[2, k + 1]);
								}
							}
							if (decimal.Compare(decimal.Multiply(decimal.Divide(d2, num13), 100m), 33m) < 0)
							{
								return n;
							}
						}
					}
				}
			}
			return result;
		}
	}

	public static void FindPipeBottoms()
	{
		object[,] array = new object[2, 1];
		decimal num = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)1.03, (object)1.02));
		if (GlobalForm.IntradayData)
		{
			num = 1.0004m;
		}
		array = null;
		int num2 = 0;
		int chartStartIndex = GlobalForm.ChartStartIndex;
		checked
		{
			int num3 = GlobalForm.ChartEndIndex - 3;
			for (int i = chartStartIndex; i <= num3; i++)
			{
				array = (object[,])Utils.CopyArray((Array)array, (Array)new object[2, num2 + 1 + 1]);
				array[0, num2] = RuntimeHelpers.GetObjectValue(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i + 2]) < 0, (object)GlobalForm.nHLC[2, i], (object)GlobalForm.nHLC[2, i + 2]));
				array[0, num2] = decimal.Subtract(Conversions.ToDecimal(array[0, num2]), GlobalForm.nHLC[2, i + 1]);
				if (decimal.Compare(Conversions.ToDecimal(array[0, num2]), 0m) > 0)
				{
					if (GlobalForm.IntradayData)
					{
						array[1, num2] = GlobalForm.nDT[0, i + 1];
					}
					else
					{
						array[1, num2] = GlobalForm.nDT[0, i + 1].Date;
					}
					num2++;
				}
				if (decimal.Compare(GlobalForm.nHLC[2, i], decimal.Multiply(num, GlobalForm.nHLC[2, i + 1])) <= 0 || decimal.Compare(GlobalForm.nHLC[2, i + 3], decimal.Multiply(num, GlobalForm.nHLC[2, i + 2])) <= 0 || !((decimal.Compare(decimal.Multiply(GlobalForm.nHLC[2, i + 1], num), GlobalForm.nHLC[2, i + 3]) < 0) & (decimal.Compare(decimal.Multiply(GlobalForm.nHLC[2, i + 2], num), GlobalForm.nHLC[2, i]) < 0)))
				{
					continue;
				}
				decimal d2;
				if (GlobalForm.StrictPatterns)
				{
					decimal num4 = decimal.Subtract(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[2, i + 1]);
					if (decimal.Compare(num4, decimal.Subtract(GlobalForm.nHLC[1, i + 2], GlobalForm.nHLC[2, i + 2])) < 0)
					{
						num4 = decimal.Subtract(GlobalForm.nHLC[1, i + 2], GlobalForm.nHLC[2, i + 2]);
					}
					if (decimal.Compare(num4, 0m) <= 0)
					{
						continue;
					}
					decimal d = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[1, i + 2]) > 0, (object)GlobalForm.nHLC[1, i + 2], (object)GlobalForm.nHLC[1, i + 1]));
					d2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i + 1], GlobalForm.nHLC[2, i + 2]) > 0, (object)GlobalForm.nHLC[2, i + 1], (object)GlobalForm.nHLC[2, i + 2]));
					if (decimal.Compare(decimal.Divide(decimal.Subtract(d, d2), num4), 0.5m) <= 0)
					{
						continue;
					}
				}
				else
				{
					decimal num5 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i + 3]) < 0, (object)GlobalForm.nHLC[2, i], (object)GlobalForm.nHLC[2, i + 3]));
					decimal num6 = ((decimal.Compare(GlobalForm.nHLC[1, i + 1], num5) <= 0) ? decimal.Subtract(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[2, i + 1]) : decimal.Subtract(num5, GlobalForm.nHLC[2, i + 1]));
					if (decimal.Compare(num6, 0m) <= 0)
					{
						continue;
					}
					decimal num7 = ((decimal.Compare(GlobalForm.nHLC[1, i + 2], num5) <= 0) ? decimal.Subtract(GlobalForm.nHLC[1, i + 2], GlobalForm.nHLC[2, i + 2]) : decimal.Subtract(num5, GlobalForm.nHLC[2, i + 2]));
					if (decimal.Compare(num7, 0m) <= 0)
					{
						continue;
					}
					decimal num4 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num6, num7) > 0, (object)num6, (object)num7));
					d2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i + 1], GlobalForm.nHLC[2, i + 2]) < 0, (object)GlobalForm.nHLC[2, i + 2], (object)GlobalForm.nHLC[2, i + 1]));
					decimal d = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[1, i + 2]) < 0, (object)GlobalForm.nHLC[1, i + 1], (object)GlobalForm.nHLC[1, i + 2]));
					d = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(d, num5) < 0, (object)d, (object)num5));
					if (decimal.Compare(num4, 0m) == 0 || decimal.Compare(decimal.Divide(decimal.Subtract(d, d2), num4), 0.5m) <= 0)
					{
						continue;
					}
				}
				int num8 = CheckConfirmation(i + 1, i + 2, -1);
				decimal d3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i + 3]) < 0, (object)GlobalForm.nHLC[2, i], (object)GlobalForm.nHLC[2, i + 3]));
				d3 = decimal.Subtract(d3, d2);
				if (!CheckSpikes(i, d3, num2, array))
				{
					switch (num8)
					{
					case 1:
						AddPattern(i + 1, 0, i + 2, 0, 0, 0, 104, "PB");
						break;
					case 0:
						AddPattern(i + 1, 0, i + 2, 0, 0, 0, 104, "PB?");
						break;
					}
				}
			}
		}
	}

	public static void FindPipeTops()
	{
		object[,] array = new object[2, 1];
		decimal num = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.97, (object)0.98));
		if (GlobalForm.IntradayData)
		{
			num = 0.9996m;
		}
		array = null;
		int num2 = 0;
		int chartStartIndex = GlobalForm.ChartStartIndex;
		checked
		{
			int num3 = GlobalForm.ChartEndIndex - 3;
			for (int i = chartStartIndex; i <= num3; i++)
			{
				array = (object[,])Utils.CopyArray((Array)array, (Array)new object[2, num2 + 1 + 1]);
				array[0, num2] = RuntimeHelpers.GetObjectValue(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i + 2]) > 0, (object)GlobalForm.nHLC[1, i], (object)GlobalForm.nHLC[1, i + 2]));
				array[0, num2] = decimal.Subtract(Conversions.ToDecimal(array[0, num2]), GlobalForm.nHLC[1, i + 1]);
				if (decimal.Compare(Conversions.ToDecimal(array[0, num2]), 0m) > 0)
				{
					if (GlobalForm.IntradayData)
					{
						array[1, num2] = GlobalForm.nDT[0, i + 1];
					}
					else
					{
						array[1, num2] = GlobalForm.nDT[0, i + 1].Date;
					}
					num2++;
				}
				if (decimal.Compare(GlobalForm.nHLC[1, i], decimal.Multiply(num, GlobalForm.nHLC[1, i + 1])) >= 0 || decimal.Compare(GlobalForm.nHLC[1, i + 3], decimal.Multiply(num, GlobalForm.nHLC[1, i + 2])) >= 0 || !((decimal.Compare(decimal.Multiply(GlobalForm.nHLC[1, i + 1], num), GlobalForm.nHLC[1, i + 3]) > 0) & (decimal.Compare(decimal.Multiply(GlobalForm.nHLC[1, i + 2], num), GlobalForm.nHLC[1, i]) > 0)))
				{
					continue;
				}
				decimal d;
				if (GlobalForm.StrictPatterns)
				{
					decimal num4 = decimal.Subtract(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[2, i + 1]);
					if (decimal.Compare(num4, decimal.Subtract(GlobalForm.nHLC[1, i + 2], GlobalForm.nHLC[2, i + 2])) < 0)
					{
						num4 = decimal.Subtract(GlobalForm.nHLC[1, i + 2], GlobalForm.nHLC[2, i + 2]);
					}
					if (decimal.Compare(num4, 0m) <= 0)
					{
						continue;
					}
					d = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[1, i + 2]) > 0, (object)GlobalForm.nHLC[1, i + 2], (object)GlobalForm.nHLC[1, i + 1]));
					decimal d2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i + 1], GlobalForm.nHLC[2, i + 2]) > 0, (object)GlobalForm.nHLC[2, i + 1], (object)GlobalForm.nHLC[2, i + 2]));
					if (decimal.Compare(decimal.Divide(decimal.Subtract(d, d2), num4), 0.5m) <= 0)
					{
						continue;
					}
				}
				else
				{
					decimal num5 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i + 3]) > 0, (object)GlobalForm.nHLC[1, i], (object)GlobalForm.nHLC[1, i + 3]));
					decimal num6 = ((decimal.Compare(GlobalForm.nHLC[2, i + 1], num5) >= 0) ? decimal.Subtract(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[2, i + 1]) : decimal.Subtract(GlobalForm.nHLC[1, i + 1], num5));
					if (decimal.Compare(num6, 0m) <= 0)
					{
						continue;
					}
					decimal num7 = ((decimal.Compare(GlobalForm.nHLC[2, i + 2], num5) >= 0) ? decimal.Subtract(GlobalForm.nHLC[1, i + 2], GlobalForm.nHLC[2, i + 2]) : decimal.Subtract(GlobalForm.nHLC[1, i + 2], num5));
					if (decimal.Compare(num7, 0m) <= 0)
					{
						continue;
					}
					decimal num4 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(num6, num7) > 0, (object)num6, (object)num7));
					d = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[1, i + 2]) > 0, (object)GlobalForm.nHLC[1, i + 2], (object)GlobalForm.nHLC[1, i + 1]));
					decimal d2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i + 1], GlobalForm.nHLC[2, i + 2]) > 0, (object)GlobalForm.nHLC[2, i + 1], (object)GlobalForm.nHLC[2, i + 2]));
					d2 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(d2, num5) > 0, (object)d2, (object)num5));
					if (decimal.Compare(num4, 0m) == 0 || decimal.Compare(decimal.Divide(decimal.Subtract(d, d2), num4), 0.5m) <= 0)
					{
						continue;
					}
				}
				int num8 = CheckConfirmation(i + 1, i + 2, 1);
				decimal d3 = Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i + 3]) > 0, (object)GlobalForm.nHLC[1, i], (object)GlobalForm.nHLC[1, i + 3]));
				d3 = decimal.Subtract(d, d3);
				if (!CheckSpikesT(i, d3, num2, array))
				{
					switch (num8)
					{
					case -1:
						AddPattern(i + 1, 0, i + 2, 0, 0, 0, 103, "PT");
						break;
					case 0:
						AddPattern(i + 1, 0, i + 2, 0, 0, 0, 103, "PT?");
						break;
					}
				}
			}
		}
	}

	private static void FindPivotD()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 2;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[1, i - 1]) > 0 && decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i - 2]) < 0 && HLRegression(i - 1, 2, 5) == -1)
				{
					AddPattern(i, 0, i, 0, 0, 0, 43, "p");
				}
			}
		}
	}

	private static void FindPivotU()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 2;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[2, i - 1]) < 0 && HLRegression(i - 1, 2, 5) == 1)
				{
					AddPattern(i, 0, i, 0, 0, 0, 42, "P");
				}
			}
		}
	}

	private static bool FindPriceTrend(int LSIndex, decimal ArmPitHigh)
	{
		checked
		{
			for (int i = LSIndex - 1; i >= 0 && decimal.Compare(GlobalForm.nHLC[2, i], ArmPitHigh) <= 0; i += -1)
			{
				if (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, LSIndex]) < 0)
				{
					return true;
				}
			}
			return false;
		}
	}

	public static void FindPothole()
	{
		if (TrendLines(-1, 0, 66, 0.375m, 3, Special: false) <= 0)
		{
			return;
		}
		int num = Information.UBound((Array)TLArray, 2);
		checked
		{
			for (int i = 0; i <= num; i++)
			{
				int num2 = TLArray[1, i] - TLArray[0, i];
				if (!unchecked(num2 >= 22 && num2 <= 66))
				{
					continue;
				}
				int num3 = TLArray[0, i];
				int num4 = TLArray[1, i];
				int num5 = num4 + 1;
				int hLCRange = GlobalForm.HLCRange;
				for (int j = num5; j <= hLCRange; j++)
				{
					if (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num4]) < 0)
					{
						num4 = j - 1;
						break;
					}
				}
				if (num4 - num3 > 66)
				{
					continue;
				}
				int num6 = Convert.ToInt32(decimal.Multiply(2.5m, new decimal(num4 - num3)));
				int num7 = num3;
				int num8 = num3;
				int num9 = num3 + 1;
				int num10 = num4;
				for (int j = num9; j <= num10; j++)
				{
					num7 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, num7]) > 0, (object)j, (object)num7));
					num8 = Conversions.ToInteger(Interaction.IIf((decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num8]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, j], 0m) > 0), (object)j, (object)num8));
				}
				if (decimal.Compare(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num8]), GlobalForm.nHLC[1, num7]), 0.05m) > 0)
				{
					continue;
				}
				decimal d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, num7], GlobalForm.nHLC[2, num8]), 0.075m);
				int num11 = num4 + 1;
				int num12 = num4 + 22;
				for (int j = num11; j <= num12 && j + 1 <= GlobalForm.HLCRange; j++)
				{
					if (decimal.Compare(GlobalForm.nHLC[1, j], decimal.Subtract(GlobalForm.nHLC[2, num8], d)) >= 0)
					{
						continue;
					}
					int num13 = j + 1;
					int hLCRange2 = GlobalForm.HLCRange;
					int num14 = num13;
					while (num14 <= hLCRange2)
					{
						if (decimal.Compare(GlobalForm.nHLC[1, num14], GlobalForm.nHLC[2, num8]) < 0)
						{
							num14++;
							continue;
						}
						goto IL_028f;
					}
					if (GlobalForm.HLCRange - num3 < 126)
					{
						AddPattern(num3, num4, GlobalForm.HLCRange, 0, 0, 0, 37, "Pothole?");
						return;
					}
					continue;
					IL_028f:
					int num15 = j;
					int num16 = j;
					int num17 = num14;
					int k;
					for (k = num16; k <= num17; k++)
					{
						num15 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num15]) < 0, (object)k, (object)num15));
					}
					if (num15 - num4 > num4 - num3 || num14 - num15 > num6)
					{
						break;
					}
					int num18 = num15 + 1;
					int hLCRange3 = GlobalForm.HLCRange;
					k = num18;
					while (true)
					{
						if (k <= hLCRange3)
						{
							if (decimal.Compare(GlobalForm.nHLC[3, k], GlobalForm.nHLC[1, num7]) > 0)
							{
								AddPattern(num3, num4, num14, 0, num15, 0, 37, "Pothole");
								break;
							}
							if (decimal.Compare(GlobalForm.nHLC[3, k], GlobalForm.nHLC[2, num15]) < 0)
							{
								break;
							}
							k++;
							continue;
						}
						AddPattern(num3, num4, num14, 0, num15, 0, 37, "Pothole?");
						break;
					}
					break;
				}
			}
		}
	}

	public static void FindRectangles(int PatternType)
	{
		int[,] array = new int[3, 1];
		string pText = Conversions.ToString(Interaction.IIf(PatternType == 101, (object)"RT", (object)"RB"));
		int num = TrendLines(-1, 0, 126, 0.25m, 3, Conversions.ToBoolean(Interaction.IIf(GlobalForm.StrictPatterns, (object)true, (object)false)));
		checked
		{
			if (num > 0)
			{
				array = new int[3, Information.UBound((Array)TLArray, 2) + 1];
				int num2 = 0;
				int num3 = Information.UBound((Array)TLArray, 2);
				for (num = 0; num <= num3; num++)
				{
					if (decimal.Compare(Math.Abs(TLSlopeArray[num]), 0.007m) <= 0)
					{
						array[0, num2] = TLArray[0, num];
						array[1, num2] = TLArray[1, num];
						array[2, num2] = TLArray[2, num];
						num2++;
					}
				}
				if (num2 <= 0)
				{
					return;
				}
				array = (int[,])Utils.CopyArray((Array)array, (Array)new int[3, num2 - 1 + 1]);
				num = TrendLines(1, 0, 126, 0.25m, 3, Conversions.ToBoolean(Interaction.IIf(GlobalForm.StrictPatterns, (object)true, (object)false)));
				if (num > 0)
				{
					int num4 = Information.UBound((Array)array, 2);
					for (num = 0; num <= num4; num++)
					{
						int num5 = Information.UBound((Array)TLArray, 2);
						for (num2 = 0; num2 <= num5; num2++)
						{
							if (decimal.Compare(Math.Abs(TLSlopeArray[num2]), 0.007m) > 0)
							{
								continue;
							}
							int TStart = TLArray[0, num2];
							int TEnd = TLArray[1, num2];
							int BStart = array[0, num];
							int BEnd = array[1, num];
							int num6 = TEnd - TStart;
							int num7 = BEnd - BStart;
							num6 = Conversions.ToInteger(Interaction.IIf(num6 < num7, (object)num7, (object)num6));
							num6 = Convert.ToInt32(decimal.Multiply(new decimal(num6), 0.57m));
							if (unchecked(BStart >= TStart && BEnd <= TEnd))
							{
								if (decimal.Compare(new decimal(BEnd - BStart), decimal.Multiply(new decimal(TEnd - TStart), 0.57m)) >= 0 && FRVerify(PatternType, TLArray[0, num2], TLArray[1, num2], TStart, BStart, TEnd, BEnd))
								{
									CheckLineExtensions(ref TStart, ref TEnd, ref BStart, ref BEnd);
									if (!CheckTouches(TStart, TEnd, BStart, BEnd))
									{
										ExtendLines(ref TStart, ref TEnd, ref BStart, ref BEnd);
										AddPattern(TStart, 0, TEnd, BStart, 0, BEnd, PatternType, pText);
										break;
									}
								}
							}
							else if (unchecked(BStart <= TStart && BEnd >= TEnd))
							{
								if (decimal.Compare(new decimal(TEnd - TStart), decimal.Multiply(new decimal(BEnd - BStart), 0.57m)) >= 0 && FRVerify(PatternType, array[0, num], array[1, num], TStart, BStart, TEnd, BEnd))
								{
									CheckLineExtensions(ref TStart, ref TEnd, ref BStart, ref BEnd);
									if (!CheckTouches(TStart, TEnd, BStart, BEnd))
									{
										ExtendLines(ref TStart, ref TEnd, ref BStart, ref BEnd);
										AddPattern(TStart, 0, TEnd, BStart, 0, BEnd, PatternType, pText);
										break;
									}
								}
							}
							else if (unchecked(BStart >= TStart && BEnd >= TEnd && BStart < TEnd))
							{
								if (TEnd - BStart > num6 && FRVerify(PatternType, TLArray[0, num2], array[1, num], TStart, BStart, TEnd, BEnd))
								{
									CheckLineExtensions(ref TStart, ref TEnd, ref BStart, ref BEnd);
									if (!CheckTouches(TStart, TEnd, BStart, BEnd))
									{
										ExtendLines(ref TStart, ref TEnd, ref BStart, ref BEnd);
										AddPattern(TStart, 0, TEnd, BStart, 0, BEnd, PatternType, pText);
										break;
									}
								}
							}
							else if (unchecked(BStart <= TStart && BEnd <= TEnd && BEnd > TStart) && BEnd - TStart > num6 && FRVerify(PatternType, array[0, num], TLArray[1, num2], TStart, BStart, TEnd, BEnd))
							{
								CheckLineExtensions(ref TStart, ref TEnd, ref BStart, ref BEnd);
								if (!CheckTouches(TStart, TEnd, BStart, BEnd))
								{
									ExtendLines(ref TStart, ref TEnd, ref BStart, ref BEnd);
									AddPattern(TStart, 0, TEnd, BStart, 0, BEnd, PatternType, pText);
									break;
								}
							}
						}
					}
				}
			}
			array = null;
			TLArray = null;
		}
	}

	private static void CheckLineExtensions(ref int TStart, ref int TEnd, ref int BStart, ref int BEnd)
	{
		int num = TStart;
		checked
		{
			int num2 = TStart + 1;
			int num3 = TEnd;
			for (int i = num2; i <= num3; i++)
			{
				num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0, (object)i, (object)num));
			}
			int num4 = BStart;
			int num5 = BStart + 1;
			int num6 = BEnd;
			for (int i = num5; i <= num6; i++)
			{
				num4 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num4]) < 0, (object)i, (object)num4));
			}
			decimal d;
			if (decimal.Compare(GlobalForm.nHLC[1, num], 5m) < 0)
			{
				decimal priceScale = GetPriceScale(GlobalForm.nHLC[1, num], GlobalForm.nHLC[1, num]);
				d = decimal.Multiply(0.25m, priceScale);
			}
			else
			{
				d = 0.25m;
			}
			if (TStart < BStart)
			{
				int num7 = BStart;
				int num8 = TStart;
				for (int i = num7; i >= num8; i += -1)
				{
					if (decimal.Compare(decimal.Add(GlobalForm.nHLC[2, i], d), GlobalForm.nHLC[2, num4]) < 0)
					{
						TStart = i + 1;
						return;
					}
				}
			}
			else if (TStart > BStart)
			{
				int num9 = TStart;
				int num10 = BStart;
				for (int i = num9; i >= num10; i += -1)
				{
					if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i], d), GlobalForm.nHLC[1, num]) > 0)
					{
						BStart = i + 1;
						return;
					}
				}
			}
			if (TEnd < BEnd)
			{
				int num11 = TEnd;
				int num12 = BEnd;
				for (int i = num11; i <= num12; i++)
				{
					if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i], d), GlobalForm.nHLC[1, num]) > 0)
					{
						BEnd = i - 1;
						break;
					}
				}
			}
			else
			{
				if (TEnd <= BEnd)
				{
					return;
				}
				int num13 = BEnd;
				int num14 = TEnd;
				for (int i = num13; i <= num14; i++)
				{
					if (decimal.Compare(decimal.Add(GlobalForm.nHLC[2, i], d), GlobalForm.nHLC[2, num4]) < 0)
					{
						TEnd = i - 1;
						break;
					}
				}
			}
		}
	}

	private static void ExtendLines(ref int TStart, ref int TEnd, ref int BStart, ref int BEnd)
	{
		int num = TStart;
		checked
		{
			int num2 = TStart + 1;
			int num3 = TEnd;
			for (int i = num2; i <= num3; i++)
			{
				num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0, (object)i, (object)num));
			}
			int num4 = BStart;
			int num5 = BStart + 1;
			int num6 = BEnd;
			for (int i = num5; i <= num6; i++)
			{
				num4 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num4]) < 0, (object)i, (object)num4));
			}
			int num7 = TStart;
			int num8 = BEnd;
			if (TStart < BStart)
			{
				num7 = BStart;
			}
			if (TEnd < BEnd)
			{
				num8 = TEnd;
			}
			for (int i = num7; i >= 0; i += -1)
			{
				if ((decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0) | (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num4]) < 0))
				{
					TStart = i + 1;
					BStart = i + 1;
					break;
				}
			}
			int num9 = num8;
			int hLCRange = GlobalForm.HLCRange;
			for (int i = num9; i <= hLCRange; i++)
			{
				if ((decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num]) > 0) | (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num4]) < 0))
				{
					TEnd = i - 1;
					BEnd = i - 1;
					break;
				}
			}
		}
	}

	private static void FindRB()
	{
		GlobalForm.NestedSpecial = true;
		FindAllTops(10);
		int num = Information.UBound((Array)ArrayTops, 1);
		checked
		{
			int num2 = num - 1;
			for (int i = 0; i <= num2; i++)
			{
				int num3 = ArrayTops[i];
				int num4 = i + 1;
				int num5 = num;
				for (int j = num4; j <= num5; j++)
				{
					int num6 = ArrayTops[j];
					if (num6 - num3 > 325)
					{
						break;
					}
					int num7 = num3 + 1;
					int num8 = num6;
					int k;
					for (k = num7; k <= num8; k++)
					{
						if (decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, num3]) >= 0)
						{
							num6 = k;
							break;
						}
					}
					if (k - num3 < 35 || decimal.Compare(GlobalForm.nHLC[1, num6], GlobalForm.nHLC[1, num3]) < 0)
					{
						continue;
					}
					int num9 = num3;
					int num10 = num3 + 1;
					int num11 = num6;
					for (k = num10; k <= num11; k++)
					{
						num9 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num9]) < 0, (object)k, (object)num9));
					}
					int num12 = num3 + (int)Math.Round((double)(num6 - num3) / 5.0);
					int num13 = num3 + 2 * (int)Math.Round((double)(num6 - num3) / 5.0);
					int num14 = num3 + 3 * (int)Math.Round((double)(num6 - num3) / 5.0);
					int num15 = (int)Math.Round((double)num6 - (double)(num6 - num3) / 5.0);
					decimal num16 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num3], GlobalForm.nHLC[2, num9]), 5m);
					decimal d = decimal.Add(GlobalForm.nHLC[2, num9], new decimal(1.75 * Convert.ToDouble(num16)));
					decimal d2 = decimal.Add(GlobalForm.nHLC[2, num9], decimal.Multiply(3m, num16));
					decimal.Add(GlobalForm.nHLC[2, num9], decimal.Multiply(4m, num16));
					decimal.Add(GlobalForm.nHLC[2, num9], decimal.Multiply(6m, num16));
					bool flag = false;
					int num17 = num15;
					for (k = num12; k <= num17; k++)
					{
						decimal d3 = decimal.Divide(decimal.Add(GlobalForm.nHLC[1, k], GlobalForm.nHLC[2, k]), 2m);
						if (decimal.Compare(d3, d2) >= 0)
						{
							flag = true;
							break;
						}
						if (unchecked(k >= num13 && k <= num14) && decimal.Compare(d3, d) >= 0)
						{
							flag = true;
							break;
						}
					}
					if (flag)
					{
						continue;
					}
					int num18 = num6 + 1;
					int num19 = num6 + 7;
					k = num18;
					while (k <= num19)
					{
						if (k > GlobalForm.HLCRange || decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, num6]) >= 0)
						{
							k++;
							continue;
						}
						goto IL_0422;
					}
					if (GlobalForm.StrictPatterns)
					{
						decimal d4 = default(decimal);
						if (num3 - 10 >= 0)
						{
							int num20 = num3 - 10;
							int num21 = num3 - 1;
							for (k = num20; k <= num21; k++)
							{
								d4 = decimal.Add(d4, decimal.Subtract(GlobalForm.nHLC[1, k], GlobalForm.nHLC[2, k]));
							}
							d4 = decimal.Divide(d4, 10m);
							int num22 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, num3 - 1], GlobalForm.nHLC[1, num3 + 1]) > 0, (object)(num3 - 1), (object)(num3 + 1)));
							if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num3], GlobalForm.nHLC[1, num22]), decimal.Multiply(2m, d4)) > 0)
							{
								break;
							}
						}
					}
					HarmonicTarget = Convert.ToDouble(decimal.Add(GlobalForm.nHLC[1, num3], decimal.Subtract(GlobalForm.nHLC[1, num3], GlobalForm.nHLC[2, num9])));
					AddPattern(num3, 0, num6, 0, 0, 0, 66, "Rounding bottom");
					break;
					IL_0422:;
				}
			}
		}
	}

	private static void FindRTop(int iType)
	{
		GlobalForm.NestedSpecial = true;
		FindAllBottoms(10);
		int num = Information.UBound((Array)ArrayBottoms, 1);
		checked
		{
			int num2 = num - 1;
			for (int i = 0; i <= num2; i++)
			{
				int num3 = ArrayBottoms[i];
				int num4 = i + 1;
				int num5 = num;
				for (int j = num4; j <= num5; j++)
				{
					int num6 = ArrayBottoms[j];
					if (num6 - num3 > 325)
					{
						break;
					}
					int num7 = num3 + 1;
					int num8 = num6;
					int k;
					for (k = num7; k <= num8; k++)
					{
						if (decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num3]) <= 0)
						{
							num6 = k;
							break;
						}
					}
					if (k - num3 < 35 || decimal.Compare(GlobalForm.nHLC[2, num6], GlobalForm.nHLC[2, num3]) > 0)
					{
						continue;
					}
					int num9 = num3;
					int num10 = num3 + 1;
					int num11 = num6;
					for (k = num10; k <= num11; k++)
					{
						num9 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, num9]) > 0, (object)k, (object)num9));
					}
					int num12 = num3 + (int)Math.Round((double)(num6 - num3) / 5.0);
					int num13 = num3 + 2 * (int)Math.Round((double)(num6 - num3) / 5.0);
					int num14 = num3 + 3 * (int)Math.Round((double)(num6 - num3) / 5.0);
					int num15 = (int)Math.Round((double)num6 - (double)(num6 - num3) / 5.0);
					decimal num16 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num9], GlobalForm.nHLC[2, num3]), 5m);
					decimal d = decimal.Subtract(GlobalForm.nHLC[1, num9], new decimal(1.75 * Convert.ToDouble(num16)));
					decimal d2 = decimal.Subtract(GlobalForm.nHLC[1, num9], decimal.Multiply(3m, num16));
					decimal.Subtract(GlobalForm.nHLC[1, num9], decimal.Multiply(4m, num16));
					decimal.Subtract(GlobalForm.nHLC[1, num9], decimal.Multiply(6m, num16));
					bool flag = false;
					int num17 = num15;
					for (k = num12; k <= num17; k++)
					{
						decimal d3 = decimal.Divide(decimal.Add(GlobalForm.nHLC[2, k], GlobalForm.nHLC[1, k]), 2m);
						if (decimal.Compare(d3, d2) <= 0)
						{
							flag = true;
							break;
						}
						if (unchecked(k >= num13 && k <= num14) && decimal.Compare(d3, d) <= 0)
						{
							flag = true;
							break;
						}
					}
					if (flag)
					{
						continue;
					}
					HarmonicTarget = Convert.ToDouble(decimal.Add(GlobalForm.nHLC[2, num3], decimal.Subtract(GlobalForm.nHLC[2, num3], GlobalForm.nHLC[1, num9])));
					int num18 = num6 + 1;
					int num19 = num6 + 7;
					for (k = num18; k <= num19; k++)
					{
						if (k > GlobalForm.HLCRange)
						{
							continue;
						}
						switch (iType)
						{
						case 65:
							if (decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num6]) <= 0)
							{
								continue;
							}
							break;
						case 48:
							if (decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num6]) >= 0)
							{
								continue;
							}
							break;
						default:
							continue;
						}
						goto IL_03e8;
					}
					if (iType == 65)
					{
						AddPattern(num3, 0, num6, 0, 0, 0, 65, "Rounding top");
					}
					if (iType != 48)
					{
						break;
					}
					int num20 = (int)Math.Round((double)(num6 - num3) / 4.0);
					int num21 = num6;
					int num22 = num6 + num20;
					for (k = num21; k <= num22 && k <= GlobalForm.HLCRange; k++)
					{
						if (decimal.Compare(GlobalForm.nHLC[3, k], GlobalForm.nHLC[2, num6]) < 0)
						{
							AddPattern(num3, k - 1, num6, 0, 0, 0, 48, "Cup with handle, inverted");
							break;
						}
					}
					break;
					IL_03e8:;
				}
			}
		}
	}

	private static void FindShark32()
	{
		int chartStartIndex = GlobalForm.ChartStartIndex;
		checked
		{
			int num = GlobalForm.ChartEndIndex - 2;
			for (int i = chartStartIndex; i <= num; i++)
			{
				if ((decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i + 1]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i + 1]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, i + 1], GlobalForm.nHLC[1, i + 2]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i + 1], GlobalForm.nHLC[2, i + 2]) < 0))
				{
					AddPattern(i, 0, i + 2, 0, 0, 0, 60, "S32");
				}
			}
		}
	}

	private static void FindSpikeDown()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int num2 = GlobalForm.ChartEndIndex - 1;
			for (int i = num; i <= num2; i++)
			{
				decimal d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.5m);
				if (((decimal.Compare(GlobalForm.nHLC[2, i - 1], decimal.Subtract(GlobalForm.nHLC[1, i], d)) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i + 1], decimal.Subtract(GlobalForm.nHLC[1, i], d)) > 0)) && decimal.Compare(GlobalForm.nHLC[3, i], decimal.Subtract(GlobalForm.nHLC[1, i], decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.25m))) > 0)
				{
					d = FindWideRange(i - 1);
					if (((decimal.Compare(d, -1m) != 0) & (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), d) > 0)) && HLRegression(i - 1, 2, 5) == -1)
					{
						AddPattern(i, 0, i, 0, 0, 0, 40, "s");
					}
				}
			}
		}
	}

	private static void FindSpikeUp()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int num2 = GlobalForm.ChartEndIndex - 1;
			for (int i = num; i <= num2; i++)
			{
				decimal d = decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.5m);
				if (((decimal.Compare(GlobalForm.nHLC[1, i - 1], decimal.Add(GlobalForm.nHLC[2, i], d)) < 0) & (decimal.Compare(GlobalForm.nHLC[1, i + 1], decimal.Add(GlobalForm.nHLC[2, i], d)) < 0)) && decimal.Compare(GlobalForm.nHLC[3, i], decimal.Add(GlobalForm.nHLC[2, i], decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.25m))) < 0)
				{
					d = FindWideRange(i - 1);
					if (((decimal.Compare(d, -1m) != 0) & (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), d) > 0)) && HLRegression(i - 1, 2, 5) == 1)
					{
						AddPattern(i, 0, i, 0, 0, 0, 41, "S");
					}
				}
			}
		}
	}

	private static void FindSymTriangle()
	{
		int[,] array = new int[3, 1];
		int num = TrendLines(-1, 1, 126, 0.25m, 3, Special: true);
		checked
		{
			if (num > 0)
			{
				array = new int[3, Information.UBound((Array)TLArray, 2) + 1];
				int num2 = 0;
				int num3 = Information.UBound((Array)TLArray, 2);
				for (num = 0; num <= num3; num++)
				{
					if (decimal.Compare(TLSlopeArray[num], 0.013m) >= 0)
					{
						array[0, num2] = TLArray[0, num];
						array[1, num2] = TLArray[1, num];
						array[2, num2] = TLArray[2, num];
						num2++;
					}
				}
				if (num2 <= 0)
				{
					return;
				}
				array = (int[,])Utils.CopyArray((Array)array, (Array)new int[3, num2 - 1 + 1]);
				num = TrendLines(1, -1, 126, 0.25m, 3, Special: true);
				if (num > 0)
				{
					int num4 = Information.UBound((Array)array, 2);
					for (num = 0; num <= num4; num++)
					{
						int num5 = Information.UBound((Array)TLArray, 2);
						for (num2 = 0; num2 <= num5; num2++)
						{
							if (decimal.Compare(TLSlopeArray[num2], -0.013m) > 0)
							{
								continue;
							}
							int num6 = TLArray[0, num2];
							int num7 = TLArray[1, num2];
							int num8 = array[0, num];
							int num9 = array[1, num];
							int num10 = num7 - num6;
							int num11 = num9 - num8;
							num10 = Conversions.ToInteger(Interaction.IIf(num10 < num11, (object)num11, (object)num10));
							num10 = Convert.ToInt32(decimal.Multiply(new decimal(num10), 0.55m));
							if (unchecked(num8 >= num6 && num9 <= num7))
							{
								if (decimal.Compare(new decimal(num9 - num8), decimal.Multiply(new decimal(num7 - num6), 0.55m)) >= 0 && !CheckSymTri(num6, num7, num8, num9) && !SymWhiteSpace(num6, num7, num8, num9))
								{
									AddPattern(num6, 0, num7, num8, 0, num9, 87, "SymT");
									break;
								}
							}
							else if (unchecked(num8 <= num6 && num9 >= num7))
							{
								if (decimal.Compare(new decimal(num7 - num6), decimal.Multiply(new decimal(num9 - num8), 0.55m)) >= 0 && !CheckSymTri(num6, num7, num8, num9) && !SymWhiteSpace(num6, num7, num8, num9))
								{
									AddPattern(num6, 0, num7, num8, 0, num9, 87, "SymT");
									break;
								}
							}
							else if (unchecked(num8 >= num6 && num9 >= num7 && num8 < num7))
							{
								if (num7 - num8 > num10 && !CheckSymTri(num6, num7, num8, num9) && !SymWhiteSpace(num6, num7, num8, num9))
								{
									AddPattern(num6, 0, num7, num8, 0, num9, 87, "SymT");
									break;
								}
							}
							else if (unchecked(num8 <= num6 && num9 <= num7 && num9 > num6) && num9 - num6 > num10 && !CheckSymTri(num6, num7, num8, num9) && !SymWhiteSpace(num6, num7, num8, num9))
							{
								AddPattern(num6, 0, num7, num8, 0, num9, 87, "SymT");
								break;
							}
						}
					}
				}
			}
			array = null;
			TLArray = null;
		}
	}

	private static void Find3Bar()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int num2 = GlobalForm.ChartEndIndex - 2;
			for (int i = num; i <= num2; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[3, i - 1], GlobalForm.nHLC[3, i]) > 0 && ((decimal.Compare(GlobalForm.nHLC[2, i + 1], GlobalForm.nHLC[2, i]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i + 1], GlobalForm.nHLC[2, i + 2]) < 0)) && ((GlobalForm.StrictPatterns & (decimal.Compare(GlobalForm.nHLC[3, i + 2], GlobalForm.nHLC[1, i]) > 0) & (decimal.Compare(GlobalForm.nHLC[3, i + 2], GlobalForm.nHLC[1, i + 1]) > 0)) | (!GlobalForm.StrictPatterns & (decimal.Compare(GlobalForm.nHLC[3, i + 2], GlobalForm.nHLC[1, i + 1]) > 0))))
				{
					AddPattern(i, 0, i + 2, 0, 0, 0, 59, "3Bar");
				}
			}
		}
	}

	private static void FindThreeLR()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 3;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				if ((decimal.Compare(GlobalForm.nHLC[2, i - 3], GlobalForm.nHLC[2, i - 2]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 2], GlobalForm.nHLC[2, i - 1]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i - 3]) > 0))
				{
					AddPattern(i - 3, 0, i, 0, 0, 0, 32, "3L-R");
				}
			}
		}
	}

	private static void FindThreeLRInv()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 3;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				if ((decimal.Compare(GlobalForm.nHLC[1, i - 3], GlobalForm.nHLC[1, i - 2]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, i - 2], GlobalForm.nHLC[1, i - 1]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i - 3]) < 0))
				{
					AddPattern(i - 3, 0, i, 0, 0, 0, 31, "i3LR");
				}
			}
		}
	}

	private static void FindTLs(int iType)
	{
		TLArray = null;
		TLArray = new int[3, 2];
		GlobalForm.NestedSpecial = true;
		checked
		{
			switch (iType)
			{
			case 58:
			{
				FindAllTops(3);
				int num15 = Information.UBound((Array)ArrayTops, 1);
				for (int i = 0; i <= num15; i++)
				{
					TLArray[0, 0] = ArrayTops[i];
					int num16 = i + 1;
					int num17 = Information.UBound((Array)ArrayTops, 1);
					for (int j = num16; j <= num17; j++)
					{
						TLArray[0, 1] = ArrayTops[j];
						if ((ArrayTops[j] - ArrayTops[i] > GlobalForm.TLDNLength) & (GlobalForm.TLDNLength < 1000))
						{
							break;
						}
						decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[1, ArrayTops[i]]), new decimal(ArrayTops[j] - ArrayTops[i]));
						if (decimal.Compare(d, 0m) >= 0)
						{
							continue;
						}
						int num4 = ArrayTops[j];
						int num5 = 1;
						int num18 = i + 1;
						int num19 = Information.UBound((Array)ArrayTops, 1);
						for (int k = num18; k <= num19; k++)
						{
							decimal num8 = decimal.Add(decimal.Multiply(d, new decimal(ArrayTops[k] - ArrayTops[i])), GlobalForm.nHLC[1, ArrayTops[i]]);
							if ((ArrayTops[k] - ArrayTops[i] > GlobalForm.TLDNLength) & (GlobalForm.TLDNLength < 1000))
							{
								goto end_IL_0320;
							}
							if (CheckNearness(GlobalForm.nHLC[1, ArrayTops[k]], num8, -1m, 0.1m))
							{
								num4 = ArrayTops[k];
								TLArray = (int[,])Utils.CopyArray((Array)TLArray, (Array)new int[3, num5 + 1]);
								TLArray[0, num5] = ArrayTops[k];
								num5++;
							}
							else if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[k]], decimal.Add(num8, 0.1m)) > 0)
							{
								break;
							}
							if (unchecked(GlobalForm.FormTypeLoaded == 4 && num5 == 3))
							{
								break;
							}
						}
						if (num5 < 3)
						{
							continue;
						}
						int num20 = TLArray[0, 0];
						int num21 = TLArray[0, Information.UBound((Array)TLArray, 2)];
						int num22 = (int)Math.Round((double)num20 + (double)(num21 - num20) / 3.0);
						int num23 = (int)Math.Round((double)num21 - (double)(num21 - num20) / 3.0);
						int num24 = num5 - 1;
						int num14 = 1;
						while (num14 <= num24)
						{
							if (!((TLArray[0, num14] > num22) & (TLArray[0, num14] < num23)))
							{
								num14++;
								continue;
							}
							goto IL_02b9;
						}
						continue;
						IL_02b9:
						if (decimal.Compare(GlobalForm.nHLC[1, TLArray[0, 0]], GlobalForm.nHLC[1, num4]) >= 0)
						{
							AddPattern(ArrayTops[i], TLArray[0, num5 - 1], num4, 0, 0, 0, iType, "TL");
						}
						break;
						continue;
						end_IL_0320:
						break;
					}
				}
				break;
			}
			case 57:
			{
				FindAllBottoms(3);
				int num = Information.UBound((Array)ArrayBottoms, 1);
				for (int i = 0; i <= num; i++)
				{
					TLArray[0, 0] = ArrayBottoms[i];
					int num2 = i + 1;
					int num3 = Information.UBound((Array)ArrayBottoms, 1);
					for (int j = num2; j <= num3; j++)
					{
						TLArray[0, 1] = ArrayBottoms[j];
						if ((ArrayBottoms[j] - ArrayBottoms[i] > GlobalForm.TLUpLength) & (GlobalForm.TLUpLength < 1000))
						{
							break;
						}
						decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, ArrayBottoms[j]], GlobalForm.nHLC[2, ArrayBottoms[i]]), new decimal(ArrayBottoms[j] - ArrayBottoms[i]));
						if (decimal.Compare(d, 0m) <= 0)
						{
							continue;
						}
						int num4 = ArrayBottoms[j];
						int num5 = 1;
						int num6 = i + 1;
						int num7 = Information.UBound((Array)ArrayBottoms, 1);
						for (int k = num6; k <= num7; k++)
						{
							decimal num8 = decimal.Add(decimal.Multiply(d, new decimal(ArrayBottoms[k] - ArrayBottoms[i])), GlobalForm.nHLC[2, ArrayBottoms[i]]);
							if ((ArrayBottoms[k] - ArrayBottoms[i] > GlobalForm.TLUpLength) & (GlobalForm.TLUpLength < 1000))
							{
								goto end_IL_0641;
							}
							if (CheckNearness(GlobalForm.nHLC[2, ArrayBottoms[k]], num8, -1m, 0.1m))
							{
								num4 = ArrayBottoms[k];
								TLArray = (int[,])Utils.CopyArray((Array)TLArray, (Array)new int[3, num5 + 1]);
								TLArray[0, num5] = ArrayBottoms[k];
								num5++;
							}
							else if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[k]], decimal.Subtract(num8, 0.1m)) < 0)
							{
								break;
							}
							if (unchecked(GlobalForm.FormTypeLoaded == 4 && num5 == 3))
							{
								break;
							}
						}
						if (num5 < 3)
						{
							continue;
						}
						int num9 = TLArray[0, 0];
						int num10 = TLArray[0, Information.UBound((Array)TLArray, 2)];
						int num11 = (int)Math.Round((double)num9 + (double)(num10 - num9) / 3.0);
						int num12 = (int)Math.Round((double)num10 - (double)(num10 - num9) / 3.0);
						int num13 = num5 - 1;
						int num14 = 1;
						while (num14 <= num13)
						{
							if (!((TLArray[0, num14] > num11) & (TLArray[0, num14] < num12)))
							{
								num14++;
								continue;
							}
							goto IL_05da;
						}
						continue;
						IL_05da:
						if (decimal.Compare(GlobalForm.nHLC[2, TLArray[0, 0]], GlobalForm.nHLC[2, num4]) <= 0)
						{
							AddPattern(ArrayBottoms[i], TLArray[0, num5 - 1], num4, 0, 0, 0, iType, "TL");
						}
						break;
						continue;
						end_IL_0641:
						break;
					}
				}
				break;
			}
			}
			GlobalForm.NestedSpecial = false;
		}
	}

	private static bool FindTopArmpit(int Index1, int Index2, int BottomSize)
	{
		ArmPit = -1m;
		for (int i = 0; i <= BottomSize; i = checked(i + 1))
		{
			if ((ArrayBottoms[i] >= Index1) & (ArrayBottoms[i] <= Index2))
			{
				if (decimal.Compare(ArmPit, -1m) == 0)
				{
					ArmPit = GlobalForm.nHLC[2, ArrayBottoms[i]];
				}
				if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[i]], ArmPit) < 0)
				{
					ArmPit = GlobalForm.nHLC[2, ArrayBottoms[i]];
				}
			}
			else if (ArrayBottoms[i] > Index2)
			{
				break;
			}
		}
		if (decimal.Compare(ArmPit, -1m) == 0)
		{
			return true;
		}
		return false;
	}

	private static bool FindTopDualHead(int LSIndex, int RSIndex, int i, int z, decimal Symmetry)
	{
		bool result = false;
		checked
		{
			int num = i + 1;
			int num2 = z - 1;
			for (int j = num; j <= num2; j++)
			{
				if (ArrayTops[j] == HeadIndex || !CheckNearness(GlobalForm.nHLC[1, HeadIndex], GlobalForm.nHLC[1, ArrayTops[j]], -1m, 0.1m))
				{
					continue;
				}
				int num3 = Conversions.ToInteger(Interaction.IIf(HeadIndex < ArrayTops[j], (object)HeadIndex, (object)ArrayTops[j]));
				int num4 = Conversions.ToInteger(Interaction.IIf(HeadIndex < ArrayTops[j], (object)ArrayTops[j], (object)HeadIndex));
				HeadIndex = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, num3], GlobalForm.nHLC[1, num4]) >= 0, (object)num3, (object)num4));
				if ((double)(num4 - num3) > (double)(RSIndex - LSIndex) / 2.0)
				{
					return true;
				}
				int num5 = RSIndex - num4;
				int num6 = num3 - LSIndex;
				if (num6 < num5)
				{
					num5 = num3 - LSIndex;
					num6 = RSIndex - num4;
				}
				if (num5 == 0)
				{
					return true;
				}
				if ((double)num6 / (double)num5 > Convert.ToDouble(Symmetry))
				{
					result = true;
					break;
				}
				Head2Index = Conversions.ToInteger(Interaction.IIf(HeadIndex != num3, (object)num3, (object)num4));
				for (int k = i; k <= z; k++)
				{
					if (((ArrayTops[k] != Head2Index) & (ArrayTops[k] != HeadIndex)) && ((decimal.Compare(GlobalForm.nHLC[1, ArrayTops[k]], GlobalForm.nHLC[1, HeadIndex]) >= 0) | (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[k]], GlobalForm.nHLC[1, Head2Index]) >= 0)))
					{
						Head2Index = 0;
						break;
					}
				}
				break;
			}
			if (Head2Index == 0 && NotSymmetrical)
			{
				result = true;
			}
			NotSymmetrical = false;
			return result;
		}
	}

	private static bool FindTopOuterShoulders(int LSIndex, int RSIndex, int i, int z, int TopSize, decimal Symmetry, decimal HeadShoulder)
	{
		checked
		{
			for (int j = i - 1; j >= 0; j += -1)
			{
				decimal num = GlobalForm.nHLC[1, ArrayTops[j]];
				if (decimal.Compare(num, GlobalForm.nHLC[1, HeadIndex]) >= 0 || (Head2Index != 0 && decimal.Compare(num, GlobalForm.nHLC[1, Head2Index]) >= 0))
				{
					break;
				}
				int k;
				for (k = z + 1; k <= TopSize; k++)
				{
					if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[k]], GlobalForm.nHLC[1, HeadIndex]) >= 0 || (Head2Index != 0 && decimal.Compare(GlobalForm.nHLC[1, ArrayTops[k]], GlobalForm.nHLC[1, Head2Index]) >= 0))
					{
						goto end_IL_0319;
					}
					if (!CheckNearness(GlobalForm.nHLC[1, ArrayTops[k]], num, -1m, 0.25m))
					{
						continue;
					}
					int num2 = ArrayTops[k] - HeadIndex;
					int num3 = HeadIndex - ArrayTops[j];
					if (num3 < num2)
					{
						num2 = HeadIndex - ArrayTops[j];
						num3 = ArrayTops[k] - HeadIndex;
					}
					if (num2 == 0)
					{
						return true;
					}
					if (!((double)num3 / (double)num2 < Convert.ToDouble(Symmetry)) || CheckNearness(GlobalForm.nHLC[1, HeadIndex], GlobalForm.nHLC[1, ArrayTops[k]], -1m, HeadShoulder) || CheckNearness(GlobalForm.nHLC[1, HeadIndex], GlobalForm.nHLC[1, ArrayTops[j]], -1m, HeadShoulder))
					{
						continue;
					}
					goto IL_01bf;
				}
				continue;
				IL_01bf:
				decimal num4 = new decimal(HeadIndex - LSIndex);
				num4 = decimal.Multiply(2m, Conversions.ToDecimal(Interaction.IIf(decimal.Compare(new decimal(RSIndex - HeadIndex), num4) > 0, (object)(RSIndex - HeadIndex), (object)num4)));
				if ((decimal.Compare(new decimal(HeadIndex - ArrayTops[j]), num4) <= 0) & (decimal.Compare(new decimal(ArrayTops[k] - HeadIndex), num4) <= 0))
				{
					if (ArrayTops[k] - ArrayTops[j] <= 126)
					{
						if (CheckNearness(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[1, LSIndex], 0.8m, -1m))
						{
							if (CheckNearness(GlobalForm.nHLC[1, ArrayTops[k]], GlobalForm.nHLC[1, RSIndex], 0.8m, -1m))
							{
								iLS2 = ArrayTops[j];
								iRS2 = ArrayTops[k];
								return false;
							}
							return true;
						}
						return true;
					}
					return true;
				}
				return true;
				continue;
				end_IL_0319:
				break;
			}
			return false;
		}
	}

	private static bool FindTopPriceTrend(int LSIndex, decimal ArmPitLow)
	{
		checked
		{
			for (int i = LSIndex - 1; i >= 0 && decimal.Compare(GlobalForm.nHLC[1, i], ArmPitLow) >= 0; i += -1)
			{
				if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, LSIndex]) > 0)
				{
					return true;
				}
			}
			return false;
		}
	}

	private static void Findtwodance()
	{
		//IL_036a: Unknown result type (might be due to invalid IL or missing references)
		int try0000_dispatch = -1;
		int num3 = default(int);
		int num = default(int);
		int num2 = default(int);
		int num5 = default(int);
		int chartEndIndex = default(int);
		decimal d = default(decimal);
		decimal num7 = default(decimal);
		decimal num8 = default(decimal);
		decimal dojiRange = default(decimal);
		int num9 = default(int);
		while (true)
		{
			try
			{
				/*Note: ILSpy has introduced the following switch to emulate a goto from catch-block to try-block*/;
				checked
				{
					int num4;
					int num6;
					switch (try0000_dispatch)
					{
					default:
						ProjectData.ClearProjectError();
						num3 = 2;
						goto IL_0007;
					case 1044:
						{
							num = num2;
							switch (num3)
							{
							case 2:
								break;
							case 1:
								goto IL_03a8;
							default:
								goto end_IL_0000;
							}
							goto IL_0360;
						}
						IL_03a8:
						num4 = unchecked(num + 1);
						while (true)
						{
							num = 0;
							switch (num4)
							{
							case 1:
								break;
							case 2:
								goto IL_0007;
							case 3:
								goto IL_001e;
							case 4:
								goto IL_006e;
							case 5:
								goto IL_009a;
							case 6:
								goto IL_010a;
							case 7:
								goto IL_017a;
							case 8:
								goto IL_01b2;
							case 9:
								goto IL_01da;
							case 10:
								goto IL_0241;
							case 11:
								goto IL_02a8;
							case 12:
								goto IL_02de;
							case 13:
								goto IL_0310;
							case 14:
								goto IL_031e;
							case 15:
								goto IL_032d;
							case 16:
								goto IL_0334;
							case 17:
								goto IL_034c;
							case 19:
								goto IL_0360;
							case 20:
								goto end_IL_0000_2;
							case 22:
								goto IL_038a;
							default:
								goto end_IL_0000;
							case 18:
							case 21:
							case 23:
								goto end_IL_0000_3;
							}
							break;
							IL_038a:
							num2 = 22;
							ProjectData.ClearProjectError();
							if (num == 0)
							{
								throw ProjectData.CreateProjectError(-2146828268);
							}
							num4 = num;
						}
						goto default;
						IL_034c:
						num2 = 17;
						num5++;
						goto IL_0355;
						IL_0360:
						num2 = 19;
						Interaction.MsgBox((object)"Error in FindTwoDance()", (MsgBoxStyle)0, (object)null);
						break;
						IL_0007:
						num2 = 2;
						num6 = GlobalForm.ChartStartIndex + 1;
						chartEndIndex = GlobalForm.ChartEndIndex;
						num5 = num6;
						goto IL_0355;
						IL_0355:
						if (num5 > chartEndIndex)
						{
							goto end_IL_0000_3;
						}
						goto IL_001e;
						IL_001e:
						num2 = 3;
						if ((decimal.Compare(GlobalForm.nHLC[1, num5 - 1], GlobalForm.nHLC[1, num5]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, num5 - 1], GlobalForm.nHLC[2, num5]) < 0))
						{
							goto IL_006e;
						}
						goto IL_034c;
						IL_006e:
						num2 = 4;
						d = Math.Abs(decimal.Subtract(GlobalForm.nHLC[3, num5 - 1], GlobalForm.nHLC[0, num5 - 1]));
						goto IL_009a;
						IL_009a:
						num2 = 5;
						num7 = decimal.Subtract(GlobalForm.nHLC[1, num5 - 1], Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[3, num5 - 1], GlobalForm.nHLC[0, num5 - 1]) > 0, (object)GlobalForm.nHLC[3, num5 - 1], (object)GlobalForm.nHLC[0, num5 - 1])));
						goto IL_010a;
						IL_010a:
						num2 = 6;
						num8 = decimal.Subtract(Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[3, num5 - 1], GlobalForm.nHLC[0, num5 - 1]) > 0, (object)GlobalForm.nHLC[0, num5 - 1], (object)GlobalForm.nHLC[3, num5 - 1])), GlobalForm.nHLC[2, num5 - 1]);
						goto IL_017a;
						IL_017a:
						num2 = 7;
						if ((decimal.Compare(num8, decimal.Multiply(3m, d)) > 0) & (decimal.Compare(num8, decimal.Multiply(2m, num7)) > 0))
						{
							goto IL_01b2;
						}
						goto IL_034c;
						IL_01b2:
						num2 = 8;
						d = Math.Abs(decimal.Subtract(GlobalForm.nHLC[3, num5], GlobalForm.nHLC[0, num5]));
						goto IL_01da;
						IL_01da:
						num2 = 9;
						num7 = decimal.Subtract(GlobalForm.nHLC[1, num5], Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[3, num5], GlobalForm.nHLC[0, num5]) > 0, (object)GlobalForm.nHLC[3, num5], (object)GlobalForm.nHLC[0, num5])));
						goto IL_0241;
						IL_0241:
						num2 = 10;
						num8 = decimal.Subtract(Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[3, num5], GlobalForm.nHLC[0, num5]) > 0, (object)GlobalForm.nHLC[0, num5], (object)GlobalForm.nHLC[3, num5])), GlobalForm.nHLC[2, num5]);
						goto IL_02a8;
						IL_02a8:
						num2 = 11;
						if ((decimal.Compare(num7, decimal.Multiply(3m, d)) > 0) & (decimal.Compare(num7, decimal.Multiply(2m, num8)) > 0))
						{
							goto IL_02de;
						}
						goto IL_034c;
						IL_02de:
						num2 = 12;
						dojiRange = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.01m, (object)0.03m));
						goto IL_0310;
						IL_0310:
						num2 = 13;
						if (FindCandles.WithinRange(num5, dojiRange))
						{
							goto IL_031e;
						}
						goto IL_034c;
						IL_031e:
						num2 = 14;
						num9 = HLRegression(num5 - 2, 2, 5);
						goto IL_032d;
						IL_032d:
						num2 = 15;
						if (num9 == -1)
						{
							goto IL_0334;
						}
						goto IL_034c;
						IL_0334:
						num2 = 16;
						AddPattern(num5 - 1, 0, num5, 0, 0, 0, 0, "2D");
						goto IL_034c;
						end_IL_0000_2:
						break;
					}
					num2 = 20;
					ProjectData.ClearProjectError();
					if (num == 0)
					{
						throw ProjectData.CreateProjectError(-2146828268);
					}
					num = 0;
					break;
				}
				end_IL_0000:;
			}
			catch (object obj) when (obj is Exception && num3 != 0 && num == 0)
			{
				ProjectData.SetProjectError((Exception)obj);
				try0000_dispatch = 1044;
				continue;
			}
			throw ProjectData.CreateProjectError(-2146828237);
			continue;
			end_IL_0000_3:
			break;
		}
		if (num != 0)
		{
			ProjectData.ClearProjectError();
		}
	}

	private static void FindTwoDid()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				if ((decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i]) < 0))
				{
					decimal num2 = FindWideRange(i - 2);
					if (decimal.Compare(num2, -1m) != 0 && decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[2, i - 1]), decimal.Multiply(1.5m, num2)) > 0 && decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), decimal.Multiply(1.5m, num2)) > 0)
					{
						AddPattern(i - 1, 0, i, 0, 0, 0, 23, "2Did");
					}
				}
			}
		}
	}

	private static void FindTwoTall()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				decimal num2 = FindWideRange(i - 2);
				if (decimal.Compare(num2, -1m) != 0 && decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[2, i - 1]), decimal.Multiply(2m, num2)) > 0 && decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), decimal.Multiply(2m, num2)) > 0)
				{
					AddPattern(i - 1, 0, i, 0, 0, 0, 22, "2T");
				}
			}
		}
	}

	private static void FindTripleBottoms()
	{
		FindAllBottoms(5);
		int num = Information.UBound((Array)ArrayBottoms, 1);
		if (num < 3)
		{
			return;
		}
		FindAllTops(2);
		if (Information.UBound((Array)ArrayTops, 1) < 2)
		{
			return;
		}
		int num2 = num;
		checked
		{
			for (int i = 0; i <= num2; i++)
			{
				if (i + 2 > num)
				{
					continue;
				}
				decimal point = GlobalForm.nHLC[2, ArrayBottoms[i]];
				int num3 = i + 1;
				int num4 = num;
				for (int j = num3; j <= num4 && ArrayBottoms[j] - ArrayBottoms[i] <= 126; j++)
				{
					decimal num5 = GlobalForm.nHLC[2, ArrayBottoms[j]];
					if (!CheckNearness(point, num5, -1m, 0.25m))
					{
						continue;
					}
					int num6 = j + 1;
					int num7 = num;
					for (int k = num6; k <= num7; k++)
					{
						if (ArrayBottoms[k] - ArrayBottoms[i] > 126)
						{
							goto end_IL_0384;
						}
						decimal point2 = GlobalForm.nHLC[2, ArrayBottoms[k]];
						if (!(CheckNearness(point, point2, -1m, 0.25m) & CheckNearness(num5, point2, -1m, 0.25m)) || TBCheckDownTrend(i, k))
						{
							continue;
						}
						int num8 = CheckConfirmation(ArrayBottoms[i] + 1, ArrayBottoms[k] - 1, -1);
						if (!unchecked(num8 == 0 || num8 == 1))
						{
							continue;
						}
						bool flag = true;
						int num9 = Information.UBound((Array)ArrayTops, 1);
						for (int l = 0; l <= num9; l++)
						{
							if (!((ArrayBottoms[i] < ArrayTops[l]) & (ArrayBottoms[j] > ArrayTops[l])))
							{
								continue;
							}
							int num10 = l + 1;
							int num11 = Information.UBound((Array)ArrayTops, 1);
							for (int m = num10; m <= num11; m++)
							{
								if ((ArrayBottoms[j] < ArrayTops[m]) & (ArrayBottoms[k] > ArrayTops[m]))
								{
									flag = false;
									break;
								}
							}
							break;
						}
						if (flag)
						{
							continue;
						}
						int num12 = i + 1;
						int num13 = k - 1;
						for (int l = num12; l <= num13; l++)
						{
							if (l != j)
							{
								decimal point3 = GlobalForm.nHLC[2, ArrayBottoms[l]];
								if (!CheckNearness(point3, GlobalForm.nHLC[2, ArrayBottoms[i]], -1m, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.125m, (object)0.25m))) | !CheckNearness(point3, GlobalForm.nHLC[2, ArrayBottoms[j]], -1m, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.125m, (object)0.25m))) | !CheckNearness(point3, GlobalForm.nHLC[2, ArrayBottoms[k]], -1m, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.125m, (object)0.25m))))
								{
									flag = true;
									break;
								}
							}
						}
						if (!flag && !CheckFor3rdBottom(i, j, k, 0.25m))
						{
							AddPattern(ArrayBottoms[i], ArrayBottoms[j], ArrayBottoms[k], 0, 0, 0, 86, Conversions.ToString(Interaction.IIf(num8 == 1, (object)"B", (object)"B?")));
							goto end_IL_0384;
						}
					}
					continue;
					end_IL_0384:
					break;
				}
			}
		}
	}

	private static void FindTripleTops()
	{
		FindAllTops(5);
		int num = Information.UBound((Array)ArrayTops, 1);
		if (num < 3)
		{
			return;
		}
		FindAllBottoms(2);
		if (Information.UBound((Array)ArrayBottoms, 1) < 2)
		{
			return;
		}
		int num2 = num;
		checked
		{
			for (int i = 0; i <= num2; i++)
			{
				if (i + 2 > num)
				{
					continue;
				}
				decimal point = GlobalForm.nHLC[1, ArrayTops[i]];
				int num3 = i + 1;
				int num4 = num;
				for (int j = num3; j <= num4 && ArrayTops[j] - ArrayTops[i] <= 126; j++)
				{
					decimal point2 = GlobalForm.nHLC[1, ArrayTops[j]];
					if (!CheckNearness(point, point2, -1m, 0.25m))
					{
						continue;
					}
					int num5 = j + 1;
					int num6 = num;
					for (int k = num5; k <= num6; k++)
					{
						if (ArrayTops[k] - ArrayTops[i] > 126)
						{
							goto end_IL_03cb;
						}
						decimal point3 = GlobalForm.nHLC[1, ArrayTops[k]];
						if (!CheckNearness(point, point3, -1m, 0.25m) || TTCheckUpTrend(i, k))
						{
							continue;
						}
						int num7 = CheckConfirmation(ArrayTops[i] + 1, ArrayTops[k] - 1, 1);
						if (!unchecked(num7 == 0 || num7 == -1))
						{
							continue;
						}
						bool flag = true;
						int num8 = Information.UBound((Array)ArrayBottoms, 1);
						for (int l = 0; l <= num8; l++)
						{
							if (!((ArrayTops[i] < ArrayBottoms[l]) & (ArrayTops[j] > ArrayBottoms[l])))
							{
								continue;
							}
							int num9 = l + 1;
							int num10 = Information.UBound((Array)ArrayBottoms, 1);
							for (int m = num9; m <= num10; m++)
							{
								if ((ArrayTops[j] < ArrayBottoms[m]) & (ArrayTops[k] > ArrayBottoms[m]))
								{
									flag = false;
									break;
								}
							}
							break;
						}
						if (flag)
						{
							continue;
						}
						int num11 = i + 1;
						int num12 = k - 1;
						for (int l = num11; l <= num12; l++)
						{
							if (l != j)
							{
								decimal d = GlobalForm.nHLC[1, ArrayTops[l]];
								if ((decimal.Compare(d, GlobalForm.nHLC[1, ArrayTops[i]]) > 0) | (decimal.Compare(d, GlobalForm.nHLC[1, ArrayTops[j]]) > 0) | (decimal.Compare(d, GlobalForm.nHLC[1, ArrayTops[k]]) > 0))
								{
									flag = true;
									break;
								}
							}
						}
						if (!flag && !CheckForTop(i, k, 0.25m))
						{
							decimal priceScale = GetPriceScale(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[1, ArrayTops[i]]);
							if (decimal.Compare(priceScale, 0m) != 0 && !((decimal.Compare(GlobalForm.nHLC[1, ArrayTops[j]], decimal.Add(GlobalForm.nHLC[1, ArrayTops[i]], Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0, (object)decimal.Divide(0.1m, priceScale))))) > 0) & (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[j]], decimal.Add(GlobalForm.nHLC[1, ArrayTops[k]], Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0, (object)decimal.Divide(0.1m, priceScale))))) > 0)))
							{
								AddPattern(ArrayTops[i], ArrayTops[j], ArrayTops[k], 0, 0, 0, 85, Conversions.ToString(Interaction.IIf(num7 == -1, (object)"T", (object)"T?")));
							}
							goto end_IL_03cb;
						}
					}
					continue;
					end_IL_03cb:
					break;
				}
			}
		}
	}

	private static void FindUglyDoubleBottoms()
	{
		FindAllBottoms(4);
		int num = Information.UBound((Array)ArrayBottoms, 1);
		if (num < 2)
		{
			return;
		}
		FindAllTops(5);
		if (Information.UBound((Array)ArrayTops, 1) == 0)
		{
			return;
		}
		checked
		{
			int num2 = num - 1;
			for (int i = 0; i <= num2; i++)
			{
				int num3 = i + 1;
				if (ArrayBottoms[num3] - ArrayBottoms[i] > 126)
				{
					break;
				}
				if (!((decimal.Compare(decimal.Multiply(GlobalForm.nHLC[2, ArrayBottoms[i]], 1.05m), GlobalForm.nHLC[2, ArrayBottoms[num3]]) <= 0) & (decimal.Compare(decimal.Multiply(GlobalForm.nHLC[2, ArrayBottoms[i]], 1.15m), GlobalForm.nHLC[2, ArrayBottoms[num3]]) >= 0)) || CheckDBDownTrend(i, num3, 0m, 98))
				{
					continue;
				}
				int num4 = ArrayBottoms[i];
				int num5 = ArrayBottoms[i] + 1;
				int num6 = ArrayBottoms[num3];
				for (int j = num5; j <= num6; j++)
				{
					num4 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, num4]) > 0, (object)j, (object)num4));
				}
				bool flag = false;
				int num7 = ArrayBottoms[num3] + 1;
				int hLCRange = GlobalForm.HLCRange;
				for (int j = num7; j <= hLCRange && decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[2, ArrayBottoms[num3]]) >= 0; j++)
				{
					if (decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[1, num4]) > 0)
					{
						flag = true;
						break;
					}
				}
				if (flag)
				{
					int num8 = CheckConfirmation(ArrayBottoms[i] + 1, ArrayBottoms[num3] - 1, -1);
					if (unchecked(num8 == 1 || num8 == 0))
					{
						AddPattern(ArrayBottoms[i], 0, ArrayBottoms[num3], 0, 0, 0, 34, Conversions.ToString(Interaction.IIf(num8 == 1, (object)"UDB", (object)"UDB?")));
					}
				}
			}
		}
	}

	private static void FindUglyDoubleTops()
	{
		FindAllTops(4);
		int num = Information.UBound((Array)ArrayTops, 1);
		if (num < 2)
		{
			return;
		}
		FindAllBottoms(5);
		if (Information.UBound((Array)ArrayBottoms, 1) < 1)
		{
			return;
		}
		checked
		{
			int num2 = num - 1;
			for (int i = 0; i <= num2; i++)
			{
				int num3 = i + 1;
				if (ArrayTops[num3] - ArrayTops[i] > 126)
				{
					break;
				}
				if (!((decimal.Compare(decimal.Multiply(GlobalForm.nHLC[1, ArrayTops[i]], 0.95m), GlobalForm.nHLC[1, ArrayTops[num3]]) >= 0) & (decimal.Compare(decimal.Multiply(GlobalForm.nHLC[1, ArrayTops[i]], 0.85m), GlobalForm.nHLC[1, ArrayTops[num3]]) <= 0)) || CheckDTUpTrend(i, num3, 0m, 97))
				{
					continue;
				}
				int num4 = ArrayTops[i];
				int num5 = ArrayTops[i] + 1;
				int num6 = ArrayTops[num3];
				for (int j = num5; j <= num6; j++)
				{
					num4 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num4]) < 0, (object)j, (object)num4));
				}
				bool flag = false;
				int num7 = ArrayTops[num3] + 1;
				int hLCRange = GlobalForm.HLCRange;
				for (int j = num7; j <= hLCRange && decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[1, ArrayTops[num3]]) <= 0; j++)
				{
					if (decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[2, num4]) < 0)
					{
						flag = true;
						break;
					}
				}
				if (flag)
				{
					int num8 = CheckConfirmation(ArrayTops[i] + 1, ArrayTops[num3] - 1, 1);
					if (unchecked(num8 == 0 || num8 == -1))
					{
						AddPattern(ArrayTops[i], 0, ArrayTops[num3], 0, 0, 0, 33, Conversions.ToString(Interaction.IIf(num8 == -1, (object)"UDT", (object)"UDT?")));
					}
				}
			}
		}
	}

	private static void FindVBottoms()
	{
		int num = Conversions.ToInteger(Interaction.IIf(GlobalForm.StrictPatterns, (object)15, (object)7));
		FindAllTops(3);
		int num2 = Information.UBound((Array)ArrayTops, 1);
		if (num2 < 2)
		{
			return;
		}
		FindAllBottoms(5);
		int num3 = Information.UBound((Array)ArrayBottoms, 1);
		if (num3 == 0)
		{
			return;
		}
		decimal num4 = FindPeakBottomMove(ArrayTops, ArrayBottoms, num2, num3);
		if ((decimal.Compare(num4, 0.074m) > 0) | (decimal.Compare(num4, 0m) == 0))
		{
			num4 = 0.074m;
		}
		int num5 = num2;
		checked
		{
			for (int i = 0; i <= num5; i++)
			{
				int num6 = num3;
				for (int j = 1; j <= num6; j++)
				{
					if (!((ArrayBottoms[j - 1] < ArrayTops[i]) & (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[j - 1]], GlobalForm.nHLC[1, ArrayTops[i]]) < 0) & (ArrayBottoms[j] > ArrayTops[i]) & (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[i]], GlobalForm.nHLC[2, ArrayBottoms[j]]) > 0)))
					{
						continue;
					}
					int num7 = i + 1;
					if (num7 > num2)
					{
						return;
					}
					if (ArrayBottoms[j] >= ArrayTops[num7])
					{
						break;
					}
					double num8 = Convert.ToDouble(GlobalForm.nHLC[2, ArrayBottoms[j]]) + Convert.ToDouble(decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[i]], GlobalForm.nHLC[2, ArrayBottoms[j]])) * 0.382;
					num7 = -1;
					int num9 = ArrayBottoms[j] + 1;
					int hLCRange = GlobalForm.HLCRange;
					for (int k = num9; k <= hLCRange; k++)
					{
						if (Convert.ToDouble(GlobalForm.nHLC[1, k]) >= num8)
						{
							num7 = k;
							break;
						}
					}
					if (num7 == -1)
					{
						continue;
					}
					long num10 = num7 - ArrayTops[i];
					if (unchecked(num10 >= num && num10 <= 65))
					{
						if (decimal.Compare(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[i]], GlobalForm.nHLC[2, ArrayBottoms[j]]), GlobalForm.nHLC[1, ArrayTops[i]]), num4) < 0)
						{
							continue;
						}
						int num11 = ArrayBottoms[j] + 1;
						int num12 = num7;
						for (int k = num11; k <= num12; k++)
						{
							if (decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, ArrayBottoms[j]]) < 0)
							{
								goto end_IL_04db;
							}
						}
						int num13 = ArrayTops[i] + 1;
						int num14 = ArrayBottoms[j] - 1;
						for (int k = num13; k <= num14; k++)
						{
							if (decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, ArrayTops[i]]) > 0)
							{
								goto end_IL_04db;
							}
						}
						int num15 = ArrayBottoms[j];
						int num16 = ((num15 - 30 >= 0) ? (num15 - 30) : 0);
						decimal num17 = default(decimal);
						int num18 = 0;
						int num19 = num16 + 1;
						int num20 = num15 - 2;
						int num21;
						for (int k = num19; k <= num20; k++)
						{
							if ((decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, k - 1]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, k + 1]) < 0))
							{
								num21 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, k - 1], GlobalForm.nHLC[2, k + 1]) < 0, (object)(k - 1), (object)(k + 1)));
								num17 = decimal.Subtract(decimal.Add(num17, GlobalForm.nHLC[2, num21]), GlobalForm.nHLC[2, k]);
								num18++;
							}
						}
						if (!((num18 != 0) & (num15 + 1 <= GlobalForm.HLCRange)))
						{
							AddPattern(ArrayTops[i], ArrayBottoms[j], num7, 0, 0, 0, 56, "V-Bot");
							break;
						}
						num21 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, num15 - 1], GlobalForm.nHLC[2, num15 + 1]) < 0, (object)(num15 - 1), (object)(num15 + 1)));
						if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[2, num21], GlobalForm.nHLC[2, num15]), decimal.Divide(decimal.Multiply(3m, num17), new decimal(num18))) <= 0)
						{
							AddPattern(ArrayTops[i], ArrayBottoms[j], num7, 0, 0, 0, 56, "V-Bot");
							break;
						}
					}
					else if (num10 > 65)
					{
						break;
					}
					continue;
					end_IL_04db:
					break;
				}
			}
		}
	}

	private static decimal FindPeakBottomMove(int[] ArrayTops, int[] ArrayBottoms, int TopSize, int BottomSize)
	{
		decimal num = default(decimal);
		decimal num2 = default(decimal);
		checked
		{
			int num3 = TopSize - 1;
			for (int i = 0; i <= num3; i++)
			{
				for (int j = 0; j <= BottomSize && ArrayBottoms[j] <= ArrayTops[i + 1]; j++)
				{
					if (ArrayBottoms[j] > ArrayTops[i])
					{
						decimal num4 = decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[i]], GlobalForm.nHLC[2, ArrayBottoms[j]]);
						num = Conversions.ToDecimal(Interaction.IIf(((decimal.Compare(num4, 0m) > 0) & (decimal.Compare(num4, num) < 0)) | (decimal.Compare(num, 0m) == 0), (object)num4, (object)num));
						num2 = Conversions.ToDecimal(Interaction.IIf((decimal.Compare(num4, 0m) > 0) & (decimal.Compare(num4, num2) > 0), (object)num4, (object)num2));
					}
				}
			}
			num2 = decimal.Divide(num2, GlobalForm.nHLC[1, ArrayTops[TopSize]]);
			num = decimal.Divide(num, GlobalForm.nHLC[1, ArrayTops[TopSize]]);
			if (decimal.Compare(decimal.Subtract(num2, num), 0m) > 0)
			{
				return decimal.Add(num, decimal.Multiply(decimal.Subtract(num2, num), 0.4m));
			}
			return default(decimal);
		}
	}

	private static void FindVTops()
	{
		int num = Conversions.ToInteger(Interaction.IIf(GlobalForm.StrictPatterns, (object)15, (object)7));
		FindAllTops(2);
		int num2 = Information.UBound((Array)ArrayTops, 1);
		if (num2 == 0)
		{
			return;
		}
		FindAllBottoms(3);
		int num3 = Information.UBound((Array)ArrayBottoms, 1);
		if (num3 < 2)
		{
			return;
		}
		decimal num4 = FindBottomPeakMove(ArrayTops, ArrayBottoms, num2, num3);
		if ((decimal.Compare(num4, 0.069m) > 0) | (decimal.Compare(num4, 0m) == 0))
		{
			num4 = 0.069m;
		}
		int num5 = num3;
		checked
		{
			for (int i = 0; i <= num5; i++)
			{
				int num6 = num2;
				for (int j = 1; j <= num6; j++)
				{
					if (!((ArrayTops[j - 1] < ArrayBottoms[i]) & (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[j - 1]], GlobalForm.nHLC[2, ArrayBottoms[i]]) > 0) & (ArrayTops[j] > ArrayBottoms[i]) & (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[i]], GlobalForm.nHLC[1, ArrayTops[j]]) < 0)))
					{
						continue;
					}
					int num7 = i + 1;
					if (num7 > num3 || ArrayTops[j] >= ArrayBottoms[num7])
					{
						break;
					}
					double num8 = Convert.ToDouble(GlobalForm.nHLC[1, ArrayTops[j]]) - Convert.ToDouble(decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[2, ArrayBottoms[i]])) * 0.382;
					num7 = -1;
					int num9 = ArrayTops[j] + 1;
					int hLCRange = GlobalForm.HLCRange;
					for (int k = num9; k <= hLCRange; k++)
					{
						if (Convert.ToDouble(GlobalForm.nHLC[2, k]) <= num8)
						{
							num7 = k;
							break;
						}
					}
					if (num7 == -1)
					{
						break;
					}
					int num10 = num7 - ArrayBottoms[i];
					if (unchecked(num10 >= num && num10 <= 65))
					{
						if (decimal.Compare(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[2, ArrayBottoms[i]]), GlobalForm.nHLC[2, ArrayBottoms[i]]), num4) < 0)
						{
							continue;
						}
						int num11 = ArrayTops[j] + 1;
						int num12 = num7;
						for (int k = num11; k <= num12; k++)
						{
							if (decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, ArrayTops[j]]) > 0)
							{
								goto end_IL_04d8;
							}
						}
						int num13 = ArrayBottoms[i] + 1;
						int num14 = ArrayTops[j] - 1;
						for (int k = num13; k <= num14; k++)
						{
							if (decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, ArrayBottoms[i]]) < 0)
							{
								goto end_IL_04d8;
							}
						}
						int num15 = ArrayTops[j];
						int num16 = ((num15 - 30 >= 0) ? (num15 - 30) : 0);
						decimal num17 = default(decimal);
						int num18 = 0;
						int num19 = num16 + 1;
						int num20 = num15 - 2;
						int num21;
						for (int k = num19; k <= num20; k++)
						{
							if ((decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, k - 1]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, k + 1]) > 0))
							{
								num21 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, k - 1], GlobalForm.nHLC[1, k + 1]) > 0, (object)(k - 1), (object)(k + 1)));
								num17 = decimal.Subtract(decimal.Add(num17, GlobalForm.nHLC[1, k]), GlobalForm.nHLC[1, num21]);
								num18++;
							}
						}
						if (!((num18 != 0) & (num15 + 1 <= GlobalForm.HLCRange)))
						{
							AddPattern(ArrayBottoms[i], ArrayTops[j], num7, 0, 0, 0, 55, "V-Top");
							break;
						}
						num21 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, num15 - 1], GlobalForm.nHLC[1, num15 + 1]) > 0, (object)(num15 - 1), (object)(num15 + 1)));
						if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num15], GlobalForm.nHLC[1, num21]), decimal.Divide(decimal.Multiply(3m, num17), new decimal(num18))) <= 0)
						{
							AddPattern(ArrayBottoms[i], ArrayTops[j], num7, 0, 0, 0, 55, "V-Top");
							break;
						}
					}
					else if (num10 > 65)
					{
						break;
					}
					continue;
					end_IL_04d8:
					break;
				}
			}
		}
	}

	private static decimal FindBottomPeakMove(int[] ArrayTops, int[] ArrayBottoms, int TopSize, int BottomSize)
	{
		decimal num = default(decimal);
		decimal num2 = default(decimal);
		checked
		{
			int num3 = BottomSize - 1;
			for (int i = 0; i <= num3; i++)
			{
				for (int j = 0; j <= TopSize && ArrayTops[j] <= ArrayBottoms[i + 1]; j++)
				{
					if (ArrayTops[j] > ArrayBottoms[i])
					{
						decimal num4 = decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[2, ArrayBottoms[i]]);
						num = Conversions.ToDecimal(Interaction.IIf(((decimal.Compare(num4, 0m) > 0) & (decimal.Compare(num4, num) < 0)) | (decimal.Compare(num, 0m) == 0), (object)num4, (object)num));
						num2 = Conversions.ToDecimal(Interaction.IIf((decimal.Compare(num4, 0m) > 0) & (decimal.Compare(num4, num2) > 0), (object)num4, (object)num2));
					}
				}
			}
			num2 = decimal.Divide(num2, GlobalForm.nHLC[1, ArrayTops[TopSize]]);
			num = decimal.Divide(num, GlobalForm.nHLC[1, ArrayTops[TopSize]]);
			if (decimal.Compare(decimal.Subtract(num2, num), 0m) > 0)
			{
				return decimal.Multiply(num2, 0.4m);
			}
			return default(decimal);
		}
	}

	private static void FindWedges(int Flag)
	{
		decimal d = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.06, (object)0.01));
		int[,] array = new int[3, 1];
		decimal[] array2 = new decimal[1];
		string pText = Conversions.ToString(Interaction.IIf(Flag == 92, (object)"RW", (object)"FW"));
		int num = default(int);
		switch (Flag)
		{
		case 92:
			num = 1;
			break;
		case 96:
			num = -1;
			break;
		}
		int num2 = TrendLines(-1, num, 126, 0.2m, 3, Special: true);
		checked
		{
			if (num2 > 0)
			{
				array = new int[3, Information.UBound((Array)TLArray, 2) + 1];
				array2 = new decimal[Information.UBound((Array)TLArray, 2) + 1];
				int num3 = 0;
				int num4 = Information.UBound((Array)TLArray, 2);
				for (num2 = 0; num2 <= num4; num2++)
				{
					if (((num == 1) & (decimal.Compare(TLSlopeArray[num2], 0.01m) >= 0)) | ((num == -1) & (decimal.Compare(TLSlopeArray[num2], decimal.Multiply(-1m, d)) <= 0)))
					{
						array[0, num3] = TLArray[0, num2];
						array[1, num3] = TLArray[1, num2];
						array[2, num3] = TLArray[2, num2];
						array2[num3] = TLSlopeArray[num2];
						num3++;
					}
				}
				if (num3 <= 0)
				{
					return;
				}
				array = (int[,])Utils.CopyArray((Array)array, (Array)new int[3, num3 - 1 + 1]);
				num2 = TrendLines(1, num, 126, 0.2m, 3, Special: true);
				if (num2 > 0)
				{
					int num5 = Information.UBound((Array)array, 2);
					for (num2 = 0; num2 <= num5; num2++)
					{
						int num6 = Information.UBound((Array)TLArray, 2);
						for (num3 = 0; num3 <= num6; num3++)
						{
							if (!(((num == 1) & (decimal.Compare(TLSlopeArray[num3], 0.01m) >= 0)) | ((num == -1) & (decimal.Compare(TLSlopeArray[num3], decimal.Multiply(-1m, d)) <= 0))))
							{
								continue;
							}
							int num7 = TLArray[0, num3];
							int iSDate = num7;
							int num8 = TLArray[1, num3];
							int iEndDate = num8;
							int num9 = array[0, num2];
							int num10 = array[1, num2];
							int num11 = num8 - num7;
							int num12 = num10 - num9;
							num11 = Conversions.ToInteger(Interaction.IIf(num11 < num12, (object)num12, (object)num11));
							num11 = Convert.ToInt32(decimal.Multiply(new decimal(num11), 0.57m));
							if (!unchecked(num9 >= num7 && num10 <= num8))
							{
								continue;
							}
							if (decimal.Compare(new decimal(num10 - num9), decimal.Multiply(new decimal(num8 - num7), 0.57m)) >= 0)
							{
								if (FWVerify(num2, num3, Flag, array2))
								{
									AddPattern(iSDate, 0, iEndDate, num9, 0, num10, Flag, pText);
									break;
								}
							}
							else
							{
								if (!unchecked(num9 <= num7 && num10 >= num8))
								{
									continue;
								}
								if (decimal.Compare(new decimal(num8 - num7), decimal.Multiply(new decimal(num10 - num9), 0.57m)) >= 0)
								{
									if (FWVerify(num2, num3, Flag, array2))
									{
										AddPattern(iSDate, 0, iEndDate, num9, 0, num10, Flag, pText);
										break;
									}
								}
								else
								{
									if (!unchecked(num9 >= num7 && num10 >= num8 && num9 < num8))
									{
										continue;
									}
									if (num8 - num9 > num11)
									{
										if (FWVerify(num2, num3, Flag, array2))
										{
											AddPattern(iSDate, 0, iEndDate, num9, 0, num10, Flag, pText);
											break;
										}
									}
									else if (unchecked(num9 <= num7 && num10 <= num8 && num10 > num7) && num10 - num7 > num11 && FWVerify(num2, num3, Flag, array2))
									{
										AddPattern(iSDate, 0, iEndDate, num9, 0, num10, Flag, pText);
										break;
									}
								}
							}
						}
					}
				}
			}
			array = null;
			TLArray = null;
		}
	}

	private static decimal FindWideRange(int i)
	{
		if (i < 21)
		{
			return -1m;
		}
		decimal d = default(decimal);
		checked
		{
			int num = i - 21;
			for (int j = i; j >= num; j += -1)
			{
				d = decimal.Subtract(decimal.Add(d, GlobalForm.nHLC[1, j]), GlobalForm.nHLC[2, j]);
			}
			return decimal.Divide(d, 22m);
		}
	}

	private static void FindVerticalRunDown()
	{
		int num = 2;
		int num2 = 0;
		int num3 = 0;
		int num4 = 0;
		checked
		{
			if (!GlobalForm.StrictPatterns)
			{
				int chartStartIndex = GlobalForm.ChartStartIndex;
				int num5 = GlobalForm.ChartEndIndex - 1;
				for (int i = chartStartIndex; i <= num5; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i + 1]) > 0)
					{
						if (decimal.Compare(CalcOverlap(i, -1), 0.25m) <= 0)
						{
							num2++;
							if (num2 == 1)
							{
								num3 = 0;
								num2++;
								num4 = i;
							}
							continue;
						}
						if (decimal.Compare(GlobalForm.nHLC[1, num4], GlobalForm.nHLC[1, i]) < 0)
						{
							num3 = 0;
							num2++;
							num4 = i;
							continue;
						}
						if (num2 > 0)
						{
							num3++;
						}
						if (num3 > num)
						{
							if (num2 >= 4)
							{
								CheckVerticalDown(num4, i, 0.25m);
							}
							num3 = 0;
							num2 = 0;
						}
						continue;
					}
					if (decimal.Compare(GlobalForm.nHLC[1, num4], GlobalForm.nHLC[1, i]) < 0)
					{
						num3 = 0;
						num2++;
						num4 = i;
						continue;
					}
					if (num2 > 0)
					{
						num3++;
					}
					if (num3 > num)
					{
						if (num2 >= 4)
						{
							CheckVerticalDown(num4, i, 0.25m);
						}
						num3 = 0;
						num2 = 0;
					}
				}
				return;
			}
			num2 = 0;
			int chartStartIndex2 = GlobalForm.ChartStartIndex;
			int num6 = GlobalForm.ChartEndIndex - 1;
			for (int i = chartStartIndex2; i <= num6; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i + 1]) > 0)
				{
					if (decimal.Compare(CalcOverlap(i, -1), 0.25m) <= 0)
					{
						num2++;
						continue;
					}
					if (num2 >= 4)
					{
						AddPattern(i - num2, 0, i, 0, 0, 0, 24, "VRD");
					}
					num2 = 0;
				}
				else
				{
					if (num2 >= 4)
					{
						AddPattern(i - num2, 0, i, 0, 0, 0, 24, "VRD");
					}
					num2 = 0;
				}
			}
		}
	}

	private static void CheckVerticalDown(int iRunStart, int iEndRun, decimal MaxOverlap)
	{
		checked
		{
			int num = default(int);
			for (int i = iRunStart; i <= iEndRun; i++)
			{
				if (decimal.Compare(CalcOverlap(i, -1), MaxOverlap) <= 0)
				{
					num = i;
					break;
				}
			}
			int num2 = iEndRun + 1;
			int num3 = num + 1;
			int num4 = default(int);
			for (int i = num2; i >= num3; i += -1)
			{
				if (decimal.Compare(CalcOverlap(i - 1, -1), MaxOverlap) <= 0)
				{
					num4 = i;
					break;
				}
			}
			int num5 = num4 + 1;
			int hLCRange = GlobalForm.HLCRange;
			for (int i = num5; i <= hLCRange && ((decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i]) > 0)); i++)
			{
				num4 = i;
			}
			int num6 = num + 1;
			int num7 = num4;
			for (int i = num6; i <= num7; i++)
			{
				if ((decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i]) < 0))
				{
					num4 = i - 1;
					break;
				}
			}
			if (1 + num4 - num < 4)
			{
				return;
			}
			int num8 = 0;
			int num9 = num;
			int num10 = num4;
			for (int i = num9; i <= num10; i++)
			{
				if (decimal.Compare(CalcOverlap(i, -1), MaxOverlap) > 0)
				{
					num8++;
				}
			}
			if (num4 - num + 1 - num8 > 2)
			{
				AddPattern(num, 0, num4, 0, 0, 0, 24, "VRD");
			}
		}
	}

	private static decimal CalcOverlap(int iStart, int Direction)
	{
		checked
		{
			decimal result;
			if (iStart + 1 < GlobalForm.HLCRange)
			{
				int num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, iStart], GlobalForm.nHLC[1, iStart + 1]) >= 0, (object)(-1), (object)1));
				decimal num2 = decimal.Subtract(GlobalForm.nHLC[1, iStart], GlobalForm.nHLC[2, iStart]);
				if (decimal.Compare(num2, 0m) == 0)
				{
					result = ((!((decimal.Compare(GlobalForm.nHLC[1, iStart], GlobalForm.nHLC[1, iStart + 1]) <= 0) & (decimal.Compare(GlobalForm.nHLC[1, iStart], GlobalForm.nHLC[2, iStart + 1]) >= 0))) ? default(decimal) : 100m);
				}
				else
				{
					switch (num)
					{
					case -1:
						if (Direction == -1)
						{
							return decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iStart + 1], GlobalForm.nHLC[2, iStart]), num2);
						}
						result = 100m;
						break;
					case 1:
						if (Direction == 1)
						{
							return decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iStart], GlobalForm.nHLC[2, iStart + 1]), num2);
						}
						result = 100m;
						break;
					default:
						result = 100m;
						break;
					}
				}
			}
			else
			{
				result = 100m;
			}
			return result;
		}
	}

	private static void FindVerticalRunUp()
	{
		int num = 2;
		int num2 = 0;
		int num3 = 0;
		int num4 = 0;
		checked
		{
			if (!GlobalForm.StrictPatterns)
			{
				int chartStartIndex = GlobalForm.ChartStartIndex;
				int num5 = GlobalForm.ChartEndIndex - 1;
				for (int i = chartStartIndex; i <= num5; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i + 1]) < 0)
					{
						if (decimal.Compare(CalcOverlap(i, 1), 0.25m) <= 0)
						{
							num2++;
							if (num2 == 1)
							{
								num3 = 0;
								num2++;
								num4 = i;
							}
							continue;
						}
						if (decimal.Compare(GlobalForm.nHLC[1, num4], GlobalForm.nHLC[1, i]) > 0)
						{
							num3 = 0;
							num2++;
							num4 = i;
							continue;
						}
						if (num2 > 0)
						{
							num3++;
						}
						if (num3 > num)
						{
							if (num2 >= 4)
							{
								CheckVerticalUp(num4, i, 0.25m);
							}
							num3 = 0;
							num2 = 0;
						}
						continue;
					}
					if (decimal.Compare(GlobalForm.nHLC[1, num4], GlobalForm.nHLC[1, i]) > 0)
					{
						num3 = 0;
						num2++;
						num4 = i;
						continue;
					}
					if (num2 > 0)
					{
						num3++;
					}
					if (num3 > num)
					{
						if (num2 >= 4)
						{
							CheckVerticalUp(num4, i, 0.25m);
						}
						num3 = 0;
						num2 = 0;
					}
				}
				return;
			}
			num2 = 0;
			int chartStartIndex2 = GlobalForm.ChartStartIndex;
			int num6 = GlobalForm.ChartEndIndex - 1;
			for (int i = chartStartIndex2; i <= num6; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i + 1]) < 0)
				{
					if (decimal.Compare(CalcOverlap(i, 1), 0.25m) <= 0)
					{
						num2++;
						continue;
					}
					if (num2 >= 4)
					{
						AddPattern(i - num2, 0, i, 0, 0, 0, 25, "VRU");
					}
					num2 = 0;
				}
				else
				{
					if (num2 >= 4)
					{
						AddPattern(i - num2, 0, i, 0, 0, 0, 25, "VRU");
					}
					num2 = 0;
				}
			}
		}
	}

	private static void CheckVerticalUp(int iRunStart, int iEndRun, decimal MaxOverlap)
	{
		checked
		{
			int num = default(int);
			for (int i = iRunStart; i <= iEndRun; i++)
			{
				if (decimal.Compare(CalcOverlap(i, 1), MaxOverlap) <= 0)
				{
					num = i;
					break;
				}
			}
			int num2 = iEndRun + 1;
			int num3 = num + 1;
			int num4 = default(int);
			for (int i = num2; i >= num3; i += -1)
			{
				if (decimal.Compare(CalcOverlap(i - 1, 1), MaxOverlap) <= 0)
				{
					num4 = i;
					break;
				}
			}
			int num5 = num4 + 1;
			int hLCRange = GlobalForm.HLCRange;
			for (int i = num5; i <= hLCRange && ((decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i]) < 0)); i++)
			{
				num4 = i;
			}
			int num6 = num + 1;
			int num7 = num4;
			for (int i = num6; i <= num7; i++)
			{
				if ((decimal.Compare(GlobalForm.nHLC[1, i - 1], GlobalForm.nHLC[1, i]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], GlobalForm.nHLC[2, i]) > 0))
				{
					num4 = i - 1;
					break;
				}
			}
			if (1 + num4 - num < 4)
			{
				return;
			}
			int num8 = 0;
			int num9 = num;
			int num10 = num4;
			for (int i = num9; i <= num10; i++)
			{
				if (decimal.Compare(CalcOverlap(i, 1), MaxOverlap) > 0)
				{
					num8++;
				}
			}
			if (num4 - num + 1 - num8 > 2)
			{
				AddPattern(num, 0, num4, 0, 0, 0, 25, "VRU");
			}
		}
	}

	private static void FindWeeklyReversals(int iType)
	{
		checked
		{
			if (iType == 53)
			{
				int num = GlobalForm.ChartStartIndex + 1;
				int chartEndIndex = GlobalForm.ChartEndIndex;
				for (int i = num; i <= chartEndIndex; i++)
				{
					if (((decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, i - 1]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, i - 1]) < 0) & (decimal.Compare(GlobalForm.nHLC[3, i], GlobalForm.nHLC[2, i - 1]) < 0)) && HLRegression(i - 1, 2, 5) == 1)
					{
						AddPattern(i - 1, 0, i, 0, 0, 0, 53, "WRT");
					}
				}
				return;
			}
			int num2 = GlobalForm.ChartStartIndex + 1;
			int chartEndIndex2 = GlobalForm.ChartEndIndex;
			for (int j = num2; j <= chartEndIndex2; j++)
			{
				if (((decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, j - 1]) > 0) & (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, j - 1]) < 0) & (decimal.Compare(GlobalForm.nHLC[3, j], GlobalForm.nHLC[1, j - 1]) > 0)) && HLRegression(j - 1, 2, 5) == -1)
				{
					AddPattern(j - 1, 0, j, 0, 0, 0, 54, "WRB");
				}
			}
		}
	}

	private static void FindWideRangeD()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 2;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[3, i], decimal.Add(GlobalForm.nHLC[2, i], decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.25m))) < 0)
				{
					decimal num2 = FindWideRange(i - 1);
					if (((decimal.Compare(num2, -1m) != 0) & (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), decimal.Multiply(3m, num2)) > 0)) && HLRegression(i - 1, 2, 5) == 1)
					{
						AddPattern(i, 0, i, 0, 0, 0, 39, "w");
					}
				}
			}
		}
	}

	private static void FindWideRangeU()
	{
		checked
		{
			int num = GlobalForm.ChartStartIndex + 2;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num; i <= chartEndIndex; i++)
			{
				if (decimal.Compare(GlobalForm.nHLC[3, i], decimal.Subtract(GlobalForm.nHLC[1, i], decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 0.25m))) > 0)
				{
					decimal num2 = FindWideRange(i - 1);
					if (((decimal.Compare(num2, -1m) != 0) & (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), decimal.Multiply(3m, num2)) > 0)) && HLRegression(i - 1, 2, 5) == -1)
					{
						AddPattern(i, 0, i, 0, 0, 0, 38, "W");
					}
				}
			}
		}
	}

	private static void FindWolfeWave(int Flag)
	{
		_ = new object[6];
		FindAllTops(3);
		int num = Information.UBound((Array)ArrayTops, 1);
		if (num < 2)
		{
			return;
		}
		FindAllBottoms(3);
		int num2 = Information.UBound((Array)ArrayBottoms, 1);
		if (num2 < 2)
		{
			return;
		}
		checked
		{
			switch (Flag)
			{
			case 26:
			{
				int num20 = num;
				for (int i = 0; i <= num20; i++)
				{
					int num4 = ArrayTops[i];
					int num21 = num2;
					for (int j = 1; j <= num21; j++)
					{
						int num6 = ArrayBottoms[j];
						if (DateTime.Compare(GlobalForm.nDT[0, num6], GlobalForm.nDT[0, num4]) <= 0)
						{
							continue;
						}
						if (decimal.Compare(GlobalForm.nHLC[2, num6], GlobalForm.nHLC[1, num4]) >= 0)
						{
							break;
						}
						for (int k = num4 - 1; k >= 0; k += -1)
						{
							if (decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num6]) >= 0)
							{
								continue;
							}
							int iPoint = k + 1;
							if (FindPoint1(Flag, num2, num, ref iPoint, num4, num6))
							{
								break;
							}
							for (int l = i - 1; l >= 0 && DateTime.Compare(GlobalForm.nDT[0, ArrayTops[l]], GlobalForm.nDT[0, iPoint]) >= 0; l += -1)
							{
								if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[l]], GlobalForm.nHLC[1, num4]) > 0)
								{
									num4 = ArrayTops[l];
								}
							}
							if (iPoint >= num4)
							{
								break;
							}
							int num22 = i + 1;
							int num23 = num;
							for (int l = num22; l <= num23; l++)
							{
								int m;
								for (int num9 = ArrayTops[l]; DateTime.Compare(GlobalForm.nDT[0, num9], GlobalForm.nDT[0, num6]) > 0; num9 = ArrayTops[m])
								{
									if (!((decimal.Compare(GlobalForm.nHLC[1, num9], GlobalForm.nHLC[2, num6]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, num9], GlobalForm.nHLC[1, num4]) < 0)))
									{
										goto end_IL_050b;
									}
									int num24 = j + 1;
									int num25 = num2;
									int num12 = num24;
									int num13;
									while (num12 <= num25)
									{
										num13 = ArrayBottoms[num12];
										if (DateTime.Compare(GlobalForm.nDT[0, num13], GlobalForm.nDT[0, num9]) <= 0)
										{
											num12++;
											continue;
										}
										goto IL_0231;
									}
									goto end_IL_050b;
									IL_0310:
									decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num9], GlobalForm.nHLC[1, num4]), new decimal(num9 - num4));
									decimal num14 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, num6], GlobalForm.nHLC[2, iPoint]), new decimal(num6 - iPoint));
									if (decimal.Compare(d, num14) < 0 && ((num12 - j == 1) & (l - i == 1)) && DateTime.Compare(GlobalForm.nDT[0, ArrayBottoms[j - 1]], GlobalForm.nDT[0, iPoint]) <= 0)
									{
										decimal d2 = decimal.Subtract(GlobalForm.nHLC[2, iPoint], decimal.Multiply(num14, new decimal(iPoint)));
										decimal d3 = decimal.Add(decimal.Multiply(num14, new decimal(num13)), d2);
										decimal d4 = decimal.Subtract(GlobalForm.nHLC[2, num6], decimal.Multiply(d, new decimal(num6)));
										decimal d5 = decimal.Add(decimal.Multiply(d, new decimal(num13)), d4);
										decimal d7 = new decimal(num6 - iPoint);
										if (decimal.Compare(new decimal(num13), decimal.Add(decimal.Multiply(Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)1.5, (object)2)), d7), new decimal(num6))) < 0 && ((decimal.Compare(GlobalForm.nHLC[2, num13], d3) <= 0) & (decimal.Compare(GlobalForm.nHLC[2, num13], d5) >= 0)))
										{
											AddPattern(iPoint, num6, num13, num4, 0, num9, 26, "WW Bu");
										}
									}
									goto end_IL_050b;
									IL_028b:
									int num16;
									int num26 = num16;
									int num27 = num;
									for (m = num26; m <= num27 && DateTime.Compare(GlobalForm.nDT[0, ArrayTops[m]], GlobalForm.nDT[0, num13]) <= 0; m++)
									{
										if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[m]], GlobalForm.nHLC[1, num9]) > 0)
										{
											goto IL_02e4;
										}
									}
									goto IL_0310;
									IL_0231:
									if (decimal.Compare(GlobalForm.nHLC[2, num13], GlobalForm.nHLC[1, num9]) >= 0)
									{
										goto end_IL_050b;
									}
									int num28 = i + 1;
									int num29 = num;
									num16 = num28;
									while (num16 <= num29)
									{
										if (DateTime.Compare(GlobalForm.nDT[0, ArrayTops[num16]], GlobalForm.nDT[0, num6]) <= 0)
										{
											num16++;
											continue;
										}
										goto IL_028b;
									}
									goto IL_0310;
									IL_02e4:;
								}
							}
							break;
						}
						break;
						continue;
						end_IL_050b:
						break;
					}
				}
				break;
			}
			case 27:
			{
				int num3 = num2;
				for (int i = 0; i <= num3; i++)
				{
					int num4 = ArrayBottoms[i];
					int num5 = num;
					for (int j = 1; j <= num5; j++)
					{
						int num6 = ArrayTops[j];
						if (DateTime.Compare(GlobalForm.nDT[0, num6], GlobalForm.nDT[0, num4]) <= 0)
						{
							continue;
						}
						if (decimal.Compare(GlobalForm.nHLC[1, num6], GlobalForm.nHLC[2, num4]) <= 0)
						{
							break;
						}
						for (int k = num4 - 1; k >= 0; k += -1)
						{
							if (decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, num6]) <= 0)
							{
								continue;
							}
							int iPoint = k + 1;
							if (FindPoint1(Flag, num2, num, ref iPoint, num4, num6))
							{
								break;
							}
							for (int l = i - 1; l >= 0 && DateTime.Compare(GlobalForm.nDT[0, ArrayBottoms[l]], GlobalForm.nDT[0, iPoint]) >= 0; l += -1)
							{
								if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[l]], GlobalForm.nHLC[2, num4]) < 0)
								{
									num4 = ArrayBottoms[l];
								}
							}
							if (iPoint >= num4)
							{
								break;
							}
							int num7 = i + 1;
							int num8 = num2;
							for (int l = num7; l <= num8; l++)
							{
								int m;
								for (int num9 = ArrayBottoms[l]; DateTime.Compare(GlobalForm.nDT[0, num9], GlobalForm.nDT[0, num6]) > 0; num9 = ArrayBottoms[m])
								{
									if (!((decimal.Compare(GlobalForm.nHLC[2, num9], GlobalForm.nHLC[1, num6]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, num9], GlobalForm.nHLC[2, num4]) > 0)))
									{
										goto end_IL_09f2;
									}
									int num10 = j + 1;
									int num11 = num;
									int num12 = num10;
									int num13;
									while (num12 <= num11)
									{
										num13 = ArrayTops[num12];
										if (DateTime.Compare(GlobalForm.nDT[0, num13], GlobalForm.nDT[0, num9]) <= 0)
										{
											num12++;
											continue;
										}
										goto IL_0718;
									}
									goto end_IL_09f2;
									IL_07f7:
									decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, num9], GlobalForm.nHLC[2, num4]), new decimal(num9 - num4));
									decimal num14 = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num6], GlobalForm.nHLC[1, iPoint]), new decimal(num6 - iPoint));
									if (decimal.Compare(d, num14) > 0 && ((num12 - j == 1) & (l - i == 1)) && DateTime.Compare(GlobalForm.nDT[0, ArrayTops[j - 1]], GlobalForm.nDT[0, iPoint]) <= 0)
									{
										decimal d2 = decimal.Subtract(GlobalForm.nHLC[1, iPoint], decimal.Multiply(num14, new decimal(iPoint)));
										decimal d3 = decimal.Add(decimal.Multiply(num14, new decimal(num13)), d2);
										decimal d4 = decimal.Subtract(GlobalForm.nHLC[1, num6], decimal.Multiply(d, new decimal(num6)));
										decimal d5 = decimal.Add(decimal.Multiply(d, new decimal(num13)), d4);
										decimal d6 = new decimal(num6 - iPoint);
										if (decimal.Compare(new decimal(num13), decimal.Add(decimal.Multiply(Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)1.5, (object)2)), d6), new decimal(num6))) < 0 && ((decimal.Compare(GlobalForm.nHLC[1, num13], d3) >= 0) & (decimal.Compare(GlobalForm.nHLC[1, num13], d5) <= 0)))
										{
											AddPattern(iPoint, num6, num13, num4, 0, num9, 27, "WW Be");
										}
									}
									goto end_IL_09f2;
									IL_0772:
									int num16;
									int num15 = num16;
									int num17 = num2;
									for (m = num15; m <= num17 && DateTime.Compare(GlobalForm.nDT[0, ArrayBottoms[m]], GlobalForm.nDT[0, num13]) <= 0; m++)
									{
										if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[m]], GlobalForm.nHLC[2, num9]) < 0)
										{
											goto IL_07cb;
										}
									}
									goto IL_07f7;
									IL_0718:
									if (decimal.Compare(GlobalForm.nHLC[1, num13], GlobalForm.nHLC[2, num9]) <= 0)
									{
										goto end_IL_09f2;
									}
									int num18 = i + 1;
									int num19 = num2;
									num16 = num18;
									while (num16 <= num19)
									{
										if (DateTime.Compare(GlobalForm.nDT[0, ArrayBottoms[num16]], GlobalForm.nDT[0, num6]) <= 0)
										{
											num16++;
											continue;
										}
										goto IL_0772;
									}
									goto IL_07f7;
									IL_07cb:;
								}
							}
							break;
						}
						break;
						continue;
						end_IL_09f2:
						break;
					}
				}
				break;
			}
			}
		}
	}

	private static bool FindPoint1(int Flag, int BottomSize, int TopSize, ref int iPoint1, int iPoint2, int iPoint3)
	{
		bool result = true;
		checked
		{
			if (Flag == 26)
			{
				for (int i = 1; i <= BottomSize; i++)
				{
					if (DateTime.Compare(GlobalForm.nDT[0, ArrayBottoms[i]], GlobalForm.nDT[0, iPoint2]) > 0)
					{
						if (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[i - 1]], GlobalForm.nHLC[2, iPoint3]) > 0)
						{
							iPoint1 = ArrayBottoms[i - 1];
							result = false;
						}
						break;
					}
				}
			}
			else
			{
				for (int i = 1; i <= TopSize; i++)
				{
					if (DateTime.Compare(GlobalForm.nDT[0, ArrayTops[i]], GlobalForm.nDT[0, iPoint2]) > 0)
					{
						if (decimal.Compare(GlobalForm.nHLC[1, ArrayTops[i - 1]], GlobalForm.nHLC[1, iPoint3]) < 0)
						{
							iPoint1 = ArrayTops[i - 1];
							result = false;
						}
						break;
					}
				}
			}
			return result;
		}
	}

	private static bool FRVerify(int PatternType, int StartIndex, int EndIndex, int TopDateStart, int BottomDateStart, int TopDateEnd, int BottomDateEnd)
	{
		int num = Conversions.ToInteger(Interaction.IIf(TopDateStart < BottomDateStart, (object)TopDateStart, (object)BottomDateStart));
		if (checked(Conversions.ToInteger(Interaction.IIf(TopDateEnd > BottomDateEnd, (object)TopDateEnd, (object)BottomDateEnd)) - num) <= 15)
		{
			return false;
		}
		int num2 = CheckTrend(StartIndex, EndIndex, 1);
		if (num2 == 1 && PatternType == 101)
		{
			return true;
		}
		if (num2 == -1 && PatternType == 102)
		{
			return true;
		}
		return false;
	}

	private static bool FWVerify(int i, int j, int Flag, decimal[] SlopeBot)
	{
		decimal d = Math.Abs(TLSlopeArray[j]);
		decimal d2 = Math.Abs(SlopeBot[i]);
		bool result = false;
		switch (Flag)
		{
		case 92:
			if (decimal.Compare(d2, decimal.Add(d, 0.04m)) > 0)
			{
				result = true;
			}
			break;
		case 96:
			if (decimal.Compare(d2, decimal.Subtract(d, 0.04m)) < 0)
			{
				result = true;
			}
			break;
		}
		return result;
	}

	private static decimal GetPercent(decimal Percent)
	{
		if (GlobalForm.Futures)
		{
			return decimal.Divide(Percent, 4m);
		}
		if (GlobalForm.NearFutures)
		{
			return decimal.Divide(Percent, 2m);
		}
		if (!GlobalForm.StrictPatterns)
		{
			decimal d = Percent;
			Percent = ((decimal.Compare(d, 0m) < 0 || decimal.Compare(d, 1m) > 0) ? decimal.Multiply(Percent, 1.5m) : decimal.Multiply(Percent, 2m));
		}
		return Percent;
	}

	public static decimal GetPriceScale(decimal Bottom1, decimal Bottom2)
	{
		if (decimal.Compare(decimal.Add(Bottom1, Bottom2), 0m) != 0)
		{
			return decimal.Divide(decimal.Divide(decimal.Add(Bottom1, Bottom2), 2m), 40m);
		}
		if (decimal.Compare(Bottom1, 0m) > 0)
		{
			return decimal.Divide(Bottom1, 40m);
		}
		return decimal.Divide(Bottom2, 40m);
	}

	public static int HLRegression(int iEnd, int DayWk, int LOOKBACK)
	{
		//IL_0088: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			int num = iEnd - (LOOKBACK - 1);
			int result;
			if (unchecked(num < 0 || iEnd < 0))
			{
				result = 0;
			}
			else
			{
				int num2 = 1;
				double num3 = 0.0;
				double num4 = 0.0;
				double num5 = 0.0;
				double num6 = 0.0;
				float num7 = default(float);
				for (int i = num; i <= iEnd; i++)
				{
					switch (DayWk)
					{
					case 0:
						num7 = Convert.ToSingle(decimal.Subtract(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]));
						break;
					case -1:
						Interaction.MsgBox((object)"Error in HLRegression.", (MsgBoxStyle)0, (object)null);
						break;
					case 2:
						num7 = Convert.ToSingle(decimal.Divide(decimal.Add(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, i]), 2m));
						break;
					case 3:
						num7 = Convert.ToSingle(GlobalForm.nHLC[3, i]);
						break;
					}
					num3 += (double)num2;
					num4 += (double)num7;
					num5 += (double)(num2 * num2);
					num6 += (double)((float)num2 * num7);
					num2++;
				}
				int num8 = num2 - 1;
				float num9 = (((double)num8 * num5 - num3 * num3 == 0.0) ? 0f : ((float)(((double)num8 * num6 - num3 * num4) / ((double)num8 * num5 - num3 * num3))));
				if (num9 < 0f)
				{
					result = -1;
					if (((iEnd + 1 <= GlobalForm.HLCRange) & (iEnd - 1 >= 0)) && ((decimal.Compare(GlobalForm.nHLC[1, iEnd], GlobalForm.nHLC[1, iEnd + 1]) < 0) & (decimal.Compare(GlobalForm.nHLC[1, iEnd - 1], GlobalForm.nHLC[1, iEnd]) < 0)))
					{
						result = 1;
					}
				}
				else if (num9 == 0f)
				{
					result = 0;
				}
				else
				{
					result = 1;
					if (((iEnd + 1 <= GlobalForm.HLCRange) & (iEnd - 1 >= 0)) && ((decimal.Compare(GlobalForm.nHLC[1, iEnd], GlobalForm.nHLC[1, iEnd + 1]) > 0) & (decimal.Compare(GlobalForm.nHLC[1, iEnd - 1], GlobalForm.nHLC[1, iEnd]) > 0)))
					{
						result = -1;
					}
				}
			}
			return result;
		}
	}

	private static bool TBCheckDownTrend(int j, int k)
	{
		int num = ArrayBottoms[j];
		int num2 = ArrayBottoms[k];
		checked
		{
			int num3 = default(int);
			for (int i = num; i <= num2; i++)
			{
				if (i == ArrayBottoms[j])
				{
					num3 = i;
				}
				if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num3]) > 0)
				{
					num3 = i;
				}
			}
			for (int i = ArrayBottoms[j]; i >= 0; i += -1)
			{
				if (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[1, num3]) > 0)
				{
					return false;
				}
				if (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, ArrayBottoms[j]]) < 0)
				{
					return true;
				}
			}
			return false;
		}
	}

	private static int TopCheck(int i, int LastFound, int TLUpDown, decimal MinExcursion, bool Special, int TouchCnt, decimal MaxExcursion, int TLCount, int LinePart)
	{
		decimal d = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.002, (object)0.004));
		if (TLUpDown == 0 && decimal.Compare(decimal.Divide(Math.Abs(decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[i]], GlobalForm.nHLC[1, ArrayTops[LastFound]])), Conversions.ToDecimal(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, ArrayTops[i]], GlobalForm.nHLC[1, ArrayTops[LastFound]]) < 0, (object)GlobalForm.nHLC[1, ArrayTops[i]], (object)GlobalForm.nHLC[1, ArrayTops[LastFound]]))), d) >= 0)
		{
			return TLCount;
		}
		checked
		{
			if (ArrayTops[LastFound] - ArrayTops[i] == 0)
			{
				return TLCount;
			}
			decimal num = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[LastFound]], GlobalForm.nHLC[1, ArrayTops[i]]), new decimal(ArrayTops[LastFound] - ArrayTops[i]));
			if (unchecked(((decimal.Compare(num, 0m) < 0 && TLUpDown == -1) | (decimal.Compare(num, 0m) > 0 && TLUpDown == 1)) || TLUpDown == 0))
			{
				bool flag = false;
				int num2 = ArrayTops[i] + 1;
				int num3 = ArrayTops[LastFound];
				for (int j = num2; j <= num3; j++)
				{
					decimal point = decimal.Add(decimal.Multiply(num, new decimal(j - ArrayTops[i])), GlobalForm.nHLC[1, ArrayTops[i]]);
					if (CheckOneNear(GlobalForm.nHLC[1, j], point, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)MinExcursion, (object)MaxExcursion))))
					{
						return TLCount;
					}
				}
				if (!flag)
				{
					bool flag2 = default(bool);
					if (unchecked(Special && TouchCnt > 2))
					{
						if (LinePart == 0)
						{
							return TLCount;
						}
						int num4 = (int)Math.Round((double)(ArrayTops[LastFound] - ArrayTops[i]) / (double)LinePart);
						int num5 = ArrayTops[i] + num4;
						int num6 = ArrayTops[LastFound] - num4;
						flag2 = false;
						int num7 = num6;
						for (int k = num5; k <= num7; k++)
						{
							decimal point = decimal.Add(decimal.Multiply(num, new decimal(k - ArrayTops[i])), GlobalForm.nHLC[1, ArrayTops[i]]);
							if (CheckNearness(GlobalForm.nHLC[1, k], point, -1m, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)MinExcursion, (object)MaxExcursion))))
							{
								flag2 = true;
								break;
							}
						}
					}
					if (unchecked((Special && (TouchCnt == 2 || flag2)) || !Special))
					{
						int iStart = ArrayTops[i];
						int iEnd = ArrayTops[LastFound];
						if (!DupCheck(TLCount, iStart, iEnd))
						{
							TLArray = (int[,])Utils.CopyArray((Array)TLArray, (Array)new int[3, TLCount + 1]);
							TLSlopeArray = (decimal[])Utils.CopyArray((Array)TLSlopeArray, (Array)new decimal[TLCount + 1]);
							TLArray[0, TLCount] = ArrayTops[i];
							TLArray[1, TLCount] = ArrayTops[LastFound];
							TLArray[2, TLCount] = TouchCnt;
							TLSlopeArray[TLCount] = num;
							TLCount++;
						}
					}
				}
			}
			return TLCount;
		}
	}

	public static int TrendLines(int TLTopsBots, int TLUpDown, int MaxLength, decimal MaxExcursion, int Touches, bool Special)
	{
		TLArray = null;
		TLSlopeArray = null;
		bool flag = false;
		int num = 0;
		checked
		{
			if (TLTopsBots == 1)
			{
				FindAllTops(2);
				decimal num2;
				decimal num3;
				if (Information.UBound((Array)ArrayTops, 1) > 0)
				{
					if ((decimal.Compare(GlobalForm.nHLC[1, ArrayTops[0]], 5m) < 0) & (decimal.Compare(GlobalForm.nHLC[2, ArrayTops[ArrayTops.Length - 1]], 5m) < 0))
					{
						decimal priceScale = GetPriceScale(GlobalForm.nHLC[1, ArrayTops[0]], GlobalForm.nHLC[1, ArrayTops[0]]);
						num2 = decimal.Multiply(0.13m, priceScale);
						num3 = decimal.Multiply(MaxExcursion, priceScale);
						flag = true;
					}
					else
					{
						num2 = 0.13m;
						num3 = MaxExcursion;
					}
				}
				num2 = 0.13m;
				num3 = MaxExcursion;
				while (true)
				{
					int num4 = Information.UBound((Array)ArrayTops, 1);
					for (int i = 0; i <= num4; i++)
					{
						int num5 = i + 1;
						int num6 = Information.UBound((Array)ArrayTops, 1);
						for (int j = num5; j <= num6 && ArrayTops[j] - ArrayTops[i] <= MaxLength; j++)
						{
							if (ArrayTops[j] - ArrayTops[i] == 0)
							{
								return num;
							}
							if ((TLUpDown != 0) & (CheckSlope(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[1, ArrayTops[i]], 0.005m) == 0))
							{
								continue;
							}
							decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[1, ArrayTops[i]]), new decimal(ArrayTops[j] - ArrayTops[i]));
							if (!unchecked(((decimal.Compare(d, 0m) < 0 && TLUpDown == -1) | (decimal.Compare(d, 0m) > 0 && TLUpDown == 1)) || TLUpDown == 0))
							{
								continue;
							}
							int lastFound = j;
							int num7 = 0;
							int num8 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[1, ArrayTops[i]]) > 0, (object)ArrayTops[j], (object)ArrayTops[i]));
							int num9 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, ArrayTops[j]], GlobalForm.nHLC[1, ArrayTops[i]]) < 0, (object)ArrayTops[j], (object)ArrayTops[i]));
							decimal.Subtract(GlobalForm.nHLC[1, num8], GlobalForm.nHLC[1, num9]);
							int num10 = i;
							int num11 = j;
							for (int k = num10; k <= num11 && ArrayTops[k] - ArrayTops[i] <= MaxLength; k++)
							{
								decimal point = decimal.Add(decimal.Multiply(d, new decimal(ArrayTops[k] - ArrayTops[i])), GlobalForm.nHLC[1, ArrayTops[i]]);
								if (CheckNearness(GlobalForm.nHLC[1, ArrayTops[k]], point, -1m, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)num2, (object)num3))))
								{
									lastFound = k;
									num7++;
								}
								else if (CheckOneNear(GlobalForm.nHLC[1, ArrayTops[k]], point, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)num2, (object)num3))))
								{
									break;
								}
							}
							if (num7 >= Touches)
							{
								num = TopCheck(i, lastFound, TLUpDown, num2, Special, num7, num3, num, 3);
							}
						}
					}
					if (!unchecked(num < 5 && flag))
					{
						break;
					}
					flag = false;
					num2 = 0.13m;
					num3 = MaxExcursion;
				}
			}
			else
			{
				FindAllBottoms(2);
				decimal num2 = default(decimal);
				decimal num3 = default(decimal);
				if (Information.UBound((Array)ArrayBottoms, 1) > 0)
				{
					if ((decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[0]], 5m) < 0) & (decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[ArrayBottoms.Length - 1]], 5m) < 0))
					{
						decimal priceScale2 = GetPriceScale(GlobalForm.nHLC[2, ArrayBottoms[0]], GlobalForm.nHLC[2, ArrayBottoms[0]]);
						num2 = decimal.Multiply(0.13m, priceScale2);
						num3 = decimal.Multiply(MaxExcursion, priceScale2);
						flag = true;
					}
					else
					{
						num2 = 0.13m;
						num3 = MaxExcursion;
					}
				}
				while (true)
				{
					int num12 = Information.UBound((Array)ArrayBottoms, 1);
					for (int i = 0; i <= num12; i++)
					{
						int num13 = i + 1;
						int num14 = Information.UBound((Array)ArrayBottoms, 1);
						for (int j = num13; j <= num14 && ArrayBottoms[j] - ArrayBottoms[i] <= MaxLength; j++)
						{
							if (ArrayBottoms[j] - ArrayBottoms[i] == 0)
							{
								return num;
							}
							decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, ArrayBottoms[j]], GlobalForm.nHLC[2, ArrayBottoms[i]]), new decimal(ArrayBottoms[j] - ArrayBottoms[i]));
							if (((TLUpDown != 0) & (CheckSlope(GlobalForm.nHLC[2, ArrayBottoms[j]], GlobalForm.nHLC[2, ArrayBottoms[i]], 0.005m) == 0)) || !unchecked(((decimal.Compare(d, 0m) < 0 && TLUpDown == -1) | (decimal.Compare(d, 0m) > 0 && TLUpDown == 1)) || TLUpDown == 0))
							{
								continue;
							}
							int lastFound = j;
							int num7 = 0;
							int num8 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[j]], GlobalForm.nHLC[2, ArrayBottoms[i]]) > 0, (object)ArrayBottoms[j], (object)ArrayBottoms[i]));
							int num9 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, ArrayBottoms[j]], GlobalForm.nHLC[2, ArrayBottoms[i]]) < 0, (object)ArrayBottoms[j], (object)ArrayBottoms[i]));
							decimal.Subtract(GlobalForm.nHLC[2, num8], GlobalForm.nHLC[2, num9]);
							int num15 = i;
							int num16 = j;
							for (int k = num15; k <= num16 && ArrayBottoms[k] - ArrayBottoms[i] <= MaxLength; k++)
							{
								decimal point = decimal.Add(decimal.Multiply(d, new decimal(ArrayBottoms[k] - ArrayBottoms[i])), GlobalForm.nHLC[2, ArrayBottoms[i]]);
								if (CheckNearness(GlobalForm.nHLC[2, ArrayBottoms[k]], point, -1m, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)num2, (object)num3))))
								{
									lastFound = k;
									num7++;
								}
								else if (CheckOneNear(GlobalForm.nHLC[2, ArrayBottoms[k]], point, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)decimal.Negate(num2), (object)decimal.Negate(num3)))))
								{
									break;
								}
							}
							if (num7 >= Touches)
							{
								num = BottomCheck(i, lastFound, TLUpDown, num2, Special, ref num7, num3, num, 3);
							}
						}
					}
					if (!unchecked(num < 5 && flag))
					{
						break;
					}
					flag = false;
					num2 = 0.13m;
					num3 = MaxExcursion;
				}
			}
			return num;
		}
	}

	private static bool TTCheckUpTrend(int iTop1, int iLastTop)
	{
		int num = ArrayTops[iTop1];
		int num2 = ArrayTops[iLastTop];
		checked
		{
			int num3 = default(int);
			for (int i = num; i <= num2; i++)
			{
				if (i == ArrayTops[iTop1])
				{
					num3 = i;
				}
				if (decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num3]) < 0)
				{
					num3 = i;
				}
			}
			for (int i = ArrayTops[iTop1]; i >= 0; i += -1)
			{
				if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, ArrayTops[iTop1]]) > 0)
				{
					return true;
				}
				if (decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[2, num3]) < 0)
				{
					return false;
				}
			}
			return false;
		}
	}

	private static bool Verify(int Flag, int PatternStart)
	{
		if (Flag == 113 || Flag == 112)
		{
			return true;
		}
		int num = CheckTrend(PatternStart, 0, -1);
		if ((Flag == 114 && num == -1) || (Flag == 111 && num == 1))
		{
			return true;
		}
		return false;
	}

	private static bool WhiteSpaceCheck(int iTopStart, int iTopEnd, int iBottomStart, int iBottomEnd)
	{
		decimal num;
		decimal num2;
		if (decimal.Compare(GlobalForm.nHLC[1, iTopStart], 5m) < 0)
		{
			decimal priceScale = GetPriceScale(GlobalForm.nHLC[1, iTopStart], GlobalForm.nHLC[1, iTopEnd]);
			num = decimal.Multiply(0.13m, priceScale);
			num2 = decimal.Multiply(0.25m, priceScale);
		}
		else
		{
			num = 0.13m;
			num2 = 0.25m;
		}
		checked
		{
			int num3 = (int)Math.Round((double)(iTopEnd - iTopStart) * 0.618);
			int num4 = iTopStart;
			bool flag = false;
			if (iTopEnd - iTopStart != 0)
			{
				decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iTopEnd], GlobalForm.nHLC[1, iTopStart]), new decimal(iTopEnd - iTopStart));
				decimal d2 = GlobalForm.nHLC[1, iTopStart];
				for (int i = iTopStart + 1; i <= iTopEnd; i++)
				{
					if (i - num4 >= num3)
					{
						flag = true;
						break;
					}
					decimal point = decimal.Add(decimal.Multiply(d, new decimal(i - iTopStart)), d2);
					if (CheckNearness(GlobalForm.nHLC[1, i], point, -1m, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)num, (object)num2))))
					{
						num4 = i;
					}
				}
			}
			if (!flag)
			{
				num3 = (int)Math.Round((double)(iBottomEnd - iBottomStart) * 0.618);
				num4 = iBottomStart;
				if (iBottomEnd - iBottomStart != 0)
				{
					decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, iBottomEnd], GlobalForm.nHLC[2, iBottomStart]), new decimal(iBottomEnd - iBottomStart));
					decimal d2 = GlobalForm.nHLC[2, iBottomStart];
					for (int i = iBottomStart + 1; i <= iBottomEnd; i++)
					{
						if (i - num4 >= num3)
						{
							flag = true;
							break;
						}
						decimal point = decimal.Add(decimal.Multiply(d, new decimal(i - iBottomStart)), d2);
						if (CheckNearness(GlobalForm.nHLC[2, i], point, -1m, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)num, (object)num2))))
						{
							num4 = i;
						}
					}
				}
			}
			return flag;
		}
	}

	private static bool SymWhiteSpace(int iTopStart, int iTopEnd, int iBottomStart, int iBottomEnd)
	{
		int num = Conversions.ToInteger(Interaction.IIf(iTopStart < iBottomStart, (object)iTopStart, (object)iBottomStart));
		int num2 = Conversions.ToInteger(Interaction.IIf(iTopEnd > iBottomEnd, (object)iTopEnd, (object)iBottomEnd));
		checked
		{
			int num3 = (int)Math.Round((double)(num2 - num) * 0.5);
			decimal dHeight = decimal.Subtract(GlobalForm.nHLC[1, iTopStart], GlobalForm.nHLC[2, iBottomStart]);
			int num4 = iTopStart;
			bool flag = false;
			if (iTopEnd - iTopStart != 0)
			{
				decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iTopEnd], GlobalForm.nHLC[1, iTopStart]), new decimal(iTopEnd - iTopStart));
				decimal d2 = GlobalForm.nHLC[1, iTopStart];
				int num5 = iTopStart + 1;
				int num6 = num2;
				for (int i = num5; i <= num6; i++)
				{
					if (i - num4 >= num3)
					{
						flag = true;
						break;
					}
					decimal dTestPoint = decimal.Add(decimal.Multiply(d, new decimal(i - iTopStart)), d2);
					if (NewCheckNearness(iTopStart, iBottomStart, dHeight, dTestPoint, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.05, (object)0.1)), TestTop: true, i))
					{
						num4 = i;
					}
				}
			}
			if (CheckSlope(GlobalForm.nHLC[1, iTopStart], GlobalForm.nHLC[1, iTopEnd], 0.005m) == 0)
			{
				flag = true;
			}
			if (!flag)
			{
				num4 = iBottomStart;
				if (iBottomEnd - iBottomStart != 0)
				{
					decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, iBottomEnd], GlobalForm.nHLC[2, iBottomStart]), new decimal(iBottomEnd - iBottomStart));
					decimal d2 = GlobalForm.nHLC[2, iBottomStart];
					int num7 = iBottomStart + 1;
					int num8 = num2;
					for (int i = num7; i <= num8; i++)
					{
						if (i - num4 >= num3)
						{
							flag = true;
							break;
						}
						decimal dTestPoint = decimal.Add(decimal.Multiply(d, new decimal(i - iBottomStart)), d2);
						if (NewCheckNearness(iTopStart, iBottomStart, dHeight, dTestPoint, Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.05, (object)0.1)), TestTop: false, i))
						{
							num4 = i;
						}
					}
				}
			}
			if (!flag && CheckSlope(GlobalForm.nHLC[2, iBottomStart], GlobalForm.nHLC[2, iBottomEnd], 0.005m) == 0)
			{
				flag = true;
			}
			return flag;
		}
	}

	private static bool TriangleWhiteSpaceCheck(int iTopStart, int iTopEnd, int iBottomStart, int iBottomEnd, int iType)
	{
		decimal percent = Conversions.ToDecimal(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.05, (object)0.1));
		double num = default(double);
		switch (iType)
		{
		case 89:
			num = Conversions.ToDouble(Interaction.IIf(GlobalForm.StrictPatterns, (object)0.5, (object)0.618));
			break;
		case 88:
			num = 0.707;
			break;
		}
		int num2 = Conversions.ToInteger(Interaction.IIf(iTopStart < iBottomStart, (object)iTopStart, (object)iBottomStart));
		int num3 = Conversions.ToInteger(Interaction.IIf(iTopEnd > iBottomEnd, (object)iTopEnd, (object)iBottomEnd));
		checked
		{
			int num4 = (int)Math.Round((double)(num3 - num2) * num);
			int num5 = num2;
			int num6 = num2;
			int num7 = num2 + 1;
			int num8 = num3;
			for (int i = num7; i <= num8; i++)
			{
				num5 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num5]) > 0, (object)i, (object)num5));
				num6 = Conversions.ToInteger(Interaction.IIf((decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num6]) < 0) & (decimal.Compare(GlobalForm.nHLC[2, i], 0m) > 0), (object)i, (object)num6));
			}
			decimal num9 = decimal.Subtract(GlobalForm.nHLC[1, num5], GlobalForm.nHLC[2, num6]);
			if (decimal.Compare(num9, 0m) == 0)
			{
				return true;
			}
			int num10 = iTopStart;
			bool flag = false;
			if (iTopEnd - iTopStart != 0)
			{
				decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, num3], GlobalForm.nHLC[1, iTopStart]), new decimal(num3 - iTopStart));
				decimal d2 = GlobalForm.nHLC[1, iTopStart];
				int num11 = iTopStart + 1;
				int num12 = num3;
				for (int i = num11; i <= num12; i++)
				{
					if (i - num10 > num4)
					{
						flag = true;
						break;
					}
					decimal dTestPoint = decimal.Add(decimal.Multiply(d, new decimal(i - iTopStart)), d2);
					if (iType == 89)
					{
						if (NewCheckNearness(num5, num6, num9, GlobalForm.nHLC[1, i], percent, TestTop: true, -1))
						{
							num10 = i;
						}
					}
					else if (NewCheckNearness(num5, num6, num9, dTestPoint, percent, TestTop: true, i))
					{
						num10 = i;
					}
				}
			}
			if (!flag)
			{
				num10 = iBottomStart;
				if (iBottomEnd - iBottomStart != 0)
				{
					decimal d = decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, num3], GlobalForm.nHLC[2, iBottomStart]), new decimal(num3 - iBottomStart));
					decimal d2 = GlobalForm.nHLC[2, iBottomStart];
					int num13 = iBottomStart + 1;
					int num14 = num3;
					for (int i = num13; i <= num14; i++)
					{
						if (i - num10 > num4)
						{
							flag = true;
							break;
						}
						decimal dTestPoint = decimal.Add(decimal.Multiply(d, new decimal(i - iBottomStart)), d2);
						if (iType == 89)
						{
							if (NewCheckNearness(num5, num6, num9, dTestPoint, percent, TestTop: false, i))
							{
								num10 = i;
							}
						}
						else if (NewCheckNearness(num5, num6, num9, GlobalForm.nHLC[2, i], percent, TestTop: false, -1))
						{
							num10 = i;
						}
					}
				}
			}
			return Conversions.ToBoolean(Interaction.IIf(false, (object)(!flag), (object)flag));
		}
	}

	private static bool CheckBroadeningSlope(int iTStart, int iTEnd, int iBStart, int iBend)
	{
		int num = Conversions.ToInteger(Interaction.IIf(iTStart < iBStart, (object)iTStart, (object)iBStart));
		int num2 = Conversions.ToInteger(Interaction.IIf(iTEnd > iBend, (object)iTEnd, (object)iBend));
		decimal d;
		if (decimal.Compare(GlobalForm.nHLC[1, iTStart], 5m) < 0)
		{
			decimal priceScale = GetPriceScale(GlobalForm.nHLC[1, iTStart], GlobalForm.nHLC[1, iTEnd]);
			d = decimal.Multiply(0.25m, priceScale);
		}
		else
		{
			d = 0.25m;
		}
		d = decimal.Multiply(d, 2m);
		checked
		{
			int num3 = (int)Math.Round((double)(num + num2) / 2.0);
			int num4 = num;
			int num5 = num3 + 1;
			int num6 = num + 1;
			int num7 = num2;
			int num8 = default(int);
			int num9 = default(int);
			for (int i = num6; i <= num7; i++)
			{
				if (i <= num3)
				{
					num4 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num4]) > 0, (object)i, (object)num4));
					num8 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num8]) < 0, (object)i, (object)num8));
				}
				else
				{
					num5 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, i], GlobalForm.nHLC[1, num5]) > 0, (object)i, (object)num5));
					num9 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, i], GlobalForm.nHLC[2, num9]) < 0, (object)i, (object)num9));
				}
			}
			if ((decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, num4], d), GlobalForm.nHLC[1, num5]) > 0) | (decimal.Compare(decimal.Add(GlobalForm.nHLC[2, num8], d), GlobalForm.nHLC[2, num9]) < 0))
			{
				return Conversions.ToBoolean(Interaction.IIf(false, (object)false, (object)true));
			}
			return Conversions.ToBoolean(Interaction.IIf(false, (object)true, (object)false));
		}
	}

	private static bool AdjustLines(int iTopStart, int iTopEnd, int iBottomStart, int iBottomEnd, int iType)
	{
		if (iType != 113 && iType != 112)
		{
			return false;
		}
		decimal d;
		if (decimal.Compare(GlobalForm.nHLC[1, iTopStart], 5m) < 0)
		{
			decimal priceScale = GetPriceScale(GlobalForm.nHLC[1, iTopStart], GlobalForm.nHLC[1, iTopEnd]);
			d = decimal.Multiply(0.25m, priceScale);
		}
		else
		{
			d = 0.25m;
		}
		d = decimal.Multiply(d, 2m);
		checked
		{
			switch (iType)
			{
			case 113:
			{
				decimal d3 = GlobalForm.nHLC[2, Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, iBottomStart], GlobalForm.nHLC[2, iBottomEnd]) < 0, (object)iBottomStart, (object)iBottomEnd))];
				int num3 = iBottomStart + 1;
				int num4 = iBottomEnd - 1;
				for (int i = num3; i <= num4; i++)
				{
					if (decimal.Compare(decimal.Add(GlobalForm.nHLC[2, i], d), d3) < 0)
					{
						return Conversions.ToBoolean(Interaction.IIf(false, (object)false, (object)true));
					}
				}
				break;
			}
			case 112:
			{
				decimal d2 = GlobalForm.nHLC[1, Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, iTopStart], GlobalForm.nHLC[1, iTopEnd]) > 0, (object)iTopStart, (object)iTopEnd))];
				int num = iTopStart + 1;
				int num2 = iTopEnd - 1;
				for (int i = num; i <= num2; i++)
				{
					if (decimal.Compare(decimal.Subtract(GlobalForm.nHLC[1, i], d), d2) > 0)
					{
						return Conversions.ToBoolean(Interaction.IIf(false, (object)false, (object)true));
					}
				}
				break;
			}
			}
			return Conversions.ToBoolean(Interaction.IIf(false, (object)true, (object)false));
		}
	}

	public static void FindWeinsteinStages(string Filename, int Source)
	{
		//IL_015b: Unknown result type (might be due to invalid IL or missing references)
		checked
		{
			if (Filename != null)
			{
				bool flag = false;
				switch (Source)
				{
				case 1:
				{
					bool flag4 = true;
					if (flag4 == MyProject.Forms.ListChartForm.DailyRadioButton.Checked)
					{
						flag = true;
					}
					else if (flag4 != MyProject.Forms.ListChartForm.WeeklyRadioButton.Checked && flag4 == MyProject.Forms.ListChartForm.MonthlyRadioButton.Checked)
					{
						flag = true;
					}
					break;
				}
				case 0:
				{
					bool flag3 = true;
					if (flag3 == MyProject.Forms.ListForm.DailyRadioButton.Checked)
					{
						flag = true;
					}
					else if (flag3 != MyProject.Forms.ListForm.WeeklyRadioButton.Checked && flag3 == MyProject.Forms.ListForm.MonthlyRadioButton.Checked)
					{
						flag = true;
					}
					break;
				}
				case 2:
				{
					bool flag2 = true;
					if (flag2 == MyProject.Forms.ChartForm.DailyRadioButton.Checked)
					{
						flag = true;
					}
					else if (flag2 != MyProject.Forms.ChartForm.WeeklyRadioButton.Checked && flag2 == MyProject.Forms.ChartForm.MonthlyRadioButton.Checked)
					{
						flag = true;
					}
					break;
				}
				}
				if (flag)
				{
					ProgressBar ProgBar = null;
					Label ErrorLabel = null;
					if (GlobalForm.LoadFile(Filename, ref ProgBar, ref ErrorLabel, QuickExit: false, 1))
					{
						return;
					}
					if (GlobalForm.HLCRange < 30)
					{
						GlobalForm.WStages = new int[GlobalForm.HLCRange + 1];
						return;
					}
				}
				decimal[] array = new decimal[GlobalForm.HLCRange + 1];
				GlobalForm.WStages = new int[GlobalForm.HLCRange + 1];
				decimal d = default(decimal);
				int hLCRange = GlobalForm.HLCRange;
				for (int i = 0; i <= hLCRange; i++)
				{
					if (i > 29)
					{
						d = decimal.Add(d, decimal.Subtract(GlobalForm.nHLC[3, i], GlobalForm.nHLC[3, i - 30]));
						array[i] = decimal.Divide(d, 30m);
					}
					else
					{
						d = decimal.Add(d, GlobalForm.nHLC[3, i]);
						array[i] = decimal.Divide(d, new decimal(i + 1));
					}
				}
				DetermineStages(array, 30);
				if (Filename == null)
				{
					return;
				}
				switch (Source)
				{
				case 1:
				{
					bool flag7 = true;
					if (flag7 == MyProject.Forms.ListChartForm.DailyRadioButton.Checked)
					{
						ProgressBar ProgBar = null;
						Label ErrorLabel = null;
						GlobalForm.LoadFile(Filename, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
					}
					else if (flag7 != MyProject.Forms.ListChartForm.WeeklyRadioButton.Checked && flag7 == MyProject.Forms.ListChartForm.MonthlyRadioButton.Checked)
					{
						ProgressBar ProgBar = null;
						Label ErrorLabel = null;
						GlobalForm.LoadFile(Filename, ref ProgBar, ref ErrorLabel, QuickExit: false, 2);
					}
					break;
				}
				case 0:
				{
					bool flag6 = true;
					if (flag6 == MyProject.Forms.ListForm.DailyRadioButton.Checked)
					{
						ProgressBar ProgBar = null;
						Label ErrorLabel = null;
						GlobalForm.LoadFile(Filename, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
					}
					else if (flag6 != MyProject.Forms.ListForm.WeeklyRadioButton.Checked && flag6 == MyProject.Forms.ListForm.MonthlyRadioButton.Checked)
					{
						ProgressBar ProgBar = null;
						Label ErrorLabel = null;
						GlobalForm.LoadFile(Filename, ref ProgBar, ref ErrorLabel, QuickExit: false, 2);
					}
					break;
				}
				case 2:
				{
					bool flag5 = true;
					if (flag5 == MyProject.Forms.ChartForm.DailyRadioButton.Checked)
					{
						ProgressBar ProgBar = null;
						Label ErrorLabel = null;
						GlobalForm.LoadFile(Filename, ref ProgBar, ref ErrorLabel, QuickExit: false, 0);
					}
					else if (flag5 != MyProject.Forms.ChartForm.WeeklyRadioButton.Checked && flag5 == MyProject.Forms.ChartForm.MonthlyRadioButton.Checked)
					{
						ProgressBar ProgBar = null;
						Label ErrorLabel = null;
						GlobalForm.LoadFile(Filename, ref ProgBar, ref ErrorLabel, QuickExit: false, 2);
					}
					break;
				}
				}
			}
			else
			{
				MessageBox.Show("Missing filename in FindWeinsteinStages().", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
			}
		}
	}

	public static void DetermineStages(decimal[] MovAvg, int lsMALENGTH)
	{
		//IL_04f7: Unknown result type (might be due to invalid IL or missing references)
		if (GlobalForm.HLCRange < lsMALENGTH)
		{
			return;
		}
		checked
		{
			try
			{
				int num = lsMALENGTH - 1;
				int hLCRange = GlobalForm.HLCRange;
				for (int i = num; i <= hLCRange; i++)
				{
					if (decimal.Compare(GlobalForm.nHLC[2, i], MovAvg[i]) > 0)
					{
						GlobalForm.WStages[i] = 2;
					}
					else if (decimal.Compare(GlobalForm.nHLC[1, i], MovAvg[i]) < 0)
					{
						GlobalForm.WStages[i] = 4;
					}
					else
					{
						GlobalForm.WStages[i] = 5;
					}
				}
				if (GlobalForm.WStages[0] == 0)
				{
					int num2 = GlobalForm.HLCRange - 1;
					for (int i = 0; i <= num2; i++)
					{
						if ((GlobalForm.WStages[i] == 0) & (GlobalForm.WStages[i + 1] != 0))
						{
							for (int j = i; j >= 0; j += -1)
							{
								GlobalForm.WStages[j] = GlobalForm.WStages[i + 1];
							}
							break;
						}
					}
				}
				bool flag;
				do
				{
					flag = false;
					int num3 = GlobalForm.HLCRange - 1;
					for (int i = 1; i <= num3; i++)
					{
						int num4;
						if (i + 12 > GlobalForm.HLCRange)
						{
							num4 = GlobalForm.HLCRange - i;
							if (num4 == 0)
							{
								break;
							}
						}
						else
						{
							num4 = 12;
						}
						if ((GlobalForm.WStages[i] == 5) & (GlobalForm.WStages[i + 1] == 4))
						{
							int num5 = i + 2;
							int num6 = i + num4;
							for (int j = num5; j <= num6 && !((GlobalForm.WStages[j] != 5) & (GlobalForm.WStages[j] != 4)); j++)
							{
								if (GlobalForm.WStages[j] == 5)
								{
									int num7 = i + 1;
									int num8 = j - 1;
									for (int k = num7; k <= num8; k++)
									{
										GlobalForm.WStages[k] = 5;
									}
									flag = true;
									break;
								}
							}
						}
						if ((GlobalForm.WStages[i] == 4) & (GlobalForm.WStages[i + 1] == 5))
						{
							int num9 = i + 2;
							int num10 = i + num4;
							for (int j = num9; j <= num10 && !((GlobalForm.WStages[j] != 4) & (GlobalForm.WStages[j] != 5)); j++)
							{
								if (GlobalForm.WStages[j] == 4)
								{
									int num11 = i + 1;
									int num12 = j - 1;
									for (int l = num11; l <= num12; l++)
									{
										GlobalForm.WStages[l] = 4;
									}
									flag = true;
									break;
								}
							}
						}
						if ((GlobalForm.WStages[i] == 5) & (GlobalForm.WStages[i + 1] == 2))
						{
							int num13 = i + 2;
							int num14 = i + num4;
							for (int j = num13; j <= num14 && !((GlobalForm.WStages[j] != 5) & (GlobalForm.WStages[j] != 2)); j++)
							{
								if (GlobalForm.WStages[j] == 5)
								{
									int num15 = i + 1;
									int num16 = j - 1;
									for (int m = num15; m <= num16; m++)
									{
										GlobalForm.WStages[m] = 5;
									}
									flag = true;
									break;
								}
							}
						}
						if (!((GlobalForm.WStages[i] == 2) & (GlobalForm.WStages[i + 1] == 5)))
						{
							continue;
						}
						int num17 = i + 2;
						int num18 = i + num4;
						for (int j = num17; j <= num18 && !((GlobalForm.WStages[j] != 2) & (GlobalForm.WStages[j] != 5)); j++)
						{
							if (GlobalForm.WStages[j] == 2)
							{
								int num19 = i + 1;
								int num20 = j - 1;
								for (int n = num19; n <= num20; n++)
								{
									GlobalForm.WStages[n] = 2;
								}
								flag = true;
								break;
							}
						}
					}
				}
				while (flag);
				if (GlobalForm.WStages[0] == 5)
				{
					int hLCRange2 = GlobalForm.HLCRange;
					for (int i = 0; i <= hLCRange2; i++)
					{
						if (GlobalForm.WStages[i] != 5)
						{
							int num21 = GlobalForm.WStages[i] - 1;
							if (num21 == 0)
							{
								num21 = 4;
							}
							for (int j = i - 1; j >= 0; j += -1)
							{
								GlobalForm.WStages[j] = num21;
							}
							break;
						}
					}
				}
				int hLCRange3 = GlobalForm.HLCRange;
				for (int i = 1; i <= hLCRange3; i++)
				{
					if (GlobalForm.WStages[i] == 5)
					{
						int num21 = GlobalForm.WStages[i - 1] + 1;
						if (num21 == 5)
						{
							num21 = 1;
						}
						int num22 = i;
						int hLCRange4 = GlobalForm.HLCRange;
						for (int j = num22; j <= hLCRange4; j++)
						{
							GlobalForm.WStages[j] = num21;
							if (j + 1 <= GlobalForm.HLCRange && GlobalForm.WStages[j + 1] != 5)
							{
								break;
							}
						}
					}
					if (i <= GlobalForm.HLCRange - 5 && GlobalForm.WStages[i] != GlobalForm.WStages[i + 1])
					{
						if (GlobalForm.WStages[i + 1] != GlobalForm.WStages[i + 2])
						{
							GlobalForm.WStages[i + 1] = GlobalForm.WStages[i + 2];
						}
						else if (GlobalForm.WStages[i + 1] != GlobalForm.WStages[i + 3])
						{
							GlobalForm.WStages[i + 1] = GlobalForm.WStages[i + 3];
							GlobalForm.WStages[i + 2] = GlobalForm.WStages[i + 3];
						}
						else if (GlobalForm.WStages[i + 1] != GlobalForm.WStages[i + 4])
						{
							GlobalForm.WStages[i + 1] = GlobalForm.WStages[i + 4];
							GlobalForm.WStages[i + 2] = GlobalForm.WStages[i + 4];
							GlobalForm.WStages[i + 3] = GlobalForm.WStages[i + 4];
						}
						else if (GlobalForm.WStages[i + 1] != GlobalForm.WStages[i + 5])
						{
							GlobalForm.WStages[i + 1] = GlobalForm.WStages[i + 5];
							GlobalForm.WStages[i + 2] = GlobalForm.WStages[i + 5];
							GlobalForm.WStages[i + 3] = GlobalForm.WStages[i + 5];
							GlobalForm.WStages[i + 4] = GlobalForm.WStages[i + 5];
						}
					}
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				MessageBox.Show("Failure in DetermineStages(), probably the flip conversion loop.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				ProjectData.ClearProjectError();
			}
		}
	}

	public static bool NewCheckNearness(int iHH, int iLL, decimal dHeight, decimal dTestPoint, decimal Percent, bool TestTop, int iTestPt)
	{
		decimal d;
		decimal d2;
		if (iTestPt == -1)
		{
			if (TestTop)
			{
				d = decimal.Add(GlobalForm.nHLC[1, iHH], decimal.Multiply(dHeight, Percent));
				d2 = decimal.Subtract(GlobalForm.nHLC[1, iHH], decimal.Multiply(dHeight, Percent));
			}
			else
			{
				d = decimal.Add(GlobalForm.nHLC[2, iLL], decimal.Multiply(dHeight, Percent));
				d2 = decimal.Subtract(GlobalForm.nHLC[2, iLL], decimal.Multiply(dHeight, Percent));
			}
			return Conversions.ToBoolean(Interaction.IIf((decimal.Compare(dTestPoint, d) > 0) | (decimal.Compare(dTestPoint, d2) < 0), (object)false, (object)true));
		}
		d = decimal.Add(dTestPoint, decimal.Multiply(dHeight, Percent));
		d2 = decimal.Subtract(dTestPoint, decimal.Multiply(dHeight, Percent));
		if (TestTop)
		{
			return Conversions.ToBoolean(Interaction.IIf((decimal.Compare(GlobalForm.nHLC[1, iTestPt], d) > 0) | (decimal.Compare(GlobalForm.nHLC[1, iTestPt], d2) < 0), (object)false, (object)true));
		}
		return Conversions.ToBoolean(Interaction.IIf((decimal.Compare(GlobalForm.nHLC[2, iTestPt], d) > 0) | (decimal.Compare(GlobalForm.nHLC[2, iTestPt], d2) < 0), (object)false, (object)true));
	}
}
