using System;
using System.Collections.ObjectModel;
using System.Drawing;
using System.Windows.Forms.DataVisualization.Charting;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz;

[StandardModule]
internal sealed class ShowPatterns
{
	private static Font BoldFont;

	private static Font drawFont;

	public static void DisplayAllPatterns(ChartPaintEventArgs e, DateTime ChStart, DateTime ChEnd)
	{
		//IL_002a: Unknown result type (might be due to invalid IL or missing references)
		//IL_007d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0047: Unknown result type (might be due to invalid IL or missing references)
		//IL_004d: Expected O, but got Unknown
		//IL_009d: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a4: Expected O, but got Unknown
		//IL_00ae: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b8: Expected O, but got Unknown
		//IL_00c3: Unknown result type (might be due to invalid IL or missing references)
		//IL_00cd: Expected O, but got Unknown
		GlobalForm.SetupDateIndexes(ChStart, ChEnd);
		if ((GlobalForm.ShowCandles & (GlobalForm.CandleCount > 0)) && e.ChartElement is Series && Operators.CompareString(((Series)e.ChartElement).Name, "CandleSeries", false) == 0)
		{
			Series series = (Series)e.ChartElement;
			DisplayCandles(e, series);
		}
		if (!(GlobalForm.ShowAllPatterns & (GlobalForm.PatternCount > 0)) || !(e.ChartElement is Series) || Operators.CompareString(((Series)e.ChartElement).Name, "CandleSeries", false) != 0)
		{
			return;
		}
		Series series2 = (Series)e.ChartElement;
		drawFont = new Font("Arial", 8f);
		BoldFont = new Font("Arial", 8f, (FontStyle)1);
		checked
		{
			int num = GlobalForm.PatternCount - 1;
			for (int i = 0; i <= num; i++)
			{
				int ReturnStart = GlobalForm.ChartPatterns[i].iStartDate;
				int ReturnEnd = GlobalForm.ChartPatterns[i].iEndDate;
				GlobalForm.GetStartEndDates(i, ref ReturnStart, ref ReturnEnd);
				if (((ReturnStart >= GlobalForm.ChartStartIndex) & (ReturnEnd <= GlobalForm.ChartEndIndex)) && GlobalForm.PatternList[GlobalForm.ChartPatterns[i].Type] == 1)
				{
					switch (GlobalForm.ChartPatterns[i].Type)
					{
					case 4:
					case 5:
						ShowABCD(e, series2, i);
						break;
					case 84:
						ShowBARRB(e, series2, i);
						break;
					case 83:
						ShowBARRT(e, series2, i);
						break;
					case 2:
					case 3:
					case 6:
					case 7:
					case 8:
					case 9:
					case 10:
					case 11:
					case 28:
					case 29:
						ShowBat(e, series2, i);
						break;
					case 111:
					case 112:
					case 113:
					case 114:
						ShowBroadeningPatterns(e, series2, i);
						break;
					case 109:
					case 110:
						ShowBroadeningWedges(e, series2, i);
						break;
					case 1:
					case 82:
						ShowChannels(e, series2, i);
						break;
					case 66:
					case 81:
						ShowCup(e, series2, i);
						break;
					case 100:
						ShowDeadCatBounce(e, series2, i);
						break;
					case 18:
					case 19:
					case 20:
					case 21:
					case 34:
					case 98:
					case 115:
						ShowDoubleBottoms(e, series2, i);
						break;
					case 14:
					case 15:
					case 16:
					case 17:
					case 33:
					case 97:
					case 116:
						ShowDoubleTops(e, series2, i);
						break;
					case 96:
						ShowWedges(e, series2, i);
						break;
					case 95:
						ShowHighTightFlag(e, series2, i);
						break;
					case 93:
					case 94:
						ShowHeadShouldersBottoms(e, series2, i);
						break;
					case 107:
					case 108:
						ShowHeadShouldersTops(e, series2, i);
						break;
					case 75:
					case 76:
						ShowIslands(e, series2, i);
						break;
					case 38:
					case 39:
					case 40:
					case 41:
					case 42:
					case 43:
					case 44:
					case 45:
					case 51:
					case 52:
					case 69:
					case 70:
					case 99:
						ShowInvertedDCB(e, series2, i, drawFont);
						break;
					case 73:
					case 74:
						ShowMeasuredMoves(e, series2, i);
						break;
					case 0:
					case 12:
					case 13:
					case 22:
					case 23:
					case 31:
					case 32:
					case 46:
					case 47:
					case 49:
					case 50:
					case 53:
					case 54:
					case 59:
					case 60:
					case 68:
					case 71:
					case 72:
					case 77:
					case 117:
					case 118:
					case 119:
					case 120:
					case 121:
					case 122:
					case 123:
						ShowNR47(e, series2, i);
						break;
					case 67:
					case 78:
						ShowPennant(e, series2, i);
						break;
					case 104:
					case 106:
						ShowPipeBottoms(e, series2, i);
						break;
					case 103:
					case 105:
						ShowPipeTops(e, series2, i);
						break;
					case 30:
					case 37:
						ShowPothole(e, series2, i);
						break;
					case 101:
					case 102:
						ShowRectangles(e, series2, i);
						break;
					case 92:
						ShowWedges(e, series2, i);
						break;
					case 48:
					case 65:
						ShowRoundTop(e, series2, i);
						break;
					case 91:
						Show3FallingPeaks(e, series2, i);
						break;
					case 90:
						Show3RisingValleys(e, series2, i);
						break;
					case 57:
					case 58:
						ShowTLs(e, series2, i);
						break;
					case 89:
						ShowAscTriangles(e, series2, i);
						break;
					case 88:
						ShowDescTriangles(e, series2, i);
						break;
					case 87:
						ShowSymTriangles(e, series2, i);
						break;
					case 86:
						ShowTripleBottoms(e, series2, i);
						break;
					case 85:
						ShowTripleTops(e, series2, i);
						break;
					case 55:
						ShowVTop(e, series2, i);
						break;
					case 56:
						ShowVBottom(e, series2, i);
						break;
					case 24:
					case 25:
						ShowVerticals(e, series2, i);
						break;
					case 26:
						ShowWolfeBull(e, series2, i);
						break;
					case 27:
						ShowWolfeBear(e, series2, i);
						break;
					}
				}
			}
			drawFont.Dispose();
			BoldFont.Dispose();
		}
	}

