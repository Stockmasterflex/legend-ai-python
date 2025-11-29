using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz;

[DesignerGenerated]
public class HelpScoreForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

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

	[field: AccessedThroughProperty("Label1")]
	internal virtual Label Label1
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

	[field: AccessedThroughProperty("Label3")]
	internal virtual Label Label3
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
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

	[field: AccessedThroughProperty("Label7")]
	internal virtual Label Label7
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

	[field: AccessedThroughProperty("Label9")]
	internal virtual Label Label9
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label4")]
	internal virtual Label Label4
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label10")]
	internal virtual Label Label10
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label11")]
	internal virtual Label Label11
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public HelpScoreForm()
	{
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
		//IL_03b3: Unknown result type (might be due to invalid IL or missing references)
		//IL_03bd: Expected O, but got Unknown
		//IL_0489: Unknown result type (might be due to invalid IL or missing references)
		//IL_0493: Expected O, but got Unknown
		//IL_04fe: Unknown result type (might be due to invalid IL or missing references)
		//IL_0508: Expected O, but got Unknown
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(HelpScoreForm));
		DoneButton = new Button();
		Label1 = new Label();
		Label2 = new Label();
		Label3 = new Label();
		Label5 = new Label();
		Label6 = new Label();
		Label7 = new Label();
		Label8 = new Label();
		Label9 = new Label();
		Label4 = new Label();
		Label10 = new Label();
		Label11 = new Label();
		((Control)this).SuspendLayout();
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(684, 434);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(60, 23);
		((Control)DoneButton).TabIndex = 22;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)Label1).Location = new Point(42, 126);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(702, 47);
		((Control)Label1).TabIndex = 23;
		Label1.Text = componentResourceManager.GetString("Label1.Text");
		((Control)Label2).Location = new Point(44, 336);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(615, 27);
		((Control)Label2).TabIndex = 24;
		Label2.Text = "Not all chart patterns are scored. The following chart patterns with upward breakouts are scored: ";
		((Control)Label3).Location = new Point(88, 363);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(571, 29);
		((Control)Label3).TabIndex = 25;
		Label3.Text = "Big W, double bottom,  head-and-shoulders bottom,  complex head-and-shoulders bottom,  rectangle (top and bottom), ascending triangle, and triple bottom.";
		((Control)Label5).Location = new Point(91, 434);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(568, 29);
		((Control)Label5).TabIndex = 28;
		Label5.Text = "Big M, double top, head-and-shoulders top, complex head-and-shoulders top,  rectangle (top and bottom), descending triangle, and triple top.";
		((Control)Label6).Location = new Point(44, 407);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(615, 27);
		((Control)Label6).TabIndex = 27;
		Label6.Text = "The following chart patterns with downward breakouts are scored: ";
		((Control)Label7).Location = new Point(42, 217);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(699, 34);
		((Control)Label7).TabIndex = 29;
		Label7.Text = "After scoring, highlight rows you wish to copy to the clipboard, and then click Clipboard. Pasting to the clipboard may take several minutes.";
		((Control)Label8).Location = new Point(42, 251);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(699, 47);
		((Control)Label8).TabIndex = 30;
		Label8.Text = componentResourceManager.GetString("Label8.Text");
		((Control)Label9).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label9).Location = new Point(12, 19);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(732, 77);
		((Control)Label9).TabIndex = 31;
		Label9.Text = componentResourceManager.GetString("Label9.Text");
		((Control)Label4).Location = new Point(42, 173);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(699, 34);
		((Control)Label4).TabIndex = 32;
		Label4.Text = "If you wish to score a stock not highlighted on the Main Form, enter the symbol in the \"Symbol\" text box. The file MUST exist in the portfolio otherwise it won't be scored and an error may occur.";
		((Control)Label10).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label10).Location = new Point(12, 110);
		((Control)Label10).Name = "Label10";
		((Control)Label10).Size = new Size(732, 16);
		((Control)Label10).TabIndex = 33;
		Label10.Text = "USE:";
		((Control)Label11).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label11).Location = new Point(12, 310);
		((Control)Label11).Name = "Label11";
		((Control)Label11).Size = new Size(732, 16);
		((Control)Label11).TabIndex = 34;
		Label11.Text = "PATTERNS SCORED:";
		((Form)this).AcceptButton = (IButtonControl)(object)DoneButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(756, 472);
		((Control)this).Controls.Add((Control)(object)Label11);
		((Control)this).Controls.Add((Control)(object)Label10);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)Label9);
		((Control)this).Controls.Add((Control)(object)Label8);
		((Control)this).Controls.Add((Control)(object)Label7);
		((Control)this).Controls.Add((Control)(object)Label5);
		((Control)this).Controls.Add((Control)(object)Label6);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Control)this).Name = "HelpScoreForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Help Score Form";
		((Control)this).ResumeLayout(false);
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}
}
