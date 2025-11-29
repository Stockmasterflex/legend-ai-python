using System;
using System.IO;
using System.Net;
using System.Text.RegularExpressions;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz;

public class Token
{
	private static Regex regex_crumb;

	public static string Cookie { get; set; } = "";

	public static string Crumb { get; set; } = "";

	public static bool Refresh(string symbol = "SPY")
	{
		ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
		try
		{
			Cookie = "";
			Crumb = "";
			HttpWebRequest obj = (HttpWebRequest)WebRequest.Create(string.Format("https://finance.yahoo.com/quote/{0}?p={0}", symbol));
			obj.CookieContainer = new CookieContainer();
			obj.Method = "GET";
			using HttpWebResponse httpWebResponse = (HttpWebResponse)obj.GetResponse();
			string cookie = httpWebResponse.GetResponseHeader("Set-Cookie").Split(Conversions.ToCharArrayRankOne(";"))[0];
			string text = "";
			using (Stream stream = httpWebResponse.GetResponseStream())
			{
				text = new StreamReader(stream).ReadToEnd();
			}
			if (text.Length < 5000)
			{
				return false;
			}
			string crumb = getCrumb(text);
			text = "";
			if (crumb != null)
			{
				Cookie = cookie;
				Crumb = crumb;
				return true;
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			Cookie = "-1";
			Crumb = "-1";
			ProjectData.ClearProjectError();
		}
		return false;
	}

	private static string getCrumb(string html)
	{
		string result = null;
		try
		{
			if (regex_crumb == null)
			{
				regex_crumb = new Regex("CrumbStore\":{\"crumb\":\"(?<crumb>.+?)\"}", RegexOptions.Compiled | RegexOptions.CultureInvariant);
			}
			MatchCollection matchCollection = regex_crumb.Matches(html);
			if (matchCollection.Count > 0)
			{
				result = matchCollection[0].Groups["crumb"].Value;
			}
			matchCollection = null;
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			ProjectData.ClearProjectError();
		}
		GC.Collect();
		return result;
	}
}