	private static void DisplayCandles(ChartPaintEventArgs e, Series series)
	{
		//IL_000f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0016: Expected O, but got Unknown
		//IL_0020: Unknown result type (might be due to invalid IL or missing references)
		//IL_0027: Expected O, but got Unknown
		//IL_0368: Unknown result type (might be due to invalid IL or missing references)
		//IL_036f: Expected O, but got Unknown
		//IL_04ed: Unknown result type (might be due to invalid IL or missing references)
		//IL_04f4: Expected O, but got Unknown
		//IL_06ec: Unknown result type (might be due to invalid IL or missing references)
		//IL_06f3: Expected O, but got Unknown
		int num = 8;
		ChartGraphics chartGraphics = e.ChartGraphics;
		SolidBrush val = new SolidBrush(Color.Red);
		Font val2 = new Font("Arial", 8f);
		checked
		{
			int num2 = GlobalForm.CandleCount - 1;
			PointF absolutePoint = default(PointF);
			decimal value = default(decimal);
			PointF absolutePoint2 = default(PointF);
			PointF absolutePoint3 = default(PointF);
			for (int i = 0; i <= num2; i++)
			{
				if (!((GlobalForm.CandlePatterns[i].iStartDate >= GlobalForm.ChartStartIndex) & (GlobalForm.CandlePatterns[i].iEndDate <= GlobalForm.ChartEndIndex)) || !(GlobalForm.CandlePatterns[i].RenderColor == Color.Red))
				{
					continue;
				}
				bool flag = false;
				decimal dPriceTarget = GlobalForm.CandlePatterns[i].dPriceTarget;
				int type = GlobalForm.CandlePatterns[i].Type;
				if (GlobalForm.ShowUnHit)
				{
					int num3 = GlobalForm.CandlePatterns[i].iEndDate + 1;
					int hLCRange = GlobalForm.HLCRange;
					for (int j = num3; j <= hLCRange; j++)
					{
						if (decimal.Compare(dPriceTarget, 0m) > 0 && ((decimal.Compare(GlobalForm.nHLC[1, j], dPriceTarget) >= 0) & (decimal.Compare(GlobalForm.nHLC[2, j], dPriceTarget) <= 0)))
						{
							flag = true;
							break;
						}
						if (decimal.Compare(GlobalForm.CandlePatterns[i].dStopPrice, 0m) > 0 && ((Convert.ToDouble(GlobalForm.nHLC[1, j]) >= Conversion.Val((object)GlobalForm.CandlePatterns[i].dStopPrice)) & (Convert.ToDouble(GlobalForm.nHLC[2, j]) <= Conversion.Val((object)GlobalForm.CandlePatterns[i].dStopPrice))))
						{
							flag = true;
							break;
						}
					}
				}
				int num4 = GlobalForm.CandlePatterns[i].iStartDate;
				int iEndDate = GlobalForm.CandlePatterns[i].iEndDate;
				if (unchecked(type == 77 || type == 27 || type == 10 || type == 26))
				{
					num4 = iEndDate - 1;
				}
				int num5 = num4;
				int num6 = num4;
				int num7 = num4;
				int num8 = iEndDate;
				for (int k = num7; k <= num8; k++)
				{
					num6 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num6]) <= 0, (object)k, (object)num6));
					num5 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, num5]) >= 0, (object)k, (object)num5));
				}
				int num9 = 0;
				foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
				{
					if ((num9 + GlobalForm.ChartStartIndex == GlobalForm.CandlePatterns[i].iStartDate) | (num9 + GlobalForm.ChartStartIndex == GlobalForm.CandlePatterns[i].iEndDate))
					{
						absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num9 + 1));
						absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						absolutePoint.Y -= 6f;
						SolidBrush val3 = new SolidBrush(Color.Red);
						chartGraphics.Graphics.FillEllipse((Brush)(object)val3, (float)((double)absolutePoint.X - (double)num / 2.0), (float)((double)absolutePoint.Y - (double)num / 2.0), (float)num, (float)num);
						((Brush)val3).Dispose();
						if (GlobalForm.PatternTargets && num9 + GlobalForm.ChartStartIndex == GlobalForm.CandlePatterns[i].iEndDate)
						{
							if ((GlobalForm.ShowTargetprice & (!GlobalForm.ShowUnHit | unchecked(GlobalForm.ShowUnHit && !flag))) && decimal.Compare(dPriceTarget, 0m) > 0)
							{
								int num10 = FindCross(dPriceTarget, num9 + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
								absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num9);
								absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(dPriceTarget));
								absolutePoint3.Y = absolutePoint2.Y;
								absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
								if (GlobalForm.IncludePhrase)
								{
									e.ChartGraphics.Graphics.DrawString("Target: " + GlobalForm.LimitDecimals(dPriceTarget), val2, (Brush)(object)val, absolutePoint2);
								}
								absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num10);
								absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
								Pen val4 = new Pen(Color.FromArgb(192, 0, 0), 2f);
								e.ChartGraphics.Graphics.DrawLine(val4, absolutePoint2, absolutePoint3);
								val4.Dispose();
							}
							if ((GlobalForm.ShowStopLoss & (!GlobalForm.ShowUnHit | unchecked(GlobalForm.ShowUnHit && !flag))) && ((decimal.Compare(GlobalForm.CandlePatterns[i].dStopPrice, 0m) != 0) & (decimal.Compare(GlobalForm.CandlePatterns[i].dStopPrice, 0m) > 0)))
							{
								int num10 = FindCross(GlobalForm.CandlePatterns[i].dStopPrice, num9 + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
								absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num9);
								absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(GlobalForm.CandlePatterns[i].dStopPrice));
								absolutePoint3.Y = absolutePoint2.Y;
								absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
								absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num10);
								absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
								if (GlobalForm.IncludePhrase)
								{
									if (DateTime.Compare(GlobalForm.CandlePatterns[i].StopDate.Date, DateTime.MinValue) == 0)
									{
										e.ChartGraphics.Graphics.DrawString("Stop: " + GlobalForm.CandlePatterns[i].dStopPrice, val2, (Brush)(object)val, absolutePoint2);
									}
									else
									{
										e.ChartGraphics.Graphics.DrawString("Stop: " + GlobalForm.CandlePatterns[i].dStopPrice + " as of " + Conversions.ToString(GlobalForm.CandlePatterns[i].StopDate), val2, (Brush)(object)val, absolutePoint2);
									}
								}
								Pen val5 = new Pen(Color.FromArgb(192, 0, 192), 2f);
								e.ChartGraphics.Graphics.DrawLine(val5, absolutePoint2, absolutePoint3);
								val5.Dispose();
							}
							if (GlobalForm.ShowUltHighLow && ((decimal.Compare(GlobalForm.CandlePatterns[i].UltHLPrice, 0m) != 0) & (decimal.Compare(GlobalForm.CandlePatterns[i].UltHLPrice, 0m) > 0)))
							{
								int num10 = FindCross(GlobalForm.CandlePatterns[i].UltHLPrice, num9 + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
								absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num9);
								absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(GlobalForm.CandlePatterns[i].UltHLPrice));
								absolutePoint3.Y = absolutePoint2.Y;
								absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
								absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num10);
								absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
								e.ChartGraphics.Graphics.DrawLine(Pens.Gray, absolutePoint2, absolutePoint3);
								if (GlobalForm.IncludePhrase)
								{
									e.ChartGraphics.Graphics.DrawString("Ultimate " + Conversions.ToString(Interaction.IIf(GlobalForm.CandlePatterns[i].UltHiLow, (object)"high", (object)"low")) + " " + GlobalForm.CandlePatterns[i].UltHLPrice + " on " + GlobalForm.CandlePatterns[i].UltHLDate, val2, (Brush)(object)val, absolutePoint2);
								}
							}
						}
					}
					if (GlobalForm.ShowUpTarget | GlobalForm.ShowDownTarget)
					{
						if (GlobalForm.CandlePatterns[i].iBkoutDirection == 1)
						{
							if (num9 + GlobalForm.ChartStartIndex == num5)
							{
								value = new decimal(item.YValues[0]);
							}
						}
						else if (num9 + GlobalForm.ChartStartIndex == num6)
						{
							value = new decimal(item.YValues[1]);
						}
					}
					if (num9 + GlobalForm.ChartStartIndex == GlobalForm.CandlePatterns[i].iEndDate)
					{
						break;
					}
					num9++;
				}
				if (!GlobalForm.PatternTargets)
				{
					break;
				}
				if (GlobalForm.ShowUpTarget)
				{
					int num10 = FindCross(new decimal(Convert.ToDouble(value) * (1.0 + 0.01 * (double)GlobalForm.ShowUpPercentage)), num9 + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
					absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num9);
					absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(value) * (1.0 + 0.01 * (double)GlobalForm.ShowUpPercentage));
					absolutePoint3.Y = absolutePoint2.Y;
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
					absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num10);
					absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
					e.ChartGraphics.Graphics.DrawLine(Pens.Green, absolutePoint2, absolutePoint3);
					if (GlobalForm.IncludePhrase)
					{
						e.ChartGraphics.Graphics.DrawString(GlobalForm.ShowUpPercentage + "% Up", val2, (Brush)(object)val, absolutePoint2);
					}
				}
				if (GlobalForm.ShowDownTarget && Convert.ToDouble(value) * (1.0 - 0.01 * (double)GlobalForm.ShowDownPercentage) > 0.0)
				{
					int num10 = FindCross(new decimal(Convert.ToDouble(value) * (1.0 - 0.01 * (double)GlobalForm.ShowDownPercentage)), num9 + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
					absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num9);
					absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(value) * (1.0 - 0.01 * (double)GlobalForm.ShowDownPercentage));
					absolutePoint3.Y = absolutePoint2.Y;
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
					absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num10);
					absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
					e.ChartGraphics.Graphics.DrawLine(Pens.Green, absolutePoint2, absolutePoint3);
					if (GlobalForm.IncludePhrase)
					{
						e.ChartGraphics.Graphics.DrawString(GlobalForm.ShowDownPercentage + "% Down", val2, (Brush)(object)val, absolutePoint2);
					}
				}
				break;
			}
			val2.Dispose();
			((Brush)val).Dispose();
		}
	}

	private static int FindCross(decimal TargetPrice, int Index, bool SpecialCase)
	{
		double num = ((!GlobalForm.IntradayData) ? 0.01 : 0.0001);
		checked
		{
			int num2 = Index + 1;
			int chartEndIndex = GlobalForm.ChartEndIndex;
			for (int i = num2; i <= chartEndIndex; i++)
			{
				if (SpecialCase)
				{
					if ((Convert.ToDouble(GlobalForm.nHLC[1, i]) + num > Convert.ToDouble(TargetPrice)) & (Convert.ToDouble(GlobalForm.nHLC[2, i]) - num < Convert.ToDouble(TargetPrice)))
					{
						if (i + 1 > GlobalForm.ChartEndIndex)
						{
							return GlobalForm.ChartEndIndex;
						}
						return i + 1;
					}
					if (i > 0 && (((decimal.Compare(GlobalForm.nHLC[1, i], TargetPrice) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i - 1], TargetPrice) < 0)) | ((decimal.Compare(GlobalForm.nHLC[1, i - 1], TargetPrice) > 0) & (decimal.Compare(GlobalForm.nHLC[2, i], TargetPrice) < 0))))
					{
						if (i + 1 > GlobalForm.ChartEndIndex)
						{
							return GlobalForm.ChartEndIndex;
						}
						return i + 1;
					}
					continue;
				}
				if ((Convert.ToDouble(GlobalForm.nHLC[1, i]) + num >= Convert.ToDouble(TargetPrice)) & (Convert.ToDouble(GlobalForm.nHLC[2, i]) - num <= Convert.ToDouble(TargetPrice)))
				{
					if (i + 1 > GlobalForm.ChartEndIndex)
					{
						return GlobalForm.ChartEndIndex;
					}
					return i + 1;
				}
				if (i > 0 && (((Convert.ToDouble(GlobalForm.nHLC[1, i]) + num >= Convert.ToDouble(TargetPrice)) & (Convert.ToDouble(GlobalForm.nHLC[2, i - 1]) - num <= Convert.ToDouble(TargetPrice))) | ((Convert.ToDouble(GlobalForm.nHLC[1, i - 1]) + num >= Convert.ToDouble(TargetPrice)) & (Convert.ToDouble(GlobalForm.nHLC[2, i]) - num <= Convert.ToDouble(TargetPrice)))))
				{
					if (i + 1 > GlobalForm.ChartEndIndex)
					{
						return GlobalForm.ChartEndIndex;
					}
					return i + 1;
				}
			}
			return GlobalForm.ChartEndIndex;
		}
	}

	public static PointF DrawTextAbove(ChartPaintEventArgs e, DataPoint point, int Index, int PatternIndex)
	{
		//IL_00c0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ee: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f9: Expected O, but got Unknown
		//IL_00f9: Expected O, but got Unknown
		PointF empty = PointF.Empty;
		empty.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)Index);
		empty.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, point.YValues[0]);
		PointF pointF = empty;
		empty.Y -= 2f;
		empty = e.ChartGraphics.GetAbsolutePoint(empty);
		float num = GlobalForm.CalculateCharacterWidth(e);
		empty.X += num;
		e.ChartGraphics.Graphics.DrawString(GlobalForm.ChartPatterns[PatternIndex].iText, (Font)Interaction.IIf(GlobalForm.ChartPatterns[PatternIndex].RenderColor == Color.Red, (object)BoldFont, (object)drawFont), (Brush)Interaction.IIf(GlobalForm.ChartPatterns[PatternIndex].RenderColor == Color.Red, (object)Brushes.Red, (object)Brushes.Black), empty);
		return e.ChartGraphics.GetAbsolutePoint(pointF);
	}

	public static PointF DrawTextBelow(ChartPaintEventArgs e, DataPoint point, int Index, int PatternIndex)
	{
		//IL_00c0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00ee: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f9: Expected O, but got Unknown
		//IL_00f9: Expected O, but got Unknown
		PointF empty = PointF.Empty;
		empty.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)Index);
		empty.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, point.YValues[1]);
		PointF pointF = empty;
		empty.Y += 1f;
		empty = e.ChartGraphics.GetAbsolutePoint(empty);
		float num = GlobalForm.CalculateCharacterWidth(e);
		empty.X += num;
		e.ChartGraphics.Graphics.DrawString(GlobalForm.ChartPatterns[PatternIndex].iText, (Font)Interaction.IIf(GlobalForm.ChartPatterns[PatternIndex].RenderColor == Color.Red, (object)BoldFont, (object)drawFont), (Brush)Interaction.IIf(GlobalForm.ChartPatterns[PatternIndex].RenderColor == Color.Red, (object)Brushes.Red, (object)Brushes.Black), empty);
		return e.ChartGraphics.GetAbsolutePoint(pointF);
	}

	private static void ShowRoundTop(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_0157: Unknown result type (might be due to invalid IL or missing references)
		//IL_0185: Unknown result type (might be due to invalid IL or missing references)
		//IL_0191: Expected O, but got Unknown
		//IL_0191: Expected O, but got Unknown
		bool flag = Conversions.ToBoolean(Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)true, (object)false));
		int num = 0;
		checked
		{
			PointF absolutePoint = default(PointF);
			PointF absolutePoint2 = default(PointF);
			PointF absolutePoint3 = default(PointF);
			PointF pointF = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					absolutePoint2.Y = absolutePoint.Y;
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
				}
				if ((num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate) | (num + GlobalForm.ChartStartIndex == GlobalForm.ChartEndIndex))
				{
					absolutePoint3.Y = absolutePoint.Y + 2f;
					absolutePoint3.X = absolutePoint.X;
					absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
					e.ChartGraphics.Graphics.DrawString(GlobalForm.ChartPatterns[i].iText, (Font)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)BoldFont, (object)drawFont), (Brush)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)Brushes.Red, (object)Brushes.Black), absolutePoint3);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
					if (flag)
					{
						e.ChartGraphics.Graphics.DrawLine(Pens.Red, absolutePoint, absolutePoint2);
						if (GlobalForm.ChartPatterns[i].Type == 65)
						{
							ShowTarget(e, series, i, num);
						}
					}
					if (GlobalForm.ChartPatterns[i].Type == 65)
					{
						break;
					}
				}
				if (GlobalForm.ChartPatterns[i].Type == 48 && num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF.Y = absolutePoint2.Y;
					if (flag)
					{
						e.ChartGraphics.Graphics.DrawLine(Pens.Blue, absolutePoint2, pointF);
						ShowTarget(e, series, i, num);
						e.ChartGraphics.Graphics.DrawString("Handle", BoldFont, Brushes.Blue, absolutePoint2);
					}
					break;
				}
				num++;
			}
		}
	}

	private static void Show3FallingPeaks(ChartPaintEventArgs e, Series series, int i)
	{
		int num = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					DrawTextAbove(e, item, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
				{
					DrawTextAbove(e, item, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					DrawTextAbove(e, item, num, i);
					ShowTarget(e, series, i, num);
					break;
				}
				num++;
			}
		}
	}

	private static void Show3RisingValleys(ChartPaintEventArgs e, Series series, int i)
	{
		int num = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					DrawTextBelow(e, item, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
				{
					DrawTextBelow(e, item, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					DrawTextBelow(e, item, num, i);
					ShowTarget(e, series, i, num);
					break;
				}
				num++;
			}
		}
	}

	private static void ShowABCD(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_01a2: Unknown result type (might be due to invalid IL or missing references)
		//IL_01ae: Expected O, but got Unknown
		//IL_0577: Unknown result type (might be due to invalid IL or missing references)
		//IL_0583: Expected O, but got Unknown
		//IL_026d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0279: Expected O, but got Unknown
		//IL_0642: Unknown result type (might be due to invalid IL or missing references)
		//IL_064e: Expected O, but got Unknown
		//IL_0373: Unknown result type (might be due to invalid IL or missing references)
		//IL_037f: Expected O, but got Unknown
		//IL_0748: Unknown result type (might be due to invalid IL or missing references)
		//IL_0754: Expected O, but got Unknown
		ShowNR47(e, series, i);
		int num = 0;
		checked
		{
			PointF absolutePoint = default(PointF);
			PointF absolutePoint2 = default(PointF);
			PointF absolutePoint3 = default(PointF);
			PointF pointF = default(PointF);
			if (GlobalForm.ChartPatterns[i].Type == 4)
			{
				foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
				{
					if (GlobalForm.ChartPatterns[i].RenderColor == Color.Red)
					{
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
						{
							absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
							GlobalForm.ChartPatterns[i].iText = "A";
							DrawTextBelow(e, item, num, i);
							absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						}
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
						{
							absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
							GlobalForm.ChartPatterns[i].iText = "B";
							DrawTextAbove(e, item, num, i);
							absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint2);
						}
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
						{
							absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
							GlobalForm.ChartPatterns[i].iText = "C";
							DrawTextBelow(e, item, num, i);
							absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint3);
						}
						if (GlobalForm.ChartPatterns[i].iEndDate != 0)
						{
							if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
							{
								pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num);
								pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
								GlobalForm.ChartPatterns[i].iText = "D";
								DrawTextAbove(e, item, num, i);
								ShowTarget(e, series, i, num);
								pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
								pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
								e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint3, pointF);
								GlobalForm.ChartPatterns[i].iText = "ABCD Be";
								break;
							}
						}
						else if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
						{
							ShowTarget(e, series, i, num);
						}
					}
					num++;
				}
				return;
			}
			if (GlobalForm.ChartPatterns[i].Type != 5)
			{
				return;
			}
			foreach (DataPoint item2 in (Collection<DataPoint>)(object)series.Points)
			{
				if (GlobalForm.ChartPatterns[i].RenderColor == Color.Red)
				{
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
					{
						absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0]);
						GlobalForm.ChartPatterns[i].iText = "A";
						DrawTextAbove(e, item2, num, i);
						absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
					{
						absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[1]);
						GlobalForm.ChartPatterns[i].iText = "B";
						DrawTextBelow(e, item2, num, i);
						absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint2);
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
					{
						absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0]);
						GlobalForm.ChartPatterns[i].iText = "C";
						DrawTextAbove(e, item2, num, i);
						absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
						e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint3);
					}
					if (GlobalForm.ChartPatterns[i].iEndDate != 0)
					{
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
						{
							pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num);
							pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[1]);
							GlobalForm.ChartPatterns[i].iText = "D";
							DrawTextBelow(e, item2, num, i);
							ShowTarget(e, series, i, num);
							pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint3, pointF);
							GlobalForm.ChartPatterns[i].iText = "ABCD Bu";
							break;
						}
					}
					else if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
					{
						ShowTarget(e, series, i, num);
					}
				}
				num++;
			}
		}
	}

	private static void ShowTLs(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_0175: Unknown result type (might be due to invalid IL or missing references)
		//IL_0181: Expected O, but got Unknown
		//IL_044e: Unknown result type (might be due to invalid IL or missing references)
		//IL_045a: Expected O, but got Unknown
		//IL_024a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0256: Expected O, but got Unknown
		//IL_0523: Unknown result type (might be due to invalid IL or missing references)
		//IL_052f: Expected O, but got Unknown
		//IL_02a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_02ac: Expected O, but got Unknown
		//IL_0579: Unknown result type (might be due to invalid IL or missing references)
		//IL_0585: Expected O, but got Unknown
		int num = 0;
		checked
		{
			PointF absolutePoint = default(PointF);
			PointF absolutePoint2 = default(PointF);
			float num2 = default(float);
			PointF absolutePoint3 = default(PointF);
			if (GlobalForm.ChartPatterns[i].Type == 57)
			{
				foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
				{
					if (GlobalForm.ChartPatterns[i].RenderColor == Color.Red)
					{
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
						{
							absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
							absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						}
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
						{
							absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
							absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
							num2 = (absolutePoint2.Y - absolutePoint.Y) / (absolutePoint2.X - absolutePoint.X);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint2);
						}
						if (num + GlobalForm.ChartStartIndex > GlobalForm.ChartPatterns[i].iEndDate)
						{
							absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
							absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
							float num3 = num2 * (absolutePoint3.X - absolutePoint2.X) + absolutePoint2.Y;
							if (GlobalForm.FormTypeLoaded == 4)
							{
								absolutePoint3.Y = num3;
								e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint3);
							}
							else if (num3 < absolutePoint3.Y)
							{
								absolutePoint3.Y = num3;
								e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint3);
								ShowTarget(e, series, i, num);
								break;
							}
						}
					}
					num++;
				}
				return;
			}
			if (GlobalForm.ChartPatterns[i].Type != 58)
			{
				return;
			}
			foreach (DataPoint item2 in (Collection<DataPoint>)(object)series.Points)
			{
				if (GlobalForm.ChartPatterns[i].RenderColor == Color.Red)
				{
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
					{
						absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0]);
						absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
					{
						absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0]);
						absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						num2 = (absolutePoint2.Y - absolutePoint.Y) / (absolutePoint2.X - absolutePoint.X);
						e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint2);
					}
					if (num + GlobalForm.ChartStartIndex > GlobalForm.ChartPatterns[i].iEndDate)
					{
						absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0]);
						absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
						float num3 = num2 * (absolutePoint3.X - absolutePoint2.X) + absolutePoint2.Y;
						if (GlobalForm.FormTypeLoaded == 4)
						{
							absolutePoint3.Y = num3;
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint3);
						}
						else if (num3 > absolutePoint3.Y)
						{
							absolutePoint3.Y = num3;
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint3);
							ShowTarget(e, series, i, num);
							break;
						}
					}
				}
				num++;
			}
		}
	}

	private static void ShowAscTriangles(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_033b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0349: Expected O, but got Unknown
		//IL_03d1: Unknown result type (might be due to invalid IL or missing references)
		//IL_03df: Expected O, but got Unknown
		int num = GlobalForm.ChartPatterns[i].iStartDate;
		int iStartDate = GlobalForm.ChartPatterns[i].iStartDate;
		int iEndDate = GlobalForm.ChartPatterns[i].iEndDate;
		checked
		{
			for (int j = iStartDate; j <= iEndDate; j++)
			{
				num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, num]) > 0, (object)j, (object)num));
			}
			int num2 = 0;
			decimal num3 = default(decimal);
			decimal num4 = default(decimal);
			decimal num5 = default(decimal);
			decimal d = default(decimal);
			decimal d2 = default(decimal);
			decimal value = default(decimal);
			decimal num6 = default(decimal);
			PointF pointF2 = default(PointF);
			PointF pointF = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					num3 = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num2 + 1)));
					_ = num2 + GlobalForm.ChartStartIndex;
				}
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
				{
					num4 = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]));
					num5 = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num2 + 1)));
					DrawTextBelow(e, item, num2, i);
				}
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date)
				{
					d = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num2 + 1)));
					d2 = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]));
				}
				if (num2 + GlobalForm.ChartStartIndex == num)
				{
					value = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]));
				}
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					decimal value2 = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num2 + 1)));
					if (decimal.Compare(decimal.Subtract(num5, d), 0m) != 0)
					{
						num6 = decimal.Divide(decimal.Subtract(num4, d2), decimal.Subtract(num5, d));
					}
					decimal d3 = num4;
					pointF.Y = Convert.ToSingle(decimal.Add(decimal.Multiply(num6, decimal.Subtract(num3, num5)), d3));
					if (decimal.Compare(num6, 0m) != 0)
					{
						pointF2.X = -1f * ((pointF.Y - Convert.ToSingle(value)) / Convert.ToSingle(num6)) + Convert.ToSingle(num3);
					}
					if (pointF2.X < Convert.ToSingle(value2))
					{
						pointF2.X = Convert.ToSingle(value2);
					}
					pointF2.Y = Convert.ToSingle(value);
					pointF.X = Convert.ToSingle(num3);
					pointF.Y = Convert.ToSingle(value);
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF.X += 4f;
					PointF absolutePoint = e.ChartGraphics.GetAbsolutePoint(pointF2);
					absolutePoint.X += 4f;
					e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF, absolutePoint);
					pointF.X = Convert.ToSingle(num3);
					pointF.Y = Convert.ToSingle(decimal.Add(decimal.Multiply(num6, decimal.Subtract(num3, num5)), d3));
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF.X += 4f;
					e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF, absolutePoint);
					ShowTarget(e, series, i, num2);
					break;
				}
				num2++;
			}
		}
	}

	public static void ShowBARRB(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_03a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_03ac: Expected O, but got Unknown
		//IL_03e0: Unknown result type (might be due to invalid IL or missing references)
		//IL_03ec: Expected O, but got Unknown
		int num = 0;
		bool flag = false;
		float num3;
		float num6 = default(float);
		PointF pointF2 = default(PointF);
		PointF pointF5 = default(PointF);
		bool flag2;
		string text;
		checked
		{
			int num2 = (int)Math.Round((double)GlobalForm.ChartPatterns[i].iStartDate + (double)(GlobalForm.ChartPatterns[i].iEndDate - GlobalForm.ChartPatterns[i].iStartDate) / 4.0);
			num3 = Convert.ToSingle(GlobalForm.ChartPatterns[i].dChannelHeight);
			int num4 = default(int);
			if (GlobalForm.PatternTargets & GlobalForm.ShowBARRLines)
			{
				num4 = GlobalForm.ChartPatterns[i].iStartDate;
				int num5 = GlobalForm.ChartPatterns[i].iStartDate + 1;
				int iEndDate = GlobalForm.ChartPatterns[i].iEndDate;
				for (int j = num5; j <= iEndDate; j++)
				{
					num4 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num4]) < 0, (object)j, (object)num4));
				}
				num6 = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(GlobalForm.nHLC[2, num4]));
			}
			PointF pointF3 = default(PointF);
			PointF pointF = default(PointF);
			PointF pointF4 = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					if (GlobalForm.PatternTargets & GlobalForm.ShowBARRLines)
					{
						_ = pointF.Y;
						_ = pointF.X;
						pointF2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0] - (double)num3);
						num3 = pointF.Y - pointF2.Y;
						pointF2.X = pointF.X;
					}
					DrawTextAbove(e, item, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == num4)
				{
					_ = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
				}
				if (!flag & (num + GlobalForm.ChartStartIndex >= num2))
				{
					pointF3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					flag = true;
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					pointF4.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					pointF4.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					ShowTarget(e, series, i, num);
					break;
				}
				num++;
			}
			if (num + GlobalForm.ChartStartIndex != GlobalForm.ChartPatterns[i].iEndDate)
			{
				return;
			}
			float num7 = (pointF4.Y - pointF.Y) / (pointF4.X - pointF.X);
			pointF3.Y = num7 * (pointF3.X - pointF.X) + pointF.Y;
			if (GlobalForm.PatternTargets & GlobalForm.ShowBARRLines)
			{
				pointF5 = pointF4;
			}
			pointF3 = e.ChartGraphics.GetAbsolutePoint(pointF3);
			pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
			pointF4 = e.ChartGraphics.GetAbsolutePoint(pointF4);
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Blue), pointF, pointF3);
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF3, pointF4);
			if (!(GlobalForm.PatternTargets & GlobalForm.ShowBARRLines))
			{
				return;
			}
			flag2 = false;
			text = "Warning line";
		}
		while (true)
		{
			PointF absolutePoint = e.ChartGraphics.GetAbsolutePoint(pointF2);
			pointF5.Y -= num3;
			PointF absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(pointF5);
			e.ChartGraphics.Graphics.DrawLine(Pens.Blue, absolutePoint, absolutePoint2);
			if (GlobalForm.IncludePhrase)
			{
				e.ChartGraphics.Graphics.DrawString(text, drawFont, Brushes.Red, absolutePoint);
				text = "Buy Line";
			}
			pointF2.Y -= num3;
			if (!((pointF5.Y <= 0f) | (pointF5.Y >= num6 && flag2)))
			{
				flag2 = true;
				continue;
			}
			break;
		}
	}

	public static void ShowBARRT(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_03a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_03ac: Expected O, but got Unknown
		//IL_03e0: Unknown result type (might be due to invalid IL or missing references)
		//IL_03ec: Expected O, but got Unknown
		int num = 0;
		bool flag = false;
		float num3;
		float num6 = default(float);
		PointF pointF2 = default(PointF);
		PointF pointF5 = default(PointF);
		bool flag2;
		string text;
		checked
		{
			int num2 = (int)Math.Round((double)GlobalForm.ChartPatterns[i].iStartDate + (double)(GlobalForm.ChartPatterns[i].iEndDate - GlobalForm.ChartPatterns[i].iStartDate) / 4.0);
			num3 = Convert.ToSingle(GlobalForm.ChartPatterns[i].dChannelHeight);
			int num4 = default(int);
			if (GlobalForm.PatternTargets & GlobalForm.ShowBARRLines)
			{
				num4 = GlobalForm.ChartPatterns[i].iStartDate;
				int num5 = GlobalForm.ChartPatterns[i].iStartDate + 1;
				int iEndDate = GlobalForm.ChartPatterns[i].iEndDate;
				for (int j = num5; j <= iEndDate; j++)
				{
					num4 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.nHLC[1, num4]) > 0, (object)j, (object)num4));
				}
				num6 = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(GlobalForm.nHLC[1, num4]));
			}
			PointF pointF3 = default(PointF);
			PointF pointF = default(PointF);
			PointF pointF4 = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					if (GlobalForm.PatternTargets & GlobalForm.ShowBARRLines)
					{
						_ = pointF.Y;
						_ = pointF.X;
						pointF2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1] + (double)num3);
						num3 = pointF2.Y - pointF.Y;
						pointF2.X = pointF.X;
					}
					DrawTextBelow(e, item, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == num4)
				{
					_ = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
				}
				if (!flag & (num + GlobalForm.ChartStartIndex >= num2))
				{
					pointF3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					flag = true;
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					pointF4.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					pointF4.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					ShowTarget(e, series, i, num);
					break;
				}
				num++;
			}
			if (num + GlobalForm.ChartStartIndex != GlobalForm.ChartPatterns[i].iEndDate)
			{
				return;
			}
			float num7 = (pointF4.Y - pointF.Y) / (pointF4.X - pointF.X);
			pointF3.Y = num7 * (pointF3.X - pointF.X) + pointF.Y;
			if (GlobalForm.PatternTargets & GlobalForm.ShowBARRLines)
			{
				pointF5 = pointF4;
			}
			pointF3 = e.ChartGraphics.GetAbsolutePoint(pointF3);
			pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
			pointF4 = e.ChartGraphics.GetAbsolutePoint(pointF4);
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Blue), pointF, pointF3);
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF3, pointF4);
			if (!(GlobalForm.PatternTargets & GlobalForm.ShowBARRLines))
			{
				return;
			}
			flag2 = false;
			text = "Warning line";
		}
		while (true)
		{
			PointF absolutePoint = e.ChartGraphics.GetAbsolutePoint(pointF2);
			pointF5.Y += num3;
			PointF absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(pointF5);
			e.ChartGraphics.Graphics.DrawLine(Pens.Blue, absolutePoint, absolutePoint2);
			if (GlobalForm.IncludePhrase)
			{
				e.ChartGraphics.Graphics.DrawString(text, drawFont, Brushes.Red, absolutePoint);
				text = "Sell Line";
			}
			pointF2.Y += num3;
			if (!((pointF5.Y <= 0f) | (pointF5.Y <= num6 && flag2)))
			{
				flag2 = true;
				continue;
			}
			break;
		}
	}

	private static void ShowBat(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_0209: Unknown result type (might be due to invalid IL or missing references)
		//IL_0215: Expected O, but got Unknown
		//IL_06b2: Unknown result type (might be due to invalid IL or missing references)
		//IL_06be: Expected O, but got Unknown
		//IL_02d4: Unknown result type (might be due to invalid IL or missing references)
		//IL_02e0: Expected O, but got Unknown
		//IL_077d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0789: Expected O, but got Unknown
		//IL_039f: Unknown result type (might be due to invalid IL or missing references)
		//IL_03ab: Expected O, but got Unknown
		//IL_0848: Unknown result type (might be due to invalid IL or missing references)
		//IL_0854: Expected O, but got Unknown
		//IL_0492: Unknown result type (might be due to invalid IL or missing references)
		//IL_049f: Expected O, but got Unknown
		//IL_093b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0948: Expected O, but got Unknown
		string iText = GlobalForm.ChartPatterns[i].iText;
		ShowNR47(e, series, i);
		int num = 0;
		checked
		{
			PointF absolutePoint = default(PointF);
			PointF absolutePoint2 = default(PointF);
			PointF absolutePoint3 = default(PointF);
			PointF absolutePoint4 = default(PointF);
			PointF pointF = default(PointF);
			if ((GlobalForm.ChartPatterns[i].Type == 11) | (GlobalForm.ChartPatterns[i].Type == 9) | (GlobalForm.ChartPatterns[i].Type == 3) | (GlobalForm.ChartPatterns[i].Type == 7) | (GlobalForm.ChartPatterns[i].Type == 28))
			{
				foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
				{
					if (GlobalForm.ChartPatterns[i].RenderColor == Color.Red)
					{
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
						{
							absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
							GlobalForm.ChartPatterns[i].iText = "X";
							DrawTextAbove(e, item, num, i);
							absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						}
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
						{
							absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
							GlobalForm.ChartPatterns[i].iText = "A";
							DrawTextBelow(e, item, num, i);
							absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint2);
						}
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
						{
							absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
							GlobalForm.ChartPatterns[i].iText = "B";
							DrawTextAbove(e, item, num, i);
							absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint3);
						}
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMid2Date)
						{
							absolutePoint4.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
							GlobalForm.ChartPatterns[i].iText = "C";
							DrawTextBelow(e, item, num, i);
							absolutePoint4.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint4 = e.ChartGraphics.GetAbsolutePoint(absolutePoint4);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint3, absolutePoint4);
						}
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
						{
							pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num);
							pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
							GlobalForm.ChartPatterns[i].iText = "D";
							DrawTextAbove(e, item, num, i);
							ShowTarget(e, series, i, num);
							pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint4, pointF);
							break;
						}
					}
					num++;
				}
			}
			else if ((GlobalForm.ChartPatterns[i].Type == 10) | (GlobalForm.ChartPatterns[i].Type == 8) | (GlobalForm.ChartPatterns[i].Type == 2) | (GlobalForm.ChartPatterns[i].Type == 6) | (GlobalForm.ChartPatterns[i].Type == 29))
			{
				foreach (DataPoint item2 in (Collection<DataPoint>)(object)series.Points)
				{
					if (GlobalForm.ChartPatterns[i].RenderColor == Color.Red)
					{
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
						{
							absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[1]);
							GlobalForm.ChartPatterns[i].iText = "X";
							DrawTextBelow(e, item2, num, i);
							absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						}
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
						{
							absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0]);
							GlobalForm.ChartPatterns[i].iText = "A";
							DrawTextAbove(e, item2, num, i);
							absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint2);
						}
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
						{
							absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[1]);
							GlobalForm.ChartPatterns[i].iText = "B";
							DrawTextBelow(e, item2, num, i);
							absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint3);
						}
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMid2Date)
						{
							absolutePoint4.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0]);
							GlobalForm.ChartPatterns[i].iText = "C";
							DrawTextAbove(e, item2, num, i);
							absolutePoint4.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint4 = e.ChartGraphics.GetAbsolutePoint(absolutePoint4);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint3, absolutePoint4);
						}
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
						{
							pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num);
							pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[1]);
							GlobalForm.ChartPatterns[i].iText = "D";
							DrawTextBelow(e, item2, num, i);
							ShowTarget(e, series, i, num);
							pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint4, pointF);
							break;
						}
					}
					num++;
				}
			}
			GlobalForm.ChartPatterns[i].iText = iText;
		}
	}

	private static void ShowBroadeningPatterns(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_05a6: Unknown result type (might be due to invalid IL or missing references)
		//IL_05b4: Expected O, but got Unknown
		//IL_05e8: Unknown result type (might be due to invalid IL or missing references)
		//IL_05f6: Expected O, but got Unknown
		DataPoint point = null;
		int num;
		bool flag;
		if (GlobalForm.ChartPatterns[i].iStartDate < GlobalForm.ChartPatterns[i].iStart2Date)
		{
			num = GlobalForm.ChartPatterns[i].iStartDate;
			flag = true;
		}
		else
		{
			num = GlobalForm.ChartPatterns[i].iStart2Date;
			flag = false;
		}
		int num2;
		bool flag2;
		if (GlobalForm.ChartPatterns[i].iEndDate > GlobalForm.ChartPatterns[i].iEnd2Date)
		{
			num2 = GlobalForm.ChartPatterns[i].iEndDate;
			flag2 = true;
		}
		else
		{
			num2 = GlobalForm.ChartPatterns[i].iEnd2Date;
			flag2 = false;
		}
		checked
		{
			if (GlobalForm.ChartStartIndex + ((Collection<DataPoint>)(object)series.Points).Count < num || num2 > ((Collection<DataPoint>)(object)series.Points).Count + GlobalForm.ChartStartIndex)
			{
				return;
			}
			int num3 = 0;
			PointF absolutePoint = default(PointF);
			PointF absolutePoint2 = default(PointF);
			PointF absolutePoint3 = default(PointF);
			PointF absolutePoint4 = default(PointF);
			PointF absolutePoint5 = default(PointF);
			int index = default(int);
			PointF pointF = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num3 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num3 + 1));
					absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				}
				if (num3 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num3 + 1));
					absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
				}
				if (num3 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
				{
					absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num3 + 1));
					absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
				}
				if (num3 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date)
				{
					absolutePoint4.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num3 + 1));
					absolutePoint4.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					absolutePoint4 = e.ChartGraphics.GetAbsolutePoint(absolutePoint4);
				}
				if (num3 + GlobalForm.ChartStartIndex == num)
				{
					absolutePoint5.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num3);
					absolutePoint5.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[Conversions.ToInteger(Interaction.IIf(flag, (object)0, (object)1))]);
					absolutePoint5 = e.ChartGraphics.GetAbsolutePoint(absolutePoint5);
					point = item;
					index = num3;
				}
				if (num3 + GlobalForm.ChartStartIndex >= num2)
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num3);
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[Conversions.ToInteger(Interaction.IIf(flag2, (object)0, (object)1))]);
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					ShowTarget(e, series, i, num3);
					break;
				}
				num3++;
			}
			if (!((absolutePoint2.X - absolutePoint.X == 0f) | (absolutePoint4.X - absolutePoint3.X == 0f)))
			{
				decimal value = new decimal((absolutePoint2.Y - absolutePoint.Y) / (absolutePoint2.X - absolutePoint.X));
				decimal value2 = new decimal((absolutePoint4.Y - absolutePoint3.Y) / (absolutePoint4.X - absolutePoint3.X));
				new decimal(absolutePoint.Y - Convert.ToSingle(value) * absolutePoint.X);
				new decimal(absolutePoint3.Y - Convert.ToSingle(value2) * absolutePoint3.X);
				if (GlobalForm.ChartPatterns[i].iStartDate <= GlobalForm.ChartPatterns[i].iStart2Date)
				{
					absolutePoint3.Y -= Convert.ToSingle(value2) * (absolutePoint3.X - absolutePoint.X);
					absolutePoint3.X = absolutePoint.X;
					DrawTextAbove(e, point, index, i);
				}
				else
				{
					absolutePoint.Y -= Convert.ToSingle(value) * (absolutePoint.X - absolutePoint3.X);
					absolutePoint.X = absolutePoint3.X;
					DrawTextBelow(e, point, index, i);
				}
				if (GlobalForm.ChartPatterns[i].iEndDate >= GlobalForm.ChartPatterns[i].iEnd2Date)
				{
					absolutePoint4.Y += Convert.ToSingle(value2) * (absolutePoint2.X - absolutePoint4.X);
					absolutePoint4.X = absolutePoint2.X;
				}
				else
				{
					absolutePoint2.Y += Convert.ToSingle(value) * (absolutePoint4.X - absolutePoint2.X);
					absolutePoint2.X = absolutePoint4.X;
				}
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint2);
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint3, absolutePoint4);
			}
		}
	}

	private static void ShowBroadeningWedges(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_099d: Unknown result type (might be due to invalid IL or missing references)
		//IL_09a9: Expected O, but got Unknown
		//IL_09dd: Unknown result type (might be due to invalid IL or missing references)
		//IL_09ea: Expected O, but got Unknown
		DataPoint val = null;
		int iStartDate = GlobalForm.ChartPatterns[i].iStartDate;
		int iStart2Date = GlobalForm.ChartPatterns[i].iStart2Date;
		int iEndDate = GlobalForm.ChartPatterns[i].iEndDate;
		int iEnd2Date = GlobalForm.ChartPatterns[i].iEnd2Date;
		int num = iStartDate;
		int num2 = GlobalForm.ChartPatterns[i].iEndDate;
		int num3 = iStart2Date;
		int num4 = GlobalForm.ChartPatterns[i].iEnd2Date;
		checked
		{
			decimal d = new decimal(GlobalForm.ChartPatterns[i].iEndDate - iStartDate);
			decimal d2 = new decimal(GlobalForm.ChartPatterns[i].iEnd2Date - iStart2Date);
			decimal d3 = decimal.Subtract(GlobalForm.nHLC[1, GlobalForm.ChartPatterns[i].iEndDate], GlobalForm.nHLC[1, iStartDate]);
			decimal d4 = decimal.Subtract(GlobalForm.nHLC[2, GlobalForm.ChartPatterns[i].iEnd2Date], GlobalForm.nHLC[2, iStart2Date]);
			decimal d5 = decimal.Divide(d3, d);
			decimal d6 = decimal.Divide(d4, d2);
			decimal priceScale = FindPatterns.GetPriceScale(GlobalForm.nHLC[1, iStartDate], GlobalForm.nHLC[1, iEndDate]);
			decimal d7 = decimal.Multiply(0.2m, priceScale);
			if (iStart2Date < iStartDate)
			{
				int num5 = iStartDate - 1;
				int num6 = iStart2Date;
				for (int j = num5; j >= num6 && !(Convert.ToSingle(decimal.Add(decimal.Multiply(d5, new decimal(j - iStartDate)), GlobalForm.nHLC[1, iStartDate])) < Convert.ToSingle(decimal.Subtract(GlobalForm.nHLC[1, j], d7))); j += -1)
				{
					num = j;
				}
			}
			else if (iStart2Date > iStartDate)
			{
				int num7 = iStart2Date - 1;
				int num8 = iStartDate;
				for (int j = num7; j >= num8 && !(Convert.ToSingle(decimal.Add(decimal.Multiply(d6, new decimal(j - iStart2Date)), GlobalForm.nHLC[2, iStart2Date])) > Convert.ToSingle(decimal.Add(GlobalForm.nHLC[2, j], d7))); j += -1)
				{
					num3 = j;
				}
			}
			if (iEnd2Date < iEndDate)
			{
				int num9 = iEnd2Date + 1;
				int num10 = iEndDate;
				for (int j = num9; j <= num10 && !(Convert.ToSingle(decimal.Add(decimal.Multiply(d6, new decimal(j - iEnd2Date)), GlobalForm.nHLC[2, iEnd2Date])) > Convert.ToSingle(decimal.Add(GlobalForm.nHLC[2, j], d7))); j++)
				{
					num4 = j;
				}
			}
			else if (iEnd2Date > iEndDate)
			{
				int num11 = iEndDate + 1;
				int num12 = iEnd2Date;
				for (int j = num11; j <= num12 && !(Convert.ToSingle(decimal.Add(decimal.Multiply(d5, new decimal(j - iEndDate)), GlobalForm.nHLC[1, iEndDate])) < Convert.ToSingle(decimal.Subtract(GlobalForm.nHLC[1, j], d7))); j++)
				{
					num2 = j;
				}
			}
			int num13 = 0;
			int num14 = 0;
			int index = 0;
			int num15 = Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iStartDate < GlobalForm.ChartPatterns[i].iStart2Date, (object)GlobalForm.ChartPatterns[i].iStartDate, (object)GlobalForm.ChartPatterns[i].iStart2Date));
			int num16 = Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iEndDate < GlobalForm.ChartPatterns[i].iEnd2Date, (object)GlobalForm.ChartPatterns[i].iEnd2Date, (object)GlobalForm.ChartPatterns[i].iEndDate));
			if (((Collection<DataPoint>)(object)series.Points).Count + GlobalForm.ChartStartIndex < num15 || num16 > ((Collection<DataPoint>)(object)series.Points).Count + GlobalForm.ChartStartIndex)
			{
				return;
			}
			PointF pointF5 = default(PointF);
			PointF pointF6 = default(PointF);
			PointF pointF7 = default(PointF);
			PointF pointF8 = default(PointF);
			PointF pointF = default(PointF);
			PointF pointF3 = default(PointF);
			PointF pointF2 = default(PointF);
			PointF pointF4 = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num13 + GlobalForm.ChartStartIndex == num)
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num13 + 1));
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
				}
				if (num13 + GlobalForm.ChartStartIndex == num3)
				{
					pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num13 + 1));
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
				}
				if (num13 + GlobalForm.ChartStartIndex == num2)
				{
					pointF3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num13 + 1));
					pointF3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
				}
				if (num13 + GlobalForm.ChartStartIndex == num4)
				{
					pointF4.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num13 + 1));
					pointF3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
				}
				if (num13 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					pointF5.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num13 + 1));
					pointF5.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					if (num14 == 0)
					{
						num14 = num13;
						index = num13;
						val = item;
					}
				}
				if (num13 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					pointF6.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					pointF6.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num13 + 1));
					if (GlobalForm.ChartPatterns[i].iEndDate > GlobalForm.ChartPatterns[i].iEnd2Date)
					{
						ShowTarget(e, series, i, num13 + 1);
						break;
					}
				}
				if (num13 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
				{
					pointF7.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num13 + 1));
					pointF7.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					if (num14 == 0)
					{
						num14 = num13;
						index = num13;
						val = item;
					}
				}
				if (num13 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date)
				{
					pointF8.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					pointF8.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num13 + 1));
					if (GlobalForm.ChartPatterns[i].iEnd2Date > GlobalForm.ChartPatterns[i].iEndDate)
					{
						ShowTarget(e, series, i, num13 + 1);
						break;
					}
				}
				num13++;
			}
			if (!Information.IsNothing((object)val))
			{
				if (GlobalForm.ChartPatterns[i].Type == 109)
				{
					DrawTextAbove(e, val, num14, i);
				}
				else if (GlobalForm.ChartPatterns[i].Type == 110)
				{
					DrawTextBelow(e, val, index, i);
				}
			}
			pointF5 = e.ChartGraphics.GetAbsolutePoint(pointF5);
			pointF6 = e.ChartGraphics.GetAbsolutePoint(pointF6);
			pointF7 = e.ChartGraphics.GetAbsolutePoint(pointF7);
			pointF8 = e.ChartGraphics.GetAbsolutePoint(pointF8);
			pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
			pointF3 = e.ChartGraphics.GetAbsolutePoint(pointF3);
			pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
			pointF4 = e.ChartGraphics.GetAbsolutePoint(pointF4);
			if (!((pointF6.X - pointF5.X == 0f) | (pointF8.X - pointF7.X == 0f)))
			{
				decimal value = new decimal((pointF6.Y - pointF5.Y) / (pointF6.X - pointF5.X));
				decimal value2 = new decimal((pointF8.Y - pointF7.Y) / (pointF8.X - pointF7.X));
				if (GlobalForm.ChartPatterns[i].iStartDate != num)
				{
					pointF5.Y += Convert.ToSingle(value) * (pointF.X - pointF5.X);
					pointF5.X = pointF.X;
				}
				if (GlobalForm.ChartPatterns[i].iStart2Date != num3)
				{
					pointF7.Y += Convert.ToSingle(value2) * (pointF2.X - pointF7.X);
					pointF7.X = pointF2.X;
				}
				if (GlobalForm.ChartPatterns[i].iEndDate != num2)
				{
					pointF6.Y += Convert.ToSingle(value) * (pointF3.X - pointF6.X);
					pointF6.X = pointF3.X;
				}
				if (GlobalForm.ChartPatterns[i].iEnd2Date != num4)
				{
					pointF8.Y += Convert.ToSingle(value2) * (pointF4.X - pointF8.X);
					pointF8.X = pointF4.X;
				}
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF5, pointF6);
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF7, pointF8);
			}
		}
	}

	private static void ShowDescTriangles(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_033d: Unknown result type (might be due to invalid IL or missing references)
		//IL_034b: Expected O, but got Unknown
		//IL_03d3: Unknown result type (might be due to invalid IL or missing references)
		//IL_03e1: Expected O, but got Unknown
		int num = GlobalForm.ChartPatterns[i].iStartDate;
		checked
		{
			int num2 = GlobalForm.ChartPatterns[i].iStartDate + 1;
			int iEndDate = GlobalForm.ChartPatterns[i].iEndDate;
			for (int j = num2; j <= iEndDate; j++)
			{
				num = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, num]) < 0, (object)j, (object)num));
			}
			int num3 = 0;
			decimal num4 = default(decimal);
			decimal num5 = default(decimal);
			decimal num6 = default(decimal);
			decimal d = default(decimal);
			decimal d2 = default(decimal);
			decimal value = default(decimal);
			decimal num7 = default(decimal);
			PointF pointF2 = default(PointF);
			PointF pointF = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num3 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					num4 = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num3 + 1)));
					DrawTextBelow(e, item, num3, i);
					_ = num3 + GlobalForm.ChartStartIndex;
				}
				if (num3 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
				{
					num5 = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num3 + 1)));
					num6 = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]));
				}
				if (num3 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date)
				{
					d = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num3 + 1)));
					d2 = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]));
				}
				if (num3 + GlobalForm.ChartStartIndex == num)
				{
					value = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]));
				}
				if (num3 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					decimal value2 = new decimal(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num3 + 1)));
					if (decimal.Compare(decimal.Subtract(num5, d), 0m) != 0)
					{
						num7 = decimal.Divide(decimal.Subtract(num6, d2), decimal.Subtract(num5, d));
					}
					decimal d3 = num6;
					pointF.Y = Convert.ToSingle(decimal.Add(decimal.Multiply(num7, decimal.Subtract(num4, num5)), d3));
					if (decimal.Compare(num7, 0m) != 0)
					{
						pointF2.X = -1f * ((pointF.Y - Convert.ToSingle(value)) / Convert.ToSingle(num7)) + Convert.ToSingle(num4);
					}
					if (pointF2.X < Convert.ToSingle(value2))
					{
						pointF2.X = Convert.ToSingle(value2);
					}
					pointF2.Y = Convert.ToSingle(value);
					pointF.X = Convert.ToSingle(num4);
					pointF.Y = Convert.ToSingle(value);
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF.X += 4f;
					PointF absolutePoint = e.ChartGraphics.GetAbsolutePoint(pointF2);
					absolutePoint.X += 4f;
					e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF, absolutePoint);
					pointF.X = Convert.ToSingle(num4);
					pointF.Y = Convert.ToSingle(decimal.Add(decimal.Multiply(num7, decimal.Subtract(num4, num5)), d3));
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF.X += 4f;
					e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF, absolutePoint);
					ShowTarget(e, series, i, num3);
					break;
				}
				num3++;
			}
		}
	}

	private static void ShowDoubleBottoms(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_0130: Unknown result type (might be due to invalid IL or missing references)
		//IL_013c: Expected O, but got Unknown
		int num = 0;
		checked
		{
			PointF absolutePoint = default(PointF);
			PointF pointF = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					DrawTextBelow(e, item, num, i);
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					ShowTarget(e, series, i, num);
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, pointF);
					break;
				}
				num++;
			}
		}
	}

	private static void ShowDoubleTops(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_0130: Unknown result type (might be due to invalid IL or missing references)
		//IL_013c: Expected O, but got Unknown
		int num = 0;
		checked
		{
			PointF absolutePoint = default(PointF);
			PointF pointF = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					DrawTextAbove(e, item, num, i);
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					ShowTarget(e, series, i, num);
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, pointF);
					break;
				}
				num++;
			}
		}
	}

	private static void ShowHCR(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_043d: Unknown result type (might be due to invalid IL or missing references)
		//IL_044a: Expected O, but got Unknown
		//IL_04d2: Unknown result type (might be due to invalid IL or missing references)
		//IL_04e0: Expected O, but got Unknown
		DataPoint val = null;
		PointF pointF = default(PointF);
		PointF pointF2 = default(PointF);
		PointF pointF3 = default(PointF);
		PointF pointF4 = default(PointF);
		int num = Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iEndDate > GlobalForm.ChartPatterns[i].iEnd2Date, (object)GlobalForm.ChartPatterns[i].iEndDate, (object)GlobalForm.ChartPatterns[i].iEnd2Date));
		int num2 = 0;
		checked
		{
			int num3 = default(int);
			int num4 = default(int);
			int index = default(int);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num2);
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					num3 = num2 + GlobalForm.ChartStartIndex;
				}
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num2);
				}
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
				{
					pointF3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num2);
					pointF3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					num4 = num2 + GlobalForm.ChartStartIndex;
					val = item;
					index = num2;
				}
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date)
				{
					pointF4.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num2);
				}
				if (((num2 + GlobalForm.ChartStartIndex > GlobalForm.ChartPatterns[i].iStartDate) & (num2 + GlobalForm.ChartStartIndex <= GlobalForm.ChartPatterns[i].iEndDate)) && decimal.Compare(GlobalForm.nHLC[1, num2 + GlobalForm.ChartStartIndex], GlobalForm.nHLC[1, num3]) > 0)
				{
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					num3 = num2 + GlobalForm.ChartStartIndex;
				}
				if (((num2 + GlobalForm.ChartStartIndex > GlobalForm.ChartPatterns[i].iStart2Date) & (num2 + GlobalForm.ChartStartIndex <= GlobalForm.ChartPatterns[i].iEnd2Date)) && decimal.Compare(GlobalForm.nHLC[2, num2 + GlobalForm.ChartStartIndex], GlobalForm.nHLC[2, num4]) < 0)
				{
					pointF3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					num4 = num2 + GlobalForm.ChartStartIndex;
					val = item;
					index = num2;
				}
				if (num2 + GlobalForm.ChartStartIndex == num)
				{
					break;
				}
				num2++;
			}
			if (!Information.IsNothing((object)val))
			{
				try
				{
					DrawTextBelow(e, val, index, i);
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					ProjectData.ClearProjectError();
				}
			}
			pointF.X = Conversions.ToSingle(Interaction.IIf(pointF.X < pointF3.X, (object)pointF.X, (object)pointF3.X));
			pointF3.X = pointF.X;
			pointF2.X = Conversions.ToSingle(Interaction.IIf(pointF2.X < pointF4.X, (object)pointF4.X, (object)pointF2.X));
			pointF4.X = pointF2.X;
			pointF2.Y = pointF.Y;
			pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
			pointF.X += 4f;
			pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
			pointF2.X += 4f;
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF, pointF2);
			pointF4.Y = pointF3.Y;
			pointF3 = e.ChartGraphics.GetAbsolutePoint(pointF3);
			pointF3.X += 4f;
			pointF4 = e.ChartGraphics.GetAbsolutePoint(pointF4);
			pointF4.X += 4f;
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF3, pointF4);
		}
	}

	private static void ShowHeadShouldersBottoms(ChartPaintEventArgs e, Series series, int i)
	{
		string text = Conversions.ToString(Interaction.IIf(Operators.CompareString(Strings.Right(GlobalForm.ChartPatterns[i].iText, 1), "?", false) == 0, (object)"?", (object)""));
		int num = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if ((num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate) | (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate) | (((GlobalForm.ChartPatterns[i].iStart2Date != 0) & (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)) | ((GlobalForm.ChartPatterns[i].iEnd2Date != 0) & (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date))))
				{
					GlobalForm.ChartPatterns[i].iText = "S" + text;
					DrawTextBelow(e, item, num, i);
				}
				if ((num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate) | ((GlobalForm.ChartPatterns[i].iMid2Date != 0) & (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMid2Date)))
				{
					GlobalForm.ChartPatterns[i].iText = "H" + text;
					DrawTextBelow(e, item, num, i);
				}
				if ((GlobalForm.ChartPatterns[i].iEnd2Date != 0) & (GlobalForm.ChartPatterns[i].iEndDate < GlobalForm.ChartPatterns[i].iEnd2Date))
				{
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date)
					{
						ShowHSTarget(e, series, i, num);
						break;
					}
				}
				else if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					ShowHSTarget(e, series, i, num);
					break;
				}
				num++;
			}
		}
	}

	private static void ShowHeadShouldersTops(ChartPaintEventArgs e, Series series, int i)
	{
		string text = Conversions.ToString(Interaction.IIf(Operators.CompareString(Strings.Right(GlobalForm.ChartPatterns[i].iText, 1), "?", false) == 0, (object)"?", (object)""));
		int num = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if ((num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate) | (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate) | (((GlobalForm.ChartPatterns[i].iStart2Date != 0) & (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)) | ((GlobalForm.ChartPatterns[i].iEnd2Date != 0) & (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date))))
				{
					GlobalForm.ChartPatterns[i].iText = "S" + text;
					DrawTextAbove(e, item, num, i);
				}
				if ((num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate) | ((GlobalForm.ChartPatterns[i].iMid2Date != 0) & (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMid2Date)))
				{
					GlobalForm.ChartPatterns[i].iText = "H" + text;
					DrawTextAbove(e, item, num, i);
				}
				if ((GlobalForm.ChartPatterns[i].iEnd2Date != 0) & (GlobalForm.ChartPatterns[i].iEndDate < GlobalForm.ChartPatterns[i].iEnd2Date))
				{
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date)
					{
						ShowHSTarget(e, series, i, num);
						break;
					}
				}
				else if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					ShowHSTarget(e, series, i, num);
					break;
				}
				num++;
			}
		}
	}

	private static void ShowHighTightFlag(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_0031: Unknown result type (might be due to invalid IL or missing references)
		//IL_0038: Expected O, but got Unknown
		PointF empty = PointF.Empty;
		int num = 0;
		Pen val = (Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red);
		checked
		{
			PointF pointF = default(PointF);
			PointF pointF2 = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					DrawTextAbove(e, item, num, i);
					pointF.X = (float)(e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num) + 1.0);
					empty.X = pointF.X;
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF2.Y = pointF.Y;
					empty.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					empty = e.ChartGraphics.GetAbsolutePoint(empty);
					e.ChartGraphics.Graphics.DrawLine(val, pointF, empty);
					pointF2.Y = empty.Y + (pointF.Y - empty.Y) / 8f;
					pointF2.X = empty.X + 30f;
					e.ChartGraphics.Graphics.DrawLine(val, empty, pointF2);
					empty.Y = pointF2.Y;
					e.ChartGraphics.Graphics.DrawLine(val, pointF2, empty);
					ShowTarget(e, series, i, num);
					break;
				}
				num++;
			}
		}
	}

	private static void ShowChannels(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_01f4: Unknown result type (might be due to invalid IL or missing references)
		//IL_0201: Expected O, but got Unknown
		//IL_0235: Unknown result type (might be due to invalid IL or missing references)
		//IL_0241: Expected O, but got Unknown
		//IL_046e: Unknown result type (might be due to invalid IL or missing references)
		//IL_047b: Expected O, but got Unknown
		//IL_04af: Unknown result type (might be due to invalid IL or missing references)
		//IL_04bb: Expected O, but got Unknown
		decimal dChannelHeight = GlobalForm.ChartPatterns[i].dChannelHeight;
		int num = 0;
		checked
		{
			PointF absolutePoint = default(PointF);
			PointF absolutePoint2 = default(PointF);
			PointF absolutePoint3 = default(PointF);
			PointF absolutePoint4 = default(PointF);
			if (GlobalForm.ChartPatterns[i].Type == 1)
			{
				foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
				{
					if (GlobalForm.ChartPatterns[i].RenderColor == Color.Red)
					{
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
						{
							absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(dChannelHeight) + item.YValues[1]);
							absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint2.X = absolutePoint.X;
							absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
							absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
							absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						}
						if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
						{
							absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(dChannelHeight) + item.YValues[1]);
							absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
							absolutePoint4.X = absolutePoint3.X;
							absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
							absolutePoint4.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
							absolutePoint4 = e.ChartGraphics.GetAbsolutePoint(absolutePoint4);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint3);
							e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint4);
							GlobalForm.ChartPatterns[i].PriceTarget = GlobalForm.ChartPatterns[i].PriceTarget;
							ShowTarget(e, series, i, num + 1);
						}
					}
					num++;
				}
				return;
			}
			if (GlobalForm.ChartPatterns[i].Type != 82)
			{
				return;
			}
			foreach (DataPoint item2 in (Collection<DataPoint>)(object)series.Points)
			{
				if (GlobalForm.ChartPatterns[i].RenderColor == Color.Red)
				{
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
					{
						absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0] - Convert.ToDouble(dChannelHeight));
						absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint2.X = absolutePoint.X;
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0]);
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
					{
						absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0] - Convert.ToDouble(dChannelHeight));
						absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint4.X = absolutePoint3.X;
						absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
						absolutePoint4.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0]);
						absolutePoint4 = e.ChartGraphics.GetAbsolutePoint(absolutePoint4);
						e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint3);
						e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint4);
						GlobalForm.ChartPatterns[i].PriceTarget = GlobalForm.ChartPatterns[i].PriceTarget;
						ShowTarget(e, series, i, num + 1);
					}
				}
				num++;
			}
		}
	}

	private static void ShowCup(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_016b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0199: Unknown result type (might be due to invalid IL or missing references)
		//IL_01a5: Expected O, but got Unknown
		//IL_01a5: Expected O, but got Unknown
		bool flag = Conversions.ToBoolean(Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)true, (object)false));
		int num = 0;
		checked
		{
			PointF absolutePoint = default(PointF);
			PointF absolutePoint2 = default(PointF);
			PointF absolutePoint3 = default(PointF);
			PointF pointF = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					if (GlobalForm.ChartPatterns[i].Type == 66)
					{
						absolutePoint2.Y = absolutePoint.Y;
					}
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
				}
				if ((num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate) | (num + GlobalForm.ChartStartIndex == GlobalForm.ChartEndIndex))
				{
					absolutePoint3.Y = absolutePoint.Y - 2f;
					absolutePoint3.X = absolutePoint.X;
					absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
					e.ChartGraphics.Graphics.DrawString(GlobalForm.ChartPatterns[i].iText, (Font)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)BoldFont, (object)drawFont), (Brush)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)Brushes.Red, (object)Brushes.Black), absolutePoint3);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
				{
					if (GlobalForm.ChartPatterns[i].Type == 81)
					{
						absolutePoint2.Y = absolutePoint.Y;
					}
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
					if (flag)
					{
						e.ChartGraphics.Graphics.DrawLine(Pens.Red, absolutePoint, absolutePoint2);
						if (GlobalForm.ChartPatterns[i].Type == 66)
						{
							ShowTarget(e, series, i, num);
						}
					}
					if (GlobalForm.ChartPatterns[i].Type == 66)
					{
						break;
					}
				}
				if (GlobalForm.ChartPatterns[i].Type == 81 && num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF.Y = absolutePoint2.Y;
					if (flag)
					{
						e.ChartGraphics.Graphics.DrawLine(Pens.Blue, absolutePoint2, pointF);
						ShowTarget(e, series, i, num);
						e.ChartGraphics.Graphics.DrawString("Handle", BoldFont, Brushes.Blue, absolutePoint2);
					}
					break;
				}
				num++;
			}
		}
	}

	private static void ShowDeadCatBounce(ChartPaintEventArgs e, Series series, int i)
	{
		int num = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					DrawTextAbove(e, item, num, i);
					ShowTarget(e, series, i, num);
					break;
				}
				num++;
			}
		}
	}

	private static void ShowIslands(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_02be: Unknown result type (might be due to invalid IL or missing references)
		//IL_02ec: Unknown result type (might be due to invalid IL or missing references)
		//IL_02f8: Expected O, but got Unknown
		//IL_02f8: Expected O, but got Unknown
		bool flag = Conversions.ToBoolean(Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)true, (object)false));
		int num = 0;
		checked
		{
			int num2 = default(int);
			int num3 = default(int);
			int num4 = default(int);
			PointF absolutePoint = default(PointF);
			PointF pointF = default(PointF);
			PointF pointF2 = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					num2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, num + GlobalForm.ChartStartIndex - 1], GlobalForm.nHLC[2, num + GlobalForm.ChartStartIndex]) < 0, (object)1, (object)(-1)));
					if (num2 == 1)
					{
						pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					}
					else
					{
						pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					}
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					num3 = num;
					num4 = num;
				}
				else if ((num + GlobalForm.ChartStartIndex > GlobalForm.ChartPatterns[i].iStartDate) & (num + GlobalForm.ChartStartIndex <= GlobalForm.ChartPatterns[i].iEndDate))
				{
					if (num2 == 1)
					{
						if (decimal.Compare(GlobalForm.nHLC[2, num + GlobalForm.ChartStartIndex], GlobalForm.nHLC[2, num3 + GlobalForm.ChartStartIndex]) < 0)
						{
							num3 = num;
							pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
						}
					}
					else if (decimal.Compare(GlobalForm.nHLC[1, num + GlobalForm.ChartStartIndex], GlobalForm.nHLC[1, num4 + GlobalForm.ChartStartIndex]) > 0)
					{
						num4 = num;
						pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					}
				}
				if ((num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate) | (num + GlobalForm.ChartStartIndex == GlobalForm.ChartEndIndex))
				{
					if (num2 == 1)
					{
						absolutePoint.Y = pointF.Y;
					}
					else
					{
						absolutePoint.Y = pointF.Y - 2f;
					}
					absolutePoint.X = pointF.X;
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					e.ChartGraphics.Graphics.DrawString(GlobalForm.ChartPatterns[i].iText, (Font)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)BoldFont, (object)drawFont), (Brush)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)Brushes.Red, (object)Brushes.Black), absolutePoint);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					pointF2.Y = pointF.Y;
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
					if (flag)
					{
						e.ChartGraphics.Graphics.DrawLine(Pens.Red, pointF, pointF2);
						ShowTarget(e, series, i, num);
					}
					break;
				}
				num++;
			}
		}
	}

	private static void ShowInvertedDCB(ChartPaintEventArgs e, Series series, int i, Font drawFont)
	{
		//IL_00ed: Unknown result type (might be due to invalid IL or missing references)
		//IL_00f8: Expected O, but got Unknown
		PointF empty = PointF.Empty;
		int num = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					empty.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					empty.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					PointF absolutePoint = e.ChartGraphics.GetAbsolutePoint(empty);
					absolutePoint.X -= GlobalForm.StringSize.Width / 2f;
					e.ChartGraphics.Graphics.DrawString(GlobalForm.ChartPatterns[i].iText, drawFont, (Brush)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)Brushes.Red, (object)Brushes.Black), absolutePoint);
					ShowTarget(e, series, i, num + 1);
					break;
				}
				num++;
			}
		}
	}

	private static void ShowMeasuredMoves(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_0146: Unknown result type (might be due to invalid IL or missing references)
		//IL_0152: Expected O, but got Unknown
		//IL_044c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0458: Expected O, but got Unknown
		//IL_01f0: Unknown result type (might be due to invalid IL or missing references)
		//IL_01fc: Expected O, but got Unknown
		//IL_04f6: Unknown result type (might be due to invalid IL or missing references)
		//IL_0502: Expected O, but got Unknown
		//IL_02af: Unknown result type (might be due to invalid IL or missing references)
		//IL_02bb: Expected O, but got Unknown
		//IL_05b5: Unknown result type (might be due to invalid IL or missing references)
		//IL_05c1: Expected O, but got Unknown
		int num = 0;
		checked
		{
			PointF absolutePoint = default(PointF);
			PointF absolutePoint2 = default(PointF);
			PointF absolutePoint3 = default(PointF);
			PointF pointF = default(PointF);
			if (GlobalForm.ChartPatterns[i].Type == 73)
			{
				foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
				{
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
					{
						absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
						absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						DrawTextBelow(e, item, num, i);
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
					{
						absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
						absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint2);
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
					{
						absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
						absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
						e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint3);
					}
					if (GlobalForm.ChartPatterns[i].iEndDate != 0 && num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
					{
						pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
						pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
						e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint3, pointF);
						if (GlobalForm.ChartPatterns[i].RenderColor == Color.Red)
						{
							ShowTarget(e, series, i, num);
						}
						break;
					}
					num++;
				}
				return;
			}
			if (GlobalForm.ChartPatterns[i].Type != 74)
			{
				return;
			}
			foreach (DataPoint item2 in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0]);
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					DrawTextAbove(e, item2, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
				{
					absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[1]);
					absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
					e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint2);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
				{
					absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0]);
					absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
					e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint3);
				}
				if (GlobalForm.ChartPatterns[i].iEndDate != 0 && num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[1]);
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint3, pointF);
					if (GlobalForm.ChartPatterns[i].RenderColor == Color.Red)
					{
						ShowTarget(e, series, i, num);
					}
					break;
				}
				num++;
			}
		}
	}

	private static void ShowNR47(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_051d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0528: Expected O, but got Unknown
		//IL_0481: Unknown result type (might be due to invalid IL or missing references)
		//IL_048c: Expected O, but got Unknown
		PointF empty = PointF.Empty;
		bool flag = Conversions.ToBoolean(Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)true, (object)false));
		if (!flag)
		{
			if ((GlobalForm.ChartPatterns[i].Type == 27) | (GlobalForm.ChartPatterns[i].Type == 26))
			{
				GlobalForm.ChartPatterns[i].iText = Conversions.ToString(Interaction.IIf(GlobalForm.ChartPatterns[i].Type == 27, (object)"WW Be", (object)"WW Bu"));
			}
			else if ((GlobalForm.ChartPatterns[i].Type == 4) | (GlobalForm.ChartPatterns[i].Type == 5))
			{
				GlobalForm.ChartPatterns[i].iText = Conversions.ToString(Interaction.IIf(GlobalForm.ChartPatterns[i].Type == 4, (object)"ABCD Be", (object)"ABCD Bu"));
			}
			else if ((GlobalForm.ChartPatterns[i].Type == 11) | (GlobalForm.ChartPatterns[i].Type == 10))
			{
				GlobalForm.ChartPatterns[i].iText = Conversions.ToString(Interaction.IIf(GlobalForm.ChartPatterns[i].Type == 11, (object)"Bat Be", (object)"Bat Bu"));
			}
			else if ((GlobalForm.ChartPatterns[i].Type == 9) | (GlobalForm.ChartPatterns[i].Type == 8))
			{
				GlobalForm.ChartPatterns[i].iText = Conversions.ToString(Interaction.IIf(GlobalForm.ChartPatterns[i].Type == 9, (object)"Butt Be", (object)"Butt Bu"));
			}
			else if ((GlobalForm.ChartPatterns[i].Type == 7) | (GlobalForm.ChartPatterns[i].Type == 6))
			{
				GlobalForm.ChartPatterns[i].iText = Conversions.ToString(Interaction.IIf(GlobalForm.ChartPatterns[i].Type == 7, (object)"Crab Be", (object)"Crab Bu"));
			}
			else if ((GlobalForm.ChartPatterns[i].Type == 28) | (GlobalForm.ChartPatterns[i].Type == 29))
			{
				GlobalForm.ChartPatterns[i].iText = Conversions.ToString(Interaction.IIf(GlobalForm.ChartPatterns[i].Type == 28, (object)"Gar Be", (object)"Gar Bu"));
			}
		}
		int num = 0;
		checked
		{
			int num2 = default(int);
			PointF absolutePoint = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					num2 = num;
					empty.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
				}
				else if (((num + GlobalForm.ChartStartIndex > GlobalForm.ChartPatterns[i].iStartDate) & (num + GlobalForm.ChartStartIndex <= GlobalForm.ChartPatterns[i].iEndDate)) && decimal.Compare(GlobalForm.nHLC[2, num + GlobalForm.ChartStartIndex], GlobalForm.nHLC[2, num2 + GlobalForm.ChartStartIndex]) < 0)
				{
					num2 = num;
					empty.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(empty);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					empty.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(empty);
				}
				if ((num + GlobalForm.ChartStartIndex >= GlobalForm.ChartPatterns[i].iEndDate) | (num + GlobalForm.ChartStartIndex == GlobalForm.ChartEndIndex))
				{
					empty.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					empty = e.ChartGraphics.GetAbsolutePoint(empty);
					if (flag)
					{
						e.ChartGraphics.Graphics.DrawString(GlobalForm.ChartPatterns[i].iText, BoldFont, (Brush)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)Brushes.Red, (object)Brushes.Black), absolutePoint);
						ShowTarget(e, series, i, num);
						int type = GlobalForm.ChartPatterns[i].Type;
						if (unchecked((uint)(type - 4) > 7u && (uint)(type - 26) > 3u))
						{
							e.ChartGraphics.Graphics.DrawLine(Pens.Red, absolutePoint, empty);
						}
					}
					else
					{
						e.ChartGraphics.Graphics.DrawString(GlobalForm.ChartPatterns[i].iText, drawFont, (Brush)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)Brushes.Red, (object)Brushes.Black), absolutePoint);
					}
					break;
				}
				num++;
			}
		}
	}

	private static void ShowPennant(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_0035: Unknown result type (might be due to invalid IL or missing references)
		//IL_003c: Expected O, but got Unknown
		PointF pointF = PointF.Empty;
		DataPoint point = null;
		int num = 0;
		Pen val = (Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red);
		int type = GlobalForm.ChartPatterns[i].Type;
		int num2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, GlobalForm.ChartPatterns[i].iStartDate], GlobalForm.nHLC[1, GlobalForm.ChartPatterns[i].iMidDate]) < 0, (object)1, (object)(-1)));
		checked
		{
			PointF absolutePoint = default(PointF);
			int index = default(int);
			PointF absolutePoint2 = default(PointF);
			PointF absolutePoint3 = default(PointF);
			PointF pointF2 = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[Conversions.ToInteger(Interaction.IIf(num2 == 1, (object)1, (object)0))]);
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					index = num;
					point = item;
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[Conversions.ToInteger(Interaction.IIf(num2 == 1, (object)0, (object)1))]);
					absolutePoint2.X = pointF.X;
					absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
					absolutePoint3.X = pointF.X;
					absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					e.ChartGraphics.Graphics.DrawLine(val, absolutePoint, pointF);
					if (absolutePoint.Y < pointF.Y)
					{
						DrawTextAbove(e, point, index, i);
					}
					else
					{
						DrawTextBelow(e, point, index, i);
					}
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					pointF2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[Conversions.ToInteger(Interaction.IIf(type == 67, (object)3, (object)0))]);
					pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
					PointF pointF3 = pointF2;
					e.ChartGraphics.Graphics.DrawLine(val, absolutePoint2, pointF2);
					if (type == 67)
					{
						e.ChartGraphics.Graphics.DrawLine(val, absolutePoint3, pointF2);
					}
					else
					{
						pointF3.Y = pointF2.Y - (absolutePoint2.Y - absolutePoint3.Y);
						e.ChartGraphics.Graphics.DrawLine(val, absolutePoint3, pointF3);
					}
					ShowTarget(e, series, i, num);
					break;
				}
				num++;
			}
		}
	}

	private static void ShowPipeBottoms(ChartPaintEventArgs e, Series series, int i)
	{
		int num = -1;
		int num2 = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					if (decimal.Compare(GlobalForm.nHLC[2, GlobalForm.ChartPatterns[i].iStartDate], GlobalForm.nHLC[2, GlobalForm.ChartPatterns[i].iEndDate]) < 0)
					{
						DrawTextBelow(e, item, num2, i);
					}
					else
					{
						num = num2;
					}
				}
				else if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					if (num != -1)
					{
						DrawTextBelow(e, item, num, i);
					}
					ShowTarget(e, series, i, num2);
					break;
				}
				num2++;
			}
		}
	}

	private static void ShowPipeTops(ChartPaintEventArgs e, Series series, int i)
	{
		int num = -1;
		int num2 = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					if (decimal.Compare(GlobalForm.nHLC[1, GlobalForm.ChartPatterns[i].iStartDate], GlobalForm.nHLC[1, GlobalForm.ChartPatterns[i].iEndDate]) > 0)
					{
						DrawTextAbove(e, item, num2, i);
					}
					else
					{
						num = num2;
					}
				}
				else if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					if (num != -1)
					{
						DrawTextAbove(e, item, num, i);
					}
					ShowTarget(e, series, i, num2);
					break;
				}
				num2++;
			}
		}
	}

	private static void ShowPothole(ChartPaintEventArgs e, Series series, int i)
	{
		bool flag = Conversions.ToBoolean(Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)true, (object)false));
		int num = 0;
		checked
		{
			PointF absolutePoint = default(PointF);
			PointF absolutePoint3 = default(PointF);
			PointF absolutePoint2 = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					absolutePoint2.Y = absolutePoint.Y;
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					DrawTextBelow(e, item, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
				{
					absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
					if (flag)
					{
						e.ChartGraphics.Graphics.DrawLine(Pens.Red, absolutePoint, absolutePoint2);
					}
				}
				if (GlobalForm.ChartPatterns[i].iMid2Date != 0 && num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMid2Date)
				{
					absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
					if (flag)
					{
						e.ChartGraphics.Graphics.DrawLine(Pens.Red, absolutePoint2, absolutePoint3);
					}
				}
				if (((GlobalForm.ChartPatterns[i].iEndDate != 0) & (GlobalForm.ChartPatterns[i].iMid2Date != 0)) && num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
					if (flag)
					{
						e.ChartGraphics.Graphics.DrawLine(Pens.Red, absolutePoint3, absolutePoint2);
						ShowTarget(e, series, i, num);
					}
					break;
				}
				num++;
			}
		}
	}

	private static void ShowRectangles(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_0446: Unknown result type (might be due to invalid IL or missing references)
		//IL_0453: Expected O, but got Unknown
		//IL_04db: Unknown result type (might be due to invalid IL or missing references)
		//IL_04e9: Expected O, but got Unknown
		DataPoint val = null;
		PointF pointF = default(PointF);
		PointF pointF2 = default(PointF);
		PointF pointF3 = default(PointF);
		PointF pointF4 = default(PointF);
		int num = Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iEndDate > GlobalForm.ChartPatterns[i].iEnd2Date, (object)GlobalForm.ChartPatterns[i].iEndDate, (object)GlobalForm.ChartPatterns[i].iEnd2Date));
		int num2 = 0;
		checked
		{
			int num3 = default(int);
			int num4 = default(int);
			int index = default(int);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num2);
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					num3 = num2 + GlobalForm.ChartStartIndex;
				}
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num2);
				}
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
				{
					pointF3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num2);
					pointF3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					num4 = num2 + GlobalForm.ChartStartIndex;
					val = item;
					index = num2;
				}
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date)
				{
					pointF4.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num2);
				}
				if (((num2 + GlobalForm.ChartStartIndex > GlobalForm.ChartPatterns[i].iStartDate) & (num2 + GlobalForm.ChartStartIndex <= GlobalForm.ChartPatterns[i].iEndDate)) && decimal.Compare(GlobalForm.nHLC[1, num2 + GlobalForm.ChartStartIndex], GlobalForm.nHLC[1, num3]) > 0)
				{
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					num3 = num2 + GlobalForm.ChartStartIndex;
				}
				if (((num2 + GlobalForm.ChartStartIndex > GlobalForm.ChartPatterns[i].iStart2Date) & (num2 + GlobalForm.ChartStartIndex <= GlobalForm.ChartPatterns[i].iEnd2Date)) && decimal.Compare(GlobalForm.nHLC[2, num2 + GlobalForm.ChartStartIndex], GlobalForm.nHLC[2, num4]) < 0)
				{
					pointF3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					num4 = num2 + GlobalForm.ChartStartIndex;
					val = item;
					index = num2;
				}
				if (num2 + GlobalForm.ChartStartIndex == num)
				{
					ShowTarget(e, series, i, num2);
					break;
				}
				num2++;
			}
			if (!Information.IsNothing((object)val))
			{
				try
				{
					DrawTextBelow(e, val, index, i);
				}
				catch (Exception ex)
				{
					ProjectData.SetProjectError(ex);
					Exception ex2 = ex;
					ProjectData.ClearProjectError();
				}
			}
			pointF.X = Conversions.ToSingle(Interaction.IIf(pointF.X < pointF3.X, (object)pointF.X, (object)pointF3.X));
			pointF3.X = pointF.X;
			pointF2.X = Conversions.ToSingle(Interaction.IIf(pointF2.X < pointF4.X, (object)pointF4.X, (object)pointF2.X));
			pointF4.X = pointF2.X;
			pointF2.Y = pointF.Y;
			pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
			pointF.X += 4f;
			pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
			pointF2.X += 4f;
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF, pointF2);
			pointF4.Y = pointF3.Y;
			pointF3 = e.ChartGraphics.GetAbsolutePoint(pointF3);
			pointF3.X += 4f;
			pointF4 = e.ChartGraphics.GetAbsolutePoint(pointF4);
			pointF4.X += 4f;
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF3, pointF4);
		}
	}

	private static void ShowWedges(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_0556: Unknown result type (might be due to invalid IL or missing references)
		//IL_0564: Expected O, but got Unknown
		//IL_0598: Unknown result type (might be due to invalid IL or missing references)
		//IL_05a6: Expected O, but got Unknown
		//IL_06d5: Unknown result type (might be due to invalid IL or missing references)
		//IL_06e3: Expected O, but got Unknown
		//IL_0717: Unknown result type (might be due to invalid IL or missing references)
		//IL_0725: Expected O, but got Unknown
		PointF pointF = default(PointF);
		PointF pointF2 = default(PointF);
		PointF pointF3 = default(PointF);
		PointF pointF4 = default(PointF);
		PointF pointF5 = default(PointF);
		int num = Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iEndDate > GlobalForm.ChartPatterns[i].iEnd2Date, (object)GlobalForm.ChartPatterns[i].iEndDate, (object)GlobalForm.ChartPatterns[i].iEnd2Date));
		int num2 = 0;
		checked
		{
			int num3 = default(int);
			int num4 = default(int);
			decimal d = default(decimal);
			decimal num5 = default(decimal);
			decimal d2 = default(decimal);
			decimal d3 = default(decimal);
			decimal d4 = default(decimal);
			int num6 = default(int);
			decimal num7;
			decimal d5;
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					num3 = num2;
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num2 + 1));
				}
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					pointF2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num2 + 1));
					num4 = num2;
				}
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
				{
					pointF3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					DrawTextBelow(e, item, num2, i);
					pointF3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num2 + 1));
				}
				if (num2 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date)
				{
					pointF4.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					pointF4.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num2 + 1));
				}
				if (num2 + GlobalForm.ChartStartIndex == num)
				{
					if ((pointF4.X - pointF3.X != 0f) & (pointF2.X - pointF.X != 0f))
					{
						if (GlobalForm.ChartPatterns[i].iStartDate < GlobalForm.ChartPatterns[i].iStart2Date)
						{
							decimal value = new decimal((pointF4.Y - pointF3.Y) / (pointF4.X - pointF3.X));
							pointF3.Y = Convert.ToSingle(value) * (pointF.X - pointF3.X) + pointF3.Y;
							pointF3.X = pointF.X;
						}
						else
						{
							decimal value = new decimal((pointF2.Y - pointF.Y) / (pointF2.X - pointF.X));
							pointF.X = pointF3.X;
							pointF.Y = Convert.ToSingle(value) * (pointF.X - pointF2.X) + pointF2.Y;
						}
						pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
						pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
						pointF3 = e.ChartGraphics.GetAbsolutePoint(pointF3);
						pointF4 = e.ChartGraphics.GetAbsolutePoint(pointF4);
						d = new decimal((pointF2.Y - pointF.Y) / (pointF2.X - pointF.X));
						num5 = new decimal((pointF4.Y - pointF3.Y) / (pointF4.X - pointF3.X));
						d2 = new decimal(pointF.Y);
						d3 = new decimal(pointF3.Y);
						d4 = new decimal((pointF2.X - pointF.X) / (float)(num4 - num3));
						num6 = 0;
						ShowTarget(e, series, i, num2);
					}
				}
				else if (num2 + GlobalForm.ChartStartIndex > num)
				{
					num7 = decimal.Add(decimal.Multiply(decimal.Multiply(d, new decimal(num2 - num3)), d4), d2);
					d5 = decimal.Add(decimal.Multiply(decimal.Multiply(num5, new decimal(num2 - num3)), d4), d3);
					if (decimal.Compare(d, num5) > 0)
					{
						if (decimal.Compare(num7, d5) >= 0)
						{
							num6 = num2;
							pointF5.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num2);
							pointF5.Y = 0f;
							pointF5 = e.ChartGraphics.GetAbsolutePoint(pointF5);
							pointF5.Y = Convert.ToSingle(num7);
							break;
						}
					}
					else if (decimal.Compare(num7, d5) <= 0)
					{
						num6 = num2;
						pointF5.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num2);
						pointF5.Y = 0f;
						pointF5 = e.ChartGraphics.GetAbsolutePoint(pointF5);
						pointF5.Y = Convert.ToSingle(num7);
						break;
					}
				}
				num2++;
			}
			if (num6 != 0)
			{
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF, pointF5);
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF3, pointF5);
				return;
			}
			num2--;
			num7 = decimal.Add(decimal.Multiply(decimal.Multiply(d, new decimal(num2 - num3)), d4), d2);
			d5 = decimal.Add(decimal.Multiply(decimal.Multiply(num5, new decimal(num2 - num3)), d4), d3);
			if (decimal.Compare(d, num5) > 0)
			{
				pointF5.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num2);
				pointF5.Y = 0f;
				pointF5 = e.ChartGraphics.GetAbsolutePoint(pointF5);
				if (GlobalForm.ChartPatterns[i].Type == 96)
				{
					pointF5.Y = Convert.ToSingle(d5);
				}
				else
				{
					pointF5.Y = Convert.ToSingle(num7);
				}
			}
			else
			{
				pointF5.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num2);
				pointF5.Y = 0f;
				pointF5 = e.ChartGraphics.GetAbsolutePoint(pointF5);
				pointF5.Y = Convert.ToSingle(num7);
			}
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF, pointF5);
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), pointF3, pointF5);
		}
	}

	private static void ShowHSTarget(ChartPaintEventArgs e, Series series, int i, int iPoint)
	{
		if (!(GlobalForm.PatternTargets & (GlobalForm.ChartPatterns[i].RenderColor == Color.Red)))
		{
			return;
		}
		ShowTarget(e, series, i, iPoint);
		if (!GlobalForm.ShowConfirmation)
		{
			return;
		}
		int type = GlobalForm.ChartPatterns[i].Type;
		checked
		{
			int iLeftArmpit = GlobalForm.ChartPatterns[i].iStartDate + 1;
			int iLeftArmpit2 = iLeftArmpit;
			int iRightArmpit = GlobalForm.ChartPatterns[i].iMidDate + 1;
			int iRightArmpit2 = iRightArmpit;
			int iHead;
			int num;
			int num2;
			int iRS;
			int num7;
			PointF pointF;
			PointF pointF2;
			if (unchecked((uint)(type - 93)) > 1u)
			{
				switch (type)
				{
				case 107:
					num = GlobalForm.ChartPatterns[i].iStartDate + 1;
					_ = ref GlobalForm.ChartPatterns[i];
					num2 = GlobalForm.ChartPatterns[i].iMidDate - 1;
					iHead = GlobalForm.ChartPatterns[i].iMidDate;
					break;
				case 108:
					if ((GlobalForm.ChartPatterns[i].iStart2Date != 0) & (GlobalForm.ChartPatterns[i].iStart2Date < GlobalForm.ChartPatterns[i].iStartDate))
					{
						num = GlobalForm.ChartPatterns[i].iStart2Date + 1;
						_ = ref GlobalForm.ChartPatterns[i];
					}
					else
					{
						num = GlobalForm.ChartPatterns[i].iStartDate + 1;
						_ = ref GlobalForm.ChartPatterns[i];
					}
					if ((GlobalForm.ChartPatterns[i].iMid2Date != 0) & (GlobalForm.ChartPatterns[i].iMid2Date < GlobalForm.ChartPatterns[i].iMidDate))
					{
						num2 = GlobalForm.ChartPatterns[i].iMid2Date + 1;
						iHead = GlobalForm.ChartPatterns[i].iMid2Date;
					}
					else
					{
						num2 = GlobalForm.ChartPatterns[i].iMidDate + 1;
						iHead = GlobalForm.ChartPatterns[i].iMidDate;
					}
					break;
				default:
					return;
				}
				int num3 = num;
				int num4 = num2;
				for (int j = num3; j <= num4; j++)
				{
					iLeftArmpit2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.nHLC[2, iLeftArmpit2]) <= 0, (object)j, (object)iLeftArmpit2));
				}
				if (type == 107)
				{
					num = GlobalForm.ChartPatterns[i].iMidDate + 1;
					_ = ref GlobalForm.ChartPatterns[i];
					num2 = GlobalForm.ChartPatterns[i].iEndDate - 1;
					iRS = GlobalForm.ChartPatterns[i].iEndDate;
				}
				else
				{
					if ((GlobalForm.ChartPatterns[i].iMid2Date != 0) & (GlobalForm.ChartPatterns[i].iMid2Date > GlobalForm.ChartPatterns[i].iMidDate))
					{
						num = GlobalForm.ChartPatterns[i].iMid2Date + 1;
						_ = ref GlobalForm.ChartPatterns[i];
					}
					else
					{
						num = GlobalForm.ChartPatterns[i].iMidDate + 1;
						_ = ref GlobalForm.ChartPatterns[i];
					}
					if ((GlobalForm.ChartPatterns[i].iEnd2Date != 0) & (GlobalForm.ChartPatterns[i].iEnd2Date > GlobalForm.ChartPatterns[i].iEndDate))
					{
						num2 = GlobalForm.ChartPatterns[i].iEnd2Date - 1;
						iRS = GlobalForm.ChartPatterns[i].iEnd2Date;
					}
					else
					{
						num2 = GlobalForm.ChartPatterns[i].iEndDate - 1;
						iRS = GlobalForm.ChartPatterns[i].iEndDate;
					}
				}
				int num5 = num;
				int num6 = num2;
				for (int k = num5; k <= num6; k++)
				{
					iRightArmpit2 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, iRightArmpit2]) <= 0, (object)k, (object)iRightArmpit2));
				}
				CheckArmpits(ref iLeftArmpit2, ref iRightArmpit2, iHead, iRS, i);
				num7 = 0;
				pointF = PointF.Empty;
				pointF2 = PointF.Empty;
				foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
				{
					if (num7 + GlobalForm.ChartStartIndex == iLeftArmpit2)
					{
						pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
						pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num7 + 1));
						pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					}
					if (num7 + GlobalForm.ChartStartIndex == iRightArmpit2)
					{
						pointF2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
						pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num7 + 1));
						pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
						break;
					}
					num7++;
				}
				if (!((pointF != PointF.Empty) & (pointF2 != PointF.Empty)))
				{
					return;
				}
				PointF pointF3 = default(PointF);
				if (pointF.Y > pointF2.Y)
				{
					if (pointF.X - pointF2.X != 0f)
					{
						float num8 = (pointF.Y - pointF2.Y) / (pointF.X - pointF2.X);
						pointF3.X = pointF.X + (pointF2.X - pointF.X) * 2f;
						pointF3.Y = num8 * (pointF2.X - pointF.X) * 2f + pointF.Y;
						e.ChartGraphics.Graphics.DrawLine(Pens.Blue, pointF, pointF3);
					}
				}
				else
				{
					pointF3.X = pointF2.X + (pointF2.X - pointF.X) * 2f;
					pointF3.Y = pointF2.Y;
					e.ChartGraphics.Graphics.DrawLine(Pens.Blue, pointF2, pointF3);
				}
				return;
			}
			if (type == 94)
			{
				num = GlobalForm.ChartPatterns[i].iStartDate + 1;
				_ = ref GlobalForm.ChartPatterns[i];
				num2 = GlobalForm.ChartPatterns[i].iMidDate - 1;
				iHead = GlobalForm.ChartPatterns[i].iMidDate;
			}
			else
			{
				if ((GlobalForm.ChartPatterns[i].iStart2Date != 0) & (GlobalForm.ChartPatterns[i].iStart2Date < GlobalForm.ChartPatterns[i].iStartDate))
				{
					num = GlobalForm.ChartPatterns[i].iStart2Date + 1;
					_ = ref GlobalForm.ChartPatterns[i];
				}
				else
				{
					num = GlobalForm.ChartPatterns[i].iStartDate + 1;
					_ = ref GlobalForm.ChartPatterns[i];
				}
				if ((GlobalForm.ChartPatterns[i].iMid2Date != 0) & (GlobalForm.ChartPatterns[i].iMid2Date < GlobalForm.ChartPatterns[i].iMidDate))
				{
					num2 = GlobalForm.ChartPatterns[i].iMid2Date + 1;
					iHead = GlobalForm.ChartPatterns[i].iMid2Date;
				}
				else
				{
					num2 = GlobalForm.ChartPatterns[i].iMidDate + 1;
					iHead = GlobalForm.ChartPatterns[i].iMidDate;
				}
			}
			int num9 = num;
			int num10 = num2;
			for (int l = num9; l <= num10; l++)
			{
				iLeftArmpit = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, l], GlobalForm.nHLC[1, iLeftArmpit]) >= 0, (object)l, (object)iLeftArmpit));
			}
			if (type == 94)
			{
				num = GlobalForm.ChartPatterns[i].iMidDate + 1;
				_ = ref GlobalForm.ChartPatterns[i];
				num2 = GlobalForm.ChartPatterns[i].iEndDate - 1;
				iRS = GlobalForm.ChartPatterns[i].iEndDate;
			}
			else
			{
				if ((GlobalForm.ChartPatterns[i].iMid2Date != 0) & (GlobalForm.ChartPatterns[i].iMid2Date > GlobalForm.ChartPatterns[i].iMidDate))
				{
					num = GlobalForm.ChartPatterns[i].iMid2Date + 1;
					_ = ref GlobalForm.ChartPatterns[i];
				}
				else
				{
					num = GlobalForm.ChartPatterns[i].iMidDate + 1;
					_ = ref GlobalForm.ChartPatterns[i];
				}
				if ((GlobalForm.ChartPatterns[i].iEnd2Date != 0) & (GlobalForm.ChartPatterns[i].iEnd2Date > GlobalForm.ChartPatterns[i].iEndDate))
				{
					num2 = GlobalForm.ChartPatterns[i].iEnd2Date - 1;
					iRS = GlobalForm.ChartPatterns[i].iEnd2Date;
				}
				else
				{
					num2 = GlobalForm.ChartPatterns[i].iEndDate - 1;
					iRS = GlobalForm.ChartPatterns[i].iEndDate;
				}
			}
			int num11 = num;
			int num12 = num2;
			for (int m = num11; m <= num12; m++)
			{
				iRightArmpit = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, m], GlobalForm.nHLC[1, iRightArmpit]) >= 0, (object)m, (object)iRightArmpit));
			}
			CheckArmpits(ref iLeftArmpit, ref iRightArmpit, iHead, iRS, i);
			num7 = 0;
			pointF = PointF.Empty;
			pointF2 = PointF.Empty;
			foreach (DataPoint item2 in (Collection<DataPoint>)(object)series.Points)
			{
				if (num7 + GlobalForm.ChartStartIndex == iLeftArmpit)
				{
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0]);
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num7 + 1));
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
				}
				if (num7 + GlobalForm.ChartStartIndex == iRightArmpit)
				{
					pointF2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[0]);
					pointF2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num7 + 1));
					pointF2 = e.ChartGraphics.GetAbsolutePoint(pointF2);
					break;
				}
				num7++;
			}
			if (!((pointF != PointF.Empty) & (pointF2 != PointF.Empty)))
			{
				return;
			}
			PointF pointF4 = default(PointF);
			if (pointF.Y < pointF2.Y)
			{
				if (pointF.X - pointF2.X != 0f)
				{
					float num13 = (pointF.Y - pointF2.Y) / (pointF.X - pointF2.X);
					pointF4.X = pointF.X + (pointF2.X - pointF.X) * 2f;
					pointF4.Y = num13 * (pointF2.X - pointF.X) * 2f + pointF.Y;
					e.ChartGraphics.Graphics.DrawLine(Pens.Blue, pointF, pointF4);
				}
			}
			else
			{
				pointF4.X = pointF2.X + (pointF2.X - pointF.X) * 2f;
				pointF4.Y = pointF2.Y;
				e.ChartGraphics.Graphics.DrawLine(Pens.Blue, pointF2, pointF4);
			}
		}
	}

	private static void CheckArmpits(ref int iLeftArmpit, ref int iRightArmpit, int iHead, int iRS, int i)
	{
		checked
		{
			if (iRightArmpit - iLeftArmpit == 0)
			{
				return;
			}
			if ((GlobalForm.ChartPatterns[i].Type == 107) | (GlobalForm.ChartPatterns[i].Type == 108))
			{
				if (decimal.Compare(GlobalForm.nHLC[2, iLeftArmpit], GlobalForm.nHLC[2, iRightArmpit]) >= 0)
				{
					return;
				}
				int num = iLeftArmpit;
				int num2 = iRS - 1;
				for (int j = num; j <= num2; j++)
				{
					float num3 = Convert.ToSingle(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[2, iLeftArmpit], GlobalForm.nHLC[2, iRightArmpit]), new decimal(iLeftArmpit - iRightArmpit)));
					if (Convert.ToSingle(GlobalForm.nHLC[2, j]) < num3 * (float)(j - iLeftArmpit) + Convert.ToSingle(GlobalForm.nHLC[2, iLeftArmpit]))
					{
						if (j < iHead)
						{
							iLeftArmpit = j;
						}
						else
						{
							iRightArmpit = j;
						}
					}
				}
			}
			else
			{
				if (decimal.Compare(GlobalForm.nHLC[1, iLeftArmpit], GlobalForm.nHLC[1, iRightArmpit]) <= 0)
				{
					return;
				}
				int num4 = iLeftArmpit;
				int num5 = iRS - 1;
				for (int j = num4; j <= num5; j++)
				{
					float num3 = Convert.ToSingle(decimal.Divide(decimal.Subtract(GlobalForm.nHLC[1, iLeftArmpit], GlobalForm.nHLC[1, iRightArmpit]), new decimal(iLeftArmpit - iRightArmpit)));
					if (Convert.ToSingle(GlobalForm.nHLC[1, j]) > num3 * (float)(j - iLeftArmpit) + Convert.ToSingle(GlobalForm.nHLC[1, iLeftArmpit]))
					{
						if (j < iHead)
						{
							iLeftArmpit = j;
						}
						else
						{
							iRightArmpit = j;
						}
					}
				}
			}
		}
	}

	private static void ShowSymTriangles(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_067a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0686: Expected O, but got Unknown
		//IL_06ba: Unknown result type (might be due to invalid IL or missing references)
		//IL_06c7: Expected O, but got Unknown
		//IL_05f7: Unknown result type (might be due to invalid IL or missing references)
		//IL_0604: Expected O, but got Unknown
		//IL_0638: Unknown result type (might be due to invalid IL or missing references)
		//IL_0645: Expected O, but got Unknown
		int num = Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iStartDate < GlobalForm.ChartPatterns[i].iStart2Date, (object)GlobalForm.ChartPatterns[i].iStartDate, (object)GlobalForm.ChartPatterns[i].iStart2Date));
		int num2 = Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iEndDate > GlobalForm.ChartPatterns[i].iEnd2Date, (object)GlobalForm.ChartPatterns[i].iEnd2Date, (object)GlobalForm.ChartPatterns[i].iEndDate));
		int num3 = Conversions.ToInteger(Interaction.IIf(GlobalForm.ChartPatterns[i].iEndDate > GlobalForm.ChartPatterns[i].iEnd2Date, (object)GlobalForm.ChartPatterns[i].iEndDate, (object)GlobalForm.ChartPatterns[i].iEnd2Date));
		bool flag = false;
		int num4 = 0;
		checked
		{
			if (((Collection<DataPoint>)(object)series.Points).Count + GlobalForm.ChartStartIndex < num || ((num2 > ((Collection<DataPoint>)(object)series.Points).Count + GlobalForm.ChartStartIndex) | (num3 > ((Collection<DataPoint>)(object)series.Points).Count + GlobalForm.ChartStartIndex)))
			{
				return;
			}
			int num5 = default(int);
			PointF absolutePoint = default(PointF);
			PointF absolutePoint2 = default(PointF);
			PointF absolutePoint3 = default(PointF);
			PointF absolutePoint4 = default(PointF);
			float num6 = default(float);
			float num7 = default(float);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num4 + GlobalForm.ChartStartIndex == num)
				{
					num5 = num4 + 1;
				}
				if (num4 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num4 + 1));
				}
				if (num4 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num4 + 1));
				}
				if (num4 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
				{
					absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num4 + 1));
					DrawTextBelow(e, item, num4, i);
				}
				if (num4 + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date)
				{
					absolutePoint4.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					absolutePoint4.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num4 + 1));
				}
				if (num4 + GlobalForm.ChartStartIndex == num3)
				{
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
					absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
					absolutePoint4 = e.ChartGraphics.GetAbsolutePoint(absolutePoint4);
					if ((absolutePoint2.X - absolutePoint.X == 0f) | (absolutePoint4.X - absolutePoint3.X == 0f))
					{
						return;
					}
					num6 = (absolutePoint2.Y - absolutePoint.Y) / (absolutePoint2.X - absolutePoint.X);
					num7 = (absolutePoint4.Y - absolutePoint3.Y) / (absolutePoint4.X - absolutePoint3.X);
					if (GlobalForm.ChartPatterns[i].iStartDate <= GlobalForm.ChartPatterns[i].iStart2Date)
					{
						absolutePoint3.Y -= num7 * (absolutePoint3.X - absolutePoint.X);
						absolutePoint3.X = absolutePoint.X;
					}
					else
					{
						absolutePoint.Y -= num6 * (absolutePoint.X - absolutePoint3.X);
						absolutePoint.X = absolutePoint3.X;
					}
					if (GlobalForm.ChartPatterns[i].iEndDate <= GlobalForm.ChartPatterns[i].iEnd2Date)
					{
						absolutePoint4.Y -= num7 * (absolutePoint4.X - absolutePoint2.X);
						absolutePoint4.X = absolutePoint2.X;
					}
					else
					{
						absolutePoint2.Y -= num6 * (absolutePoint2.X - absolutePoint4.X);
						absolutePoint2.X = absolutePoint4.X;
					}
					ShowTarget(e, series, i, num4 + 1);
					break;
				}
				num4++;
			}
			num4 = 0;
			int num8 = default(int);
			float num9 = default(float);
			PointF absolutePoint5 = default(PointF);
			foreach (DataPoint item2 in (Collection<DataPoint>)(object)series.Points)
			{
				_ = item2;
				if (num4 + GlobalForm.ChartStartIndex == num2)
				{
					num8 = num4 + 1;
					if (num8 - num5 == 0)
					{
						break;
					}
					num9 = (absolutePoint2.X - absolutePoint.X) / (float)(num8 - num5);
				}
				if (num4 + GlobalForm.ChartStartIndex > num2)
				{
					float num10 = num6 * (float)(num4 + 1 - num8) * num9 + absolutePoint2.Y;
					float num11 = num7 * (float)(num4 + 1 - num8) * num9 + absolutePoint4.Y;
					if (num10 >= num11)
					{
						flag = true;
						absolutePoint5.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num4 + 1));
						absolutePoint5 = e.ChartGraphics.GetAbsolutePoint(absolutePoint5);
						absolutePoint5.Y = num10;
						break;
					}
				}
				num4++;
			}
			if (flag)
			{
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint5);
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint3, absolutePoint5);
			}
			else
			{
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint2);
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint3, absolutePoint4);
			}
		}
	}

	private static void ShowTarget(ChartPaintEventArgs e, Series series, int i, int iPoint)
	{
		//IL_0273: Unknown result type (might be due to invalid IL or missing references)
		//IL_027a: Expected O, but got Unknown
		//IL_04db: Unknown result type (might be due to invalid IL or missing references)
		//IL_04e2: Expected O, but got Unknown
		//IL_06e8: Unknown result type (might be due to invalid IL or missing references)
		//IL_06f3: Expected O, but got Unknown
		//IL_04bb: Unknown result type (might be due to invalid IL or missing references)
		//IL_04c6: Expected O, but got Unknown
		//IL_0441: Unknown result type (might be due to invalid IL or missing references)
		//IL_044c: Expected O, but got Unknown
		if (!GlobalForm.PatternTargets || !(GlobalForm.ChartPatterns[i].RenderColor == Color.Red))
		{
			return;
		}
		float num = GlobalForm.CalculateCharacterWidth(e);
		bool flag = false;
		decimal priceTarget = GlobalForm.ChartPatterns[i].PriceTarget;
		checked
		{
			if (GlobalForm.ShowUnHit)
			{
				int num2 = GlobalForm.ChartPatterns[i].iEndDate + 1;
				int hLCRange = GlobalForm.HLCRange;
				for (int j = num2; j <= hLCRange; j++)
				{
					if (decimal.Compare(priceTarget, 0m) != 0 && ((decimal.Compare(GlobalForm.nHLC[1, j], priceTarget) >= 0) & (decimal.Compare(GlobalForm.nHLC[2, j], priceTarget) <= 0)))
					{
						flag = true;
						break;
					}
					if (decimal.Compare(GlobalForm.ChartPatterns[i].StopPrice, 0m) != 0 && ((decimal.Compare(GlobalForm.nHLC[1, j], GlobalForm.ChartPatterns[i].StopPrice) >= 0) & (decimal.Compare(GlobalForm.nHLC[2, j], GlobalForm.ChartPatterns[i].StopPrice) <= 0)))
					{
						flag = true;
						break;
					}
				}
			}
			PointF absolutePoint = default(PointF);
			PointF absolutePoint2 = default(PointF);
			if ((GlobalForm.ShowTargetprice & (!GlobalForm.ShowUnHit | unchecked(GlobalForm.ShowUnHit && !flag))) && decimal.Compare(priceTarget, 0m) != 0)
			{
				int num3 = FindCross(priceTarget, iPoint + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
				absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)iPoint);
				absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(priceTarget));
				absolutePoint2.Y = absolutePoint.Y;
				absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				absolutePoint.X += num;
				if (GlobalForm.IncludePhrase)
				{
					e.ChartGraphics.Graphics.DrawString("Target: " + GlobalForm.LimitDecimals(priceTarget), BoldFont, Brushes.Red, absolutePoint);
				}
				absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num3);
				absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
				absolutePoint2.X += num;
				Pen val = new Pen(Color.FromArgb(192, 0, 0), 2f);
				e.ChartGraphics.Graphics.DrawLine(val, absolutePoint, absolutePoint2);
				val.Dispose();
			}
			if ((GlobalForm.ShowStopLoss & (!GlobalForm.ShowUnHit | unchecked(GlobalForm.ShowUnHit && !flag))) && ((decimal.Compare(GlobalForm.ChartPatterns[i].StopPrice, 0m) != 0) & (decimal.Compare(GlobalForm.ChartPatterns[i].StopPrice, 0m) > 0)))
			{
				int num3 = FindCross(GlobalForm.ChartPatterns[i].StopPrice, iPoint + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
				absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)iPoint);
				absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(GlobalForm.ChartPatterns[i].StopPrice));
				absolutePoint2.Y = absolutePoint.Y;
				absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				absolutePoint.X += num;
				absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num3);
				absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
				absolutePoint2.X += num;
				if (GlobalForm.IncludePhrase)
				{
					if (Operators.CompareString(GlobalForm.ChartPatterns[i].StopDate, (string)null, false) == 0)
					{
						e.ChartGraphics.Graphics.DrawString("Stop: " + GlobalForm.ChartPatterns[i].StopPrice, BoldFont, (Brush)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)Brushes.Red, (object)Brushes.Black), absolutePoint);
					}
					else
					{
						e.ChartGraphics.Graphics.DrawString("Stop: " + GlobalForm.ChartPatterns[i].StopPrice + " as of " + GlobalForm.ChartPatterns[i].StopDate, BoldFont, (Brush)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)Brushes.Red, (object)Brushes.Black), absolutePoint);
					}
				}
				Pen val2 = new Pen(Color.FromArgb(192, 0, 192), 2f);
				e.ChartGraphics.Graphics.DrawLine(val2, absolutePoint, absolutePoint2);
				val2.Dispose();
			}
			if (GlobalForm.ShowUltHighLow && ((decimal.Compare(GlobalForm.ChartPatterns[i].UltHLPrice, 0m) != 0) & (decimal.Compare(GlobalForm.ChartPatterns[i].UltHLPrice, 0m) > 0)))
			{
				int num3 = FindCross(GlobalForm.ChartPatterns[i].UltHLPrice, iPoint + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
				absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)iPoint);
				absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(GlobalForm.ChartPatterns[i].UltHLPrice));
				absolutePoint2.Y = absolutePoint.Y;
				absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				absolutePoint.X += num;
				absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num3);
				absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
				absolutePoint2.X += num;
				e.ChartGraphics.Graphics.DrawLine(Pens.Gray, absolutePoint, absolutePoint2);
				if (GlobalForm.IncludePhrase)
				{
					e.ChartGraphics.Graphics.DrawString("Ultimate " + Conversions.ToString(Interaction.IIf(GlobalForm.ChartPatterns[i].UltHiLow, (object)"high", (object)"low")) + " " + GlobalForm.ChartPatterns[i].UltHLPrice + " on " + GlobalForm.ChartPatterns[i].UltHLDate, BoldFont, (Brush)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Red, (object)Brushes.Red, (object)Brushes.Black), absolutePoint);
				}
			}
			decimal num4 = default(decimal);
			if (GlobalForm.ShowConfirmation | GlobalForm.ShowUpTarget | GlobalForm.ShowDownTarget)
			{
				int type = GlobalForm.ChartPatterns[i].Type;
				num4 = GlobalForm.ChartPatterns[i].dBreakoutPrice;
				int num5 = GlobalForm.ChartPatterns[i].iStartDate + 1;
				int num6 = GlobalForm.ChartPatterns[i].iEndDate - 1;
				if (type == 95)
				{
					num6++;
				}
				if (unchecked(type == 106 || type == 105 || type == 104 || type == 103))
				{
					num5 = GlobalForm.ChartPatterns[i].iStartDate;
					num6 = GlobalForm.ChartPatterns[i].iEndDate;
				}
				int num7 = num5;
				int num8 = num5;
				int num9 = num5;
				int num10 = num6;
				for (int k = num9; k <= num10; k++)
				{
					num8 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[2, k], GlobalForm.nHLC[2, num8]) <= 0, (object)k, (object)num8));
					num7 = Conversions.ToInteger(Interaction.IIf(decimal.Compare(GlobalForm.nHLC[1, k], GlobalForm.nHLC[1, num7]) >= 0, (object)k, (object)num7));
				}
				if (GlobalForm.ShowConfirmation)
				{
					int num11 = 0;
					switch (type)
					{
					case 84:
					{
						foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
						{
							if (num11 + GlobalForm.ChartStartIndex >= GlobalForm.ChartPatterns[i].iEndDate)
							{
								absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
								absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num11 + 1));
								absolutePoint2.Y = absolutePoint.Y;
								num4 = new decimal(item.YValues[0]);
								break;
							}
							num11++;
						}
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						absolutePoint.X += num;
						int num3 = FindCross(num4, iPoint + GlobalForm.ChartStartIndex, SpecialCase: true) - GlobalForm.ChartStartIndex;
						absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num3);
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						absolutePoint2.X += num;
						e.ChartGraphics.Graphics.DrawLine(Pens.Blue, absolutePoint, absolutePoint2);
						if (GlobalForm.IncludePhrase)
						{
							e.ChartGraphics.Graphics.DrawString("Confirm", BoldFont, Brushes.Red, absolutePoint);
						}
						break;
					}
					case 83:
					{
						foreach (DataPoint item2 in (Collection<DataPoint>)(object)series.Points)
						{
							if (num11 + GlobalForm.ChartStartIndex >= GlobalForm.ChartPatterns[i].iEndDate)
							{
								absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item2.YValues[1]);
								absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num11 + 1));
								absolutePoint2.Y = absolutePoint.Y;
								num4 = new decimal(item2.YValues[1]);
								break;
							}
							num11++;
						}
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						absolutePoint.X += num;
						int num3 = FindCross(num4, iPoint + GlobalForm.ChartStartIndex, SpecialCase: true) - GlobalForm.ChartStartIndex;
						absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num3);
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						absolutePoint2.X += num;
						e.ChartGraphics.Graphics.DrawLine(Pens.Blue, absolutePoint, absolutePoint2);
						if (GlobalForm.IncludePhrase)
						{
							e.ChartGraphics.Graphics.DrawString("Confirm", BoldFont, Brushes.Red, absolutePoint);
						}
						break;
					}
					case 14:
					case 15:
					case 16:
					case 17:
					case 33:
					case 85:
					case 91:
					case 97:
					case 103:
					case 105:
					case 116:
					{
						foreach (DataPoint item3 in (Collection<DataPoint>)(object)series.Points)
						{
							if (num11 + GlobalForm.ChartStartIndex == num8)
							{
								absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item3.YValues[1]);
								absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num11 + 1));
								absolutePoint2.Y = absolutePoint.Y;
								num4 = new decimal(item3.YValues[1]);
								break;
							}
							num11++;
						}
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						absolutePoint.X += num;
						int num3 = FindCross(num4, iPoint + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
						absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num3);
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						absolutePoint2.X += num;
						e.ChartGraphics.Graphics.DrawLine(Pens.Blue, absolutePoint, absolutePoint2);
						if (GlobalForm.IncludePhrase)
						{
							e.ChartGraphics.Graphics.DrawString("Confirm", BoldFont, Brushes.Red, absolutePoint);
						}
						break;
					}
					case 18:
					case 19:
					case 20:
					case 21:
					case 34:
					case 86:
					case 90:
					case 95:
					case 98:
					case 104:
					case 106:
					case 115:
					{
						foreach (DataPoint item4 in (Collection<DataPoint>)(object)series.Points)
						{
							if (num11 + GlobalForm.ChartStartIndex == num7)
							{
								absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item4.YValues[0]);
								absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num11 + 1));
								num4 = new decimal(item4.YValues[0]);
								absolutePoint2.Y = absolutePoint.Y;
								break;
							}
							num11++;
						}
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						absolutePoint.X += num;
						int num3 = FindCross(num4, iPoint + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
						absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num3);
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						absolutePoint2.X += num;
						e.ChartGraphics.Graphics.DrawLine(Pens.Blue, absolutePoint, absolutePoint2);
						if (GlobalForm.IncludePhrase)
						{
							e.ChartGraphics.Graphics.DrawString("Confirm", BoldFont, Brushes.Red, absolutePoint);
						}
						break;
					}
					case 55:
					{
						decimal num13 = decimal.Subtract(GlobalForm.nHLC[1, GlobalForm.ChartPatterns[i].iMidDate], decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, GlobalForm.ChartPatterns[i].iMidDate], GlobalForm.nHLC[2, num5]), 0.382m));
						foreach (DataPoint item5 in (Collection<DataPoint>)(object)series.Points)
						{
							if ((num11 + GlobalForm.ChartStartIndex > GlobalForm.ChartPatterns[i].iMidDate) & (item5.YValues[1] <= Convert.ToDouble(num13)))
							{
								absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(num13));
								absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num11 + 1));
								absolutePoint2.Y = absolutePoint.Y;
								num4 = num13;
								break;
							}
							num11++;
						}
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						absolutePoint.X += num;
						int num3 = FindCross(num4, iPoint + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
						absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num3);
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						absolutePoint2.X += num;
						e.ChartGraphics.Graphics.DrawLine(Pens.Blue, absolutePoint, absolutePoint2);
						if (GlobalForm.IncludePhrase)
						{
							e.ChartGraphics.Graphics.DrawString("Confirm", BoldFont, Brushes.Red, absolutePoint);
						}
						break;
					}
					case 56:
					{
						decimal num12 = decimal.Add(GlobalForm.nHLC[2, GlobalForm.ChartPatterns[i].iMidDate], decimal.Multiply(decimal.Subtract(GlobalForm.nHLC[1, GlobalForm.ChartPatterns[i].iStartDate], GlobalForm.nHLC[2, GlobalForm.ChartPatterns[i].iMidDate]), 0.382m));
						foreach (DataPoint item6 in (Collection<DataPoint>)(object)series.Points)
						{
							if ((num11 + GlobalForm.ChartStartIndex > GlobalForm.ChartPatterns[i].iMidDate) & (item6.YValues[0] >= Convert.ToDouble(num12)))
							{
								absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(num12));
								absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num11 + 1));
								absolutePoint2.Y = absolutePoint.Y;
								num4 = num12;
								break;
							}
							num11++;
						}
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						absolutePoint.X += num;
						int num3 = FindCross(num4, iPoint + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
						absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num3);
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						absolutePoint2.X += num;
						e.ChartGraphics.Graphics.DrawLine(Pens.Blue, absolutePoint, absolutePoint2);
						if (GlobalForm.IncludePhrase)
						{
							e.ChartGraphics.Graphics.DrawString("Confirm", BoldFont, Brushes.Red, absolutePoint);
						}
						break;
					}
					}
				}
			}
			if (GlobalForm.ShowUpTarget && Convert.ToDouble(num4) * (1.0 + 0.01 * (double)GlobalForm.ShowUpPercentage) > 0.0)
			{
				int num3 = FindCross(new decimal(Convert.ToDouble(num4) * (1.0 + 0.01 * (double)GlobalForm.ShowUpPercentage)), iPoint + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
				absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)iPoint);
				absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(num4) * (1.0 + 0.01 * (double)GlobalForm.ShowUpPercentage));
				absolutePoint2.Y = absolutePoint.Y;
				absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				absolutePoint.X += num;
				absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num3);
				absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
				absolutePoint2.X += num;
				e.ChartGraphics.Graphics.DrawLine(Pens.Green, absolutePoint, absolutePoint2);
				if (GlobalForm.IncludePhrase)
				{
					e.ChartGraphics.Graphics.DrawString(GlobalForm.ShowUpPercentage + "% Up", BoldFont, Brushes.Red, absolutePoint);
				}
			}
			if (GlobalForm.ShowDownTarget && Convert.ToDouble(num4) * (1.0 - 0.01 * (double)GlobalForm.ShowDownPercentage) > 0.0)
			{
				int num3 = FindCross(new decimal(Convert.ToDouble(num4) * (1.0 - 0.01 * (double)GlobalForm.ShowDownPercentage)), iPoint + GlobalForm.ChartStartIndex, SpecialCase: false) - GlobalForm.ChartStartIndex;
				absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)iPoint);
				absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, Convert.ToDouble(num4) * (1.0 - 0.01 * (double)GlobalForm.ShowDownPercentage));
				absolutePoint2.Y = absolutePoint.Y;
				absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
				absolutePoint.X += num;
				absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num3);
				absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
				absolutePoint2.X += num;
				e.ChartGraphics.Graphics.DrawLine(Pens.Green, absolutePoint, absolutePoint2);
				if (GlobalForm.IncludePhrase)
				{
					e.ChartGraphics.Graphics.DrawString(GlobalForm.ShowDownPercentage + "% Down", BoldFont, Brushes.Red, absolutePoint);
				}
			}
		}
	}

	private static void ShowTripleBottoms(ChartPaintEventArgs e, Series series, int i)
	{
		int num = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					DrawTextBelow(e, item, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
				{
					DrawTextBelow(e, item, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					DrawTextBelow(e, item, num, i);
					ShowTarget(e, series, i, num);
					break;
				}
				num++;
			}
		}
	}

	private static void ShowTripleTops(ChartPaintEventArgs e, Series series, int i)
	{
		int num = 0;
		checked
		{
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					DrawTextAbove(e, item, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
				{
					DrawTextAbove(e, item, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					DrawTextAbove(e, item, num, i);
					ShowTarget(e, series, i, num);
					break;
				}
				num++;
			}
		}
	}

	private static void ShowVTop(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_01d1: Unknown result type (might be due to invalid IL or missing references)
		//IL_01dd: Expected O, but got Unknown
		//IL_0211: Unknown result type (might be due to invalid IL or missing references)
		//IL_021d: Expected O, but got Unknown
		int num = 0;
		PointF absolutePoint = default(PointF);
		absolutePoint.X = -1f;
		checked
		{
			PointF absolutePoint2 = default(PointF);
			PointF absolutePoint3 = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
				{
					absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
					DrawTextAbove(e, item, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					ShowTarget(e, series, i, num);
					break;
				}
				num++;
			}
			if (absolutePoint.X != -1f)
			{
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint3);
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint3, absolutePoint);
			}
		}
	}

	private static void ShowVBottom(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_01d1: Unknown result type (might be due to invalid IL or missing references)
		//IL_01dd: Expected O, but got Unknown
		//IL_0211: Unknown result type (might be due to invalid IL or missing references)
		//IL_021d: Expected O, but got Unknown
		int num = 0;
		PointF absolutePoint = default(PointF);
		absolutePoint.X = -1f;
		checked
		{
			PointF absolutePoint2 = default(PointF);
			PointF absolutePoint3 = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
				{
					absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
					absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
					DrawTextBelow(e, item, num, i);
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					ShowTarget(e, series, i, num);
					break;
				}
				num++;
			}
			if (absolutePoint.X != -1f)
			{
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint3);
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint3, absolutePoint);
			}
		}
	}

	public static void ShowVerticals(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_01c3: Unknown result type (might be due to invalid IL or missing references)
		//IL_01cf: Expected O, but got Unknown
		int num = 0;
		int type = GlobalForm.ChartPatterns[i].Type;
		PointF pointF = default(PointF);
		checked
		{
			PointF absolutePoint = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
				{
					absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[Conversions.ToInteger(Interaction.IIf(type == 24, (object)0, (object)1))]);
					absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
					if (type == 24)
					{
						DrawTextAbove(e, item, num, i);
					}
					else
					{
						DrawTextBelow(e, item, num, i);
					}
				}
				if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
				{
					pointF.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[Conversions.ToInteger(Interaction.IIf(type == 24, (object)1, (object)0))]);
					pointF.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
					pointF = e.ChartGraphics.GetAbsolutePoint(pointF);
					ShowTarget(e, series, i, num);
					break;
				}
				num++;
			}
			if (pointF != default(PointF))
			{
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, pointF);
			}
		}
	}

	private static void ShowWolfeBull(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_0733: Unknown result type (might be due to invalid IL or missing references)
		//IL_0740: Expected O, but got Unknown
		//IL_07ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_07ba: Expected O, but got Unknown
		//IL_0574: Unknown result type (might be due to invalid IL or missing references)
		//IL_0581: Expected O, but got Unknown
		//IL_05b5: Unknown result type (might be due to invalid IL or missing references)
		//IL_05c2: Expected O, but got Unknown
		//IL_088f: Unknown result type (might be due to invalid IL or missing references)
		//IL_089c: Expected O, but got Unknown
		//IL_0697: Unknown result type (might be due to invalid IL or missing references)
		//IL_06a4: Expected O, but got Unknown
		checked
		{
			if (((Collection<DataPoint>)(object)series.Points).Count + GlobalForm.ChartStartIndex < GlobalForm.ChartPatterns[i].iStartDate || GlobalForm.ChartPatterns[i].iEndDate > ((Collection<DataPoint>)(object)series.Points).Count + GlobalForm.ChartStartIndex)
			{
				return;
			}
			ShowNR47(e, series, i);
			int num = 0;
			PointF absolutePoint = default(PointF);
			int num2 = default(int);
			PointF absolutePoint2 = default(PointF);
			int num3 = default(int);
			PointF absolutePoint3 = default(PointF);
			int num4 = default(int);
			PointF absolutePoint4 = default(PointF);
			decimal d = default(decimal);
			decimal num6 = default(decimal);
			decimal d2 = default(decimal);
			decimal d3 = default(decimal);
			decimal d4 = default(decimal);
			decimal d5 = default(decimal);
			int num7 = default(int);
			bool flag = default(bool);
			bool flag2 = default(bool);
			PointF absolutePoint5 = default(PointF);
			decimal num8 = default(decimal);
			decimal num9 = default(decimal);
			PointF absolutePoint6 = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (GlobalForm.ChartPatterns[i].RenderColor == Color.Red)
				{
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
					{
						absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
						GlobalForm.ChartPatterns[i].iText = "1";
						DrawTextBelow(e, item, num, i);
						absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						num2 = num + 1;
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
					{
						absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
						GlobalForm.ChartPatterns[i].iText = "2";
						DrawTextAbove(e, item, num, i);
						absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						num3 = num + 1;
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
					{
						absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
						GlobalForm.ChartPatterns[i].iText = "3";
						DrawTextBelow(e, item, num, i);
						absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
						num4 = num;
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date)
					{
						absolutePoint4.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
						GlobalForm.ChartPatterns[i].iText = "4";
						DrawTextAbove(e, item, num, i);
						absolutePoint4.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint4 = e.ChartGraphics.GetAbsolutePoint(absolutePoint4);
						int num5 = num + 1;
						if ((absolutePoint4.X - absolutePoint2.X == 0f) | (absolutePoint3.X - absolutePoint.X == 0f) | (num5 - num3 == 0) | (num4 - num2 == 0))
						{
							return;
						}
						d = new decimal((absolutePoint4.Y - absolutePoint2.Y) / (absolutePoint4.X - absolutePoint2.X));
						num6 = new decimal((absolutePoint3.Y - absolutePoint.Y) / (absolutePoint3.X - absolutePoint.X));
						d2 = new decimal(absolutePoint2.Y);
						d3 = new decimal(absolutePoint.Y);
						d4 = new decimal((absolutePoint4.X - absolutePoint2.X) / (float)(num5 - num3));
						d5 = new decimal((absolutePoint3.X - absolutePoint.X) / (float)(num4 - num2));
						num7 = 0;
						flag = false;
						flag2 = false;
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
					{
						absolutePoint5.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint5.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
						absolutePoint5 = e.ChartGraphics.GetAbsolutePoint(absolutePoint5);
						GlobalForm.ChartPatterns[i].iText = "5";
						DrawTextBelow(e, item, num, i);
						flag = true;
					}
					if (unchecked(checked(num + GlobalForm.ChartStartIndex) > GlobalForm.ChartPatterns[i].iEnd2Date && !flag2))
					{
						num8 = decimal.Add(decimal.Multiply(decimal.Multiply(d, new decimal(num - num3)), d4), d2);
						num9 = decimal.Add(decimal.Multiply(decimal.Multiply(num6, new decimal(num - num2)), d5), d3);
						if (decimal.Compare(d, num6) > 0 && decimal.Compare(num8, num9) >= 0)
						{
							flag2 = true;
							num7 = num;
							absolutePoint6.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num);
							absolutePoint6.Y = 0f;
							absolutePoint6 = e.ChartGraphics.GetAbsolutePoint(absolutePoint6);
							absolutePoint6.Y = Convert.ToSingle(num8);
							if (flag)
							{
								break;
							}
						}
					}
				}
				num++;
			}
			if (num7 != 0)
			{
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint6);
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint6);
				if (GlobalForm.PatternTargets && absolutePoint4.X - absolutePoint.X != 0f)
				{
					decimal d6 = decimal.Multiply(-1m, new decimal((absolutePoint4.Y - absolutePoint.Y) / (absolutePoint4.X - absolutePoint.X)));
					decimal d7 = new decimal(absolutePoint.Y);
					decimal d8 = new decimal(absolutePoint.X - absolutePoint6.X);
					PointF pointF = default(PointF);
					pointF.Y = Convert.ToSingle(decimal.Add(decimal.Multiply(d6, d8), d7));
					pointF.X = absolutePoint6.X;
					e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, pointF);
					e.ChartGraphics.Graphics.DrawString("Target", drawFont, Brushes.Red, pointF);
				}
				return;
			}
			absolutePoint6.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num);
			absolutePoint6 = e.ChartGraphics.GetAbsolutePoint(absolutePoint6);
			absolutePoint6.Y = Convert.ToSingle(num8);
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint6);
			absolutePoint6.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num);
			absolutePoint6 = e.ChartGraphics.GetAbsolutePoint(absolutePoint6);
			absolutePoint6.Y = Convert.ToSingle(num9);
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint6);
			if (GlobalForm.PatternTargets && absolutePoint4.X - absolutePoint.X != 0f)
			{
				decimal d9 = decimal.Multiply(-1m, new decimal((absolutePoint4.Y - absolutePoint.Y) / (absolutePoint4.X - absolutePoint.X)));
				decimal d10 = new decimal(absolutePoint.Y);
				decimal d11 = new decimal(absolutePoint.X - absolutePoint6.X);
				PointF pointF2 = default(PointF);
				pointF2.Y = Convert.ToSingle(decimal.Add(decimal.Multiply(d9, d11), d10));
				pointF2.X = absolutePoint6.X;
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, pointF2);
			}
		}
	}

	private static void ShowWolfeBear(ChartPaintEventArgs e, Series series, int i)
	{
		//IL_0729: Unknown result type (might be due to invalid IL or missing references)
		//IL_0736: Expected O, but got Unknown
		//IL_07a3: Unknown result type (might be due to invalid IL or missing references)
		//IL_07b0: Expected O, but got Unknown
		//IL_056a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0577: Expected O, but got Unknown
		//IL_05ab: Unknown result type (might be due to invalid IL or missing references)
		//IL_05b8: Expected O, but got Unknown
		//IL_0885: Unknown result type (might be due to invalid IL or missing references)
		//IL_0892: Expected O, but got Unknown
		//IL_068d: Unknown result type (might be due to invalid IL or missing references)
		//IL_069a: Expected O, but got Unknown
		checked
		{
			if (((Collection<DataPoint>)(object)series.Points).Count + GlobalForm.ChartStartIndex < GlobalForm.ChartPatterns[i].iStartDate || GlobalForm.ChartPatterns[i].iEndDate > ((Collection<DataPoint>)(object)series.Points).Count + GlobalForm.ChartStartIndex)
			{
				return;
			}
			ShowNR47(e, series, i);
			int num = 0;
			PointF absolutePoint = default(PointF);
			int num2 = default(int);
			PointF absolutePoint2 = default(PointF);
			int num3 = default(int);
			PointF absolutePoint3 = default(PointF);
			int num4 = default(int);
			PointF absolutePoint4 = default(PointF);
			decimal d = default(decimal);
			decimal d2 = default(decimal);
			decimal d3 = default(decimal);
			decimal d4 = default(decimal);
			decimal d5 = default(decimal);
			decimal d6 = default(decimal);
			int num6 = default(int);
			bool flag = default(bool);
			bool flag2 = default(bool);
			PointF absolutePoint5 = default(PointF);
			decimal num7 = default(decimal);
			decimal num8 = default(decimal);
			PointF absolutePoint6 = default(PointF);
			foreach (DataPoint item in (Collection<DataPoint>)(object)series.Points)
			{
				if (GlobalForm.ChartPatterns[i].RenderColor == Color.Red)
				{
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStartDate)
					{
						absolutePoint.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
						GlobalForm.ChartPatterns[i].iText = "1";
						DrawTextAbove(e, item, num, i);
						absolutePoint.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint = e.ChartGraphics.GetAbsolutePoint(absolutePoint);
						num2 = num + 1;
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iStart2Date)
					{
						absolutePoint2.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
						GlobalForm.ChartPatterns[i].iText = "2";
						DrawTextBelow(e, item, num, i);
						absolutePoint2.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint2 = e.ChartGraphics.GetAbsolutePoint(absolutePoint2);
						num3 = num + 1;
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iMidDate)
					{
						absolutePoint3.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
						GlobalForm.ChartPatterns[i].iText = "3";
						DrawTextAbove(e, item, num, i);
						absolutePoint3.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint3 = e.ChartGraphics.GetAbsolutePoint(absolutePoint3);
						num4 = num + 1;
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEnd2Date)
					{
						absolutePoint4.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[1]);
						GlobalForm.ChartPatterns[i].iText = "4";
						DrawTextBelow(e, item, num, i);
						absolutePoint4.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint4 = e.ChartGraphics.GetAbsolutePoint(absolutePoint4);
						int num5 = num + 1;
						if ((absolutePoint4.X - absolutePoint2.X == 0f) | (absolutePoint3.X - absolutePoint.X == 0f) | (num5 - num3 == 0) | (num4 - num2 == 0))
						{
							return;
						}
						d = new decimal((absolutePoint4.Y - absolutePoint2.Y) / (absolutePoint4.X - absolutePoint2.X));
						d2 = new decimal((absolutePoint3.Y - absolutePoint.Y) / (absolutePoint3.X - absolutePoint.X));
						d3 = new decimal(absolutePoint.Y);
						d4 = new decimal(absolutePoint2.Y);
						d5 = new decimal((absolutePoint4.X - absolutePoint2.X) / (float)(num5 - num3));
						d6 = new decimal((absolutePoint3.X - absolutePoint.X) / (float)(num4 - num2));
						num6 = 0;
						flag = false;
						flag2 = false;
					}
					if (num + GlobalForm.ChartStartIndex == GlobalForm.ChartPatterns[i].iEndDate)
					{
						absolutePoint5.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)(num + 1));
						absolutePoint5.Y = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)3, item.YValues[0]);
						absolutePoint5 = e.ChartGraphics.GetAbsolutePoint(absolutePoint5);
						GlobalForm.ChartPatterns[i].iText = "5";
						DrawTextAbove(e, item, num, i);
						flag = true;
					}
					if (unchecked(checked(num + GlobalForm.ChartStartIndex) > GlobalForm.ChartPatterns[i].iEnd2Date && !flag2))
					{
						num7 = decimal.Add(decimal.Multiply(decimal.Multiply(d, new decimal(num - num3)), d5), d4);
						num8 = decimal.Add(decimal.Multiply(decimal.Multiply(d2, new decimal(num - num2)), d6), d3);
						if (decimal.Compare(num8, num7) > 0)
						{
							flag2 = true;
							num6 = num;
							absolutePoint6.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num);
							absolutePoint6.Y = 0f;
							absolutePoint6 = e.ChartGraphics.GetAbsolutePoint(absolutePoint6);
							absolutePoint6.Y = Convert.ToSingle(num7);
							if (flag)
							{
								break;
							}
						}
					}
				}
				num++;
			}
			if (num6 != 0)
			{
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint6);
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint6);
				if (GlobalForm.PatternTargets && absolutePoint4.X - absolutePoint.X != 0f)
				{
					decimal d7 = decimal.Multiply(-1m, new decimal((absolutePoint4.Y - absolutePoint.Y) / (absolutePoint4.X - absolutePoint.X)));
					decimal d8 = new decimal(absolutePoint.Y);
					decimal d9 = new decimal(absolutePoint.X - absolutePoint6.X);
					PointF pointF = default(PointF);
					pointF.Y = Convert.ToSingle(decimal.Add(decimal.Multiply(d7, d9), d8));
					pointF.X = absolutePoint6.X;
					e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, pointF);
					e.ChartGraphics.Graphics.DrawString("Target", drawFont, Brushes.Red, pointF);
				}
				return;
			}
			absolutePoint6.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num);
			absolutePoint6 = e.ChartGraphics.GetAbsolutePoint(absolutePoint6);
			absolutePoint6.Y = Convert.ToSingle(num7);
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint2, absolutePoint6);
			absolutePoint6.X = (float)e.ChartGraphics.GetPositionFromAxis("ChartArea1", (AxisName)0, (double)num);
			absolutePoint6 = e.ChartGraphics.GetAbsolutePoint(absolutePoint6);
			absolutePoint6.Y = Convert.ToSingle(num8);
			e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, absolutePoint6);
			if (GlobalForm.PatternTargets && absolutePoint4.X - absolutePoint.X != 0f)
			{
				decimal d10 = decimal.Multiply(-1m, new decimal((absolutePoint4.Y - absolutePoint.Y) / (absolutePoint4.X - absolutePoint.X)));
				decimal d11 = new decimal(absolutePoint.Y);
				decimal d12 = new decimal(absolutePoint.X - absolutePoint6.X);
				PointF pointF2 = default(PointF);
				pointF2.Y = Convert.ToSingle(decimal.Add(decimal.Multiply(d10, d12), d11));
				pointF2.X = absolutePoint6.X;
				e.ChartGraphics.Graphics.DrawLine((Pen)Interaction.IIf(GlobalForm.ChartPatterns[i].RenderColor == Color.Black, (object)Pens.Black, (object)Pens.Red), absolutePoint, pointF2);
			}
		}
	}
}
