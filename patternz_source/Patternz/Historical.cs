using System;
using System.Collections.Generic;
using System.Net;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz;

public class Historical
{
	public static List<HistoryPrice> Get(string symbol, DateTime start, DateTime end)
	{
		List<HistoryPrice> result = new List<HistoryPrice>();
		try
		{
			string raw = GetRaw(symbol, start, end);
			if (raw != null)
			{
				result = Parse(raw);
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		return result;
	}

	public static string GetRaw(string symbol, DateTime start, DateTime end)
	{
		string text = null;
		string result;
		try
		{
			string format = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history&crumb={3}";
			if (((Operators.CompareString(Token.Cookie, "", false) == 0) & (Operators.CompareString(Token.Crumb, "", false) == 0)) && !Token.Refresh(symbol))
			{
				if (((Operators.CompareString(Token.Cookie, "", false) == 0) & (Operators.CompareString(Token.Crumb, "", false) == 0)) | ((Operators.CompareString(Token.Cookie, "-1", false) == 0) & (Operators.CompareString(Token.Crumb, "-1", false) == 0)))
				{
					result = null;
				}
				else if (!GlobalForm.Recursive)
				{
					GlobalForm.Recursive = true;
					text = GetRaw(symbol, start, end);
					GlobalForm.Recursive = false;
					result = text;
				}
				else
				{
					GlobalForm.Recursive = false;
					result = null;
				}
				goto IL_01ab;
			}
			format = string.Format(format, symbol, Math.Round(DateTimeToUnixTimestamp(start), 0), Math.Round(DateTimeToUnixTimestamp(end), 0), Token.Crumb);
			using WebClient webClient = new WebClient();
			webClient.Headers.Add(HttpRequestHeader.Cookie, Token.Cookie);
			text = webClient.DownloadString(format);
		}
		catch (WebException ex)
		{
			ProjectData.SetProjectError((Exception)ex);
			WebException ex2 = ex;
			HttpWebResponse httpWebResponse = (HttpWebResponse)ex2.Response;
			if (!GlobalForm.Recursive)
			{
				GlobalForm.Recursive = true;
				if (httpWebResponse.StatusCode == HttpStatusCode.Unauthorized)
				{
					Token.Cookie = "";
					Token.Crumb = "";
					result = GetRaw(symbol, start, end);
					ProjectData.ClearProjectError();
					goto IL_01ab;
				}
			}
			GlobalForm.Recursive = false;
			result = text;
			ProjectData.ClearProjectError();
			goto IL_01ab;
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			ProjectData.ClearProjectError();
		}
		result = text;
		goto IL_01ab;
		IL_01ab:
		return result;
	}

	private static List<HistoryPrice> Parse(string csvData)
	{
		List<HistoryPrice> list = new List<HistoryPrice>();
		checked
		{
			try
			{
				string[] array = csvData.Split(new char[1] { Convert.ToChar(10) });
				int num = array.Length - 1;
				for (int i = 1; i <= num; i++)
				{
					string text = array[i];
					if (string.IsNullOrEmpty(text))
					{
						continue;
					}
					string[] array2 = text.Split(Conversions.ToCharArrayRankOne(","));
					if (Operators.CompareString(array2[1], "null", false) != 0)
					{
						HistoryPrice historyPrice = new HistoryPrice();
						HistoryPrice historyPrice2 = historyPrice;
						historyPrice2.Date = DateTime.Parse(array2[0]);
						historyPrice2.Open = Convert.ToDouble(array2[1]);
						historyPrice2.High = Convert.ToDouble(array2[2]);
						historyPrice2.Low = Convert.ToDouble(array2[3]);
						historyPrice2.Close = Convert.ToDouble(array2[4]);
						historyPrice2.AdjClose = Convert.ToDouble(array2[5]);
						if (Operators.CompareString(array2[6], "null", false) != 0)
						{
							historyPrice2.Volume = Convert.ToDouble(array2[6]);
						}
						historyPrice2 = null;
						list.Add(historyPrice);
					}
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				ProjectData.ClearProjectError();
			}
			return list;
		}
	}

	public static DateTime UnixTimestampToDateTime(double unixTimeStamp)
	{
		return new DateTime(1970, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc).AddSeconds(unixTimeStamp);
	}

	public static double DateTimeToUnixTimestamp(DateTime dateTime)
	{
		return (dateTime.ToUniversalTime() - new DateTime(1970, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc)).TotalSeconds;
	}
}
