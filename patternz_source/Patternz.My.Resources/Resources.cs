using System.CodeDom.Compiler;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Globalization;
using System.Resources;
using System.Runtime.CompilerServices;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz.My.Resources;

[StandardModule]
[GeneratedCode("System.Resources.Tools.StronglyTypedResourceBuilder", "17.0.0.0")]
[DebuggerNonUserCode]
[CompilerGenerated]
[HideModuleName]
internal sealed class Resources
{
	private static ResourceManager resourceMan;

	private static CultureInfo resourceCulture;

	[EditorBrowsable(EditorBrowsableState.Advanced)]
	internal static ResourceManager ResourceManager
	{
		get
		{
			if (object.ReferenceEquals(resourceMan, null))
			{
				resourceMan = new ResourceManager("Patternz.Resources", typeof(Resources).Assembly);
			}
			return resourceMan;
		}
	}

	[EditorBrowsable(EditorBrowsableState.Advanced)]
	internal static CultureInfo Culture
	{
		get
		{
			return resourceCulture;
		}
		set
		{
			resourceCulture = value;
		}
	}

	internal static Bitmap PZBestTrade => (Bitmap)RuntimeHelpers.GetObjectValue(ResourceManager.GetObject("PZBestTrade", resourceCulture));

	internal static Bitmap PZBestTrade1 => (Bitmap)RuntimeHelpers.GetObjectValue(ResourceManager.GetObject("PZBestTrade1", resourceCulture));

	internal static Bitmap PZForecast => (Bitmap)RuntimeHelpers.GetObjectValue(ResourceManager.GetObject("PZForecast", resourceCulture));

	internal static Bitmap ZoomIconM => (Bitmap)RuntimeHelpers.GetObjectValue(ResourceManager.GetObject("ZoomIconM", resourceCulture));

	internal static Bitmap ZoomIconP => (Bitmap)RuntimeHelpers.GetObjectValue(ResourceManager.GetObject("ZoomIconP", resourceCulture));
}
